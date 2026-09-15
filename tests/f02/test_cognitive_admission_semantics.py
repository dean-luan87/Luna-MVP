from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

from capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.engine_v1 import (
    CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1,
)
from capabilities.evaluation.cognitive_requirement_alternative_satisfaction_basis.fixtures_v1 import (
    build_alternative_satisfaction_cases_v1,
)
from capabilities.evaluation.full_end_to_end_cognitive_logic_conformance_regression.fixtures_v1 import (
    ContrastSpecV1,
    build_replay_inputs_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.observation_gateway.observation_gateway_engine_v1 import (
    ObservationGatewayEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_core_types_v1 import (
    ARouteIngressRefsV1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import GoalContextV1
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_engine_v1 import (
    ARouteRequiredCognitiveConditionFormationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    CurrentCognitiveSituationV1,
    GovernedObjectiveConditionRuleV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.brain_cognitive_loop_closure_assimilation_controlled.brain_cognitive_loop_closure_assimilation_engine_v1 import (
    _build_closure,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_core_types_v1 import (
    CognitiveReferenceSemanticV1,
    SourceRefV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_engine_v1 import (
    CognitiveStateFormationEngineV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
    requirement_establishment_from_condition_formation_status_v1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_state_formation_io_types_v1 import (
    CognitiveStateFormationInputV1,
)
from capabilities.midplatform.core.cognitive_flow.integration.cognitive_result_to_decision_governance_controlled_handoff.engine_v1 import (
    build_cognitive_decision_handoff_candidate_v1,
)
from capabilities.midplatform.core.execution_mode_v1 import (
    CONTROLLED_REPLAY_RUNTIME,
    LIVE_RUNTIME,
)


def _ref(owner: str, value: str) -> SourceRefV1:
    return SourceRefV1(owner, value, "v1", f"trace:{value}", f"provenance:{value}")


def _request(
    *,
    establishment_status: str = "NOT_ESTABLISHED",
    establishment_ref: str | None = None,
    establishment_basis: str | None = None,
    required: tuple[str, ...] = (),
    available: tuple[str, ...] = (),
    mode: str = CONTROLLED_REPLAY_RUNTIME,
    semantic_refs: tuple[CognitiveReferenceSemanticV1, ...] = (),
) -> CognitiveStateFormationInputV1:
    return CognitiveStateFormationInputV1(
        scenario_id="F02",
        context_refs=(_ref("Context", "context:f02"),),
        pcn_refs=(_ref("PCN", "pcn:f02"),),
        intent_refs=(_ref("Intent", "intent:f02"),),
        field_refs=(_ref("Field", "field:f02"),),
        observation_refs=(_ref("Observation", "observation:f02"),),
        evidence_refs=(_ref("Evidence", "evidence:f02"),),
        task_refs=(_ref("Task", "task:f02"),),
        role_refs=(_ref("Role", "role:f02"),),
        goal_refs=(_ref("Goal", "goal:f02"),),
        concern_refs=(_ref("Concern", "concern:f02"),),
        information_need_refs=(_ref("Need", "need:f02"),),
        relation_refs=(_ref("Field", "relation:f02"),),
        required_information_refs=required,
        available_information_refs=available,
        requirement_establishment_status=establishment_status,
        requirement_establishment_ref=establishment_ref,
        requirement_establishment_basis=establishment_basis,
        semantic_reference_values=semantic_refs,
        execution_mode=mode,
        synthetic_only=False,
        candidate_only=True,
        replay_input_ref="replay:f02" if mode == CONTROLLED_REPLAY_RUNTIME else None,
        runtime_observation_ref="runtime:f02" if mode == LIVE_RUNTIME else None,
        execution_ref="execution:f02",
    )


def _established_request(**kwargs: object) -> CognitiveStateFormationInputV1:
    params = {
        "required": ("information:f02",),
        "available": ("information:f02",),
    }
    params.update(kwargs)
    request = _request(
        establishment_status="ESTABLISHED",
        establishment_ref="required-conditions:f02:v1",
        establishment_basis="ACTIVE_REQUIRED_CONDITIONS",
        **params,
    )
    required = tuple(request.required_information_refs)
    available = tuple(request.available_information_refs)
    goal_ref = request.goal_refs[0].source_ref
    proof = ARouteRequiredCognitiveConditionFormationEngineV1().form(
        ARouteRequiredCognitiveConditionFormationRequestV1(
            goal_context=GoalContextV1(
                goal_ref=goal_ref,
                primary_goal=goal_ref,
                secondary_goal_refs=(),
                success_condition_refs=(),
                stop_condition_refs=(),
                provenance={"source": "f02-test-fixture"},
                trace="trace:f02:required-condition",
            ),
            governed_condition_rules=(
                GovernedObjectiveConditionRuleV1(
                    rule_ref="rule:f02:required-condition",
                    condition_ref="condition:f02:required-condition",
                    objective_refs=(goal_ref,),
                    satisfaction_coverage_refs=required,
                    source_refs=("governance:f02:test",),
                    provenance_refs=("provenance:f02:test",),
                ),
            ),
            current_situation=CurrentCognitiveSituationV1(
                current_cognitive_coverage_refs=available,
            ),
            formation_trace_ref="trace:f02:required-condition:v1",
        )
    )
    return replace(request, required_cognitive_condition_formation_result=proof)


def _no_active_establishment_proof():
    goal_ref = "goal:f02"
    return ARouteRequiredCognitiveConditionFormationEngineV1().form(
        ARouteRequiredCognitiveConditionFormationRequestV1(
            goal_context=GoalContextV1(
                goal_ref=goal_ref,
                primary_goal=goal_ref,
                secondary_goal_refs=(),
                success_condition_refs=(),
                stop_condition_refs=(),
                provenance={"source": "f02-test-fixture"},
                trace="trace:f02:no-active",
            ),
            governed_condition_rules=(),
            current_situation=CurrentCognitiveSituationV1(),
            formation_trace_ref="trace:f02:no-active:v1",
        )
    )


def _run_full_route(spec: ContrastSpecV1, *, forged_replay: bool = False):
    gateway_request, route_request = build_replay_inputs_v1(spec)
    if forged_replay:
        replay = replace(
            gateway_request.replay_input,
            requirement_establishment_status="ESTABLISHED",
            requirement_establishment_ref="forged:canonical-looking-ref",
            requirement_establishment_basis="NO_ACTIVE_REQUIRED_CONDITIONS",
            required_cognitive_condition_formation_result=None,
        )
        gateway_request = replace(gateway_request, replay_input=replay)
    gateway = ObservationGatewayEngineV1().run_case(gateway_request)
    route_request = replace(
        route_request,
        ingress=ARouteIngressRefsV1(
            observation_refs=(gateway.observation.observation_id,) if gateway.observation else (),
            perception_refs=tuple(item.evidence_id for item in gateway.evidence),
            field_refs=route_request.ingress.field_refs,
            relation_refs=route_request.ingress.relation_refs,
        ),
        replay_admission=gateway.replay_admission,
    )
    return gateway, ARouteOrchestrationEngineV1().run_case(route_request)


def _semantic_request(*, mode: str = CONTROLLED_REPLAY_RUNTIME, suffix: str = "f02"):
    refs = (
        CognitiveReferenceSemanticV1(f"role:{suffix}", "ROLE", "workspace-owner"),
        CognitiveReferenceSemanticV1(f"goal:{suffix}", "TARGET", "document"),
        CognitiveReferenceSemanticV1(f"task:{suffix}", "TASK_LABEL", "find-document"),
        CognitiveReferenceSemanticV1(f"evidence:{suffix}", "EVIDENCE_TOPIC", "document"),
    )
    request = replace(
        _established_request(mode=mode, semantic_refs=refs),
        role_refs=(_ref("Role", f"role:{suffix}"),),
        goal_refs=(_ref("Goal", f"goal:{suffix}"),),
        task_refs=(_ref("Task", f"task:{suffix}"),),
        evidence_refs=(_ref("Evidence", f"evidence:{suffix}"),),
    )
    return request


def test_omitted_establishment_defaults_to_not_established() -> None:
    output = CognitiveStateFormationEngineV1().run_case(_request())
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.sufficiency_candidate.requirement_establishment_status == "NOT_ESTABLISHED"
    assert output.stop_candidate is None


def test_not_established_empty_refs_is_not_sufficient_or_stop() -> None:
    output = CognitiveStateFormationEngineV1().run_case(_request(required=(), available=()))
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.stop_candidate is None


def test_explicit_no_active_requirements_can_be_sufficient() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        replace(
            _request(
            establishment_status="ESTABLISHED",
            establishment_ref="required-conditions:none:f02",
            establishment_basis="NO_ACTIVE_REQUIRED_CONDITIONS",
            ),
            required_cognitive_condition_formation_result=_no_active_establishment_proof(),
        )
    )
    assert output.sufficiency_candidate.status == "SUFFICIENT"
    assert output.stop_candidate is not None


def test_established_unmet_requirement_is_insufficient_without_stop() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _established_request(required=("information:f02",), available=())
    )
    assert output.sufficiency_candidate.status == "INSUFFICIENT"
    assert output.stop_candidate is None


def test_unavailable_withheld_and_invalid_are_fail_closed() -> None:
    for status in ("UNAVAILABLE", "WITHHELD", "INVALID"):
        output = CognitiveStateFormationEngineV1().run_case(
            _request(
                establishment_status=status,
                establishment_ref=None,
                required=("information:f02",),
                available=("information:f02",),
            )
        )
        assert output.sufficiency_candidate.status in {"UNKNOWN", "WITHHELD"}
        assert output.stop_candidate is None


def test_valid_established_satisfied_path_remains_sufficient_and_stops() -> None:
    output = CognitiveStateFormationEngineV1().run_case(_established_request())
    assert output.sufficiency_candidate.status == "SUFFICIENT"
    assert output.stop_candidate is not None


def test_handoff_rejects_provisional_sufficiency_without_establishment() -> None:
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        {
            "case_id": "F02",
            "brain_request": {"goal_ref": "g", "intent_ref": "i", "concern_ref": "c", "context_ref": "x"},
            "information_need": {"information_need_ref": "n"},
            "loop_instance": {"cognitive_loop_ref": "l"},
        },
        {
            "sufficiency_status": "SUFFICIENT",
            "sufficiency_ref": "s",
            "stop_ref": "stop",
            "current_world_ref": "world",
            "hypothesis_refs": ["h"],
            "ingress_refs": ["e"],
        },
    )
    assert handoff is None
    assert errors == ("decision_handoff_requires_requirement_establishment",)


def test_brain_closure_rejects_sufficiency_without_establishment() -> None:
    proof = SimpleNamespace(
        sufficiency_status="SUFFICIENT",
        requirement_establishment_status="NOT_ESTABLISHED",
        requirement_establishment_ref=None,
        sufficiency_ref="s",
    )
    result = _build_closure(None, None, proof)
    assert result[-1] == ("closure_requires_sufficient_cognition",)


def test_opaque_ref_rename_preserves_typed_semantics() -> None:
    first = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="a"))
    second = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="b"))
    assert first.attention_selection_candidate.conflicting_focus == second.attention_selection_candidate.conflicting_focus
    assert first.evidence_relevance_candidates[0].relevance_state == second.evidence_relevance_candidates[0].relevance_state
    assert first.cognitive_hypotheses[0].state == second.cognitive_hypotheses[0].state
    assert first.cognitive_hypotheses[0].hypothesis_statement_candidate == second.cognitive_hypotheses[0].hypothesis_statement_candidate
    assert first.current_world_candidate.world_state_kind_candidate == second.current_world_candidate.world_state_kind_candidate


