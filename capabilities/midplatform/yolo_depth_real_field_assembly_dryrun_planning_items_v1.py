# -*- coding: utf-8 -*-
"""YOLO + Depth Real Field Assembly DryRun Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-YOLO-Depth-Controlled-Real-Model-DryRun-v1-001"
SELECTED_NEXT_ROUTE = "YOLO Depth Controlled Real Model DryRun"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_yolo_execution", "real_depth_model_execution", "model_download", "weight_download",
        "large_dependency_install", "real_camera_read", "real_video_stream", "real_runtime",
        "field_simulation", "task_reasoning", "world_model_entry", "memory_candidate",
        "integration_test", "scene_graph_runtime", "slam_runtime", "bytetrack_runtime",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_controlled_dryrun_execution",
    "dryrun_planning_not_mock_skeleton",
    "real_output_contract_not_world_model_fact",
    "authorization_matrix_not_production_runtime",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_world_model_fact": True,
    "no_persistent_memory": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_real_yolo_execution": True,
    "no_real_depth_execution": True,
    "no_runtime_execution": True,
    "no_field_simulation": True,
    "no_task_execution": True,
    "controlled_dryrun_deferred_to_next_phase": True,
    "no_large_dependency_install": True,
}

REAL_FRAME_INPUT_PACKAGE_CONTRACT: Dict[str, Any] = {
    "contract_id": "real_frame_input_package_contract_v1",
    "package_type": "RealFrameInputPackage",
    "required_fields": (
        "frame_input_id", "frame_ref", "frame_width", "frame_height", "timestamp",
        "source_ref", "test_case_id",
    ),
    "optional_fields": ("image_path", "camera_ref", "expected_scene_notes"),
    "candidate_only": True,
}

YOLO_REAL_OUTPUT_PACKAGE_CONTRACT: Dict[str, Any] = {
    "contract_id": "yolo_real_output_package_contract_v1",
    "package_type": "YOLORealOutputPackage",
    "required_fields": (
        "detector_run_id", "model_ref", "frame_ref", "timestamp", "frame_width",
        "frame_height", "detections",
    ),
    "detection_fields": ("bbox_xyxy", "label", "confidence", "source_refs"),
    "maps_to": "ObjectObservationCandidate",
    "yolo_already_integrated": True,
}

DEPTH_REAL_OUTPUT_PACKAGE_CONTRACT: Dict[str, Any] = {
    "contract_id": "depth_real_output_package_contract_v1",
    "package_type": "DepthRealOutputPackage",
    "required_fields": (
        "depth_run_id", "model_ref", "frame_ref", "timestamp", "frame_width",
        "frame_height", "depth_map_shape", "depth_value_unit", "depth_source",
        "depth_confidence",
    ),
    "optional_fields": ("depth_map_ref", "raw_output_ref"),
    "maps_to": "DepthObservationCandidate",
    "depth_source_default": "estimated",
    "depth_error_expected": True,
}

REAL_FIELD_ASSEMBLY_DRYRUN_RESULT_CONTRACT: Dict[str, Any] = {
    "contract_id": "real_field_assembly_dryrun_result_candidate_contract_v1",
    "package_type": "RealFieldAssemblyDryRunResultCandidate",
    "pipeline_stages": (
        "ObjectObservationCandidate", "DepthObservationCandidate",
        "MultiModelAlignedObservationCandidate", "ObjectDepthHintCandidate",
        "FieldGeometryCandidate", "EnhancedFieldSceneCandidate",
        "FieldAssemblyResultCandidate",
    ),
    "traceability_required": True,
    "candidate_only": True,
}

REAL_FIELD_ASSEMBLY_SUCCESS_CRITERIA: Dict[str, Any] = {
    "criteria_id": "real_field_assembly_success_criteria_v1",
    "minimum_object_count": 1,
    "minimum_geometry_candidate_count": 1,
    "required_alignment_success": True,
    "required_field_scene_candidate": True,
    "required_warning_propagation": True,
    "allowed_degradation": (
        "depth_missing_unknown_fallback", "geometry_unknown", "entity_2d_only",
        "relative_depth_weak_geometry", "low_confidence_degraded",
    ),
    "prohibited_outputs": (
        "world_model_entry", "memory_candidate", "scene_relation_candidate",
        "field_simulation_result", "task_execution_result",
    ),
    "pass_fail_policy": "minimum_go_plus_quality_notes",
    "minimum_go_rules": (
        "at_least_one_yolo_to_object_observation",
        "depth_or_explicit_missing_fallback",
        "at_least_one_aligned_candidate",
        "at_least_one_depth_hint_or_unknown_fallback",
        "at_least_one_geometry_or_geometry_unknown",
        "at_least_one_enhanced_field_scene",
        "warning_missing_degradation_preserved",
        "candidate_only_outputs",
    ),
    "quality_rules": (
        "multi_zone_distribution_when_multiple_objects",
        "estimated_relative_not_high_confidence",
        "invalid_bbox_depth_mismatch_handled",
        "quality_summaries_present",
        "readiness_for_success_path_hardening_when_quality_met",
    ),
}

REAL_MODEL_EXECUTION_AUTHORIZATION_MATRIX: Dict[str, Any] = {
    "matrix_id": "real_model_execution_authorization_matrix_v1",
    "current_phase": "planning_only_no_execution",
    "next_phase": SELECTED_NEXT_PHASE,
    "models": (
        {
            "model_id": "detector_yolo",
            "status": "already_integrated_p0",
            "planning_phase_execution": False,
            "controlled_dryrun_phase": "requires_local_runner_confirmation",
        },
        {
            "model_id": "depth_anything_v2",
            "status": "candidate_p0",
            "planning_phase_execution": False,
            "controlled_dryrun_phase": "requires_download_authorization",
        },
        {
            "model_id": "unidepth_v2",
            "status": "candidate_p0",
            "planning_phase_execution": False,
            "controlled_dryrun_phase": "requires_download_authorization",
        },
        {
            "model_id": "local_depth_adapter",
            "status": "preferred_if_available",
            "planning_phase_execution": False,
            "controlled_dryrun_phase": "allowed_if_local_adapter_exists",
        },
        {
            "model_id": "depth_mock_adapter_real_frame",
            "status": "fallback_only",
            "planning_phase_execution": False,
            "controlled_dryrun_phase": "allowed_if_real_depth_not_authorized",
        },
    ),
    "authorization_gates": (
        "yolo_local_runner_available",
        "depth_model_download_authorized_or_local_adapter",
        "real_test_image_allowed",
        "raw_model_output_artifact_write_allowed",
        "no_runtime_offline_dryrun_only",
    ),
}

DRYRUN_FAILURE_POINT_POLICY: Dict[str, Any] = {
    "policy_id": "dryrun_failure_point_policy_v1",
    "failure_points": (
        {"point": "yolo_no_detection", "action": "empty_scene_no_crash", "rollback": "none"},
        {"point": "depth_missing", "action": "unknown_fallback_entity_2d_or_geometry_unknown", "rollback": "depth_adapter"},
        {"point": "alignment_timestamp_mismatch", "action": "degrade_or_reject_alignment", "rollback": "alignment_policy"},
        {"point": "invalid_yolo_bbox", "action": "reject_fusion_geometry", "rollback": "detector_output_review"},
        {"point": "depth_low_confidence", "action": "geometry_confidence_low", "rollback": "depth_adapter_or_mock"},
        {"point": "relative_depth_only", "action": "weak_geometry_no_high_confidence", "rollback": "metric_depth_if_available"},
        {"point": "assembly_quality_degraded", "action": "retain_scene_with_warnings", "rollback": "geometry_or_fusion_stage"},
    ),
}

DRYRUN_TRACEABILITY_POLICY: Dict[str, Any] = {
    "policy_id": "dryrun_traceability_policy_v1",
    "required_refs": (
        "frame_input_ref", "yolo_output_ref", "depth_output_ref", "model_ref",
        "raw_output_ref", "detector_run_id", "depth_run_id",
    ),
    "propagate_through": (
        "ObjectObservationCandidate", "DepthObservationCandidate",
        "ObjectDepthHintCandidate", "FieldGeometryCandidate",
        "EnhancedFieldEntityCandidate", "EnhancedFieldSceneCandidate",
    ),
    "no_world_model_write": True,
}

NEXT_CONTROLLED_DRYRUN_PLAN: Dict[str, Any] = {
    "plan_id": "next_controlled_dryrun_plan_v1",
    "target_phase": SELECTED_NEXT_PHASE,
    "execution_mode": "offline_controlled_dryrun",
    "deferred_from_planning": True,
    "preconditions": (
        "authorization_matrix_resolved",
        "yolo_local_runner_confirmed",
        "depth_source_selected",
        "real_frame_input_package_prepared",
        "skeleton_pipeline_modules_ready",
    ),
    "execution_steps": (
        "load_real_frame_input_package",
        "run_or_ingest_yolo_real_output_package",
        "run_or_ingest_depth_real_output_package",
        "map_to_object_and_depth_observation_candidates",
        "run_multi_model_alignment",
        "run_depth_object_fusion",
        "run_field_geometry_candidate_generation",
        "run_field_assembly",
        "emit_real_field_assembly_dryrun_result_candidate",
        "evaluate_against_success_criteria",
    ),
    "no_runtime": True,
    "no_weight_download_in_planning": True,
}

PLANNING_RULES: Tuple[str, ...] = (
    "yolo_output_maps_to_object_observation_candidate",
    "depth_output_maps_to_depth_observation_candidate",
    "same_frame_timestamp_required_for_alignment",
    "missing_depth_uses_unknown_fallback_not_drop_object",
    "invalid_bbox_rejected_with_reason",
    "estimated_depth_never_hardware_fact",
    "warning_missing_degradation_full_chain",
    "no_scene_relation_in_dryrun",
    "no_field_simulation_in_dryrun",
    "controlled_execution_deferred_to_next_phase",
)

DRYRUN_PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "single_object_real_yolo_depth",
        "description": "Single YOLO detection + depth → EnhancedFieldSceneCandidate",
        "inputs": ("RealFrameInputPackage", "YOLORealOutputPackage", "DepthRealOutputPackage"),
        "expected": ("entity_geometry_enhanced_or_degraded", "enhanced_field_scene"),
        "pass_condition": "minimum_go_met",
    },
    {
        "case_id": "multiple_objects_real_yolo_depth",
        "description": "Multiple detections → multiple entities + zone_summary",
        "inputs": ("multi_detection_yolo", "depth_map"),
        "expected": ("entity_count>=2", "zone_summary"),
        "pass_condition": "quality_multi_zone",
    },
    {
        "case_id": "yolo_real_depth_missing_fallback",
        "description": "YOLO present, depth missing → unknown fallback",
        "inputs": ("yolo_only",),
        "expected": ("entity_2d_only_or_geometry_unknown", "depth_quality_degraded"),
        "pass_condition": "minimum_go_with_fallback",
    },
    {
        "case_id": "depth_real_low_confidence_degraded",
        "description": "Low depth confidence → geometry confidence low",
        "inputs": ("yolo", "depth_low_conf"),
        "expected": ("geometry_confidence_low",),
        "pass_condition": "degradation_preserved",
    },
    {
        "case_id": "frame_timestamp_mismatch_degraded_or_rejected",
        "description": "YOLO/depth timestamp mismatch → alignment degrade/reject",
        "inputs": ("yolo_ts_t0", "depth_ts_t1"),
        "expected": ("alignment_degraded_or_rejected",),
        "pass_condition": "failure_point_handled",
    },
    {
        "case_id": "invalid_yolo_bbox_rejected",
        "description": "Invalid bbox from detector rejected with reason",
        "inputs": ("yolo_invalid_bbox",),
        "expected": ("fusion_or_geometry_rejected",),
        "pass_condition": "failure_point_handled",
    },
    {
        "case_id": "relative_depth_real_weak_geometry",
        "description": "Relative depth → weak geometry, not high confidence",
        "inputs": ("yolo", "depth_relative"),
        "expected": ("geometry_weak_estimated", "no_high_confidence"),
        "pass_condition": "quality_rule_met",
    },
    {
        "case_id": "real_field_scene_quality_summary",
        "description": "Scene/depth/geometry quality summaries emitted",
        "inputs": ("full_pipeline",),
        "expected": ("scene_quality_summary", "depth_quality_summary", "geometry_quality_summary"),
        "pass_condition": "quality_summaries_present",
    },
    {
        "case_id": "no_detection_no_field_entity",
        "description": "Zero YOLO detections → no entity, dryrun stable",
        "inputs": ("empty_yolo",),
        "expected": ("entity_count_0", "no_crash"),
        "pass_condition": "failure_point_handled",
    },
    {
        "case_id": "real_model_output_traceability_preserved",
        "description": "model_ref, raw_output_ref, frame_ref preserved end-to-end",
        "inputs": ("yolo", "depth"),
        "expected": ("traceability_refs_complete",),
        "pass_condition": "traceability_policy_met",
    },
)

PIPELINE_CHAIN: Tuple[str, ...] = (
    "YOLORealOutputPackage",
    "DepthRealOutputPackage",
    "ObjectObservationCandidate",
    "DepthObservationCandidate",
    "MultiModelAlignment",
    "DepthObjectFusion",
    "FieldGeometryCandidate",
    "FieldAssembly",
    "EnhancedFieldSceneCandidate",
)
