"""Candidate-only formation of governed information-acquisition strategies.

This module extends the existing Cognitive Flow continuity after Branch
Governance.  It only projects explicit, governed acquisition bases into
traceable strategy candidates.  It does not invent strategies, coordinate
them, select resources, or execute an observation.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Iterable, Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceDecisionV1,
    GOVERNANCE_STATUSES,
)
from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    CognitiveBranchCandidateV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)


ACQUISITION_MODES = (
    "PERCEPTION",
    "RETRIEVAL",
    "INTERACTION",
    "HYPOTHETICAL_REASONING",
    "OTHER_GOVERNED",
    "UNKNOWN",
)
FORMATION_STATUSES = (
    "FORMED_CANDIDATES",
    "NO_GOVERNED_ACQUISITION_BASIS",
    "NO_ADMITTED_BRANCH",
    "INVALID_INPUT",
)


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


@dataclass(frozen=True)
class GovernedAcquisitionBasisV1:
    """An explicit upstream basis; it is not an acquisition strategy."""

    basis_ref: str
    branch_ref: str
    information_need_refs: Tuple[str, ...] = field(default_factory=tuple)
    information_gap_refs: Tuple[str, ...] = field(default_factory=tuple)
    acquisition_mode_candidate: str = "UNKNOWN"
    expected_information_contribution_refs: Tuple[str, ...] = field(
        default_factory=tuple
    )
    required_capability_class_refs: Tuple[str, ...] = field(default_factory=tuple)
    opportunity_refs: Tuple[str, ...] = field(default_factory=tuple)
    dependency_refs: Tuple[str, ...] = field(default_factory=tuple)
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class InformationAcquisitionStrategyCandidateV1:
    """A governed-basis projection, not a selected or executable strategy."""

    strategy_ref: str
    branch_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    acquisition_basis_refs: Tuple[str, ...]
    expected_information_contribution_refs: Tuple[str, ...]
    acquisition_mode_candidate: str
    required_capability_class_refs: Tuple[str, ...]
    opportunity_refs: Tuple[str, ...]
    dependency_refs: Tuple[str, ...]
    lineage_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    formation_status: str = "FORMED_CANDIDATE"


@dataclass(frozen=True)
class InformationAcquisitionStrategyFormationInputV1:
    """Governed branch state and explicit bases consumed by formation."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    branch_candidates: Tuple[CognitiveBranchCandidateV1, ...] = field(
        default_factory=tuple
    )
    governance_decisions: Tuple[CognitiveBranchGovernanceDecisionV1, ...] = field(
        default_factory=tuple
    )
    need_candidates: Tuple[CognitiveNeedCandidateV1, ...] = field(
        default_factory=tuple
    )
    governed_acquisition_bases: Tuple[GovernedAcquisitionBasisV1, ...] = field(
        default_factory=tuple
    )
    current_cognitive_state_ref: str = ""
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class InformationAcquisitionStrategyFormationResultV1:
    """Immutable strategy candidates and explicit non-execution boundaries."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    input_branch_refs: Tuple[str, ...]
    admitted_branch_refs: Tuple[str, ...]
    excluded_branch_refs: Tuple[str, ...]
    strategy_refs: Tuple[str, ...]
    strategies: Tuple[InformationAcquisitionStrategyCandidateV1, ...]
    excluded_basis_refs: Tuple[str, ...]
    current_cognitive_state_ref: str
    context_refs: Tuple[str, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    strategy_coordination_executed: bool = False
    strategy_priority_assigned: bool = False
    resource_merge_executed: bool = False
    resource_acquisition_executed: bool = False
    attention_formed: bool = False
    observation_demand_formed: bool = False
    capability_requirement_formed: bool = False
    capability_resolution_executed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    field_mutation: bool = False
    current_world_mutation: bool = False
    memory_pcn_mutation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _strategy_ref(
    formation_ref: str,
    branch_ref: str,
    basis_ref: str,
    source_state_ref: str,
) -> str:
    digest = hashlib.sha256(
        f"{formation_ref}|{branch_ref}|{basis_ref}|{source_state_ref}".encode(
            "utf-8"
        )
    ).hexdigest()[:24]
    return f"acquisition-strategy:candidate:{digest}"


def _normalize_mode(value: str) -> str:
    return value if value in ACQUISITION_MODES else "UNKNOWN"


def _validate_input(
    request: InformationAcquisitionStrategyFormationInputV1,
) -> Tuple[str, ...]:
    errors = []
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

    branch_refs = [branch.branch_ref for branch in request.branch_candidates]
    if len(set(branch_refs)) != len(branch_refs):
        errors.append("duplicate_branch_ref")
    for branch in request.branch_candidates:
        if (
            not branch.candidate_only
            or not branch.read_only
            or branch.truth_declared
            or branch.world_truth_declared
            or branch.current_world_mutation
            or branch.field_mutation
            or branch.formation_status != "FORMED_CANDIDATE"
        ):
            errors.append(f"invalid_branch_candidate:{branch.branch_ref}")
        if branch.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"branch_problem_mismatch:{branch.branch_ref}")
        if branch.source_state_ref != request.source_state_ref:
            errors.append(f"branch_source_state_mismatch:{branch.branch_ref}")

    decision_refs = [decision.branch_ref for decision in request.governance_decisions]
    if len(set(decision_refs)) != len(decision_refs):
        errors.append("duplicate_governance_decision_branch_ref")
    branch_ref_set = set(branch_refs)
    for decision in request.governance_decisions:
        if decision.branch_ref not in branch_ref_set:
            errors.append(f"decision_branch_missing:{decision.branch_ref}")
        if decision.governance_status not in GOVERNANCE_STATUSES:
            errors.append(f"unsupported_governance_status:{decision.branch_ref}")
        if not decision.candidate_only or not decision.read_only:
            errors.append(f"invalid_governance_decision:{decision.branch_ref}")
        if decision.truth_declared or decision.world_truth_declared:
            errors.append(f"governance_decision_truth_declared:{decision.branch_ref}")
        if decision.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            errors.append(f"decision_problem_mismatch:{decision.branch_ref}")
        if decision.source_state_ref != request.source_state_ref:
            errors.append(f"decision_source_state_mismatch:{decision.branch_ref}")

    need_ids = [need.need_id for need in request.need_candidates]
    if len(set(need_ids)) != len(need_ids):
        errors.append("duplicate_need_id")
    for need in request.need_candidates:
        if not need.candidate_only:
            errors.append(f"invalid_need_candidate:{need.need_id}")

    for basis in request.governed_acquisition_bases:
        if not basis.basis_ref:
            errors.append("acquisition_basis_ref_missing")
        if not basis.branch_ref:
            errors.append("acquisition_basis_branch_ref_missing")
        if not basis.candidate_only or not basis.read_only:
            errors.append(f"invalid_acquisition_basis:{basis.basis_ref}")
        if basis.truth_declared or basis.world_truth_declared:
            errors.append(f"acquisition_basis_truth_declared:{basis.basis_ref}")
        if any(ref not in need_ids for ref in basis.information_need_refs):
            errors.append(f"acquisition_basis_need_missing:{basis.basis_ref}")

    return tuple(dict.fromkeys(errors))


def _invalid_result(
    request: InformationAcquisitionStrategyFormationInputV1,
    errors: Tuple[str, ...],
) -> InformationAcquisitionStrategyFormationResultV1:
    return InformationAcquisitionStrategyFormationResultV1(
        formation_ref=request.formation_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status="INVALID_INPUT",
        input_branch_refs=tuple(branch.branch_ref for branch in request.branch_candidates),
        admitted_branch_refs=(),
        excluded_branch_refs=tuple(branch.branch_ref for branch in request.branch_candidates),
        strategy_refs=(),
        strategies=(),
        excluded_basis_refs=tuple(
            basis.basis_ref for basis in request.governed_acquisition_bases
        ),
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        context_refs=request.context_refs,
        trace_ref=request.trace_ref or f"trace:{request.formation_ref}",
        provenance_refs=_unique(
            (
                "provenance:information-acquisition-strategy-formation:v1",
                *request.provenance_refs,
            )
        ),
        candidate_only=request.candidate_only,
        validation_errors=errors,
    )


def form_information_acquisition_strategy_candidates(
    request: InformationAcquisitionStrategyFormationInputV1,
) -> InformationAcquisitionStrategyFormationResultV1:
    """Project explicit bases for admitted branches into distinct candidates."""

    errors = _validate_input(request)
    if errors:
        return _invalid_result(request, errors)

    branch_by_ref = {branch.branch_ref: branch for branch in request.branch_candidates}
    decisions_by_ref = {
        decision.branch_ref: decision for decision in request.governance_decisions
    }
    admitted_refs = tuple(
        branch_ref
        for branch_ref, decision in decisions_by_ref.items()
        if decision.governance_status == "ADMITTED"
    )
    excluded_refs = tuple(
        branch_ref
        for branch_ref in branch_by_ref
        if branch_ref not in set(admitted_refs)
    )
    provenance = _unique(
        (
            "provenance:information-acquisition-strategy-formation:v1",
            *request.provenance_refs,
        )
    )
    base_refs_seen = set()
    excluded_basis_refs = []
    strategies = []
    for basis in request.governed_acquisition_bases:
        if basis.basis_ref in base_refs_seen:
            excluded_basis_refs.append(basis.basis_ref)
            continue
        base_refs_seen.add(basis.basis_ref)
        branch = branch_by_ref.get(basis.branch_ref)
        if branch is None or basis.branch_ref not in set(admitted_refs):
            excluded_basis_refs.append(basis.basis_ref)
            continue
        if not set(basis.information_need_refs).issubset(
            set(branch.information_need_refs)
        ) or not set(basis.information_gap_refs).issubset(
            set(branch.information_gap_refs)
        ):
            excluded_basis_refs.append(basis.basis_ref)
            continue
        strategy_ref = _strategy_ref(
            request.formation_ref,
            branch.branch_ref,
            basis.basis_ref,
            request.source_state_ref,
        )
        strategies.append(
            InformationAcquisitionStrategyCandidateV1(
                strategy_ref=strategy_ref,
                branch_ref=branch.branch_ref,
                parent_cognitive_problem_ref=branch.parent_cognitive_problem_ref,
                source_state_ref=branch.source_state_ref,
                information_need_refs=_unique(basis.information_need_refs),
                information_gap_refs=_unique(basis.information_gap_refs),
                acquisition_basis_refs=(basis.basis_ref,),
                expected_information_contribution_refs=_unique(
                    basis.expected_information_contribution_refs
                ),
                acquisition_mode_candidate=_normalize_mode(
                    basis.acquisition_mode_candidate
                ),
                required_capability_class_refs=_unique(
                    basis.required_capability_class_refs
                ),
                opportunity_refs=_unique(basis.opportunity_refs),
                dependency_refs=_unique(basis.dependency_refs),
                lineage_refs=_unique(
                    (
                        branch.branch_ref,
                        *branch.lineage_refs,
                        *branch.derived_from_refs,
                    )
                ),
                provenance_refs=_unique(
                    (
                        *provenance,
                        *branch.provenance_refs,
                        *basis.provenance_refs,
                        branch.trace_ref,
                    )
                ),
                trace_ref=f"trace:{request.formation_ref}:{strategy_ref}",
            )
        )

    if not admitted_refs:
        status = "NO_ADMITTED_BRANCH"
    elif not strategies:
        status = "NO_GOVERNED_ACQUISITION_BASIS"
    else:
        status = "FORMED_CANDIDATES"
    return InformationAcquisitionStrategyFormationResultV1(
        formation_ref=request.formation_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status=status,
        input_branch_refs=tuple(branch_by_ref),
        admitted_branch_refs=admitted_refs,
        excluded_branch_refs=excluded_refs,
        strategy_refs=tuple(strategy.strategy_ref for strategy in strategies),
        strategies=tuple(strategies),
        excluded_basis_refs=_unique(tuple(excluded_basis_refs)),
        current_cognitive_state_ref=request.current_cognitive_state_ref,
        context_refs=request.context_refs,
        trace_ref=request.trace_ref,
        provenance_refs=provenance,
    )


__all__ = [
    "ACQUISITION_MODES",
    "FORMATION_STATUSES",
    "GovernedAcquisitionBasisV1",
    "InformationAcquisitionStrategyCandidateV1",
    "InformationAcquisitionStrategyFormationInputV1",
    "InformationAcquisitionStrategyFormationResultV1",
    "form_information_acquisition_strategy_candidates",
]
