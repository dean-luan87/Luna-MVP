# -*- coding: utf-8 -*-
"""
Run Summary Reference M0.2（运行总结入口最小工程对象）

定位：
- 从已落地的 frame（主链事实、白盒、时间轴事件、调度状态等）生成轻量 summary reference
- 形成「运行总结链」在工程上的最小独立入口，不做深总结算法
- Summary 必须派生自已存在的 trace/event 信息，不得替代 Raw Trace

与三层日志语义对齐：
- Raw Trace：主链层原始事实切片（黑匣子语义）
- Structured Event：时间轴等结构化事件切片
- Summary Reference：供后处理 / 图书馆 future 的轻摘要入口（Derived from Trace）
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .information_source_scheduler import build_source_scheduling_summary
from .task_chain_state_snapshot import build_task_chain_progress_summary
from .memory_invocation_explanation import build_memory_usage_summary_line
from .mainline_state_snapshot import build_mainline_state_summary_line
from .mainline_narrative_alignment import build_narrative_brief


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


def build_raw_trace_slice(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    黑匣子语义：从 frame 抽取最小「原始运行事实」切片（非总结、非解释）。
    """
    if not isinstance(frame, dict):
        return {"layer": "raw_trace", "trace_anchor_id": None, "invalid_frame": True}
    inputs = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}
    goal = frame.get("goal") if isinstance(frame.get("goal"), dict) else {}
    state = frame.get("state") if isinstance(frame.get("state"), dict) else {}
    decision = frame.get("decision") if isinstance(frame.get("decision"), dict) else {}
    outputs = frame.get("outputs") if isinstance(frame.get("outputs"), dict) else {}
    cons = frame.get("consequence") if isinstance(frame.get("consequence"), dict) else {}
    return {
        "layer": "raw_trace",
        "trace_anchor_id": frame.get("trace_anchor_id"),
        "frame_seq": inputs.get("frame_seq"),
        "current_ts": inputs.get("current_ts"),
        "route": inputs.get("route"),
        "raw_observation_summary": inputs.get("raw_observation_summary"),
        "goal_type": goal.get("goal_type"),
        "goal_status": goal.get("goal_status"),
        "risk_score": state.get("risk_score"),
        "safety_level": state.get("safety_level"),
        "decision_owner": decision.get("decision_owner"),
        "decision_type": decision.get("decision_type"),
        "action_summary": outputs.get("action_summary"),
        "expected_risk": cons.get("expected_risk"),
    }


