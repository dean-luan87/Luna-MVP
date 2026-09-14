"""Controlled inputs for candidate-only Branch Governance."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceInputV1,
)
from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    CognitiveBranchCandidateV1,
    form_governed_cognitive_branches,
)
from capabilities.evaluation.governed_cognitive_branch_formation.fixtures_v1 import (
    build_branch_formation_cases_v1,
)


SOURCE_MODE = "CONTROLLED_COGNITIVE_BRANCH_GOVERNANCE_TEST"
PARENT_PROBLEM_REF = "problem:controlled:current-question:v1"
SOURCE_STATE_REF = "state:controlled:cognitive:v1"


@dataclass(frozen=True)
class BranchGovernanceCaseV1:
    case_id: str
    request: CognitiveBranchGovernanceInputV1
    expected_statuses: Tuple[str, ...]
    evaluation_marker: str = ""


def _formed(case_id: str) -> Tuple[CognitiveBranchCandidateV1, ...]:
    source_case = next(
        case
        for case in build_branch_formation_cases_v1()
        if case.case_id == case_id
    )
    return form_governed_cognitive_branches(source_case.request).branches


def _request(
    governance_ref: str,
    branches: Tuple[CognitiveBranchCandidateV1, ...],
    *,
    current_hypothesis_refs: Tuple[str, ...] = (),
    current_information_need_refs: Tuple[str, ...] = (),
    current_information_gap_refs: Tuple[str, ...] = (),
    current_conflict_refs: Tuple[str, ...] = (),
    currently_satisfied_need_refs: Tuple[str, ...] = (),
    currently_not_needed_branch_refs: Tuple[str, ...] = (),
    context_refs: Tuple[str, ...] = ("context:controlled:opaque:a",),
) -> CognitiveBranchGovernanceInputV1:
    return CognitiveBranchGovernanceInputV1(
        governance_ref=governance_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        branch_candidates=branches,
        current_hypothesis_refs=current_hypothesis_refs,
        current_information_need_refs=current_information_need_refs,
        current_information_gap_refs=current_information_gap_refs,
        current_conflict_refs=current_conflict_refs,
        currently_satisfied_need_refs=currently_satisfied_need_refs,
        currently_not_needed_branch_refs=currently_not_needed_branch_refs,
        context_refs=context_refs,
        trace_ref=f"trace:governance:{governance_ref}",
        provenance_refs=("provenance:controlled:branch-governance:v1",),
    )


def build_branch_governance_cases_v1() -> Tuple[BranchGovernanceCaseV1, ...]:
    hypothesis_branches = _formed("MULTIPLE_HYPOTHESIS_ALTERNATIVES")
    hypothesis_a, hypothesis_b = hypothesis_branches
    gap_branches = _formed("MULTIPLE_UNRESOLVED_GAPS")
    gap_location, _gap_access = gap_branches

    invalid_candidate = replace(hypothesis_a, truth_declared=True)

    return (
        BranchGovernanceCaseV1(
            "MULTIPLE_VALID_BRANCHES",
            _request(
                "multiple-valid",
                hypothesis_branches,
                current_hypothesis_refs=(
                    "hypothesis:controlled:a",
                    "hypothesis:controlled:b",
                ),
            ),
            ("ADMITTED", "ADMITTED"),
        ),
        BranchGovernanceCaseV1(
            "ONE_VALID_ONE_INVALID_BASIS",
            _request(
                "one-valid-one-invalid",
                hypothesis_branches,
                current_hypothesis_refs=("hypothesis:controlled:a",),
            ),
            ("ADMITTED", "REJECTED"),
        ),
        BranchGovernanceCaseV1(
            "CURRENTLY_NOT_NEEDED_BUT_VALID",
            _request(
                "currently-not-needed",
                (hypothesis_a,),
                current_hypothesis_refs=("hypothesis:controlled:a",),
                currently_not_needed_branch_refs=(hypothesis_a.branch_ref,),
            ),
            ("DEFERRED",),
        ),
        BranchGovernanceCaseV1(
            "NO_CANONICAL_EQUIVALENCE_RETAIN_BOTH",
            _request(
                "no-canonical-equivalence",
                hypothesis_branches,
                current_hypothesis_refs=(
                    "hypothesis:controlled:a",
                    "hypothesis:controlled:b",
                ),
            ),
            ("ADMITTED", "ADMITTED"),
        ),
        BranchGovernanceCaseV1(
            "NO_BRANCHES",
            _request("no-branches", ()),
            (),
        ),
        BranchGovernanceCaseV1(
            "IRRELEVANT_CONTEXT_CHANGE",
            _request(
                "irrelevant-context",
                hypothesis_branches,
                current_hypothesis_refs=(
                    "hypothesis:controlled:a",
                    "hypothesis:controlled:b",
                ),
                context_refs=("context:controlled:opaque:changed",),
            ),
            ("ADMITTED", "ADMITTED"),
        ),
        BranchGovernanceCaseV1(
            "BASIS_REMOVED:base",
            _request(
                "basis-removed-base",
                (hypothesis_a,),
                current_hypothesis_refs=("hypothesis:controlled:a",),
            ),
            ("ADMITTED",),
        ),
        BranchGovernanceCaseV1(
            "BASIS_REMOVED:changed",
            _request("basis-removed-changed", (hypothesis_a,)),
            ("REJECTED",),
        ),
        BranchGovernanceCaseV1(
            "NEED_BECOMES_CURRENTLY_SATISFIED:base",
            _request(
                "need-satisfied-base",
                (gap_location,),
                current_information_need_refs=("need:controlled:location",),
                current_information_gap_refs=("gap:controlled:location",),
            ),
            ("ADMITTED",),
        ),
        BranchGovernanceCaseV1(
            "NEED_BECOMES_CURRENTLY_SATISFIED:changed",
            _request(
                "need-satisfied-changed",
                (gap_location,),
                current_information_need_refs=("need:controlled:location",),
                current_information_gap_refs=("gap:controlled:location",),
                currently_satisfied_need_refs=("need:controlled:location",),
                currently_not_needed_branch_refs=(gap_location.branch_ref,),
            ),
            ("DEFERRED",),
        ),
        BranchGovernanceCaseV1(
            "RESOURCE_AVAILABILITY_CHANGE:available",
            _request(
                "resource-availability",
                hypothesis_branches,
                current_hypothesis_refs=(
                    "hypothesis:controlled:a",
                    "hypothesis:controlled:b",
                ),
            ),
            ("ADMITTED", "ADMITTED"),
            evaluation_marker="provider=available;budget=ample",
        ),
        BranchGovernanceCaseV1(
            "RESOURCE_AVAILABILITY_CHANGE:unavailable",
            _request(
                "resource-availability",
                hypothesis_branches,
                current_hypothesis_refs=(
                    "hypothesis:controlled:a",
                    "hypothesis:controlled:b",
                ),
            ),
            ("ADMITTED", "ADMITTED"),
            evaluation_marker="provider=unavailable;budget=low",
        ),
        BranchGovernanceCaseV1(
            "INVALID_CANDIDATE",
            _request(
                "invalid-candidate",
                (invalid_candidate,),
                current_hypothesis_refs=("hypothesis:controlled:a",),
            ),
            ("REJECTED",),
        ),
    )


__all__ = [
    "SOURCE_MODE",
    "BranchGovernanceCaseV1",
    "build_branch_governance_cases_v1",
]
