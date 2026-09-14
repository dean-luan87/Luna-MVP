# -*- coding: utf-8 -*-
"""SLAM spatial mapping adapter core v1 — based on smoke IO inspection."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.local_map_candidate_builder_v1 import (
    build_local_map_candidate,
    build_map_quality_candidate,
)
from capabilities.midplatform.slam_spatial_mapping_adapter_input_builder_v1 import (
    build_spatial_mapping_adapter_input_package,
)
from capabilities.midplatform.slam_spatial_mapping_adapter_static_validators_v1 import (
    validate_camera_pose_candidate,
    validate_local_map_candidate,
    validate_map_quality_candidate,
    validate_no_world_model_assembly_boundary,
    validate_spatial_anchor_candidate,
    validate_spatial_mapping_adapter_input_package,
    validate_spatial_mapping_adapter_result_candidate,
    validate_spatial_mapping_raw_output_candidate,
)
from capabilities.midplatform.spatial_anchor_candidate_builder_v1 import build_spatial_anchor_candidates
from capabilities.midplatform.spatial_mapping_adapter_result_assembler_v1 import (
    assemble_spatial_mapping_adapter_result,
)
from capabilities.midplatform.spatial_mapping_output_normalizer_v1 import (
    normalize_spatial_mapping_output_to_candidates,
)
from capabilities.midplatform.spatial_mapping_raw_output_loader_v1 import (
    load_spatial_mapping_raw_output_candidate,
)


def load_smoke_io_inspection_artifacts(smoke_io_root: Path) -> Dict[str, Any]:
    """Load upstream smoke IO inspection artifacts."""
    import json
    artifacts: Dict[str, Any] = {"root": str(smoke_io_root)}
    for name in (
        "slam_spatial_mapping_model_smoke_io_inspection_report_v1.json",
        "model_smoke_run_candidate_registry_v1.json",
        "model_io_inspection_candidate_registry_v1.json",
        "model_candidate_mapping_feasibility_registry_v1.json",
        "slam_spatial_mapping_available_model_review_v1.json",
        "slam_spatial_mapping_input_format_review_v1.json",
        "slam_spatial_mapping_output_format_review_v1.json",
        "slam_spatial_mapping_failure_point_review_v1.json",
        "slam_spatial_mapping_candidate_mapping_review_v1.json",
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
        "source_ref": "spatial_mapping_skeleton_fixture",
        "fixture_type": "local_real_image_fixture",
        "candidate_only": True,
    }


def _mock_scene(case_id: str, entity_label: str = "person") -> Dict[str, Any]:
    return {
        "field_scene_id": f"efs_{case_id}",
        "frame_ref": f"frame_{case_id}_0",
        "timestamp": "2026-06-11T10:00:00Z",
        "entity_candidates": [{
            "entity_id": f"ent_{case_id}",
            "observation_id": f"obs_{case_id}",
            "label": entity_label,
            "observation_count": 3,
        }],
        "zone_summary": {"total_entity_count": 1},
        "source_refs": [f"efs_{case_id}"],
        "traceability_refs": [f"frame_{case_id}_0"],
        "candidate_only": True,
    }


def run_skeleton_case(
    case: Dict[str, Any],
    *,
    inspection_artifacts: Dict[str, Any],
) -> Dict[str, Any]:
    """Run one adapter skeleton case based on smoke IO inspection."""
    case_id = case["case_id"]
    frame_count = case.get("frame_count", 1)
    overrides = dict(case.get("overrides") or {})
    entity_label = case.get("entity_label", "person")
    source_smoke_case_id = case.get("source_smoke_case_id", "slam_cached_output_inspection")

    smoke_run, io_inspection = _find_smoke_io_pair(inspection_artifacts, source_smoke_case_id)
    frames = [_mock_frame(i, case_id) for i in range(frame_count)]
    scenes = [_mock_scene(case_id, entity_label)] if frame_count >= 1 else []

    adapter_input = build_spatial_mapping_adapter_input_package(
        frame_inputs=frames,
        session_ref=f"session_{case_id}",
        smoke_run=smoke_run,
        io_inspection=io_inspection,
        enhanced_field_scenes=scenes,
    )
    validate_spatial_mapping_adapter_input_package(adapter_input)

    raw_output = load_spatial_mapping_raw_output_candidate(
        smoke_run=smoke_run,
        io_inspection=io_inspection,
        frame_refs=[f.get("frame_ref") for f in frames],
    )
    validate_spatial_mapping_raw_output_candidate(raw_output)

    poses, trajectories, warnings, failure_points = normalize_spatial_mapping_output_to_candidates(
        adapter_input=adapter_input,
        raw_output=raw_output,
        case_overrides=overrides,
    )
    anchors = build_spatial_anchor_candidates(
        adapter_input=adapter_input,
        raw_output=raw_output,
        poses=poses,
        case_overrides=overrides,
    )
    trajectory = trajectories[0] if trajectories else None
    local_map = build_local_map_candidate(
        adapter_input=adapter_input,
        raw_output=raw_output,
        poses=poses,
        anchors=anchors,
        trajectory=trajectory,
        case_overrides=overrides,
    )
    map_quality = build_map_quality_candidate(
        local_map=local_map,
        raw_output=raw_output,
        poses=poses,
        anchors=anchors,
        case_overrides=overrides,
    )

    for p in poses:
        validate_camera_pose_candidate(p)
    for a in anchors:
        validate_spatial_anchor_candidate(a)
    if local_map:
        validate_local_map_candidate(local_map)
    if map_quality:
        validate_map_quality_candidate(map_quality)

    result = assemble_spatial_mapping_adapter_result(
        adapter_input=adapter_input,
        raw_output=raw_output,
        poses=poses,
        trajectories=trajectories,
        anchors=anchors,
        local_maps=[local_map] if local_map else [],
        map_qualities=[map_quality] if map_quality else [],
        warnings=warnings,
        failure_points=failure_points,
    )
    validate_spatial_mapping_adapter_result_candidate(result)
    validate_no_world_model_assembly_boundary(result)

    return {
        "case_id": case_id,
        "case_passed": False,
        "source_smoke_case_id": source_smoke_case_id,
        "adapter_input": adapter_input,
        "raw_output": raw_output,
        "adapter_result": result,
        "poses": poses,
        "trajectories": trajectories,
        "anchors": anchors,
        "local_map": local_map,
        "map_quality": map_quality,
    }


def _evaluate_case(case: Dict[str, Any], row: Dict[str, Any]) -> bool:
    result = row.get("adapter_result") or {}
    raw = row.get("raw_output") or {}
    poses = row.get("poses") or []
    trajectories = row.get("trajectories") or []
    anchors = row.get("anchors") or []
    local_map = row.get("local_map") or {}
    map_quality = row.get("map_quality") or {}
    adapter_input = row.get("adapter_input") or {}

    if case.get("expect_execution_mode") and adapter_input.get("execution_mode") != case["expect_execution_mode"]:
        return False
    if case.get("expect_poses_min") is not None and len(poses) < case["expect_poses_min"]:
        return False
    if case.get("expect_trajectory") is True and not trajectories:
        return False
    if case.get("expect_anchors_min") and len(anchors) < case["expect_anchors_min"]:
        return False
    if case.get("expect_map_degraded") or case.get("expect_quality_degraded"):
        if map_quality and map_quality.get("quality_status") not in ("degraded", "blocked"):
            return False
    if case.get("expect_pose_conf_not_high"):
        if any(p.get("pose_confidence") == "high" for p in poses):
            return False
    if case.get("expect_local_map") and not local_map.get("local_map_candidate_id"):
        return False
    if case.get("expect_blocked") and not raw.get("_blocked"):
        return False
    if case.get("expect_no_fabrication"):
        if poses or local_map:
            return False
    if case.get("expect_not_real_run"):
        mode = adapter_input.get("execution_mode")
        raw_warnings = " ".join(raw.get("warning_codes") or [])
        if mode == "cached_output" and "not_real_run" not in raw_warnings:
            return False
        if mode == "adapter_stub" and "not_real_run" not in raw_warnings:
            return False
    if case.get("expect_task_readiness") and not result.get("readiness_for_midplatform_task_collaboration"):
        return False
    if case.get("expect_later_wm_readiness") and not result.get("readiness_for_later_world_model_candidate_assembly"):
        return False
    if case.get("expect_no_wm_assembly") or case.get("expect_no_wm_candidate"):
        if result.get("world_model_candidate_generated") or result.get("world_model_entry_created"):
            return False
    if case.get("expect_new_protocol") is False:
        return True
    if case.get("expect_no_simulation"):
        flags = result.get("non_execution_flags") or {}
        return flags.get("no_field_simulation") is True
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
