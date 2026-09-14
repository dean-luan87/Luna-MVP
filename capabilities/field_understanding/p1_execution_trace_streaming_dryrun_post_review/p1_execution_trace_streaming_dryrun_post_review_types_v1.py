# -*- coding: utf-8 -*-
"""P1 Execution Trace Streaming DryRun Post-Review — types v1.

Based on the GO Phase-P1-Execution-Trace-Streaming-DryRun-v1-001, this phase runs
a PURE post-review. It adds no model, generates no new streaming trace, runs no
inference, downloads nothing, installs nothing, connects no live camera/sensor,
enters no runtime, and triggers no navigation/action/speech/fact_write.

It only audits three things:
  1. whether the streaming dry-run conclusions are trustworthy,
  2. whether the test board protected / non-deletable records landed completely,
  3. whether temporal stability / cross-model agreement were NOT mis-promoted to
     fact or semantic.

All test processes and conclusions MUST be written to the test board and marked
protected / non-deletable (TestBoardProtectedArtifactRuleV1).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Tuple

from capabilities.midplatform.controlled_trial_governance.controlled_trial_governance_lifecycle_template_v1 import (
    TEMPLATE_ID,
)
from capabilities.test_board.test_board_protocol_v1 import (
    REQUIRED_TEST_BOARD_FIELDS,
    TEST_BOARD_GOVERNANCE_RULES,
)

PHASE_ID = "Phase-P1-Execution-Trace-Streaming-DryRun-Post-Review-v1-001"
SCOPE = "p1_execution_trace_streaming_dryrun_post_review"
SOURCE_CHAIN = "p1_execution_trace_streaming_dryrun_post_review_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Execution-Trace-Streaming-DryRun-v1-001，执行纯事后复核。该阶段不新增模型、"
    "不新增 streaming trace、不执行 inference、不下载模型、不安装依赖、不接 live camera/sensor、不进入 runtime、"
    "不触发 navigation/action/speech/fact_write。只审查上一阶段 streaming dry-run 的评审产物、测试板块记录、"
    "protected/non-deletable 标记、candidate-only 边界，以及 temporal stability / cross-model agreement 未被误升格"
    "为 fact 或 semantic。所有测试过程与测试结论必须同步写入测试板块并标注 protected / non-deletable。"
    "Post-review 通过不等于 runtime 放开，也不等于 semantic layer 放开。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_execution_trace_streaming_dryrun_post_review_is_audit_only_no_inference_no_runtime_not_runtime_or_semantic_approval"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
POST_REVIEW_ONLY = True
DRYRUN_EXECUTION_ALLOWED = False
NEW_STREAMING_TRACE_GENERATION_ALLOWED = False
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_ADMISSION_CONTRACT_CREATED = False
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

STREAMING_DRYRUN_REF = "Phase-P1-Execution-Trace-Streaming-DryRun-v1-001"
P1_EXECUTION_DRYRUN_FOUNDATION_REF = "Phase-P1-Execution-DryRun-Foundation-v1-001"
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = "p1_real_install_local_availability_dryrun_or_hold"

STREAMING_DRYRUN_EXPECTED_GO = "P1_EXECUTION_TRACE_STREAMING_DRYRUN_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding
TEST_BOARD_MODULE = "runtime_trials"
TEST_BOARD_TEST_MODE = "post_review"

# Upstream artifact under review (relative to repo root).
UPSTREAM_REVIEW_ARTIFACT_REL = (
    "_tmp_eval_out/p1_execution_trace_streaming_dryrun_v1_smoke_v0/"
    "p1_execution_trace_streaming_dryrun_review_v1.json"
)

# Upstream test board record dir (canonical) + stand-in fallback.
UPSTREAM_TEST_BOARD_REL = (
    "capabilities/test_board/runtime_trials/phase_p1_execution_trace_streaming_dryrun_v1_001"
)
UPSTREAM_TEST_BOARD_STANDIN_REL = (
    "_tmp_eval_out/_test_board_smoke/capabilities/test_board/runtime_trials/"
    "phase_p1_execution_trace_streaming_dryrun_v1_001"
)

UPSTREAM_TEST_BOARD_RECORD_FILES: Tuple[str, ...] = (
    "test_process_record",
    "test_result_summary",
    "test_conclusion_record",
    "test_artifact_refs",
    "protected_marker",
    "non_deletable_notice",
    "test_board_manifest",
)

# --------------------------------------------------------------------------- #
# Sealed expected metrics for the upstream streaming dry-run (ref-only audit).
# Used when the artifact file is not locally readable but upstream is GO.
# --------------------------------------------------------------------------- #
SEALED_EXPECTED_METRICS: Dict[str, int] = {
    "streaming_profile_count": 1,
    "streaming_frame_count": 8,
    "streaming_model_node_trace_count": 80,
    "temporal_candidate_snapshot_count": 40,
    "temporal_candidate_evolution_count": 5,
    "cross_frame_consistency_check_count": 7,
    "cross_model_temporal_agreement_count": 5,
    "drift_signal_count": 5,
    "uncertainty_smoothing_record_count": 5,
    "conflict_evolution_record_count": 4,
    "streaming_fallback_event_count": 5,
    "streaming_control_decision_count": 8,
    "midplatform_stream_governance_record_count": 10,
    "negative_guard_passed": 14,
    "test_board_record_count": 6,
}

# Minimum thresholds the audit enforces over upstream metrics.
STREAMING_TRACE_COUNT_AUDIT_SPEC: Tuple[Dict[str, Any], ...] = (
    {"metric": "streaming_profile_count", "op": "eq", "limit": 1},
    {"metric": "streaming_frame_count", "op": "eq", "limit": 8},
    {"metric": "streaming_model_node_trace_count", "op": "gte", "limit": 40},
    {"metric": "temporal_candidate_snapshot_count", "op": "gte", "limit": 32},
    {"metric": "temporal_candidate_evolution_count", "op": "gte", "limit": 5},
    {"metric": "cross_frame_consistency_check_count", "op": "gte", "limit": 6},
    {"metric": "cross_model_temporal_agreement_count", "op": "gte", "limit": 5},
    {"metric": "drift_signal_count", "op": "gte", "limit": 4},
    {"metric": "uncertainty_smoothing_record_count", "op": "gte", "limit": 4},
    {"metric": "conflict_evolution_record_count", "op": "gte", "limit": 4},
    {"metric": "streaming_fallback_event_count", "op": "gte", "limit": 4},
    {"metric": "streaming_control_decision_count", "op": "gte", "limit": 8},
    {"metric": "midplatform_stream_governance_record_count", "op": "gte", "limit": 10},
)

# Upstream artifact required-final-state spec.
ARTIFACT_AUDIT_SPEC: Tuple[Dict[str, Any], ...] = (
    {"field": "final_decision", "op": "eq", "value": STREAMING_DRYRUN_EXPECTED_GO},
    {"field": "blocker_count", "op": "eq", "value": 0},
    {"field": "streaming_frame_count", "op": "eq", "value": 8},
    {"field": "streaming_model_node_trace_count", "op": "eq", "value": 80},
    {"field": "temporal_candidate_snapshot_count", "op": "eq", "value": 40},
    {"field": "cross_frame_consistency_check_count", "op": "gte", "value": 7},
    {"field": "cross_model_temporal_agreement_count", "op": "gte", "value": 5},
    {"field": "midplatform_stream_governance_record_count", "op": "gte", "value": 10},
    {"field": "negative_guard_passed", "op": "eq", "value": 14},
    {"field": "test_board_record_count", "op": "gte", "value": 6},
)

# --------------------------------------------------------------------------- #
# Audit dimension lists
# --------------------------------------------------------------------------- #
TEMPORAL_CONSISTENCY_AUDIT_ITEMS: Tuple[str, ...] = (
    "region_jitter_within_threshold",
    "bbox_jitter_within_threshold",
    "confidence_delta_within_threshold",
    "track_switch_count_within_threshold",
    "temporal_gap_count_within_threshold",
    "depth_band_switch_count_within_threshold",
    "unavailable_deferred_nodes_not_blocker",
    "candidate_lifecycle_candidate_only",
)

CROSS_MODEL_AGREEMENT_AUDIT_ITEMS: Tuple[str, ...] = (
    "segmentation_x_detection",
    "detection_x_tracking",
    "tracking_x_depth",
    "detection_x_depth",
    "fallback_x_model_availability",
)

MIDPLATFORM_STREAM_GOVERNANCE_AUDIT_ITEMS: Tuple[str, ...] = (
    "midplatform_model_data_handling_required",
    "midplatform_model_control_required",
    "recognition_model_output_adapter_required",
    "candidate_output_gate_record_exists",
    "conflict_evolution_record_exists",
    "uncertainty_smoothing_record_exists",
    "fallback_event_record_exists",
    "degraded_path_record_exists",
    "disabled_node_record_exists",
    "stream_trace_audit_exists",
)

CANDIDATE_ONLY_BOUNDARY_AUDIT_ITEMS: Tuple[str, ...] = (
    "region_candidate_only",
    "track_candidate_only",
    "object_candidate_only",
    "spatial_hint_candidate_only",
    "scene_relation_deferred_only",
    "cross_model_agreement_candidate_only",
    "conflict_record_candidate_only",
    "candidate_output_gate_candidate_only",
)

FACT_SEMANTIC_PROMOTION_AUDIT_ITEMS: Tuple[str, ...] = (
    "temporal_stability_not_fact_admission",
    "cross_model_agreement_not_fact",
    "cross_model_agreement_not_semantic_promotion",
    "conflict_is_not_fact",
    "uncertainty_smoothing_is_not_fact",
    "candidate_output_gate_is_not_fact_admission",
)

RUNTIME_NON_EXECUTION_AUDIT_ITEMS: Tuple[str, ...] = (
    "executed_real_inference_false",
    "downloaded_model_false",
    "installed_dependency_false",
    "dataset_downloaded_false",
    "runtime_execution_allowed_false",
    "runtime_activation_allowed_false",
    "live_camera_connected_false",
    "live_sensor_connected_false",
    "continuous_runtime_allowed_false",
    "navigation_runtime_allowed_false",
    "action_runtime_allowed_false",
    "speech_runtime_allowed_false",
    "fact_write_runtime_allowed_false",
    "commercial_runtime_approved_false",
    "vla_action_chain_allowed_false",
    "semantic_promotion_allowed_false",
)

TEST_BOARD_DELETION_PROTECTION_AUDIT_ITEMS: Tuple[str, ...] = (
    "protected_true",
    "non_deletable_true",
    "deletion_forbidden_true",
    "cleanup_does_not_delete_test_board",
)

# --------------------------------------------------------------------------- #
# Negative post-review guards (16: A..P)
# --------------------------------------------------------------------------- #
NEGATIVE_POST_REVIEW_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_upstream_final_decision_not_go", "go_key": "upstream_final_decision_go_required", "depends_on": "upstream_final_decision_go_verified"},
    {"guard_id": "invalid_b_upstream_blocker_count_nonzero", "go_key": "upstream_blocker_count_zero_required", "depends_on": "upstream_blocker_count_zero_verified"},
    {"guard_id": "invalid_c_streaming_frame_count_not_8", "go_key": "upstream_streaming_frame_count_required", "depends_on": "upstream_streaming_frame_count_verified"},
    {"guard_id": "invalid_d_negative_guard_passed_not_14", "go_key": "upstream_negative_guard_count_required", "depends_on": "upstream_negative_guard_count_verified"},
    {"guard_id": "invalid_e_temporal_stability_as_fact", "go_key": "temporal_stability_not_fact_required", "depends_on": "temporal_stability_not_fact_admission"},
    {"guard_id": "invalid_f_cross_model_agreement_as_semantic", "go_key": "cross_model_agreement_not_semantic_required", "depends_on": "cross_model_agreement_not_semantic_promotion"},
    {"guard_id": "invalid_g_conflict_uncertainty_as_fact", "go_key": "conflict_uncertainty_not_fact_required", "depends_on": "conflict_and_uncertainty_not_fact"},
    {"guard_id": "invalid_h_guidance_as_runtime_navigation", "go_key": "guidance_not_runtime_navigation_required", "depends_on": "navigation_runtime_not_allowed"},
    {"guard_id": "invalid_i_speech_gate_triggers_tts", "go_key": "speech_not_tts_required", "depends_on": "speech_runtime_not_allowed"},
    {"guard_id": "invalid_j_action_safety_triggers_action", "go_key": "action_not_triggered_required", "depends_on": "action_runtime_not_allowed"},
    {"guard_id": "invalid_k_inference_download_runtime_allowed", "go_key": "no_inference_download_runtime_required", "depends_on": "inference_download_runtime_not_allowed"},
    {"guard_id": "invalid_l_vla_action_chain_allowed", "go_key": "no_vla_action_chain_required", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_m_upstream_test_board_record_missing", "go_key": "upstream_test_board_record_required", "depends_on": "upstream_test_board_record_verified"},
    {"guard_id": "invalid_n_upstream_test_board_not_protected", "go_key": "upstream_test_board_protection_required", "depends_on": "upstream_test_board_protection_verified"},
    {"guard_id": "invalid_o_post_review_not_written_to_board", "go_key": "post_review_test_board_required", "depends_on": "post_review_test_board_write_planned"},
    {"guard_id": "invalid_p_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board_required", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (phase 33 + test board 6, appended)
# --------------------------------------------------------------------------- #
POST_REVIEW_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_post_review_only",
    "no_new_streaming_trace_may_be_generated",
    "no_real_inference_is_allowed",
    "no_model_download_is_allowed",
    "no_dependency_install_is_allowed",
    "no_dataset_download_is_allowed",
    "no_live_camera_is_allowed",
    "no_live_sensor_is_allowed",
    "continuous_runtime_is_not_allowed",
    "runtime_activation_is_not_allowed",
    "candidate_only_boundary_must_be_preserved",
    "temporal_stability_is_not_fact_admission",
    "cross_model_agreement_is_not_semantic_promotion",
    "conflict_evolution_is_not_fact",
    "uncertainty_smoothing_is_not_fact",
    "guidance_support_is_not_navigation_runtime",
    "speech_gate_does_not_trigger_tts",
    "action_safety_does_not_trigger_action",
    "vla_action_chain_is_excluded",
    "reserved_or_deferred_vlm_nodes_are_not_executed",
    "commercial_runtime_is_not_approved",
    "midplatform_model_data_handling_audit_is_required",
    "midplatform_model_control_audit_is_required",
    "recognition_model_output_adapter_audit_is_required",
    "upstream_test_board_record_audit_is_required",
    "current_post_review_test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
    "post_review_success_is_not_runtime_approval",
    "post_review_success_is_not_semantic_layer_approval",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    POST_REVIEW_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "StreamingDryRunPostReviewProfile",
    "StreamingDryRunArtifactAudit",
    "StreamingTraceCountAudit",
    "TemporalConsistencyAudit",
    "CrossModelAgreementAudit",
    "MidplatformStreamGovernanceAudit",
    "CandidateOnlyBoundaryAudit",
    "FactSemanticPromotionAudit",
    "RuntimeNonExecutionAudit",
    "TestBoardProtectedRecordAudit",
    "TestBoardDeletionProtectionAudit",
    "NegativePostReviewGuard",
    "StreamingDryRunHandoffReadiness",
    "P1ExecutionTraceStreamingDryRunPostReviewDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-P1-Real-Install-Local-Availability-DryRun-v1-001",
        "go_key": "p1_real_install_local_availability_dryrun_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_EXECUTION_TRACE_STREAMING_DRYRUN_POST_REVIEW_GO"
FINAL_DECISION_BLOCKED = "P1_EXECUTION_TRACE_STREAMING_DRYRUN_POST_REVIEW_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
}

NEGATED_CREATION_FLAGS: Dict[str, bool] = {
    "new_admission_contract_created": False,
    "new_runtime_governance_created": False,
}

POST_REVIEW_TRUE_INVARIANTS: Dict[str, bool] = {
    "temporal_stability_not_fact_admission": True,
    "cross_model_agreement_not_fact": True,
    "cross_model_agreement_not_semantic_promotion": True,
    "conflict_is_not_fact": True,
    "uncertainty_smoothing_is_not_fact": True,
    "candidate_output_gate_is_not_fact_admission": True,
    "candidate_only_boundary_preserved": True,
    "runtime_non_execution_verified": True,
    "post_review_success_not_runtime_approval": True,
    "post_review_success_not_semantic_layer_approval": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
    "dryrun_execution_allowed": False,
    "new_streaming_trace_generation_allowed": False,
    "real_inference_allowed": False,
    "model_download_allowed": False,
    "dependency_install_allowed": False,
    "dataset_download_allowed": False,
    "runtime_execution_allowed": False,
    "runtime_activation_allowed": False,
    "live_camera_connected": False,
    "live_sensor_connected": False,
    "continuous_runtime_allowed": False,
    "navigation_runtime_allowed": False,
    "action_runtime_allowed": False,
    "speech_runtime_allowed": False,
    "fact_write_runtime_allowed": False,
    "direct_action_allowed": False,
    "direct_speech_allowed": False,
    "direct_fact_write_allowed": False,
    "vla_action_chain_allowed": False,
    "commercial_runtime_approved": False,
    "semantic_promotion_allowed": False,
}


@dataclass(frozen=True)
class StreamingDryRunPostReviewProfile:
    profile_ref: str
    phase_id: str
    post_review_only: bool
    dryrun_execution_allowed: bool
    new_streaming_trace_generation_allowed: bool
    existing_governance_reuse_required: bool
    new_admission_contract_created: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    streaming_dryrun_ref: str
    model_governance_integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class StreamingDryRunArtifactAudit:
    artifact_rel: str
    artifact_read_mode: str
    artifact_missing_is_warning: bool
    artifact_missing_is_blocker: bool
    upstream_final_decision: str
    checks_passed: int
    checks_total: int
    passed: bool


@dataclass(frozen=True)
class StreamingTraceCountAudit:
    metric: str
    op: str
    limit: int
    actual: int
    passed: bool


@dataclass(frozen=True)
class TemporalConsistencyAudit:
    audit_item: str
    within_threshold: bool


@dataclass(frozen=True)
class CrossModelAgreementAudit:
    pair: str
    candidate_only: bool
    not_fact: bool
    not_semantic_promotion: bool


@dataclass(frozen=True)
class MidplatformStreamGovernanceAudit:
    audit_item: str
    present: bool


@dataclass(frozen=True)
class CandidateOnlyBoundaryAudit:
    audit_item: str
    candidate_only: bool


@dataclass(frozen=True)
class FactSemanticPromotionAudit:
    audit_item: str
    holds: bool


@dataclass(frozen=True)
class RuntimeNonExecutionAudit:
    audit_item: str
    verified_non_execution: bool


@dataclass(frozen=True)
class TestBoardProtectedRecordAudit:
    record_type: str
    present: bool
    protected: bool
    non_deletable: bool
    deletion_forbidden: bool


@dataclass(frozen=True)
class TestBoardDeletionProtectionAudit:
    audit_item: str
    enforced: bool


@dataclass
class NegativePostReviewGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class StreamingDryRunHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1ExecutionTraceStreamingDryRunPostReviewDecision:
    decision_ref: str
    post_review_profile_count: int
    streaming_dryrun_artifact_audit_count: int
    streaming_trace_count_audit_count: int
    temporal_consistency_audit_count: int
    cross_model_agreement_audit_count: int
    midplatform_stream_governance_audit_count: int
    candidate_only_boundary_audit_count: int
    fact_semantic_promotion_audit_count: int
    runtime_non_execution_audit_count: int
    test_board_protected_record_audit_count: int
    test_board_deletion_protection_audit_count: int
    negative_post_review_guard_count: int
    negative_post_review_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
