# -*- coding: utf-8 -*-
"""RGB Vision + SLAM Spatial Evidence Cross-Modal Integrated Closure — types v1.

Cross-modal integrated closure that merges the RGB Vision Evidence Chain ("what is
seen": color/shape/text/symbol/object/region/relation) with the SLAM Backend
Evidence Chain ("where / how moving": pose/motion/anchor/drift/relocalization/
local_map) into one Luna Phase-One environment cognition mainline — an RGB-first +
SLAM-as-spatial-evidence unified evidence baseline.

  RGB vision evidence candidates  ─┐
                                   ├─ cross-modal alignment (candidate-only)
  SLAM spatial evidence candidates ┘
  -> cross_modal_*_candidate
  -> field_context / task_context / task_risk / guidance candidate
  -> Field / Task / Guidance candidate replay

Closure + Matrix Review only. No real model inference, no model/dataset download,
no training, no live camera/sensor, no SLAM runtime, no ROS/GPS/map API, no
navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001"
SCOPE = "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure"
SOURCE_CHAIN = "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "对 RGB Vision Evidence Chain 与 SLAM Backend Evidence Chain 做 cross-modal integrated closure。"
    "把“看见什么”与“空间证据在哪里”合并到 Luna 一期环境认知主链，形成 RGB-first + SLAM-as-spatial-"
    "evidence 的统一 evidence baseline。只做 Closure + Matrix Review，集中验证不拆单一模态；不做真实模型"
    "推理，不下载模型，不训练，不接 live camera / live sensor，不启动 SLAM runtime，不接 ROS / GPS / "
    "map API，不触发 navigation / action / speech / fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "rgb_vision_slam_spatial_evidence_cross_modal_integrated_closure_only"
VISION_HARDWARE_BASELINE = "rgb_first_first_person_camera"
SLAM_ROLE = "spatial_evidence_provider"
SYSTEM_OBJECTIVE = "cognitive_world_reconstruction"
TARGET_ENTRYPOINT = "field_synthesis_v1"
RGB_INTERFACE_ADAPTER_REF = "external_vision_interface_adapter"
SLAM_INTERFACE_ADAPTER_REF = "external_slam_backend_interface_adapter"
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
RGB_VISION_PLANNING_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
)
RGB_VISION_DRYRUN_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-DryRun-v1-001"
)
ROBOFLOW_DATASET_DRYRUN_REF = (
    "Phase-RGB-Vision-Roboflow-Dataset-Integrated-Evidence-Replay-DryRun-v1-001"
)
VISION_TEST_SOURCE_BACKUP_POOL_REF = "Phase-Luna-Vision-Test-Source-Backup-Pool-v1-001"
VISION_TEST_SOURCE_INTEGRATED_REPLAY_REF = (
    "Phase-RGB-Vision-Test-Source-Integrated-Evidence-Replay-DryRun-v1-001"
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

NEXT_PHASE_REF = "Phase-Visual-Symbol-Evidence-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Closure stages
# --------------------------------------------------------------------------- #
STAGE_REFS: Tuple[str, ...] = (
    "rgb_vision_evidence_chain_closure",
    "slam_backend_evidence_chain_closure",
    "rtab_multi_export_spatial_evidence_replay_closure",
    "field_task_guidance_safety_chain_closure",
    "runtime_governance_closure",
)

# --------------------------------------------------------------------------- #
# Cross-modal alignment policies
# --------------------------------------------------------------------------- #
ALIGNMENT_POLICY_IDS: Tuple[str, ...] = (
    "object_to_anchor_alignment",
    "region_to_local_map_alignment",
    "text_to_spatial_anchor_alignment",
    "visual_symbol_to_field_context_alignment",
    "scene_relation_to_field_structure_alignment",
    "tracking_to_motion_risk_alignment",
    "depth_vio_to_slam_pose_alignment",
    "uncertainty_conflict_alignment",
)

ALIGNMENT_SUPPORTED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{a}_supported" for a in ALIGNMENT_POLICY_IDS
)

# --------------------------------------------------------------------------- #
# Cross-modal candidate outputs
# --------------------------------------------------------------------------- #
CROSS_MODAL_CANDIDATE_IDS: Tuple[str, ...] = (
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

CROSS_MODAL_CANDIDATE_COVERED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_covered" for c in CROSS_MODAL_CANDIDATE_IDS
)

# --------------------------------------------------------------------------- #
# Field/Task/Guidance + safety + conflict GO keys
# --------------------------------------------------------------------------- #
FIELD_TASK_GUIDANCE_PATH_GO_KEYS: Tuple[str, ...] = (
    "rgb_evidence_adapter_required",
    "slam_evidence_adapter_required",
    "cross_modal_output_candidate_only",
    "field_task_guidance_candidate_only",
    "guidance_candidate_remains_candidate",
    "speech_gate_candidate_not_tts",
    "action_safety_candidate_exists",
    "observation_only_scope_preserved",
)

SAFETY_GO_KEYS: Tuple[str, ...] = (
    "object_identity_not_fact",
    "ocr_text_not_fact",
    "segmentation_not_route_activation",
    "tracking_not_action_trigger",
    "color_shape_symbol_not_fact",
    "visual_symbol_requires_context_validation",
    "monocular_depth_vio_slam_pose_not_field_identity",
    "scene_relation_not_final_interpretation",
    "scene_graph_not_final_field_identity",
    "relocalization_does_not_restore_runtime_trust",
    "drift_remains_uncertainty_evidence",
    "health_candidate_only",
    "gps_does_not_override_field_identity",
    "conflict_not_direct_fact_write",
    "conflict_not_direct_action_speech_navigation",
)

CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "cross_modal_closure_is_not_runtime_activation",
    "integrated_closure_must_be_used_no_rgb_only_or_slam_only_validation",
    "rgb_first_remains_default_vision_hardware_baseline",
    "slam_remains_spatial_evidence_provider_not_final_field_authority",
    "luna_objective_remains_cognitive_world_reconstruction",
    "rgb_evidence_must_pass_interface_adapter",
    "slam_evidence_must_pass_interface_adapter",
    "cross_modal_output_is_candidate_only",
    "object_identity_is_not_fact",
    "ocr_text_is_not_fact",
    "segmentation_is_not_route_activation",
    "tracking_is_not_action_trigger",
    "color_shape_visual_symbol_is_not_fact",
    "visual_symbol_meaning_requires_context_validation",
    "monocular_depth_vio_slam_pose_does_not_override_field_identity",
    "scene_relation_is_not_final_interpretation",
    "scene_graph_is_not_final_field_identity",
    "relocalization_does_not_restore_runtime_trust",
    "drift_remains_uncertainty_evidence",
    "health_remains_risk_evidence_candidate",
    "gps_gnss_does_not_override_field_identity",
    "conflict_does_not_directly_write_fact",
    "conflict_does_not_directly_trigger_action_speech_navigation",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "observation_only_scope_must_be_preserved",
    "no_dataset_download_no_training_no_model_download_no_runtime_build",
    "no_live_camera_live_sensor_gps_map_api_ros_imu",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "this_closure_seals_the_rgb_vision_plus_slam_spatial_evidence_cross_modal_baseline",
)

CLOSURE_OBJECT_TYPES: Tuple[str, ...] = (
    "CrossModalEvidenceClosureProfile",
    "CrossModalStageRef",
    "RGBVisionEvidenceCoverageRef",
    "SLAMSpatialEvidenceCoverageRef",
    "CrossModalEvidenceAlignmentPolicy",
    "CrossModalFieldSynthesisPathClosure",
    "CrossModalTaskGuidancePathClosure",
    "CrossModalConflictAndUncertaintyPolicy",
    "CrossModalSafetyBoundaryClosure",
    "RGBVisionSLAMSpatialEvidenceCrossModalIntegratedClosureDecision",
)

FINAL_DECISION_GO = "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_GO"
FINAL_DECISION_BLOCKED = "RGB_VISION_SLAM_SPATIAL_EVIDENCE_CROSS_MODAL_INTEGRATED_CLOSURE_BLOCKED"

# RGB / SLAM coverage references (carried from the two sealed chains)
RGB_VISION_COVERAGE_IDS: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
    "text_evidence_candidate",
    "spatial_hint_candidate",
    "attribute_candidate",
    "scene_relation_candidate",
    "color_evidence_candidate",
    "shape_evidence_candidate",
    "visual_symbol_candidate",
    "task_context_candidate",
    "task_risk_candidate",
)

SLAM_SPATIAL_COVERAGE_IDS: Tuple[str, ...] = (
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

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "integrated_validation_mode_used": True,
    "single_modality_validation_not_used": True,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "model_download_allowed": False,
    "slam_backend_model_download_allowed": False,
    "slam_backend_runtime_build_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "real_gps_connected": False,
    "real_map_api_connected": False,
    "real_navigation_started": False,
    "ros_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class CrossModalEvidenceClosureProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    rgb_vision_evidence_chain_closure_ref: str
    slam_backend_evidence_chain_closure_ref: str
    rgb_interface_adapter_ref: str
    slam_interface_adapter_ref: str
    vision_hardware_baseline: str
    slam_role: str
    system_objective: str
    target_entrypoint: str
    runtime_trial_mode: str
    stage_refs: Tuple[str, ...]
    alignment_policy_ids: Tuple[str, ...]
    cross_modal_candidate_ids: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class CrossModalStageRef:
    stage_ref: str
    phase_ref: str
    expected_final_decision: str
    coverage: Tuple[str, ...]


@dataclass(frozen=True)
class RGBVisionEvidenceCoverageRef:
    coverage_ref: str
    rgb_vision_coverage_ids: Tuple[str, ...]
    rgb_vision_coverage_count: int


@dataclass(frozen=True)
class SLAMSpatialEvidenceCoverageRef:
    coverage_ref: str
    slam_spatial_coverage_ids: Tuple[str, ...]
    slam_spatial_coverage_count: int


@dataclass(frozen=True)
class CrossModalEvidenceAlignmentPolicy:
    alignment_ref: str
    rgb_side: str
    slam_side: str
    purpose: str
    rule: str
    supported: bool


@dataclass(frozen=True)
class CrossModalFieldSynthesisPathClosure:
    closure_ref: str
    rgb_evidence_adapter_required: bool
    slam_evidence_adapter_required: bool
    cross_modal_output_candidate_only: bool
    field_candidate_can_reference_cross_modal_evidence: bool
    field_candidate_cannot_write_fact: bool


@dataclass(frozen=True)
class CrossModalTaskGuidancePathClosure:
    closure_ref: str
    task_context_can_reference_object_text_region_symbol_anchor_field_structure: bool
    task_risk_can_reference_dynamic_risk_drift_health_conflict_uncertainty: bool
    field_task_guidance_candidate_only: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    observation_only_scope_preserved: bool


@dataclass(frozen=True)
class CrossModalConflictAndUncertaintyPolicy:
    policy_ref: str
    ocr_symbol_mismatch_emits_conflict_candidate: bool
    object_segmentation_mismatch_emits_uncertainty_candidate: bool
    symbol_pose_mismatch_emits_spatial_consistency_or_conflict_candidate: bool
    relocalization_does_not_restore_runtime_trust: bool
    drift_only_increases_uncertainty: bool
    health_only_risk_evidence: bool
    gps_does_not_override_field_identity: bool
    conflict_not_direct_fact_write: bool
    conflict_not_direct_action_speech_navigation: bool


@dataclass(frozen=True)
class CrossModalSafetyBoundaryClosure:
    closure_ref: str
    rgb_first_hardware_baseline_preserved: bool
    slam_role_spatial_evidence_provider: bool
    cognitive_world_reconstruction_objective_preserved: bool
    object_identity_not_fact: bool
    ocr_text_not_fact: bool
    segmentation_not_route_activation: bool
    tracking_not_action_trigger: bool
    color_shape_symbol_not_fact: bool
    visual_symbol_requires_context_validation: bool
    monocular_depth_vio_slam_pose_not_field_identity: bool
    scene_relation_not_final_interpretation: bool
    scene_graph_not_final_field_identity: bool
    no_live_camera_sensor_gps_map_api_ros_imu: bool
    no_navigation_action_speech_fact_write: bool


@dataclass(frozen=True)
class RGBVisionSLAMSpatialEvidenceCrossModalIntegratedClosureDecision:
    decision_ref: str
    closure_profile_count: int
    stage_ref_count: int
    cross_modal_alignment_policy_count: int
    cross_modal_candidate_output_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
