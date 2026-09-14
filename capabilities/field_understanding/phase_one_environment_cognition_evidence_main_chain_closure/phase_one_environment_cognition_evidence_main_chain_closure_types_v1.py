# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Evidence Main Chain Closure — types v1.

Integrated closure that seals Luna's Phase-One environment cognition evidence
mainline. This phase adds NO new information source, does NOT open the future
information-association mechanism, and does NOT touch audio / crowd / surface /
user-state / map / memory expansion directions. It only seals the already
completed chains:

  - RGB Vision Evidence Chain
  - SLAM Backend Evidence Chain
  - RGB + SLAM Cross-Modal Integrated Closure
  - Field / Task / Guidance Safety Chain
  - Runtime Governance
  - Interface Layer + Model Admission Governance

Closure + Matrix Review only. No real model inference, no model/dataset download,
no training, no live camera/sensor, no runtime, no ROS/GPS/map API, no
navigation/action/speech/fact_write. Future latent-relation / hidden-object-
relation mechanisms are recorded but deferred (not part of this closure).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
SCOPE = "phase_one_environment_cognition_evidence_main_chain_closure"
SOURCE_CHAIN = "phase_one_environment_cognition_evidence_main_chain_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "对 Luna 一期环境认知 evidence 主链做 integrated closure。不新增信息源、不展开未来信息关联机制、"
    "不接入音频/人群/材质/用户状态/地图/记忆等扩展方向，只封存当前已完成的 RGB Vision Evidence Chain、"
    "SLAM Backend Evidence Chain、RGB+SLAM Cross-Modal Integrated Closure、Field/Task/Guidance Safety "
    "Chain、Runtime Governance、Interface Layer、Model Admission。只做 Closure + Matrix Review；不做真实"
    "模型推理，不下载模型，不训练，不接 live camera / live sensor，不启动 runtime，不接 ROS/GPS/map "
    "API，不触发 navigation/action/speech/fact_write。未来潜在关系机制与隐藏物体关系机制仅记录、不展开。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "phase_one_environment_cognition_evidence_main_chain_closure_only"
PHASE_ONE_SCOPE = "environment_cognition_evidence_main_chain"
VISION_HARDWARE_BASELINE = "rgb_first_first_person_camera"
SLAM_ROLE = "spatial_evidence_provider"
SYSTEM_OBJECTIVE = "cognitive_world_reconstruction"
TARGET_ENTRYPOINT = "field_synthesis_v1"
GENERIC_JSON_SPATIAL_TRACE_PARSER_REF = "Phase-Generic-JSON-Spatial-Trace-Parser-v1-001"
INTERFACE_ADAPTER_REF = "external_model_backend_interface_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
)
SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001"
)
RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF = (
    "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001"
)
RTAB_MULTI_EXPORT_CLOSURE_REF = (
    "Phase-RTAB-Map-Multi-Export-Spatial-Evidence-Replay-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REFS: Tuple[str, ...] = (
    "Phase-Visual-Symbol-Evidence-DryRun-v1-001",
    "Phase-PhaseOne-Real-Recognition-DryRun-v1-001",
)

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
STAGE_REFS: Tuple[str, ...] = (
    "rgb_vision_evidence_chain_closure",
    "slam_backend_evidence_chain_closure",
    "rgb_vision_slam_cross_modal_closure",
    "field_task_guidance_safety_chain_closure",
    "runtime_governance_closure",
    "interface_and_model_admission_governance",
)

# --------------------------------------------------------------------------- #
# Evidence source closure
# --------------------------------------------------------------------------- #
EVIDENCE_SOURCE_IDS: Tuple[str, ...] = (
    "rgb_vision_evidence_chain",
    "ocr_text_evidence_chain",
    "segmentation_region_evidence_chain",
    "tracking_dynamic_risk_evidence_chain",
    "visual_symbol_evidence_chain",
    "slam_spatial_evidence_chain",
    "rtab_multi_export_spatial_evidence_chain",
    "tum_trajectory_spatial_evidence_chain",
    "multi_backend_slam_output_evidence_chain",
    "cross_modal_rgb_slam_alignment_chain",
)

EVIDENCE_SOURCE_COVERED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{s}_covered" for s in EVIDENCE_SOURCE_IDS
)

# --------------------------------------------------------------------------- #
# Candidate layer closure
# --------------------------------------------------------------------------- #
CANDIDATE_LAYER_IDS: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
    "text_evidence_candidate",
    "color_evidence_candidate",
    "shape_evidence_candidate",
    "visual_symbol_candidate",
    "spatial_hint_candidate",
    "pose_candidate",
    "motion_candidate",
    "health_candidate",
    "anchor_candidate",
    "relocalization_candidate",
    "drift_candidate",
    "scene_relation_candidate",
    "semantic_place_candidate",
    "field_structure_candidate",
    "local_map_candidate",
    "uncertainty_hint_candidate",
    "cross_modal_object_anchor_candidate",
    "cross_modal_region_structure_candidate",
    "cross_modal_text_anchor_candidate",
    "cross_modal_symbol_context_candidate",
    "cross_modal_scene_relation_structure_candidate",
    "cross_modal_motion_risk_candidate",
    "cross_modal_spatial_consistency_candidate",
    "cross_modal_uncertainty_candidate",
    "cross_modal_conflict_candidate",
    "field_context_candidate",
    "task_context_candidate",
    "task_risk_candidate",
    "guidance_candidate",
)

CANDIDATE_LAYER_COVERED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_covered" for c in CANDIDATE_LAYER_IDS
)

