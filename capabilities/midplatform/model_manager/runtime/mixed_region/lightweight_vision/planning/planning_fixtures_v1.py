# -*- coding: utf-8 -*-
"""Lightweight Vision Planning — deterministic fixtures v1."""

from __future__ import annotations

from typing import Any, Dict

PLANNING_FIXTURES: Dict[str, Dict[str, Any]] = {
    "stacked_papers": {
        "scene_type": "stacked_documents",
        "attention_gate": {"allowed_region_ids": ["reg_documents"], "blocked_regions": []},
        "source_region_id": "region_001",
    },
    "shelf_price_tags": {
        "scene_type": "retail_shelf",
        "attention_gate": {"allowed_region_ids": ["reg_shelf"], "blocked_regions": []},
        "source_region_id": "region_002",
    },
    "device_screen": {
        "scene_type": "device_screen",
        "attention_gate": {"allowed_region_ids": ["reg_device"], "blocked_regions": []},
        "source_region_id": "region_003",
    },
    "glass_reflection": {
        "scene_type": "glass_reflection",
        "attention_gate": {"allowed_region_ids": ["reg_sign"], "blocked_regions": []},
        "source_region_id": "region_004",
    },
    "attention_blocked": {
        "scene_type": "retail_shelf",
        "attention_gate": {
            "allowed_region_ids": ["reg_shelf"],
            "blocked_regions": [{"region_id": "reg_ad", "blocked_entity_ids": ["bg_ad"]}],
        },
        "blocked_runtimes_for": ["reg_ad"],
        "source_region_id": "region_005",
    },
    "runtime_unavailable": {
        "scene_type": "stacked_documents",
        "attention_gate": {"allowed_region_ids": ["reg_documents"], "blocked_regions": []},
        "runtime_unavailable": True,
        "source_region_id": "region_006",
    },
    "document_layout": {
        "scene_type": "document_layout",
        "attention_gate": {"allowed_region_ids": ["reg_doc"], "blocked_regions": []},
        "source_region_id": "region_007",
    },
    "model_conflict": {
        "scene_type": "document_layout",
        "attention_gate": {"allowed_region_ids": ["reg_doc"], "blocked_regions": []},
        "source_region_id": "region_008",
        "runtime_conflict": True,
    },
}


def get_fixture(key: str) -> Dict[str, Any]:
    return PLANNING_FIXTURES.get(key, PLANNING_FIXTURES["stacked_papers"])
