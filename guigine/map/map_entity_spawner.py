from __future__ import annotations

from typing import Dict

import pytmx

from guigine.components.base import Position
from guigine.components.collider import Collider
from guigine.components.sprite import Sprite
from guigine.ecs.core import Entity
from guigine.ecs.entity_manager import EntityManager
from guigine.map.spawners.spawn import EntitySpawner, GenericEntitySpawner
from guigine.map.tile_map import TileMap


class MapEntitySpawner:
    def __init__(self, spawn_tile_layer_entities: bool = True):
        self._spawners: Dict[str, EntitySpawner] = {}
        self.spawn_tile_layer_entities = spawn_tile_layer_entities

    def register_spawner(self, layer_name: str, spawner: EntitySpawner):
        self._spawners[layer_name.lower()] = spawner

    def register_factory(self, layer_name: str, factory):
        self.register_spawner(layer_name, GenericEntitySpawner(factory))

    def spawn_entities(self, tilemap: TileMap, entity_manager: EntityManager):
        if self.spawn_tile_layer_entities:
            tilemap.draw_static_object_layers = False
            for layer in tilemap.tmx_data.visible_layers:
                if isinstance(layer, pytmx.TiledTileLayer) and layer.name and layer.name.lower() in ("obj", "obj2"):
                    self._spawn_from_tile_layer(layer, tilemap, entity_manager)
        else:
            tilemap.draw_static_object_layers = True

        for layer in tilemap.tmx_data.objectgroups:
            layer_name = (layer.name or "").lower()
            spawner = self._spawners.get(layer_name)
            if spawner and isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    spawner.spawn(obj, entity_manager, tilemap)

    def _spawn_from_tile_layer(self, layer: pytmx.TiledTileLayer, tilemap: TileMap, entity_manager: EntityManager):
        for x, y, gid in layer:
            if isinstance(gid, int) and gid != 0:
                image = tilemap.tmx_data.get_tile_image_by_gid(gid)
                entity = Entity()
                if image:
                    entity.add(Sprite(image))
                entity.add(Position(x * tilemap.tile_width, y * tilemap.tile_height), Collider(tilemap.tile_width, tilemap.tile_height))
                entity_manager.add_entity(entity)
