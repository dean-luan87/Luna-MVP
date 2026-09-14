# -*- coding: utf-8 -*-
"""RGB Vision / OCR / Segmentation Integrated Evidence Replay Planning — types v1.

Planning-only baseline for external RGB vision / OCR / segmentation / tracking model
outputs entering the Luna integrated evidence replay. RGB-first / cognition-first:
the Luna phase-1 primary vision hardware baseline is a conventional RGB camera;
ToF / stereo / industrial depth is optional auxiliary only, never the default route.

  external RGB vision model output
  -> Interface Adapter
  -> Generic JSON Spatial Trace / evidence candidate
  -> Generic JSON Spatial Trace Parser replay
  -> spatial_evidence_candidate_bundle
  -> Field / Task / Guidance candidate replay (candidate-only)
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
SCOPE = "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_only"
SOURCE_CHAIN = "rgb_vision_ocr_segmentation_integrated_evidence_replay_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "在 RTAB multi-export spatial evidence replay 已封口后，规划外部 RGB vision / OCR / "
    "segmentation / tracking 输出进入 Luna integrated evidence replay。坚持 RGB-first / "
    "cognition-first：Luna 一期主视觉硬件基线为传统 RGB 摄像头，ToF / 双目 / 工业深度仅作"
    "可选辅助，不作默认路线。本阶段只做 Planning + Matrix Review，不接 live camera，不启动"
    "视觉 runtime，不接真实传感器，不触发 navigation / action / speech / fact_write。"
)

# --------------------------------------------------------------------------- #
# Hardware baseline bindings
# --------------------------------------------------------------------------- #
VISION_HARDWARE_BASELINE = "rgb_first_first_person_camera"
DEPTH_HARDWARE_DEFAULT = "not_required"
TOF_STEREO_DEPTH_ROLE = "optional_auxiliary_only"
SYSTEM_OBJECTIVE = "cognitive_world_reconstruction"

RUNTIME_TRIAL_MODE = "rgb_vision_integrated_evidence_replay_planning_only"
TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "external_vision_interface_adapter"
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"

CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream phase references
# --------------------------------------------------------------------------- #
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

SEALED_UPSTREAM_PHASE_REFS: Tuple[str, ...] = (
    RTAB_MULTI_EXPORT_CLOSURE_REF,
    FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF,
    GOVERNANCE_CLOSURE_REF,
    INTERFACE_LAYER_GOVERNANCE_REF,
    MODEL_ADMISSION_GOVERNANCE_REF,
)

# --------------------------------------------------------------------------- #
# Observation pool / future-admission candidate models (watch list only)
# --------------------------------------------------------------------------- #
OBSERVATION_POOL_REFS: Tuple[str, ...] = (
    "grounded_sam_2",
    "yolo_open_vocabulary_detection",
    "ocr_provider_enhancement_candidate",
    "tracking_supervision_adapter",
    "monocular_depth_estimation",
    "rgb_based_vio_visual_odometry_candidate",
    "scene_text_signage_understanding",
    "semantic_instance_segmentation",
)

# --------------------------------------------------------------------------- #
# External vision output source types (7)
# --------------------------------------------------------------------------- #
VISION_SOURCE_REFS: Tuple[str, ...] = (
    "rgb_frame_or_video_file",
    "object_detection_output",
    "segmentation_output",
    "tracking_output",
    "ocr_text_output",
    "monocular_depth_or_vio_output",
    "scene_relation_output",
)

VISION_SOURCE_GO_KEYS: Tuple[str, ...] = (
    "rgb_frame_or_video_source_supported",
    "object_detection_output_supported",
    "segmentation_output_supported",
    "tracking_output_supported",
    "ocr_text_output_supported",
    "monocular_depth_or_vio_output_supported",
    "scene_relation_output_supported",
)

VISION_OUTPUT_CANDIDATE_TYPES: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "track_evidence_candidate",
    "text_evidence_candidate",
    "spatial_hint_candidate",
    "scene_relation_candidate",
)

# --------------------------------------------------------------------------- #
# Integrated replay scenarios (7)
# --------------------------------------------------------------------------- #
REPLAY_SCENARIO_REFS: Tuple[str, ...] = (
    "rgb_scene_object_region_replay",
    "rgb_ocr_scene_text_replay",
    "rgb_tracking_dynamic_risk_replay",
    "rgb_monocular_depth_spatial_hint_replay",
    "rgb_scene_relation_task_replay",
    "rgb_integrated_field_task_guidance_replay_path",
    "invalid_vision_output_blocked",
)

REPLAY_SCENARIO_GO_KEYS: Tuple[str, ...] = (
    "rgb_scene_object_region_replay_supported",
    "rgb_ocr_scene_text_replay_supported",
    "rgb_tracking_dynamic_risk_replay_supported",
    "rgb_monocular_depth_spatial_hint_replay_supported",
    "rgb_scene_relation_task_replay_supported",
    "rgb_integrated_field_task_guidance_replay_path_supported",
    "invalid_vision_output_blocked",
)

# --------------------------------------------------------------------------- #
# Origin metadata required for any admitted vision output
# --------------------------------------------------------------------------- #
ORIGIN_METADATA_REQUIRED_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "confidence",
    "frame_origin_or_file_origin",
)

UNIVERSAL_BLOCKED_OPERATIONS: Tuple[str, ...] = (
    "live_camera_connect",
    "live_sensor_connect",
    "real_gps_connect",
    "real_map_api_connect",
    "ros_connect",
    "real_navigation",
    "direct_action",
    "direct_speech_tts",
    "direct_fact_write",
    "native_output_direct_to_field",
)

PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "rgb_first_is_default_vision_hardware_baseline",
    "tof_stereo_industrial_depth_is_optional_auxiliary_not_default",
    "vision_evidence_replay_planning_is_not_live_runtime",
    "external_vision_model_output_must_enter_interface_adapter_before_internal_format",
    "external_model_native_output_must_not_enter_field_task_guidance_directly",
    "ocr_output_is_evidence_candidate_not_fact",
    "segmentation_output_is_region_evidence_not_route_activation",
    "tracking_output_is_motion_evidence_not_action_trigger",
    "monocular_depth_vio_output_is_spatial_hint_not_field_identity",
    "scene_relation_output_is_relation_candidate_not_final_interpretation",
    "source_chain_confidence_origin_metadata_must_be_preserved",
    "field_task_guidance_replay_remains_candidate_only",
    "no_live_camera_sensor_gps_map_ros_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "integrated_validation_mode_must_be_used_no_single_loader_split",
)

DECLARED_PRINCIPLES: Tuple[str, ...] = (
    "luna_phase_1_default_vision_input_is_conventional_rgb_camera",
    "stereo_tof_industrial_depth_not_phase_1_default_baseline",
    "luna_objective_is_first_person_world_cognition_not_industrial_ranging",
    "depth_slam_vio_tof_are_spatial_evidence_aux_not_primary_vision_route",
    "rgb_output_enters_evidence_candidate_not_direct_fact_action_speech",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RGBVisionIntegratedEvidenceReplayPlanningProfile",
    "RGBVisionHardwareBaselinePolicy",
    "ExternalVisionOutputSourcePolicy",
    "VisionEvidenceCandidateMappingPolicy",
    "OCRTextEvidenceMappingPolicy",
    "SegmentationTrackingEvidenceMappingPolicy",
    "RGBVisionIntegratedReplayScenarioPolicy",
    "RGBVisionSafetyBoundaryPolicy",
    "RGBVisionIntegratedEvidenceReplayPlanningDecision",
)

FINAL_DECISION_GO = "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_PLANNING_GO"
FINAL_DECISION_BLOCKED = (
    "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_PLANNING_BLOCKED"
)

NEXT_PHASE_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-DryRun-v1-001"
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only_enforced": True,
    "integrated_validation_mode_used": True,
    "single_loader_validation_not_used": True,
    "real_file_replay_execution_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
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
class RGBVisionIntegratedEvidenceReplayPlanningProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    generic_json_spatial_trace_parser_ref: str
    rtab_multi_export_closure_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    vision_hardware_baseline: str
    depth_hardware_default: str
    tof_stereo_depth_role: str
    system_objective: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    pipeline_stages: Tuple[str, ...]
    vision_source_refs: Tuple[str, ...]
    replay_scenario_refs: Tuple[str, ...]
    observation_pool_refs: Tuple[str, ...]
    sealed_upstream_phase_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RGBVisionHardwareBaselinePolicy:
    policy_ref: str
    vision_hardware_baseline: str
    depth_hardware_default: str
    tof_stereo_depth_role: str
    system_objective: str
    rgb_first_hardware_baseline_declared: bool
    tof_stereo_depth_optional_auxiliary_only: bool
    cognitive_world_reconstruction_objective_declared: bool
    depth_slam_vio_are_auxiliary_only: bool
    rgb_output_enters_evidence_candidate_only: bool
    declared_principles: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class ExternalVisionOutputSourcePolicy:
    policy_ref: str
    source_ref: str
    source_zh: str
    provider_examples: Tuple[str, ...]
    output_candidate_type: str
    purpose_zh: str
    requires_interface_adapter: bool
    requires_source_chain: bool
    requires_confidence: bool
    requires_origin_metadata: bool
    native_output_direct_to_field_blocked: bool
    blocked_operations: Tuple[str, ...]
    source_chain: str
    supported: bool


@dataclass(frozen=True)
class VisionEvidenceCandidateMappingPolicy:
    policy_ref: str
    target_internal_format: str
    interface_adapter_ref: str
    generic_json_output_required: bool
    generic_json_parser_required: bool
    parser_ref: str
    target_entrypoint: str
    source_chain_required: bool
    confidence_required: bool
    origin_metadata_required: bool
    external_model_output_adapter_required: bool
    native_output_direct_to_field_blocked: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class OCRTextEvidenceMappingPolicy:
    policy_ref: str
    output_candidate_type: str
    ocr_output_not_fact: bool
    requires_source_chain: bool
    requires_confidence: bool
    scene_text_signage_supported: bool
    text_evidence_candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class SegmentationTrackingEvidenceMappingPolicy:
    policy_ref: str
    segmentation_output_candidate_type: str
    tracking_output_candidate_type: str
    segmentation_output_not_route_activation: bool
    tracking_output_not_action_trigger: bool
    monocular_depth_vio_not_field_identity: bool
    scene_relation_not_final_interpretation: bool
    region_evidence_candidate_only: bool
    track_evidence_candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionIntegratedReplayScenarioPolicy:
    scenario_ref: str
    input_description: str
    output_planning_target: str
    scenario_requirements: Tuple[str, ...]
    blocked_operations: Tuple[str, ...]
    allowed_next_step: str
    source_chain: str
    supported: bool
    blocked_scenario: bool


@dataclass(frozen=True)
class RGBVisionSafetyBoundaryPolicy:
    policy_ref: str
    external_model_output_adapter_required: bool
    native_output_direct_to_field_blocked: bool
    ocr_output_not_fact: bool
    segmentation_output_not_route_activation: bool
    tracking_output_not_action_trigger: bool
    monocular_depth_vio_not_field_identity: bool
    scene_relation_not_final_interpretation: bool
    field_task_guidance_replay_candidate_only: bool
    guidance_candidate_not_runtime_navigation: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_required: bool
    no_live_camera: bool
    no_live_sensor: bool
    no_action_speech_fact_write: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionIntegratedEvidenceReplayPlanningDecision:
    decision_ref: str
    profile_ref: str
    planning_profile_count: int
    vision_output_source_policy_count: int
    integrated_replay_scenario_count: int
    rtab_multi_export_spatial_evidence_replay_closure_go_verified: bool
    field_task_guidance_safety_chain_closure_go_verified: bool
    interface_layer_governance_verified: bool
    model_admission_governance_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    rgb_first_hardware_baseline_declared: bool
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
