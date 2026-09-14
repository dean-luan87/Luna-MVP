# -*- coding: utf-8 -*-
"""Information Processing Core static validators v1 — static validation only."""

from __future__ import annotations

from typing import Any, Mapping, Tuple

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.information_processing_core_contracts_v1 import (
    INFORMATION_TYPE_CONTRACT,
    NON_EXECUTION_CONTRACT,
    WORKLOAD_CONTRACT,
    check_information_type_contract,
    check_io_input_contract,
    check_io_output_contract,
    check_non_execution_contract,
    check_traceability_contract,
    check_workload_contract,
)
from capabilities.midplatform.information_processing_core_types_v1 import (
    InformationProcessingResultCandidate,
    InformationType,
)

STATIC_VALIDATOR_FUNCTIONS: Tuple[str, ...] = (
    "validate_raw_information_input",
    "validate_information_type_signal",
    "validate_information_candidate",
    "validate_classification_candidate",
    "validate_traceability_refs",
    "validate_governance_refs",
    "validate_non_execution_boundary",
    "validate_unknown_classification_allowed",
    "validate_forbidden_side_effects_absent",
    "validate_core_not_constrained_by_peripheral_contract",
    "validate_processing_result_candidate",
    "validate_workload_control",
)

FORBIDDEN_SIDE_EFFECT_FLAGS: Tuple[str, ...] = (
    "record_created", "grant_issued", "authorization_request_created",
    "runtime_executed", "whitebox_called", "route_executed", "handoff_executed",
    "promotion_executed", "persistent_write_executed",
)


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def validate_raw_information_input(obj: Any) -> ValidationResult:
    ok, issues = check_io_input_contract(obj)
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def validate_information_type_signal(obj: Any) -> ValidationResult:
    issues = []
    detected = _value(obj, "detected_type", "")
    ok, type_issues = check_information_type_contract(detected)
    issues.extend(type_issues)
    if not _value(obj, "signal_id"):
        issues.append("signal_id_missing")
    out_ok, out_issues = check_io_output_contract(obj)
    issues.extend(out_issues)
    if not out_ok:
        ok = False
    return ValidationResult(valid=ok and out_ok, issues=tuple(issues), blocked=not ok)


def validate_information_candidate(obj: Any) -> ValidationResult:
    issues = []
    ok, out_issues = check_io_output_contract(obj)
    issues.extend(out_issues)
    trace_ok, trace_issues = check_traceability_contract(obj)
    issues.extend(trace_issues)
    valid = ok and trace_ok
    return ValidationResult(valid=valid, issues=tuple(issues), blocked=not valid)


def validate_classification_candidate(obj: Any) -> ValidationResult:
    issues = []
    info_type = _value(obj, "information_type", "")
    ok, type_issues = check_information_type_contract(info_type)
    issues.extend(type_issues)
    out_ok, out_issues = check_io_output_contract(obj)
    issues.extend(out_issues)
    valid = ok and out_ok
    return ValidationResult(valid=valid, issues=tuple(issues), blocked=not valid)


def validate_traceability_refs(obj: Any) -> ValidationResult:
    ok, issues = check_traceability_contract(obj)
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def validate_governance_refs(obj: Any) -> ValidationResult:
    return ValidationResult(valid=True, issues=(), blocked=False)


def validate_non_execution_boundary(obj: Any) -> ValidationResult:
    flags = {k: _value(obj, k, NON_EXECUTION_CONTRACT.get(k)) for k in NON_EXECUTION_CONTRACT if k != "contract_id"}
    flags.update({
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": _value(obj, "real_execution", False) is False,
        "no_route_execution": True,
        "no_real_handoff_execution": True,
        "no_candidate_promotion_execution": True,
        "no_whitebox_runtime_call": True,
        "no_persistent_write": True,
    })
    ok, issues = check_non_execution_contract(flags)
    if _value(obj, "candidate_only", True) is not True:
        issues = tuple(list(issues) + ["candidate_only_not_true"])
        ok = False
    if _value(obj, "side_effect_allowed", False) is not False:
        issues = tuple(list(issues) + ["side_effect_allowed_not_false"])
        ok = False
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def validate_unknown_classification_allowed(obj: Any) -> ValidationResult:
    detected = _value(obj, "detected_type", _value(obj, "information_type", ""))
    if detected == InformationType.UNKNOWN_INFORMATION.value:
        if INFORMATION_TYPE_CONTRACT.get("unknown_information_allowed") is not True:
            return ValidationResult(valid=False, issues=("unknown_not_allowed",), blocked=True)
    return ValidationResult(valid=True, issues=(), blocked=False)


def validate_forbidden_side_effects_absent(obj: Any) -> ValidationResult:
    issues = [f for f in FORBIDDEN_SIDE_EFFECT_FLAGS if _value(obj, f, False) is True]
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_core_not_constrained_by_peripheral_contract(obj: Any) -> ValidationResult:
    issues = []
    if _value(obj, "handoff_contract_required", False) is True:
        issues.append("handoff_contract_should_not_be_required")
    if _value(obj, "integration_contract_required", False) is True:
        issues.append("integration_contract_should_not_be_required")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_processing_result_candidate(obj: Any) -> ValidationResult:
    issues = []
    ok, out_issues = check_io_output_contract(obj)
    issues.extend(out_issues)
    trace_ok, trace_issues = check_traceability_contract(obj)
    issues.extend(trace_issues)
    if isinstance(obj, InformationProcessingResultCandidate):
        if not obj.validation_pass and obj.processing_status not in ("reject", "defer", "unknown"):
            issues.append("validation_pass_inconsistent")
    valid = ok and trace_ok and len(issues) == 0
    return ValidationResult(valid=valid, issues=tuple(issues), blocked=not valid)


def validate_workload_control(flags: Mapping[str, bool]) -> ValidationResult:
    ok, issues = check_workload_contract(flags)
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def run_all_static_validators(obj: Any) -> Tuple[ValidationResult, ...]:
    return (
        validate_raw_information_input(obj),
        validate_non_execution_boundary(obj),
        validate_forbidden_side_effects_absent(obj),
        validate_core_not_constrained_by_peripheral_contract(obj),
    )
