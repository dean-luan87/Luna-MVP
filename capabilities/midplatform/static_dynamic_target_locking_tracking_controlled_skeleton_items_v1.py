# -*- coding: utf-8 -*-
"""Static/Dynamic target locking tracking controlled skeleton items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Trajectory-Analysis-Task-Impact-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Trajectory Analysis Task Impact Planning"

NEXT_STAGE_SPLIT_PLAN: Dict[str, Any] = {
    "recommended_next": SELECTED_NEXT_PHASE,
    "deferred": ("trajectory_trend_analysis", "task_impact_extraction", "task_simulation"),
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_tracking", "bytetrack", "yolo", "supervision", "model_download", "real_inference",
        "trajectory_prediction", "task_simulation", "world_model_fact", "runtime",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "skeleton_not_real_tracking", "track_id_hint_not_fact",
    "target_candidate_not_world_model_fact", "skeleton_not_midplatform_completed",
)


def _ent(eid: str, label: str, bbox: Dict[str, float], conf: float = 0.85, **kw: Any) -> Dict[str, Any]:
    return {
        "entity_candidate_id": eid, "label": label, "confidence": conf, "bbox": bbox,
        "pseudo_3d_position": kw.get("pseudo_3d", {"x": 100, "y": 100, "z": 3.0}),
        "field_zone": kw.get("field_zone", "working_zone"),
        **{k: v for k, v in kw.items() if k not in ("pseudo_3d", "field_zone")},
    }


DRYRUN_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "static_door_lock_same_field",
        "continuity_status": "same_field",
        "field_session_ref": "fsess_1",
        "prev_scene": {"field_scene_id": "fs_p1", "entities": [_ent("e_d1", "door", {"x1": 10, "y1": 10, "x2": 80, "y2": 200})]},
        "curr_scene": {"field_scene_id": "fs_c1", "entities": [_ent("e_d2", "door", {"x1": 12, "y1": 12, "x2": 82, "y2": 202})]},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_task_impact_hints": ("navigation_relevant",),
        "prohibited": ("inherit_from_old_session",),
    },
    {
        "case_id": "static_sign_weak_lock_low_confidence",
        "continuity_status": "same_field", "field_session_ref": "fsess_2",
        "prev_scene": {"field_scene_id": "fs_p2", "entities": [_ent("e_s1", "sign", {"x1": 50, "y1": 50, "x2": 120, "y2": 100}, 0.35)]},
        "curr_scene": {"field_scene_id": "fs_c2", "entities": [_ent("e_s2", "sign", {"x1": 52, "y1": 52, "x2": 122, "y2": 102}, 0.3)]},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_lock_status": "weak_locked", "expected_task_impact_hints": ("navigation_relevant",),
        "prohibited": ("silently_drop_low_conf",),
    },
    {
        "case_id": "static_obstacle_inner_zone_priority",
        "continuity_status": "same_field", "field_session_ref": "fsess_3",
        "prev_scene": {"field_scene_id": "fs_p3", "entities": [_ent("e_o1", "obstacle", {"x1": 200, "y1": 300, "x2": 280, "y2": 400}, field_zone="inner_zone", risk_hint="near_collision")]},
        "curr_scene": {"field_scene_id": "fs_c3", "entities": [_ent("e_o2", "obstacle", {"x1": 202, "y1": 302, "x2": 282, "y2": 402}, field_zone="inner_zone", risk_hint="near_collision")]},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_task_impact_hints": ("route_blocker_candidate",), "expected_priority": "P0",
        "prohibited": (),
    },
    {
        "case_id": "duplicate_cups_do_not_merge",
        "continuity_status": "same_field", "field_session_ref": "fsess_4",
        "prev_scene": {"field_scene_id": "fs_p4", "entities": [
            _ent("e_c1", "cup", {"x1": 10, "y1": 10, "x2": 40, "y2": 40}),
            _ent("e_c2", "cup", {"x1": 200, "y1": 200, "x2": 230, "y2": 230}),
        ]},
        "curr_scene": {"field_scene_id": "fs_c4", "entities": [
            _ent("e_c3", "cup", {"x1": 12, "y1": 12, "x2": 42, "y2": 42}),
            _ent("e_c4", "cup", {"x1": 202, "y1": 202, "x2": 232, "y2": 232}),
        ]},
        "expected_static_lock_count": 2, "expected_dynamic_track_count": 0,
        "expected_task_impact_hints": ("find_object_relevant",), "prohibited": ("merge_duplicate_labels",),
    },
    {
        "case_id": "dynamic_person_moves_between_frames",
        "continuity_status": "same_field", "field_session_ref": "fsess_5",
        "prev_scene": {"field_scene_id": "fs_p5", "entities": [_ent("e_p1", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150})]},
        "curr_scene": {"field_scene_id": "fs_c5", "entities": [_ent("e_p2", "person", {"x1": 120, "y1": 10, "x2": 170, "y2": 150})]},
        "expected_static_lock_count": 0, "expected_dynamic_track_count": 1,
        "expected_motion": "moving", "expected_task_impact_hints": ("safety_relevant",),
        "prohibited": ("infer_trajectory",),
    },
    {
        "case_id": "dynamic_vehicle_relevant_to_road_crossing",
        "continuity_status": "same_field", "field_session_ref": "fsess_6",
        "prev_scene": {"field_scene_id": "fs_p6", "entities": [_ent("e_v1", "vehicle", {"x1": 300, "y1": 100, "x2": 400, "y2": 200})]},
        "curr_scene": {"field_scene_id": "fs_c6", "entities": [_ent("e_v2", "vehicle", {"x1": 350, "y1": 100, "x2": 450, "y2": 200})]},
        "expected_static_lock_count": 0, "expected_dynamic_track_count": 1,
        "expected_motion": "likely_moving", "expected_task_impact_hints": ("road_crossing_relevant",),
        "prohibited": (),
    },
    {
        "case_id": "moving_target_without_tracker_id",
        "continuity_status": "same_field", "field_session_ref": "fsess_7",
        "prev_scene": {"field_scene_id": "fs_p7", "entities": [_ent("e_p3", "person", {"x1": 50, "y1": 50, "x2": 100, "y2": 180})]},
        "curr_scene": {"field_scene_id": "fs_c7", "entities": [_ent("e_p4", "person", {"x1": 200, "y1": 50, "x2": 250, "y2": 180})]},
        "tracker_hint_id": None,
        "expected_static_lock_count": 0, "expected_dynamic_track_count": 1,
        "expected_weak_track": True, "prohibited": ("require_tracker_id",),
    },
    {
        "case_id": "occluded_target_freeze_lock",
        "continuity_status": "field_occluded", "field_session_ref": "fsess_8",
        "prev_scene": {"field_scene_id": "fs_p8", "entities": [_ent("e_cu1", "cup", {"x1": 100, "y1": 100, "x2": 140, "y2": 140})]},
        "curr_scene": {"field_scene_id": "fs_c8", "entities": [_ent("e_cu2", "cup", {"x1": 100, "y1": 100, "x2": 140, "y2": 140})]},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_visibility": "occluded", "prohibited": ("delete_occluded", "new_motion_judgment"),
    },
    {
        "case_id": "lost_target_after_long_gap",
        "continuity_status": "field_lost", "field_session_ref": "fsess_9",
        "prev_scene": {"field_scene_id": "fs_p9", "entities": [_ent("e_ch1", "chair", {"x1": 80, "y1": 80, "x2": 160, "y2": 200})]},
        "curr_scene": {"field_scene_id": "fs_c9", "entities": []},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_lock_status": "lock_lost", "prohibited": ("maintain_high_confidence",),
    },
    {
        "case_id": "recovered_target_after_occlusion",
        "continuity_status": "field_recovering", "field_session_ref": "fsess_10",
        "prev_scene": {"field_scene_id": "fs_p10", "entities": [_ent("e_sh1", "shelf", {"x1": 20, "y1": 20, "x2": 200, "y2": 300})]},
        "curr_scene": {"field_scene_id": "fs_c10", "entities": [_ent("e_sh2", "shelf", {"x1": 22, "y1": 22, "x2": 202, "y2": 302})]},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_lock_status": "lock_recovered", "expected_task_impact_hints": ("find_object_relevant",),
        "prohibited": (),
    },
    {
        "case_id": "new_field_resets_old_targets",
        "continuity_status": "new_field_required", "field_session_ref": "fsess_11",
        "prev_scene": {"field_scene_id": "fs_p11", "entities": [_ent("e_t1", "table", {"x1": 10, "y1": 10, "x2": 200, "y2": 100})]},
        "curr_scene": {"field_scene_id": "fs_c11", "entities": [_ent("e_b1", "bed", {"x1": 10, "y1": 10, "x2": 200, "y2": 100})]},
        "expected_static_lock_count": 0, "expected_dynamic_track_count": 0,
        "prohibited": ("inherit_old_static_lock", "continue_old_track"),
    },
    {
        "case_id": "field_shift_preserves_static_anchor",
        "continuity_status": "field_shift", "field_session_ref": "fsess_12",
        "prev_scene": {"field_scene_id": "fs_p12", "entities": [_ent("e_tb1", "table", {"x1": 50, "y1": 50, "x2": 250, "y2": 150})]},
        "curr_scene": {"field_scene_id": "fs_c12", "entities": [_ent("e_tb2", "table", {"x1": 55, "y1": 55, "x2": 255, "y2": 155})]},
        "expected_static_lock_count": 1, "expected_dynamic_track_count": 0,
        "expected_low_stability": True, "prohibited": ("reset_all_locks",),
    },
)
