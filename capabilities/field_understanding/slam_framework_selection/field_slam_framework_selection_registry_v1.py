# -*- coding: utf-8 -*-
"""Field SLAM Framework Selection — registry v1."""

from __future__ import annotations

from typing import Any, Dict, FrozenSet, List, Tuple

REGISTRY_ID = "field_slam_framework_selection_registry_v1"

FRAMEWORK_GROUPS: Tuple[str, ...] = (
    "vio_pose_first",
    "visual_inertial_slam",
    "graph_rgbd_slam",
    "metric_semantic_slam",
    "metric_semantic_scene_graph",
    "embodied_scene_graph_qa",
)

FIT_LEVELS: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "not_applicable",
    "unknown",
)

PRIORITY_LEVELS: Tuple[str, ...] = (
    "p0",
    "p1",
    "p2",
    "observation",
    "deferred",
    "blocked",
)

RUNTIME_WEIGHTS: Tuple[str, ...] = (
    "light",
    "medium",
    "heavy",
    "unknown",
)

ENGINEERING_RISKS: Tuple[str, ...] = (
    "low",
    "medium",
    "high",
    "unknown",
)

LICENSE_TYPES: Tuple[str, ...] = (
    "gpl_3",
    "gpl_v3",
    "bsd",
    "bsd_2_clause",
    "bsd_conditional",
    "mit",
    "apache_2",
    "custom",
    "unknown",
)

LICENSE_RISKS: Tuple[str, ...] = (
    "low",
    "medium",
    "high",
    "unknown",
)

COMMERCIAL_MODIFICATION_RISKS: Tuple[str, ...] = (
    "low",
    "medium",
    "high",
    "unknown",
)

OPEN_SOURCE_STATUS: Tuple[str, ...] = (
    "open_source",
    "paper_with_code",
    "paper_only",
    "mixed",
    "unknown",
)

FORBIDDEN_SELECTION_POLICIES: Tuple[str, ...] = (
    "select_by_accuracy_only",
    "bypass_field_synthesis",
    "choose_full_mapping_as_p0_without_pose_need",
    "treat_scene_graph_as_runtime_slam",
    "allow_framework_direct_action",
    "mark_gpl_as_commercial_runtime_without_license_gate",
    "skip_license_gate",
)

GPL_LICENSE_TYPES: FrozenSet[str] = frozenset({"gpl_3", "gpl_v3"})

P0_EVIDENCE_FIT_LEVELS: FrozenSet[str] = frozenset({"high", "medium"})

OBSERVATION_ONLY_FRAMEWORK_REFS: FrozenSet[str] = frozenset({"grapheqa", "hydra", "kimera"})

SLAM_BACKEND_REGISTRY: Dict[str, Dict[str, Any]] = {
    "openvins": {
        "role": "technical_reference",
        "outputs": ("PoseCandidate", "MotionCandidate", "SLAMHealthCandidate"),
        "commercial_runtime_allowed": False,
    },
    "vins_fusion": {
        "role": "technical_reference",
        "outputs": ("PoseCandidate", "MotionCandidate", "SLAMHealthCandidate"),
        "commercial_runtime_allowed": False,
    },
    "orb_slam3": {
        "role": "p1_reference",
        "outputs": (
            "PoseCandidate",
            "SpatialAnchorCandidate",
            "LocalMapCandidate",
            "RelocalizationCandidate",
        ),
        "commercial_runtime_allowed": False,
    },
    "rtab_map": {
        "role": "p2_reference",
        "outputs": ("PoseCandidate", "SpatialAnchorCandidate", "LocalMapCandidate"),
        "commercial_runtime_allowed": False,
    },
    "kimera": {
        "role": "semantic_spatial_observation",
        "outputs": ("LocalMapCandidate", "SpatialAnchorCandidate", "SemanticFieldObjectCandidate"),
        "commercial_runtime_allowed": False,
    },
    "hydra": {
        "role": "semantic_spatial_observation",
        "outputs": ("FieldGraphCandidate", "SemanticMemoryMapCandidate"),
        "commercial_runtime_allowed": False,
    },
    "grapheqa": {
        "role": "observation_only",
        "outputs": (),
        "commercial_runtime_allowed": False,
    },
    "custom_luna_vio": {
        "role": "future_runtime_candidate",
        "outputs": ("PoseCandidate", "MotionCandidate", "SLAMHealthCandidate"),
        "commercial_runtime_allowed": True,
    },
}

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "framework_groups": FRAMEWORK_GROUPS,
    "fit_levels": FIT_LEVELS,
    "priority_levels": PRIORITY_LEVELS,
    "runtime_weights": RUNTIME_WEIGHTS,
    "engineering_risks": ENGINEERING_RISKS,
    "license_types": LICENSE_TYPES,
    "license_risks": LICENSE_RISKS,
    "commercial_modification_risks": COMMERCIAL_MODIFICATION_RISKS,
    "open_source_status": OPEN_SOURCE_STATUS,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    required = (
        "framework_groups",
        "fit_levels",
        "priority_levels",
        "runtime_weights",
        "engineering_risks",
        "license_types",
        "license_risks",
        "commercial_modification_risks",
        "open_source_status",
    )
    for domain in required:
        if domain not in REGISTRY or not REGISTRY[domain]:
            issues.append(f"registry_domain_missing:{domain}")
    if len(FORBIDDEN_SELECTION_POLICIES) < 7:
        issues.append("forbidden_selection_policies_incomplete")
    return len(issues) == 0, issues
