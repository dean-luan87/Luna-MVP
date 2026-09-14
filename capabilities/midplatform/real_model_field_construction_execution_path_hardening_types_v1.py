# -*- coding: utf-8 -*-
"""Real Model Field Construction Execution Path Hardening — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

EXECUTION_PATH_RESULT_FIELDS: Tuple[str, ...] = (
    "execution_result_id", "frame_input_ref", "yolo_output_ref", "depth_output_ref",
    "enhanced_field_scene_ref", "execution_path_status", "yolo_execution_mode",
    "depth_execution_mode", "field_quality_report_ref", "quality_gate_status",
    "localized_failure_points", "warning_summary", "missing_information",
    "traceability_refs", "candidate_only",
)

QUALITY_REPORT_FIELDS: Tuple[str, ...] = (
    "quality_report_id", "enhanced_field_scene_ref", "field_quality_status",
    "depth_quality_status", "geometry_quality_status", "zone_reasonableness_status",
    "quality_scores", "quality_blockers", "quality_warnings", "mock_depth_marked_as_real",
    "candidate_only",
)

EXECUTION_PATH_STATUSES: Tuple[str, ...] = (
    "pass_real_yolo_real_depth",
    "pass_real_yolo_mock_depth_labeled",
    "pass_real_yolo_cached_depth_adapter",
    "degraded_missing_depth",
    "degraded_geometry_unknown",
    "blocked_by_authorization",
    "failed_no_yolo_detection",
    "failed_field_construction",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_field_simulation": True,
    "no_task_reasoning": True,
    "no_navigation_action": True,
    "no_unauthorized_download": True,
    "no_weight_download": True,
    "no_model_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "controlled_offline_execution_path_hardening": True,
    "field_simulation_deferred": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_EXECUTION_PATH_HARDENING_READY_FOR_REAL_DEPTH_MODEL_ADAPTER_CONTROLLED_EXECUTION"
)
