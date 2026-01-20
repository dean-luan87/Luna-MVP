from typing import Dict, List, Any, Optional
import time

from .schema import EvaluationMetrics, SCHEMA_VERSION


_ENVELOPE_ORDER = {
    "WITHIN_ENVELOPE": 1,
    "SAFE_ENOUGH": 2,
    "ADMISSIBLE": 3,
    "UNACCEPTABLE": 4,
}


def _rank(mapping: Dict[str, int], value: Optional[str], default: int) -> int:
    if value is None:
        return default
    return mapping.get(value, default)


def evaluate_metrics(timeline: List[Dict[str, Any]], window: str) -> EvaluationMetrics:
    if not timeline:
        return EvaluationMetrics(
            schema_version=SCHEMA_VERSION,
            window=window,
            metrics={},
            sample_size=0,
            generated_at=time.time(),
        )

    authority_levels = [item.get("authority_panel", {}).get("effective") for item in timeline]
    envelope_statuses = [item.get("envelope", {}).get("status") for item in timeline]
    time_to_risk = [
        item.get("risk_panel", {}).get("time_to_risk")
        for item in timeline
        if item.get("risk_panel", {}).get("time_to_risk") is not None
    ]

    oscillations = sum(
        1 for idx in range(1, len(authority_levels)) if authority_levels[idx] != authority_levels[idx - 1]
    )
    authority_oscillation_rate = oscillations / max(len(authority_levels) - 1, 1)

    boundary_hits = sum(1 for status in envelope_statuses if status and status != "WITHIN_ENVELOPE")
    envelope_boundary_hit_rate = boundary_hits / max(len(envelope_statuses), 1)

    avg_time_to_risk = sum(time_to_risk) / len(time_to_risk) if time_to_risk else 0.0
    min_time_to_risk = min(time_to_risk) if time_to_risk else 0.0

    metrics = {
        "authority_oscillation_rate": round(authority_oscillation_rate, 4),
        "envelope_boundary_hit_rate": round(envelope_boundary_hit_rate, 4),
        "avg_time_to_risk": round(avg_time_to_risk, 4),
        "min_time_to_risk": round(min_time_to_risk, 4),
    }

    return EvaluationMetrics(
        schema_version=SCHEMA_VERSION,
        window=window,
        metrics=metrics,
        sample_size=len(timeline),
        generated_at=time.time(),
    )
