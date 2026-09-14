"""Active observation precondition candidate contracts v1.

These contracts extend the Field Perception Orchestrator observation-demand
substrate.  They describe eligibility for an observation; they do not invoke a
provider, mutate Self or Field state, or issue an action.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


OWNER = "Field Perception Orchestrator / Active Observation Preconditions"
SELF_STATE_OWNER = "Self State Awareness"

NECESSITY_STATUSES = ("REQUIRED", "NOT_REQUIRED", "DEFERRED")
FEASIBILITY_STATUSES = (
    "NOT_OBSERVABLE",
    "APPROACHING_OBSERVABLE",
    "OBSERVABLE_UNSTABLE",
    "OBSERVABLE",
    "LOSING_OBSERVABILITY",
)
WINDOW_STATUSES = ("OPEN", "CLOSED", "UNSTABLE")
CONDITION_GAP_KINDS = (
    "TARGET_NOT_VISIBLE",
    "TARGET_INCOMPLETE",
    "TARGET_TOO_SMALL",
    "VIEW_ORIENTATION_UNSUITABLE",
    "MOTION_UNSTABLE",
    "OCCLUDED",
    "SENSOR_UNAVAILABLE",
)
ADJUSTMENT_KINDS = (
    "NEED_TARGET_VISIBLE",
    "NEED_TARGET_MORE_COMPLETE",
    "NEED_LARGER_TARGET_SCALE",
    "NEED_MORE_FRONTAL_VIEW",
    "NEED_LOWER_RELATIVE_MOTION",
    "NEED_STABLE_VIEW",
    "NEED_CLEAR_LINE_OF_SIGHT",
    "NEED_SENSOR_AVAILABLE",
)


@dataclass(frozen=True)
class SelfPerceptualViewpointStateV1:
    """A time-bounded Self State projection used by observation regulation."""

    state_ref: str
    self_ref: str
    temporal_ref: str
    orientation_candidate: str
    motion_state_candidate: str
    stability_candidate: str
    current_view_ref: str
    visible_region_refs: Tuple[str, ...]
    sensor_availability_candidate: str
    sensor_availability_refs: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    owner: str = SELF_STATE_OWNER
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationRequirementV1:
    observation_requirement_ref: str
    observation_demand_ref: str
    observation_request_ref: str
    capability_requirement_ref: str
    capability_ref: str
    target_ref: str
    field_ref: str
    required_information_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class MinimumObservationConditionsV1:
    observation_requirement_ref: str
    target_visibility_requirement: str
    target_completeness_requirement: str
    relative_scale_requirement: str
    view_orientation_requirement: str
    stability_requirement: str
    occlusion_requirement: str
    sensor_requirement: str
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class RelativeObservationStateV1:
    relative_state_ref: str
    self_state_ref: str
    target_ref: str
    field_ref: str
    observation_requirement_ref: str
    temporal_ref: str
    target_visibility_candidate: str
    target_completeness_candidate: str
    target_scale_candidate: str
    relative_orientation_candidate: str
    relative_motion_candidate: str
    stability_candidate: str
    occlusion_candidate: str
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationNecessityCandidateV1:
    necessity_ref: str
    observation_requirement_ref: str
    information_need_ref: str
    current_cognitive_state_ref: str
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    information_gap_refs: Tuple[str, ...]
    continuation_possible_candidate: bool | None
    status: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationFeasibilityCandidateV1:
    feasibility_ref: str
    observation_requirement_ref: str
    necessity_ref: str
    minimum_conditions_ref: str
    self_state_ref: str
    relative_state_ref: str
    field_ref: str
    target_ref: str
    status: str
    satisfied_condition_refs: Tuple[str, ...]
    unsatisfied_condition_refs: Tuple[str, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationWindowCandidateV1:
    window_ref: str
    observation_requirement_ref: str
    necessity_ref: str
    feasibility_ref: str
    status: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationCapabilityEligibilityCandidateV1:
    eligibility_ref: str
    observation_requirement_ref: str
    capability_ref: str
    necessity_ref: str
    window_ref: str
    eligible_now: bool
    capability_available_candidate: bool
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationConditionGapV1:
    gap_ref: str
    observation_requirement_ref: str
    information_need_ref: str
    kind: str
    unsatisfied_condition_ref: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class RelativeObservationAdjustmentNeedV1:
    adjustment_ref: str
    observation_requirement_ref: str
    condition_gap_ref: str
    kind: str
    reason: str
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ObservationPreconditionRequestV1:
    case_id: str
    state_id: str
    cycle_index: int
    temporal_ref: str
    goal_ref: str
    concern_ref: str
    information_need_ref: str
    current_cognitive_state_ref: str
    information_gap_refs: Tuple[str, ...]
    required_information_refs: Tuple[str, ...]
    available_information_refs: Tuple[str, ...]
    continuation_possible_candidate: bool | None
    observation_requirement: ObservationRequirementV1
    minimum_conditions: MinimumObservationConditionsV1
    self_state: SelfPerceptualViewpointStateV1
    relative_state: RelativeObservationStateV1
    observation_demand_ref: str
    observation_request_ref: str
    available_capabilities: Tuple[str, ...]
    previous_window_state: str | None
    source_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ActiveObservationPreconditionResultV1:
    case_id: str
    state_id: str
    cycle_index: int
    request: ObservationPreconditionRequestV1
    necessity: ObservationNecessityCandidateV1
    feasibility: ObservationFeasibilityCandidateV1
    window: ObservationWindowCandidateV1
    capability_eligibility: ObservationCapabilityEligibilityCandidateV1
    condition_gaps: Tuple[ObservationConditionGapV1, ...]
    adjustment_needs: Tuple[RelativeObservationAdjustmentNeedV1, ...]
    trace_refs: Tuple[str, ...]
    provenance_refs: Tuple[str, ...]
    behavior: Dict[str, bool] = field(default_factory=dict)
    validation_errors: Tuple[str, ...] = field(default_factory=tuple)
    candidate_only: bool = True
