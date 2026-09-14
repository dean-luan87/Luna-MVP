# -*- coding: utf-8 -*-
"""Decision Center static validators v1."""

from __future__ import annotations

from typing import Any, Mapping

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.core.micro_os_static_validators_v1 import (
    RUNTIME_BOUNDARY_KEYS,
    validate_candidate_not_fact,
    validate_governance_guard,
    validate_no_runtime_flags,
    validate_required_health_tag,
    validate_required_trace,
)

DC_RUNTIME_BOUNDARY_KEYS = RUNTIME_BOUNDARY_KEYS + (
    "decision_center_runtime_enabled_now",
    "decision_center_mounted_now",
    "output_gate_mounted_now",
    "task_manager_mounted_now",
    "health_watchdog_mounted_now",
)

DC_CANDIDATE_TYPE_NAMES = (
    "DecisionCandidate",
    "DecisionReadinessCandidate",
    "DecisionBlockCandidate",
    "DecisionExplanationCandidate",
    "DownstreamDecisionHandoffCandidate",
)

II_FROZEN_TYPE_NAMES = (
    "DecisionContextCandidate",
    "ConflictCandidate",
    "GapCandidate",
    "RequiredObservationCandidate",
    "PriorityAttentionMapCandidate",
    "InformationAllocationCandidate",
    "TaskWorldSliceCandidate",
    "LiveWorldStateCandidate",
)


def validate_dc_input_contract(obj: Any) -> ValidationResult:
    issues = []
    trace_ref = getattr(obj, "trace_ref", None) or getattr(obj, "trace_id", None)
    if not trace_ref:
        issues.append("missing_trace")
    for check in (validate_candidate_not_fact,):
        result = check(obj)
        if not result.valid:
            issues.extend(result.issues)
    if getattr(obj, "high_risk", False) and not getattr(obj, "governance_check_ref", None):
        issues.append("governance_ref_missing_for_high_risk")
    blocked = "governance_ref_missing_for_high_risk" in issues
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=blocked)


def validate_dc_output_candidate_only(obj: Any) -> ValidationResult:
    fact_status = getattr(obj, "fact_status", None)
    if fact_status and fact_status != "not_fact":
        return ValidationResult(valid=False, issues=("fact_status_not_candidate",), blocked=True)
    return validate_candidate_not_fact(obj)


def validate_dc_decision_not_final_action(obj: Any) -> ValidationResult:
    if getattr(obj, "final_action", False):
        return ValidationResult(valid=False, issues=("final_action_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_dc_no_task_execution(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    if global_b.get("task_execution_now") is True:
        return ValidationResult(valid=False, issues=("task_execution_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_dc_no_user_output(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    if global_b.get("user_output_allowed_now") is True:
        return ValidationResult(valid=False, issues=("user_output_allowed_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_dc_no_memory_worldmodel_write(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    issues = []
    if global_b.get("memory_write_allowed_now") is True:
        issues.append("memory_write_allowed_now")
    if global_b.get("worldmodel_write_allowed_now") is True:
        issues.append("worldmodel_write_allowed_now")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_dc_governance_required_for_high_risk(obj: Any) -> ValidationResult:
    if getattr(obj, "high_risk", False) and not getattr(obj, "governance_check_ref", None):
        return ValidationResult(valid=False, issues=("governance_ref_missing_for_high_risk",), blocked=True)
    return validate_governance_guard(obj)


def validate_dc_health_required(obj: Any) -> ValidationResult:
    if hasattr(obj, "health_refs") and getattr(obj, "readiness_status", None) == "not_ready":
        if not getattr(obj, "health_refs", None):
            return ValidationResult(valid=False, issues=("health_refs_missing",), blocked=True)
    return validate_required_health_tag(obj) if hasattr(obj, "health_tag") else ValidationResult(valid=True)


def validate_dc_no_information_integration_redefinition(obj: Any) -> ValidationResult:
    type_name = type(obj).__name__
    if type_name in II_FROZEN_TYPE_NAMES:
        return ValidationResult(valid=False, issues=("ii_type_redefinition_forbidden",), blocked=True)
    return ValidationResult(valid=True)


def validate_dc_boundary_matrix(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    issues = [k for k in DC_RUNTIME_BOUNDARY_KEYS if global_b.get(k) is True]
    if global_b.get("decision_center_files_created_now") is not True:
        issues.append("decision_center_files_created_now_false")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))
