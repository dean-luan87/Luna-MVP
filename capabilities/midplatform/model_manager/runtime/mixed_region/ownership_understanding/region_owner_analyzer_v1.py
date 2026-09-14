# -*- coding: utf-8 -*-
"""Region Owner Analyzer — discover information carriers, not text blobs v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

# Planning fixtures — object/surface segmentation stand-ins
OWNERSHIP_SCENES: Dict[str, Dict[str, Any]] = {
    "stacked_documents": {
        "scene_type": "desktop_documents",
        "object_candidates": [
            {"object_id": "paper_001", "type": "document", "position": "front", "bbox": [80, 60, 320, 280]},
            {"object_id": "paper_002", "type": "document", "position": "behind", "bbox": [140, 120, 380, 340]},
        ],
        "information_slots": ["ownership", "text", "layout"],
        "region_type_candidate": "multi_document_surface",
        "requires_ownership_first": True,
    },
    "glass_reflection": {
        "scene_type": "shopfront_glass",
        "object_candidates": [
            {"object_id": "sign_real", "type": "business_sign", "position": "physical", "bbox": [50, 80, 350, 200]},
            {"object_id": "sign_reflection", "type": "reflection", "position": "virtual", "bbox": [60, 210, 340, 320]},
        ],
        "information_slots": ["ownership", "text", "visual_symbol"],
        "region_type_candidate": "glass_reflection_surface",
        "requires_ownership_first": True,
    },
    "shelf_multi_entity": {
        "scene_type": "retail_shelf",
        "object_candidates": [
            {"object_id": "product_a", "type": "product_package", "position": "shelf", "bbox": [20, 100, 150, 280]},
            {"object_id": "price_tag", "type": "price_label", "position": "attached", "bbox": [30, 260, 120, 300]},
            {"object_id": "bg_ad", "type": "background_ad", "position": "behind", "bbox": [100, 50, 400, 180]},
        ],
        "information_slots": ["ownership", "text", "visual_symbol", "layout"],
        "region_type_candidate": "retail_shelf_region",
        "requires_ownership_first": True,
    },
    "device_screen": {
        "scene_type": "desk_with_phone",
        "object_candidates": [
            {"object_id": "phone_device", "type": "device", "position": "physical", "bbox": [200, 150, 320, 350]},
            {"object_id": "phone_screen", "type": "screen_content", "position": "display", "bbox": [210, 170, 310, 300]},
            {"object_id": "desk_label", "type": "environment_text", "position": "environment", "bbox": [50, 80, 180, 120]},
        ],
        "information_slots": ["ownership", "text", "context"],
        "region_type_candidate": "device_environment_region",
        "requires_ownership_first": True,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def analyze_region_owners(
    *,
    profile_key: str = "stacked_documents",
    upstream_region_id: str = "region_001",
) -> Dict[str, Any]:
    """
    Region Discovery + Ownership Analysis.
    Discover multiple information carriers before OCR — not a single text_region blob.
    """
    scene = OWNERSHIP_SCENES.get(profile_key, OWNERSHIP_SCENES["stacked_documents"])
    objects = scene.get("object_candidates") or []

    return {
        "analysis_id": _uid("roa"),
        "upstream_region_id": upstream_region_id,
        "region_discovery_complete": True,
        "scene_type": scene.get("scene_type"),
        "region_type_candidate": scene.get("region_type_candidate"),
        "object_candidates": objects,
        "object_count": len(objects),
        "information_slots": scene.get("information_slots", []),
        "requires_ownership_first": scene.get("requires_ownership_first", True),
        "not_full_image_ocr": True,
        "not_recognizer": True,
        "candidate_only": True,
    }
