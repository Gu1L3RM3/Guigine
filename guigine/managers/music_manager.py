from __future__ import annotations

from guigine.managers.audio_manager import AudioManager


class MusicManager:
    def __init__(self, audio_manager: AudioManager):
        self.audio_manager = audio_manager
        self.current_track: str | None = None

    def play(self, filename: str | None, fade_ms: int = 800, loop: bool = True):
        self.current_track = filename
        self.audio_manager.play_music(filename, fade_ms=fade_ms, loop=loop)

    def stop(self, fade_ms: int = 600):
        self.current_track = None
        self.audio_manager.stop_music(fade_ms=fade_ms)

    def set_volume(self, value: float):
        self.audio_manager.set_bus_volume("music", value)
