# -*- coding: utf-8 -*-
"""Mixed Region Analyzer — Region Intelligence: information slot activation v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

# Region profiles — what information slots a region type needs
REGION_PROFILES: Dict[str, Dict[str, Any]] = {
    "shopfront_mixed": {
        "region_type_candidate": "mixed_business_sign",
        "information_slots": ["text", "visual_symbol", "style"],
        "composition": ["text", "person_illustration", "food_icon", "decorative_font"],
    },
    "metro_mixed": {
        "region_type_candidate": "transit_direction_sign",
        "information_slots": ["text", "direction_symbol", "layout_relation"],
        "composition": ["text", "arrow", "line_color", "station_icon"],
    },
    "shopfront_occlusion": {
        "region_type_candidate": "mixed_business_sign",
        "information_slots": ["text", "visual_symbol", "style"],
        "text_damaged": True,
        "composition": ["partial_text", "person_illustration", "hotpot_icon"],
    },
    "logo_mixed": {
        "region_type_candidate": "brand_signage",
        "information_slots": ["text", "visual_symbol", "logo"],
        "composition": ["brand_text", "logo_shape", "product_image"],
    },
    "logo_only": {
        "region_type_candidate": "logo_dominant_sign",
        "information_slots": ["logo", "visual_symbol", "style"],
        "text_absent": True,
        "composition": ["logo_only", "brand_shape"],
    },
    "artistic_text": {
        "region_type_candidate": "artistic_business_sign",
        "information_slots": ["text", "visual_symbol", "style"],
        "artistic_font": True,
        "composition": ["artistic_text", "flame_shape", "dining_scene"],
    },
    "coffee_artistic_wrong": {
        "region_type_candidate": "commercial_sign",
        "information_slots": ["text", "visual_symbol", "context"],
        "artistic_font": True,
        "composition": ["distorted_text", "coffee_cup", "storefront"],
    },
    "billboard_multi": {
        "region_type_candidate": "multi_object_advertisement",
        "information_slots": ["logo", "text", "price_number", "visual_symbol", "qr_code", "layout"],
        "multi_object": True,
        "composition": ["brand_logo", "price_digits", "product_image", "qr_code"],
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def analyze_mixed_region(
    *,
    region_evidence: Dict[str, Any],
    profile_key: str = "shopfront_mixed",
) -> Dict[str, Any]:
    """
    Region Intelligence Analyzer — NOT a recognizer.
    Determines what observation modes (information slots) a region needs.
    """
    profile = REGION_PROFILES.get(profile_key, REGION_PROFILES["shopfront_mixed"])
    regions = region_evidence.get("regions") or []
    region_id = (regions[0].get("region_id") if regions else None) or "region_001"

    return {
        "analysis_id": _uid("mra"),
        "upstream_evidence_id": region_evidence.get("evidence_id"),
        "region_id": region_id,
        "region_type_candidate": profile.get("region_type_candidate"),
        "information_slots": profile.get("information_slots", []),
        "required_information": profile.get("information_slots", []),
        "region_count": len(regions),
        "composition": profile.get("composition", []),
        "text_damaged": profile.get("text_damaged", False),
        "text_absent": profile.get("text_absent", False),
        "artistic_font": profile.get("artistic_font", False),
        "multi_object": profile.get("multi_object", False),
        "not_recognizer": True,
        "not_text_or_image_binary": True,
        "candidate_only": True,
    }
