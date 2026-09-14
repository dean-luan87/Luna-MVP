# -*- coding: utf-8 -*-
"""Attention Allocation Adapter — L0 → Value → Budget → Region Intel gate v1."""

from __future__ import annotations

from typing import Any, Dict, Optional
from uuid import uuid4

from capabilities.midplatform.situation_understanding.attention_allocation.l0_observation_scan_v1 import (
    run_l0_observation_scan,
)
from capabilities.midplatform.situation_understanding.attention_allocation.observation_budget_manager_v1 import (
    allocate_observation_budget,
)
from capabilities.midplatform.situation_understanding.attention_allocation.value_assessment_v1 import (
    assess_region_value,
)

FINAL_GO = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_ALLOCATION_PLANNING_GO"
FINAL_BLOCKED = "P1_MIDPLATFORM_LUNA_SITUATION_UNDERSTANDING_ATTENTION_ALLOCATION_PLANNING_BLOCKED"


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def run_attention_allocation(
    *,
    scan_fixture: str = "subway_platform",
    goal_type: str = "find_subway_exit",
    user_goal: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Full Attention Allocation pipeline — gates Region Intelligence.
    NOT: image → all models → fusion
    """
    l0_scan = run_l0_observation_scan(fixture_key=scan_fixture)
    value_assessment = assess_region_value(l0_scan=l0_scan, goal_type=goal_type)
    budget = allocate_observation_budget(value_assessment=value_assessment, goal_type=goal_type)

    return {
        "pipeline_id": _uid("att"),
        "layer": "attention_allocation",
        "user_goal": user_goal or {"goal_type": goal_type},
        "l0_observation_scan": l0_scan,
        "value_assessment": value_assessment,
        "observation_budget": budget,
        "region_intelligence_triggered_for": budget.get("deep_understanding_regions") or [],
        "region_intelligence_skipped_for": budget.get("skipped_regions") or [],
        "attention_before_region_intelligence": True,
        "not_see_then_ocr": True,
        "not_all_models_start": budget.get("not_all_regions_sam", False),
        "candidate_only": True,
        "not_fact": True,
    }
