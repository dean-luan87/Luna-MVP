from dataclasses import dataclass
from typing import Optional

from ..interfaces import Vec2
from .relative_motion import (
    build_relative_state,
    compute_min_distance,
    compute_time_to_closest_approach,
    compute_relative_acceleration,
)


_CLOSING_SPEED_EPS = 0.05


@dataclass(frozen=True)
class RiskEvent:
    type: str
    level: str
    time_to_risk: float
    closing_speed: float


def evaluate_vo_lite(
    self_pos: Vec2,
    self_vel: Vec2,
    other_pos: Vec2,
    other_vel: Vec2,
    horizon_sec: float,
    danger_radius: float,
    self_acc: Optional[Vec2] = None,
    other_acc: Optional[Vec2] = None,
) -> Optional[RiskEvent]:
    state = build_relative_state(self_pos, self_vel, other_pos, other_vel)
    if abs(state.closing_speed) < _CLOSING_SPEED_EPS:
        return None

    tca = compute_time_to_closest_approach(state.rel_pos, state.rel_vel)
    if tca is None or tca <= 0 or tca > horizon_sec:
        return None

    min_dist = compute_min_distance(state.rel_pos, state.rel_vel, tca)
    if min_dist > danger_radius:
        return None

    rel_acc = compute_relative_acceleration(self_vel, self_acc, other_vel, other_acc)
    if state.closing_speed > 0 and rel_acc < 0:
        level = "MEDIUM"
    else:
        level = "HIGH" if tca <= horizon_sec / 2 else "MEDIUM"
    return RiskEvent(
        type="RELATIVE_MOTION",
        level=level,
        time_to_risk=tca,
        closing_speed=state.closing_speed,
    )
