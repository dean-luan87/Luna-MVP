# -*- coding: utf-8 -*-
"""Real Model Field Construction Execution Path Hardening — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Real-Field-Construction-Quality-Evaluation-v1-001"
SELECTED_NEXT_ROUTE = "Real Field Construction Quality Evaluation"
DEFERRED_PHASES = (
    "Phase-Midplatform-Field-Simulation-Skeleton-v1-001",
    "Phase-Midplatform-Task-Reasoning-Planning-v1-001",
)

ROUTE_CORRECTION: Dict[str, Any] = {
    "correction_id": "route_correction_defer_field_simulation_v1",
    "deferred_phases": DEFERRED_PHASES,
    "reason": "real_field_construction_quality_before_simulation",
    "route_switched_from_simulation_to_real_content": True,
    "resume_after": (
        "real_field_construction_quality_evaluation",
        "multi_frame_real_field_construction_dryrun",
        "real_depth_model_adapter_controlled_execution",
    ),
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_simulation", "field_simulation_execution", "task_reasoning",
        "navigation_action", "world_model_entry", "memory_candidate",
        "fact_admission", "unauthorized_model_download", "unauthorized_weight_download",
        "real_camera_read", "real_video_stream", "production_runtime",
        "integration_test", "candidate_lifecycle_manager", "module_handoff_contract",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "execution_path_hardening_not_field_simulation",
    "quality_report_not_world_model_fact",
    "mock_depth_must_remain_labeled_not_real",
    "stub_depth_must_remain_labeled_not_full_real_model",
    "cached_yolo_is_real_integrated_output_not_mock_detection",
    "cached_yolo_not_real_runner",
)

DEFAULT_EXECUTION_AUTHORIZATION: Dict[str, Any] = {
    "matrix_id": "real_model_execution_authorization_matrix_v2",
    "yolo_path": "cached_output",
    "yolo_local_runner_available": False,
    "yolo_model_ref": "yolo_integrated_cached",
    "depth_path": "mock_adapter_with_real_frame_alignment",
    "local_depth_adapter_available": False,
    "depth_model_download_authorized": False,
    "depth_anything_v2_authorized": False,
    "require_real_depth_when_available": True,
    "mock_depth_must_not_pass_as_real": True,
    "no_unauthorized_download": True,
}

EXECUTION_HARDENING_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "real_yolo_real_depth_if_available",
        "source_case_id": "real_image_yolo_with_depth_available",
        "yolo_mode": "real_runner",
        "depth_mode": "real_adapter",
        "expect_scene": True,
        "expect_yolo_mode": "real_runner",
        "expect_depth_mode": "real_adapter",
        "expect_execution_status": "pass_real_yolo_real_depth",
        "expect_not_mock_as_real": True,
    },
    {
        "case_id": "real_yolo_stub_depth_path",
        "source_case_id": "real_image_yolo_with_depth_available",
        "yolo_mode": "real_runner",
        "depth_mode": "stub",
        "expect_scene": True,
        "expect_yolo_mode": "real_runner",
        "expect_depth_mode": "stub_depth",
        "expect_execution_status": "pass_real_yolo_stub_depth",
        "expect_not_stub_as_full_real": True,
    },
    {
        "case_id": "cached_yolo_real_depth_if_available",
        "source_case_id": "real_image_yolo_with_depth_available",
        "yolo_mode": "cached",
        "depth_mode": "real_adapter",
        "expect_scene": True,
        "expect_yolo_mode": "cached_output",
        "expect_depth_mode": "real_adapter",
        "expect_execution_status": "pass_cached_yolo_real_depth",
    },
    {
        "case_id": "cached_yolo_mock_depth_alignment",
        "source_case_id": "real_image_yolo_depth_mock_alignment",
        "yolo_mode": "cached",
        "depth_mode": "mock",
        "expect_scene": True,
        "expect_degraded": True,
        "expect_execution_status": "pass_cached_yolo_mock_depth_alignment",
        "expect_not_mock_as_real": True,
    },
    {
        "case_id": "yolo_only_missing_depth_fallback",
        "source_case_id": "real_image_yolo_no_depth_fallback",
        "yolo_mode": "cached",
        "depth_mode": "missing",
        "expect_scene": True,
        "expect_execution_status": "degraded_missing_depth",
        "expect_depth_mode": "missing",
    },
    {
        "case_id": "multi_image_batch_field_construction",
        "batch_case_ids": (
            "real_image_yolo_with_depth_available",
            "real_image_yolo_depth_mock_alignment",
            "real_image_multiple_objects_field_assembly",
            "real_image_yolo_no_depth_fallback",
            "traceability_preserved_full_chain",
        ),
        "yolo_mode": "cached",
        "depth_mode": "mock",
        "expect_batch_min": 5,
    },
    {
        "case_id": "no_detection_failure_localization",
        "source_case_id": "real_image_no_detection_graceful_fail",
        "yolo_mode": "cached",
        "depth_mode": "mock",
        "expect_no_scene": True,
        "expect_execution_status": "failed_no_detection",
        "expect_localization_area": "yolo_output_bridge",
    },
    {
        "case_id": "invalid_bbox_failure_localization",
        "source_case_id": "real_image_invalid_bbox_handling",
        "yolo_mode": "cached",
        "depth_mode": "mock",
        "expect_scene": True,
        "expect_localization_area": "yolo_output_bridge",
    },
    {
        "case_id": "depth_blocked_by_authorization",
        "source_case_id": "real_image_yolo_with_depth_available",
        "yolo_mode": "cached",
        "depth_mode": "blocked",
        "expect_depth_blocked": True,
        "expect_execution_status": "blocked_depth_authorization",
        "optional_meta": True,
    },
    {
        "case_id": "traceability_full_chain_real_content",
        "source_case_id": "traceability_preserved_full_chain",
        "yolo_mode": "cached",
        "depth_mode": "real_adapter",
        "expect_scene": True,
        "expect_traceability_min": 6,
    },
)
