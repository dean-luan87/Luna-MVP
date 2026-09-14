# -*- coding: utf-8 -*-
"""Information Channel Activation — route slots to capabilities v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

# Information slot → Luna capability (not model name)
SLOT_CAPABILITY_MAP: Dict[str, str] = {
    "text": "understand_region_text",
    "visual_symbol": "understand_region_visual",
    "style": "understand_region_visual",
    "direction_symbol": "understand_region_visual",
    "logo": "understand_region_visual",
    "layout": "understand_region_layout",
    "layout_relation": "understand_region_layout",
    "spatial": "understand_region_layout",
    "context": "understand_region_context",
    "scene_relation": "understand_region_context",
    "price_number": "understand_region_text",
    "qr_code": "understand_region_visual",
    "ownership": "understand_region_ownership",
}

# Capability → default provider (Model Manager binding)
CAPABILITY_PROVIDER_MAP: Dict[str, str] = {
    "understand_region_text": "paddleocr_recognizer_v1",
    "understand_region_visual": "vision_model_v1",
    "understand_region_layout": "spatial_analyzer_v1",
    "understand_region_context": "context_analyzer_v1",
    "understand_region_ownership": "region_owner_analyzer_v1",
}

CHANNEL_MAP: Dict[str, str] = {
    "understand_region_text": "text_channel",
    "understand_region_visual": "visual_channel",
    "understand_region_layout": "spatial_channel",
    "understand_region_context": "context_channel",
    "understand_region_ownership": "ownership_channel",
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def activate_information_channels(
    *,
    region_analysis: Dict[str, Any],
    region_id: str = "region_001",
) -> Dict[str, Any]:
    """
    Activate information channels based on required slots.
    Model Manager routes slots — not fixed OCR+VLM.
    """
    slots: List[str] = region_analysis.get("information_slots") or []
    activations: List[Dict[str, Any]] = []
    channels_activated: List[str] = []

    for slot in slots:
        capability = SLOT_CAPABILITY_MAP.get(slot, f"understand_region_{slot}")
        provider = CAPABILITY_PROVIDER_MAP.get(capability, "deferred_v1")
        channel = CHANNEL_MAP.get(capability, "unknown_channel")
        if channel not in channels_activated:
            channels_activated.append(channel)
        activations.append({
            "information_slot": slot,
            "capability": capability,
            "provider_id": provider,
            "channel": channel,
            "region_id": region_id,
            "not_model_driven": True,
        })

    return {
        "activation_id": _uid("ica"),
        "region_id": region_id,
        "region_type_candidate": region_analysis.get("region_type_candidate"),
        "information_slots": slots,
        "channel_activations": activations,
        "channels_activated": channels_activated,
        "not_fixed_ocr_plus_vlm": True,
        "candidate_only": True,
    }
