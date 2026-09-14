# -*- coding: utf-8 -*-
"""Phase One Environment Cognition Evidence Baseline Handoff Review — types v1.

Baseline Handoff Review over the already-frozen Luna Phase-One environment
cognition evidence main chain. This phase adds NO new capability, NO new
information source, runs NO dry-run, connects NO runtime. It only confirms that
the Phase One Environment Cognition Evidence Main Chain Closure can serve as the
stable upstream baseline for downstream phases (Visual Symbol Evidence DryRun,
real-recognition dry-run, future audio/behavior/memory/map expansion). It is a
mainline handoff point only — to keep downstream references unambiguous.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-PhaseOne-Environment-Cognition-Evidence-Baseline-Handoff-Review-v1-001"
SCOPE = "phase_one_environment_cognition_evidence_baseline_handoff_review"
SOURCE_CHAIN = "phase_one_environment_cognition_evidence_baseline_handoff_review_v1"

HANDOFF_PRINCIPLE_ZH = (
    "对已冻结的 Luna 一期环境认知 evidence 主链做 Baseline Handoff Review。不新增能力、不新增信息源、"
    "不做 dry-run、不接 runtime，只确认 Phase One Environment Cognition Evidence Main Chain Closure 可"
    "作为后续 Visual Symbol Evidence DryRun、真实识别 dry-run、音频/行为/记忆/地图等未来扩展阶段的稳定"
    "上游基线。这是主线交接点，避免后续阶段引用混乱。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "phase_one_environment_cognition_evidence_baseline_handoff_review_only"
BASELINE_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
BASELINE_FINAL_DECISION = "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_MAIN_CHAIN_CLOSURE_GO"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
MAIN_CHAIN_CLOSURE_REF = BASELINE_REF
RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
)
SLAM_BACKEND_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-SLAM-Backend-Evidence-Chain-Integrated-Closure-v1-001"
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

HANDOFF_TARGET_REFS: Tuple[str, ...] = (
    "Phase-Visual-Symbol-Evidence-DryRun-v1-001",
    "Phase-PhaseOne-Real-Recognition-DryRun-v1-001",
)

# --------------------------------------------------------------------------- #
# Handoff targets (readiness, recorded as ready — not started here)
# --------------------------------------------------------------------------- #
HANDOFF_READINESS_FLAGS: Dict[str, bool] = {
    "ready_for_visual_symbol_evidence_dryrun": True,
    "ready_for_real_recognition_dryrun_planning": True,
    "ready_for_future_audio_evidence_planning_when_requested": True,
    "ready_for_future_relation_mechanism_planning_when_requested": True,
}

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
HANDOFF_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_handoff_review_only",
    "no_new_capability_is_added",
    "no_new_information_source_is_added",
    "no_deferred_expansion_is_expanded_in_this_phase",
    "no_dryrun_execution",
    "no_runtime_activation",
    "no_model_download_no_dataset_download_no_training",
    "no_live_camera_live_sensor_gps_map_api_ros_imu",
    "no_navigation_action_speech_fact_write",
    "main_chain_closure_remains_the_current_baseline",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

HANDOFF_OBJECT_TYPES: Tuple[str, ...] = (
    "PhaseOneEvidenceBaselineHandoffReviewProfile",
    "PhaseOneEvidenceBaselineUpstreamRef",
    "PhaseOneEvidenceBaselineScopeSummary",
    "PhaseOneEvidenceBaselineDeferredExpansionSummary",
    "PhaseOneEvidenceBaselineHandoffDecision",
)

FINAL_DECISION_GO = "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_BASELINE_HANDOFF_REVIEW_GO"
FINAL_DECISION_BLOCKED = (
    "PHASE_ONE_ENVIRONMENT_COGNITION_EVIDENCE_BASELINE_HANDOFF_REVIEW_BLOCKED"
)

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "new_capability_added": False,
    "new_information_source_added": False,
    "deferred_expansion_expanded": False,
    "dryrun_execution_allowed": False,
    "runtime_activation_allowed": False,
    "model_download_allowed": False,
    "dataset_download_allowed": False,
    "training_use_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "real_gps_connected": False,
    "real_map_api_connected": False,
    "ros_connected": False,
    "imu_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}

DEFERRED_EXPANSION_IDS: Tuple[str, ...] = (
    "audio_evidence",
    "human_behavior_gesture_crowd_flow_evidence",
    "surface_physical_risk_evidence",
    "perception_quality_evidence",
    "environment_event_temporal_change_evidence",
    "user_state_evidence",
    "memory_context_evidence",
    "external_map_poi_hint_evidence",
    "latent_information_association_mechanism",
    "hidden_object_object_relation_mechanism",
)


@dataclass(frozen=True)
class PhaseOneEvidenceBaselineHandoffReviewProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    baseline_ref: str
    baseline_final_decision: str
    controlled_trial_governance_template_ref: str
    handoff_target_refs: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class PhaseOneEvidenceBaselineUpstreamRef:
    upstream_ref: str
    artifact_rel: str
    expected_final_decision: str
    verify_flag: str


@dataclass(frozen=True)
class PhaseOneEvidenceBaselineScopeSummary:
    summary_ref: str
    rgb_vision_evidence_baseline_frozen: bool
    slam_spatial_evidence_baseline_frozen: bool
    cross_modal_alignment_baseline_frozen: bool
    field_task_guidance_candidate_path_frozen: bool
    deferred_expansion_record_preserved: bool


@dataclass(frozen=True)
class PhaseOneEvidenceBaselineDeferredExpansionSummary:
    summary_ref: str
    deferred_expansion_ids: Tuple[str, ...]
    future_information_source_expansion_deferred: bool
    latent_relation_mechanism_deferred: bool
    hidden_object_relation_mechanism_deferred: bool


@dataclass(frozen=True)
class PhaseOneEvidenceBaselineHandoffDecision:
    decision_ref: str
    handoff_review_profile_count: int
    upstream_ref_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
