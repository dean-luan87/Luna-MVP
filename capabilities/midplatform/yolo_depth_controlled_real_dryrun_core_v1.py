# -*- coding: utf-8 -*-
"""Controlled real dryrun core v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.depth_real_output_bridge_v1 import run_or_load_depth_output
from capabilities.midplatform.real_frame_input_loader_v1 import load_real_frame_input_package
from capabilities.midplatform.real_model_candidate_conversion_v1 import (
    convert_depth_output_to_depth_observation_candidate,
    convert_yolo_output_to_object_observation_candidates,
)
from capabilities.midplatform.yolo_depth_controlled_real_dryrun_result_assembler_v1 import (
    assemble_real_field_assembly_dryrun_result,
)
from capabilities.midplatform.yolo_depth_controlled_real_dryrun_static_validators_v1 import (
    validate_real_dryrun_result,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_pipeline_v1 import (
    run_real_field_assembly_pipeline,
)
from capabilities.midplatform.yolo_real_output_bridge_v1 import run_or_load_yolo_real_output


def _resolve_authorization(base: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    auth = copy.deepcopy(base)
    depth_mode = case.get("depth_mode", "mock")
    if depth_mode == "local_adapter":
        auth["depth_path"] = "local_depth_adapter"
        auth["local_depth_adapter_available"] = True
    elif depth_mode == "authorized_model":
        auth["depth_path"] = "authorized_depth_model"
        auth["depth_model_download_authorized"] = True
    elif depth_mode == "missing":
        pass
    else:
        auth["depth_path"] = "mock_adapter_with_real_frame_alignment"
    return auth


def run_controlled_dryrun_case(
    case: Dict[str, Any],
    *,
    base_authorization: Dict[str, Any],
    work_dir: str,
) -> Dict[str, Any]:
    """Execute one controlled real model dryrun case."""
    case_id = case["case_id"]
    frame_defaults = {"frame_width": 640, "frame_height": 480, "timestamp": "2026-06-11T10:00:00Z"}
    frame_pkg, frame_fps = load_real_frame_input_package(
        frame_input_id=f"rfi_{case_id}",
        image_path=f"/tmp/controlled_dryrun/{case_id}.png",
        frame_ref=case.get("frame_ref", f"frame_{case_id}"),
        frame_width=frame_defaults["frame_width"],
        frame_height=frame_defaults["frame_height"],
        timestamp=frame_defaults["timestamp"],
        test_case_id=case_id,
        source_ref="controlled_dryrun_fixture_v1",
        work_dir=work_dir,
    )
    warnings: List[str] = list(frame_fps)
    failure_points: List[str] = list(frame_fps)

    if not frame_pkg:
        return {
            "case_id": case_id,
            "case_passed": False,
            "failure_points": failure_points,
            "warnings": warnings,
            "dryrun_result": None,
        }

    auth = _resolve_authorization(base_authorization, case)
    yolo_pkg, yolo_warn, yolo_fps = run_or_load_yolo_real_output(
        frame_pkg=frame_pkg,
        authorization=auth,
        cached_detections=list(case.get("detections") or []),
    )
    warnings.extend(yolo_warn)
    failure_points.extend(yolo_fps)

    depth_pkg = None
    depth_warn: List[str] = []
    depth_fps: List[str] = []
    if case.get("depth_mode") != "missing":
        depth_pkg, depth_warn, depth_fps = run_or_load_depth_output(
            frame_pkg=frame_pkg,
            authorization=auth,
            depth_samples=case.get("depth_samples"),
            timestamp_override=case.get("depth_timestamp"),
            depth_confidence=case.get("depth_confidence", "medium"),
        )
        warnings.extend(depth_warn)
        failure_points.extend(depth_fps)

    objects, obj_warn = convert_yolo_output_to_object_observation_candidates(yolo_pkg, frame_pkg)
    warnings.extend(obj_warn)
    depth_obs, dep_warn = convert_depth_output_to_depth_observation_candidate(depth_pkg, frame_pkg)
    warnings.extend(dep_warn)

    pipeline: Dict[str, Any] = {}
    dryrun_result = None
    if objects:
        pipeline = run_real_field_assembly_pipeline(
            frame_pkg=frame_pkg,
            yolo_pkg=yolo_pkg,
            depth_pkg=depth_pkg,
            objects=objects,
            depth_obs=depth_obs,
        )
        dryrun_result = assemble_real_field_assembly_dryrun_result(
            frame_pkg=frame_pkg,
            yolo_pkg=yolo_pkg,
            depth_pkg=depth_pkg,
            objects=objects,
            depth_obs=depth_obs,
            pipeline=pipeline,
            warnings=warnings,
            failure_points=failure_points,
            authorization_summary={
                "yolo_execution_mode": yolo_pkg.get("execution_mode"),
                "depth_execution_mode": (depth_pkg or {}).get("execution_mode"),
                "depth_path": auth.get("depth_path"),
                "no_unauthorized_download": True,
            },
        )
        valid, val_issues = validate_real_dryrun_result(dryrun_result)
        if not valid:
            warnings.extend(val_issues)
    elif yolo_pkg:
        dryrun_result = assemble_real_field_assembly_dryrun_result(
            frame_pkg=frame_pkg,
            yolo_pkg=yolo_pkg,
            depth_pkg=depth_pkg,
            objects=[],
            depth_obs=depth_obs,
            pipeline={},
            warnings=warnings,
            failure_points=failure_points + ["no_valid_yolo_detections"],
            authorization_summary={
                "yolo_execution_mode": yolo_pkg.get("execution_mode"),
                "depth_execution_mode": (depth_pkg or {}).get("execution_mode"),
                "depth_path": auth.get("depth_path"),
                "no_unauthorized_download": True,
            },
        )

    passed = _evaluate_case(case, dryrun_result, pipeline, objects, warnings, failure_points)
    return {
        "case_id": case_id,
        "case_passed": passed,
        "frame_pkg": frame_pkg,
        "yolo_pkg": yolo_pkg,
        "depth_pkg": depth_pkg,
        "objects": objects,
        "depth_obs": depth_obs,
        "pipeline": pipeline,
        "dryrun_result": dryrun_result,
        "warnings": warnings,
        "failure_points": failure_points,
    }


def _evaluate_case(
    case: Dict[str, Any],
    result: Dict[str, Any] | None,
    pipeline: Dict[str, Any],
    objects: List[Dict[str, Any]],
    warnings: List[str],
    failure_points: List[str],
) -> bool:
    if result is None:
        return case.get("expect_scene") is False

    status = result.get("success_path_status", "")
    if case.get("expect_status") and status != case["expect_status"]:
        return False
    if case.get("expect_status_prefix") and not status.startswith(case["expect_status_prefix"]):
        return False

    if case.get("expect_scene") and not result.get("enhanced_field_scene_candidate"):
        return False
    if case.get("expect_scene") is False and result.get("enhanced_field_scene_candidate"):
        return False

    if case.get("expect_objects_min") and len(objects) < case["expect_objects_min"]:
        return False
    if case.get("expect_objects_max") is not None and len(objects) > case["expect_objects_max"]:
        return False

    aligned = result.get("aligned_observation_candidates") or []
    if case.get("expect_aligned_min") and len(aligned) < case["expect_aligned_min"]:
        return False

    scene = result.get("enhanced_field_scene_candidate") or {}
    asm = result.get("field_assembly_result_candidate") or {}
    entities = scene.get("enhanced_entity_candidates") or asm.get("enhanced_entity_candidates") or []
    if case.get("expect_entities_min") and len(entities) < case["expect_entities_min"]:
        return False

    if case.get("expect_zone_summary"):
        zs = scene.get("zone_summary") or {}
        total = zs.get("total_entity_count", 0)
        if not (
            total >= case.get("expect_entities_min", 1)
            or any(zs.get(k, 0) > 0 for k in (
                "inner_zone_entity_count", "working_zone_entity_count",
                "forecast_zone_entity_count", "unknown_zone_entity_count",
            ))
        ):
            return False

    if case.get("expect_invalid_bbox_warning"):
        if not any("invalid_bbox" in w for w in warnings):
            return False

    if case.get("expect_failure_points") and not failure_points:
        return False

    if case.get("expect_ts_degraded"):
        aligned_statuses = [c.get("alignment_status") for c in aligned]
        if not any(s in ("aligned_weak", "aligned_degraded") for s in aligned_statuses):
            if not any("timestamp" in w.lower() for w in warnings):
                return False

    if case.get("expect_traceability_min"):
        refs = result.get("traceability_refs") or []
        if len(refs) < case["expect_traceability_min"]:
            return False

    if case.get("expect_geometry_unknown"):
        if not any(
            (g.get("geometry_status") or "").endswith("unknown")
            for g in (result.get("field_geometry_candidates") or [])
        ):
            ents = scene.get("enhanced_entity_candidates") or []
            if not any(e.get("entity_status") == "entity_geometry_unknown" for e in ents):
                return False

    return True


def run_all_controlled_dryrun_cases(
    *,
    base_authorization: Dict[str, Any],
    cases: Tuple[Dict[str, Any], ...],
    work_dir: str,
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    for case in cases:
        row = run_controlled_dryrun_case(case, base_authorization=base_authorization, work_dir=work_dir)
        results.append(row)
        if not row.get("case_passed"):
            all_passed = False
    return results, all_passed
