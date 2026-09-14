# -*- coding: utf-8 -*-
"""Real model field construction quality report assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional

from capabilities.midplatform.real_model_execution_path_failure_localizer_v1 import (
    localize_execution_failure_points,
)


def assemble_execution_path_result(
    *,
    frame_pkg: Dict[str, Any],
    yolo_pkg: Dict[str, Any],
    depth_pkg: Optional[Dict[str, Any]],
    dryrun_result: Dict[str, Any],
    quality_report: Dict[str, Any],
    localized: List[Dict[str, Any]],
) -> Dict[str, Any]:
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    depth_mode = (depth_pkg or {}).get("execution_mode")
    yolo_mode = yolo_pkg.get("execution_mode", "cached_output")

    if quality_report.get("mock_depth_marked_as_real"):
        exec_status = "blocked_by_authorization"
    elif dryrun_result.get("success_path_status") == "failed_no_yolo_detection":
        exec_status = "failed_no_yolo_detection"
    elif not scene.get("field_scene_id"):
        exec_status = "failed_field_construction"
    elif depth_mode in ("real_adapter", "authorized_model"):
        exec_status = "pass_real_yolo_cached_depth_adapter" if yolo_mode == "cached_output" else "pass_real_yolo_real_depth"
    elif depth_mode == "mock_adapter_with_real_frame_alignment":
        exec_status = "pass_real_yolo_mock_depth_labeled"
    elif not depth_pkg:
        exec_status = "degraded_missing_depth"
    else:
        exec_status = dryrun_result.get("success_path_status", "degraded_geometry_unknown")

    return {
        "execution_result_id": f"exr_{uuid.uuid4().hex[:12]}",
        "frame_input_ref": frame_pkg.get("frame_input_id"),
        "yolo_output_ref": yolo_pkg.get("detector_run_id"),
        "depth_output_ref": (depth_pkg or {}).get("depth_run_id"),
        "enhanced_field_scene_ref": scene.get("field_scene_id"),
        "execution_path_status": exec_status,
        "yolo_execution_mode": yolo_mode,
        "depth_execution_mode": depth_mode or "missing",
        "field_quality_report_ref": quality_report.get("quality_report_id"),
        "quality_gate_status": quality_report.get("quality_gate_status"),
        "localized_failure_points": localized,
        "warning_summary": dryrun_result.get("warning_summary"),
        "missing_information": dryrun_result.get("missing_information") or [],
        "traceability_refs": dryrun_result.get("traceability_refs") or [],
        "candidate_only": True,
    }


def finalize_quality_report(
    quality_report: Dict[str, Any],
    zone_status: str,
    zone_notes: List[str],
) -> Dict[str, Any]:
    report = dict(quality_report)
    report["zone_reasonableness_status"] = zone_status
    if zone_notes:
        report["quality_warnings"] = sorted(set((report.get("quality_warnings") or []) + zone_notes))
        if zone_status == "unreasonable":
            report["quality_blockers"] = list(report.get("quality_blockers") or []) + zone_notes
            report["quality_gate_status"] = "blocked"
    return report
