# -*- coding: utf-8 -*-
"""Pseudo 3D projection policy v1."""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.field_scene_small_range_types_v1 import bbox_center

PSEUDO_3D_PROJECTION_POLICY: Dict[str, Any] = {
    "policy_id": "pseudo_3d_projection_policy_v1",
    "coordinate_mode": "normalized_image_depth_hint",
    "projection_formula": {
        "x_norm": "bbox_center_x / frame_width",
        "y_norm": "bbox_center_y / frame_height",
        "z_hint": "object_depth_hint | weak_relative_depth | unknown",
    },
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


def compute_bbox_center(
    bbox: Dict[str, Any],
    *,
    frame_width: int,
    frame_height: int,
) -> Tuple[Optional[Dict[str, float]], bool, str]:
    """Return bbox center, valid flag, reason."""
    valid, reason = _bbox_valid(bbox, frame_width, frame_height)
    if not valid:
        return None, False, reason
    center = bbox_center(bbox)
    if center["x"] < 0 or center["y"] < 0 or center["x"] > frame_width or center["y"] > frame_height:
        return center, False, "bbox_center_out_of_frame"
    return center, True, ""


def estimate_pseudo_3d_position(
    *,
    bbox_center_pt: Dict[str, float],
    frame_width: int,
    frame_height: int,
    depth_hint: Optional[float],
    depth_value_unit: str,
    bbox_valid: bool = True,
) -> Tuple[Dict[str, Any], str]:
    """Return pseudo_3d_position dict and pseudo_3d_status."""
    if not bbox_valid or frame_width <= 0 or frame_height <= 0:
        return {
            "x_norm": None,
            "y_norm": None,
            "z_hint": None,
            "coordinate_mode": "normalized_image_depth_hint",
        }, "pseudo_3d_rejected"

    x_norm = bbox_center_pt["x"] / float(frame_width)
    y_norm = bbox_center_pt["y"] / float(frame_height)

    if depth_value_unit == "unknown" or depth_hint is None:
        return {
            "x_norm": x_norm,
            "y_norm": y_norm,
            "z_hint": None,
            "coordinate_mode": "normalized_image_depth_hint",
        }, "pseudo_3d_unknown"

    if depth_value_unit == "relative":
        return {
            "x_norm": x_norm,
            "y_norm": y_norm,
            "z_hint": float(depth_hint),
            "coordinate_mode": "normalized_image_depth_hint",
            "relative_depth_weak": True,
        }, "pseudo_3d_weak_estimated"

    return {
        "x_norm": x_norm,
        "y_norm": y_norm,
        "z_hint": float(depth_hint),
        "coordinate_mode": "normalized_image_depth_hint",
    }, "pseudo_3d_estimated"
