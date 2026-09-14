# -*- coding: utf-8 -*-
"""Segmentation / Mask Model smoke IO inspection — items v1."""

from __future__ import annotations

from typing import Any, Dict, Tuple

SELECTED_NEXT_PHASE = "Phase-Midplatform-Segmentation-Mask-Adapter-Skeleton-v1-001"
SELECTED_NEXT_ROUTE = "Segmentation Mask Adapter Skeleton"

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

DEFAULT_SEGMENTATION_MASK_AVAILABILITY: Dict[str, Any] = {
    "matrix_id": "segmentation_mask_availability_matrix_v1",
    "local_segmentation_available": False,
    "local_freespace_available": False,
    "local_weights_available": False,
    "dependencies_available": False,
    "grounded_sam_cached_output_available": True,
    "sam_cached_output_available": True,
    "freespace_cached_output_available": True,
    "adapter_stub_available": True,
    "model_download_authorized": False,
    "weight_download_authorized": False,
    "camera_runtime_authorized": False,
    "video_stream_authorized": False,
    "no_unauthorized_download": True,
}

CACHED_GROUNDED_SAM_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_grounded_sam_output_fixture_v1",
    "model_role": "segmentation_mask_model",
    "subtype": "grounded_sam",
    "outputs": {
        "mask_ref": "mask_gsam_fixture_001",
        "bbox": [80, 60, 320, 280],
        "polygon": [[80, 60], [320, 60], [320, 280], [80, 280]],
        "confidence": 0.89,
        "label": "person",
    },
}

CACHED_SAM_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_sam_output_fixture_v1",
    "model_role": "segmentation_mask_model",
    "subtype": "sam",
    "outputs": {
        "mask": "mask_sam_fixture_001",
        "bbox": [50, 40, 200, 180],
        "polygon": [[50, 40], [200, 40], [200, 180], [50, 180]],
        "mask_quality": 0.86,
        "confidence": 0.86,
    },
}

CACHED_FREESPACE_OUTPUT_SAMPLE: Dict[str, Any] = {
    "sample_id": "cached_freespace_output_fixture_v1",
    "model_role": "segmentation_mask_model",
    "subtype": "freespace",
    "outputs": {
        "free_space_mask": "freespace_mask_fixture_001",
        "passable_area": [[0, 200], [640, 200], [640, 480], [0, 480]],
        "region_label": "walkable_floor",
        "region_type": "floor",
        "confidence": 0.84,
    },
}

ADAPTER_STUB_IO_SAMPLE: Dict[str, Any] = {
    "sample_id": "segmentation_mask_adapter_stub_io_fixture_v1",
    "input_format": "RealFrameInputPackage[] + ObjectObservationCandidate[] + FieldGeometryCandidate optional + TextRegionCandidate optional",
    "output_format": "mask/polygon/bbox/confidence/region candidate-shaped dicts",
    "execution_mode": "adapter_stub",
}

CANDIDATE_MAPPING_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"model_output": "mask", "target": "MaskObservationCandidate", "status": "feasible"},
    {"model_output": "polygon", "target": "ObjectBoundaryCandidate", "status": "feasible"},
    {"model_output": "free_space", "target": "FreeSpaceCandidate", "status": "feasible"},
    {"model_output": "region_label", "target": "RegionObservationCandidate", "status": "feasible"},
    {"model_output": "confidence", "target": "MaskQualityCandidate", "status": "feasible"},
)

_STUB_OVERRIDE: Dict[str, Any] = {
    "adapter_stub_available": True, "local_segmentation_available": False,
    "grounded_sam_cached_output_available": False, "sam_cached_output_available": False,
    "freespace_cached_output_available": False,
}

SMOKE_IO_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "segmentation_local_adapter_available_smoke",
        "path": "P0",
        "inspect_subtype": "segmentation",
        "availability_override": {"local_segmentation_available": True, "local_weights_available": True, "dependencies_available": True},
        "expect_execution_mode": "local_real_model",
        "expect_smoke_completed": True,
    },
    {
        "case_id": "grounded_sam_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "grounded_sam",
        "availability_override": {"grounded_sam_cached_output_available": True, "local_segmentation_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "sam_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "sam",
        "availability_override": {"sam_cached_output_available": True, "local_segmentation_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "segmentation_adapter_stub_io_inspection",
        "path": "P2",
        "inspect_subtype": "segmentation",
        "availability_override": dict(_STUB_OVERRIDE),
        "expect_execution_mode": "adapter_stub",
        "expect_mapping_feasible": True,
        "expect_not_real_run": True,
    },
    {
        "case_id": "freespace_cached_output_inspection",
        "path": "P1",
        "inspect_subtype": "freespace",
        "availability_override": {"freespace_cached_output_available": True, "local_freespace_available": False},
        "expect_execution_mode": "cached_output",
        "expect_parseable": True,
        "expect_freespace_output": True,
    },
    {
        "case_id": "missing_weight_blocked",
        "path": "P3",
        "availability_override": {"local_segmentation_available": True, "local_weights_available": False},
        "expect_execution_mode": "blocked_by_missing_weight",
        "expect_no_download": True,
    },
    {
        "case_id": "missing_dependency_blocked",
        "path": "P3",
        "availability_override": {"local_segmentation_available": True, "local_weights_available": True, "dependencies_available": False},
        "expect_execution_mode": "blocked_by_missing_dependency",
        "expect_no_download": True,
    },
    {
        "case_id": "mask_observation_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "grounded_sam",
        "availability_override": {"grounded_sam_cached_output_available": True},
        "expect_mapping_target": "MaskObservationCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "object_boundary_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "sam",
        "availability_override": {"sam_cached_output_available": True},
        "expect_mapping_target": "ObjectBoundaryCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "freespace_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "freespace",
        "availability_override": {"freespace_cached_output_available": True},
        "expect_mapping_target": "FreeSpaceCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "region_label_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "freespace",
        "availability_override": {"freespace_cached_output_available": True},
        "expect_mapping_target": "RegionObservationCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "mask_quality_mapping_feasibility",
        "path": "P1",
        "inspect_subtype": "grounded_sam",
        "availability_override": {"grounded_sam_cached_output_available": True},
        "expect_mapping_target": "MaskQualityCandidate",
        "expect_mapping_status": "feasible",
    },
    {
        "case_id": "traceability_preserved",
        "path": "P1",
        "inspect_subtype": "grounded_sam",
        "availability_override": {"grounded_sam_cached_output_available": True},
        "expect_traceability": True,
    },
    {
        "case_id": "cached_output_not_marked_as_real_run",
        "path": "P1",
        "inspect_subtype": "grounded_sam",
        "availability_override": {"grounded_sam_cached_output_available": True},
        "expect_cached_not_real": True,
    },
    {
        "case_id": "adapter_stub_not_marked_as_real_run",
        "path": "P2",
        "inspect_subtype": "segmentation",
        "availability_override": dict(_STUB_OVERRIDE),
        "expect_stub_not_real": True,
    },
    {
        "case_id": "no_new_protocol_without_reason",
        "path": "P2",
        "inspect_subtype": "segmentation",
        "availability_override": dict(_STUB_OVERRIDE),
        "expect_new_protocol": False,
    },
)
