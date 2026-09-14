# -*- coding: utf-8 -*-
"""Text Detection Runtime Metrics — usage not accuracy v1."""

from __future__ import annotations

from typing import Any, Dict


_METRICS: Dict[str, Any] = {
    "slot_selected_count": 0,
    "slot_noop_count": 0,
    "invalid_activation_count": 0,
    "handoff_success_count": 0,
    "handoff_attempt_count": 0,
    "evidence_quality_scores": [],
}


def record_slot_selected() -> None:
    _METRICS["slot_selected_count"] += 1


def record_slot_noop() -> None:
    _METRICS["slot_noop_count"] += 1


def record_invalid_activation() -> None:
    _METRICS["invalid_activation_count"] += 1


def record_handoff(*, success: bool, evidence_quality: float = 0.0) -> None:
    _METRICS["handoff_attempt_count"] += 1
    if success:
        _METRICS["handoff_success_count"] += 1
    _METRICS["evidence_quality_scores"].append(evidence_quality)


def get_runtime_usage_metrics() -> Dict[str, Any]:
    attempts = _METRICS["handoff_attempt_count"] or 1
    scores = _METRICS["evidence_quality_scores"]
    return {
        "slot_selected_count": _METRICS["slot_selected_count"],
        "slot_noop_count": _METRICS["slot_noop_count"],
        "invalid_activation_count": _METRICS["invalid_activation_count"],
        "handoff_success_rate": round(_METRICS["handoff_success_count"] / attempts, 3),
        "evidence_quality_score": round(sum(scores) / len(scores), 3) if scores else 0.0,
        "metrics_type": "runtime_usage_not_model_accuracy",
        "candidate_only": True,
    }


def reset_runtime_metrics() -> None:
    for k in _METRICS:
        if isinstance(_METRICS[k], list):
            _METRICS[k] = []
        else:
            _METRICS[k] = 0
