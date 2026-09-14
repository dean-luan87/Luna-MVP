"""Controlled composition of canonical cognition and Decision Governance."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    build_brain_closure_run_v1,
)
from capabilities.midplatform.core.decision_governance.decision_core_types_v1 import (
    DecisionOptionCandidateV1,
    RiskCandidateV1,
    SourceRefV1,
    UtilityCandidateV1,
)
from capabilities.midplatform.core.decision_governance.decision_governance_engine_v1 import (
    DecisionGovernanceEngineV1,
)
from capabilities.midplatform.core.decision_governance.decision_io_types_v1 import (
    DecisionGovernanceInputV1,
)
from capabilities.midplatform.core.decision_governance.decision_static_validators_v1 import (
    validate_candidates,
    validate_handoff,
    validate_input_refs_read_only,
    validate_no_runtime_side_effects,
    validate_trace_completeness,
)

from .cognitive_result_to_decision_governance_handoff_types_v1 import (
    COGNITION_OWNER,
    DECISION_OWNER,
    CognitiveDecisionHandoffCandidateV1,
    DecisionHandoffAttemptV1,
)


PHASE = "Phase-P1-Luna-Cognitive-Result-To-Decision-Governance-Controlled-Handoff-Integration-v1-001"
EXECUTION_INSTANCE_REF = "cognitive-decision-handoff-controlled-session"
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


def _ref(owner: str, ref_id: str, ref_type: str) -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _proofs(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list(case.get("cognitive_proofs") or [])


def _final_proof(case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    proofs = _proofs(case)
    return proofs[-1] if proofs else None


def build_cognitive_decision_handoff_candidate_v1(
    case: Dict[str, Any], proof: Optional[Dict[str, Any]]
) -> Tuple[Optional[CognitiveDecisionHandoffCandidateV1], Tuple[str, ...]]:
    """Gate a Decision handoff on canonical final cognition readiness."""

    request = case.get("brain_request") or {}
    need = case.get("information_need") or {}
    loop = case.get("loop_instance") or {}
    if proof is None:
        return None, ("decision_handoff_requires_cognitive_proof",)
    if proof.get("sufficiency_status") != "SUFFICIENT":
        return None, ("decision_handoff_requires_sufficient_cognition",)
    if not proof.get("sufficiency_ref"):
        return None, ("decision_handoff_requires_sufficiency_ref",)
    if not proof.get("stop_ref"):
        return None, ("decision_handoff_requires_canonical_stop",)
    if not proof.get("current_world_ref"):
        return None, ("decision_handoff_requires_current_world_ref",)
    if not proof.get("hypothesis_refs"):
        return None, ("decision_handoff_requires_hypothesis_refs",)
    if not proof.get("ingress_refs"):
        return None, ("decision_handoff_requires_evidence_refs",)

    handoff_ref = f"cognitive-decision-handoff:{case['case_id']}:{proof['execution_ref']}"
    provenance_refs = (
        proof["execution_ref"],
        proof["sufficiency_ref"],
        proof["stop_ref"],
        *tuple(proof.get("hypothesis_refs") or ()),
        *tuple(proof.get("ingress_refs") or ()),
    )
    return (
        CognitiveDecisionHandoffCandidateV1(
            handoff_ref=handoff_ref,
            case_id=case["case_id"],
            producer_owner_ref=COGNITION_OWNER,
            consumer_owner_ref=DECISION_OWNER,
            goal_ref=request["goal_ref"],
            intent_ref=request["intent_ref"],
            concern_ref=request["concern_ref"],
            context_ref=request["context_ref"],
            information_need_ref=need["information_need_ref"],
            cognitive_loop_ref=loop["cognitive_loop_ref"],
            a_route_execution_ref=proof["execution_ref"],
            current_world_ref=proof["current_world_ref"],
            hypothesis_refs=tuple(proof["hypothesis_refs"]),
            evidence_refs=tuple(proof["ingress_refs"]),
            sufficiency_ref=proof["sufficiency_ref"],
            stop_ref=proof["stop_ref"],
            provenance_refs=provenance_refs,
            execution_instance_ref=proof["execution_ref"].split(":", 1)[0],
        ),
        (),
    )


def _decision_input(handoff: CognitiveDecisionHandoffCandidateV1) -> DecisionGovernanceInputV1:
    """Map the read-only cognitive handoff into canonical Decision input."""

    policy_owner = DECISION_OWNER
    intent_refs = (_ref("Intent Governance", handoff.intent_ref, "INTENT"),)
    causal_refs = tuple(
        _ref(COGNITION_OWNER, ref, "COGNITIVE_PROVENANCE")
        for ref in handoff.provenance_refs
    )
    context_refs = (_ref("Context Foundation", handoff.context_ref, "CONTEXT"),)
    field_refs = (_ref(COGNITION_OWNER, handoff.current_world_ref, "CURRENT_WORLD_CANDIDATE"),)
    role_refs = (_ref("Role", f"role:{handoff.case_id}", "ROLE"),)
    permission_refs = (_ref(policy_owner, f"permission:{handoff.case_id}:controlled-candidate", "PERMISSION"),)
    safety_refs = (_ref(policy_owner, f"safety:{handoff.case_id}:controlled-candidate", "SAFETY"),)
    resource_refs = (_ref(policy_owner, f"resource:{handoff.case_id}:controlled-candidate", "RESOURCE"),)
    constraint_refs = (
        _ref(COGNITION_OWNER, handoff.sufficiency_ref, "SUFFICIENCY"),
        _ref(COGNITION_OWNER, handoff.stop_ref, "STOP"),
    )
    evidence_refs = tuple(
        _ref(COGNITION_OWNER, ref, "EVIDENCE") for ref in handoff.evidence_refs
    )
    option_id = f"option:{handoff.case_id}:controlled-candidate"
    option = DecisionOptionCandidateV1(
        option_id=option_id,
        option_statement="controlled candidate derived from the completed cognitive result",
        utility=UtilityCandidateV1(
            utility_ref_id=f"utility:{handoff.case_id}:controlled-candidate",
            expected_benefit=90,
            provenance=handoff.provenance_refs,
        ),
        risk=RiskCandidateV1(
            risk_ref_id=f"risk:{handoff.case_id}:controlled-candidate",
            severity=1,
            likelihood=1,
            provenance=handoff.provenance_refs,
        ),
        cost=1,
        hard_constraints_ok=True,
        permission_allowed=True,
        safety_allowed=True,
        role_allowed=True,
        reversibility="REVERSIBLE",
        intent_alignment=2,
        evidence_ready=True,
    )
    return DecisionGovernanceInputV1(
        scenario_id=f"{handoff.case_id}__HANDOFF",
        intent_refs=intent_refs,
        causal_refs=causal_refs,
        context_refs=context_refs,
        field_refs=field_refs,
        role_refs=role_refs,
        permission_refs=permission_refs,
        safety_refs=safety_refs,
        resource_refs=resource_refs,
        constraint_refs=constraint_refs,
        evidence_refs=evidence_refs,
        options=(option,),
        intent_preferred_option_ids=(option_id,),
        synthetic_only=True,
        candidate_only=True,
    )


def _attempt(cycle_index: int, proof: Optional[Dict[str, Any]], case: Dict[str, Any]) -> Tuple[DecisionHandoffAttemptV1, Optional[CognitiveDecisionHandoffCandidateV1], Tuple[str, ...]]:
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    if handoff is None:
        return (
            DecisionHandoffAttemptV1(
                cycle_index=cycle_index,
                status="ABSENT",
                rejection_reason=errors[0],
                source_execution_ref=proof.get("execution_ref") if proof else None,
                sufficiency_status=proof.get("sufficiency_status") if proof else None,
                stop_ref=proof.get("stop_ref") if proof else None,
            ),
            None,
            errors,
        )
    return (
        DecisionHandoffAttemptV1(
            cycle_index=cycle_index,
            status="ADMITTED",
            handoff_ref=handoff.handoff_ref,
            source_execution_ref=handoff.a_route_execution_ref,
            sufficiency_status="SUFFICIENT",
            stop_ref=handoff.stop_ref,
        ),
        handoff,
        (),
    )


def _decision_result(handoff: CognitiveDecisionHandoffCandidateV1) -> Dict[str, Any]:
    request = _decision_input(handoff)
    all_refs = (
        request.intent_refs
        + request.causal_refs
        + request.context_refs
        + request.field_refs
        + request.role_refs
        + request.permission_refs
        + request.safety_refs
        + request.resource_refs
        + request.constraint_refs
        + request.evidence_refs
    )
    output = DecisionGovernanceEngineV1().run_case(request)
    checks = {
        "input_refs_read_only": validate_input_refs_read_only(all_refs),
        "decision_candidates_valid": validate_candidates(output.decision_candidates),
        "trace_complete": validate_trace_completeness(output),
        "handoff_valid": validate_handoff(output.handoff_candidate),
        "no_runtime_side_effects": validate_no_runtime_side_effects(output),
        "candidate_only": output.candidate_only is True,
        "decision_owner": all(item.owner == DECISION_OWNER for item in output.decision_candidates),
    }
    trace = output.trace_candidate
    candidate_refs = tuple(item.decision_candidate_id for item in output.decision_candidates)
    return {
        "request": _jsonable(request),
        "output": _jsonable(output),
        "decision_candidate_refs": list(candidate_refs),
        "decision_trace_ref": trace.trace_id,
        "decision_trace_causal_refs": list(trace.causal_refs),
        "decision_trace_evidence_refs": list(trace.evidence_refs),
        "decision_candidate_provenance_via_cognition": all(
            ref in trace.causal_refs or ref in trace.evidence_refs
            for ref in handoff.provenance_refs
        ),
        "cognition_provenance_refs": list(handoff.provenance_refs),
        "checks": checks,
        "all_checks_passed": all(checks.values()),
    }


def _case_result(case: Dict[str, Any]) -> Dict[str, Any]:
    proofs = _proofs(case)
    attempts = []
    handoff: Optional[CognitiveDecisionHandoffCandidateV1] = None
    attempt_errors: list[str] = []
    for index, proof in enumerate(proofs, start=1):
        attempt, candidate, errors = _attempt(index, proof, case)
        attempts.append(_jsonable(attempt))
        attempt_errors.extend(errors)
        if candidate is not None:
            handoff = candidate

    decision = _decision_result(handoff) if handoff else None
    final_proof = _final_proof(case) or {}
    request = case.get("brain_request") or {}
    need = case.get("information_need") or {}
    loop = case.get("loop_instance") or {}
    gateways = list(case.get("gateway_results") or [])
    traceability = {
        "goal_ref": request.get("goal_ref"),
        "intent_ref": request.get("intent_ref"),
        "concern_ref": request.get("concern_ref"),
        "context_ref": request.get("context_ref"),
        "information_need_ref": need.get("information_need_ref"),
        "cognitive_loop_ref": loop.get("cognitive_loop_ref"),
        "gateway_admission_refs": [
            (item.get("replay_admission") or {}).get("gateway_admission_ref")
            for item in gateways
        ],
        "a_route_execution_refs": [item.get("execution_ref") for item in proofs],
        "evidence_refs": [
            item.get("evidence_id")
            for gateway in gateways
            for item in gateway.get("evidence", [])
        ],
        "hypothesis_refs": [
            ref for proof_item in proofs for ref in proof_item.get("hypothesis_refs", [])
        ],
        "current_world_refs": [
            proof_item.get("current_world_ref")
            for proof_item in proofs
            if proof_item.get("current_world_ref")
        ],
        "sufficiency_refs": [
            proof_item.get("sufficiency_ref")
            for proof_item in proofs
            if proof_item.get("sufficiency_ref")
        ],
        "information_gap_ref": next(
            (proof_item.get("information_gap_ref") for proof_item in proofs if proof_item.get("information_gap_ref")),
            None,
        ),
        "reobservation_ref": next(
            (proof_item.get("reobservation_ref") for proof_item in proofs if proof_item.get("reobservation_ref")),
            None,
        ),
        "hypothesis_revision_ref": next(
            (proof_item.get("hypothesis_revision_ref") for proof_item in proofs if proof_item.get("hypothesis_revision_ref")),
            None,
        ),
        "stop_ref": final_proof.get("stop_ref"),
        "closure_candidate_ref": (case.get("closure_assessment") or {}).get("assessment_ref"),
        "assimilation_candidate_ref": (case.get("assimilation_candidate") or {}).get("assimilation_ref"),
    }
    raw_errors = list(case.get("validation_errors") or [])
    # The expected absent first-cycle attempt is a governed rejection, not a
    # positive-case validation error.
    positive_errors = [
        error for error in attempt_errors
        if error != "decision_handoff_requires_sufficient_cognition"
    ]
    if handoff and decision:
        traceability["decision_handoff_ref"] = handoff.handoff_ref
        traceability["decision_trace_ref"] = decision["decision_trace_ref"]
        traceability["decision_candidate_refs"] = decision["decision_candidate_refs"]
    return {
        "case_id": case.get("case_id"),
        "cognitive_case": case,
        "execution_mode": final_proof.get("execution_mode"),
        "cognitive_cycle_count": (case.get("loop_instance") or {}).get("cycle_count"),
        "final_cognition_execution_ref": final_proof.get("execution_ref"),
        "final_sufficiency_ref": final_proof.get("sufficiency_ref"),
        "final_sufficiency_status": final_proof.get("sufficiency_status"),
        "final_stop_ref": final_proof.get("stop_ref"),
        "traceability": traceability,
        "handoff_attempts": attempts,
        "decision_handoff": _jsonable(handoff) if handoff else None,
        "decision_handoff_ref": handoff.handoff_ref if handoff else None,
        "decision_governance_consumed": decision is not None,
        "decision": decision,
        "owner_boundaries": {
            "cstate_owns_decision": False,
            "brain_owns_decision": False,
            "evaluation_owns_decision": False,
            "decision_governance_owns_decision_candidate": True,
        },
        "forbidden_behaviors": {
            "task_execution": False,
            "action_execution": False,
            "device_control": False,
            "model_invocation": False,
            "provider_invocation": False,
            "live_observation_execution": False,
            "field_mutation": False,
            "memory_mutation": False,
            "experience_mutation": False,
            "learning_mutation": False,
            "world_truth_declared": False,
        },
        "validation_errors": raw_errors + positive_errors,
    }


def _negative_premature_handoff(cases: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    case = next(item for item in cases if item.get("case_id") == "CASE_B_GAP_REOBSERVE_REVISE_STOP")
    proof = _proofs(case)[0]
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case, proof)
    rejected = handoff is None and "decision_handoff_requires_sufficient_cognition" in errors
    return {
        "fixture": "premature_decision_handoff_before_sufficiency",
        "expected": "REJECTED",
        "rejected": rejected,
        "decision_governance_called": False,
        "cycle": 1,
        "sufficiency_status": proof.get("sufficiency_status"),
        "errors": list(errors),
    }


def build_decision_handoff_run_v1(
    execution_instance_ref: str = EXECUTION_INSTANCE_REF,
) -> Dict[str, Any]:
    source = build_brain_closure_run_v1(execution_instance_ref)
    source_cases = list(source["cases"])
    cases = [_case_result(case) for case in source_cases]
    return {
        "phase": PHASE,
        "source_integration_phase": source.get("phase"),
        "execution_instance_ref": execution_instance_ref,
        "case_count": len(cases),
        "cases": cases,
        "negative_test": _negative_premature_handoff(source_cases),
        "deferred": ["task_execution", "action_execution", "model_provider_execution", "archive_integration"],
    }


__all__ = [
    "PHASE",
    "EXPECTED_CASES",
    "build_cognitive_decision_handoff_candidate_v1",
    "build_decision_handoff_run_v1",
]
