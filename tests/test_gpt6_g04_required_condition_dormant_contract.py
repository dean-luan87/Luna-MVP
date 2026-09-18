"""Regression protection for GPT6-G04 Required Condition return contracts."""

import pytest

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import GoalContextV1
from capabilities.evaluation.a_route_required_cognitive_condition_formation.fixtures_v1 import (
    build_required_condition_formation_cases_v1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_orchestration_engine_v1 import (
    ARouteOrchestrationEngineV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    CurrentCognitiveSituationV1,
    DORMANT,
    GovernedObjectiveConditionRuleV1,
    NO_ACTIVE_REQUIRED_CONDITIONS,
)


def _dormant_request(
    *,
    objective_refs: tuple[str, ...] = ("goal:active",),
    activation_all_refs: tuple[str, ...] = (),
    activation_any_refs: tuple[str, ...] = (),
    suppress_if_any_refs: tuple[str, ...] = (),
    situation_refs: tuple[str, ...] = (),
) -> ARouteRequiredCognitiveConditionFormationRequestV1:
    return ARouteRequiredCognitiveConditionFormationRequestV1(
        goal_context=GoalContextV1(
            goal_ref="goal:active",
            primary_goal="goal:active",
            secondary_goal_refs=(),
            success_condition_refs=(),
            stop_condition_refs=(),
            provenance={"source": "gpt6-g04-test"},
            trace="trace:gpt6-g04",
        ),
        governed_condition_rules=(
            GovernedObjectiveConditionRuleV1(
                rule_ref="rule:gpt6-g04",
                condition_ref="condition:gpt6-g04",
                objective_refs=objective_refs,
                activation_all_refs=activation_all_refs,
                activation_any_refs=activation_any_refs,
                suppress_if_any_refs=suppress_if_any_refs,
                source_refs=("source:gpt6-g04",),
                provenance_refs=("provenance:gpt6-g04",),
            ),
        ),
        current_situation=CurrentCognitiveSituationV1(
            current_world_condition_refs=situation_refs,
        ),
        formation_trace_ref="trace:gpt6-g04:formation",
    )


@pytest.mark.parametrize(
    ("reason", "formation_request"),
    (
        (
            "objective_not_active",
            _dormant_request(objective_refs=("goal:other",)),
        ),
        (
            "activation_all_not_satisfied",
            _dormant_request(activation_all_refs=("condition:all",)),
        ),
        (
            "activation_any_not_satisfied",
            _dormant_request(activation_any_refs=("condition:any",)),
        ),
        (
            "suppressed_by_current_situation",
            _dormant_request(
                suppress_if_any_refs=("condition:suppress",),
                situation_refs=("condition:suppress",),
            ),
        ),
    ),
)
def test_legal_dormant_rules_preserve_five_field_contract(reason: str, formation_request) -> None:
    result = ARouteOrchestrationEngineV1.form_required_cognitive_conditions(formation_request)

    assert result.status == NO_ACTIVE_REQUIRED_CONDITIONS
    assert len(result.candidates) == 1
    candidate = result.candidates[0]
    assert candidate.status == DORMANT
    assert candidate.reason == reason
    assert candidate.satisfaction_status == "UNSATISFIED"
    assert candidate.satisfaction_coverage_refs == ()
    assert not result.active_required_condition_refs


def test_active_required_condition_path_remains_valid() -> None:
    request = build_required_condition_formation_cases_v1()[0].request

    result = ARouteOrchestrationEngineV1.form_required_cognitive_conditions(request)

    assert result.status == "CONDITIONS_FORMED"
    assert result.active_required_condition_refs
