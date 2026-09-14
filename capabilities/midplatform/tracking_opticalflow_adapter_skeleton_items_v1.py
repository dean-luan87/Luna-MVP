# -*- coding: utf-8 -*-
"""Tracking / Optical Flow adapter skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Tracking-OpticalFlow-Task-Collaboration-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Tracking Optical Flow Task Collaboration Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_tracking_execution", "real_opticalflow_execution", "model_download", "weight_download",
        "large_dependency_install", "camera_runtime", "video_stream_runtime", "field_simulation",
        "simulated_route", "task_reasoning", "task_action_output", "navigation_suggestion",
        "world_model_candidate_assembly", "world_model_entry_write", "world_entity_candidate_generation",
        "fact_admission", "new_protocol_without_reason", "production_runtime",
        "cached_output_as_real_run", "adapter_stub_as_real_run",
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
    "reuse_object_observation_candidate": True,
    "reuse_multi_model_aligned_observation_candidate": True,
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
    {"output": "ObjectTrackCandidate", "role": "future_object_identity_continuity", "assembly": "deferred"},
    {"output": "ObjectPersistenceCandidate", "role": "future_world_entity_persistence", "assembly": "deferred"},
    {"output": "MotionCandidate", "role": "future_dynamic_risk_evidence", "assembly": "deferred"},
    {"output": "TrackingQualityCandidate", "role": "future_quality_gate", "assembly": "deferred"},
)

TASK_COLLABORATION_MAPPING: Tuple[Dict[str, Any], ...] = (
    {
        "scenario": "road_crossing_safety",
        "models": ("YOLO", "Depth", "Tracking / Optical Flow"),
        "tracking_outputs": ("ObjectTrackCandidate", "MotionCandidate", "TrackingQualityCandidate"),
    },
    {
        "scenario": "moving_obstacle_avoidance",
        "models": ("YOLO", "Depth", "Tracking / Optical Flow"),
        "tracking_outputs": ("MotionCandidate", "ObjectTrackCandidate", "TrackingQualityCandidate"),
    },
    {
        "scenario": "find_moving_object",
        "models": ("YOLO", "Tracking", "Depth_optional"),
        "tracking_outputs": ("ObjectTrackCandidate", "ObjectPersistenceCandidate"),
    },
    {
        "scenario": "return_to_location_context",
        "models": ("SLAM / Spatial Mapping", "YOLO", "Tracking_optional"),
        "tracking_outputs": ("ObjectPersistenceCandidate", "MotionCandidate"),
    },
)

SMOKE_IO_ARTIFACT_FILES: Tuple[str, ...] = (
    "tracking_opticalflow_model_smoke_io_inspection_report_v1.json",
    "model_smoke_run_candidate_registry_v1.json",
    "model_io_inspection_candidate_registry_v1.json",
    "model_candidate_mapping_feasibility_registry_v1.json",
    "tracking_opticalflow_available_model_review_v1.json",
    "tracking_opticalflow_input_format_review_v1.json",
    "tracking_opticalflow_output_format_review_v1.json",
    "tracking_opticalflow_failure_point_review_v1.json",
    "tracking_opticalflow_candidate_mapping_review_v1.json",
    "model_execution_authorization_review_v1.json",
    "new_protocol_reason_required_report_v1.json",
)

SKELETON_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "object_track_from_cached_tracking_output",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "expect_tracks_min": 1,
        "expect_execution_mode": "cached_output",
        "expect_not_real_run": True,
    },
    {
        "case_id": "object_track_from_adapter_stub",
        "source_smoke_case_id": "tracking_adapter_stub_io_inspection",
        "frame_count": 1,
        "inspect_subtype": "tracking",
        "expect_tracks_min": 1,
        "expect_execution_mode": "adapter_stub",
        "expect_not_real_run": True,
    },
    {
        "case_id": "optical_flow_cached_output_to_motion_candidate",
        "source_smoke_case_id": "optical_flow_cached_output_inspection",
        "frame_count": 1,
        "inspect_subtype": "optical_flow",
        "expect_motions_min": 1,
        "expect_execution_mode": "cached_output",
    },
    {
        "case_id": "bbox_delta_to_motion_candidate",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "overrides": {"force_bbox_delta": True},
        "expect_motions_min": 1,
    },
    {
        "case_id": "object_persistence_from_track_sequence",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "expect_persistence_min": 1,
    },
    {
        "case_id": "short_track_not_persistent",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 1,
        "inspect_subtype": "tracking",
        "overrides": {"short_track": True, "observation_count": 1},
        "expect_not_persistent": True,
    },
    {
        "case_id": "identity_switch_degrades_persistence",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "overrides": {"identity_switch_risk": "high"},
        "expect_persistence_degraded": True,
    },
    {
        "case_id": "lost_track_lifecycle_degraded",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "overrides": {"lifecycle_status": "lost", "lost_frame_count": 5},
        "expect_lost_degraded": True,
    },
    {
        "case_id": "tracking_quality_from_cached_output",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "expect_quality_min": 1,
    },
    {
        "case_id": "blocked_missing_weight_no_output_fabrication",
        "source_smoke_case_id": "missing_weight_blocked",
        "frame_count": 1,
        "inspect_subtype": "tracking",
        "expect_blocked": True,
        "expect_no_fabrication": True,
    },
    {
        "case_id": "blocked_missing_dependency_no_output_fabrication",
        "source_smoke_case_id": "missing_dependency_blocked",
        "frame_count": 1,
        "inspect_subtype": "tracking",
        "expect_blocked": True,
        "expect_no_fabrication": True,
    },
    {
        "case_id": "readiness_for_task_collaboration_true",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "expect_task_readiness": True,
    },
    {
        "case_id": "readiness_for_later_world_model_candidate_assembly_true",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 2,
        "inspect_subtype": "tracking",
        "expect_later_wm_readiness": True,
        "expect_no_wm_assembly": True,
    },
    {
        "case_id": "no_new_protocol_created",
        "source_smoke_case_id": "no_new_protocol_without_reason",
        "inspect_subtype": "tracking",
        "expect_new_protocol": False,
    },
    {
        "case_id": "no_action_output",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 1,
        "inspect_subtype": "tracking",
        "expect_no_action": True,
    },
    {
        "case_id": "no_world_model_assembly",
        "source_smoke_case_id": "tracking_cached_output_inspection",
        "frame_count": 1,
        "inspect_subtype": "tracking",
        "expect_no_wm_candidate": True,
    },
)
