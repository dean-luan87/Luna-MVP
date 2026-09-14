# -*- coding: utf-8 -*-
"""Recognition Midplatform Model Governance Integrated Closure Post-Review — types v1.

Based on the already-GO Recognition Midplatform Model Governance Integrated Closure,
this phase performs a post-review only. It adds no model, adds no capability, runs no
model, runs no inference, downloads nothing, does not rewrite governance rules, and
does not enter runtime trial planning. The goal is to confirm whether the model
expansion + midplatform governance integrated closure is a trustworthy upstream
baseline for the future Model Governance Runtime Trial Planning.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-Post-Review-v1-001"
)
SCOPE = "recognition_midplatform_model_governance_integrated_closure_post_review"
SOURCE_CHAIN = (
    "recognition_midplatform_model_governance_integrated_closure_post_review_v1"
)

POST_REVIEW_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Midplatform Model Governance Integrated Closure，执行 post-review。该阶段只做"
    "事后复核，不新增模型，不新增能力，不运行模型，不执行 inference，不下载模型，不改写治理规则，不进入 runtime "
    "trial planning。目标是确认模型扩张 + 中台治理 integrated closure 是否具备作为后续 Model Governance Runtime "
    "Trial Planning 上游基线的可信度。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "post_review_audits_baseline_trust_only_no_capability_change_no_runtime_planning"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = (
    "recognition_midplatform_model_governance_integrated_closure_post_review_only"
)
POST_REVIEW_ONLY = True
INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_PHASE_REF = "Phase-Model-Governance-Runtime-Trial-Planning-v1-001"

INTEGRATED_CLOSURE_EXPECTED_GO = (
    "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_GO"
)

# Thresholds the post-review re-asserts against the closure artifact.
CLOSURE_EXPECTED_STAGE_REF_COUNT_MIN = 17
CLOSURE_EXPECTED_ARTIFACT_REF_COUNT_MIN = 4
CLOSURE_EXPECTED_CAPABILITY_COVERAGE_MIN = 5
CLOSURE_EXPECTED_CANDIDATE_COVERAGE_MIN = 60
CLOSURE_EXPECTED_NEGATIVE_GUARD_PASSED = 14

# --------------------------------------------------------------------------- #
# Coverage audit dimensions (4)
# --------------------------------------------------------------------------- #
COVERAGE_AUDIT_DIMENSIONS: Tuple[str, ...] = (
    "p1_p2_output_candidate_coverage_complete",
    "interaction_candidate_coverage_complete",
    "midplatform_data_handling_coverage_complete",
    "midplatform_model_control_coverage_complete",
)

# --------------------------------------------------------------------------- #
# Boundary audit items (16) — must still hold in the closure artifact.
# --------------------------------------------------------------------------- #
BOUNDARY_AUDIT_ITEMS: Tuple[str, ...] = (
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

# Condensed boundary GO keys.
CONDENSED_BOUNDARY_GO_KEYS: Tuple[str, ...] = (
    "candidate_only_boundary_preserved",
    "fact_admission_blocked",
    "runtime_activation_blocked",
    "commercial_runtime_not_approved",
    "reserved_only_family_not_executed",
    "vla_action_chain_excluded",
    "luna_emotion_multimodal_brain_first_preserved",
)

# --------------------------------------------------------------------------- #
# Negative guard audit (14) — re-audit the closure's negative closure guards.
# --------------------------------------------------------------------------- #
NEGATIVE_GUARD_AUDIT_IDS: Tuple[str, ...] = (
    "invalid_upstream_go_missing",
    "invalid_p1_p2_output_adapter_coverage_missing",
    "invalid_multi_model_interaction_coverage_missing",
    "invalid_midplatform_data_handling_coverage_missing",
    "invalid_midplatform_model_control_coverage_missing",
    "invalid_candidate_ingress_fact_admission",
    "invalid_agreement_conflict_fact_write",
    "invalid_fallback_download_inference",
    "invalid_reserved_family_execution",
    "invalid_candidate_gate_fact_admission",
    "invalid_guidance_speech_action_runtime",
    "invalid_vla_action_chain_current_scope",
    "invalid_model_tuning_dataset_usage_approval",
    "invalid_commercial_runtime_approval",
)

# --------------------------------------------------------------------------- #
# Handoff readiness targets (5) — recorded only, not entered.
# --------------------------------------------------------------------------- #
HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-Model-Governance-Runtime-Trial-Planning-v1-001",
        "go_key": "runtime_trial_planning_readiness_recorded",
    },
    {
        "target_ref": "Phase-Recognition-Model-P1-Download-License-Planning-v1-001",
        "go_key": "p1_download_license_planning_readiness_recorded",
    },
    {
        "target_ref": "Phase-Recognition-Model-P1-Real-Output-Adapter-DryRun-v1-001",
        "go_key": "p1_real_output_adapter_readiness_recorded",
    },
    {
        "target_ref": "Phase-Future-Emotion-Multimodal-Bridge-Planning-v1-001",
        "go_key": "emotion_multimodal_bridge_planning_readiness_recorded",
    },
    {
        "target_ref": "Phase-Future-Audio-Speech-Evidence-Planning-v1-001",
        "go_key": "audio_speech_evidence_planning_readiness_recorded",
    },
)

# --------------------------------------------------------------------------- #
# Governance rules (22)
# --------------------------------------------------------------------------- #
POST_REVIEW_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_post_review_only",
    "no_new_model_is_added",
    "no_new_model_download_is_allowed",
    "no_inference_is_allowed",
    "no_new_image_or_video_recognition_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "no_training_is_allowed",
    "runtime_trial_planning_is_not_executed_in_this_phase",
    "integrated_closure_artifact_must_be_verified",
    "four_sealed_layer_artifacts_must_be_verified",
    "gated_upstream_go_must_be_verified",
    "ref_only_stages_must_remain_lineage_references_only",
    "candidate_only_boundary_must_remain_intact",
    "fact_admission_must_remain_blocked",
    "runtime_activation_must_remain_blocked",
    "commercial_runtime_must_remain_unapproved",
    "reserved_only_families_must_remain_non_executing",
    "vla_action_chain_must_remain_excluded",
    "luna_emotion_multimodal_brain_cognition_first_principle_must_remain_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "ModelGovernanceIntegratedClosurePostReviewProfile",
    "ModelGovernancePostReviewStageAudit",
    "ModelGovernancePostReviewArtifactAudit",
    "ModelGovernancePostReviewCoverageAudit",
    "ModelGovernancePostReviewBoundaryAudit",
    "ModelGovernancePostReviewNegativeGuardAudit",
    "ModelGovernancePostReviewHandoffReadiness",
    "ModelGovernanceIntegratedClosurePostReviewDecision",
)

FINAL_DECISION_GO = (
    "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_POST_REVIEW_GO"
)
FINAL_DECISION_BLOCKED = (
    "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_POST_REVIEW_BLOCKED"
)

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
    "runtime_trial_planning_allowed": False,
    "runtime_activation_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class ModelGovernanceIntegratedClosurePostReviewProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    post_review_only: bool
    integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    coverage_audit_dimensions: Tuple[str, ...]
    boundary_audit_items: Tuple[str, ...]
    negative_guard_audit_ids: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelGovernancePostReviewStageAudit:
    stage_index: int
    phase_ref: str
    expected_go: str
    gated: bool
    go_verified: bool


@dataclass(frozen=True)
class ModelGovernancePostReviewArtifactAudit:
    layer: str
    phase_ref: str
    artifact_rel: str
    final_decision: str
    blocker_count: int
    failed_checks_empty: bool
    sealed_ok: bool


@dataclass(frozen=True)
class ModelGovernancePostReviewCoverageAudit:
    dimension: str
    closure_reported: bool
    audit_ok: bool


@dataclass(frozen=True)
class ModelGovernancePostReviewBoundaryAudit:
    boundary_item: str
    closure_reported: bool
    still_holds: bool


@dataclass(frozen=True)
class ModelGovernancePostReviewNegativeGuardAudit:
    guard_id: str
    closure_passed: bool
    still_blocks: bool


@dataclass(frozen=True)
class ModelGovernancePostReviewHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class ModelGovernanceIntegratedClosurePostReviewDecision:
    decision_ref: str
    post_review_profile_count: int
    stage_ref_audit_count: int
    artifact_audit_count: int
    coverage_audit_count: int
    boundary_audit_count: int
    negative_guard_audit_count: int
    handoff_readiness_count: int
    integrated_closure_go_verified: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
