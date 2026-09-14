"""Controlled runner entry for the Dynamic Cognitive Flow candidate fixture.

This module exposes a callable result builder only.  It does not start a
runtime, invoke a provider, or write an artifact by itself.
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

RUNNER_PATH = Path(__file__).resolve()
REPO_ROOT = next(
    candidate
    for candidate in (RUNNER_PATH, *RUNNER_PATH.parents)
    if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir()
)
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_engine_v1 import (  # noqa: E402
    DynamicCognitiveFlowEngineV1,
)
from capabilities.midplatform.core.cognitive_flow.cognitive_dynamic_loop_fixture_v1 import (  # noqa: E402
    build_dynamic_cognitive_loop_scenarios_v1,
)


PHASE_ID = "Phase-Luna-Dynamic-Cognitive-Flow-Minimum-Actionable-Loop-Controlled-Implementation-v1-001"


def _case_passed(case_result: Dict[str, object]) -> bool:
    expected = case_result["expected"]
    actual = case_result["actual"]
    if not isinstance(expected, dict) or not isinstance(actual, dict):
        return False
    for field in (
        "final_disposition",
        "next_step_disposition",
        "state_version_count",
        "reconsideration_count",
        "non_materialized_plan_count",
    ):
        if expected.get(field) != actual.get(field):
            return False
    expected_eligible = expected.get("eligible_invocation")
    if expected_eligible is not None and expected_eligible != actual.get("eligible_invocation"):
        return False
    return bool(actual.get("candidate_only")) and not bool(
        actual.get("runtime_execution") or actual.get("provider_invocation")
    )


def build_controlled_implementation_result_v1() -> Dict[str, object]:
    """Build candidate-only scenario results for a later authorized terminal run."""

    engine = DynamicCognitiveFlowEngineV1()
    scenario_results: List[Dict[str, object]] = []
    for scenario in build_dynamic_cognitive_loop_scenarios_v1():
        output = engine.run_case(scenario.request)
        scenario_results.append(
            {
                "scenario_id": scenario.scenario_id,
                "title": scenario.title,
                "expected": {
                    "final_disposition": scenario.expected_final_disposition,
                    "next_step_disposition": scenario.expected_next_step_disposition,
                    "state_version_count": scenario.expected_state_version_count,
                    "reconsideration_count": scenario.expected_reconsideration_count,
                    "non_materialized_plan_count": scenario.expected_non_materialized_plan_count,
                    "eligible_invocation": scenario.expected_eligible_invocation,
                },
                "actual": {
                    "final_disposition": output.final_disposition,
                    "next_step_disposition": output.next_step_disposition,
                    "state_version_count": len(output.state_versions),
                    "reconsideration_count": len(output.reconsiderations),
                    "non_materialized_plan_count": len(output.non_materialized_plan_refs),
                    "resolution_ref_count": len(output.resolution_refs),
                    "invocation_candidate_count": len(output.invocation_candidate_refs),
                    "eligible_invocation": bool(output.eligible_invocation_refs),
                    "candidate_only": output.candidate_only,
                    "runtime_execution": output.runtime_execution,
                    "provider_invocation": output.provider_invocation,
                },
                "candidate_output": asdict(output),
            }
        )
    failed_case_ids = [
        str(case["scenario_id"])
        for case in scenario_results
        if not _case_passed(case)
    ]
    return {
        "phase": PHASE_ID,
        "mode": "CONTROLLED_IMPLEMENTATION",
        "owner": "Cognitive Flow Governance",
        "scenario_count": len(scenario_results),
        "all_cases_passed": not failed_case_ids,
        "failed_case_ids": failed_case_ids,
        "key_dynamic_loop_guards": {
            "candidate_only": True,
            "remaining_plan_candidates_binding": False,
            "stop_sufficient_is_failure": False,
            "capability_failure_is_task_failure": False,
            "stale_requirement_forces_invocation": False,
            "runtime_execution": False,
            "provider_invocation": False,
        },
        "candidate_only": True,
        "runtime_execution": False,
        "provider_invocation": False,
        "camera_activation": False,
        "scheduler_execution": False,
        "learning_execution": False,
        "memory_mutation": False,
        "automatic_capability_acquisition": False,
        "action_execution": False,
        "scenario_results": scenario_results,
    }


__all__ = ["PHASE_ID", "build_controlled_implementation_result_v1"]


if __name__ == "__main__":
    result = build_controlled_implementation_result_v1()
    summary = {
        "phase": result["phase"],
        "scenario_count": result["scenario_count"],
        "all_cases_passed": result["all_cases_passed"],
        "failed_case_ids": result["failed_case_ids"],
        "key_dynamic_loop_guards": result["key_dynamic_loop_guards"],
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["all_cases_passed"] else 1)
