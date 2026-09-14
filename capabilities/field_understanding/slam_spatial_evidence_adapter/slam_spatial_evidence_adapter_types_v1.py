# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Adapter Skeleton — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-SLAM-Spatial-Evidence-Provider-Adapter-Skeleton-v1-001"
SCOPE = "slam_spatial_evidence_adapter_skeleton_planning_only"
SOURCE_CHAIN = "slam_spatial_evidence_adapter_v1"

ADAPTER_SKELETON_PRINCIPLE_EN = (
    "SLAM Spatial Evidence Adapter Skeleton translates backend-like output into Luna "
    "spatial evidence candidates; it does not activate, run, or license any real SLAM backend."
)
ADAPTER_SKELETON_PRINCIPLE_ZH = (
    "SLAM Spatial Evidence Adapter Skeleton 只负责把类似 SLAM 的输出翻译成 Luna 空间证据候选，"
    "不负责启动、运行或授权任何真实 SLAM 后端。"
)

INHERITED_TRANSLATION_PRINCIPLE_ZH = "能翻译，不等于能启用。"
INHERITED_ADMISSION_PRINCIPLE_ZH = "能准入规划，不等于 runtime enable。"
INHERITED_SKELETON_PRINCIPLE_ZH = "能定义 runtime skeleton，不等于 runtime execute。"
INHERITED_CANDIDATE_PRINCIPLE_ZH = (
    "能生成 spatial evidence candidate，不等于能 action / speech / fact_write。"
)

FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"
GENERIC_SLAM_ADAPTER_CONTRACT_REF = "generic_slam_adapter_contract_v1"

FINAL_DECISION_READY_FOR_DRYRUN_CASES = (
    "SLAM_SPATIAL_EVIDENCE_ADAPTER_SKELETON_READY_FOR_DRYRUN_CASES"
)
FINAL_DECISION_MAPPING_CASES_READY_FOR_RUNNER = (
    "SLAM_SPATIAL_EVIDENCE_ADAPTER_MAPPING_CASES_READY_FOR_RUNNER"
)
FINAL_DECISION_MAPPING_REVIEW_GO = (
    "SLAM_SPATIAL_EVIDENCE_ADAPTER_MAPPING_REVIEW_GO"
)
FINAL_DECISION_MAPPING_REVIEW_BLOCKED = (
    "SLAM_SPATIAL_EVIDENCE_ADAPTER_MAPPING_REVIEW_BLOCKED"
)

SUPPORTED_CANDIDATE_TYPES: Tuple[str, ...] = (
    "PoseCandidate",
    "MotionCandidate",
    "SpatialAnchorCandidate",
    "LocalMapCandidate",
    "SLAMHealthCandidate",
    "MapDriftCandidate",
    "RelocalizationCandidate",
)

RESERVED_CANDIDATE_TYPES: Tuple[str, ...] = (
    "SemanticFieldObjectCandidate",
    "FieldGraphCandidate",
    "SemanticMemoryMapCandidate",
)

MOCK_BACKEND_KINDS: Tuple[str, ...] = (
    "mock_vio",
    "mock_visual_slam",
    "mock_rgbd_slam",
    "mock_metric_semantic_slam",
    "mock_scene_graph",
    "mock_neural_slam",
    "unknown_mock_backend",
)

ALLOWED_INPUT_MODES: Tuple[str, ...] = (
    "mock_trace",
    "synthetic_frame",
    "manual_fixture",
)

RESERVED_INPUT_MODES: Tuple[str, ...] = ("recorded_offline_stub",)

FORBIDDEN_INPUT_MODES: Tuple[str, ...] = (
    "live_camera",
    "live_imu",
    "ros_topic",
)

FORBIDDEN_BACKEND_KINDS: Tuple[str, ...] = (
    "openvins_real",
    "vins_fusion_real",
    "orb_slam3_real",
    "rtabmap_real",
    "kimera_real",
    "hydra_real",
)

FORBIDDEN_LICENSE_STATUSES: Tuple[str, ...] = ("commercial_runtime_approved",)

VISION_OCR_POLLUTION_CANDIDATES: Tuple[str, ...] = (
    "DetectionCandidate",
    "TrackingCandidate",
    "SceneUnderstandingCandidate",
    "ocr_result_candidate",
    "ocr_evidence_pack_candidate",
    "roi_candidate",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "architecture_definition_only": True,
    "no_real_slam_backend": True,
    "no_camera_runtime": True,
    "no_imu_runtime": True,
    "no_ros_runtime": True,
    "no_provider_runtime": True,
    "no_benchmark": True,
    "no_map_persistence": True,
    "no_fact_write": True,
    "no_action_output": True,
    "no_speech_output": True,
    "no_commercial_runtime_selection": True,
}

MOCK_SLAM_BACKEND_OUTPUT_FIELDS: Tuple[str, ...] = (
    "backend_ref",
    "backend_kind",
    "backend_label",
    "output_mode",
    "frame_refs",
    "source_chain",
    "real_backend_connected",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "commercial_runtime_candidate",
    "technical_reference_only",
    "candidate_only",
)

