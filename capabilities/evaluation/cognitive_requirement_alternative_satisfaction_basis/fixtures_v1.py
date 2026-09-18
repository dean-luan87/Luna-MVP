"""Controlled fixtures for requirement/basis satisfaction semantics."""

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


SOURCE_MODE = (
    "CONTROLLED_COGNITIVE_REQUIREMENT_ALTERNATIVE_SATISFACTION_BASIS_TEST"
)
FIELD_REF = "condition:field:controlled:alternative-basis:v1"
GOAL_REF = "goal:controlled:alternative-basis:v1"
REQUIREMENT_REF = "condition:cognitive:exit-direction-known:v1"
LEGACY_REQUIREMENT_REF = "condition:legacy:exact-coverage:v1"
LEGACY_COVERAGE_REF = "coverage:legacy:exact-coverage:v1"
BASIS_A = "basis:controlled:exit-direction:a:v1"
BASIS_B = "basis:controlled:exit-direction:b:v1"
BASIS_C = "basis:controlled:exit-direction:c:v1"


@dataclass(frozen=True)
class AlternativeSatisfactionCaseV1:
    case_id: str
    request: ARouteRequiredCognitiveConditionFormationRequestV1
    expected_status: str
    expected_satisfaction_status: str
    expected_satisfaction_coverage_refs: Tuple[str, ...]


def _goal() -> GoalContextV1:
    return GoalContextV1(
        goal_ref=GOAL_REF,
        primary_goal="controlled requirement satisfaction objective",
        secondary_goal_refs=(),
        success_condition_refs=(),
        stop_condition_refs=(),
        provenance={"owner": "controlled objective governance"},
        trace="trace:controlled:alternative-basis:goal:v1",
    )


def _world(case_id: str) -> CurrentWorldCandidateV1:
    return CurrentWorldCandidateV1(
        current_world_id=f"world:controlled:alternative-basis:{case_id}:v1",
        attention_refs=(),
        active_hypothesis_refs=(),
        alternative_hypothesis_refs=(),
        context_refs=("context:opaque:controlled:v1",),
        field_state_refs=("field:controlled:alternative-basis:v1",),
        pcn_refs=(),
        intent_refs=(),
        observation_refs=(),
        uncertainty_refs=(),
        conflict_refs=(),
        temporal_refs=(),
        source_versions=(("current_world", "current-world-candidate-v1"),),
        world_state_kind_candidate="PARTIAL",
        world_stability_candidate="CONTROLLED",
        trace_ref=f"trace:world:controlled:alternative-basis:{case_id}",
        provenance_refs=(f"provenance:world:controlled:alternative-basis:{case_id}",),
    )


def _request(
    case_id: str,
    *,
    requirement_ref: str,
    coverage_refs: Tuple[str, ...] = (),
    alternative_basis_refs: Tuple[str, ...] = (),
    legacy_coverage_refs: Tuple[str, ...] = (),
) -> ARouteRequiredCognitiveConditionFormationRequestV1:
    return ARouteRequiredCognitiveConditionFormationRequestV1(
        goal_context=_goal(),
        governed_condition_rules=(
            GovernedObjectiveConditionRuleV1(
                rule_ref=f"rule:controlled:alternative-basis:{case_id}:v1",
                condition_ref=requirement_ref,
                objective_refs=(GOAL_REF,),
                activation_all_refs=(FIELD_REF,),
                satisfaction_coverage_refs=legacy_coverage_refs,
                alternative_satisfaction_basis_refs=alternative_basis_refs,
                minimum_set_ref=f"minimum-set:controlled:{case_id}:v1",
                source_refs=(f"source:controlled:{case_id}:v1",),
                provenance_refs=(f"provenance:controlled:{case_id}:v1",),
            ),
        ),
        current_situation=CurrentCognitiveSituationV1(
            current_cognitive_view_refs=("view:controlled:alternative-basis:v1",),
            current_cognitive_coverage_refs=coverage_refs,
            current_world_refs=(_world(case_id).current_world_id,),
            field_condition_refs=(FIELD_REF,),
        ),
        formation_trace_ref=f"trace:controlled:alternative-basis:{case_id}:v1",
    )


def build_alternative_satisfaction_cases_v1() -> Tuple[AlternativeSatisfactionCaseV1, ...]:
    alternatives = (BASIS_A, BASIS_B, BASIS_C)
    return (
        AlternativeSatisfactionCaseV1(
            "LEGACY_EXACT_COVERAGE",
            _request(
                "legacy-covered",
                requirement_ref=LEGACY_REQUIREMENT_REF,
                coverage_refs=(LEGACY_COVERAGE_REF,),
                legacy_coverage_refs=(LEGACY_COVERAGE_REF,),
            ),
            "CONDITIONS_FORMED",
            "SATISFIED",
            (LEGACY_COVERAGE_REF,),
        ),
        AlternativeSatisfactionCaseV1(
            "LEGACY_EXACT_COVERAGE_MISSING",
            _request(
                "legacy-missing",
                requirement_ref=LEGACY_REQUIREMENT_REF,
                legacy_coverage_refs=(LEGACY_COVERAGE_REF,),
            ),
            "CONDITIONS_FORMED",
            "UNSATISFIED",
            (),
        ),
        AlternativeSatisfactionCaseV1(
            "ALTERNATIVE_BASIS_A",
            _request(
                "basis-a",
                requirement_ref=REQUIREMENT_REF,
                coverage_refs=(BASIS_A,),
                alternative_basis_refs=alternatives,
            ),
            "CONDITIONS_FORMED",
            "SATISFIED",
            (BASIS_A,),
        ),
        AlternativeSatisfactionCaseV1(
            "ALTERNATIVE_BASIS_B",
            _request(
                "basis-b",
                requirement_ref=REQUIREMENT_REF,
                coverage_refs=(BASIS_B,),
                alternative_basis_refs=alternatives,
            ),
            "CONDITIONS_FORMED",
            "SATISFIED",
            (BASIS_B,),
        ),
        AlternativeSatisfactionCaseV1(
            "NO_ALTERNATIVE_BASIS_COVERED",
            _request(
                "basis-none",
                requirement_ref=REQUIREMENT_REF,
                alternative_basis_refs=alternatives,
            ),
            "CONDITIONS_FORMED",
            "UNSATISFIED",
            (),
        ),
        AlternativeSatisfactionCaseV1(
            "MULTIPLE_ALTERNATIVE_BASES_COVERED",
            _request(
                "basis-multiple",
                requirement_ref=REQUIREMENT_REF,
                coverage_refs=(BASIS_A, BASIS_B),
                alternative_basis_refs=alternatives,
            ),
            "CONDITIONS_FORMED",
            "SATISFIED",
            (BASIS_A,),
        ),
    )


__all__ = [
    "AlternativeSatisfactionCaseV1",
    "BASIS_A",
    "BASIS_B",
    "BASIS_C",
    "LEGACY_COVERAGE_REF",
    "LEGACY_REQUIREMENT_REF",
    "REQUIREMENT_REF",
    "SOURCE_MODE",
    "build_alternative_satisfaction_cases_v1",
]
