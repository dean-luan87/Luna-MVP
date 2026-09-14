# -*- coding: utf-8 -*-
"""slot_ownership_discovery — Entity / Surface Discovery v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.model_manager.runtime.mixed_region.ownership_understanding.region_owner_analyzer_v1 import (
    analyze_region_owners,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_slot_ownership_discovery(
    *,
    profile_key: str,
    attention_gate: Dict[str, Any],
    entity_id_map: Dict[str, str] | None = None,
    blocked_entity_ids: List[str] | None = None,
    upstream_region_id: str = "reg_gated",
) -> Dict[str, Any]:
    """
    slot_ownership_discovery — discover information carriers in attention-allowed region.
    NOT: full-image entity discovery.
    """
    allowed = attention_gate.get("allowed_region_ids") or []
    if not allowed:
        return {
            "slot_id": "slot_ownership_discovery",
            "discovery_status": "blocked_no_allowed_regions",
            "entity_candidates": [],
            "candidate_only": True,
        }

    analysis = analyze_region_owners(profile_key=profile_key, upstream_region_id=upstream_region_id)
    blocked = set(blocked_entity_ids or [])
    mapping = entity_id_map or {}

    entities: List[Dict[str, Any]] = []
    for obj in analysis.get("object_candidates") or []:
        raw_id = obj.get("object_id", "")
        if raw_id in blocked:
            continue
        entity_id = mapping.get(raw_id, raw_id)
        entities.append({
            "entity_id": entity_id,
            "entity_type_candidate": obj.get("type", "unknown"),
            "attention_gate": "allowed",
            "ownership_candidate": {
                "owner_type": f"{obj.get('type', 'unknown')}_surface",
                "raw_object_id": raw_id,
            },
            "bbox": obj.get("bbox"),
            "candidate_only": True,
            "not_fact": True,
        })

    return {
        "slot_id": "slot_ownership_discovery",
        "discovery_status": "ok",
        "upstream_region_id": upstream_region_id,
        "attention_gated": True,
        "allowed_region_ids": allowed,
        "entity_candidates": entities,
        "entity_count": len(entities),
        "carrier_before_ocr": True,
        "not_full_image_discovery": True,
        "candidate_only": True,
    }
