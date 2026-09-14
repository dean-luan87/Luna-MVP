# -*- coding: utf-8 -*-
"""Segmentation / Mask adapter skeleton — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Segmentation-Mask-Task-Collaboration-Planning-v1-001"
SELECTED_NEXT_ROUTE = "Segmentation Mask Task Collaboration Planning"

PROHIBITED_SCOPE: Dict[str, Any] = {
    "prohibited": (
        "real_segmentation_execution", "model_download", "weight_download", "large_dependency_install",
        "camera_runtime", "video_stream_runtime", "field_simulation", "simulated_route",
        "task_reasoning", "task_action_output", "navigation_suggestion",
        "world_model_candidate_assembly", "world_model_entry_write", "world_entity_candidate_generation",
        "world_geometry_candidate_generation", "fact_admission", "new_protocol_without_reason",
        "production_runtime", "cached_output_as_real_run", "adapter_stub_as_real_run",
    ),
}

DO_NOT_MISCLASSIFY: Tuple[str, ...] = (
    "adapter_skeleton_based_on_smoke_io_inspection",
    "cached_output_not_real_model_run",
    "adapter_stub_not_real_model_run",
    "blocked_not_fabricated_output",
    "readiness_not_world_model_assembly",
    "freespace_not_navigation_permission",
)

PROTOCOL_REUSE_DECISION: Dict[str, Any] = {
    "decision_id": "protocol_reuse_decision_v1",
    "new_protocol_added": False,
    "reuse_real_frame_input_package": True,
    "reuse_object_observation_candidate": True,
    "reuse_multi_model_aligned_observation_candidate": True,
    "reuse_enhanced_field_scene_candidate": True,
    "reuse_field_geometry_candidate": True,
    "reuse_text_region_candidate": True,
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
    {"output": "MaskObservationCandidate", "role": "future_entity_boundary_stability", "assembly": "deferred"},
    {"output": "FreeSpaceCandidate", "role": "future_passable_region", "assembly": "deferred"},
    {"output": "RegionObservationCandidate", "role": "future_spatial_region", "assembly": "deferred"},
    {"output": "ObjectBoundaryCandidate", "role": "future_geometry_boundary", "assembly": "deferred"},
)

TASK_COLLABORATION_MAPPING: Tuple[Dict[str, Any], ...] = (
    {
        "scenario": "navigation_passability",
        "models": ("YOLO", "Depth_Geometry", "Segmentation_Mask"),
        "segmentation_outputs": ("FreeSpaceCandidate", "MaskObservationCandidate", "RegionObservationCandidate", "MaskQualityCandidate"),
    },
    {
        "scenario": "obstacle_avoidance_context",
        "models": ("YOLO", "Depth_Geometry", "Segmentation_Mask"),
        "segmentation_outputs": ("ObjectBoundaryCandidate", "MaskObservationCandidate", "RegionObservationCandidate"),
    },
    {
        "scenario": "door_area_detection",
        "models": ("YOLO", "Segmentation_Mask", "Depth_optional"),
        "segmentation_outputs": ("RegionObservationCandidate", "ObjectBoundaryCandidate", "FreeSpaceCandidate"),
    },
    {
        "scenario": "object_interaction_boundary",
        "models": ("YOLO", "Segmentation_Mask", "Depth_optional"),
        "segmentation_outputs": ("ObjectBoundaryCandidate", "MaskObservationCandidate", "MaskQualityCandidate"),
    },
)

SMOKE_IO_ARTIFACT_FILES: Tuple[str, ...] = (
    "segmentation_mask_model_smoke_io_inspection_report_v1.json",
    "model_smoke_run_candidate_registry_v1.json",
    "model_io_inspection_candidate_registry_v1.json",
    "model_candidate_mapping_feasibility_registry_v1.json",
    "segmentation_mask_available_model_review_v1.json",
    "segmentation_mask_input_format_review_v1.json",
    "segmentation_mask_output_format_review_v1.json",
    "segmentation_mask_failure_point_review_v1.json",
    "segmentation_mask_candidate_mapping_review_v1.json",
    "model_execution_authorization_review_v1.json",
    "new_protocol_reason_required_report_v1.json",
)

_STUB_OVERRIDE: Dict[str, Any] = {
    "adapter_stub_available": True, "local_segmentation_available": False,
    "grounded_sam_cached_output_available": False, "sam_cached_output_available": False,
    "freespace_cached_output_available": False,
}

SKELETON_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "mask_observation_from_grounded_sam_cached_output",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "expect_masks_min": 1,
        "expect_execution_mode": "cached_output",
        "expect_not_real_run": True,
    },
    {
        "case_id": "mask_observation_from_sam_cached_output",
        "source_smoke_case_id": "sam_cached_output_inspection",
        "inspect_subtype": "sam",
        "expect_masks_min": 1,
        "expect_execution_mode": "cached_output",
    },
    {
        "case_id": "freespace_from_cached_output",
        "source_smoke_case_id": "freespace_cached_output_inspection",
        "inspect_subtype": "freespace",
        "expect_freespace_min": 1,
        "expect_execution_mode": "cached_output",
    },
    {
        "case_id": "mask_from_adapter_stub",
        "source_smoke_case_id": "segmentation_adapter_stub_io_inspection",
        "inspect_subtype": "segmentation",
        "availability_override": dict(_STUB_OVERRIDE),
        "expect_masks_min": 1,
        "expect_execution_mode": "adapter_stub",
        "expect_not_real_run": True,
    },
    {
        "case_id": "object_boundary_from_polygon",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "expect_boundaries_min": 1,
    },
    {
        "case_id": "object_boundary_without_object_ref_degraded",
        "source_smoke_case_id": "sam_cached_output_inspection",
        "inspect_subtype": "sam",
        "overrides": {"no_object_ref": True},
        "expect_boundaries_min": 1,
        "expect_boundary_degraded": True,
    },
    {
        "case_id": "freespace_without_geometry_degraded",
        "source_smoke_case_id": "freespace_cached_output_inspection",
        "inspect_subtype": "freespace",
        "overrides": {"no_geometry_ref": True},
        "expect_freespace_min": 1,
        "expect_freespace_degraded": True,
    },
    {
        "case_id": "region_observation_from_label",
        "source_smoke_case_id": "region_label_mapping_feasibility",
        "inspect_subtype": "freespace",
        "expect_regions_min": 1,
    },
    {
        "case_id": "mask_quality_from_cached_output",
        "source_smoke_case_id": "mask_quality_mapping_feasibility",
        "inspect_subtype": "grounded_sam",
        "expect_quality_min": 1,
    },
    {
        "case_id": "prompt_dependency_degrades_quality",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "overrides": {"prompt_dependency_high": True},
        "expect_quality_degraded": True,
    },
    {
        "case_id": "low_confidence_mask_degraded",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "overrides": {"low_confidence": True, "confidence": 0.35},
        "expect_quality_degraded": True,
    },
    {
        "case_id": "blocked_missing_weight_no_output_fabrication",
        "source_smoke_case_id": "missing_weight_blocked",
        "inspect_subtype": "segmentation",
        "expect_blocked": True,
        "expect_no_fabrication": True,
    },
    {
        "case_id": "blocked_missing_dependency_no_output_fabrication",
        "source_smoke_case_id": "missing_dependency_blocked",
        "inspect_subtype": "segmentation",
        "expect_blocked": True,
        "expect_no_fabrication": True,
    },
    {
        "case_id": "readiness_for_task_collaboration_true",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "expect_task_readiness": True,
    },
    {
        "case_id": "readiness_for_later_world_model_candidate_assembly_true",
        "source_smoke_case_id": "freespace_cached_output_inspection",
        "inspect_subtype": "freespace",
        "include_geometry": True,
        "expect_later_wm_readiness": True,
        "expect_no_wm_assembly": True,
    },
    {
        "case_id": "no_new_protocol_created",
        "source_smoke_case_id": "no_new_protocol_without_reason",
        "inspect_subtype": "segmentation",
        "availability_override": dict(_STUB_OVERRIDE),
        "expect_new_protocol": False,
    },
    {
        "case_id": "no_action_output",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "expect_no_action": True,
    },
    {
        "case_id": "no_world_model_assembly",
        "source_smoke_case_id": "grounded_sam_cached_output_inspection",
        "inspect_subtype": "grounded_sam",
        "expect_no_wm_candidate": True,
    },
)
