# -*- coding: utf-8 -*-
"""Segmentation / Mask adapter types v1."""

from __future__ import annotations

from typing import Dict, Tuple

ADAPTER_INPUT_FIELDS: Tuple[str, ...] = (
    "adapter_input_id", "model_role", "model_ref", "execution_mode", "smoke_run_ref",
    "io_inspection_ref", "frame_input_refs", "object_observation_refs",
    "aligned_observation_refs", "enhanced_field_scene_refs", "field_geometry_refs",
    "text_region_refs", "prompt_refs", "session_ref", "authorization_ref", "source_refs",
    "traceability_refs", "candidate_only",
)

RAW_OUTPUT_FIELDS: Tuple[str, ...] = (
    "raw_output_id", "source_smoke_run_ref", "source_io_inspection_ref", "model_ref",
    "execution_mode", "frame_refs", "timestamp_range", "output_payload_type",
    "raw_mask_payload", "raw_polygon_payload", "raw_boundary_payload",
    "raw_freespace_payload", "raw_region_label_payload", "raw_quality_payload",
    "parseability_status", "warning_codes", "missing_information", "source_refs",
    "traceability_refs", "candidate_only",
)

MASK_OBSERVATION_FIELDS: Tuple[str, ...] = (
    "mask_observation_candidate_id", "source_raw_output_ref", "frame_ref", "timestamp",
    "mask_ref", "mask_encoding_type", "associated_object_observation_refs",
    "associated_text_region_refs", "label_hint", "mask_confidence", "mask_area_summary",
    "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

OBJECT_BOUNDARY_FIELDS: Tuple[str, ...] = (
    "object_boundary_candidate_id", "source_raw_output_ref", "frame_ref",
    "associated_object_observation_refs", "associated_mask_refs", "bbox", "polygon",
    "contour", "boundary_confidence", "boundary_quality", "warning_codes",
    "missing_information", "source_refs", "evidence_refs", "traceability_refs", "candidate_only",
)

FREESPACE_FIELDS: Tuple[str, ...] = (
    "freespace_candidate_id", "source_raw_output_ref", "frame_ref", "freespace_region_ref",
    "passable_area_polygon", "passable_area_mask_ref", "region_type", "passability_confidence",
    "geometry_refs", "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

REGION_OBSERVATION_FIELDS: Tuple[str, ...] = (
    "region_observation_candidate_id", "source_raw_output_ref", "frame_ref", "region_label",
    "region_ref", "bbox", "polygon", "associated_geometry_refs", "region_confidence",
    "region_quality", "warning_codes", "missing_information", "source_refs", "evidence_refs",
    "traceability_refs", "candidate_only",
)

MASK_QUALITY_FIELDS: Tuple[str, ...] = (
    "mask_quality_candidate_id", "source_raw_output_ref", "mask_quality", "boundary_quality",
    "freespace_quality", "region_label_quality", "occlusion_risk", "blur_risk",
    "prompt_dependency_risk", "quality_status", "blockers", "warnings", "source_refs",
    "traceability_refs", "candidate_only",
)

ADAPTER_RESULT_FIELDS: Tuple[str, ...] = (
    "adapter_result_id", "adapter_input_ref", "smoke_run_ref", "io_inspection_ref",
    "execution_mode", "mask_observation_candidates", "object_boundary_candidates",
    "freespace_candidates", "region_observation_candidates", "mask_quality_candidates",
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
    "no_real_segmentation_execution": True,
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
    "no_world_geometry_candidate_generated": True,
    "no_world_model_entry_write": True,
    "no_fact_admission": True,
    "no_new_protocol_without_reason": True,
    "adapter_skeleton_only": True,
    "cached_output_not_marked_as_real_run": True,
    "adapter_stub_not_marked_as_real_run": True,
}

FINAL_DECISION_GO = (
    "MIDPLATFORM_SEGMENTATION_MASK_ADAPTER_SKELETON_READY_FOR_SEGMENTATION_MASK_TASK_COLLABORATION_PLANNING"
)
