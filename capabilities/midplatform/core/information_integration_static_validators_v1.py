# -*- coding: utf-8 -*-
"""Information Integration static validators v1."""

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
    validate_required_ttl,
)

II_RUNTIME_BOUNDARY_KEYS = RUNTIME_BOUNDARY_KEYS + (
    "information_integration_runtime_enabled_now",
    "information_integration_mounted_now",
    "output_gate_mounted_now",
    "decision_center_mounted_now",
    "health_watchdog_mounted_now",
)

CANDIDATE_TYPE_NAMES = (
    "LiveWorldStateCandidate",
    "TaskWorldSliceCandidate",
    "PriorityAttentionMapCandidate",
    "InformationAllocationCandidate",
    "ConflictCandidate",
    "GapCandidate",
    "RequiredObservationCandidate",
    "DecisionContextCandidate",
)


def validate_ii_input_contract(obj: Any) -> ValidationResult:
    issues = []
    for check in (validate_required_trace, validate_required_health_tag, validate_required_ttl, validate_candidate_not_fact):
        result = check(obj)
        if not result.valid:
            issues.extend(result.issues)
    blocked = "ttl_missing" in issues or "missing_health_tag" in issues
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=blocked)


def validate_ii_output_candidate_only(obj: Any) -> ValidationResult:
    fact_status = getattr(obj, "fact_status", None)
    if fact_status and fact_status != "not_fact":
        return ValidationResult(valid=False, issues=("fact_status_not_candidate",), blocked=True)
    return validate_candidate_not_fact(obj)


def validate_ii_no_fact_write(obj: Any) -> ValidationResult:
    if getattr(obj, "write_allowed", False) or getattr(obj, "fact_promoted", False):
        return ValidationResult(valid=False, issues=("fact_write_attempted",), blocked=True)
    return ValidationResult(valid=True)


def validate_ii_no_memory_worldmodel_write(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    issues = []
    if global_b.get("memory_write_allowed_now") is True:
        issues.append("memory_write_allowed_now")
    if global_b.get("worldmodel_write_allowed_now") is True:
        issues.append("worldmodel_write_allowed_now")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_ii_no_user_output(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    if global_b.get("user_output_allowed_now") is True:
        return ValidationResult(valid=False, issues=("user_output_allowed_now",), blocked=True)
    return ValidationResult(valid=True)


def validate_ii_recall_context_hint_only(recall_context: Mapping[str, Any]) -> ValidationResult:
    issues = []
    if recall_context.get("promoted_to_fact"):
        issues.append("recall_promoted_to_fact")
    if recall_context.get("overrides_realtime_safety"):
        issues.append("recall_overrides_realtime_safety")
    if not recall_context.get("hint_only") and not recall_context.get("known_state_candidate"):
        issues.append("recall_not_hint_only")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_ii_governance_required_for_high_risk(obj: Any) -> ValidationResult:
    if getattr(obj, "high_risk", False) and not getattr(obj, "governance_check_ref", None):
        return ValidationResult(valid=False, issues=("governance_ref_missing_for_high_risk",), blocked=True)
    return validate_governance_guard(obj)


def validate_ii_health_required(obj: Any) -> ValidationResult:
    return validate_required_health_tag(obj)


def validate_ii_boundary_matrix(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    issues = [k for k in II_RUNTIME_BOUNDARY_KEYS if global_b.get(k) is True]
    if global_b.get("information_integration_files_created_now") is not True:
        issues.append("information_integration_files_created_now_false")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))
