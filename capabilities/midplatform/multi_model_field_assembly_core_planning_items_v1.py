# -*- coding: utf-8 -*-
"""Multi-Model Field Assembly Core Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Multi-Model-Alignment-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Multi-Model Alignment Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "model_download", "weight_download", "large_dependency_install",
        "depth_anything_v2_execution", "unidepth_execution", "slam_runtime",
        "scene_graph_runtime", "real_multi_model_runtime", "field_simulation",
        "detector_replanning", "single_depth_only_route", "task_execution",
        "world_model_entry", "memory_candidate", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_model_download",
    "multi_model_planning_not_single_depth_ingestion",
    "field_assembly_not_world_model_fact",
    "interaction_policy_not_production_runtime",
    "alignment_not_detector_replanning",
)

MULTI_MODEL_ROLE_REGISTRY: Dict[str, Any] = {
    "registry_id": "multi_model_role_registry_v1",
    "route_correction": "shift_from_single_model_sequence_to_multi_model_field_assembly",
    "prior_detector_status": "yolo_object_observation_candidate_ingestion_go",
    "prior_depth_status": "depth_observation_candidate_ingestion_skeleton_go",
    "roles": (
        {
            "tier": "P0",
            "model_id": "detector_yolo",
            "role": "object_discovery",
            "outputs": ("bbox", "label", "confidence", "frame_ref", "timestamp", "model_ref"),
            "maps_to": ("ObjectObservationCandidate",),
            "primary_input": True,
        },
        {
            "tier": "P0",
            "model_id": "depth_model",
            "role": "coarse_depth",
            "outputs": ("depth_map_ref", "depth_value_unit", "global_depth_confidence", "object_depth_hint", "depth_bucket"),
            "maps_to": ("DepthObservationCandidate", "ObjectDepthHintCandidate"),
            "auxiliary_to": "detector_yolo",
        },
        {
            "tier": "P0",
            "model_id": "geometry_builder",
            "role": "spatial_state_from_2d_plus_depth",
            "outputs": ("pseudo_3d_position", "distance_bucket", "field_zone", "object_spatial_state", "geometry_confidence"),
            "maps_to": ("FieldGeometryCandidate", "ObjectSpatialStateCandidate"),
            "depends_on": ("detector_yolo", "depth_model"),
        },
        {
            "tier": "P1",
            "model_id": "tracking_bytetrack",
            "role": "short_term_continuity",
            "outputs": ("tracker_hint_id", "movement_hint", "short_term_continuity"),
            "maps_to": ("DynamicTargetTrackCandidate",),
            "future": True,
        },
        {
            "tier": "P1",
            "model_id": "ocr",
            "role": "text_region_recognition",
            "outputs": ("text_region", "recognized_text", "reading_order", "confidence"),
            "maps_to": ("TextObservationCandidate", "TextRegionCandidate"),
            "future": True,
        },
        {
            "tier": "P1",
            "model_id": "segmentation_sam",
            "role": "mask_and_boundary",
            "outputs": ("mask_ref", "segmentation_confidence", "object_boundary"),
            "maps_to": ("MaskObservationCandidate", "ObjectBoundaryCandidate"),
            "future": True,
        },
        {
            "tier": "P2",
            "model_id": "slam_reconstruction",
            "role": "pose_and_spatial_continuity",
            "outputs": ("camera_pose", "local_map", "point_cloud"),
            "maps_to": ("PoseObservationCandidate", "SceneGeometryCandidate", "SpatialAnchorCandidate"),
            "future_review": True,
        },
        {
            "tier": "P2",
            "model_id": "scene_graph",
            "role": "object_relation_topology",
            "outputs": ("object_node", "relation_edge"),
            "maps_to": ("SceneRelationCandidate", "FieldRelationCandidate"),
            "future_review": True,
        },
    ),
}

MULTI_MODEL_INTERACTION_POLICY: Dict[str, Any] = {
    "policy_id": "multi_model_interaction_policy_v1",
    "core_question": "how_models_interact_to_assemble_field",
    "interaction_stages": (
        "frame_time_alignment",
        "object_depth_linking",
        "object_geometry_linking",
        "confidence_fusion",
        "conflict_handling",
        "missing_model_fallback",
        "field_entity_assembly",
        "field_geometry_assembly",
        "field_scene_enhancement",
    ),
    "primary_inputs": ("ObjectObservationCandidate",),
    "auxiliary_inputs": ("DepthObservationCandidate", "ObjectDepthHintCandidate"),
    "assembly_outputs": ("FieldEntityCandidate", "FieldGeometryCandidate", "FieldSceneCandidate"),
    "candidate_only": True,
}

MULTI_MODEL_ALIGNMENT_POLICY: Dict[str, Any] = {
    "policy_id": "multi_model_alignment_policy_v1",
    "alignment_keys": ("frame_ref", "timestamp", "camera_ref", "frame_width", "frame_height"),
    "rules": (
        {"condition": "same_frame_ref", "status": "strong_alignment", "confidence": "high"},
        {"condition": "timestamp_delta_small", "status": "weak_alignment", "confidence": "medium"},
        {"condition": "frame_ref_mismatch_and_large_timestamp_delta", "status": "reject_alignment", "action": "reject_fusion"},
        {"condition": "missing_frame_ref", "status": "fallback_alignment", "confidence": "low"},
    ),
    "timestamp_gap_threshold_sec": 1.0,
    "timestamp_gap_action": "warning_and_confidence_downgrade",
    "frame_ref_mismatch_action": "reject_alignment",
}

OBJECT_DEPTH_LINKING_POLICY: Dict[str, Any] = {
    "policy_id": "object_depth_linking_policy_v1",
    "link_method_primary": "bbox_center_median_sampling",
    "link_method_reserved": ("bbox_center_mean_sampling", "bbox_area_sampling", "mask_area_sampling"),
    "input": ("ObjectObservationCandidate", "DepthObservationCandidate"),
    "output": "ObjectDepthHintCandidate",
    "rules": (
        "frame_ref_must_match",
        "bbox_center_samples_depth_map",
        "depth_missing_yields_unknown_hint_not_drop_object",
        "depth_unreliable_downgrades_confidence",
    ),
}

CONFIDENCE_FUSION_POLICY: Dict[str, Any] = {
    "policy_id": "confidence_fusion_policy_v1",
    "sources": ("detector_confidence", "depth_confidence", "geometry_confidence", "alignment_confidence"),
    "outputs": ("field_entity_confidence", "field_geometry_confidence"),
    "rules": (
        "any_key_source_unknown_blocks_high_confidence",
        "estimated_depth_requires_depth_error_expected_true",
        "confidence_fusion_is_candidate_not_fact",
        "relative_depth_caps_geometry_confidence",
    ),
    "fusion_method": "conservative_min_of_key_sources",
}

CONFLICT_HANDLING_POLICY: Dict[str, Any] = {
    "policy_id": "conflict_handling_policy_v1",
    "conflict_types": (
        "frame_mismatch", "timestamp_mismatch", "bbox_depth_mismatch",
        "label_conflict", "depth_unreliable", "geometry_out_of_range", "duplicate_object_conflict",
    ),
    "outputs": ("conflict_refs", "warning_codes", "missing_information", "degradation_reason_codes"),
    "rules": (
        "frame_mismatch_rejects_fusion",
        "duplicate_objects_not_merged_by_default",
        "conflicts_recorded_not_silent_drop",
    ),
}

MISSING_MODEL_FALLBACK_POLICY: Dict[str, Any] = {
    "policy_id": "missing_model_fallback_policy_v1",
    "when_depth_missing": {
        "retain_object_observation": True,
        "field_entity_generatable": True,
        "field_geometry": "degraded_or_unknown",
        "field_zone": "unknown_or_weak_estimated",
        "pseudo_3d_position": "pseudo_3d_unknown",
    },
    "when_detector_missing": {
        "depth_alone_no_field_entity": True,
        "depth_as_background_evidence": True,
    },
    "when_geometry_missing": {
        "output_2d_field_scene_only": True,
        "no_pseudo_3d": True,
    },
    "prohibited": ("silent_drop_object_on_missing_depth", "depth_alone_creates_entity"),
}

FIELD_GEOMETRY_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_geometry_candidate_contract_v1",
    "required_fields": (
        "geometry_candidate_id", "object_observation_ref", "bbox", "bbox_center",
        "pseudo_3d_position", "distance_bucket", "field_zone", "geometry_confidence",
        "depth_error_expected", "source_refs", "evidence_refs", "candidate_only",
    ),
    "optional_fields": ("object_depth_hint_ref", "depth_hint", "geometry_reliability_reasons"),
    "pseudo_3d_status_values": ("estimated", "pseudo_3d_unknown"),
    "field_zones": ("inner_zone", "working_zone", "forecast_zone", "unknown"),
    "distance_buckets": ("near", "middle", "far", "unknown"),
    "rules": (
        "valid_depth_generates_pseudo_3d",
        "estimated_depth_geometry_confidence_not_high",
        "depth_unknown_pseudo_3d_unknown",
        "invalid_bbox_no_geometry_candidate",
    ),
    "candidate_only": True,
}

MULTI_MODEL_ALIGNED_OBSERVATION_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "multi_model_aligned_observation_candidate_contract_v1",
    "required_fields": (
        "aligned_candidate_id", "frame_ref", "timestamp", "object_observation_ref",
        "alignment_status", "alignment_confidence", "missing_model_outputs",
        "source_refs", "evidence_refs", "candidate_only",
    ),
    "optional_fields": (
        "depth_observation_ref", "object_depth_hint_ref", "geometry_candidate_ref",
        "conflict_refs", "warning_codes",
    ),
    "alignment_status_values": ("strong", "weak", "rejected", "fallback"),
    "candidate_only": True,
}

FIELD_ASSEMBLY_RESULT_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_assembly_result_candidate_contract_v1",
    "required_fields": (
        "assembly_result_id", "aligned_candidates", "field_entity_candidates",
        "field_geometry_candidates", "field_scene_candidate", "missing_information",
        "conflict_summary", "warning_summary", "readiness_for_field_first_core",
        "candidate_only",
    ),
    "optional_fields": ("degradation_summary", "input_model_outputs", "fused_entity_candidates"),
    "candidate_only": True,
}

FIELD_ASSEMBLY_PLAN: Dict[str, Any] = {
    "plan_id": "field_assembly_plan_v1",
    "core_question": "how_multi_model_outputs_assemble_into_field",
    "inputs": (
        "ObjectObservationCandidate", "DepthObservationCandidate", "ObjectDepthHintCandidate",
        "FieldGeometryCandidate", "MaskObservationCandidate", "TrackCandidate", "TextObservationCandidate",
    ),
    "outputs": (
        "FieldEntityCandidate", "FieldGeometryCandidate", "FieldSceneCandidate", "FieldAssemblyResultCandidate",
    ),
    "assembly_stages": (
        "align_observations",
        "fuse_object_depth",
        "build_geometry_candidates",
        "assemble_field_entities",
        "assemble_field_scene",
        "summarize_conflicts_and_degradations",
    ),
    "field_entity_from": ("ObjectObservationCandidate", "ObjectDepthHintCandidate"),
    "field_geometry_from": ("ObjectObservationCandidate", "ObjectDepthHintCandidate", "FieldGeometryCandidate"),
    "field_scene_from": ("FieldEntityCandidate", "FieldGeometryCandidate"),
    "traceability_required": True,
    "candidate_only": True,
}

NEXT_IMPLEMENTATION_SEQUENCE: Dict[str, Any] = {
    "sequence_id": "next_implementation_sequence_v1",
    "route_correction": "multi_model_field_assembly_before_single_model_dryrun",
    "sequence": (
        {"order": 1, "phase": "Multi-Model Alignment Skeleton", "focus": "YOLO object + depth output alignment"},
        {"order": 2, "phase": "Depth + Object Fusion Skeleton", "focus": "ObjectDepthHintCandidate + confidence degradation"},
        {"order": 3, "phase": "Field Geometry Candidate Skeleton", "focus": "bbox + depth → pseudo_3d / field_zone"},
        {"order": 4, "phase": "Field Assembly Skeleton", "focus": "multi-model → FieldSceneCandidate"},
        {"order": 5, "phase": "YOLO + Depth Real Field Assembly DryRun", "focus": "real multi-model field assembly dryrun"},
    ),
    "deferred": (
        "single_depth_only_dryrun",
        "detector_replanning",
        "slam_production_integration",
        "scene_graph_production_integration",
    ),
}

PLANNING_RULES: Tuple[Dict[str, str], ...] = (
    {"rule_id": "multi_model_not_single_depth", "desc": "core is multi-model interaction not isolated depth"},
    {"rule_id": "field_assembly_core", "desc": "outputs assemble into FieldSceneCandidate not isolated candidates"},
    {"rule_id": "detector_already_go", "desc": "YOLO/detector ingestion complete, no repeat planning"},
    {"rule_id": "depth_auxiliary_not_primary", "desc": "depth enhances detector objects, not standalone entity source"},
    {"rule_id": "geometry_from_object_plus_depth", "desc": "geometry requires object + depth interaction"},
    {"rule_id": "confidence_fusion_candidate", "desc": "fused confidence is candidate not fact"},
    {"rule_id": "conflict_recorded", "desc": "model conflicts recorded in conflict_summary"},
    {"rule_id": "missing_depth_keeps_object", "desc": "missing depth retains object, degrades geometry"},
    {"rule_id": "depth_without_object_no_entity", "desc": "depth alone does not create FieldEntity"},
    {"rule_id": "no_weight_download", "desc": "planning only, no model download"},
)

MOCK_PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "yolo_object_depth_aligned", "input": "same_frame_yolo_and_depth", "expected": "strong_alignment", "pass_condition": "aligned_observation"},
    {"case_id": "frame_ref_mismatch_rejected", "input": "frame_0_yolo_frame_1_depth", "expected": "reject_fusion", "pass_condition": "alignment_rejected"},
    {"case_id": "timestamp_gap_degraded", "input": "small_timestamp_delta", "expected": "weak_alignment", "pass_condition": "confidence_downgraded"},
    {"case_id": "missing_depth_keeps_object", "input": "yolo_only_no_depth", "expected": "object_retained_geometry_unknown", "pass_condition": "entity_without_geometry"},
    {"case_id": "depth_without_object_no_entity", "input": "depth_only_no_detector", "expected": "no_field_entity", "pass_condition": "depth_background_only"},
    {"case_id": "valid_depth_generates_geometry", "input": "bbox_plus_depth_hint", "expected": "pseudo_3d_and_field_zone", "pass_condition": "geometry_candidate"},
    {"case_id": "estimated_depth_confidence_not_high", "input": "estimated_depth", "expected": "geometry_confidence_not_high", "pass_condition": "depth_error_expected"},
    {"case_id": "depth_unreliable_degrades_geometry", "input": "low_depth_confidence", "expected": "geometry_degraded", "pass_condition": "degradation_reason"},
    {"case_id": "duplicate_objects_not_merged_by_default", "input": "two_same_label_bboxes", "expected": "two_entities", "pass_condition": "no_auto_merge"},
    {"case_id": "field_scene_assembly_with_multiple_objects", "input": "multi_object_aligned", "expected": "field_scene_with_entities", "pass_condition": "field_scene_candidate"},
    {"case_id": "conflict_summary_generated", "input": "frame_mismatch_case", "expected": "conflict_refs_populated", "pass_condition": "conflict_summary"},
    {"case_id": "readiness_for_core_pipeline_true", "input": "valid_entity_plus_geometry", "expected": "readiness_true", "pass_condition": "field_first_core_ready"},
)
