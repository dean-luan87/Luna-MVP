from typing import Optional

from .interfaces import Vec2


def norm(v: Vec2) -> float:
    return (v.x * v.x + v.y * v.y) ** 0.5


def dot(a: Vec2, b: Vec2) -> float:
    return a.x * b.x + a.y * b.y


def relative_velocity(v1: Vec2, v2: Vec2) -> Vec2:
    return Vec2(v1.x - v2.x, v1.y - v2.y)


def time_to_closest_approach(p_rel: Vec2, v_rel: Vec2) -> Optional[float]:
    v2 = v_rel.x * v_rel.x + v_rel.y * v_rel.y
    if v2 == 0:
        return None
    t = -dot(p_rel, v_rel) / v2
    if t < 0:
        return 0.0
    return t
