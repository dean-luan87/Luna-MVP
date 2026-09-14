# -*- coding: utf-8 -*-
"""Core Capability and Peripheral Service Recalibration item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

CAPABILITY_FRAMEWORK: Dict[str, Any] = {
    "framework_id": "midplatform_capability_framework_v1",
    "capability_scope": (
        "Midplatform is the center layer for information processing, candidate object governance, "
        "module collaboration scheduling, evidence tracing, and state transition at candidate level."
    ),
    "collaboration_mode": "candidate_first_module_coordination",
    "upstream_intake_mode": "receive_normalize_candidate_inputs_with_traceability",
    "internal_processing_mode": "boundary_lifecycle_alignment_governance_checks_then_candidate_outputs",
    "downstream_handoff_mode": "emit_handoff_candidates_not_real_handoff_execution",
    "governance_support_mode": "safety_authorization_privacy_hard_constraints_only",
    "non_execution_boundary": True,
    "not_protocol_repository": True,
    "not_task_list_only": True,
    "not_governance_gate_collection_only": True,
}

CORE_FUNCTION_DEFINITION: Dict[str, Any] = {
    "definition_id": "midplatform_core_function_definition_v1",
    "primary_core_function": "Information Processing Core",
    "secondary_core_functions": ("Candidate Processing Core", "Orchestration Decision Core"),
    "non_core_support_functions": (
        "boundary_registry_support", "protocol_traceability_support",
        "governance_constraint_support", "module_handoff_contract_support",
        "integration_contract_support", "file_size_governance_support",
    ),
    "why_this_is_core": (
        "Midplatform receives information, normalizes to candidates, applies checks, "
        "produces candidate-level decisions and handoff outputs, maintains traceability "
        "without executing runtime actions."
    ),
    "what_must_not_constrain_core": (
        "peripheral_contracts_must_not_block_candidate_reasoning",
        "protocol_adaptation_must_not_dominate_core_definition",
        "handoff_walls_must_not_predefine_core_output_expression",
        "management_rules_must_not_override_non_safety_core_processing",
    ),
    "information_processing_meaning": (
        "receive_information", "identify_information_type", "judge_information_state",
        "normalize_to_candidate", "boundary_lifecycle_alignment_governance_checks",
        "generate_route_defer_reject_close_handoff_candidates",
        "generate_traceability_bundle", "update_candidate_level_state_on_feedback",
        "no_real_runtime_action",
    ),
}


def _module(module_id: str, module_role: str, core_relation: str, priority: str, *, constrain: bool = False) -> Dict[str, Any]:
    return {
        "module_id": module_id, "module_role": module_role, "core_relation": core_relation,
        "should_constrain_core": constrain, "should_serve_core": True,
        "current_priority_after_recalibration": priority,
    }


CORE_MODULE_SELECTION: Tuple[Dict[str, Any], ...] = (
    _module("task_manager_core_orchestration", "orchestration_decision_skeleton", "core", "P0"),
    _module("candidate_lifecycle_manager", "candidate_state_processing", "core", "P1"),
    _module("information_processing_core", "upstream_intake_and_normalization", "core", "P1"),
    _module("module_boundary_registry", "boundary_ref_support", "core_support", "P2"),
    _module("evidence_record_approval_permission_alignment", "alignment_ref_support", "core_support", "P2"),
    _module("protocol_registry_input_output_traceability", "traceability_support", "core_support", "P2"),
    _module("governance_constraints", "safety_authorization_constraints", "governance_support", "P2", constrain=True),
    _module("module_handoff_contract", "downstream_handoff_contract", "peripheral_contract", "P3"),
    _module("integration_contract", "cross_module_integration_contract", "peripheral_contract", "P4"),
    _module("owner_approval_request_closed_module", "closed_authorization_subchain", "peripheral_contract", "deferred"),
    _module("file_size_governance", "engineering_quality_support", "governance_support", "P3"),
    _module("task_center_drive_brain", "future_drive_brain", "future_design", "future"),
    _module("survival_brain", "future_survival_brain", "future_design", "future"),
    _module("reflection_brain", "future_reflection_brain", "future_design", "future"),
    _module("health_memory_world_model_hooks", "future_integration_hooks", "future_design", "future"),
)

PERIPHERAL_SERVICE_PRINCIPLES: Tuple[Dict[str, Any], ...] = (
    {"service_id": "boundary", "serves_core": True, "principle": "prevent_role_confusion_without_locking_core_evolution"},
    {"service_id": "lifecycle", "serves_core": True, "principle": "help_core_judge_state_without_blocking_candidate_results"},
    {"service_id": "alignment", "serves_core": True, "principle": "prevent_mistaken_promotion_without_blocking_candidate_reasoning"},
    {"service_id": "governance", "serves_core": True, "principle": "prevent_overreach_without_blocking_information_processing"},
    {"service_id": "protocol", "serves_core": True, "principle": "stabilize_collaboration_without_forcing_wrong_protocol_fit"},
    {"service_id": "handoff", "serves_core": True, "principle": "carry_core_outputs_without_premature_hard_handoff_walls"},
    {"service_id": "constitution", "serves_core": True, "principle": "protect_safety_floor_without_suppressing_core_growth"},
    {"service_id": "file_size_governance", "serves_core": True, "principle": "support_engineering_quality_without_driving_business_structure"},
)

CORE_CAPABILITY_MARKING: Tuple[Dict[str, Any], ...] = (
    {"capability_id": "can_receive_candidate", "status": "marked", "evidence_ref": "orchestration_input_candidate", "blocking_gap": None, "peripheral_dependency": "boundary_registry_ref", "should_extend_core_next": False},
    {"capability_id": "can_normalize_input", "status": "marked", "evidence_ref": "normalize_orchestration_input", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_check_boundary_refs", "status": "marked", "evidence_ref": "check_boundary_for_candidate", "blocking_gap": None, "peripheral_dependency": "module_boundary_registry_planning", "should_extend_core_next": False},
    {"capability_id": "can_check_lifecycle_refs", "status": "partial", "evidence_ref": "check_lifecycle_for_candidate", "blocking_gap": "candidate_lifecycle_manager_runtime_absent", "peripheral_dependency": "candidate_lifecycle_unification_planning", "should_extend_core_next": True},
    {"capability_id": "can_check_alignment_refs", "status": "marked", "evidence_ref": "check_alignment_for_candidate", "blocking_gap": None, "peripheral_dependency": "evidence_record_approval_permission_alignment_planning", "should_extend_core_next": False},
    {"capability_id": "can_check_governance_refs", "status": "marked", "evidence_ref": "check_governance_for_candidate", "blocking_gap": None, "peripheral_dependency": "governance_constraints", "should_extend_core_next": False},
    {"capability_id": "can_build_route_candidate", "status": "marked", "evidence_ref": "produce_candidate_route", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_build_handoff_candidate", "status": "marked", "evidence_ref": "produce_module_handoff_candidate", "blocking_gap": "module_handoff_contract_not_implemented", "peripheral_dependency": "module_handoff_contract", "should_extend_core_next": False},
    {"capability_id": "can_build_traceability_bundle", "status": "marked", "evidence_ref": "produce_traceability_bundle", "blocking_gap": None, "peripheral_dependency": "protocol_registry_input_output_traceability", "should_extend_core_next": False},
    {"capability_id": "can_build_blocker_decision", "status": "marked", "evidence_ref": "blocker_decision_path_dryrun", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_build_defer_decision", "status": "marked", "evidence_ref": "defer_decision_path_dryrun", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_build_reject_decision", "status": "marked", "evidence_ref": "reject_decision_path_dryrun", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_build_close_decision", "status": "marked", "evidence_ref": "close_decision_path_dryrun", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_assemble_orchestration_result", "status": "marked", "evidence_ref": "assemble_orchestration_result", "blocking_gap": None, "peripheral_dependency": None, "should_extend_core_next": False},
    {"capability_id": "can_hold_non_execution_boundary", "status": "marked", "evidence_ref": "module_level_controlled_dryrun_11_11", "blocking_gap": None, "peripheral_dependency": "governance_constraints", "should_extend_core_next": False},
    {"capability_id": "can_identify_information_type", "status": "missing", "evidence_ref": None, "blocking_gap": "information_processing_core_not_implemented", "peripheral_dependency": None, "should_extend_core_next": True},
    {"capability_id": "can_update_candidate_state_on_feedback", "status": "missing", "evidence_ref": None, "blocking_gap": "candidate_lifecycle_manager_runtime_absent", "peripheral_dependency": "candidate_lifecycle_manager", "should_extend_core_next": True},
)

CONFLICT_RESOLUTION_RULES: Tuple[str, ...] = (
    "if_protocol_limits_core_reasoning_modify_protocol_not_core",
    "if_governance_blocks_candidate_result_modify_governance_unless_safety_critical",
    "if_boundary_prematurely_locks_core_adjust_boundary_not_core_scope",
    "if_handoff_contract_limits_core_output_modify_handoff_contract",
    "constitution_safety_floor_core_must_obey",
    "only_safety_authorization_privacy_critical_may_hard_constrain_core",
    "ordinary_management_rules_must_not_override_core_capability",
)

ROUTE_REASSESSMENT: Tuple[Dict[str, Any], ...] = (
    {"route_id": "A", "route": "information_processing_core_controlled_implementation", "enhances_core_directly": True, "peripheral_only": False, "premature_wall_risk": False, "recalibrated_priority": "P1"},
    {"route_id": "B", "route": "candidate_lifecycle_manager_controlled_implementation", "enhances_core_directly": True, "peripheral_only": False, "premature_wall_risk": False, "recalibrated_priority": "P1"},
    {"route_id": "C", "route": "task_manager_core_orchestration_capability_expansion", "enhances_core_directly": True, "peripheral_only": False, "premature_wall_risk": False, "recalibrated_priority": "P2"},
    {"route_id": "D", "route": "module_handoff_contract_controlled_implementation", "enhances_core_directly": False, "peripheral_only": True, "premature_wall_risk": True, "recalibrated_priority": "P3"},
    {"route_id": "E", "route": "integration_contract_planning", "enhances_core_directly": False, "peripheral_only": True, "premature_wall_risk": True, "recalibrated_priority": "P4"},
)

SELECTED_NEXT_ROUTE = "Information Processing Core Controlled Implementation"
SELECTED_ROUTE_ID = "A"
NEXT_PHASE_GO = "Phase-Midplatform-Information-Processing-Core-Controlled-Implementation-v1-001"
NEXT_PHASE_ALTERNATE = "Phase-Midplatform-Candidate-Lifecycle-Manager-Controlled-Implementation-v1-001"
NEXT_ROUTE_B = NEXT_PHASE_ALTERNATE
NEXT_ROUTE_C = "Phase-Midplatform-Task-Manager-Core-Orchestration-Capability-Expansion-v1-001"
NEXT_ROUTE_D = "Phase-Midplatform-Module-Handoff-Contract-Controlled-Implementation-v1-001"
NEXT_ROUTE_E = "Phase-Midplatform-Integration-Contract-Planning-v1-001"

DO_NOT_MISCLASSIFY_RULES: Tuple[str, ...] = (
    "handoff_contract_p1_gap_not_must_implement_immediately",
    "peripheral_contract_not_core_capability",
    "governance_support_not_core_driver",
    "protocol_rule_not_core_definition",
    "boundary_rule_not_core_architecture",
    "module_dryrun_go_not_midplatform_completed",
    "core_capability_marking_not_runtime_readiness",
    "core_first_recalibration_not_invalidate_prior_go",
    "future_brain_design_not_current_implementation",
)
