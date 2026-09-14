# -*- coding: utf-8 -*-
"""Real model execution path failure localizer v1."""

from __future__ import annotations

from typing import Any, Dict, List

_LOCALIZATION_RULES: tuple[tuple[str, str], ...] = (
    ("invalid_bbox", "yolo_output_bridge"),
    ("no_yolo", "yolo_output_bridge"),
    ("no_detection", "yolo_output_bridge"),
    ("blocked_by_authorization", "authorization_policy"),
    ("depth_missing", "depth_output_bridge"),
    ("mock_depth", "depth_output_bridge"),
    ("alignment", "multi_model_alignment"),
    ("timestamp", "multi_model_alignment"),
    ("fusion", "depth_object_fusion"),
    ("geometry", "field_geometry_candidate"),
    ("field_assembly", "field_assembly"),
    ("mock_depth_marked_as_real", "depth_output_bridge"),
    ("zone_", "field_zone_assignment"),
)


def localize_execution_failure_points(
    *,
    failure_points: List[str],
    warnings: List[str],
    quality_blockers: List[str],
    success_path_status: str,
) -> List[Dict[str, Any]]:
    localized: List[Dict[str, Any]] = []
    seen: set[str] = set()
    tokens = list(failure_points) + list(warnings) + list(quality_blockers) + [success_path_status]
    for token in tokens:
        tl = str(token).lower()
        for pattern, area in _LOCALIZATION_RULES:
            if pattern in tl:
                key = f"{area}:{pattern}"
                if key in seen:
                    continue
                seen.add(key)
                localized.append({
                    "failure_token": token,
                    "recommended_fix_area": area,
                    "blocker_or_warning": "blocker" if token in quality_blockers else "warning",
                })
    return localized
