# -*- coding: utf-8 -*-
"""Field SLAM Interface Contract — registry v1."""

from __future__ import annotations

from typing import Dict, FrozenSet, List, Tuple

REGISTRY_ID = "field_slam_interface_registry_v1"

SLAM_SOURCE_METHODS: Tuple[str, ...] = (
    "vio",
    "visual_odometry",
    "imu_fusion",
    "rgbd_slam",
    "monocular_vio",
    "stereo_vio",
    "unknown",
)

MOTION_STATES: Tuple[str, ...] = (
    "stationary",
    "walking_forward",
    "turning_left",
    "turning_right",
    "backward_motion",
    "unstable_motion",
    "unknown",
)

SPEED_BANDS: Tuple[str, ...] = (
    "stopped",
    "slow",
    "normal",
    "fast",
    "unknown",
)

HEADING_CHANGES: Tuple[str, ...] = (
    "none",
    "slight_left",
    "moderate_left",
    "sharp_left",
    "slight_right",
    "moderate_right",
    "sharp_right",
    "reversing",
    "unknown",
)

STABILITY_LEVELS: Tuple[str, ...] = (
    "stable",
    "moderately_stable",
    "unstable",
    "very_unstable",
    "unknown",
)

ANCHOR_TYPES: Tuple[str, ...] = (
    "door_anchor",
    "elevator_anchor",
    "exit_anchor",
    "corner_anchor",
    "crosswalk_anchor",
    "stairs_anchor",
    "handrail_anchor",
    "sign_anchor",
    "wall_anchor",
    "unknown_anchor",
)

RELATIVE_POSITION_BANDS: Tuple[str, ...] = (
    "front",
    "front_left",
    "front_right",
    "left",
    "right",
    "behind",
    "near",
    "mid",
    "far",
    "unknown",
)

DRIFT_RISK_LEVELS: Tuple[str, ...] = (
    "none",
    "low",
    "medium",
    "high",
    "unknown",
)

TRACKING_STATUSES: Tuple[str, ...] = (
    "tracking_ok",
    "tracking_degraded",
    "tracking_lost",
    "initializing",
    "unknown",
)

FEATURE_QUALITY_LEVELS: Tuple[str, ...] = (
    "good",
    "moderate",
    "poor",
    "insufficient",
    "unknown",
)

IMU_QUALITY_LEVELS: Tuple[str, ...] = (
    "good",
    "moderate",
    "poor",
    "unavailable",
    "unknown",
)

LIGHTING_QUALITY_LEVELS: Tuple[str, ...] = (
    "good",
    "moderate",
    "low",
    "very_low",
    "unknown",
)

MOTION_BLUR_LEVELS: Tuple[str, ...] = (
    "none",
    "low",
    "moderate",
    "high",
    "unknown",
)

DRIFT_POLICIES: Tuple[str, ...] = (
    "use_normally",
    "downweight_spatial_evidence",
    "request_relocalization",
    "discard_local_map",
    "needs_more_observation",
)

RELOCALIZATION_STATUSES: Tuple[str, ...] = (
    "matched",
    "partially_matched",
    "not_matched",
    "ambiguous",
    "unknown",
)

SUSPECTED_DRIFT_SOURCES: Tuple[str, ...] = (
    "feature_poor",
    "motion_blur",
    "lighting_change",
    "fast_rotation",
    "tracking_lost",
    "loop_closure_error",
    "unknown",
)

FORBIDDEN_SLAM_POLICIES: Tuple[str, ...] = (
    "slam_direct_action",
    "slam_direct_speech",
    "slam_direct_fact_write",
    "slam_override_field",
    "slam_override_map",
    "slam_confirm_destination",
)

SLAM_BYPASS_FIELD_SYNTHESIS_KEYS: Tuple[str, ...] = (
    "bypass_field_synthesis",
    "skip_field_synthesis",
    "direct_to_action",
    "direct_to_speech",
    "direct_fact_write",
    "slam_direct_action",
    "slam_direct_speech",
)

SLAM_FIELD_IDENTITY_OVERRIDE_KEYS: Tuple[str, ...] = (
    "field_type_override",
    "revised_field_type",
    "slam_derived_field_type",
    "identity_from_slam",
    "field_identity_from_slam",
)

SLAM_DESTINATION_CONFIRMATION_KEYS: Tuple[str, ...] = (
    "confirm_destination",
    "destination_confirmed",
    "slam_confirm_destination",
    "confirmed_destination",
)

SLAM_EVIDENCE_GOVERNANCE_CHAIN: Tuple[str, ...] = (
    "slam_vio_imu_output",
    "slam_evidence_candidate",
    "field_synthesis",
    "field_information",
    "spatial_action_fusion",
    "decision_candidate",
)

FORBIDDEN_SLAM_OUTPUT_PATHS: Tuple[str, ...] = (
    "slam_to_direct_action",
    "slam_to_speech",
    "slam_to_fact_write",
    "slam_to_confirmed_map",
)

HIGH_DRIFT_RISK_LEVELS: FrozenSet[str] = frozenset({"high"})
TRACKING_DEGRADED_STATUSES: FrozenSet[str] = frozenset(
    {"tracking_degraded", "tracking_lost"}
)

LOCAL_MAP_MAX_TIME_WINDOW_MS = 300_000

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "slam_source_methods": SLAM_SOURCE_METHODS,
    "motion_states": MOTION_STATES,
    "speed_bands": SPEED_BANDS,
    "heading_changes": HEADING_CHANGES,
    "stability_levels": STABILITY_LEVELS,
    "anchor_types": ANCHOR_TYPES,
    "relative_position_bands": RELATIVE_POSITION_BANDS,
    "drift_risk_levels": DRIFT_RISK_LEVELS,
    "tracking_statuses": TRACKING_STATUSES,
    "feature_quality_levels": FEATURE_QUALITY_LEVELS,
    "imu_quality_levels": IMU_QUALITY_LEVELS,
    "lighting_quality_levels": LIGHTING_QUALITY_LEVELS,
    "motion_blur_levels": MOTION_BLUR_LEVELS,
    "drift_policies": DRIFT_POLICIES,
    "relocalization_statuses": RELOCALIZATION_STATUSES,
    "suspected_drift_sources": SUSPECTED_DRIFT_SOURCES,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry_value(domain: str, value: str) -> bool:
    return is_registered(domain, value)


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    required_domains = (
        "slam_source_methods",
        "motion_states",
        "speed_bands",
        "heading_changes",
        "stability_levels",
        "anchor_types",
        "relative_position_bands",
        "drift_risk_levels",
        "tracking_statuses",
        "feature_quality_levels",
        "imu_quality_levels",
        "lighting_quality_levels",
        "motion_blur_levels",
        "drift_policies",
        "relocalization_statuses",
    )
    for domain in required_domains:
        if domain not in REGISTRY or not REGISTRY[domain]:
            issues.append(f"registry_domain_missing:{domain}")
    if len(FORBIDDEN_SLAM_POLICIES) < 6:
        issues.append("forbidden_slam_policies_incomplete")
    if len(SLAM_EVIDENCE_GOVERNANCE_CHAIN) != 6:
        issues.append("slam_evidence_governance_chain_incomplete")
    return len(issues) == 0, issues
