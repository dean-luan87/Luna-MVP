# -*- coding: utf-8 -*-
"""Per-Entity Channel Activation Adapter — dryrun v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

CHANNEL_REASONS = {
    "document_surface": "document_surface_with_visible_text",
    "product_package_surface": "product_package_with_label",
    "price_label_surface": "price_label_attached",
    "background_ad_surface": "background_advertisement",
    "business_sign_surface": "business_sign_with_text",
    "reflection_surface": "reflection_artifact_not_real_sign",
    "dynamic_object_surface": "dynamic_object_context",
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def adapt_per_entity_channel_activation(
    *,
    entity_candidates: List[Dict[str, Any]],
    text_owner_assignments: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Per-entity channel activation candidates — NOT global model start."""
    owners_with_text = {t.get("owner_entity_id") for t in text_owner_assignments}
    candidates: List[Dict[str, Any]] = []
    all_channels: List[str] = []

    for entity in entity_candidates:
        eid = entity.get("entity_id", "")
        etype = entity.get("entity_type_candidate", "unknown")
        channels = ["ownership"]
        if eid in owners_with_text:
            channels.append("text")
        if "document" in etype:
            channels.append("layout")
        elif "product" in etype or "sign" in etype:
            channels.append("visual")
        elif "reflection" in etype:
            channels = ["ownership", "context"]

        for c in channels:
            if c not in all_channels:
                all_channels.append(c)

        candidates.append({
            "entity_id": eid,
            "channels": channels,
            "reason": CHANNEL_REASONS.get(etype, "entity_surface_detected"),
            "candidate_only": True,
        })

    return {
        "activation_id": _uid("peca"),
        "per_entity_channel_activation_candidates": candidates,
        "activated_channel_types": all_channels,
        "no_all_model_activation": True,
        "not_global_model_start": True,
        "candidate_only": True,
    }
