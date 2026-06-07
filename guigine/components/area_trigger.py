from __future__ import annotations

from typing import Callable, Optional

from pygame import Rect

from guigine.ecs.core import Component, Entity


class AreaTrigger(Component):
    def __init__(
        self,
        area: Rect,
        once: bool = False,
        active: bool = True,
        on_entered: Optional[Callable[[object], None]] = None,
        on_stayed: Optional[Callable[[object], None]] = None,
        on_exit: Optional[Callable[[object], None]] = None,
    ):
        self.area = area.copy()
        self.once = once
        self.active = active
        self.triggered_entities = set()
        self.on_entered = on_entered
        self.on_stayed = on_stayed
        self.on_exit = on_exit

    def get_rect(self, x: float, y: float) -> Rect:
        rect = self.area.copy()
        rect.topleft = (x + self.area.x, y + self.area.y)
        return rect

    def check_collision(self, entity: Entity, entity_rect: Rect, area_rect: Rect | None = None) -> None:
        if not self.active:
            return
        target_area = area_rect if area_rect is not None else self.area
        in_area = target_area.colliderect(entity_rect)
        if in_area and entity not in self.triggered_entities:
            self.triggered_entities.add(entity)
            if self.on_entered:
                self.on_entered(entity)
            if self.once:
                self.active = False
        elif in_area and entity in self.triggered_entities:
            if self.on_stayed:
                self.on_stayed(entity)
        elif not in_area and entity in self.triggered_entities:
            self.triggered_entities.remove(entity)
            if self.on_exit:
                self.on_exit(entity)

    def to_dict(self) -> dict:
        return {
            "type": self.__class__.__name__,
            "rect": [self.area.x, self.area.y, self.area.width, self.area.height],
            "once": self.once,
            "active": self.active,
        }
