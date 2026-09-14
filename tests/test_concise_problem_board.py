# -*- coding: utf-8 -*-
"""简洁模式问题区、展示语义、聚合、top 选择回归。"""

from __future__ import annotations

import json
from pathlib import Path

from capabilities.voice.observations.request_trace_alert_presentation import (
    PRESENTATION_DANGER,
    PRESENTATION_OK,
    alert_level_to_presentation_semantic,
)
from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_concise_problem_board import build_concise_problem_board
from capabilities.voice.observations.request_trace_issue_analyzer import analyze_request_trace_issue
from capabilities.voice.observations.request_trace_problem_aggregator import is_degraded_but_handled
from capabilities.voice.observations.request_trace_problem_extractor import extract_problem_summary
from capabilities.voice.observations.request_trace_top_problem_selector import select_top_problem

FIXTURES = Path(__file__).resolve().parent.parent / "docs" / "architecture" / "voice" / "fixtures" / "extracted"


def _load(name: str) -> RequestTraceProblemSummary:
    from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary

    p = FIXTURES / name
    c = RequestTraceChain.from_dict(json.loads(p.read_text(encoding="utf-8")))
    issue, diag = analyze_request_trace_issue(c)
    return extract_problem_summary(c, issue, diag)


def test_presentation_mapping() -> None:
    assert alert_level_to_presentation_semantic("normal") == PRESENTATION_OK
    assert alert_level_to_presentation_semantic("critical") == PRESENTATION_DANGER


def test_board_has_top_and_buckets() -> None:
    items = [
        _load("fixture_piper_ok_001_trace.json"),
        _load("fixture_legacy_rb_003_trace.json"),
    ]
    board = build_concise_problem_board(items, active_limit=5)
    assert board.top_problem is not None
    top, reason = select_top_problem(items)
    assert top is not None
    assert board.top_problem.problem_id == top.problem_id
    assert len(reason) > 0
    legacy = _load("fixture_legacy_rb_003_trace.json")
    assert is_degraded_but_handled(legacy)
    assert board.top_problem is not None and is_degraded_but_handled(board.top_problem)
    assert isinstance(board.counts_by_alert_level, dict)


def test_all_success_empty_top_message() -> None:
    from capabilities.voice.observations.request_trace_problem_summary import RequestTraceProblemSummary

    one = _load("fixture_piper_ok_001_trace.json")
    top, reason = select_top_problem([one])
    assert top is None
    assert "无高优先级" in reason or "成功" in reason
