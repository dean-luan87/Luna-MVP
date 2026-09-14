# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — static validators v1."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.field_understanding.slam_interface.field_slam_interface_registry_v1 import (
    FORBIDDEN_SLAM_POLICIES,
    HIGH_DRIFT_RISK_LEVELS,
    LOCAL_MAP_MAX_TIME_WINDOW_MS,
    SLAM_BYPASS_FIELD_SYNTHESIS_KEYS,
    SLAM_DESTINATION_CONFIRMATION_KEYS,
    SLAM_FIELD_IDENTITY_OVERRIDE_KEYS,
    TRACKING_DEGRADED_STATUSES,
    is_registered,
    validate_registry,
)
from capabilities.field_understanding.slam_interface.field_slam_interface_types_v1 import (
    FINAL_DECISION_READY_FOR_DRYRUN_CASES,
    LOCAL_MAP_CANDIDATE_FIELDS,
    MAP_DRIFT_CANDIDATE_FIELDS,
    MOTION_CANDIDATE_FIELDS,
    PHASE_ID,
    POSE_CANDIDATE_FIELDS,
    RELOCALIZATION_CANDIDATE_FIELDS,
    SLAM_HEALTH_CANDIDATE_FIELDS,
    SLAM_INTERFACE_CANDIDATE_TYPES,
    SPATIAL_ANCHOR_CANDIDATE_FIELDS,
    LocalMapCandidate,
    MapDriftCandidate,
    MotionCandidate,
    PoseCandidate,
    RelocalizationCandidate,
    SLAMHealthCandidate,
    SpatialAnchorCandidate,
    candidate_to_dict,
)

VALIDATOR_RULE_IDS: Tuple[str, ...] = (
    "rule_01_slam_candidate_only_required",
    "rule_02_slam_confidence_range",
    "rule_03_pose_source_method_and_refs",
    "rule_04_motion_state_registered",
    "rule_05_motion_no_direct_action_readiness",
    "rule_06_spatial_anchor_stability_observed",
    "rule_07_spatial_anchor_no_direct_static_fact_write",
    "rule_08_local_map_time_window_not_long_term",
    "rule_09_local_map_high_drift_not_ready_for_action",
    "rule_10_slam_health_tracking_lost_downweight",
    "rule_11_map_drift_policy_not_forbidden",
    "rule_12_relocalization_match_score_range",
    "rule_13_relocalization_matched_requires_anchors",
    "rule_14_slam_no_bypass_field_synthesis",
    "rule_15_slam_evidence_affects_dimensions_not_identity",
    "rule_16_slam_anchor_no_direct_destination_confirm",
    "rule_17_slam_health_degradation_transfer_signal",
)


def _missing_fields(data: Dict[str, Any], fields: Sequence[str]) -> List[str]:
    return [f"missing_{f}" for f in fields if f not in data]


def _confidence_ok(value: Any) -> bool:
    return isinstance(value, (int, float)) and 0.0 <= float(value) <= 1.0


def validate_slam_candidate_only(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if data.get("candidate_only") is not True:
        issues.append("candidate_only_required")
    if data.get("is_fact") is True:
        issues.append("is_fact_not_allowed")
    if data.get("fact_layer_admitted") is True:
        issues.append("fact_layer_admission_not_allowed")
    return len(issues) == 0, issues


def validate_pose_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, POSE_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("pose_confidence")):
        issues.append("pose_confidence_out_of_range")
    ok3, issues3 = validate_pose_source_method_and_refs(data)
    if not ok3:
        issues.extend(issues3)
    if data.get("source_method") and not is_registered("slam_source_methods", data["source_method"]):
        issues.append("source_method_not_registered")
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    ok15, issues15 = validate_slam_evidence_affects_dimensions_not_identity(data)
    if not ok15:
        issues.extend(issues15)
    return len(issues) == 0, issues


def validate_motion_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MOTION_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok4, issues4 = validate_motion_state_registered(data)
    if not ok4:
        issues.extend(issues4)
    ok5, issues5 = validate_motion_no_direct_action_readiness(data)
    if not ok5:
        issues.extend(issues5)
    if data.get("speed_band") and not is_registered("speed_bands", data["speed_band"]):
        issues.append("speed_band_not_registered")
    if data.get("heading_change") and not is_registered("heading_changes", data["heading_change"]):
        issues.append("heading_change_not_registered")
    if data.get("stability_level") and not is_registered("stability_levels", data["stability_level"]):
        issues.append("stability_level_not_registered")
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    return len(issues) == 0, issues


