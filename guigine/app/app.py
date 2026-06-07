from __future__ import annotations

import pygame

from guigine.app.config import EngineConfig
from guigine.app.context import SceneContext
from guigine.app.scene_manager import SceneManager
from guigine.managers.audio_manager import AudioManager
from guigine.managers.event_manager import EventManager
from guigine.managers.input_manager import InputManager
from guigine.managers.music_manager import MusicManager
from guigine.managers.time_manager import TimeManager
from guigine.managers.ui_manager import UIManager
from guigine.resources.resource_manager import ResourceManager


class EngineApp:
    def __init__(
        self,
        config: EngineConfig | None = None,
    ):
        self.config = config or EngineConfig()
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((self.config.width, self.config.height))
        pygame.display.set_caption(self.config.title)
        self.clock = pygame.time.Clock()
        self.fps = self.config.fps
        self.resources = ResourceManager(asset_root=self.config.asset_root)
        self.events = EventManager()
        self.time = TimeManager()
        self.input = InputManager()
        self.ui = UIManager()
        self.audio = AudioManager(self.resources)
        self.music = MusicManager(self.audio)
        self.scene_manager = SceneManager()
        self.context = SceneContext(
            screen=self.screen,
            resources=self.resources,
            scene_manager=self.scene_manager,
            input=self.input,
            ui=self.ui,
            audio=self.audio,
            music=self.music,
        )
        self.scene_manager.bind_context(self.context)
        self.running = True

    def register_scene(self, name: str, factory) -> None:
        self.scene_manager.register(name, factory)

    def start(self, initial_scene: str) -> None:
        self.scene_manager.change(initial_scene)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            events = pygame.event.get()
            events = self.input.process_events(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            scene = self.scene_manager.active_scene
            if scene is None:
                raise RuntimeError("EngineApp started without an active scene")

            scene.process_input(events)
            scene.update(dt)
            scene.render()
            self.scene_manager.update_transition()
            self.scene_manager.draw_transition(self.screen)
            pygame.display.flip()

        self.shutdown()

    def shutdown(self) -> None:
        if self.scene_manager.active_scene is not None:
            self.scene_manager.active_scene.end()
        pygame.quit()
