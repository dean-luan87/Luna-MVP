# -*- coding: utf-8 -*-
"""Evidence Record Approval Permission Alignment Planning item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

ALIGNMENT_OBJECT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "object_id", "object_role", "object_layer", "owning_module",
    "allowed_source_objects", "allowed_downstream_objects",
    "required_evidence_refs", "required_approval_refs", "required_permission_refs",
    "traceability_required", "runtime_required_now", "creation_allowed_now",
)

def _obj(
    object_id: str,
    object_role: str,
    object_layer: str,
    owning_module: str,
    *,
    sources: Tuple[str, ...] = (),
    downstream: Tuple[str, ...] = (),
    evidence_refs: bool = False,
    approval_refs: bool = False,
    permission_refs: bool = False,
) -> Dict[str, Any]:
    return {
        "object_id": object_id,
        "object_role": object_role,
        "object_layer": object_layer,
        "owning_module": owning_module,
        "allowed_source_objects": list(sources),
        "allowed_downstream_objects": list(downstream),
        "required_evidence_refs": evidence_refs,
        "required_approval_refs": approval_refs,
        "required_permission_refs": permission_refs,
        "traceability_required": True,
        "runtime_required_now": False,
        "creation_allowed_now": False,
    }

ALIGNMENT_OBJECT_REGISTRY: Tuple[Dict[str, Any], ...] = (
    _obj("evidence_candidate", "evidence_candidate", "candidate", "candidate_lifecycle_manager",
         downstream=("evidence_record_approval_permission_alignment",)),
    _obj("evidence_record", "evidence_record", "record", "future_runtime_adapter",
         sources=("evidence_candidate",), evidence_refs=True),
    _obj("record_candidate", "record_candidate", "candidate", "candidate_lifecycle_manager",
         downstream=("evidence_record_approval_permission_alignment",), evidence_refs=True),
    _obj("request_record", "request_record", "record", "future_runtime_adapter",
         sources=("record_candidate",), evidence_refs=True, approval_refs=True),
    _obj("approval_candidate", "approval_candidate", "candidate", "candidate_lifecycle_manager",
         sources=("record_candidate",), downstream=("evidence_record_approval_permission_alignment",), evidence_refs=True),
    _obj("approval_record", "approval_record", "record", "future_runtime_adapter",
         sources=("approval_candidate",), evidence_refs=True, approval_refs=True),
    _obj("ack_record_candidate", "ack_record_candidate", "candidate", "candidate_lifecycle_manager",
         sources=("record_candidate",), downstream=("evidence_record_approval_permission_alignment",)),
    _obj("ack_record", "ack_record", "record", "future_runtime_adapter",
         sources=("ack_record_candidate",), evidence_refs=True),
    _obj("permission_candidate", "permission_candidate", "candidate", "candidate_lifecycle_manager",
         sources=("approval_candidate",), downstream=("evidence_record_approval_permission_alignment",),
         evidence_refs=True, approval_refs=True),
    _obj("grant_candidate", "grant_candidate", "candidate", "candidate_lifecycle_manager",
         sources=("permission_candidate",), downstream=("evidence_record_approval_permission_alignment",),
         evidence_refs=True, approval_refs=True, permission_refs=True),
    _obj("grant_record", "grant_record", "grant", "future_runtime_adapter",
         sources=("grant_candidate",), evidence_refs=True, approval_refs=True, permission_refs=True),
    _obj("authorization_request_candidate", "authorization_request_candidate", "candidate", "candidate_lifecycle_manager",
         sources=("permission_candidate",), downstream=("evidence_record_approval_permission_alignment",),
         evidence_refs=True, approval_refs=True),
    _obj("authorization_request", "authorization_request", "authorization", "future_runtime_adapter",
         sources=("authorization_request_candidate",), evidence_refs=True, approval_refs=True, permission_refs=True),
)

CANDIDATE_REAL_BOUNDARY_MATRIX: Tuple[Dict[str, str], ...] = (
    {"candidate": "evidence_candidate", "real_object": "evidence_record", "rule": "evidence_candidate_not_evidence_record"},
    {"candidate": "record_candidate", "real_object": "request_record", "rule": "record_candidate_not_request_record"},
    {"candidate": "approval_candidate", "real_object": "approval_record", "rule": "approval_candidate_not_approval_record"},
    {"candidate": "ack_record_candidate", "real_object": "ack_record", "rule": "ack_record_candidate_not_ack_record"},
    {"candidate": "permission_candidate", "real_object": "grant_record", "rule": "permission_candidate_not_grant"},
    {"candidate": "grant_candidate", "real_object": "grant_record", "rule": "grant_candidate_not_grant_record"},
    {"candidate": "authorization_request_candidate", "real_object": "authorization_request", "rule": "authorization_request_candidate_not_authorization_request"},
    {"candidate": "promotion_ready", "real_object": "promotion_executed", "rule": "promotion_ready_not_promotion_executed"},
    {"candidate": "upgraded_candidate", "real_object": "real_object_created", "rule": "upgraded_candidate_not_real_object_created"},
)

PROMOTION_CREATION_PRECONDITIONS: Tuple[Dict[str, Any], ...] = (
    {"precondition_id": "explicit_authorization_present", "executed_now": False},
    {"precondition_id": "owner_operator_approval_when_required", "executed_now": False},
    {"precondition_id": "evidence_chain_complete", "executed_now": False},
    {"precondition_id": "traceability_chain_complete", "executed_now": False},
    {"precondition_id": "boundary_ownership_validated", "executed_now": False},
    {"precondition_id": "lifecycle_state_promotion_ready", "executed_now": False},
    {"precondition_id": "forbidden_transition_absent", "executed_now": False},
    {"precondition_id": "governance_constraints_satisfied", "executed_now": False},
    {"precondition_id": "runtime_permission_explicitly_granted", "executed_now": False},
    {"precondition_id": "rollback_expiry_revocation_route_defined", "executed_now": False},
)

ALIGNMENT_RESPONSIBILITY_MATRIX: Tuple[Dict[str, str], ...] = (
    {"module_id": "candidate_lifecycle_manager", "responsibility": "manage candidate state; do not create real objects"},
    {"module_id": "evidence_record_approval_permission_alignment", "responsibility": "define object boundaries and pre-promotion alignment rules; do not create real objects"},
    {"module_id": "task_manager_core_orchestration_skeleton", "responsibility": "coordinate flow; no direct authorization or record/grant creation"},
    {"module_id": "module_boundary_registry", "responsibility": "provide ownership and not_owned constraints"},
    {"module_id": "protocol_registry_input_output_traceability", "responsibility": "provide protocol and traceability refs"},
    {"module_id": "governance_constraints", "responsibility": "cross-cut constrain alignment behavior"},
    {"module_id": "owner_approval_request_closed_module", "responsibility": "closed case input only; do not reopen"},
    {"module_id": "future_runtime_adapter", "responsibility": "future execute real promotion; currently absent"},
)

FORBIDDEN_ALIGNMENT_TRANSITIONS: Tuple[Dict[str, str], ...] = (
    {"from": "evidence_candidate", "to": "evidence_record", "forbidden_now": True},
    {"from": "record_candidate", "to": "request_record", "forbidden_now": True},
    {"from": "approval_candidate", "to": "approval_record", "forbidden_now": True},
    {"from": "ack_record_candidate", "to": "ack_record", "forbidden_now": True},
    {"from": "permission_candidate", "to": "grant_record", "forbidden_now": True},
    {"from": "grant_candidate", "to": "grant_record", "forbidden_now": True},
    {"from": "authorization_request_candidate", "to": "authorization_request", "forbidden_now": True},
    {"from": "evidence_record_approval_permission_alignment", "to": "runtime_execution", "forbidden_now": True},
    {"from": "task_manager_core_orchestration_skeleton", "to": "direct_authorization", "forbidden_now": True},
)

TRACEABILITY_CONTRACT: Tuple[Dict[str, Any], ...] = (
    {"contract_id": "real_object_traces_to_source_candidate", "implemented_now": False},
    {"contract_id": "promoted_candidate_records_promotion_evidence", "implemented_now": False},
    {"contract_id": "approval_grant_auth_have_explicit_authorization_refs", "implemented_now": False},
    {"contract_id": "promotion_trace_candidate_level_plan_only", "implemented_now": True},
    {"contract_id": "no_real_trace_record_created", "implemented_now": True},
)

ALIGNMENT_GAPS: Tuple[Dict[str, Any], ...] = (
    {"gap_id": "alignment_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "real_record_creation_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "grant_issuance_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "authorization_request_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "rollback_expiry_revocation_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "integration_test_deferred", "status": "deferred", "priority": "P3", "blocker_now": False},
    {"gap_id": "runtime_adapter_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
    {"gap_id": "whitebox_runtime_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
)

SELECTED_NEXT_ROUTE = "Task Manager Core Orchestration Skeleton Consolidation"
NEXT_ROUTE_A = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Candidate-Lifecycle-Manager-Skeleton-Planning-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Evidence-Record-Approval-Permission-Alignment-Skeleton-Planning-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Module-Integration-Gap-Consolidation-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"

REAL_OBJECT_IDS: Tuple[str, ...] = (
    "evidence_record", "request_record", "approval_record", "ack_record",
    "grant_record", "authorization_request",
)

CANDIDATE_OBJECT_IDS: Tuple[str, ...] = (
    "evidence_candidate", "record_candidate", "approval_candidate", "ack_record_candidate",
    "permission_candidate", "grant_candidate", "authorization_request_candidate",
)
