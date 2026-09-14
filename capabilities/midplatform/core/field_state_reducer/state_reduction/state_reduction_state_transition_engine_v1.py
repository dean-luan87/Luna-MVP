from __future__ import annotations

from typing import Any, Dict, List

from .state_reduction_types_v1 import StateTransitionResult


def evaluate_state_transition(
    current_status: str,
    requested_status: str,
    temporal_snapshot: Dict[str, Any],
    conflict_snapshot: Dict[str, Any],
    plan_intended_change: str,
) -> StateTransitionResult:
    reasons: List[str] = []
    required_evidence: List[str] = []
    trace: List[Dict[str, Any]] = []

    transition = f"{current_status}->{requested_status}"

    if current_status == "revoked" and requested_status == "active":
        reasons.append("revoked_not_reactivatable")
    if (
        current_status == "expired"
        and requested_status == "active"
        and not bool(temporal_snapshot.get("new_event_available", False))
    ):
        reasons.append("expired_requires_new_event")
        required_evidence.append("new_event")
    if (
        current_status == "suspended"
        and requested_status == "active"
        and not bool(temporal_snapshot.get("refresh_evidence_available", False))
    ):
        reasons.append("suspended_requires_refresh_evidence")
        required_evidence.append("refresh_evidence")
    if current_status == "superseded" and requested_status == "active":
        reasons.append("superseded_not_reactivatable")
    if (
        current_status == "conflicted"
        and requested_status == "active"
        and not bool(conflict_snapshot.get("resolution_available", False))
    ):
        reasons.append("conflicted_requires_resolution")
        required_evidence.append("conflict_resolution")
    if (
        current_status == "unresolved"
        and requested_status == "active"
        and not bool(temporal_snapshot.get("sufficient_evidence", False))
    ):
        reasons.append("unresolved_requires_sufficient_evidence")
        required_evidence.append("sufficient_evidence")

    if plan_intended_change == "no_state_change":
        requested_status = current_status
        transition = f"{current_status}->{current_status}"

    transition_allowed = len(reasons) == 0
    transition_status = requested_status if transition_allowed else current_status

    trace.append(
        {
            "requested_transition": transition,
            "transition_allowed": transition_allowed,
            "transition_status": transition_status,
        }
    )

    return StateTransitionResult(
        requested_transition=transition,
        transition_allowed=transition_allowed,
        transition_status=transition_status,
        required_evidence=tuple(dict.fromkeys(required_evidence)),
        rejection_reasons=tuple(dict.fromkeys(reasons)),
        transition_trace=tuple(trace),
    )
