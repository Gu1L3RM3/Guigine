from __future__ import annotations

import pygame

from guigine.app.context import SceneContext
from guigine.components.base import Position, Velocity
from guigine.components.collider import Collider
from guigine.components.sprite import Sprite
from guigine.ecs.core import Entity
from examples.shared_assets import FONT_PRIMARY, MUSIC_MAP, SFX_CONFIRM
from guigine.map.map_entity_spawner import MapEntitySpawner
from guigine.map.map_renderer import MapRenderer
from guigine.map.tile_map_loader import TileMapLoader
from guigine.scene.base_scene import BaseScene
from guigine.systems.physics import PhysicsSystem
from guigine.systems.render import RenderSystem


class TmxScene(BaseScene):
    def __init__(self, context: SceneContext):
        self.tilemap = TileMapLoader(context.resources, walk_layer_name="ground2").load("demo/demo_map.tmx")
        super().__init__(context, world_width=self.tilemap.map_width, world_height=self.tilemap.map_height)

        self.map_renderer = MapRenderer(self.tilemap, self.camera, self.screen,scale=1)
        self.physics = PhysicsSystem()
        self.physics.set_external_static_colliders(self.tilemap.solid_colliders)
        self.render_system = RenderSystem(self.screen, self.camera, self.entity_manager)

        self.spawner = MapEntitySpawner(spawn_tile_layer_entities=True)
        self.spawner.register_factory("props", self._spawn_prop_from_object)
        self.spawner.spawn_entities(self.tilemap, self.entity_manager)
        self.font = self.resources.load_font(FONT_PRIMARY, 10)

        spawn_x, spawn_y = self.tilemap.get_spawn_point("player") or (32, 32)
        self.player = self._create_player(spawn_x, spawn_y)
        self.camera.follow = self.player
        self.add_system(self.physics)

    def start(self) -> None:
        self.context.music.play(MUSIC_MAP, fade_ms=600)

    def _create_player(self, x: int, y: int):
        surface = pygame.Surface((16, 16), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        pygame.draw.rect(surface, (245, 210, 90), (2, 1, 12, 14), border_radius=3)
        pygame.draw.rect(surface, (80, 50, 20), (5, 4, 2, 2))
        pygame.draw.rect(surface, (80, 50, 20), (9, 4, 2, 2))
        player = self.entity_manager.create(
            Position(x, y),
            Velocity(),
            Collider(12, 12, offset_x=2, offset_y=2),
            Sprite(surface),
        )
        return player

    def _spawn_prop_from_object(self, obj, entity_manager, tilemap):
        width = max(1, int(obj.width or tilemap.tile_width))
        height = max(1, int(obj.height or tilemap.tile_height))
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))
        pygame.draw.rect(surface, (146, 102, 57), (0, 0, width, height), border_radius=3)
        pygame.draw.rect(surface, (98, 66, 36), (2, 2, max(1, width - 4), max(1, height - 4)), 2, border_radius=3)
        entity = Entity()
        entity.add(Position(obj.x, obj.y), Sprite(surface), Collider(width, height))
        return entity

    def process_input(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("splash", duration=0.25)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("basic", duration=0.25)
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.context.audio.play_ui(SFX_CONFIRM)
                self.scene_manager.start_fade("widgets_only", duration=0.25)
                return

        velocity = self.player.get(Velocity)
        velocity.vx = 0.0
        velocity.vy = 0.0
        keys = pygame.key.get_pressed()
        speed = 170.0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            velocity.vx -= speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            velocity.vx += speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            velocity.vy -= speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            velocity.vy += speed

    def update(self, dt: float) -> None:
        self.physics.cache_static_colliders(self.entity_manager)
        self.update_systems(dt)
        self.camera.update(dt)

    def render(self) -> None:
        self.screen.fill(self.background_color)
        self.map_renderer.draw()
        self.render_system.draw()
        self.map_renderer.draw_foreground()

        title = self.font.render("TMX MAP EXAMPLE", True, (240, 240, 240))
        hint = self.font.render("WASD MOVE  TAB MENU  1 NO MAP  3 WIDGETS", True, (190, 190, 200))
        info = self.font.render("COLLIDERS AND PROP SPAWNS COME FROM TMX", True, (140, 180, 210))
        self.screen.blit(title, (20, 20))
        self.screen.blit(hint, (20, 44))
        self.screen.blit(info, (20, 68))
