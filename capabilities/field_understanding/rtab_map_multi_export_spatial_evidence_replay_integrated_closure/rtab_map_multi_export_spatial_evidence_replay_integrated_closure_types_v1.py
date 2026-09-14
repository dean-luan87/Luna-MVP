# -*- coding: utf-8 -*-
"""RTAB-Map Multi-Export Spatial Evidence Replay Integrated Closure — types v1.

Integrated-validation closure. Verifies that sealed RTAB real-file loader outputs
(trajectory pose/motion, odometry pose/motion/health, graph anchor/relocalization/drift)
enter the Luna spatial evidence chain as a unified candidate bundle:

  RTAB real file outputs
  -> Generic JSON Spatial Trace Parser
  -> spatial_evidence_candidate_bundle
  -> spatial_odometry_fusion_candidate
  -> Field / Task / Guidance candidate replay
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RTAB-Map-Multi-Export-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
SCOPE = "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1"
SOURCE_CHAIN = "rtab_map_multi_export_spatial_evidence_replay_integrated_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "对 RTAB-Map trajectory / odometry / graph 三条真实文件 loader 基线做空间证据链整合 closure："
    "验证已封口的 RTAB real file loader 输出能否作为统一 spatial evidence candidate bundle，进入 "
    "spatial odometry fusion、Field / Task / Guidance candidate replay path。采用集中验证方式，不再"
    "拆单一 Planning / DryRun / Gate。复用 Generic JSON Spatial Trace Parser，不读 RTAB database，"
    "不接 ROS，不启动 live runtime，全程 candidate-only。"
)

RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF = (
    "Phase-RTAB-Map-Real-File-Loader-Integrated-DryRun-v1-001"
)
RTAB_TRAJECTORY_LOADER_DRYRUN_REF = (
    "Phase-RTAB-Map-Trajectory-Real-File-Loader-DryRun-v1-001"
)
RTAB_ODOMETRY_LOADER_DRYRUN_REF = (
    "Phase-RTAB-Map-Odometry-Real-File-Loader-DryRun-v1-001"
)
GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF = (
    "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
)
FIELD_SYNTHESIS_MAP_PLACE_OVERLAY_DRYRUN_REF = (
    "Phase-Field-Synthesis-Map-Place-Realtime-Event-Overlay-DryRun-v1-001"
)
FIELD_TO_TASK_ALIGNMENT_DRYRUN_REF = "Phase-Field-To-Task-Alignment-DryRun-v1-001"
TASK_TO_GUIDANCE_SAFETY_GATE_DRYRUN_REF = "Phase-Task-To-Guidance-Safety-Gate-DryRun-v1-001"
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
SOURCE_FAMILY = "rtab_map_real_file_exports"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
OUTPUT_CANDIDATE_CONTRACT_REF = "spatial_evidence_candidate_bundle"
FUSION_CANDIDATE_REF = "spatial_odometry_fusion_candidate"

RUNTIME_TRIAL_MODE = "rtab_multi_export_spatial_evidence_replay_integrated_closure_only"

CANDIDATE_TYPE_COVERAGE_REQUIRED: Tuple[str, ...] = (
    "pose",
    "motion",
    "health",
    "anchor",
    "relocalization",
    "drift",
)

GPS_SLAM_CONFLICT_DISTANCE_THRESHOLD_M = 5.0

FINAL_DECISION_GO = "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_GO"
FINAL_DECISION_BLOCKED = (
    "RTAB_MAP_MULTI_EXPORT_SPATIAL_EVIDENCE_REPLAY_INTEGRATED_CLOSURE_BLOCKED"
)

NEXT_PHASE_REF = (
    "Phase-External-Vision-OCR-Segmentation-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
)

REPLAY_PIPELINE: Tuple[str, ...] = (
    "rtab_trajectory_odometry_graph_real_file_outputs",
    "generic_json_spatial_trace_parser",
    "spatial_evidence_candidate_bundle",
    "spatial_odometry_fusion_candidate",
    "field_task_guidance_candidate_replay_path",
)

FIELD_TASK_GUIDANCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "FieldCandidate",
    "FieldStateCandidate",
    "TaskContextCandidate",
    "TaskRiskCandidate",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "rtab_multi_export_candidate_type_coverage",
    "rtab_multi_export_spatial_evidence_bundle_replay",
    "rtab_multi_export_spatial_odometry_fusion_replay",
    "rtab_multi_export_gps_slam_conflict_replay",
    "rtab_multi_export_field_task_guidance_replay",
    "rtab_multi_export_observation_only_scenario_replay",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_candidate_type_coverage_rejected",
    "invalid_missing_source_chain_or_file_origin_rejected",
    "invalid_runtime_trust_restore_attempt_rejected",
    "invalid_gps_field_identity_overwrite_rejected",
    "invalid_direct_action_speech_navigation_fact_write_rejected",
    "invalid_native_output_direct_to_field_rejected",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RTABMultiExportSpatialEvidenceReplayClosureProfile",
    "RTABMultiExportSpatialEvidenceInputBundle",
    "RTABMultiExportCandidateTypeCoverageResult",
    "RTABSpatialEvidenceBundleReplayResult",
    "RTABSpatialOdometryFusionReplayResult",
    "RTABFieldTaskGuidanceReplayResult",
    "RTABMultiExportSafetyBoundaryResult",
    "RTABMultiExportSpatialEvidenceReplayClosureDecision",
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "integrated_closure_is_not_live_runtime",
    "integrated_validation_mode_continues_no_single_loader_split",
    "generic_json_spatial_trace_parser_must_be_reused",
    "rtab_native_output_must_not_enter_field_synthesis_directly",
    "spatial_evidence_candidate_bundle_must_remain_candidate_only",
    "spatial_odometry_fusion_candidate_must_remain_candidate_only",
    "field_task_guidance_replay_remains_candidate_only",
    "gps_gnss_must_not_override_field_identity",
    "relocalization_must_not_restore_runtime_trust",
    "drift_remains_spatial_uncertainty_evidence",
    "health_remains_risk_evidence_candidate_only",
    "graph_anchor_must_not_write_fact",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_be_present_before_action_like_guidance",
    "no_live_sensor_no_real_gps_no_real_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "commercial_runtime_approval_not_implied",
    "this_phase_closes_rtab_multi_export_spatial_evidence_replay_baseline_if_all_checks_pass",
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only": True,
    "rtab_multi_export_spatial_evidence_replay_integrated_closure_only": True,
    "integrated_validation_mode_used": True,
    "single_loader_validation_not_used": True,
    "real_file_replay_execution_allowed": True,
    "runtime_activation_allowed": False,
    "trial_runtime_started": False,
    "live_sensor_connected": False,
    "rtab_database_read_allowed": False,
    "ros_connected": False,
    "live_rtab_runtime_started": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
    "runtime_activation_deferred": True,
}


@dataclass(frozen=True)
class RTABMultiExportSpatialEvidenceReplayClosureProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    rtab_real_file_loader_integrated_dryrun_ref: str
    source_family: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    candidate_type_coverage_required: Tuple[str, ...]
    replay_pipeline: Tuple[str, ...]
    field_task_guidance_candidate_types: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RTABMultiExportSpatialEvidenceInputBundle:
    bundle_ref: str
    source_family: str
    trajectory_scope_closed: bool
    odometry_scope_closed: bool
    graph_scope_closed: bool
    json_trace_item_count: int
    source_chain: str


@dataclass(frozen=True)
class RTABMultiExportCandidateTypeCoverageResult:
    result_ref: str
    candidate_type_coverage: Tuple[str, ...]
    candidate_type_coverage_complete: bool
    missing_candidate_types: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RTABSpatialEvidenceBundleReplayResult:
    result_ref: str
    spatial_evidence_candidate_bundle_generated: bool
    candidate_bundle_mapping_ok: bool
    source_chain_preserved: bool
    file_origin_preserved: bool
    export_session_id_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RTABSpatialOdometryFusionReplayResult:
    result_ref: str
    spatial_odometry_fusion_candidate_generated: bool
    gps_slam_conflict_candidate_generated: bool
    gps_does_not_override_field_identity: bool
    field_identity_not_overwritten: bool
    relocalization_does_not_restore_runtime_trust: bool
    drift_remains_uncertainty_evidence: bool
    health_can_only_influence_risk_as_evidence: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RTABFieldTaskGuidanceReplayResult:
    result_ref: str
    field_task_guidance_replay_path_ok: bool
    task_risk_candidate_references_health_drift_conflict: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    observation_only_scope_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RTABMultiExportSafetyBoundaryResult:
    result_ref: str
    missing_candidate_type_coverage_rejected: bool
    missing_source_chain_or_file_origin_rejected: bool
    runtime_trust_restore_attempt_rejected: bool
    gps_field_identity_overwrite_rejected: bool
    direct_action_speech_navigation_fact_write_rejected: bool
    native_output_direct_to_field_rejected: bool
    source_chain: str


@dataclass(frozen=True)
class RTABMultiExportSpatialEvidenceReplayClosureDecision:
    decision_ref: str
    closure_profile_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    rtab_real_file_loader_integrated_dryrun_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    slam_spatial_evidence_chain_field_alignment_closure_go_verified: bool
    field_task_guidance_safety_chain_closure_go_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
