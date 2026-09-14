# -*- coding: utf-8 -*-
"""Slot Provider Binding — Collaboration Slot → Model Manager Fill v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from capabilities.midplatform.model_manager.registry.provider_registry_loader_v1 import (
    get_provider_by_id,
)

SHOPFRONT_CHAIN_SLOTS: List[Dict[str, Any]] = [
    {
        "slot_id": "slot_1",
        "capability": "text_detection",
        "role": "text_detector",
        "step": 1,
        "depends_on": [],
        "output_type": "text_region_candidate",
        "not_output": "shopfront_identification",
    },
    {
        "slot_id": "slot_2",
        "capability": "text_recognition",
        "role": "ocr",
        "step": 2,
        "depends_on": ["slot_1"],
        "output_type": "ocr_text_candidate",
        "not_output": "place_fact",
    },
    {
        "slot_id": "slot_3",
        "capability": "context_reasoning",
        "role": "vlm_context",
        "step": 3,
        "depends_on": ["slot_2"],
        "output_type": "context_evidence_candidate",
        "not_output": "ocr_substitute",
        "qwen_not_ocr": True,
    },
]

DEFAULT_PROVIDER_FILL: Dict[str, str] = {
    "slot_1": "detection_v1",
    "slot_2": "ocr_v1",
    "slot_3": "qwen_vl",
}


def get_shopfront_chain_slots() -> List[Dict[str, Any]]:
    return [dict(s) for s in SHOPFRONT_CHAIN_SLOTS]


def bind_slot_providers(
    slots: Optional[List[Dict[str, Any]]] = None,
    *,
    provider_overrides: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """Model Manager fills slots with providers — swap models without changing collaboration logic."""
    slots = slots or get_shopfront_chain_slots()
    overrides = provider_overrides or {}
    bound: List[Dict[str, Any]] = []

    for slot in slots:
        slot_id = slot.get("slot_id", "")
        model_id = overrides.get(slot_id) or DEFAULT_PROVIDER_FILL.get(slot_id, "")
        provider = get_provider_by_id(model_id) or {}
        bound.append({
            **slot,
            "filled_provider_id": model_id,
            "execution_mode": provider.get("execution_mode", "tool_os"),
            "provider_type": provider.get("provider_type", "tool"),
            "slot_filled": bool(model_id),
            "candidate_only": True,
        })
    return bound


def validate_slot_bindings(bound_slots: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Ensure three-slot chain is correctly filled."""
    fill_map = {s.get("slot_id"): s.get("filled_provider_id") for s in bound_slots}
    expected = DEFAULT_PROVIDER_FILL
    return {
        "all_slots_filled": all(fill_map.get(k) == v for k, v in expected.items()),
        "slot_1_is_detector": fill_map.get("slot_1") == "detection_v1",
        "slot_2_is_ocr": fill_map.get("slot_2") == "ocr_v1",
        "slot_3_is_qwen_context": fill_map.get("slot_3") == "qwen_vl",
        "qwen_not_in_ocr_slot": fill_map.get("slot_2") != "qwen_vl",
        "candidate_only": True,
    }
