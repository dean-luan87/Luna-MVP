# -*- coding: utf-8 -*-
"""RGB Vision / OCR / Segmentation Integrated Evidence Replay DryRun — types v1.

Executes a controlled offline integrated evidence replay over local RGB image/video
sample files plus mock-but-file-based model outputs (object detection, segmentation,
tracking, OCR, monocular depth/VIO, scene relation). RGB-first / cognition-first;
depth as optional auxiliary. All outputs candidate-only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-DryRun-v1-001"
SCOPE = "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun"
SOURCE_CHAIN = "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 RGB Vision OCR Segmentation Integrated Evidence Replay Planning，执行本地 RGB "
    "图片/视频样例 + mock-but-file-based 模型输出的 integrated evidence replay dry-run。允许读取本地"
    "受控样例文件；不接 live camera，不启动真实视觉 runtime，不接真实传感器，不触发 navigation / "
    "action / speech / fact_write。全程 candidate-only，集中验证不拆单一 loader。"
)

# --------------------------------------------------------------------------- #
# Hardware baseline bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "rgb_vision_integrated_evidence_replay_dryrun_only"
VISION_HARDWARE_BASELINE = "rgb_first_first_person_camera"
DEPTH_HARDWARE_DEFAULT = "not_required"
TOF_STEREO_DEPTH_ROLE = "optional_auxiliary_only"
SYSTEM_OBJECTIVE = "cognitive_world_reconstruction"

TARGET_INTERNAL_FORMAT = "generic_json_spatial_trace"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "external_vision_interface_adapter"
GENERIC_JSON_PARSER_REF = "generic_json_spatial_trace_parser_v1"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
PLANNING_REF = "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
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

# --------------------------------------------------------------------------- #
# Source -> evidence candidate mapping
# --------------------------------------------------------------------------- #
SOURCE_RGB_FRAME = "rgb_frame_or_video_file"
SOURCE_OBJECT_DETECTION = "object_detection_output"
SOURCE_SEGMENTATION = "segmentation_output"
SOURCE_TRACKING = "tracking_output"
SOURCE_OCR = "ocr_text_output"
SOURCE_DEPTH_VIO = "monocular_depth_or_vio_output"
SOURCE_SCENE_RELATION = "scene_relation_output"

SOURCE_TO_CANDIDATE_TYPE: Dict[str, Tuple[str, ...]] = {
    SOURCE_RGB_FRAME: ("scene_observation_candidate",),
    SOURCE_OBJECT_DETECTION: ("object_evidence_candidate",),
    SOURCE_SEGMENTATION: ("region_evidence_candidate",),
    SOURCE_TRACKING: ("track_evidence_candidate", "dynamic_risk_candidate"),
    SOURCE_OCR: ("text_evidence_candidate",),
    SOURCE_DEPTH_VIO: ("spatial_hint_candidate",),
    SOURCE_SCENE_RELATION: ("scene_relation_candidate",),
}

ALL_EVIDENCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
    "text_evidence_candidate",
    "spatial_hint_candidate",
    "scene_relation_candidate",
)

# Flags that must never be present on an admitted external vision output.
PROHIBITED_OUTPUT_FLAGS: Tuple[str, ...] = (
    "direct_fact_write",
    "rewrite_field_fact",
    "route_activation",
    "direct_action",
    "direct_speech",
    "override_field_identity",
    "bypass_adapter",
    "direct_to_field_task_guidance",
    "native_direct_to_field",
)

ORIGIN_METADATA_REQUIRED_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "confidence",
    "frame_origin_or_file_origin",
    "model_output_origin",
)

# --------------------------------------------------------------------------- #
# Sample files
# --------------------------------------------------------------------------- #
SAMPLES_REL_DIR = (
    "capabilities/field_understanding/"
    "rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "sample_rgb_frame_metadata.json",
    "sample_object_detection_output.json",
    "sample_segmentation_output.json",
    "sample_tracking_output.json",
    "sample_ocr_text_output.json",
    "sample_monocular_depth_vio_output.json",
    "sample_scene_relation_output.json",
    "invalid_missing_source_chain_output.json",
    "invalid_direct_fact_write_ocr_output.json",
    "invalid_segmentation_route_activation_output.json",
    "invalid_tracking_action_trigger_output.json",
    "invalid_depth_field_identity_override_output.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "rgb_scene_object_region_integrated_replay",
    "rgb_ocr_scene_text_integrated_replay",
    "rgb_tracking_dynamic_risk_integrated_replay",
    "rgb_monocular_depth_vio_spatial_hint_replay",
    "rgb_scene_relation_task_context_replay",
    "rgb_integrated_field_task_guidance_replay_path",
    "rgb_observation_only_replay_scope",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_missing_source_chain_rejected",
    "invalid_direct_fact_write_ocr_rejected",
    "invalid_segmentation_route_activation_rejected",
    "invalid_tracking_direct_action_speech_rejected",
    "invalid_depth_vio_field_identity_override_rejected",
    "invalid_native_output_direct_to_field_rejected",
)

FIELD_TASK_GUIDANCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "FieldCandidate",
    "FieldStateCandidate",
    "TaskContextCandidate",
    "TaskEvidenceNeedCandidate",
    "TaskRiskCandidate",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RGBVisionIntegratedEvidenceReplayDryRunProfile",
    "RGBVisionFileInputBundle",
    "RGBVisionSourceAdmissionResult",
    "RGBVisionEvidenceCandidateMappingResult",
    "RGBVisionOCRReplayResult",
    "RGBVisionSegmentationTrackingReplayResult",
    "RGBVisionDepthVIOReplayResult",
    "RGBVisionSceneRelationReplayResult",
    "RGBVisionFieldTaskGuidanceReplayResult",
    "RGBVisionIntegratedEvidenceReplayDryRunDecision",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "rgb_integrated_dryrun_is_not_live_runtime",
    "integrated_validation_mode_must_be_used_no_single_loader_split",
    "rgb_first_remains_default_hardware_baseline",
    "tof_stereo_industrial_depth_remains_optional_auxiliary_only",
    "external_model_output_must_pass_source_admission_and_adapter_mapping",
    "native_vision_output_must_not_enter_field_task_guidance_directly",
    "ocr_output_is_text_evidence_candidate_not_fact",
    "segmentation_output_is_region_evidence_not_route_activation",
    "tracking_output_is_motion_risk_evidence_not_action_speech_trigger",
    "monocular_depth_vio_output_is_spatial_hint_not_field_identity",
    "scene_relation_output_is_relation_candidate_not_final_interpretation",
    "all_source_chain_confidence_origin_metadata_must_be_preserved",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist_before_action_like_guidance",
    "no_live_camera_no_live_sensor_no_real_gps_no_map_api_no_ros",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "commercial_runtime_approval_not_implied",
)

FINAL_DECISION_GO = "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = (
    "RGB_VISION_OCR_SEGMENTATION_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_BLOCKED"
)

NEXT_PHASE_REF = "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only_enforced": True,
    "integrated_validation_mode_used": True,
    "single_loader_validation_not_used": True,
    "real_file_replay_execution_allowed": True,
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
class RGBVisionIntegratedEvidenceReplayDryRunProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    planning_ref: str
    rtab_multi_export_closure_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    interface_adapter_ref: str
    generic_json_spatial_trace_parser_ref: str
    vision_hardware_baseline: str
    depth_hardware_default: str
    tof_stereo_depth_role: str
    system_objective: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    source_to_candidate_type: Dict[str, Tuple[str, ...]]
    field_task_guidance_candidate_types: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RGBVisionFileInputBundle:
    bundle_ref: str
    sample_file: str
    source_ref: str
    item_count: int
    source_chain: str


@dataclass(frozen=True)
class RGBVisionSourceAdmissionResult:
    result_ref: str
    sample_file: str
    source_ref: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    format_ref_ok: bool
    source_chain_present: bool
    confidence_present: bool
    origin_metadata_present: bool
    prohibited_flags_absent: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RGBVisionEvidenceCandidateMappingResult:
    result_ref: str
    source_ref: str
    output_candidate_types: Tuple[str, ...]
    candidate_count: int
    adapter_mapping_used: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    origin_metadata_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionOCRReplayResult:
    result_ref: str
    text_evidence_candidate_generated: bool
    ocr_output_not_fact: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    origin_metadata_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionSegmentationTrackingReplayResult:
    result_ref: str
    region_evidence_candidate_generated: bool
    track_evidence_candidate_generated: bool
    dynamic_risk_candidate_generated: bool
    segmentation_output_not_route_activation: bool
    tracking_output_not_action_trigger: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionDepthVIOReplayResult:
    result_ref: str
    spatial_hint_candidate_generated: bool
    monocular_depth_vio_not_field_identity: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionSceneRelationReplayResult:
    result_ref: str
    scene_relation_candidate_generated: bool
    task_context_can_reference_relation_candidates: bool
    scene_relation_not_final_interpretation: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionFieldTaskGuidanceReplayResult:
    result_ref: str
    field_task_guidance_replay_path_ok: bool
    task_context_can_reference_relation_candidates: bool
    task_risk_can_reference_tracking_and_spatial_hint: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    observation_only_scope_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionIntegratedEvidenceReplayDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    planning_go_verified: bool
    rtab_multi_export_spatial_evidence_replay_closure_go_verified: bool
    field_task_guidance_safety_chain_closure_go_verified: bool
    interface_layer_governance_verified: bool
    model_admission_governance_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
