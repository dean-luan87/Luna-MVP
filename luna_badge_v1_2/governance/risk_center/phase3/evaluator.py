from typing import List, Dict, Any

from .schema import RiskPhase3Output, RiskAcceleration, RiskCurvature, RiskIrreversibility
from .acceleration import evaluate_acceleration
from .curvature import evaluate_curvature
from .irreversibility import evaluate_irreversibility


def evaluate_phase3(risk_history: List[Dict[str, Any]]) -> RiskPhase3Output:
    try:
        acc = evaluate_acceleration(risk_history)
    except Exception:
        acc = RiskAcceleration.UNKNOWN

    try:
        vo_history = [item.get("vo", {}) for item in risk_history]
        curv = evaluate_curvature(vo_history)
    except Exception:
        curv = RiskCurvature.UNKNOWN

    try:
        latest = risk_history[-1] if risk_history else {}
        irr = evaluate_irreversibility(latest)
    except Exception:
        irr = RiskIrreversibility.UNKNOWN

    return RiskPhase3Output(
        acceleration=acc,
        curvature=curv,
        irreversibility=irr,
    )
