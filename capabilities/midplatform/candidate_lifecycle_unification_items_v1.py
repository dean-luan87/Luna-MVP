# -*- coding: utf-8 -*-
"""Candidate Lifecycle Unification Planning item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

CANDIDATE_TYPE_REQUIRED_FIELDS: Tuple[str, ...] = (
    "candidate_type", "owning_module", "allowed_source_modules", "allowed_downstream_modules",
    "allowed_states", "forbidden_states", "promotion_allowed_now", "runtime_required_now",
    "evidence_required", "governance_refs", "ttl_policy_ref", "traceability_required",
)

UNIFIED_LIFECYCLE_STATES: Tuple[str, ...] = (
    "created", "validated", "routed", "aligned", "promotion_ready",
    "closed", "upgraded", "rejected", "deferred", "expired", "revoked",
)

NON_FINAL_STATES: Tuple[str, ...] = ("created", "validated", "routed", "aligned", "promotion_ready", "deferred")
FINAL_STATES: Tuple[str, ...] = ("closed", "upgraded", "rejected", "expired", "revoked")

COMMON_ALLOWED_STATES: Tuple[str, ...] = UNIFIED_LIFECYCLE_STATES
COMMON_FORBIDDEN_STATES: Tuple[str, ...] = ("runtime_executed", "record_created", "grant_created")

_BASE_GOVERNANCE_REFS: Tuple[str, ...] = ("governance_constraints", "module_boundary_registry")
_BASE_SOURCES: Tuple[str, ...] = ("protocol_registry_input_output_traceability", "task_manager_core_orchestration_skeleton")
_BASE_DOWNSTREAM: Tuple[str, ...] = ("task_manager_core_orchestration_skeleton", "evidence_record_approval_permission_alignment")

def _ctype(
    candidate_type: str,
    *,
    evidence_required: bool = False,
    sources: Tuple[str, ...] = _BASE_SOURCES,
    downstream: Tuple[str, ...] = _BASE_DOWNSTREAM,
    ttl: str = "default_candidate_ttl_v1",
) -> Dict[str, Any]:
    return {
        "candidate_type": candidate_type,
        "owning_module": "candidate_lifecycle_manager",
        "allowed_source_modules": list(sources),
        "allowed_downstream_modules": list(downstream),
        "allowed_states": list(COMMON_ALLOWED_STATES),
        "forbidden_states": list(COMMON_FORBIDDEN_STATES),
        "promotion_allowed_now": False,
        "runtime_required_now": False,
        "evidence_required": evidence_required,
        "governance_refs": list(_BASE_GOVERNANCE_REFS),
        "ttl_policy_ref": ttl,
        "traceability_required": True,
    }

CANDIDATE_TYPE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    _ctype("input_candidate"),
    _ctype("output_candidate"),
    _ctype("task_candidate"),
    _ctype("decision_candidate"),
    _ctype("evidence_candidate", evidence_required=True),
    _ctype("record_candidate", evidence_required=True),
    _ctype("approval_candidate", evidence_required=True),
    _ctype("permission_candidate", evidence_required=True),
    _ctype("memory_candidate", ttl="memory_candidate_ttl_v1"),
    _ctype("world_model_entry_candidate", ttl="world_model_candidate_ttl_v1"),
    _ctype("health_signal_candidate", ttl="health_signal_candidate_ttl_v1"),
)

STATE_MACHINE_DEFINITIONS: Tuple[Dict[str, str], ...] = (
    {"state": "created", "meaning": "Candidate instantiated at planning level", "is_final": "false"},
    {"state": "validated", "meaning": "Schema and governance refs validated", "is_final": "false"},
    {"state": "routed", "meaning": "Routed to downstream module chain", "is_final": "false"},
    {"state": "aligned", "meaning": "Boundary alignment rules satisfied", "is_final": "false"},
    {"state": "promotion_ready", "meaning": "Preconditions met; promotion NOT executed", "is_final": "false"},
    {"state": "closed", "meaning": "Candidate-level closure; NOT runtime closure", "is_final": "true"},
    {"state": "upgraded", "meaning": "Candidate-level upgrade; NOT real record/grant/auth request", "is_final": "true"},
    {"state": "rejected", "meaning": "Candidate rejected at candidate level", "is_final": "true"},
    {"state": "deferred", "meaning": "Secondary objective deferred", "is_final": "false"},
    {"state": "expired", "meaning": "TTL exceeded at candidate level", "is_final": "true"},
    {"state": "revoked", "meaning": "Governance revocation at candidate level", "is_final": "true"},
)

ALLOWED_TRANSITIONS: Tuple[Dict[str, str], ...] = (
    {"from": "created", "to": "validated"},
    {"from": "validated", "to": "routed"},
    {"from": "routed", "to": "aligned"},
    {"from": "aligned", "to": "promotion_ready"},
    {"from": "promotion_ready", "to": "closed"},
    {"from": "promotion_ready", "to": "upgraded"},
    {"from": "promotion_ready", "to": "rejected"},
    {"from": "promotion_ready", "to": "deferred"},
    {"from": "deferred", "to": "validated"},
    {"from": "deferred", "to": "rejected"},
    {"from": "deferred", "to": "expired"},
)

FORBIDDEN_TRANSITIONS: Tuple[Dict[str, str], ...] = (
    {"from": "candidate", "to": "real_record", "rule_id": "candidate_not_promoted_to_record"},
    {"from": "permission_candidate", "to": "grant", "rule_id": "permission_candidate_not_promoted_to_grant"},
    {"from": "authorization_request_candidate", "to": "authorization_request", "rule_id": "authorization_request_candidate_not_promoted_to_authorization_request"},
    {"from": "evidence_candidate", "to": "evidence_record", "rule_id": "evidence_candidate_not_promoted_to_evidence_record"},
    {"from": "approval_candidate", "to": "approval_record", "rule_id": "approval_candidate_not_promoted_to_approval_record"},
    {"from": "record_candidate", "to": "request_record", "rule_id": "record_candidate_not_promoted_to_request_record"},
    {"from": "record_candidate", "to": "ack_record", "rule_id": "record_candidate_not_promoted_to_ack_record"},
    {"from": "candidate_lifecycle_manager", "to": "runtime_execution", "rule_id": "lifecycle_manager_not_runtime_execution"},
    {"from": "candidate_lifecycle_manager", "to": "direct_authorization", "rule_id": "lifecycle_manager_not_direct_authorization"},
)

FORBIDDEN_PROMOTION_RULES: Tuple[str, ...] = tuple(r["rule_id"] for r in FORBIDDEN_TRANSITIONS)

ANY_TO_TERMINAL: Tuple[Dict[str, str], ...] = tuple(
    {"from": state, "to": terminal}
    for state in NON_FINAL_STATES
    for terminal in ("rejected", "deferred", "expired", "revoked")
)

RESPONSIBILITY_MATRIX: Tuple[Dict[str, Any], ...] = (
    {"module_id": "module_boundary_registry", "responsibility": "provide ownership and not_owned constraints"},
    {"module_id": "candidate_lifecycle_manager", "responsibility": "plan state transitions and candidate-state management"},
    {"module_id": "task_manager_core_orchestration_skeleton", "responsibility": "coordinate candidate flow routing"},
    {"module_id": "protocol_registry_input_output_traceability", "responsibility": "provide protocol and traceability refs"},
    {"module_id": "evidence_record_approval_permission_alignment", "responsibility": "provide promotion boundary alignment rules"},
    {"module_id": "governance_constraints", "responsibility": "cross-cut constrain transition behavior"},
    {"module_id": "owner_approval_request_closed_module", "responsibility": "downstream closed example input only"},
    {"module_id": "file_size_governance", "responsibility": "constrain engineering files only; no business state ownership"},
)

PROMOTION_PRECONDITIONS: Tuple[Dict[str, Any], ...] = (
    {"precondition_id": "explicit_authorization_required", "required": True, "executed_now": False},
    {"precondition_id": "evidence_chain_complete", "required": True, "executed_now": False},
    {"precondition_id": "traceability_refs_complete", "required": True, "executed_now": False},
    {"precondition_id": "boundary_ownership_validated", "required": True, "executed_now": False},
    {"precondition_id": "forbidden_transition_absent", "required": True, "executed_now": False},
    {"precondition_id": "governance_constraints_satisfied", "required": True, "executed_now": False},
    {"precondition_id": "runtime_permission_not_granted_now", "required": True, "executed_now": False},
    {"precondition_id": "owner_operator_approval_when_applicable", "required": True, "executed_now": False},
)

CLOSURE_REJECTION_DEFERRAL_RULES: Tuple[Dict[str, Any], ...] = (
    {"rule_id": "candidate_closed", "condition": "Primary flow complete or explicitly terminated at candidate level"},
    {"rule_id": "candidate_rejected", "condition": "Governance or validation failure; boundary violation"},
    {"rule_id": "candidate_deferred", "condition": "Secondary objective deprioritized; primary objective protected"},
    {"rule_id": "candidate_expired", "condition": "TTL exceeded without promotion_ready transition"},
    {"rule_id": "candidate_revoked", "condition": "Governance revocation or policy override"},
    {"rule_id": "secondary_objective_defer_discard", "condition": "Mark secondary candidates deferred or rejected without blocking primary"},
    {"rule_id": "primary_objective_protection", "condition": "Primary objective candidates retain higher priority in routing and closure"},
)

LIFECYCLE_INTEGRATION_GAPS: Tuple[Dict[str, Any], ...] = (
    {"gap_id": "lifecycle_manager_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "evidence_alignment_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "orchestration_skeleton_in_progress", "status": "in_progress", "priority": "P2", "blocker_now": False},
    {"gap_id": "distributed_ready_field_alignment", "status": "deferred", "priority": "P3", "blocker_now": False},
    {"gap_id": "health_memory_world_model_hooks", "status": "deferred", "priority": "future", "blocker_now": False},
    {"gap_id": "runtime_adapter_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
    {"gap_id": "whitebox_runtime_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
)

SELECTED_NEXT_ROUTE = "Evidence Record Approval Permission Alignment Planning"
NEXT_ROUTE_A = "Phase-Midplatform-Evidence-Record-Approval-Permission-Alignment-Planning-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Candidate-Lifecycle-Manager-Skeleton-Planning-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Module-Boundary-Registry-DryRun-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"

STATE_MACHINE_SEMANTICS: Tuple[str, ...] = (
    "upgraded_not_real_record_or_grant_or_authorization_request",
    "promotion_ready_not_promotion_executed",
    "closed_not_runtime_closure",
    "rejected_deferred_expired_revoked_are_candidate_level_states",
)
