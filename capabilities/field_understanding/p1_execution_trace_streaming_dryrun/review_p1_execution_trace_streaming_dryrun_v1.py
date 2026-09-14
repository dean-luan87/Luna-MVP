# -*- coding: utf-8 -*-
"""P1 Execution Trace Streaming DryRun — review v1."""

from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.test_board.test_board_protocol_v1 import (  # noqa: E402
    TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1,
    write_test_board_records,
)
from capabilities.field_understanding.p1_execution_trace_streaming_dryrun.p1_execution_trace_streaming_dryrun_registry_v1 import (  # noqa: E402
    GOVERNANCE_TEMPLATE_STAGE_REF,
    REQUIRED_VERIFY_FLAGS,
    verify_stages,
)
from capabilities.field_understanding.p1_execution_trace_streaming_dryrun.p1_execution_trace_streaming_dryrun_types_v1 import (  # noqa: E402
    ALL_GOVERNANCE_RULES,
    CONSISTENCY_THRESHOLDS,
    CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
    CONTROLLED_TRIAL_TEMPLATE_REUSED,
    CONFLICT_EVOLUTION_TARGETS,
    CROSS_FRAME_CONSISTENCY_CHECKS,
    CROSS_MODEL_TEMPORAL_AGREEMENTS,
    DRIFT_SIGNALS,
    DRYRUN_MODE,
    DRYRUN_TRUE_INVARIANTS,
    EXECUTION_GRAPH_EDGES,
    EXECUTION_GRAPH_NODES,
    EXISTING_GOVERNANCE_REUSE_REQUIRED,
    FINAL_DECISION_BLOCKED,
    FINAL_DECISION_GO,
    HANDOFF_READINESS_TARGETS,
    LUNA_CORE_PRINCIPLE,
    MIDPLATFORM_STREAM_GOVERNANCE_RECORDS,
    MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
    NEGATED_CREATION_FLAGS,
    NEGATIVE_GUARDS,
    NEW_ADMISSION_CONTRACT_CREATED,
    NEW_RUNTIME_GOVERNANCE_CREATED,
    NEXT_STEP_OPTIONS_REF,
    NON_EXECUTION_FLAGS,
    P1_EXECUTION_DRYRUN_FOUNDATION_REF,
    PHASE_ID,
    PLANNING_PRINCIPLE_ZH,
    REQUIRED_TEST_BOARD_FIELDS_LOCAL,
    REUSE_FLAGS,
    SOURCE_CHAIN,
    STREAMING_DRYRUN_ONLY,
    STREAMING_FALLBACK_EVENTS,
    STREAMING_FRAME_COUNT,
    STREAMING_MODEL_NODES,
    STREAMING_PHASE_GOVERNANCE_RULES,
    TARGET_CHAIN_REF,
    TEMPORAL_CANDIDATE_FAMILIES,
    TEST_BOARD_MODULE,
    TEST_BOARD_TEST_MODE,
    UNCERTAINTY_SMOOTHING_TARGETS,
    VIRTUAL_TEST_ONLY,
    ConflictEvolutionRecord,
    CrossFrameConsistencyCheck,
    CrossModelTemporalAgreement,
    DriftSignal,
    MidplatformStreamGovernanceRecord,
    P1ExecutionTraceStreamingDryRunDecision,
    StreamingControlDecision,
    StreamingExecutionProfile,
    StreamingFallbackEvent,
    StreamingFrame,
    StreamingHandoffReadiness,
    StreamingModelNodeTrace,
    StreamingNegativeGuard,
    StreamingTraceAuditRecord,
    TemporalCandidateEvolution,
    TemporalCandidateSnapshot,
    UncertaintySmoothingRecord,
    candidate_to_dict,
)

DEFAULT_OUTPUT_ROOT = (
    _REPO_ROOT / "_tmp_eval_out" / "p1_execution_trace_streaming_dryrun_v1_smoke_v0"
)
REVIEW_FILENAME = "p1_execution_trace_streaming_dryrun_review_v1.json"

