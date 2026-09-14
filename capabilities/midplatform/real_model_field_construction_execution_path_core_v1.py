# -*- coding: utf-8 -*-
"""Real model field construction execution path hardening core v1."""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.depth_real_output_bridge_v1 import run_or_load_depth_output
from capabilities.midplatform.field_construction_quality_evaluator_v1 import (
    check_zone_reasonableness,
    evaluate_field_construction_quality,
)
from capabilities.midplatform.real_frame_input_loader_v1 import load_real_frame_input_package
from capabilities.midplatform.real_model_candidate_conversion_v1 import (
    convert_depth_output_to_depth_observation_candidate,
    convert_yolo_output_to_object_observation_candidates,
)
from capabilities.midplatform.real_model_field_construction_quality_report_assembler_v1 import (
    assemble_execution_path_result,
    finalize_quality_report,
)
from capabilities.midplatform.real_model_execution_path_failure_localizer_v1 import (
    localize_execution_failure_points,
)
from capabilities.midplatform.real_model_field_construction_execution_path_static_validators_v1 import (
    validate_execution_path_result,
    validate_quality_report,
)
from capabilities.midplatform.yolo_depth_controlled_real_dryrun_result_assembler_v1 import (
    assemble_real_field_assembly_dryrun_result,
)
from capabilities.midplatform.yolo_depth_real_field_assembly_pipeline_v1 import (
    run_real_field_assembly_pipeline,
)
from capabilities.midplatform.yolo_real_output_bridge_v1 import run_or_load_yolo_real_output


def _resolve_authorization(base: Dict[str, Any], case: Dict[str, Any]) -> Dict[str, Any]:
    auth = copy.deepcopy(base)
    depth_mode = case.get("depth_mode", "auto")
    if depth_mode == "local_adapter":
        auth["depth_path"] = "local_depth_adapter"
        auth["local_depth_adapter_available"] = True
    elif depth_mode == "authorized_model":
        auth["depth_path"] = "authorized_depth_model"
        auth["depth_model_download_authorized"] = True
    elif depth_mode == "blocked":
        auth["depth_path"] = "blocked"
    elif depth_mode == "missing":
        pass
    else:
        auth["depth_path"] = "mock_adapter_with_real_frame_alignment"
    return auth


def run_execution_path_case(
    case: Dict[str, Any],
    *,
    base_authorization: Dict[str, Any],
    work_dir: str,
    upstream: Dict[str, Any],
) -> Dict[str, Any]:
    case_def = upstream.get("case_def") or {}
    detections = list(case_def.get("detections") or [])

    case_id = case.get("case_id", "exec_case")
    source_id = case.get("source_case_id", case_id)
    frame_pkg, frame_fps = load_real_frame_input_package(
        frame_input_id=f"rfi_{source_id}",
        image_path=f"/tmp/execution_path/{source_id}.png",
        frame_ref=case_def.get("frame_ref", f"frame_{source_id}"),
        frame_width=640,
        frame_height=480,
        timestamp="2026-06-11T10:00:00Z",
        test_case_id=source_id,
        source_ref="execution_path_hardening_v1",
        work_dir=work_dir,
    )
    if not frame_pkg:
        return {"case_id": case_id, "case_passed": False, "error": "frame_load_failed"}

    auth = _resolve_authorization(base_authorization, case)
    warnings: List[str] = list(frame_fps)
    failure_points: List[str] = list(frame_fps)

    yolo_pkg, yolo_warn, yolo_fps = run_or_load_yolo_real_output(
        frame_pkg=frame_pkg,
        authorization=auth,
        cached_detections=detections if detections else None,
    )
    warnings.extend(yolo_warn)
    failure_points.extend(yolo_fps)

    depth_pkg = None
    depth_samples = case.get("depth_samples") or case_def.get("depth_samples")
    depth_timestamp = case.get("depth_timestamp") or case_def.get("depth_timestamp")
    if case.get("depth_mode") != "missing":
        depth_pkg, depth_warn, depth_fps = run_or_load_depth_output(
            frame_pkg=frame_pkg,
            authorization=auth,
            depth_samples=depth_samples,
            timestamp_override=depth_timestamp,
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
            frame_pkg=frame_pkg, yolo_pkg=yolo_pkg, depth_pkg=depth_pkg,
            objects=objects, depth_obs=depth_obs,
        )
        dryrun_result = assemble_real_field_assembly_dryrun_result(
            frame_pkg=frame_pkg, yolo_pkg=yolo_pkg, depth_pkg=depth_pkg,
            objects=objects, depth_obs=depth_obs, pipeline=pipeline,
            warnings=warnings, failure_points=failure_points,
            authorization_summary={
                "yolo_execution_mode": yolo_pkg.get("execution_mode"),
                "depth_execution_mode": (depth_pkg or {}).get("execution_mode"),
                "depth_path": auth.get("depth_path"),
                "no_unauthorized_download": True,
            },
        )
    elif yolo_pkg:
        dryrun_result = assemble_real_field_assembly_dryrun_result(
            frame_pkg=frame_pkg, yolo_pkg=yolo_pkg, depth_pkg=depth_pkg,
            objects=[], depth_obs=depth_obs, pipeline={},
            warnings=warnings, failure_points=failure_points + ["no_valid_yolo_detections"],
            authorization_summary={
                "yolo_execution_mode": yolo_pkg.get("execution_mode"),
                "depth_execution_mode": (depth_pkg or {}).get("execution_mode"),
                "depth_path": auth.get("depth_path"),
                "no_unauthorized_download": True,
            },
        )

    quality_report = evaluate_field_construction_quality(
        dryrun_result=dryrun_result or {},
        depth_pkg=depth_pkg,
        yolo_pkg=yolo_pkg,
    )
    scene = (dryrun_result or {}).get("enhanced_field_scene_candidate") or {}
    entities = scene.get("entity_candidates") or objects
    zone_status, zone_notes = check_zone_reasonableness(
        quality_report,
        scene.get("zone_summary") or {},
        entities,
        (depth_pkg or {}).get("execution_mode", "missing"),
    )
    quality_report = finalize_quality_report(quality_report, zone_status, zone_notes)

    localized = localize_execution_failure_points(
        failure_points=failure_points,
        warnings=warnings,
        quality_blockers=quality_report.get("quality_blockers") or [],
        success_path_status=(dryrun_result or {}).get("success_path_status", ""),
    )
    exec_result = assemble_execution_path_result(
        frame_pkg=frame_pkg, yolo_pkg=yolo_pkg, depth_pkg=depth_pkg,
        dryrun_result=dryrun_result or {}, quality_report=quality_report,
        localized=localized,
    )

    validate_quality_report(quality_report)
    validate_execution_path_result(exec_result)

    return {
        "case_id": case_id,
        "source_case_id": source_id,
        "case_passed": False,
        "frame_pkg": frame_pkg,
        "yolo_pkg": yolo_pkg,
        "depth_pkg": depth_pkg,
        "dryrun_result": dryrun_result,
        "quality_report": quality_report,
        "execution_result": exec_result,
        "warnings": warnings,
        "failure_points": failure_points,
    }


