# -*- coding: utf-8 -*-
"""Document Surface — attached-to uncertainty runtime v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

ATTACHED_CATEGORIES = (
    "receipt_attached_clear",
    "receipt_attached_uncertain",
)
MIN_ATTACHED_CONF = 0.55


def _uid(p: str) -> str:
    return f"{p}_{uuid4().hex[:8]}"


def apply_attached_to_uncertainty_strategy(
    *,
    pipeline_result: Dict[str, Any],
    category: str,
) -> Dict[str, Any]:
    if category not in ATTACHED_CATEGORIES:
        return {**pipeline_result, "attached_to_strategy": {"applied": False}}

    surfaces = list(pipeline_result.get("document_surface_candidates") or [])
    relations: List[Dict[str, Any]] = list(pipeline_result.get("relation_hint_candidates") or [])
    uncertain = category == "receipt_attached_uncertain"

    if len(surfaces) >= 2 and not uncertain:
        conf_ok = all((s.get("boundary_confidence_candidate") or 0) >= MIN_ATTACHED_CONF for s in surfaces[:2])
        if conf_ok:
            relations.append({
                "relation_id": _uid("rel"),
                "relation_type_candidate": "attached_to",
                "entity_a": surfaces[0].get("surface_id"),
                "entity_b": surfaces[1].get("surface_id"),
                "evidence_basis": "spatial_adjacency_candidate",
                "candidate_only": True,
                "not_fact": True,
            })
        else:
            uncertain = True
    else:
        uncertain = True

    if uncertain:
        relations = [{
            "relation_id": _uid("rel"),
            "relation_type_candidate": "uncertain_relation",
            "uncertain_attached_to_candidate": True,
            "entity_a": surfaces[0].get("surface_id") if surfaces else None,
            "entity_b": surfaces[1].get("surface_id") if len(surfaces) > 1 else None,
            "evidence_basis": "insufficient_attachment_evidence",
            "candidate_only": True,
            "not_fact": True,
        }]
        next_action = "request_more_evidence"
    else:
        next_action = None

    return {
        **pipeline_result,
        "relation_hint_candidates": relations,
        "next_action_candidate": next_action,
        "attached_to_strategy": {
            "applied": True,
            "uncertain": uncertain,
            "no_receipt_text_to_package": True,
            "candidate_only": True,
            "not_fact": True,
        },
    }
