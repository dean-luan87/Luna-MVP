# -*- coding: utf-8 -*-
"""YOLO + Depth Controlled Real DryRun — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

REAL_DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "dryrun_result_id", "frame_input_ref", "yolo_output_ref", "depth_output_ref",
    "object_observation_candidates", "depth_observation_candidates",
    "aligned_observation_candidates", "object_depth_hint_candidates",
    "field_geometry_candidates", "enhanced_field_scene_candidate",
    "field_assembly_result_candidate", "success_path_status", "warning_summary",
    "missing_information", "degradation_summary", "failure_points",
    "readiness_for_core_pipeline", "readiness_for_success_path_hardening",
    "execution_boundary_summary", "source_refs", "evidence_refs", "traceability_refs",
    "candidate_only",
)

SUCCESS_PATH_STATUSES: Tuple[str, ...] = (
    "pass_real_yolo_real_depth",
    "pass_real_yolo_depth_fallback",
    "pass_real_yolo_mock_depth_alignment",
    "degraded_missing_depth",
    "degraded_low_depth_confidence",
    "failed_no_yolo_detection",
    "failed_alignment",
    "failed_field_assembly",
    "blocked_by_authorization",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_unauthorized_download": True,
    "no_weight_download": True,
    "no_model_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "no_field_simulation": True,
    "no_task_execution": True,
    "controlled_offline_dryrun": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_YOLO_DEPTH_CONTROLLED_REAL_MODEL_DRYRUN_READY_FOR_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING"
)
