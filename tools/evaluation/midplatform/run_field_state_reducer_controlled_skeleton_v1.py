# -*- coding: utf-8 -*-
"""Run Field State Reducer controlled skeleton v1 (non-runtime)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.field_state_reducer_fixture_v1 import (
    build_xiaobeimen_construction_closure_fixture_v1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_skeleton_v1 import (
    FieldStateReducerSkeletonV1,
)
from capabilities.midplatform.core.field_state_reducer.field_state_reducer_types_v1 import (
    FieldStateReducerConfigSnapshotV1,
    FieldStateReducerInputV1,
    FieldStateReducerVersionSnapshotV1,
)


def run_field_state_reducer_controlled_skeleton_v1() -> Dict[str, Any]:
    fixture_events = build_xiaobeimen_construction_closure_fixture_v1()
    reducer = FieldStateReducerSkeletonV1()

    reducer_input = FieldStateReducerInputV1(
        admitted_field_events=fixture_events,
        temporal_validity_snapshot={
            "snapshot_id": "temporal_snapshot_xiaobeimen_v1",
            "scope": "xiaobeimen_construction_closure",
            "synthetic": True,
        },
        reducer_config_snapshot=FieldStateReducerConfigSnapshotV1(
            reduction_policy_version="v1",
            event_type_registry_version="v1",
            conflict_resolution_matrix_version="v1",
            deterministic_evaluation_timestamp="2026-07-15T00:00:00Z",
        ),
        reducer_version_snapshot=FieldStateReducerVersionSnapshotV1(
            reducer_version="field_state_reducer_skeleton_v1",
            reduction_policy_version="v1",
            registry_version="v1",
            configuration_snapshot_ref="cfg_snapshot_v1",
        ),
        direct_state_mutation_requested=False,
        skeleton_only=True,
        no_external_lookup=True,
        no_provider_recall=True,
        no_action_trigger=True,
    )

    output = reducer.reduce(reducer_input)

    return {
        "phase": "Phase-Luna-Field-State-Reducer-Controlled-Skeleton-Implementation-v1-001",
        "stage": "Controlled Skeleton Implementation",
        "runtime_execution": False,
        "state_mutation_executed": False,
        "skeleton_only": True,
        "candidate_only": True,
        "resulting_state": None,
        "reduction_decision": output.reduction_decision,
        "state_change_type": output.state_change_type,
        "deterministic_replay_key": output.deterministic_replay_key,
        "reducer_trace": output.reducer_trace,
    }


def main() -> int:
    result = run_field_state_reducer_controlled_skeleton_v1()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
