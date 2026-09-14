# -*- coding: utf-8 -*-
"""Health Watchdog static validators v1."""

from __future__ import annotations

from typing import Any, Mapping

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.core.micro_os_static_validators_v1 import (
    RUNTIME_BOUNDARY_KEYS,
    validate_candidate_not_fact,
)

HW_RUNTIME_BOUNDARY_KEYS = RUNTIME_BOUNDARY_KEYS + (
    "health_watchdog_runtime_enabled_now",
    "health_watchdog_mounted_now",
    "recovery_execution_now",
    "module_restart_now",
    "process_control_now",
    "output_gate_mounted_now",
    "task_manager_mounted_now",
)

DECISION_CENTER_FROZEN_TYPE_NAMES = (
    "DecisionCandidate",
    "DecisionReadinessCandidate",
    "DecisionBlockCandidate",
    "DecisionExplanationCandidate",
    "DownstreamDecisionHandoffCandidate",
)


def _global(boundary_matrix: Mapping[str, Any]) -> Mapping[str, Any]:
    return boundary_matrix.get("global_boundaries") or boundary_matrix


def validate_hw_input_contract(obj: Any) -> ValidationResult:
    issues = []
    if not (getattr(obj, "trace_ref", None) or getattr(obj, "trace_id", None)):
        issues.append("missing_trace")
    if getattr(obj, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    if getattr(obj, "governance_required", False) and not (
        getattr(obj, "governance_ref", None) or getattr(obj, "governance_check_ref", None)
    ):
        issues.append("governance_ref_missing_for_high_risk")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_hw_output_candidate_only(obj: Any) -> ValidationResult:
    issues = []
    if getattr(obj, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_hw_no_recovery_execution(obj: Any) -> ValidationResult:
    if getattr(obj, "recovery_execution", False):
        return ValidationResult(valid=False, issues=("recovery_execution_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_no_restart(obj: Any) -> ValidationResult:
    if getattr(obj, "restart_allowed", False):
        return ValidationResult(valid=False, issues=("restart_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_no_process_control(obj: Any) -> ValidationResult:
    if getattr(obj, "process_control_allowed", False):
        return ValidationResult(valid=False, issues=("process_control_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_no_task_execution(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    if _global(boundary_matrix).get("task_execution_now") is True:
        return ValidationResult(valid=False, issues=("task_execution_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_no_user_output(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    if _global(boundary_matrix).get("user_output_allowed_now") is True:
        return ValidationResult(valid=False, issues=("user_output_allowed_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_no_memory_worldmodel_write(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = _global(boundary_matrix)
    issues = []
    if global_b.get("memory_write_allowed_now") is True:
        issues.append("memory_write_allowed_now")
    if global_b.get("worldmodel_write_allowed_now") is True:
        issues.append("worldmodel_write_allowed_now")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_hw_governance_required_for_high_risk_recovery(obj: Any) -> ValidationResult:
    if getattr(obj, "governance_required", False) and not getattr(obj, "governance_ref", None):
        return ValidationResult(valid=False, issues=("governance_ref_missing_for_high_risk_recovery",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_no_decision_center_redefinition(obj: Any) -> ValidationResult:
    type_name = type(obj).__name__
    if type_name in DECISION_CENTER_FROZEN_TYPE_NAMES:
        return ValidationResult(valid=True)
    if type_name.startswith("Decision") or type_name == "DownstreamDecisionHandoffCandidate":
        return ValidationResult(valid=False, issues=("decision_center_redefinition_forbidden",), blocked=True)
    return ValidationResult(valid=True)


def validate_hw_boundary_matrix(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = _global(boundary_matrix)
    issues = [k for k in HW_RUNTIME_BOUNDARY_KEYS if global_b.get(k) is True]
    if global_b.get("health_watchdog_files_created_now") is not True:
        issues.append("health_watchdog_files_created_now_false")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))
