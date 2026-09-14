# -*- coding: utf-8 -*-
"""
Narrative / Evidence Tension Review M0

只读审计层：从已落地 frame 中聚合 summary / entry / 主链快照 / 时间轴等信号，
输出五维「叙事—证据张力」观察结果。不裁决、不回写主链、不改写 Summary/Entry 本体。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

TENSION_STATES = ("none", "low", "medium", "high", "unknown")


def _s(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


def _to_dict(obj: Any) -> Dict[str, Any]:
    if isinstance(obj, dict):
        return obj
    if obj is not None and hasattr(obj, "to_dict"):
        d = obj.to_dict()
        return d if isinstance(d, dict) else {}
    return {}


def _rank(level: str) -> int:
    return {"none": 0, "low": 1, "medium": 2, "high": 3, "unknown": -1}.get(level, -1)


def _clamp_level(level: str) -> str:
    return level if level in TENSION_STATES else "unknown"


def _score_narrative_trace_support(frame: Dict[str, Any], rsr: Dict[str, Any], reasons: Dict[str, str]) -> str:
    """
    A：叙事↔证据支撑（nt）

    目标（M0 tightening）：
    - 不再把「事件数量多」直接等同于「关键证据足够」
    - 优先评估“关键转折/关键锚点”是否足以支撑较长叙事
    - 保守：只产生少量可信的 low/medium，不追求大面积抬高
    """
    if not rsr.get("summary_reference_applied"):
        reasons["narrative_trace_support"] = "summary_reference_not_applied"
        return "unknown"

    ev_snap = rsr.get("structured_event_layer_snapshot")
    if not isinstance(ev_snap, dict):
        ev_snap = {}
    event_count = ev_snap.get("event_count")
    if not isinstance(event_count, int):
        event_count = 0

    nar = _s(rsr.get("mainline_narrative_brief"))
    mna = _to_dict(frame.get("mainline_narrative_alignment"))
    if mna.get("narrative_brief"):
        nar = nar or _s(mna.get("narrative_brief"))
    narr_len = len(nar)

    tv = _to_dict(frame.get("reasoning_timeline_view"))
    tl_events = tv.get("events") or []
    tl_n = len(tl_events) if isinstance(tl_events, list) else 0

    # --- 关键锚点抽取：timeline 中 high/medium 重要性事件（比 event_count 更接近“关键证据”） ---
    hi_n = 0
    hi_type_n = 0
    key_n = 0
    if isinstance(tl_events, list) and tl_events:
        hi = [e for e in tl_events if isinstance(e, dict) and e.get("event_importance") in ("high", "medium")]
        hi_n = len(hi)
        hi_types = [e.get("event_type") for e in hi if _s(e.get("event_type"))]
        hi_type_n = len(set(hi_types))
        key_n = hi_n  # 当前以 high/medium 作为 key anchors 的最小近似

    # 兼容：若 timeline 缺失，则退化为 structured event_count / tl_n
    eff_events = max(event_count, tl_n)
    ratio = narr_len / float(max(eff_events, 1))

    if narr_len < 30 and eff_events <= 1:
        reasons["narrative_trace_support"] = "short_narrative_few_events_or_unknown"
        return "low"

    if eff_events == 0 and narr_len > 80:
        reasons["narrative_trace_support"] = "narrative_present_but_no_structured_events"
        return "medium"

    if ratio > 120 and eff_events < 8:
        reasons["narrative_trace_support"] = f"high_narrative_to_event_ratio(ratio={ratio:.1f})"
        return "high"

    if ratio > 55 and eff_events < 12:
        reasons["narrative_trace_support"] = f"elevated_narrative_to_event_ratio(ratio={ratio:.1f})"
        return "medium"

    # tightening：去掉 “eff_events>=18 ⇒ none” 的硬门槛。
    # 事件多≠关键证据够；这里改为“叙事长 + 关键锚点偏薄”才点亮 nt。
    if narr_len >= 900:
        if key_n <= 9 and hi_type_n <= 9:
            reasons["narrative_trace_support"] = f"thin_key_anchors_for_long_narrative(key={key_n},types={hi_type_n})"
            return "medium"  # 少量典型样本：建议 review（不等于失败）
        if key_n == 10 and hi_type_n == 10:
            reasons["narrative_trace_support"] = f"slightly_thin_key_anchors_for_long_narrative(key={key_n},types={hi_type_n})"
            return "low"  # 轻量 watch：不乱响

    # 常态复杂叙事：关键锚点足够时保持 none（避免误报）
    if key_n >= 11 and narr_len >= 600:
        reasons["narrative_trace_support"] = "key_anchors_sufficient_for_complex_narrative"
        return "none"

    reasons["narrative_trace_support"] = "balanced_or_insufficient_signal"
    return "low"


def _score_phase_closure_outcome(frame: Dict[str, Any], rsr: Dict[str, Any], reasons: Dict[str, str]) -> str:
    """B：phase/closure 与 outcome/summary 口径。"""
    cms = _s(rsr.get("closure_semantics_misalignment_summary")).lower()
    if cms and cms != "none":
        reasons["phase_closure_outcome"] = f"closure_semantics_misalignment={cms[:120]}"
        return "high"

    mss = _to_dict(frame.get("mainline_state_snapshot"))
    phase = _s(mss.get("mainline_phase")).lower()
    osi = _to_dict(frame.get("object_search_interaction"))
    term = _s(osi.get("search_terminal_status")).lower()

    if phase == "closure" and term not in ("found", "cancelled", "done") and term != "":
        reasons["phase_closure_outcome"] = "closure_phase_but_terminal_not_closed"
        return "medium"

    pcl = _s(rsr.get("phase_closure_alignment_summary"))
    if "misaligned" in pcl.lower() or "错位" in pcl:
        reasons["phase_closure_outcome"] = "phase_closure_alignment_hint"
        return "medium"

    reasons["phase_closure_outcome"] = "no_strong_closure_outcome_mismatch_signal"
    return "none"


def _score_summary_backfill(frame: Dict[str, Any], rsr: Dict[str, Any], reasons: Dict[str, str]) -> str:
    """C：entry 完整感 vs backfill 契约。"""
    pse = _to_dict(frame.get("post_processing_summary_entry"))
    if not pse.get("post_processing_summary_entry_applied"):
        reasons["summary_backfill"] = "post_processing_entry_not_applied"
        return "unknown"

    req_t = bool(pse.get("requires_trace_backfill"))
    req_e = bool(pse.get("requires_event_backfill"))
    req_w = bool(pse.get("requires_whitebox_backfill"))
    bc = sum(1 for x in (req_t, req_e, req_w) if x)

    nar_r = _s(pse.get("narrative_readable"))
    nar_len = len(nar_r)

    if bc >= 3:
        reasons["summary_backfill"] = "all_three_backfill_channels_flagged"
        lvl = "high"
    elif bc == 2:
        reasons["summary_backfill"] = "two_backfill_channels_flagged"
        lvl = "medium"
    elif bc == 1:
        reasons["summary_backfill"] = "one_backfill_channel_flagged"
        lvl = "low"
    else:
        reasons["summary_backfill"] = "no_mandatory_backfill_under_contract"
        return "none"

    if nar_len > 220 and bc >= 1:
        reasons["summary_backfill"] = (reasons.get("summary_backfill") or "") + "; long_narrative_readable_with_backfill"
        if lvl == "low":
            lvl = "medium"
        elif lvl == "medium":
            lvl = "high"

    return lvl


def _tcp_resume_value(tcp: str) -> str:
    """提取 task_chain_progress_summary 中 resume= 的值（不含字段名噪声）。"""
    if "resume=" not in tcp:
        return ""
    return _s(tcp.split("resume=", 1)[1].split(";", 1)[0])


def _lg_weak_exploration_only(tcp: str) -> bool:
    """
    主任务尚未到位但仅为「正常探索/混合推进」噪声：无局部成功风险、无插入/恢复语义。
    （main_push_hint=mixed 单独出现时常属此类，不应与「全局停滞」混为一谈。）
    """
    tl = _s(tcp).lower()
    if "local_only_risk=yes" in tl:
        return False
    if "recovering=yes" in tl or "inserted_open=yes" in tl:
        return False
    if "warn=" in tl:
        wp = tl.split("warn=", 1)[1].split(";", 1)[0].strip()
        if wp and wp not in ("none", ""):
            return False
    return "main_push_hint=mixed" in tl


def _tcp_meaningful_main_not_reached_context(tcp: str, proc: str) -> bool:
    """
    是否存在「可审计的」局部/全局推进摩擦（区别于模板里固定的 resume= 字段名命中）。
    """
    tl = _s(tcp).lower()
    pl = _s(proc).lower()

    if any(x in tl for x in ("forward", "推进", "progress")):
        return True
    if "recovering=yes" in tl or "inserted_open=yes" in tl or "local_only_risk=yes" in tl:
        return True
    rv = _tcp_resume_value(tcp)
    if rv and rv not in ("—", "-", "none", ""):
        return True
    if "main_not_progressed" in pl or "resume_frag=resume_declared_but_main_not_progressed" in pl:
        return True
    if "resume_chain_waiting_clarification" in pl or "waiting_clarification" in pl:
        return True
    return False


def _lg_escalate_high(
    reached: Any,
    tcp: str,
    proc: str,
    rf: str,
) -> bool:
    """更严重的全局停滞：结构风险叠加 / 恢复链脆弱 / 反复声明仍不到位。"""
    if reached is not False:
        return False
    tl = _s(tcp).lower()
    pl = _s(proc).lower()
    rfl = _s(rf).lower()

    frag_high = "resume_declared_but_main_not_progressed" in rfl
    if frag_high:
        return True

    structural = (
        "local_only_risk=yes" in tl
        and ("recovering=yes" in tl or "inserted_open=yes" in tl)
    )
    if structural:
        return True

    warn_part = ""
    if "warn=" in tl:
        warn_part = tl.split("warn=", 1)[1].split(";", 1)[0]
    warn_escalate = any(
        w in warn_part for w in ("pseudo_recovery", "inserted_branch", "local_success")
    )
    if "local_only_risk=yes" in tl and warn_escalate:
        return True

    if "resume_chain_waiting_clarification" in rfl and (
        "local_only_risk=yes" in tl or "main_push_hint=mixed" in tl
    ):
        return True

    if "m11x_ctx_observed" in pl and "resume_frag=" in pl:
        frag = pl.split("resume_frag=", 1)[1].split(";", 1)[0].strip()
        if frag and frag not in ("none",):
            return True

    if "recovering=yes" in tl and warn_escalate:
        return True

    return False


def _score_local_global_progress(frame: Dict[str, Any], rsr: Dict[str, Any], reasons: Dict[str, str]) -> str:
    """D：局部连贯 vs 全局主任务推进（M0：拉开 low/medium/high，避免 resume= 字段名假阳性）。"""
    rf = _s(rsr.get("resume_chain_fragility_summary"))
    if "resume_declared_but_main_not_progressed" in rf:
        reasons["local_global_progress"] = "resume_fragility_declared_main_not_progressed"
        return "high"

    reached = rsr.get("resume_chain_progress_reached_main")
    tcp = _s(rsr.get("task_chain_progress_summary"))
    proc = _s(rsr.get("process_observation_summary"))

    if reached is False:
        if _lg_escalate_high(reached, tcp, proc, rf):
            reasons["local_global_progress"] = "structural_or_fragile_global_stall_escalated"
            return "high"
        if _lg_weak_exploration_only(tcp):
            reasons["local_global_progress"] = "weak_exploration_main_mixed_not_yet_global_stall"
            return "low"
        if _tcp_meaningful_main_not_reached_context(tcp, proc):
            reasons["local_global_progress"] = "progress_language_or_structure_but_main_not_reached"
            return "medium"
        reasons["local_global_progress"] = "main_not_reached_weak_or_template_noise"
        return "low"

    if "resume_frag=resume_declared_but_main_not_progressed" in proc or "main_not_progressed" in proc:
        if _lg_escalate_high(False, tcp, proc, rf):
            reasons["local_global_progress"] = "process_observation_fragile_stall_escalated"
            return "high"
        if _tcp_meaningful_main_not_reached_context(tcp, proc):
            reasons["local_global_progress"] = "process_observation_suggests_stall"
            return "medium"
        reasons["local_global_progress"] = "process_observation_stall_weak_signal"
        return "low"

    reasons["local_global_progress"] = "no_strong_local_global_split_signal"
    return "low"


def _score_memory_bias(frame: Dict[str, Any], rsr: Dict[str, Any], reasons: Dict[str, str]) -> str:
    """E：个性化语义偏差（非污染裁决）。"""
    mbas = _s(rsr.get("memory_bias_accumulation_summary"))
    if "none" in mbas.lower() and len(mbas) < 12:
        reasons["memory_bias"] = "memory_bias_accumulation_empty"
        return "none"

    if "memory_vs" in mbas.lower() or "conflict" in mbas.lower() or "冲突" in mbas:
        reasons["memory_bias"] = "memory_bias_or_conflict_signal"
        return "high"

    mie = _to_dict(frame.get("memory_invocation_explanation"))
    eff = _s(mie.get("memory_invocation_effect_summary")).lower()
    if eff in ("memory_overweight_risk", "memory_vs_observation_conflict", "memory_vs_task_risk"):
        reasons["memory_bias"] = f"memory_effect={eff}"
        return "medium"

    if "memory_effect" in mbas.lower() or "supports_mainline" in mbas.lower():
        reasons["memory_bias"] = "memory_effect_tracing_present"
        return "low"

    if len(mbas) > 8:
        reasons["memory_bias"] = "memory_bias_accumulation_non_trivial"
        return "low"

    reasons["memory_bias"] = "insufficient_memory_bias_signal"
    return "none"


def _suggested_backfill(
    reasons: Dict[str, str],
    levels: Dict[str, str],
) -> str:
    parts: List[str] = []
    if _rank(levels.get("narrative_trace_support_tension", "none")) >= 2:
        parts.append("对照 structured_event / timeline 事件核对 narrative 覆盖")
    if _rank(levels.get("phase_closure_outcome_tension", "none")) >= 2:
        parts.append("核对 mainline_phase / closure 与 terminal、outcome 行是否同口径")
    if _rank(levels.get("summary_backfill_tension", "none")) >= 1:
        parts.append("按 post_processing 契约执行 trace/event/whitebox 分层回溯")
    if _rank(levels.get("local_global_progress_tension", "none")) >= 2:
        parts.append("对照 task_chain 与 resume 过程显影，确认主任务是否真推进")
    if _rank(levels.get("memory_bias_tension", "none")) >= 2:
        parts.append("对照 memory_invocation 与调度源，复核记忆权重是否偏稳")
    if not parts:
        parts.append("当前张力信号较弱，保持常规同链校验即可")
    return "；".join(parts)[:420]


def _brief_line(levels: Dict[str, str]) -> str:
    """一行紧凑摘要。"""
    order = (
        "narrative_trace_support_tension",
        "phase_closure_outcome_tension",
        "summary_backfill_tension",
        "local_global_progress_tension",
        "memory_bias_tension",
    )
    keys = ("nt", "pc", "sb", "lg", "mb")
    parts = [f"{k}:{levels.get(o, 'unknown')}" for k, o in zip(keys, order)]
    return "|".join(parts)


def _readable(levels: Dict[str, str], reasons: Dict[str, str]) -> str:
    lines = [
        "叙事—证据张力审计（M0，启发式）：",
        f"· 叙事↔事件支撑：{levels.get('narrative_trace_support_tension', 'unknown')} — {_s(reasons.get('narrative_trace_support'))}",
        f"· phase/closure↔outcome：{levels.get('phase_closure_outcome_tension', 'unknown')} — {_s(reasons.get('phase_closure_outcome'))}",
        f"· summary↔backfill 契约：{levels.get('summary_backfill_tension', 'unknown')} — {_s(reasons.get('summary_backfill'))}",
        f"· 局部↔全局推进：{levels.get('local_global_progress_tension', 'unknown')} — {_s(reasons.get('local_global_progress'))}",
        f"· 记忆语义偏差：{levels.get('memory_bias_tension', 'unknown')} — {_s(reasons.get('memory_bias'))}",
    ]
    return "\n".join(lines)[:2000]


@dataclass
class NarrativeEvidenceTensionReview:
    narrative_trace_support_tension: str = "unknown"
    phase_closure_outcome_tension: str = "unknown"
    summary_backfill_tension: str = "unknown"
    local_global_progress_tension: str = "unknown"
    memory_bias_tension: str = "unknown"
    tension_review_brief: str = ""
    tension_review_readable: str = ""
    tension_reason_summaries: Dict[str, str] = field(default_factory=dict)
    suggested_backfill_direction_summary: str = ""
    narrative_evidence_tension_review_applied: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "narrative_trace_support_tension": self.narrative_trace_support_tension,
            "phase_closure_outcome_tension": self.phase_closure_outcome_tension,
            "summary_backfill_tension": self.summary_backfill_tension,
            "local_global_progress_tension": self.local_global_progress_tension,
            "memory_bias_tension": self.memory_bias_tension,
            "tension_review_brief": self.tension_review_brief,
            "tension_review_readable": self.tension_review_readable,
            "tension_reason_summaries": dict(self.tension_reason_summaries),
            "suggested_backfill_direction_summary": self.suggested_backfill_direction_summary,
            "narrative_evidence_tension_review_applied": bool(self.narrative_evidence_tension_review_applied),
        }


def build_narrative_evidence_tension_review(frame: Dict[str, Any]) -> NarrativeEvidenceTensionReview:
    """
    从完整 frame 字典生成审计对象（只读；不修改 frame）。
    """
    if not isinstance(frame, dict):
        return NarrativeEvidenceTensionReview()

    rsr = _to_dict(frame.get("run_summary_reference"))
    if not rsr.get("summary_reference_applied"):
        return NarrativeEvidenceTensionReview()

    reasons: Dict[str, str] = {}

    nt = _clamp_level(_score_narrative_trace_support(frame, rsr, reasons))
    pc = _clamp_level(_score_phase_closure_outcome(frame, rsr, reasons))
    sb = _clamp_level(_score_summary_backfill(frame, rsr, reasons))
    lg = _clamp_level(_score_local_global_progress(frame, rsr, reasons))
    mb = _clamp_level(_score_memory_bias(frame, rsr, reasons))

    levels = {
        "narrative_trace_support_tension": nt,
        "phase_closure_outcome_tension": pc,
        "summary_backfill_tension": sb,
        "local_global_progress_tension": lg,
        "memory_bias_tension": mb,
    }
    brief = _brief_line(levels)
    readable = _readable(levels, reasons)
    sug = _suggested_backfill(reasons, levels)

    return NarrativeEvidenceTensionReview(
        narrative_trace_support_tension=nt,
        phase_closure_outcome_tension=pc,
        summary_backfill_tension=sb,
        local_global_progress_tension=lg,
        memory_bias_tension=mb,
        tension_review_brief=brief,
        tension_review_readable=readable,
        tension_reason_summaries=dict(reasons),
        suggested_backfill_direction_summary=sug,
        narrative_evidence_tension_review_applied=True,
    )
