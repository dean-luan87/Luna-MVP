"""Controlled fixtures for state-sensitive A-Route Need formation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_information_need_formation_types_v1 import (
    ARouteInformationNeedFormationRequestV1,
)
from capabilities.midplatform.core.cognitive_state_formation.current_world_types_v1 import (
    CurrentWorldCandidateV1,
)


SOURCE_MODE = "CONTROLLED_A_ROUTE_INFORMATION_NEED_FORMATION_TEST"
FIELD_REF = "field:controlled-office:v1"
GOAL_REF = "goal:controlled:understand-field:v1"
INTENT_REF = "intent:controlled:understand-field:v1"
CONCERN_REF = "concern:controlled:unresolved-field-condition:v1"
LOCATION_CONDITION = "condition:field-location-known:v1"
ROUTE_CONDITION = "condition:field-route-known:v1"
OWNER_CONDITION = "condition:role-owner-access-known:v1"
VISITOR_CONDITION = "condition:role-visitor-access-known:v1"


@dataclass(frozen=True)
class InformationNeedFormationCaseV1:
    case_id: str
    request: ARouteInformationNeedFormationRequestV1
    expected_status: str
    expected_unknown: Tuple[str, ...]


def _goal(goal_ref: str, conditions: Tuple[str, ...], trace: str) -> GoalContextV1:
    return GoalContextV1(
        goal_ref=goal_ref,
        primary_goal="controlled cognitive objective",
        secondary_goal_refs=(),
        success_condition_refs=conditions,
        stop_condition_refs=(),
        provenance={"owner": "controlled objective condition signal"},
        trace=trace,
    )


def _world(world_id: str, trace: str) -> CurrentWorldCandidateV1:
    return CurrentWorldCandidateV1(
        current_world_id=world_id,
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=("context:opaque:office:v1",),
        field_state_refs=(FIELD_REF,),
        pcn_refs=(),
        intent_refs=(INTENT_REF,),
        observation_refs=(),
        uncertainty_refs=(),
        conflict_refs=(),
        temporal_refs=(),
        source_versions=(("current_world", "current-world-candidate-v1"),),
        world_state_kind_candidate="PARTIAL",
        world_stability_candidate="LOW",
        trace_ref=trace,
        provenance_refs=(f"provenance:{world_id}",),
    )


def _request(
    *,
    goal: GoalContextV1,
    world: CurrentWorldCandidateV1,
    coverage: Tuple[str, ...],
    context_ref: str = "context:opaque:office:v1",
    role_refs: Tuple[str, ...] = (),
    role_conditions: Tuple[str, ...] = (),
) -> ARouteInformationNeedFormationRequestV1:
    return ARouteInformationNeedFormationRequestV1(
        goal_context=goal,
        current_world=world,
        current_cognitive_coverage_refs=coverage,
        intent_ref=INTENT_REF,
        concern_ref=CONCERN_REF,
        task_ref="task:controlled:understand-field:v1",
        context_ref=context_ref,
        field_ref=FIELD_REF,
        role_refs=role_refs,
        governed_role_condition_refs=role_conditions,
        hypothesis_ref="hypothesis:controlled:field:v1",
        attention_ref="attention:controlled:field:v1",
        formation_trace_ref=f"trace:controlled:need-formation:{world.current_world_id}",
    )


def build_information_need_formation_cases_v1() -> Tuple[InformationNeedFormationCaseV1, ...]:
    goal = _goal(GOAL_REF, (LOCATION_CONDITION, ROUTE_CONDITION), "trace:goal:understand-field")
    world_empty = _world("world:controlled:empty:v1", "trace:world:controlled:empty")
    world_location = _world("world:controlled:location:v1", "trace:world:controlled:location")
    shared_world = _world("world:controlled:shared:v1", "trace:world:controlled:shared")
    different_goal = _goal("goal:controlled:operational-state:v1", ("condition:operational-state-known:v1",), "trace:goal:operational-state")
    return (
        InformationNeedFormationCaseV1(
            "SAME_GOAL_DIFFERENT_CURRENT_WORLD",
            _request(goal=goal, world=world_empty, coverage=()),
            "NEED_FORMED",
            (LOCATION_CONDITION, ROUTE_CONDITION),
        ),
        InformationNeedFormationCaseV1(
            "SAME_GOAL_NEED_ALREADY_SATISFIED",
            _request(goal=goal, world=world_location, coverage=(LOCATION_CONDITION, ROUTE_CONDITION)),
            "NO_ACTIVE_NEED",
            (),
        ),
        InformationNeedFormationCaseV1(
            "SAME_GOAL_PARTIAL_COGNITIVE_COVERAGE",
            _request(goal=goal, world=world_location, coverage=(LOCATION_CONDITION,)),
            "NEED_FORMED",
            (ROUTE_CONDITION,),
        ),
        InformationNeedFormationCaseV1(
            "SAME_GOAL_DIFFERENT_GOVERNED_ROLE_OWNER",
            _request(
                goal=goal,
                world=shared_world,
                coverage=(LOCATION_CONDITION,),
                role_refs=("role:controlled:owner:v1",),
                role_conditions=(OWNER_CONDITION,),
            ),
            "NEED_FORMED",
            (ROUTE_CONDITION, OWNER_CONDITION),
        ),
        InformationNeedFormationCaseV1(
            "SAME_GOAL_DIFFERENT_GOVERNED_ROLE_VISITOR",
            _request(
                goal=goal,
                world=shared_world,
                coverage=(LOCATION_CONDITION,),
                role_refs=("role:controlled:visitor:v1",),
                role_conditions=(VISITOR_CONDITION,),
            ),
            "NEED_FORMED",
            (ROUTE_CONDITION, VISITOR_CONDITION),
        ),
        InformationNeedFormationCaseV1(
            "SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_A",
            _request(goal=goal, world=world_empty, coverage=(), context_ref="context:opaque:office:v1"),
            "NEED_FORMED",
            (LOCATION_CONDITION, ROUTE_CONDITION),
        ),
        InformationNeedFormationCaseV1(
            "SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE_B",
            _request(goal=goal, world=world_empty, coverage=(), context_ref="context:opaque:unrelated:v1"),
            "NEED_FORMED",
            (LOCATION_CONDITION, ROUTE_CONDITION),
        ),
        InformationNeedFormationCaseV1(
            "DIFFERENT_GOAL_SAME_CURRENT_WORLD",
            _request(goal=different_goal, world=world_location, coverage=(LOCATION_CONDITION,)),
            "NEED_FORMED",
            ("condition:operational-state-known:v1",),
        ),
    )


def build_negative_need_formation_requests_v1() -> Tuple[tuple[str, ARouteInformationNeedFormationRequestV1], ...]:
    base = _request(
        goal=_goal(GOAL_REF, (LOCATION_CONDITION,), "trace:goal:negative"),
        world=_world("world:controlled:negative:v1", "trace:world:negative"),
        coverage=(),
    )
    mutated_world = replace(base.current_world, field_mutation=True)
    return (
        ("CANDIDATE_ONLY_FALSE", replace(base, candidate_only=False)),
        ("CURRENT_WORLD_MUTATION_FLAG", replace(base, current_world=mutated_world)),
    )
