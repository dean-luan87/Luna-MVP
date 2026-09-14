# -*- coding: utf-8 -*-
"""RGB Vision Roboflow Dataset Integrated Evidence Replay DryRun — types v1.

Admits Roboflow Universe datasets strictly as an EXTERNAL RGB VISION TEST SOURCE
(not Luna fact layer, not auto-trusted labels, not default-commercial, not direct
into Field/Task/Guidance). Roboflow image/annotation samples pass license/dataset/
annotation-format/source-chain admission, then map into evidence candidates via the
external vision interface adapter, candidate-only.

  roboflow image/annotation sample
  -> license / dataset / annotation-format / source_chain admission
  -> external_vision_interface_adapter
  -> object / region / text / track / dynamic_risk / scene_observation evidence candidate
  -> Field / Task / Guidance candidate replay (candidate-only)
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.field_understanding.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun.rgb_vision_ocr_segmentation_integrated_evidence_replay_dryrun_types_v1 import (
    INTERFACE_ADAPTER_REF,
    PROHIBITED_OUTPUT_FLAGS,
    TARGET_ENTRYPOINT,
    TARGET_INTERNAL_FORMAT,
    VISION_HARDWARE_BASELINE,
    DEPTH_HARDWARE_DEFAULT,
    TOF_STEREO_DEPTH_ROLE,
    SYSTEM_OBJECTIVE,
    GENERIC_JSON_PARSER_REF,
)

PHASE_ID = "Phase-RGB-Vision-Roboflow-Dataset-Integrated-Evidence-Replay-DryRun-v1-001"
SCOPE = "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun"
SOURCE_CHAIN = "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "把 Roboflow Universe 数据集严格定位为外部 RGB 视觉测试数据源（非 Luna 事实层、非自动可信标签、"
    "非默认可商用、非直进 Field/Task/Guidance）。Roboflow 图片/标注样例先通过 license / dataset / "
    "annotation 格式 / source_chain 准入，再经 external vision interface adapter 映射成 evidence "
    "candidate，全程 candidate-only。允许读取本地受控样例；不接 live camera，不启动真实视觉 runtime，"
    "不触发 navigation / action / speech / fact_write。集中验证，不拆单一 loader。"
)

RUNTIME_TRIAL_MODE = "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun_only"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# Roboflow positioning
EXTERNAL_TEST_SOURCE = "roboflow_universe"
ROBOFLOW_ROLE = "external_rgb_vision_test_source"

# Reused boundary constants (kept consistent with the base RGB vision dry-run)
_INTERFACE_ADAPTER_REF = INTERFACE_ADAPTER_REF
_TARGET_ENTRYPOINT = TARGET_ENTRYPOINT
_PROHIBITED_OUTPUT_FLAGS = PROHIBITED_OUTPUT_FLAGS

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
RGB_VISION_DRYRUN_REF = "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-DryRun-v1-001"
RGB_VISION_PLANNING_REF = (
    "Phase-RGB-Vision-OCR-Segmentation-Integrated-Evidence-Replay-Planning-v1-001"
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
# Annotation formats + admission requirements
# --------------------------------------------------------------------------- #
ROBOFLOW_FORMAT_REF = "roboflow_dataset"
RECOGNIZED_ANNOTATION_FORMATS: Tuple[str, ...] = ("yolo", "coco", "voc", "json")

DATASET_ADMISSION_REQUIRED_FIELDS: Tuple[str, ...] = (
    "license_ref",
    "dataset_origin",
    "annotation_format_recognized",
    "source_chain",
    "confidence",
)

# Annotation type -> evidence candidate
ANNOTATION_TYPE_TO_CANDIDATE: Dict[str, Tuple[str, ...]] = {
    "bbox": ("object_evidence_candidate",),
    "segmentation": ("region_evidence_candidate",),
    "polygon": ("region_evidence_candidate",),
    "text": ("text_evidence_candidate",),
    "track": ("track_evidence_candidate", "dynamic_risk_candidate"),
}

ALL_EVIDENCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "scene_observation_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "text_evidence_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
)

# --------------------------------------------------------------------------- #
# Sample files
# --------------------------------------------------------------------------- #
SAMPLES_REL_DIR = (
    "capabilities/field_understanding/"
    "rgb_vision_roboflow_dataset_integrated_evidence_replay_dryrun/samples"
)

SAMPLE_FILES: Tuple[str, ...] = (
    "sample_roboflow_yolo_dataset.json",
    "sample_roboflow_coco_dataset.json",
    "sample_roboflow_voc_dataset.json",
    "sample_roboflow_ocr_placeholder.json",
    "sample_roboflow_tracking_placeholder.json",
    "invalid_roboflow_missing_license.json",
    "invalid_roboflow_missing_dataset_origin.json",
    "invalid_roboflow_unrecognized_annotation_format.json",
    "invalid_roboflow_missing_source_chain.json",
    "invalid_roboflow_direct_fact_write.json",
    "invalid_roboflow_model_native_direct_to_field.json",
)

POSITIVE_CASE_REFS: Tuple[str, ...] = (
    "roboflow_yolo_object_replay",
    "roboflow_coco_object_region_replay",
    "roboflow_voc_object_replay",
    "roboflow_ocr_placeholder_text_replay",
    "roboflow_tracking_placeholder_dynamic_risk_replay",
    "roboflow_license_source_admission_metadata_preserved",
    "roboflow_integrated_field_task_guidance_replay_path",
)

NEGATIVE_CASE_REFS: Tuple[str, ...] = (
    "invalid_roboflow_missing_license_rejected",
    "invalid_roboflow_missing_dataset_origin_rejected",
    "invalid_roboflow_unrecognized_annotation_format_rejected",
    "invalid_roboflow_missing_source_chain_rejected",
    "invalid_roboflow_direct_fact_write_or_route_activation_rejected",
    "invalid_roboflow_model_native_output_direct_to_field_rejected",
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
    "RGBVisionRoboflowIntegratedEvidenceReplayDryRunProfile",
    "RoboflowDatasetInputBundle",
    "RoboflowDatasetSourceAdmissionResult",
    "RoboflowAnnotationFormatRecognitionResult",
    "RoboflowEvidenceCandidateMappingResult",
    "RoboflowOCRTrackingPlaceholderReplayResult",
    "RoboflowFieldTaskGuidanceReplayResult",
    "RoboflowDatasetBoundaryResult",
    "RGBVisionRoboflowIntegratedEvidenceReplayDryRunDecision",
)

DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "roboflow_dataset_is_external_test_source_not_luna_fact_layer",
    "roboflow_annotation_is_not_auto_trusted_label",
    "roboflow_license_is_not_default_commercial",
    "roboflow_model_output_must_not_enter_field_task_guidance_directly",
    "license_must_be_present",
    "dataset_origin_must_be_present",
    "annotation_format_must_be_recognized",
    "source_chain_must_be_present",
    "confidence_must_be_present",
    "no_direct_fact_write",
    "no_direct_route_activation",
    "external_model_native_output_must_not_directly_enter_field",
    "external_output_must_pass_source_admission_and_adapter_mapping",
    "all_source_chain_license_dataset_annotation_origin_confidence_preserved",
    "field_task_guidance_replay_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist_before_action_like_guidance",
    "rgb_first_remains_default_hardware_baseline",
    "no_live_camera_no_live_sensor_no_real_gps_no_map_api_no_ros",
    "no_navigation_no_action_no_speech_no_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "commercial_data_source_and_runtime_approval_not_implied",
    "integrated_validation_mode_must_be_used_no_single_loader_split",
)

FINAL_DECISION_GO = "RGB_VISION_ROBOFLOW_DATASET_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RGB_VISION_ROBOFLOW_DATASET_INTEGRATED_EVIDENCE_REPLAY_DRYRUN_BLOCKED"

NEXT_PHASE_REF = "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "candidate_only_enforced": True,
    "integrated_validation_mode_used": True,
    "single_loader_validation_not_used": True,
    "real_file_replay_execution_allowed": True,
    "runtime_activation_allowed": False,
    "roboflow_dataset_as_fact_layer": False,
    "roboflow_annotation_auto_trusted": False,
    "roboflow_license_default_commercial": False,
    "roboflow_model_output_direct_to_field": False,
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
    "commercial_data_source_approved": False,
}


@dataclass(frozen=True)
class RGBVisionRoboflowIntegratedEvidenceReplayDryRunProfile:
    profile_ref: str
    phase_id: str
    controlled_trial_governance_template_ref: str
    rgb_vision_dryrun_ref: str
    field_task_guidance_safety_chain_closure_ref: str
    interface_adapter_ref: str
    generic_json_spatial_trace_parser_ref: str
    external_test_source: str
    roboflow_role: str
    vision_hardware_baseline: str
    depth_hardware_default: str
    tof_stereo_depth_role: str
    system_objective: str
    target_internal_format: str
    target_entrypoint: str
    runtime_trial_mode: str
    recognized_annotation_formats: Tuple[str, ...]
    dataset_admission_required_fields: Tuple[str, ...]
    annotation_type_to_candidate: Dict[str, Tuple[str, ...]]
    field_task_guidance_candidate_types: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RoboflowDatasetInputBundle:
    bundle_ref: str
    sample_file: str
    annotation_format: str
    image_count: int
    annotation_count: int
    source_chain: str


@dataclass(frozen=True)
class RoboflowDatasetSourceAdmissionResult:
    result_ref: str
    sample_file: str
    file_source_admitted: bool
    controlled_samples_path_ok: bool
    format_ref_ok: bool
    license_present: bool
    dataset_origin_present: bool
    annotation_format_recognized: bool
    source_chain_present: bool
    confidence_present: bool
    prohibited_flags_absent: bool
    rejection_reasons: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RoboflowAnnotationFormatRecognitionResult:
    result_ref: str
    annotation_format: str
    recognized: bool
    recognized_formats: Tuple[str, ...]
    source_chain: str


@dataclass(frozen=True)
class RoboflowEvidenceCandidateMappingResult:
    result_ref: str
    sample_file: str
    output_candidate_types: Tuple[str, ...]
    candidate_count: int
    adapter_mapping_used: bool
    source_chain_preserved: bool
    confidence_preserved: bool
    license_ref_preserved: bool
    dataset_ref_preserved: bool
    annotation_origin_preserved: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RoboflowOCRTrackingPlaceholderReplayResult:
    result_ref: str
    text_evidence_candidate_generated: bool
    track_evidence_candidate_generated: bool
    dynamic_risk_candidate_generated: bool
    ocr_output_not_fact: bool
    tracking_output_not_action_trigger: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RoboflowFieldTaskGuidanceReplayResult:
    result_ref: str
    field_task_guidance_replay_path_ok: bool
    task_context_can_reference_evidence_candidates: bool
    task_risk_can_reference_tracking_evidence: bool
    guidance_candidate_remains_candidate: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool
    candidate_only: bool
    source_chain: str


@dataclass(frozen=True)
class RoboflowDatasetBoundaryResult:
    result_ref: str
    missing_license_rejected: bool
    missing_dataset_origin_rejected: bool
    unrecognized_annotation_format_rejected: bool
    missing_source_chain_rejected: bool
    direct_fact_write_or_route_activation_rejected: bool
    model_native_output_direct_to_field_rejected: bool
    source_chain: str


@dataclass(frozen=True)
class RGBVisionRoboflowIntegratedEvidenceReplayDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    rgb_vision_integrated_evidence_replay_dryrun_go_verified: bool
    field_task_guidance_safety_chain_closure_go_verified: bool
    interface_layer_governance_verified: bool
    model_admission_governance_verified: bool
    controlled_trial_governance_template_ref_ok: bool
    final_decision: str
    real_file_replay_execution_allowed: bool = True
    runtime_activation_allowed: bool = False


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
