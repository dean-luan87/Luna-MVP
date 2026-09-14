# -*- coding: utf-8 -*-
"""Field quality summary builders v1."""

from __future__ import annotations

from typing import Any, Dict, List

FIELD_SCENE_QUALITY_SUMMARY_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_scene_quality_summary_registry_v1",
}
FIELD_DEPTH_QUALITY_SUMMARY_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_depth_quality_summary_registry_v1",
}
FIELD_GEOMETRY_QUALITY_SUMMARY_REGISTRY: Dict[str, Any] = {
    "registry_id": "field_geometry_quality_summary_registry_v1",
}


def build_depth_quality_summary(
    entities: List[Dict[str, Any]],
    hints: List[Dict[str, Any]],
) -> Dict[str, Any]:
    unknown_count = sum(1 for e in entities if e.get("depth_hint") is None)
    estimated_count = sum(1 for e in entities if e.get("depth_source") == "estimated")
    total = max(len(entities), 1)
    ratio_unknown = unknown_count / total
    quality = "good"
    if ratio_unknown > 0.5:
        quality = "degraded"
    elif unknown_count > 0:
        quality = "mixed"
    return {
        "depth_quality": quality,
        "unknown_depth_count": unknown_count,
        "estimated_depth_count": estimated_count,
        "depth_error_expected_all": all(e.get("depth_error_expected") is True for e in entities),
        "hint_count": len(hints),
        "degraded_reasons": (["many_unknown_depth"] if ratio_unknown > 0.5 else []),
    }


def build_geometry_quality_summary(
    entities: List[Dict[str, Any]],
    geometries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    enhanced = sum(1 for e in entities if e.get("entity_status") == "entity_geometry_enhanced")
    unknown = sum(1 for e in entities if e.get("entity_status") == "entity_geometry_unknown")
    only_2d = sum(1 for e in entities if e.get("entity_status") == "entity_2d_only")
    total = max(len(entities), 1)
    ratio_unknown = unknown / total
    quality = "good"
    if ratio_unknown > 0.5 or only_2d > enhanced:
        quality = "degraded"
    elif unknown > 0 or only_2d > 0:
        quality = "mixed"
    return {
        "geometry_quality": quality,
        "geometry_enhanced_count": enhanced,
        "geometry_unknown_count": unknown,
        "entity_2d_only_count": only_2d,
        "geometry_candidate_count": len(geometries),
        "degraded_reasons": (["many_geometry_unknown"] if ratio_unknown > 0.5 else []),
    }


def build_scene_quality_summary(
    entities: List[Dict[str, Any]],
    depth_summary: Dict[str, Any],
    geometry_summary: Dict[str, Any],
    assembly_warnings: List[str],
) -> Dict[str, Any]:
    quality = "good"
    reasons: List[str] = []
    if depth_summary.get("depth_quality") == "degraded":
        quality = "degraded"
        reasons.append("depth_quality_degraded")
    if geometry_summary.get("geometry_quality") == "degraded":
        quality = "degraded" if quality == "degraded" else "mixed"
        reasons.append("geometry_quality_degraded")
    if "frame_mismatch" in assembly_warnings or "timestamp_warning" in assembly_warnings:
        quality = "degraded"
        reasons.append("frame_or_timestamp_warning")
    low_conf = sum(1 for e in entities if "low_object_confidence" in (e.get("warning_codes") or []))
    if low_conf > 0:
        reasons.append("low_confidence_objects_present")
    return {
        "scene_quality": quality,
        "entity_count": len(entities),
        "low_confidence_entity_count": low_conf,
        "degraded_reasons": reasons,
    }
