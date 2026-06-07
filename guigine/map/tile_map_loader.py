from __future__ import annotations

import pygame
import pytmx
from pytmx.util_pygame import load_pygame

from guigine.map.tile_map import TileMap
from guigine.resources.resource_manager import ResourceManager


class TileMapLoader:
    def __init__(self, resource_manager: ResourceManager, walk_layer_name: str = "ground2"):
        self.resource_manager = resource_manager
        self.walk_layer_name = walk_layer_name

    def load(self, tmx_filename: str) -> TileMap:
        tmx_path = self.resource_manager.resolve(("maps", tmx_filename)) if isinstance(tmx_filename, tuple) else self.resource_manager.resolve(f"maps/{tmx_filename}")
        tmx_data: pytmx.TiledMap = load_pygame(str(tmx_path), pixelalpha=True)
        tilemap = TileMap(tmx_data, walk_layer_name=self.walk_layer_name)
        rel_path = tmx_filename.replace("fases/", "").replace(".tmx", "")
        tilemap.tmx_file = rel_path
        tilemap.ground_surface = self._build_surface_for_layers(tmx_data, tilemap, ("ground", "ground2", "ground3"))
        tilemap.object_surface = self._build_surface_for_layers(tmx_data, tilemap, ("obj",))
        tilemap.foreground_surface = self._build_surface_for_layers(tmx_data, tilemap, ("obj2",))
        tilemap.solid_colliders = self._collect_tile_colliders(tmx_data, tilemap, ("obj", "obj2"))
        self._collect_spawn_points(tilemap)
        for layer in self._iter_layers(tmx_data, "waypoints", pytmx.TiledObjectGroup):
            for obj in layer:
                name = (obj.name or "").lower()
                if not name:
                    continue
                tx = int(obj.x // tilemap.tile_width)
                ty = int(obj.y // tilemap.tile_height)
                tilemap.waypoints[name] = (tx, ty)
        return tilemap

    def _iter_layers(self, tmx_data, names: str | tuple[str, ...], layer_type):
        if isinstance(names, str):
            names = (names,)
        lowered = tuple(name.lower() for name in names)
        for layer in tmx_data.layers:
            if isinstance(layer, layer_type) and layer.name and layer.name.lower() in lowered:
                yield layer

    def _iter_visible_layers(self, tmx_data, names: str | tuple[str, ...], layer_type):
        for layer in self._iter_layers(tmx_data, names, layer_type):
            if getattr(layer, "visible", True):
                yield layer

    def _build_surface_for_layers(self, tmx_data: pytmx.TiledMap, tilemap: TileMap, layer_names: tuple[str, ...]) -> pygame.Surface:
        surface = pygame.Surface((tilemap.map_width, tilemap.map_height)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for layer in self._iter_visible_layers(tmx_data, layer_names, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if not isinstance(gid, int) or gid == 0:
                    continue
                image = tmx_data.get_tile_image_by_gid(gid)
                if image:
                    surface.blit(image, (x * tilemap.tile_width, y * tilemap.tile_height))
        return surface

    def _collect_tile_colliders(self, tmx_data: pytmx.TiledMap, tilemap: TileMap, layer_names: tuple[str, ...]) -> list[pygame.Rect]:
        occupied_cells: set[tuple[int, int]] = set()
        for layer in self._iter_visible_layers(tmx_data, layer_names, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                if isinstance(gid, int) and gid != 0:
                    occupied_cells.add((x, y))
        tw = tilemap.tile_width
        th = tilemap.tile_height
        return [pygame.Rect(x * tw, y * th, tw, th) for (x, y) in occupied_cells]

    def _collect_spawn_points(self, tilemap: TileMap) -> None:
        for layer in self._iter_layers(tilemap.tmx_data, ("spawn_points", "spawns"), pytmx.TiledObjectGroup):
            for obj in layer:
                name = (obj.name or "").strip().lower()
                if not name:
                    continue
                tilemap.spawn_points[name] = (int(obj.x), int(obj.y))