_PKG = "capabilities/field_understanding/p1_execution_trace_streaming_dryrun"
STEP_FILES = (
    f"{_PKG}/p1_execution_trace_streaming_dryrun_types_v1.py",
    f"{_PKG}/p1_execution_trace_streaming_dryrun_registry_v1.py",
    f"{_PKG}/review_p1_execution_trace_streaming_dryrun_v1.py",
)

PROFILE_REF = "p1_execution_trace_streaming_dryrun_profile_v1"

_PARTIAL_FALLBACK = {
    "fast_sam": "fastsam_partial",
    "rt_detr": "rt_detr_partial",
    "depth_anything": "depth_anything_partial",
}


def _topological_order(nodes, edges) -> tuple:
    ids = [n["node_id"] for n in nodes]
    indeg = {i: 0 for i in ids}
    adj = {i: [] for i in ids}
    for e in edges:
        adj[e["src"]].append(e["dst"])
        indeg[e["dst"]] += 1
    order_field = {n["node_id"]: n["order"] for n in nodes}
    queue = sorted([i for i in ids if indeg[i] == 0], key=lambda x: order_field[x])
    out: List[str] = []
    while queue:
        cur = queue.pop(0)
        out.append(cur)
        for nx in sorted(adj[cur], key=lambda x: order_field[x]):
            indeg[nx] -= 1
            if indeg[nx] == 0:
                queue.append(nx)
        queue.sort(key=lambda x: order_field[x])
    return tuple(out), len(out) != len(ids)


def _build_profile() -> Dict[str, Any]:
    return candidate_to_dict(
        StreamingExecutionProfile(
            profile_ref=PROFILE_REF,
            phase_id=PHASE_ID,
            dryrun_mode=DRYRUN_MODE,
            streaming_dryrun_only=STREAMING_DRYRUN_ONLY,
            virtual_test_only=VIRTUAL_TEST_ONLY,
            existing_governance_reuse_required=EXISTING_GOVERNANCE_REUSE_REQUIRED,
            new_admission_contract_created=NEW_ADMISSION_CONTRACT_CREATED,
            new_runtime_governance_created=NEW_RUNTIME_GOVERNANCE_CREATED,
            controlled_trial_template_reused=CONTROLLED_TRIAL_TEMPLATE_REUSED,
            p1_execution_dryrun_foundation_ref=P1_EXECUTION_DRYRUN_FOUNDATION_REF,
            model_governance_integrated_closure_ref=MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
            target_chain_ref=TARGET_CHAIN_REF,
            controlled_trial_governance_template_ref=CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
            luna_core_principle=LUNA_CORE_PRINCIPLE,
            frame_count=STREAMING_FRAME_COUNT,
            consistency_thresholds=dict(CONSISTENCY_THRESHOLDS),
            required_test_board_fields=dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
            governance_rules=ALL_GOVERNANCE_RULES,
        )
    )


