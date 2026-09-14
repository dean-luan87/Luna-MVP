# -*- coding: utf-8 -*-
"""Recognition Model P1 Download / License Planning — types v1.

This phase converges the current P1/P2 recognition-model system from a *planning
state* into a *runnable-asset state*. It is NOT a download phase and NOT a runtime
phase: it only structures every P1/P2 model into a unified runnable-asset record
(ModelAsset) with its license contract, runtime feasibility, download eligibility,
dependency profile, execution constraint, fallback strategy and availability state.

Core principles:
1. This is planning-only convergence ("planning -> runnable-asset list"), never
   a real download, never inference, never runtime execution.
2. download_allowed = True is a *planning decision* only: no auto-download, no
   runtime execution, no dataset pull — only a planning state transition.
3. License decides runtime eligibility: Apache/MIT -> runtime eligible; AGPL ->
   test-only / no commercial runtime; Unknown -> blocked until review; research-
   only datasets -> no runtime ingestion.
4. Reserved-only families (emotion bridge, etc.) stay runtime-blocked.
5. All model outputs must still become an evidence candidate and pass adapter +
   midplatform; governance reuse must be preserved (no governance bypass).
6. Luna remains emotion-multimodal brain / cognition first, with no VLA action chain.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-P1-Download-License-Planning-v1-001"
SCOPE = "recognition_model_p1_download_license_planning"
SOURCE_CHAIN = "recognition_model_p1_download_license_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "把当前 P1/P2 识别模型体系从“规划态”结构化收敛为“可运行资产态”。本阶段不是下载、不是 runtime，"
    "而是把每个 P1/P2 模型收敛为统一的可运行资产记录（ModelAsset）：包含 LicenseContract、RuntimeFeasibility、"
    "DownloadEligibility、DependencyProfile、ExecutionConstraint、FallbackStrategy、AvailabilityState。"
    "download_allowed=true 仅为规划决策：no auto-download、no runtime execution、no dataset pull、"
    "only planning state transition。License 决定 runtime 资格：Apache/MIT → runtime eligible；"
    "AGPL → test-only / no commercial runtime；Unknown → blocked until review；research-only datasets → "
    "no runtime ingestion。reserved-only 模型族保持 runtime 阻断。所有模型输出仍须先成为 evidence candidate 且"
    "经 adapter + 中台，治理复用必须保持（no governance bypass）。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_download_license_planning_converges_models_into_runnable_assets_planning_only_no_download_no_inference_no_runtime"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
PLANNING_MODE = "recognition_model_p1_download_license_planning_only"
PLANNING_ONLY = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_ADMISSION_CONTRACT_CREATED = False
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

RUNTIME_TRIAL_PLANNING_REF = "Phase-Model-Governance-Runtime-Trial-Planning-v1-001"
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = "p1_execution_dryrun_foundation"

RUNTIME_TRIAL_PLANNING_EXPECTED_GO = "MODEL_GOVERNANCE_RUNTIME_TRIAL_PLANNING_GO"

# --------------------------------------------------------------------------- #
# 1. Model family tiers (7)
# --------------------------------------------------------------------------- #
MODEL_FAMILY_TIERS: Tuple[Dict[str, str], ...] = (
    {"tier_code": "P1-A", "family": "segmentation", "tier_level_summary": "level_1_to_2_mixed"},
    {"tier_code": "P1-B", "family": "tracking", "tier_level_summary": "level_1_to_2_mixed"},
    {"tier_code": "P1-C", "family": "depth_spatial_hint", "tier_level_summary": "level_1_to_2_mixed"},
    {"tier_code": "P1-D", "family": "object_detection_completion", "tier_level_summary": "level_1_to_2_mixed"},
    {"tier_code": "P2", "family": "scene_relation_vlm", "tier_level_summary": "level_0_deferred"},
    {"tier_code": "P2", "family": "audio_speech", "tier_level_summary": "level_0_to_1_mixed"},
    {"tier_code": "P2", "family": "emotion_multimodal_bridge", "tier_level_summary": "level_0_reserved_only"},
)

# --------------------------------------------------------------------------- #
# 2. Model-asset matrix (runnable-asset planning, candidate/contract only)
#    Each row -> one ModelAsset + derived contract/feasibility/download/dep/
#    constraint/availability records.
# --------------------------------------------------------------------------- #
MODEL_ASSET_MATRIX: Tuple[Dict[str, Any], ...] = (
    # ---- P1-A Segmentation ---- #
    {
        "model_id": "mobile_sam",
        "tier_code": "P1-A",
        "family": "segmentation",
        "license_type": "apache_like",
        "availability_state": "downloadable",
        "runtime_eligibility_level": 2,
        "cpu_runnable": True,
        "gpu_preferred": False,
        "dependency_weight": "light",
        "dependency_stable": True,
        "note": "可下载（Apache-like）",
    },
    {
        "model_id": "fast_sam",
        "tier_code": "P1-A",
        "family": "segmentation",
        "license_type": "agpl_3_0",
        "availability_state": "downloadable_test_only",
        "runtime_eligibility_level": 2,
        "cpu_runnable": True,
        "gpu_preferred": True,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "可下载但 AGPL 风险标记，test-only / no commercial runtime",
    },
    {
        "model_id": "sam2",
        "tier_code": "P1-A",
        "family": "segmentation",
        "license_type": "unknown",
        "availability_state": "deferred",
        "runtime_eligibility_level": 1,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "heavy",
        "dependency_stable": False,
        "note": "deferred（依赖未稳定）",
    },
    # ---- P1-B Tracking ---- #
    {
        "model_id": "byte_track",
        "tier_code": "P1-B",
        "family": "tracking",
        "license_type": "mit",
        "availability_state": "runnable",
        "runtime_eligibility_level": 2,
        "cpu_runnable": True,
        "gpu_preferred": False,
        "dependency_weight": "light",
        "dependency_stable": True,
        "note": "可运行（MIT）",
    },
    {
        "model_id": "deep_sort",
        "tier_code": "P1-B",
        "family": "tracking",
        "license_type": "mit",
        "availability_state": "runnable",
        "runtime_eligibility_level": 2,
        "cpu_runnable": True,
        "gpu_preferred": False,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "可运行（MIT）",
    },
    {
        "model_id": "supervision",
        "tier_code": "P1-B",
        "family": "tracking",
        "license_type": "mit",
        "availability_state": "wrapper_dependency",
        "runtime_eligibility_level": 1,
        "cpu_runnable": True,
        "gpu_preferred": False,
        "dependency_weight": "light",
        "dependency_stable": True,
        "note": "wrapper级依赖",
    },
    # ---- P1-C Depth / Spatial Hint ---- #
    {
        "model_id": "midas",
        "tier_code": "P1-C",
        "family": "depth_spatial_hint",
        "license_type": "mit",
        "availability_state": "runnable",
        "runtime_eligibility_level": 2,
        "cpu_runnable": True,
        "gpu_preferred": False,
        "dependency_weight": "light",
        "dependency_stable": True,
        "note": "CPU可运行（轻量）",
    },
    {
        "model_id": "depth_anything",
        "tier_code": "P1-C",
        "family": "depth_spatial_hint",
        "license_type": "apache_2_0",
        "availability_state": "partial_availability",
        "runtime_eligibility_level": 1,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "GPU preferred（部分可运行）",
    },
    {
        "model_id": "zoe_depth",
        "tier_code": "P1-C",
        "family": "depth_spatial_hint",
        "license_type": "mit",
        "availability_state": "deferred",
        "runtime_eligibility_level": 1,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "heavy",
        "dependency_stable": False,
        "note": "deferred（依赖重）",
    },
    # ---- P1-D Object Detection Completion ---- #
    {
        "model_id": "yolov8n",
        "tier_code": "P1-D",
        "family": "object_detection_completion",
        "license_type": "agpl_3_0",
        "availability_state": "test_only_local_weight",
        "runtime_eligibility_level": 2,
        "cpu_runnable": True,
        "gpu_preferred": True,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "test-only（已存在权重路径），AGPL no commercial runtime",
    },
    {
        "model_id": "rt_detr",
        "tier_code": "P1-D",
        "family": "object_detection_completion",
        "license_type": "apache_2_0",
        "availability_state": "partial_availability",
        "runtime_eligibility_level": 1,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "partial availability",
    },
    {
        "model_id": "grounding_dino",
        "tier_code": "P1-D",
        "family": "object_detection_completion",
        "license_type": "apache_2_0",
        "availability_state": "deferred",
        "runtime_eligibility_level": 1,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "heavy",
        "dependency_stable": False,
        "note": "deferred（依赖/体积/稳定性）",
    },
    # ---- P2 Scene Relation / VLM (all deferred) ---- #
    {
        "model_id": "scene_relation_vlm",
        "tier_code": "P2",
        "family": "scene_relation_vlm",
        "license_type": "unknown",
        "availability_state": "deferred",
        "runtime_eligibility_level": 0,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "heavy",
        "dependency_stable": False,
        "note": "deferred（输出不稳定 + compute heavy）",
    },
    {
        "model_id": "open_vocab_vlm",
        "tier_code": "P2",
        "family": "scene_relation_vlm",
        "license_type": "unknown",
        "availability_state": "deferred",
        "runtime_eligibility_level": 0,
        "cpu_runnable": False,
        "gpu_preferred": True,
        "dependency_weight": "heavy",
        "dependency_stable": False,
        "note": "deferred（输出不稳定 + compute heavy）",
    },
    # ---- P2 Audio / Speech ---- #
    {
        "model_id": "sense_voice",
        "tier_code": "P2",
        "family": "audio_speech",
        "license_type": "apache_2_0",
        "availability_state": "partial_availability",
        "runtime_eligibility_level": 1,
        "cpu_runnable": True,
        "gpu_preferred": True,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "partial availability",
    },
    {
        "model_id": "pyannote",
        "tier_code": "P2",
        "family": "audio_speech",
        "license_type": "unknown",
        "availability_state": "requires_license_review",
        "runtime_eligibility_level": 0,
        "cpu_runnable": True,
        "gpu_preferred": True,
        "dependency_weight": "medium",
        "dependency_stable": True,
        "note": "requires license review，blocked until review",
    },
    # ---- P2 Emotion Bridge (reserved-only) ---- #
    {
        "model_id": "emotion_multimodal_bridge",
        "tier_code": "P2",
        "family": "emotion_multimodal_bridge",
        "license_type": "unknown",
        "availability_state": "reserved_only",
        "runtime_eligibility_level": 0,
        "cpu_runnable": False,
        "gpu_preferred": False,
        "dependency_weight": "heavy",
        "dependency_stable": False,
        "note": "reserved-only（不进入 runtime）",
    },
)

# --------------------------------------------------------------------------- #
# 3. License decision matrix (4)
# --------------------------------------------------------------------------- #
LICENSE_DECISION_MATRIX: Tuple[Dict[str, Any], ...] = (
    {
        "license_class": "apache_or_mit",
        "runtime_eligible": True,
        "commercial_runtime_allowed": True,
        "decision": "runtime_eligible",
    },
    {
        "license_class": "agpl",
        "runtime_eligible": False,
        "commercial_runtime_allowed": False,
        "decision": "test_only_no_commercial_runtime",
    },
    {
        "license_class": "unknown",
        "runtime_eligible": False,
        "commercial_runtime_allowed": False,
        "decision": "blocked_until_review",
    },
    {
        "license_class": "research_only_dataset",
        "runtime_eligible": False,
        "commercial_runtime_allowed": False,
        "decision": "no_runtime_ingestion",
    },
)


def license_class_for(license_type: str) -> str:
    if license_type in ("apache_2_0", "apache_like", "mit"):
        return "apache_or_mit"
    if license_type in ("agpl_3_0",):
        return "agpl"
    if license_type in ("research_only", "research_only_dataset"):
        return "research_only_dataset"
    return "unknown"


def license_decision_for(license_type: str) -> Dict[str, Any]:
    klass = license_class_for(license_type)
    for row in LICENSE_DECISION_MATRIX:
        if row["license_class"] == klass:
            return row
    return LICENSE_DECISION_MATRIX[2]  # default unknown -> blocked_until_review

# --------------------------------------------------------------------------- #
# 4. Runtime eligibility levels (5: Level 0..4)
# --------------------------------------------------------------------------- #
RUNTIME_ELIGIBILITY_LEVELS: Tuple[Dict[str, Any], ...] = (
    {"level": 0, "label": "blocked", "description": "blocked_no_runtime"},
    {"level": 1, "label": "planning_only", "description": "planning_only_not_executed"},
    {"level": 2, "label": "test_only", "description": "test_only_offline_inference_allowed_future"},
    {"level": 3, "label": "controlled_runtime_eligible", "description": "controlled_runtime_eligible_future"},
    {"level": 4, "label": "full_runtime", "description": "full_runtime_future_NOT_now"},
)

# Current convergence snapshot (recorded only).
TIER_LEVEL_SNAPSHOT: Dict[str, str] = {
    "p0": "level_2_verified",
    "p1": "level_1_to_2_mixed",
    "p2": "level_0_to_1",
}

# --------------------------------------------------------------------------- #
# 5. Download eligibility policy (planning decision only)
# --------------------------------------------------------------------------- #
DOWNLOAD_ELIGIBILITY_POLICY: Dict[str, bool] = {
    "download_allowed": True,
    "no_auto_download": True,
    "no_runtime_execution": True,
    "no_dataset_pull": True,
    "only_planning_state_transition": True,
}

# --------------------------------------------------------------------------- #
# 6. Fallback strategies (>= 6, candidate-only)
# --------------------------------------------------------------------------- #
FALLBACK_STRATEGIES: Tuple[Dict[str, str], ...] = (
    {"trigger": "model_unavailable", "fallback_route": "fallback_to_available_family_member_candidate"},
    {"trigger": "license_unclear_or_unknown", "fallback_route": "blocked_until_review_record"},
    {"trigger": "agpl_commercial_runtime_requested", "fallback_route": "downgrade_to_test_only"},
    {"trigger": "dependency_unstable_or_heavy", "fallback_route": "deferred_planning_record"},
    {"trigger": "gpu_unavailable", "fallback_route": "cpu_fallback_or_defer"},
    {"trigger": "reserved_only_family_request", "fallback_route": "runtime_blocked_reserved_record"},
)

# --------------------------------------------------------------------------- #
# 7. Negative guards (7) — id -> (go_key, depends_on invariant)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {
        "guard_id": "invalid_inference_trigger",
        "go_key": "no_inference_trigger",
        "depends_on": "real_inference_not_allowed",
    },
    {
        "guard_id": "invalid_dataset_download",
        "go_key": "no_dataset_download",
        "depends_on": "dataset_download_not_allowed",
    },
    {
        "guard_id": "invalid_auto_model_pull",
        "go_key": "no_auto_model_pull",
        "depends_on": "auto_model_pull_not_allowed",
    },
    {
        "guard_id": "invalid_vla_action_activation",
        "go_key": "no_vla_action_activation",
        "depends_on": "vla_action_chain_not_allowed",
    },
    {
        "guard_id": "invalid_semantic_promotion",
        "go_key": "no_semantic_promotion",
        "depends_on": "semantic_promotion_not_allowed",
    },
    {
        "guard_id": "invalid_runtime_escalation",
        "go_key": "no_runtime_escalation",
        "depends_on": "runtime_escalation_not_allowed",
    },
    {
        "guard_id": "invalid_governance_bypass",
        "go_key": "no_governance_bypass",
        "depends_on": "governance_reuse_preserved",
    },
)

# --------------------------------------------------------------------------- #
# Governance rules (24)
# --------------------------------------------------------------------------- #
PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_p1_p2_download_license_planning_only",
    "planning_converges_models_into_runnable_asset_list_not_runtime",
    "download_allowed_is_a_planning_decision_only",
    "no_auto_download_is_enforced",
    "no_runtime_execution_is_enforced",
    "no_dataset_pull_is_enforced",
    "no_real_inference_is_enforced",
    "license_decides_runtime_eligibility",
    "apache_or_mit_is_runtime_eligible",
    "agpl_is_test_only_no_commercial_runtime",
    "unknown_license_is_blocked_until_review",
    "research_only_datasets_have_no_runtime_ingestion",
    "reserved_only_families_are_runtime_blocked",
    "runtime_eligibility_level_4_full_runtime_is_not_now",
    "p0_remains_level_2_verified",
    "model_output_must_pass_recognition_model_output_adapter",
    "model_output_must_pass_midplatform_model_data_handling",
    "model_output_must_pass_midplatform_model_control",
    "candidate_only_boundary_must_be_preserved",
    "no_semantic_promotion_without_review",
    "no_runtime_escalation_from_planning",
    "vla_action_chain_is_excluded",
    "existing_governance_must_be_reused_no_governance_bypass",
    "p1_execution_dryrun_foundation_requires_separate_phase",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelP1DownloadLicensePlanningProfile",
    "ModelAsset",
    "LicenseContract",
    "RuntimeFeasibility",
    "DownloadEligibility",
    "DependencyProfile",
    "ExecutionConstraint",
    "FallbackStrategy",
    "AvailabilityState",
    "RuntimeEligibilityLevel",
    "P1DownloadLicensePlanningNegativeGuard",
    "P1DownloadLicensePlanningHandoffReadiness",
    "RecognitionModelP1DownloadLicensePlanningDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-P1-Execution-DryRun-Foundation-v1-001",
        "go_key": "p1_execution_dryrun_foundation_readiness_recorded",
    },
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_P1_DOWNLOAD_LICENSE_PLANNING_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_P1_DOWNLOAD_LICENSE_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
}

NEGATED_CREATION_FLAGS: Dict[str, bool] = {
    "new_admission_contract_created": False,
    "new_runtime_governance_created": False,
}

PLANNING_TRUE_INVARIANTS: Dict[str, bool] = {
    "models_converged_into_runnable_asset_list": True,
    "license_decides_runtime_eligibility": True,
    "reserved_only_family_runtime_blocked": True,
    "candidate_only_boundary_preserved": True,
    "model_output_adapter_required": True,
    "midplatform_data_handling_required": True,
    "midplatform_model_control_required": True,
    "governance_reuse_preserved": True,
    "p0_level2_verified": True,
    "p1_level_mixed_recorded": True,
    "p2_level_low_recorded": True,
    "full_runtime_level_4_not_now": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "runtime_execution_allowed": False,
    "auto_download_allowed": False,
    "auto_model_pull_allowed": False,
    "dataset_download_allowed": False,
    "dataset_pull_allowed": False,
    "dataset_usage_allowed": False,
    "model_tuning_allowed": False,
    "training_use_allowed": False,
    "new_image_recognition_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "runtime_activation_allowed": False,
    "runtime_escalation_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "semantic_promotion_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelP1DownloadLicensePlanningProfile:
    profile_ref: str
    phase_id: str
    planning_mode: str
    planning_only: bool
    existing_governance_reuse_required: bool
    new_admission_contract_created: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    runtime_trial_planning_ref: str
    model_governance_integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    download_eligibility_policy: Dict[str, bool]
    tier_level_snapshot: Dict[str, str]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class ModelAsset:
    model_id: str
    tier_code: str
    family: str
    license_type: str
    availability_state: str
    runtime_eligibility_level: int
    runtime_eligibility_label: str
    download_allowed: bool
    runtime_eligible: bool
    note: str


@dataclass(frozen=True)
class LicenseContract:
    model_id: str
    license_type: str
    license_class: str
    runtime_eligible: bool
    commercial_runtime_allowed: bool
    decision: str


@dataclass(frozen=True)
class RuntimeFeasibility:
    model_id: str
    runtime_eligibility_level: int
    cpu_runnable: bool
    gpu_preferred: bool
    feasible_for_test_only: bool
    runtime_execution_now: bool


@dataclass(frozen=True)
class DownloadEligibility:
    model_id: str
    download_allowed: bool
    auto_download: bool
    requires_review: bool
    only_planning_state_transition: bool


@dataclass(frozen=True)
class DependencyProfile:
    model_id: str
    dependency_weight: str
    dependency_stable: bool
    deferred_for_dependency: bool


@dataclass(frozen=True)
class ExecutionConstraint:
    model_id: str
    no_runtime_execution: bool
    no_real_inference: bool
    no_auto_download: bool
    must_pass_adapter_and_midplatform: bool
    candidate_only: bool


@dataclass(frozen=True)
class FallbackStrategy:
    trigger: str
    fallback_route: str
    candidate_only: bool
    triggers_download_or_inference: bool


@dataclass(frozen=True)
class AvailabilityState:
    model_id: str
    state: str
    runtime_eligibility_level: int


@dataclass(frozen=True)
class RuntimeEligibilityLevel:
    level: int
    label: str
    description: str
    runtime_now: bool


@dataclass
class P1DownloadLicensePlanningNegativeGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class P1DownloadLicensePlanningHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class RecognitionModelP1DownloadLicensePlanningDecision:
    decision_ref: str
    planning_profile_count: int
    model_family_tier_count: int
    model_asset_count: int
    license_contract_count: int
    license_decision_matrix_count: int
    runtime_eligibility_level_count: int
    runtime_feasibility_count: int
    download_eligibility_count: int
    dependency_profile_count: int
    execution_constraint_count: int
    fallback_strategy_count: int
    availability_state_count: int
    negative_guard_count: int
    negative_guard_passed: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