def test_live_and_replay_preserve_typed_semantic_result() -> None:
    replay = CognitiveStateFormationEngineV1().run_case(_semantic_request(mode=CONTROLLED_REPLAY_RUNTIME, suffix="replay"))
    live = CognitiveStateFormationEngineV1().run_case(_semantic_request(mode=LIVE_RUNTIME, suffix="live"))
    assert replay.sufficiency_candidate.status == live.sufficiency_candidate.status == "SUFFICIENT"
    assert replay.cognitive_hypotheses[0].state == live.cognitive_hypotheses[0].state
    assert replay.current_world_candidate.world_state_kind_candidate == live.current_world_candidate.world_state_kind_candidate


def test_scenario_12_alternative_basis_semantics_remain_intact() -> None:
    result = CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1().run()
    cases = {case["case_id"]: case for case in result["cases"]}
    assert cases["ALTERNATIVE_BASIS_A"]["result"]["status"] == "CONDITIONS_FORMED"
    assert cases["ALTERNATIVE_BASIS_A"]["result"]["satisfied_condition_refs"]
    assert cases["MULTIPLE_ALTERNATIVE_BASES_COVERED"]["result"]["satisfied_condition_refs"]
    assert not cases["NO_ALTERNATIVE_BASIS_COVERED"]["result"]["satisfied_condition_refs"]


