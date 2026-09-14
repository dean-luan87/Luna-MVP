# -*- coding: utf-8 -*-
"""Field-First Core Recalibration item definitions v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

OLD_ROUTE = (
    "multi_source_information",
    "information_processing_core",
    "midplatform_model_direct_understanding",
    "candidate_judgment",
)

NEW_ROUTE = (
    "multi_source_information",
    "source_adapter_source_basket",
    "unified_observation_candidate",
    "field_model",
    "field_simulation",
    "task_field_view_simulation_result",
    "midplatform_reasoning_candidate",
)

CORE_ROUTE_ADJUSTMENT: Dict[str, Any] = {
    "adjustment_id": "core_route_adjustment_v1",
    "old_route": list(OLD_ROUTE),
    "new_route": list(NEW_ROUTE),
    "key_change": "midplatform_model_reads_structured_field_simulation_not_raw_world",
    "ipc_no_longer_direct_center": True,
    "field_first_midplatform_core": True,
}

FIELD_FIRST_CONCEPTS: Dict[str, Any] = {
    "definition_id": "field_first_core_concept_definition_v1",
    "world_model": "long_term_cross_scene_stable_objects_places_rules_relations_history_patterns",
    "field_model": "current_time_space_user_task_local_world_state_not_entire_world",
    "relationship": "world_model_background_perception_realtime_task_goal_scopes_field_simulation_decides",
    "midplatform_core_phase1": (
        "build_field", "update_field", "simulate_field", "generate_task_field_view", "output_reasoning_candidate",
    ),
}

FIELD_MODEL_LAYERS: Tuple[Dict[str, Any], ...] = (
    {"layer_id": "ecs_layer", "purpose": "entities_components_attributes_states", "examples": ("cup_001.material=ceramic", "car_001.mobility_state=stopped")},
    {"layer_id": "dynamic_scene_graph_layer", "purpose": "spatial_temporal_reachability_occlusion_blocking", "examples": ("cup_001 on table_001", "car_001 blocks lane_002")},
    {"layer_id": "lightweight_semantic_event_graph_layer", "purpose": "event_semantics_risk_rules_task_meaning", "examples": ("traffic_accident_001 involves car_001", "risk_zone_001 requires caution")},
)

SOURCE_MOUNTING: Dict[str, Any] = {
    "model_id": "source_mounting_model_v1",
    "path": ("frontend_source", "source_adapter", "source_basket", "observation_candidate", "field_model_builder", "field_update_candidate"),
    "source_types": ("vision", "ocr", "asr_speech", "speaker_voiceprint", "tof_depth", "imu", "location_map", "user_instruction", "health_signal", "memory_recall", "external_api"),
    "source_profile_fields": (
        "source_type", "modality", "adapter_ref", "payload_schema", "confidence_mapping",
        "freshness_policy", "known_failure_modes", "risk_mapping", "update_frequency", "allowed_candidate_types",
    ),
    "principle": "new_source_adds_profile_and_adapter_not_core_change",
}

FIELD_BOUNDARY: Dict[str, Any] = {
    "model_id": "field_boundary_model_v1",
    "standard": "self_centered_dynamic_field_boundary",
    "default_radius_m": 20,
    "zones": (("inner_zone", "0-3m"), ("working_zone", "3-10m"), ("forecast_zone", "10-20m")),
    "speed_adaptation": ("stationary_shrink", "walk_standard", "fast_walk_expand", "run_safety_expand"),
    "task_adaptation": ("navigation", "reading", "find_object", "road_crossing"),
    "risk_adaptation": "higher_risk_larger_field_higher_refresh_overload_shrink_to_task_field_view",
}

FIELD_CONTINUITY: Dict[str, Any] = {
    "model_id": "field_continuity_model_v1",
    "field_session_fields": (
        "field_id", "task_goal_ref", "user_state_ref", "spatial_anchor", "time_window",
        "active_entities", "active_relations", "active_events", "history_buffer", "continuity_status",
    ),
    "continuity_rules": ("entity_id_continuous", "state_history_continuous", "confidence_continuous", "occlusion_lost_recover_continuous", "no_reset_while_task_active"),
    "visibility_states": ("visible", "occluded_candidate", "lost_candidate", "forgotten"),
}

FIELD_SIMULATION: Dict[str, Any] = {
    "model_id": "field_simulation_model_v1",
    "modes": ("past_reconstruction", "current_state_estimation", "future_projection"),
    "task_modes": {
        "navigation": ("passable_area", "obstacles", "dynamic_trajectories", "collision_risk", "path_block", "safety_window"),
        "find_object": ("target_candidates", "possible_locations", "last_seen", "visible_region", "occlusion", "next_observe_position"),
        "reading": ("text_region", "ocr_readability", "distance_angle", "occlusion", "move_closer_or_adjust"),
        "road_crossing": ("traffic_light", "vehicle_trajectory", "pedestrian_flow", "crosswalk", "safety_window_3_5s", "blind_spot"),
    },
    "output_type": "FieldSimulationResultCandidate",
}

MIDPLATFORM_REASONING_INPUT: Dict[str, Any] = {
    "model_id": "midplatform_reasoning_input_model_v1",
    "reads": ("task_field_view", "field_simulation_result", "risk_summary", "conflict_summary", "missing_information", "candidate_reasoning_context"),
    "does_not_read": ("full_field_model_raw", "all_raw_information"),
    "responsibilities": ("understand_simulation", "judge_task_continuable", "judge_info_insufficient", "judge_active_perception_needed", "candidate_suggestions", "mark_risk_gap_conflict_downstream"),
    "forbidden": ("direct_world_model_write", "create_facts", "execute_actions", "authorize", "long_term_memory_write", "replace_field_simulation"),
}

DRIVE_LAYER_FIELD: Dict[str, Any] = {
    "model_id": "drive_layer_field_relationship_v1",
    "survival_drive": "reads_risk_dynamic_obstacles_health_can_interrupt_expand_refresh",
    "task_drive": "generates_task_field_view_focus_entities_relations_events_history_future",
    "reflection_drive": "post_task_analysis_misidentification_source_reliability_field_scope_correction_candidate",
}

PERCEPTION_LOOP: Dict[str, Any] = {
    "model_id": "perception_request_loop_model_v1",
    "chain": ("field_gap", "perception_need", "perception_request_candidate", "frontend_guidance", "new_observation_candidate", "field_update"),
    "examples": ("look_left", "inspect_region", "move_closer", "adjust_angle", "wait_and_observe"),
    "closed_loop": "observe_organize_gap_request_update_simulate_reason",
}

ATTRIBUTE_TIERS: Tuple[Dict[str, str], ...] = (
    {"tier": "stable", "examples": "material_shape_brand_color", "update": "low_frequency_strong_evidence"},
    {"tier": "semi_stable", "examples": "sticker_wear_cleanliness", "update": "medium_overwritable"},
    {"tier": "realtime_state", "examples": "position_held_water_level_speed", "update": "high_frequency_short_ttl"},
    {"tier": "relation", "examples": "ownership_shared_use", "update": "multi_observation_or_confirm"},
    {"tier": "emotional_life", "examples": "favorite_memorial_comfort", "update": "long_term_candidate_no_single_obs_fact"},
)

IPC_REPOSITIONING: Dict[str, Any] = {
    "review_id": "ipc_repositioning_review_v1",
    "ipc_status": "retained_as_support_not_direct_center",
    "ipc_prior_work_preserved": True,
    "ipc_role_in_new_route": "observation_normalization_support_upstream_of_field_not_final_reasoner",
    "ipc_not_invalidated": True,
}

DEFERRED_ROUTES: Tuple[Dict[str, Any], ...] = (
    {"route_id": "ipc_self_work_dryrun_review", "status": "deferred", "reason": "field_first_recalibration_priority"},
    {"route_id": "candidate_lifecycle_manager", "status": "deferred", "reason": "core_not_fixed_peripheral_premature"},
    {"route_id": "module_handoff_contract", "status": "deferred_p3", "reason": "peripheral_contract_premature"},
    {"route_id": "integration_test", "status": "deferred", "reason": "no_runtime"},
)

NEXT_WORK_ITEMS: Tuple[str, ...] = (
    "define_field_model", "define_field_session", "define_ecs_layer",
    "define_dynamic_scene_graph_layer", "define_semantic_event_graph_layer",
    "define_source_adapter_basket_mounting", "define_field_update_candidate",
    "define_field_boundary", "define_field_continuity", "define_field_simulation",
    "define_task_field_view", "define_drive_layer_field_relationship",
    "define_perception_request_candidate", "define_midplatform_reads_simulation_result",
)

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "field_model_not_world_model",
    "field_simulation_result_not_final_fact",
    "observation_candidate_not_record",
    "perception_request_not_runtime_action",
    "ipc_reposition_not_ipc_deletion",
    "recalibration_not_midplatform_completed",
    "field_first_not_frontend_hardware_integration",
    "handoff_contract_still_p3_defer",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Core-Work-Manual-and-Architecture-Definition-v1-001"
SELECTED_NEXT_ROUTE = "Field-First Core Work Manual and Architecture Definition"
ALTERNATE_NEXT_PHASE = "Phase-Midplatform-Field-Model-Self-Work-Core-Design-v1-001"
