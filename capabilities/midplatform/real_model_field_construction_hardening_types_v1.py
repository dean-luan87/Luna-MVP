# -*- coding: utf-8 -*-
"""Real Model Field Construction Success Path Hardening — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

HARDENED_RESULT_FIELDS: Tuple[str, ...] = (
    "hardened_result_id", "source_dryrun_result_ref", "enhanced_field_scene_ref",
    "success_path_status", "stability_status", "explainability_status",
    "reusability_status", "quality_status", "localized_failure_points",
    "warning_summary", "missing_information", "recommended_fix_areas",
    "readiness_for_core_success_path", "readiness_for_field_simulation_planning",
    "candidate_only",
)

QUALITY_ASSESSMENT_FIELDS: Tuple[str, ...] = (
    "quality_assessment_id", "enhanced_field_scene_ref", "scene_quality_status",
    "depth_quality_status", "geometry_quality_status", "zone_summary_status",
    "traceability_status", "degradation_status", "quality_score_discrete",
    "reason_codes", "candidate_only",
)

REUSABLE_CASE_FIELDS: Tuple[str, ...] = (
    "reusable_case_id", "source_case_id", "frame_input_ref", "yolo_output_ref",
    "depth_output_ref", "enhanced_field_scene_ref", "case_type", "reusable_for",
    "limitations", "required_authorization", "candidate_only",
)

STABILITY_STATUSES: Tuple[str, ...] = ("stable", "mostly_stable", "unstable", "not_applicable")
EXPLAINABILITY_STATUSES: Tuple[str, ...] = ("complete", "partial", "incomplete", "not_applicable")
REUSABILITY_STATUSES: Tuple[str, ...] = ("reusable", "reusable_degraded", "failure_baseline", "not_reusable")
QUALITY_STATUSES: Tuple[str, ...] = ("strong", "usable", "degraded_usable", "weak", "blocked")

QUALITY_SCORE_DISCRETE: Tuple[str, ...] = ("strong", "usable", "degraded_usable", "weak", "blocked")

FAILURE_LOCALIZATION_AREAS: Tuple[str, ...] = (
    "frame_input_loader", "yolo_output_bridge", "depth_output_bridge",
    "candidate_conversion", "multi_model_alignment", "depth_object_fusion",
    "field_geometry_candidate", "field_assembly", "authorization_policy",
    "traceability_policy",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_unauthorized_download": True,
    "no_weight_download": True,
    "no_model_download": True,
    "no_real_yolo_rerun": True,
    "no_real_depth_rerun": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "no_field_simulation": True,
    "no_task_execution": True,
    "hardening_only_no_model_execution": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_REAL_MODEL_FIELD_CONSTRUCTION_SUCCESS_PATH_HARDENING_READY_FOR_FIELD_SIMULATION_PLANNING"
)
