# -*- coding: utf-8 -*-
"""Trajectory Analysis Task Impact Controlled Skeleton items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-First-Core-Logic-Formal-Implementation-v1-001"
SELECTED_NEXT_ROUTE = "Field-First Core Logic Formal Implementation"

NEXT_STAGE_SPLIT_PLAN: Dict[str, Any] = {
    "recommended_next": SELECTED_NEXT_PHASE,
    "deferred": ("field_core_pipeline", "core_orchestration", "field_simulation"),
    "boundary_note": "no_more_horizontal_planning_after_skeleton_go",
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_trajectory_prediction", "real_tracking", "bytetrack", "yolo", "supervision",
        "model_download", "real_inference", "field_simulation", "task_execution",
        "navigation_instruction_output", "world_model_fact", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "skeleton_not_trajectory_prediction", "task_impact_not_final_action",
    "risk_projection_not_world_model_fact", "skeleton_not_midplatform_completed",
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
        "case_id": "person_approaching_user",
        "continuity_status": "same_field", "field_session_ref": "fsess_t1",
        "prev_scene": {"field_scene_id": "fs_p1", "entities": [_ent("e_p1", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150}, pseudo_3d={"x": 50, "y": 80, "z": 5.0})]},
        "curr_scene": {"field_scene_id": "fs_c1", "entities": [_ent("e_p2", "person", {"x1": 30, "y1": 30, "x2": 80, "y2": 170}, pseudo_3d={"x": 55, "y": 100, "z": 2.0})]},
        "expected_trajectory_count": 1, "expected_task_impact_min": 1,
        "expected_motion_patterns": ("approaching_user",), "expected_task_impact_types": ("safety_risk",),
        "expected_risk_count": 1, "prohibited": ("final_action",),
    },
    {
        "case_id": "vehicle_crossing_user_path_candidate",
        "continuity_status": "same_field", "field_session_ref": "fsess_t2",
        "prev_scene": {"field_scene_id": "fs_p2", "entities": [_ent("e_v1", "vehicle", {"x1": 10, "y1": 100, "x2": 110, "y2": 200}, pseudo_3d={"x": 60, "y": 150, "z": 4.0})]},
        "curr_scene": {"field_scene_id": "fs_c2", "entities": [_ent("e_v2", "vehicle", {"x1": 200, "y1": 100, "x2": 300, "y2": 200}, pseudo_3d={"x": 250, "y": 150, "z": 4.0})]},
        "expected_trajectory_count": 1, "expected_task_impact_min": 1,
        "expected_motion_patterns": ("crossing_user_path_candidate",), "expected_task_impact_types": ("crossing_risk",),
        "prohibited": ("navigation_instruction",),
    },
    {
        "case_id": "obstacle_static_inner_zone_route_blocker",
        "continuity_status": "same_field", "field_session_ref": "fsess_t3",
        "prev_scene": {"field_scene_id": "fs_p3", "entities": [_ent("e_o1", "obstacle", {"x1": 200, "y1": 300, "x2": 280, "y2": 400}, field_zone="inner_zone")]},
        "curr_scene": {"field_scene_id": "fs_c3", "entities": [_ent("e_o2", "obstacle", {"x1": 202, "y1": 302, "x2": 282, "y2": 402}, field_zone="inner_zone")]},
        "expected_trajectory_count": 0, "expected_task_impact_min": 1,
        "expected_task_impact_types": ("route_blocker",),
    },
    {
        "case_id": "traffic_light_static_task_relevant",
        "continuity_status": "same_field", "field_session_ref": "fsess_t4",
        "prev_scene": {"field_scene_id": "fs_p4", "entities": [_ent("e_tl1", "traffic_light", {"x1": 300, "y1": 50, "x2": 340, "y2": 120})]},
        "curr_scene": {"field_scene_id": "fs_c4", "entities": [_ent("e_tl2", "traffic_light", {"x1": 302, "y1": 52, "x2": 342, "y2": 122})]},
        "expected_trajectory_count": 0, "expected_task_impact_min": 1,
        "expected_task_impact_types": ("traffic_light_relevant",),
    },
    {
        "case_id": "elevator_door_state_relevant_static",
        "continuity_status": "same_field", "field_session_ref": "fsess_t5",
        "prev_scene": {"field_scene_id": "fs_p5", "entities": [_ent("e_el1", "elevator", {"x1": 50, "y1": 50, "x2": 150, "y2": 250})]},
        "curr_scene": {"field_scene_id": "fs_c5", "entities": [_ent("e_el2", "elevator", {"x1": 52, "y1": 52, "x2": 152, "y2": 252})]},
        "expected_trajectory_count": 0, "expected_task_impact_min": 1,
        "expected_task_impact_types": ("elevator_state_relevant",),
    },
    {
        "case_id": "moving_target_missing_depth_low_confidence",
        "continuity_status": "same_field", "field_session_ref": "fsess_t6", "depth_source": "unknown",
        "prev_scene": {"field_scene_id": "fs_p6", "entities": [_ent("e_p3", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150}, pseudo_3d={"x": 35, "y": 80, "z": 4.0})]},
        "curr_scene": {"field_scene_id": "fs_c6", "entities": [_ent("e_p4", "person", {"x1": 80, "y1": 10, "x2": 130, "y2": 150}, pseudo_3d={"x": 105, "y": 80, "z": 3.5})]},
        "expected_trajectory_count": 1, "max_trajectory_confidence": "medium",
        "expected_missing_types": ("missing_depth",), "prohibited": ("high_confidence_despite_unknown_depth",),
    },
    {
        "case_id": "moving_target_without_previous_position_missing_info",
        "continuity_status": "same_field", "field_session_ref": "fsess_t7", "inject_track_without_prev": True,
        "prev_scene": {"field_scene_id": "fs_p7", "entities": [_ent("e_p5", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150})]},
        "curr_scene": {"field_scene_id": "fs_c7", "entities": [_ent("e_p6", "person", {"x1": 120, "y1": 10, "x2": 170, "y2": 150})]},
        "expected_trajectory_count": 0,
        "expected_missing_types": ("missing_previous_position",),
        "prohibited": ("infer_trajectory_without_position",),
    },
    {
        "case_id": "field_occluded_freezes_trajectory",
        "continuity_status": "field_occluded", "field_session_ref": "fsess_t8",
        "prev_scene": {"field_scene_id": "fs_p8", "entities": [_ent("e_p7", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150})]},
        "curr_scene": {"field_scene_id": "fs_c8", "entities": [_ent("e_p8", "person", {"x1": 120, "y1": 10, "x2": 170, "y2": 150})]},
        "expect_no_trajectory": True, "expected_trajectory_count": 0,
        "expected_missing_types": ("frozen_tracking",), "prohibited": ("new_motion_trend",),
    },
    {
        "case_id": "new_field_resets_trajectory",
        "continuity_status": "new_field_required", "field_session_ref": "fsess_t9",
        "prev_scene": {"field_scene_id": "fs_p9", "entities": [_ent("e_p9", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150})]},
        "curr_scene": {"field_scene_id": "fs_c9", "entities": [_ent("e_p10", "person", {"x1": 120, "y1": 10, "x2": 170, "y2": 150})]},
        "expect_no_trajectory": True, "expected_trajectory_count": 0,
        "expected_missing_types": ("new_field_reset",), "prohibited": ("inherit_old_trajectory",),
    },
    {
        "case_id": "person_moving_away_lower_risk",
        "continuity_status": "same_field", "field_session_ref": "fsess_t10",
        "prev_scene": {"field_scene_id": "fs_p10", "entities": [_ent("e_p11", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150}, pseudo_3d={"x": 35, "y": 80, "z": 2.0})]},
        "curr_scene": {"field_scene_id": "fs_c10", "entities": [_ent("e_p12", "person", {"x1": 15, "y1": 15, "x2": 65, "y2": 155}, pseudo_3d={"x": 40, "y": 85, "z": 6.0})]},
        "expected_trajectory_count": 1,
        "expected_motion_patterns": ("moving_away",), "expected_task_impact_types": ("background_only",),
    },
    {
        "case_id": "text_region_reading_blocked_by_person",
        "continuity_status": "same_field", "field_session_ref": "fsess_t11",
        "prev_scene": {"field_scene_id": "fs_p11", "entities": [
            _ent("e_tr1", "text_region", {"x1": 100, "y1": 100, "x2": 200, "y2": 150}),
            _ent("e_p13", "person", {"x1": 50, "y1": 50, "x2": 90, "y2": 140}, pseudo_3d={"x": 70, "y": 95, "z": 3.0}),
        ]},
        "curr_scene": {"field_scene_id": "fs_c11", "entities": [
            _ent("e_tr2", "text_region", {"x1": 100, "y1": 100, "x2": 200, "y2": 150}),
            _ent("e_p14", "person", {"x1": 110, "y1": 90, "x2": 150, "y2": 180}, pseudo_3d={"x": 130, "y": 135, "z": 3.0}),
        ]},
        "expected_trajectory_count": 1, "expected_task_impact_min": 2,
        "expected_task_impact_types": ("reading_blocker",),
    },
    {
        "case_id": "duplicate_dynamic_targets_separate_trajectories",
        "continuity_status": "same_field", "field_session_ref": "fsess_t12",
        "prev_scene": {"field_scene_id": "fs_p12", "entities": [
            _ent("e_pa1", "person", {"x1": 10, "y1": 10, "x2": 50, "y2": 120}, pseudo_3d={"x": 30, "y": 65, "z": 5.0}),
            _ent("e_pb1", "person", {"x1": 200, "y1": 200, "x2": 240, "y2": 310}, pseudo_3d={"x": 220, "y": 255, "z": 4.0}),
        ]},
        "curr_scene": {"field_scene_id": "fs_c12", "entities": [
            _ent("e_pa2", "person", {"x1": 30, "y1": 30, "x2": 70, "y2": 140}, pseudo_3d={"x": 50, "y": 85, "z": 2.0}),
            _ent("e_pb2", "person", {"x1": 280, "y1": 200, "x2": 320, "y2": 310}, pseudo_3d={"x": 300, "y": 255, "z": 4.0}),
        ]},
        "expected_trajectory_count": 2, "expected_task_impact_min": 2,
        "expected_risk_count": 1, "prohibited": ("merge_duplicate_tracks",),
    },
)
