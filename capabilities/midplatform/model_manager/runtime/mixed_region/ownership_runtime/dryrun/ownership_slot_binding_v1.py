# -*- coding: utf-8 -*-
"""Ownership Slot Binding — Attention-Gated Region → slot sequence v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def bind_ownership_slots(
    *,
    attention_gate: Dict[str, Any],
    source_region_id: str = "region_001",
) -> Dict[str, Any]:
    """
    Bind Attention-Gated region to ordered Ownership Runtime slots.
    Blocked regions MUST NOT enter any slot.
    """
    allowed = attention_gate.get("allowed_region_ids") or []
    blocked = attention_gate.get("blocked_regions") or []

    if not allowed:
        return {
            "binding_id": _uid("osb"),
            "binding_status": "blocked_attention_gate",
            "attention_gate_status": "blocked",
            "source_region_id": source_region_id,
            "slot_sequence": [],
            "blocked_regions": blocked,
            "attention_gate_required": True,
            "candidate_only": True,
        }

    slot_sequence: List[str] = [
        "slot_ownership_discovery",
        "slot_occlusion_reasoning",
        "slot_text_owner_assignment",
    ]

    return {
        "binding_id": _uid("osb"),
        "binding_status": "bound",
        "attention_gate_status": "allowed",
        "source_region_id": source_region_id,
        "allowed_region_ids": allowed,
        "blocked_regions": blocked,
        "slot_sequence": slot_sequence,
        "slots_in_order": True,
        "attention_gate_required": True,
        "blocked_entities_excluded": len(blocked) > 0,
        "candidate_only": True,
    }
