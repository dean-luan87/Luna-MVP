"""Runner for the B1/B2/Dynamic/Capability/B4 controlled integration phase."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, Mapping


RUNNER_PATH = Path(__file__).resolve()


def _resolve_repo_root() -> Path:
    for candidate in (RUNNER_PATH, *RUNNER_PATH.parents):
        if (candidate / "capabilities").is_dir() and (candidate / "docs").is_dir() and (candidate / "README.md").is_file():
            return candidate
    raise RuntimeError("repository root sentinel not found")


REPO_ROOT = _resolve_repo_root()
sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.cognitive_flow.integration.real_input_dynamic_cognitive_loop_controlled.real_input_dynamic_cognitive_loop_integration_adapter_v1 import (  # noqa: E402
    build_integrated_input,
    run_integrated_case,
)
from capabilities.midplatform.core.cognitive_flow.integration.real_input_dynamic_cognitive_loop_controlled.real_input_dynamic_cognitive_loop_integration_fixture_v1 import (  # noqa: E402
    IntegratedScenarioV1,
    build_integrated_scenarios_v1,
)


PHASE = "Phase-Luna-Real-Input-Dynamic-Cognitive-Loop-Integrated-Controlled-Implementation-v1-001"


def _check(field: str, expected: Any, actual: Any) -> Dict[str, Any]:
    return {"field": field, "expected": expected, "actual": actual, "passed": expected == actual}


def _run_case(case: IntegratedScenarioV1) -> Dict[str, Any]:
    request = build_integrated_input(case)
    result = run_integrated_case(request)
    dynamic = result.dynamic_output
    checks = [
        _check("final_disposition", case.expected_final_disposition, result.final_disposition),
        _check("next_step_disposition", case.expected_next_step, result.next_step_disposition),
        _check("state_version_count", case.expected_state_count, len(dynamic.state_versions)),
        _check("dynamic_reconsideration_count", case.expected_reconsideration_count, len(dynamic.reconsiderations)),
        _check("candidate_only", True, result.guards["candidate_only"]),
        _check("plan_candidates_non_binding", True, result.guards["plan_candidates_non_binding"]),
        _check("requirement_bounded", True, result.guards["requirement_bounded"]),
        _check("scope_before_invocation", True, result.guards["scope_before_invocation"]),
        _check("no_runtime_execution", True, result.guards["no_runtime_execution"]),
        _check("no_provider_invocation", True, result.guards["no_provider_invocation"]),
    ]
    expected_requirement = case.expected_requirement_disposition
    if case.expected_requirement_disposition == "STILL_RELEVANT" and case.update_count:
        expected_requirement = "SATISFIED" if case.sufficient else "SUPERSEDED"
    actual_requirement = result.requirement_dispositions[0][1]
    checks.append(_check("requirement_disposition", expected_requirement, actual_requirement))
    if case.capability_mode == "OUT_OF_SCOPE":
        checks.extend(
            [
                _check("out_of_scope", False, result.scope_assessments[0].in_scope),
                _check("capability_gap_candidate", True, bool(result.resolutions[0].capability_gap_ref)),
                _check("alternative_need_selected", True, result.final_need_ref == f"need:{case.scenario_id}:alternative"),
            ]
        )
    if case.capability_mode in {"UNAVAILABLE", "DEGRADED"}:
        checks.append(_check("governed_capability_status", f"{case.capability_mode}_CANDIDATE", result.resolutions[0].status))
    if case.execution_outcome:
        outcome = result.capability_outcomes[0]
        checks.extend(
            [
                _check("execution_outcome", case.execution_outcome, outcome.execution_outcome),
                _check("requirement_satisfaction", case.requirement_satisfaction, outcome.requirement_satisfaction),
                _check("task_contribution", case.task_contribution, outcome.task_contribution),
            ]
        )
    if case.b4_reconsideration:
        checks.append(_check("b4_reconsideration_ref_present", True, bool(result.b4_reconsideration_refs)))
    if case.b4_reobserve:
        checks.append(_check("b4_reobserve_ref_present", True, bool(result.b4_reobserve_refs)))
    if case.scenario_id in {"I01", "I02", "I03", "I04"}:
        checks.extend(
            [
                _check("current_world_ref_present", True, bool(result.source_current_world_ref)),
                _check("b2_state_world_ref_present", True, bool(result.b2_state_world_ref)),
                _check("b2_flow_cycle_ref_present", True, bool(result.b2_flow_cycle_ref)),
                _check("current_world_read_only", True, result.guards["current_world_read_only"]),
            ]
        )
    if case.scenario_id in {"I07", "I09", "I10", "I12"}:
        checks.append(_check("remaining_candidates_non_binding", True, not request.dynamic_request.provisional_plan.binding))
    if case.scenario_id == "I08":
        checks.extend(
            [
                _check("ready_resolution", "READY_CANDIDATE", result.resolutions[0].status),
                _check("ready_invocation_candidate", True, result.invocations[0].accepted),
            ]
        )
    if case.scenario_id in {"I09", "I10", "I11", "I24"}:
        checks.extend(
            [
                _check("stop_terminates_remaining_plan", True, bool(dynamic.sufficiency_candidates[-1].terminates_remaining_plan)),
                _check("unexecuted_candidates_not_failure", True, result.guards["stop_sufficient_not_failure"]),
            ]
        )
    if case.scenario_id == "I12":
        checks.append(_check("post_sufficiency_evidence_ignored", True, bool(dynamic.ignored_evidence_update_refs)))
    if case.scenario_id in {"I13", "I14", "I15", "I16", "I27"}:
        checks.append(_check("replan_reconsideration_present", True, bool(dynamic.reconsiderations)))
    if case.scenario_id == "I15":
        checks.extend(
            [
                _check("stale_requirement_ref_present", True, bool(dynamic.stale_requirement_refs)),
                _check("stale_requirement_not_eligible", True, result.guards["stale_requirement_not_eligible"]),
            ]
        )
    if case.scenario_id == "I20":
        checks.extend(
            [
                _check("no_alternative_need_selected", None, result.final_need_ref),
                _check("no_eligible_invocation", (), dynamic.eligible_invocation_refs),
            ]
        )
    if case.scenario_id == "I28":
        checks.extend(_check(name, True, value) for name, value in result.guards.items())
    if case.scenario_id == "I27":
        checks.extend(
            [
                _check("trace_refs_reverse_linkable", True, bool(result.trace_refs)),
                _check("provenance_refs_reverse_linkable", True, bool(result.provenance_refs)),
            ]
        )
    passed = all(item["passed"] for item in checks)
    return {
        "case_id": case.scenario_id,
        "title": case.title,
        "passed": passed,
        "checks": checks,
        "final_disposition": result.final_disposition,
        "next_step_disposition": result.next_step_disposition,
        "final_state_version_ref": result.final_state_version_ref,
        "final_need_ref": result.final_need_ref,
        "requirement_dispositions": result.requirement_dispositions,
        "guards": result.guards,
    }


def build_runner_result() -> Dict[str, Any]:
    cases = [_run_case(case) for case in build_integrated_scenarios_v1()]
    failed = [case["case_id"] for case in cases if not case["passed"]]
    guard_names = (
        "candidate_only",
        "plan_candidates_non_binding",
        "stale_requirement_not_eligible",
        "stop_sufficient_not_failure",
        "capability_failure_not_task_failure",
        "no_runtime_execution",
        "no_provider_invocation",
        "no_camera_activation",
        "no_action_execution",
        "no_learning_or_memory_mutation",
    )
    key_guards = {
        name: all(case["guards"].get(name, False) for case in cases)
        for name in guard_names
    }
    return {
        "phase": PHASE,
        "scenario_count": len(cases),
        "all_cases_passed": not failed,
        "failed_case_ids": failed,
        "key_dynamic_loop_guards": key_guards,
        "cases": cases,
        "candidate_only": True,
        "real_provider_execution": False,
        "model_runtime_execution": False,
        "camera_activation": False,
        "action_execution": False,
        "learning": False,
        "memory_mutation": False,
    }


if __name__ == "__main__":
    summary = build_runner_result()
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    raise SystemExit(0 if summary["all_cases_passed"] else 1)


__all__ = ["build_runner_result"]
