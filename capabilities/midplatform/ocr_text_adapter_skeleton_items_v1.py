# -*- coding: utf-8 -*-
"""OCR / Text adapter skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-OCR-Text-Task-Collaboration-Planning-v1-001"
SELECTED_NEXT_ROUTE = "OCR Text Task Collaboration Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_ocr_execution", "model_download", "weight_download", "large_dependency_install",
        "camera_runtime", "video_stream_runtime", "field_simulation", "simulated_route",
        "task_reasoning", "task_action_output", "navigation_suggestion", "llm_text_correction",
        "world_model_candidate_assembly", "world_model_entry_write", "world_entity_candidate_generation",
        "fact_admission", "new_protocol_without_reason", "production_runtime",
        "cached_output_as_real_run", "adapter_stub_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "adapter_skeleton_based_on_smoke_io_inspection",
    "cached_output_not_real_model_run",
    "adapter_stub_not_real_model_run",
    "blocked_not_fabricated_output",
    "readiness_not_world_model_assembly",
    "field_simulation_not_reintroduced",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_object_observation_candidate": True,
    "reuse_multi_model_aligned_observation_candidate": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_spatial_anchor_candidate": True,
    "reuse_smoke_io_inspection_artifacts": True,
    "reuse_traceability_refs": True,
    "reuse_authorization_boundary": True,
}

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

LATER_WORLD_MODEL_READINESS: Tuple[Dict[str, Any], ...] = (
    {"output": "TextObservationCandidate", "role": "future_semantic_label", "assembly": "deferred"},
    {"output": "TextAnchorCandidate", "role": "future_text_spatial_anchor", "assembly": "deferred"},
    {"output": "TextRegionCandidate", "role": "future_sign_region", "assembly": "deferred"},
    {"output": "TextNormalizationCandidate", "role": "future_normalized_text", "assembly": "deferred"},
)

TASK_COLLABORATION_MAPPING: Tuple[Dict[str, Any], ...] = (
    {
        "scenario": "read_sign_or_storefront",
        "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Anchor_optional"),
        "ocr_outputs": ("TextObservationCandidate", "TextRegionCandidate", "TextAnchorCandidate", "TextQualityCandidate"),
    },
    {
        "scenario": "indoor_navigation_context",
        "models": ("YOLO", "OCR_Text", "SLAM_Spatial_Mapping"),
        "ocr_outputs": ("TextObservationCandidate", "TextAnchorCandidate", "TextRegionCandidate"),
    },
    {
        "scenario": "find_store_or_doorplate",
        "models": ("YOLO", "OCR_Text", "SLAM_optional"),
        "ocr_outputs": ("TextObservationCandidate", "TextAnchorCandidate", "TextNormalizationCandidate"),
    },
    {
        "scenario": "read_button_label_or_warning",
        "models": ("OCR_Text", "YOLO_optional", "Depth_optional"),
        "ocr_outputs": ("TextObservationCandidate", "TextRegionCandidate", "TextQualityCandidate"),
    },
)

SMOKE_IO_ARTIFACT_FILES: Tuple[str, ...] = (
    "ocr_text_model_smoke_io_inspection_report_v1.json",
    "model_smoke_run_candidate_registry_v1.json",
    "model_io_inspection_candidate_registry_v1.json",
    "model_candidate_mapping_feasibility_registry_v1.json",
    "ocr_text_available_model_review_v1.json",
    "ocr_text_input_format_review_v1.json",
    "ocr_text_output_format_review_v1.json",
    "ocr_text_failure_point_review_v1.json",
    "ocr_text_candidate_mapping_review_v1.json",
    "model_execution_authorization_review_v1.json",
    "new_protocol_reason_required_report_v1.json",
)

SKELETON_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "text_observation_from_rapidocr_cached_output",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "expect_observations_min": 1,
        "expect_execution_mode": "cached_output",
        "expect_not_real_run": True,
    },
    {
        "case_id": "text_observation_from_paddleocr_cached_output",
        "source_smoke_case_id": "paddleocr_cached_output_inspection",
        "inspect_subtype": "paddleocr",
        "expect_observations_min": 1,
        "expect_execution_mode": "cached_output",
    },
    {
        "case_id": "text_region_from_cached_region_output",
        "source_smoke_case_id": "text_region_cached_output_inspection",
        "inspect_subtype": "text_region",
        "expect_regions_min": 1,
        "expect_execution_mode": "cached_output",
    },
    {
        "case_id": "text_from_adapter_stub",
        "source_smoke_case_id": "ocr_adapter_stub_io_inspection",
        "inspect_subtype": "ocr",
        "expect_observations_min": 1,
        "expect_execution_mode": "adapter_stub",
        "expect_not_real_run": True,
    },
    {
        "case_id": "text_anchor_from_text_region_geometry",
        "source_smoke_case_id": "paddleocr_cached_output_inspection",
        "inspect_subtype": "paddleocr",
        "include_geometry": True,
        "expect_anchors_min": 1,
        "expect_anchor_conf_not_low": False,
    },
    {
        "case_id": "text_anchor_without_spatial_ref_degraded",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "overrides": {"no_spatial_ref": True},
        "expect_anchors_min": 1,
        "expect_anchor_degraded": True,
    },
    {
        "case_id": "text_normalization_from_cached_output",
        "source_smoke_case_id": "text_normalization_mapping_feasibility",
        "inspect_subtype": "text_enhancement",
        "expect_normalizations_min": 1,
    },
    {
        "case_id": "low_confidence_text_degraded",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "overrides": {"low_confidence": True, "confidence": 0.35},
        "expect_quality_degraded": True,
    },
    {
        "case_id": "ambiguous_normalization_preserved",
        "source_smoke_case_id": "text_normalization_mapping_feasibility",
        "inspect_subtype": "text_enhancement",
        "overrides": {"ambiguous": True, "ambiguity_status": "ambiguous", "alternatives": ["3F出口", "3楼出口"]},
        "expect_ambiguous": True,
    },
    {
        "case_id": "text_quality_from_cached_output",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "expect_quality_min": 1,
    },
    {
        "case_id": "blocked_missing_weight_no_output_fabrication",
        "source_smoke_case_id": "missing_weight_blocked",
        "inspect_subtype": "ocr",
        "expect_blocked": True,
        "expect_no_fabrication": True,
    },
    {
        "case_id": "blocked_missing_dependency_no_output_fabrication",
        "source_smoke_case_id": "missing_dependency_blocked",
        "inspect_subtype": "ocr",
        "expect_blocked": True,
        "expect_no_fabrication": True,
    },
    {
        "case_id": "readiness_for_task_collaboration_true",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "expect_task_readiness": True,
    },
    {
        "case_id": "readiness_for_later_world_model_candidate_assembly_true",
        "source_smoke_case_id": "paddleocr_cached_output_inspection",
        "inspect_subtype": "paddleocr",
        "include_geometry": True,
        "expect_later_wm_readiness": True,
        "expect_no_wm_assembly": True,
    },
    {
        "case_id": "no_new_protocol_created",
        "source_smoke_case_id": "no_new_protocol_without_reason",
        "inspect_subtype": "ocr",
        "expect_new_protocol": False,
    },
    {
        "case_id": "no_action_output",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "expect_no_action": True,
    },
    {
        "case_id": "no_world_model_assembly",
        "source_smoke_case_id": "rapidocr_cached_output_inspection",
        "inspect_subtype": "rapidocr",
        "expect_no_wm_candidate": True,
    },
)
