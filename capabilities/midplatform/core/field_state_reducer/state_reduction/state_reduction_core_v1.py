from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .state_reduction_types_v1 import (
    ConflictReductionResult,
    OverlayReductionResult,
    PolicyApplicationPlan,
    SelectionHandoffInput,
)
from .entity_field_relation_state_value_v1 import (
    ENTITY_FIELD_OBSERVATION_RELATION_STATE_V1,
    build_entity_field_relation_state_value_v1,
)


def reduce_state_core(
    handoff_input: SelectionHandoffInput,
    application_plan: PolicyApplicationPlan,
    conflict_result: ConflictReductionResult,
    overlay_result: OverlayReductionResult,
) -> Tuple[
    str, Dict[str, Any], str | None, Tuple[str, ...], Tuple[Dict[str, Any], ...]
]:
    existing_state = dict(handoff_input.existing_state_snapshot)
    existing_state_ref = str(existing_state.get("state_id", "")) or None
    current_status = str(existing_state.get("status", "candidate"))

    reduction_steps: List[Dict[str, Any]] = []
    reasons: List[str] = []

    intended_change = application_plan.intended_change_type
    target_status = application_plan.target_state_status

    if intended_change == "no_state_change":
        requested_status = current_status
        reduction_value = (
            dict(existing_state.get("value", {})) if existing_state else {}
        )
        reduction_steps.append({"mode": "no_state_change", "status": requested_status})
        return (
            requested_status,
            reduction_value,
            existing_state_ref,
            tuple(reasons),
            tuple(reduction_steps),
        )

    if not existing_state_ref:
        requested_status = "candidate"
        reduction_steps.append(
            {"mode": "create_candidate", "reason": "no_existing_state"}
        )
    else:
        requested_status = target_status
        reduction_steps.append(
            {
                "mode": "replacement_candidate",
                "previous_state_ref": existing_state_ref,
                "from_status": current_status,
                "to_status": requested_status,
            }
        )

    if conflict_result.conflict_status in {"unresolved", "conflicted"}:
        requested_status = conflict_result.conflict_status
        reasons.append("conflict_driven_status")

    temporal_status = str(handoff_input.temporal_snapshot.get("status", "unknown"))
    if temporal_status == "revoked":
        requested_status = "revoked"
    elif temporal_status == "expired":
        requested_status = "expired"
    elif temporal_status == "suspended":
        requested_status = "suspended"
    elif temporal_status == "superseded":
        requested_status = "superseded"

    if overlay_result.overlay_status == "temporary_overlay_candidate":
        requested_status = "candidate"
        reasons.append("temporary_overlay_is_candidate_only")

    candidate_value = {
        "selected_policy_ids": list(application_plan.selected_policy_ids),
        "intended_change_type": intended_change,
        "temporal_status": temporal_status,
        "conflict_status": conflict_result.conflict_status,
        "overlay_status": overlay_result.overlay_status,
    }

    if (
        handoff_input.state_type == ENTITY_FIELD_OBSERVATION_RELATION_STATE_V1
        and intended_change == "maintain_state"
    ):
        relation_value = build_entity_field_relation_state_value_v1(
            handoff_input.admitted_events
        )
        if relation_value is not None:
            candidate_value = relation_value

    reduction_steps.append(
        {
            "intended_change": intended_change,
            "target_state_status": target_status,
            "final_requested_status": requested_status,
            "temporal_status": temporal_status,
            "conflict_status": conflict_result.conflict_status,
            "overlay_status": overlay_result.overlay_status,
        }
    )

    return (
        requested_status,
        candidate_value,
        existing_state_ref,
        tuple(dict.fromkeys(reasons)),
        tuple(reduction_steps),
    )
