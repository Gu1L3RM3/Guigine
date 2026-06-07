from __future__ import annotations

from typing import Callable, Dict, List, Optional, Type

from guigine.ecs.core import Component, Entity


class EntityManager:
    def __init__(self):
        self._entities: Dict[int, Entity] = {}

    def create(self, *components: Component) -> Entity:
        entity = Entity()
        self.add_entity(entity, *components)
        return entity

    def add_entity(self, entity: Entity, *components: Component) -> None:
        self._entities[entity.id] = entity
        entity.add(*components)

    def remove_entity(self, entity: Entity) -> None:
        self._entities.pop(entity.id, None)

    def clear(self) -> None:
        self._entities.clear()

    def get_entities(self) -> List[Entity]:
        return list(self._entities.values())

    def get_entity_by_id(self, entity_id: int) -> Optional[Entity]:
        return self._entities.get(entity_id)

    def get_entities_with(
        self,
        *component_types: Type[Component],
        filter_fn: Optional[Callable[[Entity], bool]] = None,
    ) -> List[Entity]:
        entities = [
            entity
            for entity in self._entities.values()
            if all(entity.has(component_type) for component_type in component_types)
        ]
        if filter_fn is not None:
            entities = [entity for entity in entities if filter_fn(entity)]
        return entities
