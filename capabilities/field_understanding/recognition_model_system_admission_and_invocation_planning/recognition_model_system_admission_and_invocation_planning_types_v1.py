# -*- coding: utf-8 -*-
"""Recognition Model System Admission and Invocation Planning — types v1.

Plans HOW real recognition models are admitted into the Luna system, on top of
the already-frozen Phase-One environment cognition evidence main chain. This
phase prioritizes "can the model be admitted / can it be invoked / does its
output meet Luna system requirements" — it does NOT tune models, does NOT use
data, does NOT train, does NOT connect real business data.

Core principle:
  - model admission first, model output validation later;
  - system wiring first, model tuning later;
  - wire model into the Luna evidence main chain first, content/data usage later.

Admission order (declared, not executed here):
  1. Model System Admission Planning            (this phase)
  2. Model Invocation Feasibility DryRun
  3. Model Output Adapter DryRun
  4. Evidence Main Chain Integration DryRun
  5. Model Tuning Planning
  6. Data Usage Planning
  7. Real Recognition DryRun

Planning + Matrix Review only. No model download / repo clone / build / real
inference / tuning / dataset usage / dataset download / training / runtime /
live camera/sensor, and no navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001"
SCOPE = "recognition_model_system_admission_and_invocation_planning"
SOURCE_CHAIN = "recognition_model_system_admission_and_invocation_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已冻结的 Phase One Environment Cognition Evidence Main Chain，规划真实识别模型如何接入 Luna "
    "体系。优先解决“模型能不能接入、能不能调用、输出是否符合 Luna 体系要求”，不做模型调优、不做数据"
    "使用、不做训练、不接真实业务数据。核心原则：先模型接入再模型输出验证；先体系打通再模型调优；先"
    "模型与 Luna evidence main chain 打通，再做内容数据使用。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_system_admission_and_invocation_planning_only"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
MAIN_CHAIN_CLOSURE_REF = TARGET_CHAIN_REF
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

NEXT_PHASE_REF = "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Model families
# --------------------------------------------------------------------------- #
MODEL_FAMILY_IDS: Tuple[str, ...] = (
    "ocr_model_family",
    "object_detection_model_family",
    "segmentation_model_family",
    "tracking_model_family",
    "depth_spatial_hint_model_family",
    "visual_symbol_model_family",
    "scene_relation_model_family",
)

MODEL_FAMILY_ADMISSION_PLANNED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{m}_admission_planned" for m in MODEL_FAMILY_IDS
)

# --------------------------------------------------------------------------- #
# Invocation feasibility check items
# --------------------------------------------------------------------------- #
INVOCATION_FEASIBILITY_CHECK_ITEMS: Tuple[str, ...] = (
    "callable_interface_defined",
    "input_format_defined",
    "output_schema_defined",
    "local_or_target_runtime_requirement_declared",
    "license_ref_required",
    "model_origin_required",
    "dependency_boundary_declared",
    "resource_requirement_declared",
    "offline_or_online_mode_declared",
    "adapter_mapping_target_declared",
)

# --------------------------------------------------------------------------- #
# Model output requirement fields
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
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "license_ref",
    "model_origin",
    "confidence",
    "adapter_mapping_ref",
)

# --------------------------------------------------------------------------- #
# Admission order
# --------------------------------------------------------------------------- #
ADMISSION_ORDER: Tuple[str, ...] = (
    "model_system_admission_planning",
    "model_invocation_feasibility_dryrun",
    "model_output_adapter_dryrun",
    "evidence_main_chain_integration_dryrun",
    "model_tuning_planning",
    "data_usage_planning",
    "real_recognition_dryrun",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_system_admission_and_invocation_planning_only",
    "model_must_be_admitted_into_luna_system_before_data_usage",
    "model_invocation_feasibility_must_be_checked_before_model_tuning",
    "model_output_schema_must_be_checked_before_adapter_dryrun",
    "model_output_adapter_must_be_verified_before_evidence_main_chain_integration_dryrun",
    "model_tuning_is_deferred",
    "dataset_usage_is_deferred",
    "real_recognition_dryrun_is_deferred",
    "model_output_must_pass_interface_adapter",
    "native_model_output_must_not_enter_field_task_guidance_directly",
    "all_model_outputs_become_evidence_candidate_first",
    "field_task_guidance_path_remains_candidate_only",
    "guidance_candidate_must_not_become_runtime_navigation",
    "speech_gate_candidate_must_not_become_tts",
    "action_safety_candidate_must_exist",
    "no_live_camera_live_sensor_gps_map_api_ros",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

PLANNING_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelSystemAdmissionPlanningProfile",
    "RecognitionModelFamilyAdmissionPolicy",
    "RecognitionModelInvocationFeasibilityPolicy",
    "RecognitionModelInputRequirementPolicy",
    "RecognitionModelOutputRequirementPolicy",
    "RecognitionModelRuntimeBoundaryPolicy",
    "RecognitionModelAdapterReadinessPolicy",
    "RecognitionModelTuningDeferralPolicy",
    "RecognitionModelDataUsageDeferralPolicy",
    "RecognitionModelSystemAdmissionPlanningDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_SYSTEM_ADMISSION_AND_INVOCATION_PLANNING_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_SYSTEM_ADMISSION_AND_INVOCATION_PLANNING_BLOCKED"

ORDER_ENFORCEMENT_FLAGS: Dict[str, bool] = {
    "model_before_data_usage_order_enforced": True,
    "invocation_before_tuning_order_enforced": True,
    "output_schema_before_adapter_dryrun_order_enforced": True,
    "adapter_before_evidence_integration_order_enforced": True,
    "real_recognition_dryrun_deferred": True,
    "model_tuning_deferred": True,
    "dataset_usage_deferred": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "model_system_admission_planning_only": True,
    "model_invocation_execution_allowed": False,
    "model_output_adapter_dryrun_allowed": False,
    "real_inference_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "dataset_download_allowed": False,
    "model_download_allowed": False,
    "model_repo_clone_allowed": False,
    "model_build_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class RecognitionModelSystemAdmissionPlanningProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    model_family_ids: Tuple[str, ...]
    invocation_feasibility_check_items: Tuple[str, ...]
    required_model_output_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    admission_order: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelFamilyAdmissionPolicy:
    model_family_id: str
    examples: Tuple[str, ...]
    target_candidate: Tuple[str, ...]
    invocation_check_required: bool
    output_check_required: Tuple[str, ...]
    admission_planned: bool


@dataclass(frozen=True)
class RecognitionModelInvocationFeasibilityPolicy:
    model_family_id: str
    callable_interface_defined: bool
    input_format_defined: bool
    output_schema_defined: bool
    local_or_target_runtime_requirement_declared: bool
    license_ref_required: bool
    model_origin_required: bool
    dependency_boundary_declared: bool
    resource_requirement_declared: bool
    offline_or_online_mode_declared: bool
    adapter_mapping_target_declared: bool


@dataclass(frozen=True)
class RecognitionModelInputRequirementPolicy:
    model_family_id: str
    input_format_required: bool
    input_ref_required: bool


@dataclass(frozen=True)
class RecognitionModelOutputRequirementPolicy:
    model_family_id: str
    required_output_fields: Tuple[str, ...]
    source_chain_required: bool
    confidence_required: bool
    adapter_mapping_ref_required: bool
    allowed_use_required: bool
    commercial_use_status_required: bool


@dataclass(frozen=True)
class RecognitionModelRuntimeBoundaryPolicy:
    policy_ref: str
    model_invocation_execution_allowed: bool
    model_download_allowed: bool
    model_repo_clone_allowed: bool
    model_build_allowed: bool
    real_inference_allowed: bool


@dataclass(frozen=True)
class RecognitionModelAdapterReadinessPolicy:
    model_family_id: str
    adapter_mapping_target_declared: bool
    model_output_adapter_required: bool
    native_model_output_direct_to_field_blocked: bool
    all_model_outputs_become_evidence_candidate_first: bool


@dataclass(frozen=True)
class RecognitionModelTuningDeferralPolicy:
    policy_ref: str
    model_tuning_deferred: bool
    invocation_before_tuning_order_enforced: bool


@dataclass(frozen=True)
class RecognitionModelDataUsageDeferralPolicy:
    policy_ref: str
    dataset_usage_deferred: bool
    model_before_data_usage_order_enforced: bool
    real_recognition_dryrun_deferred: bool


@dataclass(frozen=True)
class RecognitionModelSystemAdmissionPlanningDecision:
    decision_ref: str
    planning_profile_count: int
    model_family_policy_count: int
    invocation_feasibility_policy_count: int
    output_requirement_policy_count: int
    adapter_readiness_policy_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
