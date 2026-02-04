from typing import Optional

from .interfaces import RiskSignal, WorldSnapshot
from .utils import norm


def evaluate_static_collision(
    snapshot: WorldSnapshot,
    horizon_sec: float,
) -> Optional[RiskSignal]:
    if horizon_sec <= 0:
        return None

    self_pos = snapshot.self_position
    self_vel = snapshot.self_velocity
    speed = norm(self_vel)
    if speed == 0:
        return None

    for obj in snapshot.objects:
        if obj.velocity is not None and norm(obj.velocity) > 0:
            continue

        rel_pos = (obj.position.x - self_pos.x, obj.position.y - self_pos.y)
        v = self_vel
        v2 = v.x * v.x + v.y * v.y
        if v2 == 0:
            continue

        t = (rel_pos[0] * v.x + rel_pos[1] * v.y) / v2
        if t < 0:
            t = 0.0
        if t > horizon_sec:
            continue

        closest_x = self_pos.x + v.x * t
        closest_y = self_pos.y + v.y * t
        dist = ((closest_x - obj.position.x) ** 2 + (closest_y - obj.position.y) ** 2) ** 0.5
        if dist <= obj.radius:
            return RiskSignal(
                risk_present=True,
                risk_level="HIGH",
                risk_type="STATIC_COLLISION",
                time_to_risk=t,
                confidence=None,
                reason_codes=[],
            )

    return None
