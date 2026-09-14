# -*- coding: utf-8 -*-
"""Recognition Model P1 Invocation And Local Availability DryRun — types v1.

Based on the already-GO Recognition Model P1 Family Expansion Planning, this phase
performs an invocation-entry / local-availability dry-run for the P1/P2 expansion
model families. It does NOT debug a single model, NOT download new models, NOT run
real inference, NOT use datasets, NOT tune models. It only inventories — for each of
the 7 expansion/reserved families — local visibility, callable contract, dependency
state, license boundary, fallback plan and unavailable-record policy, and produces a
P1/P2 family availability-status matrix.

Allowed here (non-invasive only): import-visibility check / package-visibility check /
command-visibility check / contract-level callable check / local-resource-visibility
check / availability-matrix generation.

Forbidden here: new model download / real inference / new image-video recognition /
single-model debugging / model tuning / dataset usage / training / live camera-sensor /
navigation-action-speech-fact_write / VLA action chain.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Recognition-Model-P1-Invocation-And-Local-Availability-DryRun-v1-001"
SCOPE = "recognition_model_p1_invocation_and_local_availability_dryrun"
SOURCE_CHAIN = "recognition_model_p1_invocation_and_local_availability_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Model P1 Family Expansion Planning，对 P1/P2 扩张模型族执行调用入口与本地"
    "可用性 dry-run。本阶段不直接调试单一模型、不下载新模型、不执行真实 inference、不使用数据集、不做模型"
    "调优，而是盘点 P1/P2 模型族在当前本地环境中的可见性、调用合约、依赖状态、license 边界、fallback 策略"
    "与 unavailable record 策略。允许 import/package/command 可见性检查、contract-level 可调用性检查、"
    "local resource 可见性检查、availability matrix 生成；只允许非侵入式探测。禁止下载新模型、真实 inference、"
    "新图像/视频识别、单模型调试、模型调优、数据集使用、训练、接 live camera/sensor、触发 "
    "navigation/action/speech/fact_write、以及 VLA 行动链。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_p2_recognition_family_availability_serves_cognition_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "recognition_model_p1_invocation_and_local_availability_dryrun_only"
P1_FAMILY_EXPANSION_PLANNING_REF = (
    "Phase-Recognition-Model-P1-Family-Expansion-Planning-v1-001"
)
P0_BASELINE_REF = "Phase-Recognition-Model-P0-Integration-Closure-v1-001"
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
TARGET_ENTRYPOINT = "field_synthesis_v1"
INTERFACE_ADAPTER_REF = "recognition_model_output_adapter"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_PHASE_REF = "Phase-Recognition-Model-P1-Output-Adapter-DryRun-v1-001"

# --------------------------------------------------------------------------- #
# Model families (7): 5 planned/expansion + 2 reserved.
# --------------------------------------------------------------------------- #
MODEL_FAMILY_IDS: Tuple[str, ...] = (
    "segmentation_family",
    "tracking_family",
    "depth_spatial_hint_family",
    "object_detection_completion_family",
    "scene_relation_vlm_family",
    "audio_speech_family",
    "emotion_multimodal_bridge_family",
)

FAMILY_AVAILABILITY_CHECKED_GO_KEYS: Dict[str, str] = {
    "segmentation_family": "segmentation_family_availability_checked",
    "tracking_family": "tracking_family_availability_checked",
    "depth_spatial_hint_family": "depth_spatial_hint_family_availability_checked",
    "object_detection_completion_family": "object_detection_completion_family_availability_checked",
    "scene_relation_vlm_family": "scene_relation_vlm_family_availability_checked",
    "audio_speech_family": "audio_speech_reserved_family_checked",
    "emotion_multimodal_bridge_family": "emotion_multimodal_bridge_reserved_checked",
}

# --------------------------------------------------------------------------- #
# Availability contract required fields
# --------------------------------------------------------------------------- #
REQUIRED_CONTRACT_FIELDS: Tuple[str, ...] = (
    "model_family",
    "candidate_models",
    "planned_target_candidates",
    "package_or_module_refs",
    "command_refs",
    "local_resource_refs",
    "license_ref",
    "model_origin",
    "source_chain",
    "callable_contract_ref",
    "output_schema_ref",
    "adapter_mapping_ref",
    "fallback_plan",
    "unavailable_record_policy",
    "allowed_use",
    "commercial_use_status",
    "availability_probe_mode",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "license_ref",
    "model_origin",
    "source_chain",
    "adapter_mapping_ref",
    "fallback_plan",
    "unavailable_record_policy",
    "allowed_use",
)

# Field -> GO required-flag key.
CONTRACT_FIELD_REQUIRED_FLAGS: Dict[str, str] = {
    "license_ref": "license_ref_required",
    "model_origin": "model_origin_required",
    "source_chain": "source_chain_required",
    "adapter_mapping_ref": "adapter_mapping_ref_required",
    "fallback_plan": "fallback_plan_required",
    "unavailable_record_policy": "unavailable_record_policy_required",
    "allowed_use": "allowed_use_required",
}

# --------------------------------------------------------------------------- #
# Availability statuses + probe modes
# --------------------------------------------------------------------------- #
ALLOWED_AVAILABILITY_STATUSES: Tuple[str, ...] = (
    "available",
    "contract_only",
    "unavailable_declared",
    "download_planning_required",
    "deferred_due_to_license_or_resource",
    "deferred_due_to_license",
    "deferred_due_to_resource",
    "deferred_due_to_output_instability",
    "test_only",
    "reserved_only",
)

ALLOWED_PROBE_MODES: Tuple[str, ...] = (
    "import_visibility",
    "package_visibility",
    "command_visibility",
    "local_resource_visibility",
    "contract_level_callable_check",
    "reserved_only_contract",
)

# --------------------------------------------------------------------------- #
# Prohibited request flags inside a contract (must trigger rejection)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "real_inference_requested",
    "new_image_recognition_requested",
    "new_model_download_requested",
    "model_repo_clone_requested",
    "single_model_debugging_requested",
    "model_tuning_requested",
    "dataset_usage_requested",
    "training_requested",
    "dataset_download_requested",
    "runtime_activation_requested",
    "live_camera_requested",
    "live_sensor_requested",
    "direct_action_requested",
    "direct_speech_requested",
    "direct_fact_write_requested",
    "vla_action_chain_requested",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "segmentation_family_local_availability_check",
    "tracking_family_local_availability_check",
    "depth_spatial_hint_family_local_availability_check",
    "object_detection_completion_family_local_availability_check",
    "scene_relation_vlm_family_local_availability_check",
    "audio_speech_reserved_family_check",
    "emotion_multimodal_bridge_reserved_check",
    "p1_p2_family_availability_matrix_generation",
)

NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_missing_license_ref",
    "invalid_missing_fallback_plan",
    "invalid_missing_unavailable_record_policy",
    "invalid_real_inference_requested",
    "invalid_new_model_download_requested",
    "invalid_single_model_debugging_requested",
    "invalid_dataset_training_requested",
    "invalid_live_camera_sensor_requested",
    "invalid_direct_action_speech_fact_write_requested",
    "invalid_vla_action_chain_requested",
)

# --------------------------------------------------------------------------- #
# Governance rules
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_p1_p2_invocation_and_local_availability_dryrun_only",
    "p0_baseline_remains_frozen",
    "no_new_model_download_is_allowed",
    "no_real_inference_is_allowed",
    "no_new_image_video_recognition_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "no_training_is_allowed",
    "local_availability_may_be_checked_by_non_invasive_probes_only",
    "unavailable_record_is_valid_if_declared",
    "download_planning_required_is_not_blocker",
    "reserved_only_family_is_not_blocker",
    "segmentation_mask_is_not_fact",
    "tracking_is_not_action_trigger",
    "depth_is_auxiliary_and_not_navigation",
    "object_identity_is_not_fact",
    "scene_relation_vlm_has_no_reasoning_authority",
    "audio_identity_requires_consent_and_confirmation",
    "emotion_multimodal_bridge_does_not_write_psychological_fact",
    "field_task_guidance_remain_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "RecognitionModelP1InvocationLocalAvailabilityDryRunProfile",
    "RecognitionModelP1FamilyAvailabilityContract",
    "RecognitionModelP1LocalVisibilityProbe",
    "RecognitionModelP1CallableContractResult",
    "RecognitionModelP1UnavailableRecord",
    "RecognitionModelP1DownloadNeedRecord",
    "RecognitionModelP1AvailabilityMatrix",
    "RecognitionModelP1InvocationLocalAvailabilityBoundaryResult",
    "RecognitionModelP1InvocationLocalAvailabilityDryRunDecision",
)

FINAL_DECISION_GO = "RECOGNITION_MODEL_P1_INVOCATION_AND_LOCAL_AVAILABILITY_DRYRUN_GO"
FINAL_DECISION_BLOCKED = (
    "RECOGNITION_MODEL_P1_INVOCATION_AND_LOCAL_AVAILABILITY_DRYRUN_BLOCKED"
)

ALLOWED_AVAILABILITY_FLAGS: Dict[str, bool] = {
    "p1_invocation_local_availability_dryrun_allowed": True,
    "import_visibility_check_allowed": True,
    "package_visibility_check_allowed": True,
    "command_visibility_check_allowed": True,
    "contract_level_callable_check_allowed": True,
    "local_resource_visibility_check_allowed": True,
    "availability_matrix_generation_allowed": True,
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
class RecognitionModelP1InvocationLocalAvailabilityDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    p1_family_expansion_planning_ref: str
    p0_baseline_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    model_family_ids: Tuple[str, ...]
    required_contract_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    allowed_availability_statuses: Tuple[str, ...]
    allowed_probe_modes: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class RecognitionModelP1FamilyAvailabilityContract:
    model_family: str
    candidate_models: Tuple[str, ...]
    planned_target_candidates: Tuple[str, ...]
    package_or_module_refs: Tuple[str, ...]
    command_refs: Tuple[str, ...]
    local_resource_refs: Tuple[str, ...]
    license_ref: str
    model_origin: str
    source_chain: str
    callable_contract_ref: str
    output_schema_ref: str
    adapter_mapping_ref: str
    fallback_plan: str
    unavailable_record_policy: str
    allowed_use: str
    commercial_use_status: str
    availability_probe_mode: str
    availability_status: str


@dataclass(frozen=True)
class RecognitionModelP1LocalVisibilityProbe:
    model_family: str
    probe_mode: str
    non_invasive: bool
    package_visible: bool
    command_visible: bool
    local_resource_visible: bool
    note: str


@dataclass(frozen=True)
class RecognitionModelP1CallableContractResult:
    model_family: str
    contract_level_callable: bool
    real_inference_executed: bool
    output_schema_ref: str
    adapter_mapping_ref: str


@dataclass(frozen=True)
class RecognitionModelP1UnavailableRecord:
    model_family: str
    declared: bool
    reason: str
    unavailable_record_policy: str


@dataclass(frozen=True)
class RecognitionModelP1DownloadNeedRecord:
    model_family: str
    download_planning_required: bool
    license_ref: str
    note: str


@dataclass(frozen=True)
class RecognitionModelP1AvailabilityMatrix:
    family_count: int
    statuses_by_family: Dict[str, str]
    status_buckets: Dict[str, Tuple[str, ...]]
    matrix_generated: bool


@dataclass(frozen=True)
class RecognitionModelP1InvocationLocalAvailabilityBoundaryResult:
    model_family: str
    adapter_mapping_ref_declared: bool
    no_real_inference: bool
    no_new_model_download: bool
    non_invasive_probe_only: bool
    output_becomes_evidence_candidate_first: bool


@dataclass
class RecognitionModelCaseResult:
    case_id: str
    case_kind: str
    accepted: bool
    expected_result: str
    passed: bool
    model_family: str = ""
    availability_status: str = ""
    reject_reasons: Tuple[str, ...] = field(default_factory=tuple)
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class RecognitionModelP1InvocationLocalAvailabilityDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    upstream_stage_ref_count: int
    family_contract_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    p1_p2_family_availability_matrix_generated: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
