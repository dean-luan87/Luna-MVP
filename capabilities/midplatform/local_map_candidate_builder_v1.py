# -*- coding: utf-8 -*-
"""Local map candidate builder v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional


def build_local_map_candidate(
    *,
    adapter_input: Dict[str, Any],
    raw_output: Dict[str, Any],
    poses: List[Dict[str, Any]],
    anchors: List[Dict[str, Any]],
    trajectory: Optional[Dict[str, Any]] = None,
    case_overrides: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Assemble LocalMapCandidate from inspection-based outputs."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return None
    raw_ref = raw_output.get("raw_output_id")
    session_ref = adapter_input.get("session_ref", "session_unknown")
    frames = adapter_input.get("_frame_packages") or []
    scenes = adapter_input.get("_scene_packages") or []
    drift_risk = overrides.get("drift_risk", (raw_output.get("raw_quality_payload") or {}).get("drift_risk", poses[0].get("drift_risk", "low") if poses else "unknown"))
    high_drift = drift_risk in ("high", "severe")
    scale_status = overrides.get("scale_status", poses[0].get("scale_status", "scale_estimated") if poses else "scale_unknown")
    no_pose = overrides.get("no_pose") or len(poses) == 0

    map_quality = "degraded" if no_pose or high_drift or scale_status == "scale_unknown" else overrides.get("map_quality", "acceptable")
    if scale_status == "scale_unknown" and map_quality == "high":
        map_quality = "acceptable"
    missing = list(overrides.get("missing_information") or [])
    if no_pose:
        missing.append("pose_missing_degraded_local_map")

    raw_map = raw_output.get("raw_map_payload") or {}
    map_id = f"lmc_{uuid.uuid4().hex[:12]}"
    return {
        "local_map_candidate_id": map_id,
        "source_raw_output_ref": raw_ref,
        "session_ref": session_ref,
        "frame_refs": [f.get("frame_ref") for f in frames],
        "camera_trajectory_ref": (trajectory or {}).get("camera_trajectory_candidate_id"),
        "spatial_anchor_refs": [a["spatial_anchor_candidate_id"] for a in anchors],
        "associated_field_scene_refs": [s.get("field_scene_id") for s in scenes if s.get("field_scene_id")],
        "local_geometry_summary": {
            "pose_count": len(poses),
            "anchor_count": len(anchors),
            "entity_count": sum(len(s.get("entity_candidates") or []) for s in scenes),
            "map_type": raw_map.get("type", "sparse_point_cloud"),
            "point_count": raw_map.get("point_count"),
        },
        "map_quality": map_quality,
        "drift_summary": {"drift_risk": drift_risk, "high_drift": high_drift},
        "missing_information": missing,
        "conflict_summary": overrides.get("conflict_summary") or [],
        "source_refs": [adapter_input.get("adapter_input_id"), raw_ref] + [s.get("field_scene_id") for s in scenes if s.get("field_scene_id")],
        "evidence_refs": [adapter_input.get("model_ref")],
        "traceability_refs": list(adapter_input.get("traceability_refs") or []) + [map_id],
        "candidate_only": True,
    }


def build_map_quality_candidate(
    *,
    local_map: Optional[Dict[str, Any]],
    raw_output: Dict[str, Any],
    poses: List[Dict[str, Any]],
    anchors: List[Dict[str, Any]],
    case_overrides: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Build MapQualityCandidate from local map and spatial outputs."""
    overrides = case_overrides or {}
    if raw_output.get("_blocked"):
        return None
    raw_ref = raw_output.get("raw_output_id")
    raw_quality = raw_output.get("raw_quality_payload") or {}
    drift_risk = overrides.get("drift_risk", raw_quality.get("drift_risk", (local_map or {}).get("drift_summary", {}).get("drift_risk", "low")))
    high_drift = drift_risk in ("high", "severe")
    scale_status = overrides.get("scale_status", raw_quality.get("scale_status", poses[0].get("scale_status", "scale_estimated") if poses else "scale_unknown"))
    scale_rel = "unreliable" if scale_status == "scale_unknown" else ("degraded" if high_drift else "acceptable")

    warnings: List[str] = []
    if high_drift:
        warnings.append("high_drift_map_quality_degraded")
    if scale_status == "scale_unknown":
        warnings.append("scale_unknown_not_high_confidence")
    if local_map and local_map.get("map_quality") == "degraded":
        warnings.append("local_map_degraded")

    quality_status = "degraded" if warnings else "acceptable"
    if scale_status == "scale_unknown" and quality_status == "high":
        quality_status = "degraded"

    mq_id = f"mqc_{uuid.uuid4().hex[:12]}"
    return {
        "map_quality_candidate_id": mq_id,
        "source_raw_output_ref": raw_ref,
        "local_map_ref": (local_map or {}).get("local_map_candidate_id"),
        "pose_quality": "degraded" if not poses else ("degraded" if high_drift else "acceptable"),
        "anchor_quality": "acceptable" if anchors else "missing",
        "drift_risk": drift_risk,
        "scale_reliability": scale_rel,
        "coverage_status": raw_quality.get("coverage", "partial" if len(poses) < 2 else "sufficient"),
        "quality_status": quality_status,
        "blockers": [],
        "warnings": warnings,
        "source_refs": [raw_ref],
        "traceability_refs": [mq_id, raw_ref],
        "candidate_only": True,
    }
