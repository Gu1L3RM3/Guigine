from __future__ import annotations

import unittest

import pygame

from _test_env import bootstrap_pygame, shutdown_pygame

from guigine.components.base import Freeze, Position, Velocity
from guigine.components.collider import Collider
from guigine.components.dynamic_collision import DynamicCollision
from guigine.ecs.entity_manager import EntityManager
from guigine.systems.physics import PhysicsSystem


class PhysicsSystemTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        self.manager = EntityManager()
        self.physics = PhysicsSystem()

    def test_moves_entity_without_collider(self) -> None:
        entity = self.manager.create(Position(0, 0), Velocity(10, 5))
        self.physics.update(self.manager, 0.5)
        self.assertEqual(entity.get(Position).xy, (5.0, 2.5))

    def test_freeze_blocks_movement(self) -> None:
        entity = self.manager.create(Position(0, 0), Velocity(10, 0), Freeze(True))
        self.physics.update(self.manager, 1.0)
        self.assertEqual(entity.get(Position).xy, (0.0, 0.0))

    def test_static_collision_stops_entity(self) -> None:
        entity = self.manager.create(Position(0, 0), Velocity(20, 0), Collider(10, 10))
        self.physics.set_external_static_colliders([pygame.Rect(15, 0, 10, 10)])
        self.physics.cache_static_colliders(self.manager)
        self.physics.update(self.manager, 1.0)
        self.assertEqual(entity.get(Position).x, 5)
        self.assertEqual(entity.get(Velocity).vx, 0)

    def test_dynamic_collision_stops_entities(self) -> None:
        mover = self.manager.create(Position(0, 0), Velocity(20, 0), Collider(10, 10))
        blocker = self.manager.create(Position(15, 0), Velocity(0, 0), Collider(10, 10))
        self.physics.update(self.manager, 1.0)
        self.assertEqual(mover.get(Position).x, 5)
        self.assertEqual(mover.get(Velocity).vx, 0)
        self.assertEqual(blocker.get(Position).x, 15)

    def test_dynamic_collision_can_be_disabled(self) -> None:
        mover = self.manager.create(Position(0, 0), Velocity(20, 0), Collider(10, 10), DynamicCollision(False))
        blocker = self.manager.create(Position(15, 0), Velocity(0, 0), Collider(10, 10))
        self.physics.update(self.manager, 1.0)
        self.assertEqual(mover.get(Position).x, 20)
        self.assertEqual(blocker.get(Position).x, 15)
