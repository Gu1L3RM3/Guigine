from __future__ import annotations

from pathlib import Path

import pygame

from guigine.resources.resource_manager import ResourceManager


class AudioManager:
    def __init__(self, resource_manager: ResourceManager | None = None):
        self.enabled = False
        self.resource_manager = resource_manager or ResourceManager()
        self._current_music: str | None = None
        self.vol_music = 0.45
        self.vol_ui = 0.70
        self.vol_sfx = 0.75
        self.vol_ambient = 0.35
        self._init_mixer()

    def _init_mixer(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.enabled = True
            pygame.mixer.set_num_channels(16)
        except pygame.error:
            self.enabled = False

    def set_bus_volume(self, bus: str, value: float):
        value = max(0.0, min(1.0, float(value)))
        if bus == "music":
            self.vol_music = value
            if self.enabled:
                pygame.mixer.music.set_volume(self.vol_music)
        elif bus == "ui":
            self.vol_ui = value
        elif bus == "sfx":
            self.vol_sfx = value
        elif bus == "ambient":
            self.vol_ambient = value

    def play_sfx(self, filename: str, volume: float = 1.0):
        if not self.enabled:
            return
        try:
            sound = self.resource_manager.load_sound(filename)
            sound.set_volume(max(0.0, min(1.0, self.vol_sfx * volume)))
            sound.play()
        except Exception:
            return

    def play_ui(self, filename: str, volume: float = 1.0):
        if not self.enabled:
            return
        try:
            sound = self.resource_manager.load_sound(filename)
            sound.set_volume(max(0.0, min(1.0, self.vol_ui * volume)))
            pygame.mixer.Channel(0).play(sound)
        except Exception:
            return

    def play_music(self, filename: str | None, fade_ms: int = 800, loop: bool = True):
        if not self.enabled:
            return
        if filename is None:
            self.stop_music(fade_ms)
            return
        if self._current_music == filename:
            return
        try:
            resolved = self.resource_manager.resolve(filename)
            if not Path(resolved).exists():
                self._current_music = None
                return
            pygame.mixer.music.load(str(resolved))
            pygame.mixer.music.set_volume(self.vol_music)
            pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
            self._current_music = filename
        except Exception:
            self._current_music = None

    def stop_music(self, fade_ms: int = 600):
        if not self.enabled:
            return
        pygame.mixer.music.fadeout(fade_ms)
        self._current_music = None
