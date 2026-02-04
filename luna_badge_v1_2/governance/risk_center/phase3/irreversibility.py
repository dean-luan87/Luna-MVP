from typing import Dict, Any

from .schema import RiskIrreversibility


def evaluate_irreversibility(risk: Dict[str, Any], min_brake_time: float = 1.0) -> RiskIrreversibility:
    ttr = risk.get("time_to_risk")
    if ttr is None:
        return RiskIrreversibility.UNKNOWN
    if ttr < min_brake_time:
        return RiskIrreversibility.LIKELY_IRREVERSIBLE
    return RiskIrreversibility.REVERSIBLE
