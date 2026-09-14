# -*- coding: utf-8 -*-
"""Attention Gate — controls Region Intelligence / model activation v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.dryrun_goal_profiles_v1 import (
    DRYRUN_GOAL_PROFILES,
    REGION_ENTITY_MAP,
)

BUDGET_THRESHOLD = 0.10
ALL_CAPABILITIES = (
    "text_recognition",
    "visual_reasoning",
    "understand_region_ownership",
    "understand_region_text",
    "understand_region_visual",
    "understand_region_layout",
    "understand_region_context",
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _assess_for_goal(*, l0_scan: Dict[str, Any], goal_type: str) -> Dict[str, Any]:
    profile = DRYRUN_GOAL_PROFILES.get(goal_type, DRYRUN_GOAL_PROFILES["find_subway_exit"])
    rules = profile.get("value_rules") or {}
    budgets = profile.get("budget_shares") or {}
    assessments: List[Dict[str, Any]] = []

    for hint in l0_scan.get("attention_priority_candidates") or []:
        rtype = hint.get("region_type", "")
        task_value = rules.get(rtype, "low")
        budget = budgets.get(rtype, 0.0)
        worth_deep = task_value in ("high", "very_high") and budget >= BUDGET_THRESHOLD
        assessments.append({
            "region_id": hint.get("region_id"),
            "region_type": rtype,
            "task_relevance": task_value,
            "budget_share": budget,
            "worth_deep_understanding": worth_deep,
            "candidate_only": True,
        })

    return {"region_value_assessments": assessments, "goal_type": goal_type}


def _allocate_budget(*, value_assessment: Dict[str, Any], goal_type: str) -> Dict[str, Any]:
    deep: List[str] = []
    skipped: List[str] = []
    allocations: List[Dict[str, Any]] = []

    for item in value_assessment.get("region_value_assessments") or []:
        trigger = item.get("worth_deep_understanding", False)
        entry = {
            "region_id": item.get("region_id"),
            "region_type": item.get("region_type"),
            "budget_share": item.get("budget_share", 0.0),
            "trigger_region_intelligence": trigger,
            "candidate_only": True,
        }
        allocations.append(entry)
        rid = item.get("region_id", "")
        if trigger:
            deep.append(rid)
        else:
            skipped.append(rid)

    return {
        "goal_type": goal_type,
        "budget_allocations": allocations,
        "deep_understanding_regions": deep,
        "skipped_regions": skipped,
        "candidate_only": True,
    }


def apply_attention_gate(
    *,
    l0_scan: Dict[str, Any],
    goal_type: str,
) -> Dict[str, Any]:
    """
    Attention Gate — NOT a label system; blocks RI and capabilities for low-value regions.
    """
    value = _assess_for_goal(l0_scan=l0_scan, goal_type=goal_type)
    budget = _allocate_budget(value_assessment=value, goal_type=goal_type)

    allowed: List[Dict[str, Any]] = []
    blocked: List[Dict[str, Any]] = []

    for item in value.get("region_value_assessments") or []:
        rid = item.get("region_id", "")
        entity = REGION_ENTITY_MAP.get(rid, {})
        caps = entity.get("capabilities") or list(ALL_CAPABILITIES)

        if item.get("worth_deep_understanding"):
            allowed.append({
                "region_id": rid,
                "region_type": item.get("region_type"),
                "entity_id": entity.get("entity_id"),
                "allowed_capabilities": caps,
                "gate_status": "allowed",
                "candidate_only": True,
            })
        else:
            blocked.append({
                "region": item.get("region_type"),
                "region_id": rid,
                "skip_reason": "low_task_value",
                "blocked_capabilities": [
                    "text_recognition",
                    "visual_reasoning",
                ] + [c for c in caps if c not in ("understand_region_ownership",)],
                "gate_status": "blocked",
                "attention_is_control_not_label": True,
                "candidate_only": True,
            })

    return {
        "gate_id": _uid("ag"),
        "goal_type": goal_type,
        "value_assessment": value,
        "observation_budget": budget,
        "allowed_regions": allowed,
        "blocked_regions": blocked,
        "region_intelligence_allowed_for": [a.get("region_id") for a in allowed],
        "region_intelligence_blocked_for": [b.get("region_id") for b in blocked],
        "attention_gates_region_intelligence": len(blocked) > 0,
        "not_all_regions_execute": len(blocked) > 0 or len(allowed) < len(value.get("region_value_assessments") or []),
        "candidate_only": True,
    }
