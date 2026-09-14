# -*- coding: utf-8 -*-
"""OCR / Text Model smoke IO inspection — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-OCR-Text-Adapter-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "OCR Text Adapter Skeleton"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "adapter_skeleton", "task_collaboration_execution", "field_simulation", "simulated_route",
        "world_model_candidate_assembly", "world_model_entry_write", "fact_admission",
        "task_reasoning", "task_action_output", "navigation_suggestion",
        "unauthorized_model_download", "unauthorized_weight_download", "large_dependency_install",
        "camera_runtime", "video_stream_runtime", "production_runtime",
        "new_protocol_without_reason", "cached_output_as_real_run", "adapter_stub_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "smoke_io_inspection_not_field_simulation",
    "blocked_not_failed_download",
    "cached_output_not_real_model_run",
    "adapter_stub_not_real_model_run",
    "inspection_not_adapter_skeleton",
)

NEW_PROTOCOL_REASON_REPORT: Dict[str, Any] = {
    "report_id": "new_protocol_reason_required_report_v1",
    "new_protocol_proposals": [],
    "owner_approval_required": False,
    "status": "no_new_protocol_proposed",
}

DEFAULT_OCR_TEXT_AVAILABILITY: Dict[str, Any] = {
    "matrix_id": "ocr_text_availability_matrix_v1",
    "local_ocr_available": False,
    "local_text_region_available": False,
    "local_weights_available": False,
    "dependencies_available": False,
    "rapidocr_cached_output_available": True,
    "paddleocr_cached_output_available": True,
    "text_region_cached_output_available": True,
    "adapter_stub_available": True,
    "model_download_authorized": False,
    "weight_download_authorized": False,
    "camera_runtime_authorized": False,
    "video_stream_authorized": False,
    "no_unauthorized_download": True,
}

CACHED_RAPIDOCR_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_rapidocr_output_fixture_v1",
    "model_role": "ocr_text_model",
    "subtype": "rapidocr",
    "outputs": {
        "text": "星巴克咖啡",
        "bbox": [120, 80, 280, 120],
        "confidence": 0.91,
        "reading_order": 0,
    },
}

CACHED_PADDLEOCR_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_paddleocr_output_fixture_v1",
    "model_role": "ocr_text_model",
    "subtype": "paddleocr",
    "outputs": {
        "text": "3F 出口",
        "bbox": [50, 200, 150, 240],
        "confidence": 0.88,
        "polygon": [[50, 200], [150, 200], [150, 240], [50, 240]],
    },
}

CACHED_TEXT_REGION_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_text_region_output_fixture_v1",
    "model_role": "ocr_text_model",
    "subtype": "text_region",
    "outputs": {
        "region_type": "signboard",
        "bbox": [100, 50, 400, 150],
        "polygon": [[100, 50], [400, 50], [400, 150], [100, 150]],
        "layout_block": {"reading_order": 0, "block_type": "title"},
    },
}

CACHED_TEXT_NORMALIZATION_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_text_normalization_fixture_v1",
    "model_role": "ocr_text_model",
    "subtype": "text_enhancement",
    "outputs": {
        "raw_text": "3 F 出 口",
        "normalized_text": "3F出口",
        "correction_applied": True,
    },
}

ADAPTER_STUB_IO_SAMPLE: Dict[str, Any] = {
    "sample_id": "ocr_text_adapter_stub_io_fixture_v1",
    "input_format": "RealFrameInputPackage[] + ObjectObservationCandidate[] + FieldGeometryCandidate optional",
    "output_format": "text/bbox/confidence/region candidate-shaped dicts",
    "execution_mode": "adapter_stub",
}

CANDIDATE_MAPPING_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"model_output": "text", "target": "TextObservationCandidate", "status": "feasible"},
    {"model_output": "bbox", "target": "TextRegionCandidate", "status": "feasible"},
    {"model_output": "text_spatial_ref", "target": "TextAnchorCandidate", "status": "feasible"},
    {"model_output": "normalized_text", "target": "TextNormalizationCandidate", "status": "feasible"},
    {"model_output": "confidence", "target": "TextQualityCandidate", "status": "feasible"},
    {"model_output": "layout_block", "target": "TextLayoutCandidate", "status": "feasible"},
)

SMOKE_IO_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "ocr_local_adapter_available_smoke",
        "path": "P0",
        "inspect_subtype": "ocr",
        "availability_override": {"local_ocr_available": True, "local_weights_available": True, "dependencies_available": True},
        "expect_execution_mode": "local_real_model",
        "expect_smoke_completed": True,
    },
    {
        "case_id": "rapidocr_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "rapidocr",
        "availability_override": {"rapidocr_cached_output_available": True, "local_ocr_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "paddleocr_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "paddleocr",
        "availability_override": {"paddleocr_cached_output_available": True, "local_ocr_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "ocr_adapter_stub_io_inspection",
        "path": "P2",
        "inspect_subtype": "ocr",
        "availability_override": {
            "adapter_stub_available": True, "local_ocr_available": False,
            "rapidocr_cached_output_available": False, "paddleocr_cached_output_available": False,
            "text_region_cached_output_available": False,
        },
        "expect_execution_mode": "adapter_stub",
        "expect_mapping_feasible": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "text_region_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "text_region",
        "availability_override": {"text_region_cached_output_available": True, "local_text_region_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_region_output": True,
    },
    {
        "case_id": "missing_weight_blocked",
        "path": "P3",
        "availability_override": {"local_ocr_available": True, "local_weights_available": False},
        "expect_execution_mode": "blocked_by_missing_weight",
        "expect_no_download": True,
    },
    {
        "case_id": "missing_dependency_blocked",
        "path": "P3",
        "availability_override": {"local_ocr_available": True, "local_weights_available": True, "dependencies_available": False},
        "expect_execution_mode": "blocked_by_missing_dependency",
        "expect_no_download": True,
    },
    {
        "case_id": "text_observation_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "rapidocr",
        "availability_override": {"rapidocr_cached_output_available": True},
        "expect_mapping_target": "TextObservationCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "text_region_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "text_region",
        "availability_override": {"text_region_cached_output_available": True},
        "expect_mapping_target": "TextRegionCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "text_anchor_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "paddleocr",
        "availability_override": {"paddleocr_cached_output_available": True},
        "expect_mapping_target": "TextAnchorCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "text_normalization_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "text_enhancement",
        "availability_override": {"rapidocr_cached_output_available": True},
        "expect_mapping_target": "TextNormalizationCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "traceability_preserved",
        "path": "P1",
        "inspect_subtype": "rapidocr",
        "availability_override": {"rapidocr_cached_output_available": True},
        "expect_traceability": True,
    },
    {
        "case_id": "cached_output_not_marked_as_real_run",
        "path": "P1",
        "inspect_subtype": "rapidocr",
        "availability_override": {"rapidocr_cached_output_available": True},
        "expect_cached_not_real": True,
    },
    {
        "case_id": "adapter_stub_not_marked_as_real_run",
        "path": "P2",
        "inspect_subtype": "ocr",
        "availability_override": {
            "adapter_stub_available": True, "local_ocr_available": False,
            "rapidocr_cached_output_available": False, "paddleocr_cached_output_available": False,
            "text_region_cached_output_available": False,
        },
        "expect_stub_not_real": True,
    },
    {
        "case_id": "no_new_protocol_without_reason",
        "path": "P2",
        "availability_override": {
            "adapter_stub_available": True, "local_ocr_available": False,
            "rapidocr_cached_output_available": False, "paddleocr_cached_output_available": False,
            "text_region_cached_output_available": False,
        },
        "expect_new_protocol": False,
    },
)