def test_required_condition_status_mapping_is_explicit() -> None:
    assert requirement_establishment_from_condition_formation_status_v1("CONDITIONS_FORMED") == (
        "ESTABLISHED",
        "ACTIVE_REQUIRED_CONDITIONS",
    )
    assert requirement_establishment_from_condition_formation_status_v1("NO_ACTIVE_REQUIRED_CONDITIONS") == (
        "ESTABLISHED",
        "NO_ACTIVE_REQUIRED_CONDITIONS",
    )


def test_unavailable_requirement_formation_is_not_sufficient() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _request(
            establishment_status="UNAVAILABLE",
            required=("information:f02",),
            available=("information:f02",),
        )
    )
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.stop_candidate is None


def test_withheld_requirement_formation_is_not_sufficient() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _request(
            establishment_status="WITHHELD",
            required=("information:f02",),
            available=("information:f02",),
        )
    )
    assert output.sufficiency_candidate.status == "WITHHELD"
    assert output.stop_candidate is None


def test_invalid_requirement_formation_is_not_sufficient() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _request(
            establishment_status="INVALID",
            required=("information:f02",),
            available=("information:f02",),
        )
    )
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.stop_candidate is None


def test_empty_requirements_without_no_active_proof_fail_closed() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _request(
            establishment_status="ESTABLISHED",
            establishment_ref="required-conditions:f02:v1",
            establishment_basis="ACTIVE_REQUIRED_CONDITIONS",
        )
    )
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.sufficiency_candidate.requirement_establishment_status == "NOT_ESTABLISHED"
    assert output.stop_candidate is None


