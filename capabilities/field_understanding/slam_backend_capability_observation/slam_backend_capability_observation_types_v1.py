# -*- coding: utf-8 -*-
"""SLAM Backend Capability Observation — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-SLAM-Backend-Capability-Observation-v1-001"
SCOPE = "slam_backend_capability_observation_matrix_only"
SOURCE_CHAIN = "slam_backend_capability_observation_v1"

OBSERVATION_PRINCIPLE_EN = (
    "Observe real SLAM backend capabilities, inputs, outputs, dependencies, license, "
    "and Luna adapter value before committing to any offline parser. "
    "This phase does not run third-party SLAM, connect camera/IMU/ROS, or implement parsers."
)
OBSERVATION_PRINCIPLE_ZH = (
    "在决定 offline parser 之前，先观察真实 SLAM 后端能力、输入输出、依赖、license "
    "与 Luna 适配价值。本阶段不运行第三方 SLAM、不接 camera/IMU/ROS、不实现 parser。"
)

MODEL_ID = "sample_slam_spatial_evidence_model"
MODEL_FAMILY = "slam"
DOMAIN_ID = "spatial_evidence"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
ADAPTER_PROFILE_REF = "slam_spatial_evidence_adapter"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"

MODEL_MANAGEMENT_CHAIN: Tuple[str, ...] = (
    "Model Management Protocol",
    "sample_slam_spatial_evidence_model",
    "slam_backend_capability_observation",
    "input_output_license_dependency_offline_export_candidate_mapping_matrix",
    "parser_decision",
)

FINAL_DECISION_READY_FOR_OFFLINE_PARSER_DECISION = (
    "SLAM_BACKEND_CAPABILITY_OBSERVATION_READY_FOR_OFFLINE_PARSER_DECISION"
)
FINAL_DECISION_REVIEW_BLOCKED = "SLAM_BACKEND_CAPABILITY_OBSERVATION_REVIEW_BLOCKED"
FINAL_DECISION_HANDOFF_READY = (
    "SLAM_BACKEND_CAPABILITY_OBSERVATION_HANDOFF_READY_FOR_JSON_PARSER"
)
NEXT_PHASE_GENERIC_JSON_PARSER = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"

OBSERVATION_BACKEND_REFS: Tuple[str, ...] = (
    "openvins",
    "orb_slam3",
    "rtab_map",
    "kimera",
    "hydra",
    "generic_trajectory_json_trace",
)

GPL_TECHNICAL_REFERENCE_ONLY_BACKENDS: Tuple[str, ...] = (
    "openvins",
    "orb_slam3",
)

LUNA_CANDIDATE_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
    "FieldGraphCandidate",
    "SemanticFieldObjectCandidate",
)

CANDIDATE_FIT_LEVELS: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "not_applicable",
    "unknown",
)

OFFLINE_TRIAL_FEASIBILITY_LEVELS: Tuple[str, ...] = (
    "high",
    "medium",
    "low",
    "not_applicable",
)

PARSER_PATH_PRIORITIES: Tuple[str, ...] = (
    "first_priority_offline_parser",
    "second_priority_trajectory_subset",
    "third_priority_offline_export",
    "fourth_priority_scene_graph_observation",
    "technical_reference_only",
    "deferred",
)

OBSERVATION_ENTRY_FIELDS: Tuple[str, ...] = (
    "observation_ref",
    "backend_ref",
    "backend_name",
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
    "source_refs",
    "observation_notes",
    "candidate_only",
)

OBSERVATION_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "trial_ref",
    "model_id",
    "model_family",
    "domain_id",
    "model_management_protocol_ref",
    "model_admission_standard_ref",
    "adapter_profile_ref",
    "output_candidate_contract_ref",
    "best_first_batch_offline_parser_backend",
    "technical_reference_only_backends",
    "generic_tum_parser_necessary",
    "generic_tum_parser_role",
    "generic_json_spatial_trace_preferred_internal_standard",
    "recommended_internal_standard_format",
    "next_phase_minimal_real_output_parser",
    "parser_priority_order",
    "observation_rationale_refs",
    "not_independent_slam_flow",
    "offline_observation_only",
    "no_runtime_activation",
    "final_decision",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "observation_matrix_only": True,
    "no_third_party_slam_runtime": True,
    "no_parser_implementation": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "no_ros_runtime": True,
    "no_provider_runtime_activation": True,
    "no_commercial_runtime_approval": True,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
}


@dataclass(frozen=True)
class SLAMBackendCapabilityObservationEntry:
    observation_ref: str
    backend_ref: str
    backend_name: str
    backend_family: str
    license_status: str
    primary_inputs: Tuple[str, ...]
    primary_outputs: Tuple[str, ...]
    output_export_options: Tuple[str, ...]
    luna_candidate_mapping: Dict[str, str]
    dependencies_runtime_requirements: Tuple[str, ...]
    offline_trial_feasibility: str
    commercial_runtime_candidate: bool
    technical_reference_only: bool
    recommended_parser_path: str
    source_refs: Tuple[str, ...]
    observation_notes: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMBackendCapabilityObservationDecision:
    decision_ref: str
    trial_ref: str
    model_id: str
    model_family: str
    domain_id: str
    model_management_protocol_ref: str
    model_admission_standard_ref: str
    adapter_profile_ref: str
    output_candidate_contract_ref: str
    best_first_batch_offline_parser_backend: str
    technical_reference_only_backends: Tuple[str, ...]
    generic_tum_parser_necessary: bool
    generic_tum_parser_role: str
    generic_json_spatial_trace_preferred_internal_standard: bool
    recommended_internal_standard_format: str
    next_phase_minimal_real_output_parser: str
    parser_priority_order: Tuple[str, ...]
    observation_rationale_refs: Tuple[str, ...]
    not_independent_slam_flow: bool
    offline_observation_only: bool
    no_runtime_activation: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
