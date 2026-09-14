# -*- coding: utf-8 -*-
"""Segmentation / Mask task collaboration planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

FINAL_DECISION_GO = (
    "MIDPLATFORM_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING_READY_FOR_SCENE_GRAPH_RELATION_MODEL_SMOKE_IO_DECISION_REVIEW"
)
SELECTED_NEXT_PHASE = "Phase-Midplatform-Scene-Graph-Relation-Model-Smoke-IO-Decision-Review-v1-001"
SELECTED_NEXT_ROUTE = "Scene Graph Relation Model Smoke IO Decision Review"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_task_reasoning_execution": True,
    "no_action_output": True,
    "no_navigation_suggestion": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_entity_candidate_generated": True,
    "no_world_geometry_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_field_simulation": True,
    "no_real_segmentation_execution": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_production_runtime": True,
    "no_new_protocol_without_reason": True,
    "task_collaboration_planning_only": True,
    "midplatform_controlled_invocation_only": True,
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "task_reasoning_execution", "task_action_output", "navigation_suggestion",
        "world_model_candidate_assembly", "world_model_entry_write",
        "world_entity_candidate_generation", "world_geometry_candidate_generation",
        "fact_admission", "field_simulation", "real_segmentation_execution",
        "model_download", "weight_download", "camera_runtime", "video_stream_runtime",
        "production_runtime", "new_protocol_without_reason", "bypass_midplatform_invocation",
        "cached_output_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_task_reasoning_execution",
    "evidence_not_action_output",
    "task_collaboration_not_world_model_assembly",
    "segmentation_mask_outputs_task_evidence_only",
    "freespace_not_navigation_permission",
    "blocked_not_fabricated_evidence",
    "cached_output_not_real_model_run",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "segmentation_mask_task_collaboration_protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_object_observation_candidate": True,
    "reuse_multi_model_aligned_observation_candidate": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_text_region_candidate": True,
    "reuse_mask_observation_candidate": True,
    "reuse_object_boundary_candidate": True,
    "reuse_freespace_candidate": True,
    "reuse_region_observation_candidate": True,
    "reuse_mask_quality_candidate": True,
    "reuse_task_evidence_bundle_candidate_pattern": True,
    "reuse_model_invocation_control_policy": True,
    "reuse_traceability_refs": True,
    "reuse_authorization_boundary": True,
}

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

UPSTREAM_SKELETON_ARTIFACTS: Tuple[str, ...] = (
    "segmentation_mask_task_collaboration_readiness_review_v1.json",
    "segmentation_mask_later_world_model_readiness_review_v1.json",
    "protocol_reuse_decision_v1.json",
    "no_action_boundary_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "segmentation_mask_adapter_result_candidate_registry_v1.json",
)

TASK_MODEL_GROUPS: Tuple[Dict[str, Any], ...] = (
    {
        "group_id": "navigation_passability",
        "models": ("YOLO", "Depth_Geometry", "Segmentation_Mask"),
        "segmentation_inputs": (
            "RealFrameInputPackage", "ObjectObservationCandidate_optional",
            "FieldGeometryCandidate", "EnhancedFieldSceneCandidate_optional",
        ),
        "segmentation_outputs": (
            "FreeSpaceCandidate", "RegionObservationCandidate",
            "MaskObservationCandidate", "MaskQualityCandidate",
        ),
        "evidence_outputs": (
            "PassabilityRegionEvidenceCandidate", "FreeSpaceEvidenceCandidate",
            "PathRegionEvidenceCandidate", "NavigationPassabilityMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_navigation_suggestion": True,
    },
    {
        "group_id": "obstacle_avoidance_context",
        "models": ("YOLO", "Depth_Geometry", "Segmentation_Mask"),
        "segmentation_inputs": (
            "ObjectObservationCandidate", "FieldGeometryCandidate",
            "RealFrameInputPackage", "EnhancedFieldSceneCandidate_optional",
        ),
        "segmentation_outputs": (
            "ObjectBoundaryCandidate", "MaskObservationCandidate",
            "RegionObservationCandidate", "MaskQualityCandidate",
        ),
        "evidence_outputs": (
            "ObstacleBoundaryEvidenceCandidate", "ObstacleRegionEvidenceCandidate",
            "ObstacleMaskQualityEvidenceCandidate", "ObstacleAvoidanceMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_navigation_suggestion": True,
    },
    {
        "group_id": "door_area_detection",
        "models": ("YOLO", "Segmentation_Mask", "Depth_Geometry_optional"),
        "segmentation_inputs": (
            "RealFrameInputPackage", "ObjectObservationCandidate_optional",
            "FieldGeometryCandidate_optional",
        ),
        "segmentation_outputs": (
            "RegionObservationCandidate", "ObjectBoundaryCandidate",
            "FreeSpaceCandidate", "MaskQualityCandidate",
        ),
        "evidence_outputs": (
            "DoorAreaEvidenceCandidate", "DoorBoundaryEvidenceCandidate",
            "DoorPassageRegionEvidenceCandidate", "DoorAreaMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_navigation_suggestion": True,
    },
    {
        "group_id": "object_interaction_boundary",
        "models": ("YOLO", "Segmentation_Mask", "Depth_Geometry_optional"),
        "segmentation_inputs": (
            "ObjectObservationCandidate", "RealFrameInputPackage",
            "FieldGeometryCandidate_optional",
        ),
        "segmentation_outputs": (
            "ObjectBoundaryCandidate", "MaskObservationCandidate", "MaskQualityCandidate",
        ),
        "evidence_outputs": (
            "ObjectInteractionBoundaryEvidenceCandidate", "ObjectMaskEvidenceCandidate",
            "InteractionRegionMissingInformationCandidate",
        ),
        "no_action_output": True,
    },
)

INVOCATION_CONTROL_POLICY: Dict[str, Any] = {
    "policy_id": "segmentation_mask_task_invocation_control_policy_v1",
    "policy_name": "ModelInvocationControlPolicy",
    "new_protocol_added": False,
    "rules": (
        "midplatform_decides_segmentation_mask_invocation",
        "segmentation_mask_must_not_invoke_other_models",
        "task_context_ref_or_field_context_ref_required",
        "authorization_ref_required",
        "outputs_return_to_candidate_layer_only",
        "outputs_must_not_enter_decision_layer",
        "outputs_must_not_write_world_model",
        "missing_failure_low_quality_must_surface",
        "task_action_and_final_decision_deferred",
    ),
}

FAILURE_DEGRADATION_POLICY: Tuple[Dict[str, Any], ...] = (
    {"condition": "no_mask_output", "impact": "region_boundary_evidence_missing", "handling": "MissingInformationCandidate"},
    {"condition": "low_confidence_mask", "impact": "mask_unreliable", "handling": "MaskQualityCandidate_degraded"},
    {"condition": "no_object_association", "impact": "boundary_cannot_bind_object", "handling": "ObjectBoundaryCandidate_not_high_confidence"},
    {"condition": "no_geometry_ref", "impact": "freespace_not_strong_passability_evidence", "handling": "FreeSpaceCandidate_degraded"},
    {"condition": "prompt_dependency_risk_high", "impact": "mask_unstable_prompt_dependent", "handling": "MaskQualityCandidate_degraded"},
    {"condition": "cached_output_only", "impact": "not_real_runtime", "handling": "execution_mode_cached_output"},
    {"condition": "blocked_by_authorization", "impact": "segmentation_mask_not_invokable", "handling": "blocked_evidence_no_fallback_fabrication"},
)

TASK_INPUT_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {"group_id": g["group_id"], "segmentation_inputs": list(g["segmentation_inputs"])} for g in TASK_MODEL_GROUPS
)

TASK_OUTPUT_EVIDENCE_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {
        "group_id": g["group_id"],
        "segmentation_outputs": list(g["segmentation_outputs"]),
        "evidence_outputs": list(g["evidence_outputs"]),
    }
    for g in TASK_MODEL_GROUPS
)

PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "navigation_passability_yolo_depth_segmentation_group", "group_id": "navigation_passability", "models": ("YOLO", "Depth_Geometry", "Segmentation_Mask")},
    {"case_id": "obstacle_avoidance_yolo_depth_segmentation_group", "group_id": "obstacle_avoidance_context", "models": ("YOLO", "Depth_Geometry", "Segmentation_Mask")},
    {"case_id": "door_area_yolo_segmentation_depth_group", "group_id": "door_area_detection", "models": ("YOLO", "Segmentation_Mask", "Depth_Geometry_optional")},
    {"case_id": "object_interaction_yolo_segmentation_depth_group", "group_id": "object_interaction_boundary", "models": ("YOLO", "Segmentation_Mask", "Depth_Geometry_optional")},
    {"case_id": "segmentation_no_mask_missing_information", "failure_condition": "no_mask_output", "expect_handling": "MissingInformationCandidate"},
    {"case_id": "segmentation_low_confidence_degraded", "failure_condition": "low_confidence_mask", "expect_handling": "MaskQualityCandidate_degraded"},
    {"case_id": "segmentation_no_object_association_degraded", "failure_condition": "no_object_association", "expect_handling": "ObjectBoundaryCandidate_not_high_confidence"},
    {"case_id": "segmentation_no_geometry_ref_freespace_degraded", "failure_condition": "no_geometry_ref", "expect_handling": "FreeSpaceCandidate_degraded"},
    {"case_id": "segmentation_prompt_dependency_degraded", "failure_condition": "prompt_dependency_risk_high", "expect_handling": "MaskQualityCandidate_degraded"},
    {"case_id": "segmentation_blocked_by_authorization", "failure_condition": "blocked_by_authorization", "expect_handling": "blocked_evidence_no_fallback_fabrication"},
    {"case_id": "segmentation_cached_output_not_real_run", "failure_condition": "cached_output_only", "expect_handling": "execution_mode_cached_output"},
    {"case_id": "task_group_no_action_output", "expect_no_action": True},
    {"case_id": "no_world_model_candidate_generated", "expect_no_wm_candidate": True},
    {"case_id": "no_new_protocol_created", "expect_new_protocol": False},
)
