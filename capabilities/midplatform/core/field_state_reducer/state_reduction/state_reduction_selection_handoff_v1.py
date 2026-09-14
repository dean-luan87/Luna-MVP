from __future__ import annotations

from typing import List, Tuple

from .state_reduction_types_v1 import SelectionHandoffInput


_REJECT_SELECTION_STATUS = {
    "unresolved_precedence",
    "unresolved_exclusion",
    "invalid_input",
}


def validate_selection_handoff(
    handoff_input: SelectionHandoffInput,
) -> Tuple[str, Tuple[str, ...]]:
    reasons: List[str] = []

    if handoff_input.selection_status in _REJECT_SELECTION_STATUS:
        reasons.append(handoff_input.selection_status)

    required_versions = {
        "policy_registry_version",
        "eligibility_matrix_version",
        "precedence_matrix_version",
        "composition_contract_version",
        "replay_contract_version",
    }
    missing_versions = [
        key
        for key in required_versions
        if not str(handoff_input.version_snapshots.get(key, ""))
    ]
    if missing_versions:
        reasons.append("missing_version_snapshot")

    if handoff_input.direct_state_write_requested:
        reasons.append("direct_state_write_forbidden")
    if handoff_input.action_trigger_requested:
        reasons.append("action_trigger_forbidden")

    if (
        handoff_input.selection_status.startswith("selected")
        and not handoff_input.selected_policy_ids
    ):
        reasons.append("missing_selected_policy_metadata")

    for policy_id in handoff_input.selected_policy_ids:
        metadata = handoff_input.selected_policy_metadata.get(policy_id)
        if not metadata or not str(metadata.get("policy_version", "")):
            reasons.append("missing_selected_policy_metadata")
            break

    if (
        not handoff_input.reducer_run_id
        or not handoff_input.field_id
        or not handoff_input.state_type
    ):
        reasons.append("invalid_input")

    handoff_status = "accepted" if not reasons else "rejected"
    return handoff_status, tuple(dict.fromkeys(reasons))
