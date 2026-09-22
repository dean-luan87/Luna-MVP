"""Controlled composition of canonical cognition and Decision Governance."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from collections.abc import Mapping
from typing import Any, Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    build_brain_closure_run_v1,
    run_brain_cognitive_case_v1,
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
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    CanonicalGatewayAdmissionResultV1,
    EvidenceReferenceBindingV1,
    ObservationGatewayAdmissionQueryV1,
    resolve_owner_bound_gateway_record,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_engine_v1 import (
    validate_a_semantic_judgment_projection,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_working_envelope_cognitive_requirement_bridge_controlled.working_envelope_governance_v1 import (
    WORKING_ENVELOPE_CURRENT,
    WorkingEnvelopeRecordV1,
    query_current_working_envelope_v1,
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
EVIDENCE_OWNER = "Observation Gateway Governance"
EVIDENCE_BINDING_KIND = "ADMITTED_EVIDENCE"


def _jsonable(value: Any) -> Any:
    if isinstance(value, ObservationGatewayAdmissionQueryV1):
        return {
            "owner": "Observation Gateway",
            "semantics": "CURRENT_ADMISSION_QUERY_ONLY",
            "authority_serialized": False,
        }
    if is_dataclass(value):
        return {key: _jsonable(item) for key, item in asdict(value).items()}
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_jsonable(item) for item in value]
    return value


def _ref(owner: str, ref_id: str, ref_type: str) -> SourceRefV1:
    return SourceRefV1(owner=owner, ref_id=ref_id, ref_type=ref_type)


def _proof_value(proof: Any, key: str, default: Any = None) -> Any:
    if isinstance(proof, Mapping):
        return proof.get(key, default)
    return getattr(proof, key, default)


def _proofs(case: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list(case.get("cognitive_proofs") or [])


def _final_proof(case: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    proofs = _proofs(case)
    return proofs[-1] if proofs else None


def _validated_evidence_binding(
    case: Dict[str, Any],
    proof: Any,
) -> Tuple[Optional[Tuple[str, ...]], Optional[str]]:
    """Validate projections against a Gateway-owned current-state query."""

    proof_admission = _proof_value(proof, "canonical_gateway_admission_result")
    if proof_admission is None:
        return None, "decision_handoff_requires_canonical_gateway_admission_result"
    execution_identity_ref = case.get("gateway_execution_identity_ref")
    proof_execution_identity_ref = _proof_value(proof, "gateway_execution_identity_ref")
    if not execution_identity_ref or proof_execution_identity_ref != execution_identity_ref:
        return None, "decision_handoff_gateway_execution_identity_mismatch"
    admission_ref = _proof_value(proof_admission, "gateway_admission_ref")
    gateway_resolution = next(
        (
            (query, owner_record)
            for query in tuple(case.get("gateway_admission_queries") or ())
            if isinstance(query, ObservationGatewayAdmissionQueryV1)
            and (
                owner_record := resolve_owner_bound_gateway_record(
                    query,
                    execution_identity_ref,
                    admission_ref,
                )
            )
            is not None
        ),
        None,
    )
    if gateway_resolution is None:
        return None, "decision_handoff_requires_gateway_admission_query"
    admitted_refs = tuple(_proof_value(proof_admission, "evidence_refs") or ())
    _gateway_query, owner_record = gateway_resolution
    state_record, canonical_admission = owner_record
    if canonical_admission is not proof_admission:
        return None, "decision_handoff_rejects_noncanonical_gateway_admission_result"
    if state_record.admission_state != "ADMITTED":
        return None, "decision_handoff_requires_governed_gateway_admission"
    if tuple(state_record.evidence_refs) != admitted_refs:
        return None, "decision_handoff_gateway_admission_evidence_mismatch"

    binding = _proof_value(proof, "evidence_binding")
    if binding is not None:
        if not isinstance(binding, EvidenceReferenceBindingV1):
            return None, "decision_handoff_requires_canonical_evidence_binding"
        if binding.owner_ref != EVIDENCE_OWNER or binding.binding_kind != EVIDENCE_BINDING_KIND:
            return None, "decision_handoff_rejects_untyped_evidence_binding"
        if binding.candidate_only is not True:
            return None, "decision_handoff_rejects_non_candidate_evidence_binding"
        if binding.gateway_admission_ref != admission_ref:
            return None, "decision_handoff_evidence_binding_admission_mismatch"
        if tuple(binding.evidence_refs) != admitted_refs:
            return None, "decision_handoff_evidence_binding_set_mismatch"
        if len(set(binding.evidence_refs)) != len(binding.evidence_refs):
            return None, "decision_handoff_rejects_duplicate_evidence_refs"

    refs = admitted_refs
    if not refs:
        return None, "decision_handoff_requires_bound_evidence_refs"
    if any(not isinstance(ref, str) or not ref for ref in refs):
        return None, "decision_handoff_rejects_malformed_evidence_refs"
    if len(set(refs)) != len(refs):
        return None, "decision_handoff_rejects_duplicate_evidence_refs"
    proof_admission_ref = _proof_value(proof, "gateway_admission_ref")
    if proof_admission_ref != admission_ref:
        return None, "decision_handoff_evidence_binding_admission_mismatch"
    proof_admitted_refs = tuple(_proof_value(proof, "admitted_evidence_refs") or ())
    if proof_admitted_refs != refs:
        return None, "decision_handoff_evidence_binding_set_mismatch"
    return refs, None


def _canonical_gateway_admission(
    case: Dict[str, Any],
    proof: Any = None,
) -> Optional[CanonicalGatewayAdmissionResultV1]:
    proof_admission = _proof_value(proof, "canonical_gateway_admission_result")
    return proof_admission if proof_admission is not None else None


def _working_envelope_lineage(
    working_envelope: Optional[WorkingEnvelopeRecordV1],
) -> Tuple[Tuple[Optional[str], Optional[str]], Optional[str]]:
    """Accept only the owner record shape as a lineage entrypoint.

    The bridge accepts only the owner registry's current record as its
    entrypoint and transports the identity.  Future Action admission must
    still re-query the Envelope owner at its own boundary.
    """

    if working_envelope is None:
        return (None, None), None
    if not isinstance(working_envelope, WorkingEnvelopeRecordV1):
        return (None, None), "decision_handoff_requires_canonical_working_envelope_record"
    if working_envelope.canonical is not True or working_envelope.state != WORKING_ENVELOPE_CURRENT:
        return (None, None), "decision_handoff_requires_current_working_envelope_record"
    owner_record = query_current_working_envelope_v1(
        working_envelope.envelope_ref,
        profile_ref=working_envelope.profile_ref,
    )
    if owner_record is not working_envelope:
        return (None, None), "decision_handoff_requires_owner_issued_working_envelope_record"
    if not all(
        isinstance(value, str) and value
        for value in (
            working_envelope.envelope_ref,
            working_envelope.envelope_version_ref,
        )
    ):
        return (None, None), "decision_handoff_requires_working_envelope_identity"
    return (
        (working_envelope.envelope_ref, working_envelope.envelope_version_ref),
        None,
    )


def build_cognitive_decision_handoff_candidate_v1(
    case: Dict[str, Any],
    proof: Optional[Any],
    *,
    working_envelope: Optional[WorkingEnvelopeRecordV1] = None,
) -> Tuple[Optional[CognitiveDecisionHandoffCandidateV1], Tuple[str, ...]]:
    """Gate a Decision handoff on canonical final cognition readiness."""

    (working_envelope_ref, working_envelope_version_ref), envelope_error = _working_envelope_lineage(
        working_envelope
    )
    if envelope_error:
        return None, (envelope_error,)

    from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
        validated_requirement_establishment_from_condition_formation_v1,
    )

    request = case.get("brain_request") or {}
    need = case.get("information_need") or {}
    loop = case.get("loop_instance") or {}
    if proof is None:
        return None, ("decision_handoff_requires_cognitive_proof",)
    if _proof_value(proof, "semantic_owner_ref") != "A_REASONING_ROLE":
        return None, ("decision_handoff_requires_a_owned_semantic_judgment",)
    semantic_judgment = _proof_value(proof, "cognitive_semantic_judgment")
    if semantic_judgment is None or _proof_value(semantic_judgment, "semantic_owner_ref") != "A_REASONING_ROLE":
        return None, ("decision_handoff_requires_a_owned_semantic_judgment",)
    judgment_errors = validate_a_semantic_judgment_projection(
        semantic_judgment,
        semantic_owner_ref=_proof_value(proof, "semantic_owner_ref"),
        semantic_judgment_ref=_proof_value(proof, "semantic_judgment_ref"),
        hypothesis_refs=_proof_value(proof, "hypothesis_refs"),
        sufficiency_ref=_proof_value(proof, "sufficiency_ref"),
        sufficiency_status=_proof_value(proof, "sufficiency_status"),
        information_gap_ref=_proof_value(proof, "information_gap_ref"),
        reobservation_ref=_proof_value(proof, "reobservation_ref"),
        hypothesis_revision_ref=_proof_value(proof, "hypothesis_revision_ref"),
        hypothesis_revision_information_gap_ref=_proof_value(
            proof, "hypothesis_revision_information_gap_ref"
        ),
        hypothesis_revision_reobservation_ref=_proof_value(
            proof, "hypothesis_revision_reobservation_ref"
        ),
        stop_ref=_proof_value(proof, "stop_ref"),
        semantic_provenance_refs=_proof_value(proof, "semantic_provenance_refs"),
    )
    if judgment_errors:
        return None, ("decision_handoff_rejects_unbound_a_judgment", *judgment_errors)
    if _proof_value(proof, "sufficiency_status") != "SUFFICIENT":
        return None, ("decision_handoff_requires_sufficient_cognition",)
    if _proof_value(proof, "requirement_establishment_status") != "ESTABLISHED" or not _proof_value(proof, "requirement_establishment_ref"):
        return None, ("decision_handoff_requires_requirement_establishment",)
    establishment = validated_requirement_establishment_from_condition_formation_v1(
        _proof_value(proof, "required_cognitive_condition_formation_result")
    )
    if establishment is None or establishment[1] != _proof_value(proof, "requirement_establishment_ref"):
        return None, ("decision_handoff_requires_validated_requirement_establishment",)
    if not _proof_value(proof, "sufficiency_ref"):
        return None, ("decision_handoff_requires_sufficiency_ref",)
    if not _proof_value(proof, "stop_ref"):
        return None, ("decision_handoff_requires_canonical_stop",)
    if not _proof_value(proof, "current_world_ref"):
        return None, ("decision_handoff_requires_current_world_ref",)
    if not _proof_value(proof, "hypothesis_refs"):
        return None, ("decision_handoff_requires_hypothesis_refs",)
    canonical_admission = _canonical_gateway_admission(case, proof)
    evidence_refs, evidence_error = _validated_evidence_binding(case, proof)
    if evidence_error:
        return None, (evidence_error,)

    handoff_ref = f"cognitive-decision-handoff:{case['case_id']}:{_proof_value(proof, 'execution_ref')}"
    provenance_refs = (
        _proof_value(proof, "execution_ref"),
        _proof_value(proof, "sufficiency_ref"),
        _proof_value(proof, "stop_ref"),
        *tuple(_proof_value(proof, "hypothesis_refs") or ()),
        *evidence_refs,
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
            a_route_execution_ref=_proof_value(proof, "execution_ref"),
            current_world_ref=_proof_value(proof, "current_world_ref"),
            hypothesis_refs=tuple(_proof_value(proof, "hypothesis_refs")),
            evidence_refs=evidence_refs,
            sufficiency_ref=_proof_value(proof, "sufficiency_ref"),
            stop_ref=_proof_value(proof, "stop_ref"),
            provenance_refs=provenance_refs,
            execution_instance_ref=_proof_value(proof, "execution_ref").split(":", 1)[0],
            semantic_owner_ref=_proof_value(proof, "semantic_owner_ref"),
            semantic_judgment_ref=_proof_value(semantic_judgment, "judgment_ref"),
            evidence_owner_ref=EVIDENCE_OWNER,
            evidence_binding_kind=EVIDENCE_BINDING_KIND,
            gateway_admission_ref=_proof_value(proof, "gateway_admission_ref"),
            admitted_evidence_refs=tuple(_proof_value(proof, "admitted_evidence_refs")),
            canonical_gateway_admission_result=canonical_admission,
            working_envelope_ref=working_envelope_ref,
            working_envelope_version_ref=working_envelope_version_ref,
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
        _ref(handoff.semantic_owner_ref, handoff.sufficiency_ref, "SUFFICIENCY"),
        _ref(handoff.semantic_owner_ref, handoff.stop_ref, "STOP"),
    )
    evidence_refs = tuple(
        _ref(handoff.evidence_owner_ref, ref, "EVIDENCE") for ref in handoff.evidence_refs
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
        working_envelope_ref=handoff.working_envelope_ref,
        working_envelope_version_ref=handoff.working_envelope_version_ref,
    )


def _attempt(
    cycle_index: int,
    proof: Optional[Any],
    case: Dict[str, Any],
    working_envelope: Optional[WorkingEnvelopeRecordV1] = None,
) -> Tuple[DecisionHandoffAttemptV1, Optional[CognitiveDecisionHandoffCandidateV1], Tuple[str, ...]]:
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        case,
        proof,
        working_envelope=working_envelope,
    )
    if handoff is None:
        return (
            DecisionHandoffAttemptV1(
                cycle_index=cycle_index,
                status="ABSENT",
                rejection_reason=errors[0],
                source_execution_ref=_proof_value(proof, "execution_ref") if proof else None,
                sufficiency_status=_proof_value(proof, "sufficiency_status") if proof else None,
                stop_ref=_proof_value(proof, "stop_ref") if proof else None,
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
    if (
        handoff.evidence_owner_ref != EVIDENCE_OWNER
        or handoff.evidence_binding_kind != EVIDENCE_BINDING_KIND
    ):
        return {
            "request": None,
            "output": None,
            "decision_candidate_refs": [],
            "decision_trace_ref": None,
            "decision_trace_causal_refs": [],
            "decision_trace_evidence_refs": [],
            "decision_candidate_provenance_via_cognition": False,
            "cognition_provenance_refs": list(handoff.provenance_refs),
            "checks": {"evidence_binding_valid": False},
            "all_checks_passed": False,
            "decision_governance_consumed": False,
            "rejection_errors": ["decision_handoff_rejects_unbound_evidence"],
        }
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
        "decision_governance_consumed": True,
    }


def _case_result(
    case: Dict[str, Any],
    working_envelope: Optional[WorkingEnvelopeRecordV1] = None,
) -> Dict[str, Any]:
    case_data = _jsonable(case) if is_dataclass(case) else case
    proof_objects = list(getattr(case, "cognitive_proofs", ())) if is_dataclass(case) else _proofs(case)
    proofs = [_jsonable(proof) for proof in proof_objects]
    attempts = []
    handoff: Optional[CognitiveDecisionHandoffCandidateV1] = None
    attempt_errors: list[str] = []
    handoff_case = case_data
    if is_dataclass(case):
        handoff_case = dict(case_data)
        handoff_case["gateway_results"] = tuple(case.gateway_results)
        handoff_case["gateway_admission_queries"] = case.gateway_admission_queries
    for index, proof in enumerate(proof_objects, start=1):
        attempt_case = dict(handoff_case)
        attempt_case["gateway_execution_identity_ref"] = _proof_value(
            proof, "gateway_execution_identity_ref"
        )
        attempt, candidate, errors = _attempt(
            index,
            proof,
            attempt_case,
            working_envelope=working_envelope,
        )
        attempts.append(_jsonable(attempt))
        attempt_errors.extend(errors)
        if candidate is not None:
            handoff = candidate

    decision = _decision_result(handoff) if handoff else None
    final_proof = proofs[-1] if proofs else {}
    request = case_data.get("brain_request") or {}
    need = case_data.get("information_need") or {}
    loop = case_data.get("loop_instance") or {}
    gateways = list(case_data.get("gateway_results") or [])
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
        "closure_candidate_ref": (case_data.get("closure_assessment") or {}).get("assessment_ref"),
        "assimilation_candidate_ref": (case_data.get("assimilation_candidate") or {}).get("assimilation_ref"),
    }
    raw_errors = list(case_data.get("validation_errors") or [])
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
        "case_id": case_data.get("case_id"),
        "cognitive_case": case_data,
        "execution_mode": final_proof.get("execution_mode"),
        "cognitive_cycle_count": (case_data.get("loop_instance") or {}).get("cycle_count"),
        "final_cognition_execution_ref": final_proof.get("execution_ref"),
        "final_sufficiency_ref": final_proof.get("sufficiency_ref"),
        "final_sufficiency_status": final_proof.get("sufficiency_status"),
        "final_stop_ref": final_proof.get("stop_ref"),
        "working_envelope_ref": handoff.working_envelope_ref if handoff else None,
        "working_envelope_version_ref": (
            handoff.working_envelope_version_ref if handoff else None
        ),
        "traceability": traceability,
        "handoff_attempts": attempts,
        "decision_handoff": _jsonable(handoff) if handoff else None,
        "decision_handoff_ref": handoff.handoff_ref if handoff else None,
        "decision_governance_consumed": bool(decision and decision.get("decision_governance_consumed")),
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


def _negative_premature_handoff(cases: Iterable[Any]) -> Dict[str, Any]:
    case = next(
        item for item in cases
        if (item.case_id if is_dataclass(item) else item.get("case_id"))
        == "CASE_B_GAP_REOBSERVE_REVISE_STOP"
    )
    if is_dataclass(case):
        case_data = _jsonable(case)
        case_data["gateway_results"] = tuple(case.gateway_results)
        proof = case.cognitive_proofs[0]
    else:
        case_data = case
        proof = _proofs(case)[0]
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case_data, proof)
    rejected = handoff is None and "decision_handoff_requires_sufficient_cognition" in errors
    return {
        "fixture": "premature_decision_handoff_before_sufficiency",
        "expected": "REJECTED",
        "rejected": rejected,
        "decision_governance_called": False,
        "cycle": 1,
        "sufficiency_status": _proof_value(proof, "sufficiency_status"),
        "errors": list(errors),
    }


def build_decision_handoff_run_v1(
    execution_instance_ref: str = EXECUTION_INSTANCE_REF,
    working_envelope: Optional[WorkingEnvelopeRecordV1] = None,
) -> Dict[str, Any]:
    source = build_brain_closure_run_v1(execution_instance_ref)
    typed_cases = [
        run_brain_cognitive_case_v1(case_id, execution_instance_ref)
        for case_id in EXPECTED_CASES
    ]
    cases = [
        _case_result(case, working_envelope=working_envelope)
        for case in typed_cases
    ]
    return {
        "phase": PHASE,
        "source_integration_phase": source.get("phase"),
        "execution_instance_ref": execution_instance_ref,
        "case_count": len(cases),
        "cases": cases,
        "negative_test": _negative_premature_handoff(typed_cases),
        "deferred": ["task_execution", "action_execution", "model_provider_execution", "archive_integration"],
    }


__all__ = [
    "PHASE",
    "EXPECTED_CASES",
    "build_cognitive_decision_handoff_candidate_v1",
    "build_decision_handoff_run_v1",
]
