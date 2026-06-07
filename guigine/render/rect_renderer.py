from __future__ import annotations

import pygame

from guigine.components.base import Position, RectangleSprite
from guigine.ecs.entity_manager import EntityManager
from guigine.render.camera import Camera


class RectangleRenderer:
    def draw(self, screen: pygame.Surface, entity_manager: EntityManager, camera: Camera) -> None:
        for entity in entity_manager.get_entities_with(Position, RectangleSprite):
            position = entity.get(Position)
            sprite = entity.get(RectangleSprite)
            rect = pygame.Rect(int(position.x), int(position.y), sprite.width, sprite.height)
            pygame.draw.rect(screen, sprite.color, camera.apply(rect))
