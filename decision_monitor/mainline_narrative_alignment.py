# -*- coding: utf-8 -*-
"""
Mainline Narrative Alignment M0.6

统一主线叙事骨架（上下文→源格局→任务位置→记忆参与→主链状态/阶段→收口→风险提示）。
只读复用现有对象，不新增推理能力，不替代 trace/event/whitebox。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .information_source_scheduler import build_source_scheduling_summary
from .task_chain_state_snapshot import build_task_chain_progress_summary
from .memory_invocation_explanation import build_memory_usage_summary_line
from .mainline_state_snapshot import build_mainline_state_summary_line


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _to_dict(v: Any) -> Optional[Dict[str, Any]]:
    if isinstance(v, dict):
        return v
    if v is not None and hasattr(v, "to_dict"):
        return v.to_dict()
    return None


@dataclass
class MainlineNarrativeAlignment:
    narrative_brief: Optional[str] = None
    context_summary: Optional[str] = None
    source_summary: Optional[str] = None
    task_summary: Optional[str] = None
    memory_summary: Optional[str] = None
    mainline_state_summary: Optional[str] = None
    closure_summary: Optional[str] = None
    risk_summary: Optional[str] = None
    mainline_narrative_alignment_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "narrative_brief": self.narrative_brief,
            "context_summary": self.context_summary,
            "source_summary": self.source_summary,
            "task_summary": self.task_summary,
            "memory_summary": self.memory_summary,
            "mainline_state_summary": self.mainline_state_summary,
            "closure_summary": self.closure_summary,
            "risk_summary": self.risk_summary,
            "mainline_narrative_alignment_applied": bool(self.mainline_narrative_alignment_applied),
        }


def _build_context_summary(frame: Dict[str, Any]) -> str:
    goal = frame.get("goal") if isinstance(frame.get("goal"), dict) else {}
    inp = frame.get("inputs") if isinstance(frame.get("inputs"), dict) else {}
    etc = _to_dict(frame.get("environment_task_context_reserve")) or {}
    g = _s(goal.get("goal_type")) or "unknown_goal"
    gs = _s(goal.get("goal_status")) or "unknown_status"
    route = _s(inp.get("route")) or "unknown_route"
    stage = _s(etc.get("task_chain_stage")) or "unknown_stage"
    return f"goal={g}/{gs}; route={route}; env_task_stage={stage}"


def _build_closure_summary(frame: Dict[str, Any]) -> str:
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else {}
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    eff = _s(cib.get("confirmation_bridge_next_effect"))
    recheck = _s(rp.get("recheck_action"))
    term = _s(osi.get("search_terminal_status")) or "none"
    if eff:
        return f"closure=confirmation_effect:{eff}; terminal={term}"
    if recheck:
        return f"closure=recheck:{recheck}; terminal={term}"
    if term not in ("", "none"):
        return f"closure=search_terminal:{term}"
    return "closure=ongoing"


def build_narrative_brief(
    *,
    summary_id: str,
    context_summary: str,
    source_summary: str,
    task_summary: str,
    memory_summary: str,
    mainline_state_summary: str,
    closure_summary: str,
    risk_summary: str,
) -> str:
    # 固定顺序：context -> source -> task -> memory -> mainline -> closure -> risk
    return (
        f"trace={summary_id}; ctx={context_summary}; "
        f"source={source_summary}; task={task_summary}; mem={memory_summary}; "
        f"mainline={mainline_state_summary}; closure={closure_summary}; risk={risk_summary}"
    )[:1000]


def build_mainline_narrative_alignment(frame: Dict[str, Any]) -> MainlineNarrativeAlignment:
    if not isinstance(frame, dict):
        return MainlineNarrativeAlignment(mainline_narrative_alignment_applied=False)

    tid = _s(frame.get("trace_anchor_id")) or "unknown"
    sss = _to_dict(frame.get("scheduled_source_state")) or {}
    tcs = _to_dict(frame.get("task_chain_state_snapshot")) or {}
    mss = _to_dict(frame.get("mainline_state_snapshot")) or {}

    source_summary = build_source_scheduling_summary(sss) if sss else "source: unavailable"
    task_summary = build_task_chain_progress_summary(tcs) if tcs else "task_chain: unavailable"
    memory_summary = build_memory_usage_summary_line(frame)
    mainline_state_summary = build_mainline_state_summary_line(mss) if mss else "mainline_state: unavailable"
    context_summary = _build_context_summary(frame)
    closure_summary = _build_closure_summary(frame)

    rsr = _to_dict(frame.get("run_summary_reference")) or {}
    risk_summary = _s(rsr.get("issue_or_risk_summary")) or "none_noted"

    brief = build_narrative_brief(
        summary_id=tid,
        context_summary=context_summary,
        source_summary=source_summary[:180],
        task_summary=task_summary[:220],
        memory_summary=memory_summary[:220],
        mainline_state_summary=mainline_state_summary[:180],
        closure_summary=closure_summary[:160],
        risk_summary=risk_summary[:180],
    )
    return MainlineNarrativeAlignment(
        narrative_brief=brief,
        context_summary=context_summary,
        source_summary=source_summary,
        task_summary=task_summary,
        memory_summary=memory_summary,
        mainline_state_summary=mainline_state_summary,
        closure_summary=closure_summary,
        risk_summary=risk_summary,
        mainline_narrative_alignment_applied=True,
    )
