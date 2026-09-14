# -*- coding: utf-8 -*-
"""SLAM Backend Integrated Output Replay DryRun — types v1.

Based on the sealed SLAM Backend Real File Output Integrated Admission Planning,
execute a mock-but-file-based multi-backend SLAM output integrated replay dry-run.
Validate that OpenVINS-like / ORB-SLAM3-like / Kimera-like / Hydra-like /
Neural-Gaussian-SLAM-like output samples can be unified into Luna Generic JSON
Spatial Trace / evidence candidates and enter the spatial-evidence ->
Field / Task / Guidance candidate replay path.

  slam backend mock file output
  -> license / source admission
  -> external slam backend interface adapter
  -> generic_json_spatial_trace
  -> spatial_evidence_candidate_bundle
  -> spatial_odometry_fusion_candidate
  -> Field / Task / Guidance candidate replay

No SLAM model download, no repo clone, no runtime build, no ROS, no live
sensor/camera/IMU/GPS, no navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-SLAM-Backend-Integrated-Output-Replay-DryRun-v1-001"
SCOPE = "slam_backend_integrated_output_replay_dryrun"
SOURCE_CHAIN = "slam_backend_integrated_output_replay_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 SLAM Backend Real File Output Integrated Admission Planning，执行 mock-but-file-based "
    "的多 SLAM 后端输出 integrated replay dry-run。验证 OpenVINS-like / ORB-SLAM3-like / Kimera-like / "
    "Hydra-like / Neural-Gaussian-SLAM-like 输出样例能否统一映射为 Luna Generic JSON Spatial Trace / "
    "evidence candidate，并进入 spatial evidence → Field / Task / Guidance candidate replay path。集中验证不"
    "拆单一后端；不下载 SLAM 模型，不 clone repo，不 build runtime，不接 ROS / camera / IMU / GPS / live "
    "sensor，不触发 navigation / action / speech / fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "slam_backend_integrated_output_replay_dryrun_only"
SOURCE_FAMILY = "slam_backend_mock_file_outputs"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "external_slam_backend_interface_adapter"
ADAPTER_MAPPING_REF = "slam_backend_output_adapter_mapping_v1"
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
ADMISSION_PLANNING_REF = (
    "Phase-SLAM-Backend-Real-File-Output-Integrated-Admission-Planning-v1-001"
)
GENERIC_TUM_DRYRUN_REF = "Phase-Generic-TUM-Real-File-Loader-DryRun-v1-001"
RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF = (
    "Phase-RTAB-Map-Real-File-Loader-Integrated-DryRun-v1-001"
)
RTAB_MULTI_EXPORT_CLOSURE_REF = (
    "Phase-RTAB-Map-Multi-Export-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
)
GENERIC_JSON_PARSER_PHASE_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF = (
    "Phase-SLAM-Spatial-Evidence-Chain-Field-Alignment-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001"

# --------------------------------------------------------------------------- #
# Backend families
# --------------------------------------------------------------------------- #
BACKEND_FAMILY_VIO = "vio"
BACKEND_FAMILY_VISUAL_SLAM = "visual_slam"
BACKEND_FAMILY_METRIC_SEMANTIC = "metric_semantic_slam"
BACKEND_FAMILY_SCENE_GRAPH = "scene_graph_slam"
BACKEND_FAMILY_NEURAL_GAUSSIAN = "neural_gaussian_slam"
BACKEND_FAMILY_MULTI = "multi_backend"

KNOWN_BACKEND_FAMILIES: Tuple[str, ...] = (
    BACKEND_FAMILY_VIO,
    BACKEND_FAMILY_VISUAL_SLAM,
    BACKEND_FAMILY_METRIC_SEMANTIC,
    BACKEND_FAMILY_SCENE_GRAPH,
    BACKEND_FAMILY_NEURAL_GAUSSIAN,
    BACKEND_FAMILY_MULTI,
)

LICENSE_TECHNICAL_REFERENCE_ONLY = "technical_reference_only_if_gpl_or_incompatible"

ALLOWED_USE_VALUES: Tuple[str, ...] = (
    "adapter_replay_dryrun_only",
    "observation_and_adapter_replay_dryrun",
    "observation_only",
)

# --------------------------------------------------------------------------- #
# Positive backend samples
# --------------------------------------------------------------------------- #
SAMPLE_BACKENDS: Dict[str, str] = {
    "openvins": "sample_openvins_trajectory_output.json",
    "orb_slam3": "sample_orb_slam3_keyframe_output.json",
    "kimera": "sample_kimera_metric_semantic_output.json",
    "hydra": "sample_hydra_scene_graph_output.json",
    "neural_gaussian": "sample_neural_gaussian_slam_output.json",
    "multi_backend": "sample_multi_backend_combined_output.json",
}

INVALID_SAMPLE_FILES: Tuple[str, ...] = (
    "invalid_missing_source_chain_backend_output.json",
    "invalid_missing_license_ref_backend_output.json",
    "invalid_gpl_backend_marked_commercial_ready.json",
    "invalid_native_backend_direct_to_field.json",
    "invalid_relocalization_runtime_trust_restore.json",
    "invalid_semantic_label_fact_write.json",
    "invalid_heavy_neural_runtime_activation.json",
)

SAMPLE_FILES: Tuple[str, ...] = tuple(SAMPLE_BACKENDS.values()) + INVALID_SAMPLE_FILES
SAMPLES_REL_DIR = (
    "capabilities/field_understanding/slam_backend_integrated_output_replay_dryrun/samples"
)

# --------------------------------------------------------------------------- #
# Unified admission requirements
# --------------------------------------------------------------------------- #
ADMISSION_REQUIRED_FIELDS: Tuple[str, ...] = (
    "backend_id",
    "backend_family",
    "output_type",
    "source_chain",
    "confidence",
    "backend_origin",
    "license_ref",
    "allowed_use",
    "commercial_use_status",
    "adapter_mapping_ref",
)

COMMERCIAL_READY_FLAGS: Tuple[str, ...] = (
    "commercial_ready",
    "commercial_runtime_approved",
    "commercial_use_approved",
)

PROHIBITED_OUTPUT_FLAGS: Tuple[str, ...] = (
    "direct_field_synthesis_write",
    "bypass_interface_adapter",
    "restore_runtime_trust",
    "direct_fact_write",
    "define_field_identity",
    "override_field_identity",
    "heavy_runtime_activation",
    "live_sensor_connect",
    "direct_action",
    "direct_speech",
    "direct_navigation",
    "route_activation",
)

# --------------------------------------------------------------------------- #
# Candidate types
# --------------------------------------------------------------------------- #
COVERAGE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "pose",
    "motion",
    "health",
    "anchor",
    "relocalization",
    "drift",
    "scene_relation",
    "field_structure",
    "local_map",
    "uncertainty_hint",
)

ALL_CANDIDATE_TYPES: Tuple[str, ...] = COVERAGE_CANDIDATE_TYPES + (
    "region",
    "semantic_place",
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

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "openvins_vio_output_replay",
    "orb_slam3_keyframe_output_replay",
    "kimera_metric_semantic_output_replay",
    "hydra_scene_graph_output_replay",
    "neural_gaussian_slam_output_observation_replay",
    "multi_backend_candidate_type_coverage",
    "multi_backend_spatial_evidence_replay_path",
    "multi_backend_observation_only_scope_replay",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_source_chain_rejected",
    "invalid_missing_license_ref_rejected",
    "invalid_gpl_marked_commercial_ready_rejected",
    "invalid_native_output_direct_to_field_rejected",
    "invalid_relocalization_runtime_trust_restore_rejected",
    "invalid_semantic_label_fact_write_rejected",
    "invalid_heavy_neural_runtime_activation_rejected",
    "invalid_direct_action_speech_navigation_fact_write_rejected",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "integrated_validation_mode_must_be_used_no_single_backend_split",
    "slam_backend_output_replay_dryrun_is_not_runtime_activation",
    "slam_backend_model_download_not_allowed",
    "slam_backend_repo_clone_not_allowed",
    "slam_backend_runtime_build_not_allowed",
    "backend_output_must_pass_interface_adapter_before_luna_internal_format",
    "backend_native_output_must_not_enter_field_task_guidance_directly",
    "generic_json_spatial_trace_remains_default_internal_spatial_trace_format",
    "source_chain_confidence_backend_origin_license_ref_must_be_preserved",
    "gpl_or_incompatible_license_backend_remains_technical_reference_only_unless_cleared",
    "vio_slam_pose_must_not_override_field_identity",
    "gps_gnss_hint_must_not_override_field_identity",
    "relocalization_must_not_restore_runtime_trust",
    "drift_remains_uncertainty_evidence",
    "health_remains_risk_evidence_candidate_only",
    "semantic_label_is_not_fact",
    "scene_graph_is_field_evidence_not_final_field_identity",
    "heavy_neural_gaussian_slam_runtime_is_not_admitted",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist_before_action_like_guidance",
    "no_live_sensor_no_real_gps_no_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "commercial_runtime_approval_not_implied",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "SLAMBackendIntegratedOutputReplayDryRunProfile",
    "SLAMBackendMockFileInputBundle",
    "SLAMBackendSourceAdmissionResult",
    "SLAMBackendOutputAdapterMappingResult",
    "SLAMBackendGenericJSONTraceConversionResult",
    "SLAMBackendCandidateCoverageResult",
    "SLAMBackendSpatialEvidenceReplayResult",
    "SLAMBackendFieldTaskGuidanceReplayResult",
    "SLAMBackendSafetyBoundaryResult",
    "SLAMBackendIntegratedOutputReplayDryRunDecision",
)

FINAL_DECISION_GO = "SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_used": True,
    "single_backend_validation_not_used": True,
    "slam_backend_model_download_allowed": False,
    "slam_backend_repo_clone_allowed": False,
    "slam_backend_runtime_build_allowed": False,
    "real_file_conversion_execution_allowed": True,
    "real_file_replay_execution_allowed": True,
    "runtime_activation_allowed": False,
    "live_sensor_connected": False,
    "real_navigation_started": False,
    "real_map_api_connected": False,
    "real_gps_connected": False,
    "ros_connected": False,
    "camera_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class SLAMBackendIntegratedOutputReplayDryRunProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    admission_planning_ref: str
    rtab_multi_export_closure_ref: str
    generic_json_spatial_trace_parser_ref: str
    slam_spatial_evidence_chain_field_alignment_closure_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    interface_adapter_ref: str
    adapter_mapping_ref: str
    source_family: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    sample_backends: Dict[str, str]
    admission_required_fields: Tuple[str, ...]
    coverage_candidate_types: Tuple[str, ...]
    field_task_guidance_candidate_types: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SLAMBackendMockFileInputBundle:
    bundle_ref: str
    backend_key: str
    backend_id: str
    backend_family: str
    output_type: str
    sample_file: str
    read_ok: bool


@dataclass(frozen=True)
class SLAMBackendSourceAdmissionResult:
    result_ref: str
    backend_id: str
    sample_file: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    required_fields_present: bool
    license_present: bool
    source_chain_present: bool
    confidence_present: bool
    backend_origin_present: bool
    adapter_mapping_ref_ok: bool
    gpl_commercial_integrity_ok: bool
    prohibited_flags_absent: bool
    rejection_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class SLAMBackendOutputAdapterMappingResult:
    result_ref: str
    backend_family: str
    candidate_count: int
    output_candidate_types: Tuple[str, ...]
    adapter_mapping_used: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    backend_origin_preserved: bool
    license_ref_preserved: bool


@dataclass(frozen=True)
class SLAMBackendGenericJSONTraceConversionResult:
    result_ref: str
    backend_id: str
    generic_json_output_ok: bool
    generic_json_parser_ref: str
    frame_count: int


@dataclass(frozen=True)
class SLAMBackendCandidateCoverageResult:
    result_ref: str
    coverage_candidate_types: Tuple[str, ...]
    generated_candidate_types: Tuple[str, ...]
    candidate_type_coverage_complete: bool


@dataclass(frozen=True)
class SLAMBackendSpatialEvidenceReplayResult:
    result_ref: str
    spatial_evidence_candidate_bundle_generated: bool
    spatial_odometry_fusion_candidate_generated: bool
    candidate_only: bool


@dataclass(frozen=True)
class SLAMBackendFieldTaskGuidanceReplayResult:
    result_ref: str
    field_task_guidance_replay_path_ok: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool


@dataclass(frozen=True)
class SLAMBackendSafetyBoundaryResult:
    result_ref: str
    vio_slam_pose_not_field_identity: bool
    gps_does_not_override_field_identity: bool
    relocalization_does_not_restore_runtime_trust: bool
    drift_remains_uncertainty_evidence: bool
    health_candidate_only: bool
    semantic_label_not_fact: bool
    scene_graph_not_final_field_identity: bool
    heavy_neural_gaussian_runtime_not_admitted: bool


@dataclass(frozen=True)
class SLAMBackendIntegratedOutputReplayDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
