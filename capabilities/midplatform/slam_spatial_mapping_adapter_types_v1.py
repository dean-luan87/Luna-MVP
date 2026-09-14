# -*- coding: utf-8 -*-
"""SLAM / Spatial Mapping adapter types v1 (revision based on smoke IO inspection)."""

from __future__ import annotations

from typing import Dict, Tuple

ADAPTER_INPUT_FIELDS: Tuple[str, ...] = (
    "adapter_input_id", "model_role", "model_ref", "execution_mode", "smoke_run_ref",
    "io_inspection_ref", "frame_inputs", "enhanced_field_scene_refs", "field_geometry_refs",
    "session_ref", "authorization_ref", "source_refs", "traceability_refs", "candidate_only",
)

RAW_OUTPUT_FIELDS: Tuple[str, ...] = (
    "raw_output_id", "source_smoke_run_ref", "source_io_inspection_ref", "model_ref",
    "execution_mode", "frame_refs", "timestamp_range", "output_payload_type",
    "raw_pose_payload", "raw_trajectory_payload", "raw_anchor_payload", "raw_map_payload",
    "raw_quality_payload", "parseability_status", "warning_codes", "missing_information",
    "source_refs", "traceability_refs", "candidate_only",
)

CAMERA_POSE_FIELDS: Tuple[str, ...] = (
    "camera_pose_candidate_id", "source_raw_output_ref", "frame_ref", "timestamp",
    "camera_ref", "session_ref", "coordinate_mode", "position_candidate",
    "orientation_candidate", "pose_confidence", "scale_status", "drift_risk",
    "quality_status", "warning_codes", "missing_information", "source_refs",
    "evidence_refs", "traceability_refs", "candidate_only",
)

CAMERA_TRAJECTORY_FIELDS: Tuple[str, ...] = (
    "camera_trajectory_candidate_id", "source_raw_output_ref", "session_ref", "frame_refs",
    "pose_candidate_refs", "trajectory_confidence", "drift_summary", "scale_status",
    "missing_information", "warning_codes", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

SPATIAL_ANCHOR_FIELDS: Tuple[str, ...] = (
    "spatial_anchor_candidate_id", "source_raw_output_ref", "anchor_type", "source_frame_refs",
    "associated_field_entity_refs", "associated_geometry_refs", "position_candidate",
    "coordinate_mode", "stability_score", "observation_count", "first_seen_at", "last_seen_at",
    "conflict_refs", "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

LOCAL_MAP_FIELDS: Tuple[str, ...] = (
    "local_map_candidate_id", "source_raw_output_ref", "session_ref", "frame_refs",
    "camera_trajectory_ref", "spatial_anchor_refs", "associated_field_scene_refs",
    "local_geometry_summary", "map_quality", "drift_summary", "missing_information",
    "conflict_summary", "source_refs", "evidence_refs", "traceability_refs", "candidate_only",
)

MAP_QUALITY_FIELDS: Tuple[str, ...] = (
    "map_quality_candidate_id", "source_raw_output_ref", "local_map_ref", "pose_quality",
    "anchor_quality", "drift_risk", "scale_reliability", "coverage_status", "quality_status",
    "blockers", "warnings", "source_refs", "traceability_refs", "candidate_only",
)

ADAPTER_RESULT_FIELDS: Tuple[str, ...] = (
    "adapter_result_id", "adapter_input_ref", "smoke_run_ref", "io_inspection_ref",
    "execution_mode", "camera_pose_candidates", "camera_trajectory_candidates",
    "spatial_anchor_candidates", "local_map_candidates", "map_quality_candidates",
    "accepted_output_count", "rejected_output_count", "missing_information",
    "warning_summary", "conflict_summary", "readiness_for_midplatform_task_collaboration",
    "readiness_for_later_world_model_candidate_assembly", "non_execution_flags",
    "source_refs", "traceability_refs", "candidate_only",
)

EXECUTION_MODES: Tuple[str, ...] = (
    "local_real_model", "local_adapter", "cached_output", "adapter_stub",
    "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_real_slam_execution": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_field_simulation": True,
    "no_task_reasoning": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_task_action_output": True,
    "no_new_protocol_without_reason": True,
    "adapter_skeleton_only": True,
    "cached_output_not_marked_as_real_run": True,
    "adapter_stub_not_marked_as_real_run": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_SLAM_SPATIAL_MAPPING_ADAPTER_SKELETON_READY_FOR_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING"
)
