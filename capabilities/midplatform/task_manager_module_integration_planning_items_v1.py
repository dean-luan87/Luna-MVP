# -*- coding: utf-8 -*-
"""Module Integration Planning item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

MODULE_BOUNDARY_REQUIRED_FIELDS: Tuple[str, ...] = (
    "module_id",
    "module_role",
    "boundary_type",
    "owned_objects",
    "consumed_objects",
    "produced_objects",
    "upstream_refs",
    "downstream_refs",
    "not_owned_objects",
    "runtime_required_now",
)

MODULE_BOUNDARY_INTEGRATION_MAP: Tuple[Dict[str, Any], ...] = (
    {
        "module_id": "task_manager_core_orchestration_skeleton",
        "module_role": "orchestration_coordinator",
        "boundary_type": "coordination_layer",
        "owned_objects": ["candidate_flow_state", "module_dispatch_plan"],
        "consumed_objects": ["candidate_lifecycle_events", "protocol_trace_refs"],
        "produced_objects": ["orchestration_plan", "candidate_routing_decisions"],
        "upstream_refs": ["candidate_lifecycle_manager", "protocol_registry_input_output_traceability"],
        "downstream_refs": ["evidence_record_approval_permission_alignment"],
        "not_owned_objects": ["records", "grants", "authorization_requests", "runtime_execution"],
        "runtime_required_now": False,
    },
    {
        "module_id": "module_boundary_registry",
        "module_role": "boundary_registry",
        "boundary_type": "structural_registry",
        "owned_objects": ["module_boundary_definitions", "ownership_matrix"],
        "consumed_objects": ["governance_constraints", "protocol_registry_entries"],
        "produced_objects": ["boundary_lookup_index", "not_owned_declarations"],
        "upstream_refs": ["governance_constraints", "protocol_registry_input_output_traceability"],
        "downstream_refs": ["candidate_lifecycle_manager", "task_manager_core_orchestration_skeleton"],
        "not_owned_objects": ["candidate_instances", "records", "runtime_bindings"],
        "runtime_required_now": False,
    },
    {
        "module_id": "candidate_lifecycle_manager",
        "module_role": "lifecycle_coordinator",
        "boundary_type": "lifecycle_layer",
        "owned_objects": ["candidate_state_transitions", "lifecycle_stage_registry"],
        "consumed_objects": ["module_boundary_definitions", "protocol_trace_refs"],
        "produced_objects": ["lifecycle_events", "candidate_status_updates"],
        "upstream_refs": ["module_boundary_registry", "protocol_registry_input_output_traceability"],
        "downstream_refs": ["task_manager_core_orchestration_skeleton", "evidence_record_approval_permission_alignment"],
        "not_owned_objects": ["records", "grants", "authorization_requests"],
        "runtime_required_now": False,
    },
    {
        "module_id": "evidence_record_approval_permission_alignment",
        "module_role": "alignment_coordinator",
        "boundary_type": "alignment_layer",
        "owned_objects": ["alignment_rules", "promotion_preconditions"],
        "consumed_objects": ["candidate_lifecycle_events", "orchestration_plan"],
        "produced_objects": ["alignment_decisions", "promotion_readiness_flags"],
        "upstream_refs": ["candidate_lifecycle_manager", "task_manager_core_orchestration_skeleton"],
        "downstream_refs": ["owner_approval_request_closed_module"],
        "not_owned_objects": ["evidence_records", "approval_records", "grants", "authorization_requests"],
        "runtime_required_now": False,
    },
    {
        "module_id": "protocol_registry_input_output_traceability",
        "module_role": "protocol_traceability",
        "boundary_type": "protocol_layer",
        "owned_objects": ["protocol_registry", "input_output_trace_index"],
        "consumed_objects": ["governance_constraints"],
        "produced_objects": ["protocol_trace_refs", "io_contract_declarations"],
        "upstream_refs": ["governance_constraints"],
        "downstream_refs": ["module_boundary_registry", "candidate_lifecycle_manager", "task_manager_core_orchestration_skeleton"],
        "not_owned_objects": ["candidate_instances", "records", "runtime_execution"],
        "runtime_required_now": False,
    },
    {
        "module_id": "governance_constraints",
        "module_role": "governance_cross_cut",
        "boundary_type": "cross_cutting_constraint",
        "owned_objects": ["governance_rules", "development_constraints"],
        "consumed_objects": [],
        "produced_objects": ["constraint_refs", "governance_gates"],
        "upstream_refs": [],
        "downstream_refs": [
            "protocol_registry_input_output_traceability",
            "module_boundary_registry",
            "candidate_lifecycle_manager",
            "task_manager_core_orchestration_skeleton",
            "evidence_record_approval_permission_alignment",
            "file_size_governance",
        ],
        "not_owned_objects": ["candidate_instances", "records", "runtime_execution"],
        "runtime_required_now": False,
    },
    {
        "module_id": "file_size_governance",
        "module_role": "engineering_governance_cross_cut",
        "boundary_type": "cross_cutting_engineering",
        "owned_objects": ["file_size_rules", "module_split_policies"],
        "consumed_objects": ["governance_constraints"],
        "produced_objects": ["file_size_governance_reviews"],
        "upstream_refs": ["governance_constraints"],
        "downstream_refs": [],
        "not_owned_objects": ["candidate_instances", "records", "runtime_execution"],
        "runtime_required_now": False,
    },
    {
        "module_id": "owner_approval_request_closed_module",
        "module_role": "downstream_governance_ready_input",
        "boundary_type": "closed_handoff_module",
        "owned_objects": ["governance_ready_handoff_package"],
        "consumed_objects": ["alignment_decisions", "functional_slice_dryrun_artifacts"],
        "produced_objects": ["governance_ready_reference"],
        "upstream_refs": ["evidence_record_approval_permission_alignment"],
        "downstream_refs": [],
        "not_owned_objects": ["new_request_issuance", "record_creation", "grant_creation"],
        "runtime_required_now": False,
    },
)

CANDIDATE_LIFECYCLE_TYPES: Tuple[str, ...] = (
    "input_candidate",
    "output_candidate",
    "task_candidate",
    "decision_candidate",
    "evidence_candidate",
    "record_candidate",
    "approval_candidate",
    "permission_candidate",
    "memory_candidate",
    "world_model_entry_candidate",
    "health_signal_candidate",
)

CANDIDATE_LIFECYCLE_STAGES: Tuple[str, ...] = (
    "created",
    "validated",
    "routed",
    "aligned",
    "promotion_ready",
    "closed",
    "upgraded",
    "rejected",
    "deferred",
)

CANDIDATE_LIFECYCLE_INTEGRATION_PLAN: Tuple[Dict[str, Any], ...] = tuple(
    {
        "candidate_type": ctype,
        "lifecycle_stages": list(CANDIDATE_LIFECYCLE_STAGES),
        "managed_by": "candidate_lifecycle_manager",
        "orchestrated_by": "task_manager_core_orchestration_skeleton",
        "runtime_implementation": False,
    }
    for ctype in CANDIDATE_LIFECYCLE_TYPES
)

ALIGNMENT_OBJECT_PAIRS: Tuple[Dict[str, str], ...] = (
    {"candidate": "evidence_candidate", "record": "evidence_record", "rule": "candidate_not_equal_record"},
    {"candidate": "approval_candidate", "record": "approval_record", "rule": "approval_candidate_not_equal_approval_record"},
    {"candidate": "record_candidate", "record": "request_record", "rule": "candidate_not_equal_record"},
    {"candidate": "record_candidate", "record": "ack_record", "rule": "candidate_not_equal_record"},
    {"candidate": "permission_candidate", "record": "grant", "rule": "permission_candidate_not_equal_grant"},
    {"candidate": "authorization_request_candidate", "record": "authorization_request", "rule": "authorization_request_candidate_not_equal_authorization_request"},
)

ALIGNMENT_PLAN_RULES: Tuple[str, ...] = (
    "candidate_not_equal_record",
    "approval_candidate_not_equal_approval_record",
    "permission_candidate_not_equal_grant",
    "authorization_request_candidate_not_equal_authorization_request",
    "evidence_candidate_not_equal_evidence_record",
    "no_real_record_created",
    "no_real_grant_created",
    "no_real_authorization_request_created",
)

ORCHESTRATION_SKELETON_RESPONSIBILITIES: Tuple[str, ...] = (
    "coordinate_candidate_flow",
    "dispatch_inter_module_candidate_chains",
)

ORCHESTRATION_SKELETON_EXCLUSIONS: Tuple[str, ...] = (
    "real_runtime_execution",
    "direct_permission_grant",
    "direct_record_creation",
    "whitebox_integration",
    "drive_brain_intelligence",
    "task_center_intelligence",
)

DEPENDENCY_GRAPH_NODES: Tuple[str, ...] = (
    "governance_constraints",
    "file_size_governance",
    "protocol_registry_input_output_traceability",
    "module_boundary_registry",
    "candidate_lifecycle_manager",
    "task_manager_core_orchestration_skeleton",
    "evidence_record_approval_permission_alignment",
    "owner_approval_request_closed_module",
)

DEPENDENCY_GRAPH_EDGES: Tuple[Dict[str, str], ...] = (
    {"from": "governance_constraints", "to": "protocol_registry_input_output_traceability", "type": "cross_cut"},
    {"from": "governance_constraints", "to": "module_boundary_registry", "type": "cross_cut"},
    {"from": "governance_constraints", "to": "candidate_lifecycle_manager", "type": "cross_cut"},
    {"from": "governance_constraints", "to": "task_manager_core_orchestration_skeleton", "type": "cross_cut"},
    {"from": "governance_constraints", "to": "evidence_record_approval_permission_alignment", "type": "cross_cut"},
    {"from": "governance_constraints", "to": "file_size_governance", "type": "cross_cut"},
    {"from": "file_size_governance", "to": "protocol_registry_input_output_traceability", "type": "engineering_cross_cut"},
    {"from": "protocol_registry_input_output_traceability", "to": "module_boundary_registry", "type": "upstream"},
    {"from": "protocol_registry_input_output_traceability", "to": "candidate_lifecycle_manager", "type": "upstream"},
    {"from": "module_boundary_registry", "to": "candidate_lifecycle_manager", "type": "upstream"},
    {"from": "candidate_lifecycle_manager", "to": "task_manager_core_orchestration_skeleton", "type": "upstream"},
    {"from": "task_manager_core_orchestration_skeleton", "to": "evidence_record_approval_permission_alignment", "type": "upstream"},
    {"from": "evidence_record_approval_permission_alignment", "to": "owner_approval_request_closed_module", "type": "upstream"},
    {"from": "runtime_adapter", "to": "task_manager_core_orchestration_skeleton", "type": "future_dependency"},
    {"from": "whitebox_runtime", "to": "runtime_adapter", "type": "future_dependency"},
    {"from": "real_execution_preauth", "to": "whitebox_runtime", "type": "future_dependency"},
)

INTEGRATION_GAPS: Tuple[Dict[str, Any], ...] = (
    {"gap_id": "module_boundary_registry_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "candidate_lifecycle_manager_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "evidence_alignment_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "orchestration_skeleton_in_progress", "status": "in_progress", "priority": "P2", "blocker_now": False},
    {"gap_id": "distributed_ready_field_alignment", "status": "deferred", "priority": "P3", "blocker_now": False},
    {"gap_id": "health_memory_world_model_hooks", "status": "deferred", "priority": "future", "blocker_now": False},
    {"gap_id": "runtime_adapter_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
    {"gap_id": "whitebox_runtime_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
)

SELECTED_NEXT_ROUTE = "Module Boundary Registry Planning"
NEXT_ROUTE_A = "Phase-Midplatform-Module-Boundary-Registry-Planning-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Candidate-Lifecycle-Unification-Planning-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Evidence-Record-Approval-Permission-Alignment-Planning-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Consolidation-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"