SLAM_BACKEND_OUTPUT_FRAME_FIELDS: Tuple[str, ...] = (
    "frame_ref",
    "timestamp",
    "backend_ref",
    "backend_kind",
    "pose_fields",
    "motion_fields",
    "anchor_fields",
    "local_map_fields",
    "health_fields",
    "drift_fields",
    "relocalization_fields",
    "source_refs",
    "candidate_only",
)

SLAM_ADAPTER_INPUT_ENVELOPE_FIELDS: Tuple[str, ...] = (
    "envelope_ref",
    "backend_output_ref",
    "backend_kind",
    "source_method",
    "license_status",
    "runtime_status",
    "input_mode",
    "recorded_offline_stub_enabled",
    "license_gate_required",
    "adapter_contract_required",
    "real_backend_connected",
    "camera_connected",
    "imu_connected",
    "ros_connected",
    "candidate_only",
)

SLAM_ADAPTER_MAPPING_RULE_FIELDS: Tuple[str, ...] = (
    "mapping_ref",
    "adapter_ref",
    "backend_field",
    "luna_candidate_type",
    "mapping_status",
    "confidence_policy",
    "degradation_policy",
    "source_refs_required",
    "candidate_only_enforced",
    "candidate_only",
)

SLAM_SPATIAL_EVIDENCE_ADAPTER_FIELDS: Tuple[str, ...] = (
    "adapter_ref",
    "backend_kind",
    "adapter_label",
    "supported_candidate_types",
    "field_synthesis_entrypoint",
    "adapter_contract_ref",
    "license_gate_required",
    "adapter_contract_required",
    "real_backend_connected",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "commercial_runtime_candidate",
    "technical_reference_only",
    "camera_connected",
    "imu_connected",
    "ros_connected",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "candidate_only",
)

SLAM_ADAPTER_OUTPUT_BUNDLE_FIELDS: Tuple[str, ...] = (
    "bundle_ref",
    "adapter_ref",
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

SLAM_ADAPTER_HEALTH_REPORT_FIELDS: Tuple[str, ...] = (
    "report_ref",
    "adapter_ref",
    "adapter_status",
    "translation_ok",
    "mapping_rules_applied",
    "backend_runtime_health_claimed",
    "adapter_health_only",
    "candidate_only",
)

SLAM_ADAPTER_PLANNING_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "planned_adapters",
    "supported_candidate_types",
    "field_synthesis_entrypoint",
    "real_backend_connected",
    "runtime_execution_allowed",
    "provider_activation_allowed",
    "camera_connected",
    "imu_connected",
    "ros_connected",
    "license_gate_required",
    "adapter_contract_required",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "candidate_only_enforced",
    "final_decision",
    "candidate_only",
)


@dataclass(frozen=True)
class MockSLAMBackendOutput:
    backend_ref: str
    backend_kind: str
    backend_label: str
    output_mode: str
    frame_refs: Tuple[str, ...]
    source_chain: Tuple[str, ...]
    real_backend_connected: bool
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    commercial_runtime_candidate: bool
    technical_reference_only: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMBackendOutputFrame:
    frame_ref: str
    timestamp: str
    backend_ref: str
    backend_kind: str
    pose_fields: Tuple[str, ...]
    motion_fields: Tuple[str, ...]
    anchor_fields: Tuple[str, ...]
    local_map_fields: Tuple[str, ...]
    health_fields: Tuple[str, ...]
    drift_fields: Tuple[str, ...]
    relocalization_fields: Tuple[str, ...]
    source_refs: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMAdapterInputEnvelope:
    envelope_ref: str
    backend_output_ref: str
    backend_kind: str
    source_method: str
    license_status: str
    runtime_status: str
    input_mode: str
    recorded_offline_stub_enabled: bool
    license_gate_required: bool
    adapter_contract_required: bool
    real_backend_connected: bool
    camera_connected: bool
    imu_connected: bool
    ros_connected: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMAdapterMappingRule:
    mapping_ref: str
    adapter_ref: str
    backend_field: str
    luna_candidate_type: str
    mapping_status: str
    confidence_policy: str
    degradation_policy: str
    source_refs_required: bool
    candidate_only_enforced: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMSpatialEvidenceAdapter:
    adapter_ref: str
    backend_kind: str
    adapter_label: str
    supported_candidate_types: Tuple[str, ...]
    field_synthesis_entrypoint: str
    adapter_contract_ref: str
    license_gate_required: bool
    adapter_contract_required: bool
    real_backend_connected: bool
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    commercial_runtime_candidate: bool
    technical_reference_only: bool
    camera_connected: bool
    imu_connected: bool
    ros_connected: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMAdapterOutputBundle:
    bundle_ref: str
    adapter_ref: str
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
class SLAMAdapterHealthReport:
    report_ref: str
    adapter_ref: str
    adapter_status: str
    translation_ok: bool
    mapping_rules_applied: int
    backend_runtime_health_claimed: bool
    adapter_health_only: bool
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMAdapterPlanningDecision:
    decision_ref: str
    planned_adapters: Tuple[str, ...]
    supported_candidate_types: Tuple[str, ...]
    field_synthesis_entrypoint: str
    real_backend_connected: bool
    runtime_execution_allowed: bool
    provider_activation_allowed: bool
    camera_connected: bool
    imu_connected: bool
    ros_connected: bool
    license_gate_required: bool
    adapter_contract_required: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    candidate_only_enforced: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
