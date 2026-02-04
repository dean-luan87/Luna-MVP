from typing import List, Dict, Any

from .schema import RiskAcceleration


_SPIKE_THRESHOLD = 5.0


def evaluate_acceleration(history: List[Dict[str, Any]]) -> RiskAcceleration:
    if len(history) < 3:
        return RiskAcceleration.UNKNOWN

    deltas = []
    for idx in range(1, len(history)):
        prev = history[idx - 1].get("time_to_risk")
        curr = history[idx].get("time_to_risk")
        if prev is None or curr is None:
            continue
        delta = prev - curr
        if abs(delta) > _SPIKE_THRESHOLD:
            continue
        deltas.append(delta)

    if len(deltas) < 2:
        return RiskAcceleration.UNKNOWN

    avg = sum(deltas) / len(deltas)
    if avg > 0.1:
        return RiskAcceleration.INCREASING
    if avg < -0.1:
        return RiskAcceleration.DECREASING
    return RiskAcceleration.STABLE
