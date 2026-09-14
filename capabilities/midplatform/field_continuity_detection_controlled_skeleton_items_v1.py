# -*- coding: utf-8 -*-
"""Field Continuity Detection Controlled Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

from capabilities.midplatform.field_continuity_detection_decision_builder_v1 import DECISION_RULES
from capabilities.midplatform.field_continuity_detection_signal_scoring_v1 import SIGNAL_SCORERS
from capabilities.midplatform.field_continuity_detection_state_machine_v1 import ALLOWED_TRANSITIONS
from capabilities.midplatform.field_continuity_detection_types_v1 import STATUS_TO_SESSION_STATE

SELECTED_NEXT_PHASE = "Phase-Midplatform-Static-Dynamic-Target-Locking-Tracking-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Static and Dynamic Target Locking Tracking Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_tracking", "bytetrack", "yolo", "supervision", "model_download", "real_inference",
        "real_video_analysis", "trajectory_analysis", "task_simulation", "world_model_fact",
        "persistent_memory", "runtime", "integration_test",
    ),
}

NEXT_STAGE_SPLIT_PLAN: Dict[str, Any] = {
    "current_stage": "Phase-Midplatform-Field-Continuity-Detection-Controlled-Skeleton-Implementation-v1-001",
    "recommended_next": SELECTED_NEXT_PHASE,
    "deferred": ("static_target_locking", "dynamic_target_tracking", "trajectory_analysis"),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "skeleton_not_tracking_implementation",
    "dryrun_not_video_inference",
    "continuity_decision_not_world_model_fact",
    "skeleton_not_midplatform_completed",
)


def _case(
    case_id: str, expected_status: str, expected_action: str,
    ctx: Dict[str, Any], prev_state: str = "active",
) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "expected_status": expected_status,
        "expected_action": expected_action,
        "evaluation_context": ctx,
        "previous_field_scene_summary": {"field_scene_id": f"fs_prev_{case_id}"},
        "current_field_scene_summary": {"field_scene_id": f"fs_curr_{case_id}"},
        "previous_field_session_state": prev_state,
        "previous_field_session_ref": f"fsess_{case_id}",
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    _case("same_field_small_camera_jitter", "same_field", "keep_session", {
        "location_prev": "room_a", "location_curr": "room_a",
        "heading_prev": 0, "heading_curr": 2,
        "entity_labels_prev": ["chair", "table"], "entity_labels_curr": ["chair", "table"],
        "layout_hash_prev": "indoor_a", "layout_hash_curr": "indoor_a",
        "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 0.5,
    }),
    _case("field_shift_user_turns_slightly", "field_shift", "keep_session_with_shift", {
        "location_prev": "room_a", "location_curr": "room_a",
        "heading_prev": 10, "heading_curr": 35,
        "entity_labels_prev": ["door", "sign"], "entity_labels_curr": ["door", "sign"],
        "layout_hash_prev": "hall_a", "layout_hash_curr": "hall_a",
        "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 1,
    }),
    _case("sudden_dark_occlusion", "field_occluded", "mark_occluded", {
        "location_prev": "room_a", "location_curr": "room_a",
        "entity_labels_prev": ["lamp", "desk"], "entity_labels_curr": [],
        "entity_count_prev": 2, "entity_count_curr": 0,
        "sudden_dark": True, "brightness_curr": "very_low", "time_gap_s": 0.5,
    }),
    _case("temporary_occlusion_then_recover", "field_recovering", "attempt_recovery", {
        "location_prev": "room_a", "location_curr": "room_a",
        "entity_labels_prev": ["shelf", "box"], "entity_labels_curr": ["shelf", "box"],
        "layout_hash_prev": "shelf_a", "layout_hash_curr": "shelf_a",
        "recovery_overlap": "high", "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 2,
    }, prev_state="occluded"),
    _case("large_heading_change_same_location", "field_shift", "keep_session_with_shift", {
        "location_prev": "room_b", "location_curr": "room_b",
        "heading_prev": 0, "heading_curr": 120,
        "entity_labels_prev": ["window", "curtain"], "entity_labels_curr": ["window", "curtain"],
        "layout_hash_prev": "room_b", "layout_hash_curr": "room_b",
        "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 1,
    }),
    _case("location_jump_new_field", "new_field_required", "create_new_session_candidate", {
        "location_prev": "office_1", "location_curr": "bedroom_2",
        "entity_labels_prev": ["desk", "monitor"], "entity_labels_curr": ["bed", "wardrobe"],
        "layout_hash_prev": "office", "layout_hash_curr": "bedroom",
        "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 5,
    }),
    _case("key_entities_overlap_same_field", "same_field", "keep_session", {
        "location_prev": "room_c", "location_curr": "room_c",
        "entity_labels_prev": ["chair", "table", "cup"], "entity_labels_curr": ["chair", "table", "cup"],
        "layout_hash_prev": "abc", "layout_hash_curr": "abc",
        "entity_count_prev": 3, "entity_count_curr": 3, "time_gap_s": 1,
    }),
    _case("key_entities_all_changed_new_field", "new_field_required", "create_new_session_candidate", {
        "location_prev": "park", "location_curr": "kitchen",
        "entity_labels_prev": ["tree", "bench"], "entity_labels_curr": ["stove", "sink"],
        "layout_hash_prev": "park", "layout_hash_curr": "kitchen",
        "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 10,
    }),
    _case("pause_resume_short_gap_recovering", "field_recovering", "attempt_recovery", {
        "location_prev": "hall", "location_curr": "hall",
        "entity_labels_prev": ["door"], "entity_labels_curr": ["door"],
        "recovery_overlap": "high", "time_gap_s": 30, "entity_count_prev": 1, "entity_count_curr": 1,
    }, prev_state="lost"),
    _case("power_cycle_long_gap_uncertain_or_new_field", "uncertain_need_recheck", "request_recheck_observation", {
        "location_prev": None, "location_curr": None,
        "entity_labels_prev": ["cabinet"], "entity_labels_curr": ["cabinet"],
        "time_gap_s": 3600, "entity_count_prev": 1, "entity_count_curr": 1,
    }, prev_state="lost"),
    _case("missing_location_use_visual_layout", "same_field", "keep_session", {
        "location_prev": None, "location_curr": None,
        "entity_labels_prev": ["pole", "sign"], "entity_labels_curr": ["pole", "sign"],
        "layout_hash_prev": "street", "layout_hash_curr": "street",
        "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 2,
    }),
    _case("low_entity_count_uncertain_need_recheck", "uncertain_need_recheck", "request_recheck_observation", {
        "location_prev": "room_d", "location_curr": "room_d",
        "entity_labels_prev": ["chair", "table", "lamp"], "entity_labels_curr": ["blob"],
        "entity_count_prev": 3, "entity_count_curr": 1, "time_gap_s": 1,
    }),
)

INVALID_TRANSITION_TEST: Dict[str, str] = {"from_state": "closed", "to_state": "active"}

SIGNAL_SCORING_REGISTRY: Dict[str, Any] = {
    "registry_id": "continuity_signal_scoring_registry_v1",
    "scorers": list(SIGNAL_SCORERS),
    "count": len(SIGNAL_SCORERS),
}

DECISION_RULE_REGISTRY: Dict[str, Any] = {
    "registry_id": "continuity_decision_rule_registry_v1",
    "rules": list(DECISION_RULES),
}

STATE_TRANSITION_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_session_state_transition_registry_v1",
    "allowed": [{"from": a, "to": b} for a, b in sorted(ALLOWED_TRANSITIONS)],
    "status_to_session_state": dict(STATUS_TO_SESSION_STATE),
}
