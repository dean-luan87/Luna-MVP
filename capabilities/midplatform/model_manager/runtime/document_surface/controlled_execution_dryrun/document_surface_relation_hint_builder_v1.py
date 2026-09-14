# -*- coding: utf-8 -*-
"""Document Surface — relation hint builder v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.document_surface.document_surface_detector_types_v1 import (
    RUNTIME_ID,
)

IMPLEMENTATION_MODE = "option_a_classical_cv_boundary"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _overlap_ratio(a: List[int], b: List[int]) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    if ix2 <= ix1 or iy2 <= iy1:
        return 0.0
    inter = (ix2 - ix1) * (iy2 - iy1)
    area_a = max(1, (ax2 - ax1) * (ay2 - ay1))
    area_b = max(1, (bx2 - bx1) * (by2 - by1))
    return inter / min(area_a, area_b)


def build_relation_hint_candidates(
    *,
    surfaces: List[Dict[str, Any]],
    category: str,
) -> List[Dict[str, Any]]:
    relations: List[Dict[str, Any]] = []
    if len(surfaces) < 2:
        return relations

    for i in range(len(surfaces)):
        for j in range(i + 1, len(surfaces)):
            a, b = surfaces[i], surfaces[j]
            bbox_a = a.get("bbox_candidate") or []
            bbox_b = b.get("bbox_candidate") or []
            if len(bbox_a) < 4 or len(bbox_b) < 4:
                continue
            overlap = _overlap_ratio(bbox_a, bbox_b)
            if overlap <= 0.05:
                continue
            if category == "receipt_attached_to_package_controlled":
                rel_type = "attached_to"
            elif category == "two_overlapping_papers_controlled":
                rel_type = "occludes" if overlap > 0.2 else "overlaps"
            else:
                rel_type = "uncertain"
            relations.append({
                "relation_id": _uid("rel"),
                "relation_type_candidate": rel_type,
                "entity_a": a.get("surface_id"),
                "entity_b": b.get("surface_id"),
                "evidence_basis": "spatial_overlap_candidate",
                "source_runtime": RUNTIME_ID,
                "implementation_mode_candidate": IMPLEMENTATION_MODE,
                "candidate_only": True,
                "not_fact": True,
            })
    return relations
