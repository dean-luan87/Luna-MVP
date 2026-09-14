# -*- coding: utf-8 -*-
"""Task Manager static validators v1."""

from __future__ import annotations

from typing import Any, Mapping

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.core.micro_os_static_validators_v1 import RUNTIME_BOUNDARY_KEYS, validate_candidate_not_fact

TM_RUNTIME_BOUNDARY_KEYS = RUNTIME_BOUNDARY_KEYS + (
    "task_manager_runtime_enabled_now",
    "task_manager_mounted_now",
    "task_execution_now",
    "tool_call_now",
    "output_gate_mounted_now",
    "module_adapter_mounted_now",
)

HEALTH_WATCHDOG_TYPE_NAMES = (
    "HealthSignalCandidate",
    "DegradationCandidate",
    "RecoveryRecommendationCandidate",
    "RequiredObservationCandidate",
    "ModuleHealthReviewCandidate",
    "WatchdogHandoffCandidate",
)

DECISION_CENTER_TYPE_NAMES = (
    "DecisionCandidate",
    "DecisionReadinessCandidate",
    "DecisionBlockCandidate",
    "DecisionExplanationCandidate",
    "DownstreamDecisionHandoffCandidate",
)


def _global(boundary_matrix: Mapping[str, Any]) -> Mapping[str, Any]:
    return boundary_matrix.get("global_boundaries") or boundary_matrix


def _value(obj: Any, name: str, default: Any = None) -> Any:
    """Read validator fields from both canonical objects and mappings."""
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_tm_input_contract(obj: Any) -> ValidationResult:
    issues = []
    if not (_value(obj, "trace_ref") or _value(obj, "trace_id")):
        issues.append("missing_trace")
    if _value(obj, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    if _value(obj, "high_risk", False) and not _value(obj, "governance_ref"):
        issues.append("governance_ref_missing_for_high_risk_task")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_tm_output_candidate_only(obj: Any) -> ValidationResult:
    issues = []
    if getattr(obj, "fact_status", "not_fact") != "not_fact":
        issues.append("fact_status_not_candidate")
    if not validate_candidate_not_fact(obj).valid:
        issues.append("candidate_not_fact_false")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_tm_task_not_execution(obj: Any) -> ValidationResult:
    if getattr(obj, "task_execution", False):
        return ValidationResult(valid=False, issues=("task_execution_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_step_not_executed(obj: Any) -> ValidationResult:
    if getattr(obj, "executed_step", False):
        return ValidationResult(valid=False, issues=("executed_step_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_handoff_not_direct_mount(obj: Any) -> ValidationResult:
    if getattr(obj, "direct_mount", False):
        return ValidationResult(valid=False, issues=("direct_mount_not_allowed",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_no_tool_call(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    if _global(boundary_matrix).get("tool_call_now") is True:
        return ValidationResult(valid=False, issues=("tool_call_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_no_user_output(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    if _global(boundary_matrix).get("user_output_allowed_now") is True:
        return ValidationResult(valid=False, issues=("user_output_allowed_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_no_memory_worldmodel_write(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = _global(boundary_matrix)
    issues = []
    if global_b.get("memory_write_allowed_now") is True:
        issues.append("memory_write_allowed_now")
    if global_b.get("worldmodel_write_allowed_now") is True:
        issues.append("worldmodel_write_allowed_now")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_tm_governance_required_for_high_risk_task(obj: Any) -> ValidationResult:
    if getattr(obj, "high_risk", False) and not getattr(obj, "governance_ref", None):
        return ValidationResult(valid=False, issues=("governance_ref_missing_for_high_risk_task",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_no_health_watchdog_redefinition(obj: Any) -> ValidationResult:
    type_name = type(obj).__name__
    if type_name in HEALTH_WATCHDOG_TYPE_NAMES:
        return ValidationResult(valid=True)
    if type_name.startswith("Health") or type_name in {"DegradationCandidate", "RecoveryRecommendationCandidate"}:
        return ValidationResult(valid=False, issues=("health_watchdog_redefinition_forbidden",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_no_decision_center_redefinition(obj: Any) -> ValidationResult:
    type_name = type(obj).__name__
    if type_name in DECISION_CENTER_TYPE_NAMES:
        return ValidationResult(valid=True)
    if type_name.startswith("Decision") or type_name == "DownstreamDecisionHandoffCandidate":
        return ValidationResult(valid=False, issues=("decision_center_redefinition_forbidden",), blocked=True)
    return ValidationResult(valid=True)


def validate_tm_boundary_matrix(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = _global(boundary_matrix)
    issues = [key for key in TM_RUNTIME_BOUNDARY_KEYS if global_b.get(key) is True]
    if global_b.get("task_manager_files_created_now") is not True:
        issues.append("task_manager_files_created_now_false")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))
