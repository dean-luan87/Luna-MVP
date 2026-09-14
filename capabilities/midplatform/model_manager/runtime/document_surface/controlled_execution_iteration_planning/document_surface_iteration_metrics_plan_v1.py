# -*- coding: utf-8 -*-
"""Document Surface — iteration metrics plan v1."""

from __future__ import annotations

from typing import Any, Dict, List

NEW_METRICS = (
    "overlap_separation_candidate_rate",
    "relation_hint_evidence_compliance_rate",
    "false_relation_guard_rate",
    "excessive_candidate_suppression_rate",
    "low_contrast_uncertainty_rate",
    "attached_to_uncertainty_rate",
    "candidate_quality_gate_pass_rate",
    "fake_relation_rate",
    "forced_multi_surface_rate",
)

RETAINED_METRICS = (
    "no_ocr_leak_rate",
    "no_fact_output_rate",
    "no_fallback_rate",
    "attention_blocked_runtime_call_rate",
    "trace_completeness_rate",
    "output_boundary_compliance_rate",
)


def build_iteration_metrics_plan() -> Dict[str, Any]:
    return {
        "plan_id": "document_surface_iteration_metrics_plan_v1",
        "new_metrics": list(NEW_METRICS),
        "retained_metrics": list(RETAINED_METRICS),
        "targets": {
            "fake_relation_rate": 0.0,
            "forced_multi_surface_rate": 0.0,
            "no_ocr_leak_rate": 1.0,
            "no_fact_output_rate": 1.0,
            "no_fallback_rate": 1.0,
            "attention_blocked_runtime_call_rate": 0.0,
            "trace_completeness_rate": 1.0,
            "output_boundary_compliance_rate": 1.0,
        },
        "accuracy_not_primary_admission_criterion": True,
        "quality_relation_noise_focus": True,
        "planning_only": True,
        "candidate_only": True,
        "not_fact": True,
    }
