# -*- coding: utf-8 -*-
"""Narrative-Trace Support Heuristic Tightening M0 单测（只测 nt，不改其它维）。"""

from __future__ import annotations

import json
from pathlib import Path

from decision_monitor.builder import DecisionMonitorBuilder

ROOT = Path(__file__).resolve().parents[1]


def _ctx(name: str) -> dict:
    p = ROOT / "tests" / "real_scenarios" / "ctx" / name
    return json.loads(p.read_text(encoding="utf-8"))


def _nt(frame_dict: dict) -> str:
    netr = frame_dict.get("narrative_evidence_tension_review")
    if netr is not None and hasattr(netr, "to_dict"):
        netr = netr.to_dict()
    d = netr if isinstance(netr, dict) else {}
    return str(d.get("narrative_trace_support_tension") or "unknown")


def _nt_reason(frame_dict: dict) -> str:
    netr = frame_dict.get("narrative_evidence_tension_review")
    if netr is not None and hasattr(netr, "to_dict"):
        netr = netr.to_dict()
    d = netr if isinstance(netr, dict) else {}
    rs = d.get("tension_reason_summaries") or {}
    return str((rs.get("narrative_trace_support") if isinstance(rs, dict) else "") or "")


def test_nt_tightening_produces_signal_but_not_everywhere():
    b = DecisionMonitorBuilder()

    # 代表：薄锚点（baseline case），应出现可解释的 nt 信号
    d1 = b.build(_ctx("R1_container_real_ctx.json")).to_dict()
    nt1 = _nt(d1)
    assert nt1 in ("low", "medium")
    assert "key_anchors" in _nt_reason(d1) or "thin_key_anchors" in _nt_reason(d1)

    # 代表：健康复杂（terminal 对齐），不应被 nt 乱打成 review
    d2 = b.build(_ctx("R87_complex_but_healthy_resume_and_global_progress_real_ctx.json")).to_dict()
    nt2 = _nt(d2)
    assert nt2 in ("none", "low")  # 允许轻微 watch，但不应默认 medium/high

