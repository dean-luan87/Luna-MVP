# -*- coding: utf-8 -*-
"""Observation Priority Graph — 现在值得关注谁？v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.dryrun_goal_profiles_v1 import (
    DRYRUN_GOAL_PROFILES,
    REGION_ENTITY_MAP,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_observation_priority_graph(
    *,
    l0_scan: Dict[str, Any],
    goal_type: str,
    budget: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Attention Graph: answers「现在值得关注谁？」
    NOT: image alone decides attention — Goal + Situation → Attention
    """
    profile = DRYRUN_GOAL_PROFILES.get(goal_type, DRYRUN_GOAL_PROFILES["find_subway_exit"])
    priority_labels = profile.get("priority_labels") or {}
    budget_map = {
        a.get("region_id"): a.get("budget_share", 0.0)
        for a in budget.get("budget_allocations") or []
    }

    nodes: List[Dict[str, Any]] = []
    for hint in l0_scan.get("attention_priority_candidates") or []:
        rid = hint.get("region_id", "")
        rtype = hint.get("region_type", "")
        entity = REGION_ENTITY_MAP.get(rid, {})
        nodes.append({
            "node_id": _uid("apn"),
            "region_id": rid,
            "region_type": rtype,
            "entity_id": entity.get("entity_id"),
            "attention_priority": priority_labels.get(rtype, "P3"),
            "budget_share": budget_map.get(rid, 0.0),
            "worth_observing": rid in (budget.get("deep_understanding_regions") or []),
            "candidate_only": True,
        })

    return {
        "graph_id": _uid("opg"),
        "graph_type": "observation_priority_graph",
        "goal_type": goal_type,
        "goal_label": profile.get("goal_label"),
        "attention_nodes": nodes,
        "not_image_decides_attention": True,
        "goal_plus_situation_drives_attention": True,
        "candidate_only": True,
    }
