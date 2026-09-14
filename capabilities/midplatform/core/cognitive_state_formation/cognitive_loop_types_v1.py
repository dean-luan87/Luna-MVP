"""Canonical candidate-only contracts for the minimum sufficient cognition loop."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


LOOP_OWNERS = ("Cognitive State Formation Governance", "Field Perception Orchestrator")
SUFFICIENCY_STATUSES = ("SUFFICIENT", "INSUFFICIENT")
STOP_REASONS = (
    "MINIMUM_SUFFICIENT_INFORMATION_REACHED",
    "NO_FURTHER_RELEVANT_OBSERVATION_REQUIRED",
)


@dataclass(frozen=True)
class CognitiveSufficiencyCandidateV1:
    sufficiency_ref: str
    owner_ref: str
    goal_ref: str
    concern_ref: str
    status: str
    evidence_refs: Tuple[str, ...]
    required_information_refs: Tuple[str, ...]
    missing_information_refs: Tuple[str, ...]
    reason: str
    stop_required: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveInformationGapCandidateV1:
    information_gap_ref: str
    owner_ref: str
    sufficiency_ref: str
    missing_information_refs: Tuple[str, ...]
    observation_need_ref: str
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveReobservationCandidateV1:
    reobservation_ref: str
    owner_ref: str
    information_gap_ref: str
    observation_need_ref: str
    next_cycle_ingress_ref: str
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveHypothesisRevisionCandidateV1:
    hypothesis_revision_ref: str
    owner_ref: str
    prior_hypothesis_refs: Tuple[str, ...]
    revised_hypothesis_refs: Tuple[str, ...]
    information_gap_ref: str
    reobservation_ref: str
    evidence_refs: Tuple[str, ...]
    reason: str
    candidate_only: bool = True


@dataclass(frozen=True)
class CognitiveStopCandidateV1:
    stop_ref: str
    owner_ref: str
    sufficiency_ref: str
    reason: str
    cycle_index: int
    candidate_only: bool = True


def validate_cognitive_loop_candidates_v1(
    *,
    sufficiency: CognitiveSufficiencyCandidateV1 | None,
    information_gap: CognitiveInformationGapCandidateV1 | None,
    reobservation: CognitiveReobservationCandidateV1 | None,
    hypothesis_revision: CognitiveHypothesisRevisionCandidateV1 | None,
    stop: CognitiveStopCandidateV1 | None,
) -> Tuple[str, ...]:
    errors = []
    if sufficiency is None:
        return ("sufficiency_candidate_missing",)
    if sufficiency.owner_ref != "Cognitive State Formation Governance":
        errors.append("sufficiency_owner_invalid")
    if sufficiency.status not in SUFFICIENCY_STATUSES:
        errors.append("sufficiency_status_invalid")
    if not sufficiency.candidate_only:
        errors.append("sufficiency_not_candidate_only")
    if sufficiency.status == "SUFFICIENT":
        if sufficiency.missing_information_refs or not sufficiency.stop_required or stop is None:
            errors.append("sufficient_state_stop_contract_invalid")
        if information_gap is not None or reobservation is not None:
            errors.append("sufficient_state_has_gap_or_reobservation")
    if sufficiency.status == "INSUFFICIENT":
        if not sufficiency.missing_information_refs or sufficiency.stop_required:
            errors.append("insufficient_state_gap_contract_invalid")
        if information_gap is None or reobservation is None:
            errors.append("insufficient_state_gap_or_reobservation_missing")
        if stop is not None:
            errors.append("insufficient_state_has_stop")
    if information_gap is not None:
        if information_gap.owner_ref != "Cognitive State Formation Governance":
            errors.append("information_gap_owner_invalid")
        if information_gap.sufficiency_ref != sufficiency.sufficiency_ref:
            errors.append("information_gap_sufficiency_link_invalid")
    if reobservation is not None:
        if reobservation.owner_ref != "Field Perception Orchestrator":
            errors.append("reobservation_owner_invalid")
        if information_gap is None or reobservation.information_gap_ref != information_gap.information_gap_ref:
            errors.append("reobservation_gap_link_invalid")
    if hypothesis_revision is not None:
        if hypothesis_revision.owner_ref != "Cognitive State Formation Governance":
            errors.append("hypothesis_revision_owner_invalid")
        if information_gap is None or reobservation is None:
            errors.append("hypothesis_revision_without_gap_reobservation")
        else:
            if hypothesis_revision.information_gap_ref != information_gap.information_gap_ref:
                errors.append("hypothesis_revision_gap_link_invalid")
            if hypothesis_revision.reobservation_ref != reobservation.reobservation_ref:
                errors.append("hypothesis_revision_reobservation_link_invalid")
    if stop is not None:
        if stop.owner_ref != "Cognitive State Formation Governance":
            errors.append("stop_owner_invalid")
        if stop.sufficiency_ref != sufficiency.sufficiency_ref:
            errors.append("stop_sufficiency_link_invalid")
        if stop.reason not in STOP_REASONS:
            errors.append("stop_reason_invalid")
        if not stop.candidate_only:
            errors.append("stop_not_candidate_only")
    return tuple(errors)
