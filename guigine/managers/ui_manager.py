from __future__ import annotations

import pygame
from pygame import Surface

from guigine.widgets.widget import Widget


class UIManager:
    def __init__(self):
        self.widgets: list[Widget] = []

    def add(self, *widgets: Widget) -> None:
        self.widgets.extend(widgets)

    def remove(self, widget: Widget) -> None:
        self.widgets.remove(widget)

    def clear(self) -> None:
        self.widgets.clear()

    def update(self, dt: float) -> None:
        for widget in self.widgets:
            widget.update(dt)

    def draw(self, surface: Surface) -> None:
        for widget in self.widgets:
            widget.draw(surface)

    def handle_event(self, event: pygame.event.Event) -> None:
        for widget in self.widgets:
            widget.handle_events(event)
