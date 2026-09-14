# -*- coding: utf-8 -*-
"""Model Governance Runtime Trial Planning — types v1.

Based on the already-GO Recognition Midplatform Model Governance Integrated Closure,
this phase plans the model-governance Runtime Trial: entry gate, execution boundary,
model scope, input/output boundary, fallback, blocker, exit and audit-record policy.
It MUST reuse existing governance protocols and admission chains; it does not create a
new admission system, does not redesign runtime governance, and runs no real runtime.

Core principles:
1. Runtime trial planning is governance reuse, not a new governance system.
2. Runtime trial planning is controlled-trial planning, not runtime execution.
3. This phase only defines trial entry / boundary / fallback / blocker / exit / audit.
4. All model outputs must still become an evidence candidate first.
5. The midplatform remains the control center for model invocation/output/state/
   degradation/blocking.
6. Luna remains emotion-multimodal brain / cognition first, with no VLA action chain.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)

PHASE_ID = "Phase-Model-Governance-Runtime-Trial-Planning-v1-001"
SCOPE = "model_governance_runtime_trial_planning"
SOURCE_CHAIN = "model_governance_runtime_trial_planning_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Recognition Midplatform Model Governance Integrated Closure，规划模型治理 Runtime Trial 的"
    "准入门、执行边界、降级路径、阻断规则、退出条件和审计记录。该阶段必须复用既有治理协议与准入链路，不创建新的"
    "准入体系，不重新设计 runtime governance，不执行真实 runtime，不下载模型，不执行 inference，不接 live "
    "camera/sensor，不触发 navigation/action/speech/fact_write。Runtime Trial Planning 是治理复用而非新体系，"
    "是受控运行试验规划而非 runtime 执行。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "runtime_trial_planning_reuses_governance_plans_controlled_trial_boundary_only_no_vla_action_chain"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
RUNTIME_TRIAL_MODE = "model_governance_runtime_trial_planning_only"
PLANNING_ONLY = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_ADMISSION_CONTRACT_CREATED = False
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = (
    "runtime_trial_planning_post_review_or_p1_download_license_planning"
)

INTEGRATED_CLOSURE_EXPECTED_GO = (
    "RECOGNITION_MIDPLATFORM_MODEL_GOVERNANCE_INTEGRATED_CLOSURE_GO"
)

# --------------------------------------------------------------------------- #
# 1. Governance reuse references (>= 8 reused assets)
# --------------------------------------------------------------------------- #
GOVERNANCE_REUSE_REFERENCES: Tuple[Dict[str, str], ...] = (
    {
        "governance_asset": "ControlledTrialGovernanceLifecycleTemplateV1",
        "usage": "trial_lifecycle_entry_gate_exit_gate_rollback_blocker_record_discipline",
    },
    {
        "governance_asset": "Phase-Midplatform-Model-Admission-Governance-Standard-v1-001",
        "usage": "model_admission_license_ref_model_origin_allowed_use_commercial_status_test_only_reserved_only_unavailable_record",
    },
    {
        "governance_asset": "Phase-Midplatform-Interface-Layer-Governance-Protocol-v1-001",
        "usage": "model_output_must_pass_adapter_no_native_direct_to_field_task_guidance",
    },
    {
        "governance_asset": "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001",
        "usage": "target_chain_ref_all_outputs_enter_evidence_candidate_path",
    },
    {
        "governance_asset": "Phase-Field-Task-Guidance-Safety-Chain-Closure-v1-001",
        "usage": "guidance_candidate_not_runtime_nav_speech_gate_not_tts_action_safety_no_action",
    },
    {
        "governance_asset": "Phase-PhaseOne-Environment-Cognition-Controlled-Runtime-Trial-Governance-Closure-v1-001",
        "usage": "runtime_activation_false_controlled_trial_boundary_no_live_uncontrolled_runtime",
    },
    {
        "governance_asset": "Phase-Midplatform-Model-Data-Handling-DryRun-v1-001",
        "usage": "candidate_ingress_normalization_source_chain_confidence_conflict_uncertainty_unavailable_reserved_degraded_lifecycle",
    },
    {
        "governance_asset": "Phase-Midplatform-Model-Control-DryRun-v1-001",
        "usage": "enable_disable_fallback_degraded_license_routing_output_blocking_availability_reserved_block_candidate_gate",
    },
)

# Optional governance reuse refs (owner/record approval): recorded if present,
# never gating, and never re-create an approval contract.
OPTIONAL_GOVERNANCE_REUSE_REFERENCES: Tuple[Dict[str, str], ...] = (
    {
        "governance_asset": "owner_approval_governance_ref",
        "usage": "future_runtime_execution_requires_owner_approval_no_rebuild_here",
        "artifact_rel": (
            "_tmp_eval_out/owner_approval_request_record_approval_closure_v1_smoke_v0/"
            "owner_approval_request_record_approval_closure_review_v1.json"
        ),
    },
    {
        "governance_asset": "record_approval_governance_ref",
        "usage": "future_runtime_execution_requires_record_approval_no_rebuild_here",
        "artifact_rel": (
            "_tmp_eval_out/record_approval_closure_v1_smoke_v0/"
            "record_approval_closure_review_v1.json"
        ),
    },
)

# --------------------------------------------------------------------------- #
# 2. Runtime trial entry gate policies (>= 10)
# --------------------------------------------------------------------------- #
ENTRY_GATE_POLICIES: Tuple[str, ...] = (
    "integrated_model_governance_closure_go_verified",
    "controlled_trial_template_ref_ok",
    "model_admission_governance_verified",
    "interface_layer_governance_verified",
    "runtime_governance_closure_verified",
    "field_task_guidance_safety_chain_verified",
    "model_data_handling_baseline_verified",
    "model_control_baseline_verified",
    "candidate_only_boundary_verified",
    "commercial_runtime_not_approved",
    "vla_action_chain_excluded",
    "owner_or_record_approval_required_for_future_execution",
)

ALLOWED_FUTURE_TRIAL_SCOPE: Tuple[str, ...] = (
    "controlled_model_invocation_trial_planning",
    "local_file_input_trial_planning",
    "candidate_output_runtime_path_planning",
    "midplatform_controlled_inference_trial_planning",
    "model_availability_fallback_disable_block_planning",
    "artifact_trace_audit_record_planning",
)

# --------------------------------------------------------------------------- #
# 3. Runtime trial execution boundary policies (>= 12)
#    mode: planning_allowed_not_executed | currently_not_allowed
# --------------------------------------------------------------------------- #
EXECUTION_BOUNDARY_PLANNING_ALLOWED: Tuple[str, ...] = (
    "local_controlled_file_input",
    "model_call_through_midplatform_control",
    "candidate_output_through_recognition_model_output_adapter",
    "candidate_ingress_through_midplatform_model_data_handling",
    "model_enable_fallback_disable_block_through_midplatform_model_control",
    "trace_audit_review_artifact_write",
)

EXECUTION_BOUNDARY_CURRENTLY_NOT_ALLOWED: Tuple[str, ...] = (
    "live_camera",
    "live_sensor",
    "continuous_runtime",
    "navigation_runtime",
    "action_runtime",
    "speech_runtime",
    "fact_write_runtime",
    "vla_action_chain",
    "commercial_runtime",
    "unapproved_dataset_usage",
    "model_tuning",
    "uncontrolled_inference",
    "model_output_bypassing_adapter",
    "model_output_bypassing_midplatform",
)

# --------------------------------------------------------------------------- #
# 4. Runtime trial model scope policies (>= 7)
# --------------------------------------------------------------------------- #
MODEL_SCOPE_POLICIES: Tuple[Dict[str, str], ...] = (
    {
        "tier": "p0",
        "model_ref": "rapidocr",
        "eligibility": "trial_eligible_if_governance_approved",
    },
    {
        "tier": "p0",
        "model_ref": "opencv_visual_symbol_rule",
        "eligibility": "trial_eligible_if_governance_approved",
    },
    {
        "tier": "p0",
        "model_ref": "yolo_lightweight",
        "eligibility": "trial_eligible_only_if_local_weight_exists_and_remains_test_only",
    },
    {
        "tier": "p1_p2",
        "model_ref": "segmentation_family",
        "eligibility": "requires_download_or_license_planning_or_local_availability_upgrade",
    },
    {
        "tier": "p1_p2",
        "model_ref": "tracking_family",
        "eligibility": "contract_only_not_runtime_eligible",
    },
    {
        "tier": "p1_p2",
        "model_ref": "depth_spatial_hint_family",
        "eligibility": "deferred_due_to_resource",
    },
    {
        "tier": "p1_p2",
        "model_ref": "object_detection_completion_family",
        "eligibility": "test_only_or_license_constrained",
    },
    {
        "tier": "p1_p2",
        "model_ref": "scene_relation_vlm_family",
        "eligibility": "deferred_due_to_output_instability",
    },
    {
        "tier": "p1_p2",
        "model_ref": "audio_speech_family",
        "eligibility": "reserved_only_runtime_blocked",
    },
    {
        "tier": "p1_p2",
        "model_ref": "emotion_multimodal_bridge_family",
        "eligibility": "reserved_only_runtime_blocked",
    },
)

# --------------------------------------------------------------------------- #
# 5. Runtime trial input boundary policies (>= 8)
# --------------------------------------------------------------------------- #
INPUT_BOUNDARY_ALLOWED: Tuple[str, ...] = (
    "local_controlled_image_file",
    "local_controlled_json_candidate_bundle",
    "sealed_artifact_reuse",
    "synthetic_test_image",
    "manually_approved_static_sample",
)

INPUT_BOUNDARY_FORBIDDEN: Tuple[str, ...] = (
    "live_camera_stream",
    "live_microphone_stream",
    "live_sensor_stream",
    "continuous_video_runtime",
    "external_dataset_batch",
    "production_user_data",
    "internet_connected_uncontrolled_input",
    "private_user_data_without_approval",
)

# --------------------------------------------------------------------------- #
# 6. Runtime trial output boundary policies (>= 8)
# --------------------------------------------------------------------------- #
OUTPUT_BOUNDARY_PATH: Tuple[str, ...] = (
    "model_output",
    "recognition_model_output_adapter",
    "evidence_candidate",
    "midplatform_model_data_handling",
    "midplatform_model_control",
    "field_task_guidance_candidate_support",
)

OUTPUT_BOUNDARY_FORBIDDEN: Tuple[str, ...] = (
    "direct_fact_write",
    "direct_field_task_guidance_write",
    "direct_navigation",
    "direct_action",
    "direct_speech_or_tts",
    "vla_action_chain",
    "commercial_runtime_output",
)

# --------------------------------------------------------------------------- #
# 7. Fallback / blocker / exit policies
# --------------------------------------------------------------------------- #
FALLBACK_POLICIES: Tuple[str, ...] = (
    "model_unavailable",
    "local_weight_missing",
    "license_boundary_unclear",
    "low_confidence",
    "adapter_mapping_failure",
    "output_schema_drift",
    "source_chain_missing",
    "confidence_missing",
    "reserved_only_family_request",
    "runtime_resource_unavailable",
)

BLOCKER_POLICIES: Tuple[str, ...] = (
    "model_output_bypasses_adapter",
    "model_output_bypasses_midplatform",
    "candidate_attempts_fact_admission",
    "guidance_becomes_runtime_navigation",
    "speech_gate_triggers_tts",
    "action_safety_triggers_action",
    "live_camera_or_sensor_requested",
    "vla_chain_injected",
    "commercial_runtime_claim",
    "model_tuning_or_dataset_usage_requested",
    "unapproved_data_used",
)

EXIT_POLICIES: Tuple[str, ...] = (
    "successful_controlled_trial_record",
    "degraded_trial_record",
    "blocked_trial_record",
    "rollback_or_stop_condition",
    "audit_artifact_required",
    "no_state_promotion_without_review",
)

# --------------------------------------------------------------------------- #
# 8. Audit / trace / record policies (>= 10)
# --------------------------------------------------------------------------- #
AUDIT_RECORD_POLICIES: Tuple[str, ...] = (
    "runtime_trial_entry_record",
    "governance_reuse_record",
    "model_scope_record",
    "input_boundary_record",
    "output_boundary_record",
    "model_invocation_control_record",
    "adapter_output_record",
    "midplatform_data_handling_record",
    "midplatform_model_control_record",
    "fallback_record",
    "blocker_record",
    "exit_record",
    "audit_trace",
    "whitebox_candidate",
    "review_artifact_ref",
)

AUDIT_RECORD_REQUIRED_FIELDS: Tuple[str, ...] = (
    "source_chain",
    "stage_ref",
    "governance_ref",
    "timestamp_or_run_ref",
)

# --------------------------------------------------------------------------- #
# 9. Negative planning guards (12) — id -> (go_key, depends_on invariant)
# --------------------------------------------------------------------------- #
NEGATIVE_PLANNING_GUARDS: Tuple[Dict[str, str], ...] = (
    {
        "guard_id": "invalid_new_admission_contract_created",
        "go_key": "new_admission_contract_blocked",
        "depends_on": "new_admission_contract_not_created",
    },
    {
        "guard_id": "invalid_missing_controlled_trial_template",
        "go_key": "missing_controlled_trial_template_blocked",
        "depends_on": "controlled_trial_template_reused",
    },
    {
        "guard_id": "invalid_runtime_trial_planning_as_execution",
        "go_key": "runtime_execution_blocked",
        "depends_on": "runtime_execution_not_allowed",
    },
    {
        "guard_id": "invalid_live_camera_sensor",
        "go_key": "live_camera_sensor_blocked",
        "depends_on": "live_camera_sensor_not_connected",
    },
    {
        "guard_id": "invalid_direct_action_speech_fact_write",
        "go_key": "direct_action_speech_fact_write_blocked",
        "depends_on": "direct_action_speech_fact_write_not_allowed",
    },
    {
        "guard_id": "invalid_guidance_runtime_navigation",
        "go_key": "guidance_runtime_navigation_blocked",
        "depends_on": "navigation_runtime_not_allowed",
    },
    {
        "guard_id": "invalid_vla_action_chain",
        "go_key": "vla_action_chain_blocked",
        "depends_on": "vla_action_chain_not_allowed",
    },
    {
        "guard_id": "invalid_commercial_runtime",
        "go_key": "commercial_runtime_blocked",
        "depends_on": "commercial_runtime_not_approved",
    },
    {
        "guard_id": "invalid_model_tuning_dataset_usage",
        "go_key": "model_tuning_dataset_usage_blocked",
        "depends_on": "model_tuning_dataset_usage_not_allowed",
    },
    {
        "guard_id": "invalid_adapter_midplatform_bypass",
        "go_key": "adapter_midplatform_bypass_blocked",
        "depends_on": "adapter_midplatform_required",
    },
    {
        "guard_id": "invalid_reserved_family_runtime_eligible",
        "go_key": "reserved_family_runtime_eligible_blocked",
        "depends_on": "reserved_only_family_runtime_blocked",
    },
    {
        "guard_id": "invalid_trial_success_runtime_promotion",
        "go_key": "trial_success_runtime_promotion_blocked",
        "depends_on": "trial_success_not_runtime_promotion",
    },
)

# --------------------------------------------------------------------------- #
# Governance rules (32)
# --------------------------------------------------------------------------- #
PLANNING_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_runtime_trial_planning_only",
    "existing_governance_contracts_must_be_reused",
    "no_new_admission_contract_is_created",
    "no_new_runtime_governance_system_is_created",
    "controlled_trial_governance_lifecycle_template_must_be_reused",
    "runtime_execution_is_not_allowed",
    "real_inference_is_not_allowed",
    "new_model_download_is_not_allowed",
    "live_camera_is_not_allowed",
    "live_sensor_is_not_allowed",
    "continuous_runtime_is_not_allowed",
    "navigation_runtime_is_not_allowed",
    "action_runtime_is_not_allowed",
    "speech_runtime_is_not_allowed",
    "fact_write_runtime_is_not_allowed",
    "commercial_runtime_is_not_approved",
    "model_tuning_is_not_allowed",
    "dataset_usage_is_not_allowed",
    "reserved_only_families_are_not_runtime_eligible",
    "model_output_must_pass_recognition_model_output_adapter",
    "model_output_must_pass_midplatform_model_data_handling",
    "model_output_must_pass_midplatform_model_control",
    "candidate_only_boundary_must_be_preserved",
    "candidate_ingress_is_not_fact_admission",
    "candidate_output_gate_is_not_fact_admission",
    "guidance_candidate_is_not_runtime_navigation",
    "speech_gate_candidate_is_not_tts",
    "action_safety_candidate_does_not_trigger_action",
    "vla_action_chain_is_excluded",
    "trial_success_is_not_runtime_promotion",
    "luna_emotion_multimodal_brain_cognition_first_principle_is_preserved",
    "future_runtime_execution_requires_separate_approval_and_dryrun",
)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "ModelGovernanceRuntimeTrialPlanningProfile",
    "GovernanceReuseReference",
    "RuntimeTrialEntryGatePolicy",
    "RuntimeTrialExecutionBoundaryPolicy",
    "RuntimeTrialModelScopePolicy",
    "RuntimeTrialInputBoundaryPolicy",
    "RuntimeTrialOutputBoundaryPolicy",
    "RuntimeTrialFallbackPolicy",
    "RuntimeTrialBlockerPolicy",
    "RuntimeTrialExitPolicy",
    "RuntimeTrialAuditRecordPolicy",
    "RuntimeTrialHandoffReadiness",
    "ModelGovernanceRuntimeTrialPlanningDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-Model-Governance-Runtime-Trial-Planning-Post-Review-v1-001",
        "go_key": "runtime_trial_planning_post_review_readiness_recorded",
    },
    {
        "target_ref": "Phase-Recognition-Model-P1-Download-License-Planning-v1-001",
        "go_key": "p1_download_license_planning_readiness_recorded",
    },
)

FINAL_DECISION_GO = "MODEL_GOVERNANCE_RUNTIME_TRIAL_PLANNING_GO"
FINAL_DECISION_BLOCKED = "MODEL_GOVERNANCE_RUNTIME_TRIAL_PLANNING_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
}

NEGATED_CREATION_FLAGS: Dict[str, bool] = {
    "new_admission_contract_created": False,
    "new_runtime_governance_created": False,
}

PLANNING_TRUE_INVARIANTS: Dict[str, bool] = {
    "p0_trial_candidate_scope_planned": True,
    "p1_p2_trial_requires_additional_planning": True,
    "reserved_only_family_runtime_blocked": True,
    "candidate_only_boundary_preserved": True,
    "model_output_adapter_required": True,
    "midplatform_data_handling_required": True,
    "midplatform_model_control_required": True,
    "commercial_runtime_not_approved": True,
    "vla_action_chain_excluded": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

RUNTIME_TRIAL_ELIGIBLE_DEFAULT = False

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "runtime_execution_allowed": False,
    "real_inference_allowed": False,
    "new_model_download_allowed": False,
    "new_image_recognition_allowed": False,
    "single_model_debugging_allowed": False,
    "model_tuning_allowed": False,
    "dataset_usage_allowed": False,
    "training_use_allowed": False,
    "dataset_download_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "runtime_activation_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
}


@dataclass(frozen=True)
class ModelGovernanceRuntimeTrialPlanningProfile:
    profile_ref: str
    phase_id: str
    runtime_trial_mode: str
    planning_only: bool
    existing_governance_reuse_required: bool
    new_admission_contract_created: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    model_governance_integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    entry_gate_policies: Tuple[str, ...]
    execution_boundary_planning_allowed: Tuple[str, ...]
    execution_boundary_currently_not_allowed: Tuple[str, ...]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class GovernanceReuseReference:
    governance_asset: str
    usage: str
    reused: bool
    optional: bool
    present: bool


@dataclass(frozen=True)
class RuntimeTrialEntryGatePolicy:
    gate_condition: str
    planned: bool


@dataclass(frozen=True)
class RuntimeTrialExecutionBoundaryPolicy:
    boundary_item: str
    mode: str


@dataclass(frozen=True)
class RuntimeTrialModelScopePolicy:
    tier: str
    model_ref: str
    eligibility: str
    runtime_trial_eligible_default: bool


@dataclass(frozen=True)
class RuntimeTrialInputBoundaryPolicy:
    input_item: str
    allowed_for_planning: bool


@dataclass(frozen=True)
class RuntimeTrialOutputBoundaryPolicy:
    output_item: str
    role: str


@dataclass(frozen=True)
class RuntimeTrialFallbackPolicy:
    trigger: str
    candidate_only: bool
    triggers_download_or_inference: bool


@dataclass(frozen=True)
class RuntimeTrialBlockerPolicy:
    violation: str
    blocks: bool


@dataclass(frozen=True)
class RuntimeTrialExitPolicy:
    exit_condition: str
    requires_audit_artifact: bool
    state_promotion_without_review: bool


@dataclass(frozen=True)
class RuntimeTrialAuditRecordPolicy:
    record_type: str
    required_fields: Tuple[str, ...]


@dataclass(frozen=True)
class RuntimeTrialHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass
class RuntimeTrialNegativePlanningGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class ModelGovernanceRuntimeTrialPlanningDecision:
    decision_ref: str
    planning_profile_count: int
    governance_reuse_ref_count: int
    entry_gate_policy_count: int
    execution_boundary_policy_count: int
    model_scope_policy_count: int
    input_boundary_policy_count: int
    output_boundary_policy_count: int
    fallback_policy_count: int
    blocker_policy_count: int
    exit_policy_count: int
    audit_record_policy_count: int
    negative_planning_guard_count: int
    negative_planning_guard_passed: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
