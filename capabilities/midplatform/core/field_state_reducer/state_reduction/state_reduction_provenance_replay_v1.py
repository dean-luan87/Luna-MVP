from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Tuple

from .state_reduction_types_v1 import FieldStateCandidate, StateReductionTrace


def _stable_hash(data: Dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(data, sort_keys=True).encode("utf-8")).hexdigest()


def build_state_reduction_trace_and_replay(
    reducer_run_id: str,
    field_id: str,
    state_type: str,
    evaluation_refs: Tuple[str, ...],
    selection_refs: Tuple[str, ...],
    application_steps: Tuple[Dict[str, Any], ...],
    state_reduction_steps: Tuple[Dict[str, Any], ...],
    transition_steps: Tuple[Dict[str, Any], ...],
    conflict_decisions: Tuple[Dict[str, Any], ...],
    overlay_decisions: Tuple[Dict[str, Any], ...],
    rejected_operations: Tuple[str, ...],
    version_snapshots: Dict[str, str],
    candidate_payload: Dict[str, Any],
) -> Tuple[StateReductionTrace, str, str]:
    fingerprint = {
        "reducer_run_id": reducer_run_id,
        "field_id": field_id,
        "state_type": state_type,
        "evaluation_refs": list(evaluation_refs),
        "selection_refs": list(selection_refs),
        "application_steps": list(application_steps),
        "state_reduction_steps": list(state_reduction_steps),
        "transition_steps": list(transition_steps),
        "conflict_decisions": list(conflict_decisions),
        "overlay_decisions": list(overlay_decisions),
        "rejected_operations": list(rejected_operations),
        "version_snapshots": dict(version_snapshots),
        "candidate_payload": dict(candidate_payload),
    }

    candidate_hash = _stable_hash(candidate_payload)
    replay_key = _stable_hash(fingerprint)
    trace_id = f"state_reduction_trace_{reducer_run_id}"

    trace = StateReductionTrace(
        trace_id=trace_id,
        evaluation_refs=evaluation_refs,
        selection_refs=selection_refs,
        application_steps=application_steps,
        state_reduction_steps=state_reduction_steps,
        transition_steps=transition_steps,
        conflict_decisions=conflict_decisions,
        overlay_decisions=overlay_decisions,
        rejected_operations=rejected_operations,
        version_snapshots=dict(version_snapshots),
        resulting_candidate_hash=candidate_hash,
        replay_key=replay_key,
    )
    return trace, replay_key, candidate_hash


def candidate_to_min_payload(candidate: FieldStateCandidate | None) -> Dict[str, Any]:
    if candidate is None:
        return {"candidate": None}
    return {
        "state_candidate_id": candidate.state_candidate_id,
        "field_id": candidate.field_id,
        "state_type": candidate.state_type,
        "candidate_status": candidate.candidate_status,
        "candidate_value": dict(candidate.candidate_value),
        "temporal_status": candidate.temporal_status,
        "selected_policy_ids": list(candidate.selected_policy_ids),
        "supporting_event_refs": list(candidate.supporting_event_refs),
        "conflicting_event_refs": list(candidate.conflicting_event_refs),
        "overlay_refs": list(candidate.overlay_refs),
        "provenance_refs": list(candidate.provenance_refs),
        "previous_state_ref": candidate.previous_state_ref,
        "policy_application_plan_ref": candidate.policy_application_plan_ref,
    }
