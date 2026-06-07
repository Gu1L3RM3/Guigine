from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from pygame import Vector2

from guigine.ecs.core import Component


@dataclass
class Position(Component):
    x: float = 0.0
    y: float = 0.0
    tile_size: int = 16

    @property
    def pos(self) -> Vector2:
        return Vector2(self.x, self.y)

    @pos.setter
    def pos(self, value: Vector2) -> None:
        self.x = float(value.x)
        self.y = float(value.y)

    @property
    def xy(self) -> Tuple[float, float]:
        return (self.x, self.y)

    @xy.setter
    def xy(self, value: Tuple[float, float]) -> None:
        self.x, self.y = float(value[0]), float(value[1])

    def xy_tuple(self) -> tuple[int, int]:
        return (int(self.x), int(self.y))

    def center_pos(self) -> Vector2:
        half = self.tile_size // 2
        return Vector2(self.x + half, self.y + half)

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "x": self.x, "y": self.y, "tile_size": self.tile_size}


class Velocity(Component):
    def __init__(self, vx: float = 0.0, vy: float = 0.0):
        self._vel = Vector2(vx, vy)

    @property
    def vel(self) -> Vector2:
        return self._vel

    @vel.setter
    def vel(self, value: Vector2) -> None:
        self._vel = Vector2(value)

    @property
    def vx(self) -> float:
        return float(self._vel.x)

    @vx.setter
    def vx(self, value: float) -> None:
        self._vel.x = value

    @property
    def vy(self) -> float:
        return float(self._vel.y)

    @vy.setter
    def vy(self, value: float) -> None:
        self._vel.y = value

    @property
    def vxy(self) -> tuple[float, float]:
        return self._vel.xy

    @vxy.setter
    def vxy(self, value: tuple[float, float]) -> None:
        self._vel.xy = value

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "vx": self.vx, "vy": self.vy}


@dataclass
class RectangleSprite(Component):
    width: int
    height: int
    color: tuple[int, int, int]

    def to_dict(self) -> dict:
        return {"width": self.width, "height": self.height, "color": list(self.color)}


@dataclass
class Freeze(Component):
    active: bool = False

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "active": self.active}


class Health(Component):
    def __init__(self, max_hp: float, current_hp: float | None = None):
        self.max_hp = max(1.0, float(max_hp))
        self.current_hp = self.max_hp if current_hp is None else max(0.0, min(float(current_hp), self.max_hp))

    def take_damage(self, amount: float) -> bool:
        self.current_hp = max(0.0, self.current_hp - max(0.0, float(amount)))
        return self.current_hp <= 0.0

    def heal_full(self) -> None:
        self.current_hp = self.max_hp

    def is_dead(self) -> bool:
        return self.current_hp <= 0.0

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "max_hp": self.max_hp, "current_hp": self.current_hp}
