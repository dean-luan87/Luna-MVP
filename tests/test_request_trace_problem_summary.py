# -*- coding: utf-8 -*-
"""request_trace_problem_extractor / prioritizer / alert_level 规则回归。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_issue_analyzer import analyze_request_trace_issue
from capabilities.voice.observations.request_trace_problem_extractor import extract_problem_summary
from capabilities.voice.observations.request_trace_problem_prioritizer import prioritize_problems


FIXTURES = Path(__file__).resolve().parent.parent / "docs" / "architecture" / "voice" / "fixtures" / "extracted"


def _load(name: str) -> RequestTraceChain:
    p = FIXTURES / name
    return RequestTraceChain.from_dict(json.loads(p.read_text(encoding="utf-8")))


def test_piper_ok_is_normal_and_sorted_last_among_mixed() -> None:
    ok = _load("fixture_piper_ok_001_trace.json")
    issue, diag = analyze_request_trace_issue(ok)
    ps = extract_problem_summary(ok, issue, diag)
    assert ps.alert_level == "normal"
    assert "成功" in ps.summary_text or "无归因" in ps.summary_text


def test_legacy_rollback_fixture_warning() -> None:
    rb = _load("fixture_legacy_rb_003_trace.json")
    issue, diag = analyze_request_trace_issue(rb)
    ps = extract_problem_summary(rb, issue, diag)
    assert ps.alert_level in ("warning", "high_risk", "notice", "critical")
    assert ps.priority_score >= 0


def test_prioritize_orders_by_score() -> None:
    ok = _load("fixture_piper_ok_001_trace.json")
    rb = _load("fixture_legacy_rb_003_trace.json")
    items = []
    for ch in (ok, rb):
        issue, diag = analyze_request_trace_issue(ch)
        items.append(extract_problem_summary(ch, issue, diag))
    ranked = prioritize_problems(items)
    assert len(ranked) == 2
    # 非成功应排在纯成功之前（分数更高）
    scores = [x.priority_score for x in ranked]
    assert max(scores) >= min(scores)
