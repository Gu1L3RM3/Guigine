from guigine.components.base import Freeze
from guigine.ecs.core import System


class FreezeSystem(System):
    def __init__(self):
        self._freeze_requests = 0
        self._is_globally_frozen = False

    def request_freeze(self, event=None):
        _ = event
        self._freeze_requests += 1

    def release_freeze(self, event=None):
        _ = event
        self._freeze_requests = max(0, self._freeze_requests - 1)

    def update(self, entity_manager, dt: float):
        _ = dt
        should_be_frozen = self._freeze_requests > 0
        if should_be_frozen == self._is_globally_frozen:
            return
        self._is_globally_frozen = should_be_frozen
        for entity in entity_manager.get_entities_with(Freeze):
            entity.get(Freeze).active = self._is_globally_frozen
