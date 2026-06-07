from __future__ import annotations

from typing import Callable, Dict, List, Optional

from pygame import Surface

from guigine.ecs.core import Component


class AnimateSprite(Component):
    def __init__(self, animations: Dict[str, List[Surface]], fps: int = 8, loop: bool = True):
        self.animations = animations
        self.fps = fps
        self.default_loop = loop
        self.loop = loop
        self.current_animation: str | None = None
        self.current_frame = 0
        self.time_acc = 0.0
        self.image: Surface | None = None
        self.done = False
        self.on_finish: Optional[Callable[[], None]] = None

    def play(
        self,
        name: str,
        reset: bool = False,
        loop: bool | None = None,
        on_finish: Callable[[], None] | None = None,
    ) -> None:
        if self.current_animation == name and not reset:
            return
        self.current_animation = name
        self.current_frame = 0
        self.time_acc = 0.0
        self.done = False
        self.loop = self.default_loop if loop is None else loop
        self.on_finish = on_finish
        if name in self.animations and self.animations[name]:
            self.image = self.animations[name][0]

    def stop(self) -> None:
        self.done = True

    def is_playing(self) -> bool:
        return not self.done

    def to_dict(self) -> dict:
        return {"type": self.__class__.__name__, "fps": self.fps, "loop": self.loop}
