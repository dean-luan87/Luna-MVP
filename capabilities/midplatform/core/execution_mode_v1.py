"""Canonical execution-mode and controlled-replay admission contracts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from capabilities.midplatform.core.cognitive_state_formation.cognitive_loop_types_v1 import (
        CognitiveInformationGapCandidateV1,
        CognitiveReobservationCandidateV1,
        CognitiveSufficiencyCandidateV1,
    )


SYNTHETIC_CONTROLLED = "SYNTHETIC_CONTROLLED"
CONTROLLED_REPLAY_RUNTIME = "CONTROLLED_REPLAY_RUNTIME"
LIVE_RUNTIME = "LIVE_RUNTIME"
EXECUTION_MODES = (SYNTHETIC_CONTROLLED, CONTROLLED_REPLAY_RUNTIME, LIVE_RUNTIME)

REPLAY_ORIGINS = ("CONTROLLED_RECORDED_FIXTURE", "REAL_RECORDED_EVIDENCE")
REPLAY_ADMISSION_STATES = ("ADMITTED_OBSERVATION",)


@dataclass(frozen=True)
class ControlledReplayInputV1:
    """Frozen, reference-only input admitted for a controlled replay."""

    replay_input_ref: str
    replay_version: str
    origin_class: str
    source_ref: str
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    ordering_refs: Tuple[str, ...]
    admission_state: str = "ADMITTED_OBSERVATION"
    non_live: bool = True
    model_invocation: bool = False
    provider_invocation: bool = False
    live_observation_execution: bool = False
    world_truth_declared: bool = False
    candidate_only: bool = True
    cycle_index: int = 1
    required_information_refs: Tuple[str, ...] = ()
    available_information_refs: Tuple[str, ...] = ()
    prior_current_world_ref: str | None = None
    prior_hypothesis_refs: Tuple[str, ...] = ()
    prior_information_gap_ref: str | None = None
    prior_reobservation_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    prior_sufficiency_candidate: CognitiveSufficiencyCandidateV1 | None = None
    prior_information_gap_candidate: CognitiveInformationGapCandidateV1 | None = None
    prior_reobservation_candidate: CognitiveReobservationCandidateV1 | None = None


@dataclass(frozen=True)
class ControlledReplayAdmissionV1:
    """Observation Gateway-owned admission proof consumed by A-Route."""

    replay_input_ref: str
    replay_version: str
    origin_class: str
    source_ref: str
    evidence_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    ordering_refs: Tuple[str, ...]
    gateway_admission_ref: str
    admission_state: str = "ADMITTED_OBSERVATION"
    owner_ref: str = "Observation Gateway Governance"
    candidate_only: bool = True
    world_truth_declared: bool = False
    model_invocation: bool = False
    provider_invocation: bool = False
    live_observation_execution: bool = False
    cycle_index: int = 1
    required_information_refs: Tuple[str, ...] = ()
    available_information_refs: Tuple[str, ...] = ()
    prior_current_world_ref: str | None = None
    prior_hypothesis_refs: Tuple[str, ...] = ()
    prior_information_gap_ref: str | None = None
    prior_reobservation_ref: str | None = None
    prior_next_cycle_ingress_ref: str | None = None
    prior_sufficiency_candidate: CognitiveSufficiencyCandidateV1 | None = None
    prior_information_gap_candidate: CognitiveInformationGapCandidateV1 | None = None
    prior_reobservation_candidate: CognitiveReobservationCandidateV1 | None = None


def validate_execution_mode(mode: str, *, synthetic_only: bool) -> Tuple[str, ...]:
    errors = []
    if mode not in EXECUTION_MODES:
        errors.append(f"invalid_execution_mode:{mode}")
    elif mode == SYNTHETIC_CONTROLLED and not synthetic_only:
        errors.append("synthetic_mode_requires_synthetic_only")
    elif mode == CONTROLLED_REPLAY_RUNTIME and synthetic_only:
        errors.append("replay_mode_requires_synthetic_only_false")
    return tuple(errors)


def validate_controlled_replay_input(
    replay: ControlledReplayInputV1 | None,
) -> Tuple[str, ...]:
    if replay is None:
        return ("replay_input_missing",)
    errors = []
    required = (
        replay.replay_input_ref,
        replay.replay_version,
        replay.origin_class,
        replay.source_ref,
        replay.evidence_refs,
        replay.provenance_refs,
        replay.ordering_refs,
    )
    if any(not value for value in required):
        errors.append("replay_identity_provenance_or_ordering_missing")
    if replay.origin_class not in REPLAY_ORIGINS:
        errors.append(f"invalid_replay_origin:{replay.origin_class}")
    if replay.admission_state not in REPLAY_ADMISSION_STATES:
        errors.append(f"invalid_replay_admission_state:{replay.admission_state}")
    if len(replay.evidence_refs) != len(replay.ordering_refs):
        errors.append("replay_evidence_ordering_length_mismatch")
    if not replay.non_live:
        errors.append("replay_must_be_non_live")
    if replay.model_invocation or replay.provider_invocation or replay.live_observation_execution:
        errors.append("replay_forbidden_runtime_capability_claimed")
    if replay.world_truth_declared or not replay.candidate_only:
        errors.append("replay_authority_boundary_invalid")
    if replay.cycle_index < 1:
        errors.append("replay_cycle_index_invalid")
    if replay.cycle_index > 1 and not replay.prior_information_gap_ref:
        errors.append("replay_followup_gap_link_missing")
    if replay.cycle_index > 1 and not replay.prior_reobservation_ref:
        errors.append("replay_followup_reobservation_link_missing")
    if replay.cycle_index > 1 and not replay.prior_next_cycle_ingress_ref:
        errors.append("replay_followup_next_cycle_ingress_link_missing")
    if replay.cycle_index > 1 and replay.prior_sufficiency_candidate is None:
        errors.append("replay_followup_sufficiency_candidate_missing")
    if replay.cycle_index > 1 and replay.prior_information_gap_candidate is None:
        errors.append("replay_followup_information_gap_candidate_missing")
    if replay.cycle_index > 1 and replay.prior_reobservation_candidate is None:
        errors.append("replay_followup_reobservation_candidate_missing")
    if replay.prior_information_gap_candidate is not None and replay.prior_information_gap_candidate.information_gap_ref != replay.prior_information_gap_ref:
        errors.append("replay_followup_information_gap_candidate_ref_mismatch")
    if replay.prior_reobservation_candidate is not None and replay.prior_reobservation_candidate.reobservation_ref != replay.prior_reobservation_ref:
        errors.append("replay_followup_reobservation_candidate_ref_mismatch")
    if replay.prior_reobservation_candidate is not None and replay.prior_reobservation_candidate.next_cycle_ingress_ref != replay.prior_next_cycle_ingress_ref:
        errors.append("replay_followup_next_cycle_ingress_candidate_ref_mismatch")
    if replay.prior_sufficiency_candidate is not None and replay.prior_information_gap_candidate is not None and replay.prior_information_gap_candidate.sufficiency_ref != replay.prior_sufficiency_candidate.sufficiency_ref:
        errors.append("replay_followup_gap_sufficiency_ref_mismatch")
    if replay.prior_information_gap_candidate is not None and replay.prior_reobservation_candidate is not None and replay.prior_reobservation_candidate.information_gap_ref != replay.prior_information_gap_candidate.information_gap_ref:
        errors.append("replay_followup_reobservation_gap_ref_mismatch")
    return tuple(errors)


def validate_controlled_replay_admission(
    admission: ControlledReplayAdmissionV1 | None,
) -> Tuple[str, ...]:
    if admission is None:
        return ("replay_admission_missing",)
    replay = ControlledReplayInputV1(
        replay_input_ref=admission.replay_input_ref,
        replay_version=admission.replay_version,
        origin_class=admission.origin_class,
        source_ref=admission.source_ref,
        evidence_refs=admission.evidence_refs,
        provenance_refs=admission.provenance_refs,
        ordering_refs=admission.ordering_refs,
        admission_state=admission.admission_state,
        model_invocation=admission.model_invocation,
        provider_invocation=admission.provider_invocation,
        live_observation_execution=admission.live_observation_execution,
        world_truth_declared=admission.world_truth_declared,
        candidate_only=admission.candidate_only,
        cycle_index=admission.cycle_index,
        required_information_refs=admission.required_information_refs,
        available_information_refs=admission.available_information_refs,
        prior_current_world_ref=admission.prior_current_world_ref,
        prior_hypothesis_refs=admission.prior_hypothesis_refs,
        prior_information_gap_ref=admission.prior_information_gap_ref,
        prior_reobservation_ref=admission.prior_reobservation_ref,
        prior_next_cycle_ingress_ref=admission.prior_next_cycle_ingress_ref,
        prior_sufficiency_candidate=admission.prior_sufficiency_candidate,
        prior_information_gap_candidate=admission.prior_information_gap_candidate,
        prior_reobservation_candidate=admission.prior_reobservation_candidate,
    )
    errors = list(validate_controlled_replay_input(replay))
    if admission.owner_ref != "Observation Gateway Governance":
        errors.append("replay_admission_owner_invalid")
    if not admission.gateway_admission_ref:
        errors.append("gateway_admission_ref_missing")
    return tuple(dict.fromkeys(errors))
