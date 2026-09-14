# -*- coding: utf-8 -*-
"""Visual Evidence Builder — Visual Channel: shapes, logos, icons v1."""

from __future__ import annotations

from typing import Any, Dict
from uuid import uuid4

VISUAL_FIXTURES: Dict[str, Dict[str, Any]] = {
    "shopfront_occlusion": {
        "features": ["person illustration", "food icon", "restaurant style"],
        "confidence": 0.9,
        "scene_hint": "dining_signage",
    },
    "metro_direction": {
        "features": ["direction arrow", "line color green", "station icon"],
        "confidence": 0.85,
        "scene_hint": "subway_signage",
    },
    "starbucks_consistent": {
        "features": ["green circular logo", "coffee cup image"],
        "confidence": 0.88,
        "scene_hint": "coffee_brand",
        "consistent_with_text": True,
    },
    "starbucks_conflict": {
        "features": ["auto repair shop facade", "wrench icon"],
        "confidence": 0.82,
        "scene_hint": "auto_repair",
        "consistent_with_text": False,
    },
    "hotpot_artistic": {
        "features": ["red flame pattern", "dining scene", "pot elements"],
        "confidence": 0.75,
        "scene_hint": "hotpot_restaurant",
        "supplements_ocr_gap": True,
    },
    "logo_only": {
        "features": ["brand logo shape", "distinctive color palette"],
        "confidence": 0.92,
        "scene_hint": "brand_identity",
        "text_absent": True,
    },
    "coffee_storefront": {
        "features": ["coffee cup image", "storefront environment", "cafe signage style"],
        "confidence": 0.86,
        "scene_hint": "coffee_shop",
        "ocr_unreliable_not_conflict": True,
    },
    "billboard_multi": {
        "features": ["brand logo", "product image", "qr code pattern"],
        "confidence": 0.88,
        "scene_hint": "retail_ad",
    },
}

VISUAL_SLOTS = frozenset({"visual_symbol", "style", "direction_symbol", "logo", "qr_code"})


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _visual_slot_required(region_analysis: Dict[str, Any]) -> bool:
    slots = region_analysis.get("information_slots") or []
    return any(s in VISUAL_SLOTS for s in slots)


def build_visual_evidence(
    *,
    fixture_key: str = "shopfront_occlusion",
    region_analysis: Dict[str, Any],
) -> Dict[str, Any]:
    """Build Visual Channel evidence — not VLM answer."""
    if not _visual_slot_required(region_analysis):
        return {
            "evidence_id": _uid("vev"),
            "type": "visual_candidate",
            "features": [],
            "status": "slot_not_required",
            "candidate_only": True,
            "not_fact": True,
        }

    fixture = VISUAL_FIXTURES.get(fixture_key, VISUAL_FIXTURES["shopfront_occlusion"])
    return {
        "evidence_id": _uid("vev"),
        "type": "visual_candidate",
        "features": fixture.get("features", []),
        "confidence": fixture.get("confidence", 0.0),
        "scene_hint": fixture.get("scene_hint"),
        "consistent_with_text": fixture.get("consistent_with_text"),
        "supplements_ocr_gap": fixture.get("supplements_ocr_gap", False),
        "text_absent_region": fixture.get("text_absent", False),
        "not_vlm_hallucination_answer": True,
        "not_invented_text": True,
        "source": "understand_region_visual",
        "candidate_only": True,
        "not_fact": True,
    }
