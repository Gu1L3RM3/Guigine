from __future__ import annotations

from dataclasses import dataclass

import pygame

from guigine.managers.audio_manager import AudioManager
from guigine.managers.input_manager import InputManager
from guigine.managers.music_manager import MusicManager
from guigine.managers.ui_manager import UIManager
from guigine.resources.resource_manager import ResourceManager


@dataclass(slots=True)
class SceneContext:
    screen: pygame.Surface
    resources: ResourceManager
    scene_manager: "SceneManager"
    input: InputManager
    ui: UIManager
    audio: AudioManager
    music: MusicManager
