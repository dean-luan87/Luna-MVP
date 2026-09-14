# -*- coding: utf-8 -*-
"""Region Intelligence Ownership DryRun Metrics v1."""

from __future__ import annotations

from typing import Any, Dict

_metrics: Dict[str, Any] = {
    "entity_discovery_count": 0,
    "selective_activation_count": 0,
    "global_ocr_blocked_count": 0,
    "missing_reasoning_count": 0,
    "semantic_conflict_count": 0,
    "handoff_success_rate": 0.0,
    "_handoffs": 0,
    "_handoff_ok": 0,
}


def reset_ownership_dryrun_metrics() -> None:
    global _metrics
    _metrics = {
        "entity_discovery_count": 0,
        "selective_activation_count": 0,
        "global_ocr_blocked_count": 0,
        "missing_reasoning_count": 0,
        "semantic_conflict_count": 0,
        "handoff_success_rate": 0.0,
        "_handoffs": 0,
        "_handoff_ok": 0,
    }


def record_entity_discovery() -> None:
    _metrics["entity_discovery_count"] += 1


def record_selective_activation(*, not_all_models: bool) -> None:
    _metrics["selective_activation_count"] += 1
    if not_all_models:
        _metrics["global_ocr_blocked_count"] += 1


def record_missing_reasoning() -> None:
    _metrics["missing_reasoning_count"] += 1


def record_semantic_conflict() -> None:
    _metrics["semantic_conflict_count"] += 1


def record_handoff(*, success: bool) -> None:
    _metrics["_handoffs"] += 1
    if success:
        _metrics["_handoff_ok"] += 1
    total = _metrics["_handoffs"] or 1
    _metrics["handoff_success_rate"] = _metrics["_handoff_ok"] / total


def get_ownership_dryrun_metrics() -> Dict[str, Any]:
    return {k: v for k, v in _metrics.items() if not k.startswith("_")}
