"""Candidate-only formation of branches from already governed alternatives.

This module extends the existing Cognitive Flow loop without creating a second
loop or taking ownership of hypothesis, need, world, or lifecycle governance.
It only organizes explicit cognitive bases into traceable branch candidates.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Tuple

from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
)


BRANCH_FORMATION_BASIS = (
    "HYPOTHESIS_ALTERNATIVE",
    "UNRESOLVED_INFORMATION_GAP",
    "EXPLICIT_GOVERNED_ALTERNATIVE",
)


@dataclass(frozen=True)
class CognitiveBranchCandidateV1:
    """A formed exploration direction, not a governance decision."""

    branch_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_basis: str
    basis_ref: str
    lineage_refs: Tuple[str, ...]
    derived_from_refs: Tuple[str, ...]
    hypothesis_refs: Tuple[str, ...]
    information_need_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    conflict_refs: Tuple[str, ...]
    formation_status: str
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    truth_declared: bool = False
    world_truth_declared: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False


@dataclass(frozen=True)
class GovernedCognitiveBranchFormationInputV1:
    """Explicit governed cognitive material consumed by branch formation."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    hypothesis_candidates: Tuple[CognitiveHypothesisCandidateV1, ...] = field(
        default_factory=tuple
    )
    unresolved_gap_need_refs: Tuple[Tuple[str, Tuple[str, ...]], ...] = field(
        default_factory=tuple
    )
    explicit_alternative_refs: Tuple[str, ...] = field(default_factory=tuple)
    evidence_refs: Tuple[str, ...] = field(default_factory=tuple)
    conflict_refs: Tuple[str, ...] = field(default_factory=tuple)
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class GovernedCognitiveBranchFormationResultV1:
    """Formation result; governance and execution remain explicitly absent."""

    formation_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    formation_status: str
    branch_refs: Tuple[str, ...]
    branches: Tuple[CognitiveBranchCandidateV1, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    governance_executed: bool = False
    resource_acquisition: bool = False
    observation_demand_formed: bool = False
    capability_requirement_formed: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    autonomous_child_runtime_spawn: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    world_truth_declared: bool = False
    validation_errors: Tuple[str, ...] = ()


def _unique(values: Tuple[str, ...]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value))


def _branch_id(parent_ref: str, basis: str, basis_ref: str) -> str:
    digest = hashlib.sha256(
        f"{parent_ref}|{basis}|{basis_ref}".encode("utf-8")
    ).hexdigest()[:24]
    return f"cognitive-branch:formed:{digest}"


def _branch_trace(formation_ref: str, branch_ref: str) -> str:
    return f"trace:{formation_ref}:{branch_ref}"


def _validate_input(
    request: GovernedCognitiveBranchFormationInputV1,
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
    hypothesis_ids = [item.hypothesis_id for item in request.hypothesis_candidates]
    if len(set(hypothesis_ids)) != len(hypothesis_ids):
        errors.append("duplicate_hypothesis_basis")
    for item in request.hypothesis_candidates:
        if not item.candidate_only:
            errors.append("hypothesis_basis_not_candidate_only")
    for gap_ref, need_refs in request.unresolved_gap_need_refs:
        if not gap_ref:
            errors.append("information_gap_basis_missing")
        if any(not ref for ref in need_refs):
            errors.append("information_need_basis_missing")
    if any(not ref for ref in request.explicit_alternative_refs):
        errors.append("explicit_alternative_basis_missing")
    return tuple(dict.fromkeys(errors))


def form_governed_cognitive_branches(
    request: GovernedCognitiveBranchFormationInputV1,
) -> GovernedCognitiveBranchFormationResultV1:
    """Form branches only from explicit, already governed cognitive bases."""

    errors = _validate_input(request)
    trace_ref = request.trace_ref or f"trace:{request.formation_ref}"
    provenance = _unique(
        (
            "provenance:governed-cognitive-branch-formation:v1",
            *request.provenance_refs,
        )
    )
    if errors:
        return GovernedCognitiveBranchFormationResultV1(
            formation_ref=request.formation_ref,
            parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
            source_state_ref=request.source_state_ref,
            formation_status="INVALID_INPUT",
            branch_refs=(),
            branches=(),
            trace_ref=trace_ref,
            provenance_refs=provenance,
            candidate_only=request.candidate_only,
            read_only=True,
            validation_errors=errors,
        )

    bases = []
    for hypothesis in request.hypothesis_candidates:
        bases.append(
            (
                "HYPOTHESIS_ALTERNATIVE",
                hypothesis.hypothesis_id,
                (hypothesis.hypothesis_id,),
                (),
                tuple(hypothesis.supporting_evidence_refs),
                tuple(hypothesis.conflict_refs) + tuple(request.conflict_refs),
            )
        )
    for gap_ref, need_refs in request.unresolved_gap_need_refs:
        bases.append(
            (
                "UNRESOLVED_INFORMATION_GAP",
                gap_ref,
                (),
                tuple(need_refs),
                tuple(request.evidence_refs),
                tuple(request.conflict_refs),
            )
        )
    for alternative_ref in request.explicit_alternative_refs:
        bases.append(
            (
                "EXPLICIT_GOVERNED_ALTERNATIVE",
                alternative_ref,
                (),
                (),
                tuple(request.evidence_refs),
                tuple(request.conflict_refs),
            )
        )

    unique_bases = []
    seen = set()
    for basis in bases:
        key = (basis[0], basis[1])
        if key not in seen:
            seen.add(key)
            unique_bases.append(basis)

    branches = []
    for basis_kind, basis_ref, hypothesis_refs, need_refs, evidence_refs, conflict_refs in unique_bases:
        branch_ref = _branch_id(
            request.parent_cognitive_problem_ref, basis_kind, basis_ref
        )
        branch_trace = _branch_trace(request.formation_ref, branch_ref)
        lineage = _unique(
            (
                request.parent_cognitive_problem_ref,
                request.source_state_ref,
                request.formation_ref,
                basis_ref,
                *hypothesis_refs,
                *need_refs,
            )
        )
        branches.append(
            CognitiveBranchCandidateV1(
                branch_ref=branch_ref,
                parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
                source_state_ref=request.source_state_ref,
                formation_basis=basis_kind,
                basis_ref=basis_ref,
                lineage_refs=lineage,
                derived_from_refs=(basis_ref,),
                hypothesis_refs=_unique(hypothesis_refs),
                information_need_refs=_unique(need_refs),
                information_gap_refs=(
                    (basis_ref,) if basis_kind == "UNRESOLVED_INFORMATION_GAP" else ()
                ),
                evidence_refs=_unique(evidence_refs),
                conflict_refs=_unique(conflict_refs),
                formation_status="FORMED_CANDIDATE",
                trace_ref=branch_trace,
                provenance_refs=_unique((*provenance, request.trace_ref, branch_trace)),
            )
        )

    status = "FORMED_CANDIDATES" if branches else "NO_EXPLICIT_BRANCH_BASIS"
    return GovernedCognitiveBranchFormationResultV1(
        formation_ref=request.formation_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        formation_status=status,
        branch_refs=tuple(item.branch_ref for item in branches),
        branches=tuple(branches),
        trace_ref=trace_ref,
        provenance_refs=provenance,
    )


__all__ = [
    "BRANCH_FORMATION_BASIS",
    "CognitiveBranchCandidateV1",
    "GovernedCognitiveBranchFormationInputV1",
    "GovernedCognitiveBranchFormationResultV1",
    "form_governed_cognitive_branches",
]
