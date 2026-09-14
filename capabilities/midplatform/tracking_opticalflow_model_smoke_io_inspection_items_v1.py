# -*- coding: utf-8 -*-
"""Tracking / Optical Flow model smoke IO inspection — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Tracking-OpticalFlow-Adapter-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Tracking Optical Flow Adapter Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "adapter_skeleton", "task_collaboration_execution", "field_simulation", "simulated_route",
        "world_model_candidate_assembly", "world_model_entry_write", "fact_admission",
        "task_reasoning", "task_action_output", "navigation_suggestion",
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
    "inspection_not_adapter_skeleton",
)

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

DEFAULT_TRACKING_OPTICALFLOW_AVAILABILITY: Dict[str, Any] = {
    "matrix_id": "tracking_opticalflow_availability_matrix_v1",
    "local_tracker_available": False,
    "local_flow_adapter_available": False,
    "local_weights_available": False,
    "dependencies_available": False,
    "cached_tracking_output_available": True,
    "cached_flow_output_available": True,
    "adapter_stub_available": True,
    "model_download_authorized": False,
    "weight_download_authorized": False,
    "camera_runtime_authorized": False,
    "video_stream_authorized": False,
    "no_unauthorized_download": True,
}

CACHED_TRACKING_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_tracking_output_fixture_v1",
    "model_role": "tracking_optical_flow",
    "subtype": "tracking",
    "outputs": {
        "track_id": "trk_fixture_001",
        "bbox_sequence": [{"frame": 0, "bbox": [10, 20, 50, 80]}, {"frame": 1, "bbox": [12, 21, 52, 81]}],
        "track_confidence": 0.78,
        "lifecycle_status": "active",
    },
}

CACHED_FLOW_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_optical_flow_output_fixture_v1",
    "model_role": "tracking_optical_flow",
    "subtype": "optical_flow",
    "outputs": {
        "motion_vector": {"dx": 0.12, "dy": -0.03},
        "flow_map_summary": {"width": 64, "height": 48, "mean_magnitude": 0.15},
    },
}

ADAPTER_STUB_IO_SAMPLE: Dict[str, Any] = {
    "sample_id": "tracking_opticalflow_adapter_stub_io_fixture_v1",
    "input_format": "RealFrameInputPackage[] + ObjectObservationCandidate[] + MultiModelAlignedObservationCandidate",
    "output_format": "track_id/bbox_sequence/motion_vector candidate-shaped dicts",
    "execution_mode": "adapter_stub",
}

CANDIDATE_MAPPING_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"model_output": "track_id", "target": "ObjectTrackCandidate", "status": "feasible"},
    {"model_output": "object_continuity", "target": "ObjectPersistenceCandidate", "status": "feasible"},
    {"model_output": "motion_vector", "target": "MotionCandidate", "status": "feasible"},
    {"model_output": "track_confidence", "target": "TrackingQualityCandidate", "status": "feasible"},
)

SMOKE_IO_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "tracking_local_adapter_available_smoke",
        "path": "P0",
        "inspect_subtype": "tracking",
        "availability_override": {"local_tracker_available": True, "local_weights_available": True, "dependencies_available": True},
        "expect_execution_mode": "local_real_model",
        "expect_smoke_completed": True,
    },
    {
        "case_id": "tracking_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "tracking",
        "availability_override": {"cached_tracking_output_available": True, "local_tracker_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "tracking_adapter_stub_io_inspection",
        "path": "P2",
        "inspect_subtype": "tracking",
        "availability_override": {"adapter_stub_available": True, "local_tracker_available": False, "cached_tracking_output_available": False, "cached_flow_output_available": False},
        "expect_execution_mode": "adapter_stub",
        "expect_mapping_feasible": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "optical_flow_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "optical_flow",
        "availability_override": {"cached_flow_output_available": True, "cached_tracking_output_available": False, "local_tracker_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_flow_output": True,
    },
    {
        "case_id": "missing_weight_blocked",
        "path": "P3",
        "availability_override": {"local_tracker_available": True, "local_weights_available": False},
        "expect_execution_mode": "blocked_by_missing_weight",
        "expect_no_download": True,
    },
    {
        "case_id": "missing_dependency_blocked",
        "path": "P3",
        "availability_override": {"local_tracker_available": True, "local_weights_available": True, "dependencies_available": False},
        "expect_execution_mode": "blocked_by_missing_dependency",
        "expect_no_download": True,
    },
    {
        "case_id": "track_id_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "tracking",
        "availability_override": {"cached_tracking_output_available": True},
        "expect_mapping_target": "ObjectTrackCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "object_persistence_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "tracking",
        "availability_override": {"cached_tracking_output_available": True},
        "expect_mapping_target": "ObjectPersistenceCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "motion_candidate_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "optical_flow",
        "availability_override": {"cached_flow_output_available": True, "cached_tracking_output_available": False},
        "expect_mapping_target": "MotionCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "traceability_preserved",
        "path": "P1",
        "inspect_subtype": "tracking",
        "availability_override": {"cached_tracking_output_available": True},
        "expect_traceability": True,
    },
    {
        "case_id": "cached_output_not_marked_as_real_run",
        "path": "P1",
        "inspect_subtype": "tracking",
        "availability_override": {"cached_tracking_output_available": True},
        "expect_cached_not_real": True,
    },
    {
        "case_id": "adapter_stub_not_marked_as_real_run",
        "path": "P2",
        "inspect_subtype": "tracking",
        "availability_override": {"adapter_stub_available": True, "cached_tracking_output_available": False, "cached_flow_output_available": False},
        "expect_stub_not_real": True,
    },
    {
        "case_id": "no_new_protocol_without_reason",
        "path": "P2",
        "availability_override": {"adapter_stub_available": True},
        "expect_new_protocol": False,
    },
)
