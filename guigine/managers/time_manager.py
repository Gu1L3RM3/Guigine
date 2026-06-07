from __future__ import annotations

import pygame


class TimeManager:
    def __init__(self):
        self.timers: dict[str, int] = {}

    def set(self, name: str, interval: float) -> None:
        self.timers[name] = pygame.time.get_ticks() + int(interval * 1000)

    def ready(self, name: str) -> bool:
        return pygame.time.get_ticks() >= self.timers.get(name, 0)

    def reset(self, name: str, interval: float) -> None:
        self.set(name, interval)

    def clear(self, name: str) -> None:
        self.timers.pop(name, None)

    def remaining(self, name: str) -> float:
        return max(0.0, (self.timers.get(name, 0) - pygame.time.get_ticks()) / 1000)
