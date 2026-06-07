from __future__ import annotations

from pathlib import Path

import pygame
import pytmx

from guigine.utils.navigation import NavGrid, PathFinder


class TileMap:
    def __init__(self, tmx_data: pytmx.TiledMap, walk_layer_name: str = "ground2"):
        self.tmx_data = tmx_data
        self.tmx_file = Path(tmx_data.filename).stem if getattr(tmx_data, "filename", None) else "map"
        self.tile_width = tmx_data.tilewidth
        self.tile_height = tmx_data.tileheight
        self.map_width = tmx_data.width * self.tile_width
        self.map_height = tmx_data.height * self.tile_height
        self.spawn_points: dict[str, tuple[int, int]] = {}
        self.waypoints: dict[str, tuple[int, int]] = {}
        self.ground_surface: pygame.Surface | None = None
        self.object_surface: pygame.Surface | None = None
        self.foreground_surface: pygame.Surface | None = None
        self.solid_colliders: list[pygame.Rect] = []
        self.draw_static_object_layers = True
        self.navgrid = NavGrid(self.tmx_data, self.tile_width, self.tile_height, walk_layer_name=walk_layer_name)
        self.pathfinder = PathFinder(self.navgrid)

    def get_tile_from_position(self, pos) -> tuple[int, int]:
        return (int(pos.x // self.tile_width), int(pos.y // self.tile_height))

    def get_spawn_point(self, name: str) -> tuple[int, int] | None:
        return self.spawn_points.get(name.lower())

    def get_waypoint_tile(self, name: str) -> tuple[int, int] | None:
        return self.waypoints.get(name.lower())
