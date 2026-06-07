from __future__ import annotations

import pygame

from guigine.app.context import SceneContext
from examples.shared_assets import (
    BUTTON_SHORT,
    BUTTON_SHORT_PRESSED,
    BUTTON_WIDE,
    BUTTON_WIDE_PRESSED,
    FONT_PRIMARY,
    MUSIC_MENU,
    SFX_CONFIRM,
    SFX_TYPE,
    SFX_UI_BACK,
    SFX_UI_HOVER,
)
from guigine.scene.base_scene import BaseScene
from guigine.widgets.button import Button
from guigine.widgets.text import Text
from guigine.widgets.type_writer import TypewriterEffect


class WidgetsOnlyScene(BaseScene):
    def __init__(self, context: SceneContext):
        super().__init__(
            context,
            world_width=context.screen.get_width(),
            world_height=context.screen.get_height(),
        )

        self.background_color = (18, 22, 30)
        self.ui = context.ui

        self.status_message = "UI READY"

        self._status_widget: Text | None = None
        self._typewriter: TypewriterEffect | None = None
        self._hovered_button_id: int | None = None

        self._build_ui()

    def start(self) -> None:
        self.context.music.play(MUSIC_MENU, fade_ms=450)

    def end(self) -> None:
        self.ui.clear()

    def process_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.ui.handle_event(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.context.audio.play_ui(SFX_UI_BACK)
                self.scene_manager.start_fade("splash", duration=0.25)
                return

    def update(self, dt: float) -> None:
        self.ui.update(dt)
        self._update_hover_sfx()

    def render(self) -> None:
        self.screen.fill(self.background_color)
        self._draw_panel()
        self.ui.draw(self.screen)

    def _build_ui(self) -> None:
        self.ui.clear()

        resources = self.resources

        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()
        center_x = screen_w // 2

        short_default = resources.load_image(BUTTON_SHORT)
        short_pressed = resources.load_image(BUTTON_SHORT_PRESSED)
        wide_default = resources.load_image(BUTTON_WIDE)
        wide_pressed = resources.load_image(BUTTON_WIDE_PRESSED)

        wide_button_size = self._get_button_size(
            screen_w=screen_w,
            width_ratio=0.26,
            min_width=260,
            max_width=330,
            height=58,
        )

        short_button_size = self._get_button_size(
            screen_w=screen_w,
            width_ratio=0.14,
            min_width=135,
            max_width=170,
            height=54,
        )

        wide_default = pygame.transform.scale(wide_default, wide_button_size)
        wide_pressed = pygame.transform.scale(wide_pressed, wide_button_size)

        short_default = pygame.transform.scale(short_default, short_button_size)
        short_pressed = pygame.transform.scale(short_pressed, short_button_size)

        title = Text(
            "WIDGETS ONLY",
            24,
            (240, 240, 240),
            (center_x, int(screen_h * 0.18)),
            FONT_PRIMARY,
            resource_manager=self.resources,
        )

        subtitle = Text(
            "Buttons, text and typewriter in a standalone Guigine UI scene",
            10,
            (160, 185, 210),
            (center_x, int(screen_h * 0.25)),
            FONT_PRIMARY,
            resource_manager=self.resources,
        )

        self._status_widget = Text(
            self.status_message,
            12,
            (255, 225, 140),
            (center_x, int(screen_h * 0.36)),
            FONT_PRIMARY,
            resource_manager=self.resources,
        )

        self._typewriter = TypewriterEffect(
            position=(center_x, int(screen_h * 0.48)),
            text="This scene proves Guigine can run pure GUI flows without any map or TMX dependency.",
            font_name=FONT_PRIMARY,
            font_size=10,
            font_color=(235, 235, 235),
            speed=25,
            sound_name=SFX_TYPE,
            resource_manager=self.resources,
        )

        button_play = Button(
            init_surface=wide_default,
            surface_pressed=wide_pressed,
            pos_center=(center_x, int(screen_h * 0.60)),
            action=self._play_feedback,
            text="PLAY SFX",
            font_size=12,
            font=FONT_PRIMARY,
            resource_manager=self.resources,
        )

        button_replay = Button(
            init_surface=wide_default,
            surface_pressed=wide_pressed,
            pos_center=(center_x, int(screen_h * 0.70)),
            action=self._replay_typewriter,
            text="REPLAY TEXT",
            font_size=12,
            font=FONT_PRIMARY,
            resource_manager=self.resources,
        )

        button_back = Button(
            init_surface=short_default,
            surface_pressed=short_pressed,
            pos_center=(center_x, int(screen_h * 0.82)),
            action=self._go_back,
            text="MENU",
            font_size=10,
            font=FONT_PRIMARY,
            resource_manager=self.resources,
        )

        self.ui.add(
            title,
            subtitle,
            self._status_widget,
            self._typewriter,
            button_play,
            button_replay,
            button_back,
        )

    def _get_button_size(
        self,
        screen_w: int,
        width_ratio: float,
        min_width: int,
        max_width: int,
        height: int,
    ) -> tuple[int, int]:
        width = int(screen_w * width_ratio)
        width = max(min_width, min(width, max_width))

        return width, height

    def _draw_panel(self) -> None:
        screen_w = self.screen.get_width()
        screen_h = self.screen.get_height()

        panel_rect = pygame.Rect(
            int(screen_w * 0.10),
            int(screen_h * 0.14),
            int(screen_w * 0.80),
            int(screen_h * 0.76),
        )

        pygame.draw.rect(
            self.screen,
            (28, 34, 46),
            panel_rect,
            border_radius=20,
        )

        pygame.draw.rect(
            self.screen,
            (70, 90, 118),
            panel_rect,
            3,
            border_radius=20,
        )

    def _play_feedback(self) -> None:
        self.context.audio.play_ui(SFX_CONFIRM)
        self._set_status("CLICK SOUND PLAYED")

    def _replay_typewriter(self) -> None:
        if self._typewriter is not None:
            self._typewriter.set_text(
                "Widgets can orchestrate presentation, feedback and navigation on their own."
            )

        self.context.audio.play_ui(SFX_CONFIRM)
        self._set_status("TYPEWRITER RESTARTED")

    def _go_back(self) -> None:
        self.context.audio.play_ui(SFX_UI_BACK)
        self.scene_manager.start_fade("splash", duration=0.25)

    def _set_status(self, text: str) -> None:
        self.status_message = text

        if self._status_widget is not None:
            screen_w = self.screen.get_width()
            screen_h = self.screen.get_height()

            self._status_widget.set_text(
                text,
                (screen_w // 2, int(screen_h * 0.36)),
            )

    def _update_hover_sfx(self) -> None:
        hovered_button_id = None

        for widget in self.ui.widgets:
            detector = getattr(widget, "gesture_detector", None)

            if detector is not None and getattr(detector, "is_hovered", False):
                hovered_button_id = widget.id
                break

        if hovered_button_id is not None and hovered_button_id != self._hovered_button_id:
            self.context.audio.play_ui(SFX_UI_HOVER, volume=0.55)

        self._hovered_button_id = hovered_button_id