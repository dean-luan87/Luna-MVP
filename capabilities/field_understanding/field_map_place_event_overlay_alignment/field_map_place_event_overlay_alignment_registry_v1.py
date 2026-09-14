# -*- coding: utf-8 -*-
"""Field Map Place / Realtime Context / Event Overlay Alignment — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.field_map_place_event_overlay_alignment.field_map_place_event_overlay_alignment_types_v1 import (
    FIELD_ALIGNMENT_GOVERNANCE_RULES,
    FIELD_ALIGNMENT_PIPELINE,
    FIELD_ALIGNMENT_SCENARIO_REFS,
    FIELD_DEFINITION_INTERNAL,
    FIELD_DEFINITION_REF,
    FIELD_DEFINITION_USER_LAYER,
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_ALIGNMENT_READY,
    INTERFACE_LAYER_PROTOCOL_REF,
    MODEL_ADMISSION_STANDARD_REF,
    PHASE_ID,
    PLANNING_OBJECT_TYPES,
    SEALED_UPSTREAM_PHASE_REFS,
    SOURCE_CHAIN,
    SPATIAL_EVIDENCE_CHAIN_REF,
    SPATIAL_ODOMETRY_FUSION_REF,
    TARGET_ENTRYPOINT,
    EventOverlayCandidate,
    FieldAlignmentDecision,
    FieldInteractionLabelCandidate,
    FieldMapPlaceAlignmentProfile,
    MapPlaceRefCandidate,
    RealtimeContextOverlayCandidate,
    SpatialEvidenceFieldBindingCandidate,
    candidate_to_dict,
)

REGISTRY_ID = "field_map_place_event_overlay_alignment_registry_v1"
PROFILE_REF = "field_map_place_alignment_profile_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "planning_object_types": PLANNING_OBJECT_TYPES,
    "field_alignment_scenario_refs": FIELD_ALIGNMENT_SCENARIO_REFS,
    "field_alignment_governance_rules": FIELD_ALIGNMENT_GOVERNANCE_RULES,
    "field_alignment_pipeline": FIELD_ALIGNMENT_PIPELINE,
    "sealed_upstream_phase_refs": SEALED_UPSTREAM_PHASE_REFS,
}

_CHAIN_PREFIX = (SOURCE_CHAIN, REGISTRY_ID)

_UPSTREAM_GO_ARTIFACTS: Tuple[Dict[str, str], ...] = (
    {
        "phase_ref": SPATIAL_EVIDENCE_CHAIN_REF,
        "artifact_rel": (
            "_tmp_eval_out/slam_spatial_evidence_chain_closure_v1_smoke_v0/"
            "slam_spatial_evidence_chain_closure_review_v1.json"
        ),
        "expected_go": "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO",
        "module_rel": (
            "capabilities/field_understanding/slam_spatial_evidence_chain_closure/"
            "slam_spatial_evidence_chain_closure_types_v1.py"
        ),
    },
    {
        "phase_ref": SPATIAL_ODOMETRY_FUSION_REF,
        "artifact_rel": (
            "_tmp_eval_out/spatial_odometry_fusion_interface_v1_smoke_v0/"
            "spatial_odometry_fusion_interface_review_v1.json"
        ),
        "expected_go": "SPATIAL_ODOMETRY_FUSION_INTERFACE_PLANNING_READY_FOR_FIELD_PROTOCOL_ALIGNMENT",
        "module_rel": (
            "capabilities/field_understanding/spatial_odometry_fusion_interface/"
            "spatial_odometry_fusion_interface_types_v1.py"
        ),
    },
    {
        "phase_ref": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "artifact_rel": (
            "_tmp_eval_out/interface_layer_governance_v1_smoke_v0/"
            "interface_layer_governance_review_v1.json"
        ),
        "expected_go": "INTERFACE_LAYER_GOVERNANCE_PROTOCOL_BASELINE_READY_FOR_ADOPTION",
        "module_rel": (
            "capabilities/midplatform/interface_layer_governance/"
            "interface_layer_governance_types_v1.py"
        ),
    },
    {
        "phase_ref": MODEL_ADMISSION_STANDARD_REF,
        "artifact_rel": (
            "_tmp_eval_out/model_admission_governance_v1_smoke_v0/"
            "model_admission_governance_run_and_review_v1.json"
        ),
        "expected_go": "MODEL_ADMISSION_GOVERNANCE_STANDARD_REVIEW_GO",
        "module_rel": (
            "capabilities/midplatform/model_admission_governance/"
            "model_admission_governance_types_v1.py"
        ),
    },
)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(PLANNING_OBJECT_TYPES) != 7:
        issues.append("planning_object_types_count_not_7")
    if len(FIELD_ALIGNMENT_SCENARIO_REFS) != 6:
        issues.append("field_alignment_scenario_refs_count_not_6")
    if len(FIELD_ALIGNMENT_GOVERNANCE_RULES) != 12:
        issues.append("field_alignment_governance_rules_count_not_12")
    if len(SEALED_UPSTREAM_PHASE_REFS) != 4:
        issues.append("sealed_upstream_phase_refs_count_not_4")
    return len(issues) == 0, issues


def _map_place(ref_suffix: str, *, place_ref: str, poi: str, category: str) -> Dict[str, Any]:
    candidate = MapPlaceRefCandidate(
        candidate_ref=f"map_place_{ref_suffix}",
        map_place_ref=place_ref,
        poi_name=poi,
        address_hint=f"address_hint_{ref_suffix}",
        category_hint=category,
        global_position_hint={"lat_lon_stub": [31.2304, 121.4737], "accuracy_m": 10.0},
        confidence=0.9,
        source_chain=_CHAIN_PREFIX + (f"map_place_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    return candidate_to_dict(candidate)


def _realtime_context(
    ref_suffix: str,
    *,
    context_type: str,
    observed_state: str,
    time_window: Tuple[int, int],
) -> Dict[str, Any]:
    candidate = RealtimeContextOverlayCandidate(
        candidate_ref=f"realtime_context_{ref_suffix}",
        realtime_context_id=f"rtc_{ref_suffix}",
        context_type=context_type,
        observed_state=observed_state,
        time_window=time_window,
        confidence=0.78,
        source_chain=_CHAIN_PREFIX + (f"realtime_context_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    return candidate_to_dict(candidate)


def _event_overlay(
    ref_suffix: str,
    *,
    event_type: str,
    base_map_place_ref: str,
    user_label: str,
    time_window: Tuple[int, int],
    active: bool = True,
) -> Dict[str, Any]:
    candidate = EventOverlayCandidate(
        candidate_ref=f"event_overlay_{ref_suffix}",
        event_overlay_id=f"evt_{ref_suffix}",
        event_type=event_type,
        base_map_place_ref=base_map_place_ref,
        user_facing_field_label=user_label,
        time_window=time_window,
        confidence=0.85 if active else 0.2,
        source_chain=_CHAIN_PREFIX + (f"event_overlay_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    result = candidate_to_dict(candidate)
    result["overlay_active"] = active
    return result


def _spatial_binding(
    ref_suffix: str,
    *,
    refs: Tuple[str, ...],
    coordinate_scope: str,
    fusion_ref: str,
    flags: Dict[str, bool],
) -> Dict[str, Any]:
    candidate = SpatialEvidenceFieldBindingCandidate(
        candidate_ref=f"spatial_binding_{ref_suffix}",
        binding_id=f"bind_{ref_suffix}",
        spatial_evidence_refs=refs,
        pose_supported=flags.get("pose", False),
        motion_supported=flags.get("motion", False),
        health_supported=flags.get("health", False),
        anchor_supported=flags.get("anchor", False),
        relocalization_supported=flags.get("relocalization", False),
        drift_supported=flags.get("drift", False),
        fusion_candidate_ref=fusion_ref,
        coordinate_scope=coordinate_scope,
        confidence=0.82,
        source_chain=_CHAIN_PREFIX + (f"spatial_binding_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    return candidate_to_dict(candidate)


def _field_label(
    ref_suffix: str,
    *,
    label: str,
    label_source: str,
    priority: int,
    map_place_ref: str,
    overlay_refs: Tuple[str, ...],
    internal_state_ref: str,
) -> Dict[str, Any]:
    candidate = FieldInteractionLabelCandidate(
        candidate_ref=f"field_label_{ref_suffix}",
        field_label=label,
        label_source=label_source,
        display_priority=priority,
        underlying_map_place_ref=map_place_ref,
        overlay_refs=overlay_refs,
        source_chain=_CHAIN_PREFIX + (f"field_label_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        internal_field_state_ref=internal_state_ref,
    )
    return candidate_to_dict(candidate)


def build_field_alignment_scenario_matrix_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "scenario_ref": "stable_map_place_field",
            "scenario_zh": "用户去商场/公司/家/地铁站；map_place_ref 作为用户交互层 field label 主锚点",
            "map_place_field_anchor": True,
            "map_place_fully_defines_field": False,
            "map_place_candidate": _map_place(
                "stable_mall",
                place_ref="place_mall_lujiazui_a",
                poi="陆家嘴商场A",
                category="shopping_mall",
            ),
            "realtime_context_candidate": None,
            "event_overlay_candidate": None,
            "spatial_evidence_binding": _spatial_binding(
                "stable_support",
                refs=("generic_tum_trajectory_chain",),
                coordinate_scope="mixed",
                fusion_ref="spatial_odometry_fusion_outdoor_gps_primary_slam_support",
                flags={"pose": True, "motion": True},
            ),
            "field_interaction_label": _field_label(
                "stable_mall",
                label="陆家嘴商场A",
                label_source="map_place",
                priority=100,
                map_place_ref="place_mall_lujiazui_a",
                overlay_refs=(),
                internal_state_ref="field_state_place_mall_lujiazui_a_v1",
            ),
            "conflict_candidate_required": False,
            "gps_overrides_field_identity": False,
            "slam_overrides_field_identity": False,
        },
        {
            "scenario_ref": "indoor_map_place_with_slam_local_field",
            "scenario_zh": "室内商场/地铁站；GPS 降权，SLAM anchor/pose/motion/health 参与局部 field 构建",
            "map_place_field_anchor": True,
            "gps_weight": "degraded",
            "map_place_candidate": _map_place(
                "indoor_metro",
                place_ref="place_metro_station_b2",
                poi="地铁站B2层",
                category="metro_station",
            ),
            "realtime_context_candidate": None,
            "event_overlay_candidate": None,
            "spatial_evidence_binding": _spatial_binding(
                "indoor_slam",
                refs=(
                    "rtab_map_odometry_chain",
                    "rtab_map_graph_chain",
                ),
                coordinate_scope="local",
                fusion_ref="spatial_odometry_fusion_indoor_slam_primary_gps_degraded",
                flags={
                    "pose": True,
                    "motion": True,
                    "health": True,
                    "anchor": True,
                    "relocalization": True,
                    "drift": True,
                },
            ),
            "field_interaction_label": _field_label(
                "indoor_metro",
                label="地铁站B2层",
                label_source="map_place",
                priority=100,
                map_place_ref="place_metro_station_b2",
                overlay_refs=("spatial_binding_indoor_slam",),
                internal_state_ref="field_state_indoor_metro_b2_v1",
            ),
            "conflict_candidate_required": False,
            "gps_overrides_field_identity": False,
            "slam_overrides_field_identity": False,
        },
        {
            "scenario_ref": "temporary_event_overlay",
            "scenario_zh": "体育馆+演唱会，广场+临时集市；event_overlay 可覆盖 user-facing label，不改写 map_place_ref",
            "event_overlay_can_override_user_facing_label": True,
            "event_overlay_rewrites_map_place": False,
            "map_place_candidate": _map_place(
                "stadium_base",
                place_ref="place_stadium_west",
                poi="西部体育馆",
                category="stadium",
            ),
            "realtime_context_candidate": None,
            "event_overlay_candidate": _event_overlay(
                "concert_night",
                event_type="concert",
                base_map_place_ref="place_stadium_west",
                user_label="周杰伦演唱会现场",
                time_window=(1_700_000_000_000, 1_700_003_600_000),
            ),
            "spatial_evidence_binding": _spatial_binding(
                "event_crowd",
                refs=("rtab_map_graph_chain",),
                coordinate_scope="local",
                fusion_ref="spatial_odometry_fusion_indoor_slam_primary_gps_degraded",
                flags={"anchor": True, "motion": True},
            ),
            "field_interaction_label": _field_label(
                "concert_night",
                label="周杰伦演唱会现场",
                label_source="event_overlay",
                priority=200,
                map_place_ref="place_stadium_west",
                overlay_refs=("event_overlay_concert_night",),
                internal_state_ref="field_state_stadium_concert_overlay_v1",
            ),
            "conflict_candidate_required": False,
        },
        {
            "scenario_ref": "realtime_context_changes_field_state",
            "scenario_zh": "同地点因人流/施工/封控等变化；realtime context 只改变 field_state，不改写 map_place fact",
            "realtime_context_changes_field_state_only": True,
            "map_place_candidate": _map_place(
                "plaza_base",
                place_ref="place_civic_plaza",
                poi="市民广场",
                category="public_plaza",
            ),
            "realtime_context_candidate": _realtime_context(
                "construction_block",
                context_type="construction",
                observed_state="north_exit_partially_closed",
                time_window=(1_700_010_000_000, 1_700_020_000_000),
            ),
            "event_overlay_candidate": None,
            "spatial_evidence_binding": _spatial_binding(
                "plaza_local",
                refs=("rtab_map_trajectory_chain",),
                coordinate_scope="local",
                fusion_ref="spatial_odometry_fusion_transition_outdoor_to_indoor",
                flags={"pose": True, "motion": True},
            ),
            "field_interaction_label": _field_label(
                "plaza_construction",
                label="市民广场（北侧施工）",
                label_source="realtime_context",
                priority=150,
                map_place_ref="place_civic_plaza",
                overlay_refs=("realtime_context_construction_block",),
                internal_state_ref="field_state_plaza_construction_overlay_v1",
            ),
            "conflict_candidate_required": False,
            "direct_fact_write": False,
        },
        {
            "scenario_ref": "map_place_spatial_conflict",
            "scenario_zh": "GPS/map_place 与 SLAM local evidence 不一致；生成 conflict candidate，不强行选边",
            "conflict_candidate_required": True,
            "map_place_candidate": _map_place(
                "conflict_north",
                place_ref="place_block_north",
                poi="北侧街区入口",
                category="street_block",
            ),
            "realtime_context_candidate": None,
            "event_overlay_candidate": None,
            "spatial_evidence_binding": _spatial_binding(
                "conflict_slam",
                refs=("rtab_map_graph_chain", "spatial_odometry_fusion_chain"),
                coordinate_scope="mixed",
                fusion_ref="spatial_odometry_fusion_gps_slam_conflict",
                flags={
                    "anchor": True,
                    "relocalization": True,
                    "drift": True,
                },
            ),
            "field_interaction_label": _field_label(
                "conflict_pending",
                label="北侧街区入口（位置待确认）",
                label_source="map_place",
                priority=100,
                map_place_ref="place_block_north",
                overlay_refs=("spatial_binding_conflict_slam",),
                internal_state_ref="field_state_map_place_spatial_conflict_v1",
            ),
            "conflict_candidate": {
                "conflict_candidate_id": "field_map_place_spatial_conflict_001",
                "conflict_kind": "map_place_vs_slam_local_evidence",
                "map_place_claim": "place_block_north",
                "slam_claim": "place_block_south_local_frame",
                "resolution": "defer_to_field_synthesis_v1",
                "candidate_only": True,
                "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
                "source_chain": list(_CHAIN_PREFIX + ("map_place_spatial_conflict",)),
            },
            "gps_overrides_field_identity": False,
            "slam_overrides_field_identity": False,
        },
        {
            "scenario_ref": "event_time_window_expired",
            "scenario_zh": "临时事件时间窗结束后 event_overlay 降权失效，user-facing label 回落 map_place_ref",
            "event_time_window_required": True,
            "event_overlay_expired": True,
            "map_place_candidate": _map_place(
                "market_base",
                place_ref="place_weekend_market_square",
                poi="周末集市广场",
                category="public_plaza",
            ),
            "realtime_context_candidate": None,
            "event_overlay_candidate": _event_overlay(
                "market_expired",
                event_type="market",
                base_map_place_ref="place_weekend_market_square",
                user_label="周末创意集市",
                time_window=(1_699_900_000_000, 1_699_950_000_000),
                active=False,
            ),
            "spatial_evidence_binding": _spatial_binding(
                "market_fallback",
                refs=("generic_tum_trajectory_chain",),
                coordinate_scope="global_coarse",
                fusion_ref="spatial_odometry_fusion_outdoor_gps_primary_slam_support",
                flags={"pose": True},
            ),
            "field_interaction_label": _field_label(
                "market_fallback",
                label="周末集市广场",
                label_source="map_place",
                priority=100,
                map_place_ref="place_weekend_market_square",
                overlay_refs=(),
                internal_state_ref="field_state_weekend_market_fallback_v1",
            ),
            "event_overlay_downgraded": True,
            "conflict_candidate_required": False,
        },
    )


def build_field_map_place_event_overlay_alignment_matrix_v1() -> Dict[str, Any]:
    scenarios = build_field_alignment_scenario_matrix_v1()

    profile = FieldMapPlaceAlignmentProfile(
        profile_ref=PROFILE_REF,
        field_definition_user_layer=FIELD_DEFINITION_USER_LAYER,
        field_definition_internal=FIELD_DEFINITION_INTERNAL,
        field_definition_ref=FIELD_DEFINITION_REF,
        spatial_evidence_chain_ref=SPATIAL_EVIDENCE_CHAIN_REF,
        spatial_odometry_fusion_ref=SPATIAL_ODOMETRY_FUSION_REF,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        target_entrypoint=TARGET_ENTRYPOINT,
        alignment_pipeline=FIELD_ALIGNMENT_PIPELINE,
        scenario_refs=FIELD_ALIGNMENT_SCENARIO_REFS,
        governance_rules=FIELD_ALIGNMENT_GOVERNANCE_RULES,
    )

    decision = FieldAlignmentDecision(
        decision_ref="field_alignment_decision_v1",
        profile_ref=PROFILE_REF,
        scenario_count=len(scenarios),
        map_place_field_anchor_supported=True,
        realtime_context_overlay_supported=True,
        event_overlay_supported=True,
        spatial_evidence_binding_supported=True,
        field_interaction_label_separated=True,
        conflict_candidate_required=True,
        field_synthesis_entrypoint_locked=FIELD_SYNTHESIS_ENTRYPOINT,
        real_map_api_connected=False,
        real_gps_connected=False,
        real_event_api_connected=False,
        runtime_activation_allowed=False,
        direct_action_allowed=False,
        direct_speech_allowed=False,
        direct_fact_write_allowed=False,
        final_decision=FINAL_DECISION_ALIGNMENT_READY,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "phase_id": PHASE_ID,
        "field_map_place_alignment_profile": candidate_to_dict(profile),
        "field_alignment_scenario_matrix": list(scenarios),
        "field_alignment_governance_rules": list(FIELD_ALIGNMENT_GOVERNANCE_RULES),
        "field_alignment_pipeline": list(FIELD_ALIGNMENT_PIPELINE),
        "field_alignment_decision": candidate_to_dict(decision),
        "sealed_upstream_go_artifacts": list(_UPSTREAM_GO_ARTIFACTS),
    }
