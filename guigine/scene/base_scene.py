from __future__ import annotations

from abc import ABC, abstractmethod

import pygame

from guigine.app.context import SceneContext
from guigine.ecs.core import System
from guigine.ecs.entity_manager import EntityManager
from guigine.render.camera import Camera


class BaseScene(ABC):
    def __init__(
        self,
        context: SceneContext,
        world_width: int,
        world_height: int,
    ):
        self.context = context
        self.screen = context.screen
        self.resources = context.resources
        self.scene_manager = context.scene_manager
        self.entity_manager = EntityManager()
        self.camera = Camera(self.screen, world_width, world_height)
        self.systems: list[System] = []
        self.background_color = (18, 18, 24)

    def add_system(self, *systems: System) -> None:
        self.systems.extend(systems)

    def update_systems(self, dt: float) -> None:
        for system in self.systems:
            system.update(self.entity_manager, dt)

    def start(self) -> None:
        pass

    def end(self) -> None:
        pass

    @abstractmethod
    def process_input(self, events: list[pygame.event.Event]) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, dt: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def render(self) -> None:
        raise NotImplementedError