# --------------------------------------------------------------------------- #
# Deferred expansion record (recorded, NOT expanded)
# --------------------------------------------------------------------------- #
DEFERRED_EXPANSION_IDS: Tuple[str, ...] = (
    "audio_evidence",
    "human_behavior_gesture_crowd_flow_evidence",
    "surface_physical_risk_evidence",
    "perception_quality_evidence",
    "environment_event_temporal_change_evidence",
    "user_state_evidence",
    "memory_context_evidence",
    "external_map_poi_hint_evidence",
    "latent_information_association_mechanism",
    "hidden_object_object_relation_mechanism",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "main_chain_closure_is_not_runtime_activation",
    "integrated_closure_must_be_used",
    "no_new_information_source_expansion_in_this_phase",
    "future_latent_relation_mechanism_is_recorded_but_deferred",
    "hidden_object_object_relation_mechanism_is_recorded_but_deferred",
    "rgb_first_remains_default_vision_hardware_baseline",
    "slam_remains_spatial_evidence_provider",
    "external_model_backend_output_must_pass_interface_adapter",
    "source_admission_is_required",
    "all_evidence_remains_candidate_only",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "no_dataset_download_no_training_no_model_download_no_runtime_build",
    "no_live_camera_live_sensor_gps_map_api_ros_imu",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "this_closure_seals_luna_phase_one_environment_cognition_evidence_main_chain_baseline",
)

CLOSURE_OBJECT_TYPES: Tuple[str, ...] = (
    "PhaseOneEnvironmentCognitionEvidenceMainChainClosureProfile",
    "PhaseOneEvidenceMainChainStageRef",
    "PhaseOneEvidenceSourceCoverageClosure",
    "PhaseOneCandidateLayerCoverageClosure",
    "PhaseOneCrossModalPathClosure",
    "PhaseOneFieldTaskGuidancePathClosure",
    "PhaseOneGovernanceBoundaryClosure",
    "PhaseOneDeferredExpansionRecord",
    "PhaseOneEnvironmentCognitionEvidenceMainChainClosureDecision",
)

FINAL_DECISION_GO = "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO"
FINAL_DECISION_BLOCKED = "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_used": True,
    "new_information_source_expansion_allowed": False,
    "future_relation_mechanism_expansion_deferred": True,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "model_download_allowed": False,
    "slam_backend_model_download_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "real_gps_connected": False,
    "real_map_api_connected": False,
    "ros_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class PhaseOneEnvironmentCognitionEvidenceMainChainClosureProfile:
    profile_ref: str
    phase_id: str
    phase_one_scope: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    interface_adapter_ref: str
    vision_hardware_baseline: str
    slam_role: str
    system_objective: str
    target_entrypoint: str
    runtime_trial_mode: str
    stage_refs: Tuple[str, ...]
    evidence_source_ids: Tuple[str, ...]
    candidate_layer_ids: Tuple[str, ...]
    deferred_expansion_ids: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class PhaseOneEvidenceMainChainStageRef:
    stage_ref: str
    phase_ref: str
    expected_final_decision: str
    coverage: str


@dataclass(frozen=True)
class PhaseOneEvidenceSourceCoverageClosure:
    closure_ref: str
    evidence_source_ids: Tuple[str, ...]
    evidence_source_coverage_count: int


@dataclass(frozen=True)
class PhaseOneCandidateLayerCoverageClosure:
    closure_ref: str
    candidate_layer_ids: Tuple[str, ...]
    candidate_layer_coverage_count: int


@dataclass(frozen=True)
class PhaseOneCrossModalPathClosure:
    closure_ref: str
    rgb_evidence_path_closed: bool
    slam_spatial_evidence_path_closed: bool
    rgb_slam_cross_modal_path_closed: bool
    generic_json_spatial_trace_parser_reused: bool
    interface_adapter_required: bool
    source_admission_required: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    origin_metadata_preserved: bool
    spatial_evidence_candidate_bundle_path_closed: bool
    spatial_odometry_fusion_candidate_path_closed: bool


@dataclass(frozen=True)
class PhaseOneFieldTaskGuidancePathClosure:
    closure_ref: str
    field_candidate_path_closed: bool
    task_candidate_path_closed: bool
    guidance_candidate_path_closed: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    observation_only_scope_preserved: bool
    all_evidence_candidate_only: bool
    field_task_guidance_candidate_only: bool


@dataclass(frozen=True)
class PhaseOneGovernanceBoundaryClosure:
    closure_ref: str
    rgb_first_hardware_baseline_preserved: bool
    slam_role_spatial_evidence_provider: bool
    cognitive_world_reconstruction_objective_preserved: bool
    object_identity_not_fact: bool
    ocr_text_not_fact: bool
    color_shape_symbol_not_fact: bool
    visual_symbol_requires_context_validation: bool
    segmentation_not_route_activation: bool
    tracking_not_action_trigger: bool
    monocular_depth_vio_slam_pose_not_field_identity: bool
    relocalization_does_not_restore_runtime_trust: bool
    drift_remains_uncertainty_evidence: bool
    health_candidate_only: bool
    gps_does_not_override_field_identity: bool
    conflict_not_direct_fact_write: bool
    conflict_not_direct_action_speech_navigation: bool


@dataclass(frozen=True)
class PhaseOneDeferredExpansionRecord:
    record_ref: str
    deferred_expansion_ids: Tuple[str, ...]
    future_information_source_expansion_deferred: bool
    latent_relation_mechanism_deferred: bool
    hidden_object_relation_mechanism_deferred: bool
    deferred_expansion_not_part_of_current_closure: bool
    current_closure_does_not_expand_new_sources: bool


@dataclass(frozen=True)
class PhaseOneEnvironmentCognitionEvidenceMainChainClosureDecision:
    decision_ref: str
    closure_profile_count: int
    stage_ref_count: int
    evidence_source_coverage_count: int
    candidate_layer_coverage_count: int
    deferred_expansion_record_present: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
