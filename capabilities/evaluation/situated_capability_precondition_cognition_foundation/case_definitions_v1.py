"""Controlled cases for generic situated capability preconditions."""

from __future__ import annotations

from typing import Tuple

from capabilities.midplatform.core.situated_capability_preconditions.situated_capability_precondition_types_v1 import (
    CapabilityNeedCandidateV1,
    CapabilityPreconditionDefinitionV1,
    SituatedCapabilityPreconditionRequestV1,
    SituatedCapabilityStateV1,
)
from capabilities.midplatform.core.situated_capability_preconditions.minimum_situated_condition_resolution_v1 import (
    CONDITION_STABLE_RELATION,
    CONDITION_TARGET_COMPLETE,
    CONDITION_TARGET_SCALE_ADEQUATE,
    CONDITION_TARGET_VISIBLE,
    PRIMARY_SIGN_TEXT_INFORMATION_NEED,
    TEXT_PRESENCE_INFORMATION_NEED,
    resolve_minimum_situated_conditions,
)


CAPABILITY_REF = "text_recognition"
CAPABILITY_REQUIREMENT_REF = "capability-requirement:text-recognition:v1"
FIELD_REF = "field:station-signage:v1"
TARGET_REF = "target:visible-transit-sign:v1"

VISIBLE = CONDITION_TARGET_VISIBLE
COMPLETE = CONDITION_TARGET_COMPLETE
SCALE = CONDITION_TARGET_SCALE_ADEQUATE
STABLE = CONDITION_STABLE_RELATION
ALL_SUPPORTED_CONDITIONS = (VISIBLE, COMPLETE, SCALE, STABLE)
ADJUSTMENTS = {
    VISIBLE: "NEED_BETTER_VISIBILITY",
    COMPLETE: "NEED_TARGET_COMPLETENESS",
    SCALE: "NEED_TARGET_SCALE",
    STABLE: "NEED_STABLE_RELATION",
}


def _definition() -> CapabilityPreconditionDefinitionV1:
    return CapabilityPreconditionDefinitionV1(
        capability_requirement_ref=CAPABILITY_REQUIREMENT_REF,
        capability_ref=CAPABILITY_REF,
        supported_condition_refs=ALL_SUPPORTED_CONDITIONS,
        optional_condition_refs=tuple(),
        adjustment_by_condition_ref=ADJUSTMENTS,
        source_refs=(
            "capabilities/registry/luna_capability_registry_v1.json",
            "docs/architecture/phase_p1_luna_situated_capability_precondition_cognition_foundation_v1/capability_preconditions.md",
        ),
        provenance_refs=("provenance:capability-preconditions:text-recognition:v1",),
    )


def _need(
    case_id: str,
    *,
    information_need_ref: str,
    goal_ref: str,
    active: bool,
    continuation: bool,
    info_available: Tuple[str, ...] = tuple(),
) -> CapabilityNeedCandidateV1:
    return CapabilityNeedCandidateV1(
        capability_need_ref=f"capability-need:{case_id}:{information_need_ref}",
        capability_requirement_ref=CAPABILITY_REQUIREMENT_REF,
        goal_ref=goal_ref,
        intent_ref="intent:understand-transit-sign:v1",
        concern_ref="concern:transit-sign-text:v1",
        information_need_ref=information_need_ref,
        current_cognitive_state_ref=f"cognitive-state:{case_id}",
        required_information_refs=(information_need_ref,),
        available_information_refs=info_available,
        information_gap_refs=tuple() if info_available else (f"information-gap:{case_id}",),
        capability_need_active_candidate=active,
        continuation_possible_candidate=continuation,
        source_refs=(f"controlled:capability-need:{case_id}",),
        provenance_refs=(f"provenance:capability-need:{case_id}",),
    )


