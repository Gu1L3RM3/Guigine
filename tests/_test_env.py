from __future__ import annotations

import os
import sys
from pathlib import Path


TESTS_DIR = Path(__file__).resolve().parent
ENGINE_ROOT = TESTS_DIR.parent
ASSET_ROOT = ENGINE_ROOT / "examples" / "assets"

if str(ENGINE_ROOT) not in sys.path:
    sys.path.insert(0, str(ENGINE_ROOT))

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame


def bootstrap_pygame() -> None:
    if not pygame.get_init():
        pygame.init()
    if not pygame.font.get_init():
        pygame.font.init()
    if pygame.display.get_surface() is None:
        pygame.display.set_mode((320, 240))


def shutdown_pygame() -> None:
    pygame.quit()
