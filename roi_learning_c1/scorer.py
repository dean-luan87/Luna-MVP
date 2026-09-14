from __future__ import annotations

from typing import Any, Dict


def _norm_appear(appear_count: int) -> float:
    return min(1.0, max(0.0, appear_count / 50.0))


def _inv_latency(avg_latency_s: float | None) -> float:
    if avg_latency_s is None:
        return 0.0
    return 1.0 / (1.0 + max(0.0, avg_latency_s))


def score_evidence(e: Dict[str, Any]) -> float:
    """
    v0 linear, explainable scoring.
    """
    hit_rate = float(e.get("hit_rate") or 0.0)
    appear = int(e.get("appear_count") or 0)
    avg_latency = e.get("avg_latency_s", None)
    stability = float(e.get("stability") or 0.0)

    s = (
        0.4 * hit_rate
        + 0.3 * _norm_appear(appear)
        + 0.2 * _inv_latency(avg_latency)
        + 0.1 * stability
    )
    return max(0.0, min(1.0, s))
