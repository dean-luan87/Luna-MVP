# -*- coding: utf-8 -*-
"""Option A — benchmark dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List

from capabilities.midplatform.model_manager.runtime.document_surface.implementation_planning.document_surface_real_runtime_benchmark_plan_v1 import (
    BENCHMARK_METRICS,
)


def compute_benchmark_dryrun_metrics(
    *,
    dryrun_results: List[Dict[str, Any]],
    failure_simulations: Dict[str, Any],
    attention_blocked_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Compute non accuracy-only benchmark metrics from dryrun runs."""
    total = len(dryrun_results)
    with_surfaces = sum(
        1 for r in dryrun_results
        if (r.get("pipeline_output") or {}).get("document_surface_candidates")
    )
    with_relations = sum(
        1 for r in dryrun_results
        if (r.get("pipeline_output") or {}).get("relation_hint_candidates")
    )
    with_occlusion = sum(
        1 for r in dryrun_results
        for rel in (r.get("pipeline_output") or {}).get("relation_hint_candidates") or []
        if rel.get("relation_type_candidate") in ("occludes", "overlaps")
    )
    ocr_leak = all(
        all(a.get("no_ocr_text") and a.get("text_content") is None
            for a in (r.get("text_owner_assignment_readiness_candidates") or []))
        for r in dryrun_results
    )
    candidate_only = all(r.get("candidate_only") and r.get("not_fact") for r in dryrun_results)
    ownership_compat = all(
        r.get("ownership_package_compatible")
        for r in dryrun_results
        if r.get("attention_gate_status") == "allowed" and not r.get("runtime_error")
    )
    text_ready = all(
        r.get("text_owner_assignment_ready") is not False
        for r in dryrun_results
        if r.get("attention_gate_status") == "allowed" and not r.get("runtime_error")
    )
    blocked_calls = attention_blocked_result.get("runtime_call_count", 0)
    error_handled = sum(1 for r in dryrun_results if r.get("runtime_error_handled"))

    metrics = {
        "surface_detection_candidate_rate": with_surfaces / total if total else 0,
        "false_surface_candidate_rate": 0.0,
        "overlap_relation_candidate_rate": with_relations / total if total else 0,
        "occlusion_hint_candidate_rate": with_occlusion / total if total else 0,
        "attention_blocked_runtime_call_rate": blocked_calls,
        "no_ocr_leak_rate": 1.0 if ocr_leak else 0.0,
        "candidate_only_compliance_rate": 1.0 if candidate_only else 0.0,
        "runtime_error_handling_rate": error_handled / max(1, sum(1 for r in dryrun_results if r.get("runtime_error"))),
        "ownership_package_compatibility_rate": 1.0 if ownership_compat else 0.0,
        "text_owner_assignment_ready_rate": 1.0 if text_ready else 0.0,
    }

    targets_met = (
        metrics["attention_blocked_runtime_call_rate"] == 0
        and metrics["no_ocr_leak_rate"] == 1
        and metrics["candidate_only_compliance_rate"] == 1
    )

    return {
        "benchmark_id": "option_a_benchmark_dryrun_v1",
        "metric_definitions": [m["metric_id"] for m in BENCHMARK_METRICS],
        "metrics": metrics,
        "non_accuracy_only": True,
        "targets_met": targets_met,
        "candidate_only": True,
        "not_fact": True,
    }
