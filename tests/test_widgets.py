from __future__ import annotations

import unittest

import pygame

from _test_env import ASSET_ROOT, bootstrap_pygame, shutdown_pygame

from guigine.managers.ui_manager import UIManager
from guigine.resources.resource_manager import ResourceManager
from guigine.widgets.button import Button
from guigine.widgets.gesture_detector import ClickType
from guigine.widgets.text import Text
from guigine.widgets.type_writer import TypewriterEffect


class WidgetEventSpy:
    def __init__(self):
        self.events = []

    def handle_events(self, event):
        self.events.append(event.type)

    def update(self, dt):
        _ = dt

    def draw(self, surface):
        _ = surface


class WidgetsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bootstrap_pygame()

    @classmethod
    def tearDownClass(cls) -> None:
        shutdown_pygame()

    def setUp(self) -> None:
        self.resources = ResourceManager(ASSET_ROOT)

    def test_text_uses_resource_font(self) -> None:
        text = Text(
            "hello",
            12,
            (255, 255, 255),
            (10, 10),
            "fonts/PressStart2P-Regular.ttf",
            resource_manager=self.resources,
        )
        self.assertEqual(text.rect.center, (10, 10))
        self.assertGreater(text.surf.get_width(), 0)

    def test_button_activate_triggers_action_and_pressed_feedback(self) -> None:
        action_calls: list[str] = []
        button = Button(
            init_surface=self.resources.load_image("images/buttons/short.png"),
            surface_pressed=self.resources.load_image("images/buttons/short_pressed.png"),
            pos_center=(60, 40),
            action=lambda: action_calls.append("called"),
            text="GO",
            font_size=10,
            font="fonts/PressStart2P-Regular.ttf",
            resource_manager=self.resources,
        )
        button.activate(press_feedback_seconds=0.3)
        button.update(0.1)
        self.assertEqual(action_calls, ["called"])
        self.assertIs(button.current_surf, button.surface_pressed)
        button.update(0.3)
        self.assertIs(button.current_surf, button.init_surface)

    def test_ui_manager_dispatches_events_and_draws_widgets(self) -> None:
        ui = UIManager()
        spy = WidgetEventSpy()
        ui.add(spy)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        ui.handle_event(event)
        ui.update(0.016)
        ui.draw(pygame.display.get_surface())
        self.assertEqual(spy.events, [pygame.KEYDOWN])

    def test_typewriter_can_skip_to_completion(self) -> None:
        effect = TypewriterEffect(
            position=(100, 100),
            text="sample",
            font_name="fonts/PressStart2P-Regular.ttf",
            font_size=10,
            sound_name=None,
            resource_manager=self.resources,
        )
        effect.skip()
        self.assertTrue(effect.finished)
        self.assertEqual(effect._current_text, "sample")