def validate_spatial_anchor_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SPATIAL_ANCHOR_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    ok6, issues6 = validate_spatial_anchor_stability_observed(data)
    if not ok6:
        issues.extend(issues6)
    ok7, issues7 = validate_spatial_anchor_no_direct_static_fact_write(data)
    if not ok7:
        issues.extend(issues7)
    ok16, issues16 = validate_slam_anchor_no_direct_destination_confirm(data)
    if not ok16:
        issues.extend(issues16)
    if data.get("anchor_type") and not is_registered("anchor_types", data["anchor_type"]):
        issues.append("anchor_type_not_registered")
    if data.get("relative_position_band") and not is_registered(
        "relative_position_bands", data["relative_position_band"]
    ):
        issues.append("relative_position_band_not_registered")
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    ok15, issues15 = validate_slam_evidence_affects_dimensions_not_identity(data)
    if not ok15:
        issues.extend(issues15)
    return len(issues) == 0, issues


def validate_local_map_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, LOCAL_MAP_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok8, issues8 = validate_local_map_time_window_not_long_term(data)
    if not ok8:
        issues.extend(issues8)
    if data.get("drift_risk") and not is_registered("drift_risk_levels", data["drift_risk"]):
        issues.append("drift_risk_not_registered")
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    ok15, issues15 = validate_slam_evidence_affects_dimensions_not_identity(data)
    if not ok15:
        issues.extend(issues15)
    return len(issues) == 0, issues


def validate_slam_health_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, SLAM_HEALTH_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    if data.get("source_method") and not is_registered("slam_source_methods", data["source_method"]):
        issues.append("source_method_not_registered")
    if data.get("tracking_status") and not is_registered("tracking_statuses", data["tracking_status"]):
        issues.append("tracking_status_not_registered")
    if data.get("feature_quality") and not is_registered("feature_quality_levels", data["feature_quality"]):
        issues.append("feature_quality_not_registered")
    if data.get("imu_quality") and not is_registered("imu_quality_levels", data["imu_quality"]):
        issues.append("imu_quality_not_registered")
    if data.get("lighting_quality") and not is_registered("lighting_quality_levels", data["lighting_quality"]):
        issues.append("lighting_quality_not_registered")
    if data.get("motion_blur_level") and not is_registered("motion_blur_levels", data["motion_blur_level"]):
        issues.append("motion_blur_level_not_registered")
    ok10, issues10 = validate_slam_health_tracking_lost_downweight(data)
    if not ok10:
        issues.extend(issues10)
    ok17, issues17 = validate_slam_health_degradation_transfer_signal(data)
    if not ok17:
        issues.extend(issues17)
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    return len(issues) == 0, issues


def validate_map_drift_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, MAP_DRIFT_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    if data.get("drift_risk") and not is_registered("drift_risk_levels", data["drift_risk"]):
        issues.append("drift_risk_not_registered")
    if data.get("suspected_drift_source") and not is_registered(
        "suspected_drift_sources", data["suspected_drift_source"]
    ):
        issues.append("suspected_drift_source_not_registered")
    ok11, issues11 = validate_map_drift_policy_not_forbidden(data)
    if not ok11:
        issues.extend(issues11)
    if data.get("recommended_policy") and not is_registered("drift_policies", data["recommended_policy"]):
        issues.append("recommended_policy_not_registered")
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    return len(issues) == 0, issues