def test_decision_handoff_rejects_unknown_sufficiency() -> None:
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        {
            "case_id": "F02-UNKNOWN",
            "brain_request": {"goal_ref": "g", "intent_ref": "i", "concern_ref": "c", "context_ref": "x"},
            "information_need": {"information_need_ref": "n"},
            "loop_instance": {"cognitive_loop_ref": "l"},
        },
        {
            "sufficiency_status": "UNKNOWN",
            "sufficiency_ref": "s",
            "stop_ref": None,
            "current_world_ref": "world",
            "hypothesis_refs": ["h"],
            "ingress_refs": ["e"],
        },
    )
    assert handoff is None
    assert errors == ("decision_handoff_requires_sufficient_cognition",)


def test_opaque_ref_rename_preserves_attention_semantics() -> None:
    first = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="attention-a"))
    second = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="attention-b"))
    assert first.attention_selection_candidate.selected_attention_refs == second.attention_selection_candidate.selected_attention_refs
    assert first.attention_selection_candidate.conflicting_focus == second.attention_selection_candidate.conflicting_focus


def test_opaque_ref_rename_preserves_hypothesis_semantics() -> None:
    first = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="hypothesis-a"))
    second = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="hypothesis-b"))
    assert first.cognitive_hypotheses[0].state == second.cognitive_hypotheses[0].state


def test_opaque_task_and_goal_ref_rename_preserves_target_semantics() -> None:
    first = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="task-goal-a"))
    second = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="task-goal-b"))
    assert first.current_world_candidate.world_state_kind_candidate == second.current_world_candidate.world_state_kind_candidate
    assert first.cognitive_hypotheses[0].hypothesis_statement_candidate == second.cognitive_hypotheses[0].hypothesis_statement_candidate


def test_opaque_relation_ref_rename_preserves_relation_semantics() -> None:
    first = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="relation-a"))
    second = CognitiveStateFormationEngineV1().run_case(_semantic_request(suffix="relation-b"))
    assert first.relation_interpretation_candidates[0].relevance_state == second.relation_interpretation_candidates[0].relevance_state


def test_scenario_12_single_alternative_preserves_requirement_meaning() -> None:
    result = CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1().run()
    cases = {case["case_id"]: case for case in result["cases"]}
    satisfied = cases["ALTERNATIVE_BASIS_A"]["result"]["satisfied_condition_refs"]
    assert len(satisfied) == 1


def test_scenario_12_multiple_alternatives_do_not_merge_facts() -> None:
    result = CognitiveRequirementAlternativeSatisfactionBasisEvaluationEngineV1().run()
    cases = {case["case_id"]: case for case in result["cases"]}
    satisfied = cases["MULTIPLE_ALTERNATIVE_BASES_COVERED"]["result"]["satisfied_condition_refs"]
    assert len(satisfied) == 1


def test_candidate_aggregate_cannot_fabricate_establishment() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _request(
            required=("information:f02",),
            available=("information:f02",),
        )
    )
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.sufficiency_candidate.requirement_establishment_status == "NOT_ESTABLISHED"


def test_gateway_route_rejects_caller_forged_establishment_authority() -> None:
    spec = ContrastSpecV1(
        "f02-forged-authority",
        "F02_FORGED_AUTHORITY",
        "S01",
        "role:workspace-owner",
        "task:find-document",
        "goal:find-document",
        "intent:find-document",
        ("information:target-identity",),
        ("information:target-identity",),
    )
    gateway, route = _run_full_route(spec, forged_replay=True)
    assert not gateway.errors
    assert route.cognitive_execution is not None
    assert route.cognitive_execution.sufficiency_status == "UNKNOWN"
    assert route.cognitive_execution.stop_ref is None


