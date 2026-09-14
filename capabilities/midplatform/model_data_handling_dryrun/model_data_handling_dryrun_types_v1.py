# -*- coding: utf-8 -*-
"""Midplatform Model Data Handling DryRun — types v1.

Based on the already-GO Recognition Model Multi-Model Interaction DryRun, this
phase executes a midplatform data-handling dry-run over multi-model evidence
candidates. It no longer validates model outputs or model-to-model interaction;
instead it validates whether the Luna midplatform can receive, normalize, compose,
trace, aggregate, conflict-handle, degrade-handle and lifecycle-manage multi-model
candidate data, and emit a Field / Task / Guidance candidate support bundle.

  multi-model evidence candidate
  -> Midplatform Model Data Handling Layer
  -> normalization -> evidence bundle -> source_chain / confidence aggregation
  -> conflict / uncertainty handling -> unavailable / reserved / degraded handling
  -> candidate lifecycle -> Field / Task / Guidance candidate support

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

PHASE_ID = "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001"
SCOPE = "midplatform_model_data_handling_dryrun"
SOURCE_CHAIN = "midplatform_model_data_handling_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model Multi-Model Interaction DryRun，执行中台对多模型 evidence candidate "
    "的数据处理 dry-run。该阶段不再验证模型输出或模型间互动本身，而是验证 Luna 中台是否能够接收、归一化、"
    "组合、追踪、聚合、冲突处理、降级处理、生命周期管理多模型 candidate 数据，并输出可供 Field / Task / "
    "Guidance 使用的 candidate support bundle。不下载模型，不执行 inference，不跑新图片，不做单模型调试，"
    "不做模型调优，不使用数据集，不训练，不接 live camera/sensor，不触发 navigation/action/speech/fact_write。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "midplatform_model_data_handling_serves_cognition_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "midplatform_model_data_handling_dryrun_only"
MULTI_MODEL_INTERACTION_DRYRUN_REF = (
    "Phase-Recognition-Model-Multi-Model-Interaction-DryRun-v1-001"
)
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

NEXT_PHASE_REF = "Phase-Midplatform-Model-Control-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Data-handling policies (10)
#   policy_id -> (produced object types, boundary)
# --------------------------------------------------------------------------- #
DATA_HANDLING_POLICY_IDS: Tuple[str, ...] = (
    "candidate_ingress",
    "candidate_normalization",
    "source_chain_aggregation",
    "confidence_policy_aggregation",
    "conflict_handling",
    "uncertainty_handling",
    "unavailable_reserved_degraded_handling",
    "evidence_bundle_composition",
    "candidate_lifecycle",
    "field_task_guidance_support_bundle",
)

POLICY_TO_OBJECTS: Dict[str, Tuple[str, ...]] = {
    "candidate_ingress": (
        "midplatform_candidate_ingress_record",
        "midplatform_candidate_acceptance_record",
    ),
    "candidate_normalization": (
        "normalized_model_candidate_bundle",
        "normalized_candidate_index",
    ),
    "source_chain_aggregation": (
        "aggregated_source_chain_record",
        "source_lineage_index",
    ),
    "confidence_policy_aggregation": (
        "aggregated_confidence_policy_candidate",
        "confidence_explanation_candidate",
    ),
    "conflict_handling": (
        "midplatform_conflict_record",
        "conflict_resolution_candidate",
        "conflict_requires_review_candidate",
    ),
    "uncertainty_handling": (
        "midplatform_uncertainty_record",
        "uncertainty_propagation_candidate",
        "uncertainty_affects_guidance_candidate",
    ),
    "unavailable_reserved_degraded_handling": (
        "model_availability_state_record",
        "reserved_family_state_record",
        "degraded_capability_state_candidate",
        "fallback_route_candidate",
    ),
    "evidence_bundle_composition": (
        "midplatform_model_evidence_bundle",
        "model_evidence_bundle_index",
        "field_task_guidance_support_bundle",
    ),
    "candidate_lifecycle": (
        "candidate_lifecycle_record",
        "candidate_state_transition_record",
        "blocked_candidate_record",
    ),
    "field_task_guidance_support_bundle": (
        "field_synthesis_support_bundle_candidate",
        "task_context_support_bundle_candidate",
        "guidance_support_bundle_candidate",
    ),
}

POLICY_BOUNDARY: Dict[str, str] = {
    "candidate_ingress": "candidate_ingress_is_not_fact_admission_no_direct_ftg_write",
    "candidate_normalization": "normalization_does_not_change_candidate_into_fact",
    "source_chain_aggregation": "source_aggregation_cannot_erase_weak_or_uncertain_source_state",
    "confidence_policy_aggregation": "high_confidence_does_not_create_fact_agreement_does_not_bypass_admission",
    "conflict_handling": "conflict_resolution_is_candidate_only_no_fact_without_admission",
    "uncertainty_handling": "uncertainty_cannot_trigger_action_speech_navigation",
    "unavailable_reserved_degraded_handling": (
        "unavailable_is_not_blocker_if_declared_reserved_must_not_execute_degraded_no_runtime_action"
    ),
    "evidence_bundle_composition": "evidence_bundle_is_not_fact_bundle_support_does_not_activate_guidance_runtime",
    "candidate_lifecycle": "blocked_or_expired_candidate_must_not_revive_without_governance",
    "field_task_guidance_support_bundle": (
        "field_task_guidance_candidate_only_guidance_not_runtime_nav_speech_gate_not_tts_action_safety_no_trigger"
    ),
}

# Reserved families that must never execute.
RESERVED_FAMILIES: Tuple[str, ...] = (
    "audio_speech_family",
    "emotion_multimodal_bridge_family",
)

POLICY_OK_GO_KEYS: Dict[str, str] = {
    "candidate_ingress": "candidate_ingress_handling_ok",
    "candidate_normalization": "candidate_normalization_handling_ok",
    "source_chain_aggregation": "source_chain_aggregation_handling_ok",
    "confidence_policy_aggregation": "confidence_policy_aggregation_handling_ok",
    "conflict_uncertainty": "conflict_uncertainty_handling_ok",
    "unavailable_reserved_degraded_handling": "unavailable_reserved_degraded_handling_ok",
    "evidence_bundle_composition": "evidence_bundle_composition_handling_ok",
    "candidate_lifecycle": "candidate_lifecycle_handling_ok",
    "field_task_guidance_support_bundle": "field_task_guidance_support_bundle_handling_ok",
    "full_midplatform_model_data_handling_bundle": "full_midplatform_model_data_handling_bundle_ok",
}

# Positive case id per case (10 cases).
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "multi_model_candidate_ingress_handling",
    "candidate_normalization_handling",
    "source_chain_aggregation_handling",
    "confidence_policy_aggregation_handling",
    "conflict_uncertainty_handling",
    "unavailable_reserved_degraded_handling",
    "evidence_bundle_composition_handling",
    "candidate_lifecycle_handling",
    "field_task_guidance_support_bundle_handling",
    "full_midplatform_model_data_handling_bundle",
)

# All 27 produced object types.
ALL_PRODUCED_OBJECTS: Tuple[str, ...] = (
    "midplatform_candidate_ingress_record",
    "midplatform_candidate_acceptance_record",
    "normalized_model_candidate_bundle",
    "normalized_candidate_index",
    "aggregated_source_chain_record",
    "source_lineage_index",
    "aggregated_confidence_policy_candidate",
    "confidence_explanation_candidate",
    "midplatform_conflict_record",
    "conflict_resolution_candidate",
    "conflict_requires_review_candidate",
    "midplatform_uncertainty_record",
    "uncertainty_propagation_candidate",
    "uncertainty_affects_guidance_candidate",
    "model_availability_state_record",
    "reserved_family_state_record",
    "degraded_capability_state_candidate",
    "fallback_route_candidate",
    "midplatform_model_evidence_bundle",
    "model_evidence_bundle_index",
    "field_task_guidance_support_bundle",
    "candidate_lifecycle_record",
    "candidate_state_transition_record",
    "blocked_candidate_record",
    "field_synthesis_support_bundle_candidate",
    "task_context_support_bundle_candidate",
    "guidance_support_bundle_candidate",
)

OBJECT_GENERATED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{o}_generated" for o in ALL_PRODUCED_OBJECTS
)

# --------------------------------------------------------------------------- #
# Ingress / handling admission fields
# --------------------------------------------------------------------------- #
REQUIRED_BUNDLE_FIELDS: Tuple[str, ...] = (
    "handling_id",
    "policy_id",
    "candidate_refs",
    "model_family_refs",
    "adapter_mapping_refs",
    "source_chain",
    "confidence_policy_ref",
    "fallback_plan",
    "unavailable_record_policy",
    "allowed_use",
    "commercial_use_status",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "candidate_refs",
    "confidence_policy_ref",
)

CONTRACT_FIELD_REQUIRED_FLAGS: Dict[str, str] = {
    "source_chain": "source_chain_required",
    "candidate_refs": "candidate_refs_required",
    "confidence_policy_ref": "confidence_policy_ref_required",
}

# --------------------------------------------------------------------------- #
# Prohibited flags (any True -> reject)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "fact_admission_requested",
    "untrusted_candidate_fact_admission_requested",
    "conflict_resolved_as_fact",
    "unavailable_model_treated_as_blocker",
    "download_requested",
    "reserved_family_executed",
    "direct_field_task_guidance_bypass",
    "direct_fact_write_requested",
    "action_requested",
    "speech_requested",
    "navigation_requested",
    "vla_action_chain_requested",
    "model_tuning_requested",
    "dataset_usage_requested",
    "training_requested",
    "blocked_expired_candidate_revived_without_governance",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_source_chain",
    "invalid_missing_candidate_refs",
    "invalid_missing_confidence_policy_ref",
    "invalid_untrusted_candidate_fact_admission",
    "invalid_conflict_resolved_as_fact",
    "invalid_unavailable_model_treated_as_blocker",
    "invalid_reserved_family_executed",
    "invalid_direct_field_task_guidance_bypass",
    "invalid_action_speech_navigation_trigger",
    "invalid_vla_action_chain_injected",
    "invalid_model_tuning_dataset_usage",
    "invalid_blocked_expired_candidate_revival",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_midplatform_model_data_handling_dryrun_only",
    "it_uses_file_based_multi_model_candidate_bundles",
    "no_new_model_download_is_allowed",
    "no_real_inference_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "no_training_is_allowed",
    "candidate_ingress_is_not_fact_admission",
    "candidate_normalization_does_not_create_fact",
    "source_chain_aggregation_must_preserve_lineage",
    "confidence_aggregation_does_not_create_fact",
    "conflict_handling_is_candidate_only",
    "uncertainty_handling_is_candidate_only",
    "unavailable_model_is_non_blocker_if_declared",
    "reserved_only_family_must_not_execute",
    "degraded_state_does_not_trigger_runtime_action",
    "evidence_bundle_is_not_fact_bundle",
    "field_task_guidance_support_bundle_is_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "blocked_or_expired_candidate_cannot_revive_without_governance",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "MidplatformModelDataHandlingDryRunProfile",
    "MidplatformModelCandidateIngressBundle",
    "MidplatformCandidateNormalizationResult",
    "MidplatformSourceChainAggregationResult",
    "MidplatformConfidencePolicyAggregationResult",
    "MidplatformConflictHandlingResult",
    "MidplatformUncertaintyHandlingResult",
    "MidplatformUnavailableReservedDegradedHandlingResult",
    "MidplatformEvidenceBundleCompositionResult",
    "MidplatformCandidateLifecycleResult",
    "MidplatformFieldTaskGuidanceSupportBundleResult",
    "MidplatformModelDataHandlingBoundaryResult",
    "MidplatformModelDataHandlingDryRunDecision",
)

FINAL_DECISION_GO = "MIDPLATFORM_MODEL_DATA_HANDLING_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "MIDPLATFORM_MODEL_DATA_HANDLING_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "midplatform_model_data_handling_dryrun_allowed": True,
    "candidate_ingress_allowed": True,
    "candidate_normalization_allowed": True,
    "source_chain_aggregation_allowed": True,
    "confidence_policy_aggregation_allowed": True,
    "conflict_handling_allowed": True,
    "uncertainty_handling_allowed": True,
    "unavailable_record_handling_allowed": True,
    "reserved_family_record_handling_allowed": True,
    "degraded_state_handling_allowed": True,
    "evidence_bundle_composition_allowed": True,
    "candidate_lifecycle_handling_allowed": True,
    "field_task_guidance_support_bundle_allowed": True,
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
class MidplatformModelDataHandlingDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    multi_model_interaction_dryrun_ref: str
    p1_output_adapter_dryrun_ref: str
    p0_baseline_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    data_handling_policy_ids: Tuple[str, ...]
    required_bundle_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelCandidateIngressBundle:
    handling_id: str
    policy_id: str
    candidate_refs: Tuple[str, ...]
    model_family_refs: Tuple[str, ...]
    source_chain: str
    mock_file_based: bool


@dataclass(frozen=True)
class MidplatformCandidateNormalizationResult:
    policy_id: str
    normalized: bool
    normalized_object_types: Tuple[str, ...]
    candidate_not_changed_into_fact: bool


@dataclass(frozen=True)
class MidplatformSourceChainAggregationResult:
    policy_id: str
    aggregated: bool
    lineage_preserved: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformConfidencePolicyAggregationResult:
    policy_id: str
    aggregated: bool
    high_confidence_does_not_create_fact: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformConflictHandlingResult:
    policy_id: str
    conflict_detected: bool
    candidate_only: bool
    resolved_as_fact: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformUncertaintyHandlingResult:
    policy_id: str
    uncertainty_propagated: bool
    candidate_only: bool
    triggers_action_speech_navigation: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformUnavailableReservedDegradedHandlingResult:
    policy_id: str
    unavailable_is_blocker: bool
    reserved_executed: bool
    degraded_triggers_runtime_action: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformEvidenceBundleCompositionResult:
    policy_id: str
    composed: bool
    is_fact_bundle: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformCandidateLifecycleResult:
    policy_id: str
    lifecycle_tracked: bool
    blocked_or_expired_revived_without_governance: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformFieldTaskGuidanceSupportBundleResult:
    policy_id: str
    support_bundle_built: bool
    candidate_only: bool
    guidance_is_runtime_navigation: bool
    speech_gate_is_tts: bool
    action_safety_triggers_action: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelDataHandlingBoundaryResult:
    policy_id: str
    boundary: str
    no_fact_admission: bool
    no_direct_ftg_write: bool
    no_action_speech_navigation: bool
    reserved_not_executed: bool


@dataclass
class MidplatformCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    policy_id: str = ""
    generated_objects: Tuple[str, ...] = field(default_factory=tuple)
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class MidplatformModelDataHandlingDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    upstream_stage_ref_count: int
    data_handling_policy_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    full_midplatform_model_data_handling_bundle_ok: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
