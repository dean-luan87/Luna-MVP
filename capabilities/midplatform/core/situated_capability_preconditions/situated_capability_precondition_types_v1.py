"""Generic situated capability precondition candidate contracts v1."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


OWNER = "Capability Admission / Capability Governance"
NECESSITY_STATUSES = ("REQUIRED", "NOT_REQUIRED", "DEFERRED")
FEASIBILITY_STATUSES = ("NOT_FEASIBLE", "FEASIBLE_UNSTABLE", "FEASIBLE")
OPPORTUNITY_STATUSES = ("OPEN", "CLOSED", "UNSTABLE")


@dataclass(frozen=True)
class CapabilityNeedCandidateV1:
    capability_need_ref: str
    capability_requirement_ref: str
    goal_ref: str
    intent_ref: str
    concern_ref: str
    information_need_ref: str
    current_cognitive_state_ref: str
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    capability_need_active_candidate: bool | None
    continuation_possible_candidate: bool | None
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityPreconditionDefinitionV1:
    capability_requirement_ref: str
    capability_ref: str
    supported_condition_refs: Tuple[str, ...]
    optional_condition_refs: Tuple[str, ...]
    adjustment_by_condition_ref: Dict[str, str]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class MinimumSituatedConditionRequirementV1:
    requirement_ref: str
    capability_requirement_ref: str
    information_need_ref: str
    goal_ref: str
    required_condition_refs: Tuple[str, ...]
    optional_condition_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SituatedConditionStateCandidateV1:
    """Candidate condition assessment derived from situated observations."""

    condition_ref: str
    status: str
    self_state_refs: Tuple[str, ...]
    field_state_refs: Tuple[str, ...]
    target_refs: Tuple[str, ...]
    relation_refs: Tuple[str, ...]
    evidence_refs: Tuple[str, ...]
    temporal_ref: str
    reason: str
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SituatedCapabilityStateV1:
    situated_state_ref: str
    capability_requirement_ref: str
    self_state_refs: Tuple[str, ...]
    field_state_refs: Tuple[str, ...]
    target_refs: Tuple[str, ...]
    relation_refs: Tuple[str, ...]
    temporal_ref: str
    satisfied_condition_refs: Tuple[str, ...]
    condition_state_refs: Tuple[str, ...]
    relation_stability_candidate: str
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True
    condition_state_candidates: Tuple[SituatedConditionStateCandidateV1, ...] = tuple()


@dataclass(frozen=True)
class CapabilityNecessityCandidateV1:
    necessity_ref: str
    capability_need_ref: str
    capability_requirement_ref: str
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    missing_information_refs: Tuple[str, ...]
    continuation_possible_candidate: bool | None
    capability_need_active_candidate: bool | None
    status: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityFeasibilityCandidateV1:
    feasibility_ref: str
    capability_requirement_ref: str
    capability_need_ref: str
    precondition_definition_ref: str
    minimum_condition_requirement_ref: str
    situated_state_ref: str
    satisfied_condition_refs: Tuple[str, ...]
    unsatisfied_condition_refs: Tuple[str, ...]
    unknown_condition_refs: Tuple[str, ...]
    status: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityConditionGapV1:
    condition_gap_ref: str
    capability_requirement_ref: str
    capability_need_ref: str
    missing_condition_ref: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityConditionAdjustmentNeedV1:
    adjustment_need_ref: str
    capability_requirement_ref: str
    condition_gap_ref: str
    adjustment_kind: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class CapabilityOpportunityCandidateV1:
    opportunity_ref: str
    capability_requirement_ref: str
    capability_need_ref: str
    feasibility_ref: str
    status: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SituatedCapabilityEligibilityCandidateV1:
    eligibility_ref: str
    capability_requirement_ref: str
    capability_ref: str
    capability_need_ref: str
    necessity_ref: str
    feasibility_ref: str
    opportunity_ref: str
    capability_available_candidate: bool
    eligible_now: bool
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SituatedCapabilityPreconditionRequestV1:
    case_id: str
    state_id: str
    cycle_index: int
    temporal_ref: str
    capability_need: CapabilityNeedCandidateV1
    precondition_definition: CapabilityPreconditionDefinitionV1
    minimum_condition_requirement: MinimumSituatedConditionRequirementV1
    situated_state: SituatedCapabilityStateV1
    capability_available_candidate: bool
    previous_opportunity_status: str | None
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SituatedCapabilityPreconditionResultV1:
    case_id: str
    state_id: str
    cycle_index: int
    request: SituatedCapabilityPreconditionRequestV1
    minimum_condition_requirement: MinimumSituatedConditionRequirementV1
    necessity: CapabilityNecessityCandidateV1
    feasibility: CapabilityFeasibilityCandidateV1
    condition_gaps: Tuple[CapabilityConditionGapV1, ...]
    adjustment_needs: Tuple[CapabilityConditionAdjustmentNeedV1, ...]
    opportunity: CapabilityOpportunityCandidateV1
    eligibility: SituatedCapabilityEligibilityCandidateV1
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    behavior: Dict[str, bool] = field(default_factory=dict)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
