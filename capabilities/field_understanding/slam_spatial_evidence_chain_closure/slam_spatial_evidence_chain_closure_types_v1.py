# -*- coding: utf-8 -*-
"""SLAM Spatial Evidence Chain Closure — types v1."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

PHASE_ID = "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
SCOPE = "slam_spatial_evidence_chain_closure_review_only"
SOURCE_CHAIN = "slam_spatial_evidence_chain_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "SLAM 空间证据链闭合审查：确认 TUM / RTAB trajectory / odometry / graph / GPS stub "
    "均已通过 Interface Layer → Generic JSON Spatial Trace → spatial_evidence_candidate_bundle "
    "→ spatial_odometry_fusion_candidate → field_synthesis_v1 标准路径进入 Luna。"
    "不新增 parser、不新增模型、不接 runtime。"
)

MODEL_ID = "sample_slam_spatial_evidence_model"
MODEL_FAMILY = "slam"
DOMAIN_ID = "spatial_evidence"
MODEL_MANAGEMENT_PROTOCOL_REF = "Model Management Protocol"
INTERFACE_LAYER_PROTOCOL_REF = "LUNA-PROTO-L1-INTERFACE-LAYER-GOVERNANCE-V1"
MODEL_ADMISSION_STANDARD_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"
SOURCE_INTERFACE_PROFILE = "spatial_evidence_ingest_interface"
INTERNAL_STANDARD_FORMAT = "generic_json_spatial_trace"
ADAPTER_PROFILE_REF = "slam_spatial_evidence_adapter"
TARGET_ENTRYPOINT = "field_synthesis_v1"
FIELD_SYNTHESIS_ENTRYPOINT = "field_synthesis_v1"

FINAL_DECISION_CLOSURE_GO = "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_GO"
FINAL_DECISION_CLOSURE_BLOCKED = "SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_BLOCKED"

STANDARD_EVIDENCE_PIPELINE: Tuple[str, ...] = (
    "External Format / Stub",
    "Interface Adapter / Ingest",
    "generic_json_spatial_trace",
    "spatial_evidence_candidate_bundle",
    "spatial_odometry_fusion_candidate",
    "field_synthesis_v1",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "SLAMSpatialEvidenceChainClosure",
    "SLAMIngestChainRef",
    "SLAMEvidenceCandidateCoverage",
    "SLAMFusionReadinessMatrix",
    "SLAMFieldAlignmentDecision",
)

INGEST_CHAIN_REFS: Tuple[str, ...] = (
    "generic_tum_trajectory_chain",
    "rtab_map_trajectory_chain",
    "rtab_map_odometry_chain",
    "rtab_map_graph_chain",
    "spatial_odometry_fusion_chain",
)

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001",
    "Phase-Generic-TUM-Trajectory-To-JSON-Spatial-Trace-Ingest-v1-001",
    "Phase-RTAB-Map-Trajectory-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
    "Phase-RTAB-Map-Odometry-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
    "Phase-RTAB-Map-Graph-Export-To-JSON-Spatial-Trace-Fixture-v1-001",
    "Phase-Spatial-Odometry-Fusion-Interface-GPS-SLAM-Planning-v1-001",
    "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
    "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "external_input_must_pass_interface_adapter_ingest",
    "spatial_input_must_map_to_generic_json_spatial_trace_or_governed_fusion_candidate",
    "backend_native_output_direct_to_field_synthesis_forbidden",
    "rtab_map_private_ingest_entrypoint_forbidden",
    "gps_gnss_must_not_override_field_identity",
    "relocalization_must_not_restore_runtime_trust",
    "gps_slam_conflict_must_remain_conflict_candidate",
    "source_chain_must_be_preserved",
    "all_outputs_candidate_only",
    "no_runtime_action_speech_fact_write_in_this_phase",
)

SLAM_SPATIAL_EVIDENCE_CHAIN_CLOSURE_FIELDS: Tuple[str, ...] = (
    "closure_ref",
    "phase_id",
    "interface_layer_protocol_ref",
    "model_management_protocol_ref",
    "model_id",
    "internal_standard_format",
    "target_entrypoint",
    "standard_evidence_pipeline",
    "ingest_chain_refs",
    "sealed_upstream_phase_refs",
    "governance_rules",
    "candidate_only",
)

SLAM_INGEST_CHAIN_REF_FIELDS: Tuple[str, ...] = (
    "chain_ref",
    "source_format_ref",
    "ingest_module_ref",
    "upstream_phase_ref",
    "upstream_go_decision",
    "pipeline",
    "output_candidate_types",
    "generic_json_spatial_trace_required",
    "field_synthesis_entrypoint",
    "candidate_only",
)

SLAM_EVIDENCE_CANDIDATE_COVERAGE_FIELDS: Tuple[str, ...] = (
    "coverage_ref",
    "pose_supported",
    "motion_supported",
    "health_supported",
    "anchor_supported",
    "relocalization_supported",
    "drift_supported",
    "gps_gnss_stub_supported",
    "spatial_odometry_fusion_supported",
    "conflict_candidate_supported",
    "field_synthesis_entrypoint_locked",
)

SLAM_FUSION_READINESS_MATRIX_FIELDS: Tuple[str, ...] = (
    "matrix_ref",
    "fusion_interface_ref",
    "fusion_scenario_count",
    "gps_slam_division_locked",
    "conflict_candidate_path_locked",
    "alignment_hint_path_locked",
    "field_protocol_alignment_next",
)

SLAM_FIELD_ALIGNMENT_DECISION_FIELDS: Tuple[str, ...] = (
    "decision_ref",
    "closure_ref",
    "chain_count",
    "generic_json_spatial_trace_required",
    "backend_native_output_direct_to_field_blocked",
    "gps_does_not_override_field_identity",
    "relocalization_does_not_restore_runtime_trust",
    "runtime_activation_allowed",
    "direct_action_allowed",
    "direct_speech_allowed",
    "direct_fact_write_allowed",
    "final_decision",
    "candidate_only",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "closure_review_only": True,
    "no_new_parser": True,
    "no_new_model": True,
    "no_runtime_activation": True,
    "no_third_party_slam_runtime": True,
    "no_live_camera": True,
    "no_live_imu": True,
    "no_real_gps_gnss": True,
    "no_ros_runtime": True,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "no_action_output": True,
    "no_speech_output": True,
    "no_fact_write": True,
}


@dataclass(frozen=True)
class SLAMSpatialEvidenceChainClosure:
    closure_ref: str
    phase_id: str
    interface_layer_protocol_ref: str
    model_management_protocol_ref: str
    model_id: str
    internal_standard_format: str
    target_entrypoint: str
    standard_evidence_pipeline: Tuple[str, ...]
    ingest_chain_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMIngestChainRef:
    chain_ref: str
    source_format_ref: str
    ingest_module_ref: str
    upstream_phase_ref: str
    upstream_go_decision: str
    pipeline: Tuple[str, ...]
    output_candidate_types: Tuple[str, ...]
    generic_json_spatial_trace_required: bool
    field_synthesis_entrypoint: str
    candidate_only: bool = True


@dataclass(frozen=True)
class SLAMEvidenceCandidateCoverage:
    coverage_ref: str
    pose_supported: bool
    motion_supported: bool
    health_supported: bool
    anchor_supported: bool
    relocalization_supported: bool
    drift_supported: bool
    gps_gnss_stub_supported: bool
    spatial_odometry_fusion_supported: bool
    conflict_candidate_supported: bool
    field_synthesis_entrypoint_locked: str


@dataclass(frozen=True)
class SLAMFusionReadinessMatrix:
    matrix_ref: str
    fusion_interface_ref: str
    fusion_scenario_count: int
    gps_slam_division_locked: bool
    conflict_candidate_path_locked: bool
    alignment_hint_path_locked: bool
    field_protocol_alignment_next: bool


@dataclass(frozen=True)
class SLAMFieldAlignmentDecision:
    decision_ref: str
    closure_ref: str
    chain_count: int
    generic_json_spatial_trace_required: bool
    backend_native_output_direct_to_field_blocked: bool
    gps_does_not_override_field_identity: bool
    relocalization_does_not_restore_runtime_trust: bool
    runtime_activation_allowed: bool
    direct_action_allowed: bool
    direct_speech_allowed: bool
    direct_fact_write_allowed: bool
    final_decision: str
    candidate_only: bool = True


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
