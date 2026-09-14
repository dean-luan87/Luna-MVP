# -*- coding: utf-8 -*-
"""Segmentation / Mask adapter core v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.freespace_candidate_builder_v1 import build_freespace_candidates
from capabilities.midplatform.object_boundary_candidate_builder_v1 import build_object_boundary_candidates
from capabilities.midplatform.segmentation_mask_adapter_input_builder_v1 import build_segmentation_mask_adapter_input_package
from capabilities.midplatform.segmentation_mask_adapter_result_assembler_v1 import assemble_segmentation_mask_adapter_result
from capabilities.midplatform.segmentation_mask_adapter_static_validators_v1 import (
    validate_freespace_candidate,
    validate_mask_observation_candidate,
    validate_mask_quality_candidate,
    validate_no_task_action_boundary,
    validate_no_world_model_assembly_boundary,
    validate_object_boundary_candidate,
    validate_region_observation_candidate,
    validate_segmentation_mask_adapter_input_package,
    validate_segmentation_mask_adapter_result_candidate,
    validate_segmentation_mask_raw_output_candidate,
)
from capabilities.midplatform.segmentation_mask_output_normalizer_v1 import normalize_segmentation_mask_output_to_candidates
from capabilities.midplatform.segmentation_mask_raw_output_loader_v1 import load_segmentation_mask_raw_output_candidate


def load_smoke_io_inspection_artifacts(smoke_io_root: Path) -> Dict[str, Any]:
    artifacts: Dict[str, Any] = {"root": str(smoke_io_root)}
    for name in (
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
        "smoke_io_case_results_v1.json",
    ):
        p = smoke_io_root / name
        try:
            artifacts[name] = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
        except (json.JSONDecodeError, OSError):
            artifacts[name] = {}
    return artifacts


def _find_smoke_io_pair(artifacts: Dict[str, Any], source_smoke_case_id: str) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    case_results = (artifacts.get("smoke_io_case_results_v1.json") or {}).get("results") or []
    smoke_runs = (artifacts.get("model_smoke_run_candidate_registry_v1.json") or {}).get("candidates") or []
    io_inspections = (artifacts.get("model_io_inspection_candidate_registry_v1.json") or {}).get("candidates") or []
    idx = next((i for i, r in enumerate(case_results) if r.get("case_id") == source_smoke_case_id), 0)
    smoke_run = smoke_runs[idx] if idx < len(smoke_runs) else (smoke_runs[0] if smoke_runs else {})
    io_inspection = io_inspections[idx] if idx < len(io_inspections) else (io_inspections[0] if io_inspections else {})
    return smoke_run, io_inspection


def _mock_frame(i: int, case_id: str) -> Dict[str, Any]:
    return {
        "frame_input_id": f"rfi_{case_id}_{i}",
        "frame_ref": f"frame_{case_id}_{i}",
        "timestamp": f"2026-06-11T10:00:{i:02d}Z",
        "frame_width": 640, "frame_height": 480,
        "source_ref": "segmentation_mask_skeleton_fixture",
        "fixture_type": "local_real_image_fixture", "candidate_only": True,
    }


def _mock_object_obs(i: int, case_id: str, label: str = "obstacle") -> Dict[str, Any]:
    return {
        "object_observation_id": f"ooc_{case_id}_{i}",
        "observation_id": f"ooc_{case_id}_{i}",
        "frame_ref": f"frame_{case_id}_{i}",
        "label": label, "bbox": [80, 60, 320, 280], "confidence": 0.85, "candidate_only": True,
    }


def _mock_aligned(case_id: str) -> Dict[str, Any]:
    return {
        "multi_model_aligned_observation_id": f"mmao_{case_id}",
        "frame_ref": f"frame_{case_id}_0", "timestamp": "2026-06-11T10:00:00Z",
        "camera_ref": "camera_fixture_0", "candidate_only": True,
    }


def _mock_geometry(case_id: str) -> Dict[str, Any]:
    return {
        "field_geometry_candidate_id": f"fgc_{case_id}",
        "frame_ref": f"frame_{case_id}_0", "geometry_type": "freespace_polygon",
        "bbox": [0, 200, 640, 480], "candidate_only": True,
    }


def run_skeleton_case(case: Dict[str, Any], *, inspection_artifacts: Dict[str, Any]) -> Dict[str, Any]:
    case_id = case["case_id"]
    overrides = dict(case.get("overrides") or {})
    inspect_subtype = case.get("inspect_subtype", "grounded_sam")
    source_smoke_case_id = case.get("source_smoke_case_id", "grounded_sam_cached_output_inspection")
    no_object = overrides.get("no_object_ref", False)

    smoke_run, io_inspection = _find_smoke_io_pair(inspection_artifacts, source_smoke_case_id)
    frames = [_mock_frame(0, case_id)]
    observations = [] if no_object else [_mock_object_obs(0, case_id)]
    aligned = [_mock_aligned(case_id)]
    geometries = [_mock_geometry(case_id)] if case.get("include_geometry") else []

    adapter_input = build_segmentation_mask_adapter_input_package(
        frame_inputs=frames,
        object_observations=observations,
        session_ref=f"session_{case_id}",
        smoke_run=smoke_run,
        io_inspection=io_inspection,
        aligned_observations=aligned,
        field_geometries=geometries,
    )
    validate_segmentation_mask_adapter_input_package(adapter_input)

    raw_output = load_segmentation_mask_raw_output_candidate(
        smoke_run=smoke_run, io_inspection=io_inspection,
        frame_refs=[f.get("frame_ref") for f in frames],
        inspect_subtype=inspect_subtype,
    )
    validate_segmentation_mask_raw_output_candidate(raw_output)

    masks, regions, qualities, warnings, failure_points = normalize_segmentation_mask_output_to_candidates(
        adapter_input=adapter_input, raw_output=raw_output, case_overrides=overrides,
    )

    boundaries = build_object_boundary_candidates(
        adapter_input=adapter_input, raw_output=raw_output, masks=masks, case_overrides=overrides,
    ) if case.get("expect_boundaries_min") or inspect_subtype in ("grounded_sam", "sam") else []

    freespaces = build_freespace_candidates(
        adapter_input=adapter_input, raw_output=raw_output, case_overrides=overrides,
    ) if case.get("expect_freespace_min") or inspect_subtype == "freespace" else []

    for m in masks:
        validate_mask_observation_candidate(m)
    for b in boundaries:
        validate_object_boundary_candidate(b)
    for f in freespaces:
        validate_freespace_candidate(f)
    for r in regions:
        validate_region_observation_candidate(r)
    for q in qualities:
        validate_mask_quality_candidate(q)

    result = assemble_segmentation_mask_adapter_result(
        adapter_input=adapter_input, raw_output=raw_output,
        masks=masks, boundaries=boundaries, freespaces=freespaces,
        regions=regions, qualities=qualities, warnings=warnings, failure_points=failure_points,
    )
    validate_segmentation_mask_adapter_result_candidate(result)
    validate_no_world_model_assembly_boundary(result)
    validate_no_task_action_boundary(result)

    return {
        "case_id": case_id, "case_passed": False, "source_smoke_case_id": source_smoke_case_id,
        "adapter_input": adapter_input, "raw_output": raw_output, "adapter_result": result,
        "masks": masks, "boundaries": boundaries, "freespaces": freespaces,
        "regions": regions, "qualities": qualities,
    }


def _evaluate_case(case: Dict[str, Any], row: Dict[str, Any]) -> bool:
    result = row.get("adapter_result") or {}
    raw = row.get("raw_output") or {}
    masks = row.get("masks") or []
    boundaries = row.get("boundaries") or []
    freespaces = row.get("freespaces") or []
    regions = row.get("regions") or []
    qualities = row.get("qualities") or []
    adapter_input = row.get("adapter_input") or {}

    if case.get("expect_execution_mode") and adapter_input.get("execution_mode") != case["expect_execution_mode"]:
        return False
    if case.get("expect_masks_min") is not None and len(masks) < case["expect_masks_min"]:
        return False
    if case.get("expect_boundaries_min") is not None and len(boundaries) < case["expect_boundaries_min"]:
        return False
    if case.get("expect_freespace_min") is not None and len(freespaces) < case["expect_freespace_min"]:
        return False
    if case.get("expect_regions_min") is not None and len(regions) < case["expect_regions_min"]:
        return False
    if case.get("expect_quality_min") is not None and len(qualities) < case["expect_quality_min"]:
        return False
    if case.get("expect_blocked") and not raw.get("_blocked"):
        return False
    if case.get("expect_no_fabrication"):
        if masks or boundaries or freespaces or regions:
            return False
    if case.get("expect_not_real_run"):
        mode = adapter_input.get("execution_mode")
        raw_warnings = " ".join(raw.get("warning_codes") or [])
        if mode == "cached_output" and "not_real_run" not in raw_warnings:
            return False
        if mode == "adapter_stub" and "not_real_run" not in raw_warnings:
            return False
    if case.get("expect_boundary_degraded"):
        if not boundaries or boundaries[0].get("boundary_confidence") != "low":
            return False
    if case.get("expect_freespace_degraded"):
        if not freespaces or freespaces[0].get("passability_confidence") != "low":
            return False
    if case.get("expect_quality_degraded"):
        if not qualities or qualities[0].get("quality_status") != "degraded":
            return False
    if case.get("expect_task_readiness") and not result.get("readiness_for_midplatform_task_collaboration"):
        return False
    if case.get("expect_later_wm_readiness") and not result.get("readiness_for_later_world_model_candidate_assembly"):
        return False
    if case.get("expect_no_wm_assembly") or case.get("expect_no_wm_candidate"):
        if result.get("world_model_candidate_generated") or result.get("world_model_entry_created"):
            return False
        if result.get("world_entity_candidate_generated") or result.get("world_geometry_candidate_generated"):
            return False
    if case.get("expect_no_action"):
        if result.get("task_action_output") or result.get("navigation_suggestion_output"):
            return False
    if case.get("expect_new_protocol") is False:
        return True
    return True


def run_all_skeleton_cases(
    cases: Tuple[Dict[str, Any], ...],
    *,
    inspection_artifacts: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    for case in cases:
        row = run_skeleton_case(case, inspection_artifacts=inspection_artifacts)
        row["case_passed"] = _evaluate_case(case, row)
        results.append(row)
        if not row.get("case_passed"):
            all_passed = False
    return results, all_passed
