# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — dry-run cases v1."""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_interface.field_slam_interface_static_validators_v1 import (
    VALIDATOR_RULE_IDS,
    validate_slam_interface_bundle,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
    NON_EXECUTION_FLAGS,
    PHASE_ID,
    SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID,
    SLAM_EVIDENCE_PROVIDER_GOVERNANCE_NOTE,
    SLAM_EVIDENCE_PROVIDER_GOVERNANCE_NOTE_ZH,
    LocalMapCandidate,
    MapDriftCandidate,
    MotionCandidate,
    PoseCandidate,
    RelocalizationCandidate,
    SLAMHealthCandidate,
    SpatialAnchorCandidate,
    candidate_to_dict,
)

FINAL_DECISION_DRYRUN_CASES_READY = "FIELD_SLAM_INTERFACE_DRYRUN_CASES_READY_FOR_RUNNER"

_TS = "2026-06-17T15:00:00Z"
_STUB = ("slam_dryrun_stub_v1",)


@dataclass(frozen=True)
class FieldSLAMInterfaceDryRunCase:
    case_id: str
    case_name: str
    case_type: str
    case_goal: str
    pose_candidates: Tuple[PoseCandidate, ...]
    motion_candidates: Tuple[MotionCandidate, ...]
    spatial_anchor_candidates: Tuple[SpatialAnchorCandidate, ...]
    local_map_candidates: Tuple[LocalMapCandidate, ...]
    slam_health_candidates: Tuple[SLAMHealthCandidate, ...]
    map_drift_candidates: Tuple[MapDriftCandidate, ...]
    relocalization_candidates: Tuple[RelocalizationCandidate, ...]
    expected_validation_ok: bool
    expected_field_influence: Tuple[str, ...]
    expected_policy: str
    expected_notes: Tuple[str, ...]


def _policy_to_action_readiness(policy: str) -> Optional[str]:
    if policy in ("needs_more_observation", "downweight_spatial_evidence"):
        return "needs_more_observation"
    return None


def _bundle_from_case(case: FieldSLAMInterfaceDryRunCase) -> Dict[str, Any]:
    poses = [candidate_to_dict(p) for p in case.pose_candidates]
    motions = [candidate_to_dict(m) for m in case.motion_candidates]
    anchors = [candidate_to_dict(a) for a in case.spatial_anchor_candidates]
    local_maps = [candidate_to_dict(lm) for lm in case.local_map_candidates]
    health_states = [candidate_to_dict(h) for h in case.slam_health_candidates]
    drift_states = [candidate_to_dict(d) for d in case.map_drift_candidates]
    relocalizations = [candidate_to_dict(r) for r in case.relocalization_candidates]

    action_readiness = _policy_to_action_readiness(case.expected_policy)

    if case.case_id == "case_03_slam_tracking_degraded" and health_states:
        health_states[0] = {
            **health_states[0],
            "spatial_evidence_downweight": True,
            "field_influence_transfer_ready": True,
        }

    if case.case_id == "case_05_local_map_drift_high":
        action_readiness = "needs_more_observation"
        if health_states:
            health_states[0] = {
                **health_states[0],
                "spatial_evidence_downweight": True,
                "field_influence_transfer_ready": True,
            }

    if case.case_id == "invalid_c_tracking_lost_still_ready":
        action_readiness = "ready_for_action_decision"
        if health_states:
            health_states[0] = {
                **health_states[0],
                "degraded_reason": (),
                "spatial_evidence_downweight": False,
                "requires_needs_more_observation": False,
            }

    if case.case_id == "invalid_d_anchor_confirms_destination" and anchors:
        anchors[0] = {**anchors[0], "slam_confirm_destination": True}

    return {
        "poses": poses,
        "motions": motions,
        "anchors": anchors,
        "local_maps": local_maps,
        "health_states": health_states,
        "drift_states": drift_states,
        "relocalizations": relocalizations,
        "action_readiness": action_readiness,
    }


def bundle_from_slam_interface_case(case: FieldSLAMInterfaceDryRunCase) -> Dict[str, Any]:
    """Build validator bundle dict for a dry-run case (shared by runner and cases)."""
    return _bundle_from_case(case)


def _validate_case(case: FieldSLAMInterfaceDryRunCase) -> Tuple[bool, List[str]]:
    return validate_slam_interface_bundle(**_bundle_from_case(case))


