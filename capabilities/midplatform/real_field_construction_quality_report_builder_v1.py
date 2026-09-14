# -*- coding: utf-8 -*-
"""Real field construction quality report builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.real_model_execution_path_failure_localizer_v1 import (
    localize_execution_failure_points,
)


def _classify_frame(exec_result: Dict[str, Any]) -> str:
    status = exec_result.get("execution_status", "")
    if status.startswith("blocked"):
        return "blocked"
    if status.startswith("failed"):
        return "failed"
    if status.startswith("degraded") or "mock" in status or "stub" in status:
        return "degraded"
    return "passed"


def build_real_field_construction_quality_report(
    *,
    execution_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Aggregate per-frame execution results into quality report candidate."""
    refs = [r["execution_path_result_id"] for r in execution_results if r.get("execution_path_result_id")]
    passed = degraded = blocked = failed = 0
    yolo_real = yolo_cached = 0
    depth_real = depth_stub = depth_mock = 0
    enhanced = geom_est = geom_unknown = 0
    zone_summary: Dict[str, int] = {}
    depth_q: Dict[str, int] = {}
    geom_q: Dict[str, int] = {}
    scene_q: Dict[str, int] = {}
    localized_all: List[Dict[str, Any]] = []
    mock_as_real = False
    stub_as_full = False

    for r in execution_results:
        bucket = _classify_frame(r)
        if bucket == "passed":
            passed += 1
        elif bucket == "degraded":
            degraded += 1
        elif bucket == "blocked":
            blocked += 1
        else:
            failed += 1

        ym = r.get("yolo_execution_mode", "")
        if ym == "real_runner":
            yolo_real += 1
        elif ym == "cached_output":
            yolo_cached += 1

        dm = r.get("depth_execution_mode", "")
        if dm == "real_adapter":
            depth_real += 1
        elif dm in ("stub_depth", "real_adapter_stub"):
            depth_stub += 1
        elif dm == "mock_adapter_with_real_frame_alignment":
            depth_mock += 1

        if r.get("enhanced_field_scene_ref"):
            enhanced += 1
        scene = r.get("enhanced_field_scene_candidate") or {}
        gq = (scene.get("geometry_quality_summary") or {})
        geom_est += gq.get("geometry_enhanced_count", 0)
        geom_unknown += gq.get("geometry_unknown_count", 0)
        zs = scene.get("zone_summary") or {}
        for k, v in zs.items():
            if isinstance(v, int):
                zone_summary[k] = zone_summary.get(k, 0) + v

        dq_status = r.get("depth_quality_status", "unknown")
        depth_q[dq_status] = depth_q.get(dq_status, 0) + 1
        gq_status = gq.get("geometry_quality", "unknown")
        geom_q[gq_status] = geom_q.get(gq_status, 0) + 1
        sq_status = (scene.get("scene_quality_summary") or {}).get("scene_quality", "unknown")
        scene_q[sq_status] = scene_q.get(sq_status, 0) + 1

        if r.get("mock_depth_marked_as_real"):
            mock_as_real = True
        if r.get("stub_depth_marked_as_full_real"):
            stub_as_full = True

        localized_all.extend(
            localize_execution_failure_points(
                failure_points=r.get("failure_points") or [],
                warnings=(r.get("warning_summary") or {}).get("warnings") or [],
                quality_blockers=r.get("quality_blockers") or [],
                success_path_status=r.get("execution_status", ""),
            )
        )

    total = len(execution_results)
    readiness = (
        total >= 5 and enhanced >= 1 and not mock_as_real and not stub_as_full
        and passed + degraded >= 1
    )

    return {
        "quality_report_id": f"rfqr_{uuid.uuid4().hex[:12]}",
        "execution_path_result_refs": refs,
        "total_frame_count": total,
        "passed_frame_count": passed,
        "degraded_frame_count": degraded,
        "blocked_frame_count": blocked,
        "failed_frame_count": failed,
        "yolo_real_runner_count": yolo_real,
        "yolo_cached_count": yolo_cached,
        "depth_real_adapter_count": depth_real,
        "depth_stub_count": depth_stub,
        "depth_mock_count": depth_mock,
        "enhanced_scene_count": enhanced,
        "geometry_estimated_count": geom_est,
        "geometry_unknown_count": geom_unknown,
        "zone_assignment_summary": zone_summary,
        "depth_quality_summary": depth_q,
        "geometry_quality_summary": geom_q,
        "field_scene_quality_summary": scene_q,
        "failure_localization_summary": localized_all,
        "readiness_for_real_field_quality_evaluation": readiness,
        "mock_depth_marked_as_real": mock_as_real,
        "stub_depth_marked_as_full_real": stub_as_full,
        "candidate_only": True,
    }
