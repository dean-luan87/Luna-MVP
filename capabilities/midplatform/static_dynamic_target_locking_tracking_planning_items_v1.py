# -*- coding: utf-8 -*-
"""Static/Dynamic Target Locking & Tracking Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SCOPE_DEFINITION: Dict[str, Any] = {
    "scope_id": "target_locking_tracking_scope_v1",
    "goal": "plan_static_and_dynamic_target_locking_tracking_within_field_session",
    "planning_only": True,
    "core_question": "What to lock, what to track, why, when not to track, how to serve tasks",
    "continuity_prerequisite": True,
    "not_in_scope": (
        "real_tracking", "bytetrack", "yolo", "trajectory_prediction", "task_simulation",
        "semantic_attachment", "world_model_fact", "persistent_memory", "runtime",
    ),
}

STATIC_TARGET_LABELS: Tuple[str, ...] = (
    "door", "elevator", "traffic_light", "sign", "text_region", "table", "chair", "cup",
    "obstacle", "stairs", "crossing", "counter", "shelf",
)

DYNAMIC_TARGET_LABELS: Tuple[str, ...] = (
    "person", "vehicle", "bicycle", "scooter", "pet", "cart",
    "elevator_door", "automatic_door", "escalator_state", "moving_obstacle",
)

TARGET_VISIBILITY_STATUSES: Tuple[str, ...] = (
    "visible", "partially_visible", "occluded", "lost", "recovered", "unknown",
)

TARGET_MOTION_STATUSES: Tuple[str, ...] = (
    "static", "likely_static", "moving", "likely_moving", "state_changing",
    "uncertain_motion", "unknown",
)

TARGET_LOCK_STATUSES: Tuple[str, ...] = (
    "locked", "weak_locked", "candidate_lock", "lock_lost", "lock_recovered", "new_target_candidate",
)

TARGET_TASK_IMPACT_HINTS: Tuple[str, ...] = (
    "safety_relevant", "navigation_relevant", "reading_relevant", "find_object_relevant",
    "road_crossing_relevant", "elevator_relevant", "route_blocker_candidate", "background_only", "unknown",
)

TARGET_PRIORITY_LEVELS: Tuple[str, ...] = ("P0", "P1", "P2", "P3")

CONTINUITY_ALLOWED_FOR_TRACKING: Tuple[str, ...] = (
    "same_field", "field_shift", "field_recovering",
)

CONTINUITY_FREEZE_TRACKING: Tuple[str, ...] = ("field_occluded", "field_lost")

CONTINUITY_RESET_TRACKING: Tuple[str, ...] = ("new_field_required",)

STATIC_TARGET_LOCK_MODEL: Dict[str, Any] = {
    "model_id": "static_target_lock_model_v1",
    "output_type": "StaticTargetLockCandidate",
    "candidate_only": True,
    "fields": (
        "lock_candidate_id", "field_session_ref", "field_scene_ref", "entity_candidate_ref",
        "label", "bbox", "pseudo_3d_position", "field_zone", "confidence", "lock_status",
        "visibility_status", "stability_score", "anchor_candidate", "task_impact_hint",
        "source_refs", "evidence_refs", "reason_codes", "candidate_only",
    ),
    "rules": (
        "same_session_label_position_overlap_lock",
        "task_relevant_static_priority",
        "low_confidence_weak_locked_not_dropped",
        "occlusion_mark_not_delete",
        "long_invisible_lock_lost",
        "new_field_no_inherit_static_lock",
    ),
}

DYNAMIC_TARGET_TRACK_MODEL: Dict[str, Any] = {
    "model_id": "dynamic_target_track_model_v1",
    "output_type": "DynamicTargetTrackCandidate",
    "candidate_only": True,
    "tracker_id_is_hint_not_fact": True,
    "fields": (
        "track_candidate_id", "field_session_ref", "previous_entity_candidate_ref",
        "current_entity_candidate_ref", "label", "previous_bbox", "current_bbox",
        "previous_pseudo_3d_position", "current_pseudo_3d_position", "visibility_status",
        "motion_status", "lock_status", "tracker_hint_id", "continuity_confidence",
        "task_impact_hint", "source_refs", "evidence_refs", "reason_codes", "candidate_only",
    ),
    "rules": (
        "continuity_allowed_required_for_track",
        "tracker_hint_id_auxiliary_only",
        "bbox_position_change_marks_moving",
        "brief_occlusion_not_immediate_lost",
        "recovery_label_layout_position_match",
        "new_field_no_track_continuation",
        "field_lost_uncertain_no_position_inference",
    ),
}

TASK_IMPACT_HINT_POLICY: Dict[str, Any] = {
    "policy_id": "target_task_impact_hint_policy_v1",
    "tracking_depends_on_continuity": True,
    "new_field_resets_tracking": True,
    "field_occluded_freezes_tracking": True,
    "tracker_id_is_hint_not_fact": True,
    "priorities": {
        "P0": ("vehicle", "person", "bicycle", "scooter", "obstacle", "stairs"),
        "P1": ("door", "elevator", "traffic_light", "sign", "text_region", "cup"),
        "P2": ("table", "shelf", "counter", "chair"),
        "P3": ("background_only",),
    },
    "label_to_hint": {
        "vehicle": "safety_relevant",
        "person": "safety_relevant",
        "obstacle": "route_blocker_candidate",
        "door": "navigation_relevant",
        "elevator": "elevator_relevant",
        "traffic_light": "road_crossing_relevant",
        "sign": "navigation_relevant",
        "text_region": "reading_relevant",
        "cup": "find_object_relevant",
    },
}

ABNORMAL_CASE_POLICY: Dict[str, Any] = {
    "policy_id": "target_abnormal_case_policy_v1",
    "cases": (
        {"id": "low_confidence_target", "handling": "candidate_lock_not_dropped"},
        {"id": "duplicate_same_label_targets", "handling": "no_merge_unless_spatial_overlap"},
        {"id": "occluded_target", "handling": "keep_candidate_lower_confidence"},
        {"id": "lost_target", "handling": "lock_lost_after_ttl"},
        {"id": "recovered_target", "handling": "label_layout_position_match"},
        {"id": "new_field_resets_tracking", "handling": "no_inherit_old_targets"},
        {"id": "field_shift_preserves_static_locks", "handling": "reduce_confidence"},
        {"id": "field_occluded_freezes_tracking", "handling": "no_new_motion_judgment"},
        {"id": "unknown_depth_target", "handling": "lock_allowed_zone_unknown"},
        {"id": "moving_target_without_tracker_id", "handling": "bbox_diff_weak_dynamic"},
    ),
}

INPUT_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "target_input_output_contract_v1",
    "inputs": (
        "FieldSceneCandidate(t-1)", "FieldSceneCandidate(t)", "FieldContinuityDecisionCandidate",
        "FieldEntityCandidate", "FieldSessionState",
    ),
    "outputs": (
        "StaticTargetLockCandidate", "DynamicTargetTrackCandidate", "TargetTrackingPlanCandidate",
        "TargetImpactCandidate",
    ),
    "candidate_only": True,
}

NEXT_IMPLEMENTATION_PLAN: Dict[str, Any] = {
    "plan_id": "target_next_implementation_plan_v1",
    "recommended_next": "Phase-Midplatform-Static-Dynamic-Target-Locking-Tracking-Controlled-Skeleton-Implementation-v1-001",
    "deferred_to_skeleton": (
        "static_lock_builder", "dynamic_track_builder", "task_impact_scorer", "mock_dryrun_runner",
    ),
    "deferred_after_tracking": ("trajectory_analysis", "task_simulation", "world_model"),
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_tracking", "bytetrack", "yolo", "supervision", "model_download", "real_inference",
        "real_video_analysis", "trajectory_prediction", "task_simulation", "world_model_fact",
        "persistent_memory", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_tracking_implementation",
    "track_id_hint_not_entity_fact",
    "target_candidate_not_world_model_fact",
    "planning_not_midplatform_completed",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Static-Dynamic-Target-Locking-Tracking-Controlled-Skeleton-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Static Dynamic Target Locking Tracking Controlled Skeleton Implementation"


def _case(
    case_id: str, continuity: str,
    static_locks: Tuple[str, ...], dynamic_tracks: Tuple[str, ...],
    hints: Tuple[str, ...], prohibited: Tuple[str, ...], pass_cond: str,
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "previous_field_scene_summary": {"mock": True},
        "current_field_scene_summary": {"mock": True},
        "continuity_status": continuity,
        "expected_static_locks": list(static_locks),
        "expected_dynamic_tracks": list(dynamic_tracks),
        "expected_task_impact_hints": list(hints),
        "expected_prohibited_behavior": list(prohibited),
        "pass_condition": pass_cond,
    }


MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    _case("static_door_lock_same_field", "same_field", ("door:locked",), (), ("navigation_relevant",), ("inherit_from_old_session",), "door_locked_same_field"),
    _case("static_sign_weak_lock_low_confidence", "same_field", ("sign:weak_locked",), (), ("navigation_relevant",), ("silently_drop_low_conf",), "weak_lock_retained"),
    _case("static_obstacle_inner_zone_priority", "same_field", ("obstacle:locked",), (), ("safety_relevant", "route_blocker_candidate"), (), "inner_zone_p0_priority"),
    _case("duplicate_cups_do_not_merge", "same_field", ("cup:locked", "cup:locked"), (), ("find_object_relevant",), ("merge_duplicate_labels",), "two_cups_separate_locks"),
    _case("dynamic_person_moves_between_frames", "same_field", (), ("person:likely_moving",), ("safety_relevant",), ("infer_trajectory",), "dynamic_track_no_trajectory"),
    _case("dynamic_vehicle_relevant_to_road_crossing", "same_field", (), ("vehicle:moving",), ("safety_relevant", "road_crossing_relevant"), (), "vehicle_p0_road_crossing"),
    _case("moving_target_without_tracker_id", "same_field", (), ("person:weak_dynamic",), ("safety_relevant",), ("require_tracker_id",), "bbox_diff_weak_track"),
    _case("occluded_target_freeze_lock", "field_occluded", ("cup:occluded",), (), (), ("new_motion_judgment", "delete_occluded"), "freeze_not_delete"),
    _case("lost_target_after_long_gap", "field_lost", ("chair:lock_lost",), (), (), ("maintain_high_confidence",), "lock_lost_not_hidden"),
    _case("recovered_target_after_occlusion", "field_recovering", ("shelf:lock_recovered",), (), ("find_object_relevant",), (), "recovery_match"),
    _case("new_field_resets_old_targets", "new_field_required", (), (), (), ("inherit_old_static_lock", "continue_old_track"), "no_inherit_new_field"),
    _case("field_shift_preserves_static_anchor", "field_shift", ("table:locked",), (), ("background_only",), ("reset_all_locks",), "static_anchor_reduced_conf"),
)
