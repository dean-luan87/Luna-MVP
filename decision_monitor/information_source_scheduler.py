# -*- coding: utf-8 -*-
"""
Information Source Scheduler M0（数据源调度层最小显式化）

定位：
- 从现有 frame 轻量整理出 scheduled_source_state
- 只做可见化与摘要，不做复杂调度算法
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

SOURCE_TYPES = (
    "user_input",
    "environment_observation",
    "task_state",
    "memory_recall",
    "novel_observation",
    "system_or_strategy",
)

CONFLICT_TYPES = (
    "none",
    "user_vs_environment",
    "memory_vs_observation",
    "task_vs_feedback",
    "multiple",
    "unknown",
)

OVERRIDE_TYPES = (
    "safety_over_goal",
    "dynamic_over_static",
    "task_over_memory",
    "none",
    "unknown",
)

PRESSURE_TYPES = ("high", "medium", "low", "unknown")
CONFIDENCE_TYPES = ("stable", "mixed", "fragile", "unknown")


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class ScheduledSourceState:
    participating_sources: List[str] = field(default_factory=list)
    dominant_source: str = "environment_observation"
    source_conflict_summary: str = "none"
    priority_override_summary: str = "none"
    timeliness_pressure: str = "unknown"
    source_confidence_summary: str = "unknown"
    dominant_source_reason_summary: Optional[str] = None
    source_scheduling_event_summaries: List[str] = field(default_factory=list)
    source_scheduling_warning_summary: Optional[str] = None
    task_state_presence_summary: Optional[str] = None
    scheduled_source_state_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "participating_sources": list(self.participating_sources),
            "dominant_source": self.dominant_source,
            "source_conflict_summary": self.source_conflict_summary,
            "priority_override_summary": self.priority_override_summary,
            "timeliness_pressure": self.timeliness_pressure,
            "source_confidence_summary": self.source_confidence_summary,
            "dominant_source_reason_summary": self.dominant_source_reason_summary,
            "source_scheduling_event_summaries": list(self.source_scheduling_event_summaries),
            "source_scheduling_warning_summary": self.source_scheduling_warning_summary,
            "task_state_presence_summary": self.task_state_presence_summary,
            "scheduled_source_state_applied": bool(self.scheduled_source_state_applied),
        }


def build_source_scheduling_summary(state: Dict[str, Any]) -> str:
    if not isinstance(state, dict):
        return "scheduled_source_state: unavailable"
    dom = _s(state.get("dominant_source")) or "unknown"
    cfx = _s(state.get("source_conflict_summary")) or "unknown"
    over = _s(state.get("priority_override_summary")) or "unknown"
    tp = _s(state.get("timeliness_pressure")) or "unknown"
    conf = _s(state.get("source_confidence_summary")) or "unknown"
    base = f"dominant={dom} | conflict={cfx} | override={over} | t={tp} | conf={conf}"
    tsp = _s(state.get("task_state_presence_summary"))
    if tsp:
        return f"{base} | task_state={tsp}"
    return base


def build_source_scheduling_events(state: Dict[str, Any]) -> List[str]:
    if not isinstance(state, dict):
        return []
    out: List[str] = []
    dom = _s(state.get("dominant_source")) or "unknown"
    out.append(f"dominant_source_selected:{dom}")
    cfx = _s(state.get("source_conflict_summary")) or "none"
    if cfx not in ("none", "unknown"):
        out.append(f"source_conflict_detected:{cfx}")
    over = _s(state.get("priority_override_summary")) or "none"
    if over not in ("none", "unknown"):
        out.append(f"priority_override_applied:{over}")
        if over == "dynamic_over_static":
            out.append("dynamic_source_overrode_static_source")
        if over == "task_over_memory":
            out.append("task_source_became_dominant")
    if dom == "memory_recall":
        out.append("memory_source_overrode_observation")
    return out


def build_scheduled_source_state(frame: Dict[str, Any]) -> ScheduledSourceState:
    if not isinstance(frame, dict):
        return ScheduledSourceState()

    src: List[str] = []
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else None
    if cib and (_s(cib.get("confirmation_input_raw_text")) or _s(cib.get("confirmation_input_type"))):
        src.append("user_input")

    etc = frame.get("environment_task_context_reserve") if isinstance(frame.get("environment_task_context_reserve"), dict) else None
    if etc:
        ec = etc.get("environment_context") if isinstance(etc.get("environment_context"), dict) else {}
        if _s(ec.get("environment_scene_type")) or _s(ec.get("environment_visibility_state")):
            src.append("environment_observation")
        tc = etc.get("task_chain_context") if isinstance(etc.get("task_chain_context"), dict) else {}
        if _s(tc.get("task_chain_stage")) or _s(tc.get("task_chain_current_action")):
            src.append("task_state")

    tcb = frame.get("task_chain_bridge") if isinstance(frame.get("task_chain_bridge"), dict) else None
    if tcb and "task_state" not in src:
        if _s(tcb.get("task_chain_state")) or _s(tcb.get("task_chain_substate")):
            src.append("task_state")

    mn = frame.get("memory_novel_information_channel") if isinstance(frame.get("memory_novel_information_channel"), dict) else None
    dom = (_s(mn.get("dominant_reasoning_channel")) or "unknown") if mn else "unknown"
    if mn:
        if dom == "memory_derived" or int(mn.get("memory_channel_count") or 0) > 0:
            src.append("memory_recall")
        if dom in ("newly_observed", "inferred_from_exclusion") or int(mn.get("novel_channel_count") or 0) > 0:
            src.append("novel_observation")

    if frame.get("strategy_injection_shadow") or frame.get("knowledge_dual_channel_interface"):
        src.append("system_or_strategy")

    # keep order, dedupe
    uniq: List[str] = []
    for s in src:
        if s in SOURCE_TYPES and s not in uniq:
            uniq.append(s)

    tcs = frame.get("task_chain_state_snapshot") if isinstance(frame.get("task_chain_state_snapshot"), dict) else None
    if tcs is None and frame.get("task_chain_state_snapshot") is not None and hasattr(frame.get("task_chain_state_snapshot"), "to_dict"):
        tcs = frame.get("task_chain_state_snapshot").to_dict()
    task_state_presence_summary: Optional[str] = None
    if isinstance(tcs, dict) and tcs.get("task_chain_state_snapshot_applied"):
        if "task_state" not in uniq:
            uniq.insert(0, "task_state")
        stg = _s(tcs.get("task_chain_stage")) or "—"
        md = _s(tcs.get("task_mode")) or "—"
        tid = _s(tcs.get("task_chain_id")) or "—"
        task_state_presence_summary = f"id={tid[:32]}; stage={stg}; mode={md}"

    if not uniq:
        uniq = ["environment_observation"]

    # dominant source (M0 rule mapping)
    dominant = "environment_observation"
    if "task_state" in uniq:
        dominant = "task_state"
    if "user_input" in uniq:
        dominant = "user_input"
    if dom == "memory_derived" and "memory_recall" in uniq:
        dominant = "memory_recall"
    if dom in ("newly_observed", "inferred_from_exclusion") and "novel_observation" in uniq:
        dominant = "novel_observation"

    # conflict summary (M0 heuristic)
    conflict = "none"
    if "user_input" in uniq and "environment_observation" in uniq:
        conflict = "user_vs_environment"
    if "memory_recall" in uniq and "novel_observation" in uniq:
        conflict = "memory_vs_observation"
    if "task_state" in uniq and "user_input" in uniq and conflict != "none":
        conflict = "multiple"
    elif "task_state" in uniq and "user_input" in uniq and conflict == "none":
        conflict = "task_vs_feedback"

    # priority override summary
    over = "none"
    st = frame.get("state") if isinstance(frame.get("state"), dict) else {}
    if bool(st.get("domain_mismatch_detected")) or bool(st.get("minimum_mode_active")):
        over = "safety_over_goal"
    elif "novel_observation" in uniq and "memory_recall" in uniq:
        over = "dynamic_over_static"
    elif "task_state" in uniq and "memory_recall" in uniq:
        over = "task_over_memory"

    # timeliness pressure
    pressure = "unknown"
    if bool(st.get("vision_degraded")) or bool(st.get("human_check_pending")):
        pressure = "high"
    elif conflict in ("multiple", "task_vs_feedback"):
        pressure = "medium"
    elif conflict == "none":
        pressure = "low"

    # confidence summary
    conf = "unknown"
    vis = st.get("vision_reliability_score")
    if isinstance(vis, (int, float)):
        if vis >= 0.75 and conflict == "none":
            conf = "stable"
        elif vis < 0.45:
            conf = "fragile"
        else:
            conf = "mixed"
    elif conflict == "none":
        conf = "mixed"
    else:
        conf = "fragile" if conflict == "multiple" else "mixed"

    tmp = ScheduledSourceState(
        participating_sources=uniq,
        dominant_source=dominant,
        source_conflict_summary=conflict if conflict in CONFLICT_TYPES else "unknown",
        priority_override_summary=over if over in OVERRIDE_TYPES else "unknown",
        timeliness_pressure=pressure if pressure in PRESSURE_TYPES else "unknown",
        source_confidence_summary=conf if conf in CONFIDENCE_TYPES else "unknown",
        dominant_source_reason_summary=f"dominant={dominant}; participating={','.join(uniq[:4])}",
        task_state_presence_summary=task_state_presence_summary,
        scheduled_source_state_applied=True,
    )
    d = tmp.to_dict()
    tmp.source_scheduling_event_summaries = build_source_scheduling_events(d)
    if conflict in ("multiple", "memory_vs_observation") or over in ("safety_over_goal", "dynamic_over_static"):
        tmp.source_scheduling_warning_summary = "surface_stable_but_logic_risky"
    else:
        tmp.source_scheduling_warning_summary = "none"
    return tmp

