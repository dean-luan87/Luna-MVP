# -*- coding: utf-8 -*-
"""Field Synthesis Map Place / Event Overlay Dry-Run — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001"
SCOPE = "field_synthesis_map_place_event_overlay_dryrun_only"
SOURCE_CHAIN = "field_synthesis_map_place_event_overlay_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "Field Synthesis dry-run：把典型场景的 candidate 输入收敛为 FieldCandidate / "
    "FieldStateCandidate / FieldInteractionLabelCandidate，验证 Field 能承接 "
    "SLAM / GPS stub / Map Place / Event Overlay / Realtime Context。不接真实 API，不触发 action。"
)

TARGET_ENTRYPOINT = "field_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
FIELD_DEFINITION_REF = (
    "map_place_plus_realtime_context_plus_event_overlay_plus_spatial_evidence"
)

FIELD_ALIGNMENT_REF = "Phase-Field-Map-Place-Realtime-Event-Overlay-Alignment-v1-001"
SPATIAL_EVIDENCE_CHAIN_REF = "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
SPATIAL_ODOMETRY_FUSION_REF = "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

FINAL_DECISION_DRYRUN_GO = "FIELD_SYNTHESIS_MAP_PLACE_REALTIME_EVENT_OVERLAY_DRYRUN_GO"
FINAL_DECISION_DRYRUN_BLOCKED = (
    "FIELD_SYNTHESIS_MAP_PLACE_REALTIME_EVENT_OVERLAY_DRYRUN_BLOCKED"
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "mall_stable_map_place_with_slam",
    "subway_station_indoor_gps_degraded",
    "stadium_concert_event_overlay",
    "plaza_temporary_market_realtime_overlay",
    "gps_slam_map_place_conflict",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_event_overlay_missing_time_window",
    "invalid_event_overlay_rewrites_map_place",
    "invalid_gps_overrides_field_identity",
    "invalid_field_synthesis_direct_action_output",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "FieldSynthesisDryRunCase",
    "FieldSynthesisInputBundle",
    "FieldSynthesisEvidenceRef",
    "FieldSynthesisDecisionCandidate",
    "FieldSynthesisDryRunTrace",
    "FieldSynthesisDryRunReviewDecision",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "map_place_anchors_field_not_fully_defines",
    "event_overlay_override_label_not_map_place_ref",
    "realtime_context_changes_field_state_only",
    "spatial_evidence_binds_local_state_not_field_identity",
    "gps_gnss_must_not_override_field_identity",
    "slam_vio_must_not_override_field_identity",
    "conflict_must_emit_field_conflict_candidate",
    "event_overlay_must_have_time_window",
    "field_interaction_label_separated_from_internal_state",
    "all_outputs_candidate_only",
    "no_action_speech_fact_write",
    "source_chain_preserved_on_all_traces",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "dryrun_only": True,
    "no_real_map_api": True,
    "no_real_gps_gnss": True,
    "no_real_event_api": True,
    "no_live_sensor": True,
    "no_runtime_activation": True,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
}


@dataclass(frozen=True)
class FieldSynthesisEvidenceRef:
    evidence_ref: str
    evidence_kind: str
    source_chain: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldSynthesisInputBundle:
    bundle_ref: str
    case_ref: str
    user_goal: str
    map_place_ref: Dict[str, Any]
    gps_gnss_stub: Dict[str, Any]
    spatial_evidence_binding: Dict[str, Any]
    realtime_context_overlay: Dict[str, Any]
    event_overlay: Dict[str, Any]
    evidence_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldSynthesisDryRunCase:
    case_ref: str
    case_kind: str
    user_goal: str
    input_bundle_ref: str
    expected_outcome: Dict[str, Any]
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldSynthesisDecisionCandidate:
    decision_ref: str
    decision_kind: str
    field_label: str
    field_state: str
    underlying_map_place_ref: str
    coordinate_scope: str
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True
    direct_action_allowed: bool = False
    direct_speech_allowed: bool = False
    direct_fact_write_allowed: bool = False


@dataclass(frozen=True)
class FieldSynthesisDryRunTrace:
    trace_ref: str
    case_ref: str
    input_bundle_ref: str
    synthesis_ok: bool
    field_candidate: Dict[str, Any]
    field_state_candidate: Dict[str, Any]
    field_interaction_label_candidate: Dict[str, Any]
    field_conflict_candidate: Dict[str, Any]
    synthesis_issues: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class FieldSynthesisDryRunReviewDecision:
    decision_ref: str
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    field_synthesis_entrypoint_locked: str
    real_map_api_connected: bool
    real_gps_connected: bool
    real_event_api_connected: bool
    runtime_activation_allowed: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
