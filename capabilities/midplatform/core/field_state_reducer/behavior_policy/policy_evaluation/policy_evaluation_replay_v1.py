from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

from ..field_state_reducer_behavior_policy_trace_types_v1 import (
    BehaviorPolicyReplayKeyV1,
)
from .policy_evaluation_types_v1 import EvaluationInput, EvaluationReplayKey


def build_evaluation_replay_key(
    evaluation_input: EvaluationInput,
    snapshot_versions: Dict[str, str],
) -> EvaluationReplayKey:
    fingerprint = {
        "evaluation_id": evaluation_input.evaluation_id,
        "policy_id": evaluation_input.policy_id,
        "state_type": evaluation_input.state_type,
        "policy_registry_version": evaluation_input.policy_registry_version,
        "eligibility_matrix_version": evaluation_input.eligibility_matrix_version,
        "evaluation_contract_version": evaluation_input.evaluation_contract_version,
        "snapshot_versions": snapshot_versions,
    }

    base = BehaviorPolicyReplayKeyV1(
        policy_registry_version=evaluation_input.policy_registry_version,
        eligibility_matrix_version=evaluation_input.eligibility_matrix_version,
        precedence_matrix_version=str(
            snapshot_versions.get("evaluation_matrix_version", "v1")
        ),
        composition_contract_version=str(
            snapshot_versions.get("condition_registry_version", "v1")
        ),
        stable_fingerprint=json.dumps(fingerprint, sort_keys=True),
    )

    replay_key = hashlib.sha256(
        json.dumps(base.__dict__, sort_keys=True).encode("utf-8")
    ).hexdigest()

    return EvaluationReplayKey(
        replay_key=replay_key, snapshot_versions=dict(snapshot_versions)
    )
