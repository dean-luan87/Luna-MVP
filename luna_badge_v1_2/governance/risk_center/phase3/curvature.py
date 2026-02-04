from typing import List, Dict, Any

from .schema import RiskCurvature


def evaluate_curvature(vo_history: List[Dict[str, Any]]) -> RiskCurvature:
    if len(vo_history) < 3:
        return RiskCurvature.UNKNOWN

    trend = 0
    valid = 0
    for idx in range(1, len(vo_history)):
        prev = vo_history[idx - 1].get("min_distance")
        curr = vo_history[idx].get("min_distance")
        if prev is None or curr is None:
            continue
        valid += 1
        if curr < prev:
            trend += 1
        elif curr > prev:
            trend -= 1

    if valid < 2:
        return RiskCurvature.UNKNOWN
    if trend > 1:
        return RiskCurvature.TOWARD_RISK
    if trend < -1:
        return RiskCurvature.AWAY_FROM_RISK
    return RiskCurvature.STABLE
