from __future__ import annotations

from typing import Any, Dict, Tuple

from .state_reduction_types_v1 import SelectionHandoffInput


def build_handoff_input_from_selection_result(
    selection_result: Dict[str, Any],
    *,
    existing_state_snapshot: Dict[str, Any],
    admitted_event_refs: Tuple[str, ...],
    temporal_snapshot: Dict[str, Any],
    conflict_snapshot: Dict[str, Any],
    overlay_snapshot: Dict[str, Any],
    owner_correction_snapshot: Dict[str, Any],
    policy_evaluation_refs: Tuple[str, ...],
    selected_policy_metadata: Dict[str, Dict[str, Any]],
    direct_state_write_requested: bool = False,
    action_trigger_requested: bool = False,
    admitted_events: Tuple[Dict[str, Any], ...] = tuple(),
) -> SelectionHandoffInput:
    return SelectionHandoffInput(
        reducer_run_id=str(selection_result.get("reducer_run_id", "")),
        field_id=str(selection_result.get("field_id", "")),
        state_type=str(selection_result.get("state_type", "")),
        selection_status=str(selection_result.get("selection_status", "")),
        selected_policy_ids=tuple(
            str(x) for x in selection_result.get("selected_policy_ids", [])
        ),
        composition_sequence=tuple(
            str(x) for x in selection_result.get("composition_sequence", [])
        ),
        policy_evaluation_refs=tuple(policy_evaluation_refs),
        selection_trace_ref=str(selection_result.get("selection_trace_ref", "")),
        selection_replay_key=str(selection_result.get("replay_key", "")),
        existing_state_snapshot=dict(existing_state_snapshot),
        admitted_event_refs=tuple(admitted_event_refs),
        temporal_snapshot=dict(temporal_snapshot),
        conflict_snapshot=dict(conflict_snapshot),
        overlay_snapshot=dict(overlay_snapshot),
        owner_correction_snapshot=dict(owner_correction_snapshot),
        version_snapshots=dict(selection_result.get("evaluated_contract_versions", {})),
        selected_policy_metadata=dict(selected_policy_metadata),
        direct_state_write_requested=direct_state_write_requested,
        action_trigger_requested=action_trigger_requested,
        admitted_events=tuple(admitted_events),
    )
