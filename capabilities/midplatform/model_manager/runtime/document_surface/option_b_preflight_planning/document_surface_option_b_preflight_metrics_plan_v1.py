# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight metrics plan v1."""

from __future__ import annotations

from typing import Any, Dict


def build_preflight_metrics_plan(*, scope: Dict[str, Any], abort_policy: Dict[str, Any]) -> Dict[str, Any]:
    abort_count = len(abort_policy.get("abort_conditions") or [])
    return {
        "metrics_plan_id": "option_b_preflight_metrics_plan_v1",
        "preflight_candidate_count": scope.get("preflight_candidate_count", 0),
        "dependency_check_planned_rate": 1.0,
        "weight_check_planned_rate": 1.0,
        "license_check_planned_rate": 1.0,
        "input_boundary_check_planned_rate": 1.0,
        "output_boundary_check_planned_rate": 1.0,
        "normalization_check_planned_rate": 1.0,
        "schema_check_planned_rate": 1.0,
        "leak_check_planned_rate": 1.0,
        "trace_field_completeness_planned_rate": 1.0,
        "abort_policy_coverage_rate": 1.0 if abort_count >= 16 else round(abort_count / 16, 4),
        "rollback_policy_coverage_rate": 1.0,
        "execution_allowed_rate": 0.0,
        "active_model_selection_rate": 0.0,
        "active_registry_update_rate": 0.0,
        "protocol_compliance_planned_rate": 1.0,
        "abort_condition_count": abort_count,
        "candidate_only": True,
        "not_fact": True,
    }
