"""Independent contract checks for the Dynamic Cognitive Flow fixture.

The verifier is intentionally provided for user-terminal execution.  It does
not execute during import and it has no runtime/provider integration.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Dict, List

VERIFY_PATH = Path(__file__).resolve()
REPO_ROOT = next(
    candidate
    for candidate in (VERIFY_PATH, *VERIFY_PATH.parents)
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
IMPLEMENTATION_DIR = VERIFY_PATH.parent
DOCUMENTATION_DIR = REPO_ROOT / "docs" / "architecture" / (
    "phase_luna_dynamic_cognitive_flow_minimum_actionable_loop_controlled_implementation_v1"
)
SOURCE_SET = (
    "cognitive_dynamic_loop_types_v1.py",
    "cognitive_dynamic_loop_engine_v1.py",
    "cognitive_dynamic_loop_fixture_v1.py",
    "run_dynamic_cognitive_flow_controlled_implementation_v1.py",
    "verify_dynamic_cognitive_flow_controlled_implementation_v1.py",
)
DOCUMENTATION_SET = (
    "phase_contract.json",
    "inventory_v1.json",
    "dynamic_loop_contract_v1.json",
    "state_transition_contract_v1.json",
    "capability_outcome_relationship_v1.json",
    "scenario_mapping_v1.json",
    "negative_guards_v1.json",
    "change_manifest_v1.json",
    "verifier_scope_v1.json",
    "implementation_summary_v1.md",
)


def verify_dynamic_cognitive_flow_controlled_implementation_v1() -> Dict[str, object]:
    scenarios = build_dynamic_cognitive_loop_scenarios_v1()
    engine = DynamicCognitiveFlowEngineV1()
    scenario_failures: List[str] = []
    negative_guard_failures: List[str] = []
    structural_failures: List[str] = []
    if len(scenarios) != 36:
        structural_failures.append(f"scenario_count:{len(scenarios)}")
    if len({scenario.scenario_id for scenario in scenarios}) != len(scenarios):
        structural_failures.append("scenario_ids_not_unique")

    for scenario in scenarios:
        output = engine.run_case(scenario.request)
        prefix = scenario.scenario_id
        if output.final_disposition != scenario.expected_final_disposition:
            scenario_failures.append(f"{prefix}:final_disposition")
        if output.next_step_disposition != scenario.expected_next_step_disposition:
            scenario_failures.append(f"{prefix}:next_step_disposition")
        if len(output.state_versions) != scenario.expected_state_version_count:
            scenario_failures.append(f"{prefix}:state_version_count")
        if len(output.reconsiderations) != scenario.expected_reconsideration_count:
            scenario_failures.append(f"{prefix}:reconsideration_count")
        if len(output.non_materialized_plan_refs) != scenario.expected_non_materialized_plan_count:
            scenario_failures.append(f"{prefix}:non_materialized_plan_count")
        if scenario.expected_eligible_invocation is not None:
            actual_eligible = bool(output.eligible_invocation_refs)
            if actual_eligible != scenario.expected_eligible_invocation:
                scenario_failures.append(f"{prefix}:stale_invocation_guard")
        if not output.candidate_only or not output.synthetic_only:
            negative_guard_failures.append(f"{prefix}:candidate_boundary")
        if output.runtime_execution or output.provider_invocation:
            negative_guard_failures.append(f"{prefix}:execution_boundary")
        if output.owner_mutation:
            negative_guard_failures.append(f"{prefix}:owner_mutation")
        if output.final_disposition == "SUFFICIENT":
            if output.next_step_disposition != "STOP_SUFFICIENT":
                scenario_failures.append(f"{prefix}:sufficient_not_stop")
            if not output.stop_sufficient_not_failure:
                negative_guard_failures.append(f"{prefix}:stop_marked_failure")

    source_set_failures = [
        path for path in SOURCE_SET if not (IMPLEMENTATION_DIR / path).is_file()
    ]
    documentation_set_failures = [
        path for path in DOCUMENTATION_SET if not (DOCUMENTATION_DIR / path).is_file()
    ]
    if source_set_failures:
        structural_failures.extend(f"source_set:{path}" for path in source_set_failures)
    if documentation_set_failures:
        structural_failures.extend(
            f"documentation_set:{path}" for path in documentation_set_failures
        )

    all_failures = scenario_failures + negative_guard_failures + structural_failures

    return {
        "phase": PHASE_ID,
        "scenario_count": len(scenarios),
        "all_checks_passed": not all_failures,
        "passed": not all_failures,
        "failed_case_ids": sorted(
            {failure.split(":", 1)[0] for failure in scenario_failures}
        ),
        "failed_checks": all_failures,
        "scenario_cases_ok": not scenario_failures and len(scenarios) == 36,
        "negative_guards_ok": not negative_guard_failures,
        "source_set_ok": not source_set_failures,
        "documentation_set_ok": not documentation_set_failures,
        "guards": {
            "candidate_only": True,
            "runtime_execution": False,
            "provider_invocation": False,
            "camera_activation": False,
            "scheduler_execution": False,
            "action_execution": False,
            "memory_mutation": False,
            "learning_execution": False,
            "automatic_capability_acquisition": False,
            "remaining_plan_candidates_binding": False,
            "stop_sufficient_is_failure": False,
        },
    }


__all__ = ["verify_dynamic_cognitive_flow_controlled_implementation_v1"]


if __name__ == "__main__":
    result = verify_dynamic_cognitive_flow_controlled_implementation_v1()
    summary = {
        "phase": result["phase"],
        "scenario_count": result["scenario_count"],
        "all_checks_passed": result["all_checks_passed"],
        "failed_case_ids": result["failed_case_ids"],
        "failed_checks": result["failed_checks"],
        "scenario_cases_ok": result["scenario_cases_ok"],
        "negative_guards_ok": result["negative_guards_ok"],
        "source_set_ok": result["source_set_ok"],
        "documentation_set_ok": result["documentation_set_ok"],
    }
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if result["all_checks_passed"] else 1)
