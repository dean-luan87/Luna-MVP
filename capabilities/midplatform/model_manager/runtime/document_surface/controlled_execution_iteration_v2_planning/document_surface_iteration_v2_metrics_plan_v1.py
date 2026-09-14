# -*- coding: utf-8 -*-
"""Document Surface — iteration v2 metrics plan v1."""

from __future__ import annotations

from typing import Any, Dict, List


def build_iteration_v2_metrics_plan() -> Dict[str, Any]:
    new_metrics: List[str] = [
        "option_a_candidate_quality_score",
        "option_b_candidate_quality_score",
        "a_b_conflict_rate",
        "validation_review_rate",
        "route_selection_trace_completeness_rate",
        "option_b_no_fact_compliance_rate",
        "option_b_no_ocr_leak_rate",
        "option_b_no_vlm_leak_rate",
        "option_b_dependency_admission_status",
    ]
    retained_metrics: List[str] = [
        "fake_relation_rate",
        "forced_multi_surface_rate",
        "no_ocr_leak_rate",
        "no_fact_output_rate",
        "no_fallback_rate",
        "attention_blocked_runtime_call_rate",
        "protocol_compliance_rate",
    ]
    retained_targets = {
        "fake_relation_rate": 0.0,
        "forced_multi_surface_rate": 0.0,
        "no_ocr_leak_rate": 1.0,
        "no_fact_output_rate": 1.0,
        "no_fallback_rate": 1.0,
        "attention_blocked_runtime_call_rate": 0.0,
        "protocol_compliance_rate": 1.0,
    }
    return {
        "plan_id": "document_surface_iteration_v2_metrics_plan_v1",
        "new_route_level_metrics": new_metrics,
        "retained_governance_metrics": retained_metrics,
        "retained_targets": retained_targets,
        "route_level_metrics_complete": len(new_metrics) >= 9,
        "candidate_only": True,
        "not_fact": True,
    }