def _state(case_id: str, state_id: str, satisfied: Tuple[str, ...], stability: str = "STABLE") -> SituatedCapabilityStateV1:
    return SituatedCapabilityStateV1(
        situated_state_ref=f"situated-capability-state:{case_id}:{state_id}",
        capability_requirement_ref=CAPABILITY_REQUIREMENT_REF,
        self_state_refs=(f"self-state:{case_id}:{state_id}",),
        field_state_refs=(FIELD_REF,),
        target_refs=(TARGET_REF,),
        relation_refs=(f"relation:self-target:{case_id}:{state_id}",),
        temporal_ref=f"temporal:controlled:{state_id}",
        satisfied_condition_refs=satisfied,
        condition_state_refs=(f"condition-state:{case_id}:{state_id}",),
        relation_stability_candidate=stability,
        source_refs=(f"controlled:situated-state:{case_id}:{state_id}",),
        provenance_refs=(f"provenance:situated-state:{case_id}:{state_id}",),
    )


def _request(
    case_id: str,
    state_id: str,
    cycle_index: int,
    *,
    active: bool,
    continuation: bool,
    available: bool,
    information_need_ref: str,
    goal_ref: str,
    satisfied: Tuple[str, ...],
    stability: str = "STABLE",
    previous_opportunity_status: str | None = None,
    info_available: Tuple[str, ...] = tuple(),
) -> SituatedCapabilityPreconditionRequestV1:
    need = _need(
        case_id,
        information_need_ref=information_need_ref,
        goal_ref=goal_ref,
        active=active,
        continuation=continuation,
        info_available=info_available,
    )
    state = _state(case_id, state_id, satisfied, stability)
    definition = _definition()
    minimum = resolve_minimum_situated_conditions(
        capability_definition=definition,
        information_need_ref=information_need_ref,
        goal_ref=need.goal_ref,
        intent_ref=need.intent_ref,
        concern_ref=need.concern_ref,
    )
    return SituatedCapabilityPreconditionRequestV1(
        case_id=case_id,
        state_id=state_id,
        cycle_index=cycle_index,
        temporal_ref=state.temporal_ref,
        capability_need=need,
        precondition_definition=definition,
        minimum_condition_requirement=minimum,
        situated_state=state,
        capability_available_candidate=available,
        previous_opportunity_status=previous_opportunity_status,
        source_refs=(f"controlled:situated-capability-case:{case_id}",),
        provenance_refs=(f"provenance:situated-capability-case:{case_id}:{state_id}",),
    )


def build_cases_v1() -> Tuple[SituatedCapabilityPreconditionRequestV1, ...]:
    return (
        _request(
            "TEXT_PRESENCE_ONLY", "t0", 0,
            information_need_ref=TEXT_PRESENCE_INFORMATION_NEED,
            goal_ref="goal:detect-text-presence:v1",
            active=True, continuation=False, available=True, satisfied=(VISIBLE,),
        ),
        _request(
            "READ_PRIMARY_SIGN_TEXT", "t0", 0,
            information_need_ref=PRIMARY_SIGN_TEXT_INFORMATION_NEED,
            goal_ref="goal:read-primary-transit-sign:v1",
            active=True, continuation=False, available=True, satisfied=ALL_SUPPORTED_CONDITIONS,
        ),
        _request(
            "SAME_CAPABILITY_DIFFERENT_INFORMATION_NEED", "presence", 0,
            information_need_ref=TEXT_PRESENCE_INFORMATION_NEED,
            goal_ref="goal:detect-text-presence:v1",
            active=True, continuation=False, available=True, satisfied=(VISIBLE,),
        ),
        _request(
            "SAME_CAPABILITY_DIFFERENT_INFORMATION_NEED", "primary", 1,
            information_need_ref=PRIMARY_SIGN_TEXT_INFORMATION_NEED,
            goal_ref="goal:read-primary-transit-sign:v1",
            active=True, continuation=False, available=True, satisfied=(VISIBLE,),
        ),
    )


__all__ = ["build_cases_v1"]
