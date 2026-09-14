# -*- coding: utf-8 -*-
"""Controlled real dryrun result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.yolo_depth_controlled_real_dryrun_types_v1 import NON_EXECUTION_FLAGS


def _resolve_success_status(
    *,
    yolo_pkg: Dict[str, Any],
    depth_pkg: Optional[Dict[str, Any]],
    objects: List[Dict[str, Any]],
    aligned: List[Dict[str, Any]],
    scene: Optional[Dict[str, Any]],
    failure_points: List[str],
    warnings: List[str],
) -> str:
    if "blocked_by_authorization" in " ".join(failure_points):
        return "blocked_by_authorization"
    if not (yolo_pkg.get("detections") or []):
        return "failed_no_yolo_detection"
    if not objects:
        if yolo_pkg.get("detections"):
            return "failed_alignment"
        return "failed_no_yolo_detection"
    if not aligned:
        return "failed_alignment"
    if not scene:
        return "failed_field_assembly"
    if not depth_pkg:
        return "degraded_missing_depth"
    if depth_pkg.get("execution_mode") == "mock_adapter_with_real_frame_alignment":
        return "pass_real_yolo_mock_depth_alignment"
    if depth_pkg.get("depth_confidence") == "low":
        return "degraded_low_depth_confidence"
    if "depth_missing" in warnings:
        return "pass_real_yolo_depth_fallback"
    return "pass_real_yolo_real_depth"


def assemble_real_field_assembly_dryrun_result(
    *,
    frame_pkg: Dict[str, Any],
    yolo_pkg: Dict[str, Any],
    depth_pkg: Optional[Dict[str, Any]],
    objects: List[Dict[str, Any]],
    depth_obs: Optional[Dict[str, Any]],
    pipeline: Dict[str, Any],
    warnings: List[str],
    failure_points: List[str],
    authorization_summary: Dict[str, Any],
) -> Dict[str, Any]:
    aligned = pipeline.get("aligned_candidates") or []
    hints = pipeline.get("object_depth_hints") or []
    geometries = pipeline.get("field_geometry_candidates") or []
    scene = pipeline.get("enhanced_field_scene")
    assembly = pipeline.get("assembly_result") or {}

    all_warnings = list(set(warnings))
    all_missing: List[str] = []
    if not depth_pkg:
        all_missing.append("depth_output_missing")
    if scene:
        all_missing.extend(scene.get("missing_information") or [])

    status = _resolve_success_status(
        yolo_pkg=yolo_pkg, depth_pkg=depth_pkg, objects=objects,
        aligned=aligned, scene=scene, failure_points=failure_points, warnings=all_warnings,
    )

    traceability = [
        frame_pkg.get("frame_input_id"),
        frame_pkg.get("frame_ref"),
        yolo_pkg.get("detector_run_id"),
        yolo_pkg.get("raw_output_ref"),
    ]
    if depth_pkg:
        traceability.extend([depth_pkg.get("depth_run_id"), depth_pkg.get("raw_output_ref")])
    if scene:
        traceability.append(scene.get("field_scene_id"))

    readiness_core = assembly.get("readiness_for_field_first_core") is True or (
        scene is not None and len(objects) > 0
    )
    readiness_hardening = assembly.get("readiness_for_real_model_success_path") is True or (
        status in ("pass_real_yolo_real_depth", "pass_real_yolo_mock_depth_alignment")
        and scene is not None
    )

    return {
        "dryrun_result_id": f"rfd_{uuid.uuid4().hex[:12]}",
        "frame_input_ref": frame_pkg.get("frame_input_id"),
        "yolo_output_ref": yolo_pkg.get("detector_run_id"),
        "depth_output_ref": (depth_pkg or {}).get("depth_run_id"),
        "object_observation_candidates": objects,
        "depth_observation_candidates": [depth_obs] if depth_obs else [],
        "aligned_observation_candidates": aligned,
        "object_depth_hint_candidates": hints,
        "field_geometry_candidates": geometries,
        "enhanced_field_scene_candidate": scene,
        "field_assembly_result_candidate": assembly,
        "success_path_status": status,
        "warning_summary": {"warnings": all_warnings, "warning_count": len(all_warnings)},
        "missing_information": sorted(set(all_missing)),
        "degradation_summary": {
            "degraded": status.startswith("degraded") or status.endswith("fallback"),
            "status": status,
        },
        "failure_points": failure_points,
        "readiness_for_core_pipeline": readiness_core,
        "readiness_for_success_path_hardening": readiness_hardening,
        "execution_boundary_summary": authorization_summary,
        "source_refs": list(frame_pkg.get("source_refs", [frame_pkg.get("source_ref")]) if isinstance(frame_pkg.get("source_refs"), list) else [frame_pkg.get("source_ref")]),
        "evidence_refs": [frame_pkg.get("frame_input_id"), yolo_pkg.get("detector_run_id")],
        "traceability_refs": [t for t in traceability if t],
        "candidate_only": True,
        "non_execution_flags": {k: v for k, v in NON_EXECUTION_FLAGS.items()},
    }
