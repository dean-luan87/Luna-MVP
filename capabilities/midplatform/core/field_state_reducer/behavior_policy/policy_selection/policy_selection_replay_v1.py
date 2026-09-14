from __future__ import annotations

import hashlib
import json
from typing import Dict

from ..field_state_reducer_behavior_policy_trace_types_v1 import (
    BehaviorPolicyReplayKeyV1,
)
from .policy_selection_types_v1 import PolicySelectionInput, PolicySelectionReplayKey


def build_policy_selection_replay_key(
    selection_input: PolicySelectionInput,
    snapshot_versions: Dict[str, str],
    ordered_policy_ids: tuple[str, ...],
    selected_policy_ids: tuple[str, ...],
) -> PolicySelectionReplayKey:
    fingerprint = {
        "selection_id": selection_input.selection_id,
        "reducer_run_id": selection_input.reducer_run_id,
        "field_id": selection_input.field_id,
        "state_type": selection_input.state_type,
        "input_evaluation_ids": [
            str(row.get("evaluation_id", ""))
            for row in selection_input.evaluation_results
        ],
        "ordered_policy_ids": list(ordered_policy_ids),
        "selected_policy_ids": list(selected_policy_ids),
        "snapshot_versions": snapshot_versions,
    }

    base = BehaviorPolicyReplayKeyV1(
        policy_registry_version=snapshot_versions.get("policy_registry_version", "v1"),
        eligibility_matrix_version=snapshot_versions.get(
            "eligibility_matrix_version", "v1"
        ),
        precedence_matrix_version=snapshot_versions.get(
            "precedence_matrix_version", "v1"
        ),
        composition_contract_version=snapshot_versions.get(
            "composition_contract_version", "v1"
        ),
        stable_fingerprint=json.dumps(fingerprint, sort_keys=True),
    )

    replay_key = hashlib.sha256(
        json.dumps(base.__dict__, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return PolicySelectionReplayKey(
        replay_key=replay_key,
        snapshot_versions=dict(snapshot_versions),
    )
