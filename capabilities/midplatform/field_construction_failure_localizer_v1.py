# -*- coding: utf-8 -*-
"""Field construction failure localizer v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.real_model_field_construction_hardening_types_v1 import (
    FAILURE_LOCALIZATION_AREAS,
)


_LOCALIZATION_RULES: Tuple[Tuple[str, str, str], ...] = (
    ("image_path", "frame_input_loader", "warning"),
    ("invalid_bbox", "yolo_output_bridge", "blocker"),
    ("no_valid_yolo", "yolo_output_bridge", "blocker"),
    ("no_yolo_detection", "yolo_output_bridge", "blocker"),
    ("blocked_by_authorization", "authorization_policy", "blocker"),
    ("depth_missing", "depth_output_bridge", "warning"),
    ("depth_observation_missing", "depth_output_bridge", "warning"),
    ("mock_depth", "depth_output_bridge", "warning"),
    ("low_depth_confidence", "depth_output_bridge", "warning"),
    ("alignment", "multi_model_alignment", "blocker"),
    ("timestamp", "multi_model_alignment", "warning"),
    ("fusion", "depth_object_fusion", "warning"),
    ("geometry", "field_geometry_candidate", "warning"),
    ("field_assembly", "field_assembly", "blocker"),
    ("traceability", "traceability_policy", "warning"),
    ("candidate_conversion", "candidate_conversion", "warning"),
)


def localize_failure_points(
    *,
    failure_points: List[str],
    warnings: List[str],
    success_path_status: str,
) -> List[Dict[str, Any]]:
    """Map failure/warning tokens to upstream fix areas."""
    localized: List[Dict[str, Any]] = []
    tokens = list(failure_points) + list(warnings) + [success_path_status]
    seen: set[str] = set()

    for token in tokens:
        token_l = str(token).lower()
        for pattern, area, severity in _LOCALIZATION_RULES:
            if pattern in token_l and area in FAILURE_LOCALIZATION_AREAS:
                key = f"{area}:{pattern}"
                if key in seen:
                    continue
                seen.add(key)
                localized.append({
                    "failure_token": token,
                    "recommended_fix_area": area,
                    "blocker_or_warning": severity,
                    "pattern_matched": pattern,
                })

    if success_path_status.startswith("failed_") and not localized:
        area = "field_assembly"
        if "alignment" in success_path_status:
            area = "multi_model_alignment"
        elif "yolo" in success_path_status:
            area = "yolo_output_bridge"
        localized.append({
            "failure_token": success_path_status,
            "recommended_fix_area": area,
            "blocker_or_warning": "blocker",
            "pattern_matched": "success_path_status",
        })

    return localized


def summarize_recommended_fix_areas(localized: List[Dict[str, Any]]) -> List[str]:
    areas = sorted({item["recommended_fix_area"] for item in localized})
    return areas
