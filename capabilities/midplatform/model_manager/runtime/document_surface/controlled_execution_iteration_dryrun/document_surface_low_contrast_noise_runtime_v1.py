# -*- coding: utf-8 -*-
"""Document Surface — low contrast noise runtime v1."""

from __future__ import annotations

from typing import Any, Dict, List

LOW_CONTRAST_CATEGORIES = (
    "low_contrast_single_paper",
    "low_contrast_texture_false_positive",
)
CAP = 5


def _overlap_bbox(a: List[int], b: List[int]) -> float:
    if len(a) < 4 or len(b) < 4:
        return 0.0
    ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
    ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter = (ix2 - ix1) * (iy2 - iy1)
    area_a = max(1, (a[2] - a[0]) * (a[3] - a[1]))
    return inter / area_a


def apply_low_contrast_noise_strategy(
    *,
    gated_result: Dict[str, Any],
    category: str,
) -> Dict[str, Any]:
    if category not in LOW_CONTRAST_CATEGORIES:
        return {**gated_result, "low_contrast_strategy": {"applied": False}}

    surfaces = list(gated_result.get("document_surface_candidates") or [])
    filtered: List[Dict[str, Any]] = []
    suppressed = 0
    for s in surfaces:
        bbox = s.get("bbox_candidate") or []
        dup = any(_overlap_bbox(bbox, f.get("bbox_candidate") or []) > 0.85 for f in filtered)
        if dup:
            suppressed += 1
            continue
        if category == "low_contrast_texture_false_positive" and (s.get("boundary_confidence_candidate") or 0) < 0.4:
            s = {**s, "false_surface_candidate": True, "gate_action": "mark_low_confidence"}
        filtered.append(s)

    if len(filtered) > CAP:
        filtered = filtered[:CAP]
        capped = True
    else:
        capped = False

    status = "low_confidence_boundary_candidate"
    next_action = "request_better_view_or_lighting" if len(filtered) <= 1 else None

    return {
        **gated_result,
        "document_surface_candidates": filtered,
        "runtime_status_candidate": status,
        "next_action_candidate": next_action,
        "low_contrast_strategy": {
            "applied": True,
            "suppressed_duplicates": suppressed,
            "capped": capped,
            "output_count": len(filtered),
            "excessive_candidate_suppression": suppressed > 0 or capped,
            "candidate_only": True,
            "not_fact": True,
        },
    }
