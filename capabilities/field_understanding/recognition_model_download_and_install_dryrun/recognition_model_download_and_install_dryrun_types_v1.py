# -*- coding: utf-8 -*-
"""Recognition Model Download And Install DryRun — types v1.

First phase that actually lands the P0 recognition models locally, but with a
tightly controlled scope: download / install / minimal import / version /
local-resource checks only. No real inference, no real image/video recognition,
no RecognitionModelOutputAdapter dry-run, no evidence-main-chain integration, no
tuning, no dataset usage / download, no training, no live camera/sensor, and no
navigation/action/speech/fact_write.

P0 install targets:
  1. RapidOCR                       -> text_evidence_candidate provider
  2. YOLO lightweight / nano        -> object_evidence_candidate provider (test-only)
  3. OpenCV rule-based visual symbol-> color/shape/visual_symbol candidate provider (no weights)
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-Download-And-Install-DryRun-v1-001"
SCOPE = "recognition_model_download_and_install_dryrun"
SOURCE_CHAIN = "recognition_model_download_and_install_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Download/License/Local-Availability Planning,执行 P0 模型下载与本地安装 dry-run。"
    "仅验证模型/依赖能否下载、安装、导入、查询版本、定位本地资源,不跑真实图片/视频识别,不产生真实"
    "模型输出,不进入 RecognitionModelOutputAdapter,不做 Evidence Main Chain 集成,不调优,不用数据集。"
    "P0 范围:RapidOCR / YOLO lightweight-nano / OpenCV rule-based visual symbol。OpenCV 不需模型权重,"
    "YOLO 维持 test-only 不默认 commercial runtime。不接 live camera/sensor,不触发 "
    "navigation/action/speech/fact_write。"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_download_and_install_dryrun_only"
DOWNLOAD_LICENSE_PLANNING_REF = (
    "Phase-Recognition-Model-Download-License-And-Local-Availability-Planning-v1-001"
)
SYSTEM_ADMISSION_PLANNING_REF = (
    "Phase-Recognition-Model-System-Admission-and-Invocation-Planning-v1-001"
)
INVOCATION_FEASIBILITY_DRYRUN_REF = (
    "Phase-Recognition-Model-Invocation-Feasibility-DryRun-v1-001"
)
OUTPUT_ADAPTER_DRYRUN_REF = "Phase-Recognition-Model-Output-Adapter-DryRun-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

INTERFACE_LAYER_GOVERNANCE_REF = "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001"
MODEL_ADMISSION_GOVERNANCE_REF = "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001"

NEXT_PHASE_REF = "Phase-Recognition-Model-Real-Output-Adapter-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# P0 install targets
# --------------------------------------------------------------------------- #
P0_INSTALL_TARGET_IDS: Tuple[str, ...] = (
    "rapidocr_p0",
    "yolo_lightweight_p0",
    "opencv_visual_symbol_p0",
)

INSTALL_TARGET_GO_KEYS: Dict[str, str] = {
    "rapidocr_p0": "rapidocr_install_target_covered",
    "yolo_lightweight_p0": "yolo_lightweight_install_target_covered",
    "opencv_visual_symbol_p0": "opencv_visual_symbol_install_target_covered",
}

INSTALL_CHECK_GO_KEYS: Dict[str, str] = {
    "rapidocr_p0": "rapidocr_install_check_ok",
    "yolo_lightweight_p0": "yolo_lightweight_install_check_ok",
    "opencv_visual_symbol_p0": "opencv_visual_symbol_install_check_ok",
}

# --------------------------------------------------------------------------- #
# Install plan fields
# --------------------------------------------------------------------------- #
REQUIRED_INSTALL_PLAN_FIELDS: Tuple[str, ...] = (
    "model_id",
    "model_family",
    "install_target",
    "download_source",
    "package_name",
    "model_resource_ref",
    "license_ref",
    "allowed_use",
    "commercial_use_status",
    "dependency_list",
    "local_runtime_requirement",
    "gpu_required",
    "offline_supported",
    "expected_import_module",
    "expected_version_check",
    "local_resource_check",
    "fallback_plan",
    "source_chain",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "download_source",
    "license_ref",
    "package_name",
    "allowed_use",
    "commercial_use_status",
    "source_chain",
    "fallback_plan",
)

# Any of these flags True in a plan -> reject (this phase must not execute them).
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "real_inference_requested",
    "real_image_recognition_requested",
    "adapter_dryrun_requested",
    "evidence_main_chain_integration_requested",
    "model_tuning_requested",
    "dataset_download_requested",
    "dataset_usage_requested",
    "training_requested",
    "runtime_activation_requested",
    "live_camera_requested",
    "live_sensor_requested",
    "direct_action_requested",
    "direct_speech_requested",
    "fact_write_requested",
    "commercial_runtime_ready",
    "commercial_runtime_requested",
)

# Allowed (non-destructive) dry-run check kinds.
ALLOWED_CHECK_KINDS: Tuple[str, ...] = (
    "package_install_check",
    "model_download_check",
    "import_check",
    "version_check",
    "local_resource_check",
    "minimal_constructor_check",
    "cli_availability_check",
    "opencv_rule_runtime_check",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "rapidocr_download_install_check",
    "yolo_lightweight_download_install_check",
    "opencv_visual_symbol_install_check",
    "p0_install_matrix_check",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_license_ref",
    "invalid_missing_download_source",
    "invalid_commercial_runtime_for_agpl_yolo",
    "invalid_real_inference_requested",
    "invalid_dataset_download_requested",
    "invalid_adapter_dryrun_requested",
    "invalid_live_camera_sensor_requested",
    "invalid_direct_action_speech_fact_write",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_download_and_install_dryrun_only",
    "p0_scope_only",
    "rapidocr_install_target_allowed_if_license_and_source_verified",
    "yolo_lightweight_install_target_remains_test_only_unless_commercial_license_cleared",
    "opencv_visual_symbol_rule_path_does_not_require_model_weights",
    "package_install_import_version_local_resource_checks_are_allowed",
    "real_inference_is_not_allowed",
    "real_image_video_recognition_is_not_allowed",
    "recognition_model_output_adapter_dryrun_is_not_executed_in_this_phase",
    "evidence_main_chain_integration_dryrun_is_not_executed_in_this_phase",
    "model_tuning_is_deferred",
    "dataset_usage_is_deferred",
    "dataset_download_is_not_allowed",
    "training_is_not_allowed",
    "live_camera_live_sensor_are_not_allowed",
    "no_navigation_action_speech_fact_write",
    "model_output_must_later_pass_recognition_model_output_adapter",
    "native_model_output_must_not_enter_field_task_guidance_directly",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DEFINED_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelDownloadInstallDryRunProfile",
    "RecognitionModelInstallPlan",
    "RecognitionModelInstallAdmissionResult",
    "RecognitionModelPackageAvailabilityResult",
    "RecognitionModelDownloadResult",
    "RecognitionModelImportVersionResult",
    "RecognitionModelLocalResourceResult",
    "RecognitionModelInstallBoundaryResult",
    "RecognitionModelDownloadInstallDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_DOWNLOAD_AND_INSTALL_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "RECOGNITION_MODEL_DOWNLOAD_AND_INSTALL_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "model_download_install_dryrun_allowed": True,
    "package_install_check_allowed": True,
    "model_download_check_allowed": True,
    "import_check_allowed": True,
    "version_check_allowed": True,
    "local_resource_check_allowed": True,
    "minimal_constructor_check_allowed": True,
    "cli_availability_check_allowed": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "real_inference_allowed": False,
    "real_image_recognition_allowed": False,
    "model_output_adapter_dryrun_allowed": False,
    "evidence_main_chain_integration_dryrun_allowed": False,
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
class RecognitionModelDownloadInstallDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    download_license_planning_ref: str
    system_admission_planning_ref: str
    invocation_feasibility_dryrun_ref: str
    output_adapter_dryrun_ref: str
    target_chain_ref: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    p0_install_target_ids: Tuple[str, ...]
    required_install_plan_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    allowed_check_kinds: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelInstallAdmissionResult:
    model_id: str
    install_target: str
    accepted: bool
    reject_reasons: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelImportVersionResult:
    install_target: str
    expected_import_module: str
    import_probe_kind: str
    import_available: bool
    note: str


@dataclass
class RecognitionModelInstallCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    install_target: str = ""
    model_id: str = ""
    planned_checks: Tuple[str, ...] = field(default_factory=tuple)
    import_available: bool = False
    real_inference_executed: bool = False
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelDownloadInstallDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    p0_install_target_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    blocker_count: int
    final_decision: str


def install_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