def build_case_forward_near_obstacle() -> FieldSLAMInterfaceDryRunCase:
    motion_ref = "motion_case01"
    anchor_ref = "anchor_case01_obstacle"
    pose_ref = "pose_case01"

    return FieldSLAMInterfaceDryRunCase(
        case_id="case_01_forward_near_obstacle",
        case_name="Forward motion with near-front obstacle",
        case_type="positive",
        case_goal="Validate MotionCandidate raises FieldRisk via field synthesis without direct action or speech.",
        pose_candidates=(
            PoseCandidate(
                pose_ref=pose_ref,
                timestamp=_TS,
                frame_ref="frame_case01",
                position_delta_m=(0.42, 0.0, 0.0),
                rotation_delta_deg=(0.0, 0.0, 0.0),
                heading_delta_deg=0.0,
                pose_confidence=0.83,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref=motion_ref,
                timestamp=_TS,
                motion_state="walking_forward",
                speed_band="normal",
                heading_change="none",
                stability_level="stable",
                confidence=0.81,
                source_refs=_STUB + ("imu_fusion_001",),
            ),
        ),
        spatial_anchor_candidates=(
            SpatialAnchorCandidate(
                anchor_ref=anchor_ref,
                object_ref="obj_case01_obstacle",
                anchor_type="unknown_anchor",
                relative_position_band="front",
                stability_score=0.74,
                observed_count=3,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
        ),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref="local_map_case01",
                time_window_ms=10_000,
                anchor_refs=(anchor_ref,),
                static_structure_refs=(),
                dynamic_state_refs=("dyn_case01_obstacle",),
                pose_refs=(pose_ref,),
                confidence=0.77,
                drift_risk="low",
            ),
        ),
        slam_health_candidates=(),
        map_drift_candidates=(),
        relocalization_candidates=(),
        expected_validation_ok=True,
        expected_field_influence=("field_risk",),
        expected_policy="influence_only",
        expected_notes=(
            "Near-front anchor + walking_forward → field_risk may rise.",
            "SLAM must not directly output stop command or speech alert.",
        ),
    )


