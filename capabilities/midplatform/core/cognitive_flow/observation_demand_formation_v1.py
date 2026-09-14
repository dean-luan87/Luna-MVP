"""Candidate-only formation of cognitive Observation Demands.

This module is the controlled boundary from Strategy Coordination to a future
perception/capability layer.  It carries an explicit governed observation
mapping forward; it does not infer targets, resolve capabilities, or execute
observation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from .information_acquisition_strategy_candidate_formation_v1 import (
    InformationAcquisitionStrategyCandidateV1,
)
from .strategy_coordination_v1 import (
    COORDINATION_STATUSES,
    StrategyCoordinationDecisionV1,
    StrategyCoordinationResultV1,
)


OBSERVATION_DEMAND_OWNER = "Cognitive Flow Observation Demand Formation"
SUPPORTED_ACQUISITION_MODES = ("PERCEPTION",)
SUPPORTED_OBSERVATION_CLASSES = ("PERCEPTION",)
FORMATION_STATUSES = (
    "OBSERVATION_DEMANDS_FORMED",
    "NO_OBSERVATION_DEMAND",
    "INVALID_INPUT",
    "UNSUPPORTED_ACQUISITION_MODE",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class GovernedObservationDemandMappingV1:
    """Explicit strategy-to-observation mapping supplied by governance.

    The mapping is an input fact for this formation boundary.  Target meaning
    is never inferred from a strategy ref, basis ref, or natural-language text.
    """

    mapping_ref: str
    strategy_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    observation_class: str
    observation_target_refs: Tuple[str, ...] = field(default_factory=tuple)
    observation_constraint_refs: Tuple[str, ...] = field(default_factory=tuple)
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ObservationDemandCandidateV1:
    """A what-to-observe candidate, never an observation execution request."""

    observation_demand_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    source_strategy_ref: str
    source_coordination_decision_ref: str
    source_branch_ref: str
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    acquisition_basis_refs: Tuple[str, ...]
    expected_information_contribution_refs: Tuple[str, ...]
    observation_class: str
    observation_target_refs: Tuple[str, ...]
    observation_constraint_refs: Tuple[str, ...]
    context_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    runtime_observation_executed: bool = False
    capability_requirement_formed: bool = False
    capability_resolution_executed: bool = False
    capability_execution: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    ocr_execution: bool = False
    camera_execution: bool = False
    slam_execution: bool = False
    resource_acquisition_executed: bool = False
    attention_formed: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class ObservationDemandFormationInputV1:
    """Strategy Coordination output plus explicit target mappings."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    coordination_result: StrategyCoordinationResultV1
    strategy_candidates: Tuple[InformationAcquisitionStrategyCandidateV1, ...] = field(
        default_factory=tuple
    )
    governed_observation_mappings: Tuple[GovernedObservationDemandMappingV1, ...] = field(
        default_factory=tuple
    )
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationDemandFormationResultV1:
    """Immutable demand candidates and explicit non-execution guards."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_strategy_refs: Tuple[str, ...]
    admitted_strategy_refs: Tuple[str, ...]
    excluded_strategy_refs: Tuple[str, ...]
    demand_refs: Tuple[str, ...]
    demands: Tuple[ObservationDemandCandidateV1, ...]
    current_cognitive_state_ref: str
    context_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    attention_formed: bool = False
    observation_demand_formed: bool = False
    capability_requirement_formed: bool = False
    capability_resolution_executed: bool = False
    capability_execution: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    ocr_execution: bool = False
    camera_execution: bool = False
    slam_execution: bool = False
    runtime_observation_executed: bool = False
    resource_acquisition_executed: bool = False
    resource_scheduling_executed: bool = False
    strategy_priority_assigned: bool = False
    winner_selected: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    evidence_fusion_executed: bool = False
    conflict_resolution_executed: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    memory_pcn_mutation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _demand_ref(formation_ref: str, strategy_ref: str, source_state_ref: str) -> str:
    digest = hashlib.sha256(
        f"{formation_ref}|{strategy_ref}|{source_state_ref}".encode("utf-8")
    ).hexdigest()[:24]
    return f"observation-demand:candidate:{digest}"


def _invalid_result(
    request: ObservationDemandFormationInputV1,
    errors: Tuple[str, ...],
    *,
    status: str = "INVALID_INPUT",
) -> ObservationDemandFormationResultV1:
    refs = tuple(strategy.strategy_ref for strategy in request.strategy_candidates)
    coordination = request.coordination_result
    return ObservationDemandFormationResultV1(
        formation_ref=request.formation_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status=status,
        input_strategy_refs=refs,
        admitted_strategy_refs=(),
        excluded_strategy_refs=refs,
        demand_refs=(),
        demands=(),
        current_cognitive_state_ref=coordination.current_cognitive_state_ref,
        context_refs=request.context_refs,
        provenance_refs=_unique(("provenance:cognitive-flow:observation-demand:v1", *request.provenance_refs)),
        trace_ref=request.trace_ref or f"trace:{request.formation_ref}",
        validation_errors=errors,
    )


def _validate(
    request: ObservationDemandFormationInputV1,
) -> Tuple[str, ...]:
    errors = []
    coordination = request.coordination_result
    if not request.formation_ref:
        errors.append("formation_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("formation_not_candidate_only")
    if not coordination.candidate_only or not coordination.read_only:
        errors.append("coordination_not_read_only_candidate")
    if coordination.truth_declared or coordination.world_truth_declared:
        errors.append("coordination_truth_declared")
    if coordination.coordination_status not in (
        "COORDINATION_DECISIONS_FORMED",
        "NO_STRATEGY_CANDIDATES",
    ):
        errors.append(f"invalid_coordination_status:{coordination.coordination_status}")
    if coordination.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
        errors.append("coordination_problem_mismatch")
    if coordination.source_state_ref != request.source_state_ref:
        errors.append("coordination_source_state_mismatch")

    strategy_refs = tuple(strategy.strategy_ref for strategy in request.strategy_candidates)
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
            or strategy.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or strategy.source_state_ref != request.source_state_ref
        ):
            errors.append(f"invalid_strategy_candidate:{strategy.strategy_ref}")

    if set(coordination.input_strategy_refs) != strategy_ref_set:
        errors.append("coordination_input_strategy_universe_mismatch")
    decisions_by_strategy = {}
    for decision in coordination.coordination_decisions:
        if decision.strategy_ref in decisions_by_strategy:
            errors.append(f"duplicate_coordination_decision:{decision.strategy_ref}")
        decisions_by_strategy[decision.strategy_ref] = decision
        if (
            decision.strategy_ref not in strategy_ref_set
            or not decision.coordination_decision_ref
            or not decision.candidate_only
            or not decision.read_only
            or decision.truth_declared
            or decision.world_truth_declared
            or decision.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or decision.source_state_ref != request.source_state_ref
        ):
            errors.append(f"invalid_coordination_decision:{decision.strategy_ref}")

    mapping_by_strategy = {}
    for mapping in request.governed_observation_mappings:
        if mapping.strategy_ref in mapping_by_strategy:
            errors.append(f"duplicate_observation_mapping:{mapping.strategy_ref}")
        mapping_by_strategy[mapping.strategy_ref] = mapping
        if (
            not mapping.mapping_ref
            or not mapping.candidate_only
            or not mapping.read_only
            or mapping.truth_declared
            or mapping.world_truth_declared
            or mapping.strategy_ref not in strategy_ref_set
            or mapping.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref
            or mapping.source_state_ref != request.source_state_ref
            or not mapping.observation_class
            or not mapping.observation_target_refs
        ):
            errors.append(f"invalid_observation_mapping:{mapping.strategy_ref}")

    admitted_refs = set(coordination.admitted_strategy_refs)
    for ref in admitted_refs:
        strategy = next((item for item in request.strategy_candidates if item.strategy_ref == ref), None)
        decision = decisions_by_strategy.get(ref)
        mapping = mapping_by_strategy.get(ref)
        if strategy is None or decision is None or decision.coordination_status != "ADMITTED":
            errors.append(f"admitted_strategy_not_backed_by_admitted_decision:{ref}")
        if mapping is None:
            errors.append(f"observation_mapping_missing:{ref}")
    return tuple(dict.fromkeys(errors))


def form_observation_demands(
    request: ObservationDemandFormationInputV1,
) -> ObservationDemandFormationResultV1:
    """Form one demand per admitted, supported, explicitly mapped strategy."""

    errors = _validate(request)
    if errors:
        return _invalid_result(request, errors)

    coordination = request.coordination_result
    strategy_by_ref = {strategy.strategy_ref: strategy for strategy in request.strategy_candidates}
    decision_by_ref = {
        decision.strategy_ref: decision for decision in coordination.coordination_decisions
    }
    mapping_by_ref = {
        mapping.strategy_ref: mapping for mapping in request.governed_observation_mappings
    }
    admitted_refs = tuple(coordination.admitted_strategy_refs)
    unsupported = tuple(
        ref
        for ref in admitted_refs
        if strategy_by_ref[ref].acquisition_mode_candidate not in SUPPORTED_ACQUISITION_MODES
    )
    if unsupported:
        return _invalid_result(
            request,
            tuple(f"unsupported_acquisition_mode:{ref}" for ref in unsupported),
            status="UNSUPPORTED_ACQUISITION_MODE",
        )
    if not admitted_refs:
        return ObservationDemandFormationResultV1(
            formation_ref=request.formation_ref,
            parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
            source_state_ref=request.source_state_ref,
            formation_status="NO_OBSERVATION_DEMAND",
            input_strategy_refs=tuple(strategy_by_ref),
            admitted_strategy_refs=(),
            excluded_strategy_refs=tuple(strategy_by_ref),
            demand_refs=(),
            demands=(),
            current_cognitive_state_ref=coordination.current_cognitive_state_ref,
            context_refs=request.context_refs,
            provenance_refs=_unique(("provenance:cognitive-flow:observation-demand:v1", *request.provenance_refs)),
            trace_ref=request.trace_ref or f"trace:{request.formation_ref}",
        )

    demands = []
    for strategy_ref in admitted_refs:
        strategy = strategy_by_ref[strategy_ref]
        decision: StrategyCoordinationDecisionV1 = decision_by_ref[strategy_ref]
        mapping = mapping_by_ref[strategy_ref]
        demand_ref = _demand_ref(
            request.formation_ref, strategy.strategy_ref, strategy.source_state_ref
        )
        demands.append(
            ObservationDemandCandidateV1(
                observation_demand_ref=demand_ref,
                parent_cognitive_problem_ref=strategy.parent_cognitive_problem_ref,
                source_state_ref=strategy.source_state_ref,
                source_strategy_ref=strategy.strategy_ref,
                source_coordination_decision_ref=decision.coordination_decision_ref,
                source_branch_ref=strategy.branch_ref,
                information_need_refs=strategy.information_need_refs,
                information_gap_refs=strategy.information_gap_refs,
                acquisition_basis_refs=strategy.acquisition_basis_refs,
                expected_information_contribution_refs=strategy.expected_information_contribution_refs,
                observation_class=mapping.observation_class,
                observation_target_refs=mapping.observation_target_refs,
                observation_constraint_refs=mapping.observation_constraint_refs,
                context_refs=_unique((*request.context_refs, *mapping.context_refs)),
                lineage_refs=_unique(
                    (
                        *strategy.lineage_refs,
                        strategy.strategy_ref,
                        decision.coordination_decision_ref,
                        mapping.mapping_ref,
                        demand_ref,
                    )
                ),
                provenance_refs=_unique(
                    (
                        *strategy.provenance_refs,
                        *decision.provenance_refs,
                        *mapping.provenance_refs,
                        *request.provenance_refs,
                    )
                ),
                trace_ref=request.trace_ref or f"trace:{demand_ref}",
            )
        )
    demand_tuple = tuple(demands)
    return ObservationDemandFormationResultV1(
        formation_ref=request.formation_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status="OBSERVATION_DEMANDS_FORMED",
        input_strategy_refs=tuple(strategy_by_ref),
        admitted_strategy_refs=admitted_refs,
        excluded_strategy_refs=tuple(
            ref for ref in strategy_by_ref if ref not in set(admitted_refs)
        ),
        demand_refs=tuple(demand.observation_demand_ref for demand in demand_tuple),
        demands=demand_tuple,
        current_cognitive_state_ref=coordination.current_cognitive_state_ref,
        context_refs=request.context_refs,
        provenance_refs=_unique(("provenance:cognitive-flow:observation-demand:v1", *request.provenance_refs)),
        trace_ref=request.trace_ref or f"trace:{request.formation_ref}",
        observation_demand_formed=True,
    )


__all__ = [
    "OBSERVATION_DEMAND_OWNER",
    "SUPPORTED_ACQUISITION_MODES",
    "SUPPORTED_OBSERVATION_CLASSES",
    "FORMATION_STATUSES",
    "GovernedObservationDemandMappingV1",
    "ObservationDemandCandidateV1",
    "ObservationDemandFormationInputV1",
    "ObservationDemandFormationResultV1",
    "form_observation_demands",
]
