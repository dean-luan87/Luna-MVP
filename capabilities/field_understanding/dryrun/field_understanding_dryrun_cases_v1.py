# -*- coding: utf-8 -*-
"""Field-Oriented Egocentric Action Understanding — dry-run cases v1."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.core.field_understanding_static_validators_v1 import (
    validate_core_bundle,
)
from capabilities.field_understanding.core.field_understanding_types_v1 import (
    FIELD_CONTEXT_GOVERNANCE_ID,
    FIELD_CONTEXT_GOVERNANCE_NOTE,
    FIELD_CONTEXT_GOVERNANCE_NOTE_ZH,
    FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID,
    FIELD_INFORMATION_PRIORITY_GOVERNANCE_NOTE,
    FIELD_INFORMATION_PRIORITY_GOVERNANCE_NOTE_ZH,
    PHASE_ID,
    ActionDistanceCandidate,
    DynamicFieldStateCandidate,
    EgocentricMapAlignmentCandidate,
    ExternalMapCandidate,
    FieldCandidate,
    FieldInfluenceCandidate,
    SemanticFieldObjectCandidate,
    SpatialFusionCandidate,
    StaticFieldStructureCandidate,
    candidate_to_dict,
)

FINAL_DECISION_DRYRUN_CASES_READY = "FIELD_UNDERSTANDING_DRYRUN_CASES_READY_FOR_RUNNER"

_TS = "2026-06-17T12:00:00Z"
_STUB = ("dryrun_stub_v1",)


@dataclass(frozen=True)
class FieldUnderstandingDryRunCase:
    case_id: str
    case_name: str
    case_goal: str
    field_candidate: FieldCandidate
    static_candidates: Tuple[StaticFieldStructureCandidate, ...]
    dynamic_candidates: Tuple[DynamicFieldStateCandidate, ...]
    semantic_candidates: Tuple[SemanticFieldObjectCandidate, ...]
    influence_candidates: Tuple[FieldInfluenceCandidate, ...]
    distance_candidates: Tuple[ActionDistanceCandidate, ...]
    external_map_candidates: Tuple[ExternalMapCandidate, ...]
    map_alignment_candidates: Tuple[EgocentricMapAlignmentCandidate, ...]
    spatial_fusion_candidate: SpatialFusionCandidate
    expected_validation_ok: bool
    expected_action_readiness: str
    expected_notes: Tuple[str, ...]


def _validate_case(case: FieldUnderstandingDryRunCase) -> Tuple[bool, List[str]]:
    return validate_core_bundle(
        field=candidate_to_dict(case.field_candidate),
        static_structures=[candidate_to_dict(s) for s in case.static_candidates],
        dynamic_states=[candidate_to_dict(d) for d in case.dynamic_candidates],
        semantic_objects=[candidate_to_dict(s) for s in case.semantic_candidates],
        influences=[candidate_to_dict(i) for i in case.influence_candidates],
        distances=[candidate_to_dict(d) for d in case.distance_candidates],
        external_maps=[candidate_to_dict(m) for m in case.external_map_candidates],
        alignments=[candidate_to_dict(a) for a in case.map_alignment_candidates],
        fusions=[candidate_to_dict(case.spatial_fusion_candidate)],
    )


def build_case_corridor_door_anchor() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case01_corridor"
    struct_ref = "struct_case01_door"
    sem_ref = "sem_case01_door"
    dist_ref = "dist_case01_door"
    fusion_ref = "fusion_case01"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="corridor",
        field_confidence=0.84,
        source_refs=_STUB,
        static_structure_refs=(struct_ref,),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(),
    )
    static = StaticFieldStructureCandidate(
        structure_ref=struct_ref,
        object_class="door",
        stability_score=0.91,
        observed_count=4,
        last_observed_at=_TS,
        position_band="mid_field",
        semantic_label="door_ahead",
        source_refs=_STUB,
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=struct_ref,
        object_class="door",
        semantic_roles=("path_anchor", "destination_anchor"),
        risk_tags=(),
        attention_tags=("task_relevant",),
        destination_tags=("possible_target",),
        memory_tags=(),
        action_relevance="medium",
        source_refs=_STUB,
        confidence=0.78,
    )
    distance = ActionDistanceCandidate(
        distance_ref=dist_ref,
        object_ref=struct_ref,
        distance_band="mid_anchor_zone",
        estimated_distance_m=4.2,
        error_band_m=1.0,
        method="object_size_prior",
        confidence=0.72,
        source_refs=_STUB,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(struct_ref,),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(),
        distance_refs=(dist_ref,),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.8,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_01_corridor_door_anchor",
        case_name="Corridor door ahead anchor",
        case_goal="Validate static structure, semantic anchor, and action distance band without confirming destination.",
        field_candidate=field,
        static_candidates=(static,),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=(),
        distance_candidates=(distance,),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="ready_for_action_decision",
        expected_notes=(
            "Door is a static path anchor, not a confirmed destination.",
            "GraphEQA observe: metric-semantic binding as candidate only.",
        ),
    )


def build_case_elevator_lobby_alignment() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case02_elevator_lobby"
    struct_ref = "struct_case02_elevator_door"
    sem_ref = "sem_case02_elevator"
    map_ref = "map_case02_elevator_poi"
    align_ref = "align_case02_elevator"
    fusion_ref = "fusion_case02"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="elevator_lobby",
        field_confidence=0.88,
        source_refs=_STUB + ("ocr_stub_v1", "map_stub_v1"),
        static_structure_refs=(struct_ref,),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(align_ref,),
    )
    static = StaticFieldStructureCandidate(
        structure_ref=struct_ref,
        object_class="elevator_door",
        stability_score=0.93,
        observed_count=5,
        last_observed_at=_TS,
        position_band="near_front",
        semantic_label="elevator_door",
        source_refs=_STUB,
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=struct_ref,
        object_class="elevator_door",
        semantic_roles=("path_anchor", "navigation_signal"),
        risk_tags=(),
        attention_tags=("high_attention", "must_confirm"),
        destination_tags=("elevator_candidate",),
        memory_tags=(),
        action_relevance="high",
        source_refs=_STUB + ("ocr_stub_v1",),
        confidence=0.86,
    )
    external_map = ExternalMapCandidate(
        map_ref=map_ref,
        map_source="external_poi_api",
        map_type="poi",
        area_ref="lobby_zone_a",
        poi_ref="elevator_bank_1",
        route_ref=None,
        expected_anchor="elevator_nearby",
        confidence=0.75,
        freshness="fresh",
    )
    alignment = EgocentricMapAlignmentCandidate(
        alignment_ref=align_ref,
        map_ref=map_ref,
        visual_anchor_refs=("vis_elevator_door_01",),
        ocr_anchor_refs=("ocr_lift_lobby_01",),
        pose_refs=(),
        semantic_match_score=0.82,
        alignment_status="aligned",
        confidence=0.81,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(struct_ref,),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(),
        distance_refs=(),
        map_alignment_refs=(align_ref,),
        conflict_refs=(),
        confidence=0.84,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_02_elevator_lobby_alignment",
        case_name="Elevator lobby OCR-visual-map alignment",
        case_goal="Validate OCR, vision, and external map triangulation as aligned candidates.",
        field_candidate=field,
        static_candidates=(static,),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=(),
        distance_candidates=(),
        external_map_candidates=(external_map,),
        map_alignment_candidates=(alignment,),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="ready_for_action_decision",
        expected_notes=(
            "OCR Lift Lobby + visual elevator_door + map POI aligned.",
            "Map remains prior; alignment is candidate-only.",
        ),
    )


def build_case_temporary_box_obstacle() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case03_corridor_box"
    dyn_ref = "dyn_case03_box"
    dist_ref = "dist_case03_box"
    fusion_ref = "fusion_case03"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="corridor",
        field_confidence=0.8,
        source_refs=_STUB,
        static_structure_refs=(),
        dynamic_state_refs=(dyn_ref,),
        semantic_object_refs=(),
        map_alignment_refs=(),
    )
    dynamic = DynamicFieldStateCandidate(
        state_ref=dyn_ref,
        object_ref="obj_case03_box",
        tracker_ref="trk_case03_box",
        dynamic_type="temporary_obstacle",
        current_state="temporary_obstacle",
        movement_trend="stationary",
        ttl_ms=5000,
        risk_level="medium",
        source_refs=_STUB,
    )
    distance = ActionDistanceCandidate(
        distance_ref=dist_ref,
        object_ref="obj_case03_box",
        distance_band="near_action_zone",
        estimated_distance_m=1.8,
        error_band_m=0.6,
        method="object_size_prior",
        confidence=0.7,
        source_refs=_STUB,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(dyn_ref,),
        semantic_refs=(),
        influence_refs=(),
        distance_refs=(dist_ref,),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.76,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_03_temporary_box_obstacle",
        case_name="Temporary box blocking corridor",
        case_goal="Validate dynamic obstacle with TTL must not enter static map.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(dynamic,),
        semantic_candidates=(),
        influence_candidates=(),
        distance_candidates=(distance,),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="ready_for_action_decision",
        expected_notes=(
            "Box is dynamic-only with ttl_ms=5000.",
            "Ready for action decision, not immediate navigation execution.",
        ),
    )


def build_case_metro_crowd_density() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case04_metro"
    dyn_ref = "dyn_case04_crowd"
    inf_move = "inf_case04_movement"
    inf_risk = "inf_case04_risk"
    inf_social = "inf_case04_social"
    fusion_ref = "fusion_case04"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="metro_station",
        field_confidence=0.87,
        source_refs=_STUB,
        static_structure_refs=(),
        dynamic_state_refs=(dyn_ref,),
        semantic_object_refs=(),
        map_alignment_refs=(),
    )
    dynamic = DynamicFieldStateCandidate(
        state_ref=dyn_ref,
        object_ref="obj_case04_crowd",
        tracker_ref="trk_case04_crowd",
        dynamic_type="crowd",
        current_state="present",
        movement_trend="lateral",
        ttl_ms=8000,
        risk_level="high",
        source_refs=_STUB,
    )
    influences = (
        FieldInfluenceCandidate(
            influence_ref=inf_move,
            field_ref=field_ref,
            influence_type="movement_constraint",
            affected_target="action_plan",
            risk_level="high",
            action_relevance="high",
            emotional_relevance="medium",
            memory_relevance="low",
            source_refs=_STUB,
            confidence=0.79,
        ),
        FieldInfluenceCandidate(
            influence_ref=inf_risk,
            field_ref=field_ref,
            influence_type="risk_increase",
            affected_target="risk_profile",
            risk_level="high",
            action_relevance="high",
            emotional_relevance="medium",
            memory_relevance="none",
            source_refs=_STUB,
            confidence=0.81,
        ),
        FieldInfluenceCandidate(
            influence_ref=inf_social,
            field_ref=field_ref,
            influence_type="social_density_increase",
            affected_target="attention_budget",
            risk_level="medium",
            action_relevance="high",
            emotional_relevance="low",
            memory_relevance="none",
            source_refs=_STUB,
            confidence=0.77,
        ),
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(dyn_ref,),
        semantic_refs=(),
        influence_refs=(inf_move, inf_risk, inf_social),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.78,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_04_metro_crowd_density",
        case_name="Metro station crowd density influence",
        case_goal="Validate field influence on movement constraint and conservative action strategy.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(dynamic,),
        semantic_candidates=(),
        influence_candidates=influences,
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="ready_for_action_decision",
        expected_notes=(
            "Crowd dynamic state drives movement_constraint and risk_increase.",
            "Dynamic tracking weight should rise; no static map write.",
        ),
    )


def build_case_map_exit_not_observed() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case05_metro_exit"
    map_ref = "map_case05_exit_a"
    align_ref = "align_case05_exit"
    fusion_ref = "fusion_case05"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="metro_station",
        field_confidence=0.7,
        source_refs=_STUB + ("map_stub_v1",),
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(),
        map_alignment_refs=(align_ref,),
    )
    external_map = ExternalMapCandidate(
        map_ref=map_ref,
        map_source="external_poi_api",
        map_type="exit_hint",
        area_ref="platform_zone_b",
        poi_ref="exit_a",
        route_ref=None,
        expected_anchor="exit_a_nearby",
        confidence=0.68,
        freshness="stale",
    )
    alignment = EgocentricMapAlignmentCandidate(
        alignment_ref=align_ref,
        map_ref=map_ref,
        visual_anchor_refs=(),
        ocr_anchor_refs=(),
        pose_refs=(),
        semantic_match_score=0.2,
        alignment_status="not_observed",
        confidence=0.55,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(),
        influence_refs=(),
        distance_refs=(),
        map_alignment_refs=(align_ref,),
        conflict_refs=("conflict_map_exit_unconfirmed",),
        confidence=0.58,
        action_readiness="needs_more_observation",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_05_map_exit_not_observed",
        case_name="Map exit hint without visual confirmation",
        case_goal="Validate external map cannot become fact without visual or OCR anchors.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(),
        influence_candidates=(),
        distance_candidates=(),
        external_map_candidates=(external_map,),
        map_alignment_candidates=(alignment,),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="needs_more_observation",
        expected_notes=(
            "Map suggests exit nearby; vision and OCR did not confirm.",
            "Must not claim user is at exit.",
        ),
    )


def build_case_night_street_low_visibility() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case06_night_street"
    inf_ref = "inf_case06_visibility"
    dist_ref = "dist_case06_front"
    fusion_ref = "fusion_case06"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="street",
        field_confidence=0.62,
        source_refs=_STUB,
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(),
        map_alignment_refs=(),
    )
    influence = FieldInfluenceCandidate(
        influence_ref=inf_ref,
        field_ref=field_ref,
        influence_type="visibility_degradation",
        affected_target="risk_profile",
        risk_level="medium",
        action_relevance="high",
        emotional_relevance="low",
        memory_relevance="none",
        source_refs=_STUB,
        confidence=0.74,
    )
    distance = ActionDistanceCandidate(
        distance_ref=dist_ref,
        object_ref="obj_case06_front_path",
        distance_band="unknown_but_risky",
        estimated_distance_m=None,
        error_band_m=None,
        method="human_like_estimation",
        confidence=0.45,
        source_refs=_STUB,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(),
        influence_refs=(inf_ref,),
        distance_refs=(dist_ref,),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.5,
        action_readiness="needs_more_observation",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_06_night_street_low_visibility",
        case_name="Night street low visibility degradation",
        case_goal="Validate field influence on conservative risk strategy under low vision confidence.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(),
        influence_candidates=(influence,),
        distance_candidates=(distance,),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="needs_more_observation",
        expected_notes=(
            "Low visibility without real sensor feed; stay at needs_more_observation.",
            "Do not escalate to blocked_by_safety without proximity evidence.",
        ),
    )


def build_case_memory_anchor_door() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case07_memory_door"
    struct_ref = "struct_case07_door"
    sem_ref = "sem_case07_door"
    fusion_ref = "fusion_case07"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="home",
        field_confidence=0.83,
        source_refs=_STUB + ("memory_stub_v1",),
        static_structure_refs=(struct_ref,),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(),
    )
    static = StaticFieldStructureCandidate(
        structure_ref=struct_ref,
        object_class="door",
        stability_score=0.95,
        observed_count=12,
        last_observed_at=_TS,
        position_band="mid_field",
        semantic_label="user_named_door",
        source_refs=_STUB + ("memory_stub_v1",),
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=struct_ref,
        object_class="door",
        semantic_roles=("memory_anchor", "destination_anchor"),
        risk_tags=(),
        attention_tags=("user_requested", "task_relevant"),
        destination_tags=("possible_target",),
        memory_tags=("seen_before", "user_named"),
        action_relevance="high",
        source_refs=_STUB + ("memory_stub_v1",),
        confidence=0.88,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(struct_ref,),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.86,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_07_memory_anchor_door",
        case_name="User memory anchor door",
        case_goal="Validate memory_tags and semantic roles for midplatform task candidacy without auto action.",
        field_candidate=field,
        static_candidates=(static,),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=(),
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="ready_for_action_decision",
        expected_notes=(
            "Memory anchor supports task candidacy only.",
            "Ready for action decision does not mean automatic navigation.",
        ),
    )


def build_case_crosswalk_vehicle_risk() -> FieldUnderstandingDryRunCase:
    field_ref = "field_case08_crosswalk"
    struct_ref = "struct_case08_crosswalk"
    dyn_ref = "dyn_case08_vehicle"
    sem_cross = "sem_case08_crosswalk"
    inf_ref = "inf_case08_risk"
    dist_ref = "dist_case08_crosswalk"
    fusion_ref = "fusion_case08"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="crosswalk",
        field_confidence=0.85,
        source_refs=_STUB,
        static_structure_refs=(struct_ref,),
        dynamic_state_refs=(dyn_ref,),
        semantic_object_refs=(sem_cross,),
        map_alignment_refs=(),
    )
    static = StaticFieldStructureCandidate(
        structure_ref=struct_ref,
        object_class="crosswalk",
        stability_score=0.92,
        observed_count=6,
        last_observed_at=_TS,
        position_band="near_front",
        semantic_label="crosswalk_marking",
        source_refs=_STUB,
    )
    dynamic = DynamicFieldStateCandidate(
        state_ref=dyn_ref,
        object_ref="obj_case08_vehicle",
        tracker_ref="trk_case08_vehicle",
        dynamic_type="vehicle",
        current_state="approaching",
        movement_trend="approaching",
        ttl_ms=3000,
        risk_level="critical",
        source_refs=_STUB,
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_cross,
        object_ref=struct_ref,
        object_class="crosswalk",
        semantic_roles=("path_anchor", "warning_signal"),
        risk_tags=("vehicle_risk", "moving_object_risk"),
        attention_tags=("high_attention", "must_confirm"),
        destination_tags=("route_checkpoint",),
        memory_tags=(),
        action_relevance="high",
        source_refs=_STUB,
        confidence=0.8,
    )
    influence = FieldInfluenceCandidate(
        influence_ref=inf_ref,
        field_ref=field_ref,
        influence_type="risk_increase",
        affected_target="action_plan",
        risk_level="critical",
        action_relevance="high",
        emotional_relevance="medium",
        memory_relevance="none",
        source_refs=_STUB,
        confidence=0.9,
    )
    distance = ActionDistanceCandidate(
        distance_ref=dist_ref,
        object_ref=struct_ref,
        distance_band="unknown_but_risky",
        estimated_distance_m=None,
        error_band_m=None,
        method="temporal_approach",
        confidence=0.55,
        source_refs=_STUB,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(struct_ref,),
        dynamic_refs=(dyn_ref,),
        semantic_refs=(sem_cross,),
        influence_refs=(inf_ref,),
        distance_refs=(dist_ref,),
        map_alignment_refs=(),
        conflict_refs=("conflict_crosswalk_vs_moving_vehicle",),
        confidence=0.72,
        action_readiness="blocked_by_safety",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_08_crosswalk_vehicle_risk",
        case_name="Crosswalk with moving vehicle risk",
        case_goal="Validate static crosswalk does not authorize crossing when dynamic vehicle risk conflicts.",
        field_candidate=field,
        static_candidates=(static,),
        dynamic_candidates=(dynamic,),
        semantic_candidates=(semantic,),
        influence_candidates=(influence,),
        distance_candidates=(distance,),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="blocked_by_safety",
        expected_notes=(
            "Crosswalk visible but vehicle moving; must not suggest crossing.",
            "Core safety governance case for Field Graph / Action-Semantic Map.",
        ),
    )


def build_case_user_exit_fact_influences_field() -> FieldUnderstandingDryRunCase:
    """User requests EXIT confirmation; OCR fact influences field but does not override it."""
    field_ref = "field_case09_uncertain_exit"
    sem_ref = "sem_case09_exit_sign"
    fact_ref = "fact_ocr_exit_01"
    inf_ref = "inf_case09_exit_confirmation"
    fusion_ref = "fusion_case09"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="corridor",
        field_confidence=0.68,
        source_refs=_STUB + ("user_request_stub_v1",),
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(),
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=fact_ref,
        object_class="fixed_sign",
        semantic_roles=("warning_signal", "navigation_signal"),
        risk_tags=("uncertain_risk",),
        attention_tags=("user_requested", "must_confirm", "high_attention"),
        destination_tags=("exit_candidate",),
        memory_tags=(),
        action_relevance="high",
        source_refs=_STUB + ("ocr_stub_v1", "user_request_stub_v1"),
        confidence=0.82,
    )
    influence = FieldInfluenceCandidate(
        influence_ref=inf_ref,
        field_ref=field_ref,
        influence_type="semantic_confirmation_needed",
        affected_target="attention_budget",
        risk_level="medium",
        action_relevance="high",
        emotional_relevance="low",
        memory_relevance="none",
        source_refs=_STUB + ("ocr_stub_v1",),
        confidence=0.8,
        fact_ref=fact_ref,
        influence_scope="attention_weighting",
        affected_field_dimension="field_attention",
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(inf_ref,),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=("conflict_exit_sign_vs_passage_unknown",),
        confidence=0.66,
        action_readiness="needs_more_observation",
        fact_influence_refs=(fact_ref,),
        fact_influence_level="strong",
        field_revision_policy="influence_only",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_09_user_exit_fact_influences_field",
        case_name="User EXIT request with fact influence on uncertain field",
        case_goal="Validate OCR EXIT fact influences field synthesis without overriding uncertain_exit_field.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=(influence,),
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="needs_more_observation",
        expected_notes=(
            "Field synthesis: uncertain_exit_field; OCR EXIT is strong fact influence only.",
            "Output: EXIT sign seen left-front, but passability not confirmed yet.",
            "Field information priority governance: fact influences, does not override field.",
        ),
    )


def build_case_metro_train_display_influences_field_state() -> FieldUnderstandingDryRunCase:
    """Metro station field context; train display OCR influences field dimensions, not field identity."""
    field_ref = "metro_station_field_001"
    struct_ref = "struct_case10_platform_sign"
    sem_ref = "sem_case10_train_display"
    fact_ref = "train_display_ocr_001"
    inf_state = "inf_case10_field_state"
    inf_action = "inf_case10_action_logic"
    inf_task = "inf_case10_task_relevance"
    fusion_ref = "fusion_case10"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="metro_station",
        field_confidence=0.86,
        source_refs=_STUB + ("ocr_stub_v1",),
        static_structure_refs=(struct_ref,),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(),
    )
    static = StaticFieldStructureCandidate(
        structure_ref=struct_ref,
        object_class="fixed_sign",
        stability_score=0.9,
        observed_count=4,
        last_observed_at=_TS,
        position_band="mid_field",
        semantic_label="platform_train_display_board",
        source_refs=_STUB,
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=fact_ref,
        object_class="fixed_sign",
        semantic_roles=("navigation_signal", "warning_signal"),
        risk_tags=(),
        attention_tags=("task_relevant", "high_attention"),
        destination_tags=("route_checkpoint",),
        memory_tags=(),
        action_relevance="high",
        source_refs=_STUB + ("ocr_stub_v1",),
        confidence=0.84,
    )
    influences = (
        FieldInfluenceCandidate(
            influence_ref=inf_state,
            field_ref=field_ref,
            influence_type="task_progress_support",
            affected_target="task_progress",
            risk_level="low",
            action_relevance="high",
            emotional_relevance="low",
            memory_relevance="none",
            source_refs=_STUB + ("ocr_stub_v1",),
            confidence=0.82,
            fact_ref=fact_ref,
            influence_scope="field_synthesis",
            affected_field_dimension="field_state",
        ),
        FieldInfluenceCandidate(
            influence_ref=inf_action,
            field_ref=field_ref,
            influence_type="attention_shift",
            affected_target="action_plan",
            risk_level="low",
            action_relevance="high",
            emotional_relevance="none",
            memory_relevance="none",
            source_refs=_STUB + ("ocr_stub_v1",),
            confidence=0.8,
            fact_ref=fact_ref,
            influence_scope="field_synthesis",
            affected_field_dimension="field_action_logic",
        ),
        FieldInfluenceCandidate(
            influence_ref=inf_task,
            field_ref=field_ref,
            influence_type="task_progress_support",
            affected_target="task_progress",
            risk_level="medium",
            action_relevance="high",
            emotional_relevance="none",
            memory_relevance="none",
            source_refs=_STUB + ("ocr_stub_v1",),
            confidence=0.81,
            fact_ref=fact_ref,
            influence_scope="field_synthesis",
            affected_field_dimension="field_task_relevance",
        ),
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(struct_ref,),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(inf_state, inf_action, inf_task),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.83,
        action_readiness="ready_for_action_decision",
        fact_influence_refs=(fact_ref,),
        fact_influence_level="strong",
        field_revision_policy="influence_only",
    )
    return FieldUnderstandingDryRunCase(
        case_id="case_10_metro_train_display_influences_field_state",
        case_name="Metro train display influences field dimensions",
        case_goal=(
            "Validate metro_station remains primary field context while train display OCR "
            "influences field_state, field_action_logic, and field_task_relevance."
        ),
        field_candidate=field,
        static_candidates=(static,),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=influences,
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=True,
        expected_action_readiness="ready_for_action_decision",
        expected_notes=(
            "Field context: metro_station; detail: train_to_xxx / 3min / platform left.",
            "Display fact must not rewrite field_type to display_screen.",
            "Output supports next action under metro field, not direct OCR command.",
            "Field provides context; details provide influence factors.",
        ),
    )


def build_invalid_case_fact_overrides_field() -> FieldUnderstandingDryRunCase:
    """Invalid: single fact attempts to directly override field information."""
    field_ref = "field_invalid_d"
    sem_ref = "sem_invalid_exit"
    fact_ref = "fact_invalid_ocr_exit"
    fusion_ref = "fusion_invalid_d"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="corridor",
        field_confidence=0.7,
        source_refs=_STUB + ("ocr_stub_v1",),
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(),
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=fact_ref,
        object_class="fixed_sign",
        semantic_roles=("destination_anchor",),
        risk_tags=(),
        attention_tags=("high_attention",),
        destination_tags=("exit_candidate",),
        memory_tags=(),
        action_relevance="high",
        source_refs=_STUB + ("ocr_stub_v1",),
        confidence=0.9,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.88,
        action_readiness="ready_for_action_decision",
        fact_influence_refs=(fact_ref,),
        fact_influence_level="strong",
        field_revision_policy="override_field",
    )
    return FieldUnderstandingDryRunCase(
        case_id="invalid_d_fact_overrides_field",
        case_name="Invalid: fact directly overrides field",
        case_goal="Reject direct fact-to-field override outside governed influence policies.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=(),
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=False,
        expected_action_readiness="unknown",
        expected_notes=("field_revision_policy_prohibited:override_field",),
    )


def build_invalid_case_fact_action_without_field_context() -> FieldUnderstandingDryRunCase:
    """Invalid: isolated fact influences action before field context is resolved."""
    field_ref = "field_invalid_e"
    fact_ref = "fact_invalid_display"
    sem_ref = "sem_invalid_display"
    inf_ref = "inf_invalid_e"
    fusion_ref = "fusion_invalid_e"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="unknown",
        field_confidence=0.0,
        source_refs=_STUB,
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(sem_ref,),
        map_alignment_refs=(),
    )
    semantic = SemanticFieldObjectCandidate(
        semantic_ref=sem_ref,
        object_ref=fact_ref,
        object_class="fixed_sign",
        semantic_roles=("navigation_signal",),
        risk_tags=(),
        attention_tags=("high_attention",),
        destination_tags=(),
        memory_tags=(),
        action_relevance="high",
        source_refs=_STUB + ("ocr_stub_v1",),
        confidence=0.85,
    )
    influence = FieldInfluenceCandidate(
        influence_ref=inf_ref,
        field_ref=field_ref,
        influence_type="task_progress_support",
        affected_target="action_plan",
        risk_level="low",
        action_relevance="high",
        emotional_relevance="none",
        memory_relevance="none",
        source_refs=_STUB,
        confidence=0.8,
        fact_ref=fact_ref,
        influence_scope="field_synthesis",
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(sem_ref,),
        influence_refs=(inf_ref,),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.7,
        action_readiness="ready_for_action_decision",
        fact_influence_refs=(fact_ref,),
        fact_influence_level="strong",
        field_revision_policy="influence_only",
    )
    return FieldUnderstandingDryRunCase(
        case_id="invalid_e_fact_action_without_field_context",
        case_name="Invalid: fact action before field context resolved",
        case_goal="Reject isolated fact driving action when field_type is unknown.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(semantic,),
        influence_candidates=(influence,),
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=False,
        expected_action_readiness="unknown",
        expected_notes=("field_context_unresolved_before_fact_action",),
    )


def build_invalid_case_dynamic_box_in_static() -> FieldUnderstandingDryRunCase:
    """Invalid: temporary box wrongly stored as static structure."""
    field_ref = "field_invalid_a"
    struct_ref = "struct_invalid_box"
    fusion_ref = "fusion_invalid_a"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="corridor",
        field_confidence=0.7,
        source_refs=_STUB,
        static_structure_refs=(struct_ref,),
        dynamic_state_refs=(),
        semantic_object_refs=(),
        map_alignment_refs=(),
    )
    static = StaticFieldStructureCandidate(
        structure_ref=struct_ref,
        object_class="box",
        stability_score=0.88,
        observed_count=1,
        last_observed_at=_TS,
        position_band="near_front",
        semantic_label="box_obstacle",
        source_refs=_STUB,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(struct_ref,),
        dynamic_refs=(),
        semantic_refs=(),
        influence_refs=(),
        distance_refs=(),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.7,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="invalid_a_dynamic_box_in_static",
        case_name="Invalid: box in static map",
        case_goal="Reject temporary obstacle polluting static field structure registry.",
        field_candidate=field,
        static_candidates=(static,),
        dynamic_candidates=(),
        semantic_candidates=(),
        influence_candidates=(),
        distance_candidates=(),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=False,
        expected_action_readiness="unknown",
        expected_notes=("object_class box is not a registered static class.",),
    )


def build_invalid_case_aligned_without_anchors() -> FieldUnderstandingDryRunCase:
    """Invalid: map alignment marked aligned without visual/OCR anchors."""
    field_ref = "field_invalid_b"
    map_ref = "map_invalid_b"
    align_ref = "align_invalid_b"
    fusion_ref = "fusion_invalid_b"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="mall",
        field_confidence=0.75,
        source_refs=_STUB + ("map_stub_v1",),
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(),
        map_alignment_refs=(align_ref,),
    )
    external_map = ExternalMapCandidate(
        map_ref=map_ref,
        map_source="offline_map_pack",
        map_type="poi",
        area_ref="mall_wing_c",
        poi_ref="shop_23",
        route_ref=None,
        expected_anchor="shop_nearby",
        confidence=0.8,
        freshness="fresh",
    )
    alignment = EgocentricMapAlignmentCandidate(
        alignment_ref=align_ref,
        map_ref=map_ref,
        visual_anchor_refs=(),
        ocr_anchor_refs=(),
        pose_refs=(),
        semantic_match_score=0.9,
        alignment_status="aligned",
        confidence=0.88,
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(),
        influence_refs=(),
        distance_refs=(),
        map_alignment_refs=(align_ref,),
        conflict_refs=(),
        confidence=0.85,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="invalid_b_aligned_without_anchors",
        case_name="Invalid: aligned map without anchors",
        case_goal="Reject map prior overreach without egocentric anchor evidence.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(),
        influence_candidates=(),
        distance_candidates=(),
        external_map_candidates=(external_map,),
        map_alignment_candidates=(alignment,),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=False,
        expected_action_readiness="unknown",
        expected_notes=("aligned_requires_visual_or_ocr_anchor_refs",),
    )


def build_invalid_case_near_zone_without_sources() -> FieldUnderstandingDryRunCase:
    """Invalid: high-risk distance band without source_refs."""
    field_ref = "field_invalid_c"
    dist_ref = "dist_invalid_c"
    fusion_ref = "fusion_invalid_c"

    field = FieldCandidate(
        field_ref=field_ref,
        field_type="corridor",
        field_confidence=0.7,
        source_refs=_STUB,
        static_structure_refs=(),
        dynamic_state_refs=(),
        semantic_object_refs=(),
        map_alignment_refs=(),
    )
    distance = ActionDistanceCandidate(
        distance_ref=dist_ref,
        object_ref="obj_invalid_obstacle",
        distance_band="near_action_zone",
        estimated_distance_m=1.2,
        error_band_m=0.4,
        method="depth_sensor",
        confidence=0.65,
        source_refs=(),
    )
    fusion = SpatialFusionCandidate(
        fusion_ref=fusion_ref,
        field_ref=field_ref,
        static_refs=(),
        dynamic_refs=(),
        semantic_refs=(),
        influence_refs=(),
        distance_refs=(dist_ref,),
        map_alignment_refs=(),
        conflict_refs=(),
        confidence=0.6,
        action_readiness="ready_for_action_decision",
    )
    return FieldUnderstandingDryRunCase(
        case_id="invalid_c_near_zone_without_sources",
        case_name="Invalid: near_action_zone without source_refs",
        case_goal="Reject high-risk distance band without evidence refs.",
        field_candidate=field,
        static_candidates=(),
        dynamic_candidates=(),
        semantic_candidates=(),
        influence_candidates=(),
        distance_candidates=(distance,),
        external_map_candidates=(),
        map_alignment_candidates=(),
        spatial_fusion_candidate=fusion,
        expected_validation_ok=False,
        expected_action_readiness="unknown",
        expected_notes=("high_risk_distance_band_requires_source_refs",),
    )


def build_dryrun_cases_v1() -> Tuple[FieldUnderstandingDryRunCase, ...]:
    return (
        build_case_corridor_door_anchor(),
        build_case_elevator_lobby_alignment(),
        build_case_temporary_box_obstacle(),
        build_case_metro_crowd_density(),
        build_case_map_exit_not_observed(),
        build_case_night_street_low_visibility(),
        build_case_memory_anchor_door(),
        build_case_crosswalk_vehicle_risk(),
        build_case_user_exit_fact_influences_field(),
        build_case_metro_train_display_influences_field_state(),
    )


def build_invalid_dryrun_cases_v1() -> Tuple[FieldUnderstandingDryRunCase, ...]:
    return (
        build_invalid_case_dynamic_box_in_static(),
        build_invalid_case_aligned_without_anchors(),
        build_invalid_case_near_zone_without_sources(),
        build_invalid_case_fact_overrides_field(),
        build_invalid_case_fact_action_without_field_context(),
    )


def build_all_dryrun_cases_v1() -> Tuple[FieldUnderstandingDryRunCase, ...]:
    return build_dryrun_cases_v1() + build_invalid_dryrun_cases_v1()


def validate_dryrun_case_ids_unique(
    cases: Tuple[FieldUnderstandingDryRunCase, ...] | None = None,
) -> Tuple[bool, List[str]]:
    cases = cases or build_all_dryrun_cases_v1()
    seen: Dict[str, int] = {}
    duplicates: List[str] = []
    for case in cases:
        seen[case.case_id] = seen.get(case.case_id, 0) + 1
    for case_id, count in seen.items():
        if count > 1:
            duplicates.append(case_id)
    return len(duplicates) == 0, duplicates


def _check_cases(
    cases: Tuple[FieldUnderstandingDryRunCase, ...],
    *,
    expect_valid: bool,
) -> Tuple[int, int, List[str]]:
    ok_count = 0
    fail_mismatches: List[str] = []
    for case in cases:
        valid, issues = _validate_case(case)
        if valid == expect_valid:
            ok_count += 1
        else:
            fail_mismatches.append(
                f"{case.case_id}:expected_valid={expect_valid}:actual_valid={valid}:issues={issues}"
            )
        readiness = case.spatial_fusion_candidate.action_readiness
        if expect_valid and readiness != case.expected_action_readiness:
            fail_mismatches.append(
                f"{case.case_id}:readiness_mismatch:expected={case.expected_action_readiness}:actual={readiness}"
            )
    return ok_count, len(cases) - ok_count, fail_mismatches


def summarize_dryrun_cases_v1() -> Dict[str, Any]:
    positive = build_dryrun_cases_v1()
    invalid = build_invalid_dryrun_cases_v1()
    all_cases = positive + invalid

    unique_ok, duplicates = validate_dryrun_case_ids_unique(all_cases)
    pos_ok, pos_fail, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, inv_fail, inv_mismatches = _check_cases(invalid, expect_valid=False)

    all_positive_validate = pos_ok == len(positive) and not pos_mismatches
    all_invalid_rejected = inv_ok == len(invalid) and not inv_mismatches
    ready = (
        len(positive) >= 10
        and len(invalid) >= 5
        and unique_ok
        and all_positive_validate
        and all_invalid_rejected
    )

    return {
        "phase_id": PHASE_ID,
        "governance_id": FIELD_INFORMATION_PRIORITY_GOVERNANCE_ID,
        "field_information_priority_governance_note": FIELD_INFORMATION_PRIORITY_GOVERNANCE_NOTE,
        "field_information_priority_governance_note_zh": FIELD_INFORMATION_PRIORITY_GOVERNANCE_NOTE_ZH,
        "field_context_governance_id": FIELD_CONTEXT_GOVERNANCE_ID,
        "field_context_governance_note": FIELD_CONTEXT_GOVERNANCE_NOTE,
        "field_context_governance_note_zh": FIELD_CONTEXT_GOVERNANCE_NOTE_ZH,
        "case_count": len(positive),
        "invalid_case_count": len(invalid),
        "dryrun_case_count": len(positive),
        "positive_case_ids": tuple(c.case_id for c in positive),
        "invalid_case_ids": tuple(c.case_id for c in invalid),
        "all_case_ids_unique": unique_ok,
        "duplicate_case_ids": duplicates,
        "all_positive_cases_validate": all_positive_validate,
        "all_invalid_cases_rejected": all_invalid_rejected,
        "cases_ok": pos_ok,
        "invalid_cases_ok": inv_ok,
        "unique_case_ids_ok": unique_ok,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "final_decision": FINAL_DECISION_DRYRUN_CASES_READY if ready else "FIELD_UNDERSTANDING_DRYRUN_CASES_NOT_READY",
    }


if __name__ == "__main__":
    import json

    summary = summarize_dryrun_cases_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
