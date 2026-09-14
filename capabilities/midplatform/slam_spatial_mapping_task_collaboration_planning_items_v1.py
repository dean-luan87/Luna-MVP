# -*- coding: utf-8 -*-
"""SLAM spatial mapping task collaboration planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

FINAL_DECISION_GO = (
    "MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_READY_FOR_TRACKING_OPTICAL_FLOW_MODEL_SMOKE_IO_INSPECTION"
)
SELECTED_NEXT_PHASE = "Phase-Midplatform-Tracking-OpticalFlow-Model-Smoke-IO-Inspection-v1-001"
SELECTED_NEXT_ROUTE = "Tracking Optical Flow Model Smoke IO Inspection"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_task_reasoning_execution": True,
    "no_action_output": True,
    "no_navigation_suggestion": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_field_simulation": True,
    "no_real_slam_execution": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "no_new_protocol_without_reason": True,
    "task_collaboration_planning_only": True,
    "midplatform_controlled_invocation_only": True,
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "task_reasoning_execution", "task_action_output", "navigation_suggestion",
        "world_model_candidate_assembly", "world_model_entry_write", "fact_admission",
        "field_simulation", "real_slam_execution", "model_download", "weight_download",
        "camera_runtime", "video_stream_runtime", "production_runtime",
        "new_protocol_without_reason", "bypass_midplatform_invocation",
        "cached_output_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_task_reasoning_execution",
    "evidence_not_action_output",
    "task_collaboration_not_world_model_assembly",
    "slam_outputs_task_evidence_only",
    "blocked_not_fabricated_evidence",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "slam_task_collaboration_protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_camera_pose_candidate": True,
    "reuse_camera_trajectory_candidate": True,
    "reuse_spatial_anchor_candidate": True,
    "reuse_local_map_candidate": True,
    "reuse_map_quality_candidate": True,
    "reuse_task_evidence_bundle_candidate_pattern": True,
    "reuse_model_invocation_control_policy": True,
    "reuse_traceability_refs": True,
    "reuse_authorization_boundary": True,
}

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

UPSTREAM_SKELETON_ARTIFACTS: Tuple[str, ...] = (
    "spatial_mapping_task_collaboration_mapping_review_v1.json",
    "spatial_mapping_later_world_model_readiness_review_v1.json",
    "protocol_reuse_decision_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "spatial_mapping_adapter_result_candidate_registry_v1.json",
)

TASK_MODEL_GROUPS: Tuple[Dict[str, Any], ...] = (
    {
        "group_id": "field_construction",
        "models": ("YOLO", "Depth", "SLAM_Spatial_Mapping"),
        "slam_inputs": ("RealFrameInputPackage", "EnhancedFieldSceneCandidate", "FieldGeometryCandidate", "session_ref"),
        "slam_outputs": ("CameraPoseCandidate", "SpatialAnchorCandidate", "LocalMapCandidate", "MapQualityCandidate"),
        "evidence_outputs": (
            "FieldConstructionEvidenceCandidate", "SpatialContinuityEvidenceCandidate",
            "LocalMapEvidenceCandidate", "FieldConstructionMissingInformationCandidate",
        ),
        "no_world_model_candidate": True,
    },
    {
        "group_id": "indoor_navigation_context",
        "models": ("YOLO", "OCR", "SLAM_Spatial_Mapping"),
        "slam_inputs": ("RealFrameInputPackage", "CameraPoseCandidate", "LocalMapCandidate", "EnhancedFieldSceneCandidate"),
        "slam_outputs": ("SpatialAnchorCandidate", "CameraTrajectoryCandidate", "LocalMapCandidate"),
        "evidence_outputs": (
            "IndoorSpatialContextEvidenceCandidate", "DoorElevatorSpatialEvidenceCandidate",
            "FloorSignSpatialEvidenceCandidate", "IndoorNavigationMissingInformationCandidate",
        ),
        "no_action_output": True,
    },
    {
        "group_id": "return_to_location_context",
        "models": ("SLAM_Spatial_Mapping", "YOLO", "Tracking_optional"),
        "slam_inputs": ("frame_sequence_refs", "SpatialAnchorCandidate", "LocalMapCandidate"),
        "slam_outputs": ("CameraTrajectoryCandidate", "SpatialAnchorCandidate", "LocalMapCandidate", "MapQualityCandidate"),
        "evidence_outputs": (
            "ReturnLocationEvidenceCandidate", "AnchorRecallEvidenceCandidate",
            "PathContinuityEvidenceCandidate", "ReturnLocationMissingInformationCandidate",
        ),
        "no_path_planning": True,
    },
    {
        "group_id": "path_memory_context",
        "models": ("SLAM_Spatial_Mapping", "Depth", "YOLO_optional"),
        "slam_inputs": ("frame_sequence_refs", "FieldGeometryCandidate", "EnhancedFieldSceneCandidate"),
        "slam_outputs": ("CameraTrajectoryCandidate", "LocalMapCandidate", "MapQualityCandidate"),
        "evidence_outputs": (
            "PathMemoryEvidenceCandidate", "TrajectoryEvidenceCandidate",
            "LocalMapQualityEvidenceCandidate", "PathMemoryMissingInformationCandidate",
        ),
        "no_long_term_memory_write": True,
    },
)

INVOCATION_CONTROL_POLICY: Dict[str, Any] = {
    "policy_id": "slam_task_invocation_control_policy_v1",
    "policy_name": "ModelInvocationControlPolicy",
    "new_protocol_added": False,
    "rules": (
        "midplatform_decides_slam_invocation",
        "slam_must_not_invoke_other_models",
        "task_context_ref_or_field_context_ref_required",
        "authorization_ref_required",
        "outputs_return_to_candidate_layer_only",
        "outputs_must_not_enter_decision_layer",
        "outputs_must_not_write_world_model",
        "missing_failure_low_quality_must_surface",
        "task_action_and_final_decision_deferred",
    ),
}

FAILURE_DEGRADATION_POLICY: Tuple[Dict[str, Any], ...] = (
    {"condition": "no_pose_output", "impact": "spatial_localization_evidence_missing", "handling": "MissingInformationCandidate"},
    {"condition": "high_drift_risk", "impact": "path_map_quality_degraded", "handling": "MapQualityCandidate_degraded"},
    {"condition": "scale_unknown", "impact": "distance_scale_unreliable", "handling": "no_high_confidence"},
    {"condition": "no_anchor", "impact": "target_location_unstable", "handling": "AnchorRecallEvidenceCandidate_degraded"},
    {"condition": "blocked_by_authorization", "impact": "slam_not_invokable", "handling": "blocked_evidence_no_fallback_fabrication"},
    {"condition": "cached_output_only", "impact": "not_real_runtime", "handling": "execution_mode_cached_output"},
)

TASK_INPUT_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {"group_id": g["group_id"], "slam_inputs": list(g["slam_inputs"])} for g in TASK_MODEL_GROUPS
)

TASK_OUTPUT_EVIDENCE_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {
        "group_id": g["group_id"],
        "slam_outputs": list(g["slam_outputs"]),
        "evidence_outputs": list(g["evidence_outputs"]),
    }
    for g in TASK_MODEL_GROUPS
)

PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "field_construction_yolo_depth_slam_group", "group_id": "field_construction", "models": ("YOLO", "Depth", "SLAM_Spatial_Mapping")},
    {"case_id": "indoor_navigation_yolo_ocr_slam_group", "group_id": "indoor_navigation_context", "models": ("YOLO", "OCR", "SLAM_Spatial_Mapping")},
    {"case_id": "return_to_location_slam_yolo_tracking_group", "group_id": "return_to_location_context", "models": ("SLAM_Spatial_Mapping", "YOLO", "Tracking_optional")},
    {"case_id": "path_memory_slam_depth_yolo_group", "group_id": "path_memory_context", "models": ("SLAM_Spatial_Mapping", "Depth", "YOLO_optional")},
    {"case_id": "slam_no_pose_missing_information", "failure_condition": "no_pose_output", "expect_handling": "MissingInformationCandidate"},
    {"case_id": "slam_high_drift_degraded_evidence", "failure_condition": "high_drift_risk", "expect_handling": "MapQualityCandidate_degraded"},
    {"case_id": "slam_scale_unknown_no_high_confidence", "failure_condition": "scale_unknown", "expect_handling": "no_high_confidence"},
    {"case_id": "slam_blocked_by_authorization", "failure_condition": "blocked_by_authorization", "expect_handling": "blocked_evidence_no_fallback_fabrication"},
    {"case_id": "slam_cached_output_not_real_run", "failure_condition": "cached_output_only", "expect_handling": "execution_mode_cached_output"},
    {"case_id": "task_group_no_action_output", "expect_no_action": True},
    {"case_id": "no_world_model_candidate_generated", "expect_no_wm_candidate": True},
    {"case_id": "no_new_protocol_created", "expect_new_protocol": False},
)
