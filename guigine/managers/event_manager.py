from __future__ import annotations

from collections import defaultdict

import pygame


class EventManager:
    def __init__(self):
        self._listeners = defaultdict(list)

    def clear(self) -> None:
        self._listeners.clear()

    def subscribe(self, event_type: str, listener: callable) -> None:
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener: callable) -> None:
        if listener in self._listeners[event_type]:
            self._listeners[event_type].remove(listener)

    def post(self, events) -> None:
        if isinstance(events, list):
            for event in events:
                name = pygame.event.event_name(event.type)
                for listener in tuple(self._listeners.get(name, ())):
                    listener(event)
        elif isinstance(events, dict) and "type" in events:
            for listener in tuple(self._listeners.get(events["type"], ())):
                listener(events)
