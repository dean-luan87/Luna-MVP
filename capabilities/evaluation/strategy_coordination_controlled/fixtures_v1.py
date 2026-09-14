"""Synthetic fixtures for candidate-only Strategy Coordination."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceDecisionV1,
)
from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    InformationAcquisitionStrategyCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.strategy_coordination_v1 import (
    GovernedStrategyCoordinationRelationV1,
    StrategyCoordinationInputV1,
)


SOURCE_MODE = "CONTROLLED_STRATEGY_COORDINATION_TEST"
PARENT_PROBLEM_REF = "problem:controlled:strategy-coordination:v1"
SOURCE_STATE_REF = "state:controlled:strategy-coordination:v1"
NEED_REF_A = "need:controlled:strategy:a:v1"
NEED_REF_B = "need:controlled:strategy:b:v1"
GAP_REF_A = "gap:controlled:strategy:a:v1"
GAP_REF_B = "gap:controlled:strategy:b:v1"


@dataclass(frozen=True)
class StrategyCoordinationCaseV1:
    case_id: str
    request: StrategyCoordinationInputV1
    expected_result_status: str
    expected_statuses: Tuple[str, ...]
    evaluation_marker: str = ""


def _strategy(
    strategy_ref: str,
    branch_ref: str,
    basis_ref: str,
    *,
    need_ref: str = NEED_REF_A,
    gap_ref: str = GAP_REF_A,
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
        acquisition_mode_candidate="PERCEPTION",
        required_capability_class_refs=(),
        opportunity_refs=(),
        dependency_refs=dependency_refs,
        lineage_refs=(branch_ref, f"lineage:{basis_ref}"),
        provenance_refs=(f"provenance:{strategy_ref}",),
        trace_ref=f"trace:{strategy_ref}",
        candidate_only=candidate_only,
    )


def _decision(
    branch_ref: str,
    status: str = "ADMITTED",
) -> CognitiveBranchGovernanceDecisionV1:
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


def _relation(
    relation_ref: str,
    kind: str,
    strategy_refs: Tuple[str, ...],
    *,
    retained_strategy_ref: str = "",
) -> GovernedStrategyCoordinationRelationV1:
    return GovernedStrategyCoordinationRelationV1(
        relation_ref=relation_ref,
        relation_kind=kind,
        strategy_refs=strategy_refs,
        coordination_basis_refs=(f"basis:coordination:{relation_ref}",),
        retained_strategy_ref=retained_strategy_ref,
    )


def _request(
    coordination_ref: str,
    strategies: Tuple[InformationAcquisitionStrategyCandidateV1, ...],
    decisions: Tuple[CognitiveBranchGovernanceDecisionV1, ...],
    *,
    satisfied_dependency_refs: Tuple[str, ...] = (),
    deferred_strategy_refs: Tuple[str, ...] = (),
    governed_relations: Tuple[GovernedStrategyCoordinationRelationV1, ...] = (),
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
        governed_relations=governed_relations,
        current_cognitive_state_ref=SOURCE_STATE_REF,
        context_refs=("context:controlled:opaque:v1",),
        trace_ref=f"trace:coordination:{coordination_ref}",
        provenance_refs=("provenance:controlled:strategy-coordination:v1",),
        candidate_only=candidate_only,
    )


def build_strategy_coordination_cases_v1() -> Tuple[StrategyCoordinationCaseV1, ...]:
    branch_a = "branch:controlled:strategy:a"
    branch_b = "branch:controlled:strategy:b"
    strategy_a = _strategy("strategy:controlled:a", branch_a, "basis:strategy:a")
    strategy_b = _strategy("strategy:controlled:b", branch_b, "basis:strategy:b")
    strategy_a2 = _strategy("strategy:controlled:a2", branch_a, "basis:strategy:a2")

    return (
        StrategyCoordinationCaseV1(
            "SINGLE_STRATEGY",
            _request("single", (strategy_a,), (_decision(branch_a),)),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED",),
        ),
        StrategyCoordinationCaseV1(
            "TWO_INDEPENDENT_STRATEGIES",
            _request("independent", (strategy_a, strategy_b), (_decision(branch_a), _decision(branch_b))),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED", "ADMITTED"),
        ),
        StrategyCoordinationCaseV1(
            "EXPLICIT_DEFERRED",
            _request(
                "deferred",
                (strategy_a, strategy_b),
                (_decision(branch_a), _decision(branch_b)),
                deferred_strategy_refs=(strategy_b.strategy_ref,),
            ),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED", "DEFERRED"),
        ),
        StrategyCoordinationCaseV1(
            "MISSING_DEPENDENCY",
            _request(
                "dependency",
                (
                    strategy_a,
                    replace(strategy_b, dependency_refs=("dependency:missing",)),
                ),
                (_decision(branch_a), _decision(branch_b)),
            ),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED", "BLOCKED_DEPENDENCY"),
        ),
        StrategyCoordinationCaseV1(
            "EXPLICIT_REDUNDANCY",
            _request(
                "redundancy",
                (strategy_a, strategy_b),
                (_decision(branch_a), _decision(branch_b)),
                governed_relations=(
                    _relation(
                        "redundancy:a-b",
                        "REDUNDANT",
                        (strategy_a.strategy_ref, strategy_b.strategy_ref),
                        retained_strategy_ref=strategy_a.strategy_ref,
                    ),
                ),
            ),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED", "SUPPRESSED_REDUNDANT"),
        ),
        StrategyCoordinationCaseV1(
            "EXPLICIT_INCOMPATIBILITY",
            _request(
                "incompatible",
                (strategy_a, strategy_b),
                (_decision(branch_a), _decision(branch_b)),
                governed_relations=(
                    _relation(
                        "incompatible:a-b",
                        "INCOMPATIBLE",
                        (strategy_a.strategy_ref, strategy_b.strategy_ref),
                    ),
                ),
            ),
            "COORDINATION_DECISIONS_FORMED",
            ("INCOMPATIBLE", "INCOMPATIBLE"),
        ),
        StrategyCoordinationCaseV1(
            "DEFERRED_BRANCH_STRATEGY",
            _request("deferred-branch", (strategy_a,), (_decision(branch_a, "DEFERRED"),)),
            "NO_STRATEGY_CANDIDATES",
            (),
        ),
        StrategyCoordinationCaseV1(
            "REJECTED_BRANCH_STRATEGY",
            _request("rejected-branch", (strategy_a,), (_decision(branch_a, "REJECTED"),)),
            "NO_STRATEGY_CANDIDATES",
            (),
        ),
        StrategyCoordinationCaseV1(
            "ZERO_STRATEGY",
            _request("zero", (), ()),
            "NO_STRATEGY_CANDIDATES",
            (),
        ),
        StrategyCoordinationCaseV1(
            "MULTIPLE_GAPS",
            _request(
                "multiple-gaps",
                (
                    strategy_a,
                    replace(
                        strategy_b,
                        information_need_refs=(NEED_REF_B,),
                        information_gap_refs=(GAP_REF_B,),
                    ),
                ),
                (_decision(branch_a), _decision(branch_b)),
            ),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED", "ADMITTED"),
        ),
        StrategyCoordinationCaseV1(
            "SCENARIO_12_SHAPE",
            _request(
                "scenario-12",
                (
                    _strategy("strategy:scenario12:signage", branch_a, "basis:scenario12:signage"),
                    _strategy("strategy:scenario12:flow", branch_a, "basis:scenario12:flow"),
                ),
                (_decision(branch_a),),
            ),
            "COORDINATION_DECISIONS_FORMED",
            ("ADMITTED", "ADMITTED"),
        ),
        StrategyCoordinationCaseV1(
            "REQUIREMENT_ALREADY_SATISFIED",
            _request("satisfied", (), ()),
            "NO_STRATEGY_CANDIDATES",
            (),
        ),
        StrategyCoordinationCaseV1(
            "INVALID_INPUT",
            _request(
                "invalid",
                (replace(strategy_a, candidate_only=False),),
                (_decision(branch_a),),
            ),
            "INVALID_INPUT",
            (),
        ),
    )


__all__ = [
    "SOURCE_MODE",
    "StrategyCoordinationCaseV1",
    "build_strategy_coordination_cases_v1",
]
