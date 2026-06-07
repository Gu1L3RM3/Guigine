from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable

import pytmx


class EntitySpawner(ABC):
    @abstractmethod
    def spawn(self, obj: pytmx.TiledObject, entity_manager, tilemap):
        raise NotImplementedError


class GenericEntitySpawner(EntitySpawner):
    def __init__(self, factory: Callable[[pytmx.TiledObject, object, object], object | None]):
        self.factory = factory

    def spawn(self, obj: pytmx.TiledObject, entity_manager, tilemap):
        entity = self.factory(obj, entity_manager, tilemap)
        if entity is not None:
            entity_manager.add_entity(entity)
