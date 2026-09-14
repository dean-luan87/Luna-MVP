# -*- coding: utf-8 -*-
"""Spatial Odometry Fusion Interface — registry + planning matrix v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.spatial_odometry_fusion_interface.spatial_odometry_fusion_interface_types_v1 import (
    FIELD_SYNTHESIS_ENTRYPOINT,
    FINAL_DECISION_PLANNING_READY,
    FUSION_GOVERNANCE_RULES,
    FUSION_INTERFACE_NAME,
    FUSION_INTERFACE_REF,
    FUSION_PIPELINE,
    FUSION_SCENARIO_REFS,
    INPUT_EVIDENCE_SOURCE_REFS,
    INTERFACE_LAYER_PROTOCOL_REF,
    INTERNAL_STANDARD_FORMAT,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    PLANNING_OBJECT_TYPES,
    SOURCE_CHAIN,
    SOURCE_INTERFACE_PROFILE,
    TARGET_ENTRYPOINT,
    GPSGNSSCoarsePositionCandidate,
    MapAlignmentHintCandidate,
    RTABGraphAnchorCandidate,
    SLAMLocalOdometryCandidate,
    SpatialOdometryFusionCandidate,
    SpatialOdometryFusionInterface,
    SpatialOdometryFusionPlanningDecision,
    candidate_to_dict,
)

REGISTRY_ID = "spatial_odometry_fusion_interface_registry_v1"

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "planning_object_types": PLANNING_OBJECT_TYPES,
    "input_evidence_source_refs": INPUT_EVIDENCE_SOURCE_REFS,
    "fusion_scenario_refs": FUSION_SCENARIO_REFS,
    "fusion_governance_rules": FUSION_GOVERNANCE_RULES,
    "fusion_pipeline": FUSION_PIPELINE,
}

_CHAIN_PREFIX = (SOURCE_CHAIN, REGISTRY_ID)


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(PLANNING_OBJECT_TYPES) != 7:
        issues.append("planning_object_types_count_not_7")
    if len(INPUT_EVIDENCE_SOURCE_REFS) != 6:
        issues.append("input_evidence_source_refs_count_not_6")
    if len(FUSION_SCENARIO_REFS) != 5:
        issues.append("fusion_scenario_refs_count_not_5")
    if len(FUSION_GOVERNANCE_RULES) != 10:
        issues.append("fusion_governance_rules_count_not_10")
    return len(issues) == 0, issues


def _gps_stub_candidate(ref_suffix: str, *, coordinate_scope: str, hint: Dict[str, Any]) -> Dict[str, Any]:
    candidate = GPSGNSSCoarsePositionCandidate(
        candidate_ref=f"gps_gnss_stub_{ref_suffix}",
        source_evidence_ref="gps_gnss_coarse_position_stub",
        coordinate_scope=coordinate_scope,
        global_position_hint=hint,
        confidence=hint.get("confidence", 0.7),
        source_chain=_CHAIN_PREFIX + (f"gps_gnss_stub_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    return candidate_to_dict(candidate)


def _slam_stub_candidate(
    ref_suffix: str,
    *,
    source_evidence_ref: str,
    coordinate_scope: str,
    motion_hint: Dict[str, Any],
) -> Dict[str, Any]:
    candidate = SLAMLocalOdometryCandidate(
        candidate_ref=f"slam_local_odometry_{ref_suffix}",
        source_evidence_ref=source_evidence_ref,
        coordinate_scope=coordinate_scope,
        local_motion_hint=motion_hint,
        confidence=motion_hint.get("confidence", 0.85),
        source_chain=_CHAIN_PREFIX + (f"slam_local_odometry_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    return candidate_to_dict(candidate)


def _rtab_graph_stub_candidate(
    ref_suffix: str,
    *,
    coordinate_scope: str,
    anchor_hint: Dict[str, Any],
    drift_status: str,
    relocalization_status: str,
) -> Dict[str, Any]:
    candidate = RTABGraphAnchorCandidate(
        candidate_ref=f"rtab_graph_anchor_{ref_suffix}",
        source_evidence_ref="rtab_map_graph_export_subset",
        coordinate_scope=coordinate_scope,
        anchor_alignment_hint=anchor_hint,
        drift_status=drift_status,
        relocalization_status=relocalization_status,
        confidence=anchor_hint.get("confidence", 0.8),
        source_chain=_CHAIN_PREFIX + (f"rtab_graph_anchor_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
        restore_runtime_trust=False,
    )
    return candidate_to_dict(candidate)


def _map_alignment_hint_stub(ref_suffix: str) -> Dict[str, Any]:
    candidate = MapAlignmentHintCandidate(
        candidate_ref=f"map_alignment_hint_{ref_suffix}",
        source_evidence_ref="map_place_ref_stub",
        coordinate_scope="aligned_local",
        anchor_alignment_hint={"map_place_ref": "place_mall_entrance_a", "alignment_kind": "place_anchor"},
        global_alignment_hint="gps_gnss_link_placeholder_v1",
        gps_anchor_ref="gps_anchor_placeholder_block_7",
        map_alignment_ref="map_alignment_placeholder_session_a",
        confidence=0.72,
        source_chain=_CHAIN_PREFIX + (f"map_alignment_hint_{ref_suffix}",),
        field_synthesis_entrypoint=FIELD_SYNTHESIS_ENTRYPOINT,
    )
    return candidate_to_dict(candidate)


def _fusion_candidate(
    scenario_ref: str,
    *,
    coordinate_scope: str,
    fusion_policy: str,
    global_hint: Dict[str, Any],
    local_hint: Dict[str, Any],
    anchor_hint: Dict[str, Any],
    drift_status: str,
    relocalization_status: str,
    confidence: float,
    source_candidate_refs: Tuple[str, ...],
    conflict_emitted: bool = False,
) -> Dict[str, Any]:
    fusion_id = f"spatial_odometry_fusion_{scenario_ref}"
    payload: Dict[str, Any] = {
        "fusion_candidate_id": fusion_id,
        "coordinate_scope": coordinate_scope,
        "global_position_hint": global_hint,
        "local_motion_hint": local_hint,
        "anchor_alignment_hint": anchor_hint,
        "drift_status": drift_status,
        "relocalization_status": relocalization_status,
        "confidence": confidence,
        "source_chain": list(_CHAIN_PREFIX + (scenario_ref, fusion_id)),
        "source_candidate_refs": list(source_candidate_refs),
        "fusion_policy": fusion_policy,
        "field_synthesis_entrypoint": FIELD_SYNTHESIS_ENTRYPOINT,
        "candidate_only": True,
    }
    if conflict_emitted:
        payload["conflict_candidate_emitted"] = True
        payload["conflict_resolution"] = "defer_to_field_synthesis_v1"
    core_payload = {
        key: payload[key]
        for key in (
            "fusion_candidate_id",
            "coordinate_scope",
            "global_position_hint",
            "local_motion_hint",
            "anchor_alignment_hint",
            "drift_status",
            "relocalization_status",
            "confidence",
            "source_chain",
            "source_candidate_refs",
            "fusion_policy",
            "field_synthesis_entrypoint",
            "candidate_only",
        )
    }
    candidate = SpatialOdometryFusionCandidate(**core_payload)
    result = candidate_to_dict(candidate)
    if conflict_emitted:
        result["conflict_candidate_emitted"] = True
        result["conflict_resolution"] = "defer_to_field_synthesis_v1"
    return result


def build_fusion_scenario_matrix_v1() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "scenario_ref": "outdoor_gps_primary_slam_support",
            "scenario_zh": "室外开阔路段：GPS 主导粗定位，SLAM 只辅助局部运动",
            "coordinate_scope": "mixed",
            "fusion_policy": "gps_primary_slam_support",
            "gps_weight": "high",
            "slam_weight": "support",
            "rtab_graph_weight": "low",
            "input_evidence_refs": (
                "gps_gnss_coarse_position_stub",
                "generic_json_spatial_trace_pose_motion",
                "rtab_map_trajectory_export_subset",
            ),
            "gps_candidate": _gps_stub_candidate(
                "outdoor_primary",
                coordinate_scope="global_coarse",
                hint={
                    "lat_lon_stub": [31.2304, 121.4737],
                    "accuracy_m": 8.0,
                    "confidence": 0.88,
                    "place_context": "outdoor_arterial_road",
                },
            ),
            "slam_candidate": _slam_stub_candidate(
                "outdoor_support",
                source_evidence_ref="generic_json_spatial_trace_pose_motion",
                coordinate_scope="local",
                motion_hint={
                    "delta_translation_m": [0.12, 0.0, 0.0],
                    "tracking_state": "ok",
                    "confidence": 0.9,
                },
            ),
            "rtab_graph_candidate": None,
            "fusion_candidate": _fusion_candidate(
                "outdoor_gps_primary_slam_support",
                coordinate_scope="mixed",
                fusion_policy="gps_primary_slam_support",
                global_hint={"primary": "gps_gnss_coarse_position_stub", "weight": "high"},
                local_hint={"primary": "generic_json_spatial_trace_pose_motion", "weight": "support"},
                anchor_hint={"role": "optional_local_stabilizer"},
                drift_status="low",
                relocalization_status="not_required",
                confidence=0.86,
                source_candidate_refs=(
                    "gps_gnss_stub_outdoor_primary",
                    "slam_local_odometry_outdoor_support",
                ),
            ),
            "conflict_candidate_required": False,
            "restore_runtime_trust": False,
        },
        {
            "scenario_ref": "indoor_slam_primary_gps_degraded",
            "scenario_zh": "室内/地下：GPS 降权，SLAM/RTAB graph 主导局部场",
            "coordinate_scope": "local",
            "fusion_policy": "slam_primary_gps_degraded",
            "gps_weight": "degraded",
            "slam_weight": "high",
            "rtab_graph_weight": "high",
            "input_evidence_refs": (
                "gps_gnss_coarse_position_stub",
                "rtab_map_odometry_export_subset",
                "rtab_map_graph_export_subset",
            ),
            "gps_candidate": _gps_stub_candidate(
                "indoor_degraded",
                coordinate_scope="global_coarse",
                hint={
                    "lat_lon_stub": [31.2304, 121.4737],
                    "accuracy_m": 45.0,
                    "confidence": 0.32,
                    "degradation_reason": "indoor_gps_weak",
                },
            ),
            "slam_candidate": _slam_stub_candidate(
                "indoor_primary",
                source_evidence_ref="rtab_map_odometry_export_subset",
                coordinate_scope="local",
                motion_hint={
                    "delta_translation_m": [0.08, 0.02, 0.0],
                    "tracking_state": "ok",
                    "confidence": 0.91,
                },
            ),
            "rtab_graph_candidate": _rtab_graph_stub_candidate(
                "indoor_anchor",
                coordinate_scope="local",
                anchor_hint={"anchor_ref": "graph_node_302", "anchor_role": "adjacent_spatial_anchor"},
                drift_status="moderate",
                relocalization_status="not_required",
            ),
            "fusion_candidate": _fusion_candidate(
                "indoor_slam_primary_gps_degraded",
                coordinate_scope="local",
                fusion_policy="slam_primary_gps_degraded",
                global_hint={"primary": "gps_gnss_coarse_position_stub", "weight": "degraded"},
                local_hint={"primary": "rtab_map_odometry_export_subset", "weight": "high"},
                anchor_hint={"primary": "rtab_map_graph_export_subset", "weight": "high"},
                drift_status="moderate",
                relocalization_status="not_required",
                confidence=0.84,
                source_candidate_refs=(
                    "gps_gnss_stub_indoor_degraded",
                    "slam_local_odometry_indoor_primary",
                    "rtab_graph_anchor_indoor_anchor",
                ),
            ),
            "conflict_candidate_required": False,
            "restore_runtime_trust": False,
        },
        {
            "scenario_ref": "transition_outdoor_to_indoor",
            "scenario_zh": "室外进入商场/地铁站：GPS → SLAM/视觉锚点切换",
            "coordinate_scope": "mixed",
            "fusion_policy": "transition_gps_to_slam_anchor",
            "gps_weight": "transition_down",
            "slam_weight": "rising",
            "rtab_graph_weight": "rising",
            "input_evidence_refs": (
                "gps_gnss_coarse_position_stub",
                "rtab_map_trajectory_export_subset",
                "rtab_map_graph_export_subset",
                "map_place_ref_stub",
            ),
            "gps_candidate": _gps_stub_candidate(
                "transition_fading",
                coordinate_scope="global_coarse",
                hint={
                    "lat_lon_stub": [31.2304, 121.4737],
                    "accuracy_m": 22.0,
                    "confidence": 0.55,
                    "transition_phase": "outdoor_to_indoor_entry",
                },
            ),
            "slam_candidate": _slam_stub_candidate(
                "transition_rising",
                source_evidence_ref="rtab_map_trajectory_export_subset",
                coordinate_scope="local",
                motion_hint={
                    "delta_translation_m": [0.15, 0.0, 0.0],
                    "tracking_state": "ok",
                    "confidence": 0.87,
                },
            ),
            "rtab_graph_candidate": _rtab_graph_stub_candidate(
                "transition_anchor",
                coordinate_scope="aligned_local",
                anchor_hint={"anchor_ref": "graph_node_301", "anchor_role": "stable_spatial_anchor"},
                drift_status="low",
                relocalization_status="candidate",
            ),
            "map_alignment_hint": _map_alignment_hint_stub("transition_entry"),
            "fusion_candidate": _fusion_candidate(
                "transition_outdoor_to_indoor",
                coordinate_scope="mixed",
                fusion_policy="transition_gps_to_slam_anchor",
                global_hint={"primary": "gps_gnss_coarse_position_stub", "weight": "transition_down"},
                local_hint={"primary": "rtab_map_trajectory_export_subset", "weight": "rising"},
                anchor_hint={
                    "primary": "rtab_map_graph_export_subset",
                    "map_place_ref": "map_place_ref_stub",
                    "weight": "rising",
                },
                drift_status="low",
                relocalization_status="candidate",
                confidence=0.78,
                source_candidate_refs=(
                    "gps_gnss_stub_transition_fading",
                    "slam_local_odometry_transition_rising",
                    "rtab_graph_anchor_transition_anchor",
                    "map_alignment_hint_transition_entry",
                ),
            ),
            "conflict_candidate_required": False,
            "restore_runtime_trust": False,
        },
        {
            "scenario_ref": "gps_slam_conflict",
            "scenario_zh": "GPS 与 SLAM/RTAB graph 不一致：不直接覆盖，生成 conflict candidate",
            "coordinate_scope": "mixed",
            "fusion_policy": "conflict_defer_to_field_synthesis",
            "gps_weight": "high_but_untrusted",
            "slam_weight": "high_but_untrusted",
            "rtab_graph_weight": "medium",
            "input_evidence_refs": (
                "gps_gnss_coarse_position_stub",
                "rtab_map_graph_export_subset",
                "map_place_ref_stub",
            ),
            "gps_candidate": _gps_stub_candidate(
                "conflict_gps",
                coordinate_scope="global_coarse",
                hint={
                    "lat_lon_stub": [31.2310, 121.4745],
                    "accuracy_m": 6.0,
                    "confidence": 0.82,
                    "claimed_place": "block_north_side",
                },
            ),
            "slam_candidate": None,
            "rtab_graph_candidate": _rtab_graph_stub_candidate(
                "conflict_graph",
                coordinate_scope="aligned_local",
                anchor_hint={
                    "anchor_ref": "graph_node_303",
                    "claimed_place": "block_south_side",
                    "misalignment_m": 18.0,
                },
                drift_status="high",
                relocalization_status="candidate",
            ),
            "map_alignment_hint": _map_alignment_hint_stub("conflict_place"),
            "fusion_candidate": _fusion_candidate(
                "gps_slam_conflict",
                coordinate_scope="mixed",
                fusion_policy="conflict_defer_to_field_synthesis",
                global_hint={
                    "primary": "gps_gnss_coarse_position_stub",
                    "claimed_place": "block_north_side",
                    "weight": "high_but_untrusted",
                },
                local_hint={
                    "primary": "rtab_map_graph_export_subset",
                    "claimed_place": "block_south_side",
                    "weight": "high_but_untrusted",
                },
                anchor_hint={"misalignment_m": 18.0, "resolution": "defer_to_field_synthesis_v1"},
                drift_status="high",
                relocalization_status="candidate",
                confidence=0.45,
                source_candidate_refs=(
                    "gps_gnss_stub_conflict_gps",
                    "rtab_graph_anchor_conflict_graph",
                    "map_alignment_hint_conflict_place",
                ),
                conflict_emitted=True,
            ),
            "conflict_candidate_required": True,
            "restore_runtime_trust": False,
        },
        {
            "scenario_ref": "rtab_graph_relocalization_with_gps_hint",
            "scenario_zh": "RTAB graph 回环/重定位 + GPS 粗锚点：只生成 alignment hint，不恢复 runtime trust",
            "coordinate_scope": "aligned_local",
            "fusion_policy": "relocalization_with_gps_alignment_hint",
            "gps_weight": "hint_only",
            "slam_weight": "medium",
            "rtab_graph_weight": "high",
            "input_evidence_refs": (
                "gps_gnss_coarse_position_stub",
                "rtab_map_graph_export_subset",
                "map_place_ref_stub",
            ),
            "gps_candidate": _gps_stub_candidate(
                "reloc_gps_hint",
                coordinate_scope="global_coarse",
                hint={
                    "lat_lon_stub": [31.2304, 121.4737],
                    "accuracy_m": 12.0,
                    "confidence": 0.68,
                    "role": "coarse_anchor_hint_only",
                },
            ),
            "slam_candidate": _slam_stub_candidate(
                "reloc_motion",
                source_evidence_ref="rtab_map_odometry_export_subset",
                coordinate_scope="local",
                motion_hint={
                    "delta_translation_m": [0.05, 0.0, 0.0],
                    "tracking_state": "ok",
                    "confidence": 0.86,
                },
            ),
            "rtab_graph_candidate": _rtab_graph_stub_candidate(
                "reloc_loop_closure",
                coordinate_scope="aligned_local",
                anchor_hint={
                    "anchor_ref": "graph_node_303",
                    "edge_ref": "edge_303_301",
                    "loop_closure": True,
                },
                drift_status="moderate",
                relocalization_status="candidate",
            ),
            "map_alignment_hint": _map_alignment_hint_stub("reloc_gps"),
            "fusion_candidate": _fusion_candidate(
                "rtab_graph_relocalization_with_gps_hint",
                coordinate_scope="aligned_local",
                fusion_policy="relocalization_with_gps_alignment_hint",
                global_hint={
                    "primary": "gps_gnss_coarse_position_stub",
                    "role": "coarse_anchor_hint_only",
                    "weight": "hint_only",
                },
                local_hint={"primary": "rtab_map_odometry_export_subset", "weight": "medium"},
                anchor_hint={
                    "primary": "rtab_map_graph_export_subset",
                    "global_alignment_hint": "gps_gnss_link_placeholder_v1",
                    "restore_runtime_trust": False,
                },
                drift_status="moderate",
                relocalization_status="candidate",
                confidence=0.76,
                source_candidate_refs=(
                    "gps_gnss_stub_reloc_gps_hint",
                    "slam_local_odometry_reloc_motion",
                    "rtab_graph_anchor_reloc_loop_closure",
                    "map_alignment_hint_reloc_gps",
                ),
            ),
            "conflict_candidate_required": False,
            "restore_runtime_trust": False,
        },
    )


def build_spatial_odometry_fusion_interface_matrix_v1() -> Dict[str, Any]:
    fusion_interface = SpatialOdometryFusionInterface(
        interface_ref=FUSION_INTERFACE_REF,
        interface_name=FUSION_INTERFACE_NAME,
        interface_layer_protocol_ref=INTERFACE_LAYER_PROTOCOL_REF,
        model_management_protocol_ref=MODEL_MANAGEMENT_PROTOCOL_REF,
        source_interface_profile=SOURCE_INTERFACE_PROFILE,
        internal_standard_format=INTERNAL_STANDARD_FORMAT,
        target_entrypoint=TARGET_ENTRYPOINT,
        fusion_pipeline=FUSION_PIPELINE,
        input_evidence_source_refs=INPUT_EVIDENCE_SOURCE_REFS,
        fusion_scenario_refs=FUSION_SCENARIO_REFS,
        governance_rules=FUSION_GOVERNANCE_RULES,
    )

    scenarios = build_fusion_scenario_matrix_v1()

    planning_decision = SpatialOdometryFusionPlanningDecision(
        decision_ref="spatial_odometry_fusion_planning_decision_v1",
        interface_ref=FUSION_INTERFACE_REF,
        fusion_scenario_count=len(scenarios),
        planning_only=True,
        real_gps_connected=False,
        runtime_activation_allowed=False,
        direct_action_allowed=False,
        direct_speech_allowed=False,
        direct_fact_write_allowed=False,
        field_synthesis_entrypoint_locked=FIELD_SYNTHESIS_ENTRYPOINT,
        final_decision=FINAL_DECISION_PLANNING_READY,
    )

    return {
        "registry_id": REGISTRY_ID,
        "source_chain": SOURCE_CHAIN,
        "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
        "spatial_odometry_fusion_interface": candidate_to_dict(fusion_interface),
        "input_evidence_source_refs": list(INPUT_EVIDENCE_SOURCE_REFS),
        "fusion_scenario_matrix": list(scenarios),
        "fusion_governance_rules": list(FUSION_GOVERNANCE_RULES),
        "fusion_pipeline": list(FUSION_PIPELINE),
        "planning_decision": candidate_to_dict(planning_decision),
    }
