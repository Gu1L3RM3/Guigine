from __future__ import annotations

import pygame

from guigine.managers.time_manager import TimeManager
from guigine.resources.resource_manager import ResourceManager
from guigine.widgets.widget import Widget


class Text(Widget):
    def __init__(
        self,
        text: str,
        font_size: int,
        font_color: tuple[int, int, int] = (255, 255, 255),
        pos_center: tuple[int, int] = (0, 0),
        font_name: str | None = None,
        resource_manager: ResourceManager | None = None,
    ):
        super().__init__()
        self.resource_manager = resource_manager or ResourceManager()
        self.font_color = font_color
        if font_name:
            self.font = self.resource_manager.load_font(font_name, font_size)
        else:
            self.font = pygame.font.Font(None, font_size)
        self.set_text(text, pos_center)

    def draw(self, surface):
        surface.blit(self.surf, self.rect)

    def set_text(self, new_text: str, new_pos_center: tuple[int, int]):
        self.surf = self.font.render(new_text, True, self.font_color)
        self.rect = self.surf.get_rect(center=new_pos_center)

    def update(self, dt):
        _ = dt
