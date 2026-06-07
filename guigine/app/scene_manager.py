from __future__ import annotations

from typing import Callable

from guigine.app.context import SceneContext
from guigine.scene.base_scene import BaseScene


SceneFactory = Callable[[SceneContext], BaseScene]


class SceneManager:
    def __init__(self, context: SceneContext | None = None):
        self._factories: dict[str, SceneFactory] = {}
        self.active_scene: BaseScene | None = None
        self.active_scene_name: str | None = None
        self.context = context
        self.transitioning = False
        self.transition_target: BaseScene | None = None
        self.transition_target_name: str | None = None
        self.transition_alpha = 0.0
        self.transition_speed = 0.0
        self.transition_surface = None
        self.transition_phase = "none"

    def bind_context(self, context: SceneContext) -> None:
        self.context = context

    def register(self, name: str, factory: SceneFactory) -> None:
        self._factories[name] = factory

    def change(self, name: str) -> None:
        if name not in self._factories:
            raise KeyError(f"Scene '{name}' is not registered")
        if self.context is None:
            raise RuntimeError("SceneManager cannot change scenes before a SceneContext is bound")
        if self.active_scene is not None:
            self.active_scene.end()
        self.active_scene = self._factories[name](self.context)
        self.active_scene_name = name
        self.active_scene.start()

    def start_fade(self, name: str, duration: float = 0.5) -> None:
        if name not in self._factories:
            raise KeyError(f"Scene '{name}' is not registered")
        if self.context is None:
            raise RuntimeError("SceneManager cannot change scenes before a SceneContext is bound")
        if self.active_scene is None:
            self.change(name)
            return
        self.transitioning = True
        self.transition_target = self._factories[name](self.context)
        self.transition_target_name = name
        self.transition_phase = "fade_out"
        self.transition_alpha = 0.0
        self.transition_speed = 255 / max(0.001, duration * 60)
        self.transition_surface = self.context.screen.copy()
        self.transition_surface.fill((0, 0, 0))

    def update_transition(self) -> None:
        if not self.transitioning:
            return
        if self.transition_phase == "fade_out":
            self.transition_alpha += self.transition_speed
            if self.transition_alpha >= 255:
                self.transition_alpha = 255
                if self.active_scene is not None:
                    self.active_scene.end()
                self.active_scene = self.transition_target
                self.active_scene_name = self.transition_target_name
                self.active_scene.start()
                self.transition_phase = "fade_in"
        elif self.transition_phase == "fade_in":
            self.transition_alpha -= self.transition_speed
            if self.transition_alpha <= 0:
                self.transition_alpha = 0
                self.transitioning = False
                self.transition_phase = "none"

    def draw_transition(self, surface) -> None:
        if self.transitioning and self.transition_surface is not None:
            self.transition_surface.set_alpha(int(self.transition_alpha))
            surface.blit(self.transition_surface, (0, 0))