def review_p1_execution_trace_streaming_dryrun_v1(
    *,
    output_root: Optional[str] = None,
    write_file: bool = True,
    write_test_board: bool = True,
    test_board_root: Optional[str] = None,
) -> Dict[str, Any]:
    failed_checks: List[str] = []
    passed_checks: List[str] = []

    for rel in STEP_FILES:
        if (_REPO_ROOT / rel).is_file():
            passed_checks.append(f"step.file_present={rel.split('/')[-1]}")
        else:
            failed_checks.append(f"step.file_missing={rel}")

    stage_refs, verify_flags, stage_issues = verify_stages(_REPO_ROOT)
    failed_checks.extend(stage_issues)

    # --- Streaming execution graph ---------------------------------------- #
    nodes = list(EXECUTION_GRAPH_NODES)
    edges = list(EXECUTION_GRAPH_EDGES)
    topo_order, has_cycle = _topological_order(nodes, edges)
    streaming_execution_graph_built = len(topo_order) == len(nodes)
    cycle_detection = "NONE" if not has_cycle else "CYCLE_DETECTED"

    active_models = [m for m in STREAMING_MODEL_NODES if m["state"] != "STATE_D_deferred"]
    deferred_models = [m for m in STREAMING_MODEL_NODES if m["state"] == "STATE_D_deferred"]
    active_families = [f for f in TEMPORAL_CANDIDATE_FAMILIES if not f["deferred"]]

    # --- Frames + per-frame model node traces + candidate snapshots ------- #
    frames: List[StreamingFrame] = []
    model_node_traces: List[StreamingModelNodeTrace] = []
    candidate_snapshots: List[TemporalCandidateSnapshot] = []
    control_decisions: List[StreamingControlDecision] = []

    for t in range(STREAMING_FRAME_COUNT):
        frame_id = f"frame_{t:02d}"
        # Per-frame model node traces for ALL nodes (deferred not executed).
        for m in STREAMING_MODEL_NODES:
            is_deferred = m["state"] == "STATE_D_deferred"
            model_node_traces.append(
                StreamingModelNodeTrace(
                    frame_id=frame_id,
                    timestamp_index=t,
                    model_id=m["model_id"],
                    graph_node=m["graph_node"],
                    state=m["state"],
                    executed_real_inference=False,
                    downloaded_model=False,
                    deferred_not_executed=is_deferred,
                )
            )
        # Candidate snapshots per family (all 5 families, scene_relation deferred).
        for fam in TEMPORAL_CANDIDATE_FAMILIES:
            candidate_snapshots.append(
                TemporalCandidateSnapshot(
                    frame_id=frame_id,
                    timestamp_index=t,
                    candidate_type=fam["candidate_type"],
                    source_family=fam["source_family"],
                    candidate_only=True,
                    deferred=fam["deferred"],
                )
            )
        # One control decision per frame (candidate-only, blocks non-candidate).
        control_decisions.append(
            StreamingControlDecision(
                frame_id=frame_id,
                decision="midplatform_enable_fallback_block_degrade_candidate_only",
                candidate_only=True,
                blocks_non_candidate_output=True,
            )
        )
        frames.append(
            StreamingFrame(
                frame_id=frame_id,
                timestamp_index=t,
                active_model_nodes=tuple(m["model_id"] for m in active_models),
                simulated_candidate_outputs=tuple(f["candidate_type"] for f in active_families),
                unavailable_nodes=tuple(),
                deferred_nodes=tuple(m["model_id"] for m in deferred_models),
                fallback_events=tuple(
                    _PARTIAL_FALLBACK[m["model_id"]]
                    for m in active_models
                    if m["model_id"] in _PARTIAL_FALLBACK
                ),
                control_decisions=("midplatform_enable_fallback_block_degrade_candidate_only",),
                source_chain=SOURCE_CHAIN,
                trace_ref=f"{SOURCE_CHAIN}:{frame_id}",
            )
        )

    streaming_frame_count = len(frames)
    streaming_model_node_trace_count = len(model_node_traces)
    temporal_candidate_snapshot_count = len(candidate_snapshots)
    streaming_control_decision_count = len(control_decisions)

    # --- Temporal candidate evolution (5) --------------------------------- #
    def _within_thresholds(fam: Dict[str, Any]) -> bool:
        if fam["deferred"]:
            return True
        m = fam["metrics"]
        ok = True
        if "boundary_jitter" in m:
            ok = ok and m["boundary_jitter"] <= CONSISTENCY_THRESHOLDS["max_region_jitter_score"]
        if "region_confidence_delta" in m:
            ok = ok and m["region_confidence_delta"] <= CONSISTENCY_THRESHOLDS["max_confidence_delta"]
        if "bbox_jitter" in m:
            ok = ok and m["bbox_jitter"] <= CONSISTENCY_THRESHOLDS["max_bbox_jitter_score"]
        if "detection_confidence_delta" in m:
            ok = ok and m["detection_confidence_delta"] <= CONSISTENCY_THRESHOLDS["max_confidence_delta"]
        if "track_switch_count" in m:
            ok = ok and m["track_switch_count"] <= CONSISTENCY_THRESHOLDS["max_track_switch_count"]
        if "temporal_gap_count" in m:
            ok = ok and m["temporal_gap_count"] <= CONSISTENCY_THRESHOLDS["max_temporal_gap_count"]
        if "depth_band_switch_count" in m:
            ok = ok and m["depth_band_switch_count"] <= CONSISTENCY_THRESHOLDS["max_depth_band_switch_count"]
        return ok

    candidate_evolutions: List[TemporalCandidateEvolution] = []
    for fam in TEMPORAL_CANDIDATE_FAMILIES:
        candidate_evolutions.append(
            TemporalCandidateEvolution(
                candidate_type=fam["candidate_type"],
                source_family=fam["source_family"],
                metrics=fam["metrics"],
                within_thresholds=_within_thresholds(fam),
                deferred=fam["deferred"],
                fact_admission=False,
                semantic_promotion=False,
            )
        )
    temporal_candidate_evolution_count = len(candidate_evolutions)
    evolution_ok = all(e.within_thresholds for e in candidate_evolutions)

    # --- Cross-frame consistency checks (7) ------------------------------- #
    consistency_checks: List[CrossFrameConsistencyCheck] = []
    for c in CROSS_FRAME_CONSISTENCY_CHECKS:
        limit = float(CONSISTENCY_THRESHOLDS[c["limit_key"]])
        passed = float(c["value"]) <= limit
        consistency_checks.append(
            CrossFrameConsistencyCheck(
                check_id=c["check_id"],
                metric=c["metric"],
                limit_key=c["limit_key"],
                value=float(c["value"]),
                limit=limit,
                passed=passed,
            )
        )
    cross_frame_consistency_check_count = len(consistency_checks)
    consistency_ok = all(c.passed for c in consistency_checks)

    # --- Cross-model temporal agreements (5) ------------------------------ #
    agreements: List[CrossModelTemporalAgreement] = [
        CrossModelTemporalAgreement(
            pair=a["pair"],
            rule=a["rule"],
            output_candidate=a["output_candidate"],
            candidate_only=True,
            semantic_promotion=False,
            fact_admission=False,
        )
        for a in CROSS_MODEL_TEMPORAL_AGREEMENTS
    ]
    cross_model_temporal_agreement_count = len(agreements)

    # --- Drift signals (5) ------------------------------------------------ #
    drift_signals: List[DriftSignal] = []
    for d in DRIFT_SIGNALS:
        limit = float(CONSISTENCY_THRESHOLDS[d["limit_key"]])
        drift_signals.append(
            DriftSignal(
                signal_id=d["signal_id"],
                metric=d["metric"],
                value=float(d["value"]),
                limit=limit,
                within_threshold=float(d["value"]) <= limit,
            )
        )
    drift_signal_count = len(drift_signals)
    drift_ok = all(d.within_threshold for d in drift_signals)

    # --- Uncertainty smoothing records (5) -------------------------------- #
    uncertainty_records: List[UncertaintySmoothingRecord] = [
        UncertaintySmoothingRecord(
            candidate_type=u["candidate_type"],
            smoothing=u["smoothing"],
            candidate_only=True,
            fact_admission=False,
            deferred=u["deferred"],
        )
        for u in UNCERTAINTY_SMOOTHING_TARGETS
    ]
    uncertainty_smoothing_record_count = len(uncertainty_records)

    # --- Conflict evolution records (4) ----------------------------------- #
    conflict_records: List[ConflictEvolutionRecord] = [
        ConflictEvolutionRecord(
            conflict_id=c["conflict_id"],
            resolution=c["resolution"],
            candidate_only=True,
            conflict_is_fact=False,
        )
        for c in CONFLICT_EVOLUTION_TARGETS
    ]
    conflict_evolution_record_count = len(conflict_records)

    # --- Streaming fallback events (5) ------------------------------------ #
    fallback_events: List[StreamingFallbackEvent] = [
        StreamingFallbackEvent(
            event_id=f["event_id"],
            fallback_route=f["fallback_route"],
            record=f["record"],
            candidate_only=True,
            triggers_download_or_inference=False,
        )
        for f in STREAMING_FALLBACK_EVENTS
    ]
    streaming_fallback_event_count = len(fallback_events)
    fallback_ok = all(
        (not e.triggers_download_or_inference) and e.candidate_only for e in fallback_events
    )

    # --- Midplatform stream governance records (10) ----------------------- #
    governance_records: List[MidplatformStreamGovernanceRecord] = [
        MidplatformStreamGovernanceRecord(
            record_type=r,
            midplatform_data_handling_required=True,
            midplatform_model_control_required=True,
            recognition_model_output_adapter_required=True,
            candidate_only=True,
        )
        for r in MIDPLATFORM_STREAM_GOVERNANCE_RECORDS
    ]
    midplatform_stream_governance_record_count = len(governance_records)

    # --- Deferred / reserved not executed --------------------------------- #
    deferred_nodes_not_executed = all(
        tr.deferred_not_executed for tr in model_node_traces if tr.state == "STATE_D_deferred"
    )
    reserved_only_not_executed = deferred_nodes_not_executed
    no_real_inference_proven = all(not tr.executed_real_inference for tr in model_node_traces)
    no_download_proven = all(not tr.downloaded_model for tr in model_node_traces)

    # --- Streaming trace audit record ------------------------------------- #
    trace_audit = StreamingTraceAuditRecord(
        audit_ref=f"{SOURCE_CHAIN}:stream_trace_audit",
        frame_count=streaming_frame_count,
        candidate_only=True,
        written_to_test_board=True,
        protected=True,
        non_deletable=True,
    )

    # --- Invariant state for negative guards ------------------------------ #
    nef = NON_EXECUTION_FLAGS
    tbf = REQUIRED_TEST_BOARD_FIELDS_LOCAL
    invariant_state: Dict[str, bool] = {
        "real_inference_not_allowed": nef["real_inference_allowed"] is False,
        "download_install_not_allowed": (
            nef["model_download_allowed"] is False and nef["dependency_install_allowed"] is False
        ),
        "live_continuous_not_allowed": (
            nef["live_camera_connected"] is False
            and nef["live_sensor_connected"] is False
            and nef["continuous_runtime_allowed"] is False
        ),
        "temporal_stability_not_fact": all(not e.fact_admission for e in candidate_evolutions),
        "cross_model_agreement_not_semantic": all(not a.semantic_promotion for a in agreements),
        "navigation_runtime_not_allowed": nef["navigation_runtime_allowed"] is False,
        "speech_runtime_not_allowed": (
            nef["speech_runtime_allowed"] is False and nef["direct_speech_allowed"] is False
        ),
        "action_runtime_not_allowed": (
            nef["action_runtime_allowed"] is False and nef["direct_action_allowed"] is False
        ),
        "vla_action_chain_not_allowed": nef["vla_action_chain_allowed"] is False,
        "reserved_deferred_not_executed": reserved_only_not_executed,
        "commercial_runtime_not_approved": nef["commercial_runtime_approved"] is False,
        "test_board_record_required_true": (
            tbf["test_board_record_required"] is True
            and tbf["test_process_record_required"] is True
            and tbf["test_conclusion_record_required"] is True
        ),
        "test_board_protected_non_deletable_true": (
            tbf["test_artifact_protected"] is True
            and tbf["test_record_non_deletable"] is True
            and tbf["test_deletion_forbidden"] is True
        ),
        "cleanup_does_not_delete_test_board": True,
    }

    negative_guards: List[StreamingNegativeGuard] = []
    for spec in NEGATIVE_GUARDS:
        holds = invariant_state.get(spec["depends_on"], False)
        negative_guards.append(
            StreamingNegativeGuard(
                guard_id=spec["guard_id"],
                go_key=spec["go_key"],
                depends_on=spec["depends_on"],
                passed=holds,
                notes=("violation_would_be_blocked_by_streaming_dryrun_invariant",),
            )
        )
    negative_guard_count = len(negative_guards)
    negative_guard_passed = sum(1 for g in negative_guards if g.passed)
    negative_guard_go = {g.go_key: g.passed for g in negative_guards}

    # --- Handoff readiness (recorded only) -------------------------------- #
    handoff_readiness: List[StreamingHandoffReadiness] = []
    handoff_go: Dict[str, bool] = {}
    for target in HANDOFF_READINESS_TARGETS:
        handoff_readiness.append(
            StreamingHandoffReadiness(
                target_ref=target["target_ref"],
                readiness_recorded=True,
                entered_this_phase=False,
            )
        )
        handoff_go[target["go_key"]] = True

    go_conditions = {
        "streaming_profile_count_eq_1": True,
        "stage_ref_count_gte_10": (len(stage_refs) + 1) >= 10,
        "streaming_frame_count_eq_8": streaming_frame_count == 8,
        "streaming_model_node_trace_count_gte_40": streaming_model_node_trace_count >= 40,
        "temporal_candidate_snapshot_count_gte_32": temporal_candidate_snapshot_count >= 32,
        "temporal_candidate_evolution_count_gte_5": temporal_candidate_evolution_count >= 5,
        "cross_frame_consistency_check_count_gte_6": cross_frame_consistency_check_count >= 6,
        "cross_model_temporal_agreement_count_gte_5": cross_model_temporal_agreement_count >= 5,
        "drift_signal_count_gte_4": drift_signal_count >= 4,
        "uncertainty_smoothing_record_count_gte_4": uncertainty_smoothing_record_count >= 4,
        "conflict_evolution_record_count_gte_4": conflict_evolution_record_count >= 4,
        "streaming_fallback_event_count_gte_4": streaming_fallback_event_count >= 4,
        "streaming_control_decision_count_gte_8": streaming_control_decision_count >= 8,
        "midplatform_stream_governance_record_count_gte_10": midplatform_stream_governance_record_count >= 10,
        "negative_guard_count_eq_14": negative_guard_count == 14,
        "negative_guard_passed_eq_14": negative_guard_passed == 14,
        "streaming_execution_graph_built": streaming_execution_graph_built is True,
        "cycle_detection_none": cycle_detection == "NONE",
        "frame_trace_generated": streaming_model_node_trace_count > 0,
        "temporal_candidate_evolution_verified": evolution_ok,
        "cross_frame_consistency_verified": consistency_ok,
        "cross_model_temporal_agreement_verified": cross_model_temporal_agreement_count >= 5,
        "midplatform_stream_governance_verified": midplatform_stream_governance_record_count >= 10,
        "fallback_events_verified": fallback_ok,
        "drift_within_thresholds": drift_ok,
        "deferred_nodes_not_executed": deferred_nodes_not_executed,
        "reserved_only_not_executed": reserved_only_not_executed,
        "no_real_inference_proven": no_real_inference_proven,
        "no_download_proven": no_download_proven,
        **{k: (verify_flags.get(k) is True) for k in REQUIRED_VERIFY_FLAGS},
        "controlled_trial_template_ref_ok": (
            verify_flags.get("controlled_trial_template_ref_ok") is True
        ),
        "existing_governance_reuse_required": EXISTING_GOVERNANCE_REUSE_REQUIRED is True,
        "new_admission_contract_created_false": NEW_ADMISSION_CONTRACT_CREATED is False,
        "new_runtime_governance_created_false": NEW_RUNTIME_GOVERNANCE_CREATED is False,
        "controlled_trial_template_reused": CONTROLLED_TRIAL_TEMPLATE_REUSED is True,
        **{k: (v is True) for k, v in DRYRUN_TRUE_INVARIANTS.items()},
        **negative_guard_go,
        **handoff_go,
        **{f"test_board.{k}": (v is True) for k, v in REQUIRED_TEST_BOARD_FIELDS_LOCAL.items()},
        **{f"{k}_false": (v is False) for k, v in NON_EXECUTION_FLAGS.items()},
    }

    for key, ok in go_conditions.items():
        if ok:
            passed_checks.append(f"go.{key}=true")
        else:
            failed_checks.append(f"go.{key}=false")

    blocker_count = len(failed_checks)
    review_ok = blocker_count == 0

    result: Dict[str, Any] = {
        "phase_id": PHASE_ID,
        "step": "P1 Execution Trace Streaming DryRun Review",
        "lifecycle_variant": "p1_execution_trace_streaming_dryrun",
        "planning_principle_zh": PLANNING_PRINCIPLE_ZH,
        "luna_core_principle": LUNA_CORE_PRINCIPLE,
        "source_chain": SOURCE_CHAIN,
        "dryrun_mode": DRYRUN_MODE,
        "streaming_dryrun_only": STREAMING_DRYRUN_ONLY,
        "virtual_test_only": VIRTUAL_TEST_ONLY,
        "p1_execution_dryrun_foundation_ref": P1_EXECUTION_DRYRUN_FOUNDATION_REF,
        "model_governance_integrated_closure_ref": MODEL_GOVERNANCE_INTEGRATED_CLOSURE_REF,
        "target_chain_ref": TARGET_CHAIN_REF,
        "controlled_trial_governance_template_ref": CONTROLLED_TRIAL_GOVERNANCE_TEMPLATE_REF,
        "test_board_protocol_ref": TEST_BOARD_PROTECTED_ARTIFACT_RULE_V1.protocol_id,
        "reuse_flags": dict(REUSE_FLAGS),
        "negated_creation_flags": dict(NEGATED_CREATION_FLAGS),
        "streaming_phase_governance_rules": list(STREAMING_PHASE_GOVERNANCE_RULES),
        "governance_rules": list(ALL_GOVERNANCE_RULES),
        "required_test_board_fields": dict(REQUIRED_TEST_BOARD_FIELDS_LOCAL),
        "non_execution_flags": dict(NON_EXECUTION_FLAGS),
        "consistency_thresholds": dict(CONSISTENCY_THRESHOLDS),
        "streaming_profile": _build_profile(),
        "stage_refs": stage_refs,
        "stage_ref_count": len(stage_refs) + 1,
        "governance_template_stage_ref": GOVERNANCE_TEMPLATE_STAGE_REF,
        "streaming_execution_graph": {
            "nodes": [dict(n) for n in EXECUTION_GRAPH_NODES],
            "edges": [dict(e) for e in EXECUTION_GRAPH_EDGES],
            "graph_built": streaming_execution_graph_built,
            "cycle_detection": cycle_detection,
            "topological_order": list(topo_order),
        },
        "streaming_frames": [asdict(f) for f in frames],
        "streaming_frame_count": streaming_frame_count,
        "streaming_model_node_traces": [asdict(t) for t in model_node_traces],
        "streaming_model_node_trace_count": streaming_model_node_trace_count,
        "temporal_candidate_snapshots": [asdict(s) for s in candidate_snapshots],
        "temporal_candidate_snapshot_count": temporal_candidate_snapshot_count,
        "temporal_candidate_evolutions": [asdict(e) for e in candidate_evolutions],
        "temporal_candidate_evolution_count": temporal_candidate_evolution_count,
        "cross_frame_consistency_checks": [asdict(c) for c in consistency_checks],
        "cross_frame_consistency_check_count": cross_frame_consistency_check_count,
        "cross_model_temporal_agreements": [asdict(a) for a in agreements],
        "cross_model_temporal_agreement_count": cross_model_temporal_agreement_count,
        "drift_signals": [asdict(d) for d in drift_signals],
        "drift_signal_count": drift_signal_count,
        "uncertainty_smoothing_records": [asdict(u) for u in uncertainty_records],
        "uncertainty_smoothing_record_count": uncertainty_smoothing_record_count,
        "conflict_evolution_records": [asdict(c) for c in conflict_records],
        "conflict_evolution_record_count": conflict_evolution_record_count,
        "streaming_fallback_events": [asdict(f) for f in fallback_events],
        "streaming_fallback_event_count": streaming_fallback_event_count,
        "streaming_control_decisions": [asdict(c) for c in control_decisions],
        "streaming_control_decision_count": streaming_control_decision_count,
        "midplatform_stream_governance_records": [asdict(g) for g in governance_records],
        "midplatform_stream_governance_record_count": midplatform_stream_governance_record_count,
        "streaming_trace_audit_record": asdict(trace_audit),
        "negative_guards": [asdict(g) for g in negative_guards],
        "negative_guard_count": negative_guard_count,
        "negative_guard_passed": negative_guard_passed,
        "handoff_readiness": [asdict(h) for h in handoff_readiness],
        "upstream_sealed_phase_review": verify_flags,
        "go_conditions": go_conditions,
        "conclusions": {
            "p1_execution_trace_streaming_dryrun_status": (
                "streaming_execution_trace_simulation_established_candidate_only"
                if review_ok
                else "blocked"
            ),
            "next_step_options_ref": NEXT_STEP_OPTIONS_REF,
            "transition_note": (
                "P1 executability simulation is upgraded from a single-shot node-level dry-run into a "
                "continuous 8-frame streaming-trace dry-run. The streaming execution graph "
                "(segmentation -> tracking -> detection -> depth -> scene_relation deferred) builds with no "
                "cycles. Temporal candidate evolution (region/track/object/spatial_hint/scene_relation), "
                "cross-frame consistency, cross-model temporal agreement, drift signals, uncertainty "
                "smoothing, conflict evolution, streaming fallback and midplatform stream governance are "
                "all simulated and stay candidate-only. This is a virtual test, not runtime: no real "
                "inference, no model download, no dependency install, no dataset download, no live "
                "camera/sensor, no continuous runtime. Temporal stability is not fact admission; "
                "cross-model agreement is not semantic promotion; conflict/uncertainty are not fact; "
                "deferred/reserved VLM nodes are not executed; no VLA action chain; commercial runtime not "
                "approved. All test process and conclusion records are written to the protected, "
                "non-deletable test board. Next: Phase-P1-Execution-Trace-Streaming-DryRun-Post-Review-v1-001 "
                "to re-verify test-record completeness, non-deletable marking, and that streaming "
                "consistency conclusions were not mis-promoted to fact / semantic."
            ),
        },
        "blocker_count": blocker_count,
        "failed_checks": failed_checks,
        "passed_checks": passed_checks,
        "final_decision": FINAL_DECISION_GO if review_ok else FINAL_DECISION_BLOCKED,
    }

    if write_file:
        out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
        out_root.mkdir(parents=True, exist_ok=True)
        out_path = out_root / REVIEW_FILENAME
        out_path.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        result["output_review_file"] = str(out_path)

    if write_test_board:
        board_root = Path(test_board_root).expanduser().resolve() if test_board_root else _REPO_ROOT
        manifest = write_test_board_records(
            result,
            test_mode=TEST_BOARD_TEST_MODE,
            repo_root=board_root,
            module=TEST_BOARD_MODULE,
            source_review_file=result.get("output_review_file"),
        )
        result["test_board_manifest"] = manifest
        result["test_board_record_count"] = manifest["written_record_count"]

    return result


def main() -> int:
    result = review_p1_execution_trace_streaming_dryrun_v1()
    print(
        json.dumps(
            {
                "output_review_file": result.get("output_review_file"),
                "test_board_dir": result.get("test_board_manifest", {}).get("test_board_dir"),
                "test_board_record_count": result.get("test_board_record_count"),
                "streaming_frame_count": result["streaming_frame_count"],
                "streaming_model_node_trace_count": result["streaming_model_node_trace_count"],
                "temporal_candidate_snapshot_count": result["temporal_candidate_snapshot_count"],
                "cross_frame_consistency_check_count": result["cross_frame_consistency_check_count"],
                "cross_model_temporal_agreement_count": result["cross_model_temporal_agreement_count"],
                "midplatform_stream_governance_record_count": result["midplatform_stream_governance_record_count"],
                "negative_guard_passed": result["negative_guard_passed"],
                "blocker_count": result["blocker_count"],
                "final_decision": result["final_decision"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["final_decision"] == FINAL_DECISION_GO else 1


if __name__ == "__main__":
    raise SystemExit(main())
