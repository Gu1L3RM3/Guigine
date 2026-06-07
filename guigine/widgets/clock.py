from __future__ import annotations

from typing import Callable

import pygame
from pygame import Surface

from guigine.resources.resource_manager import ResourceManager
from guigine.widgets.widget import Widget


class ClockWidget(Widget):
    def __init__(self, time_provider: Callable[[], tuple[int, int]], font_name: str | None = None, font_size: int = 18):
        super().__init__()
        self.time_provider = time_provider
        self.padding = 10
        resource_manager = ResourceManager()
        self.font = resource_manager.load_font(font_name, font_size) if font_name else pygame.font.Font(None, font_size)
        self.time_str = "00:00"

    def update(self, dt):
        _ = dt
        hours, minutes = self.time_provider()
        self.time_str = f"{hours:02d}:{minutes:02d}"

    def draw(self, surface: Surface):
        text_surface = self.font.render(self.time_str, True, (255, 255, 255))
        bg_rect = pygame.Rect(0, 0, text_surface.get_width() + self.padding * 2, text_surface.get_height() + self.padding * 2)
        bg_rect.topright = (surface.get_width() - 15, 15)
        text_rect = text_surface.get_rect(center=bg_rect.center)
        pygame.draw.rect(surface, (0, 0, 0, 150), bg_rect, border_radius=5)
        surface.blit(text_surface, text_rect)
