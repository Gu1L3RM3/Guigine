from __future__ import annotations

import pygame
from pygame import Vector2


class InputManager:
    def __init__(self):
        self.just_pressed_keys: set[int] = set()
        self.mouse_visible = True

    def begin_frame(self):
        self.just_pressed_keys.clear()

    def process_events(self, events: list[pygame.event.Event]) -> list[pygame.event.Event]:
        self.begin_frame()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.just_pressed_keys.add(event.key)
        return events

    def is_key_just_pressed(self, key: int) -> bool:
        return key in self.just_pressed_keys

    def get_movement_vector(
        self,
        left: int = pygame.K_a,
        right: int = pygame.K_d,
        up: int = pygame.K_w,
        down: int = pygame.K_s,
    ) -> Vector2:
        keys = pygame.key.get_pressed()
        direction = Vector2(0, 0)
        if keys[left] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[right] or keys[pygame.K_RIGHT]:
            direction.x += 1
        if keys[up] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[down] or keys[pygame.K_DOWN]:
            direction.y += 1
        if direction.length_squared() > 1:
            direction = direction.normalize()
        return direction

    def apply_mouse_visibility(self):
        pygame.mouse.set_visible(self.mouse_visible)
