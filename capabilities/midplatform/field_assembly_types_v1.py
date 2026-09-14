# -*- coding: utf-8 -*-
"""Field Assembly — types v1."""

from __future__ import annotations

from typing import Dict, Tuple

ASSEMBLY_INPUT_FIELDS: Tuple[str, ...] = (
    "assembly_input_id",
    "object_observations",
    "object_depth_hints",
    "object_spatial_states",
    "field_geometry_candidates",
    "alignment_result_ref",
    "fusion_result_ref",
    "geometry_result_ref",
)

ENHANCED_ENTITY_FIELDS: Tuple[str, ...] = (
    "entity_candidate_id",
    "field_scene_ref",
    "object_observation_ref",
    "object_depth_hint_ref",
    "object_spatial_state_ref",
    "field_geometry_ref",
    "label",
    "confidence",
    "bbox",
    "bbox_center",
    "depth_hint",
    "depth_source",
    "depth_confidence",
    "depth_error_expected",
    "pseudo_3d_position",
    "pseudo_3d_status",
    "field_zone",
    "distance_bucket",
    "geometry_confidence",
    "entity_confidence",
    "entity_status",
    "source_refs",
    "evidence_refs",
    "traceability_refs",
    "conflict_refs",
    "warning_codes",
    "missing_information",
    "fact_status",
    "candidate_only",
)

ENHANCED_SCENE_FIELDS: Tuple[str, ...] = (
    "field_scene_id",
    "field_session_ref",
    "frame_ref",
    "timestamp",
    "camera_ref",
    "user_ref",
    "field_origin",
    "field_radius_m",
    "active_zones",
    "entity_candidates",
    "geometry_candidates",
    "zone_summary",
    "scene_quality_summary",
    "depth_quality_summary",
    "geometry_quality_summary",
    "missing_information",
    "warning_summary",
    "conflict_summary",
    "readiness_for_core_pipeline",
    "source_refs",
    "evidence_refs",
    "traceability_refs",
    "non_execution_flags",
    "candidate_only",
)

ASSEMBLY_RESULT_FIELDS: Tuple[str, ...] = (
    "assembly_result_id",
    "input_alignment_result_ref",
    "input_fusion_result_ref",
    "input_geometry_result_ref",
    "enhanced_field_scene_candidate",
    "enhanced_entity_candidates",
    "accepted_entity_count",
    "rejected_entity_count",
    "geometry_enhanced_count",
    "geometry_unknown_count",
    "zone_summary",
    "warning_summary",
    "conflict_summary",
    "missing_information",
    "readiness_for_field_first_core",
    "readiness_for_real_model_success_path",
    "non_execution_flags",
    "candidate_only",
)

DRYRUN_RESULT_FIELDS: Tuple[str, ...] = (
    "case_id",
    "expected_entity_count",
    "actual_entity_count",
    "expected_rejected_count",
    "actual_rejected_count",
    "prohibited_behavior_absent",
    "case_passed",
    "reason_codes",
)

ENTITY_STATUSES: Tuple[str, ...] = (
    "entity_geometry_enhanced",
    "entity_2d_only",
    "entity_geometry_unknown",
    "entity_degraded",
    "entity_rejected",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_depth_inference": True,
    "no_runtime_execution": True,
    "no_field_simulation": True,
    "no_scene_relation_generation": True,
    "no_scene_graph_runtime": True,
    "no_slam_runtime": True,
    "no_task_execution": True,
    "no_large_dependency_install": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_FIELD_ASSEMBLY_SKELETON_READY_FOR_YOLO_DEPTH_REAL_FIELD_ASSEMBLY_DRYRUN_PLANNING"
)

DEFAULT_FIELD_RADIUS_M = 20.0
