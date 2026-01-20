from typing import Optional

from ...risk_layer.interfaces import WorldSnapshot
from .schema import RelativeState, RiskProjectionVO
from .relative import compute_tca_and_dca


def evaluate_vo(
    snapshot: WorldSnapshot,
    horizon_sec: float = 3.0,
    safety_radius: float = 0.6,
) -> RiskProjectionVO:
    best_time: Optional[float] = None
    best_dist: Optional[float] = None

    for obj in snapshot.objects:
        other_velocity = obj.velocity or snapshot.self_velocity.__class__(0.0, 0.0)
        state = RelativeState(
            self_position=snapshot.self_position,
            self_velocity=snapshot.self_velocity,
            other_position=obj.position,
            other_velocity=other_velocity,
        )
        t_ca, d_ca = compute_tca_and_dca(state)
        if t_ca is None:
            continue
        if t_ca < 0 or t_ca > horizon_sec:
            continue
        if d_ca < max(safety_radius, obj.radius):
            if best_time is None or t_ca < best_time:
                best_time = t_ca
                best_dist = d_ca

    if best_time is None:
        return RiskProjectionVO(time_to_risk=None, min_distance=None, level="NONE")

    return RiskProjectionVO(time_to_risk=best_time, min_distance=best_dist, level="HIGH")
