from __future__ import annotations

import unittest

from _test_env import ASSET_ROOT, bootstrap_pygame, shutdown_pygame

from guigine.components.base import Position
from guigine.components.collider import Collider
from guigine.ecs.core import Entity
from guigine.ecs.entity_manager import EntityManager
from guigine.map.map_entity_spawner import MapEntitySpawner
from guigine.map.tile_map_loader import TileMapLoader
from guigine.resources.resource_manager import ResourceManager


class MapEntitySpawnerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        resources = ResourceManager(ASSET_ROOT)
        self.tilemap = TileMapLoader(resources).load("demo/demo_map.tmx")
        self.entity_manager = EntityManager()

    def test_spawns_tile_layer_entities_and_object_layer_entities(self) -> None:
        seen_names: list[str] = []

        def factory(obj, entity_manager, tilemap):
            _ = entity_manager
            _ = tilemap
            seen_names.append(obj.name)
            entity = Entity()
            entity.add(Position(obj.x, obj.y), Collider(int(obj.width), int(obj.height)))
            return entity

        spawner = MapEntitySpawner(spawn_tile_layer_entities=True)
        spawner.register_factory("props", factory)
        spawner.spawn_entities(self.tilemap, self.entity_manager)

        all_entities = self.entity_manager.get_entities()
        props_entities = self.entity_manager.get_entities_with(Position, Collider)
        self.assertFalse(self.tilemap.draw_static_object_layers)
        self.assertIn("crate", seen_names)
        self.assertGreater(len(all_entities), 1)
        self.assertGreaterEqual(len(props_entities), 1)

    def test_can_leave_static_object_layers_drawn(self) -> None:
        spawner = MapEntitySpawner(spawn_tile_layer_entities=False)
        spawner.spawn_entities(self.tilemap, self.entity_manager)
        self.assertTrue(self.tilemap.draw_static_object_layers)
        self.assertEqual(self.entity_manager.get_entities(), [])
