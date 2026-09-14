"""Controlled adapter for the candidate-only Loop scenario suite."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict

from .cognitive_loop_continuity_candidate_engine_v1 import NEGATIVE_GUARDS, build_controlled_loop_results_v1
from .cognitive_loop_continuity_candidate_fixture_v1 import build_loop_scenario_specs_v1


PHASE = "Phase-Luna-Cognitive-Loop-Governed-Continuity-Candidate-Controlled-Implementation-v1-001"
CANONICAL_OWNER = "Cognitive Flow Governance"


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def build_candidate_loop_run_v1() -> Dict[str, Any]:
    specs = build_loop_scenario_specs_v1()
    results = build_controlled_loop_results_v1(specs)
    failed = [result.scenario_id for result in results if not all(item["passed"] for item in result.checks)]
    all_guards_closed = all(
        all(value is False for value in result.negative_guards.values())
        for result in results
    )
    summary = {
        "phase": PHASE,
        "canonical_owner": CANONICAL_OWNER,
        "scenario_count": len(results),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "candidate_only": True,
        "synthetic_only": True,
        "runtime_execution": False,
        "provider_invocation": False,
        "autonomous_scheduling": False,
        "autonomous_loop_spawning": False,
        "world_truth_authority": False,
        "brain_provider_selection": False,
        "negative_guard_count": len(NEGATIVE_GUARDS),
        "negative_guards_ok": all_guards_closed,
        "materialization_guard": all(
            all(item.non_duplication_guard_passed for item in result.materializations)
            for result in results
        ),
        "multi_loop_isolation_guard": all(
            any(item["field"] == "local_state_isolated" and item["passed"] for item in result.checks)
            for result in results
        ),
        "stale_requirement_forces_invocation": False,
        "stop_sufficient_is_failure": False,
        "outcome_world_truth": False,
        "outcome_action_execution": False,
        "outcome_memory_mutation": False,
        "outcome_experience_mutation": False,
        "cases": [_jsonable(result) for result in results],
    }
    return {"summary": summary}


__all__ = ["PHASE", "CANONICAL_OWNER", "build_candidate_loop_run_v1"]
