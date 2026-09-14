# -*- coding: utf-8 -*-
"""SLAM Backend Real File Output Integrated Admission Planning — types v1.

After the RTAB multi-export spatial evidence replay closure, extend SLAM / VIO /
scene-graph backend real-file-output admission to a multi-backend baseline:
generic trajectory, RGB-D graph SLAM (RTAB), VIO (OpenVINS), visual SLAM
(ORB-SLAM3), metric-semantic SLAM (Kimera), scene-graph SLAM (Hydra), and
neural/Gaussian SLAM. Planning + Matrix Review only: unified admission / adapter /
candidate mapping / replay boundary. No real conversion, no live runtime, no live
sensor/ROS/camera/IMU/GPS/map API, no navigation/action/speech/fact_write.

  slam backend real file output
  -> license / source admission
  -> external interface adapter
  -> generic_json_spatial_trace
  -> spatial_evidence_candidate_bundle
  -> Field / Task / Guidance candidate replay
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-SLAM-Backend-Real-File-Output-Integrated-Admission-Planning-v1-001"
SCOPE = "slam_backend_real_file_output_integrated_admission_planning"
SOURCE_CHAIN = "slam_backend_real_file_output_integrated_admission_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "在 RTAB multi-export spatial evidence replay 已封口后，继续推进 SLAM / VIO / scene graph 后端真实"
    "文件输出接入规划。面向多类 SLAM 后端输出（generic trajectory / RTAB / OpenVINS / ORB-SLAM3 / "
    "Kimera / Hydra / Neural-Gaussian），建立统一 admission / adapter / candidate mapping / replay "
    "boundary。只做 Planning + Matrix Review，集中验证不拆单一后端；不执行真实转换，不接 live runtime，"
    "不接 live sensor / ROS / camera / IMU / GPS / 地图 API，不触发 navigation / action / speech / "
    "fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "slam_backend_real_file_output_integrated_admission_planning_only"
SOURCE_FAMILY = "slam_backend_real_file_outputs"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "external_slam_backend_interface_adapter"
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
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

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    GENERIC_TUM_DRYRUN_REF,
    RTAB_REAL_FILE_LOADER_INTEGRATED_DRYRUN_REF,
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    GENERIC_JSON_PARSER_PHASE_REF,
    SLAM_SPATIAL_EVIDENCE_CHAIN_FIELD_ALIGNMENT_CLOSURE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
)

# --------------------------------------------------------------------------- #
# Backend output sources (registered ids)
# --------------------------------------------------------------------------- #
BACKEND_SOURCE_IDS: Tuple[str, ...] = (
    "generic_tum_trajectory",
    "rtab_map_multi_export",
    "openvins_trajectory_export",
    "orb_slam3_trajectory_export",
    "kimera_metric_semantic_output",
    "hydra_scene_graph_output",
    "neural_or_gaussian_slam_export",
)

BACKEND_REGISTERED_GO_KEYS: Tuple[str, ...] = (
    "generic_tum_trajectory_registered",
    "rtab_map_multi_export_registered",
    "openvins_trajectory_export_registered",
    "orb_slam3_trajectory_export_registered",
    "kimera_metric_semantic_output_registered",
    "hydra_scene_graph_output_registered",
    "neural_gaussian_slam_export_registered",
)

# license boundary vocab
LICENSE_TECHNICAL_REFERENCE_ONLY = "technical_reference_only_if_gpl_or_incompatible"
LICENSE_OPEN_VERIFIED = "open_verified"
LICENSE_BOUNDARY_VALUES: Tuple[str, ...] = (
    LICENSE_TECHNICAL_REFERENCE_ONLY,
    LICENSE_OPEN_VERIFIED,
)

ALLOWED_USE_VALUES: Tuple[str, ...] = (
    "baseline_reuse",
    "adapter_planning_only",
    "observation_and_adapter_planning",
    "observation_only",
)

# --------------------------------------------------------------------------- #
# Candidate mapping support keys
# --------------------------------------------------------------------------- #
CANDIDATE_MAPPING_GO_KEYS: Tuple[str, ...] = (
    "pose_candidate_mapping_supported",
    "motion_candidate_mapping_supported",
    "health_candidate_mapping_supported",
    "anchor_candidate_mapping_supported",
    "relocalization_candidate_mapping_supported",
    "drift_candidate_mapping_supported",
    "scene_relation_candidate_mapping_supported",
    "field_structure_candidate_mapping_supported",
    "local_map_uncertainty_hint_mapping_supported",
)

ALL_CANDIDATE_TYPES: Tuple[str, ...] = (
    "pose",
    "motion",
    "health",
    "anchor",
    "relocalization",
    "drift",
    "region",
    "scene_relation",
    "semantic_place",
    "field_structure_candidate",
    "local_map",
    "uncertainty_hint",
    "relocalization_hint",
)

# --------------------------------------------------------------------------- #
# Integrated scenarios
# --------------------------------------------------------------------------- #
INTEGRATED_SCENARIO_REFS: Tuple[str, ...] = (
    "generic_trajectory_and_rtab_baseline_reuse",
    "vio_trajectory_output_admission_planning",
    "visual_slam_keyframe_output_admission_planning",
    "metric_semantic_slam_output_admission_planning",
    "scene_graph_slam_output_admission_planning",
    "neural_gaussian_slam_output_observation_planning",
    "multi_backend_spatial_evidence_replay_path_planning",
    "invalid_slam_backend_output_blocked",
)

INTEGRATED_SCENARIO_GO_KEYS: Tuple[str, ...] = (
    "generic_trajectory_and_rtab_baseline_reuse_supported",
    "vio_trajectory_output_admission_supported",
    "visual_slam_keyframe_output_admission_supported",
    "metric_semantic_slam_output_admission_supported",
    "scene_graph_slam_output_admission_supported",
    "neural_gaussian_slam_observation_supported",
    "multi_backend_spatial_evidence_replay_path_supported",
    "invalid_slam_backend_output_blocked",
)

ORIGIN_METADATA_REQUIRED_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "confidence",
    "file_origin",
    "backend_origin",
    "license_ref",
)

PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "integrated_validation_mode_must_be_used_no_single_backend_split",
    "slam_backend_admission_planning_is_not_runtime_activation",
    "backend_output_must_pass_interface_adapter_before_luna_internal_format",
    "backend_native_output_must_not_enter_field_task_guidance_directly",
    "generic_json_spatial_trace_remains_default_internal_spatial_trace_format",
    "source_chain_confidence_file_origin_backend_origin_license_ref_must_be_preserved",
    "gpl_or_incompatible_license_backend_remains_technical_reference_only_unless_cleared",
    "vio_slam_pose_must_not_override_field_identity",
    "gps_gnss_hint_must_not_override_field_identity",
    "relocalization_must_not_restore_runtime_trust",
    "drift_remains_uncertainty_evidence",
    "health_remains_risk_evidence_candidate_only",
    "semantic_label_is_not_fact",
    "scene_graph_is_field_evidence_not_final_field_identity",
    "heavy_neural_gaussian_slam_runtime_is_not_admitted_in_this_phase",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_sensor_no_real_gps_no_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "commercial_runtime_approval_not_implied",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "SLAMBackendRealFileOutputAdmissionPlanningProfile",
    "SLAMBackendOutputSourcePolicy",
    "SLAMBackendLicenseBoundaryPolicy",
    "SLAMBackendOutputFormatAdmissionPolicy",
    "SLAMBackendToGenericJSONTraceMappingPolicy",
    "SLAMBackendReplayBoundaryPolicy",
    "SLAMBackendIntegratedScenarioPolicy",
    "SLAMBackendSafetyBoundaryPolicy",
    "SLAMBackendRealFileOutputAdmissionPlanningDecision",
)

FINAL_DECISION_GO = "SLAM_BACKEND_REAL_FILE_OUTPUT_INTEGRATED_ADMISSION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "SLAM_BACKEND_REAL_FILE_OUTPUT_INTEGRATED_ADMISSION_PLANNING_BLOCKED"

NEXT_PHASE_REF = "Phase-SLAM-Backend-Integrated-Output-Replay-DryRun-v1-001"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_used": True,
    "single_backend_validation_not_used": True,
    "real_file_conversion_execution_allowed": False,
    "real_file_replay_execution_allowed": False,
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
class SLAMBackendRealFileOutputAdmissionPlanningProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    rtab_multi_export_closure_ref: str
    generic_json_spatial_trace_parser_ref: str
    slam_spatial_evidence_chain_field_alignment_closure_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    interface_adapter_ref: str
    source_family: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    backend_source_ids: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SLAMBackendOutputSourcePolicy:
    source_id: str
    backend_family: str
    output_type: str
    priority: str
    candidate_types: Tuple[str, ...]
    allowed_use: str
    license_boundary: str
    source_chain_required: bool
    confidence_required: bool
    license_ref_required: bool
    backend_origin_required: bool
    adapter_required: bool
    native_output_direct_to_field_blocked: bool
    status: str = ""
    upstream_ref: str = ""
    note: str = ""


@dataclass(frozen=True)
class SLAMBackendLicenseBoundaryPolicy:
    policy_ref: str
    gpl_or_incompatible_backend_technical_reference_only: bool
    no_gpl_code_copy: bool
    no_runtime_dependency_unless_cleared: bool
    commercial_use_unknown_until_license_verified: bool
    technical_reference_backends: Tuple[str, ...]


@dataclass(frozen=True)
class SLAMBackendOutputFormatAdmissionPolicy:
    policy_ref: str
    adapter_required: bool
    source_chain_required: bool
    confidence_required: bool
    file_origin_required: bool
    backend_origin_required: bool
    license_ref_required: bool
    generic_json_output_required: bool
    generic_json_parser_required: bool


@dataclass(frozen=True)
class SLAMBackendToGenericJSONTraceMappingPolicy:
    policy_ref: str
    pose_candidate_mapping_supported: bool
    motion_candidate_mapping_supported: bool
    health_candidate_mapping_supported: bool
    anchor_candidate_mapping_supported: bool
    relocalization_candidate_mapping_supported: bool
    drift_candidate_mapping_supported: bool
    scene_relation_candidate_mapping_supported: bool
    field_structure_candidate_mapping_supported: bool
    local_map_uncertainty_hint_mapping_supported: bool
    semantic_label_not_fact: bool
    scene_graph_not_final_field_identity: bool


@dataclass(frozen=True)
class SLAMBackendReplayBoundaryPolicy:
    policy_ref: str
    backend_native_output_direct_to_field_blocked: bool
    vio_slam_pose_not_field_identity: bool
    gps_does_not_override_field_identity: bool
    relocalization_does_not_restore_runtime_trust: bool
    drift_remains_uncertainty_evidence: bool
    health_candidate_only: bool
    field_task_guidance_candidate_only: bool
    heavy_neural_gaussian_runtime_not_admitted: bool


@dataclass(frozen=True)
class SLAMBackendIntegratedScenarioPolicy:
    scenario_ref: str
    input_summary: str
    output_plan: str
    requirement: str
    blocked_scenario: bool = False


@dataclass(frozen=True)
class SLAMBackendSafetyBoundaryPolicy:
    policy_ref: str
    no_live_sensor: bool
    no_ros: bool
    no_camera: bool
    no_imu: bool
    no_real_gps: bool
    no_map_api: bool
    no_navigation_action_speech_fact_write: bool
    controlled_trial_governance_template_referenced: bool
    commercial_runtime_approval_not_implied: bool


@dataclass(frozen=True)
class SLAMBackendRealFileOutputAdmissionPlanningDecision:
    decision_ref: str
    planning_profile_count: int
    slam_backend_source_policy_count: int
    integrated_scenario_count: int
    tum_real_file_loader_dryrun_go_verified: bool
    rtab_multi_export_spatial_evidence_replay_closure_go_verified: bool
    generic_json_spatial_trace_parser_go_verified: bool
    slam_spatial_evidence_chain_field_alignment_closure_go_verified: bool
    field_task_guidance_safety_chain_closure_go_verified: bool
    interface_layer_governance_verified: bool
    model_admission_governance_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
