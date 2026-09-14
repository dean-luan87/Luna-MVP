# -*- coding: utf-8 -*-
"""Information Channel Selection — selective activation, not all models v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

ALL_CAPABILITIES = (
    "understand_region_ownership",
    "understand_region_text",
    "understand_region_visual",
    "understand_region_layout",
    "understand_region_context",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def select_information_channels(
    *,
    discovery: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Decide which capabilities are worth calling per entity.
    NOT: image → all models start → fusion
    """
    if discovery.get("runtime_unavailable"):
        return {
            "selection_id": _uid("ics"),
            "selection_status": "blocked_runtime_unavailable",
            "activated_capabilities": [],
            "candidate_only": True,
        }

    channels_map = discovery.get("channels_per_entity") or {}
    allowed = discovery.get("allowed_capabilities")
    per_entity: Dict[str, List[str]] = {}
    activated_caps: List[str] = []
    noop_caps: List[str] = []

    for eid, slots in channels_map.items():
        per_entity[eid] = slots
        for slot in slots:
            cap = {
                "ownership": "understand_region_ownership",
                "text": "understand_region_text",
                "visual": "understand_region_visual",
                "spatial": "understand_region_layout",
                "context": "understand_region_context",
            }.get(slot, f"understand_region_{slot}")
            if allowed and cap not in allowed:
                continue
            if cap not in activated_caps:
                activated_caps.append(cap)

    for cap in ALL_CAPABILITIES:
        if cap not in activated_caps:
            noop_caps.append(cap)

    global_ocr = "understand_region_text" in activated_caps and not discovery.get("global_ocr_forbidden", True)
    if discovery.get("global_ocr_forbidden") and len(per_entity) > 1:
        global_ocr = False

    return {
        "selection_id": _uid("ics"),
        "selection_status": "selective_activation",
        "per_entity_selection": per_entity,
        "activated_capabilities": activated_caps,
        "noop_capabilities": noop_caps,
        "not_all_models_started": len(noop_caps) > 0,
        "ocr_per_entity_only": discovery.get("global_ocr_forbidden", True),
        "not_global_ocr": not global_ocr,
        "ownership_before_ocr": "understand_region_ownership" in activated_caps,
        "candidate_only": True,
    }
