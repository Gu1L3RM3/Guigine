from __future__ import annotations

import unittest

from _test_env import ASSET_ROOT, bootstrap_pygame, shutdown_pygame

from guigine.app.context import SceneContext
from guigine.app.scene_manager import SceneManager
from guigine.managers.audio_manager import AudioManager
from guigine.managers.input_manager import InputManager
from guigine.managers.music_manager import MusicManager
from guigine.managers.ui_manager import UIManager
from guigine.resources.resource_manager import ResourceManager
from guigine.scene.base_scene import BaseScene


class DummyScene(BaseScene):
    def __init__(self, context: SceneContext, name: str):
        super().__init__(context, world_width=320, world_height=240)
        self.name = name
        self.started = 0
        self.ended = 0

    def start(self) -> None:
        self.started += 1

    def end(self) -> None:
        self.ended += 1

    def process_input(self, events) -> None:
        _ = events

    def update(self, dt: float) -> None:
        _ = dt

    def render(self) -> None:
        return None


class SceneManagerTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        import pygame

        screen = pygame.display.get_surface()
        assert screen is not None
        resources = ResourceManager(ASSET_ROOT)
        audio = AudioManager(resources)
        self.context = SceneContext(
            screen=screen,
            resources=resources,
            scene_manager=SceneManager(),
            input=InputManager(),
            ui=UIManager(),
            audio=audio,
            music=MusicManager(audio),
        )
        self.manager = self.context.scene_manager
        self.manager.bind_context(self.context)
        self.manager.register("one", lambda ctx: DummyScene(ctx, "one"))
        self.manager.register("two", lambda ctx: DummyScene(ctx, "two"))

    def test_change_activates_scene(self) -> None:
        self.manager.change("one")
        self.assertEqual(self.manager.active_scene_name, "one")
        self.assertEqual(self.manager.active_scene.started, 1)

    def test_change_ends_previous_scene(self) -> None:
        self.manager.change("one")
        first = self.manager.active_scene
        self.manager.change("two")
        self.assertEqual(first.ended, 1)
        self.assertEqual(self.manager.active_scene_name, "two")

    def test_start_fade_switches_scene_after_transition(self) -> None:
        self.manager.change("one")
        first = self.manager.active_scene
        self.manager.start_fade("two", duration=0.1)
        for _ in range(120):
            self.manager.update_transition()
        self.assertFalse(self.manager.transitioning)
        self.assertEqual(first.ended, 1)
        self.assertEqual(self.manager.active_scene_name, "two")
        self.assertEqual(self.manager.active_scene.started, 1)
        self.assertEqual(self.manager.transition_phase, "none")

    def test_change_raises_when_scene_missing(self) -> None:
        with self.assertRaises(KeyError):
            self.manager.change("missing")
