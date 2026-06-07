from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Type, TypeVar
import copy


class Component(ABC):
    def copy(self) -> "Component":
        return copy.deepcopy(self)

    @abstractmethod
    def to_dict(self) -> dict:
        raise NotImplementedError


TComponent = TypeVar("TComponent", bound=Component)


class Entity:
    _next_id = 1

    def __init__(self):
        self.id = Entity._next_id
        Entity._next_id += 1
        self.components: Dict[Type[Component], Component] = {}

    def add(self, *components: Component) -> None:
        for component in components:
            self.components[type(component)] = component

    def remove(self, component_type: Type[Component]) -> None:
        self.components.pop(component_type, None)

    def has(self, component_type: Type[TComponent]) -> bool:
        return component_type in self.components

    def get(self, component_type: Type[TComponent]) -> TComponent:
        component = self.components.get(component_type)
        if component is None:
            raise KeyError(f"{self.__class__.__name__} does not have {component_type.__name__}")
        return component

    def copy(self) -> "Entity":
        new_entity = type(self).__new__(type(self))
        new_entity.id = Entity._next_id
        Entity._next_id += 1
        new_entity.components = {}
        for component in self.components.values():
            new_entity.add(component.copy())
        return new_entity


class System(ABC):
    @abstractmethod
    def update(self, entity_manager: "EntityManager", dt: float) -> None:
        raise NotImplementedError
