# -*- coding: utf-8 -*-
"""Recognition Model Multi-Model Interaction DryRun — types v1.

Based on the already-GO Recognition Model P1 Output Adapter DryRun, this phase
executes a multi-model output interaction dry-run. It does NOT validate whether a
single model output passes the adapter; instead it validates whether the evidence
candidates produced by multiple model families can correctly align, cross-confirm,
conflict, reinforce, degrade and propagate uncertainty — while preserving the
Luna emotion-multimodal brain / cognition-first principle.

  multiple mock file-based candidate bundles
  -> cross-model alignment / consistency / conflict / uncertainty
  -> Luna interaction evidence candidates (candidate-only)

No new model download, no real inference, no new image recognition, no single-model
debugging, no model tuning, no dataset usage / training, no live camera-sensor, and
no navigation/action/speech/fact_write / VLA action chain.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Multi-Model-Interaction-DryRun-v1-001"
SCOPE = "recognition_model_multi_model_interaction_dryrun"
SOURCE_CHAIN = "recognition_model_multi_model_interaction_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model P1 Output Adapter DryRun，执行多模型输出交互 dry-run。该阶段不验证"
    "单个模型输出是否能过 Adapter，而是验证多个模型族的 evidence candidate 之间能否正确发生对齐、互证、"
    "冲突、补强、降级与不确定性传播，并保持 Luna emotion-multimodal brain / cognition first 原则。"
    "不下载模型，不执行真实 inference，不跑新图片，不做单模型调试，不做模型调优，不使用数据集，不训练，"
    "不接 live camera/sensor，不触发 navigation/action/speech/fact_write。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "cross_model_interaction_serves_cognition_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_multi_model_interaction_dryrun_only"
P1_OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001"
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

NEXT_PHASE_REF = "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Interaction pairs / policies (9)
#   interaction_id -> (source_model_families, output candidate types, boundary)
# --------------------------------------------------------------------------- #
INTERACTION_IDS: Tuple[str, ...] = (
    "object_segmentation_alignment",
    "object_tracking_temporal",
    "tracking_depth_dynamic_risk",
    "ocr_segmentation_text_region",
    "visual_symbol_scene_context",
    "scene_relation_object_region",
    "audio_emotion_reserved_bridge",
    "conflict_uncertainty_propagation",
    "full_multi_model_interaction_bundle",
)

INTERACTION_TO_CANDIDATES: Dict[str, Tuple[str, ...]] = {
    "object_segmentation_alignment": (
        "object_region_alignment_candidate",
        "spatial_consistency_candidate",
    ),
    "object_tracking_temporal": (
        "object_track_alignment_candidate",
        "temporal_object_consistency_candidate",
    ),
    "tracking_depth_dynamic_risk": (
        "motion_distance_risk_candidate",
        "dynamic_spatial_uncertainty_candidate",
    ),
    "ocr_segmentation_text_region": (
        "text_region_alignment_candidate",
        "text_region_consistency_candidate",
    ),
    "visual_symbol_scene_context": (
        "symbol_context_consistency_candidate",
        "symbol_meaning_hypothesis_candidate",
    ),
    "scene_relation_object_region": (
        "relation_object_region_alignment_candidate",
        "relation_hypothesis_candidate",
    ),
    "audio_emotion_reserved_bridge": (
        "multimodal_affective_bridge_candidate",
        "reserved_emotion_context_candidate",
    ),
    "conflict_uncertainty_propagation": (
        "cross_model_conflict_candidate",
        "cross_model_uncertainty_candidate",
        "model_unavailable_context_candidate",
    ),
    "full_multi_model_interaction_bundle": (
        "multi_model_interaction_bundle_candidate",
        "field_synthesis_support_candidate",
        "task_context_support_candidate",
        "guidance_support_candidate",
    ),
}

INTERACTION_SOURCE_FAMILIES: Dict[str, Tuple[str, ...]] = {
    "object_segmentation_alignment": (
        "object_detection_completion_family",
        "segmentation_family",
    ),
    "object_tracking_temporal": (
        "object_detection_completion_family",
        "tracking_family",
    ),
    "tracking_depth_dynamic_risk": ("tracking_family", "depth_spatial_hint_family"),
    "ocr_segmentation_text_region": ("ocr_model_family", "segmentation_family"),
    "visual_symbol_scene_context": (
        "visual_symbol_model_family",
        "scene_relation_vlm_family",
    ),
    "scene_relation_object_region": (
        "scene_relation_vlm_family",
        "object_detection_completion_family",
        "segmentation_family",
    ),
    "audio_emotion_reserved_bridge": (
        "audio_speech_family",
        "emotion_multimodal_bridge_family",
    ),
    "conflict_uncertainty_propagation": (
        "object_detection_completion_family",
        "segmentation_family",
        "tracking_family",
    ),
    "full_multi_model_interaction_bundle": (
        "ocr_model_family",
        "object_detection_completion_family",
        "segmentation_family",
        "tracking_family",
        "depth_spatial_hint_family",
        "visual_symbol_model_family",
        "scene_relation_vlm_family",
        "audio_speech_family",
        "emotion_multimodal_bridge_family",
    ),
}

INTERACTION_BOUNDARY: Dict[str, str] = {
    "object_segmentation_alignment": "mask_is_not_fact_object_identity_is_not_fact_alignment_does_not_activate_route",
    "object_tracking_temporal": "tracking_is_not_action_trigger",
    "tracking_depth_dynamic_risk": "risk_candidate_does_not_trigger_action_depth_is_auxiliary_no_navigation",
    "ocr_segmentation_text_region": "ocr_text_is_not_fact_text_region_does_not_trigger_route_activation",
    "visual_symbol_scene_context": "symbol_meaning_requires_context_validation_no_direct_navigation",
    "scene_relation_object_region": "vlm_has_no_reasoning_authority_scene_relation_is_not_final_interpretation",
    "audio_emotion_reserved_bridge": (
        "reserved_only_identity_requires_consent_no_psychological_fact_write_no_behavior_manipulation"
    ),
    "conflict_uncertainty_propagation": "conflict_is_not_fact_uncertainty_does_not_trigger_action_speech_navigation",
    "full_multi_model_interaction_bundle": (
        "field_task_guidance_candidate_only_guidance_not_runtime_nav_speech_gate_not_tts_action_safety_no_trigger"
    ),
}

RESERVED_INTERACTIONS: Tuple[str, ...] = ("audio_emotion_reserved_bridge",)

INTERACTION_OK_GO_KEYS: Dict[str, str] = {
    "object_segmentation_alignment": "object_segmentation_alignment_ok",
    "object_tracking_temporal": "object_tracking_temporal_ok",
    "tracking_depth_dynamic_risk": "tracking_depth_dynamic_risk_ok",
    "ocr_segmentation_text_region": "ocr_segmentation_text_region_ok",
    "visual_symbol_scene_context": "visual_symbol_scene_context_ok",
    "scene_relation_object_region": "scene_relation_object_region_ok",
    "audio_emotion_reserved_bridge": "audio_emotion_reserved_bridge_ok",
    "conflict_uncertainty_propagation": "conflict_uncertainty_propagation_ok",
    "full_multi_model_interaction_bundle": "full_multi_model_interaction_bundle_ok",
}

INTERACTION_CASE_IDS: Dict[str, str] = {
    "object_segmentation_alignment": "object_segmentation_alignment_interaction",
    "object_tracking_temporal": "object_tracking_temporal_interaction",
    "tracking_depth_dynamic_risk": "tracking_depth_dynamic_risk_interaction",
    "ocr_segmentation_text_region": "ocr_segmentation_text_region_interaction",
    "visual_symbol_scene_context": "visual_symbol_scene_context_interaction",
    "scene_relation_object_region": "scene_relation_object_region_interaction",
    "audio_emotion_reserved_bridge": "audio_emotion_reserved_bridge_interaction",
    "conflict_uncertainty_propagation": "conflict_uncertainty_propagation_interaction",
    "full_multi_model_interaction_bundle": "full_multi_model_interaction_bundle",
}

# All 21 interaction candidate types.
ALL_CANDIDATE_TYPES: Tuple[str, ...] = (
    "object_region_alignment_candidate",
    "spatial_consistency_candidate",
    "object_track_alignment_candidate",
    "temporal_object_consistency_candidate",
    "motion_distance_risk_candidate",
    "dynamic_spatial_uncertainty_candidate",
    "text_region_alignment_candidate",
    "text_region_consistency_candidate",
    "symbol_context_consistency_candidate",
    "symbol_meaning_hypothesis_candidate",
    "relation_object_region_alignment_candidate",
    "relation_hypothesis_candidate",
    "multimodal_affective_bridge_candidate",
    "reserved_emotion_context_candidate",
    "cross_model_conflict_candidate",
    "cross_model_uncertainty_candidate",
    "model_unavailable_context_candidate",
    "multi_model_interaction_bundle_candidate",
    "field_synthesis_support_candidate",
    "task_context_support_candidate",
    "guidance_support_candidate",
)

CANDIDATE_GENERATED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{c}_generated" for c in ALL_CANDIDATE_TYPES
)

# --------------------------------------------------------------------------- #
# Interaction admission fields
# --------------------------------------------------------------------------- #
REQUIRED_INTERACTION_FIELDS: Tuple[str, ...] = (
    "interaction_id",
    "interaction_type",
    "source_model_families",
    "candidate_refs",
    "source_chain",
    "confidence_policy_ref",
    "alignment_policy_ref",
    "conflict_policy_ref",
    "uncertainty_policy_ref",
    "adapter_mapping_refs",
    "fallback_plan",
    "unavailable_record_policy",
    "allowed_use",
    "commercial_use_status",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "candidate_refs",
    "confidence_policy_ref",
    "alignment_policy_ref",
    "conflict_policy_ref",
    "uncertainty_policy_ref",
    "fallback_plan",
)

CONTRACT_FIELD_REQUIRED_FLAGS: Dict[str, str] = {
    "source_chain": "source_chain_required",
    "candidate_refs": "candidate_refs_required",
    "confidence_policy_ref": "confidence_policy_ref_required",
    "alignment_policy_ref": "alignment_policy_ref_required",
    "conflict_policy_ref": "conflict_policy_ref_required",
    "uncertainty_policy_ref": "uncertainty_policy_ref_required",
    "fallback_plan": "fallback_plan_required",
}

# --------------------------------------------------------------------------- #
# Prohibited flags (any True -> reject)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "fact_write_requested",
    "cross_model_fact_write_requested",
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
    "conflict_resolved_as_fact_without_admission",
    "guidance_runtime_navigation_requested",
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
POSITIVE_CASE_IDS: Tuple[str, ...] = tuple(INTERACTION_CASE_IDS.values())

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_source_chain",
    "invalid_missing_candidate_refs",
    "invalid_cross_model_fact_write",
    "invalid_segmentation_route_activation_from_alignment",
    "invalid_tracking_depth_direct_action",
    "invalid_visual_symbol_direct_navigation_from_context",
    "invalid_scene_relation_final_interpretation",
    "invalid_audio_identity_without_consent",
    "invalid_emotion_bridge_psychological_fact_write",
    "invalid_conflict_resolved_as_fact_without_admission",
    "invalid_vla_action_chain_injected",
    "invalid_guidance_runtime_navigation_from_interaction",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_multi_model_interaction_dryrun_only",
    "it_uses_mock_file_based_candidate_bundles",
    "no_new_model_download_is_allowed",
    "no_real_inference_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "no_training_is_allowed",
    "cross_model_alignment_is_candidate_only",
    "cross_model_consistency_is_candidate_only",
    "cross_model_conflict_is_candidate_only",
    "cross_model_uncertainty_is_candidate_only",
    "object_plus_segmentation_alignment_is_not_route_activation",
    "tracking_plus_depth_risk_is_not_action_trigger",
    "ocr_plus_segmentation_text_region_alignment_is_not_fact",
    "visual_symbol_plus_scene_context_is_not_navigation",
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
    "RecognitionModelMultiModelInteractionDryRunProfile",
    "MultiModelCandidateBundle",
    "ModelInteractionPairPolicy",
    "CrossModelAlignmentResult",
    "CrossModelConsistencyResult",
    "CrossModelConflictResult",
    "CrossModelUncertaintyResult",
    "CrossModelInteractionCandidateResult",
    "MultiModelInteractionBoundaryResult",
    "RecognitionModelMultiModelInteractionDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_MULTI_MODEL_INTERACTION_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_MULTI_MODEL_INTERACTION_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "multi_model_interaction_dryrun_allowed": True,
    "mock_file_based_candidate_bundle_allowed": True,
    "cross_model_alignment_allowed": True,
    "cross_model_consistency_check_allowed": True,
    "cross_model_conflict_candidate_allowed": True,
    "cross_model_uncertainty_candidate_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "new_model_download_allowed": False,
    "real_inference_allowed": False,
    "new_image_recognition_allowed": False,
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
class RecognitionModelMultiModelInteractionDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    p1_output_adapter_dryrun_ref: str
    p1_invocation_local_availability_dryrun_ref: str
    p1_family_expansion_planning_ref: str
    p0_baseline_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    interaction_ids: Tuple[str, ...]
    required_interaction_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MultiModelCandidateBundle:
    interaction_id: str
    interaction_type: str
    source_model_families: Tuple[str, ...]
    candidate_refs: Tuple[str, ...]
    mock_file_based: bool


@dataclass(frozen=True)
class ModelInteractionPairPolicy:
    interaction_id: str
    source_model_families: Tuple[str, ...]
    output_candidate_types: Tuple[str, ...]
    boundary: str
    candidate_only: bool


@dataclass(frozen=True)
class CrossModelAlignmentResult:
    interaction_id: str
    aligned: bool
    alignment_candidate_types: Tuple[str, ...]
    boundary: str


@dataclass(frozen=True)
class CrossModelConsistencyResult:
    interaction_id: str
    consistent: bool
    consistency_candidate_types: Tuple[str, ...]


@dataclass(frozen=True)
class CrossModelConflictResult:
    interaction_id: str
    conflict_detected: bool
    conflict_candidate_only: bool
    conflict_resolved_as_fact: bool


@dataclass(frozen=True)
class CrossModelUncertaintyResult:
    interaction_id: str
    uncertainty_propagated: bool
    uncertainty_candidate_only: bool
    triggers_action_speech_navigation: bool


@dataclass(frozen=True)
class CrossModelInteractionCandidateResult:
    candidate_type: str
    source_interaction_id: str
    boundary: str
    candidate_only: bool
    reserved_only: bool = False


@dataclass(frozen=True)
class MultiModelInteractionBoundaryResult:
    interaction_id: str
    boundary: str
    no_fact_write: bool
    no_route_activation: bool
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
    interaction_id: str = ""
    generated_candidates: Tuple[str, ...] = field(default_factory=tuple)
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelMultiModelInteractionDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    upstream_stage_ref_count: int
    interaction_policy_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    full_multi_model_interaction_bundle_ok: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
