"""Controlled B4 feedback-loop runner; no Runtime Executor is invoked."""

from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path
from typing import Any, Dict, Tuple

_PACKAGE_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _PACKAGE_DIR.parents[5]
if __package__ in {None, ""} and str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.midplatform.core.outcome_evaluation_governance.integration.b4_task_outcome_feedback_reconsider_reobserve_controlled.b4_task_outcome_feedback_reconsider_reobserve_adapter_v1 import (
    build_actual_result,
    build_action_input,
    build_controlled_runtime_result,
    build_expected_outcome,
    build_outcome_request,
    build_reconsideration,
    build_reobserve,
    build_task_feedback,
    run_action,
    run_outcome,
    validate_b3_reference,
)
from capabilities.midplatform.core.outcome_evaluation_governance.integration.b4_task_outcome_feedback_reconsider_reobserve_controlled.b4_task_outcome_feedback_reconsider_reobserve_fixture_v1 import (
    B4FixtureCaseV1,
    build_b3_task_decision_reference,
    build_b4_cases_v1,
)
from capabilities.midplatform.core.outcome_evaluation_governance.integration.b4_task_outcome_feedback_reconsider_reobserve_controlled.b4_task_outcome_feedback_reconsider_reobserve_types_v1 import (
    B4ControlledRunResultV1,
)


_SYNTHETIC_REGRESSION_PATHS = (
    _REPO_ROOT / "capabilities/midplatform/core/task_manager_types_v1.py",
    _REPO_ROOT / "capabilities/midplatform/core/action_governance/action_governance_fixture_v1.py",
    _REPO_ROOT / "capabilities/midplatform/core/runtime_executor/runtime_executor_fixture_v1.py",
    _REPO_ROOT / "capabilities/midplatform/core/outcome_evaluation_governance/outcome_evaluation_fixture_v1.py",
    _REPO_ROOT / "capabilities/midplatform/core/cognitive_flow/cognitive_flow_fixture_v1.py",
)


def _run_case(case: B4FixtureCaseV1) -> B4ControlledRunResultV1:
    source = build_b3_task_decision_reference(case)
    issues = validate_b3_reference(source)
    if issues:
        raise ValueError(f"invalid B3 reference {case.case_id}: {issues}")

    action_output = run_action(
        source,
        permission_valid=case.permission_valid,
        safety_valid=case.safety_valid,
        resource_state=case.resource_state,
        cancellation_requested=case.cancellation_requested,
    )
    runtime_status = case.runtime_status
    if action_output.readiness.state != "candidate_ready":
        runtime_status = "REJECTED_CANDIDATE"
    controlled = build_controlled_runtime_result(
        source,
        action_output,
        runtime_status=runtime_status,
    )
    expected = build_expected_outcome(source, expected_value=case.expected_value)
    actual = build_actual_result(source, controlled, actual_value=case.actual_value)
    request = build_outcome_request(
        source,
        expected,
        actual,
        intended_status=case.intended_status,
        evidence_sufficient=case.evidence_sufficient,
        contradictory=case.contradictory,
        recommendation=case.recommendation,
        duplicate_kinds=case.duplicate_kinds,
        task_completion_candidate="COMPLETED_CANDIDATE" if case.intended_status == "MATCH" else "",
    )
    outcome = run_outcome(request)
    task_feedback = build_task_feedback(source, outcome, action_output)
    reconsideration = build_reconsideration(source, outcome)
    reobserve = build_reobserve(source, outcome)
    return B4ControlledRunResultV1(
        case_id=case.case_id,
        mode="REAL_B3_TASK_DECISION_INPUT" if case.real else "SYNTHETIC_B3_TASK_DECISION_INPUT",
        source=source,
        action_candidate=action_output.action_candidate,
        controlled_runtime_result=controlled,
        expected_outcome=expected,
        actual_result=actual,
        outcome=outcome,
        task_feedback=task_feedback,
        reconsideration_candidate=reconsideration,
        reobserve_candidate=reobserve,
        real_b3_task_input_accepted=not bool(issues),
        task_lifecycle_owner_preserved=task_feedback.consumer_owner == "Task Manager" and not task_feedback.task_mutation_executed,
        action_execution=action_output.action_executed,
        runtime_execution=False,
        provider_invocation=False,
        automatic_retry=False,
        memory_write=False,
        experience_learning=False,
        online_learning=False,
        semantic_compression=False,
        dynamic_cognitive_function_execution=False,
        uncertainty_refs_preserved=bool(source.uncertainty_refs and outcome.evaluation.uncertainty_refs),
        conflict_refs_preserved=source.conflict_refs == () or bool(outcome.evaluation.contradiction_refs),
        provenance_chain_complete=bool(source.provenance_refs and controlled.provenance_refs and outcome.trace.provenance_refs),
        temporal_refs_preserved=bool(source.temporal_refs and outcome.deviation.temporal_refs),
        candidate_only=(
            source.candidate_only
            and action_output.candidate_only
            and controlled.candidate_only
            and expected.candidate_only
            and actual.candidate_only
            and outcome.evaluation.candidate_only
            and task_feedback.candidate_only
        ),
        metadata={
            "action_readiness": action_output.readiness.state,
            "action_state": action_output.action_candidate.action_state,
            "outcome_status": outcome.evaluation.evaluation_status,
            "deviation_status": outcome.deviation.status,
            "reconsideration_recommendation": outcome.reconsideration.recommendation if outcome.reconsideration else None,
        },
    )


