"""Candidate-only coordination of formed acquisition strategies.

This module sits after Information Acquisition Strategy Candidate Formation.
It emits per-strategy coordination decisions without choosing an execution
winner, acquiring resources, or implementing a downstream runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Tuple

from .cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceDecisionV1,
)
from .information_acquisition_strategy_candidate_formation_v1 import (
    InformationAcquisitionStrategyCandidateV1,
)


COORDINATION_OWNER = "Cognitive Flow Strategy Coordination"
COORDINATION_STATUSES = (
    "ADMITTED",
    "DEFERRED",
    "SUPPRESSED_REDUNDANT",
    "BLOCKED_DEPENDENCY",
    "INCOMPATIBLE",
)
RELATION_KINDS = ("REDUNDANT", "INCOMPATIBLE")
RESULT_STATUSES = (
    "COORDINATION_DECISIONS_FORMED",
    "NO_STRATEGY_CANDIDATES",
    "INVALID_INPUT",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class GovernedStrategyCoordinationRelationV1:
    """An explicit coordination relation supplied by governance."""

    relation_ref: str
    relation_kind: str
    strategy_refs: Tuple[str, ...]
    coordination_basis_refs: Tuple[str, ...] = field(default_factory=tuple)
    retained_strategy_ref: str = ""
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class StrategyCoordinationDecisionV1:
    """Immutable coordination result for one eligible strategy candidate."""

    coordination_decision_ref: str
    strategy_ref: str
    branch_ref: str
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    acquisition_basis_refs: Tuple[str, ...]
    coordination_status: str
    coordination_basis_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    incompatible_strategy_refs: Tuple[str, ...]
    redundant_strategy_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    source_state_ref: str
    parent_cognitive_problem_ref: str
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class StrategyCoordinationInputV1:
    """Explicit governed context for strategy coordination."""

    coordination_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    strategy_candidates: Tuple[InformationAcquisitionStrategyCandidateV1, ...] = field(
        default_factory=tuple
    )
    branch_governance_decisions: Tuple[CognitiveBranchGovernanceDecisionV1, ...] = field(
        default_factory=tuple
    )
    satisfied_dependency_refs: Tuple[str, ...] = field(default_factory=tuple)
    deferred_strategy_refs: Tuple[str, ...] = field(default_factory=tuple)
    governed_relations: Tuple[GovernedStrategyCoordinationRelationV1, ...] = field(
        default_factory=tuple
    )
    current_cognitive_state_ref: str = ""
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class StrategyCoordinationResultV1:
    """Candidate-only coordination output, never an execution plan."""

    coordination_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    coordination_status: str
    input_strategy_refs: Tuple[str, ...]
    eligible_strategy_refs: Tuple[str, ...]
    excluded_strategy_refs: Tuple[str, ...]
    excluded_strategy_reasons: Tuple[Tuple[str, str], ...]
    admitted_strategy_refs: Tuple[str, ...]
    deferred_strategy_refs: Tuple[str, ...]
    suppressed_redundant_strategy_refs: Tuple[str, ...]
    blocked_dependency_strategy_refs: Tuple[str, ...]
    incompatible_strategy_refs: Tuple[str, ...]
    coordination_decisions: Tuple[StrategyCoordinationDecisionV1, ...]
    current_cognitive_state_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    strategy_execution: bool = False
    observation_demand_formed: bool = False
    capability_resolution_executed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    memory_pcn_mutation: bool = False
    attention_formed: bool = False
    resource_governance_executed: bool = False
    resource_acquisition_executed: bool = False
    priority_assigned: bool = False
    ranking_executed: bool = False
    winner_selected: bool = False
    evidence_fusion_executed: bool = False
    validation_errors: Tuple[str, ...] = ()


def _invalid_result(
    request: StrategyCoordinationInputV1,
    errors: Tuple[str, ...],
) -> StrategyCoordinationResultV1:
    refs = tuple(strategy.strategy_ref for strategy in request.strategy_candidates)
    return StrategyCoordinationResultV1(
        coordination_ref=request.coordination_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        coordination_status="INVALID_INPUT",
        input_strategy_refs=refs,
        eligible_strategy_refs=(),
        excluded_strategy_refs=refs,
        excluded_strategy_reasons=tuple((ref, "INVALID_INPUT") for ref in refs),
        admitted_strategy_refs=(),
        deferred_strategy_refs=(),
        suppressed_redundant_strategy_refs=(),
        blocked_dependency_strategy_refs=(),
        incompatible_strategy_refs=(),
        coordination_decisions=(),
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        context_refs=request.context_refs,
        provenance_refs=_unique(
            ("provenance:cognitive-flow:strategy-coordination:v1", *request.provenance_refs)
        ),
        trace_ref=request.trace_ref or f"trace:{request.coordination_ref}",
        candidate_only=request.candidate_only,
        validation_errors=errors,
    )


def _validate(
    request: StrategyCoordinationInputV1,
) -> Tuple[str, ...]:
    errors = []
    if not request.coordination_ref:
        errors.append("coordination_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("coordination_not_candidate_only")

    strategy_refs = [strategy.strategy_ref for strategy in request.strategy_candidates]
    if len(set(strategy_refs)) != len(strategy_refs):
        errors.append("duplicate_strategy_ref")
    strategy_ref_set = set(strategy_refs)
    for strategy in request.strategy_candidates:
        if (
            not strategy.strategy_ref
            or not strategy.candidate_only
            or not strategy.read_only
            or strategy.truth_declared
            or strategy.world_truth_declared
            or strategy.formation_status != "FORMED_CANDIDATE"
        ):
            errors.append(f"invalid_strategy_candidate:{strategy.strategy_ref}")
        if strategy.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"strategy_problem_mismatch:{strategy.strategy_ref}")
        if strategy.source_state_ref != request.source_state_ref:
            errors.append(f"strategy_source_state_mismatch:{strategy.strategy_ref}")

    decisions_by_branch = {}
    for decision in request.branch_governance_decisions:
        if decision.branch_ref in decisions_by_branch:
            errors.append(f"duplicate_branch_governance_decision:{decision.branch_ref}")
        decisions_by_branch[decision.branch_ref] = decision
        if decision.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"governance_problem_mismatch:{decision.branch_ref}")
        if decision.source_state_ref != request.source_state_ref:
            errors.append(f"governance_source_state_mismatch:{decision.branch_ref}")
        if decision.governance_status not in ("ADMITTED", "DEFERRED", "REJECTED"):
            errors.append(f"unsupported_governance_status:{decision.branch_ref}")
        if not decision.candidate_only or not decision.read_only:
            errors.append(f"invalid_governance_decision:{decision.branch_ref}")
        if decision.truth_declared or decision.world_truth_declared:
            errors.append(f"governance_truth_declared:{decision.branch_ref}")

    for strategy in request.strategy_candidates:
        if strategy.branch_ref not in decisions_by_branch:
            errors.append(f"strategy_branch_governance_missing:{strategy.strategy_ref}")

    for relation in request.governed_relations:
        if not relation.relation_ref:
            errors.append("coordination_relation_ref_missing")
        if relation.relation_kind not in RELATION_KINDS:
            errors.append(f"unsupported_coordination_relation:{relation.relation_ref}")
        if len(relation.strategy_refs) < 2:
            errors.append(f"coordination_relation_needs_two_strategies:{relation.relation_ref}")
        if not set(relation.strategy_refs).issubset(strategy_ref_set):
            errors.append(f"coordination_relation_strategy_missing:{relation.relation_ref}")
        if not relation.candidate_only or not relation.read_only:
            errors.append(f"invalid_coordination_relation:{relation.relation_ref}")
        if relation.truth_declared or relation.world_truth_declared:
            errors.append(f"coordination_relation_truth_declared:{relation.relation_ref}")
        if relation.relation_kind == "REDUNDANT" and (
            not relation.retained_strategy_ref
            or relation.retained_strategy_ref not in relation.strategy_refs
        ):
            errors.append(f"redundant_retention_missing:{relation.relation_ref}")

    return tuple(dict.fromkeys(errors))


def coordinate_acquisition_strategies(
    request: StrategyCoordinationInputV1,
) -> StrategyCoordinationResultV1:
    """Coordinate candidates using only explicit governed relations/context."""

    errors = _validate(request)
    if errors:
        return _invalid_result(request, errors)

    input_refs = tuple(strategy.strategy_ref for strategy in request.strategy_candidates)
    decisions_by_branch = {
        decision.branch_ref: decision
        for decision in request.branch_governance_decisions
    }
    eligible = tuple(
        strategy
        for strategy in request.strategy_candidates
        if decisions_by_branch[strategy.branch_ref].governance_status == "ADMITTED"
    )
    eligible_refs = {strategy.strategy_ref for strategy in eligible}
    excluded = tuple(
        strategy.strategy_ref
        for strategy in request.strategy_candidates
        if strategy.strategy_ref not in eligible_refs
    )
    excluded_reasons = tuple(
        (
            strategy.strategy_ref,
            f"SOURCE_BRANCH_{decisions_by_branch[strategy.branch_ref].governance_status}",
        )
        for strategy in request.strategy_candidates
        if strategy.strategy_ref not in eligible_refs
    )
    provenance = _unique(
        (
            "provenance:cognitive-flow:strategy-coordination:v1",
            *request.provenance_refs,
        )
    )
    if not eligible:
        return StrategyCoordinationResultV1(
            coordination_ref=request.coordination_ref,
            parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
            source_state_ref=request.source_state_ref,
            coordination_status="NO_STRATEGY_CANDIDATES",
            input_strategy_refs=input_refs,
            eligible_strategy_refs=(),
            excluded_strategy_refs=excluded,
            excluded_strategy_reasons=excluded_reasons,
            admitted_strategy_refs=(),
            deferred_strategy_refs=(),
            suppressed_redundant_strategy_refs=(),
            blocked_dependency_strategy_refs=(),
            incompatible_strategy_refs=(),
            coordination_decisions=(),
            current_cognitive_state_ref=request.current_cognitive_state_ref,
            context_refs=request.context_refs,
            provenance_refs=provenance,
            trace_ref=request.trace_ref,
        )

    incompatible: dict[str, set[str]] = {}
    suppressed: dict[str, tuple[str, ...]] = {}
    relation_basis: dict[str, Tuple[str, ...]] = {}
    for relation in request.governed_relations:
        refs = tuple(ref for ref in relation.strategy_refs if ref in eligible_refs)
        basis = _unique(relation.coordination_basis_refs)
        if relation.relation_kind == "INCOMPATIBLE":
            for ref in refs:
                incompatible.setdefault(ref, set()).update(
                    peer for peer in refs if peer != ref
                )
                relation_basis[ref] = _unique((*relation_basis.get(ref, ()), *basis))
        elif relation.retained_strategy_ref in refs:
            for ref in refs:
                if ref != relation.retained_strategy_ref:
                    suppressed[ref] = tuple(
                        peer for peer in refs if peer != ref
                    )
                    relation_basis[ref] = _unique(
                        (*relation_basis.get(ref, ()), *basis)
                    )
            relation_basis[relation.retained_strategy_ref] = _unique(
                (*relation_basis.get(relation.retained_strategy_ref, ()), *basis)
            )

    admitted = []
    deferred = []
    blocked = []
    incompatible_refs = []
    suppressed_refs = []
    decisions = []
    satisfied_dependencies = set(request.satisfied_dependency_refs)
    deferred_refs = set(request.deferred_strategy_refs)
    for strategy in eligible:
        strategy_ref = strategy.strategy_ref
        strategy_basis = list(relation_basis.get(strategy_ref, ()))
        incompatible_peers = tuple(sorted(incompatible.get(strategy_ref, ())))
        if incompatible_peers:
            status = "INCOMPATIBLE"
            strategy_basis.append("governed:explicit-incompatibility")
            incompatible_refs.append(strategy_ref)
        elif not set(strategy.dependency_refs).issubset(satisfied_dependencies):
            status = "BLOCKED_DEPENDENCY"
            strategy_basis.append("governed:dependency-coverage")
            blocked.append(strategy_ref)
        elif strategy_ref in deferred_refs:
            status = "DEFERRED"
            strategy_basis.append("governed:explicit-defer")
            deferred.append(strategy_ref)
        elif strategy_ref in suppressed:
            status = "SUPPRESSED_REDUNDANT"
            strategy_basis.append("governed:explicit-redundancy")
            suppressed_refs.append(strategy_ref)
        else:
            status = "ADMITTED"
            strategy_basis.append("governed:strategy-candidate-valid")
            admitted.append(strategy_ref)
        redundant_peers = suppressed.get(strategy_ref, ())
        decisions.append(
            StrategyCoordinationDecisionV1(
                coordination_decision_ref=(
                    f"coordination-decision:{request.coordination_ref}:{strategy_ref}"
                ),
                strategy_ref=strategy_ref,
                branch_ref=strategy.branch_ref,
                information_need_refs=_unique(strategy.information_need_refs),
                information_gap_refs=_unique(strategy.information_gap_refs),
                acquisition_basis_refs=_unique(strategy.acquisition_basis_refs),
                coordination_status=status,
                coordination_basis_refs=_unique(strategy_basis),
                dependency_refs=_unique(strategy.dependency_refs),
                incompatible_strategy_refs=incompatible_peers,
                redundant_strategy_refs=_unique(redundant_peers),
                lineage_refs=_unique(strategy.lineage_refs),
                provenance_refs=_unique(
                    (*provenance, *strategy.provenance_refs, strategy.trace_ref)
                ),
                source_state_ref=strategy.source_state_ref,
                parent_cognitive_problem_ref=strategy.parent_cognitive_problem_ref,
                trace_ref=f"trace:{request.coordination_ref}:{strategy_ref}",
            )
        )

    return StrategyCoordinationResultV1(
        coordination_ref=request.coordination_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        coordination_status="COORDINATION_DECISIONS_FORMED",
        input_strategy_refs=input_refs,
        eligible_strategy_refs=tuple(strategy.strategy_ref for strategy in eligible),
        excluded_strategy_refs=excluded,
        excluded_strategy_reasons=excluded_reasons,
        admitted_strategy_refs=tuple(admitted),
        deferred_strategy_refs=tuple(deferred),
        suppressed_redundant_strategy_refs=tuple(suppressed_refs),
        blocked_dependency_strategy_refs=tuple(blocked),
        incompatible_strategy_refs=tuple(incompatible_refs),
        coordination_decisions=tuple(decisions),
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        context_refs=request.context_refs,
        provenance_refs=provenance,
        trace_ref=request.trace_ref,
    )


__all__ = [
    "COORDINATION_OWNER",
    "COORDINATION_STATUSES",
    "RELATION_KINDS",
    "RESULT_STATUSES",
    "GovernedStrategyCoordinationRelationV1",
    "StrategyCoordinationDecisionV1",
    "StrategyCoordinationInputV1",
    "StrategyCoordinationResultV1",
    "coordinate_acquisition_strategies",
]
