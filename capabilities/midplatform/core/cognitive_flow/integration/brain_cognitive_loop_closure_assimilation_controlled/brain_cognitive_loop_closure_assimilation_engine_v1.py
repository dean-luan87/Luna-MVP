"""Controlled Brain entry, A-Route execution, closure, and assimilation bridge."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from typing import Any, Dict, Iterable, Optional, Tuple

from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
    ARouteOrchestrationRequestV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.controlled_replay_runtime_fixture_v1 import (
    build_minimum_sufficient_loop_gateway_request_v1,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_core_types_v1 import (
    ObservationGatewayAdmissionQueryV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_lifecycle_closure_types_v1 import (
    BrainAssimilationCandidateV1,
    ClosureAssessmentCandidateV1,
    ClosureDecisionCandidateV1,
    LifecycleClosureCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_loop_governed_continuity_candidate_controlled.cognitive_loop_continuity_candidate_types_v1 import (
    CognitiveOutcomeCandidateV1,
    LoopClosureRecordCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_engine_v1 import (
    validate_a_semantic_judgment_projection,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)

from .brain_cognitive_loop_closure_assimilation_fixture_v1 import (
    build_case_a_replay_v1,
    build_case_b_cycle_1_replay_v1,
    build_case_b_cycle_2_replay_v1,
)
from .brain_cognitive_loop_closure_assimilation_types_v1 import (
    BRAIN_CANONICAL_OWNER_STATUS,
    BRAIN_RESPONSIBILITY_DOMAIN,
    LOOP_LIFECYCLE_OWNER,
    PHASE,
    BrainCognitiveCaseResultV1,
    BrainCognitiveLoopInstanceV1,
    BrainCognitiveRequestV1,
    BrainInformationNeedCandidateV1,
)


NEGATIVE_GUARDS = {
    "evaluation_owns_cognition": False,
    "cstate_mutates_brain": False,
    "closure_without_sufficiency": False,
    "closure_before_stop": False,
    "assimilation_mutates_memory": False,
    "assimilation_mutates_experience": False,
    "assimilation_declares_world_truth": False,
    "decision_execution": False,
    "task_execution": False,
    "action_execution": False,
    "live_observation": False,
    "model_invocation": False,
    "provider_invocation": False,
}
NEGATIVE_GUARD_RUNTIME_COVERAGE = frozenset({"closure_without_sufficiency"})


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


def _route_for_brain(
    request: BrainCognitiveRequestV1,
    replay: Any,
    scenario_id: str,
    cycle_label: str,
):
    execution_ref = f"{request.execution_instance_ref}:{cycle_label}"
    gateway_request = build_minimum_sufficient_loop_gateway_request_v1(
        scenario_id=scenario_id,
        replay=replay,
        execution_identity_ref=execution_ref,
    )
    gateway_engine = ObservationGatewayEngineV1()
    gateway = gateway_engine.run_case(gateway_request)
    observation = gateway.observation
    admission = gateway.replay_admission
    ingress = ARouteIngressRefsV1(
        observation_refs=(observation.observation_id,) if observation else (),
        perception_refs=tuple(item.evidence_id for item in gateway.evidence),
    )
    route = ARouteOrchestrationEngineV1().run_case(
        ARouteOrchestrationRequestV1(
            scenario_id=scenario_id,
            ingress=ingress,
            context_ref=request.context_ref,
            pcn_ref=f"pcn:{request.brain_subject_ref}",
            intent_ref=request.intent_ref,
            execution_mode=CONTROLLED_REPLAY_RUNTIME,
            execution_identity_ref=execution_ref,
            replay_admission=admission,
            synthetic_only=False,
            candidate_only=True,
        )
    )
    return gateway, route, gateway_engine.admission_query


def _build_request(case_id: str, execution_instance_ref: str) -> BrainCognitiveRequestV1:
    return BrainCognitiveRequestV1(
        brain_request_ref=f"brain-request:{case_id}:{execution_instance_ref}",
        brain_subject_ref=f"brain-subject:{case_id}",
        goal_ref=f"goal:{case_id}",
        intent_ref=f"intent:{case_id}",
        concern_ref=f"concern:{case_id}",
        context_ref=f"context:{case_id}",
        role_ref=f"role:{case_id}",
        information_need_ref=f"information-need:{case_id}",
        required_information_refs=("information:target-identity", "information:target-location"),
        execution_instance_ref=execution_instance_ref,
    )


def _build_information_need(request: BrainCognitiveRequestV1) -> BrainInformationNeedCandidateV1:
    need_candidate = CognitiveNeedCandidateV1(
        need_id=request.information_need_ref,
        source_intent_ref=request.intent_ref,
        source_context_ref=request.context_ref,
        source_field_ref=None,
        source_hypothesis_ref=None,
        source_attention_ref=None,
        problem_description="information required to satisfy the active Brain concern",
        missing_information_class="goal_concern_resolution",
        required_evidence_class="controlled_replay_evidence",
        urgency="normal",
        safety_relevance="normal",
        trace_ref=f"trace:{request.information_need_ref}",
        state_version_ref=request.brain_request_ref,
    )
    return BrainInformationNeedCandidateV1(
        information_need_ref=request.information_need_ref,
        responsibility_domain=BRAIN_RESPONSIBILITY_DOMAIN,
        canonical_owner_status=BRAIN_CANONICAL_OWNER_STATUS,
        goal_ref=request.goal_ref,
        intent_ref=request.intent_ref,
        concern_ref=request.concern_ref,
        context_ref=request.context_ref,
        required_information_refs=request.required_information_refs,
        need_candidate=need_candidate,
    )


def _build_closure(
    request: BrainCognitiveRequestV1,
    loop: BrainCognitiveLoopInstanceV1,
    proof: Any,
):
    from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
        validated_requirement_establishment_from_condition_formation_v1,
    )
    establishment = validated_requirement_establishment_from_condition_formation_v1(
        getattr(proof, "required_cognitive_condition_formation_result", None)
        if proof is not None
        else None
    )
    semantic_judgment = getattr(proof, "cognitive_semantic_judgment", None) if proof is not None else None
    judgment_errors = (
        validate_a_semantic_judgment_projection(
            semantic_judgment,
            semantic_owner_ref=getattr(proof, "semantic_owner_ref", None),
            semantic_judgment_ref=getattr(proof, "semantic_judgment_ref", None),
            hypothesis_refs=getattr(proof, "hypothesis_refs", None),
            sufficiency_ref=getattr(proof, "sufficiency_ref", None),
            sufficiency_status=getattr(proof, "sufficiency_status", None),
            information_gap_ref=getattr(proof, "information_gap_ref", None),
            reobservation_ref=getattr(proof, "reobservation_ref", None),
            hypothesis_revision_ref=getattr(proof, "hypothesis_revision_ref", None),
            hypothesis_revision_information_gap_ref=getattr(
                proof, "hypothesis_revision_information_gap_ref", None
            ),
            hypothesis_revision_reobservation_ref=getattr(
                proof, "hypothesis_revision_reobservation_ref", None
            ),
            stop_ref=getattr(proof, "stop_ref", None),
            semantic_provenance_refs=getattr(proof, "semantic_provenance_refs", None),
        )
        if proof is not None
        else ("a_judgment_missing",)
    )
    if (
        proof is None
        or getattr(proof, "semantic_owner_ref", None) != "A_REASONING_ROLE"
        or semantic_judgment is None
        or getattr(semantic_judgment, "semantic_owner_ref", None) != "A_REASONING_ROLE"
        or getattr(semantic_judgment, "local_disposition", None) != "STOP_SUFFICIENT"
        or getattr(semantic_judgment, "missing_information_refs", ())
        or getattr(semantic_judgment, "information_gap_ref", None)
        or getattr(semantic_judgment, "reobservation_ref", None)
        or getattr(semantic_judgment, "next_cycle_ingress_ref", None)
        or proof.sufficiency_status != "SUFFICIENT"
        or proof.requirement_establishment_status != "ESTABLISHED"
        or not proof.requirement_establishment_ref
        or not proof.sufficiency_ref
        or establishment is None
        or establishment[1] != proof.requirement_establishment_ref
        or judgment_errors
    ):
        return (None, None, None, None, None, None, ("closure_requires_sufficient_cognition",))
    if not proof.stop_ref:
        return (None, None, None, None, None, None, ("closure_requires_canonical_stop",))
    evidence_binding = getattr(proof, "evidence_binding", None)
    evidence_refs = tuple(getattr(evidence_binding, "evidence_refs", ()) or ())
    closure_ref = f"closure-candidate:{loop.cognitive_loop_ref}:v1"
    assessment = ClosureAssessmentCandidateV1(
        assessment_ref=closure_ref,
        loop_id=loop.cognitive_loop_ref,
        cognitive_concern_ref=request.concern_ref,
        local_closure_state="OPEN",
        local_state_version_ref=proof.execution_ref,
        current_need_ref=request.information_need_ref,
        closure_reason="STOP_SUFFICIENT",
        local_sufficiency_ref=proof.sufficiency_ref,
        evidence_refs=evidence_refs,
        outstanding_requirement_refs=(),
        outstanding_observation_refs=(),
        suggested_lifecycle_disposition="COMPLETED",
        eligible_for_governance=True,
        closure_candidate_created=True,
        reason_refs=(proof.sufficiency_ref, proof.stop_ref),
    )
    acceptance = ClosureDecisionCandidateV1(
        decision_ref=f"closure-acceptance:{loop.cognitive_loop_ref}:v1",
        loop_id=loop.cognitive_loop_ref,
        assessment_ref=assessment.assessment_ref,
        governing_owner_ref=BRAIN_CANONICAL_OWNER_STATUS,
        accepted=True,
        lifecycle_disposition="COMPLETED",
        closure_reason="STOP_SUFFICIENT",
        acceptance_state_version_ref=proof.execution_ref,
        decision_reason_refs=(proof.sufficiency_ref, proof.stop_ref),
    )
    lifecycle = LifecycleClosureCandidateV1(
        lifecycle_closure_ref=f"lifecycle-closure:{loop.cognitive_loop_ref}:v1",
        loop_id=loop.cognitive_loop_ref,
        source_closure_state="OPEN",
        target_closure_state="CLOSED",
        accepted=True,
        lifecycle_disposition="COMPLETED",
        closure_reason="STOP_SUFFICIENT",
        closure_decision_ref=acceptance.decision_ref,
        final_state_version_ref=proof.execution_ref,
        final_state_freeze_ref=None,
        outstanding_requirements_disposed=True,
        outstanding_observations_disposed=True,
    )
    closure_record_ref = f"closure-record:{loop.cognitive_loop_ref}:v1"
    closure_record = LoopClosureRecordCandidateV1(
        loop_id=loop.cognitive_loop_ref,
        cognitive_concern_ref=request.concern_ref,
        final_disposition="COMPLETED",
        final_state_version_ref=proof.execution_ref,
        need_lineage_refs=(request.information_need_ref,),
        hypothesis_lineage_refs=proof.hypothesis_refs,
        evidence_refs=evidence_refs,
        current_world_refs=(proof.current_world_ref,) if proof.current_world_ref else (),
        closure_reason_ref="closure-reason:STOP_SUFFICIENT",
        trace_refs=(proof.execution_ref,),
        provenance_refs=(request.brain_request_ref, proof.execution_ref),
    )
    outcome = CognitiveOutcomeCandidateV1(
        outcome_ref=f"cognitive-outcome:{loop.cognitive_loop_ref}:v1",
        loop_id=loop.cognitive_loop_ref,
        cognitive_concern_ref=request.concern_ref,
        final_disposition="COMPLETED",
        final_state_version_ref=proof.execution_ref,
        closure_record_ref=closure_record_ref,
        evidence_refs=evidence_refs,
        sufficiency_reason_ref=proof.sufficiency_ref,
        current_world_refs=(proof.current_world_ref,) if proof.current_world_ref else (),
        trace_refs=(proof.execution_ref,),
        provenance_refs=(request.brain_request_ref, proof.execution_ref),
    )
    assimilation = BrainAssimilationCandidateV1(
        assimilation_ref=f"brain-assimilation:{loop.cognitive_loop_ref}:v1",
        brain_subject_ref=request.brain_subject_ref,
        loop_id=loop.cognitive_loop_ref,
        cognitive_outcome_ref=outcome.outcome_ref,
        closure_record_ref=closure_record_ref,
        disposition="ACCEPT_AS_COGNITIVE_REFERENCE",
        source_state_version_ref=proof.execution_ref,
        trace_refs=(proof.execution_ref,),
        provenance_refs=(request.brain_request_ref, acceptance.decision_ref),
    )
    return assessment, acceptance, lifecycle, closure_record, outcome, assimilation, ()


def _case_a(execution_instance_ref: str) -> BrainCognitiveCaseResultV1:
    request = _build_request("CASE_A_SUFFICIENT_STOP", execution_instance_ref)
    need = _build_information_need(request)
    loop_ref = f"cognitive-loop:CASE_A_SUFFICIENT_STOP:{execution_instance_ref}"
    replay = build_case_a_replay_v1()[0]
    gateway, route, gateway_query = _route_for_brain(request, replay, "S01", "case-a:cycle-1")
    proof = route.cognitive_execution
    loop = BrainCognitiveLoopInstanceV1(
        cognitive_loop_ref=loop_ref,
        brain_request_ref=request.brain_request_ref,
        lifecycle_owner_ref=LOOP_LIFECYCLE_OWNER,
        information_need_ref=need.information_need_ref,
        cycle_count=1,
        execution_refs=(proof.execution_ref,) if proof else (),
    )
    closure = _build_closure(request, loop, proof)
    errors = tuple(closure[-1])
    if route.errors:
        errors += tuple(f"a_route:{item.code}" for item in route.errors)
    if gateway.errors:
        errors += tuple(f"gateway:{item.code}" for item in gateway.errors)
    return BrainCognitiveCaseResultV1(
        case_id="CASE_A_SUFFICIENT_STOP",
        title="sufficient cognition stops and closes",
        brain_request=request,
        information_need=need,
        loop_instance=loop,
        gateway_results=(gateway,),
        gateway_admission_queries=(gateway_query,),
        route_results=(route,),
        cognitive_proofs=(proof,) if proof else (),
        closure_assessment=closure[0],
        closure_acceptance=closure[1],
        lifecycle_closure=closure[2],
        closure_record=closure[3],
        cognitive_outcome=closure[4],
        assimilation_candidate=closure[5],
        negative_guards=dict(NEGATIVE_GUARDS),
        validation_errors=errors,
    )


def _case_b(execution_instance_ref: str) -> BrainCognitiveCaseResultV1:
    request = _build_request("CASE_B_GAP_REOBSERVE_REVISE_STOP", execution_instance_ref)
    need = _build_information_need(request)
    loop_ref = f"cognitive-loop:CASE_B_GAP_REOBSERVE_REVISE_STOP:{execution_instance_ref}"
    replay_a = build_case_b_cycle_1_replay_v1()
    gateway_a, route_a, gateway_query_a = _route_for_brain(request, replay_a, "S04", "case-b:cycle-1")
    proof_a = route_a.cognitive_execution
    replay_b = build_case_b_cycle_2_replay_v1(proof_a)
    gateway_b, route_b, gateway_query_b = _route_for_brain(request, replay_b, "S10", "case-b:cycle-2")
    proof_b = route_b.cognitive_execution
    proofs = tuple(item for item in (proof_a, proof_b) if item)
    loop = BrainCognitiveLoopInstanceV1(
        cognitive_loop_ref=loop_ref,
        brain_request_ref=request.brain_request_ref,
        lifecycle_owner_ref=LOOP_LIFECYCLE_OWNER,
        information_need_ref=need.information_need_ref,
        cycle_count=2,
        execution_refs=tuple(item.execution_ref for item in proofs),
    )
    closure = _build_closure(request, loop, proof_b)
    errors = list(closure[-1])
    if not proof_a or proof_a.sufficiency_status != "INSUFFICIENT" or not proof_a.information_gap_ref or not proof_a.reobservation_ref:
        errors.append("case_b:cycle_1_gap_reobservation_missing")
    if proof_a and proof_b:
        if replay_b.prior_information_gap_ref != proof_a.information_gap_ref:
            errors.append("case_b:gap_link_invalid")
        if replay_b.prior_reobservation_ref != proof_a.reobservation_ref:
            errors.append("case_b:reobservation_link_invalid")
        if replay_b.prior_next_cycle_ingress_ref != proof_a.next_cycle_ingress_ref:
            errors.append("case_b:next_cycle_ingress_link_invalid")
        if proof_b.hypothesis_revision_information_gap_ref != proof_a.information_gap_ref:
            errors.append("case_b:revision_gap_link_invalid")
        if proof_b.hypothesis_revision_reobservation_ref != proof_a.reobservation_ref:
            errors.append("case_b:revision_reobservation_link_invalid")
    for gateway in (gateway_a, gateway_b):
        if gateway.errors:
            errors.extend(f"gateway:{item.code}" for item in gateway.errors)
    for route in (route_a, route_b):
        if route.errors:
            errors.extend(f"a_route:{item.code}" for item in route.errors)
    return BrainCognitiveCaseResultV1(
        case_id="CASE_B_GAP_REOBSERVE_REVISE_STOP",
        title="insufficiency drives re-observation, revision, and closure",
        brain_request=request,
        information_need=need,
        loop_instance=loop,
        gateway_results=(gateway_a, gateway_b),
        gateway_admission_queries=(gateway_query_a, gateway_query_b),
        route_results=(route_a, route_b),
        cognitive_proofs=proofs,
        closure_assessment=closure[0],
        closure_acceptance=closure[1],
        lifecycle_closure=closure[2],
        closure_record=closure[3],
        cognitive_outcome=closure[4],
        assimilation_candidate=closure[5],
        negative_guards=dict(NEGATIVE_GUARDS),
        validation_errors=tuple(dict.fromkeys(errors)),
    )


def _negative_closure_probe_v1() -> Dict[str, Any]:
    """One narrow fail-closed check; no cognition or external capability."""
    request = _build_request("NEGATIVE_CLOSURE_WITHOUT_SUFFICIENCY", "negative-probe")
    loop = BrainCognitiveLoopInstanceV1(
        cognitive_loop_ref="cognitive-loop:negative-probe",
        brain_request_ref=request.brain_request_ref,
        lifecycle_owner_ref=LOOP_LIFECYCLE_OWNER,
        information_need_ref=request.information_need_ref,
        cycle_count=0,
        execution_refs=(),
    )
    closure = _build_closure(request, loop, None)
    rejected = closure[0] is None and closure[1] is None and "closure_requires_sufficient_cognition" in closure[-1]
    return {
        "fixture": "closure_without_sufficiency",
        "expected": "REJECTED",
        "rejected": rejected,
        "errors": list(closure[-1]),
    }


def run_brain_cognitive_case_v1(case_id: str, execution_instance_ref: str) -> BrainCognitiveCaseResultV1:
    if case_id == "CASE_A_SUFFICIENT_STOP":
        return _case_a(execution_instance_ref)
    if case_id == "CASE_B_GAP_REOBSERVE_REVISE_STOP":
        return _case_b(execution_instance_ref)
    raise ValueError(f"unknown_brain_cognitive_case:{case_id}")


def build_brain_closure_run_v1(execution_instance_ref: str = "terminal-session") -> Dict[str, Any]:
    cases = (
        _case_a(execution_instance_ref),
        _case_b(execution_instance_ref),
    )
    return {
        "phase": PHASE,
        "execution_instance_ref": execution_instance_ref,
        "responsibility_domain": BRAIN_RESPONSIBILITY_DOMAIN,
        "canonical_owner_status": BRAIN_CANONICAL_OWNER_STATUS,
        "cases": [_jsonable(case) for case in cases],
        "negative_test": _negative_closure_probe_v1(),
        "negative_guards": dict(NEGATIVE_GUARDS),
        "negative_guard_coverage": {
            guard: {
                "guard_present": True,
                "guard_runtime_covered": guard in NEGATIVE_GUARD_RUNTIME_COVERAGE,
                "coverage_kind": "DYNAMIC" if guard in NEGATIVE_GUARD_RUNTIME_COVERAGE else "STRUCTURAL_ONLY",
            }
            for guard in NEGATIVE_GUARDS
        },
        "deferred": [
            "live_runtime",
            "model_provider_invocation",
            "decision_task_action_execution",
            "memory_experience_knowledge_promotion",
            "field_mutation",
        ],
    }


__all__ = ["build_brain_closure_run_v1", "run_brain_cognitive_case_v1"]
