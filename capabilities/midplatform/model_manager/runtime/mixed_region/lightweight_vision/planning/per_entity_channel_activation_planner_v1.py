# -*- coding: utf-8 -*-
"""Per-Entity Channel Activation Planner — lightweight vision v1."""

from __future__ import annotations

from typing import Any, Dict, List


def plan_channel_activation_from_entities(
    *,
    entity_candidates: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Plan channels per entity from lightweight vision candidates."""
    result: List[Dict[str, Any]] = []
    for e in entity_candidates:
        eid = e.get("entity_id", "")
        etype = e.get("entity_type_candidate", "")
        channels = ["ownership"]
        if "document" in etype or "sign" in etype or "price" in etype:
            channels.append("text")
        if "document" in etype:
            channels.append("layout")
        if "screen" in etype:
            channels.append("context")
        if etype == "reflection":
            channels = ["ownership", "context"]
        result.append({
            "entity_id": eid,
            "channels": channels,
            "reason": f"lightweight_vision_{etype}_detected",
            "candidate_only": True,
        })
    return result