def validate_relocalization_candidate(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = _missing_fields(data, RELOCALIZATION_CANDIDATE_FIELDS)
    ok, cand_issues = validate_slam_candidate_only(data)
    issues.extend(cand_issues)
    if not _confidence_ok(data.get("confidence")):
        issues.append("confidence_out_of_range")
    ok12, issues12 = validate_relocalization_match_score_range(data)
    if not ok12:
        issues.extend(issues12)
    ok13, issues13 = validate_relocalization_matched_requires_anchors(data)
    if not ok13:
        issues.extend(issues13)
    if data.get("relocalization_status") and not is_registered(
        "relocalization_statuses", data["relocalization_status"]
    ):
        issues.append("relocalization_status_not_registered")
    ok14, issues14 = validate_slam_no_bypass_field_synthesis(data)
    if not ok14:
        issues.extend(issues14)
    return len(issues) == 0, issues


def validate_pose_source_method_and_refs(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if not data.get("source_method"):
        issues.append("source_method_required")
    refs = data.get("source_refs") or ()
    if not refs:
        issues.append("source_refs_required")
    return len(issues) == 0, issues


def validate_motion_state_registered(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    state = data.get("motion_state")
    if not state:
        return False, ["motion_state_required"]
    if not is_registered("motion_states", state):
        return False, ["motion_state_not_registered"]
    return True, []


def validate_motion_no_direct_action_readiness(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if "action_readiness" in data:
        issues.append("motion_candidate_must_not_emit_action_readiness")
    if data.get("ready_for_action_decision") is True:
        issues.append("motion_candidate_must_not_emit_ready_for_action_decision")
    return len(issues) == 0, issues


def validate_spatial_anchor_stability_observed(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    score = data.get("stability_score")
    count = data.get("observed_count")
    if not isinstance(score, (int, float)) or not 0.0 <= float(score) <= 1.0:
        issues.append("stability_score_out_of_range")
    if not isinstance(count, int) or count < 0:
        issues.append("observed_count_invalid")
    return len(issues) == 0, issues


def validate_spatial_anchor_no_direct_static_fact_write(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if data.get("direct_static_fact_write") is True:
        issues.append("spatial_anchor_direct_static_fact_write_not_allowed")
    if data.get("static_field_structure_confirmed") is True:
        issues.append("spatial_anchor_static_field_structure_confirmed_not_allowed")
    if data.get("written_to_fact_layer") is True:
        issues.append("spatial_anchor_written_to_fact_layer_not_allowed")
    return len(issues) == 0, issues


def validate_local_map_time_window_not_long_term(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    window = data.get("time_window_ms")
    if not isinstance(window, int) or window <= 0:
        issues.append("time_window_ms_required_positive")
    elif window > LOCAL_MAP_MAX_TIME_WINDOW_MS:
        issues.append("time_window_ms_exceeds_local_map_limit")
    if data.get("long_term_map") is True:
        issues.append("local_map_long_term_map_not_allowed")
    if data.get("is_persistent_map") is True:
        issues.append("local_map_persistent_map_not_allowed")
    if data.get("confirmed_map") is True:
        issues.append("local_map_confirmed_map_not_allowed")
    return len(issues) == 0, issues


def validate_local_map_high_drift_not_ready_for_action(
    local_maps: Sequence[Dict[str, Any]],
    *,
    action_readiness: Optional[str] = None,
) -> Tuple[bool, List[str]]:
    if action_readiness != "ready_for_action_decision":
        return True, []
    issues: List[str] = []
    for idx, item in enumerate(local_maps):
        if item.get("drift_risk") in HIGH_DRIFT_RISK_LEVELS:
            issues.append(f"local_map_{idx}:high_drift_risk_not_ready_for_action_decision")
    return len(issues) == 0, issues


def validate_slam_health_tracking_lost_downweight(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    status = data.get("tracking_status")
    if status != "tracking_lost":
        return True, []
    issues: List[str] = []
    if not (data.get("degraded_reason") or ()):
        issues.append("tracking_lost_requires_degraded_reason")
    if data.get("spatial_evidence_downweight") is not True and data.get(
        "requires_needs_more_observation"
    ) is not True:
        issues.append("tracking_lost_requires_downweight_or_needs_more_observation_signal")
    return len(issues) == 0, issues


def validate_map_drift_policy_not_forbidden(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    policy = data.get("recommended_policy")
    if policy in FORBIDDEN_SLAM_POLICIES:
        return False, [f"recommended_policy_forbidden:{policy}"]
    return True, []


def validate_relocalization_match_score_range(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if not _confidence_ok(data.get("match_score")):
        return False, ["match_score_out_of_range"]
    return True, []


def validate_relocalization_matched_requires_anchors(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    if data.get("relocalization_status") != "matched":
        return True, []
    issues: List[str] = []
    if not (data.get("previous_anchor_refs") or ()):
        issues.append("matched_requires_previous_anchor_refs")
    if not (data.get("current_anchor_refs") or ()):
        issues.append("matched_requires_current_anchor_refs")
    return len(issues) == 0, issues


def validate_slam_no_bypass_field_synthesis(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in SLAM_BYPASS_FIELD_SYNTHESIS_KEYS:
        if data.get(key) is True:
            issues.append(f"slam_bypass_field_synthesis_not_allowed:{key}")
    policy = data.get("recommended_policy") or data.get("slam_policy")
    if policy in FORBIDDEN_SLAM_POLICIES:
        issues.append(f"slam_policy_forbidden:{policy}")
    return len(issues) == 0, issues


def validate_slam_evidence_affects_dimensions_not_identity(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in SLAM_FIELD_IDENTITY_OVERRIDE_KEYS:
        if data.get(key):
            issues.append(f"slam_field_identity_override_not_allowed:{key}")
    return len(issues) == 0, issues


def validate_slam_anchor_no_direct_destination_confirm(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    for key in SLAM_DESTINATION_CONFIRMATION_KEYS:
        if data.get(key) is True:
            issues.append(f"slam_anchor_destination_confirmation_not_allowed:{key}")
    return len(issues) == 0, issues


def validate_slam_health_degradation_transfer_signal(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    status = data.get("tracking_status")
    if status not in TRACKING_DEGRADED_STATUSES:
        return True, []
    issues: List[str] = []
    if not (data.get("degraded_reason") or ()):
        issues.append("tracking_degraded_requires_degraded_reason")
    transfer_ok = (
        data.get("spatial_evidence_downweight") is True
        or data.get("requires_needs_more_observation") is True
        or data.get("field_influence_transfer_ready") is True
    )
    if not transfer_ok:
        issues.append("tracking_degraded_requires_transfer_signal")
    return len(issues) == 0, issues


def validate_slam_interface_bundle(
    *,
    poses: Sequence[Dict[str, Any]] = (),
    motions: Sequence[Dict[str, Any]] = (),
    anchors: Sequence[Dict[str, Any]] = (),
    local_maps: Sequence[Dict[str, Any]] = (),
    health_states: Sequence[Dict[str, Any]] = (),
    drift_states: Sequence[Dict[str, Any]] = (),
    relocalizations: Sequence[Dict[str, Any]] = (),
    action_readiness: Optional[str] = None,
) -> Tuple[bool, List[str]]:
    issues: List[str] = []
    validators: List[Tuple[str, Tuple[bool, List[str]]]] = []
    for idx, item in enumerate(poses):
        validators.append((f"pose_{idx}", validate_pose_candidate(item)))
    for idx, item in enumerate(motions):
        validators.append((f"motion_{idx}", validate_motion_candidate(item)))
    for idx, item in enumerate(anchors):
        validators.append((f"anchor_{idx}", validate_spatial_anchor_candidate(item)))
    for idx, item in enumerate(local_maps):
        validators.append((f"local_map_{idx}", validate_local_map_candidate(item)))
    for idx, item in enumerate(health_states):
        validators.append((f"health_{idx}", validate_slam_health_candidate(item)))
    for idx, item in enumerate(drift_states):
        validators.append((f"drift_{idx}", validate_map_drift_candidate(item)))
    for idx, item in enumerate(relocalizations):
        validators.append((f"relocalization_{idx}", validate_relocalization_candidate(item)))

    ok9, issues9 = validate_local_map_high_drift_not_ready_for_action(
        local_maps, action_readiness=action_readiness
    )
    if not ok9:
        issues.extend(issues9)

    for label, (ok, item_issues) in validators:
        if not ok:
            issues.extend([f"{label}:{i}" for i in item_issues])
    return len(issues) == 0, issues


def build_sample_slam_interface_bundle_v1() -> Dict[str, Any]:
    pose = PoseCandidate(
        pose_ref="pose_sample_001",
        timestamp="2026-06-17T14:00:00Z",
        frame_ref="frame_001",
        position_delta_m=(0.35, 0.02, 0.0),
        rotation_delta_deg=(0.0, 0.0, 2.5),
        heading_delta_deg=2.5,
        pose_confidence=0.82,
        source_method="vio",
        source_refs=("vio_track_001",),
    )
    motion = MotionCandidate(
        motion_ref="motion_sample_001",
        timestamp="2026-06-17T14:00:00Z",
        motion_state="walking_forward",
        speed_band="slow",
        heading_change="slight_right",
        stability_level="stable",
        confidence=0.79,
        source_refs=("imu_fusion_001", "vio_track_001"),
    )
    anchor = SpatialAnchorCandidate(
        anchor_ref="anchor_door_001",
        object_ref="door_obj_001",
        anchor_type="door_anchor",
        relative_position_band="front_right",
        stability_score=0.88,
        observed_count=4,
        last_seen_at="2026-06-17T14:00:00Z",
        source_refs=("slam_anchor_track_001",),
    )
    local_map = LocalMapCandidate(
        local_map_ref="local_map_001",
        time_window_ms=15_000,
        anchor_refs=("anchor_door_001",),
        static_structure_refs=("struct_door_001",),
        dynamic_state_refs=(),
        pose_refs=("pose_sample_001",),
        confidence=0.76,
        drift_risk="low",
    )
    health = SLAMHealthCandidate(
        health_ref="health_001",
        source_method="vio",
        tracking_status="tracking_ok",
        feature_quality="good",
        imu_quality="good",
        lighting_quality="moderate",
        motion_blur_level="low",
        confidence=0.84,
        degraded_reason=(),
    )
    drift = MapDriftCandidate(
        drift_ref="drift_001",
        local_map_ref="local_map_001",
        drift_risk="low",
        suspected_drift_source="unknown",
        affected_refs=(),
        recommended_policy="use_normally",
        confidence=0.71,
    )
    relocalization = RelocalizationCandidate(
        relocalization_ref="reloc_001",
        previous_anchor_refs=("anchor_door_001",),
        current_anchor_refs=("anchor_door_001",),
        match_score=0.91,
        relocalization_status="matched",
        confidence=0.89,
    )
    return {
        "poses": [candidate_to_dict(pose)],
        "motions": [candidate_to_dict(motion)],
        "anchors": [candidate_to_dict(anchor)],
        "local_maps": [candidate_to_dict(local_map)],
        "health_states": [candidate_to_dict(health)],
        "drift_states": [candidate_to_dict(drift)],
        "relocalizations": [candidate_to_dict(relocalization)],
        "action_readiness": "needs_more_observation",
    }


def build_forbidden_policy_bundle_v1() -> Dict[str, Any]:
    drift = candidate_to_dict(
        MapDriftCandidate(
            drift_ref="drift_forbidden_001",
            local_map_ref="local_map_forbidden_001",
            drift_risk="high",
            suspected_drift_source="tracking_lost",
            affected_refs=("anchor_door_001",),
            recommended_policy="slam_direct_action",
            confidence=0.55,
        )
    )
    return {
        "poses": [],
        "motions": [],
        "anchors": [],
        "local_maps": [],
        "health_states": [],
        "drift_states": [drift],
        "relocalizations": [],
    }


def validate_dataclass_instance(obj: Any) -> Tuple[bool, List[str]]:
    data = candidate_to_dict(obj)
    dispatch = {
        "PoseCandidate": validate_pose_candidate,
        "MotionCandidate": validate_motion_candidate,
        "SpatialAnchorCandidate": validate_spatial_anchor_candidate,
        "LocalMapCandidate": validate_local_map_candidate,
        "SLAMHealthCandidate": validate_slam_health_candidate,
        "MapDriftCandidate": validate_map_drift_candidate,
        "RelocalizationCandidate": validate_relocalization_candidate,
    }
    fn = dispatch.get(type(obj).__name__)
    if fn is None:
        return False, ["unknown_slam_interface_candidate_type"]
    return fn(data)


def summarize_step1_baseline_v1() -> Dict[str, Any]:
    registry_ok, registry_issues = validate_registry()
    sample = build_sample_slam_interface_bundle_v1()
    sample_ok, sample_issues = validate_slam_interface_bundle(**sample)
    forbidden = build_forbidden_policy_bundle_v1()
    forbidden_ok, forbidden_issues = validate_slam_interface_bundle(**forbidden)
    forbidden_policy_rejected = (not forbidden_ok) and any(
        "recommended_policy_forbidden" in i or "slam_policy_forbidden" in i
        for i in forbidden_issues
    )

    import_ok = True
    try:
        dataclass_count = len(SLAM_INTERFACE_CANDIDATE_TYPES)
    except Exception:
        import_ok = False
        dataclass_count = 0

    ready = (
        import_ok
        and dataclass_count == 7
        and registry_ok
        and len(VALIDATOR_RULE_IDS) == 17
        and sample_ok
        and forbidden_policy_rejected
    )

    return {
        "phase_id": PHASE_ID,
        "step": "Step 1 Types / Registry / Validators",
        "import_ok": import_ok,
        "dataclass_count": dataclass_count,
        "registry_ok": registry_ok,
        "registry_issues": registry_issues,
        "validator_rules": len(VALIDATOR_RULE_IDS),
        "validator_rule_ids": list(VALIDATOR_RULE_IDS),
        "sample_bundle_ok": sample_ok,
        "sample_bundle_issues": sample_issues,
        "forbidden_policy_rejected": forbidden_policy_rejected,
        "forbidden_policy_issues": forbidden_issues,
        "final_decision": (
            FINAL_DECISION_READY_FOR_DRYRUN_CASES if ready else "FIELD_SLAM_INTERFACE_CONTRACT_STEP1_BLOCKED"
        ),
    }


def main() -> int:
    summary = summarize_step1_baseline_v1()
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["final_decision"] == FINAL_DECISION_READY_FOR_DRYRUN_CASES else 1


if __name__ == "__main__":
    raise SystemExit(main())
