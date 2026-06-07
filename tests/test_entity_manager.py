from __future__ import annotations

import unittest

from _test_env import bootstrap_pygame, shutdown_pygame

from guigine.components.base import Position, Velocity
from guigine.ecs.core import Entity
from guigine.ecs.entity_manager import EntityManager


class EntityManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        self.manager = EntityManager()

    def test_create_adds_entity_and_components(self) -> None:
        entity = self.manager.create(Position(10, 20), Velocity(1, 2))
        self.assertIs(self.manager.get_entity_by_id(entity.id), entity)
        self.assertEqual(entity.get(Position).xy, (10, 20))
        self.assertEqual(entity.get(Velocity).vxy, (1.0, 2.0))

    def test_add_entity_accepts_existing_entity(self) -> None:
        entity = Entity()
        self.manager.add_entity(entity, Position(5, 7))
        self.assertIn(entity, self.manager.get_entities())
        self.assertTrue(entity.has(Position))

    def test_get_entities_with_can_filter(self) -> None:
        first = self.manager.create(Position(10, 0), Velocity())
        self.manager.create(Position(40, 0), Velocity())
        self.manager.create(Position(100, 0))
        result = self.manager.get_entities_with(
            Position,
            Velocity,
            filter_fn=lambda entity: entity.get(Position).x < 20,
        )
        self.assertEqual([entity.id for entity in result], [first.id])

    def test_remove_and_clear_drop_entities(self) -> None:
        entity = self.manager.create(Position())
        self.manager.remove_entity(entity)
        self.assertIsNone(self.manager.get_entity_by_id(entity.id))
        self.manager.create(Position())
        self.manager.clear()
        self.assertEqual(self.manager.get_entities(), [])
