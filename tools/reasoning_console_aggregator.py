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

