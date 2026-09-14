# -*- coding: utf-8 -*-
"""Field-First Core Logic Formal Implementation — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Field-Simulation-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Field Simulation Planning"

NEXT_STAGE_SPLIT_PLAN: Dict[str, Any] = {
    "recommended_next": SELECTED_NEXT_PHASE,
    "deferred": ("field_simulation", "task_reasoning", "world_model_admission"),
    "boundary_note": "core_logic_integrated_no_more_skeleton_splits",
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_camera", "yolo", "supervision", "bytetrack", "model_download", "real_inference",
        "real_video_analysis", "field_simulation", "task_execution", "navigation_action",
        "world_model_entry", "memory_candidate", "runtime", "integration_test",
        "candidate_lifecycle_manager", "module_handoff_contract",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "core_logic_not_field_simulation", "readiness_not_final_action",
    "pipeline_not_world_model_fact", "formal_implementation_not_midplatform_completed",
)


def _obs(oid: str, label: str, bbox: Dict[str, float], conf: float = 0.85, **kw: Any) -> Dict[str, Any]:
    o: Dict[str, Any] = {
        "observation_id": oid, "timestamp": "2026-06-11T00:00:00Z", "source_ref": "mock_obs",
        "label": label, "confidence": conf, "bbox": bbox,
        "static_dynamic_hint": "dynamic" if label in ("person", "vehicle", "bicycle", "scooter") else "static",
    }
    if "depth_hint" in kw:
        o["depth_hint"] = kw["depth_hint"]
        o["depth_source"] = kw.get("depth_source", "estimated")
    return o


CORE_PIPELINE_MOCK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "normal_same_field_person_moving",
        "field_session_ref": "fsess_c1",
        "previous_observations": [_obs("o_p1", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150}, depth_hint=4.0)],
        "current_observations": [_obs("o_c1", "person", {"x1": 120, "y1": 10, "x2": 170, "y2": 150}, depth_hint=3.5)],
        "continuity_evaluation_context": {
            "location_prev": "room_a", "location_curr": "room_a",
            "entity_labels_prev": ["person"], "entity_labels_curr": ["person"],
            "layout_hash_prev": "person_a", "layout_hash_curr": "person_a",
            "entity_count_prev": 1, "entity_count_curr": 1, "time_gap_s": 0.5,
            "heading_prev": 0, "heading_curr": 2,
        },
        "expected_field_status": "same_field",
        "expected_static_locks": 0, "expected_dynamic_tracks": 1,
        "expected_trajectory_candidates": 1, "expected_task_impacts_min": 1,
        "prohibited": ("final_action",),
    },
    {
        "case_id": "new_field_resets_targets",
        "field_session_ref": "fsess_c2",
        "previous_observations": [_obs("o_p2", "table", {"x1": 10, "y1": 10, "x2": 200, "y2": 100})],
        "current_observations": [_obs("o_c2", "bed", {"x1": 10, "y1": 10, "x2": 200, "y2": 100})],
        "continuity_evaluation_context": {
            "location_prev": "office", "location_curr": "bedroom",
            "entity_labels_prev": ["table"], "entity_labels_curr": ["bed"],
            "layout_hash_prev": "office", "layout_hash_curr": "bedroom",
            "entity_count_prev": 1, "entity_count_curr": 1, "time_gap_s": 5,
        },
        "expected_field_status": "new_field_required",
        "expected_static_locks": 0, "expected_dynamic_tracks": 0,
        "expected_trajectory_candidates": 0,
        "expected_missing_information": ("new_field_reset",),
        "prohibited": ("inherit_old_targets",),
    },
    {
        "case_id": "field_occluded_freezes_tracking",
        "field_session_ref": "fsess_c3",
        "previous_observations": [_obs("o_p3", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150})],
        "current_observations": [_obs("o_c3", "person", {"x1": 120, "y1": 10, "x2": 170, "y2": 150})],
        "continuity_evaluation_context": {
            "location_prev": "room_a", "location_curr": "room_a",
            "entity_labels_prev": ["person"], "entity_labels_curr": [],
            "entity_count_prev": 1, "entity_count_curr": 0,
            "sudden_dark": True, "brightness_curr": "very_low", "time_gap_s": 0.5,
        },
        "expected_field_status": "field_occluded",
        "expect_tracking_frozen": True, "expect_no_trajectory": True,
        "expected_static_locks": 0, "expected_dynamic_tracks": 0,
        "expected_trajectory_candidates": 0,
        "expected_missing_information": ("frozen_tracking",),
        "prohibited": ("new_motion_trend",),
    },
    {
        "case_id": "missing_depth_propagates",
        "field_session_ref": "fsess_c4",
        "previous_observations": [_obs("o_p4", "person", {"x1": 10, "y1": 10, "x2": 60, "y2": 150})],
        "current_observations": [_obs("o_c4", "person", {"x1": 80, "y1": 10, "x2": 130, "y2": 150})],
        "continuity_evaluation_context": {
            "location_prev": "room_a", "location_curr": "room_a",
            "entity_labels_prev": ["person"], "entity_labels_curr": ["person"],
            "layout_hash_prev": "person_a", "layout_hash_curr": "person_a",
            "entity_count_prev": 1, "entity_count_curr": 1, "time_gap_s": 0.5,
        },
        "expected_field_status": "same_field",
        "expected_dynamic_tracks": 1,
        "expected_missing_information": ("missing_depth",),
    },
    {
        "case_id": "static_obstacle_inner_zone",
        "field_session_ref": "fsess_c5",
        "previous_observations": [_obs("o_p5", "obstacle", {"x1": 200, "y1": 300, "x2": 280, "y2": 400}, depth_hint=2.0, depth_source="estimated")],
        "current_observations": [_obs("o_c5", "obstacle", {"x1": 202, "y1": 302, "x2": 282, "y2": 402}, depth_hint=2.0, depth_source="estimated")],
        "continuity_evaluation_context": {
            "location_prev": "room_a", "location_curr": "room_a",
            "entity_labels_prev": ["obstacle"], "entity_labels_curr": ["obstacle"],
            "layout_hash_prev": "obstacle", "layout_hash_curr": "obstacle",
            "entity_count_prev": 1, "entity_count_curr": 1, "time_gap_s": 0.5,
        },
        "expected_field_status": "same_field",
        "expected_static_locks": 1, "expected_dynamic_tracks": 0,
        "expected_trajectory_candidates": 0, "expected_task_impacts_min": 1,
        "expected_task_impact_types": ("route_blocker",),
    },
    {
        "case_id": "low_confidence_object_retained",
        "field_session_ref": "fsess_c6",
        "previous_observations": [_obs("o_p6", "sign", {"x1": 50, "y1": 50, "x2": 120, "y2": 100}, conf=0.32)],
        "current_observations": [_obs("o_c6", "sign", {"x1": 52, "y1": 52, "x2": 122, "y2": 102}, conf=0.28)],
        "continuity_evaluation_context": {
            "location_prev": "room_a", "location_curr": "room_a",
            "entity_labels_prev": ["sign"], "entity_labels_curr": ["sign"],
            "layout_hash_prev": "sign", "layout_hash_curr": "sign",
            "entity_count_prev": 1, "entity_count_curr": 1, "time_gap_s": 0.5,
        },
        "expected_field_status": "same_field",
        "expect_low_confidence_retained": True,
        "expected_static_locks": 1,
    },
    {
        "case_id": "duplicate_targets_not_merged",
        "field_session_ref": "fsess_c7",
        "previous_observations": [
            _obs("o_p7a", "cup", {"x1": 10, "y1": 10, "x2": 40, "y2": 40}),
            _obs("o_p7b", "cup", {"x1": 200, "y1": 200, "x2": 230, "y2": 230}),
        ],
        "current_observations": [
            _obs("o_c7a", "cup", {"x1": 12, "y1": 12, "x2": 42, "y2": 42}),
            _obs("o_c7b", "cup", {"x1": 202, "y1": 202, "x2": 232, "y2": 232}),
        ],
        "continuity_evaluation_context": {
            "location_prev": "room_a", "location_curr": "room_a",
            "entity_labels_prev": ["cup", "cup"], "entity_labels_curr": ["cup", "cup"],
            "layout_hash_prev": "cup_cup", "layout_hash_curr": "cup_cup",
            "entity_count_prev": 2, "entity_count_curr": 2, "time_gap_s": 0.5,
        },
        "expected_field_status": "same_field",
        "expect_duplicate_count": {"label": "cup", "min": 2},
        "expected_static_locks": 2,
        "prohibited": ("merge_duplicate_labels",),
    },
    {
        "case_id": "traffic_light_static_task_relevant",
        "field_session_ref": "fsess_c8",
        "previous_observations": [_obs("o_p8", "traffic_light", {"x1": 300, "y1": 50, "x2": 340, "y2": 120})],
        "current_observations": [_obs("o_c8", "traffic_light", {"x1": 302, "y1": 52, "x2": 342, "y2": 122})],
        "continuity_evaluation_context": {
            "location_prev": "road_a", "location_curr": "road_a",
            "entity_labels_prev": ["traffic_light"], "entity_labels_curr": ["traffic_light"],
            "layout_hash_prev": "traffic_light", "layout_hash_curr": "traffic_light",
            "entity_count_prev": 1, "entity_count_curr": 1, "time_gap_s": 0.5,
        },
        "expected_field_status": "same_field",
        "expected_static_locks": 1, "expected_dynamic_tracks": 0,
        "expected_trajectory_candidates": 0, "expected_task_impacts_min": 1,
        "expected_task_impact_types": ("traffic_light_relevant",),
        "prohibited": ("navigation_action",),
    },
)

INPUT_OUTPUT_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_first_core_input_package_contract_v1",
    "input_type": "FieldFirstCoreInputPackage",
    "output_type": "FieldFirstCoreLogicResultCandidate",
    "pipeline_stages": (
        "step_1_build_small_range_field_scene",
        "step_2_detect_field_continuity",
        "step_3_build_static_dynamic_target_tracking",
        "step_4_build_trajectory_analysis_task_impact",
        "step_5_assemble_core_logic_result",
    ),
    "candidate_only": True,
}

PIPELINE_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_first_core_pipeline_registry_v1",
    "pipeline_id": "FieldFirstCorePipeline",
    "stages": INPUT_OUTPUT_CONTRACT["pipeline_stages"],
}
