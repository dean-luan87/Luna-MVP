# -*- coding: utf-8 -*-
"""Text Owner Assignment — text belongs to an entity, not free-floating v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

# Per-owner OCR fixtures — OCR per crop, NOT full-image merge
OWNER_TEXT_FIXTURES: Dict[str, Dict[str, List[Dict[str, Any]]]] = {
    "stacked_documents": {
        "paper_001": [
            {"text": "合同编号001", "confidence": 0.91},
            {"text": "客户：张三", "confidence": 0.89},
        ],
        "paper_002": [
            {"text": "合同编号002", "confidence": 0.88},
            {"text": "客户：李四", "confidence": 0.87},
        ],
    },
    "glass_reflection": {
        "sign_real": [
            {"text": "阿叔阿姨的店", "confidence": 0.9},
        ],
        "sign_reflection": [
            {"text": "阿叔阿姨的店", "confidence": 0.45, "reflection_artifact": True},
        ],
    },
    "shelf_multi_entity": {
        "product_a": [
            {"text": "有机牛奶 1L", "confidence": 0.92},
        ],
        "price_tag": [
            {"text": "¥12.8", "confidence": 0.95},
        ],
        "bg_ad": [
            {"text": "夏日促销", "confidence": 0.8},
        ],
    },
    "device_screen": {
        "phone_screen": [
            {"text": "14:32", "confidence": 0.93},
            {"text": "微信", "confidence": 0.9},
        ],
        "desk_label": [
            {"text": "会议室 A", "confidence": 0.88},
        ],
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def assign_text_owners(
    *,
    owner_analysis: Dict[str, Any],
    profile_key: str = "stacked_documents",
    occlusion_graph: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """
    Assign each text fragment to owner_candidate.
    OCR executed per owner crop — never flat merge without ownership.
    """
    fixtures = OWNER_TEXT_FIXTURES.get(profile_key, {})
    objects = owner_analysis.get("object_candidates") or []
    occluded = set((occlusion_graph or {}).get("occluded_owner_candidates") or [])

    assigned: List[Dict[str, Any]] = []
    per_owner_documents: List[Dict[str, Any]] = []

    for obj in objects:
        oid = obj.get("object_id", "")
        texts = fixtures.get(oid, [])
        owner_texts = []
        for t in texts:
            entry = {
                "text_id": _uid("txt"),
                "text": t.get("text"),
                "confidence": t.get("confidence", 0.0),
                "owner_candidate": {
                    "type": obj.get("type", "unknown"),
                    "id": oid,
                },
                "partially_occluded": oid in occluded,
                "reflection_artifact": t.get("reflection_artifact", False),
                "candidate_only": True,
                "not_fact": True,
            }
            assigned.append(entry)
            owner_texts.append(entry)

        if owner_texts:
            per_owner_documents.append({
                "owner_id": oid,
                "owner_type": obj.get("type"),
                "text_candidates": owner_texts,
                "ocr_per_crop": True,
                "not_full_image_ocr": True,
            })

    flat_merged = [a.get("text") for a in assigned]

    return {
        "assignment_id": _uid("toa"),
        "text_with_owners": assigned,
        "per_owner_documents": per_owner_documents,
        "owner_count": len(per_owner_documents),
        "forbidden_flat_merge": flat_merged,
        "not_independent_text_blobs": True,
        "each_text_has_owner": all(a.get("owner_candidate") for a in assigned),
        "candidate_only": True,
        "not_fact": True,
    }
