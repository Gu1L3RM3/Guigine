from __future__ import annotations

import unittest
from pathlib import Path

from _test_env import ASSET_ROOT, bootstrap_pygame, shutdown_pygame

from guigine.resources.resource_manager import ResourceManager


class ResourceManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        self.resources = ResourceManager(ASSET_ROOT)

    def test_resolve_joins_asset_root(self) -> None:
        resolved = self.resources.resolve("fonts/PressStart2P-Regular.ttf")
        self.assertEqual(resolved, ASSET_ROOT / "fonts/PressStart2P-Regular.ttf")

    def test_load_image_caches_by_path_and_size(self) -> None:
        first = self.resources.load_image("images/buttons/short.png")
        second = self.resources.load_image("images/buttons/short.png")
        scaled = self.resources.load_image("images/buttons/short.png", size=(100, 40))
        self.assertIs(first, second)
        self.assertNotEqual(first.get_size(), scaled.get_size())

    def test_load_font_caches_instances(self) -> None:
        first = self.resources.load_font("fonts/PressStart2P-Regular.ttf", 12)
        second = self.resources.load_font("fonts/PressStart2P-Regular.ttf", 12)
        third = self.resources.load_font("fonts/PressStart2P-Regular.ttf", 16)
        self.assertIs(first, second)
        self.assertIsNot(first, third)

    def test_absolute_path_is_preserved(self) -> None:
        absolute = Path(ASSET_ROOT / "fonts/PressStart2P-Regular.ttf").resolve()
        self.assertEqual(self.resources.resolve(absolute), absolute)
