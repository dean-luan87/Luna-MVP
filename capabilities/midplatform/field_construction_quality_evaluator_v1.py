# -*- coding: utf-8 -*-
"""Field construction quality evaluator v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional, Tuple


def evaluate_field_construction_quality(
    *,
    dryrun_result: Dict[str, Any],
    depth_pkg: Optional[Dict[str, Any]],
    yolo_pkg: Dict[str, Any],
) -> Dict[str, Any]:
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    asm = dryrun_result.get("field_assembly_result_candidate") or {}
    entities = scene.get("entity_candidates") or asm.get("enhanced_entity_candidates") or []
    sq = scene.get("scene_quality_summary") or {}
    dq = scene.get("depth_quality_summary") or {}
    gq = scene.get("geometry_quality_summary") or {}
    zone = scene.get("zone_summary") or {}

    depth_mode = (depth_pkg or {}).get("execution_mode", "missing")
    yolo_mode = yolo_pkg.get("execution_mode", "cached_output")
    mock_marked_real = (
        depth_mode == "mock_adapter_with_real_frame_alignment"
        and dryrun_result.get("success_path_status") == "pass_real_yolo_real_depth"
    )

    blockers: List[str] = []
    warnings: List[str] = list((dryrun_result.get("warning_summary") or {}).get("warnings") or [])

    if not scene.get("field_scene_id"):
        blockers.append("no_enhanced_field_scene")
    if not entities:
        blockers.append("no_entities")
    if mock_marked_real:
        blockers.append("mock_depth_marked_as_real")
    if depth_mode == "mock_adapter_with_real_frame_alignment":
        warnings.append("mock_depth_not_real_metric")
    if depth_mode in ("real_adapter", "authorized_model"):
        depth_q_status = dq.get("depth_quality", "unknown")
    elif not depth_pkg:
        depth_q_status = "missing"
        blockers.append("depth_output_missing")
    else:
        depth_q_status = "mock_labeled"

    geom_unknown = gq.get("geometry_unknown_count", 0)
    if geom_unknown > 0 and geom_unknown >= len(entities):
        warnings.append("all_geometry_unknown")

    field_q = sq.get("scene_quality", "unknown")
    geom_q = gq.get("geometry_quality", "unknown")

    if field_q == "degraded":
        warnings.extend(sq.get("degraded_reasons") or [])
    if geom_q == "degraded":
        warnings.extend(gq.get("degraded_reasons") or [])

    scores = {
        "entity_count": len(entities),
        "geometry_enhanced_count": gq.get("geometry_enhanced_count", 0),
        "geometry_unknown_count": geom_unknown,
        "zone_total": zone.get("total_entity_count", 0),
    }

    if blockers:
        quality_gate = "blocked"
    elif warnings:
        quality_gate = "degraded_pass"
    else:
        quality_gate = "pass"

    return {
        "quality_report_id": f"fcqr_{uuid.uuid4().hex[:12]}",
        "enhanced_field_scene_ref": scene.get("field_scene_id"),
        "field_quality_status": field_q,
        "depth_quality_status": depth_q_status,
        "geometry_quality_status": geom_q,
        "zone_reasonableness_status": "pending_zone_check",
        "quality_scores": scores,
        "quality_blockers": blockers,
        "quality_warnings": sorted(set(warnings)),
        "mock_depth_marked_as_real": mock_marked_real,
        "yolo_execution_mode": yolo_mode,
        "depth_execution_mode": depth_mode,
        "quality_gate_status": quality_gate,
        "candidate_only": True,
    }


def check_zone_reasonableness(
    quality_report: Dict[str, Any],
    zone_summary: Dict[str, Any],
    entities: List[Dict[str, Any]],
    depth_mode: str,
) -> Tuple[str, List[str]]:
    """Check zone assignment is structurally present and not trivially invalid."""
    notes: List[str] = []
    total = zone_summary.get("total_entity_count", 0)
    if total == 0 and entities:
        notes.append("zone_total_mismatch_entity_count")
        return "unreasonable", notes
    if total > 0 and not any(
        zone_summary.get(k, 0) > 0
        for k in ("inner_zone_entity_count", "working_zone_entity_count", "forecast_zone_entity_count", "unknown_zone_entity_count")
    ):
        notes.append("zone_counts_all_zero")
        return "unreasonable", notes
    if depth_mode in ("real_adapter", "authorized_model") and zone_summary.get("unknown_zone_entity_count", 0) == total and total > 0:
        notes.append("all_unknown_zone_with_real_depth_adapter")
        return "weak", notes
    if zone_summary.get("unknown_zone_entity_count", 0) == total and total > 1:
        notes.append("multi_entity_all_unknown_zone")
        return "weak", notes
    return "reasonable", notes
