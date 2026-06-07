from __future__ import annotations

import random

from pygame import Rect, Surface, Vector2

from guigine.components.base import Position
from guigine.ecs.core import Entity


class Camera:
    def __init__(self, screen: Surface, world_width: int, world_height: int):
        self.screen = screen
        width, height = screen.get_size()
        self.viewport = Rect(0, 0, width, height)
        self.position = Vector2(0, 0)
        self.world_width = world_width
        self.world_height = world_height
        self.scale = 1.0
        self._target: Entity | None = None
        self._shake_time_left = 0.0
        self._shake_duration = 0.0
        self._shake_intensity = 0.0
        self._shake_offset = Vector2(0, 0)

    @property
    def follow(self) -> Entity | None:
        return self._target

    @follow.setter
    def follow(self, entity: Entity) -> None:
        if not entity.has(Position):
            raise ValueError("Camera target must have a Position component")
        self._target = entity
        self._center_on_target()

    def _center_on_target(self) -> None:
        if self._target is None:
            return
        position = self._target.get(Position)
        center_x = position.x * self.scale
        center_y = position.y * self.scale

        x = center_x - self.viewport.w / 2
        y = center_y - self.viewport.h / 2

        if self.world_width > self.viewport.w:
            x = max(0, min(x, self.world_width - self.viewport.w))
        else:
            x = (self.world_width - self.viewport.w) / 2

        if self.world_height > self.viewport.h:
            y = max(0, min(y, self.world_height - self.viewport.h))
        else:
            y = (self.world_height - self.viewport.h) / 2

        self.viewport.x = round(x)
        self.viewport.y = round(y)

    def update(self, dt: float = 0.0) -> None:
        if self._target is not None:
            self._center_on_target()
        self._update_shake(dt)

    def start_shake(self, duration: float = 0.18, intensity: float = 4.0) -> None:
        self._shake_duration = max(self._shake_duration, float(duration))
        self._shake_time_left = max(self._shake_time_left, float(duration))
        self._shake_intensity = max(self._shake_intensity, float(intensity))

    def _update_shake(self, dt: float) -> None:
        if self._shake_time_left <= 0:
            self._shake_offset.xy = (0, 0)
            self._shake_duration = 0.0
            self._shake_intensity = 0.0
            return

        self._shake_time_left = max(0.0, self._shake_time_left - max(0.0, dt))
        ratio = self._shake_time_left / max(0.001, self._shake_duration)
        amplitude = self._shake_intensity * ratio
        self._shake_offset.xy = (
            random.uniform(-amplitude, amplitude),
            random.uniform(-amplitude, amplitude),
        )

    def apply(self, rect: Rect) -> Rect:
        return rect.move(
            -self.viewport.x + int(self._shake_offset.x),
            -self.viewport.y + int(self._shake_offset.y),
        )
