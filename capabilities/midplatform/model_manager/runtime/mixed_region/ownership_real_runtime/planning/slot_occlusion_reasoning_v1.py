# -*- coding: utf-8 -*-
"""slot_occlusion_reasoning — Occlusion Graph v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.occlusion_graph_v1 import (
    build_occlusion_graph,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_slot_occlusion_reasoning(
    *,
    discovery: Dict[str, Any],
    profile_key: str,
    entity_id_map: Dict[str, str] | None = None,
    blocked_entity_ids: List[str] | None = None,
) -> Dict[str, Any]:
    """
    slot_occlusion_reasoning — occlusion relations between carriers.
    Occluded ≠ absent.
    """
    owner_analysis = {
        "object_candidates": [
            {
                "object_id": e.get("ownership_candidate", {}).get("raw_object_id", e.get("entity_id")),
                "type": e.get("entity_type_candidate"),
            }
            for e in discovery.get("entity_candidates") or []
        ],
    }
    graph = build_occlusion_graph(owner_analysis=owner_analysis, profile_key=profile_key)
    mapping = entity_id_map or {}
    blocked = set(blocked_entity_ids or [])

    relations: List[Dict[str, Any]] = []
    for rel in graph.get("occlusion_relation") or []:
        front_raw = rel.get("front", "")
        behind_raw = rel.get("behind", "")
        if front_raw in blocked or behind_raw in blocked:
            continue
        front = mapping.get(front_raw, front_raw)
        behind = mapping.get(behind_raw, behind_raw)
        relation_type = "occludes"
        if rel.get("occlusion_type") == "reflection_not_occlusion":
            relation_type = "reflection_of"
        elif rel.get("occlusion_type") == "attached_to_product":
            relation_type = "attached_to"
        relations.append({
            "relation_id": _uid("rel"),
            "entity_a": front,
            "entity_b": behind,
            "relation_type": relation_type,
            "occlusion_type": rel.get("occlusion_type"),
            "candidate_only": True,
        })

    return {
        "slot_id": "slot_occlusion_reasoning",
        "relation_candidates": relations,
        "occluded_entities": [
            r.get("entity_b") for r in relations if r.get("relation_type") == "occludes"
        ],
        "not_assume_missing_absent": graph.get("not_assume_missing_title_absent") is True,
        "candidate_only": True,
    }
