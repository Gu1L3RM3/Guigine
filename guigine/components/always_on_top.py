from guigine.ecs.core import Component


class AlwaysOnTop(Component):
    def to_dict(self):
        return {"type": self.__class__.__name__}
