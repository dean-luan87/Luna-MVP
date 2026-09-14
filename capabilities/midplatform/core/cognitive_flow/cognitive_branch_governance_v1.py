"""Candidate-only governance for already formed cognitive branches.

This module evaluates formed branch candidates against an explicit governed
current cognitive state.  It emits immutable governance decisions only; it
does not mutate candidates, form new branches, acquire resources, or run a
loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Tuple

from .governed_cognitive_branch_formation_v1 import CognitiveBranchCandidateV1


GOVERNANCE_STATUSES = ("ADMITTED", "DEFERRED", "REJECTED")
GOVERNANCE_OWNER = "Cognitive Flow Branch Governance"
REASON_CODES = (
    "VALID_CURRENT_BASIS",
    "BASIS_NOT_CURRENT",
    "CURRENTLY_NOT_NEEDED",
    "INVALID_CANDIDATE",
    "PROBLEM_REF_MISMATCH",
    "SOURCE_STATE_NOT_CURRENT",
)


@dataclass(frozen=True)
class CognitiveBranchGovernanceDecisionV1:
    """One immutable decision about one formed Branch Candidate."""

    governance_decision_ref: str
    branch_ref: str
    governance_status: str
    reason_code: str
    governance_basis_refs: Tuple[str, ...]
    candidate_lineage_refs: Tuple[str, ...]
    candidate_provenance_refs: Tuple[str, ...]
    source_state_ref: str
    parent_cognitive_problem_ref: str
    provenance_refs: Tuple[str, ...]
    trace_ref: str
    candidate_only: bool = True
    read_only: bool = True
    candidate_retained: bool = True
    recoverable: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False


@dataclass(frozen=True)
class CognitiveBranchGovernanceInputV1:
    """Explicit governed state used to evaluate formed branch candidates."""

    governance_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    branch_candidates: Tuple[CognitiveBranchCandidateV1, ...] = field(
        default_factory=tuple
    )
    current_hypothesis_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_information_need_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_information_gap_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_conflict_refs: Tuple[str, ...] = field(default_factory=tuple)
    current_alternative_refs: Tuple[str, ...] = field(default_factory=tuple)
    currently_satisfied_need_refs: Tuple[str, ...] = field(default_factory=tuple)
    currently_not_needed_branch_refs: Tuple[str, ...] = field(default_factory=tuple)
    context_refs: Tuple[str, ...] = field(default_factory=tuple)
    trace_ref: str = ""
    provenance_refs: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveBranchGovernanceResultV1:
    """Candidate-only governance output; it is not execution scheduling."""

    governance_ref: str
    parent_cognitive_problem_ref: str
    source_state_ref: str
    governance_status: str
    input_branch_refs: Tuple[str, ...]
    admitted_branch_refs: Tuple[str, ...]
    deferred_branch_refs: Tuple[str, ...]
    rejected_branch_refs: Tuple[str, ...]
    governance_decisions: Tuple[CognitiveBranchGovernanceDecisionV1, ...]
    trace_ref: str
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    read_only: bool = True
    formation_executed: bool = False
    new_branch_generated: bool = False
    winner_take_all: bool = False
    execution_priority_assigned: bool = False
    resource_governance_executed: bool = False
    resource_acquisition: bool = False
    observation_demand_formed: bool = False
    capability_requirement_formed: bool = False
    current_world_mutation: bool = False
    field_mutation: bool = False
    truth_declared: bool = False
    world_truth_declared: bool = False
    decision_formed: bool = False
    task_formed: bool = False
    action_formed: bool = False
    provider_invocation: bool = False
    model_invocation: bool = False
    memory_pcn_mutation: bool = False
    merge_executed: bool = False
    convergence_executed: bool = False
    close_executed: bool = False
    reopen_executed: bool = False
    validation_errors: Tuple[str, ...] = ()


def _unique(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(dict.fromkeys(value for value in values if value and value.strip()))


def _decision_ref(governance_ref: str, branch_ref: str) -> str:
    return f"governance-decision:{governance_ref}:{branch_ref}"


def _decision_trace(governance_ref: str, branch_ref: str) -> str:
    return f"trace:{governance_ref}:{branch_ref}"


def _basis_current(
    branch: CognitiveBranchCandidateV1,
    request: CognitiveBranchGovernanceInputV1,
) -> bool:
    if branch.conflict_refs and not set(branch.conflict_refs).issubset(
        set(request.current_conflict_refs)
    ):
        return False
    if branch.formation_basis == "HYPOTHESIS_ALTERNATIVE":
        return branch.basis_ref in set(request.current_hypothesis_refs)
    if branch.formation_basis == "UNRESOLVED_INFORMATION_GAP":
        current_gaps = set(request.current_information_gap_refs)
        current_needs = set(request.current_information_need_refs)
        return branch.basis_ref in current_gaps and set(
            branch.information_need_refs
        ).issubset(current_needs)
    if branch.formation_basis == "EXPLICIT_GOVERNED_ALTERNATIVE":
        return branch.basis_ref in set(request.current_alternative_refs)
    return False


def _validate_request(
    request: CognitiveBranchGovernanceInputV1,
) -> Tuple[str, ...]:
    errors = []
    if not request.governance_ref:
        errors.append("governance_ref_missing")
    if not request.parent_cognitive_problem_ref:
        errors.append("parent_cognitive_problem_ref_missing")
    if not request.source_state_ref:
        errors.append("source_state_ref_missing")
    if not request.trace_ref:
        errors.append("trace_ref_missing")
    if not request.candidate_only:
        errors.append("governance_not_candidate_only")
    branch_refs = [branch.branch_ref for branch in request.branch_candidates]
    if len(set(branch_refs)) != len(branch_refs):
        errors.append("duplicate_branch_ref")
    return tuple(dict.fromkeys(errors))


def _invalid_result(
    request: CognitiveBranchGovernanceInputV1,
    errors: Tuple[str, ...],
) -> CognitiveBranchGovernanceResultV1:
    return CognitiveBranchGovernanceResultV1(
        governance_ref=request.governance_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        governance_status="INVALID_INPUT",
        input_branch_refs=tuple(branch.branch_ref for branch in request.branch_candidates),
        admitted_branch_refs=(),
        deferred_branch_refs=(),
        rejected_branch_refs=(),
        governance_decisions=(),
        trace_ref=request.trace_ref or f"trace:{request.governance_ref}",
        provenance_refs=_unique(
            ("provenance:cognitive-branch-governance:v1", *request.provenance_refs)
        ),
        candidate_only=request.candidate_only,
        validation_errors=errors,
    )


def govern_cognitive_branches(
    request: CognitiveBranchGovernanceInputV1,
) -> CognitiveBranchGovernanceResultV1:
    """Evaluate formed branches without mutating or scheduling them."""

    errors = _validate_request(request)
    if errors:
        return _invalid_result(request, errors)

    trace_ref = request.trace_ref
    provenance = _unique(
        ("provenance:cognitive-branch-governance:v1", *request.provenance_refs)
    )
    decisions = []
    admitted = []
    deferred = []
    rejected = []

    for branch in request.branch_candidates:
        basis_refs = _unique(
            (
                branch.basis_ref,
                *branch.hypothesis_refs,
                *branch.information_need_refs,
                *branch.information_gap_refs,
                *branch.derived_from_refs,
            )
        )
        status = "ADMITTED"
        reason = "VALID_CURRENT_BASIS"
        recoverable = True

        if (
            not branch.candidate_only
            or not branch.read_only
            or branch.truth_declared
            or branch.world_truth_declared
            or branch.current_world_mutation
            or branch.field_mutation
            or branch.formation_status != "FORMED_CANDIDATE"
        ):
            status = "REJECTED"
            reason = "INVALID_CANDIDATE"
            recoverable = False
        elif branch.parent_cognitive_problem_ref != request.parent_cognitive_problem_ref:
            status = "REJECTED"
            reason = "PROBLEM_REF_MISMATCH"
            recoverable = False
        elif branch.source_state_ref != request.source_state_ref:
            status = "REJECTED"
            reason = "SOURCE_STATE_NOT_CURRENT"
            recoverable = False
        elif not _basis_current(branch, request):
            status = "REJECTED"
            reason = "BASIS_NOT_CURRENT"
            recoverable = False
        elif branch.branch_ref in set(request.currently_not_needed_branch_refs) and (
            not branch.information_need_refs
            or set(branch.information_need_refs).issubset(
                set(request.currently_satisfied_need_refs)
            )
        ):
            status = "DEFERRED"
            reason = "CURRENTLY_NOT_NEEDED"

        decision = CognitiveBranchGovernanceDecisionV1(
            governance_decision_ref=_decision_ref(
                request.governance_ref, branch.branch_ref
            ),
            branch_ref=branch.branch_ref,
            governance_status=status,
            reason_code=reason,
            governance_basis_refs=basis_refs,
            source_state_ref=request.source_state_ref,
            parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
            candidate_lineage_refs=_unique(branch.lineage_refs),
            candidate_provenance_refs=_unique(branch.provenance_refs),
            provenance_refs=_unique(
                (*provenance, *branch.provenance_refs, branch.trace_ref)
            ),
            trace_ref=_decision_trace(request.governance_ref, branch.branch_ref),
            recoverable=recoverable,
        )
        decisions.append(decision)
        if status == "ADMITTED":
            admitted.append(branch.branch_ref)
        elif status == "DEFERRED":
            deferred.append(branch.branch_ref)
        else:
            rejected.append(branch.branch_ref)

    status = "GOVERNANCE_DECISIONS_FORMED"
    if not request.branch_candidates:
        status = "NO_BRANCHES"
    return CognitiveBranchGovernanceResultV1(
        governance_ref=request.governance_ref,
        parent_cognitive_problem_ref=request.parent_cognitive_problem_ref,
        source_state_ref=request.source_state_ref,
        governance_status=status,
        input_branch_refs=tuple(branch.branch_ref for branch in request.branch_candidates),
        admitted_branch_refs=tuple(admitted),
        deferred_branch_refs=tuple(deferred),
        rejected_branch_refs=tuple(rejected),
        governance_decisions=tuple(decisions),
        trace_ref=trace_ref,
        provenance_refs=provenance,
    )


__all__ = [
    "GOVERNANCE_STATUSES",
    "GOVERNANCE_OWNER",
    "REASON_CODES",
    "CognitiveBranchGovernanceDecisionV1",
    "CognitiveBranchGovernanceInputV1",
    "CognitiveBranchGovernanceResultV1",
    "govern_cognitive_branches",
]
