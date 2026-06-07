from __future__ import annotations

from pygame import Rect, Vector2

from guigine.ecs.core import Component


class PathFollower(Component):
    def __init__(self, path: list[tuple[int, int]], speed: float = 40, loop: bool = False, tile_size: int = 16):
        self.path: list[tuple[int, int]] = []
        self.original_path = list(path)
        self.current_index = 0
        self.speed = speed
        self.loop = loop
        self.tile_size = tile_size
        self.reach_radius = max(3.0, tile_size * 0.35)
        self.direction = Vector2(0, 0)
        self.done = True
        self.collision_rects: list[Rect] = []
        self.set_path(path)

    def restart_path(self) -> None:
        self.set_path(self.original_path)
        self.done = False

    def create_collision_rects(self) -> None:
        self.collision_rects = []
        for point in self.path:
            x = (point[0] * self.tile_size) + self.tile_size // 2
            y = (point[1] * self.tile_size) + self.tile_size // 2
            self.collision_rects.append(Rect((x, y), (2, 2)))

    def set_path(self, new_path: list[tuple[int, int]]) -> None:
        path_copy = list(new_path)
        if len(path_copy) > 1:
            path_copy.pop(0)
        self.path = path_copy
        self.done = not bool(self.path)
        self.direction = Vector2(0, 0)
        self.create_collision_rects()

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "path": self.path, "speed": self.speed}
