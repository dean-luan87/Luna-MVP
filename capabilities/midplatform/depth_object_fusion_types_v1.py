# -*- coding: utf-8 -*-
"""Depth-Object Fusion — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

FUSION_INPUT_FIELDS: Tuple[str, ...] = (
    "fusion_input_id", "aligned_candidates", "object_observations", "depth_observations",
    "alignment_result_ref",
)

BBOX_DEPTH_SAMPLING_POLICY_FIELDS: Tuple[str, ...] = (
    "policy_id", "default_method", "fallback_method", "invalid_bbox_reject",
)

OBJECT_DEPTH_HINT_FIELDS: Tuple[str, ...] = (
    "object_depth_hint_id", "aligned_candidate_ref", "object_observation_ref",
    "depth_observation_ref", "frame_ref", "timestamp", "label", "bbox",
    "bbox_sampling_policy", "sampled_depth_value", "object_depth_hint",
    "depth_value_unit", "depth_bucket", "field_zone_hint", "depth_source",
    "depth_confidence", "depth_error_expected", "depth_reliability_reasons",
    "alignment_confidence", "fusion_confidence", "missing_information",
    "warning_codes", "conflict_refs", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

FUSION_RESULT_FIELDS: Tuple[str, ...] = (
    "fusion_result_id", "input_alignment_result_ref", "object_depth_hint_candidates",
    "accepted_fusion_count", "rejected_fusion_count", "missing_depth_count",
    "unreliable_depth_count", "warning_summary", "conflict_summary",
    "missing_information", "readiness_for_field_geometry", "non_execution_flags",
    "candidate_only",
)

DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "case_id", "expected_hint_count", "actual_hint_count",
    "expected_rejected_count", "actual_rejected_count",
    "prohibited_behavior_absent", "case_passed", "reason_codes",
)

METRIC_NEAR_MAX_M = 3.0
METRIC_MIDDLE_MAX_M = 10.0
METRIC_FAR_MAX_M = 20.0

REJECTED_ALIGNMENT_STATUSES: Tuple[str, ...] = (
    "rejected_frame_mismatch", "rejected_timestamp_gap", "rejected_camera_mismatch",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_depth_inference": True,
    "no_runtime_execution": True,
    "no_field_geometry_generation": True,
    "no_pseudo_3d_position_generation": True,
    "no_field_scene_assembly": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_DEPTH_OBJECT_FUSION_SKELETON_READY_FOR_FIELD_GEOMETRY_CANDIDATE_SKELETON"
)
