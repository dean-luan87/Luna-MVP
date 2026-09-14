# -*- coding: utf-8 -*-
"""Document Surface — overlap separation runtime v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

OVERLAP_CATEGORIES = (
    "two_overlapping_papers_clear_edges",
    "two_overlapping_papers_low_overlap",
    "two_overlapping_papers_high_overlap",
)


def _uid(p: str) -> str:
    return f"{p}_{uuid4().hex[:8]}"


def apply_overlap_separation_strategy(
    *,
    gated_result: Dict[str, Any],
    category: str,
) -> Dict[str, Any]:
    if category not in OVERLAP_CATEGORIES:
        return {**gated_result, "overlap_strategy": {"applied": False}}

    surfaces = list(gated_result.get("document_surface_candidates") or [])
    relations: List[Dict[str, Any]] = []
    uncertain = False
    separation_success = False

    if category == "two_overlapping_papers_clear_edges" and len(surfaces) >= 2:
        relations.append({
            "relation_id": _uid("rel"),
            "relation_type_candidate": "overlaps",
            "entity_a": surfaces[0].get("surface_id"),
            "entity_b": surfaces[1].get("surface_id"),
            "evidence_basis": "geometric_overlap_candidate",
            "candidate_only": True,
            "not_fact": True,
        })
        separation_success = False  # never upgrade to successful separation
    elif category == "two_overlapping_papers_low_overlap" and len(surfaces) >= 2:
        relations.append({
            "relation_id": _uid("rel"),
            "relation_type_candidate": "overlaps",
            "entity_a": surfaces[0].get("surface_id"),
            "entity_b": surfaces[1].get("surface_id") if len(surfaces) > 1 else surfaces[0].get("surface_id"),
            "evidence_basis": "partial_boundary_hypothesis",
            "candidate_only": True,
            "not_fact": True,
        })
    elif category == "two_overlapping_papers_high_overlap" or len(surfaces) < 2:
        uncertain = True
        relations.append({
            "relation_id": _uid("rel"),
            "relation_type_candidate": "uncertain_relation",
            "entity_a": surfaces[0].get("surface_id") if surfaces else None,
            "entity_b": None,
            "evidence_basis": "insufficient_separation_evidence",
            "overlap_relation_uncertain_candidate": True,
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        **gated_result,
        "relation_hint_candidates": relations,
        "overlap_strategy": {
            "applied": True,
            "category": category,
            "surface_count": len(surfaces),
            "uncertain_relation": uncertain,
            "separation_success": separation_success,
            "overlapping_documents_under_separated_watch": len(surfaces) < 2,
            "no_fake_relation": True,
            "no_forced_two_surface": True,
            "candidate_only": True,
            "not_fact": True,
        },
    }
