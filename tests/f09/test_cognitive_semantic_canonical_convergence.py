from __future__ import annotations

from dataclasses import replace

import pytest

from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_engine_v1 import (
    form_cognitive_semantic_judgment,
    validate_a_semantic_judgment_projection,
)
from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_types_v1 import (
    ASemanticDecisionContextV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    run_brain_cognitive_case_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.fixtures_v1 import (
    build_replay_inputs_v1,
    get_contrast_specs_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
    build_decision_handoff_run_v1,
)
from capabilities.midplatform.core.cognitive_flow.integration.dynamic_flow_semantic_compatibility_cutover_controlled.dynamic_flow_semantic_compatibility_fixture_v1 import (
    build_compatibility_run_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_static_validators_v1 import (
    validate_input_contract,
)
from capabilities.midplatform.core.execution_mode_v1 import CONTROLLED_REPLAY_RUNTIME
from capabilities.midplatform.permission_and_admission_manager.module.runtime_execution_grant_v1 import (
    OWNER as RUNTIME_AUTHORIZATION_OWNER,
)


def _ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _cstate_request() -> CognitiveStateFormationInputV1:
    return CognitiveStateFormationInputV1(
        scenario_id="F09",
        context_refs=(_ref("Context", "context:f09"),),
        pcn_refs=(_ref("PCN", "pcn:f09"),),
        intent_refs=(_ref("Intent", "intent:f09"),),
        field_refs=(_ref("Field", "field:f09"),),
        observation_refs=(_ref("Observation", "observation:f09"),),
        evidence_refs=(_ref("Evidence", "evidence:f09"),),
        goal_refs=(_ref("Goal", "goal:f09"),),
        concern_refs=(_ref("Concern", "concern:f09"),),
        information_need_refs=(_ref("Need", "need:f09"),),
        task_refs=(_ref("Task", "task:f09"),),
        role_refs=(_ref("Role", "role:f09"),),
        relation_refs=(_ref("Field", "relation:f09"),),
        candidate_only=True,
        synthetic_only=True,
    )


def _a_context(*, contradiction_refs=()) -> ASemanticDecisionContextV1:
    return ASemanticDecisionContextV1(
        work_ref="work:f09",
        concern_ref="concern:f09",
        a_grant_ref="grant:a:f09",
        source_state_version_ref="state:f09:v1",
        goal_refs=("goal:f09",),
        intent_refs=("intent:f09",),
        role_refs=("role:f09",),
        perspective_refs=("perspective:f09",),
        field_refs=("field:f09",),
        context_refs=("context:f09",),
        current_world_refs=("current-world:f09",),
        task_behavior_refs=("task:f09",),
        emotion_modulation_refs=(),
        experience_refs=(),
        safety_refs=(),
        permission_refs=(),
        resource_envelope_refs=(),
        evidence_refs=("evidence:f09",),
        prior_need_refs=(),
        prior_hypothesis_refs=(),
        prior_requirement_refs=("information:f09",),
        trace_refs=("trace:f09",),
        provenance_refs=("provenance:f09",),
        contradiction_refs=contradiction_refs,
    )


def _a_judgment(
    *,
    sufficient: bool = True,
    evidence_ref: str = "evidence:f09",
    conflict_refs=(),
):
    return form_cognitive_semantic_judgment(
        context=_a_context(contradiction_refs=conflict_refs),
        source_snapshot_ref="state-vector:f09:v1",
        current_world_ref="current-world:f09",
        attention_refs=("attention:f09",),
        evidence_refs=(evidence_ref,),
        required_information_refs=("information:f09",),
        available_information_refs=("information:f09",) if sufficient else (),
        requirement_establishment_status="ESTABLISHED",
        conflict_refs=conflict_refs,
    )


def test_t01_cstate_is_presemantic_snapshot_only() -> None:
    engine = CognitiveStateFormationEngineV1()
    engine._build_hypothesis_projection = lambda *_args: (_ for _ in ()).throw(
        AssertionError("canonical CState invoked hypothesis formation")
    )
    engine._build_cognitive_loop_projections = lambda *_args: (_ for _ in ()).throw(
        AssertionError("canonical CState invoked semantic loop formation")
    )
    output = engine.run_case(
        replace(
            _cstate_request(),
            execution_mode=CONTROLLED_REPLAY_RUNTIME,
            synthetic_only=False,
            replay_input_ref="replay:f09",
            execution_ref="execution:f09",
        )
    )
    assert output.formation_role == "SNAPSHOT_FORMATION"
    assert output.semantic_projection_only is True
    assert output.semantic_authority is False
    assert output.cognitive_hypotheses == ()
    assert output.sufficiency_candidate is None
    assert output.information_gap_candidate is None
    assert output.stop_candidate is None
    assert output.current_world_candidate.conflict_refs == ()


def test_t02_cstate_sufficiency_is_not_canonical() -> None:
    engine = CognitiveStateFormationEngineV1()
    compatibility = engine.run_case(_cstate_request())
    canonical = engine.run_case(
        replace(
            _cstate_request(),
            execution_mode=CONTROLLED_REPLAY_RUNTIME,
            synthetic_only=False,
            replay_input_ref="replay:f09",
            execution_ref="execution:f09",
        )
    )
    assert compatibility.sufficiency_candidate is not None
    assert canonical.sufficiency_candidate is None


def test_t03_cstate_stop_is_projection_only() -> None:
    engine = CognitiveStateFormationEngineV1()
    compatibility = engine.run_case(_cstate_request())
    canonical = engine.run_case(
        replace(
            _cstate_request(),
            execution_mode=CONTROLLED_REPLAY_RUNTIME,
            synthetic_only=False,
            replay_input_ref="replay:f09",
            execution_ref="execution:f09",
        )
    )
    assert compatibility.stop_candidate is None or compatibility.semantic_projection_only is True
    assert canonical.stop_candidate is None


def test_t04_a_forms_hypothesis() -> None:
    judgment = _a_judgment(evidence_ref="evidence:new")
    assert judgment.semantic_owner_ref == "A_REASONING_ROLE"
    assert judgment.hypothesis_candidates[0].semantic_owner_ref == "A_REASONING_ROLE"
    assert judgment.hypothesis_candidates[0].supporting_evidence_refs == ("evidence:new",)
    assert judgment.hypothesis_candidates[0].source_snapshot_ref == "state-vector:f09:v1"


def test_t05_a_forms_cognitive_sufficiency() -> None:
    assert _a_judgment().sufficiency_status == "SUFFICIENT"
    assert _a_judgment(sufficient=False).sufficiency_status == "INSUFFICIENT"


def test_t06_a_forms_local_cognitive_disposition() -> None:
    judgment = _a_judgment()
    assert judgment.local_disposition == "STOP_SUFFICIENT"
    assert judgment.local_disposition_ref
    assert _a_judgment(sufficient=False).local_disposition == "ACQUIRE_INFORMATION"


def test_t19_structured_conflict_reaches_a_without_truth_promotion() -> None:
    judgment = _a_judgment(conflict_refs=("contradiction:S02",))
    hypothesis = judgment.hypothesis_candidates[0]
    assert hypothesis.conflict_refs == ("contradiction:S02",)
    assert hypothesis.state == "CONTESTED"
    assert judgment.sufficiency_status == "SUFFICIENT"
    assert judgment.local_disposition == "STOP_SUFFICIENT"
    assert judgment.current_world_truth_declared is False
    assert hypothesis.truth_declared is False
    assert hypothesis.world_truth_declared is False


def test_t20_f08_rejects_malformed_structured_conflict() -> None:
    with pytest.raises(ValueError, match="A_CONTRACT_REJECTION:context.contradiction_refs_must_be_tuple"):
        _a_judgment(conflict_refs=["contradiction:S02"])


def test_t21_case_b_binds_cycle_two_revision_to_a() -> None:
    case = run_brain_cognitive_case_v1("CASE_B_GAP_REOBSERVE_REVISE_STOP", "f09-revision")
    assert len(case.cognitive_proofs) == 2
    first, second = case.cognitive_proofs
    assert first.information_gap_ref
    assert first.reobservation_ref
    second_judgment = second.cognitive_semantic_judgment
    assert second_judgment.prior_information_gap_ref == first.information_gap_ref
    assert second_judgment.prior_reobservation_ref == first.reobservation_ref
    assert second.prior_next_cycle_ingress_ref == first.next_cycle_ingress_ref
    assert set(first.admitted_evidence_refs).isdisjoint(second.admitted_evidence_refs)
    assert second_judgment.local_disposition == "STOP_SUFFICIENT"
    assert second_judgment.reconsideration_ref
    assert second_judgment.sufficiency_status == "SUFFICIENT"
    assert second_judgment.missing_information_refs == ()
    assert second_judgment.information_gap_ref is None
    assert second_judgment.reobservation_ref is None
    assert second.hypothesis_revision_ref == second_judgment.reconsideration_ref
    assert second.hypothesis_revision_owner_ref == "A_REASONING_ROLE"
    assert case.closure_assessment is not None
    assert case.closure_acceptance is not None
    assert case.lifecycle_closure is not None
    assert case.closure_record is not None
    assert case.assimilation_candidate is not None
    assert case.validation_errors == ()
    assert case.closure_acceptance.accepted is True
    assert case.lifecycle_closure.target_closure_state == "CLOSED"
    assert second.world_truth_declared is False
    assert second.action_execution is False


def test_t21_reconsideration_history_does_not_block_resolved_closure() -> None:
    case = run_brain_cognitive_case_v1("CASE_B_GAP_REOBSERVE_REVISE_STOP", "f09-resolved-closure")
    assert case.cognitive_proofs[-1].cognitive_semantic_judgment.reconsideration_ref
    assert case.cognitive_proofs[-1].sufficiency_status == "SUFFICIENT"
    assert case.cognitive_proofs[-1].cognitive_semantic_judgment.missing_information_refs == ()
    assert case.closure_record is not None


def test_t21_reconsideration_history_does_not_bypass_current_unresolved_state() -> None:
    from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
        _build_closure,
    )

    case = run_brain_cognitive_case_v1("CASE_B_GAP_REOBSERVE_REVISE_STOP", "f09-unresolved-revision")
    first, second = case.cognitive_proofs
    unresolved_judgment = form_cognitive_semantic_judgment(
        context=_a_context(),
        source_snapshot_ref="state-vector:f09:unresolved:v1",
        current_world_ref="current-world:f09",
        attention_refs=("attention:f09",),
        evidence_refs=(),
        required_information_refs=("information:f09",),
        available_information_refs=(),
        requirement_establishment_status="ESTABLISHED",
        prior_information_gap_ref=first.information_gap_ref,
        prior_reobservation_ref=first.reobservation_ref,
    )
    assert unresolved_judgment.reconsideration_ref
    assert unresolved_judgment.sufficiency_status == "INSUFFICIENT"
    assert unresolved_judgment.information_gap_ref is not None
    unresolved_proof = replace(
        second,
        hypothesis_refs=tuple(item.hypothesis_ref for item in unresolved_judgment.hypothesis_candidates),
        sufficiency_ref=unresolved_judgment.sufficiency_ref,
        sufficiency_status=unresolved_judgment.sufficiency_status,
        information_gap_ref=unresolved_judgment.information_gap_ref,
        information_gap_availability="PRESENT",
        stop_ref=unresolved_judgment.local_disposition_ref,
        stop_availability="ABSENT",
        hypothesis_revision_ref=unresolved_judgment.reconsideration_ref,
        hypothesis_revision_information_gap_ref=unresolved_judgment.prior_information_gap_ref,
        hypothesis_revision_reobservation_ref=unresolved_judgment.prior_reobservation_ref,
        semantic_judgment_ref=unresolved_judgment.judgment_ref,
        semantic_provenance_refs=unresolved_judgment.provenance_refs,
        cognitive_semantic_judgment=unresolved_judgment,
    )
    closure = _build_closure(case.brain_request, case.loop_instance, unresolved_proof)
    assert closure[0] is None
    assert closure[1] is None
    assert closure[-1] == ("closure_requires_sufficient_cognition",)


def test_t22_consumer_rejects_unbound_revision_projection() -> None:
    case = run_brain_cognitive_case_v1("CASE_B_GAP_REOBSERVE_REVISE_STOP", "f09-forged-revision")
    proof = case.cognitive_proofs[-1]
    judgment = proof.cognitive_semantic_judgment
    errors = validate_a_semantic_judgment_projection(
        judgment,
        semantic_owner_ref=proof.semantic_owner_ref,
        semantic_judgment_ref=proof.semantic_judgment_ref,
        hypothesis_refs=proof.hypothesis_refs,
        sufficiency_ref=proof.sufficiency_ref,
        sufficiency_status=proof.sufficiency_status,
        information_gap_ref=proof.information_gap_ref,
        reobservation_ref=proof.reobservation_ref,
        hypothesis_revision_ref="hypothesis-revision:forged",
        hypothesis_revision_information_gap_ref=proof.hypothesis_revision_information_gap_ref,
        hypothesis_revision_reobservation_ref=proof.hypothesis_revision_reobservation_ref,
        stop_ref=proof.stop_ref,
        semantic_provenance_refs=proof.semantic_provenance_refs,
        conflict_refs=proof.conditioned_conflict_refs,
    )
    assert "a_judgment_revision_mismatch" in errors


def test_t23_gateway_structured_contradiction_binds_to_a() -> None:
    spec = next(item for item in get_contrast_specs_v1() if item.contrast_id == "conflicting-evidence")
    gateway_request, route_request = build_replay_inputs_v1(spec)
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    route_request = replace(
        route_request,
        ingress=ARouteIngressRefsV1(
            observation_refs=(gateway.observation.observation_id,),
            perception_refs=tuple(item.evidence_id for item in gateway.evidence),
            field_refs=route_request.ingress.field_refs,
            relation_refs=route_request.ingress.relation_refs,
        ),
        replay_admission=gateway.replay_admission,
    )
    route = ARouteOrchestrationEngineV1().run_case(route_request)
    proof = route.cognitive_execution
    assert gateway.replay_admission.contradiction_refs == (gateway.trace.contradiction_lineage[0],)
    assert proof.conditioned_conflict_refs == gateway.replay_admission.contradiction_refs
    assert proof.cognitive_semantic_judgment.hypothesis_candidates[0].state == "CONTESTED"


def test_t07_route_consumes_a_judgment_after_snapshot() -> None:
    case = run_brain_cognitive_case_v1("CASE_A_SUFFICIENT_STOP", "f09-route")
    route = case.route_results[0]
    assert route.cognitive_execution is not None
    assert route.cognitive_execution.semantic_owner_ref == "A_REASONING_ROLE"
    assert route.cognitive_execution.cognitive_semantic_judgment is not None
    assert route.cognitive_execution.sufficiency_candidate is None
    assert route.cognitive_execution.cognitive_semantic_judgment.sufficiency_ref == route.cognitive_execution.sufficiency_ref


def test_t08_decision_facing_result_preserves_a_provenance() -> None:
    summary = build_decision_handoff_run_v1("f09-handoff")
    case = next(item for item in summary["cases"] if item["case_id"] == "CASE_A_SUFFICIENT_STOP")
    handoff = case["decision_handoff"]
    assert handoff["semantic_owner_ref"] == "A_REASONING_ROLE"
    assert handoff["semantic_judgment_ref"]
    assert handoff["semantic_judgment_ref"] == case["cognitive_case"]["cognitive_proofs"][-1]["semantic_judgment_ref"]


def test_t09_brain_closure_consumes_a_disposition() -> None:
    case = run_brain_cognitive_case_v1("CASE_A_SUFFICIENT_STOP", "f09-brain")
    proof = case.cognitive_proofs[-1]
    assert proof.semantic_owner_ref == "A_REASONING_ROLE"
    assert proof.cognitive_semantic_judgment.local_disposition == "STOP_SUFFICIENT"
    assert case.closure_record is not None


def test_t10_loop_bridge_remains_mechanical() -> None:
    from capabilities.midplatform.core.cognitive_flow.integration.a_owned_semantic_decision_loop_bridge_controlled.a_owned_semantic_decision_adapter_v1 import (
        build_a_owned_semantic_decision_run_v1,
    )

    result = build_a_owned_semantic_decision_run_v1()
    assert result["summary"]["key_guards"]["loop_has_no_semantic_authority"] is True


def test_t11_a_cannot_declare_world_or_relationship_truth() -> None:
    judgment = _a_judgment()
    assert judgment.relationship_truth_mutation is False
    assert judgment.field_truth_declared is False
    assert judgment.current_world_truth_declared is False


def test_t12_dynamic_flow_is_a_compatibility_input() -> None:
    results = build_compatibility_run_v1()
    assert results
    assert all(not item.compatibility_output.semantic_authority for item in results)
    assert all(item.interpretation.a_decisions.compatibility_wrapper_only for item in results)


def test_t13_f08_malformed_structure_stays_rejected() -> None:
    request = replace(_cstate_request(), context_refs="context:f09")
    assert any("context_refs" in error for error in validate_input_contract(request))


@pytest.mark.parametrize(
    ("field", "value"),
    (
        ("attention_refs", "attention:f09"),
        ("evidence_refs", b"evidence:f09"),
        ("required_information_refs", ["information:f09"]),
        ("available_information_refs", {"information:f09": True}),
        ("prior_hypothesis_refs", ("hypothesis:f09", 7)),
        ("source_snapshot_ref", 7),
    ),
)
def test_t16_a_rejects_malformed_entry_shapes(field, value) -> None:
    kwargs = {
        "context": _a_context(),
        "source_snapshot_ref": "state-vector:f09:v1",
        "current_world_ref": "current-world:f09",
        "attention_refs": ("attention:f09",),
        "evidence_refs": ("evidence:f09",),
        "required_information_refs": ("information:f09",),
        "available_information_refs": ("information:f09",),
        "requirement_establishment_status": "ESTABLISHED",
    }
    kwargs[field] = value
    with pytest.raises(ValueError, match="A_CONTRACT_REJECTION"):
        form_cognitive_semantic_judgment(**kwargs)


@pytest.mark.parametrize(
    "forgery", ("owner", "ref", "sufficiency", "disposition", "provenance")
)
def test_t17_controlled_consumers_reject_forged_a_judgment(forgery) -> None:
    from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
        build_cognitive_decision_handoff_candidate_v1,
    )

    case = run_brain_cognitive_case_v1("CASE_A_SUFFICIENT_STOP", "f09-forgery")
    proof = case.cognitive_proofs[-1]
    judgment = proof.cognitive_semantic_judgment
    if forgery == "owner":
        forged = replace(proof, semantic_owner_ref="caller-label")
    elif forgery == "ref":
        forged = replace(proof, semantic_judgment_ref="a-semantic-judgment:forged")
    elif forgery == "sufficiency":
        forged = replace(
            proof,
            cognitive_semantic_judgment=replace(judgment, sufficiency_status="INSUFFICIENT"),
        )
    elif forgery == "disposition":
        forged = replace(
            proof,
            cognitive_semantic_judgment=replace(
                judgment,
                local_disposition="ACQUIRE_INFORMATION",
                local_disposition_ref=None,
            ),
        )
    else:
        forged = replace(
            proof,
            cognitive_semantic_judgment=replace(
                judgment,
                provenance_refs=("provenance:forged",),
            ),
        )
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(case.__dict__, forged)
    assert handoff is None
    expected_error = (
        "decision_handoff_requires_a_owned_semantic_judgment"
        if forgery == "owner"
        else "decision_handoff_rejects_unbound_a_judgment"
    )
    assert expected_error in errors


def test_t18_brain_closure_rejects_mismatched_a_judgment() -> None:
    from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
        _build_closure,
    )

    case = run_brain_cognitive_case_v1("CASE_A_SUFFICIENT_STOP", "f09-brain-forgery")
    proof = case.cognitive_proofs[-1]
    forged = replace(
        proof,
        cognitive_semantic_judgment=replace(
            proof.cognitive_semantic_judgment,
            local_disposition="ACQUIRE_INFORMATION",
            local_disposition_ref=None,
        ),
    )
    closure = _build_closure(case.brain_request, case.loop_instance, forged)
    assert closure[-1] == ("closure_requires_sufficient_cognition",)


def test_t14_f05_decision_handoff_keeps_gateway_admission_boundary() -> None:
    summary = build_decision_handoff_run_v1("f09-f05")
    case = next(item for item in summary["cases"] if item["case_id"] == "CASE_A_SUFFICIENT_STOP")
    assert case["decision_governance_consumed"] is True
    assert case["decision_handoff"]["canonical_gateway_admission_result"] is not None


def test_t15_f07_runtime_authorization_owner_is_unchanged() -> None:
    assert RUNTIME_AUTHORIZATION_OWNER == "Permission / Admission Manager"
