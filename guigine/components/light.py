from guigine.ecs.core import Component


class LightComponent(Component):
    def __init__(self, light_on: bool = True, radius: int = 25):
        self.light_on = light_on
        self.radius = radius

    def to_dict(self):
        return {"type": self.__class__.__name__, "light_on": self.light_on, "radius": self.radius}
