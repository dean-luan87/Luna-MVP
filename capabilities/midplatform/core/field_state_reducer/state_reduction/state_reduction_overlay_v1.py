from __future__ import annotations

from typing import Any, Dict, List

from .state_reduction_types_v1 import OverlayReductionResult, SelectionHandoffInput


def reduce_overlay(
    handoff_input: SelectionHandoffInput,
    selected_policy_ids: tuple[str, ...],
) -> OverlayReductionResult:
    snapshot = dict(handoff_input.overlay_snapshot)
    overlay_refs = tuple(str(x) for x in snapshot.get("overlay_refs", []))
    overlay_active = bool(snapshot.get("overlay_active", False))
    overlay_expired = bool(snapshot.get("overlay_expired", False))

    reasons: List[str] = []
    steps: List[Dict[str, Any]] = []

    substrate_mutated = bool(snapshot.get("substrate_mutation_requested", False))
    if substrate_mutated:
        reasons.append("overlay_substrate_mutation_forbidden")
        substrate_mutated = False

    refresh_required = False
    status = "none"

    if "temporary_overlay_separation" in selected_policy_ids or overlay_active:
        status = "temporary_overlay_candidate"
        refresh_required = False

    if overlay_expired:
        status = "overlay_expired"
        refresh_required = True

    if status == "overlay_expired":
        reasons.append("refresh_evidence_required_after_overlay_end")

    steps.append(
        {
            "overlay_active": overlay_active,
            "overlay_expired": overlay_expired,
            "overlay_status": status,
            "refresh_evidence_required": refresh_required,
            "substrate_mutated": substrate_mutated,
        }
    )

    return OverlayReductionResult(
        overlay_status=status,
        overlay_refs=overlay_refs,
        substrate_mutated=substrate_mutated,
        refresh_evidence_required=refresh_required,
        rejection_reasons=tuple(dict.fromkeys(reasons)),
        decision_steps=tuple(steps),
    )
