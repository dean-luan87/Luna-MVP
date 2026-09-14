# -*- coding: utf-8 -*-
"""Per-Entity Channel Activation Planner v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

CHANNEL_MAP = {
    "document": ["ownership", "text", "layout"],
    "product_package": ["ownership", "text", "visual"],
    "price_label": ["ownership", "text"],
    "background_ad": ["ownership", "text", "visual"],
    "business_sign": ["ownership", "text", "visual"],
    "reflection": ["ownership", "text", "context"],
    "device": ["ownership", "context"],
    "screen_content": ["ownership", "text", "context"],
    "environment_text": ["ownership", "text"],
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def plan_per_entity_channel_activation(
    *,
    entity_candidates: List[Dict[str, Any]],
    text_owner_assignments: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Plan which channels activate per entity — not global model start."""
    per_entity: List[Dict[str, Any]] = []
    all_caps: List[str] = []

    owners_with_text = {t.get("owner_entity_id") for t in text_owner_assignments}

    for entity in entity_candidates:
        eid = entity.get("entity_id", "")
        etype = entity.get("entity_type_candidate", "unknown")
        slots = CHANNEL_MAP.get(etype, ["ownership"])
        if eid not in owners_with_text:
            slots = [s for s in slots if s != "text"]

        caps = [f"understand_region_{s}" if s != "layout" else "understand_region_layout" for s in slots]
        for c in caps:
            if c not in all_caps:
                all_caps.append(c)

        per_entity.append({
            "entity_id": eid,
            "activated_channels": slots,
            "activated_capabilities": caps,
            "ocr_per_entity": "text" in slots and eid in owners_with_text,
            "candidate_only": True,
        })

    return {
        "activation_id": _uid("pca"),
        "per_entity_activation": per_entity,
        "activated_capabilities": all_caps,
        "not_global_model_start": True,
        "candidate_only": True,
    }
