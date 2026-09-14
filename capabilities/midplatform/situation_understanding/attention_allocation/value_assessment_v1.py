# -*- coding: utf-8 -*-
"""Value Assessment — is this region worth understanding for current goal v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

GOAL_VALUE_RULES: Dict[str, Dict[str, str]] = {
    "find_subway_exit": {
        "direction_sign": "high",
        "direction_text": "high",
        "exit_sign": "high",
        "platform_edge": "medium",
        "advertisement": "low",
        "advertisement_screen": "low",
        "passengers": "medium",
        "shop_sign": "low",
    },
    "understand_environment": {
        "direction_sign": "medium",
        "shop_sign": "high",
        "passengers": "high",
        "advertisement": "medium",
        "exit_sign": "medium",
        "moving_object": "high",
        "walkable_path": "high",
    },
    "identify_place": {
        "shop_sign": "high",
        "direction_sign": "medium",
        "advertisement": "low",
    },
}


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def assess_region_value(
    *,
    l0_scan: Dict[str, Any],
    goal_type: str = "find_subway_exit",
) -> Dict[str, Any]:
    """
    Layer 2: same text region, different value by goal.
    开往嘉会湖 → high for navigate; 夏季优惠 → low for find_exit.
    """
    rules = GOAL_VALUE_RULES.get(goal_type, GOAL_VALUE_RULES["find_subway_exit"])
    assessments: List[Dict[str, Any]] = []

    for hint in l0_scan.get("attention_priority_candidates") or []:
        rtype = hint.get("region_type", "")
        task_value = rules.get(rtype, "low")
        scan_importance = hint.get("importance", "low")

        combined = task_value
        if task_value == "high" and scan_importance == "high":
            combined = "very_high"
        elif task_value == "low":
            combined = "low"

        assessments.append({
            "assessment_id": _uid("va"),
            "region_id": hint.get("region_id"),
            "region_type": rtype,
            "task_relevance": task_value,
            "scan_importance": scan_importance,
            "combined_value": combined,
            "worth_deep_understanding": combined in ("high", "very_high"),
            "not_see_text_then_ocr": True,
            "candidate_only": True,
        })

    return {
        "assessment_id": _uid("vas"),
        "goal_type": goal_type,
        "region_value_assessments": assessments,
        "candidate_only": True,
    }
