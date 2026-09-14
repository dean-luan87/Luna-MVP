# -*- coding: utf-8 -*-
"""Midplatform Model Control DryRun — types v1.

Based on the already-GO Midplatform Model Data Handling DryRun, this phase executes
a midplatform model-control dry-run. It does not validate model outputs; it validates
the Luna midplatform's governance ability over model families: enable / disable /
fallback / degraded mode / license boundary control / priority routing / output
blocking / availability state control / reserved-only execution block / candidate
output gate, plus abnormal-state governance.

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

PHASE_ID = "Phase-Midplatform-Model-Control-DryRun-v1-001"
SCOPE = "midplatform_model_control_dryrun"
SOURCE_CHAIN = "midplatform_model_control_dryrun_v1"

DRYRUN_PRINCIPLE_ZH = (
    "基于已 GO 的 Midplatform Model Data Handling DryRun，执行中台模型控制 dry-run。该阶段验证 Luna 中台是否"
    "能够对多模型族进行启用、禁用、降级、fallback、license 边界控制、输出阻断、优先级调度、reserved-only 执行"
    "阻断、candidate output gate 与异常状态治理。不下载模型，不执行 inference，不跑新图片，不做单模型调试，"
    "不做模型调优，不使用数据集，不训练，不接 live camera/sensor，不触发 navigation/action/speech/fact_write。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "midplatform_model_control_serves_governance_not_action_no_vla_action_chain_in_scope"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "midplatform_model_control_dryrun_only"
MODEL_DATA_HANDLING_DRYRUN_REF = "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001"
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

NEXT_PHASE_REF = "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"

# --------------------------------------------------------------------------- #
# Model-control policies (11)
# --------------------------------------------------------------------------- #
MODEL_CONTROL_POLICY_IDS: Tuple[str, ...] = (
    "model_enable",
    "model_disable",
    "model_fallback",
    "model_degraded_mode",
    "model_license_boundary",
    "model_priority_routing",
    "model_output_blocking",
    "model_availability_state_control",
    "reserved_family_execution_block",
    "candidate_output_gate",
    "full_model_control_bundle",
)

POLICY_TO_OBJECTS: Dict[str, Tuple[str, ...]] = {
    "model_enable": (
        "model_enable_record",
        "model_control_state_candidate",
    ),
    "model_disable": (
        "model_disable_record",
        "blocked_model_output_record",
    ),
    "model_fallback": (
        "model_fallback_record",
        "fallback_candidate_route",
        "model_unavailable_context_candidate",
    ),
    "model_degraded_mode": (
        "degraded_model_state_record",
        "degraded_capability_state_candidate",
        "degraded_output_policy_candidate",
    ),
    "model_license_boundary": (
        "license_boundary_record",
        "commercial_runtime_block_record",
        "test_only_model_state_record",
    ),
    "model_priority_routing": (
        "model_priority_routing_record",
        "model_route_candidate",
        "routing_explanation_candidate",
    ),
    "model_output_blocking": (
        "blocked_model_output_record",
        "model_output_gate_rejection_record",
        "governance_block_reason_candidate",
    ),
    "model_availability_state_control": (
        "model_availability_control_record",
        "availability_state_route_candidate",
    ),
    "reserved_family_execution_block": (
        "reserved_family_execution_block_record",
        "reserved_family_state_record",
    ),
    "candidate_output_gate": (
        "candidate_output_gate_record",
        "candidate_gate_pass_record",
        "candidate_gate_reject_record",
    ),
    "full_model_control_bundle": (
        "midplatform_model_control_bundle",
        "model_control_audit_trace",
        "model_control_whitebox_candidate",
    ),
}

POLICY_BOUNDARY: Dict[str, str] = {
    "model_enable": "enabled_is_not_runtime_activation_enabled_does_not_trigger_inference",
    "model_disable": "disabled_model_output_must_not_enter_field_task_guidance",
    "model_fallback": "fallback_route_is_candidate_only_fallback_does_not_trigger_real_inference",
    "model_degraded_mode": "degraded_state_does_not_trigger_action_speech_navigation",
    "model_license_boundary": "commercial_runtime_approved_remains_false_unless_governance_approved",
    "model_priority_routing": "priority_routing_does_not_bypass_candidate_gate_routing_does_not_call_model",
    "model_output_blocking": "blocked_output_cannot_enter_field_task_guidance",
    "model_availability_state_control": (
        "download_planning_required_no_download_reserved_only_no_execution_unavailable_declared_not_blocker"
    ),
    "reserved_family_execution_block": "reserved_only_no_execution_no_psych_fact_write_no_behavior_manipulation",
    "candidate_output_gate": "gate_pass_is_candidate_pass_not_fact_admission",
    "full_model_control_bundle": "candidate_only_no_model_execution_no_runtime_trigger",
}

POLICY_OK_GO_KEYS: Dict[str, str] = {
    "model_enable": "model_enable_policy_control_ok",
    "model_disable": "model_disable_policy_control_ok",
    "model_fallback": "model_fallback_policy_control_ok",
    "model_degraded_mode": "model_degraded_mode_policy_control_ok",
    "model_license_boundary": "model_license_boundary_control_ok",
    "model_priority_routing": "model_priority_routing_policy_control_ok",
    "model_output_blocking": "model_output_blocking_policy_control_ok",
    "model_availability_state_control": "model_availability_state_control_ok",
    "reserved_family_execution_block": "reserved_family_execution_block_control_ok",
    "candidate_output_gate": "candidate_output_gate_control_ok",
    "full_model_control_bundle": "full_midplatform_model_control_bundle_ok",
}

# Positive case ids (11).
POSITIVE_CASE_IDS: Tuple[str, ...] = (
    "model_enable_policy_control",
    "model_disable_policy_control",
    "model_fallback_policy_control",
    "model_degraded_mode_policy_control",
    "model_license_boundary_control",
    "model_priority_routing_policy_control",
    "model_output_blocking_policy_control",
    "model_availability_state_control",
    "reserved_family_execution_block_control",
    "candidate_output_gate_control",
    "full_midplatform_model_control_bundle",
)

# All 28 distinct produced object types.
ALL_PRODUCED_OBJECTS: Tuple[str, ...] = (
    "model_enable_record",
    "model_control_state_candidate",
    "model_disable_record",
    "blocked_model_output_record",
    "model_fallback_record",
    "fallback_candidate_route",
    "model_unavailable_context_candidate",
    "degraded_model_state_record",
    "degraded_capability_state_candidate",
    "degraded_output_policy_candidate",
    "license_boundary_record",
    "commercial_runtime_block_record",
    "test_only_model_state_record",
    "model_priority_routing_record",
    "model_route_candidate",
    "routing_explanation_candidate",
    "model_output_gate_rejection_record",
    "governance_block_reason_candidate",
    "model_availability_control_record",
    "availability_state_route_candidate",
    "reserved_family_execution_block_record",
    "reserved_family_state_record",
    "candidate_output_gate_record",
    "candidate_gate_pass_record",
    "candidate_gate_reject_record",
    "midplatform_model_control_bundle",
    "model_control_audit_trace",
    "model_control_whitebox_candidate",
)

OBJECT_GENERATED_GO_KEYS: Tuple[str, ...] = tuple(
    f"{o}_generated" for o in ALL_PRODUCED_OBJECTS
)

RESERVED_FAMILIES: Tuple[str, ...] = (
    "audio_speech_family",
    "emotion_multimodal_bridge_family",
)

# --------------------------------------------------------------------------- #
# Control policy admission fields
# --------------------------------------------------------------------------- #
REQUIRED_BUNDLE_FIELDS: Tuple[str, ...] = (
    "control_id",
    "policy_id",
    "model_family",
    "license_ref",
    "allowed_use",
    "availability_state",
    "source_chain",
    "confidence_policy_ref",
    "fallback_plan",
)

REJECT_IF_MISSING_FIELDS: Tuple[str, ...] = (
    "policy_id",
    "model_family",
    "source_chain",
)

CONTRACT_FIELD_REQUIRED_FLAGS: Dict[str, str] = {
    "policy_id": "policy_id_required",
    "model_family": "model_family_required",
    "source_chain": "source_chain_required",
}

# --------------------------------------------------------------------------- #
# Prohibited flags (any True -> reject)
# --------------------------------------------------------------------------- #
PROHIBITED_REQUEST_FLAGS: Tuple[str, ...] = (
    "disabled_model_output_allowed",
    "unlicensed_model_enabled",
    "agpl_model_marked_commercial_runtime_ready",
    "commercial_runtime_ready_claimed",
    "unavailable_model_triggered_download",
    "download_requested",
    "forced_execution_requested",
    "reserved_family_executed",
    "degraded_model_triggers_action",
    "action_requested",
    "speech_requested",
    "navigation_requested",
    "blocked_output_enters_field_task_guidance",
    "direct_field_task_guidance_bypass",
    "priority_routing_bypasses_candidate_gate",
    "candidate_gate_bypass",
    "model_control_triggers_inference",
    "real_inference_requested",
    "vla_action_chain_requested",
    "model_tuning_requested",
    "dataset_usage_requested",
    "training_requested",
    "gate_pass_treated_as_fact_admission",
    "fact_admission_requested",
)

# --------------------------------------------------------------------------- #
# Cases
# --------------------------------------------------------------------------- #
NEGATIVE_CASE_IDS: Tuple[str, ...] = (
    "invalid_disabled_model_output_allowed",
    "invalid_unlicensed_model_enabled",
    "invalid_agpl_model_marked_commercial_runtime_ready",
    "invalid_unavailable_model_triggered_download",
    "invalid_reserved_family_executed",
    "invalid_degraded_model_triggers_action",
    "invalid_blocked_output_enters_field_task_guidance",
    "invalid_priority_routing_bypasses_candidate_gate",
    "invalid_model_control_triggers_inference",
    "invalid_vla_action_chain_injected",
    "invalid_model_tuning_dataset_usage",
    "invalid_gate_pass_treated_as_fact_admission",
)

# --------------------------------------------------------------------------- #
# Governance rules (26)
# --------------------------------------------------------------------------- #
DRYRUN_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_midplatform_model_control_dryrun_only",
    "no_model_execution_is_allowed",
    "no_inference_is_allowed",
    "no_model_download_is_allowed",
    "no_single_model_debugging_is_allowed",
    "no_model_tuning_is_allowed",
    "no_dataset_usage_is_allowed",
    "enabled_does_not_mean_runtime_activation",
    "disabled_model_output_must_be_blocked",
    "fallback_does_not_trigger_download_or_inference",
    "degraded_state_does_not_trigger_action_speech_navigation",
    "license_boundary_must_control_commercial_runtime_claims",
    "test_only_model_remains_test_only",
    "priority_routing_does_not_bypass_candidate_gate",
    "output_blocking_must_prevent_field_task_guidance_bypass",
    "availability_state_controls_route_but_does_not_execute_model",
    "reserved_only_family_must_not_execute",
    "candidate_output_gate_is_not_fact_admission",
    "gate_pass_remains_candidate_only",
    "conflict_uncertainty_remains_candidate_only",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded_from_current_scope",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "controlled_trial_governance_lifecycle_template_must_be_referenced",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "MidplatformModelControlDryRunProfile",
    "MidplatformModelControlPolicyBundle",
    "MidplatformModelEnableResult",
    "MidplatformModelDisableResult",
    "MidplatformModelFallbackResult",
    "MidplatformModelDegradedModeResult",
    "MidplatformModelLicenseBoundaryResult",
    "MidplatformModelPriorityRoutingResult",
    "MidplatformModelOutputBlockingResult",
    "MidplatformModelAvailabilityStateControlResult",
    "MidplatformReservedFamilyExecutionBlockResult",
    "MidplatformCandidateOutputGateResult",
    "MidplatformModelControlBoundaryResult",
    "MidplatformModelControlDryRunDecision",
)

FINAL_DECISION_GO = "MIDPLATFORM_MODEL_CONTROL_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "MIDPLATFORM_MODEL_CONTROL_DRYRUN_BLOCKED"

ALLOWED_FLAGS: Dict[str, bool] = {
    "midplatform_model_control_dryrun_allowed": True,
    "model_enable_policy_allowed": True,
    "model_disable_policy_allowed": True,
    "model_fallback_policy_allowed": True,
    "model_degraded_mode_policy_allowed": True,
    "model_license_boundary_control_allowed": True,
    "model_priority_routing_policy_allowed": True,
    "model_output_blocking_policy_allowed": True,
    "model_availability_state_control_allowed": True,
    "reserved_family_execution_block_allowed": True,
    "candidate_output_gate_allowed": True,
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
class MidplatformModelControlDryRunProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    model_data_handling_dryrun_ref: str
    multi_model_interaction_dryrun_ref: str
    p1_output_adapter_dryrun_ref: str
    p0_baseline_ref: str
    target_chain_ref: str
    target_entrypoint: str
    interface_adapter_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    model_control_policy_ids: Tuple[str, ...]
    required_bundle_fields: Tuple[str, ...]
    reject_if_missing_fields: Tuple[str, ...]
    prohibited_request_flags: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelControlPolicyBundle:
    control_id: str
    policy_id: str
    model_family: str
    license_ref: str
    availability_state: str
    source_chain: str
    mock_file_based: bool


@dataclass(frozen=True)
class MidplatformModelEnableResult:
    policy_id: str
    enabled: bool
    runtime_activated: bool
    triggered_inference: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelDisableResult:
    policy_id: str
    disabled: bool
    output_enters_ftg: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelFallbackResult:
    policy_id: str
    fallback_selected: bool
    candidate_only: bool
    triggered_download_or_inference: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelDegradedModeResult:
    policy_id: str
    degraded: bool
    state_preserved: bool
    triggers_action_speech_navigation: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelLicenseBoundaryResult:
    policy_id: str
    boundary_enforced: bool
    commercial_runtime_blocked: bool
    test_only_preserved: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelPriorityRoutingResult:
    policy_id: str
    route_built: bool
    bypasses_candidate_gate: bool
    calls_model_directly: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelOutputBlockingResult:
    policy_id: str
    output_blocked: bool
    output_enters_ftg: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelAvailabilityStateControlResult:
    policy_id: str
    state_routed: bool
    download_triggered: bool
    reserved_executed: bool
    unavailable_treated_as_blocker: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformReservedFamilyExecutionBlockResult:
    policy_id: str
    interface_preserved: bool
    execution_blocked: bool
    psych_fact_written: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformCandidateOutputGateResult:
    policy_id: str
    gated: bool
    gate_pass_is_candidate_only: bool
    gate_pass_treated_as_fact: bool
    object_types: Tuple[str, ...]


@dataclass(frozen=True)
class MidplatformModelControlBoundaryResult:
    policy_id: str
    boundary: str
    no_model_execution: bool
    no_runtime_trigger: bool
    candidate_only: bool
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
class MidplatformModelControlDryRunDecision:
    decision_ref: str
    dryrun_profile_count: int
    upstream_stage_ref_count: int
    model_control_policy_count: int
    sample_file_count: int
    positive_case_count: int
    negative_case_count: int
    positive_pass_count: int
    invalid_expected_reject_count: int
    full_midplatform_model_control_bundle_ok: bool
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
