"""Controlled governed-rule fixtures for Required Condition formation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
    ARouteRequiredCognitiveConditionFormationRequestV1,
    CurrentCognitiveSituationV1,
    GovernedObjectiveConditionRuleV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


SOURCE_MODE = "CONTROLLED_A_ROUTE_REQUIRED_COGNITIVE_CONDITION_FORMATION_TEST"
GOAL_SEAT = "goal:governed:locate-seat:v1"
GOAL_EXIT = "goal:governed:find-exit:v1"
INTENT_REF = "intent:governed:situated-navigation:v1"
CONCERN_REF = "concern:governed:safe-navigation:v1"
FIELD_CONDITION = "condition:field:office:v1"
ROLE_OPERATOR = "condition:role:operator:v1"
ROLE_VISITOR = "condition:role:visitor:v1"
SELF_READY = "self:governed:mobility:ready:v1"
SELF_LIMITED = "self:governed:mobility:limited:v1"
PREFERENCE_CONDITION = "condition:concern:seat-preference:v1"
SEAT_LOCATION = "condition:seat:location-required:v1"
SEAT_ACCESS = "condition:seat:operator-access-required:v1"
MOBILITY_PLAN = "condition:seat:mobility-adjustment-required:v1"
EXIT_LOCATION = "condition:exit:location-required:v1"


@dataclass(frozen=True)
class RequiredConditionFormationCaseV1:
    case_id: str
    request: ARouteRequiredCognitiveConditionFormationRequestV1
    expected_active: Tuple[str, ...]
    expected_satisfied: Tuple[str, ...]
    expected_status: str


def _goal(goal_ref: str, trace: str) -> GoalContextV1:
    return GoalContextV1(
        goal_ref=goal_ref,
        primary_goal="governed cognitive objective",
        secondary_goal_refs=(),
        success_condition_refs=(),
        stop_condition_refs=(),
        provenance={"owner": "controlled objective governance"},
        trace=trace,
    )


def _world(world_id: str) -> CurrentWorldCandidateV1:
    return CurrentWorldCandidateV1(
        current_world_id=world_id,
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=("context:opaque:office:v1",),
        field_state_refs=("field:controlled:v1",),
        pcn_refs=(),
        intent_refs=(INTENT_REF,),
        observation_refs=(),
        uncertainty_refs=(),
        conflict_refs=(),
        temporal_refs=(),
        source_versions={"current_world": "current-world-candidate-v1"},
        world_state_kind_candidate="PARTIAL",
        world_stability_candidate="LOW",
        trace_ref=f"trace:{world_id}",
        provenance_refs=(f"provenance:{world_id}",),
    )


def _rules() -> Tuple[GovernedObjectiveConditionRuleV1, ...]:
    """One governed rule set reused by every contrast case."""

    return (
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:seat:location:v1",
            condition_ref="condition:seat:location-required:v1",
            objective_refs=(GOAL_SEAT,),
            activation_all_refs=(FIELD_CONDITION,),
            satisfaction_coverage_refs=(SEAT_LOCATION,),
            minimum_set_ref="minimum-set:seat-location:v1",
            source_refs=("governance:objective:seat:v1",),
            provenance_refs=("provenance:governed-rule:seat-location:v1",),
        ),
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:seat:operator-access:v1",
            condition_ref="condition:seat:operator-access-required:v1",
            objective_refs=(GOAL_SEAT,),
            activation_all_refs=(FIELD_CONDITION, ROLE_OPERATOR, SELF_READY),
            satisfaction_coverage_refs=(SEAT_ACCESS,),
            minimum_set_ref="minimum-set:seat-access:v1",
            selection_rank=0,
            source_refs=("governance:role:operator:v1",),
            provenance_refs=("provenance:governed-rule:operator-access:v1",),
        ),
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:seat:visitor-access:v1",
            condition_ref="condition:seat:visitor-orientation-required:v1",
            objective_refs=(GOAL_SEAT,),
            activation_all_refs=(FIELD_CONDITION, ROLE_VISITOR),
            satisfaction_coverage_refs=(SEAT_ACCESS,),
            minimum_set_ref="minimum-set:seat-access:v1",
            selection_rank=0,
            source_refs=("governance:role:visitor:v1",),
            provenance_refs=("provenance:governed-rule:visitor-access:v1",),
        ),
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:seat:operator-access-alternative:v1",
            condition_ref="condition:seat:operator-access-alternative:v1",
            objective_refs=(GOAL_SEAT,),
            activation_all_refs=(FIELD_CONDITION, ROLE_OPERATOR, SELF_READY),
            satisfaction_coverage_refs=("condition:seat:operator-access-alternative:v1",),
            minimum_set_ref="minimum-set:seat-access:v1",
            selection_rank=1,
            source_refs=("governance:role:operator:v1",),
            provenance_refs=("provenance:governed-rule:operator-access-alternative:v1",),
        ),
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:seat:limited-mobility:v1",
            condition_ref="condition:seat:mobility-adjustment-required:v1",
            objective_refs=(GOAL_SEAT,),
            activation_all_refs=(FIELD_CONDITION, ROLE_OPERATOR, SELF_LIMITED),
            satisfaction_coverage_refs=(MOBILITY_PLAN,),
            minimum_set_ref="minimum-set:seat-access:v1",
            selection_rank=0,
            source_refs=("governance:self:mobility:v1",),
            provenance_refs=("provenance:governed-rule:mobility-adjustment:v1",),
        ),
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:seat:preference-alternative:v1",
            condition_ref="condition:seat:preference-required:v1",
            objective_refs=(GOAL_SEAT,),
            activation_all_refs=(FIELD_CONDITION, ROLE_OPERATOR, SELF_READY, PREFERENCE_CONDITION),
            satisfaction_coverage_refs=("condition:seat:preference-required:v1",),
            minimum_set_ref="minimum-set:seat-preference:v1",
            selection_rank=0,
            source_refs=("governance:concern:preference:v1",),
            provenance_refs=("provenance:governed-rule:preference:v1",),
        ),
        GovernedObjectiveConditionRuleV1(
            rule_ref="rule:exit:location:v1",
            condition_ref="condition:exit:location-required:v1",
            objective_refs=(GOAL_EXIT,),
            activation_all_refs=(FIELD_CONDITION,),
            satisfaction_coverage_refs=(EXIT_LOCATION,),
            minimum_set_ref="minimum-set:exit-location:v1",
            source_refs=("governance:objective:exit:v1",),
            provenance_refs=("provenance:governed-rule:exit-location:v1",),
        ),
    )


def _request(
    *,
    goal_ref: str = GOAL_SEAT,
    world_id: str = "world:controlled:seat-base:v1",
    context_ref: str = "context:opaque:office:v1",
    role_refs: Tuple[str, ...] = ("role:governed:operator:v1",),
    role_conditions: Tuple[str, ...] = (ROLE_OPERATOR,),
    self_information: Tuple[str, ...] = (SELF_READY,),
    external_information: Tuple[str, ...] = (),
    coverage: Tuple[str, ...] = (),
) -> ARouteRequiredCognitiveConditionFormationRequestV1:
    return ARouteRequiredCognitiveConditionFormationRequestV1(
        goal_context=_goal(goal_ref, f"trace:goal:{goal_ref}"),
        governed_condition_rules=_rules(),
        current_situation=CurrentCognitiveSituationV1(
            current_cognitive_view_refs=("view:minimum:controlled:v1",),
            current_cognitive_coverage_refs=coverage,
            current_world_refs=(world_id,),
            self_information_refs=self_information,
            external_information_refs=external_information,
            role_condition_refs=role_conditions,
            context_condition_refs=(),
            field_condition_refs=(FIELD_CONDITION,),
            intent_condition_refs=(),
            concern_condition_refs=(),
        ),
        intent_ref=INTENT_REF,
        concern_ref=CONCERN_REF,
        context_ref=context_ref,
        field_ref="field:controlled:v1",
        role_refs=role_refs,
        formation_trace_ref="trace:controlled:required-condition-formation:v1",
    )


def build_required_condition_formation_cases_v1() -> Tuple[RequiredConditionFormationCaseV1, ...]:
    return (
        RequiredConditionFormationCaseV1(
            "SAME_GOAL_DIFFERENT_COGNITIVE_SITUATION",
            _request(),
            (
                "condition:seat:location-required:v1",
                "condition:seat:operator-access-required:v1",
            ),
            (),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "SAME_GOAL_RELEVANT_STATE_CHANGE",
            _request(coverage=(SEAT_LOCATION,)),
            (
                "condition:seat:location-required:v1",
                "condition:seat:operator-access-required:v1",
            ),
            ("condition:seat:location-required:v1",),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "SAME_GOAL_NEED_ALREADY_SATISFIED",
            _request(coverage=(SEAT_LOCATION, SEAT_ACCESS)),
            (
                "condition:seat:location-required:v1",
                "condition:seat:operator-access-required:v1",
            ),
            (
                "condition:seat:location-required:v1",
                "condition:seat:operator-access-required:v1",
            ),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "SAME_GOAL_DIFFERENT_GOVERNED_ROLE",
            _request(
                role_refs=("role:governed:visitor:v1",),
                role_conditions=(ROLE_VISITOR,),
            ),
            (
                "condition:seat:location-required:v1",
                "condition:seat:visitor-orientation-required:v1",
            ),
            (),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "SAME_GOAL_SELF_STATE_CONDITIONED",
            _request(
                self_information=(SELF_LIMITED,),
            ),
            (
                "condition:seat:location-required:v1",
                "condition:seat:mobility-adjustment-required:v1",
            ),
            (),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "SAME_GOAL_IRRELEVANT_INFORMATION_CHANGE",
            _request(external_information=("external:irrelevant:weather:v1",)),
            (
                "condition:seat:location-required:v1",
                "condition:seat:operator-access-required:v1",
            ),
            (),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "DIFFERENT_GOAL_SAME_SITUATION",
            _request(goal_ref=GOAL_EXIT),
            ("condition:exit:location-required:v1",),
            (),
            "CONDITIONS_FORMED",
        ),
        RequiredConditionFormationCaseV1(
            "MINIMUM_REQUIRED_SET",
            _request(),
            (
                "condition:seat:location-required:v1",
                "condition:seat:operator-access-required:v1",
            ),
            (),
            "CONDITIONS_FORMED",
        ),
    )


def build_negative_required_condition_requests_v1() -> Tuple[tuple[str, ARouteRequiredCognitiveConditionFormationRequestV1], ...]:
    return (
        ("CANDIDATE_ONLY_FALSE", _request()),
    )
