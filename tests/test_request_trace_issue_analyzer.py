# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EX_DIR = ROOT / "docs" / "architecture" / "voice" / "fixtures" / "extracted"

from capabilities.voice.observations.request_trace_chain import RequestTraceChain  # noqa: E402
from capabilities.voice.observations.request_trace_issue import ISSUE_NONE  # noqa: E402
from capabilities.voice.observations.request_trace_issue_analyzer import (  # noqa: E402
    ISSUE_PROVIDER_CHAIN_FAILURE,
    ISSUE_PROVIDER_UNAVAILABLE,
    analyze_request_trace_issue,
)


@pytest.mark.skipif(not EX_DIR.exists(), reason="fixtures missing")
def test_analyze_piper_success():
    p = EX_DIR / "fixture_piper_ok_001_trace.json"
    c = RequestTraceChain.from_dict(json.loads(p.read_text(encoding="utf-8")))
    issue, diag = analyze_request_trace_issue(c)
    assert issue.primary_issue_type == ISSUE_NONE
    assert diag.final_status == "success"
    assert issue.severity == "info"


@pytest.mark.skipif(not EX_DIR.exists(), reason="fixtures missing")
def test_analyze_legacy_rollback():
    p = EX_DIR / "fixture_legacy_rb_003_trace.json"
    c = RequestTraceChain.from_dict(json.loads(p.read_text(encoding="utf-8")))
    issue, _diag = analyze_request_trace_issue(c)
    assert issue.primary_issue_type in (ISSUE_PROVIDER_UNAVAILABLE, ISSUE_PROVIDER_CHAIN_FAILURE)
    assert issue.final_status in ("degraded_success", "failed", "rollback_success")


@pytest.mark.skipif(not EX_DIR.exists(), reason="fixtures missing")
def test_checkpoints_non_empty():
    p = EX_DIR / "fixture_legacy_rb_003_trace.json"
    c = RequestTraceChain.from_dict(json.loads(p.read_text(encoding="utf-8")))
    issue, _diag = analyze_request_trace_issue(c)
    assert len(issue.recommended_checkpoints) >= 3
