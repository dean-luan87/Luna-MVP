"""Controlled dynamic viewpoint cases for the active observation foundation."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.field_perception_orchestrator.integration.active_observation_precondition_types_v1 import (
    MinimumObservationConditionsV1,
    ObservationPreconditionRequestV1,
    ObservationRequirementV1,
    RelativeObservationStateV1,
    SelfPerceptualViewpointStateV1,
)


CAPABILITY_REF = "text_recognition"
FIELD_REF = "field:station-signage:v1"
TARGET_REF = "target:visible-transit-sign:v1"
GOAL_REF = "goal:current-scene-understanding:v1"
CONCERN_REF = "concern:transit-sign-text:v1"
INFO_REF = "information:visible-transit-sign-text:v1"
GAP_REF = "information-gap:visible-transit-sign-text:v1"


def _self(case_id: str, state_id: str, temporal_ref: str) -> SelfPerceptualViewpointStateV1:
    return SelfPerceptualViewpointStateV1(
        state_ref=f"self-perceptual-viewpoint:{case_id}:{state_id}",
        self_ref="self:luna:v1",
        temporal_ref=temporal_ref,
        orientation_candidate="FORWARD",
        motion_state_candidate="STATIONARY_CANDIDATE",
        stability_candidate="STABLE",
        current_view_ref=f"view:station-signage:{state_id}",
        visible_region_refs=(TARGET_REF,),
        sensor_availability_candidate="AVAILABLE",
        sensor_availability_refs=("sensor:visual-input:v1",),
        source_refs=("controlled:self-state-fixture:v1",),
        provenance_refs=(f"source:self-state:{case_id}:{state_id}",),
    )


def _conditions() -> MinimumObservationConditionsV1:
    return MinimumObservationConditionsV1(
        observation_requirement_ref="observation-requirement:visible-transit-sign-text:v1",
        target_visibility_requirement="VISIBLE",
        target_completeness_requirement="COMPLETE",
        relative_scale_requirement="ADEQUATE",
        view_orientation_requirement="SUITABLE",
        stability_requirement="STABLE",
        occlusion_requirement="CLEAR",
        sensor_requirement="AVAILABLE",
        source_refs=("controlled:observation-condition-fixture:v1",),
        provenance_refs=("provenance:minimum-conditions:visible-transit-sign-text:v1",),
    )


def _requirement(case_id: str, requirement_ref: str | None = None) -> ObservationRequirementV1:
    suffix = requirement_ref or "observation-requirement:visible-transit-sign-text:v1"
    return ObservationRequirementV1(
        observation_requirement_ref=suffix,
        observation_demand_ref=f"observation-demand:{case_id}",
        observation_request_ref=f"observation-request:{case_id}",
        capability_requirement_ref=f"capability-requirement:{case_id}",
        capability_ref=CAPABILITY_REF,
        target_ref=TARGET_REF,
        field_ref=FIELD_REF,
        required_information_refs=(INFO_REF,),
        trace_refs=(f"trace:observation-requirement:{case_id}",),
        provenance_refs=(f"provenance:observation-requirement:{case_id}",),
    )


def _relative(
    case_id: str,
    state_id: str,
    temporal_ref: str,
    *,
    visibility: str,
    completeness: str,
    scale: str,
    orientation: str = "SUITABLE",
    motion: str = "LOW",
    stability: str = "STABLE",
    occlusion: str = "CLEAR",
) -> RelativeObservationStateV1:
    return RelativeObservationStateV1(
        relative_state_ref=f"relative-observation:{case_id}:{state_id}",
        self_state_ref=f"self-perceptual-viewpoint:{case_id}:{state_id}",
        target_ref=TARGET_REF,
        field_ref=FIELD_REF,
        observation_requirement_ref="observation-requirement:visible-transit-sign-text:v1",
        temporal_ref=temporal_ref,
        target_visibility_candidate=visibility,
        target_completeness_candidate=completeness,
        target_scale_candidate=scale,
        relative_orientation_candidate=orientation,
        relative_motion_candidate=motion,
        stability_candidate=stability,
        occlusion_candidate=occlusion,
        source_refs=(f"controlled:relative-state:{case_id}:{state_id}",),
        provenance_refs=(f"provenance:relative-state:{case_id}:{state_id}",),
    )


def _request(
    case_id: str,
    state_id: str,
    cycle_index: int,
    temporal_ref: str,
    *,
    continuation_possible: bool | None,
    relative: RelativeObservationStateV1,
    goal_ref: str = GOAL_REF,
    information_need_ref: str = INFO_REF,
    required_information_refs: Tuple[str, ...] = (INFO_REF,),
    available_information_refs: Tuple[str, ...] = tuple(),
    information_gap_refs: Tuple[str, ...] = (GAP_REF,),
    previous_window_state: str | None = None,
    requirement_ref: str | None = None,
) -> ObservationPreconditionRequestV1:
    requirement = _requirement(case_id, requirement_ref)
    conditions = _conditions()
    return ObservationPreconditionRequestV1(
        case_id=case_id,
        state_id=state_id,
        cycle_index=cycle_index,
        temporal_ref=temporal_ref,
        goal_ref=goal_ref,
        concern_ref=CONCERN_REF,
        information_need_ref=information_need_ref,
        current_cognitive_state_ref=f"cognitive-state:{case_id}:{state_id}",
        information_gap_refs=information_gap_refs,
        required_information_refs=required_information_refs,
        available_information_refs=available_information_refs,
        continuation_possible_candidate=continuation_possible,
        observation_requirement=requirement,
        minimum_conditions=conditions,
        self_state=_self(case_id, state_id, temporal_ref),
        relative_state=relative,
        observation_demand_ref=requirement.observation_demand_ref,
        observation_request_ref=requirement.observation_request_ref,
        available_capabilities=(CAPABILITY_REF,),
        previous_window_state=previous_window_state,
        source_refs=(f"controlled:active-observation-case:{case_id}",),
        provenance_refs=(f"provenance:active-observation-case:{case_id}:{state_id}",),
    )


def build_cases_v1() -> Tuple[ObservationPreconditionRequestV1, ...]:
    """Return four controlled states; no case label is read by the evaluator."""

    case_a = _request(
        "OBSERVATION_NOT_NECESSARY",
        "t0",
        0,
        "temporal:controlled:t0",
        continuation_possible=True,
        relative=_relative(
            "OBSERVATION_NOT_NECESSARY", "t0", "temporal:controlled:t0",
            visibility="VISIBLE", completeness="COMPLETE", scale="ADEQUATE",
        ),
    )
    case_b = _request(
        "NECESSARY_BUT_CONDITIONS_NOT_MET",
        "t0",
        0,
        "temporal:controlled:t0",
        continuation_possible=False,
        relative=_relative(
            "NECESSARY_BUT_CONDITIONS_NOT_MET", "t0", "temporal:controlled:t0",
            visibility="VISIBLE", completeness="COMPLETE", scale="SMALL",
        ),
    )
    case_c_t0 = _request(
        "DYNAMIC_STATE_REACHES_OBSERVABLE",
        "t0",
        0,
        "temporal:controlled:t0",
        continuation_possible=False,
        relative=_relative(
            "DYNAMIC_STATE_REACHES_OBSERVABLE", "t0", "temporal:controlled:t0",
            visibility="PARTIAL", completeness="PARTIAL", scale="SMALL",
        ),
    )
    case_c_t1 = _request(
        "DYNAMIC_STATE_REACHES_OBSERVABLE",
        "t1",
        1,
        "temporal:controlled:t1",
        continuation_possible=False,
        relative=_relative(
            "DYNAMIC_STATE_REACHES_OBSERVABLE", "t1", "temporal:controlled:t1",
            visibility="VISIBLE", completeness="COMPLETE", scale="ADEQUATE",
        ),
        previous_window_state="CLOSED",
    )
    case_d_t0 = _request(
        "OBSERVATION_WINDOW_LOST",
        "t0",
        0,
        "temporal:controlled:t0",
        continuation_possible=False,
        relative=_relative(
            "OBSERVATION_WINDOW_LOST", "t0", "temporal:controlled:t0",
            visibility="VISIBLE", completeness="COMPLETE", scale="ADEQUATE",
        ),
    )
    case_d_t1 = _request(
        "OBSERVATION_WINDOW_LOST",
        "t1",
        1,
        "temporal:controlled:t1",
        continuation_possible=False,
        relative=_relative(
            "OBSERVATION_WINDOW_LOST", "t1", "temporal:controlled:t1",
            visibility="VISIBLE", completeness="COMPLETE", scale="ADEQUATE",
            occlusion="OCCLUDED",
        ),
        previous_window_state="OPEN",
    )
    return (case_a, case_b, case_c_t0, case_c_t1, case_d_t0, case_d_t1)


__all__ = ["build_cases_v1"]

