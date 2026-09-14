# -*- coding: utf-8 -*-
"""SLAM spatial mapping adapter skeleton — items v1 (revision)."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-SLAM-Spatial-Mapping-Task-Collaboration-Planning-v1-001"
SELECTED_NEXT_ROUTE = "SLAM Spatial Mapping Task Collaboration Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_slam_execution", "model_download", "weight_download", "camera_runtime",
        "video_stream_runtime", "field_simulation", "task_reasoning", "task_action_output",
        "world_model_candidate_assembly", "world_model_entry_write", "fact_admission",
        "new_protocol_without_reason", "production_runtime", "cached_output_as_real_run",
        "adapter_stub_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "adapter_skeleton_based_on_smoke_io_inspection",
    "cached_output_not_real_model_run",
    "adapter_stub_not_real_model_run",
    "blocked_not_fabricated_output",
    "readiness_not_world_model_assembly",
    "field_simulation_not_reintroduced",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_smoke_io_inspection_artifacts": True,
    "reuse_traceability_refs": True,
    "reuse_authorization_boundary": True,
}

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

LATER_WORLD_MODEL_READINESS: Tuple[Dict[str, Any], ...] = (
    {"output": "CameraPoseCandidate", "role": "future_session_local_coordinate", "assembly": "deferred"},
    {"output": "CameraTrajectoryCandidate", "role": "future_multi_frame_continuity", "assembly": "deferred"},
    {"output": "SpatialAnchorCandidate", "role": "future_world_anchor", "assembly": "deferred"},
    {"output": "LocalMapCandidate", "role": "future_spatial_skeleton", "assembly": "deferred"},
    {"output": "MapQualityCandidate", "role": "future_quality_gate", "assembly": "deferred"},
)

TASK_COLLABORATION_MAPPING: Tuple[Dict[str, Any], ...] = (
    {"scenario": "field_construction", "models": ("YOLO", "Depth", "SLAM"), "slam_outputs": ("CameraPoseCandidate", "LocalMapCandidate", "SpatialAnchorCandidate")},
    {"scenario": "indoor_navigation", "models": ("YOLO", "OCR", "SLAM"), "slam_outputs": ("CameraPoseCandidate", "SpatialAnchorCandidate", "LocalMapCandidate")},
    {"scenario": "return_to_location", "models": ("SLAM", "YOLO", "Tracking_optional"), "slam_outputs": ("CameraTrajectoryCandidate", "SpatialAnchorCandidate")},
    {"scenario": "path_memory", "models": ("SLAM", "Depth", "YOLO_optional"), "slam_outputs": ("CameraTrajectoryCandidate", "LocalMapCandidate")},
)

SMOKE_IO_ARTIFACT_FILES: Tuple[str, ...] = (
    "slam_spatial_mapping_model_smoke_io_inspection_report_v1.json",
    "model_smoke_run_candidate_registry_v1.json",
    "model_io_inspection_candidate_registry_v1.json",
    "model_candidate_mapping_feasibility_registry_v1.json",
    "slam_spatial_mapping_available_model_review_v1.json",
    "slam_spatial_mapping_input_format_review_v1.json",
    "slam_spatial_mapping_output_format_review_v1.json",
    "slam_spatial_mapping_failure_point_review_v1.json",
    "slam_spatial_mapping_candidate_mapping_review_v1.json",
    "model_execution_authorization_review_v1.json",
    "new_protocol_reason_required_report_v1.json",
)

SKELETON_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "pose_candidate_from_local_real_model_output", "source_smoke_case_id": "slam_local_model_available_smoke", "frame_count": 1, "expect_poses_min": 1, "expect_execution_mode": "local_real_model"},
    {"case_id": "pose_candidate_from_cached_output", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 1, "expect_poses_min": 1, "expect_execution_mode": "cached_output", "expect_not_real_run": True},
    {"case_id": "adapter_stub_io_to_pose_candidate", "source_smoke_case_id": "slam_adapter_stub_io_inspection", "frame_count": 1, "expect_poses_min": 1, "expect_execution_mode": "adapter_stub", "expect_not_real_run": True},
    {"case_id": "trajectory_candidate_multi_frame", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 3, "expect_trajectory": True, "expect_poses_min": 1},
    {"case_id": "static_object_spatial_anchor", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 1, "expect_anchors_min": 1, "entity_label": "chair"},
    {"case_id": "local_map_from_pose_anchor_field_scene", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 2, "expect_local_map": True, "expect_anchors_min": 1},
    {"case_id": "map_quality_degraded_by_drift", "source_smoke_case_id": "drift_quality_output_mapping_feasibility", "frame_count": 1, "overrides": {"drift_risk": "high"}, "expect_quality_degraded": True},
    {"case_id": "scale_unknown_not_high_quality", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 1, "overrides": {"scale_status": "scale_unknown", "pose_confidence": "high"}, "expect_pose_conf_not_high": True},
    {"case_id": "blocked_missing_weight_no_output_fabrication", "source_smoke_case_id": "missing_weight_blocked", "frame_count": 1, "expect_blocked": True, "expect_poses_min": 0, "expect_no_fabrication": True},
    {"case_id": "readiness_for_task_collaboration_true", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 2, "expect_task_readiness": True},
    {"case_id": "readiness_for_later_world_model_candidate_assembly_true", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 2, "expect_later_wm_readiness": True, "expect_no_wm_assembly": True},
    {"case_id": "no_new_protocol_created", "source_smoke_case_id": "no_new_protocol_without_reason", "expect_new_protocol": False},
    {"case_id": "no_world_model_assembly", "source_smoke_case_id": "slam_cached_output_inspection", "frame_count": 1, "expect_no_wm_candidate": True},
    {"case_id": "no_field_simulation_reintroduced", "source_smoke_case_id": "slam_adapter_stub_io_inspection", "expect_no_simulation": True},
)
