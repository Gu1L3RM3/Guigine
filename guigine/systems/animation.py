from guigine.components.animation import AnimateSprite
from guigine.components.sprite import Sprite
from guigine.ecs.core import System


class AnimationSystem(System):
    def update(self, entity_manager, dt: float) -> None:
        entities = entity_manager.get_entities_with(Sprite, AnimateSprite)
        for entity in entities:
            animation = entity.get(AnimateSprite)
            sprite = entity.get(Sprite)
            if animation.current_animation is None or animation.done:
                continue
            frames = animation.animations.get(animation.current_animation, [])
            if not frames:
                continue
            animation.time_acc += dt
            frame_duration = 1.0 / animation.fps
            while animation.time_acc >= frame_duration:
                animation.time_acc -= frame_duration
                animation.current_frame += 1
                if animation.current_frame >= len(frames):
                    if animation.loop:
                        animation.current_frame = 0
                    else:
                        animation.current_frame = len(frames) - 1
                        animation.done = True
                        if animation.on_finish:
                            animation.on_finish()
                            animation.on_finish = None
                        break
            animation.current_frame = min(animation.current_frame, len(frames) - 1)
            sprite.image = frames[animation.current_frame]
