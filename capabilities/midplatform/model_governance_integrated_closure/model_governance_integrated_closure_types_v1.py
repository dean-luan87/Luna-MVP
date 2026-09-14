# -*- coding: utf-8 -*-
"""Recognition Midplatform Model Governance Integrated Closure — types v1.

Based on the already-GO Midplatform Model Control DryRun, this phase performs an
integrated closure over the Luna recognition-model expansion and midplatform model
governance chain. It seals four layers into a reusable stable baseline:

  P1/P2 Output Adapter
  -> Multi-Model Interaction
  -> Midplatform Model Data Handling
  -> Midplatform Model Control

This phase adds no new model, downloads nothing, runs no inference, runs no new
image/video, does no single-model debugging, no model tuning, no dataset usage, no
training, no live camera/sensor, and triggers no navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
SCOPE = "recognition_midplatform_model_governance_integrated_closure"
SOURCE_CHAIN = "recognition_midplatform_model_governance_integrated_closure_v1"

CLOSURE_PRINCIPLE_ZH = (
    "基于已 GO 的 Midplatform Model Control DryRun，对 Luna 识别模型扩张与中台模型治理链路进行 integrated "
    "closure。封口范围包括 P1/P2 输出标准、模型间互动、中台数据处理、中台模型控制四层能力，并将其固化为可复用"
    "稳定基线。不新增模型，不下载模型，不执行 inference，不跑新图片，不做单模型调试，不做模型调优，不使用数据集，"
    "不训练，不接 live camera/sensor，不触发 navigation/action/speech/fact_write。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "model_governance_integrated_closure_seals_cognition_baseline_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_midplatform_model_governance_integrated_closure_only"
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_ONLY = True
MODEL_CONTROL_DRYRUN_REF = "Phase-Midplatform-Model-Control-DryRun-v1-001"
MODEL_DATA_HANDLING_DRYRUN_REF = "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001"
MULTI_MODEL_INTERACTION_DRYRUN_REF = (
    "Phase-Recognition-Model-Multi-Model-Interaction-DryRun-v1-001"
)
P1_OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001"
P0_BASELINE_REF = "Phase-Recognition-Model-P0-Integration-Closure-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = (
    "post_review_or_Phase-Model-Governance-Runtime-Trial-Planning-v1-001"
)

# --------------------------------------------------------------------------- #
# Capability baseline coverage (5)
# --------------------------------------------------------------------------- #
CAPABILITY_BASELINE_FLAGS: Tuple[str, ...] = (
    "p1_p2_output_adapter_baseline_closed",
    "multi_model_interaction_baseline_closed",
    "midplatform_model_data_handling_baseline_closed",
    "midplatform_model_control_baseline_closed",
    "model_governance_integrated_baseline_closed",
)

# --------------------------------------------------------------------------- #
# Layer-1: P1/P2 output adapter families & candidate coverage
# --------------------------------------------------------------------------- #
P1_P2_OUTPUT_FAMILIES: Tuple[str, ...] = (
    "segmentation",
    "tracking",
    "depth_spatial_hint",
    "object_detection_completion",
    "scene_relation_vlm",
    "audio_speech_reserved",
    "emotion_multimodal_bridge_reserved",
)

P1_P2_OUTPUT_CANDIDATE_COVERAGE: Tuple[str, ...] = (
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

# --------------------------------------------------------------------------- #
# Layer-2: multi-model interaction candidate coverage
# --------------------------------------------------------------------------- #
INTERACTION_CANDIDATE_COVERAGE: Tuple[str, ...] = (
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

# --------------------------------------------------------------------------- #
# Layer-3: midplatform model data handling coverage
# --------------------------------------------------------------------------- #
MIDPLATFORM_DATA_HANDLING_COVERAGE: Tuple[str, ...] = (
    "midplatform_candidate_ingress_record",
    "normalized_model_candidate_bundle",
    "aggregated_source_chain_record",
    "aggregated_confidence_policy_candidate",
    "midplatform_conflict_record",
    "midplatform_uncertainty_record",
    "model_availability_state_record",
    "reserved_family_state_record",
    "degraded_capability_state_candidate",
    "midplatform_model_evidence_bundle",
    "candidate_lifecycle_record",
    "field_task_guidance_support_bundle",
)

# --------------------------------------------------------------------------- #
# Layer-4: midplatform model control coverage
# --------------------------------------------------------------------------- #
MIDPLATFORM_MODEL_CONTROL_COVERAGE: Tuple[str, ...] = (
    "model_enable_record",
    "model_disable_record",
    "model_fallback_record",
    "degraded_model_state_record",
    "license_boundary_record",
    "commercial_runtime_block_record",
    "model_priority_routing_record",
    "model_output_gate_rejection_record",
    "model_availability_control_record",
    "reserved_family_execution_block_record",
    "candidate_output_gate_record",
    "midplatform_model_control_bundle",
    "model_control_audit_trace",
    "model_control_whitebox_candidate",
)

ALL_CANDIDATE_COVERAGE: Tuple[str, ...] = (
    P1_P2_OUTPUT_CANDIDATE_COVERAGE
    + INTERACTION_CANDIDATE_COVERAGE
    + MIDPLATFORM_DATA_HANDLING_COVERAGE
    + MIDPLATFORM_MODEL_CONTROL_COVERAGE
)

COVERAGE_COMPLETE_FLAGS: Tuple[str, ...] = (
    "p1_p2_output_candidate_coverage_complete",
    "interaction_candidate_coverage_complete",
    "midplatform_data_handling_coverage_complete",
    "midplatform_model_control_coverage_complete",
)

# --------------------------------------------------------------------------- #
# Boundary closure invariants (16) — all must hold True.
# --------------------------------------------------------------------------- #
BOUNDARY_CLOSURE_FLAGS: Tuple[str, ...] = (
    "candidate_ingress_not_fact_admission",
    "multi_model_agreement_not_fact",
    "conflict_uncertainty_candidate_only",
    "evidence_bundle_not_fact_bundle",
    "candidate_output_gate_not_fact_admission",
    "enabled_not_runtime_activation",
    "fallback_no_download_or_inference",
    "reserved_only_family_not_executed",
    "commercial_runtime_not_approved",
    "field_task_guidance_candidate_only",
    "guidance_not_runtime_navigation",
    "speech_gate_not_tts",
    "action_safety_no_action_trigger",
    "vla_action_chain_excluded",
    "model_tuning_dataset_usage_not_approved",
    "luna_emotion_multimodal_brain_first_preserved",
)

# --------------------------------------------------------------------------- #
# Negative closure guards (14) — id -> (description, go_key, depends_on)
# `depends_on` names the closure invariant whose safe-state proves the guard
# would block any violation; the guard passes when that invariant holds.
# --------------------------------------------------------------------------- #
NEGATIVE_CLOSURE_GUARDS: Tuple[Dict[str, str], ...] = (
    {
        "guard_id": "invalid_upstream_go_missing",
        "go_key": "upstream_go_missing_blocked",
        "depends_on": "all_gated_upstream_go_verified",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_p1_p2_output_adapter_coverage_missing",
        "go_key": "p1_p2_output_adapter_coverage_missing_blocked",
        "depends_on": "p1_p2_output_candidate_coverage_complete",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_multi_model_interaction_coverage_missing",
        "go_key": "multi_model_interaction_coverage_missing_blocked",
        "depends_on": "interaction_candidate_coverage_complete",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_midplatform_data_handling_coverage_missing",
        "go_key": "midplatform_data_handling_coverage_missing_blocked",
        "depends_on": "midplatform_data_handling_coverage_complete",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_midplatform_model_control_coverage_missing",
        "go_key": "midplatform_model_control_coverage_missing_blocked",
        "depends_on": "midplatform_model_control_coverage_complete",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_candidate_ingress_fact_admission",
        "go_key": "candidate_ingress_fact_admission_blocked",
        "depends_on": "candidate_ingress_not_fact_admission",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_agreement_conflict_fact_write",
        "go_key": "agreement_conflict_fact_write_blocked",
        "depends_on": "multi_model_agreement_not_fact",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_fallback_download_inference",
        "go_key": "fallback_download_inference_blocked",
        "depends_on": "fallback_no_download_or_inference",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_reserved_family_execution",
        "go_key": "reserved_family_execution_blocked",
        "depends_on": "reserved_only_family_not_executed",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_candidate_gate_fact_admission",
        "go_key": "candidate_gate_fact_admission_blocked",
        "depends_on": "candidate_output_gate_not_fact_admission",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_guidance_speech_action_runtime",
        "go_key": "guidance_speech_action_runtime_blocked",
        "depends_on": "action_safety_no_action_trigger",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_vla_action_chain_current_scope",
        "go_key": "vla_action_chain_current_scope_blocked",
        "depends_on": "vla_action_chain_excluded",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_model_tuning_dataset_usage_approval",
        "go_key": "model_tuning_dataset_usage_approval_blocked",
        "depends_on": "model_tuning_dataset_usage_not_approved",
        "expected": "blocker",
    },
    {
        "guard_id": "invalid_commercial_runtime_approval",
        "go_key": "commercial_runtime_approval_blocked",
        "depends_on": "commercial_runtime_not_approved",
        "expected": "blocker",
    },
)

# --------------------------------------------------------------------------- #
# Core closure conclusions (22)
# --------------------------------------------------------------------------- #
CLOSURE_CONCLUSIONS: Tuple[str, ...] = (
    "recognition_model_p1_p2_output_standards_are_closed_as_baseline",
    "multi_model_interaction_dryrun_is_closed_as_baseline",
    "midplatform_model_data_handling_dryrun_is_closed_as_baseline",
    "midplatform_model_control_dryrun_is_closed_as_baseline",
    "model_governance_integrated_baseline_is_ready_for_handoff",
    "all_model_outputs_remain_evidence_candidate_before_any_downstream_use",
    "multi_model_agreement_does_not_create_fact",
    "conflict_uncertainty_remains_candidate_only",
    "candidate_ingress_is_not_fact_admission",
    "evidence_bundle_is_not_fact_bundle",
    "candidate_output_gate_is_not_fact_admission",
    "enabled_model_does_not_mean_runtime_activation",
    "fallback_does_not_trigger_download_or_inference",
    "reserved_only_family_must_not_execute",
    "commercial_runtime_remains_not_approved",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "no_tuning_or_dataset_usage_is_approved_by_this_closure",
)

# --------------------------------------------------------------------------- #
# Governance rules (30)
# --------------------------------------------------------------------------- #
CLOSURE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_integrated_closure_only",
    "no_new_model_is_added",
    "no_new_model_download_is_allowed",
    "no_inference_is_allowed",
    "no_new_image_or_video_recognition_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "no_training_is_allowed",
    "p1_p2_output_adapter_baseline_must_be_verified",
    "multi_model_interaction_baseline_must_be_verified",
    "midplatform_model_data_handling_baseline_must_be_verified",
    "midplatform_model_control_baseline_must_be_verified",
    "all_model_outputs_remain_evidence_candidate",
    "candidate_ingress_is_not_fact_admission",
    "multi_model_agreement_is_not_fact",
    "conflict_uncertainty_remains_candidate_only",
    "evidence_bundle_is_not_fact_bundle",
    "candidate_output_gate_is_not_fact_admission",
    "enabled_model_does_not_mean_runtime_activation",
    "fallback_does_not_trigger_download_or_inference",
    "reserved_only_family_must_not_execute",
    "commercial_runtime_is_not_approved",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionMidplatformModelGovernanceIntegratedClosureProfile",
    "ModelGovernanceStageRef",
    "ModelGovernanceArtifactRef",
    "ModelGovernanceCapabilityCoverage",
    "ModelGovernanceCandidateCoverage",
    "ModelGovernanceDataHandlingCoverage",
    "ModelGovernanceControlCoverage",
    "ModelGovernanceBoundaryClosure",
    "ModelGovernanceNegativeClosureGuard",
    "RecognitionMidplatformModelGovernanceIntegratedClosureDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_GO"
FINAL_DECISION_BLOCKED = (
    "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_BLOCKED"
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "new_image_recognition_allowed": False,
    "model_download_allowed": False,
    "single_model_debugging_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}

BINDING_NON_EXECUTION_FLAGS: Dict[str, bool] = {
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
class RecognitionMidplatformModelGovernanceIntegratedClosureProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    model_governance_integrated_closure_only: bool
    model_control_dryrun_ref: str
    model_data_handling_dryrun_ref: str
    multi_model_interaction_dryrun_ref: str
    p1_output_adapter_dryrun_ref: str
    p0_baseline_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    capability_baseline_flags: Tuple[str, ...]
    boundary_closure_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelGovernanceStageRef:
    stage_index: int
    phase_ref: str
    expected_go: str
    gated: bool
    go_verified: bool


@dataclass(frozen=True)
class ModelGovernanceArtifactRef:
    layer: str
    phase_ref: str
    artifact_rel: str
    final_decision: str
    present: bool


@dataclass(frozen=True)
class ModelGovernanceCapabilityCoverage:
    capability_baseline_flag: str
    closed: bool


@dataclass(frozen=True)
class ModelGovernanceCandidateCoverage:
    layer: str
    candidate_types: Tuple[str, ...]
    coverage_count: int
    coverage_complete: bool


@dataclass(frozen=True)
class ModelGovernanceDataHandlingCoverage:
    candidate_types: Tuple[str, ...]
    coverage_count: int
    coverage_complete: bool


@dataclass(frozen=True)
class ModelGovernanceControlCoverage:
    candidate_types: Tuple[str, ...]
    coverage_count: int
    coverage_complete: bool


@dataclass(frozen=True)
class ModelGovernanceBoundaryClosure:
    boundary_flag: str
    holds: bool


@dataclass
class ModelGovernanceNegativeClosureGuard:
    guard_id: str
    go_key: str
    depends_on: str
    expected: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionMidplatformModelGovernanceIntegratedClosureDecision:
    decision_ref: str
    closure_profile_count: int
    stage_ref_count: int
    artifact_ref_count: int
    capability_coverage_count: int
    candidate_coverage_count: int
    negative_closure_guard_count: int
    negative_closure_guard_passed: int
    model_governance_integrated_baseline_closed: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
