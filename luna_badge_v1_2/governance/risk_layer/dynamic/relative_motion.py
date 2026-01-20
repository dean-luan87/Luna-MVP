from typing import Optional

from ..interfaces import Vec2
from ..utils import dot, norm, relative_velocity
from .relative_state import RelativeState


def compute_time_to_closest_approach(rel_pos: Vec2, rel_vel: Vec2) -> Optional[float]:
    v2 = rel_vel.x * rel_vel.x + rel_vel.y * rel_vel.y
    if v2 == 0:
        return None
    t = -dot(rel_pos, rel_vel) / v2
    if t < 0:
        return None
    return t


def compute_min_distance(rel_pos: Vec2, rel_vel: Vec2, tca: float) -> float:
    closest = Vec2(rel_pos.x + rel_vel.x * tca, rel_pos.y + rel_vel.y * tca)
    return norm(closest)


def build_relative_state(self_pos: Vec2, self_vel: Vec2, other_pos: Vec2, other_vel: Vec2) -> RelativeState:
    rel_pos = Vec2(other_pos.x - self_pos.x, other_pos.y - self_pos.y)
    rel_vel = relative_velocity(other_vel, self_vel)
    distance = norm(rel_pos)
    closing_speed = 0.0 if distance == 0 else -(dot(rel_pos, rel_vel) / distance)
    return RelativeState(
        rel_pos=rel_pos,
        rel_vel=rel_vel,
        distance=distance,
        closing_speed=closing_speed,
    )


def compute_relative_acceleration(
    self_vel: Vec2,
    self_acc: Optional[Vec2],
    other_vel: Vec2,
    other_acc: Optional[Vec2],
) -> float:
    rel_vel = relative_velocity(other_vel, self_vel)
    speed = norm(rel_vel)
    if speed == 0:
        return 0.0
    rel_acc = relative_velocity(other_acc or Vec2(0.0, 0.0), self_acc or Vec2(0.0, 0.0))
    unit = Vec2(rel_vel.x / speed, rel_vel.y / speed)
    return dot(rel_acc, unit)
