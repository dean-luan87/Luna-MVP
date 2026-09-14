"""Compose the verified Task Manager result with the canonical Action Boundary."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.action_governance.action_confirmation_types_v1 import (
    ConfirmationStatusV1,
)
from capabilities.midplatform.core.action_governance.action_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.action_governance.action_dependency_types_v1 import (
    ActionDependencyCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
)
from capabilities.midplatform.core.action_governance.action_io_types_v1 import (
    ActionGovernanceInputV1,
)
from capabilities.midplatform.core.action_governance.action_precondition_types_v1 import (
    ActionPreconditionCandidateV1,
)
from capabilities.midplatform.core.action_governance.action_static_validators_v1 import (
    validate_action_candidate,
    validate_dependencies,
    validate_handoffs,
    validate_input_refs_read_only,
    validate_negative_guard_flags,
    validate_no_runtime_side_effects,
    validate_preconditions,
    validate_trace_completeness,
)
from capabilities.midplatform.core.cognitive_flow.integration.decision_to_task_manager_controlled_handoff.engine_v1 import (
    build_decision_task_run_v1,
)

from .task_to_action_handoff_types_v1 import (
    ACTION_BOUNDARY_OWNER,
    TASK_MANAGER_OWNER,
    TaskToActionHandoffCandidateV1,
)


PHASE = "Phase-P1-Luna-Task-To-Action-Boundary-Controlled-Handoff-Integration-v1-001"
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


def _proof(case: Dict[str, Any]) -> Dict[str, Any]:
    cognitive_case = (case.get("decision_case") or {}).get("cognitive_case") or {}
    proofs = cognitive_case.get("cognitive_proofs") or []
    return dict(proofs[-1]) if proofs else {}


def _unique(values: Iterable[Any]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(str(value) for value in values if value))


def _source(owner: str, ref_id: str, ref_type: str) -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _build_task_to_action_handoff(
    case: Dict[str, Any],
) -> Tuple[Optional[TaskToActionHandoffCandidateV1], Tuple[str, ...]]:
    task = case.get("task_manager") or {}
    if task.get("task_manager_admitted") is not True:
        return None, ("action_handoff_requires_admitted_task",)
    if task.get("task_state") not in {"admitted", "planned", "ready"}:
        return None, ("action_handoff_requires_eligible_task_state",)

    task_state_ref = str(task.get("controlled_task_state_ref") or "")
    task_trace_ref = str(task.get("task_trace_ref") or "")
    task_request = task.get("request") or {}
    task_decision_refs = task_request.get("decision_refs") or []
    decision_candidate_ref = str(case.get("decision_candidate_ref") or "")
    decision_trace_ref = str(case.get("decision_trace_ref") or "")
    proof = _proof(case)
    final_execution_ref = str(proof.get("execution_ref") or "")
    final_sufficiency_ref = str(proof.get("sufficiency_ref") or "")
    final_stop_ref = str(proof.get("stop_ref") or "")
    task_handoff = case.get("task_handoff") or {}

    required = (
        task_state_ref,
        task_trace_ref,
        decision_candidate_ref,
        decision_trace_ref,
        final_execution_ref,
        final_sufficiency_ref,
        final_stop_ref,
    )
    if not all(required):
        return None, ("action_handoff_requires_complete_task_and_cognition_refs",)
    if decision_candidate_ref not in task_decision_refs:
        return None, ("action_handoff_requires_task_decision_provenance",)

    cognitive_case = (case.get("decision_case") or {}).get("cognitive_case") or {}
    request = cognitive_case.get("brain_request") or {}
    option_ref = str((task.get("request") or {}).get("task_goal") or "")
    option_ref = option_ref.rsplit(":", 1)[-1] if option_ref else ""
    decision_output = ((case.get("decision_case") or {}).get("decision") or {}).get("output") or {}
    candidates = decision_output.get("decision_candidates") or []
    selected = next(
        (item for item in candidates if item.get("decision_candidate_id") == decision_candidate_ref),
        {},
    )
    option_ref = str(selected.get("option_id") or option_ref)
    if not option_ref:
        return None, ("action_handoff_requires_decision_option_ref",)

    provenance_refs = _unique(
        (
            *tuple(task_handoff.get("provenance_refs") or ()),
            final_execution_ref,
            final_sufficiency_ref,
            final_stop_ref,
            decision_candidate_ref,
            decision_trace_ref,
            task_state_ref,
            task_trace_ref,
        )
    )
    return (
        TaskToActionHandoffCandidateV1(
            handoff_ref=f"task-action-handoff:{case['case_id']}:{task_state_ref}",
            case_id=str(case["case_id"]),
            producer_owner=TASK_MANAGER_OWNER,
            consumer_owner=ACTION_BOUNDARY_OWNER,
            task_state_ref=task_state_ref,
            task_trace_ref=task_trace_ref,
            task_status=str(task.get("task_state")),
            decision_candidate_ref=decision_candidate_ref,
            decision_trace_ref=decision_trace_ref,
            goal_ref=str(request.get("goal_ref") or ""),
            intent_ref=str(request.get("intent_ref") or ""),
            concern_ref=str(request.get("concern_ref") or ""),
            context_ref=str(request.get("context_ref") or ""),
            cognitive_loop_ref=str(request.get("cognitive_loop_ref") or ""),
            option_ref=option_ref,
            final_cognition_execution_ref=final_execution_ref,
            final_sufficiency_ref=final_sufficiency_ref,
            final_stop_ref=final_stop_ref,
            permission_refs=_unique(
                ref.get("ref_id", "")
                for ref in ((case.get("decision_case") or {}).get("decision") or {}).get("request", {}).get("permission_refs", [])
            ),
            safety_refs=_unique(
                ref.get("ref_id", "")
                for ref in ((case.get("decision_case") or {}).get("decision") or {}).get("request", {}).get("safety_refs", [])
            ),
            resource_refs=_unique(
                ref.get("ref_id", "")
                for ref in ((case.get("decision_case") or {}).get("decision") or {}).get("request", {}).get("resource_refs", [])
            ),
            provenance_refs=provenance_refs,
        ),
        (),
    )


def _action_request(handoff: TaskToActionHandoffCandidateV1) -> Dict[str, Any]:
    precondition = ActionPreconditionCandidateV1(
        precondition_id=f"precondition:{handoff.handoff_ref}:task-admitted",
        domain="task_admission",
        status="satisfied",
        required=True,
        provenance_refs=(handoff.task_state_ref, handoff.task_trace_ref),
    )
    dependency = ActionDependencyCandidateV1(
        dependency_id=f"dependency:{handoff.handoff_ref}:decision-task-chain",
        dependency_type="decision_task_chain",
        status="satisfied",
        blocking=True,
        provenance_refs=(handoff.decision_candidate_ref, handoff.task_trace_ref),
    )
    return {
        "scenario_id": handoff.case_id,
        "selected_decision_refs": (_source("Decision Governance", handoff.decision_candidate_ref, "DECISION_CANDIDATE"),),
        "intent_refs": (_source("Intent Governance", handoff.intent_ref, "INTENT"),),
        "causal_refs": tuple(
            _source("Cognitive State Formation Governance", ref, "COGNITIVE_PROVENANCE")
            for ref in (
                handoff.final_cognition_execution_ref,
                handoff.final_sufficiency_ref,
                handoff.final_stop_ref,
            )
        ),
        "target_refs": (_source("Decision Governance", handoff.option_ref, "DECISION_OPTION"),),
        "context_refs": (
            _source("Context Governance", handoff.context_ref, "CONTEXT"),
            _source("Cognitive Flow Governance", handoff.cognitive_loop_ref, "COGNITIVE_LOOP"),
        ),
        "field_refs": (),
        "permission_refs": tuple(_source("Permission Governance", ref, "PERMISSION") for ref in handoff.permission_refs),
        "safety_refs": tuple(_source("Safety Governance", ref, "SAFETY") for ref in handoff.safety_refs),
        "confirmation_refs": (),
        "preconditions": (precondition,),
        "dependencies": (dependency,),
        "resource_refs": tuple(_source("Resource Governance", ref, "RESOURCE") for ref in handoff.resource_refs),
        "resource_state": "available",
        "permission_valid": True,
        "safety_valid": True,
        "confirmation": ConfirmationStatusV1(
            state="not_required",
            is_stale=False,
            is_fabricated=False,
            strong_confirmation=False,
        ),
        "reversibility": "reversible",
        "target_valid": True,
        "cancellation_requested": False,
        "rollback_required": False,
        "failure_result": None,
        "revision_requested": False,
        "prefer_eligible_state": False,
        "task_reference_context_refs": (
            _source("Task Manager", handoff.task_state_ref, "TASK_STATE"),
            _source("Task Manager", handoff.task_trace_ref, "TASK_TRACE"),
        ),
        "synthetic_only": True,
        "candidate_only": True,
    }


def _action_result(handoff: TaskToActionHandoffCandidateV1) -> Dict[str, Any]:
    request = _action_request(handoff)
    output = ActionGovernanceEngineV1().run_case(ActionGovernanceInputV1(**request))
    all_refs = tuple(
        ref
        for key in (
            "selected_decision_refs",
            "intent_refs",
            "causal_refs",
            "target_refs",
            "context_refs",
            "field_refs",
            "permission_refs",
            "safety_refs",
            "confirmation_refs",
            "resource_refs",
            "task_reference_context_refs",
        )
        for ref in request[key]
    )
    checks = {
        "input_refs_read_only": validate_input_refs_read_only(all_refs),
        "action_candidate_valid": validate_action_candidate(output.action_candidate),
        "preconditions_valid": validate_preconditions(output.precondition_results),
        "dependencies_valid": validate_dependencies(output.dependency_results),
        "trace_complete": validate_trace_completeness(output),
        "handoffs_valid": validate_handoffs(output),
        "negative_guard_flags": validate_negative_guard_flags(),
        "no_runtime_side_effects": validate_no_runtime_side_effects(output),
        "candidate_ready": output.action_candidate.action_state == "READY_CANDIDATE"
        and output.readiness.state == "candidate_ready",
    }
    transition_ref = output.transitions[0].provenance_ref if output.transitions else None
    admission_ok = all(checks.values())
    return {
        "request": _jsonable(request),
        "action_boundary_invoked": True,
        "action_boundary_admitted": admission_ok,
        "action_boundary_admission_ref": transition_ref,
        "action_boundary_admission_status": "CANDIDATE_ADMITTED" if admission_ok else "REJECTED",
        "candidate_only": output.candidate_only,
        "action_candidate_ref": output.action_candidate.action_candidate_id,
        "action_state": output.action_candidate.action_state,
        "action_readiness": output.readiness.state,
        "action_trace_ref": output.trace_candidate.trace_id,
        "runtime_handoff_ref": output.runtime_handoff.handoff_id,
        "action_candidate": _jsonable(output.action_candidate),
        "action_trace": _jsonable(output.trace_candidate),
        "action_transitions": _jsonable(output.transitions),
        "runtime_handoff": _jsonable(output.runtime_handoff),
        "checks": checks,
        "real_action_execution": output.action_executed,
        "device_control": output.device_control_executed,
        "runtime_dispatch": output.runtime_executed,
        "model_invocation": False,
        "provider_invocation": False,
        "live_observation_execution": False,
        "field_mutation": output.database_write_executed,
        "memory_mutation": False,
        "experience_mutation": False,
        "learning_mutation": False,
        "world_truth_declared": False,
    }


def _case_result(case: Dict[str, Any]) -> Dict[str, Any]:
    handoff, errors = _build_task_to_action_handoff(case)
    action = _action_result(handoff) if handoff else None
    task = case.get("task_manager") or {}
    cycle_attempts = []
    for attempt in case.get("cycle_task_handoff_attempts") or []:
        cycle_attempts.append(
            {
                "cycle_index": attempt.get("cycle_index"),
                "status": "ABSENT" if attempt.get("status") == "ABSENT" else "ADMITTED",
                "decision_present": attempt.get("decision_present") is True,
                "task_present": attempt.get("task_manager_invoked") is True,
                "task_manager_invoked": attempt.get("task_manager_invoked") is True,
                "action_boundary_invoked": False if attempt.get("status") == "ABSENT" else bool(action),
            }
        )
    return {
        "case_id": case.get("case_id"),
        "task_case": case,
        "execution_mode": case.get("execution_mode"),
        "cognitive_cycle_count": case.get("cognitive_cycle_count"),
        "task_manager_admitted": task.get("task_manager_admitted") is True,
        "task_state_ref": task.get("controlled_task_state_ref"),
        "task_trace_ref": task.get("task_trace_ref"),
        "task_status": task.get("task_state"),
        "task_to_action_handoff": _jsonable(handoff) if handoff else None,
        "task_to_action_handoff_ref": handoff.handoff_ref if handoff else None,
        "action_boundary": action,
        "cycle_action_handoff_attempts": cycle_attempts,
        "validation_errors": list(case.get("validation_errors") or ()) + list(errors),
        "forbidden_behaviors": {
            "action_before_valid_task": False,
            "task_manager_executes_action": False,
            "decision_executes_action": False,
            "brain_executes_action": False,
            "cstate_executes_action": False,
            "real_action_execution": bool(action and action["real_action_execution"]),
            "device_control": bool(action and action["device_control"]),
            "runtime_dispatch": bool(action and action["runtime_dispatch"]),
            "model_invocation": bool(action and action["model_invocation"]),
            "provider_invocation": bool(action and action["provider_invocation"]),
            "live_observation_execution": bool(action and action["live_observation_execution"]),
            "field_mutation": bool(action and action["field_mutation"]),
            "memory_mutation": bool(action and action["memory_mutation"]),
            "experience_mutation": bool(action and action["experience_mutation"]),
            "learning_mutation": bool(action and action["learning_mutation"]),
            "world_truth_declared": bool(action and action["world_truth_declared"]),
        },
    }


def _negative_action_handoff_probe_v1() -> Dict[str, Any]:
    handoff, errors = _build_task_to_action_handoff(
        {"case_id": "NEGATIVE_ACTION_WITHOUT_TASK", "task_manager": None}
    )
    action_boundary_invoked = False
    rejected = (
        handoff is None
        and "action_handoff_requires_admitted_task" in errors
        and not action_boundary_invoked
    )
    return {
        "fixture": "action_handoff_without_valid_task",
        "expected": "REJECTED",
        "rejected": rejected,
        "action_boundary_invoked": action_boundary_invoked,
        "errors": list(errors),
    }


def build_task_to_action_run_v1() -> Dict[str, Any]:
    source = build_decision_task_run_v1()
    cases = [_case_result(case) for case in source["cases"]]
    return {
        "phase": PHASE,
        "source_integration_phase": source.get("phase"),
        "execution_instance_ref": source.get("execution_instance_ref"),
        "case_count": len(cases),
        "cases": cases,
        "negative_test": _negative_action_handoff_probe_v1(),
        "deferred": ["real_action_execution", "device_control", "runtime_dispatch"],
    }


__all__ = ["PHASE", "EXPECTED_CASES", "build_task_to_action_run_v1"]