def build_case_turn_right_door_anchor_shift() -> FieldSLAMInterfaceDryRunCase:
    prev_anchor_ref = "anchor_case02_door_prev"
    curr_anchor_ref = "anchor_case02_door_curr"
    pose_ref = "pose_case02"

    return FieldSLAMInterfaceDryRunCase(
        case_id="case_02_turn_right_door_anchor_shift",
        case_name="Turn right shifts door anchor from front_right to front",
        case_type="positive",
        case_goal="Validate pose/motion support spatial anchor update without confirming destination.",
        pose_candidates=(
            PoseCandidate(
                pose_ref=pose_ref,
                timestamp=_TS,
                frame_ref="frame_case02",
                position_delta_m=(0.05, 0.0, 0.0),
                rotation_delta_deg=(0.0, 0.0, -18.0),
                heading_delta_deg=-18.0,
                pose_confidence=0.84,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_case02",
                timestamp=_TS,
                motion_state="turning_right",
                speed_band="slow",
                heading_change="moderate_right",
                stability_level="stable",
                confidence=0.85,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(
            SpatialAnchorCandidate(
                anchor_ref=prev_anchor_ref,
                object_ref="door_obj_case02",
                anchor_type="door_anchor",
                relative_position_band="front_right",
                stability_score=0.86,
                observed_count=2,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
            SpatialAnchorCandidate(
                anchor_ref=curr_anchor_ref,
                object_ref="door_obj_case02",
                anchor_type="door_anchor",
                relative_position_band="front",
                stability_score=0.89,
                observed_count=3,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
        ),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref="local_map_case02",
                time_window_ms=12_000,
                anchor_refs=(curr_anchor_ref,),
                static_structure_refs=("struct_case02_door",),
                dynamic_state_refs=(),
                pose_refs=(pose_ref,),
                confidence=0.8,
                drift_risk="low",
            ),
        ),
        slam_health_candidates=(),
        map_drift_candidates=(),
        relocalization_candidates=(
            RelocalizationCandidate(
                relocalization_ref="reloc_case02",
                previous_anchor_refs=(prev_anchor_ref,),
                current_anchor_refs=(curr_anchor_ref,),
                match_score=0.88,
                relocalization_status="matched",
                confidence=0.86,
            ),
        ),
        expected_validation_ok=True,
        expected_field_influence=("field_structure", "field_action_logic"),
        expected_policy="influence_only",
        expected_notes=(
            "Door anchor relative position updated by turn; not a destination confirmation.",
        ),
    )


def build_case_slam_tracking_degraded() -> FieldSLAMInterfaceDryRunCase:
    pose_ref = "pose_case03"
    local_map_ref = "local_map_case03"

    return FieldSLAMInterfaceDryRunCase(
        case_id="case_03_slam_tracking_degraded",
        case_name="SLAM tracking degraded downweights spatial evidence",
        case_type="positive",
        case_goal="Validate SLAMHealthCandidate reduces spatial evidence weight without bypassing field synthesis.",
        pose_candidates=(
            PoseCandidate(
                pose_ref=pose_ref,
                timestamp=_TS,
                frame_ref="frame_case03",
                position_delta_m=(0.12, 0.01, 0.0),
                rotation_delta_deg=(0.0, 0.0, 1.0),
                heading_delta_deg=1.0,
                pose_confidence=0.55,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_case03",
                timestamp=_TS,
                motion_state="walking_forward",
                speed_band="slow",
                heading_change="none",
                stability_level="unstable",
                confidence=0.54,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref=local_map_ref,
                time_window_ms=8_000,
                anchor_refs=(),
                static_structure_refs=(),
                dynamic_state_refs=(),
                pose_refs=(pose_ref,),
                confidence=0.52,
                drift_risk="medium",
            ),
        ),
        slam_health_candidates=(
            SLAMHealthCandidate(
                health_ref="health_case03",
                source_method="vio",
                tracking_status="tracking_degraded",
                feature_quality="poor",
                imu_quality="moderate",
                lighting_quality="low",
                motion_blur_level="moderate",
                confidence=0.58,
                degraded_reason=("feature_quality_low", "motion_blur"),
            ),
        ),
        map_drift_candidates=(
            MapDriftCandidate(
                drift_ref="drift_case03",
                local_map_ref=local_map_ref,
                drift_risk="medium",
                suspected_drift_source="motion_blur",
                affected_refs=(pose_ref,),
                recommended_policy="downweight_spatial_evidence",
                confidence=0.6,
            ),
        ),
        relocalization_candidates=(),
        expected_validation_ok=True,
        expected_field_influence=("field_risk", "field_attention"),
        expected_policy="downweight_spatial_evidence",
        expected_notes=(
            "Tracking degraded: pose/local map weight down; needs_more_observation path.",
        ),
    )


def build_case_elevator_relocalization() -> FieldSLAMInterfaceDryRunCase:
    prev_ref = "elevator_anchor_old"
    curr_ref = "elevator_anchor_now"

    return FieldSLAMInterfaceDryRunCase(
        case_id="case_04_elevator_relocalization",
        case_name="Elevator anchor re-identified supports field memory",
        case_type="positive",
        case_goal="Validate RelocalizationCandidate supports FieldMemory without direct action output.",
        pose_candidates=(
            PoseCandidate(
                pose_ref="pose_case04",
                timestamp=_TS,
                frame_ref="frame_case04",
                position_delta_m=(0.0, 0.0, 0.0),
                rotation_delta_deg=(0.0, 0.0, 0.0),
                heading_delta_deg=0.0,
                pose_confidence=0.82,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_case04",
                timestamp=_TS,
                motion_state="stationary",
                speed_band="stopped",
                heading_change="none",
                stability_level="stable",
                confidence=0.8,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(
            SpatialAnchorCandidate(
                anchor_ref=curr_ref,
                object_ref="elevator_obj_case04",
                anchor_type="elevator_anchor",
                relative_position_band="front_left",
                stability_score=0.9,
                observed_count=5,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
        ),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref="local_map_case04",
                time_window_ms=20_000,
                anchor_refs=(curr_ref,),
                static_structure_refs=("struct_case04_elevator",),
                dynamic_state_refs=(),
                pose_refs=("pose_case04",),
                confidence=0.79,
                drift_risk="low",
            ),
        ),
        slam_health_candidates=(
            SLAMHealthCandidate(
                health_ref="health_case04",
                source_method="vio",
                tracking_status="tracking_ok",
                feature_quality="good",
                imu_quality="good",
                lighting_quality="moderate",
                motion_blur_level="low",
                confidence=0.85,
                degraded_reason=(),
            ),
        ),
        map_drift_candidates=(),
        relocalization_candidates=(
            RelocalizationCandidate(
                relocalization_ref="reloc_case04",
                previous_anchor_refs=(prev_ref,),
                current_anchor_refs=(curr_ref,),
                match_score=0.86,
                relocalization_status="matched",
                confidence=0.87,
            ),
        ),
        expected_validation_ok=True,
        expected_field_influence=("field_memory", "field_structure"),
        expected_policy="influence_only",
        expected_notes=(
            "Same elevator anchor re-identified; must not output 'already at elevator'.",
        ),
    )


def build_case_local_map_drift_high() -> FieldSLAMInterfaceDryRunCase:
    local_map_ref = "local_map_case05"
    anchor_ref = "anchor_case05"

    return FieldSLAMInterfaceDryRunCase(
        case_id="case_05_local_map_drift_high",
        case_name="High local map drift requires more observation",
        case_type="positive",
        case_goal="Validate high drift blocks ready_for_action_decision and requires more observation.",
        pose_candidates=(
            PoseCandidate(
                pose_ref="pose_case05",
                timestamp=_TS,
                frame_ref="frame_case05",
                position_delta_m=(0.2, 0.05, 0.0),
                rotation_delta_deg=(0.0, 0.0, 3.0),
                heading_delta_deg=3.0,
                pose_confidence=0.5,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_case05",
                timestamp=_TS,
                motion_state="walking_forward",
                speed_band="slow",
                heading_change="slight_left",
                stability_level="unstable",
                confidence=0.51,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(
            SpatialAnchorCandidate(
                anchor_ref=anchor_ref,
                object_ref="obj_case05",
                anchor_type="corner_anchor",
                relative_position_band="front",
                stability_score=0.45,
                observed_count=2,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
        ),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref=local_map_ref,
                time_window_ms=6_000,
                anchor_refs=(anchor_ref,),
                static_structure_refs=(),
                dynamic_state_refs=(),
                pose_refs=("pose_case05",),
                confidence=0.48,
                drift_risk="high",
            ),
        ),
        slam_health_candidates=(
            SLAMHealthCandidate(
                health_ref="health_case05",
                source_method="vio",
                tracking_status="tracking_degraded",
                feature_quality="poor",
                imu_quality="moderate",
                lighting_quality="moderate",
                motion_blur_level="moderate",
                confidence=0.5,
                degraded_reason=("drift_detected",),
            ),
        ),
        map_drift_candidates=(
            MapDriftCandidate(
                drift_ref="drift_case05",
                local_map_ref=local_map_ref,
                drift_risk="high",
                suspected_drift_source="loop_closure_error",
                affected_refs=(anchor_ref, "pose_case05"),
                recommended_policy="needs_more_observation",
                confidence=0.62,
            ),
        ),
        relocalization_candidates=(),
        expected_validation_ok=True,
        expected_field_influence=("field_risk", "field_attention"),
        expected_policy="needs_more_observation",
        expected_notes=("High drift local map cannot support action readiness.",),
    )


def build_case_stationary_near_zone_no_escalation() -> FieldSLAMInterfaceDryRunCase:
    anchor_ref = "anchor_case06"

    return FieldSLAMInterfaceDryRunCase(
        case_id="case_06_stationary_near_zone_no_escalation",
        case_name="Stationary user with near-front anchor does not escalate to immediate_risk",
        case_type="positive",
        case_goal="Validate motion_state suppresses risk escalation when user has stopped.",
        pose_candidates=(
            PoseCandidate(
                pose_ref="pose_case06",
                timestamp=_TS,
                frame_ref="frame_case06",
                position_delta_m=(0.0, 0.0, 0.0),
                rotation_delta_deg=(0.0, 0.0, 0.0),
                heading_delta_deg=0.0,
                pose_confidence=0.86,
                source_method="imu_fusion",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_case06",
                timestamp=_TS,
                motion_state="stationary",
                speed_band="stopped",
                heading_change="none",
                stability_level="stable",
                confidence=0.88,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(
            SpatialAnchorCandidate(
                anchor_ref=anchor_ref,
                object_ref="obj_case06_near",
                anchor_type="unknown_anchor",
                relative_position_band="near",
                stability_score=0.8,
                observed_count=4,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
        ),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref="local_map_case06",
                time_window_ms=5_000,
                anchor_refs=(anchor_ref,),
                static_structure_refs=(),
                dynamic_state_refs=(),
                pose_refs=("pose_case06",),
                confidence=0.82,
                drift_risk="low",
            ),
        ),
        slam_health_candidates=(
            SLAMHealthCandidate(
                health_ref="health_case06",
                source_method="imu_fusion",
                tracking_status="tracking_ok",
                feature_quality="good",
                imu_quality="good",
                lighting_quality="good",
                motion_blur_level="none",
                confidence=0.87,
                degraded_reason=(),
            ),
        ),
        map_drift_candidates=(),
        relocalization_candidates=(),
        expected_validation_ok=True,
        expected_field_influence=("field_risk",),
        expected_policy="influence_only",
        expected_notes=(
            "Near-front risk present but stationary → must not escalate to immediate_risk via SLAM.",
        ),
    )


def build_invalid_case_slam_direct_speech() -> FieldSLAMInterfaceDryRunCase:
    return FieldSLAMInterfaceDryRunCase(
        case_id="invalid_a_slam_direct_speech",
        case_name="Invalid: SLAM direct speech",
        case_type="invalid",
        case_goal="Reject slam_direct_speech forbidden policy.",
        pose_candidates=(),
        motion_candidates=(),
        spatial_anchor_candidates=(),
        local_map_candidates=(),
        slam_health_candidates=(),
        map_drift_candidates=(
            MapDriftCandidate(
                drift_ref="drift_invalid_a",
                local_map_ref="local_map_invalid_a",
                drift_risk="low",
                suspected_drift_source="unknown",
                affected_refs=(),
                recommended_policy="slam_direct_speech",
                confidence=0.7,
            ),
        ),
        relocalization_candidates=(),
        expected_validation_ok=False,
        expected_field_influence=(),
        expected_policy="slam_direct_speech",
        expected_notes=("recommended_policy_forbidden:slam_direct_speech",),
    )


def build_invalid_case_slam_direct_fact_write() -> FieldSLAMInterfaceDryRunCase:
    return FieldSLAMInterfaceDryRunCase(
        case_id="invalid_b_slam_direct_fact_write",
        case_name="Invalid: SLAM direct fact layer map write",
        case_type="invalid",
        case_goal="Reject slam_direct_fact_write / slam_override_map forbidden policies.",
        pose_candidates=(),
        motion_candidates=(),
        spatial_anchor_candidates=(),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref="local_map_invalid_b",
                time_window_ms=30_000,
                anchor_refs=("anchor_invalid_b",),
                static_structure_refs=(),
                dynamic_state_refs=(),
                pose_refs=(),
                confidence=0.6,
                drift_risk="medium",
            ),
        ),
        slam_health_candidates=(),
        map_drift_candidates=(
            MapDriftCandidate(
                drift_ref="drift_invalid_b",
                local_map_ref="local_map_invalid_b",
                drift_risk="medium",
                suspected_drift_source="feature_poor",
                affected_refs=("anchor_invalid_b",),
                recommended_policy="slam_direct_fact_write",
                confidence=0.65,
            ),
        ),
        relocalization_candidates=(),
        expected_validation_ok=False,
        expected_field_influence=(),
        expected_policy="slam_direct_fact_write",
        expected_notes=("recommended_policy_forbidden:slam_direct_fact_write",),
    )


def build_invalid_case_tracking_lost_still_ready() -> FieldSLAMInterfaceDryRunCase:
    local_map_ref = "local_map_invalid_c"

    return FieldSLAMInterfaceDryRunCase(
        case_id="invalid_c_tracking_lost_still_ready",
        case_name="Invalid: tracking_lost with high drift still ready for action",
        case_type="invalid",
        case_goal="Reject tracking_lost + high drift local map used with ready_for_action_decision.",
        pose_candidates=(
            PoseCandidate(
                pose_ref="pose_invalid_c",
                timestamp=_TS,
                frame_ref="frame_invalid_c",
                position_delta_m=(0.1, 0.0, 0.0),
                rotation_delta_deg=(0.0, 0.0, 0.0),
                heading_delta_deg=0.0,
                pose_confidence=0.38,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_invalid_c",
                timestamp=_TS,
                motion_state="unstable_motion",
                speed_band="slow",
                heading_change="none",
                stability_level="very_unstable",
                confidence=0.36,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(),
        local_map_candidates=(
            LocalMapCandidate(
                local_map_ref=local_map_ref,
                time_window_ms=10_000,
                anchor_refs=("anchor_invalid_c",),
                static_structure_refs=(),
                dynamic_state_refs=(),
                pose_refs=("pose_invalid_c",),
                confidence=0.4,
                drift_risk="high",
            ),
        ),
        slam_health_candidates=(
            SLAMHealthCandidate(
                health_ref="health_invalid_c",
                source_method="vio",
                tracking_status="tracking_lost",
                feature_quality="insufficient",
                imu_quality="moderate",
                lighting_quality="very_low",
                motion_blur_level="high",
                confidence=0.35,
                degraded_reason=("tracking_lost",),
            ),
        ),
        map_drift_candidates=(
            MapDriftCandidate(
                drift_ref="drift_invalid_c",
                local_map_ref=local_map_ref,
                drift_risk="high",
                suspected_drift_source="tracking_lost",
                affected_refs=("anchor_invalid_c",),
                recommended_policy="use_normally",
                confidence=0.45,
            ),
        ),
        relocalization_candidates=(),
        expected_validation_ok=False,
        expected_field_influence=(),
        expected_policy="use_normally",
        expected_notes=(
            "tracking_lost_requires_downweight_or_needs_more_observation_signal",
            "local_map_0:high_drift_risk_not_ready_for_action_decision",
        ),
    )


def build_invalid_case_anchor_confirms_destination() -> FieldSLAMInterfaceDryRunCase:
    return FieldSLAMInterfaceDryRunCase(
        case_id="invalid_d_anchor_confirms_destination",
        case_name="Invalid: anchor directly confirms destination",
        case_type="invalid",
        case_goal="Reject SpatialAnchorCandidate directly confirming destination.",
        pose_candidates=(
            PoseCandidate(
                pose_ref="pose_invalid_d",
                timestamp=_TS,
                frame_ref="frame_invalid_d",
                position_delta_m=(0.0, 0.0, 0.0),
                rotation_delta_deg=(0.0, 0.0, 0.0),
                heading_delta_deg=0.0,
                pose_confidence=0.9,
                source_method="vio",
                source_refs=_STUB,
            ),
        ),
        motion_candidates=(
            MotionCandidate(
                motion_ref="motion_invalid_d",
                timestamp=_TS,
                motion_state="stationary",
                speed_band="stopped",
                heading_change="none",
                stability_level="stable",
                confidence=0.88,
                source_refs=_STUB,
            ),
        ),
        spatial_anchor_candidates=(
            SpatialAnchorCandidate(
                anchor_ref="anchor_invalid_d",
                object_ref="exit_obj_invalid_d",
                anchor_type="exit_anchor",
                relative_position_band="front",
                stability_score=0.92,
                observed_count=6,
                last_seen_at=_TS,
                source_refs=_STUB,
            ),
        ),
        local_map_candidates=(),
        slam_health_candidates=(),
        map_drift_candidates=(
            MapDriftCandidate(
                drift_ref="drift_invalid_d",
                local_map_ref="local_map_invalid_d",
                drift_risk="low",
                suspected_drift_source="unknown",
                affected_refs=("anchor_invalid_d",),
                recommended_policy="slam_confirm_destination",
                confidence=0.75,
            ),
        ),
        relocalization_candidates=(),
        expected_validation_ok=False,
        expected_field_influence=(),
        expected_policy="slam_confirm_destination",
        expected_notes=(
            "slam_anchor_destination_confirmation_not_allowed:slam_confirm_destination",
        ),
    )


def build_positive_slam_interface_cases_v1() -> Tuple[FieldSLAMInterfaceDryRunCase, ...]:
    return (
        build_case_forward_near_obstacle(),
        build_case_turn_right_door_anchor_shift(),
        build_case_slam_tracking_degraded(),
        build_case_elevator_relocalization(),
        build_case_local_map_drift_high(),
        build_case_stationary_near_zone_no_escalation(),
    )


def build_invalid_slam_interface_cases_v1() -> Tuple[FieldSLAMInterfaceDryRunCase, ...]:
    return (
        build_invalid_case_slam_direct_speech(),
        build_invalid_case_slam_direct_fact_write(),
        build_invalid_case_tracking_lost_still_ready(),
        build_invalid_case_anchor_confirms_destination(),
    )


def build_all_slam_interface_cases_v1() -> Tuple[FieldSLAMInterfaceDryRunCase, ...]:
    return build_positive_slam_interface_cases_v1() + build_invalid_slam_interface_cases_v1()


def validate_slam_interface_case_ids_unique(
    cases: Tuple[FieldSLAMInterfaceDryRunCase, ...] | None = None,
) -> Tuple[bool, Tuple[str, ...]]:
    cases = cases or build_all_slam_interface_cases_v1()
    seen: Dict[str, int] = {}
    duplicates: List[str] = []
    for case in cases:
        seen[case.case_id] = seen.get(case.case_id, 0) + 1
    for case_id, count in seen.items():
        if count > 1:
            duplicates.append(case_id)
    return len(duplicates) == 0, tuple(duplicates)


def _check_cases(
    cases: Tuple[FieldSLAMInterfaceDryRunCase, ...],
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
    return ok_count, len(cases) - ok_count, fail_mismatches


def summarize_slam_interface_dryrun_cases_v1() -> Dict[str, Any]:
    positive = build_positive_slam_interface_cases_v1()
    invalid = build_invalid_slam_interface_cases_v1()
    all_cases = build_all_slam_interface_cases_v1()

    unique_ok, duplicates = validate_slam_interface_case_ids_unique(all_cases)
    pos_ok, _, pos_mismatches = _check_cases(positive, expect_valid=True)
    inv_ok, _, inv_mismatches = _check_cases(invalid, expect_valid=False)

    sample_positive_ok = False
    sample_invalid_rejected = False
    if positive:
        sample_positive_ok, _ = _validate_case(positive[0])
    if invalid:
        invalid_ok, _ = _validate_case(invalid[0])
        sample_invalid_rejected = not invalid_ok

    ready = (
        len(positive) == 6
        and len(invalid) == 4
        and unique_ok
        and pos_ok == len(positive)
        and inv_ok == len(invalid)
        and not pos_mismatches
        and not inv_mismatches
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 2 Dry-run Cases",
        "governance_id": SLAM_EVIDENCE_PROVIDER_GOVERNANCE_ID,
        "slam_evidence_provider_governance_note": SLAM_EVIDENCE_PROVIDER_GOVERNANCE_NOTE,
        "slam_evidence_provider_governance_note_zh": SLAM_EVIDENCE_PROVIDER_GOVERNANCE_NOTE_ZH,
        "positive_case_count": len(positive),
        "invalid_case_count": len(invalid),
        "case_count": len(all_cases),
        "positive_case_ids": tuple(c.case_id for c in positive),
        "invalid_case_ids": tuple(c.case_id for c in invalid),
        "case_ids_unique": unique_ok,
        "duplicate_case_ids": duplicates,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "no_runtime_slam": NON_EXECUTION_FLAGS.get("no_slam_execution") is True,
        "no_camera": NON_EXECUTION_FLAGS.get("no_camera_runtime") is True,
        "no_model": NON_EXECUTION_FLAGS.get("no_model_execution") is True,
        "no_speech_gate": NON_EXECUTION_FLAGS.get("no_speech_output") is True,
        "slam_cases_ok": pos_ok,
        "slam_invalid_cases_ok": inv_ok,
        "slam_case_ids_unique_ok": unique_ok,
        "sample_positive_validate_ok": sample_positive_ok,
        "sample_invalid_rejected_ok": sample_invalid_rejected,
        "positive_validation_mismatches": pos_mismatches,
        "invalid_validation_mismatches": inv_mismatches,
        "final_decision": (
            FINAL_DECISION_DRYRUN_CASES_READY if ready else "FIELD_SLAM_INTERFACE_DRYRUN_CASES_NOT_READY"
        ),
    }


def main() -> int:
    summary = summarize_slam_interface_dryrun_cases_v1()
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["final_decision"] == FINAL_DECISION_DRYRUN_CASES_READY else 1


if __name__ == "__main__":
    raise SystemExit(main())
