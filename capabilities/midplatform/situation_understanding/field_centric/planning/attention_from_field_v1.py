# -*- coding: utf-8 -*-
"""Attention from Field + Goal — 非视觉显著性 v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

GOAL_FIELD_ATTENTION: Dict[str, Dict[str, float]] = {
    "find_exit": {
        "subway_platform": {"exit_direction": 0.90, "direction_text": 0.85, "advertisement": 0.05},
        "shopping_mall_public_area": {"exit_direction": 0.90, "floor_guide": 0.80, "promotion": 0.10},
        "restaurant_dining": {"exit_direction": 0.70, "menu": 0.20},
    },
    "understand_environment": {
        "shopping_mall_public_area": {"shop_sign": 0.70, "crowd": 0.50, "decorative_installation": 0.40},
        "street_intersection": {"traffic_signal": 0.80, "crowd": 0.60, "vehicle": 0.70},
    },
    "assess_safety": {
        "street_intersection": {"moving_vehicle": 0.95, "crowd_congestion": 0.85, "curb_edge": 0.80},
        "shopping_mall_public_area": {"glass_door": 0.80, "crowd": 0.75, "stairs": 0.70},
        "fire_safety_zone": {"fire_equipment": 0.95, "exit_sign": 0.90},
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def allocate_attention_from_field(
    *,
    field_understanding: Dict[str, Any],
    goal_type: str,
    field_key: str,
) -> Dict[str, Any]:
    """
    Attention 由 Field + Goal 共同决定，NOT 视觉显著性。
    """
    goal_map = GOAL_FIELD_ATTENTION.get(goal_type, {})
    budgets = goal_map.get(field_key, goal_map.get("shopping_mall_public_area", {}))
    risk_profile = field_understanding.get("risk_pattern_profile") or []
    info_profile = field_understanding.get("expected_information_profile") or []

    priorities: List[Dict[str, Any]] = []
    for info_type, share in budgets.items():
        priorities.append({
            "priority_id": _uid("fap"),
            "information_type": info_type,
            "budget_share": share,
            "source": "field_plus_goal",
            "not_visual_saliency": True,
            "candidate_only": True,
        })

    return {
        "allocation_id": _uid("afa"),
        "goal_type": goal_type,
        "field_candidate": field_understanding.get("field_candidate"),
        "attention_priorities": priorities,
        "risk_patterns_inherited": risk_profile,
        "information_profile_inherited": info_profile,
        "attention_from_field_and_goal": True,
        "not_saliency_driven": True,
        "candidate_only": True,
    }
