# -*- coding: utf-8 -*-
"""Information Processing Core contracts v1 — IO / type / traceability / governance / workload only."""

from __future__ import annotations

from typing import Any, Dict, Mapping, Tuple

from capabilities.midplatform.information_processing_core_types_v1 import (
    IPC_CANDIDATE_TYPES,
    INFORMATION_TYPE_REGISTRY,
)

CONTRACT_VERSION = "v1"
CONTRACT_LAYER = "candidate_planning_contract"

IO_INPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_io_input_contract_v1",
    "required_input_type": "RawInformationInput",
    "required_fields": (
        "input_id", "source_ref", "payload_ref", "payload_kind", "content_summary",
        "traceability_refs", "governance_refs",
    ),
    "forbidden_input_methods": (
        "create_record", "issue_grant", "create_authorization_request",
        "execute_route", "execute_handoff", "promote_candidate", "persist_write",
    ),
    "handoff_contract_not_required": True,
    "integration_contract_not_required": True,
}

IO_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_io_output_contract_v1",
    "primary_output_type": "InformationProcessingResultCandidate",
    "allowed_output_types": IPC_CANDIDATE_TYPES,
    "candidate_only_required": True,
    "side_effect_allowed_required": False,
    "real_execution_required": False,
    "runtime_required_now_required": False,
}

INFORMATION_TYPE_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_information_type_contract_v1",
    "registered_types": INFORMATION_TYPE_REGISTRY,
    "unknown_information_allowed": True,
    "min_type_count": 11,
    "peripheral_contract_does_not_constrain_classification": True,
    "protocol_before_workflow_forbidden": True,
}

TRACEABILITY_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_traceability_contract_v1",
    "required_ref_fields": ("traceability_refs",),
    "trace_ref_min_count": 1,
    "source_chain_required": True,
    "write_blocking_forbidden": True,
}

GOVERNANCE_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_governance_contract_v1",
    "required_ref_fields": ("governance_refs",),
    "governance_ref_min_count": 0,
    "constitution_hard_constraint_only": ("safety", "authorization", "privacy"),
    "governance_serves_core": True,
}

NON_EXECUTION_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_non_execution_contract_v1",
    "no_record_creation": True,
    "no_grant_creation": True,
    "no_authorization_request_creation": True,
    "no_runtime_execution": True,
    "no_route_execution": True,
    "no_real_handoff_execution": True,
    "no_candidate_promotion_execution": True,
    "no_whitebox_runtime_call": True,
    "no_persistent_write": True,
}

WORKLOAD_CONTRACT: Dict[str, Any] = {
    "contract_id": "ipc_workload_contract_v1",
    "single_envelope_processing": True,
    "unknown_not_silently_dropped": True,
    "incomplete_can_defer": True,
    "high_risk_governance_review_candidate": True,
    "duplicate_idempotency_supported": True,
    "overload_can_defer": True,
    "downstream_work_not_swallowed": True,
    "classification_scope_not_unbounded": True,
}

ALL_CONTRACTS: Tuple[Dict[str, Any], ...] = (
    IO_INPUT_CONTRACT,
    IO_OUTPUT_CONTRACT,
    INFORMATION_TYPE_CONTRACT,
    TRACEABILITY_CONTRACT,
    GOVERNANCE_CONTRACT,
    NON_EXECUTION_CONTRACT,
    WORKLOAD_CONTRACT,
)


def _value(obj: Any, name: str, default: Any = None) -> Any:
    if isinstance(obj, Mapping):
        return obj.get(name, default)
    return getattr(obj, name, default)


def check_io_input_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    for field in IO_INPUT_CONTRACT["required_fields"]:
        val = _value(obj, field)
        if val is None or val == "":
            issues.append(f"missing_{field}")
    if _value(obj, "candidate_only", True) is not True:
        issues.append("candidate_only_not_true")
    if _value(obj, "real_execution", False) is not False:
        issues.append("real_execution_not_false")
    return len(issues) == 0, tuple(issues)


def check_io_output_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    for flag, expected in (
        ("candidate_only", True), ("side_effect_allowed", False),
        ("real_execution", False), ("runtime_required_now", False),
    ):
        if _value(obj, flag, not expected if isinstance(expected, bool) else expected) is not expected:
            issues.append(f"{flag}_mismatch")
    return len(issues) == 0, tuple(issues)


def check_information_type_contract(info_type: str) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    if info_type not in INFORMATION_TYPE_REGISTRY:
        issues.append("unregistered_information_type")
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
    refs = _value(obj, "traceability_refs", ())
    if not refs:
        return False, ("traceability_refs_empty",)
    return True, ()


def check_governance_contract(obj: Any) -> Tuple[bool, Tuple[str, ...]]:
    return True, ()


def check_workload_contract(flags: Mapping[str, bool]) -> Tuple[bool, Tuple[str, ...]]:
    issues = []
    for key, expected in WORKLOAD_CONTRACT.items():
        if key == "contract_id":
            continue
        if flags.get(key) is not expected:
            issues.append(f"{key}_mismatch")
    return len(issues) == 0, tuple(issues)
