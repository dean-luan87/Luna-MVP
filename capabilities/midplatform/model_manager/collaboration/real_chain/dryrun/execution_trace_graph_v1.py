# -*- coding: utf-8 -*-
"""Execution Trace Graph — why this model was called v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def build_execution_trace_graph(
    *,
    goal_id: str,
    collaboration_plan_id: str,
    situation: Dict[str, Any],
    plan: Dict[str, Any],
    bound_slots: List[Dict[str, Any]],
    slot_executions: List[Dict[str, Any]],
    evidence_packages: List[Dict[str, Any]],
    validation_id: str,
    fusion_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Full trace: goal → plan → slot → provider → evidence → validation.
    Answers: "为什么用了这个模型？"
    """
    scene = (situation.get("scene_profile_candidate") or {}).get("scene_type", "")
    goal = (plan.get("plan_goal_candidate") or {}).get("goal_type", "")
    missing = [m.get("info_type") for m in situation.get("missing_information_candidates", [])]

    nodes: List[Dict[str, Any]] = [
        {"node_id": goal_id, "node_type": "goal", "goal_type": goal},
        {"node_id": collaboration_plan_id, "node_type": "collaboration_plan"},
    ]

    edges: List[Dict[str, Any]] = [
        {"from": goal_id, "to": collaboration_plan_id, "relation": "requires_collaboration"},
    ]

    slot_traces: List[Dict[str, Any]] = []
    for slot in bound_slots:
        sid = slot.get("slot_id", "")
        cap = slot.get("capability", "")
        provider = slot.get("filled_provider_id", "")
        execution = next((e for e in slot_executions if e.get("slot_id") == sid), {})
        evidence = next((p for p in evidence_packages if p.get("slot_id") == sid), {})

        why = {
            "situation": scene,
            "goal": goal,
            "missing_information": missing,
            "capability_required": cap,
            "provider_selected": provider,
            "reason": "capability_match_for_slot",
        }
        slot_trace = {
            "slot_id": sid,
            "capability": cap,
            "provider_id": provider,
            "provider_execution_id": execution.get("provider_execution_id"),
            "evidence_id": evidence.get("evidence_id") or execution.get("evidence_id"),
            "why_called": why,
        }
        slot_traces.append(slot_trace)
        nodes.append({"node_id": sid, "node_type": "collaboration_slot", "capability": cap})
        edges.append({"from": collaboration_plan_id, "to": sid, "relation": "slot_in_plan"})
        if execution.get("provider_execution_id"):
            pid = execution["provider_execution_id"]
            nodes.append({"node_id": pid, "node_type": "provider_execution", "provider_id": provider})
            edges.append({"from": sid, "to": pid, "relation": "slot_executes_provider"})
        if evidence.get("evidence_id"):
            eid = evidence["evidence_id"]
            nodes.append({"node_id": eid, "node_type": "evidence", "evidence_type": evidence.get("evidence_type")})
            edges.append({"from": execution.get("provider_execution_id", sid), "to": eid, "relation": "produces_evidence"})

    if fusion_id:
        nodes.append({"node_id": fusion_id, "node_type": "fusion"})
        edges.append({"from": collaboration_plan_id, "to": fusion_id, "relation": "fusion_of_evidence"})

    nodes.append({"node_id": validation_id, "node_type": "validation"})
    edges.append({"from": fusion_id or collaboration_plan_id, "to": validation_id, "relation": "validated_by"})

    return {
        "trace_graph_id": _uid("tg"),
        "goal_id": goal_id,
        "collaboration_plan_id": collaboration_plan_id,
        "validation_id": validation_id,
        "fusion_id": fusion_id,
        "nodes": nodes,
        "edges": edges,
        "slot_traces": slot_traces,
        "trace_complete": all([
            goal_id,
            collaboration_plan_id,
            validation_id,
            len(slot_traces) >= 1,
        ]),
        "self_explainable": True,
        "candidate_only": True,
        "not_fact": True,
    }
