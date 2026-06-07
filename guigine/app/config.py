from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class EngineConfig:
    width: int = 1280
    height: int = 720
    title: str = "Guigine"
    fps: int = 60
    asset_root: str | Path | None = None
