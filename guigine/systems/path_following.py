from pygame import Vector2

from guigine.components.animation import AnimateSprite
from guigine.components.base import Freeze, Position, Velocity
from guigine.components.path_follower import PathFollower
from guigine.ecs.core import System


class PathFollowingSystem(System):
    def update(self, entity_manager, dt: float):
        for entity in entity_manager.get_entities_with(PathFollower, Position, Velocity):
            path_follower = entity.get(PathFollower)
            position = entity.get(Position)
            velocity = entity.get(Velocity)
            if self._is_frozen(entity):
                velocity.vel.update(0, 0)
                continue
            if path_follower.done:
                if path_follower.loop:
                    path_follower.restart_path()
                else:
                    velocity.vel.update(0, 0)
                continue
            if not path_follower.collision_rects:
                path_follower.done = True
                velocity.vel.update(0, 0)
                continue
            self._update_path_progress(path_follower, position, dt)
            self._apply_velocity(path_follower, velocity)
            if path_follower.done and path_follower.loop:
                path_follower.restart_path()
                velocity.vel.update(0, 0)
                continue
            if path_follower.done:
                velocity.vel.update(0, 0)
                continue
            if entity.has(AnimateSprite) and hasattr(entity, "set_direction"):
                entity.set_direction(path_follower.direction)

    def _is_frozen(self, entity) -> bool:
        return entity.get(Freeze).active if entity.has(Freeze) else False

    def _update_path_progress(self, path_follower: PathFollower, position: Position, dt: float):
        if not path_follower.collision_rects:
            path_follower.done = True
            path_follower.direction = Vector2(0, 0)
            return
        center = position.center_pos()
        dynamic_reach = max(path_follower.reach_radius, path_follower.speed * dt + 1.0)
        while path_follower.collision_rects:
            target_rect = path_follower.collision_rects[0]
            to_target = Vector2(target_rect.center) - center
            if to_target.length_squared() > (dynamic_reach * dynamic_reach):
                break
            path_follower.collision_rects.pop(0)
        if not path_follower.collision_rects:
            path_follower.done = True
            path_follower.direction = Vector2(0, 0)
            return
        target_rect = path_follower.collision_rects[0]
        path_follower.done = False
        path_follower.direction = self._calculate_direction(center, target_rect)

    def _calculate_direction(self, start_vec: Vector2, target_rect) -> Vector2:
        direction = Vector2(target_rect.center) - start_vec
        return direction.normalize() if direction.length_squared() > 0 else Vector2()

    def _apply_velocity(self, path_follower: PathFollower, velocity: Velocity):
        velocity.vel = path_follower.direction * path_follower.speed
