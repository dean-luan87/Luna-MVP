# -*- coding: utf-8 -*-
"""SLAM Backend Capability Observation — registry v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.field_understanding.slam_backend_capability_observation.slam_backend_capability_observation_types_v1 import (
    ADAPTER_PROFILE_REF,
    GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS,
    LUNA_CANDIDATE_TYPES,
    MODEL_ADMISSION_STANDARD_REF,
    MODEL_FAMILY,
    MODEL_ID,
    MODEL_MANAGEMENT_PROTOCOL_REF,
    OBSERVATION_BACKEND_REFS,
    OBSERVATION_ENTRY_FIELDS,
    OUTPUT_CANDIDATE_CONTRACT_REF,
)

REGISTRY_ID = "slam_backend_capability_observation_registry_v1"
TRIAL_REF = "slam_backend_capability_observation_v1"

OBSERVATION_DIMENSIONS: Tuple[str, ...] = (
    "backend_family",
    "license_status",
    "primary_inputs",
    "primary_outputs",
    "output_export_options",
    "luna_candidate_mapping",
    "dependencies_runtime_requirements",
    "offline_trial_feasibility",
    "commercial_runtime_candidate",
    "technical_reference_only",
    "recommended_parser_path",
)

BACKEND_FAMILY_BY_REF: Dict[str, str] = {
    "openvins": "vio_state_estimation",
    "orb_slam3": "visual_inertial_slam",
    "rtab_map": "graph_rgbd_slam",
    "kimera": "metric_semantic_vio_slam",
    "hydra": "metric_semantic_scene_graph",
    "generic_trajectory_json_trace": "luna_internal_fallback_format",
}

BACKEND_DISPLAY_NAME_BY_REF: Dict[str, str] = {
    "openvins": "OpenVINS",
    "orb_slam3": "ORB-SLAM3",
    "rtab_map": "RTAB-Map",
    "kimera": "Kimera",
    "hydra": "Hydra",
    "generic_trajectory_json_trace": "Generic Trajectory / JSON Trace",
}

REGISTRY: Dict[str, Tuple[str, ...]] = {
    "observation_backend_refs": OBSERVATION_BACKEND_REFS,
    "observation_dimensions": OBSERVATION_DIMENSIONS,
    "luna_candidate_types": LUNA_CANDIDATE_TYPES,
    "gpl_technical_reference_only_backends": GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS,
}

MODEL_BINDING: Dict[str, str] = {
    "model_id": MODEL_ID,
    "model_family": MODEL_FAMILY,
    "domain_id": "spatial_evidence",
    "model_management_protocol_ref": MODEL_MANAGEMENT_PROTOCOL_REF,
    "model_admission_standard_ref": MODEL_ADMISSION_STANDARD_REF,
    "adapter_profile_ref": ADAPTER_PROFILE_REF,
    "output_candidate_contract_ref": OUTPUT_CANDIDATE_CONTRACT_REF,
}


def is_registered(domain: str, value: str) -> bool:
    return value in REGISTRY.get(domain, ())


def validate_registry() -> Tuple[bool, List[str]]:
    issues: List[str] = []
    if len(OBSERVATION_BACKEND_REFS) != 6:
        issues.append("observation_backend_refs_count_not_6")
    if len(OBSERVATION_DIMENSIONS) < 11:
        issues.append("observation_dimensions_incomplete")
    if len(LUNA_CANDIDATE_TYPES) != 9:
        issues.append("luna_candidate_types_count_not_9")
    for backend_ref in GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS:
        if backend_ref not in OBSERVATION_BACKEND_REFS:
            issues.append(f"gpl_backend_not_registered:{backend_ref}")
    return len(issues) == 0, issues


def empty_luna_candidate_mapping() -> Dict[str, str]:
    return {candidate_type: "not_applicable" for candidate_type in LUNA_CANDIDATE_TYPES}


def validate_observation_entry_shape(entry: Dict[str, Any]) -> Tuple[bool, List[str]]:
    issues = [f"missing_{field}" for field in OBSERVATION_ENTRY_FIELDS if field not in entry]
    backend_ref = entry.get("backend_ref")
    if backend_ref and not is_registered("observation_backend_refs", str(backend_ref)):
        issues.append(f"backend_ref_not_registered:{backend_ref}")
    mapping = entry.get("luna_candidate_mapping") or {}
    for candidate_type in LUNA_CANDIDATE_TYPES:
        if candidate_type not in mapping:
            issues.append(f"luna_candidate_mapping_missing:{candidate_type}")
    return len(issues) == 0, issues
