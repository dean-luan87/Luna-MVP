# -*- coding: utf-8 -*-
"""Recognition Model Output Adapter DryRun — types v1.

Validates, with mock-but-file-based model output samples, whether the seven
recognition-model output families can be mapped through the
RecognitionModelOutputAdapter into Luna evidence candidates that are compatible
with the already-frozen Phase-One environment cognition evidence main chain.

  model output (mock file)
  -> RecognitionModelOutputAdapter
  -> Luna evidence candidate
  -> evidence main chain compatible output

No real model inference, no real image/video recognition, no model download /
repo clone / runtime build / tuning / dataset usage / dataset download / live
camera-sensor, and no navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001"
SCOPE = "recognition_model_output_adapter_dryrun"
SOURCE_CHAIN = "recognition_model_output_adapter_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model Invocation Feasibility DryRun，执行模型输出 Adapter dry-run。"
    "使用 mock-but-file-based 的模型输出样例，验证 OCR / object detection / segmentation / tracking / "
    "depth-spatial-hint / visual symbol / scene relation 七类输出能否通过 RecognitionModelOutputAdapter "
    "映射为 Luna evidence candidate，并满足已冻结的 Phase One Environment Cognition Evidence Main Chain "
    "接入要求。不跑真实模型，不做真实图片识别，不下载模型，不 clone repo，不 build runtime，不调优，"
    "不用训练数据，不下载数据集，不接 live camera/sensor，不触发 navigation/action/speech/fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_output_adapter_dryrun_only"
INVOCATION_FEASIBILITY_DRYRUN_REF = "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"
SYSTEM_ADMISSION_PLANNING_REF = (
    "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
MAIN_CHAIN_CLOSURE_REF = TARGET_CHAIN_REF
RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
)
RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF = (
    "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Model families
# --------------------------------------------------------------------------- #
MODEL_FAMILY_IDS: Tuple[str, ...] = (
    "ocr_model_family",
    "object_detection_model_family",
    "segmentation_model_family",
    "tracking_model_family",
    "depth_spatial_hint_model_family",
    "visual_symbol_model_family",
    "scene_relation_model_family",
)

# family -> generated candidate types
FAMILY_TO_CANDIDATES: Dict[str, Tuple[str, ...]] = {
    "ocr_model_family": ("text_evidence_candidate",),
    "object_detection_model_family": ("object_evidence_candidate",),
    "segmentation_model_family": ("region_evidence_candidate",),
    "tracking_model_family": ("track_evidence_candidate", "dynamic_risk_candidate"),
    "depth_spatial_hint_model_family": ("spatial_hint_candidate",),
    "visual_symbol_model_family": (
        "color_evidence_candidate",
        "shape_evidence_candidate",
        "visual_symbol_candidate",
        "symbol_meaning_candidate",
    ),
    "scene_relation_model_family": ("scene_relation_candidate", "attribute_candidate"),
}

# family -> safety boundary
FAMILY_BOUNDARY: Dict[str, str] = {
    "ocr_model_family": "ocr_output_is_not_fact",
    "object_detection_model_family": "object_identity_is_not_fact",
    "segmentation_model_family": "segmentation_is_not_route_activation",
    "tracking_model_family": "tracking_is_not_action_trigger",
    "depth_spatial_hint_model_family": "depth_vio_does_not_override_field_identity",
    "visual_symbol_model_family": "color_shape_symbol_not_fact_meaning_requires_context_validation",
    "scene_relation_model_family": "scene_relation_is_not_final_interpretation",
}

# All 12 candidate types covered by the full bundle.
ALL_CANDIDATE_TYPES: Tuple[str, ...] = (
    "text_evidence_candidate",
    "object_evidence_candidate",
    "region_evidence_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
    "spatial_hint_candidate",
    "color_evidence_candidate",
    "shape_evidence_candidate",
    "visual_symbol_candidate",
    "symbol_meaning_candidate",
    "scene_relation_candidate",
    "attribute_candidate",
)

CANDIDATE_GENERATED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_generated" for c in ALL_CANDIDATE_TYPES
)

FAMILY_MAPPING_GO_KEYS: Dict[str, str] = {
    "ocr_model_family": "ocr_output_adapter_mapping_ok",
    "object_detection_model_family": "object_detection_output_adapter_mapping_ok",
    "segmentation_model_family": "segmentation_output_adapter_mapping_ok",
    "tracking_model_family": "tracking_output_adapter_mapping_ok",
    "depth_spatial_hint_model_family": "depth_spatial_hint_output_adapter_mapping_ok",
    "visual_symbol_model_family": "visual_symbol_output_adapter_mapping_ok",
    "scene_relation_model_family": "scene_relation_output_adapter_mapping_ok",
}

# --------------------------------------------------------------------------- #
# Admission fields
# --------------------------------------------------------------------------- #
REQUIRED_MODEL_OUTPUT_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_family",
    "model_version_ref",
    "model_origin",
    "license_ref",
    "source_chain",
    "input_ref",
    "output_schema_ref",
    "confidence",
    "frame_ref_or_timestamp_ms",
    "adapter_mapping_ref",
    "allowed_use",
    "commercial_use_status",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "license_ref",
    "model_origin",
    "confidence",
    "adapter_mapping_ref",
)

# --------------------------------------------------------------------------- #
# Prohibited flags (any True -> reject)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "native_output_direct_to_field",
    "fact_write_requested",
    "route_activation_requested",
    "direct_action_requested",
    "direct_speech_requested",
    "direct_navigation_requested",
    "field_identity_override_requested",
    "final_interpretation_requested",
    "real_inference_requested",
    "model_download_requested",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "ocr_output_adapter_mapping",
    "object_detection_output_adapter_mapping",
    "segmentation_output_adapter_mapping",
    "tracking_output_adapter_mapping",
    "depth_spatial_hint_output_adapter_mapping",
    "visual_symbol_output_adapter_mapping",
    "scene_relation_output_adapter_mapping",
    "multi_family_output_adapter_coverage",
    "evidence_main_chain_compatibility_check",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_source_chain",
    "invalid_missing_license_ref",
    "invalid_missing_model_origin",
    "invalid_missing_confidence",
    "invalid_missing_adapter_mapping_ref",
    "invalid_native_output_direct_to_field",
    "invalid_ocr_fact_write",
    "invalid_segmentation_route_activation",
    "invalid_tracking_direct_action",
    "invalid_depth_field_identity_override",
    "invalid_visual_symbol_direct_navigation",
    "invalid_scene_relation_final_interpretation",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_model_output_adapter_dryrun_only",
    "mock_file_based_model_output_is_allowed",
    "real_inference_is_not_allowed",
    "real_image_video_recognition_is_not_allowed",
    "model_download_is_not_allowed",
    "repo_clone_is_not_allowed",
    "model_build_is_not_allowed",
    "model_tuning_is_deferred",
    "dataset_usage_is_deferred",
    "training_is_not_allowed",
    "model_output_must_pass_recognition_model_output_adapter",
    "native_model_output_must_not_enter_field_task_guidance_directly",
    "all_model_outputs_become_evidence_candidate_first",
    "ocr_output_is_not_fact",
    "object_identity_is_not_fact",
    "segmentation_is_not_route_activation",
    "tracking_is_not_action_trigger",
    "depth_vio_does_not_override_field_identity",
    "color_shape_symbol_is_not_fact",
    "visual_symbol_meaning_requires_context_validation",
    "scene_relation_is_not_final_interpretation",
    "conflict_uncertainty_does_not_directly_write_fact_or_trigger_action_speech_navigation",
    "field_task_guidance_path_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "no_live_camera_live_sensor_gps_map_api_ros",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelOutputAdapterDryRunProfile",
    "RecognitionModelOutputFileBundle",
    "RecognitionModelOutputAdmissionResult",
    "RecognitionModelOutputAdapterMappingResult",
    "RecognitionModelEvidenceCandidateResult",
    "RecognitionModelCandidateCoverageResult",
    "RecognitionModelEvidenceMainChainCompatibilityResult",
    "RecognitionModelOutputAdapterBoundaryResult",
    "RecognitionModelOutputAdapterDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_OUTPUT_ADAPTER_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "model_output_adapter_dryrun_allowed": True,
    "mock_file_based_model_output_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "real_image_recognition_allowed": False,
    "model_download_allowed": False,
    "model_repo_clone_allowed": False,
    "model_build_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "dataset_download_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelOutputAdapterDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    invocation_feasibility_dryrun_ref: str
    system_admission_planning_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    model_family_ids: Tuple[str, ...]
    required_model_output_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelOutputAdmissionResult:
    model_family: str
    accepted: bool
    reject_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelEvidenceCandidateResult:
    candidate_type: str
    source_model_family: str
    boundary: str
    candidate_only: bool


@dataclass(frozen=True)
class RecognitionModelCandidateCoverageResult:
    coverage_ref: str
    covered_candidate_types: Tuple[str, ...]
    coverage_count: int
    coverage_complete: bool


@dataclass(frozen=True)
class RecognitionModelEvidenceMainChainCompatibilityResult:
    compatibility_ref: str
    output_candidate_compatible_with_main_chain: bool
    field_task_guidance_candidate_only: bool
    guidance_candidate_not_runtime_navigation: bool
    speech_gate_candidate_not_tts: bool
    action_safety_candidate_exists: bool


@dataclass
class RecognitionModelCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    model_family: str = ""
    generated_candidates: Tuple[str, ...] = field(default_factory=tuple)
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelOutputAdapterDryRunDecision:
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
