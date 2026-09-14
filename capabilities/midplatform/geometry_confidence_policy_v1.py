# -*- coding: utf-8 -*-
"""Geometry confidence policy v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

GEOMETRY_CONFIDENCE_POLICY: Dict[str, Any] = {
    "policy_id": "geometry_confidence_policy_v1",
    "estimated_depth_not_high": True,
    "relative_depth_not_high": True,
    "unknown_depth_low": True,
    "degraded_fusion_low": True,
    "low_object_confidence_low": True,
    "conflict_refs_downgrade": True,
    "frame_size_missing_downgrade": True,
}


def compute_geometry_confidence(
    *,
    object_confidence: float,
    depth_confidence: str,
    fusion_confidence: str,
    depth_value_unit: str,
    missing_information: List[str],
    warning_codes: List[str],
    conflict_refs: List[str],
    alignment_confidence: str | None = None,
    frame_size_missing: bool = False,
    pseudo_3d_status: str = "pseudo_3d_estimated",
) -> Tuple[str, List[str]]:
    """Return geometry_confidence level and reliability reasons."""
    reasons: List[str] = []

    if pseudo_3d_status == "pseudo_3d_rejected":
        return "unknown", ["invalid_bbox_geometry_rejected"]
    if pseudo_3d_status == "pseudo_3d_unknown":
        reasons.append("unknown_depth")
        return "low", reasons

    conf = "medium"

    if depth_value_unit == "relative":
        reasons.append("relative_depth_not_metric")
        conf = "low"
    elif depth_value_unit == "unknown":
        reasons.append("unknown_depth_unit")
        return "low", reasons

    if depth_confidence in ("low", "unknown"):
        reasons.append("low_depth_confidence")
        conf = "low"
    if fusion_confidence == "low":
        reasons.append("degraded_fusion_confidence")
        conf = "low"
    if alignment_confidence in ("low", "unknown", "medium") and alignment_confidence:
        if alignment_confidence != "high":
            reasons.append("alignment_confidence_not_high")
            if conf == "medium":
                conf = "low"

    if object_confidence < 0.5:
        reasons.append("low_object_confidence")
        conf = "low"

    if conflict_refs:
        reasons.append("conflict_refs_present")
        conf = "low"

    if frame_size_missing:
        reasons.append("frame_size_missing")
        conf = "low"

    if "depth_out_of_range" in warning_codes:
        reasons.append("depth_out_of_range")
        conf = "low"

    if pseudo_3d_status == "pseudo_3d_weak_estimated":
        reasons.append("weak_relative_projection")
        conf = "low"

    if missing_information:
        if "frame_width" in missing_information or "frame_height" in missing_information:
            reasons.append("frame_dimensions_missing")
            conf = "low"

    # estimated depth must not be high
    if conf == "high":
        conf = "medium"
    if depth_value_unit == "metric" and depth_confidence == "medium" and conf == "medium":
        reasons.append("estimated_depth_not_hardware")
    elif depth_confidence in ("medium", "estimated"):
        reasons.append("estimated_depth_not_hardware")

    return conf, reasons
