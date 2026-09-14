# -*- coding: utf-8 -*-
"""SLAM spatial mapping model smoke IO inspection — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-SLAM-Spatial-Mapping-Adapter-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "SLAM Spatial Mapping Adapter Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_simulation", "simulated_route", "world_model_candidate_assembly",
        "world_model_entry_write", "fact_admission", "task_reasoning", "task_action_output",
        "unauthorized_model_download", "unauthorized_weight_download", "large_dependency_install",
        "camera_runtime", "video_stream_runtime", "production_runtime",
        "new_protocol_without_reason", "cached_output_as_real_run", "adapter_stub_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "smoke_io_inspection_not_field_simulation",
    "blocked_not_failed_download",
    "cached_output_not_real_model_run",
    "adapter_stub_not_real_model_run",
    "inspection_candidate_not_world_model_entry",
)

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

DEFAULT_SLAM_AVAILABILITY: Dict[str, Any] = {
    "matrix_id": "slam_spatial_mapping_availability_matrix_v1",
    "local_slam_runner_available": False,
    "local_slam_weights_available": False,
    "slam_dependencies_available": False,
    "cached_output_available": True,
    "adapter_stub_available": True,
    "model_download_authorized": False,
    "weight_download_authorized": False,
    "camera_runtime_authorized": False,
    "video_stream_authorized": False,
    "no_unauthorized_download": True,
}

CACHED_SLAM_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_slam_output_fixture_v1",
    "model_role": "slam_spatial_mapping",
    "outputs": {
        "pose": {"position": {"x": 0.1, "y": 0.0, "z": 0.0}, "orientation": {"yaw": 0.05}, "confidence": 0.82},
        "trajectory": {"frame_count": 3, "drift_risk": "low"},
        "local_map": {"type": "sparse_point_cloud", "point_count": 1200},
        "quality": {"scale_status": "scale_estimated", "drift_risk": "low", "coverage": "partial"},
    },
}

ADAPTER_STUB_IO_SAMPLE: Dict[str, Any] = {
    "sample_id": "slam_adapter_stub_io_fixture_v1",
    "input_format": "RealFrameInputPackage[] + session_ref",
    "output_format": "pose/trajectory/anchor/local_map/quality candidate-shaped dicts",
    "execution_mode": "adapter_stub",
}

CANDIDATE_MAPPING_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"model_output": "camera_pose", "target": "CameraPoseCandidate", "status": "feasible"},
    {"model_output": "camera_trajectory", "target": "CameraTrajectoryCandidate", "status": "feasible"},
    {"model_output": "spatial_anchor", "target": "SpatialAnchorCandidate", "status": "feasible"},
    {"model_output": "local_map_sparse_point_cloud", "target": "LocalMapCandidate", "status": "feasible_with_summary"},
    {"model_output": "quality_drift_scale", "target": "MapQualityCandidate", "status": "feasible"},
)

SMOKE_IO_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "slam_local_model_available_smoke",
        "path": "P0",
        "availability_override": {"local_slam_runner_available": True, "local_slam_weights_available": True, "slam_dependencies_available": True},
        "expect_execution_mode": "local_real_model",
        "expect_smoke_completed": True,
        "expect_not_marked_as_stub": True,
    },
    {
        "case_id": "slam_cached_output_inspection",
        "path": "P1",
        "availability_override": {"cached_output_available": True, "local_slam_runner_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "slam_adapter_stub_io_inspection",
        "path": "P2",
        "availability_override": {"adapter_stub_available": True, "local_slam_runner_available": False, "cached_output_available": False},
        "expect_execution_mode": "adapter_stub",
        "expect_mapping_feasible": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "missing_weight_blocked",
        "path": "P3",
        "availability_override": {"local_slam_runner_available": True, "local_slam_weights_available": False},
        "expect_execution_mode": "blocked_by_missing_weight",
        "expect_no_download": True,
    },
    {
        "case_id": "missing_dependency_blocked",
        "path": "P3",
        "availability_override": {"local_slam_runner_available": True, "local_slam_weights_available": True, "slam_dependencies_available": False},
        "expect_execution_mode": "blocked_by_missing_dependency",
        "expect_no_download": True,
    },
    {
        "case_id": "pose_output_mapping_feasibility",
        "path": "P1",
        "availability_override": {"cached_output_available": True},
        "expect_mapping_target": "CameraPoseCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "local_map_output_mapping_feasibility",
        "path": "P1",
        "availability_override": {"cached_output_available": True},
        "expect_mapping_target": "LocalMapCandidate",
        "expect_mapping_status": "feasible_with_summary",
    },
    {
        "case_id": "drift_quality_output_mapping_feasibility",
        "path": "P1",
        "availability_override": {"cached_output_available": True},
        "expect_mapping_target": "MapQualityCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "traceability_preserved",
        "path": "P1",
        "availability_override": {"cached_output_available": True},
        "expect_traceability": True,
    },
    {
        "case_id": "no_new_protocol_without_reason",
        "path": "P2",
        "availability_override": {"adapter_stub_available": True},
        "expect_new_protocol": False,
    },
)
