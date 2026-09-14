# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-Foundation-001 — Evaluation report schema v0.

Evaluation Tools only:
- Not runtime
- Not whitebox
- Must not auto-mutate mainline decisions
"""

from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Optional


ALLOWED_EVALUATION_TYPES = {
    "ocr_provider_eval",
    "dataset_quality_gate",
    "provider_ab_test",
    "stress_test",
    "chain_test",
}

ALLOWED_RECOMMENDATIONS = {"pass", "weak_pass", "repeat", "fail", "needs_manual_review"}


@dataclasses.dataclass(frozen=True)
class EvaluationReportV0:
    evaluation_id: str
    evaluation_type: str
    module: str  # e.g. "ocr"
    provider: Optional[str]  # e.g. "rapidocr_onnxruntime_v0"
    dataset_ref: Optional[str]
    sample_count: int
    metrics: Dict[str, Any]
    failure_cases_ref: Optional[str]
    human_review_ref: Optional[str]
    recommendation: str
    runtime_integration: bool
    whitebox_integration: bool
    mainline_side_effect: bool
    created_at: str  # ISO-8601 UTC "Z"


def validate_evaluation_report_schema_v0(report: Dict[str, Any]) -> Dict[str, Any]:
    blockers: List[str] = []
    r = report if isinstance(report, dict) else {}

    def req(k: str) -> None:
        if k not in r:
            blockers.append(f"missing:{k}")

    for k in (
        "evaluation_id",
        "evaluation_type",
        "module",
        "metrics",
        "recommendation",
        "runtime_integration",
        "whitebox_integration",
        "mainline_side_effect",
        "created_at",
    ):
        req(k)

    et = r.get("evaluation_type")
    if et is not None and et not in ALLOWED_EVALUATION_TYPES:
        blockers.append(f"invalid:evaluation_type:{et}")

    rec = r.get("recommendation")
    if rec is not None and rec not in ALLOWED_RECOMMENDATIONS:
        blockers.append(f"invalid:recommendation:{rec}")

    # Hard boundaries inside schema itself
    if r.get("runtime_integration") is not False:
        blockers.append("boundary:runtime_integration_must_be_false")
    if r.get("whitebox_integration") is not False:
        blockers.append("boundary:whitebox_integration_must_be_false")
    if r.get("mainline_side_effect") is not False:
        blockers.append("boundary:mainline_side_effect_must_be_false")

    if "metrics" in r and not isinstance(r.get("metrics"), dict):
        blockers.append("invalid:metrics_must_be_object")

    sc = r.get("sample_count")
    if sc is not None:
        try:
            if int(sc) < 0:
                blockers.append("invalid:sample_count_negative")
        except Exception:
            blockers.append("invalid:sample_count_not_int")

    ok = not blockers
    return {"ok": ok, "blockers": blockers}