def test_canonical_looking_establishment_ref_has_no_authority() -> None:
    output = CognitiveStateFormationEngineV1().run_case(
        _request(
            establishment_status="ESTABLISHED",
            establishment_ref="required-conditions:canonical-looking:v1",
            establishment_basis="NO_ACTIVE_REQUIRED_CONDITIONS",
            required=(),
            available=(),
        )
    )
    assert output.sufficiency_candidate.status == "UNKNOWN"
    assert output.stop_candidate is None


def test_canonical_no_active_formation_can_authorize_empty_sufficiency() -> None:
    spec = ContrastSpecV1(
        "f02-no-active",
        "F02_NO_ACTIVE",
        "S01",
        "role:workspace-owner",
        "task:find-document",
        "goal:find-document",
        "intent:find-document",
        (),
        (),
    )
    gateway, route = _run_full_route(spec)
    assert not gateway.errors
    assert route.cognitive_execution is not None
    assert route.cognitive_execution.sufficiency_status == "SUFFICIENT"
    assert route.cognitive_execution.stop_ref is not None


def test_canonical_active_formation_preserves_unmet_and_satisfied_paths() -> None:
    base = dict(
        category="F02_ACTIVE",
        scenario_id="S01",
        role_ref="role:workspace-owner",
        task_ref="task:find-document",
        goal_ref="goal:find-document",
        intent_ref="intent:find-document",
        required_information_refs=("information:target-identity", "information:target-location"),
    )
    _, unmet = _run_full_route(
        ContrastSpecV1("f02-active-unmet", available_information_refs=("information:target-identity",), **base)
    )
    _, satisfied = _run_full_route(
        ContrastSpecV1(
            "f02-active-satisfied",
            available_information_refs=("information:target-identity", "information:target-location"),
            **base,
        )
    )
    assert unmet.cognitive_execution is not None
    assert unmet.cognitive_execution.sufficiency_status == "INSUFFICIENT"
    assert unmet.cognitive_execution.stop_ref is None
    assert satisfied.cognitive_execution is not None
    assert satisfied.cognitive_execution.sufficiency_status == "SUFFICIENT"
    assert satisfied.cognitive_execution.stop_ref is not None


def test_canonical_proof_mutation_is_withheld() -> None:
    proof = _no_active_establishment_proof()
    for mutated in (
        replace(proof, status="CONDITIONS_FORMED", active_required_condition_refs=("forged:condition",)),
        replace(proof, trace_ref="forged:formation-ref"),
    ):
        output = CognitiveStateFormationEngineV1().run_case(
            replace(_request(required=(), available=()), required_cognitive_condition_formation_result=mutated)
        )
        assert output.sufficiency_candidate.status == "UNKNOWN"
        assert output.stop_candidate is None


def test_brain_rejects_forged_establishment_without_canonical_proof() -> None:
    proof = SimpleNamespace(
        sufficiency_status="SUFFICIENT",
        requirement_establishment_status="ESTABLISHED",
        requirement_establishment_ref="forged:required-condition",
        sufficiency_ref="s",
        stop_ref="stop",
        execution_ref="execution",
        ingress_refs=("evidence",),
    )
    result = _build_closure(None, None, proof)
    assert result[-1] == ("closure_requires_sufficient_cognition",)


def test_decision_handoff_rejects_forged_establishment_without_canonical_proof() -> None:
    handoff, errors = build_cognitive_decision_handoff_candidate_v1(
        {
            "case_id": "F02-FORGED",
            "brain_request": {"goal_ref": "g", "intent_ref": "i", "concern_ref": "c", "context_ref": "x"},
            "information_need": {"information_need_ref": "n"},
            "loop_instance": {"cognitive_loop_ref": "l"},
        },
        {
            "sufficiency_status": "SUFFICIENT",
            "requirement_establishment_status": "ESTABLISHED",
            "requirement_establishment_ref": "forged:required-condition",
            "sufficiency_ref": "s",
            "stop_ref": "stop",
            "current_world_ref": "world",
            "hypothesis_refs": ["h"],
            "ingress_refs": ["e"],
            "execution_ref": "execution",
        },
    )
    assert handoff is None
    assert errors == ("decision_handoff_requires_validated_requirement_establishment",)
