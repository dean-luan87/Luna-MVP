# -*- coding: utf-8 -*-
"""Field construction success path quality assessor v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_model_field_construction_hardening_types_v1 import (
    QUALITY_SCORE_DISCRETE,
)


def _status_ok(summary: Dict[str, Any] | None, required_keys: Tuple[str, ...]) -> Tuple[str, List[str]]:
    if not summary:
        return "incomplete", ["summary_missing"]
    missing = [k for k in required_keys if k not in summary]
    if missing:
        return "incomplete", [f"missing_{k}" for k in missing]
    return "complete", []


def assess_success_path_quality(
    *,
    dryrun_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Build SuccessPathQualityAssessmentCandidate from dryrun result."""
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    scene_id = scene.get("field_scene_id")
    status = dryrun_result.get("success_path_status", "unknown")
    trace_refs = dryrun_result.get("traceability_refs") or []
    exec_boundary = dryrun_result.get("execution_boundary_summary") or {}

    scene_q, scene_issues = _status_ok(
        scene.get("scene_quality_summary"),
        ("scene_quality", "entity_count"),
    )
    depth_q, depth_issues = _status_ok(
        scene.get("depth_quality_summary"),
        ("depth_quality", "depth_error_expected_all"),
    )
    geom_q, geom_issues = _status_ok(
        scene.get("geometry_quality_summary"),
        ("geometry_quality",),
    )
    zone_q, zone_issues = _status_ok(
        scene.get("zone_summary"),
        ("total_entity_count",),
    )

    trace_status = "complete" if len(trace_refs) >= 4 else "incomplete"
    trace_issues = [] if trace_status == "complete" else ["traceability_refs_incomplete"]

    degradation = dryrun_result.get("degradation_summary") or {}
    deg_status = "degraded" if degradation.get("degraded") else "none"

    reason_codes: List[str] = []
    if status.startswith("degraded"):
        reason_codes.append(status)
    if exec_boundary.get("depth_execution_mode") == "mock_adapter_with_real_frame_alignment":
        reason_codes.append("mock_depth_adapter")
    if exec_boundary.get("depth_execution_mode") == "real_adapter":
        reason_codes.append("local_depth_adapter_stub")
    reason_codes.extend(scene_issues + depth_issues + geom_issues + zone_issues + trace_issues)

    score = _discrete_score(
        status=status,
        scene_q=scene_q,
        depth_q=depth_q,
        geom_q=geom_q,
        zone_q=zone_q,
        trace_status=trace_status,
        reason_codes=reason_codes,
    )

    return {
        "quality_assessment_id": f"spqa_{uuid.uuid4().hex[:12]}",
        "enhanced_field_scene_ref": scene_id,
        "scene_quality_status": scene_q,
        "depth_quality_status": depth_q,
        "geometry_quality_status": geom_q,
        "zone_summary_status": zone_q,
        "traceability_status": trace_status,
        "degradation_status": deg_status,
        "quality_score_discrete": score,
        "reason_codes": sorted(set(reason_codes)),
        "candidate_only": True,
    }


def _discrete_score(
    *,
    status: str,
    scene_q: str,
    depth_q: str,
    geom_q: str,
    zone_q: str,
    trace_status: str,
    reason_codes: List[str],
) -> str:
    if status.startswith("failed") or status == "blocked_by_authorization":
        return "blocked"
    if trace_status != "complete":
        return "weak"
    incomplete = sum(1 for q in (scene_q, depth_q, geom_q, zone_q) if q != "complete")
    if status == "pass_real_yolo_real_depth" and incomplete == 0:
        return "strong"
    if status in ("pass_real_yolo_mock_depth_alignment", "pass_real_yolo_depth_fallback"):
        return "degraded_usable" if incomplete <= 1 else "weak"
    if status.startswith("degraded"):
        return "degraded_usable" if incomplete <= 2 else "weak"
    if incomplete == 0:
        return "usable"
    if incomplete <= 2:
        return "degraded_usable"
    return "weak"
