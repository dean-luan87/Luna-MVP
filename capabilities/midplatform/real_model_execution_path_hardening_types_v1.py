# -*- coding: utf-8 -*-
"""Real model execution path hardening types v1."""

from __future__ import annotations

from typing import Dict, Tuple

EXECUTION_INPUT_FIELDS: Tuple[str, ...] = (
    "execution_input_id", "image_set_ref", "frame_inputs", "yolo_execution_policy",
    "depth_execution_policy", "authorization_ref", "dryrun_scope", "candidate_only",
)

FRAME_INPUT_FIELDS: Tuple[str, ...] = (
    "frame_input_id", "image_path", "frame_ref", "timestamp", "frame_width",
    "frame_height", "source_ref", "fixture_type", "candidate_only",
)

AUTHORIZATION_FIELDS: Tuple[str, ...] = (
    "authorization_id", "yolo_real_runner_allowed", "yolo_cached_output_allowed",
    "depth_real_adapter_allowed", "depth_authorized_model_allowed", "depth_stub_allowed",
    "depth_mock_fallback_allowed", "model_download_allowed", "weight_download_allowed",
    "camera_runtime_allowed", "video_stream_allowed", "candidate_only",
)

EXECUTION_PATH_RESULT_FIELDS: Tuple[str, ...] = (
    "execution_path_result_id", "frame_input_ref", "yolo_execution_mode", "depth_execution_mode",
    "yolo_output_ref", "depth_output_ref", "object_observation_candidates",
    "depth_observation_candidate", "alignment_result_ref", "fusion_result_ref",
    "geometry_result_ref", "field_assembly_result_ref", "enhanced_field_scene_ref",
    "execution_status", "failure_points", "warning_summary", "missing_information",
    "traceability_refs", "candidate_only",
)

QUALITY_REPORT_FIELDS: Tuple[str, ...] = (
    "quality_report_id", "execution_path_result_refs", "total_frame_count",
    "passed_frame_count", "degraded_frame_count", "blocked_frame_count", "failed_frame_count",
    "yolo_real_runner_count", "yolo_cached_count", "depth_real_adapter_count", "depth_stub_count",
    "depth_mock_count", "enhanced_scene_count", "geometry_estimated_count", "geometry_unknown_count",
    "zone_assignment_summary", "depth_quality_summary", "geometry_quality_summary",
    "field_scene_quality_summary", "failure_localization_summary",
    "readiness_for_real_field_quality_evaluation", "mock_depth_marked_as_real",
    "stub_depth_marked_as_full_real", "candidate_only",
)

BASELINE_FIELDS: Tuple[str, ...] = (
    "baseline_id", "source_execution_result_ref", "baseline_type", "input_frame_ref",
    "enhanced_field_scene_ref", "quality_status", "limitations", "reusable_for",
    "required_execution_mode", "candidate_only",
)

EXECUTION_STATUSES: Tuple[str, ...] = (
    "pass_real_yolo_real_depth", "pass_real_yolo_stub_depth", "pass_real_yolo_cached_depth",
    "pass_cached_yolo_real_depth", "pass_cached_yolo_mock_depth_alignment",
    "degraded_missing_depth", "degraded_cached_yolo_only", "blocked_yolo_runner_missing",
    "blocked_depth_authorization", "failed_no_detection", "failed_field_assembly",
)

BASELINE_TYPES: Tuple[str, ...] = (
    "real_yolo_real_depth_baseline", "real_yolo_stub_depth_baseline",
    "cached_yolo_real_depth_baseline", "cached_yolo_mock_depth_degraded_baseline",
    "missing_depth_fallback_baseline", "failure_localization_baseline",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_field_simulation": True,
    "no_task_reasoning": True,
    "no_navigation_action": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_unauthorized_download": True,
    "no_weight_download": True,
    "no_model_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "route_switched_from_simulation_to_real_content": True,
    "field_simulation_deferred": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_READY_FOR_REAL_FIELD_CONSTRUCTION_QUALITY_EVALUATION"
)
