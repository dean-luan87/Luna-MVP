# -*- coding: utf-8 -*-
"""Real model execution path hardening core v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.depth_execution_path_bridge_v1 import execute_or_load_depth_output_for_frame
from capabilities.midplatform.real_model_execution_authorization_resolver_v1 import (
    resolve_real_model_execution_authorization,
)
from capabilities.midplatform.real_model_execution_path_hardening_static_validators_v1 import (
    validate_real_model_execution_path_result,
)
from capabilities.midplatform.real_model_field_construction_pipeline_v1 import (
    run_real_model_field_construction_pipeline,
)
from capabilities.midplatform.yolo_execution_path_bridge_v1 import execute_or_load_yolo_output_for_frame


def _resolve_auth_overrides(case: Dict[str, Any]) -> Dict[str, Any]:
    overrides: Dict[str, Any] = {}
    yolo_mode = case.get("yolo_mode", "auto")
    depth_mode = case.get("depth_mode", "auto")

    if yolo_mode == "real_runner":
        overrides["yolo_path"] = "real_runner"
        overrides["yolo_local_runner_available"] = True
    elif yolo_mode == "cached":
        overrides["yolo_path"] = "cached_output"
        overrides["yolo_local_runner_available"] = False

    if depth_mode == "real_adapter":
        overrides["depth_path"] = "local_depth_adapter"
        overrides["local_depth_adapter_available"] = True
    elif depth_mode == "stub":
        overrides["depth_path"] = "local_depth_adapter"
        overrides["local_depth_adapter_available"] = False
    elif depth_mode == "authorized_model":
        overrides["depth_path"] = "authorized_depth_model"
        overrides["depth_model_download_authorized"] = True
    elif depth_mode == "blocked":
        overrides["depth_path"] = "blocked"
    elif depth_mode == "missing":
        pass
    else:
        overrides["depth_path"] = "mock_adapter_with_real_frame_alignment"
    return overrides


def _execution_status(
    *,
    yolo_mode: str,
    depth_mode: str,
    pipeline_status: str,
    has_scene: bool,
) -> str:
    if pipeline_status == "failed_no_detection":
        return "failed_no_detection"
    if not has_scene and pipeline_status == "failed_field_assembly":
        return "failed_field_assembly"
    if depth_mode == "blocked_depth_authorization":
        return "blocked_depth_authorization"
    if depth_mode == "missing":
        return "degraded_missing_depth"
    if yolo_mode == "real_runner" and depth_mode == "real_adapter":
        return "pass_real_yolo_real_depth"
    if yolo_mode == "real_runner" and depth_mode in ("stub_depth", "real_adapter_stub"):
        return "pass_real_yolo_stub_depth"
    if yolo_mode == "cached_output" and depth_mode == "real_adapter":
        return "pass_cached_yolo_real_depth"
    if depth_mode == "mock_adapter_with_real_frame_alignment":
        return "pass_cached_yolo_mock_depth_alignment"
    if yolo_mode == "cached_output" and depth_mode == "missing":
        return "degraded_cached_yolo_only"
    if yolo_mode == "blocked_yolo_runner_missing":
        return "blocked_yolo_runner_missing"
    return "pass_real_yolo_cached_depth" if has_scene else "failed_field_assembly"


def run_execution_case(
    *,
    case: Dict[str, Any],
    frame_pkg: Dict[str, Any],
    base_matrix: Dict[str, Any],
    case_def: Dict[str, Any],
) -> Dict[str, Any]:
    """Run one controlled execution case end-to-end."""
    overrides = _resolve_auth_overrides(case)
    auth_candidate, auth_resolved, blocked_reasons = resolve_real_model_execution_authorization(
        matrix=base_matrix, case_overrides=overrides,
    )
    runtime_auth = {**base_matrix, **overrides}

    warnings: List[str] = []
    failure_points: List[str] = list(blocked_reasons)
    detections = list(case_def.get("detections") or [])

    yolo_pkg, yolo_mode, yolo_warn, yolo_fps = execute_or_load_yolo_output_for_frame(
        frame_pkg=frame_pkg,
        authorization=runtime_auth,
        cached_detections=detections,
        prefer_real_runner=case.get("yolo_mode") == "real_runner",
    )
    warnings.extend(yolo_warn)
    failure_points.extend(yolo_fps)

    depth_pkg = None
    depth_mode = "missing"
    if case.get("depth_mode") != "missing":
        depth_pkg, depth_mode, depth_warn, depth_fps = execute_or_load_depth_output_for_frame(
            frame_pkg=frame_pkg,
            authorization=runtime_auth,
            depth_mode=case.get("depth_mode", "auto"),
            depth_samples=case.get("depth_samples") or case_def.get("depth_samples"),
            timestamp_override=case.get("depth_timestamp") or case_def.get("depth_timestamp"),
            use_stub=case.get("depth_mode") == "stub",
        )
        warnings.extend(depth_warn)
        failure_points.extend(depth_fps)

    pipeline = run_real_model_field_construction_pipeline(
        frame_pkg=frame_pkg, yolo_pkg=yolo_pkg, depth_pkg=depth_pkg,
    )
    objects = pipeline.get("object_observation_candidates") or []
    scene = pipeline.get("enhanced_field_scene_candidate") or {}
    if not scene.get("field_scene_id") and not objects:
        failure_points.append("no_yolo_detection")
    exec_status = _execution_status(
        yolo_mode=yolo_mode,
        depth_mode=depth_mode,
        pipeline_status=pipeline.get("pipeline_status", ""),
        has_scene=bool(scene.get("field_scene_id")),
    )

    mock_as_real = (
        depth_mode == "mock_adapter_with_real_frame_alignment"
        and exec_status == "pass_real_yolo_real_depth"
    )
    stub_as_full = (
        depth_mode in ("stub_depth", "real_adapter_stub")
        and exec_status == "pass_real_yolo_real_depth"
    )

    traceability = [
        frame_pkg.get("image_path"),
        frame_pkg.get("frame_input_id"),
        yolo_pkg.get("detector_run_id"),
        yolo_pkg.get("model_ref"),
        yolo_mode,
        depth_mode,
    ]
    if depth_pkg:
        traceability.extend([depth_pkg.get("depth_run_id"), depth_pkg.get("model_ref")])
    if scene.get("field_scene_id"):
        traceability.append(scene["field_scene_id"])

    result = {
        "execution_path_result_id": f"epr_{uuid.uuid4().hex[:12]}",
        "frame_input_ref": frame_pkg.get("frame_input_id"),
        "yolo_execution_mode": yolo_mode,
        "depth_execution_mode": depth_mode,
        "yolo_output_ref": yolo_pkg.get("detector_run_id"),
        "depth_output_ref": (depth_pkg or {}).get("depth_run_id"),
        "object_observation_candidates": pipeline.get("object_observation_candidates") or [],
        "depth_observation_candidate": pipeline.get("depth_observation_candidate"),
        "alignment_result_ref": pipeline.get("alignment_result_ref"),
        "fusion_result_ref": pipeline.get("fusion_result_ref"),
        "geometry_result_ref": pipeline.get("geometry_result_ref"),
        "field_assembly_result_ref": pipeline.get("field_assembly_result_ref"),
        "enhanced_field_scene_ref": scene.get("field_scene_id"),
        "enhanced_field_scene_candidate": scene,
        "execution_status": exec_status,
        "failure_points": failure_points,
        "warning_summary": {"warnings": sorted(set(warnings))},
        "missing_information": [] if scene else ["enhanced_field_scene_missing"],
        "traceability_refs": [t for t in traceability if t],
        "mock_depth_marked_as_real": mock_as_real,
        "stub_depth_marked_as_full_real": stub_as_full,
        "depth_quality_status": (
            "real" if depth_mode == "real_adapter"
            else "stub" if depth_mode in ("stub_depth", "real_adapter_stub")
            else "mock_labeled" if depth_mode == "mock_adapter_with_real_frame_alignment"
            else "missing" if depth_mode == "missing"
            else "blocked"
        ),
        "candidate_only": True,
    }
    validate_real_model_execution_path_result(result)
    return {
        "case_id": case["case_id"],
        "case_passed": False,
        "frame_pkg": frame_pkg,
        "yolo_pkg": yolo_pkg,
        "depth_pkg": depth_pkg,
        "auth_candidate": auth_candidate,
        "auth_resolved": auth_resolved,
        "execution_result": result,
    }


def _evaluate_case(case: Dict[str, Any], row: Dict[str, Any]) -> bool:
    er = row.get("execution_result") or {}
    scene = er.get("enhanced_field_scene_candidate") or {}

    if case.get("expect_no_scene") and scene.get("field_scene_id"):
        return False
    if case.get("expect_scene") and not scene.get("field_scene_id"):
        return False
    if case.get("expect_execution_status") and er.get("execution_status") != case["expect_execution_status"]:
        return False
    if case.get("expect_yolo_mode") and er.get("yolo_execution_mode") != case["expect_yolo_mode"]:
        return False
    if case.get("expect_depth_mode") and er.get("depth_execution_mode") != case["expect_depth_mode"]:
        return False
    if case.get("expect_not_mock_as_real") and er.get("mock_depth_marked_as_real"):
        return False
    if case.get("expect_not_stub_as_full_real") and er.get("stub_depth_marked_as_full_real"):
        return False
    if case.get("expect_depth_blocked") and er.get("depth_execution_mode") != "blocked_depth_authorization":
        return False
    if case.get("expect_entities_min"):
        if len(er.get("object_observation_candidates") or []) < case["expect_entities_min"]:
            return False
    if case.get("expect_localization_area"):
        fps = er.get("failure_points") or []
        if case["expect_localization_area"] not in " ".join(fps):
            if case["expect_localization_area"] == "yolo_output_bridge":
                if not any("invalid_bbox" in f or "no_detection" in f or "no_yolo" in f for f in fps):
                    return False
            elif case["expect_localization_area"] == "multi_model_alignment":
                if not any("timestamp" in f or "alignment" in f for f in fps + (er.get("warning_summary") or {}).get("warnings", [])):
                    return False
    if case.get("expect_traceability_min"):
        if len(er.get("traceability_refs") or []) < case["expect_traceability_min"]:
            return False
    if case.get("expect_degraded") and not er.get("execution_status", "").startswith("degraded") and "mock" not in er.get("execution_status", ""):
        return False
    return True


def run_all_execution_cases(
    *,
    cases: Tuple[Dict[str, Any], ...],
    frames_by_case: Dict[str, Dict[str, Any]],
    case_defs: Dict[str, Dict[str, Any]],
    base_matrix: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    auth_resolved_list: List[Dict[str, Any]] = []
    all_passed = True

    for case in cases:
        if case.get("batch_case_ids"):
            batch_rows = []
            for sid in case["batch_case_ids"]:
                sub = {**case, "case_id": f"{case['case_id']}_{sid}", "source_case_id": sid}
                frame = frames_by_case.get(sid)
                if not frame:
                    all_passed = False
                    continue
                row = run_execution_case(
                    case=sub, frame_pkg=frame, base_matrix=base_matrix,
                    case_def=case_defs.get(sid, {}),
                )
                row["case_passed"] = _evaluate_case(sub, row)
                batch_rows.append(row)
                auth_resolved_list.append(row.get("auth_resolved"))
            passed = len(batch_rows) >= case.get("expect_batch_min", 3) and all(r.get("case_passed") for r in batch_rows)
            results.append({"case_id": case["case_id"], "case_passed": passed, "batch_results": batch_rows})
            if not passed:
                all_passed = False
            continue

        sid = case.get("source_case_id", case["case_id"])
        frame = frames_by_case.get(sid)
        if not frame:
            results.append({"case_id": case["case_id"], "case_passed": False, "error": "frame_not_found"})
            all_passed = False
            continue
        row = run_execution_case(
            case=case, frame_pkg=frame, base_matrix=base_matrix,
            case_def=case_defs.get(sid, {}),
        )
        row["case_passed"] = _evaluate_case(case, row)
        results.append(row)
        auth_resolved_list.append(row.get("auth_resolved"))
        if not row.get("case_passed") and not case.get("optional_meta"):
            all_passed = False

    return results, auth_resolved_list, all_passed
