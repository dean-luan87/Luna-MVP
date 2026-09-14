# -*- coding: utf-8 -*-
"""
Mainline State / Phase Explicitness M0.4

从现有 frame 只读推导主链状态（candidate/execution/recovery/pause）与六阶段语义显式对象。
不替代主链拍板、不重写决策逻辑。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

MAINLINE_STATES = ("candidate", "execution", "recovery", "pause", "unknown")
MAINLINE_PHASES = (
    "contextualization",
    "candidate_formation",
    "path_selection",
    "recheck_or_repair",
    "closure",
    "result_feedback",
    "unknown",
)


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _get(d: Any, key: str, default: Any = None) -> Any:
    if d is None:
        return default
    if isinstance(d, dict):
        return d.get(key, default)
    return getattr(d, key, default)


@dataclass
class MainlineStateSnapshot:
    mainline_state: str = "unknown"
    mainline_phase: str = "unknown"
    mainline_state_reason_summary: str = ""
    mainline_phase_reason_summary: str = ""
    mainline_state_transition_summary: Optional[str] = None
    mainline_state_snapshot_applied: bool = False
    mainline_state_timeline_events: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mainline_state": self.mainline_state,
            "mainline_phase": self.mainline_phase,
            "mainline_state_reason_summary": self.mainline_state_reason_summary,
            "mainline_phase_reason_summary": self.mainline_phase_reason_summary,
            "mainline_state_transition_summary": self.mainline_state_transition_summary,
            "mainline_state_snapshot_applied": bool(self.mainline_state_snapshot_applied),
            "mainline_state_timeline_events": [dict(x) for x in self.mainline_state_timeline_events],
        }


def _hypothesis_count(frame: Dict[str, Any]) -> int:
    hl = frame.get("hypothesis_layer")
    if hl is not None and hasattr(hl, "hypotheses"):
        return len(getattr(hl, "hypotheses", []) or [])
    if isinstance(hl, dict):
        h = hl.get("hypotheses") or []
        return len(h) if isinstance(h, list) else 0
    return 0


def _infer_mainline_state(frame: Dict[str, Any]) -> tuple[str, str]:
    """返回 (state, reason_one_liner)。"""
    st = frame.get("state") if isinstance(frame.get("state"), dict) else {}
    tcb = frame.get("task_chain_bridge") if isinstance(frame.get("task_chain_bridge"), dict) else {}
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    if osi is not None and not isinstance(osi, dict) and hasattr(osi, "to_dict"):
        osi = osi.to_dict()
    elif not isinstance(osi, dict):
        osi = {}

    # pause：等待人/场景挂起/链上等待（主链语义，非等价于任务 paused）
    if st.get("human_check_pending") is True or st.get("goal_progress_paused") is True:
        return "pause", "human_or_goal_progress_hold"
    sg = _s(st.get("scene_gate_state"))
    if sg == "suspended":
        return "pause", "scene_gate_suspended"
    tc_st = _s(tcb.get("task_chain_state")) or ""
    if tc_st in ("waiting_user", "blocked"):
        return "pause", f"task_chain_bridge_state={tc_st}"
    if osi.get("search_waiting_user_input") is True:
        return "pause", "search_waiting_user_input"

    # recovery：拉回/中断后恢复语义（主链 ≠ 任务链 recovering 模式，仅用 bridge 子状态作弱信号）
    sub = _s(tcb.get("task_chain_substate")) or ""
    if "interrupt_then_resume" in sub or "resume" in sub.lower():
        return "recovery", "interrupt_then_resume_signal"
    gps = _s(st.get("goal_progress_state")) or ""
    if gps in ("rerouting", "rechecking"):
        return "recovery", f"goal_progress_state={gps}"

    # candidate：多假设或未收口终端
    n_hyp = _hypothesis_count(frame)
    if n_hyp >= 2:
        return "candidate", f"multiple_hypotheses_n={n_hyp}"
    term = _s(osi.get("search_terminal_status")) or "none"
    if term in ("none", "") and n_hyp >= 1:
        return "candidate", "no_search_terminal_with_hypothesis"

    # execution：默认沿路径推进
    return "execution", "default_active_path"


def _infer_mainline_phase(frame: Dict[str, Any], state: str) -> tuple[str, str]:
    """返回 (phase, reason_one_liner)。"""
    cib = frame.get("confirmation_input_bridge") if isinstance(frame.get("confirmation_input_bridge"), dict) else {}
    osi = frame.get("object_search_interaction") if isinstance(frame.get("object_search_interaction"), dict) else {}
    if not isinstance(osi, dict) and frame.get("object_search_interaction") is not None:
        o = frame.get("object_search_interaction")
        osi = o.to_dict() if hasattr(o, "to_dict") else {}
    elif not isinstance(osi, dict):
        osi = {}
    rp = frame.get("recheck_planner") if isinstance(frame.get("recheck_planner"), dict) else {}
    sss = frame.get("scheduled_source_state") if isinstance(frame.get("scheduled_source_state"), dict) else {}
    dec = frame.get("decision") if isinstance(frame.get("decision"), dict) else {}
    out = frame.get("outputs") if isinstance(frame.get("outputs"), dict) else {}

    ne = _s(cib.get("confirmation_bridge_next_effect"))
    if ne and ne not in ("none", ""):
        return "result_feedback", f"confirmation_next_effect={ne[:80]}"

    term = _s(osi.get("search_terminal_status")) or "none"
    if term in ("found", "cancelled"):
        return "closure", f"search_terminal={term}"

    rac = _s(rp.get("recheck_action"))
    if rac and not rp.get("recheck_blocked"):
        return "recheck_or_repair", f"recheck_action={rac[:80]}"
    if rp.get("recheck_blocked"):
        return "recheck_or_repair", "recheck_blocked_needs_repair_path"

    # 调度层关键切换进入主链阶段解释：避免“source 已变，mainline 叙事仍静态”
    over = _s(sss.get("priority_override_summary")) or ""
    conflict = _s(sss.get("source_conflict_summary")) or ""
    if over in ("dynamic_over_static", "safety_over_goal", "task_over_memory") or conflict in (
        "memory_vs_observation",
        "task_vs_feedback",
        "multiple",
    ):
        return "recheck_or_repair", f"source_shift_or_conflict(override={over or 'none'};conflict={conflict or 'none'})"

    n_hyp = _hypothesis_count(frame)
    if n_hyp >= 2:
        return "candidate_formation", f"hypotheses_n={n_hyp}"

    if _s(dec.get("decision_type")) and _s(out.get("action_summary")):
        return "path_selection", "decision_and_outputs_present"

    if state == "pause":
        return "recheck_or_repair", "pause_often_needs_clarification_or_repair"

    if state == "candidate":
        return "candidate_formation", "aligned_with_candidate_state"

    if state == "recovery":
        return "recheck_or_repair", "aligned_with_recovery_state"

    # 缺省：整理上下文 + 路径选择之间
    return "contextualization", "default_early_or_context_gathering"


def _build_timeline_events(state: str, phase: str, sr: str, pr: str) -> List[Dict[str, str]]:
    ev: List[Dict[str, str]] = [
        {"event_type": "mainline_state_snapshot_formed", "summary": f"state={state}; phase={phase}"},
        {"event_type": "mainline_phase_identified", "summary": pr[:220]},
    ]
    if sr != pr:
        ev.append({"event_type": "mainline_state_transition_observed", "summary": f"state_reason={sr[:120]};phase_reason={pr[:120]}"})
    return ev[:5]


def build_mainline_state_summary_line(snapshot: Optional[Dict[str, Any]]) -> str:
    """供 run_summary 一行主链状态/阶段。"""
    if not isinstance(snapshot, dict) or not snapshot.get("mainline_state_snapshot_applied"):
        return "mainline_state: unavailable"
    st = _s(snapshot.get("mainline_state")) or "—"
    ph = _s(snapshot.get("mainline_phase")) or "—"
    rs = (_s(snapshot.get("mainline_state_reason_summary")) or "")[:140]
    rp = (_s(snapshot.get("mainline_phase_reason_summary")) or "")[:140]
    return f"state={st}; phase={ph}; state_r={rs}; phase_r={rp}"[:700]


def build_mainline_state_snapshot(frame: Dict[str, Any]) -> MainlineStateSnapshot:
    if not isinstance(frame, dict):
        return MainlineStateSnapshot(mainline_state_snapshot_applied=False)

    ms, sr = _infer_mainline_state(frame)
    mp, pr = _infer_mainline_phase(frame, ms)
    if ms not in MAINLINE_STATES:
        ms = "unknown"
    if mp not in MAINLINE_PHASES:
        mp = "unknown"

    tl = _build_timeline_events(ms, mp, sr, pr)

    return MainlineStateSnapshot(
        mainline_state=ms,
        mainline_phase=mp,
        mainline_state_reason_summary=sr,
        mainline_phase_reason_summary=pr,
        mainline_state_transition_summary=None,
        mainline_state_snapshot_applied=True,
        mainline_state_timeline_events=tl,
    )
