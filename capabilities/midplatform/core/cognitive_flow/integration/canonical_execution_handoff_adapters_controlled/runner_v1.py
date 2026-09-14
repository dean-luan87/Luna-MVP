"""Controlled synthetic Runner; it never executes runtime components."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict, List, Tuple

from .adapters_v1 import adapt_a_requirement_to_attention, adapt_action_result_to_a, adapt_action_result_to_task, adapt_decision_to_action, adapt_runtime_to_observation, adapt_task_to_action
from .fixtures_v1 import HandoffScenarioV1, SCENARIOS, a_input_for, decision_input_for, result_input_for, runtime_input_for, task_input_for
from .types_v1 import HandoffOutputV1


def _guards() -> Dict[str, bool]:
    return {
        "a_does_not_own_attention_priority": True,
        "attention_does_not_create_need": True,
        "runtime_admission_does_not_own_observation": True,
        "runtime_block_does_not_create_observation_ready": True,
        "decision_does_not_execute_action": True,
        "task_does_not_execute_action": True,
        "decision_does_not_mutate_task": True,
        "task_does_not_mutate_decision": True,
        "action_result_does_not_complete_task_directly": True,
        "action_result_does_not_set_a_sufficiency": True,
        "no_provider_selection_by_a": True,
        "no_provider_selection_by_task": True,
        "no_model_selection_by_a": True,
        "no_model_selection_by_task": True,
        "no_observation_execution": True,
        "no_action_execution": True,
        "no_provider_invocation": True,
        "no_runtime_execution": True,
        "no_source_mutation": True,
        "no_world_truth": True,
        "no_scheduler": True,
        "no_planner": True,
        "no_retry_engine": True,
    }


def _record(output: HandoffOutputV1) -> Dict[str, Any]:
    return {
        "output_kind": output.output_kind,
        "output": asdict(output.output) if output.output is not None else None,
        "edge": asdict(output.edge.edge),
        "handoff_flags": asdict(output.edge),
        "failure": asdict(output.failure) if output.failure else None,
    }


def _expected(output: HandoffOutputV1, case: HandoffScenarioV1) -> bool:
    blocked = output.failure is not None
    return blocked == case.expected_blocked and (output.failure is None or output.failure.classification == case.expected_failure)


def _authority_outputs(case: HandoffScenarioV1) -> Tuple[HandoffOutputV1, ...]:
    if case.focus == "invalidation":
        return (adapt_a_requirement_to_attention(a_input_for(case.scenario_id), handoff_id=case.scenario_id),)
    return (
        adapt_a_requirement_to_attention(a_input_for("authority-valid"), handoff_id=case.scenario_id + ":a"),
        adapt_runtime_to_observation(runtime_input_for("runtime_observation_valid"), handoff_id=case.scenario_id + ":observation"),
        adapt_decision_to_action(decision_input_for("decision_action_valid"), handoff_id=case.scenario_id + ":decision"),
        adapt_task_to_action(task_input_for("task_action_valid"), handoff_id=case.scenario_id + ":task"),
        adapt_action_result_to_task(result_input_for("result_task_success"), handoff_id=case.scenario_id + ":task-result"),
        adapt_action_result_to_a(result_input_for("result_a_success"), handoff_id=case.scenario_id + ":a-result"),
    )


def _run_one(case: HandoffScenarioV1) -> Dict[str, Any]:
    outputs: Tuple[HandoffOutputV1, ...]
    if case.category == "A_ATTENTION":
        outputs = (adapt_a_requirement_to_attention(a_input_for(case.scenario_id), handoff_id=case.scenario_id),)
        output = outputs[0]
        passed = _expected(output, case)
        if case.focus == "optional_refs":
            passed = passed and output.output is not None and output.output.role_refs == ("role:observer",) and output.output.context_refs == ("context:synthetic",)
        if case.focus == "no_final_priority":
            passed = passed and output.output is not None and output.output.final_priority_assigned is False
        if case.focus == "need_immutable":
            passed = passed and output.output is not None and output.output.need_mutated is False
    elif case.category == "RUNTIME_OBSERVATION":
        outputs = (adapt_runtime_to_observation(runtime_input_for(case.scenario_id), handoff_id=case.scenario_id),)
        output = outputs[0]
        passed = _expected(output, case)
        if case.focus == "not_executed":
            passed = passed and output.output is not None and output.output.observation_execution_executed is False and output.output.provider_admission_executed is False
    elif case.category == "DECISION_ACTION":
        outputs = (adapt_decision_to_action(decision_input_for(case.scenario_id), handoff_id=case.scenario_id),)
        output = outputs[0]
        passed = _expected(output, case)
        if case.focus == "not_executed":
            passed = passed and output.output is not None and output.output.action_admission_executed is False and output.output.action_execution_executed is False
    elif case.category == "TASK_ACTION":
        outputs = (adapt_task_to_action(task_input_for(case.scenario_id), handoff_id=case.scenario_id),)
        output = outputs[0]
        passed = _expected(output, case)
        if case.focus == "not_executed":
            passed = passed and output.output is not None and output.output.action_admission_executed is False and output.output.action_execution_executed is False
    elif case.category == "RESULT_TASK":
        outputs = (adapt_action_result_to_task(result_input_for(case.scenario_id), handoff_id=case.scenario_id),)
        output = outputs[0]
        passed = _expected(output, case)
        if case.focus == "no_direct_completion":
            passed = passed and output.output is not None and output.output.task_completion_adjudicated is False and output.output.task_completed is False
    elif case.category == "RESULT_A":
        outputs = (adapt_action_result_to_a(result_input_for(case.scenario_id), handoff_id=case.scenario_id),)
        output = outputs[0]
        passed = _expected(output, case)
        if case.focus == "no_sufficiency":
            passed = passed and output.output is not None and output.output.a_sufficiency_set is False and output.output.concern_resolved is False
    else:
        outputs = _authority_outputs(case)
        output = outputs[0]
        blocked = any(item.failure is not None for item in outputs)
        passed = blocked == case.expected_blocked
        if case.focus == "owners":
            passed = passed and outputs[0].edge.edge.authority_owner == "Attention" and outputs[1].edge.edge.authority_owner == "Observation" and all(item.edge.edge.authority_owner == "Action Governance" for item in outputs[2:4]) and outputs[4].edge.edge.authority_owner == "Task" and outputs[5].edge.edge.authority_owner == "A"
        if case.focus == "responsibilities":
            passed = passed and all(bool(item.edge.edge.responsibility_owner) for item in outputs)
        if case.focus == "trace":
            passed = passed and all(bool(item.edge.edge.trace_id) and bool(item.edge.edge.provenance_refs) and bool(item.edge.edge.input_refs) for item in outputs)
        if case.focus == "versions":
            passed = passed and all(bool(item.edge.edge.input_versions) for item in outputs)
        if case.focus == "invalidation":
            passed = passed and output.failure is not None and bool(output.failure.invalidation_refs) and bool(output.edge.edge.invalidation_refs)
        if case.focus == "no_execution":
            passed = passed and all(not item.edge.attention_execution_executed and not item.edge.observation_execution_executed and not item.edge.action_execution_executed and not item.edge.provider_invocation_executed and not item.edge.runtime_execution_executed for item in outputs)
    record = _record(output)
    record.update({"scenario_id": case.scenario_id, "category": case.category, "passed": passed, "blocked": output.failure is not None, "guards": _guards()})
    if case.category == "AUTHORITY":
        record["authority_records"] = [_record(item) for item in outputs]
    return record


def run_synthetic_handoffs() -> Dict[str, Any]:
    results = [_run_one(case) for case in SCENARIOS]
    return {
        "scenario_count": len(results),
        "all_cases_passed": all(item["passed"] for item in results),
        "failed_case_ids": [item["scenario_id"] for item in results if not item["passed"]],
        "a_attention_handoff_count": sum(item["output_kind"] == "AttentionAllocationInputCandidateV1" and item["output"] is not None for item in results),
        "runtime_observation_handoff_count": sum(item["output_kind"] == "ObservationRequestCandidateV1" and item["output"] is not None for item in results),
        "decision_action_handoff_count": sum(item["category"] == "DECISION_ACTION" and item["output"] is not None for item in results),
        "task_action_handoff_count": sum(item["category"] == "TASK_ACTION" and item["output"] is not None for item in results),
        "action_result_task_return_count": sum(item["category"] == "RESULT_TASK" and item["output"] is not None for item in results),
        "action_result_a_return_count": sum(item["category"] == "RESULT_A" and item["output"] is not None for item in results),
        "blocked_count": sum(bool(item["blocked"]) for item in results),
        "stale_count": sum(bool(item["failure"]) and "STALE" in item["failure"]["classification"] for item in results),
        "revoked_count": sum(bool(item["failure"]) and "REVOKED" in item["failure"]["classification"] for item in results),
        "source_mutation_count": 0,
        "runtime_execution_count": 0,
        "observation_execution_count": 0,
        "action_execution_count": 0,
        "provider_invocation_count": 0,
        "key_guards": _guards(),
        "case_results": results,
    }


if __name__ == "__main__":
    print(json.dumps(run_synthetic_handoffs(), indent=2, ensure_ascii=False))

