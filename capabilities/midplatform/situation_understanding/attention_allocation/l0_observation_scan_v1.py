# -*- coding: utf-8 -*-
"""L0 Observation Scan — fast environment scan, no OCR/VLM v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

SCAN_FIXTURES: Dict[str, Dict[str, Any]] = {
    "subway_platform": {
        "scene_type": "subway_platform",
        "environment_type": "public_transport",
        "environment_summary": "transit platform with signage and passengers",
        "potential_regions": [
            {"region_type": "direction_sign", "importance": "high", "region_id": "reg_direction"},
            {"region_type": "platform_edge", "importance": "high", "region_id": "reg_edge"},
            {"region_type": "advertisement_screen", "importance": "low", "region_id": "reg_ad"},
            {"region_type": "passengers", "importance": "medium", "region_id": "reg_people"},
        ],
    },
    "shopping_mall": {
        "scene_type": "shopping_mall",
        "environment_type": "retail_consumption",
        "environment_summary": "indoor mall with shops and advertisements",
        "potential_regions": [
            {"region_type": "shop_sign", "importance": "medium", "region_id": "reg_shop"},
            {"region_type": "advertisement", "importance": "low", "region_id": "reg_ad"},
            {"region_type": "exit_sign", "importance": "high", "region_id": "reg_exit"},
            {"region_type": "passengers", "importance": "medium", "region_id": "reg_people"},
        ],
    },
    "street_scene": {
        "scene_type": "street_crossing",
        "environment_type": "street_mobility",
        "environment_summary": "outdoor street with dynamic objects",
        "potential_regions": [
            {"region_type": "moving_object", "importance": "high", "region_id": "reg_dynamic"},
            {"region_type": "walkable_path", "importance": "high", "region_id": "reg_path"},
            {"region_type": "advertisement", "importance": "low", "region_id": "reg_ad"},
        ],
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_l0_observation_scan(*, fixture_key: str = "subway_platform") -> Dict[str, Any]:
    """L0 fast scan — scene profile + attention priority hints, zero model cost."""
    fixture = SCAN_FIXTURES.get(fixture_key, SCAN_FIXTURES["subway_platform"])
    regions = fixture.get("potential_regions") or []

    return {
        "scan_id": _uid("scan"),
        "layer": "L0_observation_scan",
        "scene_profile_candidate": {
            "scene_type": fixture.get("scene_type"),
            "environment_type": fixture.get("environment_type"),
            "candidate_only": True,
        },
        "environment_summary_candidate": {
            "summary": fixture.get("environment_summary"),
            "candidate_only": True,
        },
        "attention_priority_candidates": [
            {
                "priority_id": _uid("ap"),
                "region_type": r.get("region_type"),
                "region_id": r.get("region_id"),
                "importance": r.get("importance"),
                "candidate_only": True,
            }
            for r in regions
        ],
        "no_ocr": True,
        "no_qwen": True,
        "no_heavy_models": True,
        "low_cost_scan": True,
        "candidate_only": True,
    }
