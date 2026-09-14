# -*- coding: utf-8 -*-
"""Task Manager Core Orchestration Implementation Planning item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

FUNCTIONAL_UNIT_REQUIRED_FIELDS: Tuple[str, ...] = (
    "unit_id", "unit_role", "input_refs", "output_refs", "owned_objects",
    "not_owned_objects", "runtime_required_now", "side_effect_allowed", "candidate_only",
)

def _unit(
    unit_id: str,
    unit_role: str,
    input_refs: Tuple[str, ...],
    output_refs: Tuple[str, ...],
    owned: Tuple[str, ...],
    not_owned: Tuple[str, ...],
) -> Dict[str, Any]:
    return {
        "unit_id": unit_id,
        "unit_role": unit_role,
        "input_refs": list(input_refs),
        "output_refs": list(output_refs),
        "owned_objects": list(owned),
        "not_owned_objects": list(not_owned),
        "runtime_required_now": False,
        "side_effect_allowed": False,
        "candidate_only": True,
    }

ORCHESTRATION_FUNCTIONAL_UNITS: Tuple[Dict[str, Any], ...] = (
    _unit("orchestration_input_normalizer", "normalize_orchestration_inputs",
          ("OrchestrationInputCandidate",), ("OrchestrationInputCandidate",),
          ("normalized_input",), ("records", "grants", "runtime_execution")),
    _unit("boundary_check_adapter", "check_boundary_refs",
          ("boundary_registry_ref",), ("AlignmentCheckRequestCandidate",),
          ("boundary_check_result",), ("records", "ownership_mutation")),
    _unit("lifecycle_state_check_adapter", "check_lifecycle_state",
          ("lifecycle_state_ref",), ("LifecycleTransitionRequestCandidate",),
          ("lifecycle_check_result",), ("promotion_execution", "records")),
    _unit("alignment_rule_check_adapter", "check_alignment_rules",
          ("alignment_rule_ref",), ("AlignmentCheckRequestCandidate",),
          ("alignment_check_result",), ("evidence_records", "grants")),
    _unit("governance_constraint_check_adapter", "check_governance_constraints",
          ("governance_constraint_ref",), ("GovernanceCheckRequestCandidate",),
          ("governance_check_result",), ("runtime_permission", "grants")),
    _unit("candidate_route_builder", "build_route_candidate",
          ("OrchestrationInputCandidate", "boundary_registry_ref"), ("CandidateRouteCandidate",),
          ("route_candidate",), ("route_execution", "runtime_execution")),
    _unit("module_handoff_candidate_builder", "build_handoff_candidate",
          ("CandidateRouteCandidate",), ("ModuleHandoffCandidate",),
          ("handoff_candidate",), ("handoff_execution", "records")),
    _unit("traceability_bundle_builder", "build_traceability_bundle",
          ("protocol_trace_ref", "alignment_rule_ref"), ("TraceabilityBundleCandidate",),
          ("traceability_bundle",), ("trace_records", "runtime_execution")),
    _unit("blocker_defer_reject_close_decision_builder", "build_decision_candidate",
          ("governance_check_result", "alignment_check_result"), ("BlockerOrDeferDecisionCandidate",),
          ("decision_candidate",), ("real_world_action", "records")),
    _unit("orchestration_result_assembler", "assemble_orchestration_result",
          ("OrchestrationPlanCandidate", "TraceabilityBundleCandidate"), ("OrchestrationResultCandidate",),
          ("orchestration_result",), ("records", "grants", "runtime_execution")),
    _unit("non_execution_guard", "enforce_non_execution_boundary",
          ("OrchestrationResultCandidate",), ("OrchestrationResultCandidate",),
          ("non_execution_flags",), ("records", "grants", "runtime_execution")),
    _unit("static_validation_helper", "run_static_validation",
          ("OrchestrationResultCandidate",), ("OrchestrationResultCandidate",),
          ("validation_report",), ("runtime_execution", "side_effects")),
)

DATA_STRUCTURE_PLAN: Tuple[Dict[str, Any], ...] = tuple(
    {
        "structure_id": sid,
        "layer": "candidate_planning_object",
        "has_traceability_refs": True,
        "has_governance_refs": True,
        "has_non_execution_flags": True,
        "runtime_execution_method": False,
        "grant_issuance_method": False,
        "record_creation_method": False,
    }
    for sid in (
        "OrchestrationInputCandidate",
        "OrchestrationPlanCandidate",
        "CandidateRouteCandidate",
        "ModuleHandoffCandidate",
        "LifecycleTransitionRequestCandidate",
        "AlignmentCheckRequestCandidate",
        "GovernanceCheckRequestCandidate",
        "TraceabilityBundleCandidate",
        "BlockerOrDeferDecisionCandidate",
        "OrchestrationResultCandidate",
    )
)

STATIC_VALIDATORS: Tuple[str, ...] = (
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
)

IMPLEMENTATION_FILES: Tuple[Dict[str, str], ...] = (
    {"path": "capabilities/midplatform/task_manager_core_orchestration_types_v1.py", "responsibility": "dataclass_typed_structures_constants"},
    {"path": "capabilities/midplatform/task_manager_core_orchestration_skeleton_v1.py", "responsibility": "orchestration_coordination_skeleton"},
    {"path": "capabilities/midplatform/task_manager_core_orchestration_static_validators_v1.py", "responsibility": "static_validation_only"},
    {"path": "capabilities/midplatform/task_manager_core_orchestration_builders_v1.py", "responsibility": "candidate_builders_only"},
    {"path": "capabilities/midplatform/task_manager_core_orchestration_contracts_v1.py", "responsibility": "io_non_execution_traceability_contracts"},
)

ALLOWED_DEPENDENCIES: Tuple[str, ...] = (
    "module_boundary_registry_planning_artifacts",
    "candidate_lifecycle_unification_artifacts",
    "evidence_record_approval_permission_alignment_artifacts",
    "governance_constraints",
    "protocol_registry_traceability",
    "file_size_governance",
)

FORBIDDEN_DEPENDENCIES: Tuple[str, ...] = (
    "runtime_adapter",
    "whitebox_runtime",
    "real_issuance_preauthorization",
    "task_center_drive_brain_implementation",
    "reflection_brain_implementation",
)

NON_EXECUTION_GUARDS: Tuple[str, ...] = (
    "no_record_creation",
    "no_grant_creation",
    "no_authorization_request_creation",
    "no_runtime_execution",
    "no_route_execution",
    "no_real_handoff_execution",
    "no_owner_approval_request_reopen",
    "no_candidate_promotion_execution",
    "no_whitebox_runtime_call",
)

IMPLEMENTATION_GAPS: Tuple[Dict[str, Any], ...] = (
    {"gap_id": "orchestration_skeleton_files_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "validators_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "builders_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "contracts_not_implemented", "status": "planned", "priority": "P2", "blocker_now": False},
    {"gap_id": "module_integration_test_deferred", "status": "deferred", "priority": "P3", "blocker_now": False},
    {"gap_id": "runtime_adapter_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
    {"gap_id": "whitebox_runtime_future_debt", "status": "future_runtime_debt", "priority": "P4", "blocker_now": False},
    {"gap_id": "drive_brain_reflection_brain_future_design", "status": "future_design", "priority": "future", "blocker_now": False},
)

SELECTED_NEXT_ROUTE = "Task Manager Core Orchestration Skeleton Controlled Implementation"
NEXT_ROUTE_A = "Phase-Midplatform-Task-Manager-Core-Orchestration-Controlled-Skeleton-Implementation-v1-001"
NEXT_ROUTE_B = "Phase-Midplatform-Task-Manager-Core-Orchestration-Types-Implementation-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Task-Manager-Core-Orchestration-Static-Validators-Implementation-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Task-Manager-Core-Orchestration-Candidate-Builders-Implementation-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Task-Manager-Core-Orchestration-Contracts-Implementation-v1-001"
