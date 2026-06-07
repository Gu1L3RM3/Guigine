from __future__ import annotations

import pygame
from pygame import Rect

from guigine.components.always_on_top import AlwaysOnTop
from guigine.components.area_trigger import AreaTrigger
from guigine.components.base import Position
from guigine.components.collider import Collider
from guigine.components.depth_anchor import DepthAnchor
from guigine.components.render_layer import RenderLayer
from guigine.components.sprite import Sprite
from guigine.ecs.core import Entity, System
from guigine.render.camera import Camera


class RenderSystem(System):
    def __init__(self, screen: pygame.Surface, camera: Camera, entity_manager,debug_mode :bool= False):
        self.screen = screen
        self.camera = camera
        self.entity_manager = entity_manager
        self.debug_mode = debug_mode
        self.debug_collider_color = (255, 0, 0)
        self.debug_area_color = (0, 255, 0)
        self.debug_sprite_rect_color = (0, 0, 255)

    def update(self, entity_manager, dt):
        _ = entity_manager
        self.camera.update(dt)

    def _draw_camera_viewport(self):
        pygame.draw.rect(self.screen, (255, 255, 0), self.camera.viewport, 1)

    def _draw_collider(self, entity: Entity, pos: Position, scale: float):
        if entity.has(Collider):
            col = entity.get(Collider)
            world_rect = col.get_rect(pos.x, pos.y)
            scaled = Rect(world_rect.x * scale, world_rect.y * scale, world_rect.width * scale, world_rect.height * scale)
            draw_rect = self.camera.apply(scaled)
            pygame.draw.rect(self.screen, self.debug_collider_color, draw_rect, 1)

    def _draw_area_triggers(self, entity: Entity, scale: float):
        if not entity.has(AreaTrigger):
            return
        area_trigger = entity.get(AreaTrigger)
        area_rect = area_trigger.area
        scaled = Rect(area_rect.x * scale, area_rect.y * scale, area_rect.width * scale, area_rect.height * scale)
        draw_rect = self.camera.apply(scaled)
        color = self.debug_area_color if area_trigger.active else (100, 100, 100)
        pygame.draw.rect(self.screen, color, draw_rect, 2)

    def _sync_sprite_rect(self, entity: Entity, from_center_pos: bool):
        pos = entity.get(Position)
        spr = entity.get(Sprite)
        if from_center_pos:
            spr.rect.center = (pos.x, pos.y)
        else:
            spr.rect.topleft = (pos.x + spr.offset_x, pos.y + spr.offset_y)

    def _world_viewport(self, viewport: Rect, scale: float) -> Rect:
        if scale <= 0:
            return Rect(viewport)
        inv = 1.0 / scale
        return Rect(int(viewport.x * inv), int(viewport.y * inv), int(viewport.width * inv) + 2, int(viewport.height * inv) + 2)

    def draw(self, from_center_pos: bool = False, scale: float = 1.0):
        entities = self.entity_manager.get_entities_with(Position, Sprite)
        viewport = self.camera.viewport
        world_viewport = self._world_viewport(viewport, scale)
        visible_entities: list[Entity] = []
        for entity in entities:
            self._sync_sprite_rect(entity, from_center_pos)
            if entity.get(Sprite).rect.colliderect(world_viewport):
                visible_entities.append(entity)
        visible_entities.sort(key=self._render_sort_key)
        for entity in visible_entities:
            self._draw_entity(entity, viewport, scale)
        self._draw_debug_info(visible_entities, scale)

    def _render_sort_key(self, entity: Entity):
        return (self._get_layer_value(entity), self._get_depth_y(entity), entity.id)

    def _get_layer_value(self, entity: Entity) -> int:
        if entity.has(RenderLayer):
            return entity.get(RenderLayer).value
        if entity.has(AlwaysOnTop):
            return RenderLayer.OVERLAY
        return RenderLayer.ACTOR

    def _get_depth_y(self, entity: Entity) -> int:
        pos = entity.get(Position)
        if entity.has(DepthAnchor):
            return int(pos.y + entity.get(DepthAnchor).offset_y)
        if entity.has(Collider):
            col = entity.get(Collider)
            return int(pos.y + col.offset_y + col.height)
        return int(pos.y + entity.get(Sprite).rect.height)

    def _draw_debug_info(self, entities: list[Entity], scale: float):
        if not self.debug_mode:
            return
        for entity in entities:
            self._draw_collider(entity, entity.get(Position), scale)
            self._draw_area_triggers(entity, scale)
        self._draw_camera_viewport()

    def _draw_entity(self, entity: Entity, viewport: Rect, scale: float):
        spr = entity.get(Sprite)
        scaled_entity_rect = Rect(spr.rect.x * scale, spr.rect.y * scale, spr.rect.width * scale, spr.rect.height * scale)
        if not viewport.colliderect(scaled_entity_rect):
            return
        image = spr.get_image_for_drawing(scale)
        draw_rect = self.camera.apply(scaled_entity_rect)
        self.screen.blit(image, draw_rect)
