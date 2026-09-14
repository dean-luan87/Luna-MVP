# -*- coding: utf-8 -*-
"""Entity Discovery Simulator — deterministic ownership-first fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

DRYRUN_SCENES: Dict[str, Dict[str, Any]] = {
    "stacked_menus": {
        "scene_type": "desk_surface",
        "entities": [
            {"entity_id": "menu_A", "ownership_type": "document", "position": "front"},
            {"entity_id": "menu_B", "ownership_type": "document", "position": "behind"},
        ],
        "relations": [
            {"entity_a": "menu_A", "entity_b": "menu_B", "relation": "occlusion", "direction": "front_over_behind"},
        ],
        "channels_per_entity": {
            "menu_A": ["ownership", "text"],
            "menu_B": ["ownership", "text", "spatial"],
        },
        "ocr_per_entity": {
            "menu_A": [{"text": "今日特价：牛肉面", "confidence": 0.9}],
            "menu_B": [{"text": "今日特价：酸辣粉", "confidence": 0.85}],
        },
        "global_ocr_forbidden": True,
    },
    "stacked_papers_occlusion": {
        "scene_type": "desk_documents",
        "entities": [
            {"entity_id": "paper_A", "ownership_type": "document", "position": "front"},
            {"entity_id": "paper_B", "ownership_type": "document", "position": "behind"},
        ],
        "relations": [
            {"entity_a": "paper_A", "entity_b": "paper_B", "relation": "occlusion", "direction": "partial_overlap"},
        ],
        "channels_per_entity": {
            "paper_A": ["ownership", "text"],
            "paper_B": ["ownership", "text", "spatial"],
        },
        "ocr_per_entity": {
            "paper_A": [
                {"text": "合同编号001", "confidence": 0.91},
                {"text": "客户：张三", "confidence": 0.89},
            ],
            "paper_B": [
                {"text": "合同编号002", "confidence": 0.88},
                {"text": "客户：李四", "confidence": 0.87},
            ],
        },
        "missing_information": [
            {
                "type": "text",
                "owner": "paper_B",
                "field": "title",
                "reason": "occluded",
                "confidence_source": "spatial_relation",
            }
        ],
        "global_ocr_forbidden": True,
    },
    "same_region_conflict": {
        "scene_type": "storefront_sign",
        "entities": [
            {"entity_id": "sign_region_001", "ownership_type": "business_sign", "position": "single"},
        ],
        "relations": [],
        "channels_per_entity": {
            "sign_region_001": ["ownership", "text", "visual"],
        },
        "ocr_per_entity": {
            "sign_region_001": [{"text": "STARBUCKS", "confidence": 0.92}],
        },
        "visual_per_entity": {
            "sign_region_001": {
                "features": ["auto repair shop logo", "wrench icon"],
                "scene_hint": "auto_repair",
                "consistent_with_text": False,
            },
        },
        "semantic_conflict": True,
        "global_ocr_forbidden": False,
    },
    "selective_channels_shelf": {
        "scene_type": "retail_shelf",
        "entities": [
            {"entity_id": "product_a", "ownership_type": "product_package", "position": "shelf"},
            {"entity_id": "price_tag", "ownership_type": "price_label", "position": "attached"},
        ],
        "relations": [
            {"entity_a": "price_tag", "entity_b": "product_a", "relation": "attached_to"},
        ],
        "channels_per_entity": {
            "product_a": ["ownership", "text", "visual"],
            "price_tag": ["ownership", "text"],
        },
        "ocr_per_entity": {
            "product_a": [{"text": "有机牛奶 1L", "confidence": 0.92}],
            "price_tag": [{"text": "¥12.8", "confidence": 0.95}],
        },
        "all_models_must_not_start": True,
        "allowed_capabilities": ["understand_region_ownership", "understand_region_text"],
    },
    "runtime_unavailable": {
        "scene_type": "desk_documents",
        "runtime_unavailable": True,
        "entities": [],
        "relations": [],
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def simulate_entity_discovery(*, fixture_key: str = "stacked_menus") -> Dict[str, Any]:
    """Discover information units in scene — before any OCR activation."""
    fixture = DRYRUN_SCENES.get(fixture_key, DRYRUN_SCENES["stacked_menus"])
    if fixture.get("runtime_unavailable"):
        return {
            "discovery_id": _uid("disc"),
            "discovery_status": "runtime_unavailable",
            "runtime_unavailable": True,
            "entity_candidates": [],
            "relation_candidates": [],
            "candidate_only": True,
        }

    entities = fixture.get("entities") or []
    return {
        "discovery_id": _uid("disc"),
        "discovery_status": "ok",
        "scene_type": fixture.get("scene_type"),
        "entity_count": len(entities),
        "raw_entities": entities,
        "relations_raw": fixture.get("relations") or [],
        "channels_per_entity": fixture.get("channels_per_entity") or {},
        "ocr_per_entity": fixture.get("ocr_per_entity") or {},
        "visual_per_entity": fixture.get("visual_per_entity") or {},
        "missing_information": fixture.get("missing_information") or [],
        "semantic_conflict": fixture.get("semantic_conflict", False),
        "global_ocr_forbidden": fixture.get("global_ocr_forbidden", True),
        "all_models_must_not_start": fixture.get("all_models_must_not_start", False),
        "allowed_capabilities": fixture.get("allowed_capabilities"),
        "ownership_first": True,
        "not_global_ocr": True,
        "candidate_only": True,
    }
