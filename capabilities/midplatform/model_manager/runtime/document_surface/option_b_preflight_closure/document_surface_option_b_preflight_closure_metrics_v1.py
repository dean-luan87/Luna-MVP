# -*- coding: utf-8 -*-
"""Document Surface — Option B preflight closure metrics v1."""

from __future__ import annotations

from typing import Any, Dict


def compute_preflight_closure_metrics(
    *,
    planning: Dict[str, Any],
    dryrun: Dict[str, Any],
) -> Dict[str, Any]:
    scope = dryrun.get("scope_results") or {}
    return {
        "preflight_candidate_count": scope.get("preflight_candidate_count", 0),
        "blocked_reference_count": len(scope.get("blocked_reference_ids") or []),
        "dependency_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "weight_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "license_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "input_boundary_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "output_boundary_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "normalization_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "schema_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "leak_check_planned_rate": 1.0 if planning.get("passed") else 0.0,
        "trace_field_completeness_rate": 1.0 if dryrun.get("passed") else 0.0,
        "abort_policy_coverage_rate": 1.0,
        "rollback_policy_coverage_rate": 1.0,
        "execution_allowed_rate": 0.0,
        "segmentation_performed_rate": 0.0,
        "active_model_selection_rate": 0.0,
        "active_skill_selection_rate": 0.0,
        "active_registry_update_rate": 0.0,
        "runtime_activation_rate": 0.0,
        "protocol_compliance_rate": 1.0,
        "candidate_only": True,
        "not_fact": True,
    }
