# -*- coding: utf-8 -*-
"""Qwen-VL Routing Validation — Model Manager dryrun assertions v1."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

FORBIDDEN_PROVIDER_REQUEST_FIELDS = (
    "memory",
    "fact_database",
    "internal_state",
    "user_preference",
    "policy_hidden_rules",
    "private_memory",
)


def validate_routing_candidate(
    *,
    capability_match: Dict[str, Any],
    routing_selection: Dict[str, Any],
    model_record: Dict[str, Any],
    expected_capability: Optional[str] = None,
    expected_provider: Optional[str] = None,
) -> Dict[str, Any]:
    """Validate Model Manager routing output."""
    capability_id = capability_match.get("required_capability", "")
    selected_model = routing_selection.get("selected_model_id")
    selected_tool = routing_selection.get("selected_tool_id")
    checks = {
        "capability_first": capability_match.get("capability_first") is True,
        "lifecycle_active": model_record.get("lifecycle_state") in ("active", "admitted"),
        "routing_candidate_only": routing_selection.get("provider_selection_candidate") is True,
    }
    if expected_capability:
        checks["expected_capability"] = capability_id == expected_capability
    if expected_provider:
        checks["expected_provider"] = selected_model == expected_provider or selected_tool == expected_provider
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True}


def validate_provider_request_boundary(provider_request: Dict[str, Any]) -> Dict[str, Any]:
    """Provider must not receive Luna internal state."""
    serialized = str(provider_request).lower()
    checks = {
        "no_memory_leak": "memory" not in serialized or "missing_information" in serialized,
        "no_fact_database": "fact_database" not in serialized,
        "no_internal_state": "internal_state" not in serialized,
        "evidence_package_only": provider_request.get("request_type") == "model_manager_provider_request",
    }
    for field in FORBIDDEN_PROVIDER_REQUEST_FIELDS:
        if field in provider_request:
            checks[f"no_{field}"] = False
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True}


def validate_no_silent_model_switch(
    *,
    provider_result: Dict[str, Any],
    fallback_plan: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Provider fault must not silently switch to another model."""
    checks = {
        "no_gemini_fallback": "gemini" not in str(fallback_plan or {}).lower(),
        "no_gpt_fallback": "gpt_vision" not in str(fallback_plan or {}).lower(),
        "error_explicit": provider_result.get("provider_error_candidate") is True or provider_result.get("invoked") is False,
        "handoff_to_l2": fallback_plan is None or fallback_plan.get("owned_by") == "L2_Agent_Planning",
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True}


def validate_model_manager_no_goal_ownership(
    *,
    plan: Dict[str, Any],
    routing_selection: Dict[str, Any],
) -> Dict[str, Any]:
    """Model Manager provides candidates; L2 owns goal."""
    goal = (plan.get("plan_goal_candidate") or {}).get("goal_type", "")
    checks = {
        "plan_goal_preserved": bool(goal),
        "mm_produces_candidate": routing_selection.get("produced_provider_candidate_not_decision") is True,
        "no_mm_decision": "decided" not in str(routing_selection.get("routing_reason", "")),
    }
    return {"passed": all(checks.values()), "checks": checks, "candidate_only": True}
