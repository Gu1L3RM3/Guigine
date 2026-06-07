from __future__ import annotations

from typing import List

import pygame

from guigine.components.base import Freeze, Position, Velocity
from guigine.components.collider import Collider
from guigine.components.dynamic_collision import DynamicCollision
from guigine.ecs.core import Entity, System
from guigine.ecs.entity_manager import EntityManager


class PhysicsSystem(System):
    def __init__(self):
        self.static_colliders: List[pygame.Rect] = []
        self.external_static_colliders: List[pygame.Rect] = []

    def set_external_static_colliders(self, colliders: List[pygame.Rect]):
        self.external_static_colliders = list(colliders)

    def cache_static_colliders(self, entity_manager: EntityManager):
        collidable_entities = entity_manager.get_entities_with(
            Position, Collider, filter_fn=lambda entity: not entity.has(Velocity)
        )
        entity_colliders = [
            entity.get(Collider).get_rect(entity.get(Position).x, entity.get(Position).y)
            for entity in collidable_entities
        ]
        self.static_colliders = [*entity_colliders, *self.external_static_colliders]

    def update(self, entity_manager: EntityManager, dt: float):
        moving_entities = entity_manager.get_entities_with(Position, Velocity)
        for entity in moving_entities:
            if entity.has(Freeze) and entity.get(Freeze).active:
                continue
            if not entity.has(Collider):
                self._move(entity, dt)
                continue
            self._move_with_collision(entity, moving_entities, dt)

    def _move(self, entity: Entity, dt: float):
        pos = entity.get(Position)
        vel = entity.get(Velocity)
        pos.x += vel.vx * dt
        pos.y += vel.vy * dt

    def _move_with_collision(self, entity: Entity, moving_entities: List[Entity], dt: float):
        vel = entity.get(Velocity)
        if vel.vx != 0:
            self._move_axis(entity, vel.vx * dt, 0, moving_entities)
        if vel.vy != 0:
            self._move_axis(entity, 0, vel.vy * dt, moving_entities)

    def _has_dynamic_collision_enabled(self, entity: Entity) -> bool:
        if not entity.has(DynamicCollision):
            return True
        return entity.get(DynamicCollision).enabled

    def _should_ignore_dynamic_collision(self, entity: Entity, other: Entity) -> bool:
        return (not self._has_dynamic_collision_enabled(entity)) or (not self._has_dynamic_collision_enabled(other))

    def _move_axis(self, entity: Entity, dx: float, dy: float, moving_entities: List[Entity]):
        pos = entity.get(Position)
        vel = entity.get(Velocity)
        col = entity.get(Collider)
        pos.x += dx
        pos.y += dy
        rect = col.get_rect(pos.x, pos.y)

        for wall in self.static_colliders:
            if rect.colliderect(wall):
                rect, vel = self._resolve_collision(rect, wall, dx, dy, vel)
                pos.x = rect.x - col.offset_x
                pos.y = rect.y - col.offset_y
                return

        for other in moving_entities:
            if other is entity or not other.has(Collider):
                continue
            if self._should_ignore_dynamic_collision(entity, other):
                continue
            other_pos = other.get(Position)
            other_col = other.get(Collider)
            other_rect = other_col.get_rect(other_pos.x, other_pos.y)
            if rect.colliderect(other_rect):
                rect, vel = self._resolve_collision(rect, other_rect, dx, dy, vel)
                pos.x = rect.x - col.offset_x
                pos.y = rect.y - col.offset_y
                return

    def _resolve_collision(self, rect, other_rect, dx, dy, vel):
        if dx > 0:
            rect.right = other_rect.left
            vel.vx = 0
        elif dx < 0:
            rect.left = other_rect.right
            vel.vx = 0
        elif dy > 0:
            rect.bottom = other_rect.top
            vel.vy = 0
        elif dy < 0:
            rect.top = other_rect.bottom
            vel.vy = 0
        return rect, vel
