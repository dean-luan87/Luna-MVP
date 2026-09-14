# -*- coding: utf-8 -*-
"""Field Task Guidance Safety Chain Closure — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
SCOPE = "field_task_guidance_safety_chain_closure_review_only"
SOURCE_CHAIN = "field_task_guidance_safety_chain_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "第一阶段主链总 closure：SLAM 空间证据 → Field 构建 → Task 候选 → "
    "Guidance / Speech Gate / Action Safety 候选，封存 Luna 一期"
    "「第一视角环境认知测试形态」的闭合链路。"
)

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
TASK_MANAGER_ENTRYPOINT = "task_manager_v1"
GUIDANCE_ENTRYPOINT = "navigation_guidance_candidate_v1"
SPEECH_GATE_ENTRYPOINT = "speech_gate_v1"
ACTION_SAFETY_ENTRYPOINT = "action_safety_candidate_v1"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
INTERNAL_STANDARD_FORMAT = "generic_json_spatial_trace"

FINAL_DECISION_CLOSURE_GO = "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_GO"
FINAL_DECISION_CLOSURE_BLOCKED = "FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_BLOCKED"

MASTER_CHAIN_PIPELINE: Tuple[str, ...] = (
    "SLAM evidence",
    "Generic JSON Spatial Trace",
    "spatial_evidence_candidate_bundle",
    "spatial_odometry_fusion_candidate",
    "Field Synthesis",
    "Field → Task Alignment",
    "Guidance / Speech Gate / Action Safety candidate chain",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "FieldTaskGuidanceSafetyChainClosure",
    "ClosedChainStageRef",
    "ClosedChainCapabilityCoverage",
    "ClosedChainScenarioCoverage",
    "ClosedChainGovernanceCoverage",
    "FieldTaskGuidanceSafetyClosureDecision",
)

CLOSED_CHAIN_STAGE_REFS: Tuple[str, ...] = (
    "spatial_evidence_ingest_chain",
    "field_alignment_chain",
    "field_synthesis_chain",
    "field_to_task_chain",
    "task_to_guidance_chain",
    "governance_and_safety_chain",
)

SCENARIO_COVERAGE_REFS: Tuple[str, ...] = (
    "mall_find_entrance_chain_closed",
    "subway_enter_station_chain_closed",
    "stadium_concert_ticket_gate_chain_closed",
    "plaza_market_crowd_chain_closed",
    "gps_slam_conflict_chain_closed",
    "home_return_chain_closed",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001",
    "Phase-Field-Map-Place-Realtime-Event-Overlay-Alignment-v1-001",
    "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001",
    "Phase-Field-To-Task-Alignment-DryRun-v1-001",
    "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001",
    "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
    "Phase-Midplatform-Task-Manager-Controlled-Skeleton-Implementation-DryRun-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    MODEL_ADMISSION_STANDARD_REF,
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "field_is_candidate_synthesis_not_map_fact",
    "map_place_anchors_field_not_fully_defines",
    "event_overlay_may_change_label_not_map_place_ref",
    "slam_spatial_evidence_binds_local_not_field_identity",
    "gps_gnss_must_not_override_field_identity",
    "gps_slam_conflict_emits_conflict_and_blocks_action_like_guidance",
    "task_route_hint_is_not_action",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts_output",
    "action_safety_required_before_action_like_guidance",
    "all_outputs_candidate_only",
    "no_direct_action_speech_fact_write_real_navigation_live_sensor",
    "all_stages_preserve_upstream_source_refs_and_source_chain",
    "closed_upstream_phases_verified_by_final_decision_and_artifact",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "closure_review_only": True,
    "no_new_parser": True,
    "no_new_model": True,
    "no_runtime_activation": True,
    "no_real_navigation": True,
    "no_real_map_api": True,
    "no_real_gps_gnss": True,
    "no_live_sensor": True,
    "real_navigation_started": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
}


@dataclass(frozen=True)
class FieldTaskGuidanceSafetyChainClosure:
    closure_ref: str
    phase_id: str
    master_chain_pipeline: Tuple[str, ...]
    closed_chain_stage_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    field_synthesis_entrypoint: str
    task_manager_entrypoint: str
    guidance_entrypoint: str
    speech_gate_entrypoint: str
    action_safety_entrypoint: str
    interface_layer_protocol_ref: str
    governance_rules: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class ClosedChainStageRef:
    stage_ref: str
    stage_zh: str
    coverage_items: Tuple[str, ...]
    upstream_phase_refs: Tuple[str, ...]
    chain_closed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class ClosedChainCapabilityCoverage:
    coverage_ref: str
    pose_supported: bool
    motion_supported: bool
    health_supported: bool
    anchor_supported: bool
    relocalization_supported: bool
    drift_supported: bool
    spatial_odometry_fusion_supported: bool
    field_conflict_candidate_supported: bool
    field_candidate_supported: bool
    task_context_candidate_supported: bool
    task_evidence_need_candidate_supported: bool
    task_route_hint_candidate_supported: bool
    task_risk_candidate_supported: bool
    guidance_candidate_supported: bool
    speech_gate_candidate_supported: bool
    action_safety_candidate_supported: bool


@dataclass(frozen=True)
class ClosedChainScenarioCoverage:
    scenario_ref: str
    field_synthesis_case_ref: str
    field_to_task_case_ref: str
    task_to_guidance_case_ref: str
    chain_closed: bool


@dataclass(frozen=True)
class ClosedChainGovernanceCoverage:
    coverage_ref: str
    candidate_only_enforced: bool
    source_chain_preserved: bool
    gps_does_not_override_field_identity: bool
    slam_does_not_override_field_identity: bool
    event_overlay_does_not_rewrite_map_place: bool
    field_interaction_label_separated: bool
    task_route_hint_not_action: bool
    guidance_candidate_not_runtime_navigation: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_required: bool
    gps_slam_conflict_blocks_action_like_guidance: bool


@dataclass(frozen=True)
class FieldTaskGuidanceSafetyClosureDecision:
    decision_ref: str
    closure_ref: str
    closed_stage_count: int
    sealed_upstream_phases_verified: bool
    scenario_coverage_count: int
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
