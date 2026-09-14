# -*- coding: utf-8 -*-
"""OCR Recognition Runtime Metrics v1 — region_to_text_success_rate, not accuracy."""

from __future__ import annotations

from typing import Any, Dict

_metrics: Dict[str, Any] = {
    "region_to_text_success_rate": 0.0,
    "low_confidence_rate": 0.0,
    "unsupported_claim_rate": 0.0,
    "latency_ms": 0.0,
    "cost_units": 0.0,
    "human_correction_rate": 0.0,
    "slot_selected_count": 0,
    "slot_noop_count": 0,
    "runtime_error_count": 0,
    "_region_attempts": 0,
    "_region_successes": 0,
    "_low_confidence_count": 0,
    "_unsupported_claim_count": 0,
}


def reset_ocr_runtime_metrics() -> None:
    global _metrics
    _metrics = {
        "region_to_text_success_rate": 0.0,
        "low_confidence_rate": 0.0,
        "unsupported_claim_rate": 0.0,
        "latency_ms": 0.0,
        "cost_units": 0.0,
        "human_correction_rate": 0.0,
        "slot_selected_count": 0,
        "slot_noop_count": 0,
        "runtime_error_count": 0,
        "_region_attempts": 0,
        "_region_successes": 0,
        "_low_confidence_count": 0,
        "_unsupported_claim_count": 0,
    }


def record_ocr_slot_selected() -> None:
    _metrics["slot_selected_count"] += 1


def record_ocr_slot_noop() -> None:
    _metrics["slot_noop_count"] += 1


def record_ocr_region_attempt(*, success: bool, low_confidence: bool = False, unsupported: bool = False) -> None:
    _metrics["_region_attempts"] += 1
    if success:
        _metrics["_region_successes"] += 1
    if low_confidence:
        _metrics["_low_confidence_count"] += 1
    if unsupported:
        _metrics["_unsupported_claim_count"] += 1
    _recompute_rates()


def record_ocr_runtime_error() -> None:
    _metrics["runtime_error_count"] += 1


def record_ocr_latency(*, latency_ms: float, cost_units: float = 0.0) -> None:
    _metrics["latency_ms"] = latency_ms
    _metrics["cost_units"] = cost_units


def _recompute_rates() -> None:
    attempts = _metrics["_region_attempts"] or 1
    _metrics["region_to_text_success_rate"] = _metrics["_region_successes"] / attempts
    _metrics["low_confidence_rate"] = _metrics["_low_confidence_count"] / attempts
    _metrics["unsupported_claim_rate"] = _metrics["_unsupported_claim_count"] / attempts


def get_ocr_runtime_metrics() -> Dict[str, Any]:
    return {
        "region_to_text_success_rate": _metrics["region_to_text_success_rate"],
        "low_confidence_rate": _metrics["low_confidence_rate"],
        "unsupported_claim_rate": _metrics["unsupported_claim_rate"],
        "latency_ms": _metrics["latency_ms"],
        "cost_units": _metrics["cost_units"],
        "human_correction_rate": _metrics["human_correction_rate"],
        "slot_selected_count": _metrics["slot_selected_count"],
        "slot_noop_count": _metrics["slot_noop_count"],
        "runtime_error_count": _metrics["runtime_error_count"],
    }
