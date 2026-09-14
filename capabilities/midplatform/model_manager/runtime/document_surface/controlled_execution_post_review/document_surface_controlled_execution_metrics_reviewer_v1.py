# -*- coding: utf-8 -*-
"""Document Surface Controlled Execution — metrics reviewer v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

METRICS_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/"
    "controlled_execution_metrics_summary.json"
)
DRYRUN_SUMMARY_REL = (
    "_tmp_eval_out/p1_midplatform_luna_model_manager_region_intelligence_ownership_document_surface_detector_real_runtime_controlled_execution_dryrun_v1/"
    "controlled_execution_dryrun_summary.json"
)

REQUIRED_METRICS = {
    "no_ocr_leak_rate": 1.0,
    "no_fact_output_rate": 1.0,
    "no_fallback_rate": 1.0,
    "attention_blocked_runtime_call_rate": 0.0,
    "trace_completeness_rate": 1.0,
    "output_boundary_compliance_rate": 1.0,
}


def review_controlled_execution_metrics(*, repo_root: Path) -> Dict[str, Any]:
    metrics: Dict[str, Any] = {}
    summary: Dict[str, Any] = {}
    mp = repo_root / METRICS_REL
    sp = repo_root / DRYRUN_SUMMARY_REL
    if mp.is_file():
        metrics = json.loads(mp.read_text(encoding="utf-8"))
    if sp.is_file():
        summary = json.loads(sp.read_text(encoding="utf-8"))

    metric_checks = {k: metrics.get(k) == v for k, v in REQUIRED_METRICS.items()}
    protocol_rate_ok = metrics.get("protocol_compliance_rate", 0) >= 1.0

    registry_items = metrics.get("total_registry_cases") or summary.get("fixture_audit", {}).get("total_registry_entries")
    executed_cases = metrics.get("executed_case_count")
    count_explanation = {
        "registry_item_count": registry_items,
        "dryrun_case_count": executed_cases,
        "mismatch": registry_items != executed_cases if registry_items is not None and executed_cases is not None else None,
        "explanation": (
            "registry items 按 manifest 图片条目计数（含 negative fixtures）；"
            "dryrun cases 按 A–H 测试行为计数，Case F attention blocked 不对应真实图片，"
            "故 case_count 可大于 registry execution image count。"
        ),
        "risk_id": "registry_item_count_case_count_mismatch_explained",
        "blocker": False,
    }

    passed = all(metric_checks.values()) and protocol_rate_ok
    return {
        "review_id": "controlled_execution_metrics_review_v1",
        "metrics": metrics,
        "metric_checks": metric_checks,
        "protocol_compliance_rate_ok": protocol_rate_ok,
        "count_explanation": count_explanation,
        "review_passed_count": sum(1 for v in metric_checks.values() if v) + (1 if protocol_rate_ok else 0),
        "review_failed_count": sum(1 for v in metric_checks.values() if not v) + (0 if protocol_rate_ok else 1),
        "passed": passed,
        "candidate_only": True,
        "not_fact": True,
    }
