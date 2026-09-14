"""Controlled synthetic runner; intentionally not executed in this phase."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict, List

from .adapters_v1 import adapt_result_to_source_state, build_brain_adjudication_input
from .fixtures_v1 import SCENARIOS, SyntheticScenarioV1


def _run_one(case: SyntheticScenarioV1) -> Dict[str, Any]:
    if case.category in {"SOURCE_RETURN", "ACTION_RETURN", "OBSERVABILITY"}:
        assert case.result is not None
        output = adapt_result_to_source_state(
            case.result,
            target_boundary=case.target_boundary,
            expected_concern_ref="concern:synthetic:1",
            adapter_kind="Synthetic Provider/Action Result adapter",
        )
        blocked = output.failure is not None
        passed = blocked == case.expected_blocked
        if case.observability_focus == "field_mutation_false":
            passed = passed and output.field_event is not None and output.field_event.field_mutation is False
        if case.observability_focus == "world_truth_false":
            passed = passed and output.current_world_update is not None and output.current_world_update.world_truth_declared is False
        if case.observability_focus == "invalidation":
            passed = passed and bool(output.edge.invalidation_refs)
        if case.observability_focus == "next_target":
            passed = passed and output.edge.next_target == "A / Field admission"
        return {
            "scenario_id": case.scenario_id,
            "passed": passed,
            "blocked": blocked,
            "failure": asdict(output.failure) if output.failure else None,
            "current_world_candidate": output.current_world_candidate_ref,
            "field_event_candidate": output.field_event.event_candidate_ref if output.field_event else None,
            "brain_input_candidate": None,
            "edge": asdict(output.edge),
            "guards": asdict(output.guards),
        }
    assert case.outcome is not None
    output = build_brain_adjudication_input(case.outcome, expected_concern_ref="concern:synthetic:1")
    blocked = output.failure is not None
    passed = blocked == case.expected_blocked
    if case.observability_focus == "brain_mutation_false":
        passed = passed and output.input_candidate is not None and output.input_candidate.brain_state_mutation is False
    if case.scenario_id == "outcome_revoked_grant":
        passed = passed and blocked is True
    return {
        "scenario_id": case.scenario_id,
        "passed": passed,
        "blocked": blocked,
        "failure": asdict(output.failure) if output.failure else None,
        "current_world_candidate": None,
        "field_event_candidate": None,
        "brain_input_candidate": output.input_candidate.input_ref if output.input_candidate else None,
        "edge": asdict(output.edge),
        "guards": asdict(output.guards),
    }


def run_synthetic_return_path() -> Dict[str, Any]:
    results: List[Dict[str, Any]] = [_run_one(case) for case in SCENARIOS]
    return {
        "scenario_count": len(results),
        "all_cases_passed": all(item["passed"] for item in results),
        "failed_case_ids": [item["scenario_id"] for item in results if not item["passed"]],
        "current_world_candidate_count": sum(bool(item["current_world_candidate"]) for item in results),
        "field_event_candidate_count": sum(bool(item["field_event_candidate"]) for item in results),
        "brain_adjudication_input_count": sum(bool(item["brain_input_candidate"]) for item in results),
        "stale_block_count": sum(1 for item in results if item["failure"] and item["failure"]["classification"] in {"SOURCE_VERSION_MISMATCH", "OUTCOME_SOURCE_STALE"}),
        "invalid_block_count": sum(bool(item["blocked"]) for item in results),
        "source_mutation_count": 0,
        "brain_mutation_count": 0,
        "runtime_execution_count": 0,
        "key_guards": {
            "candidate_only": all(item["guards"]["source_mutation_executed"] is False for item in results),
            "no_world_truth": all(item["guards"]["world_truth_declared"] is False for item in results),
            "no_brain_execution": all(item["guards"]["brain_adjudication_executed"] is False for item in results),
            "no_runtime": all(item["guards"]["runtime_execution"] is False for item in results),
        },
        "case_results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run_synthetic_return_path(), indent=2, ensure_ascii=False))
