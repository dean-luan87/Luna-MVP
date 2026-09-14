# -*- coding: utf-8 -*-
"""Document Surface — text owner assignment adapter v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

RELATION_TO_BASIS = {
    "occludes": "overlap_relation",
    "overlaps": "overlap_relation",
    "attached_to": "attached_to_relation",
    "behind": "overlap_relation",
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_text_owner_assignment_candidates(
    *,
    document_surface_candidates: List[Dict[str, Any]],
    relation_hint_candidates: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    Text owner assignment AFTER surface candidates — no OCR text.
    Each assignment binds owner_entity_candidate_ref with assignment_basis.
    """
    relation_map: Dict[str, str] = {}
    for r in relation_hint_candidates:
        entity_a = r.get("entity_a", "")
        basis = RELATION_TO_BASIS.get(r.get("relation_type_candidate", ""), "surface_containment")
        relation_map[entity_a] = basis

    assignments: List[Dict[str, Any]] = []
    for s in document_surface_candidates:
        sid = s.get("surface_id", "")
        owner = s.get("owner_entity_candidate_ref", "")
        basis = relation_map.get(sid, "surface_containment")
        if s.get("visibility_status_candidate") == "uncertain":
            basis = "uncertain"

        assignments.append({
            "text_region_id": _uid("txt"),
            "owner_entity_candidate_ref": owner,
            "surface_id": sid,
            "assignment_status_candidate": "surface_bound_candidate",
            "assignment_basis": basis,
            "text_content": None,
            "no_ocr_text": True,
            "owner_required_for_assignment": bool(owner),
            "candidate_only": True,
            "not_fact": True,
        })

    return assignments
