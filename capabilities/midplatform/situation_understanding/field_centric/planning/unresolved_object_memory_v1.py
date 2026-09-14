# -*- coding: utf-8 -*-
"""Unresolved Object Memory — 暂时无法定义的对象 v1."""

from __future__ import annotations

from typing import Any, Dict, List
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def record_unresolved_objects(
    *,
    object_ids: List[str],
    role_candidates: List[Dict[str, Any]],
    field_understanding: Dict[str, Any],
    has_interaction: bool,
    goal_relevant: bool = False,
    external_query_attempted: bool = False,
) -> Dict[str, Any]:
    """
    Unknown object 处理路径:
    1. 有交互 → 从交互推断（上游已处理）
    2. 无交互 → 外部查询
    3. 仍无结果且任务无关 → unresolved object memory
    """
    unresolved: List[Dict[str, Any]] = []
    resolved_ids = {r.get("object_id") for r in role_candidates if r.get("role_candidate") != "unresolved"}

    for oid in object_ids:
        if oid in resolved_ids:
            continue
        if has_interaction:
            continue
        if external_query_attempted and not goal_relevant:
            unresolved.append({
                "memory_id": _uid("uom"),
                "object_id": oid,
                "status": "unresolved_object_memory",
                "field_context": field_understanding.get("field_candidate"),
                "external_query_attempted": external_query_attempted,
                "goal_relevant": goal_relevant,
                "action": "record_for_later" if not goal_relevant else "escalate_for_goal",
                "candidate_only": True,
            })

    return {
        "memory_id": _uid("uomr"),
        "unresolved_objects": unresolved,
        "field_constrains_unknown_space": bool(field_understanding.get("expected_entity_profile")),
        "candidate_only": True,
    }
