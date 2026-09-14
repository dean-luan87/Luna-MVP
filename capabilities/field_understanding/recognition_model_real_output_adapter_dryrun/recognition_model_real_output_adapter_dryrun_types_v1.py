# -*- coding: utf-8 -*-
"""Recognition Model Real Output Adapter DryRun — types v1.

First phase that permits *controlled* real inference, with a very narrow scope:
P0 models, local controlled static sample images, offline file input, a single /
minimal inference, output written to this phase's artifact, output forced through
the RecognitionModelOutputAdapter, and output allowed only to become an evidence
candidate.

  P0 local sample image (offline file)
  -> minimal real inference (P0 model, if locally available)
  -> real model output record
  -> RecognitionModelOutputAdapter
  -> Luna evidence candidate (candidate-only)

Core principle preserved: Luna's long-term core remains emotional multimodality +
brain / world understanding. Recognition models serve Luna's cognitive brain; they
do NOT drive action execution and are NOT wired into a VLA action chain. No live
camera / sensor, no continuous runtime, no dataset batch inference, no training /
tuning, no commercial runtime, no main-chain integration, and no
navigation/action/speech/fact_write in this phase.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001"
SCOPE = "recognition_model_real_output_adapter_dryrun"
SOURCE_CHAIN = "recognition_model_real_output_adapter_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Download/Install DryRun,执行 P0 真模型输出 Adapter dry-run。首次允许受控真实 "
    "inference,但仅限 P0 小样例、离线本地静态图片、单次/小样例、非 live、非 runtime、非调优、"
    "非数据集、非商业 runtime。真实模型输出必须经 RecognitionModelOutputAdapter,只能成为 evidence "
    "candidate,不得进入 action/speech/navigation/fact_write。RapidOCR→text;YOLO lightweight→object"
    "(test-only,commercial_runtime_approved=false);OpenCV rule-based→color/shape/visual_symbol/"
    "symbol_meaning。核心原则:Luna 仍以情感多模态 + 大脑/世界理解为核心,识别模型服务认知大脑,"
    "不接 VLA 行动链、不做行动执行。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotional_multimodal_brain_and_world_understanding_first_"
    "recognition_models_serve_cognition_not_action_execution_no_vla_action_chain"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_real_output_adapter_dryrun_only"
DOWNLOAD_INSTALL_DRYRUN_REF = "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001"
DOWNLOAD_LICENSE_PLANNING_REF = (
    "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001"
)
INVOCATION_FEASIBILITY_DRYRUN_REF = (
    "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"
)
MOCK_OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001"
SYSTEM_ADMISSION_PLANNING_REF = (
    "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
)
RGB_VISION_SLAM_CROSS_MODAL_CLOSURE_REF = (
    "Phase-RGB-Vision-SLAM-Spatial-Evidence-Cross-Modal-Integrated-Closure-v1-001"
)
FIELD_TASK_GUIDANCE_SAFETY_CHAIN_CLOSURE_REF = (
    "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# P0 real targets
# --------------------------------------------------------------------------- #
P0_REAL_TARGET_IDS: Tuple[str, ...] = (
    "rapidocr_p0",
    "yolo_lightweight_p0",
    "opencv_visual_symbol_p0",
)

# target -> candidate types
P0_TARGET_TO_CANDIDATES: Dict[str, Tuple[str, ...]] = {
    "rapidocr_p0": ("text_evidence_candidate",),
    "yolo_lightweight_p0": ("object_evidence_candidate",),
    "opencv_visual_symbol_p0": (
        "color_evidence_candidate",
        "shape_evidence_candidate",
        "visual_symbol_candidate",
        "symbol_meaning_candidate",
    ),
}

P0_TARGET_BOUNDARY: Dict[str, str] = {
    "rapidocr_p0": "ocr_output_is_not_fact",
    "yolo_lightweight_p0": "object_identity_is_not_fact_yolo_test_only_unless_commercial_license_cleared",
    "opencv_visual_symbol_p0": (
        "color_shape_symbol_not_fact_symbol_meaning_requires_context_validation"
    ),
}

# Optional (may be unavailable -> declared unavailable record, not blocker).
OPTIONAL_AVAILABILITY_TARGETS: Tuple[str, ...] = ("rapidocr_p0", "yolo_lightweight_p0")
# Mandatory (rule runtime must produce candidates).
MANDATORY_AVAILABILITY_TARGETS: Tuple[str, ...] = ("opencv_visual_symbol_p0",)

# --------------------------------------------------------------------------- #
# Real output record fields
# --------------------------------------------------------------------------- #
REQUIRED_REAL_OUTPUT_FIELDS: Tuple[str, ...] = (
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
    "real_output",
    "inference_scope",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "license_ref",
    "model_origin",
    "confidence",
    "adapter_mapping_ref",
)

PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "commercial_runtime_ready",
    "commercial_runtime_requested",
    "fact_write_requested",
    "route_activation_requested",
    "direct_action_requested",
    "direct_speech_requested",
    "direct_navigation_requested",
    "field_identity_override_requested",
    "final_interpretation_requested",
    "native_output_direct_to_field",
    "evidence_main_chain_integration_requested",
    "live_camera_requested",
    "live_sensor_requested",
    "dataset_batch_inference_requested",
    "training_requested",
    "model_tuning_requested",
)

INFERENCE_SCOPE_VALUE = "p0_controlled_sample_only"

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "rapidocr_real_output_adapter_mapping",
    "yolo_lightweight_real_output_adapter_mapping",
    "opencv_visual_symbol_real_output_adapter_mapping",
    "p0_multi_model_real_output_coverage",
    "p0_real_output_adapter_boundary_check",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_source_chain",
    "invalid_missing_license_ref",
    "invalid_missing_model_origin",
    "invalid_missing_confidence",
    "invalid_yolo_commercial_runtime_claim",
    "invalid_ocr_fact_write",
    "invalid_visual_symbol_direct_navigation",
    "invalid_native_output_direct_to_field",
    "invalid_main_chain_integration_requested",
    "invalid_live_camera_sensor_requested",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_p0_real_model_output_adapter_dryrun_only",
    "real_inference_is_allowed_only_for_p0_local_controlled_samples",
    "live_camera_is_not_allowed",
    "live_sensor_is_not_allowed",
    "dataset_batch_inference_is_not_allowed",
    "dataset_usage_is_not_allowed",
    "training_is_not_allowed",
    "model_tuning_is_not_allowed",
    "evidence_main_chain_integration_dryrun_is_not_executed_in_this_phase",
    "recognition_model_output_adapter_must_be_used",
    "native_model_output_must_not_enter_field_task_guidance_directly",
    "all_real_model_outputs_become_evidence_candidate_first",
    "ocr_output_is_not_fact",
    "object_identity_is_not_fact",
    "color_shape_visual_symbol_is_not_fact",
    "visual_symbol_meaning_requires_context_validation",
    "yolo_remains_test_only_unless_commercial_license_cleared",
    "commercial_runtime_is_not_approved",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist_before_action_like_use",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
    "luna_remains_brain_cognition_first_not_action_execution",
)

DEFINED_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelRealOutputAdapterDryRunProfile",
    "P0RealInferenceInputSample",
    "P0RealModelOutputRecord",
    "P0RealModelOutputAdmissionResult",
    "P0RecognitionModelOutputAdapterMappingResult",
    "P0EvidenceCandidateResult",
    "P0RealOutputCoverageResult",
    "P0RealOutputBoundaryResult",
    "RecognitionModelRealOutputAdapterDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_REAL_OUTPUT_ADAPTER_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "real_model_output_adapter_dryrun_allowed": True,
    "p0_real_inference_allowed": True,
    "local_controlled_sample_only": True,
    "offline_file_input_only": True,
    "rapidocr_real_output_allowed": True,
    "yolo_lightweight_real_output_allowed": True,
    "opencv_visual_symbol_real_output_allowed": True,
    "recognition_model_output_adapter_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "dataset_batch_inference_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "model_tuning_allowed": False,
    "evidence_main_chain_integration_dryrun_allowed": False,
    "dataset_download_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelRealOutputAdapterDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    download_install_dryrun_ref: str
    download_license_planning_ref: str
    invocation_feasibility_dryrun_ref: str
    mock_output_adapter_dryrun_ref: str
    system_admission_planning_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    p0_real_target_ids: Tuple[str, ...]
    required_real_output_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class P0RealInferenceInputSample:
    sample_ref: str
    target: str
    file_path: str
    offline_file_input: bool
    local_controlled_sample: bool


@dataclass(frozen=True)
class P0RealModelOutputAdmissionResult:
    target: str
    model_id: str
    accepted: bool
    reject_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class P0EvidenceCandidateResult:
    candidate_type: str
    source_target: str
    boundary: str
    candidate_only: bool


@dataclass
class P0RealOutputCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    target: str = ""
    model_available: bool = False
    availability_state: str = ""
    real_inference_executed: bool = False
    generated_candidates: Tuple[str, ...] = field(default_factory=tuple)
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelRealOutputAdapterDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    p0_real_target_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    blocker_count: int
    final_decision: str


def real_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
