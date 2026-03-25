# -*- coding: utf-8 -*-
"""
Summary × Post-Processing Boundary Contract M0.5

从已落地的 `run_summary_reference` 派生最小后处理入口契约；不做归类算法、不写入图书馆/记忆。
Summary-first 且非 Summary-only：契约携带回溯提示，禁止以 Summary 单独作为因果证据本体。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

_CAUSAL_HINT_EN = (
    "conflict",
    "mismatch",
    "drift",
    "contamination",
    "recheck_blocked",
    "blocked_without",
    "memory_vs",
    "observation",
    "override",
    "dominant_source",
    "pseudo",
    "recovery_fail",
    "false_recovery",
    "crack",
)
_CAUSAL_HINT_ZH = ("冲突", "污染", "裂缝", "伪恢复", "回溯", "不匹配", "漂移")


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


def _get_rsr_dict(frame: Dict[str, Any]) -> Dict[str, Any]:
    r = frame.get("run_summary_reference")
    if r is not None and hasattr(r, "to_dict"):
        return r.to_dict()
    if isinstance(r, dict):
        return r
    return {}


def _blob_lower(*parts: Optional[str]) -> str:
    return " ".join(p for p in parts if p).lower()


def _mentions_causal_risk(blob: str) -> bool:
    if not blob.strip():
        return False
    b = blob.lower()
    for w in _CAUSAL_HINT_EN:
        if w in b:
            return True
    for w in _CAUSAL_HINT_ZH:
        if w in blob:
            return True
    return False


def _memory_conflict_hint(mem: Optional[str]) -> bool:
    if not mem:
        return False
    ml = mem.lower()
    if "risk" in ml or "conflict" in ml or "偏移" in mem or "冲突" in mem:
        return True
    return bool(re.search(r"memory_vs|novel|hybrid", ml))


def _any_whitebox_present(frame: Dict[str, Any]) -> bool:
    for key in (
        "grid_search_whitebox_trace",
        "recheck_whitebox_trace",
        "action_hint_whitebox_trace",
        "confirmation_whitebox_trace",
        "evidence_hypothesis_whitebox_trace",
        "experience_governance_whitebox_trace",
    ):
        w = frame.get(key) if isinstance(frame.get(key), dict) else None
        if w and _s(w.get("whitebox_summary")):
            return True
    return False


@dataclass
class PostProcessingSummaryEntry:
    """后处理链合法入口：字段来自 Summary，不等价于 Raw Trace / Structured Event / 白盒全文。"""

    entry_id: str = ""
    trace_anchor_id: Optional[str] = None
    summary_id: Optional[str] = None
    # A. 可直接作为归类/路由入口的摘要（仍须遵守「非证据本体」）
    mainline_summary: Optional[str] = None
    mainline_state_summary: Optional[str] = None
    memory_usage_summary: Optional[str] = None
    source_scheduling_summary: Optional[str] = None
    task_chain_progress_summary: Optional[str] = None
    issue_or_risk_summary: Optional[str] = None
    narrative_readable: Optional[str] = None
    process_observation_summary: Optional[str] = None
    # B. 边界写死
    summary_brief_hint_only: bool = True
    summary_not_substitute_for_raw_trace: bool = True
    library_default_reads_summary_entry_not_raw_trace: bool = True
    memory_write_forbidden_from_summary_only: bool = True
    # C. 回溯提示（非内容本体）
    requires_trace_backfill: bool = False
    requires_event_backfill: bool = False
    requires_whitebox_backfill: bool = False
    backfill_reason_summary: str = ""
    post_processing_summary_entry_applied: bool = False
    contract_version: str = "M0.5"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "trace_anchor_id": self.trace_anchor_id,
            "summary_id": self.summary_id,
            "mainline_summary": self.mainline_summary,
            "mainline_state_summary": self.mainline_state_summary,
            "memory_usage_summary": self.memory_usage_summary,
            "source_scheduling_summary": self.source_scheduling_summary,
            "task_chain_progress_summary": self.task_chain_progress_summary,
            "issue_or_risk_summary": self.issue_or_risk_summary,
            "narrative_readable": self.narrative_readable,
            "process_observation_summary": self.process_observation_summary,
            "summary_brief_hint_only": bool(self.summary_brief_hint_only),
            "summary_not_substitute_for_raw_trace": bool(self.summary_not_substitute_for_raw_trace),
            "library_default_reads_summary_entry_not_raw_trace": bool(self.library_default_reads_summary_entry_not_raw_trace),
            "memory_write_forbidden_from_summary_only": bool(self.memory_write_forbidden_from_summary_only),
            "requires_trace_backfill": bool(self.requires_trace_backfill),
            "requires_event_backfill": bool(self.requires_event_backfill),
            "requires_whitebox_backfill": bool(self.requires_whitebox_backfill),
            "backfill_reason_summary": self.backfill_reason_summary,
            "post_processing_summary_entry_applied": bool(self.post_processing_summary_entry_applied),
            "contract_version": self.contract_version,
        }


def _derive_backfill_flags(frame: Dict[str, Any], rsr: Dict[str, Any]) -> tuple[bool, bool, bool, str]:
    reasons: List[str] = []
    issue = _s(rsr.get("issue_or_risk_summary"))
    mem = _s(rsr.get("memory_usage_summary"))
    mls = _s(rsr.get("mainline_state_summary"))
    sch = _s(rsr.get("source_scheduling_summary"))
    blob_all = _blob_lower(issue, mem, mls, sch, rsr.get("mainline_summary"))

    causal_or_issue = bool(issue and issue.strip()) or _mentions_causal_risk(blob_all)
    mem_risk = _memory_conflict_hint(mem)

    req_trace = causal_or_issue or mem_risk
    if causal_or_issue:
        reasons.append("issue_or_causal_signal")
    if mem_risk:
        reasons.append("memory_risk_signal")

    req_ev = False
    ev_snap = rsr.get("structured_event_layer_snapshot") if isinstance(rsr.get("structured_event_layer_snapshot"), dict) else {}
    ev_count = ev_snap.get("event_count")
    if isinstance(ev_count, int) and ev_count < 2 and causal_or_issue:
        req_ev = True
        reasons.append("low_event_count_with_risk")

    if sch and ("override" in sch.lower() or "conflict" in sch.lower() or "覆盖" in sch or "冲突" in sch):
        req_trace = True
        req_ev = True
        reasons.append("scheduling_conflict_signal")

    req_wb = mem_risk or (mem and ("observation" in mem.lower() or "记忆" in mem))
    if req_wb:
        reasons.append("memory_channel_semantics")
    if _any_whitebox_present(frame) and (req_trace or req_ev):
        req_wb = True
        reasons.append("whitebox_recommended_for_deep_reason")

    if not reasons:
        reasons.append("minimal_contract_no_mandatory_backfill")

    return req_trace, req_ev, req_wb, ";".join(dict.fromkeys(reasons))


def build_post_processing_summary_entry(frame: Dict[str, Any]) -> PostProcessingSummaryEntry:
    """
    仅从 run_summary_reference + 已落地 frame 派生契约对象；不修改 Summary、不反写主链。
    """
    if not isinstance(frame, dict):
        return PostProcessingSummaryEntry()

    rsr = _get_rsr_dict(frame)
    if not rsr.get("summary_reference_applied"):
        return PostProcessingSummaryEntry(post_processing_summary_entry_applied=False)

    tid = _s(frame.get("trace_anchor_id"))
    sid = _s(rsr.get("summary_id")) or tid or "unknown"
    entry_id = f"ppse_{sid}"

    req_t, req_e, req_w, br = _derive_backfill_flags(frame, rsr)
    nar = frame.get("mainline_narrative_alignment")
    if nar is not None and hasattr(nar, "to_dict"):
        nar = nar.to_dict()
    nar_brief = _s(nar.get("narrative_brief")) if isinstance(nar, dict) else None
    if not nar_brief:
        nar_brief = (
            f"ctx=summary_reference; source={_s(rsr.get('source_scheduling_summary')) or '—'}; "
            f"task={_s(rsr.get('task_chain_progress_summary')) or '—'}; "
            f"mem={_s(rsr.get('memory_usage_summary')) or '—'}; "
            f"mainline={_s(rsr.get('mainline_state_summary')) or '—'}; "
            f"risk={_s(rsr.get('issue_or_risk_summary')) or '—'}"
        )
    proc_obs = _s(rsr.get("process_observation_summary"))
    if proc_obs:
        br = (br + ";process_observation_hint").strip(";")

    return PostProcessingSummaryEntry(
        entry_id=entry_id,
        trace_anchor_id=tid,
        summary_id=_s(rsr.get("summary_id")),
        mainline_summary=_s(rsr.get("mainline_summary")),
        mainline_state_summary=_s(rsr.get("mainline_state_summary")),
        memory_usage_summary=_s(rsr.get("memory_usage_summary")),
        source_scheduling_summary=_s(rsr.get("source_scheduling_summary")),
        task_chain_progress_summary=_s(rsr.get("task_chain_progress_summary")),
        issue_or_risk_summary=_s(rsr.get("issue_or_risk_summary")),
        narrative_readable=nar_brief[:800],
        process_observation_summary=proc_obs[:320] if proc_obs else None,
        summary_brief_hint_only=True,
        summary_not_substitute_for_raw_trace=True,
        library_default_reads_summary_entry_not_raw_trace=True,
        memory_write_forbidden_from_summary_only=True,
        requires_trace_backfill=req_t,
        requires_event_backfill=req_e,
        requires_whitebox_backfill=req_w,
        backfill_reason_summary=br[:500],
        post_processing_summary_entry_applied=True,
    )
