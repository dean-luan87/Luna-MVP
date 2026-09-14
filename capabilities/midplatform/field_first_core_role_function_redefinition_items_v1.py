# -*- coding: utf-8 -*-
"""Field-First Core Role Function Redefinition item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

ROLE_PRINCIPLES: Dict[str, Any] = {
    "principles_id": "role_principles_v1",
    "framework": "upstream_self_downstream_three_part",
    "current_focus": "self_work_core_responsibility_per_role",
    "no_premature_upstream_downstream_contract": True,
    "rules": (
        "core_roles_first",
        "support_roles_retained_not_defining_core",
        "peripheral_roles_deferred",
        "roles_do_not_swallow_each_other",
    ),
}

ROLE_SEPARATION_RULES: Tuple[str, ...] = (
    "normalization_does_not_simulate_field",
    "field_builder_does_not_final_decide",
    "drive_layer_does_not_write_world_model",
    "midplatform_reasoning_does_not_execute_actions",
    "boundary_controller_does_not_entity_model",
    "continuity_manager_does_not_replace_field_builder",
    "simulation_operator_does_not_final_conclude",
    "task_view_builder_does_not_raw_recognize",
)

CORE_ROLES: Tuple[Dict[str, Any], ...] = (
    {
        "role_id": "source_intake_normalization_operator",
        "name_en": "Source Intake & Normalization Operator",
        "name_zh": "信息源接收与标准化员",
        "category": "core",
        "priority": "P1",
        "ipc_reposition": "IPC retained as implementation asset for observation normalization",
        "self_work": (
            "parse_source_payload", "standardize_source_metadata",
            "annotate_confidence_freshness_risk_task_relevance",
            "generate_observation_candidate", "retain_source_adapter_traceability_refs",
        ),
        "not_responsible": (
            "create_field", "long_term_entity_merge", "field_simulation",
            "task_decision", "write_world_model_facts",
        ),
        "outputs": ("ObservationCandidate",),
    },
    {
        "role_id": "field_model_builder",
        "name_en": "Field Model Builder",
        "name_zh": "场模型构建员",
        "category": "core",
        "priority": "P0",
        "self_work": (
            "create_field_session", "establish_entity_candidates",
            "mount_entity_attribute_components", "build_spatial_temporal_reachability_relations",
            "build_semantic_event_nodes", "annotate_quality_conflict_expiry_gap",
            "output_field_model_candidate_field_update_candidate",
        ),
        "not_responsible": (
            "long_term_world_model_admission", "final_task_decision",
            "direct_frontend_action", "execute_real_actions",
        ),
        "outputs": ("FieldModelCandidate", "FieldUpdateCandidate"),
    },
    {
        "role_id": "field_state_continuity_manager",
        "name_en": "Field State & Continuity Manager",
        "name_zh": "场状态与连续性管理员",
        "category": "core",
        "priority": "P0",
        "self_work": (
            "maintain_field_session", "maintain_entity_id_continuity",
            "maintain_state_history", "handle_visible_occluded_lost_forgotten",
            "handle_attribute_ttl", "handle_dynamic_object_state_change",
            "decide_field_reset_continue_split_merge",
        ),
        "not_responsible": (
            "redefine_sources", "replace_field_builder", "replace_world_model", "task_reasoning",
        ),
        "outputs": ("FieldSessionUpdateCandidate",),
    },
    {
        "role_id": "field_boundary_controller",
        "name_en": "Field Boundary Controller",
        "name_zh": "场边界控制员",
        "category": "core",
        "priority": "P0",
        "self_work": (
            "user_centered_20m_default", "inner_working_forecast_zones",
            "speed_adapt_radius_refresh", "task_direction_weighting",
            "risk_expand_field", "overload_shrink_to_task_field_view",
            "output_field_boundary_candidate",
        ),
        "not_responsible": (
            "perception_recognition", "in_field_entity_modeling", "simulation", "midplatform_candidate_judgment",
        ),
        "outputs": ("FieldBoundaryCandidate",),
    },
    {
        "role_id": "field_simulation_operator",
        "name_en": "Field Simulation Operator",
        "name_zh": "场推演员",
        "category": "core",
        "priority": "P0",
        "self_work": (
            "past_reconstruction", "current_state_estimation", "future_projection",
            "predict_dynamic_trajectories", "judge_path_collision_occlusion_reachability",
            "output_field_simulation_result_candidate",
        ),
        "task_modes": {
            "navigation": ("passable_area", "obstacles", "dynamic_objects", "risk_window"),
            "find_object": ("target_candidates", "possible_locations", "occlusion", "next_observe_position"),
            "reading": ("text_region", "readability", "angle_distance", "occlusion"),
            "road_crossing": ("traffic_light", "vehicle_trajectory", "pedestrian_flow", "safety_window"),
        },
        "not_responsible": (
            "execute_navigation", "final_conclusion", "replace_midplatform_interpretation", "write_long_term_world_model",
        ),
        "outputs": ("FieldSimulationResultCandidate",),
    },
    {
        "role_id": "task_field_view_builder",
        "name_en": "Task Field View Builder",
        "name_zh": "任务场视图生成员",
        "category": "core",
        "priority": "P0",
        "self_work": (
            "read_task_goal", "select_task_entities_relations_events",
            "summarize_risk_conflict_missing", "generate_task_field_view_candidate",
            "limit_context_scale_prevent_overload",
        ),
        "not_responsible": (
            "raw_recognition", "full_world_understanding", "final_judgment", "direct_frontend_control",
        ),
        "outputs": ("TaskFieldViewCandidate",),
    },
    {
        "role_id": "midplatform_field_reasoning_operator",
        "name_en": "Midplatform Field Reasoning Operator",
        "name_zh": "中台场推理员",
        "category": "core",
        "priority": "P0",
        "self_work": (
            "understand_task_goal", "understand_simulation_result",
            "judge_info_sufficient", "judge_risk_acceptable",
            "judge_need_active_perception", "judge_need_governance_review",
            "output_midplatform_reasoning_candidate",
        ),
        "output_types": (
            "route_candidate", "risk_candidate", "defer_candidate", "need_more_info_candidate",
            "perception_request_need", "governance_review_candidate",
            "task_continue_candidate", "task_blocked_candidate",
        ),
        "not_responsible": (
            "direct_raw_world_understanding", "read_all_raw_sources",
            "direct_field_model_write", "create_facts", "execute_actions",
            "authorize", "write_long_term_memory",
        ),
        "outputs": ("MidplatformReasoningCandidate",),
    },
)

DRIVE_LAYER_ROLES: Tuple[Dict[str, Any], ...] = (
    {
        "role_id": "survival_drive_controller",
        "name_en": "Survival Drive Controller",
        "name_zh": "生存驱动控制员",
        "category": "drive",
        "priority": "P1",
        "self_work": (
            "read_risk_field", "read_dynamic_object_risk", "read_path_safety_risk",
            "read_health_permission_privacy_risk", "interrupt_task_when_needed",
            "expand_field_or_raise_refresh", "trigger_perception_request_candidate",
        ),
    },
    {
        "role_id": "task_drive_controller",
        "name_en": "Task Drive Controller",
        "name_zh": "任务驱动控制员",
        "category": "drive",
        "priority": "P1",
        "self_work": (
            "maintain_task_goal", "specify_task_entities_relations",
            "specify_task_field_view_requirements", "specify_field_simulation_type",
            "judge_task_continue_pause_redirect_end",
        ),
    },
    {
        "role_id": "reflection_drive_controller",
        "name_en": "Reflection Drive Controller",
        "name_zh": "反思驱动控制员",
        "category": "drive",
        "priority": "P2",
        "self_work": (
            "analyze_misidentification", "analyze_miss_detection",
            "analyze_source_reliability", "analyze_field_boundary_size",
            "analyze_simulation_error", "generate_future_correction_candidate",
        ),
    },
)

SUPPORT_ROLES: Tuple[Dict[str, Any], ...] = (
    {
        "role_id": "traceability_recorder",
        "name_en": "Traceability Recorder",
        "name_zh": "追溯记录员",
        "category": "support",
        "priority": "P2",
        "self_work": ("record_source_evidence_field_simulation_reasoning_refs",),
    },
    {
        "role_id": "governance_referee",
        "name_en": "Governance Referee",
        "name_zh": "治理裁判",
        "category": "support",
        "priority": "P2",
        "self_work": ("handle_safety_authorization_privacy_health_permission_owner_approval",),
    },
    {
        "role_id": "world_model_admission_gate",
        "name_en": "World Model Admission Gate",
        "name_zh": "世界模型准入门",
        "category": "support",
        "priority": "P2",
        "self_work": ("judge_field_info_for_long_term_world_model_admission",),
        "implementation": "interface_only_not_full_admission",
    },
    {
        "role_id": "candidate_lifecycle_manager",
        "name_en": "Candidate Lifecycle Manager",
        "name_zh": "候选生命周期管理员",
        "category": "support",
        "priority": "P3_defer",
        "status": "deferred",
        "reason": "wait_for_field_reasoning_stability",
    },
    {
        "role_id": "module_handoff_contract_manager",
        "name_en": "Module Handoff Contract Manager",
        "name_zh": "模块交接契约管理员",
        "category": "support",
        "priority": "P3_defer",
        "status": "deferred_p3",
        "reason": "must_not_reverse_limit_core",
    },
)

ROLE_MAIN_CHAIN: Tuple[str, ...] = (
    "source_intake_normalization_operator",
    "field_model_builder",
    "field_state_continuity_manager",
    "field_boundary_controller",
    "field_simulation_operator",
    "task_field_view_builder",
    "midplatform_field_reasoning_operator",
    "drive_layer_controllers",
    "perception_request_candidate",
    "frontend_active_sensing",
)

CLOSED_LOOP_CHAIN: Tuple[str, ...] = (
    "frontend_observe",
    "normalize_observation_candidate",
    "build_field",
    "update_field",
    "simulate_field",
    "generate_task_field_view",
    "midplatform_candidate_judgment",
    "drive_layer_gap_detection",
    "active_perception_request",
    "frontend_supplement_observe",
    "field_update",
)

ROLE_PRIORITY: Dict[str, Tuple[str, ...]] = {
    "P0_must_define": (
        "field_model_builder", "field_state_continuity_manager", "field_boundary_controller",
        "field_simulation_operator", "task_field_view_builder", "midplatform_field_reasoning_operator",
    ),
    "P1_support_define": (
        "source_intake_normalization_operator", "survival_drive_controller",
        "task_drive_controller", "perception_request_candidate",
    ),
    "P2_light_reserve": (
        "reflection_drive_controller", "traceability_recorder", "governance_referee",
        "world_model_admission_gate",
    ),
    "P3_defer": (
        "candidate_lifecycle_manager", "module_handoff_contract_manager", "integration_contract_manager",
    ),
}

PRIOR_WORK_REPOSITIONING: Tuple[Dict[str, Any], ...] = (
    {"asset_id": "information_processing_core", "new_role": "source_intake_normalization_operator_implementation_asset", "invalidated": False},
    {"asset_id": "task_manager_core_orchestration", "new_role": "future_routing_after_field_reasoning", "invalidated": False},
    {"asset_id": "candidate_lifecycle_unification", "new_role": "candidate_state_governance_asset_not_current_mainline", "invalidated": False},
    {"asset_id": "evidence_record_approval_permission_alignment", "new_role": "future_governance_admission_asset", "invalidated": False},
    {"asset_id": "module_handoff_contract", "new_role": "p3_defer_continues", "invalidated": False, "status": "deferred_p3"},
)

WORK_MANUAL_OUTPUTS: Tuple[str, ...] = (
    "midplatform_role_function_table",
    "field_model_work_manual",
    "field_session_work_manual",
    "field_boundary_work_manual",
    "field_continuity_work_manual",
    "field_simulation_work_manual",
    "task_field_view_work_manual",
    "midplatform_field_reasoning_work_manual",
    "drive_layer_field_relationship_manual",
    "perception_request_candidate_draft",
    "prior_asset_repositioning_table",
)

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "role_redefinition_not_implementation",
    "core_role_not_single_ipc",
    "support_role_not_core_mainline",
    "deferred_role_not_auto_advanced_by_prior_go",
    "drive_controller_not_processing_operator",
    "perception_request_not_runtime_action",
    "role_definition_not_downstream_contract",
    "field_first_org_not_world_model_implementation",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Core-Work-Manual-and-Architecture-Definition-v1-001"
SELECTED_NEXT_ROUTE = "Field-First Core Work Manual and Architecture Definition"
NEXT_PHASE_FINAL_DECISION_TARGET = "MIDPLATFORM_FIELD_FIRST_CORE_WORK_MANUAL_AND_ARCHITECTURE_READY_FOR_FIELD_MODEL_SELF_WORK_CORE_DESIGN"
