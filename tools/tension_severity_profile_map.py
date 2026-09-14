# -*- coding: utf-8 -*-
"""
M1.4+：将 narrative_evidence_tension_review 原始档位映射为
severity 风险画像（none / watch / review / critical_candidate）。

依据：docs/TENSION_SEVERITY_PROFILE_SPEC_M0.md（解读层，不参与 harness 判定）。
"""

from __future__ import annotations

from typing import Any, Dict, Optional

RAW_KEYS = (
    "narrative_trace_support_tension",
    "phase_closure_outcome_tension",
    "summary_backfill_tension",
    "local_global_progress_tension",
    "memory_bias_tension",
)


def _g(net: Dict[str, Any], k: str) -> str:
    v = net.get(k)
    if v is None:
        return "unknown"
    t = str(v).strip()
    return t if t else "unknown"


def map_severity_profile_m14(net: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    文档化映射：单轮结果；critical_candidate 仅当「pc=high 且 lg=high」同帧（与 Spec 一致）。
    """
    if not isinstance(net, dict) or not net.get("narrative_evidence_tension_review_applied"):
        return None

    nt = _g(net, "narrative_trace_support_tension")
    pc = _g(net, "phase_closure_outcome_tension")
    sb = _g(net, "summary_backfill_tension")
    lg = _g(net, "local_global_progress_tension")
    mb = _g(net, "memory_bias_tension")

    per: Dict[str, str] = {}

    # nt
    if nt in ("none", "unknown"):
        per["nt"] = "none"
    elif nt == "low":
        per["nt"] = "watch"
    elif nt in ("medium", "high"):
        per["nt"] = "review"
    else:
        per["nt"] = "none"

    # pc（有区分力）
    if pc == "high":
        per["pc"] = "review"
    elif pc == "none":
        per["pc"] = "none"
    else:
        per["pc"] = "watch"

    # sb / mb：饱和维 → 默认 watch
    if sb == "high":
        per["sb"] = "watch"
    elif sb == "none":
        per["sb"] = "none"
    else:
        per["sb"] = "watch"

    if mb == "high":
        per["mb"] = "watch"
    elif mb == "none":
        per["mb"] = "none"
    else:
        per["mb"] = "watch"

    # lg：与 pc 配对
    if lg == "high":
        per["lg"] = "critical_candidate" if pc == "high" else "review"
    elif lg == "medium":
        per["lg"] = "review" if pc == "high" else "watch"
    elif lg in ("none", "unknown"):
        per["lg"] = "none"
    else:
        per["lg"] = "watch"

    # overall（单轮）
    if pc == "high" and lg == "high":
        overall = "critical_candidate"
    elif per["pc"] == "review" or per["lg"] in ("review", "critical_candidate"):
        overall = "review"
    elif per["nt"] == "review":
        overall = "review"
    elif any(per[k] == "watch" for k in ("sb", "mb", "lg", "nt")):
        overall = "watch"
    else:
        overall = "none"

    return {
        "profile_version": "M1.4",
        "per_dimension": per,
        "overall_severity_profile": overall,
        "notes": "documentary_mapping; not hard-fail; see TENSION_SEVERITY_PROFILE_SPEC_M0.md",
    }
