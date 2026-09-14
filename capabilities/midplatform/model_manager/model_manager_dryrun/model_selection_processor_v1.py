# -*- coding: utf-8 -*-
"""Model Selection Processor — provider candidate + handoff v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

TEACHER_PROVIDERS = frozenset({"qwen_vl", "gpt_vision", "gemini_vision"})
TOOL_PROVIDERS = frozenset({"ocr_v1", "slam_v1", "depth_v1", "detection_v1", "mobile_sam_v1"})


def _uid(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def select_provider_candidate(
    *,
    capability_match: Dict[str, Any],
    scoring_result: Dict[str, Any],
    min_score: float = 0.3,
) -> Dict[str, Any]:
    """Select best provider candidate; does NOT execute or decide plan."""
    capability_id = capability_match.get("required_capability", "")
    eligible = scoring_result.get("eligible_providers") or []
    scores = scoring_result.get("provider_scores") or []
    selected = eligible[0] if eligible else None

    route_type = "noop"
    selected_model = None
    selected_tool = None
    should_invoke = False

    if selected and selected.get("routing_score", 0) >= 0.5:
        if selected.get("provider_type") == "tool":
            route_type = "tool"
            selected_tool = selected["model_id"]
        else:
            route_type = "model"
            selected_model = selected["model_id"]
            should_invoke = True
    elif selected and selected.get("routing_score", 0) >= min_score:
        if selected.get("provider_type") == "tool":
            route_type = "tool"
            selected_tool = selected["model_id"]
        else:
            route_type = "model"
            selected_model = selected["model_id"]
            should_invoke = True

    return {
        "selection_id": _uid("psc"),
        "required_capability": capability_id,
        "route_type": route_type,
        "selected_model_id": selected_model,
        "selected_tool_id": selected_tool,
        "selected_provider": selected,
        "provider_scores": scores,
        "noop_providers": scoring_result.get("noop_providers", []),
        "routing_reason": scoring_result.get("routing_reason", "capability_first"),
        "should_invoke_model": should_invoke,
        "should_request_teacher": should_invoke and route_type == "model",
        "provider_selection_candidate": True,
        "produced_provider_candidate_not_decision": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_capability_missing_candidate(
    *,
    capability_id: str,
    reason: str,
    unavailable_providers: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """When no provider is available — return to L2, do not silently fallback."""
    return {
        "missing_id": _uid("cmc"),
        "capability_id": capability_id,
        "missing_reason": reason,
        "unavailable_providers": unavailable_providers or [],
        "no_silent_model_fallback": True,
        "return_to_l2_agent_planning": True,
        "capability_missing_candidate": True,
        "candidate_only": True,
        "not_fact": True,
    }


def build_fallback_plan_candidate(
    *,
    capability_id: str,
    original_plan: Dict[str, Any],
    missing: Dict[str, Any],
) -> Dict[str, Any]:
    """Fallback plan candidate for L2 — Model Manager does not own plan."""
    goal = (original_plan.get("plan_goal_candidate") or {}).get("goal_type", "")
    return {
        "fallback_id": _uid("fpc"),
        "original_plan_id": original_plan.get("plan_id", ""),
        "original_goal": goal,
        "suggested_actions": [
            {"action": "replan_with_alternative_capability", "capability_id": capability_id},
            {"action": "request_user_clarification"},
            {"action": "defer_tool_execution"},
        ],
        "missing_ref": missing.get("missing_id"),
        "fallback_plan_candidate": True,
        "owned_by": "L2_Agent_Planning",
        "candidate_only": True,
        "not_fact": True,
    }


def build_handoff_candidates(
    selection: Dict[str, Any],
) -> Dict[str, Any]:
    """Build Tool OS / Teacher Adapter handoff candidates — selection only, no execution."""
    model_id = selection.get("selected_model_id")
    tool_id = selection.get("selected_tool_id")
    route_type = selection.get("route_type", "noop")

    tool_os_handoff = {
        "handoff_id": _uid("toh"),
        "target": "tool_os",
        "should_handoff": route_type == "tool" and tool_id is not None,
        "selected_tool_id": tool_id,
        "handoff_type": "tool_execution_request_candidate",
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }

    teacher_handoff = {
        "handoff_id": _uid("tah"),
        "target": "teacher_adapter",
        "should_handoff": route_type == "model" and model_id is not None,
        "selected_model_id": model_id,
        "handoff_type": "teacher_evidence_request_candidate",
        "not_executed": True,
        "candidate_only": True,
        "not_fact": True,
    }

    return {
        "tool_os_handoff_candidate": tool_os_handoff,
        "teacher_adapter_handoff_candidate": teacher_handoff,
    }
