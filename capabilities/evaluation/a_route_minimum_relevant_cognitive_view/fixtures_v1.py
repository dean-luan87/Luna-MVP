"""Controlled, semantic-condition-driven fixtures for minimum view selection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from capabilities.cognitive_flow.cognitive_primitives.types_v1 import (
    EntityCandidateV1,
    RelationCandidateV1,
)
from capabilities.cognitive_flow.current_cognitive_context.context_inputs_v1 import (
    GoalContextV1,
)
from capabilities.midplatform.core.a_route_orchestration.a_route_minimum_relevant_cognitive_view_types_v1 import (
    ARouteMinimumRelevantCognitiveViewRequestV1,
    AvailableCognitiveInformationItemV1,
    EXTERNAL_INFORMATION,
    SELF_INFORMATION,
)
from capabilities.midplatform.field_perception_orchestrator.integration.active_observation_precondition_types_v1 import (
    SelfPerceptualViewpointStateV1,
)


SOURCE_MODE = "CONTROLLED_A_ROUTE_MINIMUM_RELEVANT_COGNITIVE_VIEW_TEST"
SEAT_CONDITION = "condition:goal:seat-location"
EXIT_CONDITION = "condition:goal:exit-location"
OWNER_CONDITION = "condition:role:workspace-owner"
VISITOR_CONDITION = "condition:role:visitor"
ENERGY_CONDITION = "condition:unrelated:energy-audit"
NOISE_CONDITION = "condition:unrelated:clutter"


@dataclass(frozen=True)
class MinimumViewCaseV1:
    case_id: str
    category: str
    request: ARouteMinimumRelevantCognitiveViewRequestV1


def _goal(goal_ref: str, conditions: Tuple[str, ...]) -> GoalContextV1:
    return GoalContextV1(
        goal_ref=goal_ref,
        primary_goal="controlled governed objective",
        secondary_goal_refs=(),
        success_condition_refs=conditions,
        stop_condition_refs=(),
        provenance={"fixture": "governed-goal-condition"},
        trace=f"trace:goal:{goal_ref}",
    )


def _self_viewpoint() -> SelfPerceptualViewpointStateV1:
    return SelfPerceptualViewpointStateV1(
        state_ref="self-state:viewpoint:001",
        self_ref="self:cognitive-agent:001",
        temporal_ref="temporal:self-viewpoint:001",
        orientation_candidate="FORWARD",
        motion_state_candidate="STATIONARY",
        stability_candidate="STABLE",
        current_view_ref="viewpoint:current:001",
        visible_region_refs=("region:front:001",),
        sensor_availability_candidate="AVAILABLE",
        sensor_availability_refs=("sensor:visual:001",),
        source_refs=("self-state-source:controlled:001",),
        provenance_refs=("provenance:self-viewpoint:controlled:001",),
    )


def _entity() -> EntityCandidateV1:
    return EntityCandidateV1(
        entity_id="entity-candidate:chair:001",
        entity_type="object_candidate",
        attributes={"observed_object_class_candidate": "chair"},
        evidence_refs=("evidence:chair:001",),
        observation_refs=("observation:chair:001",),
        trace_ref="trace:entity:chair:001",
        provenance_refs=("provenance:entity:chair:001",),
    )


def _relation() -> RelationCandidateV1:
    return RelationCandidateV1(
        relation_id="relation-candidate:chair-observed-in-field:001",
        subject_ref="entity-candidate:chair:001",
        predicate="OBSERVED_IN_FIELD",
        object_ref="field:office:001",
        evidence_refs=("evidence:chair:001",),
        trace_ref="trace:relation:chair-field:001",
        provenance_refs=("provenance:relation:chair-field:001",),
    )


_SELF_VIEWPOINT = _self_viewpoint()
_ENTITY = _entity()
_RELATION = _relation()


def _item(
    information_ref: str,
    object_type: str,
    information_kind: str,
    conditions: Tuple[str, ...],
    source_refs: Tuple[str, ...],
) -> AvailableCognitiveInformationItemV1:
    return AvailableCognitiveInformationItemV1(
        information_ref=information_ref,
        object_type=object_type,
        information_kind=information_kind,
        support_condition_refs=conditions,
        source_refs=source_refs,
        provenance_refs=(f"provenance:view-item:{information_ref}",),
    )


def _base_items() -> Tuple[AvailableCognitiveInformationItemV1, ...]:
    return (
        _item(
            "self:viewpoint:current",
            SELF_INFORMATION,
            "situated_self_viewpoint",
            (SEAT_CONDITION,),
            (_SELF_VIEWPOINT.state_ref,),
        ),
        _item(
            "self:capability:visual",
            SELF_INFORMATION,
            "self_capability_state",
            (SEAT_CONDITION,),
            ("self-capability-state:visual:001",),
        ),
        _item(
            _ENTITY.entity_id,
            EXTERNAL_INFORMATION,
            "entity_candidate",
            (SEAT_CONDITION,),
            (_ENTITY.entity_id,),
        ),
        _item(
            _RELATION.relation_id,
            EXTERNAL_INFORMATION,
            "field_relation_state_candidate",
            (SEAT_CONDITION,),
            (_RELATION.relation_id,),
        ),
        _item(
            "self:state:mobility",
            SELF_INFORMATION,
            "situated_self_state",
            (EXIT_CONDITION,),
            ("self-state:mobility:001",),
        ),
        _item(
            "external:exit:relation",
            EXTERNAL_INFORMATION,
            "field_relation_state_candidate",
            (EXIT_CONDITION,),
            ("relation-candidate:exit-field:001",),
        ),
        _item(
            "self:role:workspace-scope",
            SELF_INFORMATION,
            "self_role_scope_candidate",
            (OWNER_CONDITION,),
            ("self-role-scope:001",),
        ),
        _item(
            "external:shared-access:relation",
            EXTERNAL_INFORMATION,
            "field_relation_state_candidate",
            (VISITOR_CONDITION,),
            ("relation-candidate:shared-access:001",),
        ),
        _item(
            "self:resource:battery",
            SELF_INFORMATION,
            "self_resource_state",
            (ENERGY_CONDITION,),
            ("self-resource:battery:001",),
        ),
        _item(
            "external:clutter:poster",
            EXTERNAL_INFORMATION,
            "external_irrelevant_context",
            (NOISE_CONDITION,),
            ("external-clutter:poster:001",),
        ),
    )


def _request(
    goal_ref: str,
    conditions: Tuple[str, ...],
    *,
    items: Tuple[AvailableCognitiveInformationItemV1, ...] | None = None,
    role_conditions: Tuple[str, ...] = (),
    context_ref: str = "context:office:opaque:001",
    candidate_only: bool = True,
) -> ARouteMinimumRelevantCognitiveViewRequestV1:
    return ARouteMinimumRelevantCognitiveViewRequestV1(
        goal_context=_goal(goal_ref, conditions),
        available_information=items or _base_items(),
        governed_role_condition_refs=role_conditions,
        intent_ref="intent:controlled:cognition",
        concern_ref="concern:minimum-relevant-view",
        context_ref=context_ref,
        field_ref="field:office:001",
        role_refs=("role:controlled",),
        current_world_ref="world:candidate:office:001",
        current_cognitive_state_ref="cognitive-state:controlled:001",
        candidate_only=candidate_only,
    )


def build_minimum_view_cases_v1() -> Tuple[MinimumViewCaseV1, ...]:
    base = _base_items()
    seat = _request("goal:find-seat", (SEAT_CONDITION,))
    exit_goal = _request("goal:find-exit", (EXIT_CONDITION,))
    seat_with_battery = _request(
        "goal:find-seat",
        (SEAT_CONDITION,),
        items=base + (_item(
            "self:resource:temperature",
            SELF_INFORMATION,
            "self_resource_state",
            (ENERGY_CONDITION,),
            ("self-resource:temperature:001",),
        ),),
    )
    seat_without_chair = _request(
        "goal:find-seat",
        (SEAT_CONDITION,),
        items=tuple(item for item in base if item.information_ref != _ENTITY.entity_id)
        + (_item(
            "external:chair:updated-relation",
            EXTERNAL_INFORMATION,
            "field_relation_state_candidate",
            (SEAT_CONDITION,),
            ("relation-candidate:chair-field:updated",),
        ),),
    )
    seat_with_degraded_self = _request(
        "goal:find-seat",
        (SEAT_CONDITION,),
        items=tuple(
            item for item in base if item.information_ref != "self:capability:visual"
        )
        + (_item(
            "self:capability:visual:degraded",
            SELF_INFORMATION,
            "self_capability_state",
            (SEAT_CONDITION,),
            ("self-capability-state:visual:degraded",),
        ),),
    )
    return (
        MinimumViewCaseV1("SAME_INFORMATION_DIFFERENT_GOAL:seat", "goal", seat),
        MinimumViewCaseV1("SAME_INFORMATION_DIFFERENT_GOAL:exit", "goal", exit_goal),
        MinimumViewCaseV1("SAME_GOAL_IRRELEVANT_EXTERNAL_CHANGE", "irrelevant_external", _request("goal:find-seat", (SEAT_CONDITION,), items=base + (_item("external:irrelevant:notice", EXTERNAL_INFORMATION, "external_irrelevant_context", (NOISE_CONDITION,), ("external-irrelevant:notice:001",)),))),
        MinimumViewCaseV1("SAME_GOAL_IRRELEVANT_SELF_CHANGE", "irrelevant_self", seat_with_battery),
        MinimumViewCaseV1("SAME_GOAL_RELEVANT_EXTERNAL_CHANGE", "relevant_external", seat_without_chair),
        MinimumViewCaseV1("SAME_GOAL_RELEVANT_SELF_CHANGE", "relevant_self", seat_with_degraded_self),
        MinimumViewCaseV1("SELF_AND_EXTERNAL_REQUIRED_TOGETHER", "self_external", seat),
        MinimumViewCaseV1("SAME_GOAL_DIFFERENT_GOVERNED_ROLE:owner", "role", _request("goal:find-seat", (SEAT_CONDITION,), role_conditions=(OWNER_CONDITION,))),
        MinimumViewCaseV1("SAME_GOAL_DIFFERENT_GOVERNED_ROLE:visitor", "role", _request("goal:find-seat", (SEAT_CONDITION,), role_conditions=(VISITOR_CONDITION,))),
        MinimumViewCaseV1("SAME_GOAL_IRRELEVANT_CONTEXT_CHANGE", "irrelevant_context", _request("goal:find-seat", (SEAT_CONDITION,), context_ref="context:unrelated:opaque:changed")),
        MinimumViewCaseV1("GOAL_CHANGE_REACTIVATES_EXCLUDED_INFORMATION:seat", "reactivation", seat),
        MinimumViewCaseV1("GOAL_CHANGE_REACTIVATES_EXCLUDED_INFORMATION:exit", "reactivation", exit_goal),
    )


def build_negative_minimum_view_requests_v1() -> Tuple[Tuple[str, ARouteMinimumRelevantCognitiveViewRequestV1], ...]:
    return (
        (
            "CANDIDATE_ONLY_REQUIRED",
            _request("goal:find-seat", (SEAT_CONDITION,), candidate_only=False),
        ),
        (
            "DUPLICATE_INFORMATION_REJECTED",
            _request("goal:find-seat", (SEAT_CONDITION,), items=_base_items() + (_base_items()[0],)),
        ),
        (
            "NO_GOVERNED_CONDITION_NO_SELECTION",
            _request("goal:opaque", (), items=_base_items()),
        ),
    )


__all__ = [
    "MinimumViewCaseV1",
    "SOURCE_MODE",
    "build_minimum_view_cases_v1",
    "build_negative_minimum_view_requests_v1",
]
