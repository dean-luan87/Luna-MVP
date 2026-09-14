# -*- coding: utf-8 -*-
"""Occlusion Graph — front/behind relations between information carriers v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

OCCLUSION_FIXTURES: Dict[str, List[Dict[str, str]]] = {
    "stacked_documents": [
        {"front": "paper_001", "behind": "paper_002", "occlusion_type": "partial_overlap"},
    ],
    "glass_reflection": [
        {"front": "sign_real", "behind": "sign_reflection", "occlusion_type": "reflection_not_occlusion"},
    ],
    "shelf_multi_entity": [
        {"front": "product_a", "behind": "bg_ad", "occlusion_type": "spatial_layer"},
        {"front": "price_tag", "behind": "bg_ad", "occlusion_type": "attached_to_product"},
    ],
    "device_screen": [
        {"front": "phone_screen", "behind": "phone_device", "occlusion_type": "content_on_device"},
    ],
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_occlusion_graph(
    *,
    owner_analysis: Dict[str, Any],
    profile_key: str = "stacked_documents",
) -> Dict[str, Any]:
    """
    Occlusion Graph — which carrier is in front, what may be hidden.
    If paper_B title missing → may be occluded, not absent.
    """
    relations = OCCLUSION_FIXTURES.get(profile_key, [])
    occluded_objects = [r.get("behind") for r in relations]

    return {
        "graph_id": _uid("ocg"),
        "occlusion_relation": relations,
        "occluded_owner_candidates": occluded_objects,
        "partial_visibility_acknowledged": len(relations) > 0,
        "not_assume_missing_title_absent": True,
        "candidate_only": True,
    }
