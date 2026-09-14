# -*- coding: utf-8 -*-
"""Model Registry State Machine — lifecycle transitions v1."""

from __future__ import annotations

from typing import Any, Dict, FrozenSet, Optional, Tuple

LIFECYCLE_STATES = (
    "discovered",
    "candidate",
    "evaluating",
    "admitted",
    "active",
    "deprecated",
    "blocked",
)

ROUTING_ELIGIBLE_STATES: FrozenSet[str] = frozenset({"admitted", "active"})
EXECUTION_ELIGIBLE_STATES: FrozenSet[str] = frozenset({"active"})

VALID_TRANSITIONS: Dict[str, Tuple[str, ...]] = {
    "discovered": ("candidate", "blocked"),
    "candidate": ("evaluating", "blocked"),
    "evaluating": ("admitted", "candidate", "blocked"),
    "admitted": ("active", "deprecated", "blocked"),
    "active": ("deprecated", "blocked"),
    "deprecated": ("blocked",),
    "blocked": (),
}

TRANSITION_REQUIRES: Dict[Tuple[str, str], str] = {
    ("discovered", "candidate"): "registration_complete",
    ("candidate", "evaluating"): "admission_pipeline_started",
    ("evaluating", "admitted"): "benchmark_passed",
    ("evaluating", "candidate"): "evaluation_failed",
    ("admitted", "active"): "activation_approved",
    ("active", "deprecated"): "replacement_available",
    ("any", "blocked"): "policy_violation",
}


def can_transition(from_state: str, to_state: str) -> bool:
    if to_state == "blocked":
        return from_state != "blocked"
    allowed = VALID_TRANSITIONS.get(from_state, ())
    return to_state in allowed


def is_routing_eligible(state: str, *, admission_status: str = "") -> bool:
    if state == "blocked":
        return False
    if state in ROUTING_ELIGIBLE_STATES:
        return admission_status in ("admitted", "active", "") or state == "active"
    return False


def is_execution_eligible(state: str) -> bool:
    return state in EXECUTION_ELIGIBLE_STATES


def transition_model_state(
    *,
    model_record: Dict[str, Any],
    to_state: str,
    reason: str,
    trigger: Optional[str] = None,
) -> Dict[str, Any]:
    """Apply lifecycle transition; returns updated record + trace entry."""
    from_state = model_record.get("lifecycle_state", "discovered")
    if not can_transition(from_state, to_state):
        return {
            "success": False,
            "error": f"invalid_transition:{from_state}->{to_state}",
            "model_id": model_record.get("model_id"),
            "candidate_only": True,
        }

    trace_entry = {
        "from_state": from_state,
        "to_state": to_state,
        "reason": reason,
        "trigger": trigger or reason,
        "candidate_only": True,
        "not_fact": True,
    }
    history = list(model_record.get("lifecycle_trace", []))
    history.append(trace_entry)

    updated = dict(model_record)
    updated["lifecycle_state"] = to_state
    updated["lifecycle_trace"] = history
    updated["last_transition_reason"] = reason

    if to_state == "admitted":
        updated["admission_status"] = "admitted"
    elif to_state == "active":
        updated["admission_status"] = "admitted"
        updated["activation_status"] = "active"
    elif to_state == "deprecated":
        updated["activation_status"] = "deprecated"
    elif to_state == "blocked":
        updated["admission_status"] = "blocked"
        updated["activation_status"] = "blocked"

    return {
        "success": True,
        "model_record": updated,
        "transition": trace_entry,
        "routing_eligible": is_routing_eligible(
            to_state,
            admission_status=updated.get("admission_status", ""),
        ),
        "execution_eligible": is_execution_eligible(to_state),
        "candidate_only": True,
        "not_fact": True,
    }
