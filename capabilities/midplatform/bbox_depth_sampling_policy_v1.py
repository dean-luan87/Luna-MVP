# -*- coding: utf-8 -*-
"""BBox depth sampling policy v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.depth_object_fusion_types_v1 import (
    METRIC_FAR_MAX_M,
    METRIC_MIDDLE_MAX_M,
    METRIC_NEAR_MAX_M,
)
from capabilities.midplatform.field_scene_small_range_types_v1 import bbox_center

BBOX_DEPTH_SAMPLING_POLICY: Dict[str, Any] = {
    "policy_id": "bbox_depth_sampling_policy_v1",
    "default_method": "bbox_center_sample",
    "fallback_method": "bbox_center_median_sample",
    "reserved_methods": ("bbox_area_sample",),
    "invalid_bbox_reject": True,
}


def _bbox_valid(bbox: Dict[str, Any], fw: int, fh: int) -> Tuple[bool, str]:
    if not bbox:
        return False, "missing_bbox"
    try:
        x1, y1 = float(bbox.get("x1", 0)), float(bbox.get("y1", 0))
        x2, y2 = float(bbox.get("x2", 0)), float(bbox.get("y2", 0))
    except (TypeError, ValueError):
        return False, "invalid_bbox_coords"
    if x2 <= x1 or y2 <= y1:
        return False, "invalid_bbox_dimensions"
    if x1 < 0 or y1 < 0 or x2 > fw or y2 > fh:
        return False, "bbox_out_of_frame"
    return True, ""


def _sample_from_map(
    depth: Dict[str, Any],
    center: Dict[str, float],
    method: str = "bbox_center_sample",
) -> Optional[float]:
    samples = depth.get("depth_map_samples") or depth.get("depth_map_mock") or {}
    key = f"{int(center['x'])}_{int(center['y'])}"
    if key in samples:
        return float(samples[key])
    if method == "bbox_center_median_sample":
        med_key = f"med_{int(center['x'])}_{int(center['y'])}"
        if med_key in samples:
            return float(samples[med_key])
    grid = depth.get("depth_map_grid")
    if grid and isinstance(grid, list):
        cy, cx = int(center["y"]), int(center["x"])
        if 0 <= cy < len(grid) and 0 <= cx < len(grid[cy]):
            return float(grid[cy][cx])
    if depth.get("sampled_depth_override") is not None:
        return float(depth["sampled_depth_override"])
    return None


def depth_bucket_and_zone(
    value: Optional[float],
    unit: str,
) -> Tuple[str, str, List[str]]:
    warnings: List[str] = []
    if value is None or unit == "unknown":
        return "unknown", "unknown", warnings
    if unit == "relative":
        warnings.append("relative_depth_not_metric")
        norm = float(value)
        if norm < 0.33:
            return "near", "inner_zone", warnings
        if norm < 0.66:
            return "middle", "working_zone", warnings
        return "far", "forecast_zone", warnings
    v = float(value)
    if v < 0 or v >= METRIC_FAR_MAX_M:
        if v >= METRIC_FAR_MAX_M:
            warnings.append("depth_out_of_range")
        return "unknown", "unknown", warnings
    if v <= METRIC_NEAR_MAX_M:
        return "near", "inner_zone", warnings
    if v <= METRIC_MIDDLE_MAX_M:
        return "middle", "working_zone", warnings
    return "far", "forecast_zone", warnings


def sample_depth_for_object_bbox(
    obj: Dict[str, Any],
    depth: Optional[Dict[str, Any]],
    *,
    method: str = "bbox_center_sample",
) -> Tuple[Optional[float], str, List[str], List[str]]:
    warnings: List[str] = []
    missing: List[str] = []
    fw = int(obj.get("frame_width", 640))
    fh = int(obj.get("frame_height", 480))
    valid, reason = _bbox_valid(obj.get("bbox") or {}, fw, fh)
    if not valid:
        return None, reason, warnings, missing

    if not depth or not depth.get("depth_map_ref"):
        missing.append("depth_map_missing")
        return None, "depth_map_missing", warnings, missing

    center = bbox_center(obj.get("bbox") or {})
    shape = depth.get("depth_map_shape") or []
    if shape and len(shape) >= 2:
        dh, dw = int(shape[0]), int(shape[1])
        if dw != fw or dh != fh:
            warnings.append("depth_map_shape_mismatch")

    sampled = _sample_from_map(depth, center, method)
    if sampled is None:
        missing.append("depth_sample_failed")
        return None, "depth_sample_failed", warnings, missing
    return sampled, "sampled", warnings, missing
