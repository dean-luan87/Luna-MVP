# -*- coding: utf-8 -*-
"""Field Simulation Skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Task-Reasoning-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Task Reasoning Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "task_reasoning", "navigation_action", "action_recommendation",
        "world_model_entry", "memory_candidate", "fact_admission",
        "scene_graph", "slam", "production_runtime", "real_yolo_rerun",
        "real_depth_rerun", "model_download", "weight_download",
        "real_camera_read", "real_video_stream",
        "candidate_lifecycle_manager", "module_handoff_contract",
        "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "skeleton_not_task_reasoning",
    "simulation_candidate_not_world_model_fact",
    "safety_risk_not_navigation_instruction",
    "task_relevance_not_action_output",
)

SKELETON_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "current_state_from_real_yolo_real_depth_success",
        "source_case_id": "real_image_yolo_with_depth_available",
        "expect_mode": "current_state_simulation",
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "current_state_from_mock_depth_degraded",
        "source_case_id": "real_image_yolo_depth_mock_alignment",
        "expect_mode": "current_state_simulation",
        "expect_status": ("generated", "generated_degraded"),
        "expect_degraded": True,
    },
    {
        "case_id": "missing_depth_occlusion_simulation",
        "source_case_id": "real_image_yolo_no_depth_fallback",
        "expect_mode": "occlusion_and_missing_info_simulation",
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "multiple_objects_safety_risk_projection",
        "source_case_id": "real_image_multiple_objects_field_assembly",
        "expect_mode": "safety_risk_projection",
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "multiple_objects_task_relevance_projection",
        "source_case_id": "real_image_multiple_objects_field_assembly",
        "expect_mode": "task_relevance_field_projection",
        "expect_no_action": True,
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "invalid_bbox_failure_simulation_blocked",
        "source_case_id": "real_image_invalid_bbox_handling",
        "expect_all_blocked": True,
        "expect_status": ("blocked_quality_insufficient",),
    },
    {
        "case_id": "no_detection_blocked_no_entity",
        "source_case_id": "real_image_no_detection_graceful_fail",
        "expect_all_blocked": True,
        "expect_status": ("blocked_no_scene", "blocked_no_entity"),
    },
    {
        "case_id": "timestamp_mismatch_short_horizon_blocked",
        "source_case_id": "timestamp_mismatch_degraded",
        "expect_mode": "current_state_simulation",
        "expect_short_horizon_blocked": True,
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "unknown_geometry_field_quality_projection",
        "source_case_id": "real_image_yolo_no_depth_fallback",
        "expect_mode": "field_quality_projection",
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "inner_zone_entity_safety_risk_projection",
        "source_case_id": "real_image_yolo_with_depth_available",
        "expect_mode": "safety_risk_projection",
        "expect_status": ("generated", "generated_degraded"),
        "optional_meta": True,
    },
    {
        "case_id": "traceability_preserved_in_simulation",
        "source_case_id": "traceability_preserved_full_chain",
        "expect_traceability_min": 4,
        "expect_status": ("generated", "generated_degraded"),
    },
    {
        "case_id": "no_action_no_fact_boundary",
        "source_case_id": "real_image_yolo_with_depth_available",
        "expect_no_action_no_fact": True,
        "optional_meta": True,
    },
)
