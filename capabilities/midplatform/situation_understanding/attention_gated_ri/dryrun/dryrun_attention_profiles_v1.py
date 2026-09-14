# -*- coding: utf-8 -*-
"""DryRun goal profiles — Goal + Situation → Attention (extended goals) v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

GOAL_VALUE_RULES: Dict[str, Dict[str, str]] = {
    "find_subway_exit": {
        "direction_sign": "high",
        "exit_sign": "high",
        "platform_edge": "medium",
        "advertisement_screen": "low",
        "advertisement": "low",
        "passengers": "medium",
        "shop_sign": "low",
    },
    "find_coffee_shop": {
        "shop_sign": "high",
        "menu": "high",
        "advertisement": "low",
        "exit_sign": "low",
        "passengers": "low",
    },
    "assess_danger": {
        "passengers": "high",
        "moving_object": "high",
        "vehicle": "high",
        "direction_sign": "low",
        "advertisement": "low",
        "walkable_path": "medium",
    },
    "understand_environment": {
        "passengers": "high",
        "shop_sign": "high",
        "direction_sign": "medium",
        "advertisement": "medium",
    },
}

GOAL_BUDGETS: Dict[str, Dict[str, float]] = {
    "find_subway_exit": {
        "direction_sign": 0.45,
        "exit_sign": 0.45,
        "advertisement_screen": 0.05,
        "advertisement": 0.05,
        "passengers": 0.20,
        "platform_edge": 0.10,
    },
    "find_coffee_shop": {
        "shop_sign": 0.90,
        "menu": 0.70,
        "passengers": 0.10,
        "advertisement": 0.05,
        "exit_sign": 0.05,
    },
    "assess_danger": {
        "passengers": 0.80,
        "moving_object": 0.60,
        "vehicle": 0.60,
        "direction_sign": 0.20,
        "advertisement": 0.05,
        "walkable_path": 0.30,
    },
}

PRIORITY_FROM_BUDGET = (
    (0.70, "P0"),
    (0.40, "P1"),
    (0.15, "P2"),
    (0.0, "P3"),
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _priority_label(budget: float) -> str:
    for threshold, label in PRIORITY_FROM_BUDGET:
        if budget >= threshold:
            return label
    return "P3"


def assess_region_value_for_goal(
    *,
    l0_scan: Dict[str, Any],
    goal_type: str,
) -> Dict[str, Any]:
    """Value assessment with dryrun-extended goals."""
    rules = GOAL_VALUE_RULES.get(goal_type, GOAL_VALUE_RULES["find_subway_exit"])
    assessments: List[Dict[str, Any]] = []

    for hint in l0_scan.get("attention_priority_candidates") or []:
        rtype = hint.get("region_type", "")
        task_value = rules.get(rtype, "low")
        worth_deep = task_value in ("high", "very_high")

        assessments.append({
            "assessment_id": _uid("va"),
            "region_id": hint.get("region_id"),
            "region_type": rtype,
            "task_relevance": task_value,
            "worth_deep_understanding": worth_deep,
            "candidate_only": True,
        })

    return {
        "assessment_id": _uid("vas"),
        "goal_type": goal_type,
        "region_value_assessments": assessments,
        "goal_driven_not_image_driven": True,
        "candidate_only": True,
    }


def allocate_budget_for_goal(
    *,
    value_assessment: Dict[str, Any],
    goal_type: str,
    budget_threshold: float = 0.10,
) -> Dict[str, Any]:
    """Budget allocation with dryrun-extended goals."""
    budgets = GOAL_BUDGETS.get(goal_type, GOAL_BUDGETS["find_subway_exit"])
    allocations: List[Dict[str, Any]] = []
    deep_regions: List[str] = []
    skipped_regions: List[str] = []

    for item in value_assessment.get("region_value_assessments") or []:
        rtype = item.get("region_type", "")
        budget = budgets.get(rtype, 0.0)
        trigger_deep = budget >= budget_threshold and item.get("worth_deep_understanding", False)

        entry = {
            "allocation_id": _uid("oba"),
            "region_id": item.get("region_id"),
            "region_type": rtype,
            "budget_share": budget,
            "priority": _priority_label(budget),
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
        "attention_is_control_not_label": True,
        "candidate_only": True,
    }
