# -*- coding: utf-8 -*-
"""
Reasoning Timeline View M0（推理时间轴视图）

定位（写死）：
- 结构树：表达分支/排除/收敛关系
- 时间轴：表达先后顺序/关键转折/状态切换
- 两者并列视角；时间轴只读主线输出，不重算主逻辑

M0：按逻辑顺序生成事件序列（event_index），不做真实时间戳系统。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _get(d: Any, *keys: str) -> Any:
    cur = d
    for k in keys:
        if cur is None:
            return None
        if isinstance(cur, dict):
            cur = cur.get(k)
        else:
            cur = getattr(cur, k, None)
    return cur


EVENT_TYPES = (
    "flow_entered",
    "hypothesis_selected",
    "path_switched",
    "feedback_received",
    "issue_detected",
    "quality_changed",
    "fallback_triggered",
    "optimization_hint_generated",
    "validation_result_changed",
    "continuity_changed",
    "resolution_updated",
    "context_premise_recorded",
    "contamination_guard_reserved",
    "post_processing_reserved",
    "scheduled_source_state_formed",
    "dominant_source_selected",
    "source_conflict_detected",
    "priority_override_applied",
    "dynamic_source_overrode_static_source",
    "memory_source_overrode_observation",
    "task_source_became_dominant",
    "task_chain_state_snapshot_formed",
    "task_mode_detected",
    "task_resume_target_present",
    # M0.1 任务链位置解释（与 task_position_timeline_events 对齐）
    "task_chain_position_interpreted",
    "task_subtask_relationship_observed",
    "task_resume_target_active",
    "task_partial_progress_detected",
    "task_local_success_without_main_progress",
    "task_recovery_path_visible",
    # M0.3 记忆调用解释
    "memory_invocation_explained",
    "memory_invocation_supports_mainline",
    "memory_invocation_risk_detected",
    "memory_invocation_conflict_with_observation",
    # M0.4 主链状态/阶段显式化
    "mainline_state_snapshot_formed",
    "mainline_phase_identified",
    "mainline_state_transition_observed",
    # M1.1.x-A process observation anchors
    "resume_chain_declared",
    "resume_chain_not_progressing_main",
    "resume_chain_fragility_detected",
    "memory_bias_accumulation_detected",
    "memory_bias_overrode_observation_tendency",
    "memory_bias_requires_conservative_repair",
    "phase_identified_but_closure_misaligned",
    "closure_semantics_repair_candidate",
)


@dataclass
class ReasoningTimelineEvent:
    event_index: int
    event_type: str
    event_summary: str
    event_source_module: Optional[str] = None
    event_importance: str = "low"  # high / medium / low
    related_node_id: Optional[str] = None
    related_issue_type: Optional[str] = None
    related_quality_flag: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_index": int(self.event_index),
            "event_type": self.event_type,
            "event_summary": self.event_summary,
            "event_source_module": self.event_source_module,
            "event_importance": self.event_importance,
            "related_node_id": self.related_node_id,
            "related_issue_type": self.related_issue_type,
            "related_quality_flag": self.related_quality_flag,
        }


@dataclass
class ReasoningTimelineViewResult:
    events: List[ReasoningTimelineEvent] = field(default_factory=list)
    key_transition_count: int = 0
    key_transition_summary: Optional[str] = None
    timeline_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "events": [e.to_dict() for e in self.events],
            "key_transition_count": int(self.key_transition_count),
            "key_transition_summary": self.key_transition_summary,
            "timeline_applied": bool(self.timeline_applied),
        }


def _importance(event_type: str) -> str:
    if event_type in ("path_switched", "fallback_triggered", "issue_detected", "resolution_updated", "validation_result_changed"):
        return "high"
    if event_type in ("hypothesis_selected", "feedback_received", "continuity_changed", "optimization_hint_generated"):
        return "medium"
    return "low"


def build_reasoning_timeline_view(frame: Dict[str, Any]) -> ReasoningTimelineViewResult:
    """
    抽取规则（M0）：
    - 事件来自：flow/hypothesis/tree/metrics/quality/recheck/feedback/optimization/continuity/resolution
    - 按固定逻辑顺序生成；缺失则跳过
    """
    if not isinstance(frame, dict):
        return ReasoningTimelineViewResult(timeline_applied=False, key_transition_summary="invalid frame")

    events: List[ReasoningTimelineEvent] = []
    idx = 0

    def add(
        event_type: str,
        summary: str,
        source: Optional[str],
        *,
        related_node_id: Optional[str] = None,
        related_issue_type: Optional[str] = None,
        related_quality_flag: Optional[str] = None,
    ) -> None:
        nonlocal idx
        idx += 1
        events.append(
            ReasoningTimelineEvent(
                event_index=idx,
                event_type=event_type,
                event_summary=summary,
                event_source_module=source,
                event_importance=_importance(event_type),
                related_node_id=related_node_id,
                related_issue_type=related_issue_type,
                related_quality_flag=related_quality_flag,
            )
        )

    # 1) flow_entered
    flow = _s(_get(frame, "object_search_interaction", "interaction_flow_type")) or _s(
        _get(frame, "confirmation_input_bridge", "confirmation_bridge_target_flow")
    )
    if flow:
        add("flow_entered", f"flow_entered: {flow}", "object_search_interaction")

    # 2) hypothesis_selected
    hyp0 = None
    hyps = _get(frame, "hypothesis_layer", "hypotheses")
    if isinstance(hyps, list) and hyps:
        hyp0 = hyps[0] if isinstance(hyps[0], dict) else None
    hyp_sum = _s(_get(hyp0, "hypothesis_summary")) if isinstance(hyp0, dict) else None
    hyp_type = _s(_get(hyp0, "hypothesis_type")) if isinstance(hyp0, dict) else None
    if hyp_sum or hyp_type:
        add("hypothesis_selected", f"hypothesis_selected: {hyp_type or '—'} · {hyp_sum or ''}".strip(), "hypothesis_layer")

    # 2.5) memory vs novel channel (M0): summarize dominant channels as event (low/medium importance)
    mn = frame.get("memory_novel_information_channel") if isinstance(frame.get("memory_novel_information_channel"), dict) else None
    if mn:
        dom_r = _s(_get(mn, "dominant_reasoning_channel"))
        dom_d = _s(_get(mn, "dominant_decision_channel"))
        if dom_r or dom_d:
            add(
                "flow_entered",
                f"info_channel: reasoning={dom_r or '—'} decision={dom_d or '—'}",
                "memory_novel_information_channel",
            )
        cand = _get(mn, "novel_memory_candidate")
        if isinstance(cand, dict) and _s(cand.get("candidate_label")):
            add(
                "quality_changed",
                f"novel_memory_candidate: {cand.get('candidate_label')} · ready={cand.get('candidate_ready_for_memory')}",
                "memory_novel_information_channel",
            )

    # 3) path_switched (M0: if continuity broken or feedback-driven active path exists)
    cont = frame.get("spatiotemporal_continuity_reserve") if isinstance(frame.get("spatiotemporal_continuity_reserve"), dict) else None
    cont_lvl = _s(_get(cont, "continuity_support_level")) if isinstance(cont, dict) else None
    cont_broken = bool(_get(cont, "continuity_broken") is True) if isinstance(cont, dict) else False
    if cont_broken:
        add("path_switched", "path_switched: continuity broken triggered path change", "spatiotemporal_continuity_reserve")

    # 4) feedback_received
    fb_raw = _s(_get(frame, "confirmation_input_bridge", "confirmation_input_raw_text"))
    fb_type = _s(_get(frame, "confirmation_input_bridge", "confirmation_input_type"))
    if fb_raw or fb_type:
        add("feedback_received", f"feedback_received: {fb_type or '—'} · {fb_raw or ''}".strip(), "confirmation_input_bridge")

    # 5) continuity_changed (M0: emit current state as event)
    if cont_lvl:
        inf = _s(_get(cont, "continuity_influence_reason")) if isinstance(cont, dict) else None
        add("continuity_changed", f"continuity: {cont_lvl}" + (f" · {inf}" if inf else ""), "spatiotemporal_continuity_reserve")

    # 6) issue_detected
    metrics = frame.get("reasoning_tree_metrics") if isinstance(frame.get("reasoning_tree_metrics"), dict) else None
    issue = _s(_get(metrics, "possible_tree_issue_type")) if isinstance(metrics, dict) else None
    if issue:
        reason = _s(_get(metrics, "possible_tree_issue_reason")) if isinstance(metrics, dict) else None
        add("issue_detected", f"issue_detected: {issue}" + (f" · {reason}" if reason else ""), "reasoning_tree_metrics", related_issue_type=issue)

    # 7) fallback_triggered
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else None
    r_action = _s(_get(rp, "recheck_action")) if isinstance(rp, dict) else None
    r_reason = _s(_get(rp, "recheck_reason")) if isinstance(rp, dict) else None
    if r_action in ("hold_and_confirm", "ask_user_for_clarification"):
        add("fallback_triggered", f"fallback_triggered: {r_action}" + (f" · {r_reason}" if r_reason else ""), "recheck_planner")

    # 8) quality_changed (M0: emit current grade as event)
    qo = frame.get("reasoning_tree_quality_overlay") if isinstance(frame.get("reasoning_tree_quality_overlay"), dict) else None
    grade = _s(_get(qo, "quality_grade")) if isinstance(qo, dict) else None
    if grade:
        qsum = _s(_get(qo, "quality_summary")) if isinstance(qo, dict) else None
        add("quality_changed", f"quality: {grade}" + (f" · {qsum}" if qsum else ""), "reasoning_tree_quality_overlay")

    # 9) optimization_hint_generated
    oh = frame.get("optimization_hint") if isinstance(frame.get("optimization_hint"), dict) else None
    oh_type = _s(_get(oh, "optimization_hint_type")) if isinstance(oh, dict) else None
    if oh_type and oh_type != "none":
        mod = _s(_get(oh, "suggested_optimization_module")) if isinstance(oh, dict) else None
        add("optimization_hint_generated", f"optimization_hint: {oh_type}" + (f" · module={mod}" if mod else ""), "optimization_hint")

    # 10) validation_result_changed (M0: emit current validation result)
    ofl = frame.get("optimization_feedback_loop") if isinstance(frame.get("optimization_feedback_loop"), dict) else None
    vr = _s(_get(ofl, "validation_result")) if isinstance(ofl, dict) else None
    if vr and vr != "not_applicable":
        add("validation_result_changed", f"validation: {vr}", "optimization_feedback_loop")

    # 11) resolution_updated
    term = _s(_get(frame, "object_search_interaction", "search_terminal_status"))
    blocked = bool(_get(metrics, "blocked") is True) if isinstance(metrics, dict) else False
    resolved = bool(_get(metrics, "resolved") is True) if isinstance(metrics, dict) else False
    if term or blocked or resolved:
        add(
            "resolution_updated",
            "resolution_updated: "
            + ("resolved" if resolved else ("blocked" if blocked else "unresolved"))
            + (f" · terminal={term}" if term else ""),
            "reasoning_tree_metrics",
            related_issue_type=issue,
        )

    # key transition summary (top 1~3 high importance events)
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else None)

    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=True,
    )


def append_context_premise_event(
    view: ReasoningTimelineViewResult,
    premise_summary: Optional[str],
) -> ReasoningTimelineViewResult:
    """
    在已有时间轴末尾追加一条「前提条件」摘要事件（M0）。
    由 builder 在 environment_task_context_reserve 生成后调用。
    """
    if not premise_summary or not str(premise_summary).strip():
        return view
    text = str(premise_summary).strip()
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    events.append(
        ReasoningTimelineEvent(
            event_index=nxt,
            event_type="context_premise_recorded",
            event_summary=f"context premise: {text[:240]}",
            event_source_module="environment_task_context_reserve",
            event_importance="low",
        )
    )
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_contamination_guard_event(
    view: ReasoningTimelineViewResult,
    observation_summary: Optional[str],
) -> ReasoningTimelineViewResult:
    """在已有时间轴末尾追加一条污染观察占位事件（M0）。由 builder 在 decision_contamination_guard_reserve 生成后调用。"""
    if not observation_summary or not str(observation_summary).strip():
        return view
    text = str(observation_summary).strip()
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    events.append(
        ReasoningTimelineEvent(
            event_index=nxt,
            event_type="contamination_guard_reserved",
            event_summary=f"contamination_guard_reserved: {text[:240]}",
            event_source_module="decision_contamination_guard_reserve",
            event_importance="low",
        )
    )
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_post_processing_reserved_event(
    view: ReasoningTimelineViewResult,
    summary_text: Optional[str],
) -> ReasoningTimelineViewResult:
    """在已有时间轴末尾追加一条后置信息处理占位事件（M0）。由 builder 在 post_processing_intelligence_reserve 生成后调用。"""
    if not summary_text or not str(summary_text).strip():
        return view
    text = str(summary_text).strip()
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    events.append(
        ReasoningTimelineEvent(
            event_index=nxt,
            event_type="post_processing_reserved",
            event_summary=f"post_processing_reserved: {text[:240]}",
            event_source_module="post_processing_intelligence_reserve",
            event_importance="low",
        )
    )
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_task_chain_snapshot_event(
    view: ReasoningTimelineViewResult,
    task_chain_state_snapshot: Optional[Dict[str, Any]],
) -> ReasoningTimelineViewResult:
    """在已有时间轴末尾追加任务链快照相关事件（M0）。"""
    if not isinstance(task_chain_state_snapshot, dict):
        return view
    if not task_chain_state_snapshot.get("task_chain_state_snapshot_applied"):
        return view
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    stg = _s(task_chain_state_snapshot.get("task_chain_stage")) or "—"
    md = _s(task_chain_state_snapshot.get("task_mode")) or "—"
    events.append(
        ReasoningTimelineEvent(
            event_index=nxt,
            event_type="task_chain_state_snapshot_formed",
            event_summary=f"task_chain_state_snapshot_formed: stage={stg} mode={md}",
            event_source_module="task_chain_state_snapshot",
            event_importance="low",
        )
    )
    nxt += 1
    events.append(
        ReasoningTimelineEvent(
            event_index=nxt,
            event_type="task_mode_detected",
            event_summary=f"task_mode_detected: {md}",
            event_source_module="task_chain_state_snapshot",
            event_importance="low",
        )
    )
    nxt += 1
    rt = _s(task_chain_state_snapshot.get("task_resume_target"))
    if rt:
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="task_resume_target_present",
                event_summary=f"task_resume_target_present: {rt[:200]}",
                event_source_module="task_chain_state_snapshot",
                event_importance="low",
            )
        )
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_task_chain_position_explanation_events(
    view: ReasoningTimelineViewResult,
    task_chain_state_snapshot: Optional[Dict[str, Any]],
) -> ReasoningTimelineViewResult:
    """
    M0.1：将 task_position_timeline_events 注入时间轴（解释用；不替代主链状态机）。
    """
    if not isinstance(task_chain_state_snapshot, dict):
        return view
    if not task_chain_state_snapshot.get("task_chain_state_snapshot_applied"):
        return view
    tl = task_chain_state_snapshot.get("task_position_timeline_events") or []
    if not isinstance(tl, list) or not tl:
        return view
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    medium_types = {
        "task_local_success_without_main_progress",
        "task_recovery_path_visible",
        "task_partial_progress_detected",
    }
    for item in tl[:8]:
        if not isinstance(item, dict):
            continue
        et = _s(item.get("event_type"))
        sm = _s(item.get("summary")) or ""
        if not et:
            continue
        imp = "medium" if et in medium_types else "low"
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type=et,
                event_summary=f"{et}: {sm[:220]}",
                event_source_module="task_chain_state_snapshot",
                event_importance=imp,
            )
        )
        nxt += 1
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_memory_invocation_explanation_events(
    view: ReasoningTimelineViewResult,
    memory_invocation_explanation: Optional[Dict[str, Any]],
) -> ReasoningTimelineViewResult:
    """M0.3：将 memory_invocation_timeline_events 注入时间轴（解释用，不判定记忆正确性）。"""
    if not isinstance(memory_invocation_explanation, dict):
        return view
    if not memory_invocation_explanation.get("memory_invocation_explanation_applied"):
        return view
    tl = memory_invocation_explanation.get("memory_invocation_timeline_events") or []
    if not isinstance(tl, list) or not tl:
        return view
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    risk_types = {"memory_invocation_risk_detected", "memory_invocation_conflict_with_observation"}
    for item in tl[:6]:
        if not isinstance(item, dict):
            continue
        et = _s(item.get("event_type"))
        sm = _s(item.get("summary")) or ""
        if not et:
            continue
        imp = "medium" if et in risk_types or et == "memory_invocation_supports_mainline" else "low"
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type=et,
                event_summary=f"{et}: {sm[:220]}",
                event_source_module="memory_invocation_explanation",
                event_importance=imp,
            )
        )
        nxt += 1
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_mainline_state_snapshot_events(
    view: ReasoningTimelineViewResult,
    mainline_state_snapshot: Optional[Dict[str, Any]],
) -> ReasoningTimelineViewResult:
    """M0.4：注入主链状态/阶段显式化事件（只读推导，不替代拍板）。"""
    if not isinstance(mainline_state_snapshot, dict):
        return view
    if not mainline_state_snapshot.get("mainline_state_snapshot_applied"):
        return view
    tl = mainline_state_snapshot.get("mainline_state_timeline_events") or []
    if not isinstance(tl, list) or not tl:
        return view
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    for item in tl[:5]:
        if not isinstance(item, dict):
            continue
        et = _s(item.get("event_type"))
        sm = _s(item.get("summary")) or ""
        if not et:
            continue
        imp = "low"
        if et == "mainline_state_transition_observed":
            imp = "medium"
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type=et,
                event_summary=f"{et}: {sm[:220]}",
                event_source_module="mainline_state_snapshot",
                event_importance=imp,
            )
        )
        nxt += 1
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_scheduled_source_state_event(
    view: ReasoningTimelineViewResult,
    scheduled_source_state: Optional[Dict[str, Any]],
) -> ReasoningTimelineViewResult:
    """在已有时间轴末尾追加调度层形成与关键事件（M0.1）。"""
    if not isinstance(scheduled_source_state, dict):
        return view
    dominant_source = scheduled_source_state.get("dominant_source")
    if not dominant_source or not str(dominant_source).strip():
        return view
    text = str(dominant_source).strip()
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1
    to_add: List[tuple[str, str]] = [
        ("scheduled_source_state_formed", f"scheduled_source_state_formed: source={text[:120]}"),
        ("dominant_source_selected", f"dominant_source_selected: {text[:120]}"),
    ]
    conflict = _s(scheduled_source_state.get("source_conflict_summary")) or "none"
    if conflict not in ("none", "unknown"):
        to_add.append(("source_conflict_detected", f"source_conflict_detected: {conflict}"))
    over = _s(scheduled_source_state.get("priority_override_summary")) or "none"
    if over not in ("none", "unknown"):
        to_add.append(("priority_override_applied", f"priority_override_applied: {over}"))
        if over == "dynamic_over_static":
            to_add.append(("dynamic_source_overrode_static_source", "dynamic_source_overrode_static_source"))
    if text == "memory_recall":
        to_add.append(("memory_source_overrode_observation", "memory_source_overrode_observation"))
    if text == "task_state":
        to_add.append(("task_source_became_dominant", "task_source_became_dominant"))

    for et, summary in to_add[:4]:
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type=et,
                event_summary=summary,
                event_source_module="information_source_scheduler",
                event_importance="low",
            )
        )
        nxt += 1
    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )


def append_m11x_process_observation_events(
    view: ReasoningTimelineViewResult,
    run_summary_reference: Optional[Dict[str, Any]],
) -> ReasoningTimelineViewResult:
    """M1.1.x-A：将过程观察锚点注入 timeline（仅显影，不改决策）。"""
    if not isinstance(run_summary_reference, dict):
        return view
    proc = _s(run_summary_reference.get("process_observation_summary"))
    if not proc:
        return view
    events = list(view.events)
    nxt = max((e.event_index for e in events), default=0) + 1

    resume_stage = _s(run_summary_reference.get("resume_chain_stage_summary")) or ""
    resume_frag = _s(run_summary_reference.get("resume_chain_fragility_summary")) or "none"
    resume_main = run_summary_reference.get("resume_chain_progress_reached_main")
    mem_acc = _s(run_summary_reference.get("memory_bias_accumulation_summary")) or "none"
    mem_shift = _s(run_summary_reference.get("memory_bias_weight_shift_summary")) or "none"
    phase_clo = _s(run_summary_reference.get("phase_closure_alignment_summary")) or ""
    clo_mis = _s(run_summary_reference.get("closure_semantics_misalignment_summary")) or "none"

    if resume_stage:
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="resume_chain_declared",
                event_summary=f"resume_chain_declared: {resume_stage[:220]}",
                event_source_module="run_summary_builder",
                event_importance="low",
            )
        )
        nxt += 1
    if resume_main is False:
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="resume_chain_not_progressing_main",
                event_summary=f"resume_chain_not_progressing_main: frag={resume_frag[:140]}",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )
        nxt += 1
    if resume_frag and resume_frag != "none":
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="resume_chain_fragility_detected",
                event_summary=f"resume_chain_fragility_detected: {resume_frag[:180]}",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )
        nxt += 1
    if mem_acc and mem_acc != "none":
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="memory_bias_accumulation_detected",
                event_summary=f"memory_bias_accumulation_detected: {mem_acc[:220]}",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )
        nxt += 1
    if mem_shift and mem_shift != "none":
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="memory_bias_overrode_observation_tendency",
                event_summary=f"memory_bias_overrode_observation_tendency: {mem_shift[:220]}",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )
        nxt += 1
    if "conflict" in mem_acc.lower() or "overweight" in mem_acc.lower():
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="memory_bias_requires_conservative_repair",
                event_summary="memory_bias_requires_conservative_repair: memory-observation conflict visible",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )
        nxt += 1
    if clo_mis and clo_mis != "none":
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="phase_identified_but_closure_misaligned",
                event_summary=f"phase_identified_but_closure_misaligned: {phase_clo[:220]}",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )
        nxt += 1
        events.append(
            ReasoningTimelineEvent(
                event_index=nxt,
                event_type="closure_semantics_repair_candidate",
                event_summary=f"closure_semantics_repair_candidate: {clo_mis[:180]}",
                event_source_module="run_summary_builder",
                event_importance="medium",
            )
        )

    high = [e for e in events if e.event_importance == "high"]
    key_cnt = len(high)
    key_summ = "；".join([e.event_summary for e in high[:3]]) if high else (events[-1].event_summary if events else view.key_transition_summary)
    return ReasoningTimelineViewResult(
        events=events,
        key_transition_count=key_cnt,
        key_transition_summary=key_summ,
        timeline_applied=bool(view.timeline_applied),
    )

