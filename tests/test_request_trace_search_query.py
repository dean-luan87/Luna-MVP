# -*- coding: utf-8 -*-
"""request_trace_search_query 问题导向检索回归。"""

from __future__ import annotations

import json
from pathlib import Path

from capabilities.voice.observations.request_trace_chain import RequestTraceChain
from capabilities.voice.observations.request_trace_query import load_chains_from_directory
from capabilities.voice.observations.request_trace_search_entry import RequestTraceSearchEntry
from capabilities.voice.observations.request_trace_search_query import search_chains_to_results

FIXTURES = Path(__file__).resolve().parent.parent / "docs" / "architecture" / "voice" / "fixtures" / "extracted"


def _load_all() -> list[RequestTraceChain]:
    return load_chains_from_directory(str(FIXTURES), "*.json")


def test_search_piper_provider() -> None:
    chains = _load_all()
    entry = RequestTraceSearchEntry(provider_name="piper")
    r = search_chains_to_results(chains, entry)
    assert len(r) >= 1
    assert all((x.provider_name or "").lower() == "piper" for x in r)


def test_problem_focus_rollback() -> None:
    chains = _load_all()
    entry = RequestTraceSearchEntry(problem_focus="rollback")
    r = search_chains_to_results(chains, entry)
    assert len(r) == 1
    assert "legacy_rollback" in r[0].chain_type


def test_alert_level_high_risk() -> None:
    chains = _load_all()
    entry = RequestTraceSearchEntry(alert_level="high_risk")
    r = search_chains_to_results(chains, entry)
    assert len(r) >= 1
    assert r[0].alert_level == "high_risk"