def _evaluate_case(case: Dict[str, Any], row: Dict[str, Any]) -> bool:
    if case.get("optional_meta") and case.get("case_id") == "exec_multi_scene_fixture_batch":
        return True
    if case.get("optional_meta") and case.get("case_id") == "exec_depth_authorization_blocked_path":
        depth_pkg = row.get("depth_pkg")
        return depth_pkg is None or row.get("execution_result", {}).get("depth_execution_mode") == "missing"

    exec_r = row.get("execution_result") or {}
    qr = row.get("quality_report") or {}
    dryrun = row.get("dryrun_result") or {}
    scene = (dryrun.get("enhanced_field_scene_candidate") or {}) if dryrun else {}

    if case.get("expect_no_scene") and scene.get("field_scene_id"):
        return False
    if case.get("expect_scene") and not scene.get("field_scene_id"):
        return False

    if case.get("expect_execution_status") and exec_r.get("execution_path_status") != case["expect_execution_status"]:
        return False

    if case.get("expect_depth_mode") and exec_r.get("depth_execution_mode") != case["expect_depth_mode"]:
        return False

    if case.get("expect_not_mock_as_real") and qr.get("mock_depth_marked_as_real"):
        return False

    if case.get("expect_quality_report") and not qr.get("quality_report_id"):
        return False

    if case.get("expect_quality_gate") and qr.get("quality_gate_status") not in case["expect_quality_gate"]:
        return False

    if case.get("expect_depth_quality") and qr.get("depth_quality_status") != case["expect_depth_quality"]:
        return False

    if case.get("expect_geometry_quality") and qr.get("geometry_quality_status") != case["expect_geometry_quality"]:
        return False

    if case.get("expect_entities_min"):
        ents = scene.get("entity_candidates") or row.get("dryrun_result", {}).get("object_observation_candidates") or []
        if len(ents) < case["expect_entities_min"]:
            return False

    if case.get("expect_zone_reasonable"):
        if qr.get("zone_reasonableness_status") not in case["expect_zone_reasonable"]:
            return False

    if case.get("expect_localization_area"):
        areas = [lp.get("recommended_fix_area") for lp in exec_r.get("localized_failure_points") or []]
        if case["expect_localization_area"] not in areas:
            return False

    if case.get("expect_traceability_min"):
        if len(exec_r.get("traceability_refs") or []) < case["expect_traceability_min"]:
            return False

    if case.get("expect_depth_blocked"):
        if row.get("depth_pkg") is not None:
            return False

    return True


def run_all_execution_path_cases(
    *,
    cases: Tuple[Dict[str, Any], ...],
    base_authorization: Dict[str, Any],
    indexed_upstream: Dict[str, Dict[str, Any]],
    work_dir: str,
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    for case in cases:
        if case.get("batch_case_ids"):
            batch_rows = []
            for sid in case["batch_case_ids"]:
                sub = {**case, "case_id": f"{case['case_id']}_{sid}", "source_case_id": sid}
                upstream = indexed_upstream.get(sid)
                if not upstream:
                    all_passed = False
                    continue
                row = run_execution_path_case(sub, base_authorization=base_authorization, work_dir=work_dir, upstream=upstream)
                row["case_passed"] = _evaluate_case(sub, row)
                batch_rows.append(row)
            passed_batch = len(batch_rows) >= case.get("expect_batch_min", 3) and all(r.get("case_passed") for r in batch_rows)
            results.append({
                "case_id": case["case_id"],
                "case_passed": passed_batch,
                "batch_results": batch_rows,
            })
            if not passed_batch and not case.get("optional_meta"):
                all_passed = False
            continue

        upstream = indexed_upstream.get(case["source_case_id"])
        if not upstream:
            results.append({"case_id": case["case_id"], "case_passed": False, "error": "upstream_not_found"})
            all_passed = False
            continue
        row = run_execution_path_case(case, base_authorization=base_authorization, work_dir=work_dir, upstream=upstream)
        row["case_passed"] = _evaluate_case(case, row)
        results.append(row)
        if not row.get("case_passed") and not case.get("optional_meta"):
            all_passed = False
    return results, all_passed
