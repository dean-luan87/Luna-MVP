# -*- coding: utf-8 -*-
"""OCR / Text adapter types v1."""

from __future__ import annotations

from typing import Dict, Tuple

ADAPTER_INPUT_FIELDS: Tuple[str, ...] = (
    "adapter_input_id", "model_role", "model_ref", "execution_mode", "smoke_run_ref",
    "io_inspection_ref", "frame_input_refs", "object_observation_refs",
    "aligned_observation_refs", "enhanced_field_scene_refs", "field_geometry_refs",
    "spatial_anchor_refs", "session_ref", "authorization_ref", "source_refs",
    "traceability_refs", "candidate_only",
)

RAW_OUTPUT_FIELDS: Tuple[str, ...] = (
    "raw_output_id", "source_smoke_run_ref", "source_io_inspection_ref", "model_ref",
    "execution_mode", "frame_refs", "timestamp_range", "output_payload_type",
    "raw_text_payload", "raw_region_payload", "raw_layout_payload",
    "raw_normalization_payload", "raw_quality_payload", "parseability_status",
    "warning_codes", "missing_information", "source_refs", "traceability_refs", "candidate_only",
)

TEXT_OBSERVATION_FIELDS: Tuple[str, ...] = (
    "text_observation_candidate_id", "source_raw_output_ref", "frame_ref", "timestamp",
    "text", "normalized_text", "language_hint", "confidence", "source_region_ref",
    "reading_order_index", "text_type_hint", "warning_codes", "missing_information",
    "source_refs", "evidence_refs", "traceability_refs", "candidate_only",
)

TEXT_REGION_FIELDS: Tuple[str, ...] = (
    "text_region_candidate_id", "source_raw_output_ref", "frame_ref", "bbox", "polygon",
    "region_type", "region_confidence", "associated_object_observation_refs",
    "associated_geometry_refs", "reading_order_index", "warning_codes", "missing_information",
    "source_refs", "evidence_refs", "traceability_refs", "candidate_only",
)

TEXT_ANCHOR_FIELDS: Tuple[str, ...] = (
    "text_anchor_candidate_id", "source_text_observation_ref", "source_text_region_ref",
    "associated_spatial_anchor_refs", "associated_field_geometry_refs", "anchor_text",
    "normalized_anchor_text", "anchor_type", "anchor_confidence", "spatial_reliability",
    "observation_count", "warning_codes", "missing_information", "source_refs",
    "evidence_refs", "traceability_refs", "candidate_only",
)

TEXT_NORMALIZATION_FIELDS: Tuple[str, ...] = (
    "text_normalization_candidate_id", "source_text_observation_ref", "original_text",
    "normalized_text", "normalization_method", "correction_confidence", "ambiguity_status",
    "alternatives", "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

TEXT_QUALITY_FIELDS: Tuple[str, ...] = (
    "text_quality_candidate_id", "source_raw_output_ref", "recognition_quality",
    "region_quality", "layout_quality", "normalization_quality", "blur_risk",
    "occlusion_risk", "orientation_risk", "quality_status", "blockers", "warnings",
    "source_refs", "traceability_refs", "candidate_only",
)

ADAPTER_RESULT_FIELDS: Tuple[str, ...] = (
    "adapter_result_id", "adapter_input_ref", "smoke_run_ref", "io_inspection_ref",
    "execution_mode", "text_observation_candidates", "text_region_candidates",
    "text_anchor_candidates", "text_normalization_candidates", "text_quality_candidates",
    "accepted_output_count", "rejected_output_count", "missing_information",
    "warning_summary", "conflict_summary", "readiness_for_midplatform_task_collaboration",
    "readiness_for_later_world_model_candidate_assembly", "non_execution_flags",
    "source_refs", "traceability_refs", "candidate_only",
)

EXECUTION_MODES: Tuple[str, ...] = (
    "local_real_model", "local_adapter", "cached_output", "adapter_stub",
    "blocked_by_authorization", "blocked_by_missing_dependency", "blocked_by_missing_weight",
    "failed_runtime_error",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "no_real_ocr_execution": True,
    "no_model_download": True,
    "no_weight_download": True,
    "no_camera_runtime": True,
    "no_video_stream_runtime": True,
    "no_field_simulation": True,
    "no_task_reasoning": True,
    "no_task_action_output": True,
    "no_navigation_suggestion": True,
    "no_world_model_assembly": True,
    "no_world_model_candidate_generated": True,
    "no_world_entity_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_llm_text_correction": True,
    "no_new_protocol_without_reason": True,
    "adapter_skeleton_only": True,
    "cached_output_not_marked_as_real_run": True,
    "adapter_stub_not_marked_as_real_run": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_OCR_TEXT_ADAPTER_SKELETON_READY_FOR_OCR_TEXT_TASK_COLLABORATION_PLANNING"
)
