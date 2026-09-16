"""Compose the verified cognition-to-Decision path with Task Manager."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
    build_decision_handoff_run_v1,
)
from capabilities.midplatform.core.task_manager.module.task_manager_module_api_v1 import (
    run_task_manager_module_v1,
)

from .decision_to_task_manager_handoff_types_v1 import (
    DECISION_OWNER,
    TASK_MANAGER_OWNER,
    DecisionToTaskManagerHandoffCandidateV1,
)


PHASE = "Phase-P1-Luna-Decision-To-Task-Manager-Controlled-Handoff-Integration-v1-001"
EXECUTION_INSTANCE_REF = "cognitive-decision-task-controlled-session"
EXPECTED_CASES = (
    "CASE_A_SUFFICIENT_STOP",
    "CASE_B_GAP_REOBSERVE_REVISE_STOP",
)
def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _proofs(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list((case.get("cognitive_case") or {}).get("cognitive_proofs") or [])


def _final_decision(case: Dict[str, Any]) -> Dict[str, Any]:
    return case.get("decision") or {}


def build_decision_task_handoff_candidate_v1(
    case: Dict[str, Any],
) -> Tuple[Optional[DecisionToTaskManagerHandoffCandidateV1], Tuple[str, ...]]:
    """Require a selected eligible Decision Candidate before Task intake."""

    decision = _final_decision(case)
    decision_output = decision.get("output") or {}
    if decision.get("all_checks_passed") is not True:
        return None, ("task_handoff_requires_valid_decision_result",)
    if case.get("validation_errors"):
        return None, ("task_handoff_rejects_invalid_cognition_or_decision",)
    selection = decision_output.get("selection_candidate") or {}
    candidates = decision_output.get("decision_candidates") or []
    selected_ref = selection.get("selected_candidate_ref")
    selected = next(
        (item for item in candidates if item.get("decision_candidate_id") == selected_ref),
        None,
    )
    if not decision or not selected_ref or selected is None:
        return None, ("task_handoff_requires_valid_selected_decision",)
    if selection.get("execution_eligibility_candidate") is not True:
        return None, ("task_handoff_requires_decision_eligibility",)
    if selected.get("eligibility_candidate") is not True:
        return None, ("task_handoff_requires_eligible_decision_candidate",)
    if selected.get("action_authority") is not False or selected.get("task_authority") is not False:
        return None, ("task_handoff_rejects_decision_with_execution_authority",)
    if decision_output.get("candidate_only") is not True:
        return None, ("task_handoff_requires_candidate_only_decision",)
    if decision_output.get("decision_output") is not False:
        return None, ("task_handoff_rejects_decision_output",)
    downstream_handoff = decision_output.get("handoff_candidate") or {}
    if (
        downstream_handoff.get("candidate_only") is not True
        or downstream_handoff.get("decision_executed") is not False
        or downstream_handoff.get("action_triggered") is not False
        or downstream_handoff.get("task_created") is not False
    ):
        return None, ("task_handoff_requires_candidate_only_decision_handoff",)

    cognitive_case = case.get("cognitive_case") or {}
    request = cognitive_case.get("brain_request") or {}
    loop = cognitive_case.get("loop_instance") or {}
    trace_ref = decision.get("decision_trace_ref")
    source_handoff = (decision_output.get("handoff_candidate") or {}).get("handoff_id")
    proof = _proofs(case)[-1] if _proofs(case) else {}
    if not trace_ref or not source_handoff or not proof.get("execution_ref"):
        return None, ("task_handoff_requires_decision_provenance",)

    provenance_refs = tuple(
        dict.fromkeys(
            (
                selected_ref,
                trace_ref,
                source_handoff,
                proof.get("execution_ref"),
                proof.get("sufficiency_ref"),
                proof.get("stop_ref"),
            )
        )
    )
    return (
        DecisionToTaskManagerHandoffCandidateV1(
            handoff_ref=f"decision-task-handoff:{case['case_id']}:{selected_ref}",
            case_id=case["case_id"],
            producer_owner_ref=DECISION_OWNER,
            consumer_owner_ref=TASK_MANAGER_OWNER,
            source_decision_handoff_ref=source_handoff,
            decision_candidate_ref=selected_ref,
            decision_trace_ref=trace_ref,
            selected_candidate_ref=selected_ref,
            option_ref=selected.get("option_id", ""),
            goal_ref=request.get("goal_ref", ""),
            intent_ref=request.get("intent_ref", ""),
            concern_ref=request.get("concern_ref", ""),
            context_ref=request.get("context_ref", ""),
            cognitive_loop_ref=loop.get("cognitive_loop_ref", ""),
            constraint_refs=tuple(
                ref.get("ref_id", "") for ref in decision.get("request", {}).get("constraint_refs", [])
            ),
            permission_refs=tuple(
                ref.get("ref_id", "") for ref in decision.get("request", {}).get("permission_refs", [])
            ),
            safety_refs=tuple(
                ref.get("ref_id", "") for ref in decision.get("request", {}).get("safety_refs", [])
            ),
            resource_refs=tuple(
                ref.get("ref_id", "") for ref in decision.get("request", {}).get("resource_refs", [])
            ),
            provenance_refs=provenance_refs,
            execution_instance_ref=(
                request.get("execution_instance_ref") or proof["execution_ref"]
            ),
        ),
        (),
    )


def _task_manager_request(handoff: DecisionToTaskManagerHandoffCandidateV1) -> Dict[str, Any]:
    task_request_id = f"task-request:{handoff.case_id}:{handoff.decision_candidate_ref}"
    cognition_execution_ref = next(
        (
            ref
            for ref in handoff.provenance_refs
            if str(ref).startswith("a-route-execution:")
        ),
        handoff.execution_instance_ref,
    )
    return {
        "task_request_id": task_request_id,
        "task_type": "atomic",
        "task_goal": f"candidate_task:{handoff.case_id}:{handoff.option_ref}",
        "requester_ref": handoff.handoff_ref,
        "trace_ref": handoff.decision_trace_ref,
        "priority": "normal",
        "context_snapshot": {
            "context_refs": [handoff.context_ref, handoff.cognitive_loop_ref],
            "request_direct_action_execution": False,
            "request_direct_model_call": False,
            "request_direct_field_state_write": False,
            "request_bypass_capability_module_api": False,
        },
        "context_refs": [handoff.context_ref, handoff.cognitive_loop_ref],
        "decision_refs": [handoff.decision_candidate_ref, handoff.decision_trace_ref],
        "dependency_refs": (),
        "dependency_snapshot": {},
        "resource_constraints": {"resource_refs": list(handoff.resource_refs)},
        "permission_snapshot": {
            "governance_ref": handoff.source_decision_handoff_ref,
            "permission_refs": list(handoff.permission_refs),
        },
        "capability_requirements": [],
        "deadline_or_timeout": "candidate-only",
        "interruption_policy": {"required_revalidation": True},
        "recovery_policy": {"allow_recovery_candidate": True},
        "version_snapshots": {
            "decision_candidate_ref": handoff.decision_candidate_ref,
            "decision_trace_ref": handoff.decision_trace_ref,
            "cognition_execution_ref": cognition_execution_ref,
        },
        "requested_control": "",
    }


def _admission_step(task_result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    steps = ((task_result.get("diagnostics") or {}).get("step_results") or ())
    return next((dict(item) for item in steps if item.get("step") == "admission"), None)


def _task_result(handoff: DecisionToTaskManagerHandoffCandidateV1) -> Dict[str, Any]:
    request = _task_manager_request(handoff)
    result = run_task_manager_module_v1(request)
    admission = _admission_step(result)
    return {
        "request": request,
        "admission": admission,
        "task_manager_owner_ref": TASK_MANAGER_OWNER,
        "task_manager_invoked": True,
        "task_manager_admitted": bool(admission and admission.get("ok") is True),
        "task_state_ref": result.get("task_id"),
        "task_state": result.get("task_status"),
        "task_trace_ref": result.get("trace_ref"),
        "task_manager_output": _jsonable(result),
        "task_candidate_ref": None,
        "controlled_task_state_ref": result.get("task_id"),
        "task_execution": False,
        "action_execution": result.get("action_execution_executed") is True,
        "model_invocation": result.get("model_call_executed") is True,
        "provider_invocation": False,
        "live_observation_execution": False,
        "field_mutation": result.get("state_mutation_executed") is True,
        "memory_mutation": result.get("fact_promotion_executed") is True,
        "experience_mutation": False,
        "learning_mutation": False,
        "world_truth_declared": False,
        "runtime_dispatch": result.get("runtime_dispatch_executed") is True,
    }


def _cycle_task_attempts(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    attempts = []
    for index, proof in enumerate(_proofs(case), start=1):
        if proof.get("sufficiency_status") != "SUFFICIENT" or not proof.get("stop_ref"):
            attempts.append({
                "cycle_index": index,
                "status": "ABSENT",
                "reason": "task_handoff_requires_valid_decision",
                "decision_present": False,
                "task_manager_invoked": False,
            })
        else:
            attempts.append({
                "cycle_index": index,
                "status": "ADMITTED",
                "reason": None,
                "decision_present": True,
                "task_manager_invoked": True,
            })
    return attempts


def _case_result(case: Dict[str, Any]) -> Dict[str, Any]:
    handoff, errors = build_decision_task_handoff_candidate_v1(case)
    task = _task_result(handoff) if handoff else None
    attempts = _cycle_task_attempts(case)
    return {
        "case_id": case.get("case_id"),
        "decision_case": case,
        "execution_mode": ((case.get("cognitive_case") or {}).get("cognitive_proofs") or [{}])[-1].get("execution_mode"),
        "cognitive_cycle_count": case.get("cognitive_cycle_count"),
        "decision_candidate_ref": handoff.decision_candidate_ref if handoff else None,
        "decision_trace_ref": handoff.decision_trace_ref if handoff else None,
        "decision_handoff_ref": handoff.source_decision_handoff_ref if handoff else None,
        "task_handoff": _jsonable(handoff) if handoff else None,
        "task_handoff_ref": handoff.handoff_ref if handoff else None,
        "task_manager": task,
        "task_manager_invocation_count": 1 if task else 0,
        "cycle_task_handoff_attempts": attempts,
        "owner_boundaries": {
            "decision_owns_decision_candidate": True,
            "task_manager_owns_task_state": bool(task),
            "task_manager_owns_decision": False,
            "brain_owns_task": False,
            "cstate_owns_task": False,
            "decision_executes_task": False,
        },
        "forbidden_behaviors": {
            "task_before_valid_decision": False,
            "decision_executes_task": False,
            "brain_owns_task": False,
            "cstate_owns_task": False,
            "task_manager_owns_decision": False,
            "action_execution": bool(task and task["action_execution"]),
            "device_control": False,
            "model_invocation": bool(task and task["model_invocation"]),
            "provider_invocation": bool(task and task["provider_invocation"]),
            "live_observation_execution": bool(task and task["live_observation_execution"]),
            "field_mutation": bool(task and task["field_mutation"]),
            "memory_mutation": bool(task and task["memory_mutation"]),
            "experience_mutation": bool(task and task["experience_mutation"]),
            "learning_mutation": bool(task and task["learning_mutation"]),
            "world_truth_declared": bool(task and task["world_truth_declared"]),
        },
        "validation_errors": list(case.get("validation_errors") or ()) + list(errors),
    }


def _negative_task_handoff_probe_v1() -> Dict[str, Any]:
    handoff, errors = build_decision_task_handoff_candidate_v1({"case_id": "NEGATIVE_TASK_WITHOUT_DECISION"})
    task_manager_invoked = False
    task_handoff_admitted = handoff is not None
    rejected = (
        handoff is None
        and bool(errors)
        and "task_handoff_requires_valid_decision_result" in errors
        and not task_manager_invoked
        and not task_handoff_admitted
    )
    return {
        "fixture": "task_handoff_without_valid_decision",
        "expected": "REJECTED",
        "rejected": rejected,
        "task_manager_invoked": task_manager_invoked,
        "task_handoff_admitted": task_handoff_admitted,
        "errors": list(errors),
    }


def build_decision_task_run_v1(
    execution_instance_ref: str = EXECUTION_INSTANCE_REF,
) -> Dict[str, Any]:
    source = build_decision_handoff_run_v1(execution_instance_ref)
    cases = [_case_result(case) for case in source["cases"]]
    return {
        "phase": PHASE,
        "source_integration_phase": source.get("phase"),
        "execution_instance_ref": execution_instance_ref,
        "case_count": len(cases),
        "cases": cases,
        "negative_test": _negative_task_handoff_probe_v1(),
        "deferred": ["action_execution", "device_control", "runtime_dispatch", "archive_integration"],
    }


__all__ = [
    "PHASE",
    "EXPECTED_CASES",
    "build_decision_task_handoff_candidate_v1",
    "build_decision_task_run_v1",
]
