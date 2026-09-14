from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in __import__("sys").path:
    __import__("sys").path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_decision_skeleton_v1 import (  # noqa: E402
    build_behavior_policy_decision_skeleton,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_fixture_v1 import (  # noqa: E402
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_FIXTURES_V1,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_registry_skeleton_v1 import (  # noqa: E402
    FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1,
)
from capabilities.midplatform.core.field_state_reducer.behavior_policy.field_state_reducer_behavior_policy_static_validators_v1 import (  # noqa: E402
    validate_policy_ids_known,
    validate_policy_registry_complete,
    validate_skeleton_decision_boundary,
)


def run_field_state_reducer_behavior_policy_controlled_skeleton_v1(
    output_root: Path,
) -> Dict[str, Any]:
    output_root.mkdir(parents=True, exist_ok=True)

    fixture_only = all(
        row.get("synthetic") is True
        for row in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_FIXTURES_V1
    )
    registry_ok, registry_issues = validate_policy_registry_complete(
        FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
    )
    policy_ids = tuple(
        str(r.get("policy_id", ""))
        for r in FIELD_STATE_REDUCER_BEHAVIOR_POLICY_REGISTRY_SKELETON_V1
    )
    ids_ok, ids_issues = validate_policy_ids_known(policy_ids)

    decision, trace = build_behavior_policy_decision_skeleton(
        field_id="field_placeholder_v1",
        state_type="path_state",
        temporal_inputs={"status": "active"},
        confidence_inputs={"mode": "placeholder"},
        conflict_inputs={"mode": "preserve"},
        owner_correction_inputs={"candidate_only": True},
        overlay_inputs={"layered": True},
    )
    boundary_ok, boundary_issues = validate_skeleton_decision_boundary(
        decision.__dict__
    )

    result = {
        "runner_id": "run_field_state_reducer_behavior_policy_controlled_skeleton_v1",
        "fixture_only": fixture_only,
        "registry_loaded": registry_ok,
        "policy_ids_known": ids_ok,
        "decision_boundary_ok": boundary_ok,
        "registry_issues": registry_issues,
        "policy_id_issues": ids_issues,
        "decision_boundary_issues": boundary_issues,
        "policy_count": len(policy_ids),
        "state_type_count": 12,
        "decision": {
            "decision_id": decision.decision_id,
            "decision_outcome": decision.decision_outcome,
            "resulting_state_candidate": decision.resulting_state_candidate,
            "selected_policy_ids": list(decision.selected_policy_ids),
            "policy_execution_executed": decision.policy_execution_executed,
            "state_mutation_executed": decision.state_mutation_executed,
            "fact_promotion_executed": decision.fact_promotion_executed,
            "action_trigger_executed": decision.action_trigger_executed,
            "runtime_execution": decision.runtime_execution,
            "skeleton_only": decision.skeleton_only,
            "candidate_only": decision.candidate_only,
        },
        "trace": {
            "trace_id": trace.trace_id,
            "candidate_policy_ids": list(trace.candidate_policy_ids),
            "eligible_policy_ids": list(trace.eligible_policy_ids),
            "rejected_policy_ids": list(trace.rejected_policy_ids),
            "selected_policy_ids": list(trace.selected_policy_ids),
            "precedence_steps": [s.__dict__ for s in trace.precedence_steps],
            "composition_sequence": list(trace.composition_sequence),
            "replay_key": trace.replay_key,
        },
        "no_database": True,
        "no_provider_recall": True,
        "no_external_lookup": True,
        "no_model_call": True,
        "no_action": True,
        "runtime_execution": False,
    }

    out_path = (
        output_root
        / "field_state_reducer_behavior_policy_controlled_skeleton_result_v1.json"
    )
    out_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=4), encoding="utf-8"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(
            REPO_ROOT
            / "_tmp_eval_out"
            / "field_state_reducer_behavior_policy_controlled_skeleton_v1_smoke_v0"
        ),
    )
    args = parser.parse_args()

    result = run_field_state_reducer_behavior_policy_controlled_skeleton_v1(
        output_root=Path(args.output_root)
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
