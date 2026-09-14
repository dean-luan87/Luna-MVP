"""Fixture-only Context Integration DryRun; no role inference or runtime."""
from __future__ import annotations
import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Mapping, Tuple
from capabilities.cognitive_flow.current_cognitive_context.controlled_skeleton.current_cognitive_context_skeleton_v1 import CurrentCognitiveContextControlledSkeletonV1
from .current_cognitive_context_integration_dryrun_serializer_v1 import canonical_json_dumps_v1, write_canonical_json_v1
from .current_cognitive_context_integration_dryrun_types_v1 import CurrentCognitiveContextIntegrationFixtureV1

_CASES = (
    ("home_member_context", "social_context"),
    ("workplace_assistant_context", "task_context"),
    ("navigation_assistant_context", "navigation_context"),
    ("unknown_environment_context", "unknown_environment_context"),
    ("role_conflict_context", "risk_awareness_context"),
    ("goal_change_context", "exploration_context"),
)

def fixed_fixtures_v1() -> Tuple[CurrentCognitiveContextIntegrationFixtureV1, ...]:
    result = []
    for case_id, context_type in _CASES:
        trace = "trace:context-integration:" + case_id
        role = "role:" + case_id
        goal = "goal:" + case_id
        request = {
            "context_id": "context:" + case_id, "context_type": context_type,
            "field_reference": "field:" + case_id, "field_view_reference": "view:" + case_id,
            "survival_context_reference": "survival:" + case_id,
            "task_context_reference": "task-bundle:" + role + ":" + goal,
            "attention_context_reference": "attention:" + case_id,
            "uncertainty_reference": "uncertainty:" + case_id,
            "information_gap_reference": "gap:" + case_id,
            "spatial_scope_reference": "spatial:" + case_id,
            "temporal_scope_reference": "temporal:" + case_id,
            "experience_reference": "experience:" + case_id,
            "provenance_reference": "provenance:" + case_id,
            "trace_reference": trace,
        }
        result.append(CurrentCognitiveContextIntegrationFixtureV1(case_id, role, goal, request))
    return tuple(result)

def _run_once_v1() -> Mapping[str, object]:
    cases = []
    for fixture in fixed_fixtures_v1():
        candidate = CurrentCognitiveContextControlledSkeletonV1.create_candidate(fixture.request)
        validation = CurrentCognitiveContextControlledSkeletonV1.validate_candidate(candidate)
        if not validation.valid:
            raise ValueError("invalid fixture: " + fixture.case_id)
        cases.append({"case_id": fixture.case_id, "role_reference": fixture.role_reference, "goal_reference": fixture.goal_reference, "candidate": json.loads(CurrentCognitiveContextControlledSkeletonV1.serialize_candidate(candidate)), "validation_issue_count": 0})
    flags = asdict(CurrentCognitiveContextControlledSkeletonV1.flags())
    flags.update({"dryrun_executed": True, "fixture_only": True, "simulation_only": True, "role_inferred": False, "role_evolved": False})
    return {"schema_version": "luna.current_cognitive_context.integration_dryrun.v1", "cases": cases, "runtime_flags": flags}

def run_integration_dryrun_v1(output_dir: Path) -> Mapping[str, object]:
    run1, run2 = _run_once_v1(), _run_once_v1()
    payload = dict(run1)
    payload["case_count"] = len(run1["cases"])
    payload["deterministic_run2_equal"] = canonical_json_dumps_v1(run1) == canonical_json_dumps_v1(run2)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_canonical_json_v1(output_dir / "integration_dryrun_result_v1.json", payload)
    return payload

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    result = run_integration_dryrun_v1(args.output_dir)
    print(canonical_json_dumps_v1({"case_count": result["case_count"], "deterministic_run2_equal": result["deterministic_run2_equal"]}))

if __name__ == "__main__": main()
