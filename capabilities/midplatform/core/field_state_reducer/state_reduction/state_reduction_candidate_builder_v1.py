from __future__ import annotations

from typing import Any, Dict

from .state_reduction_types_v1 import (
    FieldStateCandidate,
    OverlayReductionResult,
    PolicyApplicationPlan,
    SelectionHandoffInput,
    StateTransitionResult,
)


def build_field_state_candidate(
    handoff_input: SelectionHandoffInput,
    application_plan: PolicyApplicationPlan,
    requested_status: str,
    candidate_value: Dict[str, Any],
    previous_state_ref: str | None,
    transition_result: StateTransitionResult,
    trace_ref: str,
    replay_key: str,
    conflicting_event_refs: tuple[str, ...],
    overlay_result: OverlayReductionResult,
) -> FieldStateCandidate:
    state_candidate_id = f"state_candidate_{handoff_input.reducer_run_id}"

    owner_refs = tuple(
        str(x)
        for x in handoff_input.owner_correction_snapshot.get(
            "owner_correction_refs", []
        )
    )

    provenance_refs = tuple(
        dict.fromkeys(
            list(handoff_input.policy_evaluation_refs)
            + [handoff_input.selection_trace_ref, handoff_input.selection_replay_key]
        )
    )

    return FieldStateCandidate(
        state_candidate_id=state_candidate_id,
        field_id=handoff_input.field_id,
        state_type=handoff_input.state_type,
        candidate_status=transition_result.transition_status,
        candidate_value=dict(candidate_value),
        temporal_status=str(handoff_input.temporal_snapshot.get("status", "unknown")),
        confidence_snapshot=dict(
            handoff_input.temporal_snapshot.get("confidence_snapshot", {})
        ),
        supporting_event_refs=tuple(handoff_input.admitted_event_refs),
        conflicting_event_refs=conflicting_event_refs,
        overlay_refs=overlay_result.overlay_refs,
        owner_correction_refs=owner_refs,
        provenance_refs=provenance_refs,
        selected_policy_ids=tuple(application_plan.selected_policy_ids),
        policy_application_plan_ref=application_plan.application_plan_id,
        previous_state_ref=previous_state_ref,
        transition_result={
            "requested_transition": transition_result.requested_transition,
            "transition_allowed": transition_result.transition_allowed,
            "transition_status": transition_result.transition_status,
            "required_evidence": list(transition_result.required_evidence),
            "rejection_reasons": list(transition_result.rejection_reasons),
        },
        trace_ref=trace_ref,
        replay_key=replay_key,
        candidate_only=True,
        fact_admitted=False,
        persisted=False,
    )
