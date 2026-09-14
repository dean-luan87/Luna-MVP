# -*- coding: utf-8 -*-
"""
Memory Invocation Explanation M0.3（记忆调用解释）

定位：只解释「当前帧已发生的记忆参与」，不实现记忆选择/写入/评分。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

EFFECT_SUMMARIES = (
    "supports_mainline",
    "neutral_reference",
    "memory_overweight_risk",
    "memory_vs_observation_conflict",
    "memory_vs_task_risk",
    "unknown",
)

MEMORY_TYPE_TAGS = (
    "spatial_memory",
    "task_memory",
    "interaction_memory",
    "historical_pattern",
    "unknown",
)


def _s(x: Any) -> Optional[str]:
    if x is None:
        return None
    t = str(x)
    return t if t.strip() else None


@dataclass
class MemoryInvocationExplanation:
    memory_invoked: bool = False
    memory_type_summary: str = "unknown"
    memory_invocation_reason_summary: str = ""
    memory_invocation_used_content_summary: str = ""
    memory_invocation_effect_summary: str = "unknown"
    memory_invocation_alternative_summary: Optional[str] = None
    memory_invocation_explanation_applied: bool = False
    memory_invocation_timeline_events: List[Dict[str, str]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory_invoked": bool(self.memory_invoked),
            "memory_type_summary": self.memory_type_summary,
            "memory_invocation_reason_summary": self.memory_invocation_reason_summary,
            "memory_invocation_used_content_summary": self.memory_invocation_used_content_summary,
            "memory_invocation_effect_summary": self.memory_invocation_effect_summary,
            "memory_invocation_alternative_summary": self.memory_invocation_alternative_summary,
            "memory_invocation_explanation_applied": bool(self.memory_invocation_explanation_applied),
            "memory_invocation_timeline_events": [dict(x) for x in self.memory_invocation_timeline_events],
        }


def _mn_dict(frame: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    mn = frame.get("memory_novel_information_channel")
    if mn is not None and hasattr(mn, "to_dict"):
        mn = mn.to_dict()
    return mn if isinstance(mn, dict) else None


def _sss_dict(frame: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    s = frame.get("scheduled_source_state")
    if s is not None and hasattr(s, "to_dict"):
        s = s.to_dict()
    return s if isinstance(s, dict) else None


def _infer_memory_types(frame: Dict[str, Any], mn: Optional[Dict[str, Any]]) -> List[str]:
    tags: List[str] = []
    if frame.get("spatial_memory_pools") is not None:
        tags.append("spatial_memory")
    ot = frame.get("object_temporal_ledger")
    if ot is not None and hasattr(ot, "to_dict"):
        ot = ot.to_dict()
    if isinstance(ot, dict) and (ot.get("last_confirmed_location") or ot.get("focus_object_entry")):
        if "spatial_memory" not in tags:
            tags.append("spatial_memory")
    if frame.get("experience_evolution") is not None:
        tags.append("historical_pattern")
    tcs = frame.get("task_chain_state_snapshot")
    if tcs is not None and hasattr(tcs, "to_dict"):
        tcs = tcs.to_dict()
    if isinstance(tcs, dict) and tcs.get("task_chain_state_snapshot_applied"):
        tags.append("task_memory")
    if frame.get("object_search_interaction") is not None:
        tags.append("interaction_memory")
    if mn and int(mn.get("memory_channel_count") or 0) > 0 and not tags:
        tags.append("historical_pattern")
    if not tags:
        tags.append("unknown")
    return tags[:5]


def _reason_summary(frame: Dict[str, Any], mn: Optional[Dict[str, Any]], sss: Optional[Dict[str, Any]]) -> str:
    parts: List[str] = []
    dom = _s(sss.get("dominant_source")) if sss else None
    if dom == "memory_recall":
        parts.append("dominant_source_is_memory_recall")
    etc = frame.get("environment_task_context_reserve")
    if etc is not None and hasattr(etc, "to_dict"):
        etc = etc.to_dict()
    if isinstance(etc, dict):
        prem = _s(etc.get("context_premise_summary")) or ""
        if prem and ("熟悉" in prem or "familiar" in prem.lower()):
            parts.append("familiar_scene_or_premise_hit")
        tc = etc.get("task_chain_context") if isinstance(etc.get("task_chain_context"), dict) else {}
        if _s(tc.get("task_chain_stage")):
            parts.append("task_context_stage_present")
    tcs = frame.get("task_chain_state_snapshot")
    if tcs is not None and hasattr(tcs, "to_dict"):
        tcs = tcs.to_dict()
    if isinstance(tcs, dict) and _s(tcs.get("task_mode")) == "recovering":
        parts.append("recovery_task_context_linked")
    if mn and int(mn.get("novel_channel_count") or 0) == 0 and int(mn.get("memory_channel_count") or 0) > 0:
        parts.append("novel_sparse_memory_channels_active")
    if not parts:
        parts.append("channel_or_scheduler_signal")
    return "; ".join(parts)[:400]


def _used_content_summary(mn: Optional[Dict[str, Any]]) -> str:
    if not mn:
        return "none_observed"
    chans = mn.get("information_channels") or []
    if not isinstance(chans, list):
        return "none_observed"
    bits: List[str] = []
    for c in chans[:6]:
        if not isinstance(c, dict):
            continue
        if c.get("channel_type") != "memory_derived":
            continue
        lab = _s(c.get("channel_label")) or "memory"
        summ = _s(c.get("channel_summary")) or ""
        bits.append(f"{lab}:{summ[:80]}")
    if not bits:
        dr = _s(mn.get("dominant_reasoning_channel"))
        if dr:
            return f"dominant_reasoning_channel={dr}"
        return "memory_markers_only"
    return " | ".join(bits)[:400]


def _effect_summary(sss: Optional[Dict[str, Any]], mn: Optional[Dict[str, Any]]) -> str:
    if not sss:
        return "unknown"
    cfx = _s(sss.get("source_conflict_summary")) or "none"
    over = _s(sss.get("priority_override_summary")) or "none"
    dom = _s(sss.get("dominant_source")) or ""
    if cfx == "memory_vs_observation":
        return "memory_vs_observation_conflict"
    if cfx == "task_vs_feedback" and dom == "memory_recall":
        return "memory_vs_task_risk"
    if over == "task_over_memory":
        return "supports_mainline"
    if dom == "memory_recall" and cfx in ("none", "unknown"):
        return "memory_overweight_risk"
    if mn and _s(mn.get("dominant_reasoning_channel")) == "memory_derived":
        if cfx in ("none", "unknown") and dom != "memory_recall":
            return "neutral_reference"
    if dom and dom != "memory_recall":
        return "neutral_reference"
    return "unknown"


def _alternatives(sss: Optional[Dict[str, Any]]) -> Optional[str]:
    if not sss:
        return None
    ps = sss.get("participating_sources")
    if not isinstance(ps, list) or len(ps) < 2:
        return None
    others = [str(x) for x in ps if str(x) != "memory_recall"]
    if not others:
        return None
    return "candidates=" + ",".join(others[:5])


def _timeline_events(
    invoked: bool,
    effect: str,
    reason: str,
) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    if not invoked:
        return out
    out.append({"event_type": "memory_invocation_explained", "summary": reason[:220]})
    if effect == "supports_mainline":
        out.append({"event_type": "memory_invocation_supports_mainline", "summary": "effect=supports_mainline"})
    if effect in ("memory_overweight_risk", "memory_vs_observation_conflict", "memory_vs_task_risk"):
        out.append({"event_type": "memory_invocation_risk_detected", "summary": f"effect={effect}"})
    if effect == "memory_vs_observation_conflict":
        out.append(
            {
                "event_type": "memory_invocation_conflict_with_observation",
                "summary": "scheduler_conflict=memory_vs_observation",
            }
        )
    return out[:6]


def build_memory_usage_summary_line(frame: Dict[str, Any], mie: Optional[Dict[str, Any]] = None) -> str:
    """供 run_summary：合并通道摘要与调用解释（轻量一行）。"""
    mn = _mn_dict(frame)
    base = ""
    if isinstance(mn, dict):
        base = _s(mn.get("channel_summary")) or ""
        if not base.strip():
            dr = mn.get("dominant_reasoning_channel")
            dd = mn.get("dominant_decision_channel")
            base = f"reasoning_channel={dr}; decision_channel={dd}"
    md = mie
    if md is None:
        raw = frame.get("memory_invocation_explanation")
        if raw is not None and hasattr(raw, "to_dict"):
            md = raw.to_dict()
        elif isinstance(raw, dict):
            md = raw
    if not isinstance(md, dict) or not md.get("memory_invocation_explanation_applied"):
        return base or "memory: no_invocation_explanation"
    inv = "yes" if md.get("memory_invoked") else "no"
    eff = _s(md.get("memory_invocation_effect_summary")) or "unknown"
    rsn = _s(md.get("memory_invocation_reason_summary")) or "—"
    typ = _s(md.get("memory_type_summary")) or "unknown"
    return (
        f"invoked={inv}; type={typ}; effect={eff}; reason={rsn[:160]}"
        + (f" | channel={base[:120]}" if base else "")
    )[:700]


def build_memory_invocation_explanation(frame: Dict[str, Any]) -> MemoryInvocationExplanation:
    if not isinstance(frame, dict):
        return MemoryInvocationExplanation(memory_invocation_explanation_applied=False)

    mn = _mn_dict(frame)
    sss = _sss_dict(frame)

    mem_count = int(mn.get("memory_channel_count") or 0) if mn else 0
    dom_src = _s(sss.get("dominant_source")) if sss else None
    invoked = bool(mem_count > 0 or dom_src == "memory_recall")

    types = _infer_memory_types(frame, mn)
    type_summary = "+".join(types) if types else "unknown"

    reason = _reason_summary(frame, mn, sss)
    used = _used_content_summary(mn)
    effect = _effect_summary(sss, mn)
    if not invoked:
        effect = "unknown"
        reason = "memory_not_selected_this_frame"
        used = "n/a"

    alt = _alternatives(sss)
    tl = _timeline_events(invoked, effect, reason)

    return MemoryInvocationExplanation(
        memory_invoked=invoked,
        memory_type_summary=type_summary,
        memory_invocation_reason_summary=reason,
        memory_invocation_used_content_summary=used,
        memory_invocation_effect_summary=effect if effect in EFFECT_SUMMARIES else "unknown",
        memory_invocation_alternative_summary=alt,
        memory_invocation_explanation_applied=True,
        memory_invocation_timeline_events=tl,
    )
