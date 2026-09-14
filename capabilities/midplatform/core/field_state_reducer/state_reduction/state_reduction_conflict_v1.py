from __future__ import annotations

from typing import Any, Dict, List

from .state_reduction_types_v1 import ConflictReductionResult, SelectionHandoffInput


def reduce_conflict(
    handoff_input: SelectionHandoffInput,
    selected_policy_ids: tuple[str, ...],
) -> ConflictReductionResult:
    snapshot = dict(handoff_input.conflict_snapshot)
    conflict_type = str(snapshot.get("conflict_type", "none"))
    unresolved = bool(snapshot.get("unresolved", False))
    preserve_conflict = bool(snapshot.get("preserve_conflict", False))
    provisional_allowed = bool(snapshot.get("provisional_candidate_allowed", True))

    conflicting_event_refs = tuple(
        str(x) for x in snapshot.get("conflicting_event_refs", [])
    )
    reasons: List[str] = []
    steps: List[Dict[str, Any]] = []

    has_conflict_refs = len(conflicting_event_refs) > 0

    if unresolved:
        preserve_conflict = True
        reasons.append("unresolved_conflict_preserved")

    if snapshot.get("winner_fabrication_requested", False):
        reasons.append("fabricated_winner_rejected")

    if "conflict_preservation" in selected_policy_ids:
        preserve_conflict = True

    if has_conflict_refs:
        preserve_conflict = True

    if unresolved and not provisional_allowed:
        reasons.append("provisional_candidate_not_allowed")

    status = "none"
    if unresolved:
        status = "unresolved"
    elif preserve_conflict:
        status = "conflicted"

    steps.append(
        {
            "conflict_type": conflict_type,
            "unresolved": unresolved,
            "preserve_conflict": preserve_conflict,
            "provisional_candidate_allowed": provisional_allowed,
            "status": status,
        }
    )

    return ConflictReductionResult(
        conflict_status=status,
        preserve_conflict=preserve_conflict,
        provisional_candidate_allowed=provisional_allowed,
        conflicting_event_refs=conflicting_event_refs,
        rejection_reasons=tuple(dict.fromkeys(reasons)),
        decision_steps=tuple(steps),
    )
