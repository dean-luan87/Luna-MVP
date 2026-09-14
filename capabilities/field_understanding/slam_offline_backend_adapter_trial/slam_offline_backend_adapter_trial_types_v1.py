# -*- coding: utf-8 -*-
"""SLAM Offline Real Backend Adapter Trial — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-SLAM-Offline-Real-Backend-Adapter-Trial-v1-001"
SCOPE = "slam_offline_backend_adapter_trial_planning_only"
SOURCE_CHAIN = "slam_offline_backend_adapter_trial_v1"

TRIAL_PRINCIPLE_EN = (
    "SLAM Offline Backend Adapter Trial is a model trial under the unified Model "
    "Management Protocol, not an independent SLAM governance lifecycle. It parses "
    "offline backend output files into spatial evidence candidates without live runtime."
)
TRIAL_PRINCIPLE_ZH = (
    "SLAM 离线后端适配试验是统一模型管理协议下的模型试验，不是独立的 SLAM 治理流程。"
    "它只解析离线后端输出文件为空间证据候选，不启动实时运行时。"
)

INHERITED_TRANSLATION_PRINCIPLE_ZH = "能翻译，不等于能启用。"
INHERITED_ADMISSION_PRINCIPLE_ZH = "能准入规划，不等于 runtime enable。"
INHERITED_CANDIDATE_PRINCIPLE_ZH = (
    "能生成 spatial evidence candidate，不等于能 action / speech / fact_write。"
)

MODEL_ID = "sample_slam_spatial_evidence_model"
MODEL_FAMILY = "slam"
DOMAIN_ID = "spatial_evidence"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
ADAPTER_PROFILE_REF = "slam_spatial_evidence_adapter"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"

FINAL_DECISION_READY_FOR_CASES = (
    "SLAM_OFFLINE_BACKEND_ADAPTER_TRIAL_PLANNING_READY_FOR_CASES"
)
FINAL_DECISION_CASES_READY_FOR_RUNNER = (
    "SLAM_OFFLINE_BACKEND_ADAPTER_TRIAL_CASES_READY_FOR_RUNNER"
)
FINAL_DECISION_REVIEW_GO = "SLAM_OFFLINE_BACKEND_ADAPTER_TRIAL_REVIEW_GO"
FINAL_DECISION_REVIEW_BLOCKED = "SLAM_OFFLINE_BACKEND_ADAPTER_TRIAL_REVIEW_BLOCKED"

OFFLINE_BACKEND_FORMAT_STUBS: Tuple[str, ...] = (
    "rtab_map_export_stub",
    "kimera_export_stub",
    "hydra_scene_graph_stub",
    "orb_slam3_trajectory_stub",
    "openvins_trajectory_stub",
    "generic_tum_trajectory_stub",
    "generic_json_spatial_trace_stub",
)

GPL_TECHNICAL_REFERENCE_ONLY_STUBS: Tuple[str, ...] = (
    "orb_slam3_trajectory_stub",
    "openvins_trajectory_stub",
)

OFFLINE_INPUT_MODES: Tuple[str, ...] = (
    "offline_file",
    "recorded_dataset_export",
    "third_party_backend_export",
    "manual_fixture",
)

FORBIDDEN_RUNTIME_MODES: Tuple[str, ...] = (
    "live_camera",
    "live_imu",
    "ros_topic",
    "ros_runtime",
    "provider_runtime_activation",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "offline_trial_only": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "no_ros_runtime": True,
    "no_provider_runtime_activation": True,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
    "no_commercial_runtime_approval": True,
}

OFFLINE_SLAM_BACKEND_OUTPUT_FILE_FIELDS: Tuple[str, ...] = (
    "file_ref",
    "backend_format_stub",
    "file_kind",
    "source_backend_label",
    "source_chain",
    "offline_only",
    "live_runtime_forbidden",
    "technical_reference_only",
    "commercial_runtime_candidate",
    "candidate_only",
)

OFFLINE_SLAM_BACKEND_OUTPUT_PARSER_FIELDS: Tuple[str, ...] = (
    "parser_ref",
    "backend_format_stub",
    "parser_status",
    "supported_record_types",
    "output_record_schema_ref",
    "offline_only",
    "live_runtime_forbidden",
    "candidate_only",
)

OFFLINE_SLAM_TRIAL_INPUT_MANIFEST_FIELDS: Tuple[str, ...] = (
    "manifest_ref",
    "trial_ref",
    "model_id",
    "backend_format_stub",
    "input_files",
    "input_mode",
    "offline_only",
    "live_camera_forbidden",
    "live_imu_forbidden",
    "ros_runtime_forbidden",
    "candidate_only",
)

OFFLINE_SLAM_ADAPTER_TRIAL_CONFIG_FIELDS: Tuple[str, ...] = (
    "config_ref",
    "trial_ref",
    "model_id",
    "model_family",
    "domain_id",
    "model_management_protocol_ref",
    "model_admission_standard_ref",
    "adapter_profile_ref",
    "output_candidate_contract_ref",
    "field_synthesis_entrypoint",
    "backend_format_stub",
    "offline_only",
    "provider_runtime_activation_allowed",
    "commercial_runtime_approved",
    "candidate_only",
)

OFFLINE_SLAM_PARSED_EVIDENCE_BUNDLE_FIELDS: Tuple[str, ...] = (
    "bundle_ref",
    "trial_ref",
    "model_id",
    "source_chain",
    "field_synthesis_entrypoint",
    "output_candidate_types",
    "pose_candidates",
    "motion_candidates",
    "spatial_anchor_candidates",
    "local_map_candidates",
    "slam_health_candidates",
    "map_drift_candidates",
    "relocalization_candidates",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "candidate_only",
)

OFFLINE_SLAM_TRIAL_REVIEW_POLICY_FIELDS: Tuple[str, ...] = (
    "policy_ref",
    "trial_ref",
    "review_mode",
    "offline_parse_only",
    "adapter_mapping_required",
    "field_synthesis_entrypoint_locked",
    "provider_runtime_activation_forbidden",
    "commercial_runtime_approval_forbidden",
    "candidate_only",
)

OFFLINE_SLAM_TRIAL_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "trial_ref",
    "model_id",
    "model_family",
    "domain_id",
    "model_management_protocol_ref",
    "model_admission_standard_ref",
    "adapter_profile_ref",
    "output_candidate_contract_ref",
    "field_synthesis_entrypoint",
    "offline_backend_format_stub_count",
    "not_independent_slam_flow",
    "offline_only",
    "provider_runtime_activation_allowed",
    "commercial_runtime_approved",
    "candidate_only_enforced",
    "final_decision",
    "candidate_only",
)


@dataclass(frozen=True)
class OfflineSLAMBackendOutputFile:
    file_ref: str
    backend_format_stub: str
    file_kind: str
    source_backend_label: str
    source_chain: Tuple[str, ...]
    offline_only: bool
    live_runtime_forbidden: bool
    technical_reference_only: bool
    commercial_runtime_candidate: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class OfflineSLAMBackendOutputParser:
    parser_ref: str
    backend_format_stub: str
    parser_status: str
    supported_record_types: Tuple[str, ...]
    output_record_schema_ref: str
    offline_only: bool
    live_runtime_forbidden: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class OfflineSLAMTrialInputManifest:
    manifest_ref: str
    trial_ref: str
    model_id: str
    backend_format_stub: str
    input_files: Tuple[str, ...]
    input_mode: str
    offline_only: bool
    live_camera_forbidden: bool
    live_imu_forbidden: bool
    ros_runtime_forbidden: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class OfflineSLAMAdapterTrialConfig:
    config_ref: str
    trial_ref: str
    model_id: str
    model_family: str
    domain_id: str
    model_management_protocol_ref: str
    model_admission_standard_ref: str
    adapter_profile_ref: str
    output_candidate_contract_ref: str
    field_synthesis_entrypoint: str
    backend_format_stub: str
    offline_only: bool
    provider_runtime_activation_allowed: bool
    commercial_runtime_approved: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class OfflineSLAMParsedEvidenceBundle:
    bundle_ref: str
    trial_ref: str
    model_id: str
    source_chain: Tuple[str, ...]
    field_synthesis_entrypoint: str
    output_candidate_types: Tuple[str, ...]
    pose_candidates: Tuple[Dict[str, Any], ...]
    motion_candidates: Tuple[Dict[str, Any], ...]
    spatial_anchor_candidates: Tuple[Dict[str, Any], ...]
    local_map_candidates: Tuple[Dict[str, Any], ...]
    slam_health_candidates: Tuple[Dict[str, Any], ...]
    map_drift_candidates: Tuple[Dict[str, Any], ...]
    relocalization_candidates: Tuple[Dict[str, Any], ...]
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class OfflineSLAMTrialReviewPolicy:
    policy_ref: str
    trial_ref: str
    review_mode: str
    offline_parse_only: bool
    adapter_mapping_required: bool
    field_synthesis_entrypoint_locked: str
    provider_runtime_activation_forbidden: bool
    commercial_runtime_approval_forbidden: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class OfflineSLAMTrialPlanningDecision:
    decision_ref: str
    trial_ref: str
    model_id: str
    model_family: str
    domain_id: str
    model_management_protocol_ref: str
    model_admission_standard_ref: str
    adapter_profile_ref: str
    output_candidate_contract_ref: str
    field_synthesis_entrypoint: str
    offline_backend_format_stub_count: int
    not_independent_slam_flow: bool
    offline_only: bool
    provider_runtime_activation_allowed: bool
    commercial_runtime_approved: bool
    candidate_only_enforced: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
