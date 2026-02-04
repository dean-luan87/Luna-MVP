from typing import Optional, Tuple

from ...risk_layer.interfaces import Vec2
from .schema import RelativeState


def _dot(a: Vec2, b: Vec2) -> float:
    return a.x * b.x + a.y * b.y


def _norm_sq(v: Vec2) -> float:
    return v.x * v.x + v.y * v.y


def compute_relative_velocity(state: RelativeState) -> Vec2:
    return Vec2(state.other_velocity.x - state.self_velocity.x, state.other_velocity.y - state.self_velocity.y)


def compute_tca_and_dca(state: RelativeState) -> Tuple[Optional[float], float]:
    rel_pos = Vec2(state.other_position.x - state.self_position.x, state.other_position.y - state.self_position.y)
    rel_vel = compute_relative_velocity(state)
    denom = _norm_sq(rel_vel)
    if denom < 1e-6:
        return None, (_norm_sq(rel_pos) ** 0.5)
    t_ca = -_dot(rel_pos, rel_vel) / denom
    closest = Vec2(rel_pos.x + rel_vel.x * t_ca, rel_pos.y + rel_vel.y * t_ca)
    d_ca = (_norm_sq(closest) ** 0.5)
    return t_ca, d_ca
