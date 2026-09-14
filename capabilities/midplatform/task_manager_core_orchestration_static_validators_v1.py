# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration static validators v1 — static validation only."""

from __future__ import annotations

from typing import Any, Mapping, Optional, Tuple

from capabilities.midplatform.core.micro_os_common_types_v1 import ValidationResult
from capabilities.midplatform.task_manager_core_orchestration_contracts_v1 import (
    NON_EXECUTION_CONTRACT,
    check_allowed_candidate_output_contract,
    check_governance_contract,
    check_io_output_contract,
    check_non_execution_contract,
    check_traceability_contract,
)
from capabilities.midplatform.task_manager_core_orchestration_types_v1 import (
    OrchestrationResultCandidate,
)

FORBIDDEN_SIDE_EFFECT_FLAGS: Tuple[str, ...] = (
    "route_execution",
    "handoff_execution",
    "promotion_execution",
    "record_created",
    "grant_issued",
    "authorization_request_created",
    "runtime_executed",
    "whitebox_called",
)

FUTURE_DESIGN_MODULES: Tuple[str, ...] = (
    "drive_brain",
    "reflection_brain",
    "task_center_runtime",
    "whitebox_runtime",
    "module_adapter_runtime",
)


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def _refs(obj: Any, name: str) -> Tuple[str, ...]:
    val = _value(obj, name, ())
    if val is None:
        return ()
    if isinstance(val, str):
        return (val,)
    return tuple(str(v) for v in val)


def validate_boundary_refs(obj: Any) -> ValidationResult:
    issues = []
    ref = _value(obj, "boundary_registry_ref", "")
    if not ref:
        issues.append("boundary_registry_ref_missing")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_lifecycle_state_refs(obj: Any) -> ValidationResult:
    issues = []
    ref = _value(obj, "lifecycle_state_ref", "")
    if not ref:
        issues.append("lifecycle_state_ref_missing")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_alignment_rule_refs(obj: Any) -> ValidationResult:
    issues = []
    ref = _value(obj, "alignment_rule_ref", "")
    if not ref:
        issues.append("alignment_rule_ref_missing")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_governance_constraint_refs(obj: Any) -> ValidationResult:
    issues = []
    ref = _value(obj, "governance_constraint_ref", "")
    gov_refs = _refs(obj, "governance_refs")
    if not ref and not gov_refs:
        issues.append("governance_constraint_ref_missing")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_traceability_refs(obj: Any) -> ValidationResult:
    ok, issues = check_traceability_contract(obj)
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def validate_non_execution_boundary(obj: Any) -> ValidationResult:
    flags = {k: _value(obj, k, NON_EXECUTION_CONTRACT.get(k)) for k in NON_EXECUTION_CONTRACT if k != "contract_id"}
    flags.update({
        "no_record_creation": True,
        "no_grant_creation": True,
        "no_authorization_request_creation": True,
        "no_runtime_execution": _value(obj, "real_execution", False) is False,
        "no_route_execution": _value(obj, "route_execution", False) is False,
        "no_real_handoff_execution": _value(obj, "handoff_execution", False) is False,
        "no_owner_approval_request_reopen": True,
        "no_candidate_promotion_execution": _value(obj, "promotion_execution", False) is False,
        "no_whitebox_runtime_call": True,
    })
    ok, issues = check_non_execution_contract(flags)
    if _value(obj, "candidate_only", True) is not True:
        issues = tuple(list(issues) + ["candidate_only_not_true"])
        ok = False
    if _value(obj, "side_effect_allowed", False) is not False:
        issues = tuple(list(issues) + ["side_effect_allowed_not_false"])
        ok = False
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def validate_candidate_only_outputs(obj: Any) -> ValidationResult:
    ok, issues = check_io_output_contract(obj)
    type_name = type(obj).__name__
    allowed_ok, allowed_issues = check_allowed_candidate_output_contract(type_name)
    if not allowed_ok:
        issues = tuple(list(issues) + list(allowed_issues))
        ok = False
    return ValidationResult(valid=ok, issues=issues, blocked=not ok)


def validate_forbidden_side_effects_absent(obj: Any) -> ValidationResult:
    issues = []
    for flag in FORBIDDEN_SIDE_EFFECT_FLAGS:
        if _value(obj, flag, False) is True:
            issues.append(f"{flag}_present")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_owner_approval_request_chain_not_reopened(obj: Any) -> ValidationResult:
    issues = []
    refs = _refs(obj, "governance_refs") + _refs(obj, "traceability_refs")
    for ref in refs:
        lowered = ref.lower()
        if "owner_approval_request_reopen" in lowered or "reopen_owner_approval" in lowered:
            issues.append("owner_approval_request_chain_reopen_detected")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_future_design_not_implemented(obj: Any) -> ValidationResult:
    issues = []
    module_ref = str(_value(obj, "source_module_ref", _value(obj, "route_target_module_ref", "")))
    for mod in FUTURE_DESIGN_MODULES:
        if mod in module_ref.lower():
            issues.append(f"future_design_module_implemented:{mod}")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def validate_orchestration_result_candidate(
    result: OrchestrationResultCandidate,
) -> ValidationResult:
    issues = []
    checks = (
        validate_traceability_refs(result),
        validate_non_execution_boundary(result),
        validate_candidate_only_outputs(result),
        validate_forbidden_side_effects_absent(result),
        validate_owner_approval_request_chain_not_reopened(result),
        validate_future_design_not_implemented(result),
    )
    if not _refs(result, "governance_refs"):
        issues.append("governance_refs_empty")
    for check in checks:
        if not check.valid:
            issues.extend(check.issues)
    if not result.skeleton_pass:
        issues.append("skeleton_pass_false")
    required_refs = (
        result.plan_candidate_ref,
        result.route_candidate_ref,
        result.handoff_candidate_ref,
        result.traceability_bundle_ref,
        result.decision_candidate_ref,
    )
    for ref in required_refs:
        if not ref:
            issues.append("missing_result_ref")
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


def run_all_static_validators(obj: Any) -> ValidationResult:
    checks = (
        validate_boundary_refs(obj),
        validate_lifecycle_state_refs(obj),
        validate_alignment_rule_refs(obj),
        validate_governance_constraint_refs(obj),
        validate_traceability_refs(obj),
        validate_non_execution_boundary(obj),
        validate_candidate_only_outputs(obj),
        validate_forbidden_side_effects_absent(obj),
        validate_owner_approval_request_chain_not_reopened(obj),
        validate_future_design_not_implemented(obj),
    )
    issues = []
    for check in checks:
        if not check.valid:
            issues.extend(check.issues)
    return ValidationResult(valid=len(issues) == 0, issues=tuple(issues), blocked=bool(issues))


STATIC_VALIDATOR_FUNCTIONS: Tuple[str, ...] = (
    "validate_boundary_refs",
    "validate_lifecycle_state_refs",
    "validate_alignment_rule_refs",
    "validate_governance_constraint_refs",
    "validate_traceability_refs",
    "validate_non_execution_boundary",
    "validate_candidate_only_outputs",
    "validate_forbidden_side_effects_absent",
    "validate_owner_approval_request_chain_not_reopened",
    "validate_future_design_not_implemented",
    "validate_orchestration_result_candidate",
)