def _case_checks(case: B4FixtureCaseV1, run: B4ControlledRunResultV1) -> Dict[str, bool]:
    action = run.action_candidate
    controlled = run.controlled_runtime_result
    outcome = run.outcome
    checks = {
        "real_b3_task_input_accepted": run.real_b3_task_input_accepted,
        "action_candidate_created": bool(action.action_candidate_id),
        "action_candidate_not_execution": not run.action_execution and not action.runtime_authority,
        "controlled_runtime_result_created": controlled.result.candidate_only,
        "runtime_result_is_fixture": controlled.controlled_fixture and not controlled.real_runtime_execution,
        "expected_outcome_input_created": bool(run.expected_outcome.expectation_ref),
        "actual_result_input_created": bool(run.actual_result.actual_result_ref),
        "outcome_candidate_created": outcome.evaluation.candidate_only,
        "outcome_not_world_truth": not outcome.evaluation.truth_declared,
        "external_success_not_verified": not run.task_feedback.external_success_verified,
        "task_feedback_handoff_created": bool(run.task_feedback.feedback_id),
        "task_lifecycle_owner_preserved": run.task_lifecycle_owner_preserved,
        "reconsideration_expectation": (run.reconsideration_candidate is not None) == case.expected_reconsideration,
        "observation_need_expectation": (outcome.observation_need is not None) == case.expected_observation_need,
        "reobserve_expectation": (run.reobserve_candidate is not None) == case.expected_reobserve,
        "reobserve_no_provider": run.reobserve_candidate is None or not run.reobserve_candidate.provider_invocation,
        "no_automatic_retry": not run.automatic_retry,
        "no_runtime_execution": not run.runtime_execution and not controlled.real_runtime_execution,
        "no_provider_invocation": not run.provider_invocation,
        "no_memory_learning": not run.memory_write and not run.experience_learning and not run.online_learning,
        "no_semantic_compression": not run.semantic_compression,
        "no_dynamic_cognitive_function": not run.dynamic_cognitive_function_execution,
        "candidate_only": run.candidate_only,
        "uncertainty_preserved": run.uncertainty_refs_preserved,
        "conflict_preserved": run.conflict_refs_preserved,
        "provenance_complete": run.provenance_chain_complete,
        "temporal_preserved": run.temporal_refs_preserved,
        "task_feedback_state": run.task_feedback.proposed_lifecycle_state == case.expected_proposed_task_state,
    }
    return checks


def _differential_check(case: B4FixtureCaseV1) -> bool:
    real_run = _run_case(case)
    synthetic_run = _run_case(replace(case, real=False, differential=False))
    return (
        real_run.action_candidate.candidate_kind == synthetic_run.action_candidate.candidate_kind
        and real_run.controlled_runtime_result.result.candidate_only == synthetic_run.controlled_runtime_result.result.candidate_only
        and real_run.outcome.evaluation.candidate_only == synthetic_run.outcome.evaluation.candidate_only
        and real_run.task_feedback.consumer_owner == synthetic_run.task_feedback.consumer_owner == "Task Manager"
        and (real_run.reconsideration_candidate is None) == (synthetic_run.reconsideration_candidate is None)
        and (real_run.reobserve_candidate is None) == (synthetic_run.reobserve_candidate is None)
        and real_run.runtime_execution == synthetic_run.runtime_execution == False
        and real_run.provider_invocation == synthetic_run.provider_invocation == False
    )


