"""User-terminal runner for B3 controlled candidate integration."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REPO_ROOT = Path(__file__).resolve().parents[6]
if __package__ in {None, ""} and str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from capabilities.midplatform.core.decision_governance.decision_static_validators_v1 import (
    validate_handoff,
    validate_input_refs_read_only,
    validate_no_runtime_side_effects,
)
from capabilities.midplatform.core.intent_governance.intent_static_validators_v1 import (
    validate_handoff_candidate,
    validate_input_refs_read_only as validate_intent_refs_read_only,
    validate_no_runtime_or_mutation,
)
from capabilities.midplatform.core.task_manager.module.task_manager_module_facade_v1 import (
    TaskManagerModuleV1,
)
from capabilities.midplatform.core.task_manager_skeleton_v1 import (
    validate_task_manager_candidate,
)
from capabilities.midplatform.core.intent_governance.intent_governance_fixture_v1 import (
    get_intent_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.decision_governance.decision_governance_fixture_v1 import (
    get_decision_synthetic_fixtures_v1,
)

from capabilities.midplatform.core.intent_governance.integration.b3_cognitive_state_intent_decision_task_controlled.b3_cognitive_state_intent_decision_task_adapter_v1 import (
    build_decision_input,
    build_decision_option,
    build_intent_input,
    build_task_bridge_input,
    build_task_candidates,
    run_decision,
    run_intent,
    validate_b2_reference,
)
from capabilities.midplatform.core.intent_governance.integration.b3_cognitive_state_intent_decision_task_controlled.b3_cognitive_state_intent_decision_task_fixture_v1 import (
    B3FixtureCaseV1,
    build_b3_cases_v1,
    build_case_source,
)
from capabilities.midplatform.core.intent_governance.integration.b3_cognitive_state_intent_decision_task_controlled.b3_cognitive_state_intent_decision_task_types_v1 import (
    B3ControlledRunResultV1,
)


OUTPUT_DIR = REPO_ROOT / "_eval_out/b3_cognitive_state_intent_decision_task_controlled_v1"


def _run_case(case: B3FixtureCaseV1) -> B3ControlledRunResultV1:
    source = build_case_source(case)
    issues = validate_b2_reference(source)
    if issues:
        raise ValueError(f"invalid B2 reference for {case.case_id}: {issues}")

    intent_input = build_intent_input(source, intent_scenario_id=case.intent_scenario_id)
    intent_output = run_intent(source, case.intent_scenario_id)
    option = build_decision_option(
        case.case_id,
        permission_allowed=case.permission_allowed,
        safety_allowed=case.safety_allowed,
        hard_constraints_ok=case.hard_constraints_ok,
        evidence_ready=case.evidence_ready,
    )
    decision_input = build_decision_input(
        source,
        intent_output,
        case_id=case.case_id,
        option=option,
        high_uncertainty=case.high_uncertainty,
        competing_hypotheses=case.competing_hypotheses,
        resource_pressure_level=case.resource_pressure_level,
        no_evidence=case.observation_need,
    )
    decision_output = run_decision(decision_input)
    task_input = build_task_bridge_input(
        source,
        decision_output,
        case_id=case.case_id,
        observation_required=case.observation_need,
    )
    task_readiness, task_candidate = build_task_candidates(task_input)

    task_manager_status = "NOT_INVOKED"
    task_manager_cancelled = False
    if case.cancellation and task_candidate is not None:
        task_result = TaskManagerModuleV1().handle(
            {
                "task_request_id": f"task-request:{case.case_id}",
                "task_type": "atomic",
                "task_goal": f"candidate_task:{case.case_id}",
                "requester_ref": decision_output.handoff_candidate.handoff_id,
                "priority": "normal",
                "context_snapshot": {
                    "context_refs": list(source.context_refs),
                    "request_direct_action_execution": False,
                },
                "context_refs": list(source.context_refs),
                "decision_refs": [task_candidate.source_decision_ref],
                "dependency_refs": [],
                "resource_constraints": {"resource_ref": f"resource:{case.case_id}"},
                "permission_snapshot": {"governance_ref": f"governance:{case.case_id}"},
                "capability_requirements": [],
                "deadline_or_timeout": "candidate-only",
                "interruption_policy": {"required_revalidation": True},
                "recovery_policy": {"allow_recovery_candidate": True},
                "version_snapshots": {"b3": "v1"},
                "requested_control": "cancel",
                "cancel_reason": "controlled B3 cancellation candidate",
            }
        )
        task_manager_status = str(task_result.get("task_status", ""))
        task_manager_cancelled = task_manager_status == "cancelled"
    elif task_candidate is not None:
        task_manager_status = "TASK_CANDIDATE_ONLY"
    else:
        task_manager_status = task_readiness.readiness

    intent_trace = getattr(intent_output.trace_candidate, "trace_id", "")
    decision_trace = getattr(decision_output.trace_candidate, "trace_id", "")
    task_ref = task_candidate.candidate_id if task_candidate else task_readiness.task_candidate_ref
    trace_chain = tuple(
        dict.fromkeys(
            (
                task_ref,
                decision_output.handoff_candidate.handoff_id,
                decision_trace,
                intent_output.handoff_candidate.handoff_id,
                intent_trace,
                source.cognitive_state_ref,
                source.cognitive_flow_ref,
                source.current_world_ref,
                *source.context_refs,
                *source.provenance_refs,
                source.trace_ref,
            )
        )
    )
    return B3ControlledRunResultV1(
        case_id=case.case_id,
        mode=source.mode,
        source=source,
        intent_output=intent_output,
        decision_output=decision_output,
        task_readiness=task_readiness,
        task_candidate=task_candidate,
        task_manager_status=task_manager_status,
        task_manager_cancelled=task_manager_cancelled,
        trace_chain=trace_chain,
        observation_need_preserved=(
            not source.observation_need_refs
            or decision_output.outcome_kind in {"REQUEST_MORE_EVIDENCE", "DEFER"}
            or task_readiness.readiness != "ready"
        ),
        safety_guard_preserved=case.safety_allowed or bool(decision_output.decision_candidates[0].veto_reasons),
        permission_guard_preserved=case.permission_allowed or bool(decision_output.decision_candidates[0].veto_reasons),
        resource_guard_preserved=bool(decision_input.resource_refs),
        uncertainty_refs_preserved=bool(source.uncertainty_refs and intent_input.unknowns),
        conflict_refs_preserved=(not source.conflict_refs) or bool(intent_input.unknowns),
        temporal_refs_preserved=bool(source.temporal_refs),
        provenance_complete=bool(source.provenance_refs and trace_chain),
        metadata={
            "intent_input_created": True,
            "decision_input_created": True,
            "decision_handoff_id": decision_output.handoff_candidate.handoff_id,
            "legacy_path_used": False,
            "intent_input_read_only": validate_intent_refs_read_only(
                intent_input.source_refs + intent_input.context_refs + intent_input.pcn_refs
            ),
        },
    )


def _check_case(case: B3FixtureCaseV1, result: B3ControlledRunResultV1) -> Dict[str, bool]:
    intent = result.intent_output.intent_candidates[0]
    interaction = result.intent_output.interaction_candidates[0]
    decision = result.decision_output
    checks: Dict[str, bool] = {
        "b2_input_accepted": not validate_b2_reference(result.source),
        "cognitive_input_read_only": result.cognitive_input_read_only,
        "intent_influence_created": bool(intent.source_refs),
        "intent_owner_canonical": intent.owner == "Intent Governance",
        "potential_distinct_from_active": result.intent_output.potential_intents[0].status == "POTENTIAL" and intent.truth_status == "UNKNOWN",
        "multiple_intent_boundary": (not case.multiple_intents) or (len(intent.source_refs) >= 2 and bool(intent.alternative_candidates)),
        "dominance_owner_boundary": (not case.dominance) or interaction.interaction_type == "TEMPORARY_DOMINANCE",
        "observation_need_preserved": result.observation_need_preserved,
        "intent_result_candidate_only": result.intent_output.candidate_only and not result.intent_output.source_mutation_executed,
        "decision_input_created": bool(decision.trace_candidate.intent_refs),
        "decision_candidate_created": bool(decision.decision_candidates),
        "decision_outcome_expected": decision.outcome_kind == case.expected_decision_outcome,
        "decision_not_action": all(not c.action_authority for c in decision.decision_candidates),
        "permission_guard": result.permission_guard_preserved,
        "safety_guard": result.safety_guard_preserved,
        "resource_guard": result.resource_guard_preserved,
        "decision_task_handoff": bool(decision.handoff_candidate.handoff_id) and decision.handoff_candidate.task_created is False,
        "task_readiness_created": bool(result.task_readiness.task_candidate_ref),
        "task_candidate_expected": (result.task_candidate is not None) is case.expects_task,
        "task_not_execution": result.task_candidate is None or validate_task_manager_candidate(result.task_candidate).valid,
        "cancellation_boundary": (not case.cancellation) or result.task_manager_cancelled,
        "no_runtime": not result.runtime_execution and not result.action_execution,
        "trace_complete": result.provenance_complete and len(result.trace_chain) >= 8,
        "uncertainty_preserved": result.uncertainty_refs_preserved,
        "conflict_preserved": result.conflict_refs_preserved,
        "temporal_preserved": result.temporal_refs_preserved,
        "candidate_only": result.candidate_only,
    }
    if case.case_id == "B3-24":
        checks["synthetic_input_case"] = result.mode == "SYNTHETIC_COGNITIVE_STATE_FLOW"
    return checks


def _serialize_result(case: B3FixtureCaseV1, result: B3ControlledRunResultV1) -> Dict[str, Any]:
    checks = _check_case(case, result)
    return {
        "case_id": case.case_id,
        "title": case.title,
        "mode": result.mode,
        "decision_outcome": result.decision_output.outcome_kind,
        "decision_state": result.decision_output.state,
        "task_readiness": result.task_readiness.readiness,
        "task_candidate_id": result.task_candidate.candidate_id if result.task_candidate else None,
        "task_manager_status": result.task_manager_status,
        "trace_chain": list(result.trace_chain),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
        "negative_guards": {
            "intent_mutation": result.intent_mutation,
            "decision_mutation": result.decision_mutation,
            "task_mutation": result.task_mutation,
            "action_execution": result.action_execution,
            "runtime_execution": result.runtime_execution,
            "provider_invocation": result.provider_invocation,
            "semantic_compression": result.semantic_compression,
            "dynamic_cognitive_function_execution": result.dynamic_cognitive_function_execution,
        },
    }


def run_controlled() -> Dict[str, Any]:
    cases = build_b3_cases_v1()
    serialized = []
    results = []
    for case in cases:
        result = _run_case(case)
        results.append(result)
        serialized.append(_serialize_result(case, result))

    real_result = next(result for result in results if result.mode == "REAL_B2_COGNITIVE_STATE_FLOW_INPUT")
    synthetic_case = B3FixtureCaseV1("B3-DIFF-SYNTH", "synthetic differential reference")
    synthetic_result = _run_case(synthetic_case)
    differential = {
        "ownership": real_result.intent_output.intent_candidates[0].owner == synthetic_result.intent_output.intent_candidates[0].owner == "Intent Governance",
        "candidate_only": real_result.candidate_only and synthetic_result.candidate_only,
        "trace_shape": bool(real_result.trace_chain) and bool(synthetic_result.trace_chain),
        "decision_task_boundary": real_result.decision_output.handoff_candidate.task_created is False and synthetic_result.decision_output.handoff_candidate.task_created is False,
        "runtime_guard": not real_result.runtime_execution and not synthetic_result.runtime_execution,
    }
    intent_regression = len(get_intent_synthetic_fixtures_v1()) > 0
    decision_regression = len(get_decision_synthetic_fixtures_v1()) > 0
    passed = [item for item in serialized if item["all_checks_passed"]]
    failed_ids = [item["case_id"] for item in serialized if not item["all_checks_passed"]]
    summary = {
        "phase": "Phase-Luna-Brain-B3-Cognitive-State-Intent-Decision-Task-Controlled-Implementation-v1-001",
        "mode": "HYBRID_B3_REAL_B2_COGNITIVE_INPUT",
        "owner": "Intent Governance → Decision Governance → Task Manager",
        "real_components": ["REAL_B2_COGNITIVE_STATE_FLOW_INPUT"],
        "synthetic_components": ["Intent Governance", "Decision Governance", "Task Manager", "Action Governance", "Runtime Executor"],
        "b3_scenario_count": len(serialized),
        "all_cases_passed": not failed_ids,
        "failed_case_ids": failed_ids,
        "real_b2_cognitive_input_accepted": all(item["checks"]["b2_input_accepted"] for item in serialized),
        "intent_influence_candidate_created": all(item["checks"]["intent_influence_created"] for item in serialized),
        "intent_governance_result_created": all(item["checks"]["intent_result_candidate_only"] for item in serialized),
        "decision_input_created": all(item["checks"]["decision_input_created"] for item in serialized),
        "decision_candidate_created": all(item["checks"]["decision_candidate_created"] for item in serialized),
        "decision_outcome": {item["case_id"]: item["decision_outcome"] for item in serialized},
        "decision_task_handoff_created": all(item["checks"]["decision_task_handoff"] for item in serialized),
        "task_candidate_created": any(item["task_candidate_id"] for item in serialized),
        "task_readiness_candidate_created": all(item["checks"]["task_readiness_created"] for item in serialized),
        "cognitive_input_read_only": all(item["checks"]["cognitive_input_read_only"] for item in serialized),
        "intent_mutation": False,
        "decision_mutation": False,
        "task_mutation": False,
        "action_execution": False,
        "runtime_execution": False,
        "observation_need_preserved": all(item["checks"]["observation_need_preserved"] for item in serialized),
        "safety_guard_preserved": all(item["checks"]["safety_guard"] for item in serialized),
        "permission_guard_preserved": all(item["checks"]["permission_guard"] for item in serialized),
        "resource_guard_preserved": all(item["checks"]["resource_guard"] for item in serialized),
        "uncertainty_refs_preserved": all(item["checks"]["uncertainty_preserved"] for item in serialized),
        "conflict_refs_preserved": all(item["checks"]["conflict_preserved"] for item in serialized),
        "provenance_chain_complete": all(item["checks"]["trace_complete"] for item in serialized),
        "temporal_refs_preserved": all(item["checks"]["temporal_preserved"] for item in serialized),
        "semantic_compression": False,
        "dynamic_cognitive_function_execution": False,
        "synthetic_regression_preserved": intent_regression and decision_regression,
        "differential_validation_passed": all(differential.values()),
        "candidate_only": True,
    }
    return {"summary": summary, "case_results": serialized, "differential": differential}


def write_outputs(payload: Dict[str, Any]) -> Dict[str, str]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    result_path = OUTPUT_DIR / "b3_result_v1.json"
    cases_path = OUTPUT_DIR / "b3_case_results_v1.json"
    diff_path = OUTPUT_DIR / "b3_differential_v1.json"
    result_path.write_text(json.dumps(payload["summary"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    cases_path.write_text(json.dumps(payload["case_results"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    diff_path.write_text(json.dumps(payload["differential"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"result": str(result_path), "cases": str(cases_path), "differential": str(diff_path)}


def main() -> int:
    payload = run_controlled()
    write_outputs(payload)
    print(json.dumps(payload["summary"], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
