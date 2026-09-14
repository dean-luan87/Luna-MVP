# -*- coding: utf-8 -*-
"""Field zone assignment policy v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_geometry_candidate_types_v1 import (
    METRIC_FAR_MAX_M,
    METRIC_MIDDLE_MAX_M,
    METRIC_NEAR_MAX_M,
)

FIELD_ZONE_ASSIGNMENT_POLICY: Dict[str, Any] = {
    "policy_id": "field_zone_assignment_policy_v1",
    "metric_zones": (
        {"range_m": "0-3", "distance_bucket": "near", "field_zone": "inner_zone"},
        {"range_m": "3-10", "distance_bucket": "middle", "field_zone": "working_zone"},
        {"range_m": "10-20", "distance_bucket": "far", "field_zone": "forecast_zone"},
        {"range_m": "20+", "distance_bucket": "unknown", "field_zone": "unknown"},
    ),
    "relative_weak_zones": (
        {"depth_bucket": "near", "field_zone": "inner_zone", "weak_hint": True},
        {"depth_bucket": "middle", "field_zone": "working_zone", "weak_hint": True},
        {"depth_bucket": "far", "field_zone": "forecast_zone", "weak_hint": True},
    ),
    "unknown_unit": {"distance_bucket": "unknown", "field_zone": "unknown"},
    "out_of_range_warning": "depth_out_of_range",
}


def assign_field_zone_from_depth_hint(
    hint: Dict[str, Any],
) -> Tuple[str, str, List[str]]:
    """Return distance_bucket, field_zone, warning_codes."""
    warnings: List[str] = list(hint.get("warning_codes") or [])
    unit = hint.get("depth_value_unit", "unknown")
    bucket = hint.get("depth_bucket", "unknown")
    zone_hint = hint.get("field_zone_hint", "unknown")
    depth_val = hint.get("object_depth_hint") or hint.get("sampled_depth_value")

    if unit == "unknown" or depth_val is None:
        return "unknown", "unknown", warnings

    if unit == "relative":
        warnings.append("relative_depth_not_metric")
        if bucket == "near":
            return "near", "inner_zone", warnings
        if bucket == "middle":
            return "middle", "working_zone", warnings
        if bucket == "far":
            return "far", "forecast_zone", warnings
        return "unknown", "unknown", warnings

    v = float(depth_val)
    if v >= METRIC_FAR_MAX_M:
        warnings.append("depth_out_of_range")
        return "unknown", "unknown", warnings
    if v < 0:
        warnings.append("depth_out_of_range")
        return "unknown", "unknown", warnings
    if v < METRIC_NEAR_MAX_M:
        return "near", "inner_zone", warnings
    if v < METRIC_MIDDLE_MAX_M:
        return "middle", "working_zone", warnings
    if v < METRIC_FAR_MAX_M:
        return "far", "forecast_zone", warnings

    if zone_hint in ("inner_zone", "working_zone", "forecast_zone"):
        dist = {"inner_zone": "near", "working_zone": "middle", "forecast_zone": "far"}.get(zone_hint, "unknown")
        return dist, zone_hint, warnings
    return "unknown", "unknown", warnings
