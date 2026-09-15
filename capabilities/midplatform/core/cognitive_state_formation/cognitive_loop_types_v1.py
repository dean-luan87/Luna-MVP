"""Canonical candidate-only contracts for the minimum sufficient cognition loop."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, fields
from enum import Enum
from typing import Mapping, Tuple



LOOP_OWNERS = ("Cognitive State Formation Governance", "Field Perception Orchestrator")
class RequirementEstablishmentStatusV1(str, Enum):
    NOT_ESTABLISHED = "NOT_ESTABLISHED"
    ESTABLISHED = "ESTABLISHED"
    UNAVAILABLE = "UNAVAILABLE"
    INVALID = "INVALID"
    WITHHELD = "WITHHELD"


SUFFICIENCY_STATUSES = ("SUFFICIENT", "INSUFFICIENT", "UNKNOWN", "WITHHELD")


def requirement_establishment_from_condition_formation_status_v1(
    formation_status: str,
) -> tuple[str, str]:
    """Map canonical Required Cognitive Condition formation to admission state.

    The mapping is deliberately explicit: an absent or unknown formation
    result cannot establish requirements by implication.
    """

    return {
        "CONDITIONS_FORMED": (RequirementEstablishmentStatusV1.ESTABLISHED.value, "ACTIVE_REQUIRED_CONDITIONS"),
        "NO_ACTIVE_REQUIRED_CONDITIONS": (
            RequirementEstablishmentStatusV1.ESTABLISHED.value,
            "NO_ACTIVE_REQUIRED_CONDITIONS",
        ),
        "REJECTED": (RequirementEstablishmentStatusV1.INVALID.value, "REJECTED"),
    }.get(formation_status, (RequirementEstablishmentStatusV1.WITHHELD.value, "FORMATION_STATUS_UNAVAILABLE"))


def validated_requirement_establishment_from_condition_formation_v1(
    formation: ARouteRequiredCognitiveConditionFormationResultV1 | Mapping[str, object] | None,
) -> tuple[str, str | None, str | None] | None:
    """Project only a structurally valid canonical formation result.

    The string fields carried by ingress/admission remain compatibility
    declarations.  This projection is the authority boundary used by the
    cognitive loop: it accepts the existing A-Route formation result type,
    checks its candidate-only contract and internal identity relationships,
    and derives the establishment reference from the formation trace.
    """

    from capabilities.midplatform.core.a_route_orchestration.a_route_required_cognitive_condition_formation_types_v1 import (
        ACTIVE_REQUIRED,
        CONDITIONS_FORMED,
        FORMATION_OWNER,
        FORMATION_SCHEMA_VERSION,
        NO_ACTIVE_REQUIRED_CONDITIONS,
        ARouteRequiredCognitiveConditionFormationResultV1,
        RequiredCognitiveConditionCandidateV1,
    )

    if isinstance(formation, Mapping):
        candidate_type = RequiredCognitiveConditionCandidateV1
        candidate_rows = formation.get("candidates")
        if not isinstance(candidate_rows, (tuple, list)):
            return None
        try:
            candidate_values = []
            candidate_tuple_fields = {
                field.name
                for field in fields(candidate_type)
                if field.name.endswith("_refs")
            }
            for row in candidate_rows:
                if not isinstance(row, Mapping):
                    return None
                candidate_row = dict(row)
                for field_name in candidate_tuple_fields:
                    if field_name in candidate_row:
                        candidate_row[field_name] = tuple(candidate_row[field_name])
                candidate_values.append(candidate_type(**candidate_row))
            result_values = dict(formation)
            result_tuple_fields = {
                field.name
                for field in fields(ARouteRequiredCognitiveConditionFormationResultV1)
                if field.name.endswith("_refs")
            }
            for field_name in result_tuple_fields:
                if field_name in result_values:
                    result_values[field_name] = tuple(result_values[field_name])
            result_values["candidates"] = tuple(candidate_values)
            formation = ARouteRequiredCognitiveConditionFormationResultV1(**result_values)
        except (TypeError, ValueError, KeyError):
            return None
    if not isinstance(formation, ARouteRequiredCognitiveConditionFormationResultV1):
        return None
    if (
        formation.schema_version != FORMATION_SCHEMA_VERSION
        or formation.owner_ref != FORMATION_OWNER
        or not formation.candidate_only
        or not formation.read_only
        or formation.truth_declared
        or formation.world_truth_declared
        or not formation.trace_ref
        or not formation.provenance_refs
    ):
        return None
    if any(
        getattr(formation, field_name, False)
        for field_name in (
            "goal_mutation",
            "intent_mutation",
            "concern_mutation",
            "role_mutation",
            "context_mutation",
            "field_mutation",
            "self_mutation",
            "current_world_mutation",
            "memory_mutation",
            "pcn_mutation",
            "provider_invocation",
            "model_invocation",
            "observation_execution",
            "decision_execution",
            "task_execution",
            "action_execution",
        )
    ):
        return None
    candidate_ids = tuple(candidate.condition_ref for candidate in formation.candidates)
    if len(candidate_ids) != len(set(candidate_ids)):
        return None
    if len(formation.active_required_condition_refs) != len(set(formation.active_required_condition_refs)):
        return None
    if len(formation.satisfied_condition_refs) != len(set(formation.satisfied_condition_refs)):
        return None
    if len(formation.dormant_condition_refs) != len(set(formation.dormant_condition_refs)):
        return None
    active_candidates = {
        candidate.condition_ref
        for candidate in formation.candidates
        if candidate.status == ACTIVE_REQUIRED
    }
    if set(formation.active_required_condition_refs) != active_candidates:
        return None
    if formation.status == CONDITIONS_FORMED and not formation.active_required_condition_refs:
        return None
    if formation.status == NO_ACTIVE_REQUIRED_CONDITIONS and formation.active_required_condition_refs:
        return None
    if formation.status == CONDITIONS_FORMED:
        basis = "ACTIVE_REQUIRED_CONDITIONS"
    elif formation.status == NO_ACTIVE_REQUIRED_CONDITIONS:
        basis = NO_ACTIVE_REQUIRED_CONDITIONS
    else:
        return None
    expected_digest = hashlib.sha256(
        "|".join(
            (
                formation.goal_ref,
                formation.intent_ref or "",
                formation.concern_ref or "",
                *formation.active_required_condition_refs,
            )
        ).encode("utf-8")
    ).hexdigest()[:24]
    if formation.trace_ref.rsplit(":", 1)[-1] != expected_digest:
        return None
    return (RequirementEstablishmentStatusV1.ESTABLISHED.value, formation.trace_ref, basis)


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
    requirement_establishment_status: str = RequirementEstablishmentStatusV1.NOT_ESTABLISHED.value
    requirement_establishment_ref: str | None = None
    requirement_establishment_basis: str | None = None


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
        if sufficiency.requirement_establishment_status != RequirementEstablishmentStatusV1.ESTABLISHED.value:
            errors.append("sufficient_state_requirement_establishment_missing")
        if not sufficiency.requirement_establishment_ref:
            errors.append("sufficient_state_requirement_establishment_ref_missing")
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
    if sufficiency.status in {"UNKNOWN", "WITHHELD"}:
        if sufficiency.stop_required or stop is not None:
            errors.append("unresolved_state_has_stop")
        if information_gap is not None or reobservation is not None:
            errors.append("unresolved_state_has_gap_or_reobservation")
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
