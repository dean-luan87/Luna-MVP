# -*- coding: utf-8 -*-
"""Module Integration Gap Consolidation item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple


def _completed(
    module_id: str,
    completion_level: str,
    next_usage: str,
) -> Dict[str, Any]:
    return {
        "module_id": module_id,
        "completion_level": completion_level,
        "runtime_ready": False,
        "integration_tested": False,
        "next_usage": next_usage,
    }


COMPLETED_MODULES: Tuple[Dict[str, Any], ...] = (
    _completed("module_boundary_registry_planning", "planning", "boundary_ref_source_for_orchestration"),
    _completed("candidate_lifecycle_unification_planning", "planning", "lifecycle_ref_source_for_orchestration"),
    _completed("evidence_record_approval_permission_alignment_planning", "planning", "alignment_ref_source_for_orchestration"),
    _completed("task_manager_core_orchestration_skeleton_consolidation", "consolidated", "orchestration_skeleton_role_definition"),
    _completed("task_manager_core_orchestration_controlled_skeleton_implementation", "controlled_implemented", "candidate_orchestration_builders_validators"),
    _completed("task_manager_core_orchestration_module_level_controlled_dryrun", "module_dryrun_go", "module_level_controlled_flow_verified"),
    _completed("owner_approval_request_closed_module", "governance_ready", "closed_subchain_handoff_only"),
    _completed("foundation_layer_consolidated", "consolidated", "foundation_refs_for_midplatform"),
    _completed("protocol_registry_input_output_traceability", "consolidated", "traceability_ref_registry"),
    _completed("governance_constraints", "governance_ready", "non_execution_governance_refs"),
    _completed("file_size_governance", "governance_ready", "module_split_file_size_rules"),
    _completed("module_first_result_first_rules", "governance_ready", "engineering_cadence_rules"),
)

GAP_CLASSIFICATIONS: Tuple[str, ...] = (
    "required_next_for_structure",
    "required_before_integration_test",
    "deferred_until_runtime",
    "future_runtime_debt",
    "future_design",
    "optional_quality",
    "already_resolved",
)


def _gap(
    gap_id: str,
    gap_type: str,
    priority: str,
    blocker_now: bool,
    required_before_integration_test: bool,
    required_before_runtime: bool,
    can_defer: bool,
    recommended_route: str,
    classification: str,
) -> Dict[str, Any]:
    return {
        "gap_id": gap_id,
        "gap_type": gap_type,
        "priority": priority,
        "blocker_now": blocker_now,
        "required_before_integration_test": required_before_integration_test,
        "required_before_runtime": required_before_runtime,
        "can_defer": can_defer,
        "recommended_route": recommended_route,
        "classification": classification,
    }


REMAINING_GAPS: Tuple[Dict[str, Any], ...] = (
    _gap("module_handoff_contract_not_implemented", "structure", "P1", True, True, True, False,
         "Phase-Midplatform-Module-Handoff-Contract-Controlled-Implementation-v1-001", "required_next_for_structure"),
    _gap("module_boundary_registry_runtime_absent", "runtime", "P3", False, False, True, True,
         "deferred_until_runtime", "deferred_until_runtime"),
    _gap("candidate_lifecycle_manager_runtime_absent", "structure", "P2", False, True, True, False,
         "Phase-Midplatform-Candidate-Lifecycle-Manager-Controlled-Implementation-v1-001", "required_next_for_structure"),
    _gap("evidence_alignment_runtime_absent", "structure", "P2", False, True, True, True,
         "Phase-Midplatform-Evidence-Alignment-Controlled-Implementation-v1-001", "required_before_integration_test"),
    _gap("midplatform_module_boundary_registry_runtime_not_implemented", "runtime", "P3", False, False, True, True,
         "deferred_until_runtime", "deferred_until_runtime"),
    _gap("distributed_ready_field_alignment_deferred", "alignment", "P3", False, True, True, True,
         "Phase-Midplatform-Integration-Contract-Planning-v1-001", "required_before_integration_test"),
    _gap("health_memory_world_model_hooks_deferred", "integration", "P4", False, True, True, True,
         "deferred_until_runtime", "optional_quality"),
    _gap("integration_test_planning_deferred", "integration", "P2", False, True, False, True,
         "Phase-Midplatform-Integration-Contract-Planning-v1-001", "required_before_integration_test"),
    _gap("governance_debt_consolidation_pending", "governance", "P3", False, False, False, True,
         "Phase-Midplatform-Governance-Debt-Consolidation-v1-001", "optional_quality"),
    _gap("runtime_adapter_future_debt", "runtime", "P4", False, False, True, True,
         "deferred_until_runtime", "future_runtime_debt"),
    _gap("whitebox_runtime_future_debt", "runtime", "P4", False, False, True, True,
         "deferred_until_runtime", "future_runtime_debt"),
    _gap("real_execution_preauthorization_gate_deferred", "authorization", "P4", False, False, True, True,
         "deferred_until_runtime", "deferred_until_runtime"),
    _gap("task_center_drive_brain_future_design", "brain", "future", False, False, True, True,
         "future_design", "future_design"),
    _gap("survival_brain_future_design", "brain", "future", False, False, True, True,
         "future_design", "future_design"),
    _gap("reflection_brain_future_design", "brain", "future", False, False, True, True,
         "future_design", "future_design"),
    _gap("time_bound_task_elasticity_tradeoff_future_design", "design", "future", False, False, True, True,
         "future_design", "future_design"),
)

MODULE_CHAIN_READINESS: Dict[str, Any] = {
    "boundary_to_lifecycle_controlled_flow": True,
    "lifecycle_to_alignment_controlled_flow": True,
    "alignment_to_orchestration_controlled_flow": True,
    "orchestration_produces_handoff_candidate": True,
    "module_handoff_contract_implemented": False,
    "integration_level_contract_implemented": False,
    "system_level_test_plan_implemented": False,
    "runtime_adapter_ready": False,
    "whitebox_runtime_ready": False,
    "real_execution_authorization_ready": False,
    "runtime_not_ready": True,
    "real_execution_not_ready": True,
    "integration_test_planning_deferred": True,
}

NEXT_MODULE_CANDIDATES: Tuple[Dict[str, Any], ...] = (
    {"route_id": "A", "module": "Module Handoff Contract Controlled Implementation",
     "phase_id": "Phase-Midplatform-Module-Handoff-Contract-Controlled-Implementation-v1-001", "priority": "P1"},
    {"route_id": "B", "module": "Candidate Lifecycle Manager Controlled Implementation",
     "phase_id": "Phase-Midplatform-Candidate-Lifecycle-Manager-Controlled-Implementation-v1-001", "priority": "P2"},
    {"route_id": "C", "module": "Evidence Alignment Controlled Implementation",
     "phase_id": "Phase-Midplatform-Evidence-Alignment-Controlled-Implementation-v1-001", "priority": "P2"},
    {"route_id": "D", "module": "Midplatform Integration Contract Planning",
     "phase_id": "Phase-Midplatform-Integration-Contract-Planning-v1-001", "priority": "P3"},
    {"route_id": "E", "module": "Governance Debt Consolidation",
     "phase_id": "Phase-Midplatform-Governance-Debt-Consolidation-v1-001", "priority": "P3"},
)

SELECTED_NEXT_MODULE = "Module Handoff Contract Controlled Implementation"
SELECTED_NEXT_ROUTE = "Phase-Midplatform-Module-Handoff-Contract-Controlled-Implementation-v1-001"
NEXT_ROUTE_A = SELECTED_NEXT_ROUTE
NEXT_ROUTE_B = "Phase-Midplatform-Candidate-Lifecycle-Manager-Controlled-Implementation-v1-001"
NEXT_ROUTE_C = "Phase-Midplatform-Evidence-Alignment-Controlled-Implementation-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Integration-Contract-Planning-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Governance-Debt-Consolidation-v1-001"

DO_NOT_REOPEN_RULES: Tuple[str, ...] = (
    "core_orchestration_submodule_not_extended_after_module_dryrun_go",
    "owner_approval_request_chain_not_reopened",
    "l1_protocol_not_re_reviewed",
    "shared_protocol_not_re_run",
    "future_brain_interface_not_implemented",
    "controlled_skeleton_dryrun_go_not_runtime_ready",
    "module_dryrun_go_not_midplatform_completed",
    "no_fragmentary_core_orchestration_phases",
)