def build_structured_event_slice(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    结构化事件语义：从 reasoning_timeline_view 等抽取事件层摘要（仍属日志链，非自由生成总结）。
    """
    if not isinstance(frame, dict):
        return {"layer": "structured_event", "event_count": 0}
    tv = frame.get("reasoning_timeline_view")
    if tv is not None and hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    if not isinstance(tv, dict):
        tv = {}
    events = tv.get("events") or []
    if not isinstance(events, list):
        events = []
    types: List[str] = []
    for e in events:
        if isinstance(e, dict) and e.get("event_type"):
            types.append(str(e["event_type"]))
    distinct: List[str] = []
    seen = set()
    for t in types:
        if t not in seen:
            seen.add(t)
            distinct.append(t)
    return {
        "layer": "structured_event",
        "event_count": len(events),
        "distinct_event_types": distinct[:16],
        "key_transition_summary": tv.get("key_transition_summary"),
        "key_transition_count": tv.get("key_transition_count"),
        "timeline_applied": tv.get("timeline_applied"),
    }


@dataclass
class RunSummaryReference:
    summary_id: Optional[str] = None
    summary_brief: Optional[str] = None
    mainline_summary: Optional[str] = None
    memory_usage_summary: Optional[str] = None
    source_scheduling_summary: Optional[str] = None
    issue_or_risk_summary: Optional[str] = None
    summary_reference_applied: bool = False
    raw_trace_layer_snapshot: Dict[str, Any] = field(default_factory=dict)
    structured_event_layer_snapshot: Dict[str, Any] = field(default_factory=dict)
    task_chain_progress_summary: Optional[str] = None
    mainline_state_summary: Optional[str] = None
    mainline_narrative_brief: Optional[str] = None
    # M1.1.x-A: 过程观察锚点（只读显影，不改收口规则）
    process_observation_summary: Optional[str] = None
    resume_chain_stage_summary: Optional[str] = None
    resume_chain_fragility_summary: Optional[str] = None
    resume_chain_progress_reached_main: Optional[bool] = None
    memory_bias_accumulation_summary: Optional[str] = None
    memory_bias_weight_shift_summary: Optional[str] = None
    memory_bias_conflict_stage_summary: Optional[str] = None
    phase_closure_alignment_summary: Optional[str] = None
    closure_semantics_misalignment_summary: Optional[str] = None
    summary_feed_note: str = "summary_feed_derived_from_trace_not_substitute"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "summary_brief": self.summary_brief,
            "mainline_summary": self.mainline_summary,
            "memory_usage_summary": self.memory_usage_summary,
            "source_scheduling_summary": self.source_scheduling_summary,
            "issue_or_risk_summary": self.issue_or_risk_summary,
            "summary_reference_applied": bool(self.summary_reference_applied),
            "raw_trace_layer_snapshot": dict(self.raw_trace_layer_snapshot),
            "structured_event_layer_snapshot": dict(self.structured_event_layer_snapshot),
            "task_chain_progress_summary": self.task_chain_progress_summary,
            "mainline_state_summary": self.mainline_state_summary,
            "mainline_narrative_brief": self.mainline_narrative_brief,
            "process_observation_summary": self.process_observation_summary,
            "resume_chain_stage_summary": self.resume_chain_stage_summary,
            "resume_chain_fragility_summary": self.resume_chain_fragility_summary,
            "resume_chain_progress_reached_main": self.resume_chain_progress_reached_main,
            "memory_bias_accumulation_summary": self.memory_bias_accumulation_summary,
            "memory_bias_weight_shift_summary": self.memory_bias_weight_shift_summary,
            "memory_bias_conflict_stage_summary": self.memory_bias_conflict_stage_summary,
            "phase_closure_alignment_summary": self.phase_closure_alignment_summary,
            "closure_semantics_misalignment_summary": self.closure_semantics_misalignment_summary,
            "summary_feed_note": self.summary_feed_note,
        }


def _build_process_observation(frame: Dict[str, Any]) -> Dict[str, Any]:
    """M1.1.x-A 过程显影：R60/R61/R64 只读锚点。"""
    if not isinstance(frame, dict):
        return {}
    tcs = frame.get("task_chain_state_snapshot") if isinstance(frame.get("task_chain_state_snapshot"), dict) else {}
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    mie = frame.get("memory_invocation_explanation") if isinstance(frame.get("memory_invocation_explanation"), dict) else {}
    mss = frame.get("mainline_state_snapshot") if isinstance(frame.get("mainline_state_snapshot"), dict) else {}
    sss = frame.get("scheduled_source_state") if isinstance(frame.get("scheduled_source_state"), dict) else {}
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    ctx_flags = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}

    resume_target = _s(tcs.get("task_resume_target"))
    task_mode = _s(tcs.get("task_mode")) or "unknown"
    task_stage = _s(tcs.get("task_chain_stage")) or "unknown"
    recheck_action = _s(rp.get("recheck_action")) or "none"
    terminal = _s(osi.get("search_terminal_status")) or "none"
    phase = _s(mss.get("mainline_phase")) or "unknown"
    effect = _s(cib.get("confirmation_bridge_next_effect")) or "none"
    mem_effect = _s(mie.get("memory_invocation_effect_summary")) or "unknown"
    source_override = _s(sss.get("priority_override_summary")) or "none"
    source_conflict = _s(sss.get("source_conflict_summary")) or "none"

    resume_progress_main = bool(
        task_mode == "main"
        and terminal in ("found", "cancelled")
        and effect not in ("none", "uncertain")
    )
    resume_frag = "none"
    if resume_target and not resume_progress_main and task_mode in ("subtask", "recovering", "inserted"):
        resume_frag = "resume_declared_but_main_not_progressed"
    elif resume_target and recheck_action in ("ask_user_for_clarification", "hold_and_confirm"):
        resume_frag = "resume_chain_waiting_clarification"

    mem_bias_stage = "none"
    if mem_effect in ("supports_mainline", "overweight_memory", "memory_vs_observation_conflict"):
        mem_bias_stage = f"memory_effect={mem_effect}"
    if source_conflict in ("memory_vs_observation", "multiple"):
        mem_bias_stage = f"{mem_bias_stage}|source_conflict={source_conflict}" if mem_bias_stage != "none" else f"source_conflict={source_conflict}"
    mem_bias_shift = "none"
    if mem_effect == "supports_mainline" and source_override in ("dynamic_over_static", "task_over_memory"):
        mem_bias_shift = f"memory_support_under_override({source_override})"
    elif "memory" in source_override or "memory" in mem_effect:
        mem_bias_shift = f"memory_weight_shift_hint(override={source_override})"

    phase_closure = f"phase={phase}; closure_effect={effect}; recheck={recheck_action}; terminal={terminal}"
    closure_mis = "none"
    if phase == "recheck_or_repair" and effect == "none" and terminal == "none":
        closure_mis = "phase_repair_visible_but_closure_still_none"
    elif phase == "closure" and terminal == "none" and recheck_action in ("ask_user_for_clarification", "hold_and_confirm"):
        closure_mis = "closure_named_but_still_repair_path"

    proc = (
        f"resume_frag={resume_frag}; "
        f"memory_bias_stage={mem_bias_stage}; "
        f"phase_closure={closure_mis if closure_mis != 'none' else 'aligned_or_unknown'}"
    )
    # 用 ctx expected flag 只做锚点标注，避免误判为通用规则
    if any(
        bool(ctx_flags.get(k))
        for k in (
            "recovery_declared_but_resume_chain_fragile_expected",
            "memory_bias_accumulated_under_familiar_context_expected",
            "phase_correct_but_closure_semantics_misaligned_expected",
        )
    ):
        proc = "m11x_ctx_observed; " + proc

    return {
        "process_observation_summary": proc[:420],
        "resume_chain_stage_summary": f"stage={task_stage}; mode={task_mode}; resume_target={resume_target or 'none'}; recheck={recheck_action}; terminal={terminal}"[:300],
        "resume_chain_fragility_summary": resume_frag[:180],
        "resume_chain_progress_reached_main": resume_progress_main,
        "memory_bias_accumulation_summary": mem_bias_stage[:260],
        "memory_bias_weight_shift_summary": mem_bias_shift[:220],
        "memory_bias_conflict_stage_summary": f"mem_effect={mem_effect}; source_conflict={source_conflict}; source_override={source_override}"[:280],
        "phase_closure_alignment_summary": phase_closure[:280],
        "closure_semantics_misalignment_summary": closure_mis[:180],
    }


def build_run_summary_reference(frame: Dict[str, Any]) -> RunSummaryReference:
    """
    从完整 frame 构建 run_summary_reference；仅聚合已有字段，不发明主链事实。
    """
    if not isinstance(frame, dict):
        return RunSummaryReference(summary_reference_applied=False)

    raw = build_raw_trace_slice(frame)
    ev = build_structured_event_slice(frame)

    mi = frame.get("mainline_integration") if isinstance(frame.get("mainline_integration"), dict) else {}
    mainline_summary = _s(mi.get("integration_summary")) or ""

    memory_usage_summary = build_memory_usage_summary_line(frame)

    sss = frame.get("scheduled_source_state") if isinstance(frame.get("scheduled_source_state"), dict) else None
    source_scheduling_summary = ""
    if isinstance(sss, dict):
        source_scheduling_summary = build_source_scheduling_summary(sss)

    cons = frame.get("consequence") if isinstance(frame.get("consequence"), dict) else {}
    parts: List[str] = []
    dcg = frame.get("decision_contamination_guard_reserve") if isinstance(frame.get("decision_contamination_guard_reserve"), dict) else None
    if isinstance(dcg, dict):
        obs = _s(dcg.get("contamination_observation_summary"))
        if obs:
            parts.append(f"contamination:{obs[:160]}")
    tcb = frame.get("task_chain_bridge") if isinstance(frame.get("task_chain_bridge"), dict) else None
    if isinstance(tcb, dict) and tcb.get("task_chain_blocked"):
        parts.append(f"task_chain_blocked:{_s(tcb.get('task_chain_block_reason')) or 'yes'}")
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else None
    if isinstance(rp, dict) and rp.get("recheck_blocked"):
        parts.append(f"recheck_blocked:{_s(rp.get('recheck_block_reason')) or 'yes'}")
    qo = frame.get("reasoning_tree_quality_overlay") if isinstance(frame.get("reasoning_tree_quality_overlay"), dict) else None
    if isinstance(qo, dict):
        qs = _s(qo.get("quality_summary"))
        if qs:
            parts.append(f"quality:{qs[:120]}")
    er = _s(cons.get("expected_risk"))
    if er:
        parts.append(f"consequence_risk:{er[:120]}")

    issue_or_risk_summary = " | ".join(parts) if parts else "none_noted"

    seq = raw.get("frame_seq")
    summary_id = _s(frame.get("trace_anchor_id")) or (f"seq_{seq}" if seq is not None else "unknown")

    sch_short = (source_scheduling_summary[:80] + "…") if len(source_scheduling_summary) > 80 else source_scheduling_summary
    tcs = frame.get("task_chain_state_snapshot") if isinstance(frame.get("task_chain_state_snapshot"), dict) else None
    if tcs is None and frame.get("task_chain_state_snapshot") is not None and hasattr(frame.get("task_chain_state_snapshot"), "to_dict"):
        tcs = frame.get("task_chain_state_snapshot").to_dict()
    task_chain_progress_summary = build_task_chain_progress_summary(tcs) if isinstance(tcs, dict) else "task_chain: unavailable"

    mss = frame.get("mainline_state_snapshot") if isinstance(frame.get("mainline_state_snapshot"), dict) else None
    if mss is None and frame.get("mainline_state_snapshot") is not None and hasattr(frame.get("mainline_state_snapshot"), "to_dict"):
        mss = frame.get("mainline_state_snapshot").to_dict()
    mainline_state_summary = build_mainline_state_summary_line(mss) if isinstance(mss, dict) else "mainline_state: unavailable"

    mem_short = memory_usage_summary
    if mem_short and len(mem_short) > 220:
        mem_short = mem_short[:217] + "…"
    mls_short = mainline_state_summary
    if mls_short and len(mls_short) > 180:
        mls_short = mls_short[:177] + "…"
    etc = frame.get("environment_task_context_reserve")
    if etc is not None and hasattr(etc, "to_dict"):
        etc = etc.to_dict()
    if not isinstance(etc, dict):
        etc = {}
    inp = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}
    goal = frame.get("goal") if isinstance(frame.get("goal"), dict) else {}
    ctx = (
        f"goal={_s(goal.get('goal_type')) or 'unknown'}/{_s(goal.get('goal_status')) or 'unknown'};"
        f"route={_s(inp.get('route')) or 'unknown'};"
        f"stage={_s(etc.get('task_chain_stage')) or 'unknown'}"
    )
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else {}
    rp2 = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    closure = (
        f"effect={_s(cib.get('confirmation_bridge_next_effect')) or 'none'};"
        f"recheck={_s(rp2.get('recheck_action')) or 'none'};"
        f"terminal={_s(osi.get('search_terminal_status')) or 'none'}"
    )
    narrative_brief = build_narrative_brief(
        summary_id=summary_id,
        context_summary=ctx[:140],
        source_summary=(sch_short or "source: unavailable")[:180],
        task_summary=task_chain_progress_summary[:220],
        memory_summary=(mem_short or "memory: unavailable")[:220],
        mainline_state_summary=(mls_short or "mainline_state: unavailable")[:180],
        closure_summary=closure[:140],
        risk_summary=issue_or_risk_summary[:180],
    )
    summary_brief = narrative_brief
    obs = _build_process_observation(frame)

    return RunSummaryReference(
        summary_id=summary_id,
        summary_brief=summary_brief[:800],
        mainline_summary=mainline_summary or None,
        memory_usage_summary=memory_usage_summary or None,
        source_scheduling_summary=source_scheduling_summary or None,
        issue_or_risk_summary=issue_or_risk_summary,
        summary_reference_applied=True,
        raw_trace_layer_snapshot=raw,
        structured_event_layer_snapshot=ev,
        task_chain_progress_summary=task_chain_progress_summary,
        mainline_state_summary=mainline_state_summary,
        mainline_narrative_brief=narrative_brief,
        process_observation_summary=_s(obs.get("process_observation_summary")),
        resume_chain_stage_summary=_s(obs.get("resume_chain_stage_summary")),
        resume_chain_fragility_summary=_s(obs.get("resume_chain_fragility_summary")),
        resume_chain_progress_reached_main=obs.get("resume_chain_progress_reached_main"),
        memory_bias_accumulation_summary=_s(obs.get("memory_bias_accumulation_summary")),
        memory_bias_weight_shift_summary=_s(obs.get("memory_bias_weight_shift_summary")),
        memory_bias_conflict_stage_summary=_s(obs.get("memory_bias_conflict_stage_summary")),
        phase_closure_alignment_summary=_s(obs.get("phase_closure_alignment_summary")),
        closure_semantics_misalignment_summary=_s(obs.get("closure_semantics_misalignment_summary")),
    )


def build_log_chain_layer_summaries(frame: Dict[str, Any]) -> Dict[str, Any]:
    """
    供聚合层一次性读取三层语义的最小摘要（不改变主链）。
    """
    raw = build_raw_trace_slice(frame)
    ev = build_structured_event_slice(frame)
    rsr = build_run_summary_reference(frame)
    return {
        "raw_trace_one_liner": _raw_trace_one_liner(raw),
        "structured_event_one_liner": _structured_event_one_liner(ev),
        "summary_reference_one_liner": rsr.summary_brief,
        "run_summary_reference": rsr.to_dict(),
    }


def _raw_trace_one_liner(raw: Dict[str, Any]) -> str:
    return (
        f"seq={raw.get('frame_seq')} anchor={raw.get('trace_anchor_id') or '—'} "
        f"goal={raw.get('goal_type') or '—'}/{raw.get('goal_status') or '—'} "
        f"decision={raw.get('decision_type') or '—'}@{raw.get('decision_owner') or '—'} "
        f"action={raw.get('action_summary') or '—'}"
    )


def _structured_event_one_liner(ev: Dict[str, Any]) -> str:
    n = ev.get("event_count", 0)
    types = ev.get("distinct_event_types") or []
    head = ",".join(types[:5]) if types else "—"
    kt = ev.get("key_transition_summary") or "—"
    return f"events={n} types[{head}] key={str(kt)[:80]}"
