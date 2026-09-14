# -*- coding: utf-8 -*-
"""Micro-OS static validators v1 — boundary / governance / health guards."""

from __future__ import annotations

from typing import Any, Mapping

from capabilities.midplatform.core.micro_os_common_types_v1 import (
    Event,
    HealthIssueCandidate,
    ValidationResult,
    WorkingMemoryEntry,
)

RUNTIME_BOUNDARY_KEYS = (
    "real_event_bus_enabled_now",
    "real_working_memory_enabled_now",
    "real_scheduler_enabled_now",
    "real_async_queue_enabled_now",
    "true_multithreading_enabled_now",
    "runtime_enabled_now",
    "model_invoked_now",
    "provider_invoked_now",
    "task_execution_now",
    "memory_write_allowed_now",
    "worldmodel_write_allowed_now",
    "user_output_allowed_now",
    "real_health_monitoring_enabled_now",
    "recovery_executed_now",
)


def validate_no_runtime_flags(boundary_matrix: Mapping[str, Any]) -> ValidationResult:
    global_b = boundary_matrix.get("global_boundaries") or boundary_matrix
    issues = [k for k in RUNTIME_BOUNDARY_KEYS if global_b.get(k) is True]
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues))


def validate_candidate_not_fact(obj: Any) -> ValidationResult:
    if hasattr(obj, "candidate_not_fact"):
        ok = getattr(obj, "candidate_not_fact") is True
        return ValidationResult(valid=ok, issues=() if ok else ("candidate_not_fact_false",))
    if isinstance(obj, Mapping):
        ok = obj.get("candidate_not_fact") is True or obj.get("candidate_only") is True
        return ValidationResult(valid=ok, issues=() if ok else ("candidate_not_fact_false",))
    return ValidationResult(valid=True)


def validate_required_trace(obj: Any) -> ValidationResult:
    trace_id = getattr(obj, "trace_id", None) or (obj.get("trace_id") if isinstance(obj, Mapping) else None)
    ok = bool(trace_id)
    return ValidationResult(valid=ok, issues=() if ok else ("missing_trace_id",))


def validate_required_health_tag(obj: Any) -> ValidationResult:
    if isinstance(obj, Event):
        ok = obj.health_tag is not None
        return ValidationResult(valid=ok, issues=() if ok else ("missing_health_tag",), blocked=not ok)
    if isinstance(obj, Mapping):
        ok = bool(obj.get("health_tag"))
        return ValidationResult(valid=ok, issues=() if ok else ("missing_health_tag",), blocked=not ok)
    return ValidationResult(valid=True)


def validate_required_ttl(obj: Any) -> ValidationResult:
    if isinstance(obj, WorkingMemoryEntry):
        ok = obj.ttl is not None
        return ValidationResult(valid=ok, issues=() if ok else ("ttl_missing",), blocked=not ok)
    if isinstance(obj, Event):
        ok = obj.ttl_hint is not None
        return ValidationResult(valid=ok, issues=() if ok else ("ttl_missing",), blocked=not ok)
    if isinstance(obj, Mapping):
        ok = obj.get("ttl") is not None or obj.get("ttl_hint") is not None
        return ValidationResult(valid=ok, issues=() if ok else ("ttl_missing",), blocked=not ok)
    return ValidationResult(valid=True)


def validate_governance_guard(obj: Any) -> ValidationResult:
    if isinstance(obj, Event):
        if obj.governance_required and (obj.governance_check_ref is None or not obj.governance_check_ref.cleared):
            return ValidationResult(valid=False, issues=("governance_not_cleared",), blocked=True)
        return ValidationResult(valid=True)
    if isinstance(obj, Mapping):
        if obj.get("governance_required") and not obj.get("governance_check_ref"):
            return ValidationResult(valid=False, issues=("governance_not_cleared",), blocked=True)
    return ValidationResult(valid=True)


def health_issue_from_validation(result: ValidationResult, signal: str) -> HealthIssueCandidate:
    return HealthIssueCandidate(signal=signal, severity="warning" if not result.blocked else "error", blocked=result.blocked)
