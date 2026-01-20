from typing import Optional

from .interfaces import RiskSignal, Vec2, WorldSnapshot
from .utils import norm, relative_velocity, time_to_closest_approach


def evaluate_dynamic_collision(
    snapshot: WorldSnapshot,
    horizon_sec: float,
) -> Optional[RiskSignal]:
    if horizon_sec <= 0:
        return None

    self_pos = snapshot.self_position
    self_vel = snapshot.self_velocity

    for obj in snapshot.objects:
        if obj.velocity is None:
            continue
        if norm(obj.velocity) == 0:
            continue

        rel_pos = (
            obj.position.x - self_pos.x,
            obj.position.y - self_pos.y,
        )
        rel_vel = relative_velocity(obj.velocity, self_vel)
        t = time_to_closest_approach(
            p_rel=Vec2(rel_pos[0], rel_pos[1]),
            v_rel=rel_vel,
        )
        if t is None or t > horizon_sec:
            continue

        closest_self = (
            self_pos.x + self_vel.x * t,
            self_pos.y + self_vel.y * t,
        )
        closest_obj = (
            obj.position.x + obj.velocity.x * t,
            obj.position.y + obj.velocity.y * t,
        )
        dist = ((closest_self[0] - closest_obj[0]) ** 2 + (closest_self[1] - closest_obj[1]) ** 2) ** 0.5
        if dist <= obj.radius:
            return RiskSignal(
                risk_present=True,
                risk_level="HIGH",
                risk_type="DYNAMIC_COLLISION",
                time_to_risk=t,
                confidence=None,
                reason_codes=[],
            )

    return None
