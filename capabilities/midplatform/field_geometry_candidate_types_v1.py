# -*- coding: utf-8 -*-
"""Field Geometry Candidate — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

GEOMETRY_INPUT_FIELDS: Tuple[str, ...] = (
    "geometry_input_id",
    "object_observations",
    "object_depth_hints",
    "depth_object_fusion_result_ref",
)

OBJECT_SPATIAL_STATE_FIELDS: Tuple[str, ...] = (
    "object_spatial_state_id",
    "object_observation_ref",
    "object_depth_hint_ref",
    "frame_ref",
    "timestamp",
    "label",
    "bbox",
    "bbox_center",
    "depth_hint",
    "depth_value_unit",
    "pseudo_3d_position",
    "pseudo_3d_status",
    "distance_bucket",
    "field_zone",
    "spatial_confidence",
    "spatial_reliability_reasons",
    "depth_error_expected",
    "geometry_warning_codes",
    "missing_information",
    "source_refs",
    "evidence_refs",
    "traceability_refs",
    "candidate_only",
)

FIELD_GEOMETRY_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "geometry_candidate_id",
    "object_spatial_state_ref",
    "object_observation_ref",
    "object_depth_hint_ref",
    "frame_ref",
    "timestamp",
    "label",
    "bbox",
    "bbox_center",
    "pseudo_3d_position",
    "field_zone",
    "distance_bucket",
    "geometry_confidence",
    "geometry_status",
    "geometry_reliability_reasons",
    "depth_error_expected",
    "warning_codes",
    "missing_information",
    "conflict_refs",
    "source_refs",
    "evidence_refs",
    "traceability_refs",
    "candidate_only",
)

GEOMETRY_GENERATION_RESULT_FIELDS: Tuple[str, ...] = (
    "geometry_generation_result_id",
    "input_depth_object_fusion_result_ref",
    "object_spatial_state_candidates",
    "field_geometry_candidates",
    "accepted_geometry_count",
    "rejected_geometry_count",
    "geometry_unknown_count",
    "warning_summary",
    "missing_information",
    "readiness_for_field_assembly",
    "non_execution_flags",
    "candidate_only",
)

DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "case_id",
    "expected_spatial_count",
    "actual_spatial_count",
    "expected_geometry_count",
    "actual_geometry_count",
    "expected_rejected_count",
    "actual_rejected_count",
    "prohibited_behavior_absent",
    "case_passed",
    "reason_codes",
)

PSEUDO_3D_STATUSES: Tuple[str, ...] = (
    "pseudo_3d_estimated",
    "pseudo_3d_weak_estimated",
    "pseudo_3d_unknown",
    "pseudo_3d_rejected",
)

GEOMETRY_STATUSES: Tuple[str, ...] = (
    "geometry_estimated",
    "geometry_weak_estimated",
    "geometry_unknown",
    "geometry_rejected",
)

METRIC_NEAR_MAX_M = 3.0
METRIC_MIDDLE_MAX_M = 10.0
METRIC_FAR_MAX_M = 20.0

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_depth_inference": True,
    "no_runtime_execution": True,
    "no_field_scene_assembly": True,
    "no_scene_relation_generation": True,
    "no_slam_runtime": True,
    "no_field_simulation": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_GEOMETRY_CANDIDATE_SKELETON_READY_FOR_FIELD_ASSEMBLY_SKELETON"
)
