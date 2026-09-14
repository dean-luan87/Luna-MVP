# -*- coding: utf-8 -*-
"""Recognition Model Evidence Main Chain Integration DryRun — types v1.

Verifies that the *real* model output evidence candidates produced (and sealed)
by the previous phase can enter the frozen Phase-One environment cognition
evidence main chain and flow along the Field / Task / Guidance candidate path —
while preserving Luna's brain / cognition-first principle.

  sealed real model output artifact (real_ocr_output.json / real_visual_symbol_output.json /
      YOLO declared_unavailable record)
  -> RecognitionModelOutputAdapter evidence candidate (reused, not re-inferred)
  -> Phase One Evidence Main Chain ingress
  -> FieldSynthesisCandidate / TaskContextCandidate / GuidanceCandidate /
     SpeechGateCandidate / ActionSafetyCandidate (candidate-only)

This phase does NOT re-run inference, does NOT download YOLO weights, does NOT
recognize new images, does NOT touch live camera/sensor, does NOT tune models,
does NOT use datasets/training, and triggers NO navigation/action/speech/
fact_write. No VLA action chain is permitted.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001"
SCOPE = "recognition_model_evidence_main_chain_integration_dryrun"
SOURCE_CHAIN = "recognition_model_evidence_main_chain_integration_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Real Output Adapter DryRun,执行真实模型输出 candidate 进入 Luna 一期 Evidence Main "
    "Chain 的 integrated dry-run。不再验证模型能否调用,而是验证真实模型输出经 Adapter 生成的 evidence "
    "candidate 能否接入 Field/Task/Guidance candidate path,并保持 Luna brain/cognition first。复用上一"
    "阶段真实输出 artifact(real_ocr_output.json / real_visual_symbol_output.json / YOLO "
    "declared_unavailable record),不重新 inference、不下载 YOLO 权重、不跑新图片、不接 live camera/"
    "sensor、不调优、不用数据集、不训练,不触发 navigation/action/speech/fact_write,不允许 VLA 行动链。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "recognition_candidates_feed_cognition_not_action_no_vla_action_chain"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_evidence_main_chain_integration_dryrun_only"
REAL_OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001"
DOWNLOAD_INSTALL_DRYRUN_REF = "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001"
DOWNLOAD_LICENSE_PLANNING_REF = (
    "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001"
)
MOCK_OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001"
INVOCATION_FEASIBILITY_DRYRUN_REF = (
    "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"
)
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
GOVERNANCE_CLOSURE_REF = (
    "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001"
)
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-Recognition-Model-P0-Integration-Closure-v1-001"

# Sealed real-output artifacts reused from the previous phase.
REUSED_REAL_OUTPUT_ARTIFACTS: Tuple[str, ...] = (
    "real_ocr_output.json",
    "real_visual_symbol_output.json",
)
PREV_PHASE_ARTIFACT_DIR_REL = (
    "_tmp_eval_out/recognition_model_real_output_adapter_dryrun_v1_smoke_v0"
)

# --------------------------------------------------------------------------- #
# Candidate admission
# --------------------------------------------------------------------------- #
EVIDENCE_CANDIDATE_TYPES: Tuple[str, ...] = (
    "text_evidence_candidate",
    "color_evidence_candidate",
    "shape_evidence_candidate",
    "visual_symbol_candidate",
    "symbol_meaning_candidate",
)

REQUIRED_CANDIDATE_FIELDS: Tuple[str, ...] = (
    "candidate_type",
    "source_chain",
    "confidence",
)
REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = ("source_chain", "confidence")

# Availability records (e.g. YOLO declared_unavailable) skip the confidence check.
AVAILABILITY_RECORD_KIND = "model_availability"
REQUIRED_AVAILABILITY_FIELDS: Tuple[str, ...] = ("source_chain", "availability_state")

PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "direct_fact_write_requested",
    "fact_write_requested",
    "direct_navigation_requested",
    "runtime_navigation_requested",
    "guidance_runtime_navigation_requested",
    "speech_gate_tts_requested",
    "tts_activation_requested",
    "direct_action_requested",
    "action_trigger_requested",
    "vla_action_chain_requested",
    "vla_action_chain_injected",
    "treat_unavailable_as_blocker",
    "yolo_weight_download_requested",
    "model_download_requested",
    "model_tuning_requested",
    "dataset_usage_requested",
    "training_requested",
    "new_inference_requested",
    "new_image_recognition_requested",
)

# --------------------------------------------------------------------------- #
# Main chain candidate path outputs
# --------------------------------------------------------------------------- #
MAIN_CHAIN_PATH_CANDIDATES: Tuple[str, ...] = (
    "FieldSynthesisCandidate",
    "TaskContextCandidate",
    "TaskRiskCandidate",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
)

# Derived hint / hypothesis candidates produced on ingress.
DERIVED_CANDIDATE_TYPES: Tuple[str, ...] = (
    "text_observation_candidate",
    "facility_text_hint_candidate",
    "exit_text_hint_candidate",
    "visual_symbol_observation_candidate",
    "direction_hint_candidate",
    "exit_direction_candidate",
    "cross_modal_consistency_candidate",
    "exit_sign_hypothesis_candidate",
    "field_affordance_hint_candidate",
    "model_availability_state_candidate",
    "object_detection_unavailable_record",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "real_ocr_candidate_main_chain_ingress",
    "real_visual_symbol_candidate_main_chain_ingress",
    "real_ocr_visual_symbol_cross_validation",
    "yolo_declared_unavailable_non_blocker_ingress",
    "real_p0_candidate_bundle_main_chain_path",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_candidate_missing_source_chain",
    "invalid_candidate_missing_confidence",
    "invalid_candidate_direct_fact_write",
    "invalid_visual_symbol_direct_navigation",
    "invalid_guidance_candidate_runtime_navigation",
    "invalid_speech_gate_tts_activation",
    "invalid_action_trigger_from_candidate",
    "invalid_yolo_unavailable_treated_as_blocker",
    "invalid_vla_action_chain_injected",
    "invalid_model_tuning_dataset_usage",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_evidence_main_chain_integration_dryrun_only",
    "it_reuses_sealed_real_model_output_artifacts",
    "new_real_inference_is_not_allowed",
    "new_image_video_recognition_is_not_allowed",
    "yolo_weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "model_tuning_is_deferred",
    "dataset_usage_is_deferred",
    "training_is_not_allowed",
    "ocr_output_is_not_fact",
    "visual_symbol_meaning_is_not_fact",
    "ocr_plus_visual_symbol_consistency_remains_hypothesis_candidate",
    "exit_text_does_not_directly_activate_route",
    "direction_symbol_does_not_directly_activate_navigation",
    "field_synthesis_candidate_must_not_write_fact",
    "task_context_candidate_must_not_become_final_task_decision",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_trigger_tts",
    "action_safety_candidate_must_not_trigger_action",
    "yolo_unavailable_is_non_blocker_if_declared",
    "no_navigation_action_speech_fact_write",
    "no_live_camera_live_sensor_gps_map_api_ros",
    "vla_action_chain_is_not_allowed_in_current_phase",
    "luna_remains_emotion_multimodal_brain_cognition_first",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DEFINED_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelEvidenceMainChainIntegrationDryRunProfile",
    "RealModelEvidenceCandidateBundle",
    "RealModelEvidenceCandidateAdmissionResult",
    "EvidenceMainChainIngressResult",
    "FieldSynthesisCandidateResult",
    "TaskContextCandidateResult",
    "GuidanceCandidateResult",
    "SpeechGateCandidateResult",
    "ActionSafetyCandidateResult",
    "RealModelMainChainBoundaryResult",
    "RecognitionModelEvidenceMainChainIntegrationDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "real_model_output_reuse_allowed": True,
    "evidence_main_chain_integration_dryrun_allowed": True,
    "field_task_guidance_candidate_path_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "new_image_recognition_allowed": False,
    "model_download_allowed": False,
    "yolo_weight_download_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "dataset_download_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelEvidenceMainChainIntegrationDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    real_output_adapter_dryrun_ref: str
    download_install_dryrun_ref: str
    mock_output_adapter_dryrun_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    reused_real_output_artifacts: Tuple[str, ...]
    required_candidate_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    main_chain_path_candidates: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RealModelEvidenceCandidateAdmissionResult:
    candidate_type: str
    accepted: bool
    reject_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class EvidenceMainChainIngressResult:
    ingress_ref: str
    admitted_candidate_types: Tuple[str, ...]
    generated_candidate_types: Tuple[str, ...]
    candidate_only: bool


@dataclass
class MainChainIntegrationCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    admitted_candidates: Tuple[str, ...] = field(default_factory=tuple)
    generated_candidates: Tuple[str, ...] = field(default_factory=tuple)
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelEvidenceMainChainIntegrationDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    real_output_artifact_ref_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    blocker_count: int
    final_decision: str


def integration_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
