"""Controlled inputs for candidate-only governed branch formation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    GovernedCognitiveBranchFormationInputV1,
)
from capabilities.midplatform.core.cognitive_state_formation.cognitive_hypothesis_types_v1 import (
    CognitiveHypothesisCandidateV1,
)


SOURCE_MODE = "CONTROLLED_GOVERNED_COGNITIVE_BRANCH_FORMATION_TEST"


@dataclass(frozen=True)
class BranchFormationCaseV1:
    case_id: str
    request: GovernedCognitiveBranchFormationInputV1
    expected_branch_count: int
    expected_basis: Tuple[str, ...]


def _hypothesis(
    hypothesis_id: str,
    *,
    evidence_ref: str,
    conflict_refs: Tuple[str, ...] = (),
) -> CognitiveHypothesisCandidateV1:
    return CognitiveHypothesisCandidateV1(
        hypothesis_id=hypothesis_id,
        hypothesis_statement_candidate=f"explicit explanation candidate {hypothesis_id}",
        subject_refs=("subject:controlled:problem",),
        supporting_evidence_refs=(evidence_ref,),
        opposing_evidence_refs=(),
        alternative_hypothesis_refs=(),
        unknown_refs=(),
        conflict_refs=conflict_refs,
        attention_refs=(),
        context_refs=("context:controlled:opaque",),
        field_refs=("field:controlled",),
        pcn_refs=(),
        intent_refs=("intent:controlled:exploration",),
        confidence_candidate="LOW",
        state="CONTESTED" if conflict_refs else "SUPPORTED",
        revision_parent_ref=None,
        trace_ref=f"trace:{hypothesis_id}",
        provenance_refs=(f"provenance:{hypothesis_id}",),
    )


def _request(
    formation_ref: str,
    *,
    hypotheses: Tuple[CognitiveHypothesisCandidateV1, ...] = (),
    gap_need_refs: Tuple[Tuple[str, Tuple[str, ...]], ...] = (),
    alternatives: Tuple[str, ...] = (),
    evidence_refs: Tuple[str, ...] = (),
    conflict_refs: Tuple[str, ...] = (),
    context_refs: Tuple[str, ...] = ("context:controlled:opaque:a",),
    candidate_only: bool = True,
) -> GovernedCognitiveBranchFormationInputV1:
    return GovernedCognitiveBranchFormationInputV1(
        formation_ref=formation_ref,
        parent_cognitive_problem_ref="problem:controlled:current-question:v1",
        source_state_ref="state:controlled:cognitive:v1",
        hypothesis_candidates=hypotheses,
        unresolved_gap_need_refs=gap_need_refs,
        explicit_alternative_refs=alternatives,
        evidence_refs=evidence_refs,
        conflict_refs=conflict_refs,
        context_refs=context_refs,
        trace_ref=f"trace:formation:{formation_ref}",
        provenance_refs=("provenance:controlled:branch-input:v1",),
        candidate_only=candidate_only,
    )


def build_branch_formation_cases_v1() -> Tuple[BranchFormationCaseV1, ...]:
    hypothesis_a = _hypothesis("hypothesis:controlled:a", evidence_ref="evidence:controlled:a")
    hypothesis_b = _hypothesis("hypothesis:controlled:b", evidence_ref="evidence:controlled:b")
    hypothesis_c = _hypothesis("hypothesis:controlled:c", evidence_ref="evidence:controlled:c")
    conflict = ("conflict:controlled:ab",)
    return (
        BranchFormationCaseV1(
            "SINGLE_SUFFICIENT_EXPLANATION",
            _request(
                "single-sufficient",
                hypotheses=(
                    _hypothesis(
                        "hypothesis:controlled:single",
                        evidence_ref="evidence:controlled:single",
                    ),
                ),
            ),
            1,
            ("HYPOTHESIS_ALTERNATIVE",),
        ),
        BranchFormationCaseV1(
            "MULTIPLE_HYPOTHESIS_ALTERNATIVES",
            _request("multiple-hypotheses", hypotheses=(hypothesis_a, hypothesis_b)),
            2,
            ("HYPOTHESIS_ALTERNATIVE", "HYPOTHESIS_ALTERNATIVE"),
        ),
        BranchFormationCaseV1(
            "MULTIPLE_UNRESOLVED_GAPS",
            _request(
                "multiple-gaps",
                gap_need_refs=(
                    ("gap:controlled:location", ("need:controlled:location",)),
                    ("gap:controlled:access", ("need:controlled:access",)),
                ),
            ),
            2,
            ("UNRESOLVED_INFORMATION_GAP", "UNRESOLVED_INFORMATION_GAP"),
        ),
        BranchFormationCaseV1(
            "EXPLICIT_CONFLICT_WITH_EXISTING_ALTERNATIVES",
            _request(
                "conflict-alternatives",
                hypotheses=(
                    _hypothesis("hypothesis:controlled:conflict-a", evidence_ref="evidence:controlled:a", conflict_refs=conflict),
                    _hypothesis("hypothesis:controlled:conflict-b", evidence_ref="evidence:controlled:b", conflict_refs=conflict),
                ),
                conflict_refs=conflict,
            ),
            2,
            ("HYPOTHESIS_ALTERNATIVE", "HYPOTHESIS_ALTERNATIVE"),
        ),
        BranchFormationCaseV1(
            "IRRELEVANT_CONTEXT_CHANGE",
            _request(
                "context-change",
                hypotheses=(hypothesis_a, hypothesis_b),
                context_refs=("context:controlled:opaque:changed",),
            ),
            2,
            ("HYPOTHESIS_ALTERNATIVE", "HYPOTHESIS_ALTERNATIVE"),
        ),
        BranchFormationCaseV1(
            "SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES:base",
            _request("alternatives-base", hypotheses=(hypothesis_a, hypothesis_b)),
            2,
            ("HYPOTHESIS_ALTERNATIVE", "HYPOTHESIS_ALTERNATIVE"),
        ),
        BranchFormationCaseV1(
            "SAME_PROBLEM_DIFFERENT_EXISTING_ALTERNATIVES:changed",
            _request("alternatives-changed", hypotheses=(hypothesis_a, hypothesis_c)),
            2,
            ("HYPOTHESIS_ALTERNATIVE", "HYPOTHESIS_ALTERNATIVE"),
        ),
        BranchFormationCaseV1(
            "NO_EXPLICIT_BRANCH_BASIS",
            _request("no-basis", evidence_refs=("evidence:controlled:single",)),
            0,
            (),
        ),
    )


def build_negative_branch_formation_requests_v1() -> Tuple[Tuple[str, GovernedCognitiveBranchFormationInputV1], ...]:
    return (
        (
            "CANDIDATE_ONLY_FALSE",
            _request("negative-candidate-only", candidate_only=False),
        ),
        (
            "HYPOTHESIS_NOT_CANDIDATE_ONLY",
            _request(
                "negative-hypothesis",
                hypotheses=(
                    replace(
                        _hypothesis(
                            "hypothesis:controlled:invalid",
                            evidence_ref="evidence:controlled:invalid",
                        ),
                        candidate_only=False,
                    ),
                ),
            ),
        ),
    )


__all__ = [
    "SOURCE_MODE",
    "BranchFormationCaseV1",
    "build_branch_formation_cases_v1",
    "build_negative_branch_formation_requests_v1",
]
