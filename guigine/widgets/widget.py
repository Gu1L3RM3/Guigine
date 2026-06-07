from __future__ import annotations

from abc import ABC, abstractmethod

import pygame
from pygame import Surface


class Widget(ABC):
    _next_id = 1

    def __init__(self):
        self.id = Widget._next_id
        Widget._next_id += 1

    @abstractmethod
    def draw(self, surface: Surface):
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float):
        raise NotImplementedError

    def handle_events(self, event: pygame.event.Event):
        _ = event
