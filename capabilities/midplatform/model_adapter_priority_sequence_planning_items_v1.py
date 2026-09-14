# -*- coding: utf-8 -*-
"""Model adapter priority sequence planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-SLAM-Spatial-Mapping-Model-Adapter-Smoke-IO-Inspection-v1-001"
SELECTED_NEXT_ROUTE = "SLAM Spatial Mapping Model Smoke IO Inspection"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "field_simulation", "simulation_test_route", "task_reasoning_execution",
        "task_action_output", "world_model_entry_write", "fact_admission",
        "new_protocol_without_reason", "model_runtime", "unauthorized_model_download",
        "camera_runtime", "video_stream_runtime", "production_runtime",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "priority_planning_not_adapter_implementation",
    "candidate_definition_not_new_protocol",
    "world_model_candidate_not_world_model_entry",
    "task_evidence_not_task_action",
)

MODEL_ADAPTER_PRIORITY_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "adapter_id": "slam_spatial_mapping",
        "priority": "P0",
        "status": "next_to_implement",
        "owner_authorization_required": True,
        "reason": "world_model_spatial_skeleton_camera_pose_local_map_anchor",
    },
    {
        "adapter_id": "tracking_optical_flow",
        "priority": "P1",
        "status": "planned",
        "owner_authorization_required": False,
        "reason": "object_persistence_motion_dynamic_tasks",
    },
    {
        "adapter_id": "ocr_text_model",
        "priority": "P2",
        "status": "planned",
        "owner_authorization_required": True,
        "reason": "text_anchor_sign_storefront_floor",
    },
    {
        "adapter_id": "segmentation_grounded_mask",
        "priority": "P3",
        "status": "planned",
        "owner_authorization_required": True,
        "reason": "boundary_freespace_passability",
    },
    {
        "adapter_id": "scene_graph_relation",
        "priority": "P4",
        "status": "deferred",
        "owner_authorization_required": True,
        "reason": "depends_on_stable_object_geometry_anchor_map",
    },
)

REUSE_PATH_REGISTRY: Tuple[Dict[str, Any], ...] = (
    {
        "adapter_id": "slam_spatial_mapping",
        "reuse_packages": (
            "RealFrameInputPackage", "EnhancedFieldSceneCandidate", "FieldGeometryCandidate",
        ),
        "reuse_patterns": (
            "source_refs", "evidence_refs", "traceability_refs", "candidate_only_boundary",
            "authorization_boundary", "real_model_execution_path_hardening_pattern",
        ),
        "new_candidate_definitions_only": (
            "CameraPoseCandidate", "CameraTrajectoryCandidate", "SpatialAnchorCandidate",
            "LocalMapCandidate", "MapQualityCandidate",
        ),
        "new_protocol_required": False,
    },
    {
        "adapter_id": "tracking_optical_flow",
        "reuse_packages": (
            "ObjectObservationCandidate", "MultiModelAlignedObservationCandidate",
            "FieldGeometryCandidate", "EnhancedFieldEntityCandidate",
        ),
        "reuse_patterns": ("conflict_resolution_pattern", "missing_information_pattern"),
        "new_candidate_definitions_only": (
            "ObjectTrackCandidate", "ObjectPersistenceCandidate", "MotionCandidate",
        ),
        "new_protocol_required": False,
    },
    {
        "adapter_id": "ocr_text_model",
        "reuse_packages": (
            "RealFrameInputPackage", "ObjectObservationCandidate", "EnhancedFieldSceneCandidate",
        ),
        "reuse_patterns": ("source_refs", "evidence_refs", "traceability_refs", "candidate_only_boundary"),
        "new_candidate_definitions_only": (
            "TextObservationCandidate", "TextRegionCandidate", "TextAnchorCandidate",
        ),
        "new_protocol_required": False,
    },
    {
        "adapter_id": "segmentation_grounded_mask",
        "reuse_packages": (
            "ObjectObservationCandidate", "FieldGeometryCandidate", "EnhancedFieldSceneCandidate",
        ),
        "reuse_patterns": ("candidate_only_boundary",),
        "new_candidate_definitions_only": (
            "MaskObservationCandidate", "ObjectBoundaryCandidate", "FreeSpaceCandidate",
        ),
        "new_protocol_required": False,
    },
    {
        "adapter_id": "scene_graph_relation",
        "reuse_packages": ("EnhancedFieldEntityCandidate", "WorldGeometryCandidate"),
        "reuse_patterns": ("candidate_only_boundary",),
        "new_candidate_definitions_only": ("SceneRelationCandidate", "WorldRelationCandidate"),
        "new_protocol_required": False,
        "implementation_deferred": True,
    },
)

WORLD_MODEL_CONSTRUCTION_MAPPING: Tuple[Dict[str, Any], ...] = (
    {"model": "YOLO_Detector", "input": "ObjectObservationCandidate", "output": "WorldEntityCandidate source", "status": "integrated"},
    {"model": "Depth_Geometry", "input": "ObjectDepthHintCandidate", "output": "WorldGeometryCandidate source", "status": "integrated"},
    {"model": "SLAM_Spatial_Mapping", "input": "CameraPoseCandidate", "output": "WorldModelCandidate spatial skeleton", "status": "P0_planned"},
    {"model": "Tracking", "input": "ObjectPersistenceCandidate", "output": "WorldEntityCandidate identity continuity", "status": "P1_planned"},
    {"model": "OCR", "input": "TextAnchorCandidate", "output": "WorldEntityCandidate semantic anchor", "status": "P2_planned"},
    {"model": "Segmentation", "input": "FreeSpaceCandidate", "output": "WorldGeometryCandidate boundary evidence", "status": "P3_planned"},
    {"model": "Scene_Graph", "input": "WorldRelationCandidate", "output": "deferred", "status": "P4_deferred"},
)

TASK_COLLABORATION_MAPPING: Tuple[Dict[str, Any], ...] = (
    {
        "scenario_id": "navigation_passability",
        "models": ("YOLO", "Depth_Geometry", "Segmentation_optional"),
        "outputs": ("PassabilityEvidenceCandidate", "ObstacleCandidate", "RouteRiskCandidate"),
    },
    {
        "scenario_id": "find_object",
        "models": ("YOLO", "Tracking", "Depth_optional"),
        "outputs": ("TargetObjectCandidate", "ObjectLocationCandidate", "FindObjectEvidenceCandidate"),
    },
    {
        "scenario_id": "road_crossing_safety",
        "models": ("YOLO", "Depth", "Tracking"),
        "outputs": ("MovingObjectCandidate", "CrossingRiskCandidate", "SafetyRiskCandidate"),
    },
    {
        "scenario_id": "read_sign_or_storefront",
        "models": ("YOLO", "OCR", "SpatialAnchor_optional"),
        "outputs": ("TextObservationCandidate", "StorefrontCandidate", "TextAnchorCandidate"),
    },
    {
        "scenario_id": "field_construction",
        "models": ("YOLO", "Depth", "SLAM_Spatial_Mapping"),
        "outputs": ("EnhancedFieldSceneCandidate", "LocalMapCandidate", "WorldModelCandidate"),
    },
    {
        "scenario_id": "indoor_navigation",
        "models": ("YOLO", "OCR", "SLAM_Spatial_Mapping"),
        "outputs": ("DoorCandidate", "ElevatorCandidate", "FloorSignCandidate", "IndoorSpatialAnchorCandidate"),
    },
)

SCENARIO_MODEL_GROUPS: Tuple[Dict[str, Any], ...] = TASK_COLLABORATION_MAPPING

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "model_adapter_protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "new_protocol_count": 0,
    "reuse_existing_candidates": True,
    "reuse_source_evidence_traceability_refs": True,
    "reuse_authorization_boundary": True,
    "reuse_candidate_only_boundary": True,
    "candidate_definitions_are_not_protocols": True,
    "owner_approval_required_for_new_protocol": True,
}

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "model_adapter_new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "reason_required_for_any_new_protocol": True,
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

DEFERRED_ADAPTERS: Tuple[Dict[str, Any], ...] = (
    {"adapter_id": "scene_graph_relation", "priority": "P4", "reason": "depends_on_stable_object_geometry_tracking_anchor"},
)

NEXT_SKELETON_RECOMMENDATION: Dict[str, Any] = {
    "recommendation_id": "next_model_adapter_skeleton_recommendation_v1",
    "recommended_adapter": "slam_spatial_mapping",
    "recommended_phase": SELECTED_NEXT_PHASE,
    "recommended_route": SELECTED_NEXT_ROUTE,
    "onboarding_rule": "model_smoke_io_inspection_before_adapter_skeleton",
    "candidate_outputs": (
        "CameraPoseCandidate", "CameraTrajectoryCandidate", "SpatialAnchorCandidate",
        "LocalMapCandidate", "MapQualityCandidate",
    ),
    "constraints": {
        "reuse_existing_io_boundary": True,
        "no_new_protocol_without_reason": True,
        "no_real_slam_runtime": True,
        "no_model_download": True,
        "candidate_only": True,
        "serve_world_model_and_task_collaboration": True,
    },
}

PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "slam_priority_for_world_skeleton", "expect_priority": "P0", "adapter": "slam_spatial_mapping"},
    {"case_id": "tracking_priority_for_object_persistence", "expect_priority": "P1", "adapter": "tracking_optical_flow"},
    {"case_id": "ocr_priority_for_text_anchor", "expect_priority": "P2", "adapter": "ocr_text_model"},
    {"case_id": "segmentation_priority_for_boundary_passability", "expect_priority": "P3", "adapter": "segmentation_grounded_mask"},
    {"case_id": "scene_graph_deferred", "expect_status": "deferred", "adapter": "scene_graph_relation"},
    {"case_id": "field_construction_uses_yolo_depth_slam", "scenario": "field_construction", "models": ("YOLO", "Depth", "SLAM_Spatial_Mapping")},
    {"case_id": "road_crossing_uses_yolo_depth_tracking", "scenario": "road_crossing_safety", "models": ("YOLO", "Depth", "Tracking")},
    {"case_id": "read_sign_uses_yolo_ocr_spatial_anchor", "scenario": "read_sign_or_storefront", "models": ("YOLO", "OCR", "SpatialAnchor_optional")},
    {"case_id": "no_new_protocol_without_reason", "expect_new_protocol": False},
    {"case_id": "simulation_not_next_phase", "forbidden_in_next": "Field-Simulation"},
    {"case_id": "task_reasoning_not_next_phase", "forbidden_in_next": "Task-Reasoning"},
    {"case_id": "adapter_sequence_respects_cleanup_review", "inherit_cleanup": True},
)
