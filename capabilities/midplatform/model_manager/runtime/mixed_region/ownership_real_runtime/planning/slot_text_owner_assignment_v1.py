# -*- coding: utf-8 -*-
"""slot_text_owner_assignment — text must bind to owner_candidate v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.text_owner_assignment_v1 import (
    assign_text_owners,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_slot_text_owner_assignment(
    *,
    discovery: Dict[str, Any],
    occlusion: Dict[str, Any],
    profile_key: str,
    entity_id_map: Dict[str, str] | None = None,
    blocked_entity_ids: List[str] | None = None,
) -> Dict[str, Any]:
    """
    slot_text_owner_assignment — OCR per owner crop, text bound to owner_entity_id.
    FORBIDDEN: isolated text list without owner.
    """
    mapping = entity_id_map or {}
    blocked = set(blocked_entity_ids or [])

    owner_analysis = {
        "object_candidates": [
            {
                "object_id": e.get("ownership_candidate", {}).get("raw_object_id", e.get("entity_id")),
                "type": e.get("entity_type_candidate"),
            }
            for e in discovery.get("entity_candidates") or []
            if e.get("ownership_candidate", {}).get("raw_object_id", e.get("entity_id")) not in blocked
        ],
    }
    occlusion_graph = {
        "occluded_owner_candidates": [
            mapping.get(x, x) for x in (occlusion.get("occluded_entities") or [])
        ],
    }
    assignment = assign_text_owners(
        owner_analysis=owner_analysis,
        profile_key=profile_key,
        occlusion_graph=occlusion_graph,
    )

    text_owner_assignments: List[Dict[str, Any]] = []
    for entry in assignment.get("text_with_owners") or []:
        raw_owner = (entry.get("owner_candidate") or {}).get("id", "")
        if raw_owner in blocked:
            continue
        owner_entity_id = mapping.get(raw_owner, raw_owner)
        text_owner_assignments.append({
            "text_region_id": entry.get("text_id", _uid("text")),
            "owner_entity_id": owner_entity_id,
            "text_candidate": entry.get("text"),
            "assignment_confidence": entry.get("confidence", 0.0),
            "partially_occluded": entry.get("partially_occluded", False),
            "reflection_artifact": entry.get("reflection_artifact", False),
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        "slot_id": "slot_text_owner_assignment",
        "text_owner_assignments": text_owner_assignments,
        "per_owner_ocr": True,
        "not_flat_merge": True,
        "no_isolated_text_list": all(t.get("owner_entity_id") for t in text_owner_assignments),
        "each_text_has_owner": len(text_owner_assignments) == 0 or all(
            t.get("owner_entity_id") for t in text_owner_assignments
        ),
        "candidate_only": True,
    }
