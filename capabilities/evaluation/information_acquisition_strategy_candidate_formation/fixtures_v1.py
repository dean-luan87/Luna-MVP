"""Controlled inputs for governed acquisition strategy formation."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Tuple

from capabilities.midplatform.core.cognitive_flow.cognitive_branch_governance_v1 import (
    CognitiveBranchGovernanceDecisionV1,
)
from capabilities.midplatform.core.cognitive_flow.governed_cognitive_branch_formation_v1 import (
    CognitiveBranchCandidateV1,
)
from capabilities.midplatform.core.cognitive_flow.information_acquisition_strategy_candidate_formation_v1 import (
    GovernedAcquisitionBasisV1,
    InformationAcquisitionStrategyFormationInputV1,
)
from capabilities.midplatform.model_manager.registries.universal_capability_slot.cognitive_need_capability_requirement_bridge_types_v1 import (
    CognitiveNeedCandidateV1,
)


SOURCE_MODE = (
    "CONTROLLED_INFORMATION_ACQUISITION_STRATEGY_CANDIDATE_FORMATION_TEST"
)
PARENT_PROBLEM_REF = "problem:controlled:acquisition:v1"
SOURCE_STATE_REF = "state:controlled:acquisition:v1"
NEED_REF = "need:controlled:unknown:v1"
GAP_REF = "gap:controlled:unknown:v1"


@dataclass(frozen=True)
class AcquisitionStrategyFormationCaseV1:
    case_id: str
    request: InformationAcquisitionStrategyFormationInputV1
    expected_status: str
    expected_strategy_count: int
    evaluation_marker: str = ""


def _branch(branch_ref: str, basis_ref: str) -> CognitiveBranchCandidateV1:
    return CognitiveBranchCandidateV1(
        branch_ref=branch_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        formation_basis="HYPOTHESIS_ALTERNATIVE",
        basis_ref=basis_ref,
        lineage_refs=(f"lineage:{branch_ref}",),
        derived_from_refs=(basis_ref,),
        hypothesis_refs=(basis_ref,),
        information_need_refs=(NEED_REF,),
        information_gap_refs=(GAP_REF,),
        evidence_refs=(f"evidence:{branch_ref}",),
        conflict_refs=(),
        formation_status="FORMED_CANDIDATE",
        trace_ref=f"trace:branch:{branch_ref}",
        provenance_refs=(f"provenance:{branch_ref}",),
    )


def _need() -> CognitiveNeedCandidateV1:
    return CognitiveNeedCandidateV1(
        need_id=NEED_REF,
        source_intent_ref="intent:controlled:acquisition:v1",
        source_context_ref="context:controlled:opaque:v1",
        source_field_ref="field:controlled:acquisition:v1",
        source_hypothesis_ref="hypothesis:controlled:acquisition:v1",
        source_attention_ref=None,
        problem_description="controlled missing cognitive information",
        missing_information_class="CONTROLLED_UNKNOWN",
        required_evidence_class="CONTROLLED_EVIDENCE",
        urgency="NORMAL",
        safety_relevance="NONE",
        trace_ref="trace:need:controlled:unknown:v1",
        state_version_ref=SOURCE_STATE_REF,
    )


def _decision(
    governance_ref: str,
    branch: CognitiveBranchCandidateV1,
    status: str,
    reason: str = "VALID_CURRENT_BASIS",
) -> CognitiveBranchGovernanceDecisionV1:
    return CognitiveBranchGovernanceDecisionV1(
        governance_decision_ref=f"governance-decision:{governance_ref}:{branch.branch_ref}",
        branch_ref=branch.branch_ref,
        governance_status=status,
        reason_code=reason,
        governance_basis_refs=(branch.basis_ref,),
        candidate_lineage_refs=branch.lineage_refs,
        candidate_provenance_refs=branch.provenance_refs,
        source_state_ref=SOURCE_STATE_REF,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        provenance_refs=(f"provenance:governance:{governance_ref}",),
        trace_ref=f"trace:governance:{governance_ref}:{branch.branch_ref}",
        recoverable=status != "REJECTED",
    )


def _basis(
    basis_ref: str,
    branch_ref: str,
    *,
    mode: str = "PERCEPTION",
    contribution: Tuple[str, ...] = ("information:controlled:contribution:v1",),
    capability_refs: Tuple[str, ...] = (),
    opportunity_refs: Tuple[str, ...] = (),
) -> GovernedAcquisitionBasisV1:
    return GovernedAcquisitionBasisV1(
        basis_ref=basis_ref,
        branch_ref=branch_ref,
        information_need_refs=(NEED_REF,),
        information_gap_refs=(GAP_REF,),
        acquisition_mode_candidate=mode,
        expected_information_contribution_refs=contribution,
        required_capability_class_refs=capability_refs,
        opportunity_refs=opportunity_refs,
        dependency_refs=(f"dependency:{basis_ref}",),
        provenance_refs=(f"provenance:basis:{basis_ref}",),
    )


def _request(
    formation_ref: str,
    branches: Tuple[CognitiveBranchCandidateV1, ...],
    decisions: Tuple[CognitiveBranchGovernanceDecisionV1, ...],
    bases: Tuple[GovernedAcquisitionBasisV1, ...] = (),
    *,
    context_refs: Tuple[str, ...] = ("context:controlled:opaque:a",),
    candidate_only: bool = True,
) -> InformationAcquisitionStrategyFormationInputV1:
    return InformationAcquisitionStrategyFormationInputV1(
        formation_ref=formation_ref,
        parent_cognitive_problem_ref=PARENT_PROBLEM_REF,
        source_state_ref=SOURCE_STATE_REF,
        branch_candidates=branches,
        governance_decisions=decisions,
        need_candidates=(_need(),),
        governed_acquisition_bases=bases,
        current_cognitive_state_ref=SOURCE_STATE_REF,
        context_refs=context_refs,
        trace_ref=f"trace:strategy-formation:{formation_ref}",
        provenance_refs=("provenance:controlled:strategy-formation:v1",),
        candidate_only=candidate_only,
    )


def build_information_acquisition_strategy_cases_v1() -> Tuple[
    AcquisitionStrategyFormationCaseV1, ...
]:
    branch_a = _branch("branch:controlled:a", "hypothesis:controlled:a")
    branch_b = _branch("branch:controlled:b", "hypothesis:controlled:b")
    branch_c = _branch("branch:controlled:c", "hypothesis:controlled:c")
    admitted_a = _decision("admitted-a", branch_a, "ADMITTED")
    admitted_b = _decision("admitted-b", branch_b, "ADMITTED")
    deferred_a = _decision("deferred-a", branch_a, "DEFERRED", "CURRENTLY_NOT_NEEDED")
    rejected_a = _decision("rejected-a", branch_a, "REJECTED", "BASIS_NOT_CURRENT")

    return (
        AcquisitionStrategyFormationCaseV1(
            "ONE_BRANCH_ONE_STRATEGY",
            _request(
                "one-one",
                (branch_a,),
                (admitted_a,),
                (_basis("basis:controlled:a", branch_a.branch_ref),),
            ),
            "FORMED_CANDIDATES",
            1,
        ),
        AcquisitionStrategyFormationCaseV1(
            "ONE_BRANCH_MULTIPLE_STRATEGIES",
            _request(
                "one-many",
                (branch_a,),
                (admitted_a,),
                tuple(
                    _basis(ref, branch_a.branch_ref)
                    for ref in ("basis:controlled:a", "basis:controlled:b", "basis:controlled:c")
                ),
            ),
            "FORMED_CANDIDATES",
            3,
        ),
        AcquisitionStrategyFormationCaseV1(
            "MULTIPLE_BRANCHES_MULTIPLE_STRATEGIES",
            _request(
                "many-many",
                (branch_a, branch_b),
                (admitted_a, admitted_b),
                (
                    _basis("basis:controlled:a1", branch_a.branch_ref),
                    _basis("basis:controlled:a2", branch_a.branch_ref),
                    _basis("basis:controlled:b1", branch_b.branch_ref),
                ),
            ),
            "FORMED_CANDIDATES",
            3,
        ),
        AcquisitionStrategyFormationCaseV1(
            "NO_GOVERNED_ACQUISITION_BASIS",
            _request("no-basis", (branch_a,), (admitted_a,)),
            "NO_GOVERNED_ACQUISITION_BASIS",
            0,
        ),
        AcquisitionStrategyFormationCaseV1(
            "DEFERRED_BRANCH",
            _request(
                "deferred",
                (branch_a,),
                (deferred_a,),
                (_basis("basis:controlled:deferred", branch_a.branch_ref),),
            ),
            "NO_ADMITTED_BRANCH",
            0,
        ),
        AcquisitionStrategyFormationCaseV1(
            "REJECTED_BRANCH",
            _request(
                "rejected",
                (branch_a,),
                (rejected_a,),
                (_basis("basis:controlled:rejected", branch_a.branch_ref),),
            ),
            "NO_ADMITTED_BRANCH",
            0,
        ),
        AcquisitionStrategyFormationCaseV1(
            "IRRELEVANT_CONTEXT_CHANGE:base",
            _request(
                "context-stability",
                (branch_a,),
                (admitted_a,),
                (_basis("basis:controlled:stable", branch_a.branch_ref),),
                context_refs=("context:controlled:opaque:base",),
            ),
            "FORMED_CANDIDATES",
            1,
        ),
        AcquisitionStrategyFormationCaseV1(
            "IRRELEVANT_CONTEXT_CHANGE:changed",
            _request(
                "context-stability",
                (branch_a,),
                (admitted_a,),
                (_basis("basis:controlled:stable", branch_a.branch_ref),),
                context_refs=("context:controlled:opaque:changed",),
            ),
            "FORMED_CANDIDATES",
            1,
        ),
        AcquisitionStrategyFormationCaseV1(
            "SAME_NEED_DIFFERENT_GOVERNED_BASES:base",
            _request(
                "basis-sensitivity",
                (branch_a,),
                (admitted_a,),
                (
                    _basis("basis:controlled:a", branch_a.branch_ref),
                    _basis("basis:controlled:b", branch_a.branch_ref),
                ),
            ),
            "FORMED_CANDIDATES",
            2,
        ),
        AcquisitionStrategyFormationCaseV1(
            "SAME_NEED_DIFFERENT_GOVERNED_BASES:changed",
            _request(
                "basis-sensitivity",
                (branch_a,),
                (admitted_a,),
                (
                    _basis("basis:controlled:a", branch_a.branch_ref),
                    _basis("basis:controlled:c", branch_a.branch_ref),
                ),
            ),
            "FORMED_CANDIDATES",
            2,
        ),
        AcquisitionStrategyFormationCaseV1(
            "UNKNOWN_MODE",
            _request(
                "unknown-mode",
                (branch_a,),
                (admitted_a,),
                (_basis("basis:controlled:unknown-mode", branch_a.branch_ref, mode=""),),
            ),
            "FORMED_CANDIDATES",
            1,
        ),
        AcquisitionStrategyFormationCaseV1(
            "CAPABILITY_CLASS_REF_PRESERVATION",
            _request(
                "capability-ref",
                (branch_a,),
                (admitted_a,),
                (
                    _basis(
                        "basis:controlled:capability",
                        branch_a.branch_ref,
                        capability_refs=("capability-class:controlled:evidence",),
                    ),
                ),
            ),
            "FORMED_CANDIDATES",
            1,
        ),
        AcquisitionStrategyFormationCaseV1(
            "OPPORTUNITY_REF_PRESERVATION",
            _request(
                "opportunity-ref",
                (branch_a,),
                (admitted_a,),
                (
                    _basis(
                        "basis:controlled:opportunity",
                        branch_a.branch_ref,
                        opportunity_refs=("opportunity:controlled:visible",),
                    ),
                ),
            ),
            "FORMED_CANDIDATES",
            1,
        ),
        AcquisitionStrategyFormationCaseV1(
            "NO_BRANCHES",
            _request("no-branches", (), (), ()),
            "NO_ADMITTED_BRANCH",
            0,
        ),
        AcquisitionStrategyFormationCaseV1(
            "INVALID_INPUT",
            _request(
                "invalid-input",
                (replace(branch_a, candidate_only=False),),
                (admitted_a,),
                (_basis("basis:controlled:invalid", branch_a.branch_ref),),
                candidate_only=False,
            ),
            "INVALID_INPUT",
            0,
        ),
    )


__all__ = [
    "SOURCE_MODE",
    "AcquisitionStrategyFormationCaseV1",
    "build_information_acquisition_strategy_cases_v1",
]
