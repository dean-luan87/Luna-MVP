"""Controlled Self/Field/Target/Relation inputs for condition derivation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.midplatform.core.situated_capability_preconditions.situated_state_perception_types_v1 import (
    SituatedStatePerceptionRequestV1,
)
from capabilities.midplatform.field_perception_orchestrator.integration.active_observation_precondition_types_v1 import (
    RelativeObservationStateV1,
    SelfPerceptualViewpointStateV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.minimum_situated_condition_resolution_v1 import (
    PRIMARY_SIGN_TEXT_INFORMATION_NEED,
)


CAPABILITY_REQUIREMENT_REF = "capability-requirement:text-recognition:v1"
CAPABILITY_REF = "text_recognition"
OBSERVATION_REQUIREMENT_REF = "observation-requirement:station-sign:v1"
FIELD_REF = "field:station-signage:v1"
TARGET_REF = "target:visible-transit-sign:v1"
PRIMARY_GOAL_REF = "goal:read-primary-transit-sign:v1"


@dataclass(frozen=True)
class SituatedStateCaseBindingV1:
    """Raw candidate inputs; no condition status is fixture-declared."""

    request: SituatedStatePerceptionRequestV1
    goal_ref: str
    information_need_ref: str
    capability_available_candidate: bool
    continuation_possible_candidate: bool
    capability_need_active_candidate: bool


def _self_state(case_id: str, state_id: str, *, stability: str = "STABLE") -> SelfPerceptualViewpointStateV1:
    return SelfPerceptualViewpointStateV1(
        state_ref=f"self-state:{case_id}:{state_id}",
        self_ref="self:luna:v1",
        temporal_ref=f"temporal:controlled:{case_id}:{state_id}",
        orientation_candidate="FRONTAL",
        motion_state_candidate="STATIONARY",
        stability_candidate=stability,
        current_view_ref=f"view:station-sign:{case_id}:{state_id}",
        visible_region_refs=(TARGET_REF,),
        sensor_availability_candidate="AVAILABLE",
        sensor_availability_refs=("sensor:vision:v1",),
        source_refs=(f"controlled:self-observation:{case_id}:{state_id}",),
        provenance_refs=(f"provenance:self-observation:{case_id}:{state_id}",),
    )


def _relative(
    case_id: str,
    state_id: str,
    *,
    visibility: str = "VISIBLE",
    completeness: str = "COMPLETE",
    scale: str = "ADEQUATE",
    orientation: str = "FRONTAL",
    motion: str = "LOW",
    stability: str = "STABLE",
    occlusion: str = "CLEAR",
) -> RelativeObservationStateV1:
    return RelativeObservationStateV1(
        relative_state_ref=f"relative-state:{case_id}:{state_id}",
        self_state_ref=f"self-state:{case_id}:{state_id}",
        target_ref=TARGET_REF,
        field_ref=FIELD_REF,
        observation_requirement_ref=OBSERVATION_REQUIREMENT_REF,
        temporal_ref=f"temporal:controlled:{case_id}:{state_id}",
        target_visibility_candidate=visibility,
        target_completeness_candidate=completeness,
        target_scale_candidate=scale,
        relative_orientation_candidate=orientation,
        relative_motion_candidate=motion,
        stability_candidate=stability,
        occlusion_candidate=occlusion,
        source_refs=(f"controlled:relative-observation:{case_id}:{state_id}",),
        provenance_refs=(f"provenance:relative-observation:{case_id}:{state_id}",),
    )


def _binding(
    case_id: str,
    state_id: str,
    cycle_index: int,
    *,
    self_stability: str = "STABLE",
    visibility: str = "VISIBLE",
    completeness: str = "COMPLETE",
    scale: str = "ADEQUATE",
    orientation: str = "FRONTAL",
    motion: str = "LOW",
    relation_stability: str = "STABLE",
    occlusion: str = "CLEAR",
    capability_available: bool = True,
    continuation: bool = False,
    active: bool = True,
) -> SituatedStateCaseBindingV1:
    self_state = _self_state(case_id, state_id, stability=self_stability)
    relative_state = _relative(
        case_id,
        state_id,
        visibility=visibility,
        completeness=completeness,
        scale=scale,
        orientation=orientation,
        motion=motion,
        stability=relation_stability,
        occlusion=occlusion,
    )
    temporal_ref = relative_state.temporal_ref
    request = SituatedStatePerceptionRequestV1(
        case_id=case_id,
        state_id=state_id,
        cycle_index=cycle_index,
        temporal_ref=temporal_ref,
        capability_requirement_ref=CAPABILITY_REQUIREMENT_REF,
        situated_state_ref=f"situated-capability-state:{case_id}:{state_id}",
        self_state=self_state,
        relative_state=relative_state,
        field_state_refs=(FIELD_REF,),
        target_refs=(TARGET_REF,),
        evidence_refs=(f"observation-candidate:{case_id}:{state_id}",),
        source_refs=(f"controlled:situated-input:{case_id}:{state_id}",),
        provenance_refs=(f"provenance:situated-input:{case_id}:{state_id}",),
    )
    return SituatedStateCaseBindingV1(
        request=request,
        goal_ref=PRIMARY_GOAL_REF,
        information_need_ref=PRIMARY_SIGN_TEXT_INFORMATION_NEED,
        capability_available_candidate=capability_available,
        continuation_possible_candidate=continuation,
        capability_need_active_candidate=active,
    )


def build_cases_v1() -> Tuple[SituatedStateCaseBindingV1, ...]:
    return (
        _binding("TARGET_NOT_VISIBLE", "t0", 0, visibility="NOT_VISIBLE"),
        _binding("TARGET_BECOMES_VISIBLE", "t0", 0, visibility="NOT_VISIBLE"),
        _binding("TARGET_BECOMES_VISIBLE", "t1", 1),
        _binding("TARGET_PARTIALLY_VISIBLE", "t0", 0, visibility="PARTIAL", completeness="PARTIAL"),
        _binding("TARGET_SCALE_INADEQUATE", "t0", 0, scale="SMALL"),
        _binding("RELATION_UNSTABLE", "t0", 0, motion="HIGH", relation_stability="UNSTABLE"),
        _binding("RELATION_BECOMES_STABLE", "t0", 0, motion="HIGH", relation_stability="UNSTABLE"),
        _binding("RELATION_BECOMES_STABLE", "t1", 1),
        _binding(
            "UNKNOWN_STATE_DOES_NOT_PASS",
            "t0",
            0,
            visibility="UNKNOWN",
            completeness="UNKNOWN",
            scale="UNKNOWN",
            orientation="UNKNOWN",
            motion="UNKNOWN",
            relation_stability="UNKNOWN",
            occlusion="UNKNOWN",
            self_stability="UNKNOWN",
        ),
        _binding("SAME_INFORMATION_NEED_DIFFERENT_SITUATED_STATE", "good", 0),
        _binding("SAME_INFORMATION_NEED_DIFFERENT_SITUATED_STATE", "poor", 1, scale="SMALL"),
        _binding(
            "OBSERVATION_NOT_NECESSARY_FROM_SITUATED_INPUT",
            "t0",
            0,
            continuation=True,
        ),
    )


__all__ = [
    "CAPABILITY_REF",
    "CAPABILITY_REQUIREMENT_REF",
    "FIELD_REF",
    "SituatedStateCaseBindingV1",
    "build_cases_v1",
]
