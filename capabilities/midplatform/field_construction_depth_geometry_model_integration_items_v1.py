# -*- coding: utf-8 -*-
"""Field Construction Depth / Geometry Model Integration Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

# --- Priority tiers ---

P0_DEPTH_MODELS: Tuple[str, ...] = (
    "depth_anything_v2",
    "unidepth",
    "unidepth_v2",
    "metric3d_reference",
)

P1_FIELD_GEOMETRY: Tuple[str, ...] = (
    "field_geometry_adapter",
    "pseudo_3d_position_builder",
    "field_zone_assigner",
    "distance_bucket_classifier",
)

P2_SLAM_CANDIDATES: Tuple[str, ...] = (
    "lingbot_map",
    "mast3r_slam",
    "orb_slam3",
    "pyslam",
)

P3_SCENE_GRAPH_CANDIDATES: Tuple[str, ...] = (
    "hydra",
    "hov_sg",
    "concept_graphs",
    "open3dsg",
)

P2_DEFERRED: Tuple[str, ...] = P2_SLAM_CANDIDATES + P3_SCENE_GRAPH_CANDIDATES + (
    "field_simulation", "full_slam_production", "full_scene_graph_production",
)

# --- Core plans / contracts ---

DEPTH_MODEL_ADAPTER_PLAN: Dict[str, Any] = {
    "adapter_id": "depth_model_adapter_plan_v1",
    "role": "field_construction_depth_source_not_detector",
    "near_term_primary": "depth_anything_v2",
    "near_term_alternatives": ("unidepth", "unidepth_v2"),
    "reference_candidates": ("metric3d_reference",),
    "maps_to_candidate_types": ("DepthObservationCandidate", "ObjectDepthHintCandidate"),
    "candidate_only": True,
    "input_contract": (
        "frame_ref", "image_ref", "timestamp", "frame_width", "frame_height",
        "camera_ref", "source_ref",
    ),
    "output_contract": (
        "depth_observation_id", "depth_map_ref", "depth_source", "depth_confidence",
        "depth_error_expected", "frame_ref", "timestamp", "candidate_only",
    ),
    "alignment_with_yolo": (
        "same_frame_ref", "same_timestamp", "same_frame_width_height",
    ),
    "non_execution_boundary": {
        "no_weight_download": True,
        "no_production_inference": True,
        "candidate_only": True,
    },
    "download_authorization_status": "pending_owner_authorization",
}

DEPTH_OBSERVATION_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "depth_observation_candidate_contract_v1",
    "candidate_type": "DepthObservationCandidate",
    "required_fields": (
        "depth_observation_id", "frame_ref", "timestamp", "depth_source",
        "depth_confidence", "depth_error_expected", "candidate_only",
    ),
    "optional_fields": (
        "depth_map_ref", "depth_map_format", "camera_ref", "model_ref",
        "source_refs", "evidence_refs", "traceability_refs", "warning_codes",
    ),
    "depth_source_values": ("estimated", "hardware", "unknown"),
    "depth_confidence_values": ("high", "medium", "low", "unknown"),
    "defaults": {
        "depth_source": "estimated",
        "depth_confidence": "low",
        "depth_error_expected": True,
        "candidate_only": True,
    },
    "not_hardware_fact": True,
}

OBJECT_DEPTH_HINT_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "object_depth_hint_candidate_contract_v1",
    "candidate_type": "ObjectDepthHintCandidate",
    "required_fields": (
        "depth_hint_id", "observation_ref", "frame_ref", "timestamp",
        "object_depth_hint", "depth_source", "depth_confidence",
        "depth_error_expected", "candidate_only",
    ),
    "optional_fields": (
        "bbox_ref", "depth_sample_method", "model_ref", "source_refs",
        "warning_codes", "missing_information",
    ),
    "depth_sample_methods": (
        "bbox_center_median", "bbox_center_mean", "bbox_region_median",
    ),
    "defaults": {
        "depth_source": "estimated",
        "depth_confidence": "low",
        "depth_error_expected": True,
        "candidate_only": True,
    },
    "fusion_input": ("ObjectObservationCandidate", "DepthObservationCandidate"),
}

FIELD_GEOMETRY_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "field_geometry_candidate_contract_v1",
    "candidate_types": (
        "FieldGeometryCandidate", "ObjectSpatialStateCandidate", "SpatialAnchorCandidate",
    ),
    "field_geometry_required": (
        "geometry_id", "frame_ref", "timestamp", "pseudo_3d_position",
        "field_zone", "distance_bucket", "candidate_only",
    ),
    "object_spatial_state_required": (
        "spatial_state_id", "observation_ref", "pseudo_3d_position",
        "field_zone", "distance_bucket", "depth_source", "depth_confidence",
        "depth_error_expected", "candidate_only",
    ),
    "spatial_anchor_required": (
        "anchor_id", "frame_ref", "anchor_type", "pseudo_3d_position", "candidate_only",
    ),
    "field_zones": ("inner_zone", "working_zone", "forecast_zone", "unknown"),
    "distance_buckets": ("near", "middle", "far", "unknown"),
    "pseudo_3d_status_values": ("estimated", "pseudo_3d_unknown"),
    "candidate_only": True,
}

YOLO_DEPTH_FUSION_MAPPING: Dict[str, Any] = {
    "mapping_id": "yolo_depth_fusion_mapping_v1",
    "source_types": ("ObjectObservationCandidate", "DepthObservationCandidate"),
    "target_types": ("ObjectDepthHintCandidate", "ObjectSpatialStateCandidate"),
    "alignment_keys": ("frame_ref", "timestamp", "frame_width", "frame_height"),
    "field_mappings": (
        {"yolo": "bbox", "depth": "depth_map_ref", "fusion": "object_depth_hint"},
        {"yolo": "observation_id", "depth": "depth_observation_id", "fusion": "observation_ref"},
        {"yolo": "label", "fusion": "entity_type_hint"},
        {"yolo": "confidence", "fusion": "detection_confidence_preserved"},
        {"depth": "depth_source", "fusion": "depth_source"},
        {"depth": "depth_confidence", "fusion": "depth_confidence"},
    ),
    "bbox_to_depth_hint": {
        "method": "bbox_center_median_on_depth_map",
        "fallback": "bbox_center_mean",
        "invalid_depth_values": ("nan", "inf", "zero", "out_of_range"),
    },
    "pseudo_3d_derivation": {
        "x": "bbox_center_x",
        "y": "bbox_center_y",
        "z": "object_depth_hint",
        "status": "estimated_when_depth_present_else_pseudo_3d_unknown",
    },
    "field_zone_derivation": {
        "near": "distance_bucket_near",
        "middle": "distance_bucket_middle",
        "far": "distance_bucket_far",
        "unknown": "depth_missing_or_unreliable",
    },
    "candidate_only": True,
}

SPATIAL_RELATION_CANDIDATE_CONTRACT: Dict[str, Any] = {
    "contract_id": "spatial_relation_candidate_contract_v1",
    "candidate_type": "SceneRelationCandidate",
    "required_fields": (
        "relation_id", "subject_entity_ref", "object_entity_ref",
        "relation_type", "confidence", "candidate_only",
    ),
    "optional_fields": (
        "spatial_predicate", "distance_hint", "direction_hint",
        "observed_vs_inferred", "source_refs", "warning_codes",
    ),
    "relation_types": (
        "near", "far", "left_of", "right_of", "above", "below",
        "in_front_of", "behind", "inside_zone", "unknown",
    ),
    "observed_vs_inferred_policy": "explicit_mark_inferred_not_fact",
    "dependency": "requires_pseudo_3d_or_field_geometry_first",
    "near_term_status": "future_review_p3_not_first_batch",
    "candidate_only": True,
}

FIELD_CONSTRUCTION_MODEL_PRIORITY_PLAN: Dict[str, Any] = {
    "priority_plan_id": "field_construction_model_priority_plan_v1",
    "route_correction": "detector_ingestion_complete_shift_to_field_construction",
    "prior_detector_status": "yolo_observation_candidate_ingestion_skeleton_go",
    "no_repeat_detector_planning": True,
    "priority_order": (
        {"tier": "P0", "focus": "depth_model_adapter", "models": list(P0_DEPTH_MODELS)},
        {"tier": "P1", "focus": "field_geometry_adapter", "modules": list(P1_FIELD_GEOMETRY)},
        {"tier": "P2", "focus": "slam_candidate_review", "models": list(P2_SLAM_CANDIDATES), "status": "future_review_not_near_term"},
        {"tier": "P3", "focus": "scene_graph_review", "models": list(P3_SCENE_GRAPH_CANDIDATES), "status": "future_review_not_near_term"},
    ),
    "minimal_meaningful_chain": (
        "yolo_bbox",
        "depth_anything_v2_or_unidepth_depth_estimate",
        "object_depth_hint",
        "pseudo_3d_position",
        "field_zone",
        "FieldSceneCandidate_enhancement",
    ),
    "recommended_sequence": (
        "Field Construction Depth Geometry Model Integration Planning",
        "Depth Observation Candidate Ingestion Skeleton",
        "YOLO + Depth Real Field Scene DryRun",
        "Field Geometry Spatial Relation Skeleton",
        "Real-Model Field Construction Success Path",
    ),
    "candidate_only": True,
}

FIELD_GEOMETRY_ADAPTER_PLAN: Dict[str, Any] = {
    "adapter_id": "field_geometry_adapter_plan_v1",
    "role": "bbox_plus_depth_to_pseudo_3d_and_field_zone",
    "input_contract": ("ObjectObservationCandidate", "ObjectDepthHintCandidate"),
    "output_contract": (
        "FieldGeometryCandidate", "ObjectSpatialStateCandidate", "SpatialAnchorCandidate",
    ),
    "operations": (
        "bbox_center_ray_projection",
        "object_depth_hint_to_pseudo_3d",
        "field_zone_assignment",
        "distance_bucket_near_middle_far",
        "inner_working_forecast_zone_mapping",
    ),
    "field_zone_mapping": {
        "inner_zone": "near_and_task_relevant",
        "working_zone": "middle_interaction_range",
        "forecast_zone": "far_or_peripheral",
        "unknown": "depth_missing_or_unreliable",
    },
    "candidate_only": True,
}

DEPTH_UNRELIABLE_FALLBACK_POLICY: Dict[str, Any] = {
    "policy_id": "depth_unreliable_fallback_execution_policy_v1",
    "when_depth_missing": {
        "depth_source": "unknown",
        "depth_confidence": "unknown",
        "depth_error_expected": True,
        "object_depth_hint": None,
        "pseudo_3d_position": {"status": "pseudo_3d_unknown", "x": None, "y": None, "z": None},
        "field_zone": "unknown",
        "distance_bucket": "unknown",
    },
    "when_depth_unreliable": {
        "depth_source": "estimated",
        "depth_confidence": "low",
        "depth_error_expected": True,
        "object_depth_hint": "retain_with_low_confidence_warning",
        "pseudo_3d_position": "estimated_with_warning",
        "field_zone": "unknown_or_conservative",
    },
    "when_depth_estimated": {
        "depth_source": "estimated",
        "depth_confidence": "medium_or_low",
        "depth_error_expected": True,
        "not_hardware_fact": True,
        "pseudo_3d_position": "estimated",
    },
    "prohibited": (
        "treat_estimated_depth_as_hardware_fact",
        "silent_drop_no_depth",
        "upgrade_pseudo_3d_to_fact",
    ),
    "field_scene_enhancement": "FieldSceneCandidate.entities receive pseudo_3d_position and field_zone",
}

SLAM_CANDIDATE_REVIEW: Dict[str, Any] = {
    "review_id": "streaming_3d_slam_candidate_review_v1",
    "status": "future_review_not_near_term_integration",
    "candidates": (
        {
            "model_id": "lingbot_map",
            "category": "streaming_3d_reconstruction",
            "realtime_capable": "planned_review",
            "monocular_rgb": "planned_review",
            "outputs": ("camera_pose", "point_cloud", "mesh"),
            "observed_vs_inferred": "must_explicit_review",
            "edge_device_fit": "planned_review",
            "future_spatial_adapter": True,
        },
        {
            "model_id": "mast3r_slam",
            "category": "realtime_monocular_dense_slam",
            "realtime_capable": "planned_review",
            "monocular_rgb": True,
            "outputs": ("camera_pose", "dense_point_cloud", "depth"),
            "observed_vs_inferred": "must_explicit_review",
            "edge_device_fit": "planned_review",
            "future_spatial_adapter": True,
        },
        {
            "model_id": "orb_slam3",
            "category": "mature_visual_slam",
            "realtime_capable": True,
            "monocular_rgb": True,
            "outputs": ("camera_pose", "sparse_map", "multi_map"),
            "observed_vs_inferred": "must_explicit_review",
            "edge_device_fit": "moderate_review",
            "future_spatial_adapter": True,
        },
        {
            "model_id": "pyslam",
            "category": "python_slam_framework",
            "realtime_capable": "variable",
            "monocular_rgb": True,
            "outputs": ("camera_pose", "map"),
            "observed_vs_inferred": "must_explicit_review",
            "edge_device_fit": "planned_review",
            "future_spatial_adapter": True,
        },
    ),
    "integration_decision": "defer_until_depth_pseudo_3d_field_runs",
}

SCENE_GRAPH_CANDIDATE_REVIEW: Dict[str, Any] = {
    "review_id": "scene_graph_spatial_relation_review_v1",
    "status": "future_review_not_near_term_integration",
    "candidates": (
        {
            "model_id": "hydra",
            "category": "incremental_3d_scene_graph",
            "outputs": ("object_node", "relation_edge"),
            "dependencies": ("point_cloud", "slam_or_rgbd"),
            "maps_to": "SceneRelationCandidate",
            "task_planning_fit": "future",
        },
        {
            "model_id": "hov_sg",
            "category": "open_vocabulary_3d_scene_graph",
            "outputs": ("object_node", "relation_edge", "language_grounding"),
            "dependencies": ("point_cloud", "rgbd_or_slam"),
            "maps_to": "SceneRelationCandidate",
            "task_planning_fit": "future",
        },
        {
            "model_id": "concept_graphs",
            "category": "open_vocabulary_scene_graph",
            "outputs": ("object_node", "relation_edge"),
            "dependencies": ("rgbd_or_slam", "detector"),
            "maps_to": "SceneRelationCandidate",
            "task_planning_fit": "future",
        },
        {
            "model_id": "open3dsg",
            "category": "3d_scene_graph",
            "outputs": ("object_node", "relation_edge"),
            "dependencies": ("point_cloud", "slam"),
            "maps_to": "SceneRelationCandidate",
            "task_planning_fit": "future",
        },
    ),
    "integration_decision": "defer_until_field_geometry_skeleton_go",
}

FIELD_SCENE_ENHANCEMENT_PLAN: Dict[str, Any] = {
    "plan_id": "field_scene_candidate_enhancement_plan_v1",
    "target": "FieldSceneCandidate",
    "enhancement_fields": (
        "entity_candidates.pseudo_3d_position",
        "entity_candidates.field_zone",
        "entity_candidates.depth_hint",
        "entity_candidates.depth_source",
        "entity_candidates.depth_confidence",
        "entity_candidates.depth_error_expected",
        "depth_quality_summary",
    ),
    "entry_chain": (
        "ObjectObservationCandidate",
        "ObjectDepthHintCandidate",
        "ObjectSpatialStateCandidate",
        "FieldEntityCandidate",
        "FieldSceneCandidate",
    ),
    "without_depth": "field_scene_2d_only_degraded",
    "with_depth": "field_scene_coarse_3d_enhanced",
    "candidate_only": True,
}

DOWNLOAD_AUTHORIZATION_STATUS: Dict[str, Any] = {
    "status_id": "depth_model_download_authorization_status_v1",
    "weight_download": "not_authorized_in_this_phase",
    "large_dependency_install": "not_authorized_in_this_phase",
    "local_environment_check": "allowed_planning_only",
    "owner_authorization_required_for": (
        "weight_download", "pip_install_depth_anything", "pip_install_unidepth",
    ),
    "planning_only": True,
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "weight_download", "large_dependency_install", "production_depth_inference",
        "slam_runtime", "scene_graph_runtime", "field_simulation",
        "detector_replanning", "yolo_reintegration", "task_execution",
        "world_model_fact", "memory_write", "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_depth_model_download",
    "depth_adapter_plan_not_production_inference",
    "pseudo_3d_not_hardware_fact",
    "slam_review_not_slam_integration",
    "scene_graph_review_not_scene_graph_runtime",
    "detector_ingestion_already_complete_no_repeat",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Depth-Observation-Candidate-Ingestion-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Depth Observation Candidate Ingestion Skeleton"

PLANNING_RULES: Tuple[Dict[str, str], ...] = (
    {"rule_id": "detector_complete_no_repeat", "desc": "YOLO ingestion skeleton GO; no repeat detector planning"},
    {"rule_id": "p0_depth_first", "desc": "P0: depth model adapter before SLAM or scene graph"},
    {"rule_id": "yolo_depth_alignment", "desc": "YOLO bbox aligned with depth via frame_ref and timestamp"},
    {"rule_id": "bbox_to_depth_hint", "desc": "bbox center samples depth map for object_depth_hint"},
    {"rule_id": "depth_unreliable_fallback", "desc": "missing/unreliable depth degrades to unknown pseudo_3d"},
    {"rule_id": "pseudo_3d_to_field_scene", "desc": "pseudo_3d_position enters FieldSceneCandidate entity"},
    {"rule_id": "slam_future_review_only", "desc": "LingBot-Map/MASt3R-SLAM/ORB-SLAM3 review only not integration"},
    {"rule_id": "scene_graph_future_review", "desc": "Hydra/HOV-SG/ConceptGraphs review only not integration"},
    {"rule_id": "no_weight_download", "desc": "no weight download in planning phase"},
    {"rule_id": "estimated_depth_not_fact", "desc": "estimated depth never treated as hardware fact"},
)

MOCK_PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "yolo_depth_frame_alignment", "input": "yolo_bbox_plus_depth_map_same_frame", "expected": "aligned_fusion", "pass_condition": "frame_ref_timestamp_match"},
    {"case_id": "bbox_center_depth_hint", "input": "bbox_on_depth_map", "expected": "object_depth_hint", "pass_condition": "bbox_center_median"},
    {"case_id": "depth_missing_fallback_unknown", "input": "yolo_no_depth", "expected": "depth_source_unknown", "pass_condition": "pseudo_3d_unknown"},
    {"case_id": "depth_unreliable_low_confidence", "input": "noisy_depth_sample", "expected": "depth_confidence_low", "pass_condition": "warning_not_drop"},
    {"case_id": "pseudo_3d_from_bbox_depth", "input": "bbox_center_plus_depth_hint", "expected": "pseudo_3d_estimated", "pass_condition": "x_y_z_populated"},
    {"case_id": "field_zone_near_middle_far", "input": "depth_hint_buckets", "expected": "field_zone_assigned", "pass_condition": "inner_working_forecast"},
    {"case_id": "field_scene_candidate_enhanced", "input": "spatial_state_list", "expected": "FieldSceneCandidate_enhanced", "pass_condition": "pseudo_3d_on_entity"},
    {"case_id": "slam_deferred_future_review", "input": "slam_integration_request", "expected": "p2_deferred", "pass_condition": "not_near_term"},
    {"case_id": "scene_graph_deferred_future_review", "input": "scene_graph_request", "expected": "p3_deferred", "pass_condition": "not_near_term"},
    {"case_id": "no_detector_replanning", "input": "detector_planning_request", "expected": "blocked_already_go", "pass_condition": "no_repeat_detector"},
)