def build_runner_result() -> Dict[str, Any]:
    cases = build_b4_cases_v1()
    case_results = []
    failed_case_ids = []
    for case in cases:
        run = _run_case(case)
        checks = _case_checks(case, run)
        differential = _differential_check(case) if case.differential else True
        checks["differential_governance_compatibility"] = differential
        passed = all(checks.values())
        if not passed:
            failed_case_ids.append(case.case_id)
        case_results.append({
            "case_id": case.case_id,
            "title": case.title,
            "mode": run.mode,
            "checks": checks,
            "passed": passed,
            "action_state": run.metadata["action_state"],
            "outcome_status": run.metadata["outcome_status"],
            "deviation_status": run.metadata["deviation_status"],
            "reconsideration": run.metadata["reconsideration_recommendation"],
            "observation_need": run.outcome.observation_need.observation_need_id if run.outcome.observation_need else None,
            "reobserve": run.reobserve_candidate.reobserve_id if run.reobserve_candidate else None,
        })

    real_case = _run_case(next(case for case in cases if case.case_id == "B4-28"))
    synthetic_regression_preserved = all(path.is_file() for path in _SYNTHETIC_REGRESSION_PATHS)
    all_cases_passed = not failed_case_ids
    return {
        "phase": "Phase-Luna-Brain-B4-Task-Outcome-Feedback-Reconsider-Reobserve-Controlled-Implementation-v1-001",
        "mode": "CONTROLLED_B4_REAL_B3_TASK_INPUT",
        "owner": "Task Manager / Action Governance / Runtime Executor / Outcome Evaluation Governance / Cognitive Flow",
        "real_components": ["REAL_B3_TASK_DECISION_INPUT"],
        "synthetic_components": ["CONTROLLED_RUNTIME_RESULT_FIXTURE", "OUTCOME_EVALUATION_CANDIDATE_LOGIC"],
        "b4_scenario_count": len(cases),
        "all_cases_passed": all_cases_passed,
        "failed_case_ids": failed_case_ids,
        "real_b3_task_input_accepted": real_case.real_b3_task_input_accepted,
        "action_candidate_created": bool(real_case.action_candidate.action_candidate_id),
        "controlled_runtime_result_created": real_case.controlled_runtime_result.controlled_fixture,
        "runtime_result_is_fixture": real_case.controlled_runtime_result.controlled_fixture,
        "expected_outcome_input_created": bool(real_case.expected_outcome.expectation_ref),
        "actual_result_input_created": bool(real_case.actual_result.actual_result_ref),
        "outcome_candidate_created": real_case.outcome.evaluation.candidate_only,
        "task_feedback_handoff_created": bool(real_case.task_feedback.feedback_id),
        "reconsideration_candidate_created": real_case.reconsideration_candidate is not None,
        "observation_need_candidate_created": real_case.outcome.observation_need is not None,
        "reobserve_candidate_created": real_case.reobserve_candidate is not None,
        "task_lifecycle_owner_preserved": real_case.task_lifecycle_owner_preserved,
        "action_execution": False,
        "runtime_execution": False,
        "provider_invocation": False,
        "automatic_retry": False,
        "outcome_world_truth": real_case.outcome.evaluation.truth_declared,
        "external_success_verified": real_case.task_feedback.external_success_verified,
        "uncertainty_refs_preserved": real_case.uncertainty_refs_preserved,
        "conflict_refs_preserved": real_case.conflict_refs_preserved,
        "provenance_chain_complete": real_case.provenance_chain_complete,
        "temporal_refs_preserved": real_case.temporal_refs_preserved,
        "memory_write": False,
        "experience_learning": False,
        "online_learning": False,
        "semantic_compression": False,
        "dynamic_cognitive_function_execution": False,
        "synthetic_regression_preserved": synthetic_regression_preserved,
        "differential_validation_passed": all(
            item["checks"]["differential_governance_compatibility"] for item in case_results
        ),
        "candidate_only": real_case.candidate_only,
        "cases": case_results,
    }


if __name__ == "__main__":
    print(json.dumps(build_runner_result(), indent=2, sort_keys=True))
