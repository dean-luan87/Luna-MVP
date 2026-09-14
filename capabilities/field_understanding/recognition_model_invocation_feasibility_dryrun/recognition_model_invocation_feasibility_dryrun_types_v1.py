# -*- coding: utf-8 -*-
"""Recognition Model Invocation Feasibility DryRun — types v1.

Validates whether recognition-model invocation ENTRY POINTS are usable, on top of
the already-GO Recognition Model System Admission and Invocation Planning. This
phase only checks model-family invocation entry points, dependency visibility,
command/package availability, stub invocation contracts, and placeholder I/O
schema. It does NOT run real recognition, NOT real images, NOT model tuning,
NOT data usage.

Allowed here: import availability check / command availability check / lightweight
stub invocation / mock callable contract check / local placeholder output schema
check / package-module presence check.

Forbidden here: model weight download / repo clone / model runtime build / real
inference / real image-video recognition / model tuning / dataset download /
training data usage / live camera-sensor / navigation/action/speech/fact_write.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"
SCOPE = "recognition_model_invocation_feasibility_dryrun"
SOURCE_CHAIN = "recognition_model_invocation_feasibility_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model System Admission and Invocation Planning，执行模型调用可行性 dry-run。"
    "只检查模型族的调用入口、依赖可见性、命令/包可用性、stub invocation contract、输入输出 schema "
    "placeholder 是否满足 Luna 接入要求。允许 import/command/stub/contract/placeholder 检查；禁止下载模型"
    "权重、clone repo、build runtime、真实 inference、真实图片识别、模型调优、数据集下载、训练数据使用、"
    "接 live camera/sensor、触发 navigation/action/speech/fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_invocation_feasibility_dryrun_only"
PLANNING_REF = "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

# --------------------------------------------------------------------------- #
# Upstream references
# --------------------------------------------------------------------------- #
SYSTEM_ADMISSION_PLANNING_REF = PLANNING_REF
MAIN_CHAIN_CLOSURE_REF = TARGET_CHAIN_REF
RGB_VISION_EVIDENCE_CHAIN_CLOSURE_REF = (
    "Phase-RGB-Vision-Evidence-Chain-Integrated-Closure-v1-001"
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

NEXT_PHASE_REF = "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001"

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

FAMILY_FEASIBILITY_CHECKED_GO_KEYS: Dict[str, str] = {
    "ocr_model_family": "ocr_invocation_feasibility_checked",
    "object_detection_model_family": "object_detection_invocation_feasibility_checked",
    "segmentation_model_family": "segmentation_invocation_feasibility_checked",
    "tracking_model_family": "tracking_invocation_feasibility_checked",
    "depth_spatial_hint_model_family": "depth_spatial_hint_invocation_feasibility_checked",
    "visual_symbol_model_family": "visual_symbol_invocation_feasibility_checked",
    "scene_relation_model_family": "scene_relation_invocation_feasibility_checked",
}

# --------------------------------------------------------------------------- #
# Callable contract required fields
# --------------------------------------------------------------------------- #
REQUIRED_CONTRACT_FIELDS: Tuple[str, ...] = (
    "model_family",
    "callable_interface_ref",
    "input_format_ref",
    "output_schema_ref",
    "runtime_requirement_ref",
    "model_origin",
    "license_ref",
    "dependency_boundary_ref",
    "resource_requirement_ref",
    "offline_or_online_mode",
    "adapter_mapping_target",
    "source_chain",
    "confidence_policy_ref",
    "invocation_mode",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "model_origin",
    "license_ref",
    "output_schema_ref",
    "source_chain",
    "adapter_mapping_target",
)

ALLOWED_INVOCATION_MODES: Tuple[str, ...] = (
    "stub_only",
    "import_check",
    "command_check",
    "contract_check",
)

# --------------------------------------------------------------------------- #
# Prohibited request flags inside a contract (must trigger rejection)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "real_inference_requested",
    "real_image_recognition_requested",
    "model_download_requested",
    "model_repo_clone_requested",
    "model_build_requested",
    "native_output_direct_to_field",
    "dataset_usage_requested",
    "training_requested",
    "runtime_activation_requested",
    "live_camera_requested",
    "live_sensor_requested",
    "direct_action_requested",
    "direct_speech_requested",
    "direct_fact_write_requested",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "ocr_invocation_feasibility_contract_check",
    "object_detection_invocation_feasibility_contract_check",
    "segmentation_invocation_feasibility_contract_check",
    "tracking_invocation_feasibility_contract_check",
    "depth_spatial_hint_invocation_feasibility_contract_check",
    "visual_symbol_invocation_feasibility_contract_check",
    "scene_relation_invocation_feasibility_contract_check",
    "multi_family_invocation_feasibility_matrix",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_model_origin",
    "invalid_missing_license_ref",
    "invalid_missing_output_schema_ref",
    "invalid_real_inference_requested",
    "invalid_model_download_requested",
    "invalid_native_output_direct_to_field",
    "invalid_dataset_usage_or_training_requested",
    "invalid_runtime_activation_or_live_sensor_requested",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_invocation_feasibility_dryrun_only",
    "stub_invocation_is_allowed",
    "import_availability_check_is_allowed",
    "command_availability_check_is_allowed",
    "placeholder_output_schema_check_is_allowed",
    "real_inference_is_not_allowed",
    "real_image_video_recognition_is_not_allowed",
    "model_download_is_not_allowed",
    "repo_clone_is_not_allowed",
    "model_build_is_not_allowed",
    "model_tuning_is_deferred",
    "dataset_usage_is_deferred",
    "training_is_not_allowed",
    "model_output_adapter_dryrun_is_not_executed_in_this_phase",
    "native_model_output_must_not_enter_field_task_guidance_directly",
    "adapter_mapping_target_must_be_declared",
    "all_future_model_output_must_become_evidence_candidate_first",
    "field_task_guidance_path_remains_candidate_only",
    "no_live_camera_live_sensor_gps_map_api_ros",
    "no_navigation_action_speech_fact_write",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelInvocationFeasibilityDryRunProfile",
    "RecognitionModelCallableContract",
    "RecognitionModelImportAvailabilityResult",
    "RecognitionModelCommandAvailabilityResult",
    "RecognitionModelStubInvocationResult",
    "RecognitionModelPlaceholderOutputSchemaResult",
    "RecognitionModelInvocationBoundaryResult",
    "RecognitionModelInvocationFeasibilityDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_INVOCATION_FEASIBILITY_DRYRUN_BLOCKED"

ALLOWED_FEASIBILITY_FLAGS: Dict[str, bool] = {
    "model_invocation_feasibility_dryrun_allowed": True,
    "stub_invocation_allowed": True,
    "import_availability_check_allowed": True,
    "command_availability_check_allowed": True,
    "placeholder_output_schema_check_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "model_output_adapter_dryrun_allowed": False,
    "real_inference_allowed": False,
    "real_image_recognition_allowed": False,
    "model_download_allowed": False,
    "model_repo_clone_allowed": False,
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
class RecognitionModelInvocationFeasibilityDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    planning_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    model_family_ids: Tuple[str, ...]
    required_contract_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    allowed_invocation_modes: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelCallableContract:
    model_family: str
    callable_interface_ref: str
    input_format_ref: str
    output_schema_ref: str
    runtime_requirement_ref: str
    model_origin: str
    license_ref: str
    dependency_boundary_ref: str
    resource_requirement_ref: str
    offline_or_online_mode: str
    adapter_mapping_target: str
    source_chain: str
    confidence_policy_ref: str
    invocation_mode: str


@dataclass(frozen=True)
class RecognitionModelImportAvailabilityResult:
    model_family: str
    import_check_allowed: bool
    import_check_mode: str
    note: str


@dataclass(frozen=True)
class RecognitionModelCommandAvailabilityResult:
    model_family: str
    command_check_allowed: bool
    command_check_mode: str
    note: str


@dataclass(frozen=True)
class RecognitionModelStubInvocationResult:
    model_family: str
    stub_invocation_allowed: bool
    real_inference_executed: bool
    placeholder_output_schema_ref: str


@dataclass(frozen=True)
class RecognitionModelPlaceholderOutputSchemaResult:
    model_family: str
    expected_output_fields: Tuple[str, ...]
    placeholder_schema_ok: bool


@dataclass(frozen=True)
class RecognitionModelInvocationBoundaryResult:
    model_family: str
    adapter_mapping_target_declared: bool
    native_output_direct_to_field_blocked: bool
    all_model_outputs_become_evidence_candidate_first: bool
    no_real_inference: bool


@dataclass
class RecognitionModelCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    model_family: str = ""
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelInvocationFeasibilityDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    model_family_contract_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
