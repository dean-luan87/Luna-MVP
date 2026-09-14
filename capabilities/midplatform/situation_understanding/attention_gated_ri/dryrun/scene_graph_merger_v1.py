# -*- coding: utf-8 -*-
"""Scene Graph — merge Ownership + Attention (Observation Priority) v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4

from capabilities.midplatform.situation_understanding.attention_gated_ri.dryrun.dryrun_goal_profiles_v1 import (
    REGION_ENTITY_MAP,
)


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def merge_scene_graph(
    *,
    priority_graph: Dict[str, Any],
    gated_ri: Dict[str, Any],
    gate: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Scene Graph nodes combine:
    - Ownership: 这个东西是谁的？
    - Attention: 现在值得关注谁？
    """
    attention_by_region = {
        n.get("region_id"): n for n in priority_graph.get("attention_nodes") or []
    }
    blocked_by_region = {
        b.get("region_id"): b for b in gate.get("blocked_regions") or []
    }
    activated_ids = {e.get("region_id") for e in gated_ri.get("entity_candidates") or []}

    entities: List[Dict[str, Any]] = []
    for node in priority_graph.get("attention_nodes") or []:
        rid = node.get("region_id", "")
        meta = REGION_ENTITY_MAP.get(rid, {})
        blocked = blocked_by_region.get(rid)
        entities.append({
            "entity_id": meta.get("entity_id") or rid,
            "region_id": rid,
            "region_type": node.get("region_type"),
            "ownership": meta.get("ownership_type", "unknown"),
            "attention": {
                "priority": node.get("attention_priority"),
                "budget_share": node.get("budget_share"),
                "worth_observing": node.get("worth_observing"),
                "gate_status": "blocked" if blocked else "allowed",
            },
            "reason": blocked.get("skip_reason") if blocked else "task_relevant",
            "region_intelligence_activated": rid in activated_ids,
            "candidate_only": True,
        })

    return {
        "scene_graph_id": _uid("sg"),
        "graph_type": "scene_graph",
        "goal_type": priority_graph.get("goal_type"),
        "entities": entities,
        "ownership_plus_attention": True,
        "not_ownership_alone": True,
        "candidate_only": True,
    }
