# -*- coding: utf-8 -*-
"""Information Ownership Graph — entity_candidates + relation_candidates v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _entity_completeness(
    *,
    channels: Dict[str, Any],
    missing: List[Dict[str, Any]],
    entity_id: str,
) -> Dict[str, Any]:
    text_ch = channels.get("text") or {}
    has_text = bool(text_ch.get("candidates"))
    entity_missing = [m for m in missing if m.get("owner") == entity_id]
    if entity_missing:
        return {
            "information_completeness": 0.7,
            "missing_reason": entity_missing[0].get("reason"),
            "not_confidence": True,
        }
    if has_text:
        return {"information_completeness": 0.9, "not_confidence": True}
    return {"information_completeness": 0.3, "not_confidence": True}


def build_information_ownership_graph(
    *,
    discovery: Dict[str, Any],
    channel_selection: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build Ownership Graph output structure:
    entity_candidates[] + relation_candidates[]
    """
    if discovery.get("runtime_unavailable"):
        return {
            "graph_id": _uid("iog"),
            "entity_candidates": [],
            "relation_candidates": [],
            "graph_status": "runtime_unavailable",
            "candidate_only": True,
        }

    entities_raw = discovery.get("raw_entities") or []
    ocr_map = discovery.get("ocr_per_entity") or {}
    visual_map = discovery.get("visual_per_entity") or {}
    channels_map = discovery.get("channels_per_entity") or {}
    missing = discovery.get("missing_information") or []
    selection = channel_selection or {}

    entity_candidates: List[Dict[str, Any]] = []
    for ent in entities_raw:
        eid = ent.get("entity_id", "")
        selected = selection.get("per_entity_selection", {}).get(eid, channels_map.get(eid, []))
        text_cands = ocr_map.get(eid, []) if "text" in selected else []
        visual_raw = visual_map.get(eid, {}) if "visual" in selected else {}

        channels: Dict[str, Any] = {
            "ownership": {
                "activated": "ownership" in selected,
                "ownership_candidate": {"type": ent.get("ownership_type"), "id": eid},
            },
            "text": {
                "activated": "text" in selected,
                "candidates": text_cands,
            },
            "visual": {
                "activated": "visual" in selected,
                "features": visual_raw.get("features", []),
                "scene_hint": visual_raw.get("scene_hint"),
            },
            "spatial": {
                "activated": "spatial" in selected,
                "hints": ["partially_occluded"] if any(
                    m.get("owner") == eid and m.get("reason") == "occluded" for m in missing
                ) else [],
            },
            "context": {"activated": False, "relations": []},
        }

        entity_candidates.append({
            "entity_id": eid,
            "ownership_candidate": {"type": ent.get("ownership_type"), "id": eid, "position": ent.get("position")},
            "information_channels": channels,
            "completeness": _entity_completeness(channels=channels, missing=missing, entity_id=eid),
            "candidate_only": True,
            "not_fact": True,
        })

    relation_candidates = [
        {
            "entity_a": r.get("entity_a"),
            "entity_b": r.get("entity_b"),
            "relation": r.get("relation"),
            "direction": r.get("direction"),
            "candidate_only": True,
        }
        for r in discovery.get("relations_raw") or []
    ]

    return {
        "graph_id": _uid("iog"),
        "scene_type": discovery.get("scene_type"),
        "entity_candidates": entity_candidates,
        "relation_candidates": relation_candidates,
        "entity_count": len(entity_candidates),
        "relation_count": len(relation_candidates),
        "not_flat_text_visual_spatial": True,
        "candidate_only": True,
    }
