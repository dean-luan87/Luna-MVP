# -*- coding: utf-8 -*-
"""Depth Observation Candidate Ingestion — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

DEPTH_MODEL_OUTPUT_MOCK_FIELDS: Tuple[str, ...] = (
    "depth_output_id", "model_ref", "source_type", "frame_ref", "image_ref",
    "timestamp", "frame_width", "frame_height", "depth_map_ref", "depth_map_shape",
    "depth_value_unit", "depth_value_range", "depth_confidence_map_ref",
    "global_depth_confidence", "depth_source", "candidate_only",
)

DEPTH_OBSERVATION_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "depth_observation_id", "depth_output_ref", "model_ref", "frame_ref", "timestamp",
    "frame_width", "frame_height", "depth_map_ref", "depth_map_shape", "depth_value_unit",
    "depth_source", "depth_confidence", "depth_error_expected", "reliability_level",
    "missing_information", "warning_codes", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

OBJECT_DEPTH_HINT_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "object_depth_hint_id", "object_observation_ref", "depth_observation_ref", "frame_ref",
    "timestamp", "label", "bbox", "bbox_sampling_policy", "sampled_depth_value",
    "object_depth_hint", "depth_bucket", "field_zone_hint", "depth_source",
    "depth_confidence", "depth_error_expected", "depth_reliability_reasons",
    "missing_information", "warning_codes", "source_refs", "evidence_refs", "candidate_only",
)

DEPTH_INGESTION_RESULT_FIELDS: Tuple[str, ...] = (
    "ingestion_result_id", "depth_observation_candidate", "object_depth_hint_candidates",
    "accepted_object_count", "rejected_object_count", "depth_missing_count",
    "depth_unreliable_count", "warning_summary", "missing_information",
    "readiness_for_field_geometry", "non_execution_flags", "candidate_only",
)

DEPTH_SAMPLING_POLICY_FIELDS: Tuple[str, ...] = (
    "policy_id", "default_method", "fallback_method", "invalid_bbox_reject",
)

DEPTH_RELIABILITY_POLICY_FIELDS: Tuple[str, ...] = (
    "policy_id", "estimated_depth_error_expected", "no_hardware_fact",
    "unreliable_confidence_threshold", "missing_depth_bucket",
)

DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "case_id", "expected_hint_count", "actual_hint_count",
    "expected_rejected_count", "actual_rejected_count",
    "prohibited_behavior_absent", "case_passed", "reason_codes",
)

DEPTH_BUCKETS: Tuple[str, ...] = ("near", "middle", "far", "unknown")
FIELD_ZONE_HINTS: Tuple[str, ...] = ("inner_zone", "working_zone", "forecast_zone", "unknown")
DEPTH_VALUE_UNITS: Tuple[str, ...] = ("relative", "metric", "unknown")

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_depth_model_download": True,
    "no_weight_download": True,
    "no_real_depth_inference": True,
    "no_runtime_execution": True,
    "no_large_dependency_install": True,
    "no_slam_runtime": True,
    "no_scene_graph_runtime": True,
    "no_hardware_depth_fact": True,
}

TIMESTAMP_GAP_THRESHOLD_SEC: float = 1.0

FINAL_DECISION_GO = (
    "MIDPLATFORM_DEPTH_OBSERVATION_CANDIDATE_INGESTION_SKELETON_READY_FOR_YOLO_DEPTH_REAL_FIELD_SCENE_DRYRUN_PLANNING"
)
