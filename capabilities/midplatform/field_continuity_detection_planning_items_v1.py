# -*- coding: utf-8 -*-
"""Field Continuity Detection Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SCOPE_DEFINITION: Dict[str, Any] = {
    "scope_id": "field_continuity_scope_v1",
    "goal": "plan_field_continuity_detection_between_field_scene_candidates",
    "planning_only": True,
    "core_question": "Is current field the same field, shifted same field, or new field?",
    "upstream_outputs": ("FieldSceneCandidate", "FieldEntityCandidate", "FieldSceneConstructionResultCandidate"),
    "not_in_scope": ("real_tracking", "video_inference", "trajectory_simulation", "task_simulation", "semantic_attachment", "world_model_fact", "persistent_memory", "runtime"),
}

CONTINUITY_STATUSES: Tuple[str, ...] = (
    "same_field", "field_shift", "field_occluded", "field_lost", "field_recovering",
    "new_field_required", "uncertain_need_recheck",
)

RECOMMENDED_ACTIONS: Tuple[str, ...] = (
    "keep_session", "keep_session_with_shift", "mark_occluded", "mark_lost",
    "attempt_recovery", "create_new_session_candidate", "request_recheck_observation",
)

FIELD_SESSION_STATES: Tuple[str, ...] = ("active", "shifted", "occluded", "lost", "recovering", "closed", "replaced")

STATE_TRANSITIONS: Tuple[Dict[str, str], ...] = (
    {"from": "active", "to": "shifted"}, {"from": "active", "to": "occluded"},
    {"from": "active", "to": "lost"}, {"from": "active", "to": "closed"},
    {"from": "shifted", "to": "active"}, {"from": "occluded", "to": "active"},
    {"from": "occluded", "to": "lost"}, {"from": "lost", "to": "recovering"},
    {"from": "lost", "to": "replaced"}, {"from": "recovering", "to": "active"},
    {"from": "recovering", "to": "replaced"},
)

SIGNAL_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {"signal_id": "location_continuity_signal", "sources": ("GPS", "map_location_hint", "user_state.location_hint"), "rules": ("location_close_supports_same_field", "location_jump_supports_new_field_required", "location_missing_weak_unknown")},
    {"signal_id": "camera_heading_signal", "sources": ("CameraStateCandidate.heading_hint", "IMU_heading_placeholder"), "rules": ("heading_small_change_same_field", "heading_medium_change_field_shift", "heading_large_change_uncertain_or_new_field_possible")},
    {"signal_id": "key_entity_overlap_signal", "sources": ("FieldEntityCandidate.labels", "bbox", "pseudo_3d_position"), "rules": ("high_key_entity_overlap_same_field", "few_key_entities_missing_field_shift_or_occluded", "all_key_entities_replaced_new_field_required")},
    {"signal_id": "spatial_layout_similarity_signal", "sources": ("relative_entity_positions", "zone_distribution", "pseudo_3d_position"), "rules": ("layout_similar_same_field", "layout_translated_or_rotated_field_shift", "layout_completely_different_new_field_required")},
    {"signal_id": "visual_quality_change_signal", "sources": ("brightness_hint", "blur_hint", "low_light_hint", "motion_state"), "rules": ("sudden_dark_field_occluded_or_uncertain", "strong_motion_blur_field_occluded_or_uncertain", "low_visual_quality_not_immediate_new_field")},
    {"signal_id": "occlusion_signal", "sources": ("large_unknown_foreground", "entity_count_sudden_drop"), "rules": ("brief_occlusion_field_occluded", "long_occlusion_field_lost")},
    {"signal_id": "time_gap_signal", "sources": ("timestamp_gap_seconds",), "rules": ("short_gap_same_field_possible", "medium_gap_uncertain_need_recheck", "long_gap_field_lost_or_new_field_required")},
    {"signal_id": "session_recovery_signal", "sources": ("previous_lost_field", "key_entity_overlap", "location_heading_consistency"), "rules": ("recoverable_field_recovering", "not_recoverable_new_field_required")},
)

DECISION_MODEL_FIELDS: Tuple[str, ...] = (
    "continuity_decision_id", "previous_field_scene_ref", "current_field_scene_ref",
    "previous_field_session_ref", "recommended_field_session_ref", "continuity_status",
    "continuity_confidence", "signal_results", "supporting_signals", "conflicting_signals",
    "reason_codes", "missing_information", "recommended_action", "should_keep_field_session",
    "should_create_new_field_session", "should_request_recheck", "non_execution_flags",
)

DECISION_MODEL: Dict[str, Any] = {
    "model_id": "field_continuity_decision_model_v1",
    "output_type": "FieldContinuityDecisionCandidate",
    "fields": list(DECISION_MODEL_FIELDS),
    "candidate_only": True,
    "multi_signal_voting": True,
    "recommended_actions": list(RECOMMENDED_ACTIONS),
}

ABNORMAL_CASE_POLICY: Dict[str, Any] = {
    "policy_id": "field_continuity_abnormal_case_policy_v1",
    "cases": (
        {"id": "camera_jitter_slight", "status": "field_shift"},
        {"id": "camera_jitter_severe", "status": "uncertain_need_recheck"},
        {"id": "sudden_dark", "status": "field_occluded"},
        {"id": "brief_occlusion", "status": "field_occluded"},
        {"id": "occlusion_recovery", "status": "field_recovering"},
        {"id": "power_cycle_resume", "status": "field_recovering"},
        {"id": "user_turn", "status": "field_shift"},
        {"id": "leave_room", "status": "new_field_required"},
        {"id": "all_key_entities_changed", "status": "new_field_required"},
        {"id": "missing_gps", "status": "same_field"},
    ),
}

INPUT_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_continuity_input_output_contract_v1",
    "inputs": ("FieldSceneCandidate(t-1)", "FieldSceneCandidate(t)", "CameraStateCandidate", "UserStateCandidate"),
    "output": "FieldContinuityDecisionCandidate",
    "candidate_only": True,
}

NEXT_IMPLEMENTATION_PLAN: Dict[str, Any] = {
    "plan_id": "field_continuity_next_implementation_plan_v1",
    "recommended_next": "Phase-Midplatform-Field-Continuity-Detection-Controlled-Skeleton-Implementation-v1-001",
    "deferred_to_skeleton": ("signal_scoring_engine", "decision_builder", "state_transition_validator"),
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "scope_id": "prohibited_scope_v1",
    "prohibited": ("real_tracking", "bytetrack", "yolo", "supervision", "model_download", "real_inference", "real_video_analysis", "trajectory_analysis", "task_simulation", "world_model_fact", "persistent_memory", "runtime", "integration_test"),
}

PLANNING_PRINCIPLES: Dict[str, Any] = {
    "principles_id": "field_continuity_planning_principles_v1",
    "rules": ("continuity_before_tracking", "no_rebuild_field_every_frame", "no_wrong_continuation_of_old_field", "multi_signal_voting_not_single_signal", "continuity_output_candidate_only"),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_tracking_implementation", "planning_not_video_inference",
    "continuity_decision_not_world_model_fact", "planning_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Continuity-Detection-Controlled-Skeleton-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Field Continuity Detection Controlled Skeleton Implementation"


def _case(case_id: str, status: str, action: str, signals: Dict[str, str], pass_cond: str) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "previous_field_summary": {"mock": True},
        "current_field_summary": {"mock": True},
        "signal_results": signals,
        "expected_status": status,
        "expected_recommended_action": action,
        "pass_condition": pass_cond,
    }


MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    _case("same_field_small_camera_jitter", "same_field", "keep_session", {"camera_heading_signal": "small_change", "key_entity_overlap_signal": "high"}, "high_overlap_small_heading"),
    _case("field_shift_user_turns_slightly", "field_shift", "keep_session_with_shift", {"camera_heading_signal": "medium_change", "key_entity_overlap_signal": "high"}, "same_entities_medium_heading"),
    _case("sudden_dark_occlusion", "field_occluded", "mark_occluded", {"visual_quality_change_signal": "sudden_dark"}, "dark_not_immediate_new_field"),
    _case("temporary_occlusion_then_recover", "field_recovering", "attempt_recovery", {"session_recovery_signal": "recoverable"}, "overlap_restored"),
    _case("large_heading_change_same_location", "field_shift", "keep_session_with_shift", {"camera_heading_signal": "large_change", "location_continuity_signal": "close"}, "large_heading_same_location"),
    _case("location_jump_new_field", "new_field_required", "create_new_session_candidate", {"location_continuity_signal": "jump", "key_entity_overlap_signal": "none"}, "location_and_entities_changed"),
    _case("key_entities_overlap_same_field", "same_field", "keep_session", {"key_entity_overlap_signal": "high", "spatial_layout_similarity_signal": "similar"}, "key_entities_match"),
    _case("key_entities_all_changed_new_field", "new_field_required", "create_new_session_candidate", {"key_entity_overlap_signal": "none"}, "all_key_entities_replaced"),
    _case("pause_resume_short_gap_recovering", "field_recovering", "attempt_recovery", {"time_gap_signal": "short", "session_recovery_signal": "recoverable"}, "short_gap_overlap"),
    _case("power_cycle_long_gap_uncertain_or_new_field", "uncertain_need_recheck", "request_recheck_observation", {"time_gap_signal": "long"}, "long_gap_weak_signals"),
    _case("missing_location_use_visual_layout", "same_field", "keep_session", {"location_continuity_signal": "missing", "spatial_layout_similarity_signal": "similar"}, "no_gps_layout_sufficient"),
    _case("low_entity_count_uncertain_need_recheck", "uncertain_need_recheck", "request_recheck_observation", {"key_entity_overlap_signal": "low"}, "low_count_conflicting"),
)
