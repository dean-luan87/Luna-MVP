# -*- coding: utf-8 -*-
"""Observation Budget Manager — attention budget allocation v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

GOAL_BUDGETS: Dict[str, Dict[str, float]] = {
    "find_subway_exit": {
        "direction_sign": 0.40,
        "direction_text": 0.40,
        "exit_sign": 0.15,
        "advertisement": 0.05,
        "advertisement_screen": 0.05,
        "passengers": 0.0,
        "platform_edge": 0.0,
    },
    "understand_environment": {
        "passengers": 0.30,
        "shop_sign": 0.30,
        "direction_sign": 0.30,
        "advertisement": 0.10,
        "other": 0.0,
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def allocate_observation_budget(
    *,
    value_assessment: Dict[str, Any],
    goal_type: str = "find_subway_exit",
    budget_threshold: float = 0.10,
) -> Dict[str, Any]:
    """
    Layer 3: allocate finite attention/compute budget per region type.
    Regions below threshold → no Region Intelligence trigger.
    """
    budgets = GOAL_BUDGETS.get(goal_type, GOAL_BUDGETS["find_subway_exit"])
    allocations: List[Dict[str, Any]] = []
    deep_regions: List[str] = []
    skipped_regions: List[str] = []

    for item in value_assessment.get("region_value_assessments") or []:
        rtype = item.get("region_type", "")
        budget = budgets.get(rtype, budgets.get("other", 0.0))
        trigger_deep = budget >= budget_threshold and item.get("worth_deep_understanding", False)

        entry = {
            "allocation_id": _uid("oba"),
            "region_id": item.get("region_id"),
            "region_type": rtype,
            "budget_share": budget,
            "trigger_region_intelligence": trigger_deep,
            "candidate_only": True,
        }
        allocations.append(entry)
        if trigger_deep:
            deep_regions.append(item.get("region_id", ""))
        else:
            skipped_regions.append(item.get("region_id", ""))

    return {
        "budget_id": _uid("obm"),
        "goal_type": goal_type,
        "budget_allocations": allocations,
        "deep_understanding_regions": deep_regions,
        "skipped_regions": skipped_regions,
        "not_all_regions_sam": len(skipped_regions) > 0,
        "selective_deep_understanding": True,
        "candidate_only": True,
    }
