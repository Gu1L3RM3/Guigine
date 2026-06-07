from __future__ import annotations

import pygame

from guigine.app.context import SceneContext
from examples.shared_assets import FONT_PRIMARY, MUSIC_MENU, SFX_CONFIRM
from guigine.scene.base_scene import BaseScene


class SplashScene(BaseScene):
    def __init__(self, context: SceneContext):
        super().__init__(context, world_width=context.screen.get_width(), world_height=context.screen.get_height())
        self.background_color = (22, 26, 34)
        self.title_font = self.resources.load_font(FONT_PRIMARY, 24)
        self.body_font = self.resources.load_font(FONT_PRIMARY, 12)

    def start(self) -> None:
        self.context.music.play(MUSIC_MENU, fade_ms=500)

    def process_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_1):
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("basic", duration=0.3)
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_t, pygame.K_2):
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("tmx_demo", duration=0.35)
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_3, pygame.K_w):
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("widgets_only", duration=0.35)

    def update(self, dt: float) -> None:
        _ = dt

    def render(self) -> None:
        self.screen.fill(self.background_color)
        title = self.title_font.render("GUIGINE", True, (240, 240, 240))
        line1 = self.body_font.render("1 OR ENTER  NO MAP GAMEPLAY", True, (200, 200, 205))
        line2 = self.body_font.render("2 OR T      TMX MAP GAMEPLAY", True, (200, 200, 205))
        line3 = self.body_font.render("3 OR W      WIDGETS ONLY UI", True, (200, 200, 205))
        line4 = self.body_font.render("MAP, NO-MAP, AND UI-ONLY FLOWS", True, (140, 180, 210))

        title_rect = title.get_rect(center=(self.screen.get_width() // 2, 180))
        line1_rect = line1.get_rect(center=(self.screen.get_width() // 2, 300))
        line2_rect = line2.get_rect(center=(self.screen.get_width() // 2, 345))
        line3_rect = line3.get_rect(center=(self.screen.get_width() // 2, 390))
        line4_rect = line4.get_rect(center=(self.screen.get_width() // 2, 460))

        self.screen.blit(title, title_rect)
        self.screen.blit(line1, line1_rect)
        self.screen.blit(line2, line2_rect)
        self.screen.blit(line3, line3_rect)
        self.screen.blit(line4, line4_rect)
