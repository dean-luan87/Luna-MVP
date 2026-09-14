# -*- coding: utf-8 -*-
"""Recognition Model P1 Output Adapter DryRun — types v1.

Based on the already-GO Recognition Model P1 Invocation and Local Availability
DryRun, this phase validates — with mock-but-file-based model output samples —
whether the seven P1/P2 expansion/reserved model families can be mapped through
the RecognitionModelOutputAdapter into Luna evidence candidates compatible with
the frozen Phase-One environment cognition evidence main chain.

  mock file-based model output
  -> RecognitionModelOutputAdapter
  -> Luna evidence candidate
  -> evidence main chain compatible output

No new model download, no real inference, no single-model debugging, no model
tuning, no dataset usage / training, no live camera-sensor, and no navigation/
action/speech/fact_write / VLA action chain.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001"
SCOPE = "recognition_model_p1_output_adapter_dryrun"
SOURCE_CHAIN = "recognition_model_p1_output_adapter_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model P1 Invocation and Local Availability DryRun，对 P1/P2 扩张模型族执行 "
    "output adapter dry-run。使用文件级 mock 输出验证 segmentation / tracking / depth-spatial-hint / "
    "object-detection-completion / scene-relation-VLM / audio-speech-reserved / "
    "emotion-multimodal-bridge-reserved 七类模型族的输出能否映射为 Luna evidence candidate，并符合 "
    "Phase One Evidence Main Chain 的候选层要求。不下载模型，不执行真实 inference，不调试单一模型，"
    "不使用数据集，不训练，不接 live camera/sensor，不触发 navigation/action/speech/fact_write。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_p2_output_adapter_serves_cognition_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_p1_output_adapter_dryrun_only"
P1_INVOCATION_LOCAL_AVAILABILITY_DRYRUN_REF = (
    "Phase-Recognition-Model-P1-Invocation-And-Local-Availability-DryRun-v1-001"
)
P1_FAMILY_EXPANSION_PLANNING_REF = (
    "Phase-Recognition-Model-P1-Family-Expansion-Planning-v1-001"
)
P0_BASELINE_REF = "Phase-Recognition-Model-P0-Integration-Closure-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_PHASE_REF = "Phase-Recognition-Model-Multi-Model-Interaction-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Model families (7): 5 P1/P2 expansion + 2 reserved.
# --------------------------------------------------------------------------- #
MODEL_FAMILY_IDS: Tuple[str, ...] = (
    "segmentation_family",
    "tracking_family",
    "depth_spatial_hint_family",
    "object_detection_completion_family",
    "scene_relation_vlm_family",
    "audio_speech_family",
    "emotion_multimodal_bridge_family",
)

RESERVED_FAMILIES: Tuple[str, ...] = (
    "audio_speech_family",
    "emotion_multimodal_bridge_family",
)

# family -> generated candidate types
FAMILY_TO_CANDIDATES: Dict[str, Tuple[str, ...]] = {
    "segmentation_family": (
        "region_evidence_candidate",
        "mask_boundary_candidate",
        "object_region_alignment_candidate",
    ),
    "tracking_family": (
        "track_evidence_candidate",
        "dynamic_risk_candidate",
        "temporal_consistency_candidate",
    ),
    "depth_spatial_hint_family": (
        "spatial_hint_candidate",
        "distance_uncertainty_candidate",
        "depth_consistency_candidate",
    ),
    "object_detection_completion_family": (
        "object_evidence_candidate",
        "open_vocab_object_candidate",
    ),
    "scene_relation_vlm_family": (
        "scene_relation_candidate",
        "attribute_candidate",
        "relation_hypothesis_candidate",
    ),
    "audio_speech_family": (
        "audio_text_candidate",
        "speaker_turn_candidate",
        "speaker_identity_candidate",
        "emotion_audio_hint_candidate",
    ),
    "emotion_multimodal_bridge_family": (
        "affective_scene_hint_candidate",
        "user_state_hint_candidate",
        "social_context_hint_candidate",
    ),
}

# family -> safety boundary
FAMILY_BOUNDARY: Dict[str, str] = {
    "segmentation_family": "mask_is_not_fact_segmentation_is_not_route_activation",
    "tracking_family": "tracking_is_not_action_trigger",
    "depth_spatial_hint_family": "depth_is_auxiliary_not_field_identity_not_navigation",
    "object_detection_completion_family": "object_identity_is_not_fact",
    "scene_relation_vlm_family": "scene_relation_is_not_final_interpretation_no_reasoning_authority",
    "audio_speech_family": "reserved_only_identity_requires_consent_no_audio_execution",
    "emotion_multimodal_bridge_family": (
        "reserved_only_no_psychological_fact_write_no_behavior_manipulation"
    ),
}

# All 21 candidate types covered by the full P1/P2 bundle.
ALL_CANDIDATE_TYPES: Tuple[str, ...] = (
    "region_evidence_candidate",
    "mask_boundary_candidate",
    "object_region_alignment_candidate",
    "track_evidence_candidate",
    "dynamic_risk_candidate",
    "temporal_consistency_candidate",
    "spatial_hint_candidate",
    "distance_uncertainty_candidate",
    "depth_consistency_candidate",
    "object_evidence_candidate",
    "open_vocab_object_candidate",
    "scene_relation_candidate",
    "attribute_candidate",
    "relation_hypothesis_candidate",
    "audio_text_candidate",
    "speaker_turn_candidate",
    "speaker_identity_candidate",
    "emotion_audio_hint_candidate",
    "affective_scene_hint_candidate",
    "user_state_hint_candidate",
    "social_context_hint_candidate",
)

CANDIDATE_GENERATED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_generated" for c in ALL_CANDIDATE_TYPES
)

FAMILY_MAPPING_GO_KEYS: Dict[str, str] = {
    "segmentation_family": "segmentation_output_adapter_mapping_ok",
    "tracking_family": "tracking_output_adapter_mapping_ok",
    "depth_spatial_hint_family": "depth_spatial_hint_output_adapter_mapping_ok",
    "object_detection_completion_family": "object_detection_completion_output_adapter_mapping_ok",
    "scene_relation_vlm_family": "scene_relation_vlm_output_adapter_mapping_ok",
    "audio_speech_family": "audio_speech_reserved_output_contract_mapping_ok",
    "emotion_multimodal_bridge_family": "emotion_multimodal_bridge_reserved_output_contract_mapping_ok",
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
    "fallback_plan",
    "unavailable_record_policy",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "license_ref",
    "model_origin",
    "confidence",
    "adapter_mapping_ref",
    "fallback_plan",
    "unavailable_record_policy",
)

CONTRACT_FIELD_REQUIRED_FLAGS: Dict[str, str] = {
    "source_chain": "source_chain_required",
    "license_ref": "license_ref_required",
    "model_origin": "model_origin_required",
    "confidence": "confidence_required",
    "adapter_mapping_ref": "adapter_mapping_ref_required",
    "fallback_plan": "fallback_plan_required",
    "unavailable_record_policy": "unavailable_record_policy_required",
}

# --------------------------------------------------------------------------- #
# Prohibited flags (any True -> reject)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "native_output_direct_to_field",
    "fact_write_requested",
    "psychological_fact_write_requested",
    "behavior_manipulation_requested",
    "route_activation_requested",
    "direct_action_requested",
    "direct_speech_requested",
    "direct_navigation_requested",
    "field_identity_override_requested",
    "final_interpretation_requested",
    "reasoning_authority_requested",
    "identity_without_consent",
    "vla_action_chain_requested",
    "real_inference_requested",
    "new_model_download_requested",
    "single_model_debugging_requested",
    "model_tuning_requested",
    "dataset_usage_requested",
    "training_requested",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "segmentation_output_adapter_mapping",
    "tracking_output_adapter_mapping",
    "depth_spatial_hint_output_adapter_mapping",
    "object_detection_completion_output_adapter_mapping",
    "scene_relation_vlm_structured_output_adapter_mapping",
    "audio_speech_reserved_output_contract_mapping",
    "emotion_multimodal_bridge_reserved_output_contract_mapping",
    "p1_p2_multi_family_output_bundle_mapping",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_source_chain",
    "invalid_missing_license_ref",
    "invalid_missing_model_origin",
    "invalid_missing_confidence",
    "invalid_missing_adapter_mapping_ref",
    "invalid_segmentation_route_activation",
    "invalid_tracking_action_trigger",
    "invalid_depth_navigation_activation",
    "invalid_scene_relation_final_interpretation",
    "invalid_audio_identity_without_consent",
    "invalid_emotion_psychological_fact_write",
    "invalid_vla_action_chain",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_p1_p2_output_adapter_dryrun_only",
    "mock_file_based_outputs_are_allowed",
    "no_new_model_download_is_allowed",
    "no_real_inference_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "no_training_is_allowed",
    "all_outputs_must_pass_recognition_model_output_adapter",
    "all_outputs_become_evidence_candidate_first",
    "mask_segmentation_output_is_not_fact",
    "tracking_is_not_action_trigger",
    "depth_is_auxiliary_and_not_navigation",
    "object_identity_is_not_fact",
    "scene_relation_vlm_has_no_reasoning_authority",
    "audio_identity_requires_consent_and_confirmation",
    "emotion_multimodal_bridge_does_not_write_psychological_fact",
    "emotion_multimodal_bridge_does_not_perform_behavior_manipulation",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelP1OutputAdapterDryRunProfile",
    "RecognitionModelP1OutputFileBundle",
    "RecognitionModelP1OutputAdmissionResult",
    "RecognitionModelP1OutputAdapterMappingResult",
    "RecognitionModelP1EvidenceCandidateResult",
    "RecognitionModelP1CandidateCoverageResult",
    "RecognitionModelP1OutputBoundaryResult",
    "RecognitionModelP1OutputAdapterDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_P1_OUTPUT_ADAPTER_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_P1_OUTPUT_ADAPTER_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "p1_output_adapter_dryrun_allowed": True,
    "mock_file_based_output_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "new_model_download_allowed": False,
    "real_inference_allowed": False,
    "single_model_debugging_allowed": False,
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
class RecognitionModelP1OutputAdapterDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    p1_invocation_local_availability_dryrun_ref: str
    p1_family_expansion_planning_ref: str
    p0_baseline_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    model_family_ids: Tuple[str, ...]
    required_model_output_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelP1OutputFileBundle:
    bundle_ref: str
    model_family: str
    output_file_ref: str
    mock_file_based: bool


@dataclass(frozen=True)
class RecognitionModelP1OutputAdmissionResult:
    model_family: str
    accepted: bool
    reject_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelP1OutputAdapterMappingResult:
    model_family: str
    adapter_ref: str
    mapped_candidate_types: Tuple[str, ...]
    boundary: str


@dataclass(frozen=True)
class RecognitionModelP1EvidenceCandidateResult:
    candidate_type: str
    source_model_family: str
    boundary: str
    candidate_only: bool
    reserved_only: bool = False


@dataclass(frozen=True)
class RecognitionModelP1CandidateCoverageResult:
    coverage_ref: str
    covered_candidate_types: Tuple[str, ...]
    coverage_count: int
    coverage_complete: bool
    reserved_families_preserved: bool


@dataclass(frozen=True)
class RecognitionModelP1OutputBoundaryResult:
    model_family: str
    boundary: str
    no_fact_write: bool
    no_action_trigger: bool
    no_navigation_activation: bool
    no_reasoning_authority: bool


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
class RecognitionModelP1OutputAdapterDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    upstream_stage_ref_count: int
    output_family_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    p1_p2_multi_family_output_bundle_mapping_ok: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
