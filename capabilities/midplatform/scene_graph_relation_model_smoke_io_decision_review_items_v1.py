# -*- coding: utf-8 -*-
"""Scene Graph / Relation Model smoke IO decision review — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

FINAL_DECISION_DEFERRED = "MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_REMAINS_DEFERRED"
FINAL_DECISION_READY = (
    "MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_DECISION_REVIEW_READY_FOR_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_INSPECTION"
)
FINAL_DECISION_BLOCKED = "MIDPLATFORM_SCENE_GRAPH_RELATION_MODEL_BLOCKED_PENDING_OWNER_DECISION"
VALID_FINAL_DECISIONS: Tuple[str, ...] = (
    FINAL_DECISION_DEFERRED,
    FINAL_DECISION_READY,
    FINAL_DECISION_BLOCKED,
)

SELECTED_NEXT_PHASE_READY = "Phase-Midplatform-Scene-Graph-Relation-Model-Smoke-IO-Inspection-v1-001"
SELECTED_NEXT_ROUTE_READY = "Scene Graph Relation Model Smoke IO Inspection"
SELECTED_NEXT_PHASE_DEFERRED = "Phase-Midplatform-World-Model-Assembly-Precondition-Review-v1-001"
SELECTED_NEXT_ROUTE_DEFERRED = "World Model Assembly Precondition Review"
SELECTED_NEXT_PHASE_BLOCKED = "Phase-Midplatform-Scene-Graph-Relation-Model-Owner-Decision-Hold-v1-001"
SELECTED_NEXT_ROUTE_BLOCKED = "Owner Decision Hold"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "decision_review_only": True,
    "no_scene_graph_runtime": True,
    "no_scene_graph_model_execution": True,
    "no_relation_candidate_generated": True,
    "no_world_relation_candidate_generated": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_entity_candidate_generated": True,
    "no_world_geometry_candidate_generated": True,
    "no_world_model_entry_created": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_task_reasoning_execution": True,
    "no_action_output": True,
    "no_field_simulation": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "no_new_protocol_without_reason": True,
    "no_smoke_io_inspection_execution": True,
    "no_adapter_skeleton": True,
    "no_task_collaboration_planning": True,
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "scene_graph_runtime", "scene_graph_model_execution", "scene_relation_generation",
        "world_relation_candidate_generation", "world_model_candidate_assembly",
        "world_model_entry_write", "fact_admission", "task_reasoning_execution",
        "task_action_output", "field_simulation", "model_download", "weight_download",
        "camera_runtime", "video_stream_runtime", "production_runtime",
        "new_protocol_without_reason", "smoke_io_inspection_execution",
        "adapter_skeleton", "task_collaboration_planning", "cached_output_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "decision_review_not_smoke_io_inspection",
    "decision_review_not_scene_graph_runtime",
    "deferred_not_blocked_review",
    "candidate_review_not_integration",
    "prerequisite_gap_not_fabricated_go",
    "relation_candidate_not_generated_in_review",
    "world_model_assembly_not_in_decision_review",
)

UPSTREAM_TASK_PLANNING_ARTIFACTS: Tuple[str, ...] = (
    "segmentation_mask_task_collaboration_planning_report_v1.json",
    "segmentation_mask_task_collaboration_model_group_registry_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "segmentation_mask_task_collaboration_protocol_reuse_decision_v1.json",
)

PREREQUISITE_CHAIN: Tuple[Dict[str, Any], ...] = (
    {
        "priority": "P0",
        "adapter_id": "slam_spatial_mapping",
        "default_output": "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/slam_spatial_mapping_task_collaboration_planning_v1_smoke_v0",
        "final_decision_go": "MIDPLATFORM_SLAM_SPATIAL_MAPPING_TASK_COLLABORATION_PLANNING_READY_FOR_TRACKING_OPTICAL_FLOW_MODEL_SMOKE_IO_INSPECTION",
        "pass_flag": "slam_task_collaboration_planning_pass",
        "anchor_role": "spatial_skeleton_camera_pose_local_map",
        "candidate_types": (
            "CameraPoseCandidate", "LocalMapCandidate", "SpatialAnchorCandidate",
            "FieldGeometryCandidate",
        ),
    },
    {
        "priority": "P1",
        "adapter_id": "tracking_optical_flow",
        "default_output": "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/tracking_opticalflow_task_collaboration_planning_v1_smoke_v0",
        "final_decision_go": "MIDPLATFORM_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING_READY_FOR_OCR_TEXT_MODEL_SMOKE_IO_INSPECTION",
        "pass_flag": "tracking_task_collaboration_planning_pass",
        "anchor_role": "object_persistence_motion_identity",
        "candidate_types": (
            "ObjectTrackCandidate", "ObjectPersistenceCandidate", "MotionCandidate",
        ),
    },
    {
        "priority": "P2",
        "adapter_id": "ocr_text_model",
        "default_output": "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/ocr_text_task_collaboration_planning_v1_smoke_v0",
        "final_decision_go": "MIDPLATFORM_OCR_TEXT_TASK_COLLABORATION_PLANNING_READY_FOR_SEGMENTATION_MASK_MODEL_SMOKE_IO_INSPECTION",
        "pass_flag": "ocr_text_task_collaboration_planning_pass",
        "anchor_role": "text_anchor_semantic_anchor",
        "candidate_types": (
            "TextObservationCandidate", "TextAnchorCandidate",
        ),
    },
    {
        "priority": "P3",
        "adapter_id": "segmentation_grounded_mask",
        "default_output": "/Users/luanlei/Desktop/Luna-Core/_tmp_eval_out/segmentation_mask_task_collaboration_planning_v1_smoke_v0",
        "final_decision_go": "MIDPLATFORM_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING_READY_FOR_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW",
        "pass_flag": "segmentation_mask_task_collaboration_planning_pass",
        "anchor_role": "boundary_freespace_passability",
        "candidate_types": (
            "MaskObservationCandidate", "ObjectBoundaryCandidate",
            "FreeSpaceCandidate", "RegionObservationCandidate",
            "ObjectObservationCandidate",
        ),
    },
)

INPUT_SOURCE_REVIEWS: Tuple[Dict[str, Any], ...] = (
    {
        "review_id": "object_source",
        "candidate_types": ("ObjectObservationCandidate", "EnhancedFieldEntityCandidate"),
        "upstream_sources": ("YOLO / Detector", "Field Assembly"),
        "upstream_priorities": ("P3", "field"),
        "relation_role": "object_node_anchor",
    },
    {
        "review_id": "geometry_depth_source",
        "candidate_types": ("ObjectDepthHintCandidate", "FieldGeometryCandidate"),
        "upstream_sources": ("Depth / Geometry", "SLAM"),
        "upstream_priorities": ("P0", "field"),
        "relation_role": "spatial_geometry_anchor",
    },
    {
        "review_id": "enhanced_field_source",
        "candidate_types": ("EnhancedFieldSceneCandidate",),
        "upstream_sources": ("Field Assembly",),
        "upstream_priorities": ("field", "P3"),
        "relation_role": "field_context_anchor",
    },
    {
        "review_id": "slam_spatial_source",
        "candidate_types": ("CameraPoseCandidate", "LocalMapCandidate", "SpatialAnchorCandidate"),
        "upstream_sources": ("SLAM / Spatial Mapping",),
        "upstream_priorities": ("P0",),
        "relation_role": "spatial_relation_frame",
    },
    {
        "review_id": "tracking_persistence_source",
        "candidate_types": ("ObjectTrackCandidate", "ObjectPersistenceCandidate", "MotionCandidate"),
        "upstream_sources": ("Tracking / Optical Flow",),
        "upstream_priorities": ("P1",),
        "relation_role": "dynamic_relation_anchor",
    },
    {
        "review_id": "text_anchor_source",
        "candidate_types": ("TextObservationCandidate", "TextAnchorCandidate"),
        "upstream_sources": ("OCR / Text",),
        "upstream_priorities": ("P2",),
        "relation_role": "text_object_relation_anchor",
    },
    {
        "review_id": "mask_boundary_source",
        "candidate_types": (
            "MaskObservationCandidate", "ObjectBoundaryCandidate",
            "FreeSpaceCandidate", "RegionObservationCandidate",
        ),
        "upstream_sources": ("Segmentation / Mask",),
        "upstream_priorities": ("P3",),
        "relation_role": "object_region_relation_anchor",
    },
)

SMOKE_IO_ELIGIBILITY_GATES: Tuple[Dict[str, Any], ...] = (
    {
        "gate_id": "object_source_gate",
        "required_any": ("ObjectObservationCandidate", "EnhancedFieldEntityCandidate"),
        "source_review_ids": ("object_source",),
    },
    {
        "gate_id": "geometry_spatial_source_gate",
        "required_any": (
            "FieldGeometryCandidate", "CameraPoseCandidate",
            "LocalMapCandidate", "SpatialAnchorCandidate",
        ),
        "source_review_ids": ("geometry_depth_source", "slam_spatial_source"),
    },
    {
        "gate_id": "auxiliary_relation_source_gate",
        "required_any": (
            "TextAnchorCandidate", "ObjectPersistenceCandidate",
            "RegionObservationCandidate", "ObjectBoundaryCandidate",
        ),
        "source_review_ids": ("text_anchor_source", "tracking_persistence_source", "mask_boundary_source"),
    },
    {
        "gate_id": "protocol_reuse_gate",
        "required_flags": (
            "candidate_only", "reuse_traceability_refs", "reuse_authorization_boundary",
        ),
    },
    {
        "gate_id": "no_new_protocol_gate",
        "required_flags": ("no_new_protocol_without_reason",),
    },
)

SCENE_GRAPH_CANDIDATE_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "model_id": "hydra",
        "category": "incremental_3d_scene_graph",
        "outputs": ("object_node", "relation_edge"),
        "dependencies": ("point_cloud", "slam_or_rgbd", "object_geometry_anchor"),
        "maps_to": "SceneRelationCandidate",
        "status": "reference_only_not_runtime",
    },
    {
        "model_id": "hov_sg",
        "category": "open_vocabulary_3d_scene_graph",
        "outputs": ("object_node", "relation_edge", "language_grounding"),
        "dependencies": ("point_cloud", "rgbd_or_slam", "tracking_anchor"),
        "maps_to": "SceneRelationCandidate",
        "status": "reference_only_not_runtime",
    },
    {
        "model_id": "concept_graphs",
        "category": "open_vocabulary_scene_graph",
        "outputs": ("object_node", "relation_edge"),
        "dependencies": ("rgbd_or_slam", "detector", "segmentation_boundary_optional"),
        "maps_to": "SceneRelationCandidate",
        "status": "reference_only_not_runtime",
    },
    {
        "model_id": "open3dsg",
        "category": "3d_scene_graph",
        "outputs": ("object_node", "relation_edge"),
        "dependencies": ("point_cloud", "slam", "object_geometry_anchor"),
        "maps_to": "SceneRelationCandidate",
        "status": "reference_only_not_runtime",
    },
)

DEPENDENCY_REVIEW: Dict[str, Any] = {
    "review_id": "scene_graph_relation_candidate_dependency_review_v1",
    "adapter_id": "scene_graph_relation",
    "priority": "P4",
    "prior_status": "deferred",
    "required_anchors": (
        "stable_object_geometry_anchor",
        "tracking_persistence_anchor",
        "spatial_skeleton_anchor",
        "boundary_freespace_anchor_optional",
        "text_anchor_optional",
    ),
    "required_p0_p3_task_collaboration_go": True,
    "smoke_io_allowed_only_when_prerequisite_chain_go": True,
    "world_model_assembly_not_in_scope": True,
    "scene_graph_runtime_not_in_scope": True,
    "expected_outputs_reference_only": (
        "SceneRelationCandidate", "RelationQualityCandidate",
    ),
    "world_relation_candidate_deferred": True,
}

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "scene_graph_relation_protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_object_observation_candidate": True,
    "reuse_enhanced_field_entity_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_scene_relation_candidate_schema": True,
    "reuse_relation_quality_candidate_schema": True,
    "reuse_candidate_only_boundary": True,
    "reuse_traceability_refs": True,
    "reuse_authorization_boundary": True,
    "reuse_world_relation_candidate_schema_reference_only": True,
}

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

DECISION_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "object_source_available_review", "source_review": "object_source"},
    {"case_id": "geometry_source_available_review", "source_review": "geometry_depth_source"},
    {"case_id": "text_anchor_source_available_review", "source_review": "text_anchor_source"},
    {"case_id": "mask_boundary_source_available_review", "source_review": "mask_boundary_source"},
    {"case_id": "tracking_persistence_source_available_review", "source_review": "tracking_persistence_source"},
    {"case_id": "relation_input_sufficiency_review", "expect_sufficiency_assigned": True},
    {"case_id": "no_relation_candidate_generated", "expect_no_relation": True},
    {"case_id": "no_world_model_assembly", "expect_no_wm": True},
    {"case_id": "no_new_protocol_without_reason", "expect_new_protocol": False},
    {"case_id": "smoke_io_decision_selected", "expect_gate_decision": True},
    {"case_id": "owner_constraint_compliance_review", "expect_owner_compliance": True},
)
