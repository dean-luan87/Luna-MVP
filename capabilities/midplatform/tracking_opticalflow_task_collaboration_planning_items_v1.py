# -*- coding: utf-8 -*-
"""Tracking / Optical Flow task collaboration planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

FINAL_DECISION_GO = (
    "MIDPLATFORM_TRACKING_OPTICALFLOW_TASK_COLLABORATION_PLANNING_READY_FOR_OCR_TEXT_MODEL_SMOKE_IO_INSPECTION"
)
SELECTED_NEXT_PHASE = "Phase-Midplatform-OCR-Text-Model-Smoke-IO-Inspection-v1-001"
SELECTED_NEXT_ROUTE = "OCR Text Model Smoke IO Inspection"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_task_reasoning_execution": True,
    "no_action_output": True,
    "no_navigation_suggestion": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_entity_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_field_simulation": True,
    "no_real_tracking_execution": True,
    "no_real_opticalflow_execution": True,
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
        "world_entity_candidate_generation", "fact_admission",
        "field_simulation", "real_tracking_execution", "real_opticalflow_execution",
        "model_download", "weight_download", "camera_runtime", "video_stream_runtime",
        "production_runtime", "new_protocol_without_reason", "bypass_midplatform_invocation",
        "cached_output_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_task_reasoning_execution",
    "evidence_not_action_output",
    "task_collaboration_not_world_model_assembly",
    "tracking_outputs_task_evidence_only",
    "blocked_not_fabricated_evidence",
    "cached_output_not_real_model_run",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "tracking_task_collaboration_protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_object_observation_candidate": True,
    "reuse_multi_model_aligned_observation_candidate": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_object_track_candidate": True,
    "reuse_object_persistence_candidate": True,
    "reuse_motion_candidate": True,
    "reuse_tracking_quality_candidate": True,
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
    "tracking_opticalflow_task_collaboration_readiness_review_v1.json",
    "tracking_opticalflow_later_world_model_readiness_review_v1.json",
    "protocol_reuse_decision_v1.json",
    "no_action_boundary_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "tracking_opticalflow_adapter_result_candidate_registry_v1.json",
)

TASK_MODEL_GROUPS: Tuple[Dict[str, Any], ...] = (
    {
        "group_id": "road_crossing_safety",
        "models": ("YOLO", "Depth", "Tracking_Optical_Flow"),
        "tracking_inputs": (
            "ObjectObservationCandidate_sequence", "RealFrameInputPackage_sequence",
            "FieldGeometryCandidate_optional", "MultiModelAlignedObservationCandidate_optional",
        ),
        "tracking_outputs": ("ObjectTrackCandidate", "MotionCandidate", "TrackingQualityCandidate"),
        "evidence_outputs": (
            "RoadCrossingMotionEvidenceCandidate", "MovingObjectEvidenceCandidate",
            "CrossingRiskEvidenceCandidate", "RoadCrossingMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_crossing_suggestion": True,
    },
    {
        "group_id": "moving_obstacle_avoidance",
        "models": ("YOLO", "Depth", "Tracking_Optical_Flow"),
        "tracking_inputs": (
            "ObjectObservationCandidate_sequence", "FieldGeometryCandidate",
            "RealFrameInputPackage_sequence",
        ),
        "tracking_outputs": ("MotionCandidate", "ObjectTrackCandidate", "TrackingQualityCandidate"),
        "evidence_outputs": (
            "MovingObstacleEvidenceCandidate", "ObstacleMotionEvidenceCandidate",
            "ObstacleAvoidanceMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_avoidance_action": True,
    },
    {
        "group_id": "find_moving_object",
        "models": ("YOLO", "Tracking_Optical_Flow", "Depth_optional"),
        "tracking_inputs": (
            "target_object_observation_refs", "frame_sequence_refs", "depth_geometry_refs_optional",
        ),
        "tracking_outputs": ("ObjectTrackCandidate", "ObjectPersistenceCandidate", "MotionCandidate"),
        "evidence_outputs": (
            "MovingTargetEvidenceCandidate", "TargetPersistenceEvidenceCandidate",
            "FindObjectTrackingEvidenceCandidate", "FindMovingObjectMissingInformationCandidate",
        ),
        "no_final_find_decision": True,
    },
    {
        "group_id": "return_to_location_context",
        "models": ("SLAM_Spatial_Mapping", "YOLO", "Tracking_Optical_Flow_optional"),
        "tracking_inputs": (
            "ObjectObservationCandidate_sequence", "SpatialAnchorCandidate_optional",
            "LocalMapCandidate_optional", "frame_sequence_refs",
        ),
        "tracking_outputs": ("ObjectPersistenceCandidate", "MotionCandidate", "TrackingQualityCandidate"),
        "evidence_outputs": (
            "ReturnLocationObjectContinuityEvidenceCandidate", "AnchorObjectPersistenceEvidenceCandidate",
            "ReturnLocationTrackingMissingInformationCandidate",
        ),
        "no_path_planning": True,
        "no_action_output": True,
    },
)

INVOCATION_CONTROL_POLICY: Dict[str, Any] = {
    "policy_id": "tracking_task_invocation_control_policy_v1",
    "policy_name": "ModelInvocationControlPolicy",
    "new_protocol_added": False,
    "rules": (
        "midplatform_decides_tracking_opticalflow_invocation",
        "tracking_opticalflow_must_not_invoke_other_models",
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
    {"condition": "no_track_output", "impact": "object_continuity_evidence_missing", "handling": "MissingInformationCandidate"},
    {"condition": "short_track", "impact": "object_persistence_insufficient", "handling": "ObjectPersistenceCandidate_not_persistent"},
    {"condition": "identity_switch_risk_high", "impact": "object_identity_unstable", "handling": "persistence_degraded_conflict_warning"},
    {"condition": "lost_track", "impact": "target_lost", "handling": "lost_track_warning_no_final_decision"},
    {"condition": "weak_motion_signal", "impact": "dynamic_risk_uncertain", "handling": "MotionCandidate_degraded"},
    {"condition": "blocked_by_authorization", "impact": "tracking_flow_not_invokable", "handling": "blocked_evidence_no_fallback_fabrication"},
    {"condition": "cached_output_only", "impact": "not_real_runtime", "handling": "execution_mode_cached_output"},
)

TASK_INPUT_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {"group_id": g["group_id"], "tracking_inputs": list(g["tracking_inputs"])} for g in TASK_MODEL_GROUPS
)

TASK_OUTPUT_EVIDENCE_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {
        "group_id": g["group_id"],
        "tracking_outputs": list(g["tracking_outputs"]),
        "evidence_outputs": list(g["evidence_outputs"]),
    }
    for g in TASK_MODEL_GROUPS
)

PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "road_crossing_yolo_depth_tracking_group", "group_id": "road_crossing_safety", "models": ("YOLO", "Depth", "Tracking_Optical_Flow")},
    {"case_id": "moving_obstacle_yolo_depth_tracking_group", "group_id": "moving_obstacle_avoidance", "models": ("YOLO", "Depth", "Tracking_Optical_Flow")},
    {"case_id": "find_moving_object_yolo_tracking_depth_group", "group_id": "find_moving_object", "models": ("YOLO", "Tracking_Optical_Flow", "Depth_optional")},
    {"case_id": "return_location_slam_yolo_tracking_group", "group_id": "return_to_location_context", "models": ("SLAM_Spatial_Mapping", "YOLO", "Tracking_Optical_Flow_optional")},
    {"case_id": "tracking_no_track_missing_information", "failure_condition": "no_track_output", "expect_handling": "MissingInformationCandidate"},
    {"case_id": "tracking_short_track_not_persistent", "failure_condition": "short_track", "expect_handling": "ObjectPersistenceCandidate_not_persistent"},
    {"case_id": "tracking_identity_switch_degraded", "failure_condition": "identity_switch_risk_high", "expect_handling": "persistence_degraded_conflict_warning"},
    {"case_id": "tracking_lost_track_degraded", "failure_condition": "lost_track", "expect_handling": "lost_track_warning_no_final_decision"},
    {"case_id": "motion_weak_signal_degraded", "failure_condition": "weak_motion_signal", "expect_handling": "MotionCandidate_degraded"},
    {"case_id": "tracking_blocked_by_authorization", "failure_condition": "blocked_by_authorization", "expect_handling": "blocked_evidence_no_fallback_fabrication"},
    {"case_id": "tracking_cached_output_not_real_run", "failure_condition": "cached_output_only", "expect_handling": "execution_mode_cached_output"},
    {"case_id": "task_group_no_action_output", "expect_no_action": True},
    {"case_id": "no_world_model_candidate_generated", "expect_no_wm_candidate": True},
    {"case_id": "no_new_protocol_created", "expect_new_protocol": False},
)
