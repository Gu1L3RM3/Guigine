from __future__ import annotations

from pathlib import Path

import pygame
from pygame import Surface

from guigine.ecs.core import Component
from guigine.resources.resource_manager import ResourceManager


class Sprite(Component):
    def __init__(
        self,
        image: Surface,
        offset_x: float = 0,
        offset_y: float = 0,
        angle: float = 0,
        image_path: str | None = None,
    ):
        self._orig_image = image.convert_alpha()
        self.image_path = image_path
        self.image = self._orig_image.copy()
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.rect = self.image.get_rect()
        self.angle = 0.0
        self._cached_scaled_image: Surface | None = None
        self._cache_key: tuple | None = None
        if angle != 0:
            self.rotate(angle)

    def rotate(self, angle_deg: float) -> None:
        self.angle = (self.angle + angle_deg) % 360
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self._orig_image, self.angle)
        self.rect = self.image.get_rect(center=old_center)
        self._cache_key = None

    def get_size_from_drawn(self) -> tuple[int, int]:
        if not self._cached_scaled_image:
            return self._orig_image.get_size()
        return self._cached_scaled_image.get_size()

    def get_image_for_drawing(self, scale: float) -> Surface:
        if scale == 1.0:
            return self.image
        current_key = (id(self.image), scale)
        if current_key == self._cache_key and self._cached_scaled_image is not None:
            return self._cached_scaled_image
        width, height = self.image.get_size()
        scaled = pygame.transform.scale(self.image, (int(width * scale), int(height * scale)))
        self._cached_scaled_image = scaled
        self._cache_key = current_key
        return scaled

    def to_dict(self) -> dict:
        if not self.image_path:
            raise ValueError("Sprite serialization requires image_path")
        return {
            "type": self.__class__.__name__,
            "image_path": self.image_path,
            "offset_x": self.offset_x,
            "offset_y": self.offset_y,
            "angle": self.angle,
        }

    @classmethod
    def from_dict(cls, data: dict, resources: ResourceManager | None = None) -> "Sprite":
        if data.get("type") != cls.__name__:
            raise ValueError("Invalid serialized Sprite payload")
        resource_manager = resources or ResourceManager()
        surface = resource_manager.load_image(Path(data["image_path"]))
        return cls(
            image=surface,
            offset_x=data["offset_x"],
            offset_y=data["offset_y"],
            angle=data["angle"],
            image_path=data["image_path"],
        )
