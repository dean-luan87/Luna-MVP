# -*- coding: utf-8 -*-
"""Field-First Minimal Real Model Adapter Integration Planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

P0_MODELS: Tuple[str, ...] = (
    "yolo_lightweight_detector",
    "supervision_output_normalization",
)

P1_OPTIONAL: Tuple[str, ...] = (
    "lightweight_depth_estimation_placeholder",
)

P2_DEFERRED: Tuple[str, ...] = (
    "bytetrack", "ocr", "sam", "grounded_sam2", "asr", "slam", "lingbot_map", "field_simulation",
)

DETECTOR_ADAPTER_PLAN: Dict[str, Any] = {
    "adapter_id": "minimal_detector_adapter_plan_v1",
    "model_family": "yolo_lightweight_or_local_detector_placeholder",
    "maps_to_candidate_type": "ObjectObservationCandidate",
    "candidate_only": True,
    "input_contract": (
        "image_path", "frame_ref", "frame_width", "frame_height", "timestamp", "source_ref", "camera_ref",
    ),
    "output_contract": (
        "observation_id", "source_type", "model_ref", "frame_ref", "timestamp", "label", "confidence", "bbox",
        "mask_ref", "depth_hint", "depth_source", "depth_confidence", "task_relevance_hint", "risk_hint",
        "candidate_only",
    ),
    "required_fields": ("observation_id", "label", "confidence", "bbox", "frame_ref", "timestamp", "source_type"),
    "optional_fields": ("mask_ref", "depth_hint", "task_relevance_hint", "risk_hint", "camera_ref"),
    "missing_field_policy": "explicit_unknown_not_silent_drop",
    "non_execution_boundary": {
        "no_weight_download": True,
        "no_production_inference": True,
        "candidate_only": True,
    },
    "download_authorization_status": "pending_owner_authorization",
}

SUPERVISION_NORMALIZATION_PLAN: Dict[str, Any] = {
    "normalization_id": "supervision_normalization_plan_v1",
    "role": "normalization_layer_not_detector",
    "accepted_input_formats": ("xyxy", "xywh", "supervision_detections"),
    "normalized_bbox_format": "xyxy_to_luna_bbox",
    "class_label_mapping_policy": "class_name_preferred_class_id_fallback",
    "confidence_mapping_policy": "preserve_raw_confidence_no_calibration_in_planning",
    "output_candidate_mapping": "ObjectObservationCandidate",
    "failure_modes": (
        "invalid_bbox", "missing_label", "zero_confidence", "empty_detection_set",
    ),
    "candidate_only": True,
}

REAL_OBSERVATION_INGESTION_PLAN: Dict[str, Any] = {
    "ingestion_plan_id": "real_observation_candidate_ingestion_plan_v1",
    "accepted_candidate_types": ("ObjectObservationCandidate", "DepthObservationCandidate"),
    "candidate_validation_rules": (
        "observation_id_unique", "bbox_within_frame", "confidence_in_0_1",
        "label_non_empty", "candidate_only_required",
    ),
    "fallback_when_depth_missing": "depth_source_unknown_depth_confidence_low",
    "fallback_when_label_unknown": "label_unknown_retained_not_dropped",
    "fallback_when_confidence_low": "retain_with_low_confidence_warning",
    "fallback_when_bbox_invalid": "reject_with_validation_reason",
    "traceability_policy": "preserve_source_refs_model_ref_frame_ref",
    "candidate_only": True,
}

DETECTOR_TO_OBSERVATION_MAPPING: Dict[str, Any] = {
    "mapping_id": "detector_output_to_observation_candidate_mapping_v1",
    "source_type": "model_detector",
    "field_mappings": (
        {"detector": "class_name", "observation": "label"},
        {"detector": "confidence", "observation": "confidence"},
        {"detector": "xyxy", "observation": "bbox"},
        {"detector": "frame_ref", "observation": "frame_ref"},
        {"detector": "model_ref", "observation": "model_ref"},
    ),
    "defaults": {
        "source_type": "model_detector",
        "depth_source": "unknown",
        "depth_confidence": "low",
        "candidate_only": True,
    },
    "candidate_only": True,
}

DEPTH_MISSING_FALLBACK_POLICY: Dict[str, Any] = {
    "policy_id": "depth_missing_fallback_policy_v1",
    "when_depth_absent": {
        "depth_source": "unknown",
        "depth_confidence": "low",
        "depth_error_expected": True,
        "pseudo_3d_position": "unknown_or_weak_estimated",
    },
    "when_depth_estimated": {
        "depth_source": "estimated",
        "depth_confidence": "medium_or_low",
        "depth_error_expected": True,
        "not_hardware_fact": True,
    },
    "prohibited": ("treat_estimated_depth_as_hardware_fact", "silent_drop_no_depth"),
    "field_core_degradation": "trajectory_confidence_capped_missing_depth_propagates",
}

REAL_MODEL_SUCCESS_PATH_READINESS: Dict[str, Any] = {
    "readiness_plan_id": "real_model_success_path_readiness_plan_v1",
    "prerequisite": "minimal_detector_adapter_and_ingestion_skeleton_go",
    "success_path_validates": (
        "real_bbox_label_confidence_into_observation_candidate",
        "field_scene_construction_from_real_observations",
        "depth_missing_correct_degradation",
        "static_dynamic_target_candidates_from_real_detections",
        "field_first_core_logic_result_stable_output",
    ),
    "deferred_until_after_ingestion_skeleton": (
        "full_production_model_selection", "bytetrack", "field_simulation",
    ),
    "recommended_sequence": (
        "Minimal Real Model Adapter Integration Planning",
        "Real Observation Candidate Ingestion Skeleton",
        "Field-First Core Real-Model Success Path DryRun",
        "Field-First Core Success Path Hardening",
        "Field Simulation Planning",
    ),
}

DOWNLOAD_AUTHORIZATION_STATUS: Dict[str, Any] = {
    "status_id": "model_download_authorization_status_v1",
    "weight_download": "not_authorized_in_this_phase",
    "large_dependency_install": "not_authorized_in_this_phase",
    "local_environment_check": "allowed_planning_only",
    "owner_authorization_required_for": ("weight_download", "pip_install_yolo", "pip_install_supervision"),
    "planning_only": True,
}

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "weight_download", "large_dependency_install", "production_model_integration",
        "bytetrack", "ocr", "sam", "grounded_sam2", "slam", "asr",
        "field_simulation", "task_execution", "world_model_fact", "memory_write",
        "runtime", "integration_test",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_model_download", "adapter_plan_not_production_inference",
    "observation_candidate_not_world_model_fact", "planning_not_field_simulation",
)

SELECTED_NEXT_PHASE = "Phase-Midplatform-Real-Observation-Candidate-Ingestion-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Real Observation Candidate Ingestion Skeleton"

PLANNING_RULES: Tuple[Dict[str, str], ...] = (
    {"rule_id": "first_batch_detector_only", "desc": "P0: detector + supervision normalization only"},
    {"rule_id": "model_output_to_observation", "desc": "detector output maps to ObjectObservationCandidate"},
    {"rule_id": "depth_unknown_explicit", "desc": "missing depth explicit unknown not hardware fact"},
    {"rule_id": "low_confidence_retained", "desc": "low confidence not silently dropped"},
    {"rule_id": "no_weight_download", "desc": "no weight download in planning phase"},
    {"rule_id": "supervision_normalization_layer", "desc": "supervision is normalization not replacement for core"},
    {"rule_id": "field_core_unchanged", "desc": "Field-First Core Pipeline not rewritten in this phase"},
    {"rule_id": "success_path_after_ingestion", "desc": "real-model dryrun after ingestion skeleton"},
)

MOCK_PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "yolo_bbox_maps_to_observation", "input": "detector_xyxy_output", "expected": "ObjectObservationCandidate", "pass_condition": "bbox_label_confidence_mapped"},
    {"case_id": "supervision_normalizes_xyxy", "input": "supervision_detections", "expected": "normalized_bbox", "pass_condition": "xyxy_to_luna_bbox"},
    {"case_id": "missing_depth_unknown_policy", "input": "detector_no_depth", "expected": "depth_source_unknown", "pass_condition": "explicit_unknown"},
    {"case_id": "low_confidence_retained", "input": "confidence_0.25", "expected": "observation_retained", "pass_condition": "not_silently_dropped"},
    {"case_id": "unknown_label_retained", "input": "label_unknown", "expected": "label_unknown", "pass_condition": "fallback_policy"},
    {"case_id": "invalid_bbox_rejected", "input": "bbox_out_of_frame", "expected": "validation_reject", "pass_condition": "bbox_validation"},
    {"case_id": "first_batch_no_bytetrack", "input": "tracking_request", "expected": "deferred_p2", "pass_condition": "scope_limited"},
    {"case_id": "no_weight_download", "input": "download_request", "expected": "blocked", "pass_condition": "authorization_pending"},
    {"case_id": "real_input_field_scene_ready", "input": "observation_list", "expected": "field_scene_constructable", "pass_condition": "core_ingestion_ready"},
    {"case_id": "depth_estimated_not_hardware", "input": "software_depth", "expected": "depth_source_estimated", "pass_condition": "not_hardware_fact"},
)
