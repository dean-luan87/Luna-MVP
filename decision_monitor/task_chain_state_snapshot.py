# -*- coding: utf-8 -*-
"""
Task Chain State Snapshot M0（任务链状态快照最小接入）

M0.1：任务链位置解释增强（只读解释，不拍板；不实现完整任务引擎）
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Dict, List, Optional, Tuple

TASK_MODES = ("main", "subtask", "inserted", "recovering", "paused", "unknown")


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class TaskChainStateSnapshot:
    task_chain_id: Optional[str] = None
    task_chain_stage: Optional[str] = None
    primary_task_id: Optional[str] = None
    active_subtask_id: Optional[str] = None
    task_mode: str = "unknown"
    task_resume_target: Optional[str] = None
    task_success_criteria_summary: Optional[str] = None
    task_chain_context_summary: Optional[str] = None
    task_chain_state_snapshot_applied: bool = False
    # M0.1 位置解释（派生自已有字段）
    task_position_reason_summary: Optional[str] = None
    task_position_event_summaries: List[str] = field(default_factory=list)
    task_position_warning_summary: Optional[str] = None
    task_position_timeline_events: List[Dict[str, str]] = field(default_factory=list)
    resume_main_progress_alignment_summary: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_chain_id": self.task_chain_id,
            "task_chain_stage": self.task_chain_stage,
            "primary_task_id": self.primary_task_id,
            "active_subtask_id": self.active_subtask_id,
            "task_mode": self.task_mode,
            "task_resume_target": self.task_resume_target,
            "task_success_criteria_summary": self.task_success_criteria_summary,
            "task_chain_context_summary": self.task_chain_context_summary,
            "task_chain_state_snapshot_applied": bool(self.task_chain_state_snapshot_applied),
            "task_position_reason_summary": self.task_position_reason_summary,
            "task_position_event_summaries": list(self.task_position_event_summaries),
            "task_position_warning_summary": self.task_position_warning_summary,
            "task_position_timeline_events": [dict(x) for x in self.task_position_timeline_events],
            "resume_main_progress_alignment_summary": self.resume_main_progress_alignment_summary,
        }


def _infer_task_mode(
    tcb: Optional[Dict[str, Any]],
    osi: Optional[Dict[str, Any]],
    arb_action: Optional[str],
) -> str:
    """轻量规则：主链/搜索/仲裁已有字段 → task_mode。"""
    if not isinstance(tcb, dict):
        return "unknown"
    tcs = (_s(tcb.get("task_chain_state")) or "").strip()
    sub = (_s(tcb.get("task_chain_substate")) or "").strip()
    bundle_st = (_s(tcb.get("task_chain_bundle_state")) or "none").strip()
    if tcs == "paused" or sub == "deferred_by_conflict":
        return "paused"
    if tcs == "blocked":
        return "paused"
    if tcs == "waiting_user":
        return "paused"
    if bundle_st in ("proposed", "active") or tcs == "bundled":
        return "inserted"
    if (arb_action or "") == "interrupt_then_resume" or "interrupt_then_resume" in sub:
        return "recovering"
    if isinstance(osi, dict):
        ss = (_s(osi.get("search_subtask_state")) or "").lower()
        if ss and ss not in ("none", "main", ""):
            return "subtask"
    if tcs in ("done", "cancelled"):
        return "main"
    if tcs == "active":
        return "main"
    return "unknown"


def build_task_chain_position_reason_summary(snap: Dict[str, Any], frame: Dict[str, Any]) -> str:
    """一句话说明当前任务在结构中的位置（解释用，非判定）。"""
    md = _s(snap.get("task_mode")) or "unknown"
    st = _s(snap.get("task_chain_stage")) or "—"
    sub = _s(snap.get("active_subtask_id"))
    rt = _s(snap.get("task_resume_target"))
    succ = _s(snap.get("task_success_criteria_summary")) or ""
    lane = "main_lane"
    if md == "subtask":
        lane = "subtask_lane"
    elif md == "inserted":
        lane = "inserted_branch_open"
    elif md == "recovering":
        lane = "recovery_lane"
    elif md == "paused":
        lane = "paused_or_hold"
    sub_note = f"subtask_focus={sub}" if sub else "no_active_subtask_label"
    resume_note = "resume_pending" if rt and "resume" in rt else ("resume_terminal_hint" if rt else "no_resume_hint")
    crit = "node_level_criteria" if "terminal=" in succ and md == "subtask" else "mixed_or_main_level"
    return f"lane={lane}; stage={st}; {sub_note}; {resume_note}; success_scope_hint={crit}"


def build_task_chain_position_event_summaries(snap: Dict[str, Any], frame: Dict[str, Any]) -> List[str]:
    """人类可读的事件摘要列表（与 timeline 类型对应）。"""
    out: List[str] = []
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else None
    term = (_s(osi.get("search_terminal_status")) if isinstance(osi, dict) else None) or "none"
    can_res = bool(isinstance(osi, dict) and osi.get("search_can_resume_main_task") is True)
    md = _s(snap.get("task_mode")) or "unknown"
    sub = _s(snap.get("active_subtask_id"))
    if sub:
        out.append(f"subtask_relationship:active_subtask={sub}")
    if _s(snap.get("task_resume_target")):
        out.append("resume_target_documented")
    if term == "found" and md == "subtask":
        out.append("node_terminal_signal_present")
    if term == "found" and can_res:
        out.append("local_success_may_not_close_main")
    if md == "recovering":
        out.append("recovery_path_requires_main_alignment")
    if md == "inserted":
        out.append("inserted_branch_active_check_exit")
    return out


def build_task_chain_warning_summary(snap: Dict[str, Any], frame: Dict[str, Any]) -> str:
    """轻量风险语义：非强判定。"""
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else None
    term = (_s(osi.get("search_terminal_status")) if isinstance(osi, dict) else None) or "none"
    can_res = bool(isinstance(osi, dict) and osi.get("search_can_resume_main_task") is True)
    md = _s(snap.get("task_mode")) or "unknown"
    if term == "found" and can_res and md == "subtask":
        return "local_success_without_confirmed_main_progress"
    if md == "recovering" and not _s(snap.get("task_resume_target")):
        return "pseudo_recovery_risk_resume_target_unclear"
    if md == "inserted" and term == "none":
        return "inserted_branch_may_not_have_exited"
    return "none"


def build_task_position_timeline_events(snap: Dict[str, Any], frame: Dict[str, Any]) -> List[Dict[str, str]]:
    """供时间轴注入的最小事件列表（类型 + 摘要）。"""
    events: List[Dict[str, str]] = []
    reason = _s(snap.get("task_position_reason_summary")) or build_task_chain_position_reason_summary(snap, frame)
    events.append({"event_type": "task_chain_position_interpreted", "summary": reason[:280]})

    sub = _s(snap.get("active_subtask_id"))
    if sub:
        events.append(
            {
                "event_type": "task_subtask_relationship_observed",
                "summary": f"active_subtask={sub}",
            }
        )

    rt = _s(snap.get("task_resume_target"))
    if rt:
        status = "active_pending" if "resume" in rt else "hint_only"
        events.append({"event_type": "task_resume_target_active", "summary": f"{status}:{rt[:160]}"})

    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else None
    term = (_s(osi.get("search_terminal_status")) if isinstance(osi, dict) else None) or "none"
    md = _s(snap.get("task_mode")) or "unknown"
    if term not in ("none", "") and md == "subtask":
        events.append({"event_type": "task_partial_progress_detected", "summary": f"terminal={term};scope=subtask"})

    can_res = bool(isinstance(osi, dict) and osi.get("search_can_resume_main_task") is True)
    if term == "found" and can_res:
        events.append(
            {
                "event_type": "task_local_success_without_main_progress",
                "summary": "terminal_found_with_resume_flag_main_may_not_be_done",
            }
        )

    if md == "recovering":
        events.append({"event_type": "task_recovery_path_visible", "summary": "mode=recovering_watch_main_alignment"})

    return events[:8]


def build_resume_main_progress_alignment_summary(snap: Dict[str, Any], frame: Dict[str, Any]) -> str:
    """
    Resume Progress Summary Alignment M0：显式、可匹配的一行（派生自已存在字段 + inputs 场景线索）。
    不拍板，仅提高同帧摘要可见性。
    """
    inputs = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    term = (_s(osi.get("search_terminal_status")) or "none").lower()
    md = _s(snap.get("task_mode")) or "unknown"
    rt = _s(snap.get("task_resume_target"))
    parts: List[str] = []
    if inputs.get("recovery_declared_but_resume_chain_fragile_expected"):
        parts.append("resume_chain_fragile_expected")
    if inputs.get("phase_correct_but_closure_semantics_misaligned_expected"):
        parts.append("closure_semantics_misaligned_expected")
    scen = _s(inputs.get("scenario_task_resume_target"))
    if scen and not rt:
        parts.append("scenario_resume_hint_pending_chain_merge")
    if rt:
        parts.append("resume_target_traced")
    if md in ("subtask", "recovering", "inserted") and term not in ("found", "cancelled"):
        parts.append("global_main_progress_not_terminal_complete")
    return "; ".join(parts) if parts else "none"


def enrich_task_chain_position_m01(base: TaskChainStateSnapshot, frame: Dict[str, Any]) -> TaskChainStateSnapshot:
    """M0.1：在最小快照上填充位置解释字段（不重算主字段）。"""
    d = base.to_dict()
    reason = build_task_chain_position_reason_summary(d, frame)
    ev_sum = build_task_chain_position_event_summaries(d, frame)
    warn = build_task_chain_warning_summary(d, frame)
    tl = build_task_position_timeline_events({**d, "task_position_reason_summary": reason}, frame)
    return replace(
        base,
        task_position_reason_summary=reason,
        task_position_event_summaries=ev_sum,
        task_position_warning_summary=warn,
        task_position_timeline_events=tl,
    )


def build_task_chain_state_snapshot(frame: Dict[str, Any]) -> TaskChainStateSnapshot:
    """
    从 frame 构建最小任务链快照；优先使用 environment_task_context_reserve.task_chain_context（若已存在）。
    """
    if not isinstance(frame, dict):
        return TaskChainStateSnapshot(task_chain_state_snapshot_applied=False)

    trace_anchor = _s(frame.get("trace_anchor_id"))
    inputs = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}
    seq = inputs.get("frame_seq")
    default_tc_id = trace_anchor or (f"tc_seq_{seq}" if seq is not None else "tc_unknown")

    goal = frame.get("goal") if isinstance(frame.get("goal"), dict) else {}
    gid = _s(goal.get("goal_id"))

    tcb = frame.get("task_chain_bridge") if isinstance(frame.get("task_chain_bridge"), dict) else None
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else None
    arb = frame.get("task_arbitration") if isinstance(frame.get("task_arbitration"), dict) else None
    arb_action = _s(arb.get("arbitration_action")) if isinstance(arb, dict) else None

    etc = frame.get("environment_task_context_reserve") if isinstance(frame.get("environment_task_context_reserve"), dict) else None
    tcc: Optional[Dict[str, Any]] = None
    if isinstance(etc, dict):
        tcc = etc.get("task_chain_context") if isinstance(etc.get("task_chain_context"), dict) else None

    task_chain_id = default_tc_id
    task_chain_stage: Optional[str] = None
    task_chain_context_summary: Optional[str] = None
    if isinstance(tcc, dict):
        task_chain_id = _s(tcc.get("task_chain_id")) or task_chain_id
        task_chain_stage = _s(tcc.get("task_chain_stage"))
        task_chain_context_summary = _s(tcc.get("task_chain_context_summary"))
    if not task_chain_stage and isinstance(tcb, dict):
        task_chain_stage = _s(tcb.get("task_chain_state")) or "active"
    if not task_chain_context_summary and isinstance(tcb, dict):
        task_chain_context_summary = _s(tcb.get("task_chain_summary_text"))

    primary_task_id = gid or (_s(arb.get("foreground_task_type")) if isinstance(arb, dict) else None) or "primary_unknown"

    active_subtask_id: Optional[str] = None
    if isinstance(osi, dict):
        active_subtask_id = _s(osi.get("search_target_label"))

    task_mode = _infer_task_mode(tcb, osi, arb_action)
    if task_mode == "unknown" and task_chain_stage:
        task_mode = "main"

    task_resume_target: Optional[str] = None
    if isinstance(osi, dict):
        if osi.get("search_can_resume_main_task") is True:
            task_resume_target = "resume_primary_search_or_main_task"
        term = _s(osi.get("search_terminal_status"))
        if term in ("found", "cancelled"):
            task_resume_target = task_resume_target or f"terminal={term}"

    hint_rt = _s(inputs.get("scenario_task_resume_target")) if isinstance(inputs, dict) else None
    if hint_rt and not task_resume_target:
        task_resume_target = hint_rt

    task_success_criteria_summary: Optional[str] = None
    if isinstance(osi, dict):
        term = _s(osi.get("search_terminal_status")) or "none"
        lvl = _s(osi.get("search_result_level"))
        task_success_criteria_summary = f"terminal={term}" + (f";level={lvl}" if lvl else "")

    base = TaskChainStateSnapshot(
        task_chain_id=task_chain_id,
        task_chain_stage=task_chain_stage or "unknown",
        primary_task_id=primary_task_id,
        active_subtask_id=active_subtask_id,
        task_mode=task_mode if task_mode in TASK_MODES else "unknown",
        task_resume_target=task_resume_target,
        task_success_criteria_summary=task_success_criteria_summary,
        task_chain_context_summary=task_chain_context_summary,
        task_chain_state_snapshot_applied=True,
    )
    align = build_resume_main_progress_alignment_summary(base.to_dict(), frame)
    base = replace(base, resume_main_progress_alignment_summary=align)
    return enrich_task_chain_position_m01(base, frame)


def build_task_chain_progress_summary(snapshot: Dict[str, Any]) -> str:
    """供 run_summary / 聚合层：区分主任务推进 vs 局部成功 vs 恢复/插入语义。"""
    if not isinstance(snapshot, dict) or not snapshot.get("task_chain_state_snapshot_applied"):
        return "task_chain: unavailable"
    st = _s(snapshot.get("task_chain_stage")) or "—"
    md = _s(snapshot.get("task_mode")) or "—"
    sub_raw = _s(snapshot.get("active_subtask_id"))
    sub = sub_raw or "—"
    resume = _s(snapshot.get("task_resume_target")) or "—"
    succ = _s(snapshot.get("task_success_criteria_summary")) or "—"
    warn = _s(snapshot.get("task_position_warning_summary")) or "none"
    reason_short = (_s(snapshot.get("task_position_reason_summary")) or "")[:120]
    main_push = md == "main" and not sub_raw
    local_only = md == "subtask" or any(
        x in warn for x in ("local_success", "pseudo_recovery", "inserted_branch")
    )
    inserted_open = md == "inserted"
    recovering = md == "recovering"
    parts = [
        f"stage={st}",
        f"mode={md}",
        f"subtask={sub}",
        f"resume={resume}",
        f"success_hint={succ}",
        f"main_push_hint={'yes' if main_push else 'mixed'}",
        f"local_only_risk={'yes' if local_only else 'no'}",
        f"inserted_open={'yes' if inserted_open else 'no'}",
        f"recovering={'yes' if recovering else 'no'}",
        f"warn={warn}",
    ]
    if reason_short:
        parts.append(f"pos={reason_short}")
    rms = _s(snapshot.get("resume_main_progress_alignment_summary")) or "none"
    if rms != "none":
        parts.append(f"resume_main_align={rms}")
    return "; ".join(parts)[:900]
