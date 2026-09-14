# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Skeleton Consolidation item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

CORE_ORCHESTRATION_RESPONSIBILITIES: Tuple[str, ...] = (
    "coordinate_candidate_inter_module_flow",
    "read_module_boundary_registry",
    "read_candidate_lifecycle_state_machine",
    "read_evidence_record_approval_permission_alignment_rules",
    "generate_orchestration_route_handoff_candidates",
    "aggregate_traceability_refs",
    "maintain_non_execution_boundary",
)

CORE_ORCHESTRATION_EXCLUSIONS: Tuple[str, ...] = (
    "direct_authorization",
    "direct_record_creation",
    "direct_grant_creation",
    "runtime_execution",
    "whitebox_integration",
    "task_center_intelligence",
    "drive_brain_intelligence",
    "reflection_brain_implementation",
)

ORCHESTRATION_INPUTS: Tuple[Dict[str, str], ...] = (
    {"input_id": "input_candidate", "category": "candidate"},
    {"input_id": "task_candidate", "category": "candidate"},
    {"input_id": "decision_candidate", "category": "candidate"},
    {"input_id": "evidence_candidate", "category": "candidate"},
    {"input_id": "approval_candidate", "category": "candidate"},
    {"input_id": "permission_candidate", "category": "candidate"},
    {"input_id": "route_request_candidate", "category": "candidate"},
    {"input_id": "module_handoff_candidate", "category": "candidate"},
    {"input_id": "boundary_registry_ref", "category": "ref"},
    {"input_id": "lifecycle_state_ref", "category": "ref"},
    {"input_id": "alignment_rule_ref", "category": "ref"},
    {"input_id": "governance_constraint_ref", "category": "ref"},
)

ORCHESTRATION_OUTPUTS: Tuple[Dict[str, str], ...] = (
    {"output_id": "orchestration_plan_candidate", "layer": "candidate"},
    {"output_id": "candidate_route_candidate", "layer": "candidate"},
    {"output_id": "module_handoff_candidate", "layer": "candidate"},
    {"output_id": "lifecycle_transition_request_candidate", "layer": "candidate"},
    {"output_id": "alignment_check_request_candidate", "layer": "candidate"},
    {"output_id": "governance_check_request_candidate", "layer": "candidate"},
    {"output_id": "traceability_bundle_candidate", "layer": "candidate"},
    {"output_id": "blocker_or_defer_decision_candidate", "layer": "candidate"},
)

FLOW_SKELETON_STEPS: Tuple[Dict[str, Any], ...] = (
    {"step_id": "receive_candidate", "produces": "orchestration_plan_candidate"},
    {"step_id": "check_module_boundary", "reads": "boundary_registry_ref"},
    {"step_id": "check_lifecycle_state", "reads": "lifecycle_state_ref"},
    {"step_id": "check_alignment_requirements", "reads": "alignment_rule_ref"},
    {"step_id": "check_governance_constraints", "reads": "governance_constraint_ref"},
    {"step_id": "produce_route_candidate", "produces": "candidate_route_candidate"},
    {"step_id": "produce_handoff_candidate", "produces": "module_handoff_candidate"},
    {"step_id": "produce_traceability_bundle", "produces": "traceability_bundle_candidate"},
    {"step_id": "mark_blocker_defer_reject_close", "produces": "blocker_or_defer_decision_candidate"},
)

FLOW_SKELETON_SEMANTICS: Tuple[str, ...] = (
    "flow_skeleton_not_runtime_flow",
    "route_candidate_not_executed_route",
    "handoff_candidate_not_real_handoff_execution",
    "blocker_defer_decision_candidate_not_final_real_world_action",
)

RESPONSIBILITY_MATRIX: Tuple[Dict[str, str], ...] = (
    {"module_id": "module_boundary_registry", "relation": "provides boundaries; orchestration does not modify ownership"},
    {"module_id": "candidate_lifecycle_manager", "relation": "provides state machine; orchestration does not execute promotion"},
    {"module_id": "evidence_record_approval_permission_alignment", "relation": "provides alignment rules; orchestration does not create real objects"},
    {"module_id": "protocol_registry_input_output_traceability", "relation": "provides protocol and traceability refs"},
    {"module_id": "governance_constraints", "relation": "cross-cut constrain orchestration behavior"},
    {"module_id": "owner_approval_request_closed_module", "relation": "closed module input only; do not reopen"},
    {"module_id": "file_size_governance", "relation": "engineering constraints only; no business flow"},
    {"module_id": "future_runtime_adapter", "relation": "future execute real actions; currently absent"},
    {"module_id": "future_drive_brain", "relation": "future intelligent goal/task decisions; not implemented"},
)

NON_EXECUTION_FORBIDDEN: Tuple[str, ...] = (
    "create_request_record",
    "create_approval_record",
    "create_ack_record",
    "create_evidence_record",
    "create_grant_or_grant_record",
    "create_authorization_request",
    "execute_candidate_promotion",
    "execute_runtime_action",
    "direct_whitebox_call",
    "execute_real_owner_operator_approval",
)

ORCHESTRATION_GAPS: Tuple[Dict[str, Any], ...] = (
    {"gap_id": "orchestration_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "route_execution_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "lifecycle_manager_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "alignment_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "module_handoff_runtime_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "integration_test_deferred", "status": "deferred", "priority": "P3", "blocker_now": False},
    {"gap_id": "drive_brain_task_center_intelligence", "status": "future_design", "priority": "future", "blocker_now": False},
    {"gap_id": "reflection_brain", "status": "future_design", "priority": "future", "blocker_now": False},
    {"gap_id": "runtime_adapter_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
    {"gap_id": "whitebox_runtime_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
)

FUTURE_BRAIN_INTERFACES: Tuple[Dict[str, Any], ...] = (
    {"interface_id": "survival_brain_future_interface", "status": "future_design", "implemented_now": False},
    {"interface_id": "task_drive_brain_future_interface", "status": "future_design", "implemented_now": False},
    {"interface_id": "reflection_brain_future_interface", "status": "future_design", "implemented_now": False},
    {"interface_id": "task_elasticity_tradeoff_future_interface", "status": "future_design", "implemented_now": False},
    {"interface_id": "health_memory_world_model_hooks_future_interface", "status": "future_design", "implemented_now": False},
)

SELECTED_NEXT_ROUTE = "Task Manager Core Orchestration Skeleton Implementation Planning"
NEXT_ROUTE_A = "Phase-Midplatform-Task-Manager-Core-Orchestration-Skeleton-Implementation-Planning-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Candidate-Lifecycle-Manager-Skeleton-Planning-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Module-Handoff-Contract-Planning-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Midplatform-Integration-Gap-Consolidation-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"
