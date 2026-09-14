from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .state_reduction_types_v1 import PolicyApplicationPlan, SelectionHandoffInput


_POLICY_TO_CHANGE_INTENT = {
    "latest_valid_event": ("create_state_candidate", "active"),
    "highest_confidence_valid_event": ("update_state_candidate", "active"),
    "multi_event_consensus": ("maintain_state", "active"),
    "negative_event_override": ("degrade_state", "degraded"),
    "revocation_override": ("revoke_state", "revoked"),
    "expiration_degrade": ("expire_state", "expired"),
    "temporary_overlay_separation": ("apply_temporary_overlay_candidate", "candidate"),
    "conflict_preservation": ("preserve_conflict", "conflicted"),
    "insufficient_evidence_unresolved": ("request_refresh_evidence", "unresolved"),
    "explicit_owner_override_candidate": ("supersede_state", "superseded"),
    "no_state_change": ("no_state_change", "candidate"),
}


def build_policy_application_plan(
    handoff_input: SelectionHandoffInput,
    handoff_status: str,
    handoff_reasons: Tuple[str, ...],
) -> PolicyApplicationPlan:
    steps: List[Dict[str, Any]] = []
    blocking_reasons: List[str] = list(handoff_reasons)
    deferred_actions: List[str] = []

    if handoff_status != "accepted":
        return PolicyApplicationPlan(
            application_plan_id=f"plan_{handoff_input.reducer_run_id}",
            selected_policy_ids=tuple(handoff_input.selected_policy_ids),
            ordered_application_steps=tuple(),
            intended_change_type="no_state_change",
            target_state_status="candidate",
            supporting_event_refs=tuple(handoff_input.admitted_event_refs),
            blocking_reasons=tuple(dict.fromkeys(blocking_reasons)),
            deferred_actions=("request_handoff_fix",),
            candidate_only=True,
        )

    ordered_ids = (
        tuple(handoff_input.composition_sequence)
        if handoff_input.composition_sequence
        else tuple(handoff_input.selected_policy_ids)
    )

    for idx, policy_id in enumerate(ordered_ids, start=1):
        intent, target_status = _POLICY_TO_CHANGE_INTENT.get(
            policy_id, ("maintain_state", "candidate")
        )
        step = {
            "step": idx,
            "policy_id": policy_id,
            "change_intent": intent,
            "target_state_status": target_status,
            "candidate_only": True,
        }
        steps.append(step)

        if intent == "request_refresh_evidence":
            deferred_actions.append("refresh_evidence")
        if intent == "apply_temporary_overlay_candidate":
            deferred_actions.append("overlay_refresh_after_end")

    intended_change_type = steps[-1]["change_intent"] if steps else "no_state_change"
    target_state_status = steps[-1]["target_state_status"] if steps else "candidate"

    if not steps:
        blocking_reasons.append("no_selected_policy")

    return PolicyApplicationPlan(
        application_plan_id=f"plan_{handoff_input.reducer_run_id}",
        selected_policy_ids=ordered_ids,
        ordered_application_steps=tuple(steps),
        intended_change_type=intended_change_type,
        target_state_status=target_state_status,
        supporting_event_refs=tuple(handoff_input.admitted_event_refs),
        blocking_reasons=tuple(dict.fromkeys(blocking_reasons)),
        deferred_actions=tuple(dict.fromkeys(deferred_actions)),
        candidate_only=True,
    )
