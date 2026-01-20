from typing import Optional

from .interfaces import RiskSignal, WorldSnapshot
from .utils import norm


def evaluate_zone_violation(
    snapshot: WorldSnapshot,
    horizon_sec: float,
) -> Optional[RiskSignal]:
    if horizon_sec <= 0:
        return None

    projected = (
        snapshot.self_position.x + snapshot.self_velocity.x * horizon_sec,
        snapshot.self_position.y + snapshot.self_velocity.y * horizon_sec,
    )
    for zone in snapshot.restricted_zones:
        dist = ((projected[0] - zone.center.x) ** 2 + (projected[1] - zone.center.y) ** 2) ** 0.5
        if dist <= zone.radius:
            return RiskSignal(
                risk_present=True,
                risk_level="HIGH",
                risk_type="ZONE_VIOLATION",
                time_to_risk=horizon_sec,
                confidence=None,
                reason_codes=[],
            )
    return None
