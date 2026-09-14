# -*- coding: utf-8 -*-
"""Recognition Model P0 Integration Closure — types v1.

Seals the full P0 recognition-model integration arc as a stable baseline:

  System Admission Planning
  -> Invocation Feasibility DryRun
  -> Mock Output Adapter DryRun (contract)
  -> Download / License / Local Availability Planning
  -> Download / Install DryRun
  -> Real Output Adapter DryRun (first controlled real inference)
  -> Evidence Main Chain Integration DryRun
  -> Field / Task / Guidance candidate path

Closure-only: no new model, no new inference, no YOLO weight download, no tuning,
no dataset usage, no live camera/sensor, and no navigation/action/speech/
fact_write. Luna remains emotion-multimodal brain / cognition first; the VLA
action chain is explicitly excluded from current scope.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-P0-Integration-Closure-v1-001"
SCOPE = "recognition_model_p0_integration_closure"
SOURCE_CHAIN = "recognition_model_p0_integration_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "基于已 GO 的 Evidence Main Chain Integration DryRun,对 P0 识别模型接入链路做 integration closure。"
    "把从模型接入体系规划、调用可行性、mock 输出 adapter、下载/license/本地可用性、下载/install、"
    "本地真实 inference、真实输出 adapter、evidence main chain ingress 到 Field/Task/Guidance candidate "
    "path 的完整链路封成稳定基线。本阶段只封口:不新增模型、不重新 inference、不下载 YOLO 权重、不跑新"
    "图片、不调优、不用数据集、不接 live camera/sensor,不触发 navigation/action/speech/fact_write。"
    "Luna 仍以情感多模态 + 大脑/世界理解为核心,VLA 行动链不在当前范围。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p0_recognition_serves_cognition_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_p0_integration_closure_only"
P0_INTEGRATION_CLOSURE_ONLY = True
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

REAL_OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001"
EVIDENCE_MAIN_CHAIN_INTEGRATION_DRYRUN_REF = (
    "Phase-Recognition-Model-Evidence-Main-Chain-Integration-DryRun-v1-001"
)

NEXT_OPTIONS_REF: Tuple[str, ...] = (
    "Phase-Recognition-Model-P0-Post-Review-v1-001",
    "Phase-Recognition-Model-YOLO-Real-Weight-DryRun-v1-001",
    "Phase-Recognition-Model-P1-Segmentation-Tracking-Admission-v1-001",
)

# --------------------------------------------------------------------------- #
# P0 capability coverage keys
# --------------------------------------------------------------------------- #
P0_CAPABILITY_KEYS: Tuple[str, ...] = (
    "rapidocr_p0_integrated",
    "opencv_visual_symbol_p0_integrated",
    "yolo_lightweight_p0_declared_unavailable_non_blocker",
)

# --------------------------------------------------------------------------- #
# Required candidate coverage (>= 21)
# --------------------------------------------------------------------------- #
REQUIRED_CANDIDATE_COVERAGE: Tuple[str, ...] = (
    "text_evidence_candidate",
    "color_evidence_candidate",
    "shape_evidence_candidate",
    "visual_symbol_candidate",
    "symbol_meaning_candidate",
    "model_availability_state_candidate",
    "text_observation_candidate",
    "facility_text_hint_candidate",
    "exit_text_hint_candidate",
    "direction_hint_candidate",
    "exit_direction_candidate",
    "cross_modal_consistency_candidate",
    "exit_sign_hypothesis_candidate",
    "field_affordance_hint_candidate",
    "FieldSynthesisCandidate",
    "TaskContextCandidate",
    "TaskRiskCandidate",
    "GuidanceCandidate",
    "SpeechGateCandidate",
    "ActionSafetyCandidate",
    "object_detection_unavailable_record",
)

# candidate type -> GO coverage key
CANDIDATE_COVERAGE_GO_KEYS: Dict[str, str] = {
    "text_evidence_candidate": "text_evidence_candidate_covered",
    "color_evidence_candidate": "color_evidence_candidate_covered",
    "shape_evidence_candidate": "shape_evidence_candidate_covered",
    "visual_symbol_candidate": "visual_symbol_candidate_covered",
    "symbol_meaning_candidate": "symbol_meaning_candidate_covered",
    "model_availability_state_candidate": "model_availability_state_candidate_covered",
    "text_observation_candidate": "text_observation_candidate_covered",
    "facility_text_hint_candidate": "facility_text_hint_candidate_covered",
    "exit_text_hint_candidate": "exit_text_hint_candidate_covered",
    "direction_hint_candidate": "direction_hint_candidate_covered",
    "exit_direction_candidate": "exit_direction_candidate_covered",
    "cross_modal_consistency_candidate": "cross_modal_consistency_candidate_covered",
    "exit_sign_hypothesis_candidate": "exit_sign_hypothesis_candidate_covered",
    "field_affordance_hint_candidate": "field_affordance_hint_candidate_covered",
    "FieldSynthesisCandidate": "field_synthesis_candidate_covered",
    "TaskContextCandidate": "task_context_candidate_covered",
    "TaskRiskCandidate": "task_risk_candidate_covered",
    "GuidanceCandidate": "guidance_candidate_covered",
    "SpeechGateCandidate": "speech_gate_candidate_covered",
    "ActionSafetyCandidate": "action_safety_candidate_covered",
    "object_detection_unavailable_record": "object_detection_unavailable_record_covered",
}

# --------------------------------------------------------------------------- #
# Core closure conclusions
# --------------------------------------------------------------------------- #
CLOSURE_CONCLUSIONS: Tuple[str, ...] = (
    "p0_recognition_model_integration_is_closed_as_a_stable_baseline",
    "real_model_output_has_been_proven_to_enter_luna_evidence_main_chain",
    "rapidocr_real_output_is_accepted_as_text_evidence_candidate_not_fact",
    "opencv_visual_symbol_output_is_accepted_as_color_shape_symbol_evidence_candidate_not_fact",
    "ocr_plus_visual_symbol_consistency_can_generate_hypothesis_candidates_only",
    "exit_text_and_right_direction_symbol_do_not_activate_route_or_navigation",
    "yolo_unavailable_is_non_blocker_if_declared",
    "yolo_remains_test_only_and_commercial_runtime_approved_false",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_not_part_of_current_scope",
    "luna_remains_emotion_multimodal_brain_cognition_first",
    "no_tuning_or_data_usage_is_approved_by_this_closure",
)

# --------------------------------------------------------------------------- #
# Negative closure checks (must be recognized as blockers)
# --------------------------------------------------------------------------- #
NEGATIVE_CLOSURE_CHECK_IDS: Tuple[str, ...] = (
    "upstream_go_missing_blocked",
    "p0_real_output_missing_without_unavailable_record_blocked",
    "yolo_unavailable_blocker_or_download_blocked",
    "ocr_symbol_fact_write_blocked",
    "exit_route_navigation_activation_blocked",
    "guidance_runtime_navigation_blocked",
    "speech_gate_tts_blocked",
    "action_safety_action_trigger_blocked",
    "vla_action_chain_current_scope_blocked",
    "model_tuning_dataset_usage_approval_blocked",
)

# --------------------------------------------------------------------------- #
# Mandatory rules
# --------------------------------------------------------------------------- #
CLOSURE_RULES: Tuple[str, ...] = (
    "this_phase_is_p0_integration_closure_only",
    "no_new_model_is_added",
    "no_new_inference_is_executed",
    "no_new_image_video_recognition_is_executed",
    "yolo_weight_download_is_not_allowed",
    "model_download_is_not_allowed",
    "model_install_is_not_executed",
    "model_tuning_is_not_allowed",
    "dataset_usage_is_not_allowed",
    "training_is_not_allowed",
    "commercial_runtime_is_not_approved",
    "ocr_output_remains_evidence_candidate_not_fact",
    "visual_symbol_output_remains_evidence_candidate_not_fact",
    "ocr_plus_symbol_consistency_remains_hypothesis_candidate",
    "exit_text_does_not_directly_activate_route",
    "direction_symbol_does_not_directly_activate_navigation",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DEFINED_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelP0IntegrationClosureProfile",
    "RecognitionModelP0StageRef",
    "RecognitionModelP0ArtifactRef",
    "RecognitionModelP0CapabilityCoverage",
    "RecognitionModelP0CandidateCoverage",
    "RecognitionModelP0BoundaryClosure",
    "RecognitionModelP0UnavailableModelRecord",
    "RecognitionModelP0IntegrationClosureDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_P0_INTEGRATION_CLOSURE_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_P0_INTEGRATION_CLOSURE_BLOCKED"

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "new_image_recognition_allowed": False,
    "model_download_allowed": False,
    "yolo_weight_download_allowed": False,
    "model_install_allowed": False,
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
class RecognitionModelP0StageRef:
    stage_index: int
    phase_ref: str
    expected_go: str
    verify_flag: str
    go_verified: bool


@dataclass(frozen=True)
class RecognitionModelP0CapabilityCoverage:
    capability_key: str
    integrated: bool
    note: str


@dataclass(frozen=True)
class RecognitionModelP0CandidateCoverage:
    coverage_ref: str
    covered_candidate_types: Tuple[str, ...]
    coverage_count: int
    coverage_complete: bool


@dataclass(frozen=True)
class RecognitionModelP0UnavailableModelRecord:
    target: str
    availability_state: str
    non_blocker: bool
    model_download_triggered: bool
    commercial_runtime_approved: bool


@dataclass(frozen=True)
class RecognitionModelP0BoundaryClosure:
    boundary_ref: str
    rules: Tuple[str, ...]
    conclusions: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelP0IntegrationClosureProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    p0_integration_closure_only: bool
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    real_output_adapter_dryrun_ref: str
    evidence_main_chain_integration_dryrun_ref: str
    luna_core_principle: str
    p0_capability_keys: Tuple[str, ...]
    required_candidate_coverage: Tuple[str, ...]
    closure_conclusions: Tuple[str, ...]
    negative_closure_check_ids: Tuple[str, ...]
    closure_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelP0IntegrationClosureDecision:
    decision_ref: str
    closure_profile_count: int
    stage_ref_count: int
    p0_capability_coverage_count: int
    candidate_coverage_count: int
    negative_closure_check_count: int
    negative_closure_blocker_check_passed: int
    blocker_count: int
    final_decision: str


def closure_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
