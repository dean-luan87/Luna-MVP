# -*- coding: utf-8 -*-
"""DryRun goal profiles — Goal + Situation → Attention (not image alone) v1."""

from __future__ import annotations

from typing import Any, Dict

DRYRUN_GOAL_PROFILES: Dict[str, Dict[str, Any]] = {
    "find_subway_exit": {
        "goal_label": "我要找出口",
        "value_rules": {
            "direction_sign": "very_high",
            "exit_sign": "very_high",
            "platform_edge": "medium",
            "advertisement_screen": "low",
            "advertisement": "low",
            "passengers": "medium",
            "shop_sign": "low",
            "menu": "low",
            "moving_object": "low",
            "vehicle": "low",
        },
        "budget_shares": {
            "direction_sign": 0.45,
            "exit_sign": 0.45,
            "passengers": 0.20,
            "advertisement_screen": 0.05,
            "advertisement": 0.05,
            "platform_edge": 0.10,
        },
        "priority_labels": {
            "direction_sign": "P0",
            "exit_sign": "P0",
            "passengers": "P2",
            "advertisement_screen": "P3",
            "advertisement": "P3",
        },
    },
    "find_coffee_shop": {
        "goal_label": "我要找一家咖啡店",
        "value_rules": {
            "shop_sign": "very_high",
            "menu": "high",
            "advertisement": "low",
            "exit_sign": "low",
            "passengers": "low",
            "direction_sign": "low",
        },
        "budget_shares": {
            "shop_sign": 0.90,
            "menu": 0.70,
            "passengers": 0.10,
            "advertisement": 0.05,
            "exit_sign": 0.05,
        },
        "priority_labels": {
            "shop_sign": "P0",
            "menu": "P1",
            "passengers": "P2",
            "advertisement": "P3",
        },
    },
    "assess_danger": {
        "goal_label": "了解环境是否危险",
        "value_rules": {
            "passengers": "very_high",
            "moving_object": "very_high",
            "vehicle": "high",
            "walkable_path": "high",
            "direction_sign": "low",
            "advertisement": "low",
            "shop_sign": "low",
        },
        "budget_shares": {
            "passengers": 0.80,
            "moving_object": 0.80,
            "vehicle": 0.60,
            "walkable_path": 0.50,
            "direction_sign": 0.20,
            "advertisement": 0.05,
        },
        "priority_labels": {
            "passengers": "P0",
            "moving_object": "P0",
            "vehicle": "P1",
            "direction_sign": "P2",
            "advertisement": "P3",
        },
    },
}

REGION_ENTITY_MAP: Dict[str, Dict[str, Any]] = {
    "reg_direction": {
        "entity_id": "direction_sign_001",
        "ownership_type": "navigation_sign",
        "region_type": "direction_sign",
        "channels": ["ownership", "text"],
        "capabilities": ["understand_region_ownership", "understand_region_text"],
        "information_value": 1.0,
    },
    "reg_ad": {
        "entity_id": "advertisement_001",
        "ownership_type": "advertisement",
        "region_type": "advertisement_screen",
        "channels": ["ownership", "text", "visual"],
        "capabilities": ["understand_region_ownership", "understand_region_text", "understand_region_visual"],
        "information_value": 0.1,
    },
    "reg_people": {
        "entity_id": "passengers_001",
        "ownership_type": "dynamic_object",
        "region_type": "passengers",
        "channels": ["ownership", "visual", "context"],
        "capabilities": ["understand_region_ownership", "understand_region_visual", "understand_region_context"],
        "information_value": 0.5,
    },
    "reg_edge": {
        "entity_id": "platform_edge_001",
        "ownership_type": "spatial_boundary",
        "region_type": "platform_edge",
        "channels": ["ownership", "spatial"],
        "capabilities": ["understand_region_ownership", "understand_region_layout"],
        "information_value": 0.6,
    },
    "reg_shop": {
        "entity_id": "shop_sign_001",
        "ownership_type": "business_sign",
        "region_type": "shop_sign",
        "channels": ["ownership", "text", "visual"],
        "capabilities": ["understand_region_ownership", "understand_region_text", "understand_region_visual"],
        "information_value": 0.9,
    },
    "reg_exit": {
        "entity_id": "exit_sign_001",
        "ownership_type": "navigation_sign",
        "region_type": "exit_sign",
        "channels": ["ownership", "text"],
        "capabilities": ["understand_region_ownership", "understand_region_text"],
        "information_value": 1.0,
    },
    "reg_dynamic": {
        "entity_id": "moving_object_001",
        "ownership_type": "dynamic_object",
        "region_type": "moving_object",
        "channels": ["ownership", "visual", "context"],
        "capabilities": ["understand_region_ownership", "understand_region_visual", "understand_region_context"],
        "information_value": 0.8,
    },
    "reg_path": {
        "entity_id": "walkable_path_001",
        "ownership_type": "spatial_path",
        "region_type": "walkable_path",
        "channels": ["ownership", "spatial"],
        "capabilities": ["understand_region_ownership", "understand_region_layout"],
        "information_value": 0.7,
    },
}
