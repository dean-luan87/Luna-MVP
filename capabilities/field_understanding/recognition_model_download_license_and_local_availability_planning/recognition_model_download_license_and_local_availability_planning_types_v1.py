# -*- coding: utf-8 -*-
"""Recognition Model Download / License / Local Availability Planning — types v1.

Inserted before any real-model dry-run. Before a single weight is downloaded,
this phase decides — at planning level only — which recognition models may be
downloaded, from where, under which license / commercial-use status, with what
size / dependency footprint, whether the local environment can run them, whether
a GPU is required, whether they support offline use, whether their output format
is stable, and what the fallback is on failure.

It produces a P0/P1/P2 batch admission plan so the first batch stays small and
does not get blocked by heavy model dependencies.

This phase performs NO download, NO install, NO clone, NO inference, NO dataset
usage, NO training, NO live sensors and triggers NO navigation/action/speech/
fact_write. It only plans.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001"
SCOPE = "recognition_model_download_license_and_local_availability_planning"
SOURCE_CHAIN = "recognition_model_download_license_and_local_availability_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "在下载任何模型权重之前,先做下载/license/本地可用性规划。仅在规划层决定:哪些模型允许下载、"
    "下载来源、license 是否允许当前用途、模型体积与依赖是否可接受、本地环境是否能运行、是否需要 GPU、"
    "是否支持离线、输出格式是否稳定、失败时是否可降级。并给出 P0/P1/P2 分批接入顺序,避免一开始被"
    "大型模型依赖拖住。本阶段不下载、不安装、不 clone、不跑 inference、不用数据集、不训练、不接 "
    "live sensor,不触发 navigation/action/speech/fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_download_license_and_local_availability_planning_only"
INVOCATION_FEASIBILITY_DRYRUN_REF = (
    "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"
)
SYSTEM_ADMISSION_PLANNING_REF = (
    "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001"
DEFERRED_NEXT_AFTER_DOWNLOAD = "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Batch tiers
# --------------------------------------------------------------------------- #
TIER_P0 = "P0"
TIER_P1 = "P1"
TIER_P2 = "P2"
ADMISSION_TIER_ORDER: Tuple[str, ...] = (TIER_P0, TIER_P1, TIER_P2)

EXPECTED_TIER_COUNTS: Dict[str, int] = {TIER_P0: 3, TIER_P1: 2, TIER_P2: 2}

# --------------------------------------------------------------------------- #
# Model roles (one P0/P1/P2 candidate per recognition family/role)
# --------------------------------------------------------------------------- #
MODEL_ROLE_IDS: Tuple[str, ...] = (
    "ocr",
    "object_detection",
    "visual_symbol",
    "segmentation",
    "tracking",
    "depth_spatial_hint",
    "scene_relation",
)

# --------------------------------------------------------------------------- #
# Required plan fields and decision dimensions
# --------------------------------------------------------------------------- #
REQUIRED_PLAN_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_role",
    "model_family",
    "tier",
    "download_allowed",
    "download_source",
    "model_weight_required",
    "license_ref",
    "license_allows_current_use",
    "commercial_use_status",
    "size_estimate",
    "dependencies",
    "dependencies_acceptable",
    "local_env_can_run",
    "gpu_required",
    "offline_supported",
    "output_format_stable",
    "fallback_on_failure",
)

# Plan rejected if any of these is missing/empty.
REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "model_role",
    "model_family",
    "tier",
    "download_source",
    "license_ref",
    "fallback_on_failure",
)

# Plan rejected if any of these boolean decisions is not satisfied.
REJECT_IF_FALSE_FIELDS: Tuple[str, ...] = (
    "license_allows_current_use",
    "dependencies_acceptable",
    "local_env_can_run",
)

# Any of these flags True in a plan -> reject (planning phase must not execute).
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "real_download_requested",
    "real_install_requested",
    "repo_clone_requested",
    "real_inference_requested",
    "dataset_download_requested",
    "training_requested",
    "runtime_activation_requested",
    "live_sensor_requested",
)

# --------------------------------------------------------------------------- #
# Decision dimensions (for documentation / coverage)
# --------------------------------------------------------------------------- #
PLANNING_DECISION_DIMENSIONS: Tuple[str, ...] = (
    "which_models_allowed_to_download",
    "download_source",
    "license_allows_current_use",
    "model_size_and_dependencies_acceptable",
    "local_env_can_run",
    "gpu_required",
    "offline_supported",
    "output_format_stable",
    "fallback_on_failure",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_download_license_local_availability_planning_only",
    "no_model_is_downloaded_in_this_phase",
    "no_install_in_this_phase",
    "no_repo_clone_in_this_phase",
    "no_real_inference_in_this_phase",
    "no_real_image_video_recognition_in_this_phase",
    "no_dataset_usage_in_this_phase",
    "no_training_in_this_phase",
    "no_dataset_download_in_this_phase",
    "license_must_be_evaluated_before_any_download",
    "license_must_allow_current_use_or_model_is_rejected",
    "commercial_use_status_must_be_recorded",
    "download_source_must_be_explicit_and_trusted",
    "model_size_and_dependencies_must_be_acceptable",
    "local_env_must_be_able_to_run_model_or_model_is_rejected",
    "gpu_requirement_must_be_recorded",
    "offline_support_must_be_recorded",
    "output_format_stability_must_be_recorded",
    "fallback_on_failure_must_be_defined",
    "first_batch_must_be_small_p0_only",
    "heavy_models_deferred_to_p1_p2",
    "admission_order_is_p0_then_p1_then_p2",
    "no_live_camera_live_sensor_gps_map_api_ros",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DEFINED_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelDownloadLicenseLocalAvailabilityPlanningProfile",
    "RecognitionModelDownloadCandidatePlan",
    "RecognitionModelLicenseEvaluation",
    "RecognitionModelLocalAvailabilityEvaluation",
    "RecognitionModelDownloadAdmissionResult",
    "RecognitionModelDownloadBatchPlan",
    "RecognitionModelDownloadPlanningCaseResult",
    "RecognitionModelDownloadPlanningDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_GO"
FINAL_DECISION_BLOCKED = (
    "RECOGNITION_MODEL_DOWNLOAD_LICENSE_AND_LOCAL_AVAILABILITY_PLANNING_BLOCKED"
)

ALLOWED_FLAGS: Dict[str, bool] = {
    "model_download_planning_allowed": True,
    "license_evaluation_allowed": True,
    "local_availability_evaluation_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_model_download_executed": False,
    "real_model_install_executed": False,
    "model_repo_clone_executed": False,
    "real_inference_allowed": False,
    "real_image_recognition_allowed": False,
    "model_build_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "dataset_download_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelDownloadLicenseLocalAvailabilityPlanningProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    invocation_feasibility_dryrun_ref: str
    system_admission_planning_ref: str
    target_chain_ref: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    model_role_ids: Tuple[str, ...]
    admission_tier_order: Tuple[str, ...]
    required_plan_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    reject_if_false_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    planning_decision_dimensions: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelDownloadAdmissionResult:
    model_id: str
    model_role: str
    tier: str
    accepted: bool
    reject_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelDownloadBatchPlan:
    tier: str
    model_ids: Tuple[str, ...]
    model_count: int


@dataclass
class RecognitionModelDownloadPlanningCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    model_id: str = ""
    model_role: str = ""
    tier: str = ""
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelDownloadPlanningDecision:
    decision_ref: str
    planning_profile_count: int
    model_plan_count: int
    p0_model_count: int
    p1_model_count: int
    p2_model_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    blocker_count: int
    final_decision: str


def planning_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
