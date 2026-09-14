# -*- coding: utf-8 -*-
"""
Luna Reasoning Console Aggregator M0

职责：
- 只读 DecisionMonitor JSONL / frame dict
- 聚合为统一 ReasoningConsoleSnapshot
- 生成最小规则版 issue attribution（possible_issue_*）

约束：
- 不反写任何主逻辑
- 不做全量扫描：默认只读取 JSONL 末尾一定窗口
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from decision_monitor.reasoning_structure_tree import build_reasoning_structure_tree


def _safe_get(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur


def _as_str(x: Any) -> Optional[str]:
    if x is None:
        return None
    s = str(x)
    return s if s.strip() else None


def tail_jsonl_records(path: str, *, max_bytes: int = 2_000_000, max_records: int = 500) -> List[Dict[str, Any]]:
    """
    读取 JSONL 末尾窗口，避免大文件全扫。
    """
    p = Path(path)
    if not p.exists():
        return []
    size = p.stat().st_size
    start = max(0, size - int(max_bytes))
    data = b""
    with p.open("rb") as f:
        if start:
            f.seek(start)
            # 丢弃可能的半行
            f.readline()
        data = f.read()
    lines = data.splitlines()
    out: List[Dict[str, Any]] = []
    for raw in lines[-max_records:]:
        try:
            d = json.loads(raw.decode("utf-8"))
            if isinstance(d, dict):
                out.append(d)
        except Exception:
            continue
    return out


@dataclass
class ReasoningConsoleSnapshot:
    # A. 基础总览区
    snapshot_id: str
    ts: Optional[float] = None
    seq: Optional[int] = None
    trace_anchor_id: Optional[str] = None
    current_goal: Optional[str] = None
    current_flow_type: Optional[str] = None
    focus_target_label: Optional[str] = None
    terminal_status: Optional[str] = None
    can_resume: Optional[bool] = None
    blocked: Optional[bool] = None
    blocked_reason: Optional[str] = None
    integration_summary: Optional[str] = None

    # B. 空间与搜索区
    focus_target_expression: Optional[str] = None
    focus_target_actionable_expression: Optional[str] = None
    suggested_search_zone: Optional[str] = None
    next_search_step_summary: Optional[str] = None
    grid_summary: Optional[str] = None
    focus_target_cell_id: Optional[str] = None
    recommended_search_cell_id: Optional[str] = None
    recommended_search_cell_human_label: Optional[str] = None
    grid_followup_hint: Optional[str] = None

    # C. 搜索建议区
    grid_search_primary_cell: Optional[str] = None
    grid_search_secondary_cells: Optional[List[str]] = None
    grid_search_strategy_type: Optional[str] = None
    grid_search_expansion_hint: Optional[str] = None

    # D. 白盒区（原样挂载）
    grid_search_whitebox_trace: Optional[Dict[str, Any]] = None
    recheck_whitebox_trace: Optional[Dict[str, Any]] = None
    action_hint_whitebox_trace: Optional[Dict[str, Any]] = None
    confirmation_whitebox_trace: Optional[Dict[str, Any]] = None
    evidence_hypothesis_whitebox_trace: Optional[Dict[str, Any]] = None
    experience_governance_whitebox_trace: Optional[Dict[str, Any]] = None

    # E. 用户可见解释区（聚合）
    user_visible_explanation_primary: Optional[str] = None
    user_visible_explanation_followup: Optional[str] = None
    user_visible_explanation_confirmation: Optional[str] = None
    user_visible_feedback_impact: Optional[str] = None
    user_visible_excluded_alternative: Optional[str] = None

    # F. Advisory / Review（提示权，无裁决权；不参与 benchmark 判定）
    advisory_soft_fail_candidate_observed: Optional[bool] = None
    advisory_clause_id: Optional[str] = None
    advisory_review_gate_recommended: Optional[bool] = None
    advisory_reason_summary: Optional[str] = None

    # F. 互动与推进区
    confirmation_input_type: Optional[str] = None
    confirmation_input_raw_text: Optional[str] = None
    confirmation_bridge_next_effect: Optional[str] = None
    recheck_action: Optional[str] = None
    recheck_blocked: Optional[bool] = None
    action_hint_primary: Optional[str] = None
    action_hint_followup: Optional[str] = None
    action_hint_confirmation: Optional[str] = None

    # G. 错误归因区（M0 规则版）
    possible_issue_type: Optional[str] = None
    possible_issue_reason: Optional[str] = None
    suggested_debug_module: Optional[str] = None

    # Reasoning Structure Tree（M0）
    reasoning_structure_tree: Optional[Dict[str, Any]] = None
    reasoning_tree_metrics: Optional[Dict[str, Any]] = None
    reasoning_tree_quality_overlay: Optional[Dict[str, Any]] = None
    reasoning_timeline_view: Optional[Dict[str, Any]] = None
    optimization_hint: Optional[Dict[str, Any]] = None
    optimization_feedback_loop: Optional[Dict[str, Any]] = None
    knowledge_dual_channel_interface: Optional[Dict[str, Any]] = None
    spatiotemporal_continuity_reserve: Optional[Dict[str, Any]] = None
    strategy_injection_shadow: Optional[Dict[str, Any]] = None
    memory_novel_information_channel: Optional[Dict[str, Any]] = None
    environment_task_context_reserve: Optional[Dict[str, Any]] = None
    decision_contamination_guard_reserve: Optional[Dict[str, Any]] = None
    contamination_observation_summary: Optional[str] = None
    contamination_entry_risk_hint: Optional[str] = None
    contamination_mitigation_reserved: Optional[str] = None
    # Environment & Task Context Reserve M0：扁平摘要（便于 API / 前端）
    environment_scene_type: Optional[str] = None
    environment_visibility_state: Optional[str] = None
    task_chain_stage: Optional[str] = None
    task_chain_current_action: Optional[str] = None
    context_premise_summary: Optional[str] = None
    whitebox_context_premise_line: Optional[str] = None

    # Post-Processing Intelligence Reserve M0（后置信息处理占位；非记忆系统）
    post_processing_intelligence_reserve: Optional[Dict[str, Any]] = None
    post_processing_summary: Optional[str] = None
    post_processing_routing_hint: Optional[str] = None
    memory_write_reserved: Optional[bool] = None
    library_link_reserved: Optional[bool] = None
    # Scheduled Source State M0
    scheduled_source_state: Optional[Dict[str, Any]] = None
    scheduled_dominant_source: Optional[str] = None
    scheduled_source_conflict_summary: Optional[str] = None
    scheduled_priority_override_summary: Optional[str] = None
    scheduled_timeliness_pressure: Optional[str] = None
    scheduled_source_confidence_summary: Optional[str] = None
    scheduled_source_warning_summary: Optional[str] = None
    scheduled_source_readable_summary: Optional[str] = None
    task_state_presence_summary: Optional[str] = None

    # Task Chain State Snapshot M0
    task_chain_state_snapshot: Optional[Dict[str, Any]] = None
    snapshot_task_chain_stage: Optional[str] = None
    snapshot_task_mode: Optional[str] = None
    snapshot_task_resume_target: Optional[str] = None
    snapshot_primary_task_id: Optional[str] = None
    snapshot_active_subtask_id: Optional[str] = None
    snapshot_task_position_reason_summary: Optional[str] = None
    snapshot_task_position_warning_summary: Optional[str] = None
    snapshot_task_position_readable: Optional[str] = None

    # Memory Invocation Explanation M0.3
    memory_invocation_explanation: Optional[Dict[str, Any]] = None
    memory_invocation_invoked: Optional[bool] = None
    memory_invocation_type_summary: Optional[str] = None
    memory_invocation_reason_summary: Optional[str] = None
    memory_invocation_used_content_summary: Optional[str] = None
    memory_invocation_effect_summary: Optional[str] = None
    memory_invocation_readable: Optional[str] = None

    # Trace × Summary Separation M0.2：黑匣子 / 结构化事件 / 总结入口分层
    raw_trace_layer_one_liner: Optional[str] = None
    structured_event_layer_one_liner: Optional[str] = None
    summary_reference_one_liner: Optional[str] = None
    run_summary_reference: Optional[Dict[str, Any]] = None
    run_summary_brief: Optional[str] = None
    run_summary_mainline_summary: Optional[str] = None
    run_summary_memory_usage_summary: Optional[str] = None
    run_summary_issue_or_risk_summary: Optional[str] = None
    run_summary_id: Optional[str] = None
    run_summary_task_chain_progress_summary: Optional[str] = None
    run_summary_mainline_state_summary: Optional[str] = None
    run_summary_mainline_narrative_brief: Optional[str] = None
    run_summary_process_observation_summary: Optional[str] = None
    run_summary_resume_chain_fragility_summary: Optional[str] = None
    run_summary_memory_bias_accumulation_summary: Optional[str] = None
    run_summary_closure_semantics_misalignment_summary: Optional[str] = None
    mainline_state_snapshot: Optional[Dict[str, Any]] = None
    snapshot_mainline_state: Optional[str] = None
    snapshot_mainline_phase: Optional[str] = None
    snapshot_mainline_state_reason: Optional[str] = None
    snapshot_mainline_phase_reason: Optional[str] = None
    # Summary × Post-Processing Boundary M0.5
    post_processing_summary_entry: Optional[Dict[str, Any]] = None
    post_processing_entry_id: Optional[str] = None
    post_processing_requires_trace_backfill: Optional[bool] = None
    post_processing_requires_event_backfill: Optional[bool] = None
    post_processing_requires_whitebox_backfill: Optional[bool] = None
    post_processing_backfill_reason_summary: Optional[str] = None
    post_processing_process_observation_summary: Optional[str] = None
    mainline_narrative_alignment: Optional[Dict[str, Any]] = None
    mainline_narrative_readable: Optional[str] = None

    # Narrative / Evidence Tension Review M0（只读审计；不进 benchmark 规则）
    narrative_evidence_tension_review: Optional[Dict[str, Any]] = None
    tension_review_readable: Optional[str] = None
    tension_review_brief: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _derive_issue(snapshot: ReasoningConsoleSnapshot) -> None:
    """
    M0 规则版归因：只做可解释 tag，不做概率与模型。
    """
    # 1) blocked recheck / human check
    if snapshot.recheck_blocked:
        snapshot.possible_issue_type = "blocked_recheck"
        snapshot.possible_issue_reason = "recheck 被阻断（可能来自 minimum_mode / scene_gate / human_check）"
        snapshot.suggested_debug_module = "recheck_planner"
        return

    # 2) confirmation mapping conflict: next_effect none but有输入
    if snapshot.confirmation_input_raw_text and (snapshot.confirmation_bridge_next_effect in (None, "none")):
        snapshot.possible_issue_type = "mapping_issue"
        snapshot.possible_issue_reason = "有用户反馈但未产生推进（next_effect=none）"
        snapshot.suggested_debug_module = "confirmation_input_bridge"
        return

    # 3) missing user-visible explanation when whitebox exists
    if snapshot.confirmation_whitebox_trace and not snapshot.user_visible_feedback_impact:
        snapshot.possible_issue_type = "missing_user_visible_explanation"
        snapshot.possible_issue_reason = "confirmation 白盒存在但用户可见解释不完整"
        snapshot.suggested_debug_module = "confirmation_whitebox_trace"
        return

    # 4) weak visual evidence but hint specific: heuristic by evidence confidence
    ev0 = None
    try:
        ev_entries = _safe_get(snapshot.recheck_whitebox_trace, "weight_allocation") or []
        if isinstance(ev_entries, list) and ev_entries:
            ev0 = ev_entries[0].get("weight_total") if isinstance(ev_entries[0], dict) else None
    except Exception:
        ev0 = None
    if ev0 is not None and isinstance(ev0, (int, float)) and float(ev0) < 0.3 and snapshot.action_hint_primary:
        snapshot.possible_issue_type = "weak_visual_evidence_but_hint_specific"
        snapshot.possible_issue_reason = "补证权重偏低但话术仍较具体，可能需要降级表达或补证"
        snapshot.suggested_debug_module = "action_hint_whitebox_trace"
        return


def aggregate_frame(frame: Dict[str, Any]) -> ReasoningConsoleSnapshot:
    trace_anchor_id = _as_str(frame.get("trace_anchor_id"))
    seq = _safe_get(frame, "inputs", "frame_seq")
    ts = _safe_get(frame, "inputs", "current_ts")
    snapshot_id = trace_anchor_id or (str(seq) if seq is not None else "unknown")

    goal_type = _as_str(_safe_get(frame, "goal", "goal_type"))
    goal_status = _as_str(_safe_get(frame, "goal", "goal_status"))
    current_goal = " / ".join([x for x in (goal_type, goal_status) if x]) or None

    osi_flow = _as_str(_safe_get(frame, "object_search_interaction", "interaction_flow_type"))
    current_flow = osi_flow or _as_str(_safe_get(frame, "confirmation_input_bridge", "confirmation_bridge_target_flow"))

    focus_target_label = _as_str(_safe_get(frame, "object_search_interaction", "search_target_label")) or _as_str(
        _safe_get(frame, "spatial_expression_sidecar", "focus_target_label")
    )
    terminal_status = _as_str(_safe_get(frame, "object_search_interaction", "search_terminal_status"))
    can_resume = _safe_get(frame, "object_search_interaction", "search_can_resume_main_task")

    # blocked：以 mainline/chain/recheck blocked 近似表达
    blocked = bool(_safe_get(frame, "task_chain_bridge", "task_chain_blocked") is True) or bool(
        _safe_get(frame, "recheck_planner", "recheck_blocked") is True
    )
    blocked_reason = _as_str(_safe_get(frame, "task_chain_bridge", "task_chain_block_reason")) or _as_str(
        _safe_get(frame, "recheck_planner", "recheck_block_reason")
    )

    integration_summary = _as_str(_safe_get(frame, "mainline_integration", "integration_summary"))

    # space/search
    focus_expr = _as_str(_safe_get(frame, "spatial_expression_sidecar", "focus_target_expression"))
    focus_act = _as_str(_safe_get(frame, "spatial_expression_sidecar", "focus_target_actionable_expression"))
    suggested_zone = _as_str(_safe_get(frame, "object_search_interaction", "suggested_search_zone"))
    next_step = _as_str(_safe_get(frame, "object_search_interaction", "next_search_step_summary"))

    grid_summary = _as_str(_safe_get(frame, "local_task_space_grid", "grid_summary"))
    focus_cell = _as_str(_safe_get(frame, "local_task_space_grid", "focus_target_cell_id"))
    rec_cell = _as_str(_safe_get(frame, "local_task_space_grid", "recommended_search_cell_id"))
    rec_cell_h = _as_str(_safe_get(frame, "local_task_space_grid", "recommended_search_cell_human_label"))
    grid_follow = _as_str(_safe_get(frame, "local_task_space_grid", "grid_followup_hint"))

    # expansion
    gse_primary = _as_str(_safe_get(frame, "grid_search_expansion", "primary_search_cell_id"))
    gse_secondary = _safe_get(frame, "grid_search_expansion", "secondary_search_cell_ids")
    if not isinstance(gse_secondary, list):
        gse_secondary = None
    gse_strategy = _as_str(_safe_get(frame, "grid_search_expansion", "expansion_strategy_type"))
    gse_hint = _as_str(_safe_get(frame, "grid_search_expansion", "grid_search_expansion_hint"))

    # whiteboxes
    grid_wb = frame.get("grid_search_whitebox_trace") if isinstance(frame.get("grid_search_whitebox_trace"), dict) else None
    recheck_wb = frame.get("recheck_whitebox_trace") if isinstance(frame.get("recheck_whitebox_trace"), dict) else None
    ah_wb = frame.get("action_hint_whitebox_trace") if isinstance(frame.get("action_hint_whitebox_trace"), dict) else None
    conf_wb = frame.get("confirmation_whitebox_trace") if isinstance(frame.get("confirmation_whitebox_trace"), dict) else None
    eh_wb = frame.get("evidence_hypothesis_whitebox_trace") if isinstance(frame.get("evidence_hypothesis_whitebox_trace"), dict) else None
    eg_wb = frame.get("experience_governance_whitebox_trace") if isinstance(frame.get("experience_governance_whitebox_trace"), dict) else None

    # user-visible: prefer action_hint > confirmation
    uv_primary = _as_str(_safe_get(ah_wb, "user_visible_explanation", "user_visible_reason_primary"))
    uv_follow = _as_str(_safe_get(ah_wb, "user_visible_explanation", "user_visible_reason_followup"))
    uv_conf = _as_str(_safe_get(ah_wb, "user_visible_explanation", "user_visible_reason_confirmation"))
    uv_impact = _as_str(_safe_get(conf_wb, "user_visible_explanation", "user_visible_changed_search_direction")) or _as_str(
        _safe_get(ah_wb, "user_visible_explanation", "user_visible_changed_by_feedback")
    )
    uv_excl = _as_str(_safe_get(conf_wb, "user_visible_explanation", "user_visible_excluded_alternative")) or _as_str(
        _safe_get(ah_wb, "user_visible_explanation", "user_visible_excluded_alternative")
    )

    # interaction/push
    cib_type = _as_str(_safe_get(frame, "confirmation_input_bridge", "confirmation_input_type"))
    cib_raw = _as_str(_safe_get(frame, "confirmation_input_bridge", "confirmation_input_raw_text"))
    cib_eff = _as_str(_safe_get(frame, "confirmation_input_bridge", "confirmation_bridge_next_effect"))
    recheck_action = _as_str(_safe_get(frame, "recheck_planner", "recheck_action"))
    recheck_blocked = _safe_get(frame, "recheck_planner", "recheck_blocked")
    ah_primary = _as_str(_safe_get(frame, "action_hint_copy", "action_hint_primary"))
    ah_follow = _as_str(_safe_get(frame, "action_hint_copy", "action_hint_followup"))
    ah_confirm = _as_str(_safe_get(frame, "action_hint_copy", "action_hint_confirmation"))

    snap = ReasoningConsoleSnapshot(
        snapshot_id=snapshot_id,
        ts=ts if isinstance(ts, (int, float)) else None,
        seq=seq if isinstance(seq, int) else None,
        trace_anchor_id=trace_anchor_id,
        current_goal=current_goal,
        current_flow_type=current_flow,
        focus_target_label=focus_target_label,
        terminal_status=terminal_status,
        can_resume=bool(can_resume) if can_resume is not None else None,
        blocked=bool(blocked),
        blocked_reason=blocked_reason,
        integration_summary=integration_summary,
        focus_target_expression=focus_expr,
        focus_target_actionable_expression=focus_act,
        suggested_search_zone=suggested_zone,
        next_search_step_summary=next_step,
        grid_summary=grid_summary,
        focus_target_cell_id=focus_cell,
        recommended_search_cell_id=rec_cell,
        recommended_search_cell_human_label=rec_cell_h,
        grid_followup_hint=grid_follow,
        grid_search_primary_cell=gse_primary,
        grid_search_secondary_cells=gse_secondary,
        grid_search_strategy_type=gse_strategy,
        grid_search_expansion_hint=gse_hint,
        grid_search_whitebox_trace=grid_wb,
        recheck_whitebox_trace=recheck_wb,
        action_hint_whitebox_trace=ah_wb,
        confirmation_whitebox_trace=conf_wb,
        evidence_hypothesis_whitebox_trace=eh_wb,
        experience_governance_whitebox_trace=eg_wb,
        user_visible_explanation_primary=uv_primary,
        user_visible_explanation_followup=uv_follow,
        user_visible_explanation_confirmation=uv_conf,
        user_visible_feedback_impact=uv_impact,
        user_visible_excluded_alternative=uv_excl,
        advisory_soft_fail_candidate_observed=_safe_get(frame, "advisory_review_observation", "soft_fail_candidate_observed"),
        advisory_clause_id=_as_str(_safe_get(frame, "advisory_review_observation", "soft_fail_candidate_clause_id")),
        advisory_review_gate_recommended=_safe_get(frame, "advisory_review_observation", "review_gate_recommended"),
        advisory_reason_summary=_as_str(_safe_get(frame, "advisory_review_observation", "soft_fail_candidate_reason_summary")),
        confirmation_input_type=cib_type,
        confirmation_input_raw_text=cib_raw,
        confirmation_bridge_next_effect=cib_eff,
        recheck_action=recheck_action,
        recheck_blocked=bool(recheck_blocked) if recheck_blocked is not None else None,
        action_hint_primary=ah_primary,
        action_hint_followup=ah_follow,
        action_hint_confirmation=ah_confirm,
    )

    # Reasoning Structure Tree (M0): only-read aggregation
    try:
        tree = build_reasoning_structure_tree(frame).to_dict()
        snap.reasoning_structure_tree = tree
    except Exception:
        snap.reasoning_structure_tree = None

    # Tree Metrics (M0): prefer frame-provided; fallback compute from tree
    try:
        m = frame.get("reasoning_tree_metrics") if isinstance(frame.get("reasoning_tree_metrics"), dict) else None
        if m is None and snap.reasoning_structure_tree:
            from decision_monitor.reasoning_tree_metrics import build_reasoning_tree_metrics

            m = build_reasoning_tree_metrics(snap.reasoning_structure_tree).to_dict()
        snap.reasoning_tree_metrics = m
    except Exception:
        snap.reasoning_tree_metrics = None

    # Reasoning Tree Quality Overlay (M0): prefer frame-provided; fallback compute from tree+metrics
    try:
        qo = frame.get("reasoning_tree_quality_overlay")
        if qo is not None and hasattr(qo, "to_dict"):
            qo = qo.to_dict()
        if qo is None and snap.reasoning_structure_tree and snap.reasoning_tree_metrics:
            from decision_monitor.reasoning_tree_quality_overlay import build_reasoning_tree_quality_overlay

            qo = build_reasoning_tree_quality_overlay(
                snap.reasoning_structure_tree,
                snap.reasoning_tree_metrics,
                frame.get("optimization_feedback_loop") if isinstance(frame.get("optimization_feedback_loop"), dict) else None,
            ).to_dict()
        snap.reasoning_tree_quality_overlay = qo if isinstance(qo, dict) else None
    except Exception:
        snap.reasoning_tree_quality_overlay = None

    # Reasoning Timeline View (M0): prefer frame-provided; fallback compute from frame dict
    try:
        tv = frame.get("reasoning_timeline_view")
        if tv is not None and hasattr(tv, "to_dict"):
            tv = tv.to_dict()
        if tv is None:
            from decision_monitor.reasoning_timeline_view import build_reasoning_timeline_view

            tv = build_reasoning_timeline_view(frame).to_dict()
        snap.reasoning_timeline_view = tv if isinstance(tv, dict) else None
    except Exception:
        snap.reasoning_timeline_view = None

    # Optimization Hint (M0): prefer frame-provided; fallback compute from metrics+tree
    try:
        oh = frame.get("optimization_hint") if isinstance(frame.get("optimization_hint"), dict) else None
        if oh is None:
            from decision_monitor.optimization_hint import build_optimization_hint

            oh = build_optimization_hint(
                reasoning_tree_metrics=snap.reasoning_tree_metrics,
                reasoning_structure_tree=snap.reasoning_structure_tree,
                whiteboxes={
                    "grid_search_whitebox_trace": grid_wb,
                    "recheck_whitebox_trace": recheck_wb,
                    "action_hint_whitebox_trace": ah_wb,
                    "confirmation_whitebox_trace": conf_wb,
                    "evidence_hypothesis_whitebox_trace": frame.get("evidence_hypothesis_whitebox_trace"),
                    "experience_governance_whitebox_trace": frame.get("experience_governance_whitebox_trace"),
                },
            ).to_dict()
        snap.optimization_hint = oh
    except Exception:
        snap.optimization_hint = None

    # Optimization Feedback Loop (M0): prefer frame-provided; fallback compute from hint+metrics
    try:
        ofl = frame.get("optimization_feedback_loop") if isinstance(frame.get("optimization_feedback_loop"), dict) else None
        if ofl is None:
            from decision_monitor.optimization_feedback_loop import build_optimization_feedback_loop

            ofl = build_optimization_feedback_loop(
                optimization_hint=snap.optimization_hint,
                reasoning_tree_metrics=snap.reasoning_tree_metrics,
                reasoning_structure_tree=snap.reasoning_structure_tree,
                baseline=None,
            ).to_dict()
        snap.optimization_feedback_loop = ofl
    except Exception:
        snap.optimization_feedback_loop = None

    # Knowledge Dual-Channel Interface (M0): prefer frame-provided; fallback compute from hint/loop/metrics
    try:
        k = frame.get("knowledge_dual_channel_interface") if isinstance(frame.get("knowledge_dual_channel_interface"), dict) else None
        if k is None:
            from decision_monitor.knowledge_dual_channel_interface import build_knowledge_dual_channel_interface

            k = build_knowledge_dual_channel_interface(
                optimization_feedback_loop=snap.optimization_feedback_loop,
                optimization_hint=snap.optimization_hint,
                reasoning_tree_metrics=snap.reasoning_tree_metrics,
            ).to_dict()
        snap.knowledge_dual_channel_interface = k
    except Exception:
        snap.knowledge_dual_channel_interface = None

    # Spatiotemporal Continuity Reserve (M0): prefer frame-provided; fallback compute from frame
    try:
        c = frame.get("spatiotemporal_continuity_reserve") if isinstance(frame.get("spatiotemporal_continuity_reserve"), dict) else None
        if c is None:
            from decision_monitor.spatiotemporal_continuity_reserve import build_spatiotemporal_continuity_reserve

            c = build_spatiotemporal_continuity_reserve(frame).to_dict()
        snap.spatiotemporal_continuity_reserve = c
    except Exception:
        snap.spatiotemporal_continuity_reserve = None

    # Strategy Injection Shadow (M0): prefer frame-provided; fallback compute from knowledge injection slot
    try:
        sh = frame.get("strategy_injection_shadow") if isinstance(frame.get("strategy_injection_shadow"), dict) else None
        if sh is None:
            from decision_monitor.strategy_injection_shadow import build_strategy_injection_shadow

            inj = None
            k = snap.knowledge_dual_channel_interface or {}
            if isinstance(k, dict):
                inj = k.get("injection_slot") if isinstance(k.get("injection_slot"), dict) else None
            sh = build_strategy_injection_shadow(
                injection_slot=inj,
                optimization_hint=snap.optimization_hint,
                optimization_feedback_loop=snap.optimization_feedback_loop,
                reasoning_tree_metrics=snap.reasoning_tree_metrics,
                reasoning_structure_tree=snap.reasoning_structure_tree,
            ).to_dict()
        snap.strategy_injection_shadow = sh
    except Exception:
        snap.strategy_injection_shadow = None

    # Memory vs Novel Information Channel (M0): prefer frame-provided; fallback compute from frame
    try:
        mn = frame.get("memory_novel_information_channel") if isinstance(frame.get("memory_novel_information_channel"), dict) else None
        if mn is None:
            from decision_monitor.memory_novel_information_channel import build_memory_novel_information_channel

            mn = build_memory_novel_information_channel(frame).to_dict()
        snap.memory_novel_information_channel = mn
    except Exception:
        snap.memory_novel_information_channel = None

    # Environment & Task Context Reserve M0
    try:
        etc = frame.get("environment_task_context_reserve") if isinstance(frame.get("environment_task_context_reserve"), dict) else None
        if etc is None:
            from decision_monitor.environment_task_context_reserve import build_environment_task_context_reserve

            etc = build_environment_task_context_reserve(frame).to_dict()
        snap.environment_task_context_reserve = etc
        if isinstance(etc, dict):
            ec = etc.get("environment_context") if isinstance(etc.get("environment_context"), dict) else {}
            tc = etc.get("task_chain_context") if isinstance(etc.get("task_chain_context"), dict) else {}
            snap.environment_scene_type = _as_str(ec.get("environment_scene_type"))
            snap.environment_visibility_state = _as_str(ec.get("environment_visibility_state"))
            snap.task_chain_stage = _as_str(tc.get("task_chain_stage"))
            snap.task_chain_current_action = _as_str(tc.get("task_chain_current_action"))
            snap.context_premise_summary = _as_str(etc.get("context_premise_summary"))
            snap.whitebox_context_premise_line = _as_str(etc.get("whitebox_context_premise_line")) or snap.context_premise_summary
    except Exception:
        snap.environment_task_context_reserve = None

    # Decision Contamination Guard Reserve M0
    try:
        dcg = frame.get("decision_contamination_guard_reserve") if isinstance(frame.get("decision_contamination_guard_reserve"), dict) else None
        if dcg is None:
            from decision_monitor.decision_contamination_guard_reserve import build_decision_contamination_guard_reserve

            dcg = build_decision_contamination_guard_reserve(frame).to_dict()
        snap.decision_contamination_guard_reserve = dcg
        if isinstance(dcg, dict):
            snap.contamination_observation_summary = _as_str(dcg.get("contamination_observation_summary"))
            eps = dcg.get("potential_entry_points")
            if isinstance(eps, list) and eps:
                r0 = eps[0].get("entry_point_risk_level") if isinstance(eps[0], dict) else None
                snap.contamination_entry_risk_hint = _as_str(r0)
            mits = dcg.get("potential_mitigation_points")
            if isinstance(mits, list) and mits:
                types = [str(x.get("mitigation_type")) for x in mits if isinstance(x, dict) and x.get("mitigation_type")]
                snap.contamination_mitigation_reserved = ",".join(types[:6]) if types else None
    except Exception:
        snap.decision_contamination_guard_reserve = None

    # Post-Processing Intelligence Reserve M0
    try:
        pp = frame.get("post_processing_intelligence_reserve") if isinstance(frame.get("post_processing_intelligence_reserve"), dict) else None
        if pp is None:
            from decision_monitor.post_processing_intelligence_reserve import build_post_processing_intelligence_reserve

            pp = build_post_processing_intelligence_reserve(frame).to_dict()
        snap.post_processing_intelligence_reserve = pp
        if isinstance(pp, dict):
            snap.post_processing_summary = _as_str(pp.get("post_processing_summary"))
            snap.memory_write_reserved = pp.get("memory_write_reserved") if isinstance(pp.get("memory_write_reserved"), bool) else None
            snap.library_link_reserved = pp.get("library_link_reserved") if isinstance(pp.get("library_link_reserved"), bool) else None
            rr = pp.get("routing_reserve") or []
            if isinstance(rr, list) and rr:
                t0 = rr[0].get("routing_target") if isinstance(rr[0], dict) else None
                snap.post_processing_routing_hint = _as_str(t0)
    except Exception:
        snap.post_processing_intelligence_reserve = None

    # Scheduled Source State M0
    try:
        ssc = frame.get("scheduled_source_state") if isinstance(frame.get("scheduled_source_state"), dict) else None
        if ssc is None:
            from decision_monitor.information_source_scheduler import build_scheduled_source_state

            ssc = build_scheduled_source_state(frame).to_dict()
        snap.scheduled_source_state = ssc
        if isinstance(ssc, dict):
            snap.scheduled_dominant_source = _as_str(ssc.get("dominant_source"))
            snap.scheduled_source_conflict_summary = _as_str(ssc.get("source_conflict_summary"))
            snap.scheduled_priority_override_summary = _as_str(ssc.get("priority_override_summary"))
            snap.scheduled_timeliness_pressure = _as_str(ssc.get("timeliness_pressure"))
            snap.scheduled_source_confidence_summary = _as_str(ssc.get("source_confidence_summary"))
            snap.scheduled_source_warning_summary = _as_str(ssc.get("source_scheduling_warning_summary"))
            snap.task_state_presence_summary = _as_str(ssc.get("task_state_presence_summary"))
            p0 = ",".join((ssc.get("participating_sources") or [])[:3]) if isinstance(ssc.get("participating_sources"), list) else None
            snap.scheduled_source_readable_summary = (
                f"dominant={snap.scheduled_dominant_source or '—'}"
                f" | conflict={snap.scheduled_source_conflict_summary or '—'}"
                f" | override={snap.scheduled_priority_override_summary or '—'}"
                f" | t={snap.scheduled_timeliness_pressure or '—'}"
                f" | conf={snap.scheduled_source_confidence_summary or '—'}"
                f" | src={p0 or '—'}"
                f" | task_presence={snap.task_state_presence_summary or '—'}"
            )
    except Exception:
        snap.scheduled_source_state = None

    # Task Chain State Snapshot M0
    try:
        tcs = frame.get("task_chain_state_snapshot") if isinstance(frame.get("task_chain_state_snapshot"), dict) else None
        if tcs is None and frame.get("task_chain_state_snapshot") is not None and hasattr(frame.get("task_chain_state_snapshot"), "to_dict"):
            tcs = frame.get("task_chain_state_snapshot").to_dict()
        snap.task_chain_state_snapshot = tcs
        if isinstance(tcs, dict):
            snap.snapshot_task_chain_stage = _as_str(tcs.get("task_chain_stage"))
            snap.snapshot_task_mode = _as_str(tcs.get("task_mode"))
            snap.snapshot_task_resume_target = _as_str(tcs.get("task_resume_target"))
            snap.snapshot_primary_task_id = _as_str(tcs.get("primary_task_id"))
            snap.snapshot_active_subtask_id = _as_str(tcs.get("active_subtask_id"))
            snap.snapshot_task_position_reason_summary = _as_str(tcs.get("task_position_reason_summary"))
            snap.snapshot_task_position_warning_summary = _as_str(tcs.get("task_position_warning_summary"))
            pr = snap.snapshot_task_position_reason_summary or ""
            pw = snap.snapshot_task_position_warning_summary or ""
            evs = tcs.get("task_position_event_summaries") if isinstance(tcs.get("task_position_event_summaries"), list) else []
            ev_head = ",".join(_as_str(x) for x in evs[:3]) if evs else ""
            parts_rd = [
                f"stage={snap.snapshot_task_chain_stage or '—'}",
                f"mode={snap.snapshot_task_mode or '—'}",
            ]
            if pr:
                parts_rd.append(pr[:200])
            if pw and pw != "none":
                parts_rd.append(f"warn={pw}")
            if ev_head:
                parts_rd.append(f"ev={ev_head}")
            snap.snapshot_task_position_readable = "|".join(parts_rd)[:500]
    except Exception:
        snap.task_chain_state_snapshot = None

    # Memory Invocation Explanation M0.3
    try:
        mie = frame.get("memory_invocation_explanation")
        if mie is not None and hasattr(mie, "to_dict"):
            mie = mie.to_dict()
        if isinstance(mie, dict) and mie.get("memory_invocation_explanation_applied"):
            snap.memory_invocation_explanation = mie
            snap.memory_invocation_invoked = bool(mie.get("memory_invoked"))
            snap.memory_invocation_type_summary = _as_str(mie.get("memory_type_summary"))
            snap.memory_invocation_reason_summary = _as_str(mie.get("memory_invocation_reason_summary"))
            snap.memory_invocation_used_content_summary = _as_str(mie.get("memory_invocation_used_content_summary"))
            snap.memory_invocation_effect_summary = _as_str(mie.get("memory_invocation_effect_summary"))
            alt = _as_str(mie.get("memory_invocation_alternative_summary"))
            parts_m = [
                f"invoked={'yes' if snap.memory_invocation_invoked else 'no'}",
                f"type={snap.memory_invocation_type_summary or '—'}",
            ]
            if snap.memory_invocation_reason_summary:
                parts_m.append(snap.memory_invocation_reason_summary[:180])
            if snap.memory_invocation_effect_summary:
                parts_m.append(f"effect={snap.memory_invocation_effect_summary}")
            if alt:
                parts_m.append(f"alt={alt[:120]}")
            snap.memory_invocation_readable = "|".join(parts_m)[:600]
        else:
            snap.memory_invocation_explanation = None
    except Exception:
        snap.memory_invocation_explanation = None

    # Mainline State / Phase M0.4
    try:
        mls = frame.get("mainline_state_snapshot") if isinstance(frame.get("mainline_state_snapshot"), dict) else None
        if mls is None and frame.get("mainline_state_snapshot") is not None and hasattr(frame.get("mainline_state_snapshot"), "to_dict"):
            mls = frame.get("mainline_state_snapshot").to_dict()
        if isinstance(mls, dict) and mls.get("mainline_state_snapshot_applied"):
            snap.mainline_state_snapshot = mls
            snap.snapshot_mainline_state = _as_str(mls.get("mainline_state"))
            snap.snapshot_mainline_phase = _as_str(mls.get("mainline_phase"))
            snap.snapshot_mainline_state_reason = _as_str(mls.get("mainline_state_reason_summary"))
            snap.snapshot_mainline_phase_reason = _as_str(mls.get("mainline_phase_reason_summary"))
        else:
            snap.mainline_state_snapshot = None
    except Exception:
        snap.mainline_state_snapshot = None

    # Summary × Post-Processing Boundary M0.5
    try:
        pse = frame.get("post_processing_summary_entry")
        if pse is not None and hasattr(pse, "to_dict"):
            pse = pse.to_dict()
        if isinstance(pse, dict) and pse.get("post_processing_summary_entry_applied"):
            snap.post_processing_summary_entry = pse
            snap.post_processing_entry_id = _as_str(pse.get("entry_id"))
            snap.post_processing_requires_trace_backfill = bool(pse.get("requires_trace_backfill"))
            snap.post_processing_requires_event_backfill = bool(pse.get("requires_event_backfill"))
            snap.post_processing_requires_whitebox_backfill = bool(pse.get("requires_whitebox_backfill"))
            snap.post_processing_backfill_reason_summary = _as_str(pse.get("backfill_reason_summary"))
            snap.post_processing_process_observation_summary = _as_str(pse.get("process_observation_summary"))
        else:
            snap.post_processing_summary_entry = None
    except Exception:
        snap.post_processing_summary_entry = None

    # Trace × Summary Separation M0.2：三层语义（raw / structured event / summary reference）
    try:
        from decision_monitor.run_summary_builder import build_log_chain_layer_summaries

        layers = build_log_chain_layer_summaries(frame)
        snap.raw_trace_layer_one_liner = _as_str(layers.get("raw_trace_one_liner"))
        snap.structured_event_layer_one_liner = _as_str(layers.get("structured_event_one_liner"))
        snap.summary_reference_one_liner = _as_str(layers.get("summary_reference_one_liner"))
        emb = frame.get("run_summary_reference")
        if isinstance(emb, dict):
            snap.run_summary_reference = emb
        elif emb is not None and hasattr(emb, "to_dict"):
            snap.run_summary_reference = emb.to_dict()
        else:
            snap.run_summary_reference = layers.get("run_summary_reference") if isinstance(layers.get("run_summary_reference"), dict) else None
        rsr = snap.run_summary_reference or {}
        snap.run_summary_brief = _as_str(rsr.get("summary_brief"))
        snap.run_summary_mainline_summary = _as_str(rsr.get("mainline_summary"))
        snap.run_summary_memory_usage_summary = _as_str(rsr.get("memory_usage_summary"))
        snap.run_summary_issue_or_risk_summary = _as_str(rsr.get("issue_or_risk_summary"))
        snap.run_summary_id = _as_str(rsr.get("summary_id"))
        snap.run_summary_task_chain_progress_summary = _as_str(rsr.get("task_chain_progress_summary"))
        snap.run_summary_mainline_state_summary = _as_str(rsr.get("mainline_state_summary"))
        snap.run_summary_mainline_narrative_brief = _as_str(rsr.get("mainline_narrative_brief"))
        snap.run_summary_process_observation_summary = _as_str(rsr.get("process_observation_summary"))
        snap.run_summary_resume_chain_fragility_summary = _as_str(rsr.get("resume_chain_fragility_summary"))
        snap.run_summary_memory_bias_accumulation_summary = _as_str(rsr.get("memory_bias_accumulation_summary"))
        snap.run_summary_closure_semantics_misalignment_summary = _as_str(rsr.get("closure_semantics_misalignment_summary"))
    except Exception:
        snap.run_summary_reference = None

    # Mainline Narrative Alignment M0.6
    try:
        nar = frame.get("mainline_narrative_alignment")
        if nar is not None and hasattr(nar, "to_dict"):
            nar = nar.to_dict()
        if isinstance(nar, dict) and nar.get("mainline_narrative_alignment_applied"):
            snap.mainline_narrative_alignment = nar
            snap.mainline_narrative_readable = _as_str(nar.get("narrative_brief"))
        else:
            snap.mainline_narrative_alignment = None
            snap.mainline_narrative_readable = snap.run_summary_mainline_narrative_brief
    except Exception:
        snap.mainline_narrative_alignment = None

    # Narrative / Evidence Tension Review M0
    try:
        netr = frame.get("narrative_evidence_tension_review")
        if netr is not None and hasattr(netr, "to_dict"):
            netr = netr.to_dict()
        if isinstance(netr, dict) and netr.get("narrative_evidence_tension_review_applied"):
            snap.narrative_evidence_tension_review = netr
            snap.tension_review_readable = _as_str(netr.get("tension_review_readable"))
            snap.tension_review_brief = _as_str(netr.get("tension_review_brief"))
        else:
            snap.narrative_evidence_tension_review = None
            snap.tension_review_readable = None
            snap.tension_review_brief = None
    except Exception:
        snap.narrative_evidence_tension_review = None
        snap.tension_review_readable = None
        snap.tension_review_brief = None

    _derive_issue(snap)
    return snap


def load_snapshots_from_jsonl(jsonl_path: str) -> List[ReasoningConsoleSnapshot]:
    frames = tail_jsonl_records(jsonl_path)
    snaps = [aggregate_frame(f) for f in frames]
    # sort by ts then seq
    snaps.sort(key=lambda s: (s.ts or 0.0, s.seq or 0))
    return snaps


def resolve_default_jsonl_path() -> Optional[str]:
    """
    优先使用环境变量；否则默认 logs/decision_monitor.jsonl（如果存在）。
    """
    env = os.environ.get("REASONING_CONSOLE_JSONL_PATH")
    if env and env.strip():
        return env.strip()
    root = Path(__file__).resolve().parents[1]
    p = root / "logs" / "decision_monitor.jsonl"
    return str(p) if p.exists() else None

