# -*- coding: utf-8 -*-
"""Ownership Real Runtime Planning — attention-gated fixtures v1."""

from __future__ import annotations

from typing import Any, Dict, List

PLANNING_FIXTURES: Dict[str, Dict[str, Any]] = {
    "stacked_papers": {
        "scene_label": "叠放纸张",
        "profile_key": "stacked_documents",
        "entity_id_map": {"paper_001": "paper_A", "paper_002": "paper_B"},
        "attention_gate": {
            "allowed_region_ids": ["reg_documents"],
            "blocked_regions": [],
        },
        "expected_entity_count": 2,
    },
    "shelf_price_tags": {
        "scene_label": "货架价签",
        "profile_key": "shelf_multi_entity",
        "entity_id_map": {
            "product_a": "product_a",
            "price_tag": "price_tag",
            "bg_ad": "bg_ad",
        },
        "attention_gate": {
            "allowed_region_ids": ["reg_shelf"],
            "blocked_regions": [],
        },
        "expected_entity_count": 3,
        "distinct_owners_required": True,
    },
    "glass_reflection": {
        "scene_label": "玻璃反光",
        "profile_key": "glass_reflection",
        "entity_id_map": {
            "sign_real": "sign_real",
            "sign_reflection": "sign_reflection",
        },
        "attention_gate": {
            "allowed_region_ids": ["reg_sign"],
            "blocked_regions": [],
        },
        "reflection_relation_required": True,
    },
    "attention_blocked_ad": {
        "scene_label": "Attention Blocked 广告",
        "profile_key": "shelf_multi_entity",
        "entity_id_map": {
            "product_a": "product_a",
            "price_tag": "price_tag",
            "bg_ad": "bg_ad",
        },
        "attention_gate": {
            "allowed_region_ids": ["reg_shelf"],
            "blocked_regions": [
                {
                    "region_id": "reg_ad",
                    "region_type": "advertisement",
                    "skip_reason": "low_task_value",
                    "blocked_entity_ids": ["bg_ad"],
                }
            ],
        },
        "blocked_entity_ids": ["bg_ad"],
    },
    "occluded_title": {
        "scene_label": "遮挡标题缺失",
        "profile_key": "stacked_documents",
        "entity_id_map": {"paper_001": "paper_A", "paper_002": "paper_B"},
        "attention_gate": {
            "allowed_region_ids": ["reg_documents"],
            "blocked_regions": [],
        },
        "missing_information": [
            {
                "owner_entity_id": "paper_B",
                "field": "title",
                "reason": "occluded",
                "not_assume_absent": True,
            }
        ],
    },
    "runtime_unavailable": {
        "scene_label": "Runtime 故障",
        "profile_key": "stacked_documents",
        "attention_gate": {
            "allowed_region_ids": ["reg_documents"],
            "blocked_regions": [],
        },
        "runtime_unavailable": True,
    },
}


def get_fixture(fixture_key: str) -> Dict[str, Any]:
    return PLANNING_FIXTURES.get(fixture_key, PLANNING_FIXTURES["stacked_papers"])


def blocked_entity_ids(fixture: Dict[str, Any]) -> List[str]:
    blocked: List[str] = list(fixture.get("blocked_entity_ids") or [])
    for br in (fixture.get("attention_gate") or {}).get("blocked_regions") or []:
        blocked.extend(br.get("blocked_entity_ids") or [])
    return list(dict.fromkeys(blocked))
