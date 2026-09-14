# -*- coding: utf-8 -*-
"""OCR / Text task collaboration planning — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

FINAL_DECISION_GO = (
    "MIDPLATFORM_OCR_TEXT_TASK_COLLABORATION_PLANNING_READY_FOR_SEGMENTATION_MASK_MODEL_SMOKE_IO_INSPECTION"
)
SELECTED_NEXT_PHASE = "Phase-Midplatform-Segmentation-Mask-Model-Smoke-IO-Inspection-v1-001"
SELECTED_NEXT_ROUTE = "Segmentation Mask Model Smoke IO Inspection"

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
    "no_real_ocr_execution": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_llm_text_correction": True,
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
        "field_simulation", "real_ocr_execution", "llm_text_correction",
        "model_download", "weight_download", "camera_runtime", "video_stream_runtime",
        "production_runtime", "new_protocol_without_reason", "bypass_midplatform_invocation",
        "cached_output_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "planning_not_task_reasoning_execution",
    "evidence_not_action_output",
    "task_collaboration_not_world_model_assembly",
    "ocr_text_outputs_task_evidence_only",
    "blocked_not_fabricated_evidence",
    "cached_output_not_real_model_run",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "ocr_text_task_collaboration_protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_object_observation_candidate": True,
    "reuse_multi_model_aligned_observation_candidate": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_spatial_anchor_candidate": True,
    "reuse_text_observation_candidate": True,
    "reuse_text_region_candidate": True,
    "reuse_text_anchor_candidate": True,
    "reuse_text_normalization_candidate": True,
    "reuse_text_quality_candidate": True,
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
    "ocr_text_task_collaboration_readiness_review_v1.json",
    "ocr_text_later_world_model_readiness_review_v1.json",
    "protocol_reuse_decision_v1.json",
    "no_action_boundary_review_v1.json",
    "no_world_model_assembly_boundary_review_v1.json",
    "ocr_text_adapter_result_candidate_registry_v1.json",
)

TASK_MODEL_GROUPS: Tuple[Dict[str, Any], ...] = (
    {
        "group_id": "read_sign_or_storefront",
        "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Anchor_optional"),
        "ocr_inputs": (
            "RealFrameInputPackage", "ObjectObservationCandidate_optional",
            "EnhancedFieldSceneCandidate_optional", "SpatialAnchorCandidate_optional",
        ),
        "ocr_outputs": (
            "TextObservationCandidate", "TextRegionCandidate",
            "TextAnchorCandidate", "TextQualityCandidate",
        ),
        "evidence_outputs": (
            "SignReadingEvidenceCandidate", "StorefrontTextEvidenceCandidate",
            "TextAnchorEvidenceCandidate", "ReadSignMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_navigation_suggestion": True,
    },
    {
        "group_id": "indoor_navigation_context",
        "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Mapping"),
        "ocr_inputs": (
            "RealFrameInputPackage", "SpatialAnchorCandidate_optional",
            "LocalMapCandidate_optional", "EnhancedFieldSceneCandidate_optional",
        ),
        "ocr_outputs": (
            "TextObservationCandidate", "TextAnchorCandidate",
            "TextRegionCandidate", "TextQualityCandidate",
        ),
        "evidence_outputs": (
            "FloorSignTextEvidenceCandidate", "DoorplateTextEvidenceCandidate",
            "ElevatorTextEvidenceCandidate", "IndoorTextContextMissingInformationCandidate",
        ),
        "no_action_output": True,
        "no_navigation_suggestion": True,
    },
    {
        "group_id": "find_store_or_doorplate",
        "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Mapping_optional"),
        "ocr_inputs": (
            "ObjectObservationCandidate_optional", "TextRegionCandidate_optional",
            "RealFrameInputPackage", "SpatialAnchorCandidate_optional",
        ),
        "ocr_outputs": (
            "TextObservationCandidate", "TextAnchorCandidate",
            "TextNormalizationCandidate", "TextQualityCandidate",
        ),
        "evidence_outputs": (
            "StoreNameEvidenceCandidate", "DoorplateEvidenceCandidate",
            "TextMatchEvidenceCandidate", "FindStoreMissingInformationCandidate",
        ),
        "no_final_find_decision": True,
        "no_action_output": True,
    },
    {
        "group_id": "read_button_label_or_warning",
        "models": ("OCR_Text", "YOLO_optional", "Depth_optional"),
        "ocr_inputs": (
            "RealFrameInputPackage", "ObjectObservationCandidate_optional",
            "FieldGeometryCandidate_optional",
        ),
        "ocr_outputs": (
            "TextObservationCandidate", "TextRegionCandidate",
            "TextQualityCandidate", "TextNormalizationCandidate",
        ),
        "evidence_outputs": (
            "ButtonLabelEvidenceCandidate", "WarningTextEvidenceCandidate",
            "InstructionTextEvidenceCandidate", "ReadLabelMissingInformationCandidate",
        ),
        "no_action_output": True,
    },
)

INVOCATION_CONTROL_POLICY: Dict[str, Any] = {
    "policy_id": "ocr_text_task_invocation_control_policy_v1",
    "policy_name": "ModelInvocationControlPolicy",
    "new_protocol_added": False,
    "rules": (
        "midplatform_decides_ocr_text_invocation",
        "ocr_text_must_not_invoke_other_models",
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
    {"condition": "no_text_output", "impact": "text_evidence_missing", "handling": "MissingInformationCandidate"},
    {"condition": "low_confidence_text", "impact": "text_reading_unreliable", "handling": "TextQualityCandidate_degraded"},
    {"condition": "no_text_region", "impact": "text_spatial_position_missing", "handling": "TextAnchorCandidate_not_high_confidence"},
    {"condition": "ambiguous_normalization", "impact": "text_correction_uncertain", "handling": "TextNormalizationCandidate_ambiguity_preserved"},
    {"condition": "no_spatial_anchor", "impact": "text_cannot_stable_spatial_anchor", "handling": "TextAnchorCandidate_degraded"},
    {"condition": "cached_output_only", "impact": "not_real_runtime", "handling": "execution_mode_cached_output"},
    {"condition": "blocked_by_authorization", "impact": "ocr_text_not_invokable", "handling": "blocked_evidence_no_fallback_fabrication"},
)

TASK_INPUT_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {"group_id": g["group_id"], "ocr_inputs": list(g["ocr_inputs"])} for g in TASK_MODEL_GROUPS
)

TASK_OUTPUT_EVIDENCE_MAPPING: Tuple[Dict[str, Any], ...] = tuple(
    {
        "group_id": g["group_id"],
        "ocr_outputs": list(g["ocr_outputs"]),
        "evidence_outputs": list(g["evidence_outputs"]),
    }
    for g in TASK_MODEL_GROUPS
)

PLANNING_CASES: Tuple[Dict[str, Any], ...] = (
    {"case_id": "read_sign_yolo_ocr_slam_group", "group_id": "read_sign_or_storefront", "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Anchor_optional")},
    {"case_id": "indoor_navigation_yolo_ocr_slam_group", "group_id": "indoor_navigation_context", "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Mapping")},
    {"case_id": "find_store_yolo_ocr_slam_group", "group_id": "find_store_or_doorplate", "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Mapping_optional")},
    {"case_id": "read_button_label_ocr_yolo_depth_group", "group_id": "read_button_label_or_warning", "models": ("OCR_Text", "YOLO_optional", "Depth_optional")},
    {"case_id": "ocr_no_text_missing_information", "failure_condition": "no_text_output", "expect_handling": "MissingInformationCandidate"},
    {"case_id": "ocr_low_confidence_degraded", "failure_condition": "low_confidence_text", "expect_handling": "TextQualityCandidate_degraded"},
    {"case_id": "ocr_no_region_anchor_degraded", "failure_condition": "no_text_region", "expect_handling": "TextAnchorCandidate_not_high_confidence"},
    {"case_id": "ocr_ambiguous_normalization_preserved", "failure_condition": "ambiguous_normalization", "expect_handling": "TextNormalizationCandidate_ambiguity_preserved"},
    {"case_id": "ocr_no_spatial_anchor_degraded", "failure_condition": "no_spatial_anchor", "expect_handling": "TextAnchorCandidate_degraded"},
    {"case_id": "ocr_blocked_by_authorization", "failure_condition": "blocked_by_authorization", "expect_handling": "blocked_evidence_no_fallback_fabrication"},
    {"case_id": "ocr_cached_output_not_real_run", "failure_condition": "cached_output_only", "expect_handling": "execution_mode_cached_output"},
    {"case_id": "task_group_no_action_output", "expect_no_action": True},
    {"case_id": "no_world_model_candidate_generated", "expect_no_wm_candidate": True},
    {"case_id": "no_new_protocol_created", "expect_new_protocol": False},
)
