from __future__ import annotations

from pathlib import Path

import pygame


class ResourceManager:
    def __init__(self, asset_root: str | Path | None = None):
        self.asset_root = Path(asset_root) if asset_root is not None else None
        self._images: dict[tuple[str, tuple[int, int] | None], pygame.Surface] = {}
        self._fonts: dict[tuple[str, int], pygame.font.Font] = {}
        self._sounds: dict[str, pygame.mixer.Sound] = {}

    def resolve(self, relative_path: str | Path) -> Path:
        path = Path(relative_path)
        if path.is_absolute() or self.asset_root is None:
            return path
        return self.asset_root / path

    def load_image(self, relative_path: str | Path, size: tuple[int, int] | None = None) -> pygame.Surface:
        key = (str(relative_path), size)
        if key not in self._images:
            image = pygame.image.load(self.resolve(relative_path)).convert_alpha()
            if size is not None:
                image = pygame.transform.scale(image, size)
            self._images[key] = image
        return self._images[key]

    def load_font(self, relative_path: str | Path, size: int) -> pygame.font.Font:
        key = (str(relative_path), size)
        if key not in self._fonts:
            self._fonts[key] = pygame.font.Font(str(self.resolve(relative_path)), size)
        return self._fonts[key]

    def load_sound(self, relative_path: str | Path) -> pygame.mixer.Sound:
        key = str(relative_path)
        if key not in self._sounds:
            self._sounds[key] = pygame.mixer.Sound(str(self.resolve(relative_path)))
        return self._sounds[key]
