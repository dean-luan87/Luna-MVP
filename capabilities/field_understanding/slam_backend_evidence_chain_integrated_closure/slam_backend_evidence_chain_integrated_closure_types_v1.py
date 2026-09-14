# -*- coding: utf-8 -*-
"""SLAM Backend Evidence Chain Integrated Closure — types v1.

Integrated closure for the SLAM / VIO / scene-graph / neural-gaussian backend
output admission chain. Seals, as one SLAM backend evidence chain baseline, the
capabilities of the TUM real-file loader, RTAB real-file multi-export, and the
mock-but-file-based multi-backend SLAM output replay:

  TUM / RTAB / OpenVINS-like / ORB-SLAM3-like / Kimera-like / Hydra-like /
  Neural-Gaussian-like
  -> license / source admission
  -> external slam backend interface adapter
  -> generic_json_spatial_trace
  -> spatial_evidence_candidate_bundle
  -> spatial_odometry_fusion_candidate
  -> Field / Task / Guidance candidate replay

Closure + Matrix Review only. No SLAM model download, no repo clone, no runtime
build, no ROS, no live sensor/camera/IMU/GPS/map API, no navigation/action/
speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001"
SCOPE = "slam_backend_evidence_chain_integrated_closure"
SOURCE_CHAIN = "slam_backend_evidence_chain_integrated_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "对 SLAM / VIO / scene graph / neural-gaussian SLAM 后端输出接入链路做 integrated closure。统一封存 "
    "TUM real file loader、RTAB real file multi-export，以及 mock-but-file-based 多 SLAM 后端输出 replay "
    "的证据链能力，归入同一条 SLAM backend evidence chain baseline。只做 Closure + Matrix Review，集中验证"
    "不拆单一后端；不下载 SLAM 模型，不 clone repo，不 build runtime，不接 ROS / camera / IMU / GPS / live "
    "sensor，不触发 navigation / action / speech / fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "slam_backend_evidence_chain_integrated_closure_only"
SOURCE_FAMILY = "slam_backend_evidence_chain"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "external_slam_backend_interface_adapter"
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
SLAM_BACKEND_INTEGRATED_OUTPUT_REPLAY_DRYRUN_REF = (
    "Phase-SLAM-Backend-Integrated-Output-Replay-DryRun-v1-001"
)
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

NEXT_PHASE_REF = "Phase-RGB-Vision-Evidence-Chain-Closure-v1-001"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
STAGE_REFS: Tuple[str, ...] = (
    "generic_tum_real_file_loader",
    "rtab_real_file_loader_integrated",
    "rtab_multi_export_spatial_evidence_replay",
    "slam_backend_admission_planning",
    "slam_backend_integrated_output_replay_dryrun",
)

# --------------------------------------------------------------------------- #
# Source family closure
# --------------------------------------------------------------------------- #
SOURCE_FAMILY_IDS: Tuple[str, ...] = (
    "generic_tum_trajectory",
    "rtab_map_multi_export",
    "openvins_like_vio_output",
    "orb_slam3_like_visual_slam_output",
    "kimera_like_metric_semantic_output",
    "hydra_like_scene_graph_output",
    "neural_gaussian_slam_like_output",
)

SOURCE_FAMILY_COVERED_GO_KEYS: Tuple[str, ...] = (
    "generic_tum_trajectory_covered",
    "rtab_map_multi_export_covered",
    "openvins_like_vio_output_covered",
    "orb_slam3_like_visual_slam_output_covered",
    "kimera_like_metric_semantic_output_covered",
    "hydra_like_scene_graph_output_covered",
    "neural_gaussian_slam_like_output_covered",
)

# --------------------------------------------------------------------------- #
# Candidate type closure
# --------------------------------------------------------------------------- #
CANDIDATE_TYPE_IDS: Tuple[str, ...] = (
    "pose",
    "motion",
    "health",
    "anchor",
    "relocalization",
    "drift",
    "region",
    "scene_relation",
    "semantic_place",
    "field_structure",
    "local_map",
    "uncertainty_hint",
)

CANDIDATE_TYPE_COVERED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_candidate_covered" for c in CANDIDATE_TYPE_IDS
)

# --------------------------------------------------------------------------- #
# Replay path closure
# --------------------------------------------------------------------------- #
REPLAY_PATH_GO_KEYS: Tuple[str, ...] = (
    "generic_json_parser_reused",
    "spatial_evidence_candidate_bundle_path_closed",
    "spatial_odometry_fusion_candidate_path_closed",
    "field_candidate_path_closed",
    "task_candidate_path_closed",
    "guidance_candidate_path_closed",
    "speech_gate_candidate_not_tts",
    "action_safety_candidate_exists",
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "integrated_closure_must_be_used_no_single_backend_closure_split",
    "slam_backend_evidence_chain_closure_is_not_runtime_activation",
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
    "action_safety_candidate_must_exist",
    "no_live_sensor_no_real_gps_no_map_api_no_ros_no_camera_no_imu",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "commercial_runtime_approval_not_implied",
    "this_closure_seals_the_slam_backend_evidence_chain_baseline",
)

CLOSURE_OBJECT_TYPES: Tuple[str, ...] = (
    "SLAMBackendEvidenceChainClosureProfile",
    "SLAMBackendEvidenceChainStageRef",
    "SLAMBackendCandidateTypeCoverageClosure",
    "SLAMBackendSourceFamilyCoverageClosure",
    "SLAMBackendReplayPathClosure",
    "SLAMBackendSafetyBoundaryClosure",
    "SLAMBackendLicenseBoundaryClosure",
    "SLAMBackendEvidenceChainIntegratedClosureDecision",
)

FINAL_DECISION_GO = "SLAM_BACKEND_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_GO"
FINAL_DECISION_BLOCKED = "SLAM_BACKEND_EVIDENCE_CHAIN_INTEGRATED_CLOSURE_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_used": True,
    "single_backend_validation_not_used": True,
    "slam_backend_model_download_allowed": False,
    "slam_backend_repo_clone_allowed": False,
    "slam_backend_runtime_build_allowed": False,
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
class SLAMBackendEvidenceChainClosureProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    slam_backend_integrated_output_replay_dryrun_ref: str
    admission_planning_ref: str
    generic_json_spatial_trace_parser_ref: str
    interface_adapter_ref: str
    source_family: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    stage_refs: Tuple[str, ...]
    source_family_ids: Tuple[str, ...]
    candidate_type_ids: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class SLAMBackendEvidenceChainStageRef:
    stage_ref: str
    phase_ref: str
    expected_final_decision: str
    coverage: Tuple[str, ...]


@dataclass(frozen=True)
class SLAMBackendCandidateTypeCoverageClosure:
    closure_ref: str
    candidate_type_ids: Tuple[str, ...]
    candidate_type_coverage_count: int
    all_candidate_types_covered: bool


@dataclass(frozen=True)
class SLAMBackendSourceFamilyCoverageClosure:
    closure_ref: str
    source_family_ids: Tuple[str, ...]
    source_family_coverage_count: int
    all_source_families_covered: bool


@dataclass(frozen=True)
class SLAMBackendReplayPathClosure:
    closure_ref: str
    generic_json_parser_reused: bool
    spatial_evidence_candidate_bundle_path_closed: bool
    spatial_odometry_fusion_candidate_path_closed: bool
    field_candidate_path_closed: bool
    task_candidate_path_closed: bool
    guidance_candidate_path_closed: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool


@dataclass(frozen=True)
class SLAMBackendSafetyBoundaryClosure:
    closure_ref: str
    vio_slam_pose_not_field_identity: bool
    gps_does_not_override_field_identity: bool
    relocalization_does_not_restore_runtime_trust: bool
    drift_remains_uncertainty_evidence: bool
    health_candidate_only: bool
    semantic_label_not_fact: bool
    scene_graph_not_final_field_identity: bool
    backend_native_output_direct_to_field_blocked: bool
    no_live_sensor_ros_camera_imu_gps_map_api: bool
    no_navigation_action_speech_fact_write: bool


@dataclass(frozen=True)
class SLAMBackendLicenseBoundaryClosure:
    closure_ref: str
    no_slam_model_download: bool
    no_repo_clone: bool
    no_runtime_build: bool
    gpl_or_incompatible_backend_technical_reference_only: bool
    commercial_runtime_approved: bool
    heavy_neural_gaussian_runtime_not_admitted: bool


@dataclass(frozen=True)
class SLAMBackendEvidenceChainIntegratedClosureDecision:
    decision_ref: str
    closure_profile_count: int
    stage_ref_count: int
    source_family_coverage_count: int
    candidate_type_coverage_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
