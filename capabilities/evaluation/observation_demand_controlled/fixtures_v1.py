"""Synthetic fixtures for candidate-only Observation Demand formation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceDecisionV1,
)
from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    InformationAcquisitionStrategyCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.observation_demand_formation_v1 import (
    GovernedObservationDemandMappingV1,
    ObservationDemandFormationInputV1,
)
from capabilities.midplatform.core.cognitive_flow.strategy_coordination_v1 import (
    GovernedStrategyCoordinationRelationV1,
    StrategyCoordinationInputV1,
    coordinate_acquisition_strategies,
)


SOURCE_MODE = "CONTROLLED_OBSERVATION_DEMAND_TEST"
PARENT_PROBLEM_REF = "problem:controlled:observation-demand:v1"
SOURCE_STATE_REF = "state:controlled:observation-demand:v1"
NEED_REF_A = "need:controlled:observation-demand:a:v1"
NEED_REF_B = "need:controlled:observation-demand:b:v1"
GAP_REF_A = "gap:controlled:observation-demand:a:v1"
GAP_REF_B = "gap:controlled:observation-demand:b:v1"


@dataclass(frozen=True)
class ObservationDemandCaseV1:
    case_id: str
    request: ObservationDemandFormationInputV1
    expected_status: str
    expected_demand_count: int
    evaluation_marker: str = ""


def _strategy(
    strategy_ref: str,
    branch_ref: str,
    basis_ref: str,
    *,
    need_ref: str = NEED_REF_A,
    gap_ref: str = GAP_REF_A,
    mode: str = "PERCEPTION",
    dependency_refs: Tuple[str, ...] = (),
    candidate_only: bool = True,
) -> InformationAcquisitionStrategyCandidateV1:
    return InformationAcquisitionStrategyCandidateV1(
        strategy_ref=strategy_ref,
        branch_ref=branch_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        information_need_refs=(need_ref,),
        information_gap_refs=(gap_ref,),
        acquisition_basis_refs=(basis_ref,),
        expected_information_contribution_refs=(f"contribution:{basis_ref}",),
        acquisition_mode_candidate=mode,
        required_capability_class_refs=(f"capability-class:{basis_ref}",),
        opportunity_refs=(f"opportunity:{basis_ref}",),
        dependency_refs=dependency_refs,
        lineage_refs=(branch_ref, f"lineage:{basis_ref}"),
        provenance_refs=(f"provenance:{strategy_ref}",),
        trace_ref=f"trace:{strategy_ref}",
        candidate_only=candidate_only,
    )


def _branch_decision(branch_ref: str, status: str = "ADMITTED") -> CognitiveBranchGovernanceDecisionV1:
    return CognitiveBranchGovernanceDecisionV1(
        governance_decision_ref=f"governance:{branch_ref}",
        branch_ref=branch_ref,
        governance_status=status,
        reason_code="VALID_CURRENT_BASIS" if status == "ADMITTED" else status,
        governance_basis_refs=(f"basis:governance:{branch_ref}",),
        candidate_lineage_refs=(branch_ref,),
        candidate_provenance_refs=(f"provenance:{branch_ref}",),
        source_state_ref=SOURCE_STATE_REF,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        provenance_refs=(f"provenance:governance:{branch_ref}",),
        trace_ref=f"trace:governance:{branch_ref}",
        recoverable=status != "REJECTED",
    )


def _coordination_input(
    coordination_ref: str,
    strategies: Tuple[InformationAcquisitionStrategyCandidateV1, ...],
    decisions: Tuple[CognitiveBranchGovernanceDecisionV1, ...],
    *,
    satisfied_dependency_refs: Tuple[str, ...] = (),
    deferred_strategy_refs: Tuple[str, ...] = (),
    relations: Tuple[GovernedStrategyCoordinationRelationV1, ...] = (),
    candidate_only: bool = True,
) -> StrategyCoordinationInputV1:
    return StrategyCoordinationInputV1(
        coordination_ref=coordination_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        strategy_candidates=strategies,
        branch_governance_decisions=decisions,
        satisfied_dependency_refs=satisfied_dependency_refs,
        deferred_strategy_refs=deferred_strategy_refs,
        governed_relations=relations,
        current_cognitive_state_ref=SOURCE_STATE_REF,
        context_refs=("context:controlled:opaque:v1",),
        trace_ref=f"trace:coordination:{coordination_ref}",
        provenance_refs=("provenance:controlled:observation-demand:v1",),
        candidate_only=candidate_only,
    )


def _mapping(strategy: InformationAcquisitionStrategyCandidateV1, *, observation_class: str = "PERCEPTION") -> GovernedObservationDemandMappingV1:
    return GovernedObservationDemandMappingV1(
        mapping_ref=f"mapping:{strategy.strategy_ref}",
        strategy_ref=strategy.strategy_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        observation_class=observation_class,
        observation_target_refs=(f"target:{strategy.acquisition_basis_refs[0]}",),
        observation_constraint_refs=(),
        context_refs=(f"mapping-context:{strategy.strategy_ref}",),
        provenance_refs=(f"provenance:mapping:{strategy.strategy_ref}",),
    )


def _request(
    formation_ref: str,
    coordination_input: StrategyCoordinationInputV1,
    mappings: Tuple[GovernedObservationDemandMappingV1, ...],
) -> ObservationDemandFormationInputV1:
    return ObservationDemandFormationInputV1(
        formation_ref=formation_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        coordination_result=coordinate_acquisition_strategies(coordination_input),
        strategy_candidates=coordination_input.strategy_candidates,
        governed_observation_mappings=mappings,
        context_refs=("context:controlled:observation-demand:v1",),
        trace_ref=f"trace:observation-demand:{formation_ref}",
        provenance_refs=("provenance:controlled:observation-demand:v1",),
    )


def build_observation_demand_cases_v1() -> Tuple[ObservationDemandCaseV1, ...]:
    branch_a = "branch:controlled:observation-demand:a"
    branch_b = "branch:controlled:observation-demand:b"
    strategy_a = _strategy("strategy:observation-demand:a", branch_a, "basis:observation:a")
    strategy_b = _strategy("strategy:observation-demand:b", branch_b, "basis:observation:b")

    def case(case_id: str, ref: str, strategies, decisions, mappings, **kwargs):
        expected_status = kwargs.pop("expected_status", "OBSERVATION_DEMANDS_FORMED")
        expected_count = kwargs.pop("expected_count", len(strategies))
        return ObservationDemandCaseV1(
            case_id,
            _request(ref, _coordination_input(ref, strategies, decisions, **kwargs), mappings),
            expected_status,
            expected_count,
        )

    cases = [
        case("SINGLE_ADMITTED_PERCEPTION_STRATEGY", "single", (strategy_a,), (_branch_decision(branch_a),), (_mapping(strategy_a),), expected_count=1),
        case("TWO_INDEPENDENT_ADMITTED_STRATEGIES", "two", (strategy_a, strategy_b), (_branch_decision(branch_a), _branch_decision(branch_b)), (_mapping(strategy_a), _mapping(strategy_b)), expected_count=2),
        case("DEFERRED_STRATEGY", "deferred", (strategy_a,), (_branch_decision(branch_a),), (_mapping(strategy_a),), deferred_strategy_refs=(strategy_a.strategy_ref,), expected_count=0, expected_status="NO_OBSERVATION_DEMAND"),
        case("BLOCKED_DEPENDENCY_STRATEGY", "blocked", (replace(strategy_a, dependency_refs=("dependency:missing",)),), (_branch_decision(branch_a),), (_mapping(strategy_a),), expected_count=0, expected_status="NO_OBSERVATION_DEMAND"),
        case("SUPPRESSED_REDUNDANT_STRATEGY", "redundant", (strategy_a, strategy_b), (_branch_decision(branch_a), _branch_decision(branch_b)), (_mapping(strategy_a), _mapping(strategy_b)), relations=(GovernedStrategyCoordinationRelationV1("relation:redundant", "REDUNDANT", (strategy_a.strategy_ref, strategy_b.strategy_ref), ("basis:explicit:redundant",), strategy_a.strategy_ref),), expected_count=1),
        case("INCOMPATIBLE_STRATEGIES", "incompatible", (strategy_a, strategy_b), (_branch_decision(branch_a), _branch_decision(branch_b)), (_mapping(strategy_a), _mapping(strategy_b)), relations=(GovernedStrategyCoordinationRelationV1("relation:incompatible", "INCOMPATIBLE", (strategy_a.strategy_ref, strategy_b.strategy_ref), ("basis:explicit:incompatible",)),), expected_count=0, expected_status="NO_OBSERVATION_DEMAND"),
        case("NO_STRATEGY_CANDIDATES", "zero", (), (), (), expected_count=0, expected_status="NO_OBSERVATION_DEMAND"),
        case("REQUIREMENT_ALREADY_SATISFIED", "satisfied", (), (), (), expected_count=0, expected_status="NO_OBSERVATION_DEMAND"),
        case("MULTIPLE_COGNITIVE_GAPS", "multiple-gaps", (strategy_a, replace(strategy_b, information_need_refs=(NEED_REF_B,), information_gap_refs=(GAP_REF_B,))), (_branch_decision(branch_a), _branch_decision(branch_b)), (_mapping(strategy_a), _mapping(strategy_b)), expected_count=2),
        case("SCENARIO_12_SHAPE", "scenario-12", (_strategy("strategy:scenario12:signage", branch_a, "basis:scenario12:signage"), _strategy("strategy:scenario12:flow", branch_a, "basis:scenario12:flow")), (_branch_decision(branch_a),), (_mapping(_strategy("strategy:scenario12:signage", branch_a, "basis:scenario12:signage")), _mapping(_strategy("strategy:scenario12:flow", branch_a, "basis:scenario12:flow"))), expected_count=2),
        case("UNSUPPORTED_ACQUISITION_MODE", "unsupported", (replace(strategy_a, acquisition_mode_candidate="RETRIEVAL"),), (_branch_decision(branch_a),), (_mapping(replace(strategy_a, acquisition_mode_candidate="RETRIEVAL"), observation_class="RETRIEVAL"),), expected_count=0, expected_status="UNSUPPORTED_ACQUISITION_MODE"),
        case("INVALID_COORDINATION_INPUT", "invalid", (strategy_a,), (_branch_decision(branch_a),), (_mapping(strategy_a),), candidate_only=False, expected_count=0, expected_status="INVALID_INPUT"),
    ]
    return tuple(cases)


__all__ = [
    "ObservationDemandCaseV1",
    "SOURCE_MODE",
    "build_observation_demand_cases_v1",
]
