"""Compose verified Task-to-Action output with Action safety closure.

This module stops at the candidate-only Runtime Executor handoff. It does not
invoke Runtime Executor, an adapter, a scheduler, a device, or an external
side effect.
"""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.action_governance.action_governance_engine_v1 import (
    ActionGovernanceEngineV1,
)
from capabilities.midplatform.core.action_governance.action_governance_fixture_v1 import (
    get_action_synthetic_fixtures_v1,
)
from capabilities.midplatform.core.action_governance.action_resource_types_v1 import (
    RESOURCE_AVAILABLE,
    normalize_resource_state,
)
from capabilities.midplatform.core.cognitive_flow.integration.task_to_action_boundary_controlled_handoff.engine_v1 import (
    build_task_to_action_run_v1,
)


PHASE = "Phase-P1-Luna-Action-Admission-Safety-And-Execution-Boundary-Closure-v1-001"
EXPECTED_CASES = (
    "CASE_A_SUFFICIENT_STOP",
    "CASE_B_GAP_REOBSERVE_REVISE_STOP",
)
NEGATIVE_CASES = (
    "action_without_permission",
    "action_fails_safety",
)


def _jsonable(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _ref_ids(items: Iterable[Any]) -> Tuple[str, ...]:
    values = []
    for item in items:
        if isinstance(item, dict) and item.get("ref_id"):
            values.append(str(item["ref_id"]))
    return tuple(dict.fromkeys(values))


def _final_cognition_refs(source_case: Dict[str, Any]) -> Dict[str, Optional[str]]:
    cognitive_case = (source_case.get("task_case") or {}).get("decision_case") or {}
    cognitive_case = cognitive_case.get("cognitive_case") or {}
    proofs = cognitive_case.get("cognitive_proofs") or ()
    proof = proofs[-1] if proofs else {}
    return {
        "execution_ref": str(proof.get("execution_ref")) if proof.get("execution_ref") else None,
        "sufficiency_ref": str(proof.get("sufficiency_ref")) if proof.get("sufficiency_ref") else None,
        "stop_ref": str(proof.get("stop_ref")) if proof.get("stop_ref") else None,
    }


def _positive_case(source_case: Dict[str, Any]) -> Dict[str, Any]:
    action = source_case.get("action_boundary") or {}
    task_case = source_case.get("task_case") or {}
    request = action.get("request") or {}
    candidate = action.get("action_candidate") or {}
    trace = action.get("action_trace") or {}
    runtime_handoff = action.get("runtime_handoff") or {}
    resource_state = normalize_resource_state(request.get("resource_state"))
    runtime_handoff_ref = str(
        runtime_handoff.get("handoff_id") or action.get("runtime_handoff_ref") or ""
    )
    execution_eligible = (
        action.get("action_boundary_admitted") is True
        and action.get("action_state") == "READY_CANDIDATE"
        and action.get("action_readiness") == "candidate_ready"
        and runtime_handoff.get("execution_readiness") == "candidate_ready"
        and resource_state == RESOURCE_AVAILABLE
    )

    # Action Governance exposes readiness as a candidate without a separate
    # readiness identifier. The canonical Runtime Executor handoff ID is the
    # only available execution-eligibility reference and is carried unchanged.
    eligibility_ref: Optional[str] = runtime_handoff_ref or None
    validation_errors = list(source_case.get("validation_errors") or ())
    preconditions = request.get("preconditions") or []
    dependencies = request.get("dependencies") or []
    cognition_refs = _final_cognition_refs(source_case)
    decision_candidate_ref = task_case.get("decision_candidate_ref")
    decision_trace_ref = task_case.get("decision_trace_ref")
    return {
        "case_id": source_case.get("case_id"),
        "source_case": source_case,
        "execution_mode": source_case.get("execution_mode"),
        "cognitive_cycle_count": source_case.get("cognitive_cycle_count"),
        "task_manager_admitted": source_case.get("task_manager_admitted") is True,
        "task_state_ref": source_case.get("task_state_ref"),
        "task_trace_ref": source_case.get("task_trace_ref"),
        "task_status": source_case.get("task_status"),
        "task_to_action_handoff": source_case.get("task_to_action_handoff"),
        "task_to_action_handoff_ref": source_case.get("task_to_action_handoff_ref"),
        "action_handoff_ref": source_case.get("task_to_action_handoff_ref"),
        "action_boundary": action,
        "action_boundary_admission_ref": action.get("action_boundary_admission_ref"),
        "action_boundary_admission_status": action.get("action_boundary_admission_status"),
        "action_candidate_ref": action.get("action_candidate_ref"),
        "action_trace_ref": action.get("action_trace_ref"),
        "permission_refs": list(_ref_ids(request.get("permission_refs") or ())),
        "safety_refs": list(_ref_ids(request.get("safety_refs") or ())),
        "constraint_refs": [
            *(item.get("precondition_id") for item in preconditions),
            *(item.get("dependency_id") for item in dependencies),
        ],
        "risk_refs": [],
        "permission_validation": {
            "status": "VALIDATED" if request.get("permission_valid") is True else "FAILED",
            "valid": request.get("permission_valid") is True,
            "permission_refs": list(_ref_ids(request.get("permission_refs") or ())),
        },
        "safety_validation": {
            "status": "VALIDATED" if request.get("safety_valid") is True else "FAILED",
            "valid": request.get("safety_valid") is True,
            "safety_refs": list(_ref_ids(request.get("safety_refs") or ())),
        },
        "constraint_validation": {
            "status": "VALIDATED"
            if all(item.get("status") == "satisfied" for item in preconditions)
            and all(item.get("status") == "satisfied" for item in dependencies)
            and request.get("resource_state") == "available"
            else "FAILED",
            "precondition_refs": [item.get("precondition_id") for item in preconditions],
            "dependency_refs": [item.get("dependency_id") for item in dependencies],
            "resource_refs": list(_ref_ids(request.get("resource_refs") or ())),
            "resource_state": resource_state,
        },
        "risk_validation": {
            "status": "NOT_INSTRUMENTED",
            "refs": [],
            "reason": "Action Governance has no separately named risk-ref field in the reused canonical input contract; safety_valid remains the canonical safety gate.",
        },
        "execution_eligibility": {
            "status": "ELIGIBLE_CANDIDATE" if execution_eligible else "NOT_EXECUTION_ELIGIBLE",
            "state": action.get("action_readiness"),
            "ref": eligibility_ref,
            "ref_source": "canonical_action_runtime_handoff_id",
            "candidate_only": True,
            "executed": False,
        },
        "execution_eligibility_ref": eligibility_ref,
        "runtime_executor_handoff": runtime_handoff,
        "runtime_executor_handoff_ref": runtime_handoff_ref or None,
        "runtime_executor_invoked": False,
        "final_cognition_execution_ref": cognition_refs["execution_ref"],
        "final_sufficiency_ref": cognition_refs["sufficiency_ref"],
        "final_stop_ref": cognition_refs["stop_ref"],
        "decision_candidate_ref": decision_candidate_ref,
        "decision_trace_ref": decision_trace_ref,
        "traceability": {
            "final_cognition_execution_ref": cognition_refs["execution_ref"],
            "final_sufficiency_ref": cognition_refs["sufficiency_ref"],
            "final_stop_ref": cognition_refs["stop_ref"],
            "decision_candidate_ref": decision_candidate_ref,
            "decision_trace_ref": decision_trace_ref,
            "task_state_ref": source_case.get("task_state_ref"),
            "task_trace_ref": source_case.get("task_trace_ref"),
            "action_candidate_ref": candidate.get("action_candidate_id"),
            "action_trace_ref": trace.get("trace_id"),
            "runtime_executor_handoff_ref": runtime_handoff_ref or None,
        },
        "validation_errors": validation_errors,
        "forbidden_behaviors": {
            "real_action_execution": action.get("real_action_execution") is True,
            "device_control": action.get("device_control") is True,
            "runtime_dispatch_executed": action.get("runtime_dispatch") is True,
            "task_manager_executes_action": False,
            "decision_executes_action": False,
            "brain_executes_action": False,
            "cstate_executes_action": False,
            "model_invocation": action.get("model_invocation") is True,
            "provider_invocation": action.get("provider_invocation") is True,
            "live_observation_execution": action.get("live_observation_execution") is True,
            "field_mutation": action.get("field_mutation") is True,
            "memory_mutation": action.get("memory_mutation") is True,
            "experience_mutation": action.get("experience_mutation") is True,
            "learning_mutation": action.get("learning_mutation") is True,
            "world_truth_declared": action.get("world_truth_declared") is True,
        },
    }


def _negative_case(fixture_id: str, public_id: str) -> Dict[str, Any]:
    fixture = next(item for item in get_action_synthetic_fixtures_v1() if item.case_id == fixture_id)
    output = ActionGovernanceEngineV1().run_case(fixture.request)
    candidate_ready = (
        output.action_candidate.action_state == "READY_CANDIDATE"
        and output.readiness.state == "candidate_ready"
    )
    runtime_handoff = _jsonable(output.runtime_handoff)
    runtime_handoff_ref = output.runtime_handoff.handoff_id
    constraints_valid = (
        all(item.status == "satisfied" for item in fixture.request.preconditions)
        and all(item.status == "satisfied" for item in fixture.request.dependencies)
        and fixture.request.resource_state == "available"
    )
    rejected = (
        fixture.request.permission_valid is False
        or fixture.request.safety_valid is False
    ) and not candidate_ready
    return {
        "fixture": public_id,
        "canonical_fixture_id": fixture_id,
        "expected": "REJECTED / NOT_EXECUTION_ELIGIBLE",
        "rejected": rejected,
        "action_boundary_invoked": True,
        "action_boundary_admitted": False,
        "action_boundary_admission_ref": None,
        "action_boundary_admission_status": "REJECTED",
        "request": _jsonable(fixture.request),
        "action_state": output.action_candidate.action_state,
        "action_readiness": output.readiness.state,
        "action_candidate_ref": output.action_candidate.action_candidate_id,
        "action_trace_ref": output.trace_candidate.trace_id,
        "action_handoff_ref": None,
        "permission_refs": [ref.ref_id for ref in fixture.request.permission_refs],
        "safety_refs": [ref.ref_id for ref in fixture.request.safety_refs],
        "constraint_refs": [
            *(item.precondition_id for item in fixture.request.preconditions),
            *(item.dependency_id for item in fixture.request.dependencies),
        ],
        "risk_refs": [],
        "permission_validation": {
            "valid": fixture.request.permission_valid,
            "permission_refs": [ref.ref_id for ref in fixture.request.permission_refs],
        },
        "safety_validation": {
            "valid": fixture.request.safety_valid,
            "safety_refs": [ref.ref_id for ref in fixture.request.safety_refs],
        },
        "constraint_validation": {
            "status": "VALIDATED" if constraints_valid else "FAILED",
            "precondition_refs": [item.precondition_id for item in fixture.request.preconditions],
            "dependency_refs": [item.dependency_id for item in fixture.request.dependencies],
            "resource_refs": [ref.ref_id for ref in fixture.request.resource_refs],
            "resource_state": fixture.request.resource_state,
        },
        "risk_validation": {
            "status": "NOT_INSTRUMENTED",
            "refs": [],
            "reason": "No separately named risk-ref field exists in the reused canonical Action input contract.",
        },
        "execution_eligibility": {
            "status": "NOT_EXECUTION_ELIGIBLE",
            "state": output.readiness.state,
            "ref": runtime_handoff_ref,
            "ref_source": "canonical_action_runtime_handoff_id",
            "candidate_only": True,
            "executed": False,
            "reason": output.readiness.reason,
        },
        "execution_eligibility_ref": runtime_handoff_ref,
        "runtime_executor_handoff": runtime_handoff,
        "runtime_executor_handoff_ref": runtime_handoff_ref,
        "runtime_executor_invoked": False,
        "validation_errors": [],
        "forbidden_behaviors": {
            "real_action_execution": output.action_executed,
            "device_control": output.device_control_executed,
            "runtime_dispatch_executed": output.runtime_executed,
            "model_invocation": False,
            "provider_invocation": False,
            "live_observation_execution": False,
            "field_mutation": output.database_write_executed,
            "memory_mutation": False,
            "experience_mutation": False,
            "learning_mutation": False,
            "world_truth_declared": False,
        },
    }


def build_action_admission_safety_run_v1() -> Dict[str, Any]:
    # This controlled safety fixture explicitly supplies available resources;
    # the generic Task-to-Action adapter defaults to UNKNOWN when no resource
    # proof is present.
    source = build_task_to_action_run_v1(resource_state="available")
    cases = [_positive_case(case) for case in source.get("cases") or ()]
    negatives = [
        _negative_case("A03_PERMISSION_REVOKED_TO_BLOCKED", "action_without_permission"),
        _negative_case("A04_SAFETY_VETO_TO_BLOCKED", "action_fails_safety"),
    ]
    return {
        "phase": PHASE,
        "source_integration_phase": source.get("phase"),
        "execution_instance_ref": source.get("execution_instance_ref"),
        "case_count": len(cases),
        "cases": cases,
        "negative_cases": negatives,
        "operational_result": "PENDING_USER_VERIFICATION",
        "cognitive_logic_result": "NOT_INDEPENDENTLY_EXERCISED",
        "final_decision": "NOT_GO",
        "deferred": [
            "runtime_executor_invocation",
            "real_action_execution",
            "device_control",
            "external_side_effect",
        ],
    }


__all__ = [
    "EXPECTED_CASES",
    "NEGATIVE_CASES",
    "PHASE",
    "build_action_admission_safety_run_v1",
]
