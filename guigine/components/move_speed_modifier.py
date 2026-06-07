from guigine.ecs.core import Component


class MoveSpeedModifier(Component):
    def __init__(self, multiplier: float = 1.0):
        self.multiplier = float(multiplier)

    def to_dict(self):
        return {"type": self.__class__.__name__, "multiplier": self.multiplier}
