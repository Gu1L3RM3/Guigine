from __future__ import annotations

import unittest

from _test_env import ASSET_ROOT, bootstrap_pygame, shutdown_pygame

from guigine.map.tile_map_loader import TileMapLoader
from guigine.resources.resource_manager import ResourceManager


class TileMapLoaderTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        self.loader = TileMapLoader(ResourceManager(ASSET_ROOT), walk_layer_name="ground2")

    def test_load_demo_map_builds_expected_runtime_data(self) -> None:
        tilemap = self.loader.load("demo/demo_map.tmx")
        self.assertEqual((tilemap.tile_width, tilemap.tile_height), (16, 16))
        self.assertEqual((tilemap.map_width, tilemap.map_height), (192, 144))
        self.assertEqual(tilemap.get_spawn_point("player"), (32, 32))
        self.assertEqual(tilemap.get_waypoint_tile("center"), (6, 4))
        self.assertIsNotNone(tilemap.ground_surface)
        self.assertIsNotNone(tilemap.object_surface)
        self.assertGreater(len(tilemap.solid_colliders), 0)

    def test_loader_collects_spawn_points_case_insensitively(self) -> None:
        tilemap = self.loader.load("demo/demo_map.tmx")
        self.assertEqual(tilemap.get_spawn_point("PLAYER"), (32, 32))
