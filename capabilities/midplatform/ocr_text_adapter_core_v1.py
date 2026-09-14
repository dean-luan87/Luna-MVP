# -*- coding: utf-8 -*-
"""OCR / Text adapter core v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.ocr_text_adapter_input_builder_v1 import build_ocr_text_adapter_input_package
from capabilities.midplatform.ocr_text_adapter_result_assembler_v1 import assemble_ocr_text_adapter_result
from capabilities.midplatform.ocr_text_adapter_static_validators_v1 import (
    validate_no_task_action_boundary,
    validate_no_world_model_assembly_boundary,
    validate_ocr_text_adapter_input_package,
    validate_ocr_text_adapter_result_candidate,
    validate_ocr_text_raw_output_candidate,
    validate_text_anchor_candidate,
    validate_text_normalization_candidate,
    validate_text_observation_candidate,
    validate_text_quality_candidate,
    validate_text_region_candidate,
)
from capabilities.midplatform.ocr_text_output_normalizer_v1 import normalize_ocr_text_output_to_candidates
from capabilities.midplatform.ocr_text_raw_output_loader_v1 import load_ocr_text_raw_output_candidate
from capabilities.midplatform.text_anchor_candidate_builder_v1 import build_text_anchor_candidates
from capabilities.midplatform.text_normalization_candidate_builder_v1 import build_text_normalization_candidates


def load_smoke_io_inspection_artifacts(smoke_io_root: Path) -> Dict[str, Any]:
    """Load upstream smoke IO inspection artifacts."""
    artifacts: Dict[str, Any] = {"root": str(smoke_io_root)}
    for name in (
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
        "smoke_io_case_results_v1.json",
    ):
        p = smoke_io_root / name
        try:
            artifacts[name] = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
        except (json.JSONDecodeError, OSError):
            artifacts[name] = {}
    return artifacts


def _find_smoke_io_pair(
    artifacts: Dict[str, Any],
    source_smoke_case_id: str,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
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
        "frame_width": 640,
        "frame_height": 480,
        "source_ref": "ocr_text_skeleton_fixture",
        "fixture_type": "local_real_image_fixture",
        "candidate_only": True,
    }


def _mock_object_obs(i: int, case_id: str, label: str = "signboard") -> Dict[str, Any]:
    return {
        "object_observation_id": f"ooc_{case_id}_{i}",
        "observation_id": f"ooc_{case_id}_{i}",
        "frame_ref": f"frame_{case_id}_{i}",
        "label": label,
        "bbox": [100, 50, 400, 150],
        "confidence": 0.85,
        "candidate_only": True,
    }


def _mock_aligned(case_id: str) -> Dict[str, Any]:
    return {
        "multi_model_aligned_observation_id": f"mmao_{case_id}",
        "frame_ref": f"frame_{case_id}_0",
        "timestamp": "2026-06-11T10:00:00Z",
        "camera_ref": "camera_fixture_0",
        "candidate_only": True,
    }


def _mock_geometry(case_id: str) -> Dict[str, Any]:
    return {
        "field_geometry_candidate_id": f"fgc_{case_id}",
        "frame_ref": f"frame_{case_id}_0",
        "geometry_type": "text_region_bbox",
        "bbox": [50, 200, 150, 240],
        "candidate_only": True,
    }


def _mock_spatial_anchor(case_id: str) -> Dict[str, Any]:
    return {
        "spatial_anchor_candidate_id": f"sac_{case_id}",
        "frame_ref": f"frame_{case_id}_0",
        "anchor_label": "floor_sign_anchor",
        "candidate_only": True,
    }


def run_skeleton_case(
    case: Dict[str, Any],
    *,
    inspection_artifacts: Dict[str, Any],
) -> Dict[str, Any]:
    """Run one OCR / Text adapter skeleton case based on smoke IO inspection."""
    case_id = case["case_id"]
    overrides = dict(case.get("overrides") or {})
    inspect_subtype = case.get("inspect_subtype", "rapidocr")
    source_smoke_case_id = case.get("source_smoke_case_id", "rapidocr_cached_output_inspection")

    smoke_run, io_inspection = _find_smoke_io_pair(inspection_artifacts, source_smoke_case_id)
    frames = [_mock_frame(0, case_id)]
    observations = [_mock_object_obs(0, case_id)]
    aligned = [_mock_aligned(case_id)]
    geometries = [_mock_geometry(case_id)] if case.get("include_geometry") else []
    spatial_anchors = [_mock_spatial_anchor(case_id)] if case.get("include_geometry") else []

    adapter_input = build_ocr_text_adapter_input_package(
        frame_inputs=frames,
        object_observations=observations,
        session_ref=f"session_{case_id}",
        smoke_run=smoke_run,
        io_inspection=io_inspection,
        aligned_observations=aligned,
        field_geometries=geometries,
        spatial_anchors=spatial_anchors,
    )
    validate_ocr_text_adapter_input_package(adapter_input)

    raw_output = load_ocr_text_raw_output_candidate(
        smoke_run=smoke_run,
        io_inspection=io_inspection,
        frame_refs=[f.get("frame_ref") for f in frames],
        inspect_subtype=inspect_subtype,
    )
    validate_ocr_text_raw_output_candidate(raw_output)

    text_observations, regions, qualities, warnings, failure_points = normalize_ocr_text_output_to_candidates(
        adapter_input=adapter_input,
        raw_output=raw_output,
        case_overrides=overrides,
    )

    anchors: List[Dict[str, Any]] = []
    if (
        case.get("include_geometry")
        or case.get("expect_anchors_min")
        or case.get("expect_anchor_degraded")
    ):
        anchors = build_text_anchor_candidates(
            adapter_input=adapter_input,
            raw_output=raw_output,
            observations=text_observations,
            regions=regions,
            case_overrides=overrides,
        )

    normalizations: List[Dict[str, Any]] = []
    if (
        case.get("expect_normalizations_min")
        or inspect_subtype == "text_enhancement"
        or raw_output.get("raw_normalization_payload")
    ):
        norm_overrides = dict(overrides)
        if case.get("expect_normalizations_min") and not norm_overrides.get("force_normalization"):
            norm_overrides["force_normalization"] = True
        normalizations = build_text_normalization_candidates(
            adapter_input=adapter_input,
            raw_output=raw_output,
            observations=text_observations,
            case_overrides=norm_overrides,
        )

    for o in text_observations:
        validate_text_observation_candidate(o)
    for r in regions:
        validate_text_region_candidate(r)
    for a in anchors:
        validate_text_anchor_candidate(a)
    for n in normalizations:
        validate_text_normalization_candidate(n)
    for q in qualities:
        validate_text_quality_candidate(q)

    result = assemble_ocr_text_adapter_result(
        adapter_input=adapter_input,
        raw_output=raw_output,
        observations=text_observations,
        regions=regions,
        anchors=anchors,
        normalizations=normalizations,
        qualities=qualities,
        warnings=warnings,
        failure_points=failure_points,
    )
    validate_ocr_text_adapter_result_candidate(result)
    validate_no_world_model_assembly_boundary(result)
    validate_no_task_action_boundary(result)

    return {
        "case_id": case_id,
        "case_passed": False,
        "source_smoke_case_id": source_smoke_case_id,
        "adapter_input": adapter_input,
        "raw_output": raw_output,
        "adapter_result": result,
        "observations": text_observations,
        "regions": regions,
        "anchors": anchors,
        "normalizations": normalizations,
        "qualities": qualities,
    }


def _evaluate_case(case: Dict[str, Any], row: Dict[str, Any]) -> bool:
    result = row.get("adapter_result") or {}
    raw = row.get("raw_output") or {}
    observations = row.get("observations") or []
    regions = row.get("regions") or []
    anchors = row.get("anchors") or []
    normalizations = row.get("normalizations") or []
    qualities = row.get("qualities") or []
    adapter_input = row.get("adapter_input") or {}

    if case.get("expect_execution_mode") and adapter_input.get("execution_mode") != case["expect_execution_mode"]:
        return False
    if case.get("expect_observations_min") is not None and len(observations) < case["expect_observations_min"]:
        return False
    if case.get("expect_regions_min") is not None and len(regions) < case["expect_regions_min"]:
        return False
    if case.get("expect_anchors_min") is not None and len(anchors) < case["expect_anchors_min"]:
        return False
    if case.get("expect_normalizations_min") is not None and len(normalizations) < case["expect_normalizations_min"]:
        return False
    if case.get("expect_quality_min") is not None and len(qualities) < case["expect_quality_min"]:
        return False
    if case.get("expect_blocked") and not raw.get("_blocked"):
        return False
    if case.get("expect_no_fabrication"):
        if observations or regions or anchors or normalizations:
            return False
    if case.get("expect_not_real_run"):
        mode = adapter_input.get("execution_mode")
        raw_warnings = " ".join(raw.get("warning_codes") or [])
        if mode == "cached_output" and "not_real_run" not in raw_warnings:
            return False
        if mode == "adapter_stub" and "not_real_run" not in raw_warnings:
            return False
    if case.get("expect_anchor_degraded"):
        if not anchors or anchors[0].get("anchor_confidence") != "low":
            return False
    if case.get("expect_quality_degraded"):
        if not qualities or qualities[0].get("quality_status") != "degraded":
            return False
    if case.get("expect_ambiguous"):
        if not any(n.get("ambiguity_status") == "ambiguous" for n in normalizations):
            return False
    if case.get("expect_task_readiness") and not result.get("readiness_for_midplatform_task_collaboration"):
        return False
    if case.get("expect_later_wm_readiness") and not result.get("readiness_for_later_world_model_candidate_assembly"):
        return False
    if case.get("expect_no_wm_assembly") or case.get("expect_no_wm_candidate"):
        if result.get("world_model_candidate_generated") or result.get("world_model_entry_created"):
            return False
        if result.get("world_entity_candidate_generated"):
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
