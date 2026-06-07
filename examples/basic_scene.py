from __future__ import annotations

import pygame

from guigine.app.context import SceneContext
from guigine.components.base import Position, RectangleSprite, Velocity
from examples.shared_assets import FONT_PRIMARY, MUSIC_WORLD, SFX_CONFIRM
from guigine.render.rect_renderer import RectangleRenderer
from guigine.scene.base_scene import BaseScene
from guigine.systems.physics import PhysicsSystem


class BasicScene(BaseScene):
    def __init__(self, context: SceneContext):
        super().__init__(context, world_width=2400, world_height=1400)
        self.renderer = RectangleRenderer()
        self.font = self.resources.load_font(FONT_PRIMARY, 14)
        self.player = self.entity_manager.create(
            Position(120, 120),
            Velocity(),
            RectangleSprite(48, 48, (90, 200, 255)),
        )
        self.camera.follow = self.player
        self.add_system(PhysicsSystem())
        self.pickups: list[pygame.Rect] = [
            pygame.Rect(320, 220, 20, 20),
            pygame.Rect(520, 380, 20, 20),
            pygame.Rect(720, 260, 20, 20),
            pygame.Rect(940, 520, 20, 20),
        ]
        self.collected = 0

    def start(self) -> None:
        self.context.music.play(MUSIC_WORLD, fade_ms=600)

    def end(self) -> None:
        return None

    def process_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("splash", duration=0.25)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("tmx_demo", duration=0.25)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("widgets_only", duration=0.25)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.context.audio.play_sfx(SFX_CONFIRM, volume=0.8)
                self.camera.start_shake(duration=0.12, intensity=3.0)
        velocity = self.player.get(Velocity)
        velocity.vx = 0.0
        velocity.vy = 0.0
        keys = pygame.key.get_pressed()
        speed = 240.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocity.vx -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocity.vx += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            velocity.vy -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velocity.vy += speed

    def update(self, dt: float) -> None:
        self.update_systems(dt)
        self._collect_pickups()
        self.camera.update(dt)

    def render(self) -> None:
        self.screen.fill(self.background_color)
        self._draw_background_grid()
        self._draw_pickups()
        self.renderer.draw(self.screen, self.entity_manager, self.camera)
        label = self.font.render("NO MAP EXAMPLE", True, (240, 240, 240))
        hint = self.font.render("WASD/ARROWS MOVE  SPACE SFX  TAB MENU", True, (180, 180, 190))
        scene_hint = self.font.render("M MAP EXAMPLE  U WIDGETS EXAMPLE", True, (180, 180, 190))
        score = self.font.render(f"PICKUPS {self.collected}", True, (255, 220, 120))
        self.screen.blit(label, (24, 24))
        self.screen.blit(hint, (24, 52))
        self.screen.blit(scene_hint, (24, 80))
        self.screen.blit(score, (24, 108))

    def _draw_background_grid(self) -> None:
        grid_color = (32, 40, 50)
        spacing = 64
        for x in range(0, self.camera.world_width + 1, spacing):
            start = self.camera.apply(pygame.Rect(x, 0, 1, self.camera.world_height))
            pygame.draw.line(self.screen, grid_color, (start.x, 0), (start.x, self.screen.get_height()))
        for y in range(0, self.camera.world_height + 1, spacing):
            start = self.camera.apply(pygame.Rect(0, y, self.camera.world_width, 1))
            pygame.draw.line(self.screen, grid_color, (0, start.y), (self.screen.get_width(), start.y))

    def _draw_pickups(self) -> None:
        for rect in self.pickups:
            draw_rect = self.camera.apply(rect)
            pygame.draw.rect(self.screen, (255, 210, 90), draw_rect, border_radius=6)
            pygame.draw.rect(self.screen, (140, 90, 30), draw_rect, 2, border_radius=6)

    def _collect_pickups(self) -> None:
        player_pos = self.player.get(Position)
        player_rect = pygame.Rect(int(player_pos.x), int(player_pos.y), 48, 48)
        remaining_pickups: list[pygame.Rect] = []
        for rect in self.pickups:
            if rect.colliderect(player_rect):
                self.collected += 1
                self.context.audio.play_sfx(SFX_CONFIRM, volume=0.65)
            else:
                remaining_pickups.append(rect)
        self.pickups = remaining_pickups
