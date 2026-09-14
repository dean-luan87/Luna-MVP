# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration contracts v1 — IO / non-execution / traceability only."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from capabilities.midplatform.task_manager_core_orchestration_types_v1 import (
    ORCHESTRATION_CANDIDATE_TYPES,
)

CONTRACT_VERSION = "v1"
CONTRACT_LAYER = "candidate_planning_contract"

IO_INPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "orchestration_io_input_contract_v1",
    "required_input_type": "OrchestrationInputCandidate",
    "required_fields": (
        "candidate_id",
        "source_module_ref",
        "boundary_registry_ref",
        "lifecycle_state_ref",
        "alignment_rule_ref",
        "governance_constraint_ref",
        "protocol_trace_ref",
        "traceability_refs",
        "governance_refs",
    ),
    "forbidden_input_methods": (
        "create_record",
        "issue_grant",
        "create_authorization_request",
        "execute_route",
        "execute_handoff",
        "promote_candidate",
    ),
}

IO_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "orchestration_io_output_contract_v1",
    "primary_output_type": "OrchestrationResultCandidate",
    "allowed_output_types": ORCHESTRATION_CANDIDATE_TYPES,
    "candidate_only_required": True,
    "side_effect_allowed_required": False,
    "real_execution_required": False,
    "runtime_required_now_required": False,
}

NON_EXECUTION_CONTRACT: Dict[str, Any] = {
    "contract_id": "orchestration_non_execution_contract_v1",
    "no_record_creation": True,
    "no_grant_creation": True,
    "no_authorization_request_creation": True,
    "no_runtime_execution": True,
    "no_route_execution": True,
    "no_real_handoff_execution": True,
    "no_owner_approval_request_reopen": True,
    "no_candidate_promotion_execution": True,
    "no_whitebox_runtime_call": True,
}

TRACEABILITY_CONTRACT: Dict[str, Any] = {
    "contract_id": "orchestration_traceability_contract_v1",
    "required_ref_fields": ("traceability_refs", "protocol_trace_ref"),
    "trace_ref_min_count": 1,
    "source_chain_required": True,
}

GOVERNANCE_CONTRACT: Dict[str, Any] = {
    "contract_id": "orchestration_governance_contract_v1",
    "required_ref_fields": ("governance_refs", "governance_constraint_ref"),
    "governance_ref_min_count": 1,
    "owner_approval_request_chain_reopen_forbidden": True,
}

ALLOWED_CANDIDATE_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "orchestration_allowed_candidate_output_contract_v1",
    "allowed_types": ORCHESTRATION_CANDIDATE_TYPES,
    "forbidden_runtime_methods": (
        "execute",
        "run_runtime",
        "call_whitebox",
        "create_record",
        "issue_grant",
        "create_authorization_request",
        "promote",
    ),
}

ALL_CONTRACTS: Tuple[Dict[str, Any], ...] = (
    IO_INPUT_CONTRACT,
    IO_OUTPUT_CONTRACT,
    NON_EXECUTION_CONTRACT,
    TRACEABILITY_CONTRACT,
    GOVERNANCE_CONTRACT,
    ALLOWED_CANDIDATE_OUTPUT_CONTRACT,
)


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def check_io_input_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    for field in IO_INPUT_CONTRACT["required_fields"]:
        val = _value(obj, field)
        if val is None or val == "" or val == ():
            issues.append(f"missing_{field}")
    if _value(obj, "candidate_only", True) is not True:
        issues.append("candidate_only_not_true")
    if _value(obj, "real_execution", False) is not False:
        issues.append("real_execution_not_false")
    return len(issues) == 0, tuple(issues)


def check_io_output_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    if _value(obj, "candidate_only", True) is not True:
        issues.append("candidate_only_not_true")
    if _value(obj, "side_effect_allowed", False) is not False:
        issues.append("side_effect_allowed_not_false")
    if _value(obj, "real_execution", False) is not False:
        issues.append("real_execution_not_false")
    if _value(obj, "runtime_required_now", False) is not False:
        issues.append("runtime_required_now_not_false")
    return len(issues) == 0, tuple(issues)


def check_non_execution_contract(flags: Mapping[str, bool]) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    for key, expected in NON_EXECUTION_CONTRACT.items():
        if key == "contract_id":
            continue
        if flags.get(key) is not expected:
            issues.append(f"{key}_mismatch")
    return len(issues) == 0, tuple(issues)


def check_traceability_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    refs = _value(obj, "traceability_refs", ())
    if not refs:
        issues.append("traceability_refs_empty")
    trace = _value(obj, "protocol_trace_ref", None)
    if trace is None and not refs:
        issues.append("protocol_trace_ref_missing")
    return len(issues) == 0, tuple(issues)


def check_governance_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    refs = _value(obj, "governance_refs", ())
    if not refs:
        issues.append("governance_refs_empty")
    return len(issues) == 0, tuple(issues)


def check_allowed_candidate_output_contract(type_name: str) -> Tuple[bool, Tuple[str, ...]]:
    if type_name not in ALLOWED_CANDIDATE_OUTPUT_CONTRACT["allowed_types"]:
        return False, (f"disallowed_output_type:{type_name}",)
    return True, ()
