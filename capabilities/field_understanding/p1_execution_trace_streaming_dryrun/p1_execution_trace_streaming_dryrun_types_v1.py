# -*- coding: utf-8 -*-
"""P1 Execution Trace Streaming DryRun — types v1.

Based on the GO Phase-P1-Execution-DryRun-Foundation-v1-001, this phase upgrades
P1 executability simulation from a single-shot node-level dry-run into a continuous
multi-frame streaming-trace dry-run. It is a virtual streaming-trace simulation
only: no model download, no dependency install, no real inference, no live
camera/sensor, no runtime, and no action/speech/fact_write/navigation.

All test processes and conclusions MUST be written to the test board and marked
protected / non-deletable (TestBoardProtectedArtifactRuleV1).

Core principles:
1. Streaming dry-run only; streaming trace is a virtual test, not runtime.
2. Temporal stability is NOT fact admission.
3. Cross-model temporal agreement is NOT semantic promotion.
4. Conflict evolution / uncertainty smoothing are NOT fact.
5. Candidate-only boundary preserved; adapter + midplatform required.
6. Reserved / deferred VLM nodes are not executed; no VLA action chain.
7. Luna remains emotion-multimodal brain / cognition first.
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

PHASE_ID = "Phase-P1-Execution-Trace-Streaming-DryRun-v1-001"
SCOPE = "p1_execution_trace_streaming_dryrun"
SOURCE_CHAIN = "p1_execution_trace_streaming_dryrun_v1"

PLANNING_PRINCIPLE_ZH = (
    "基于已 GO 的 Phase-P1-Execution-DryRun-Foundation-v1-001，把 P1 可执行性模拟从单次节点级 dry-run 升级为"
    "连续帧 streaming trace dry-run。仅做虚拟流式执行轨迹模拟：不下载模型、不安装依赖、不执行真实 inference、"
    "不接 live camera/sensor、不进入 runtime、不触发 action/speech/fact_write/navigation。开始验证模型输出在时间"
    "维度上的稳定性、漂移、冲突与中台流式治理能力。所有测试过程与测试结论必须同步写入测试板块并标注 "
    "protected / non-deletable。时间稳定性不是 fact admission；跨模型时序一致不是 semantic promotion；"
    "conflict evolution / uncertainty smoothing 不是 fact；candidate-only 边界保持；reserved/deferred VLM 不执行；"
    "无 VLA action chain。"
)

LUNA_CORE_PRINCIPLE = (
    "luna_remains_emotion_multimodal_brain_and_world_understanding_first_"
    "p1_execution_trace_streaming_dryrun_is_virtual_streaming_trace_only_no_inference_no_download_no_runtime_candidate_only"
)

# --------------------------------------------------------------------------- #
# Bindings
# --------------------------------------------------------------------------- #
DRYRUN_MODE = "p1_execution_trace_streaming_dryrun_only"
STREAMING_DRYRUN_ONLY = True
VIRTUAL_TEST_ONLY = True
EXISTING_GOVERNANCE_REUSE_REQUIRED = True
NEW_ADMISSION_CONTRACT_CREATED = False
NEW_RUNTIME_GOVERNANCE_CREATED = False
CONTROLLED_TRIAL_TEMPLATE_REUSED = True

P1_EXECUTION_DRYRUN_FOUNDATION_REF = "Phase-P1-Execution-DryRun-Foundation-v1-001"
P1_DOWNLOAD_LICENSE_PLANNING_REF = "Phase-Recognition-Model-P1-Download-License-Planning-v1-001"
RUNTIME_TRIAL_PLANNING_REF = "Phase-Model-Governance-Runtime-Trial-Planning-v1-001"
INTEGRATED_CLOSURE_POST_REVIEW_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-Post-Review-v1-001"
)
MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF = (
    "Phase-Recognition-Midplatform-Model-Governance-Integrated-Closure-v1-001"
)
TARGET_CHAIN_REF = "Phase-PhaseOne-Environment-Cognition-Evidence-Main-Chain-Closure-v1-001"
CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF = TEMPLATE_ID

NEXT_STEP_OPTIONS_REF = "p1_execution_trace_streaming_dryrun_post_review"

P1_EXECUTION_DRYRUN_FOUNDATION_EXPECTED_GO = "P1_EXECUTION_DRYRUN_FOUNDATION_GO"
TEST_BOARD_PROTOCOL_EXPECTED_GO = "TEST_BOARD_PROTECTED_ARTIFACT_RULE_GO"

# Test board binding
TEST_BOARD_MODULE = "runtime_trials"
TEST_BOARD_TEST_MODE = "dry_run"

# --------------------------------------------------------------------------- #
# Streaming config
# --------------------------------------------------------------------------- #
STREAMING_FRAME_COUNT = 8

# Execution graph (reused from foundation): 5 nodes, 4 edges, acyclic.
EXECUTION_GRAPH_NODES: Tuple[Dict[str, Any], ...] = (
    {"node_id": "segmentation", "order": 1, "deferred": False},
    {"node_id": "tracking", "order": 2, "deferred": False},
    {"node_id": "detection", "order": 3, "deferred": False},
    {"node_id": "depth", "order": 4, "deferred": False},
    {"node_id": "scene_relation", "order": 5, "deferred": True},
)
EXECUTION_GRAPH_EDGES: Tuple[Dict[str, str], ...] = (
    {"src": "segmentation", "dst": "tracking"},
    {"src": "tracking", "dst": "detection"},
    {"src": "detection", "dst": "depth"},
    {"src": "depth", "dst": "scene_relation"},
)

# Model node states (carried from foundation).
STREAMING_MODEL_NODES: Tuple[Dict[str, str], ...] = (
    {"model_id": "mobile_sam", "graph_node": "segmentation", "state": "STATE_A_runnable"},
    {"model_id": "fast_sam", "graph_node": "segmentation", "state": "STATE_B_partial"},
    {"model_id": "byte_track", "graph_node": "tracking", "state": "STATE_A_runnable"},
    {"model_id": "deep_sort", "graph_node": "tracking", "state": "STATE_A_runnable"},
    {"model_id": "yolov8n", "graph_node": "detection", "state": "STATE_A_runnable"},
    {"model_id": "rt_detr", "graph_node": "detection", "state": "STATE_B_partial"},
    {"model_id": "midas", "graph_node": "depth", "state": "STATE_A_runnable"},
    {"model_id": "depth_anything", "graph_node": "depth", "state": "STATE_B_partial"},
    {"model_id": "scene_relation_vlm", "graph_node": "scene_relation", "state": "STATE_D_deferred"},
    {"model_id": "open_vocab_vlm", "graph_node": "scene_relation", "state": "STATE_D_deferred"},
)

# --------------------------------------------------------------------------- #
# Consistency thresholds (suggested)
# --------------------------------------------------------------------------- #
CONSISTENCY_THRESHOLDS: Dict[str, float] = {
    "max_region_jitter_score": 0.25,
    "max_bbox_jitter_score": 0.30,
    "max_confidence_delta": 0.35,
    "max_track_switch_count": 1,
    "max_temporal_gap_count": 1,
    "max_depth_band_switch_count": 1,
}

# --------------------------------------------------------------------------- #
# Temporal candidate families + simulated (mock) per-family temporal metrics.
# Values chosen to stay within thresholds (structure-level mock, no inference).
# --------------------------------------------------------------------------- #
TEMPORAL_CANDIDATE_FAMILIES: Tuple[Dict[str, Any], ...] = (
    {
        "candidate_type": "region_candidate",
        "source_family": "segmentation",
        "metrics": {
            "region_persistence": "high",
            "boundary_jitter": 0.15,
            "region_confidence_delta": 0.10,
        },
        "deferred": False,
    },
    {
        "candidate_type": "track_candidate",
        "source_family": "tracking",
        "metrics": {
            "track_id_persistence": "high",
            "track_switch_count": 1,
            "temporal_gap_count": 0,
        },
        "deferred": False,
    },
    {
        "candidate_type": "object_candidate",
        "source_family": "detection",
        "metrics": {
            "object_presence_consistency": "high",
            "bbox_jitter": 0.20,
            "detection_confidence_delta": 0.18,
        },
        "deferred": False,
    },
    {
        "candidate_type": "spatial_hint_candidate",
        "source_family": "depth",
        "metrics": {
            "distance_band_stability": "high",
            "depth_uncertainty_delta": 0.12,
            "depth_band_switch_count": 1,
        },
        "deferred": False,
    },
    {
        "candidate_type": "scene_relation_candidate",
        "source_family": "scene_relation",
        "metrics": {
            "deferred_only": True,
            "no_runtime_execution": True,
            "no_semantic_promotion": True,
        },
        "deferred": True,
    },
)

# --------------------------------------------------------------------------- #
# Cross-frame consistency checks (7)
# --------------------------------------------------------------------------- #
CROSS_FRAME_CONSISTENCY_CHECKS: Tuple[Dict[str, Any], ...] = (
    {"check_id": "same_object_trackable_across_frames", "metric": "track_switch_count", "limit_key": "max_track_switch_count", "value": 1},
    {"check_id": "segmentation_region_within_jitter_threshold", "metric": "boundary_jitter", "limit_key": "max_region_jitter_score", "value": 0.15},
    {"check_id": "object_detection_presence_stable", "metric": "bbox_jitter", "limit_key": "max_bbox_jitter_score", "value": 0.20},
    {"check_id": "depth_distance_band_no_excessive_oscillation", "metric": "depth_band_switch_count", "limit_key": "max_depth_band_switch_count", "value": 1},
    {"check_id": "tracking_no_excessive_id_switches", "metric": "track_switch_count", "limit_key": "max_track_switch_count", "value": 1},
    {"check_id": "unavailable_deferred_models_not_blockers", "metric": "confidence_delta", "limit_key": "max_confidence_delta", "value": 0.0},
    {"check_id": "candidate_lifecycle_remains_candidate_only", "metric": "confidence_delta", "limit_key": "max_confidence_delta", "value": 0.0},
)

# --------------------------------------------------------------------------- #
# Cross-model temporal agreements (5)
# --------------------------------------------------------------------------- #
CROSS_MODEL_TEMPORAL_AGREEMENTS: Tuple[Dict[str, str], ...] = (
    {
        "pair": "segmentation_x_detection",
        "rule": "object_bbox_should_overlap_stable_region_candidate",
        "output_candidate": "object_region_temporal_alignment_candidate",
    },
    {
        "pair": "detection_x_tracking",
        "rule": "detected_object_should_preserve_track_id_across_frames",
        "output_candidate": "object_track_temporal_alignment_candidate",
    },
    {
        "pair": "tracking_x_depth",
        "rule": "moving_track_should_preserve_plausible_distance_trend",
        "output_candidate": "motion_distance_temporal_consistency_candidate",
    },
    {
        "pair": "detection_x_depth",
        "rule": "object_candidate_should_have_stable_spatial_hint_band",
        "output_candidate": "object_depth_temporal_alignment_candidate",
    },
    {
        "pair": "fallback_x_model_availability",
        "rule": "unavailable_partial_deferred_models_produce_fallback_or_disabled_path",
        "output_candidate": "model_availability_temporal_context_candidate",
    },
)

# --------------------------------------------------------------------------- #
# Drift signals (5)
# --------------------------------------------------------------------------- #
DRIFT_SIGNALS: Tuple[Dict[str, Any], ...] = (
    {"signal_id": "boundary_jitter_drift", "metric": "boundary_jitter", "value": 0.15, "limit_key": "max_region_jitter_score"},
    {"signal_id": "bbox_jitter_drift", "metric": "bbox_jitter", "value": 0.20, "limit_key": "max_bbox_jitter_score"},
    {"signal_id": "track_switch_drift", "metric": "track_switch_count", "value": 1, "limit_key": "max_track_switch_count"},
    {"signal_id": "depth_band_switch_drift", "metric": "depth_band_switch_count", "value": 1, "limit_key": "max_depth_band_switch_count"},
    {"signal_id": "confidence_delta_drift", "metric": "detection_confidence_delta", "value": 0.18, "limit_key": "max_confidence_delta"},
)

# --------------------------------------------------------------------------- #
# Uncertainty smoothing records (5)
# --------------------------------------------------------------------------- #
UNCERTAINTY_SMOOTHING_TARGETS: Tuple[Dict[str, Any], ...] = (
    {"candidate_type": "region_candidate", "smoothing": "temporal_confidence_smoothing", "deferred": False},
    {"candidate_type": "object_candidate", "smoothing": "temporal_confidence_smoothing", "deferred": False},
    {"candidate_type": "spatial_hint_candidate", "smoothing": "depth_uncertainty_smoothing", "deferred": False},
    {"candidate_type": "track_candidate", "smoothing": "track_gap_smoothing", "deferred": False},
    {"candidate_type": "scene_relation_candidate", "smoothing": "no_smoothing_deferred_only", "deferred": True},
)

# --------------------------------------------------------------------------- #
# Conflict evolution records (4)
# --------------------------------------------------------------------------- #
CONFLICT_EVOLUTION_TARGETS: Tuple[Dict[str, str], ...] = (
    {"conflict_id": "segmentation_vs_detection_region", "resolution": "candidate_alignment_recorded"},
    {"conflict_id": "detection_vs_tracking_id", "resolution": "candidate_track_alignment_recorded"},
    {"conflict_id": "tracking_vs_depth_motion", "resolution": "candidate_motion_consistency_recorded"},
    {"conflict_id": "detection_vs_depth_band", "resolution": "candidate_depth_alignment_recorded"},
)

# --------------------------------------------------------------------------- #
# Streaming fallback events (5)
# --------------------------------------------------------------------------- #
STREAMING_FALLBACK_EVENTS: Tuple[Dict[str, str], ...] = (
    {"event_id": "fastsam_partial", "fallback_route": "fallback_to_mobile_sam_preferred_path", "record": "partial_state_record_only"},
    {"event_id": "rt_detr_partial", "fallback_route": "fallback_to_yolov8n_test_only_local_path", "record": "no_commercial_runtime_approval"},
    {"event_id": "depth_anything_partial", "fallback_route": "fallback_to_midas_light_path", "record": "partial_state_record_only"},
    {"event_id": "vlm_deferred", "fallback_route": "scene_relation_disabled_path", "record": "no_semantic_promotion_no_runtime_execution"},
    {"event_id": "model_unavailable_in_frame", "fallback_route": "output_availability_context_candidate", "record": "not_a_blocker_unless_required_fallback_missing"},
)

# --------------------------------------------------------------------------- #
# Midplatform stream governance records (10)
# --------------------------------------------------------------------------- #
MIDPLATFORM_STREAM_GOVERNANCE_RECORDS: Tuple[str, ...] = (
    "candidate_lifecycle_over_time",
    "confidence_smoothing",
    "uncertainty_smoothing",
    "conflict_evolution",
    "fallback_event_record",
    "degraded_path_record",
    "disabled_node_record",
    "output_blocking_record",
    "candidate_output_gate_record",
    "stream_trace_audit",
)

# --------------------------------------------------------------------------- #
# Negative guards (14: A..N) — id -> (go_key, depends_on invariant)
# --------------------------------------------------------------------------- #
NEGATIVE_GUARDS: Tuple[Dict[str, str], ...] = (
    {"guard_id": "invalid_a_streaming_real_inference", "go_key": "no_real_inference", "depends_on": "real_inference_not_allowed"},
    {"guard_id": "invalid_b_model_download_or_dep_install", "go_key": "no_model_download_or_dependency_install", "depends_on": "download_install_not_allowed"},
    {"guard_id": "invalid_c_live_camera_sensor_continuous_runtime", "go_key": "no_live_camera_sensor_continuous_runtime", "depends_on": "live_continuous_not_allowed"},
    {"guard_id": "invalid_d_candidate_stability_as_fact", "go_key": "no_candidate_stability_fact_admission", "depends_on": "temporal_stability_not_fact"},
    {"guard_id": "invalid_e_cross_model_agreement_as_semantic", "go_key": "no_cross_model_agreement_semantic_promotion", "depends_on": "cross_model_agreement_not_semantic"},
    {"guard_id": "invalid_f_guidance_as_runtime_navigation", "go_key": "no_guidance_runtime_navigation", "depends_on": "navigation_runtime_not_allowed"},
    {"guard_id": "invalid_g_speech_gate_triggers_tts", "go_key": "no_speech_tts", "depends_on": "speech_runtime_not_allowed"},
    {"guard_id": "invalid_h_action_safety_triggers_action", "go_key": "no_action_runtime", "depends_on": "action_runtime_not_allowed"},
    {"guard_id": "invalid_i_vla_action_chain_injected", "go_key": "no_vla_action_chain", "depends_on": "vla_action_chain_not_allowed"},
    {"guard_id": "invalid_j_reserved_deferred_vlm_executed", "go_key": "no_reserved_deferred_vlm_execution", "depends_on": "reserved_deferred_not_executed"},
    {"guard_id": "invalid_k_commercial_runtime_approved", "go_key": "no_commercial_runtime", "depends_on": "commercial_runtime_not_approved"},
    {"guard_id": "invalid_l_test_record_not_written_to_board", "go_key": "test_board_record_required_enforced", "depends_on": "test_board_record_required_true"},
    {"guard_id": "invalid_m_test_artifact_not_protected", "go_key": "test_board_protected_marking_enforced", "depends_on": "test_board_protected_non_deletable_true"},
    {"guard_id": "invalid_n_cleanup_allows_test_board_deletion", "go_key": "cleanup_must_not_delete_test_board", "depends_on": "cleanup_does_not_delete_test_board"},
)

# --------------------------------------------------------------------------- #
# Governance rules (phase 30 + test board 6, appended)
# --------------------------------------------------------------------------- #
STREAMING_PHASE_GOVERNANCE_RULES: Tuple[str, ...] = (
    "this_phase_is_streaming_dry_run_only",
    "streaming_trace_is_virtual_test_not_runtime",
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
    "midplatform_model_data_handling_is_required",
    "midplatform_model_control_is_required",
    "recognition_model_output_adapter_is_required",
    "test_board_record_is_required",
    "test_process_record_is_required",
    "test_conclusion_record_is_required",
    "test_artifacts_are_protected",
    "test_records_are_non_deletable",
    "cleanup_must_not_delete_test_board_artifacts",
)

ALL_GOVERNANCE_RULES: Tuple[str, ...] = (
    STREAMING_PHASE_GOVERNANCE_RULES + TEST_BOARD_GOVERNANCE_RULES
)

REQUIRED_TEST_BOARD_FIELDS_LOCAL: Dict[str, bool] = dict(REQUIRED_TEST_BOARD_FIELDS)

DRYRUN_OBJECT_TYPES: Tuple[str, ...] = (
    "StreamingExecutionProfile",
    "StreamingFrame",
    "StreamingModelNodeTrace",
    "TemporalCandidateSnapshot",
    "TemporalCandidateEvolution",
    "CrossFrameConsistencyCheck",
    "CrossModelTemporalAgreement",
    "DriftSignal",
    "UncertaintySmoothingRecord",
    "ConflictEvolutionRecord",
    "StreamingFallbackEvent",
    "StreamingControlDecision",
    "MidplatformStreamGovernanceRecord",
    "StreamingTraceAuditRecord",
    "P1ExecutionTraceStreamingDryRunDecision",
)

HANDOFF_READINESS_TARGETS: Tuple[Dict[str, str], ...] = (
    {
        "target_ref": "Phase-P1-Execution-Trace-Streaming-DryRun-Post-Review-v1-001",
        "go_key": "p1_execution_trace_streaming_dryrun_post_review_readiness_recorded",
    },
)

FINAL_DECISION_GO = "P1_EXECUTION_TRACE_STREAMING_DRYRUN_GO"
FINAL_DECISION_BLOCKED = "P1_EXECUTION_TRACE_STREAMING_DRYRUN_BLOCKED"

REUSE_FLAGS: Dict[str, bool] = {
    "existing_governance_reuse_required": True,
    "controlled_trial_template_reused": True,
    "test_board_protocol_reused": True,
}

NEGATED_CREATION_FLAGS: Dict[str, bool] = {
    "new_admission_contract_created": False,
    "new_runtime_governance_created": False,
}

DRYRUN_TRUE_INVARIANTS: Dict[str, bool] = {
    "streaming_execution_graph_built": True,
    "frame_trace_generated": True,
    "temporal_candidate_evolution_verified": True,
    "cross_frame_consistency_verified": True,
    "cross_model_temporal_agreement_verified": True,
    "midplatform_stream_governance_verified": True,
    "fallback_events_verified": True,
    "deferred_nodes_not_executed": True,
    "reserved_only_not_executed": True,
    "candidate_only_boundary_preserved": True,
    "temporal_stability_not_fact_admission": True,
    "cross_model_agreement_not_semantic_promotion": True,
    "model_output_adapter_required": True,
    "midplatform_data_handling_required": True,
    "midplatform_model_control_required": True,
    "governance_reuse_preserved": True,
    "luna_emotion_multimodal_brain_first_preserved": True,
}

NON_EXECUTION_FLAGS: Dict[str, bool] = {
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
class StreamingExecutionProfile:
    profile_ref: str
    phase_id: str
    dryrun_mode: str
    streaming_dryrun_only: bool
    virtual_test_only: bool
    existing_governance_reuse_required: bool
    new_admission_contract_created: bool
    new_runtime_governance_created: bool
    controlled_trial_template_reused: bool
    p1_execution_dryrun_foundation_ref: str
    model_governance_integrated_closure_ref: str
    target_chain_ref: str
    controlled_trial_governance_template_ref: str
    luna_core_principle: str
    frame_count: int
    consistency_thresholds: Dict[str, float]
    required_test_board_fields: Dict[str, bool]
    governance_rules: Tuple[str, ...]


@dataclass(frozen=True)
class StreamingFrame:
    frame_id: str
    timestamp_index: int
    active_model_nodes: Tuple[str, ...]
    simulated_candidate_outputs: Tuple[str, ...]
    unavailable_nodes: Tuple[str, ...]
    deferred_nodes: Tuple[str, ...]
    fallback_events: Tuple[str, ...]
    control_decisions: Tuple[str, ...]
    source_chain: str
    trace_ref: str


@dataclass(frozen=True)
class StreamingModelNodeTrace:
    frame_id: str
    timestamp_index: int
    model_id: str
    graph_node: str
    state: str
    executed_real_inference: bool
    downloaded_model: bool
    deferred_not_executed: bool


@dataclass(frozen=True)
class TemporalCandidateSnapshot:
    frame_id: str
    timestamp_index: int
    candidate_type: str
    source_family: str
    candidate_only: bool
    deferred: bool


@dataclass(frozen=True)
class TemporalCandidateEvolution:
    candidate_type: str
    source_family: str
    metrics: Dict[str, Any]
    within_thresholds: bool
    deferred: bool
    fact_admission: bool
    semantic_promotion: bool


@dataclass(frozen=True)
class CrossFrameConsistencyCheck:
    check_id: str
    metric: str
    limit_key: str
    value: float
    limit: float
    passed: bool


@dataclass(frozen=True)
class CrossModelTemporalAgreement:
    pair: str
    rule: str
    output_candidate: str
    candidate_only: bool
    semantic_promotion: bool
    fact_admission: bool


@dataclass(frozen=True)
class DriftSignal:
    signal_id: str
    metric: str
    value: float
    limit: float
    within_threshold: bool


@dataclass(frozen=True)
class UncertaintySmoothingRecord:
    candidate_type: str
    smoothing: str
    candidate_only: bool
    fact_admission: bool
    deferred: bool


@dataclass(frozen=True)
class ConflictEvolutionRecord:
    conflict_id: str
    resolution: str
    candidate_only: bool
    conflict_is_fact: bool


@dataclass(frozen=True)
class StreamingFallbackEvent:
    event_id: str
    fallback_route: str
    record: str
    candidate_only: bool
    triggers_download_or_inference: bool


@dataclass(frozen=True)
class StreamingControlDecision:
    frame_id: str
    decision: str
    candidate_only: bool
    blocks_non_candidate_output: bool


@dataclass(frozen=True)
class MidplatformStreamGovernanceRecord:
    record_type: str
    midplatform_data_handling_required: bool
    midplatform_model_control_required: bool
    recognition_model_output_adapter_required: bool
    candidate_only: bool


@dataclass(frozen=True)
class StreamingTraceAuditRecord:
    audit_ref: str
    frame_count: int
    candidate_only: bool
    written_to_test_board: bool
    protected: bool
    non_deletable: bool


@dataclass
class StreamingNegativeGuard:
    guard_id: str
    go_key: str
    depends_on: str
    passed: bool
    notes: Tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class StreamingHandoffReadiness:
    target_ref: str
    readiness_recorded: bool
    entered_this_phase: bool


@dataclass(frozen=True)
class P1ExecutionTraceStreamingDryRunDecision:
    decision_ref: str
    streaming_profile_count: int
    streaming_frame_count: int
    streaming_model_node_trace_count: int
    temporal_candidate_snapshot_count: int
    temporal_candidate_evolution_count: int
    cross_frame_consistency_check_count: int
    cross_model_temporal_agreement_count: int
    drift_signal_count: int
    uncertainty_smoothing_record_count: int
    conflict_evolution_record_count: int
    streaming_fallback_event_count: int
    streaming_control_decision_count: int
    midplatform_stream_governance_record_count: int
    negative_guard_count: int
    negative_guard_passed: int
    test_board_record_count: int
    blocker_count: int
    final_decision: str


def candidate_to_dict(obj: Any) -> Dict[str, Any]:
    return asdict(obj)
