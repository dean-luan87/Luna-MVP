# -*- coding: utf-8 -*-
"""Gated Region Intelligence — only attention-allowed regions activate channels v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.dryrun_goal_profiles_v1 import (
    REGION_ENTITY_MAP,
)

CAPABILITY_COST = {
    "understand_region_ownership": 1,
    "understand_region_text": 3,
    "understand_region_visual": 4,
    "understand_region_layout": 2,
    "understand_region_context": 2,
    "text_recognition": 3,
    "visual_reasoning": 4,
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_gated_region_intelligence(*, gate: Dict[str, Any]) -> Dict[str, Any]:
    """
    Region Intelligence only for attention-allowed regions.
    Blocked regions produce NO channel activation records.
    """
    entity_candidates: List[Dict[str, Any]] = []
    activated_capabilities: List[str] = []
    compute_cost = 0
    information_value = 0.0

    for allowed in gate.get("allowed_regions") or []:
        rid = allowed.get("region_id", "")
        entity_meta = REGION_ENTITY_MAP.get(rid, {})
        caps = allowed.get("allowed_capabilities") or []
        channels: Dict[str, Any] = {}

        for slot in entity_meta.get("channels") or []:
            channels[slot] = {"activated": True, "candidate_only": True}

        for cap in caps:
            if cap not in activated_capabilities:
                activated_capabilities.append(cap)
            compute_cost += CAPABILITY_COST.get(cap, 1)

        information_value += entity_meta.get("information_value", 0.5)

        entity_candidates.append({
            "entity_id": entity_meta.get("entity_id", rid),
            "ownership_type": entity_meta.get("ownership_type"),
            "region_id": rid,
            "region_type": allowed.get("region_type"),
            "information_channels": channels,
            "activated_capabilities": caps,
            "attention_gated": True,
            "candidate_only": True,
        })

    blocked_count = len(gate.get("blocked_regions") or [])
    all_region_count = len(gate.get("allowed_regions") or []) + blocked_count

    return {
        "ri_id": _uid("gri"),
        "entity_candidates": entity_candidates,
        "activated_capabilities": activated_capabilities,
        "blocked_region_count": blocked_count,
        "activated_region_count": len(entity_candidates),
        "total_region_count": all_region_count,
        "compute_cost": compute_cost,
        "information_value": information_value,
        "not_all_models_started": blocked_count > 0,
        "attention_controlled_activation": True,
        "candidate_only": True,
    }
