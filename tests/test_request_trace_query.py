# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
EX_DIR = ROOT / "docs" / "architecture" / "voice" / "fixtures" / "extracted"

from capabilities.voice.observations.request_trace_query import (  # noqa: E402
    TraceQuery,
    filter_summaries,
    load_chains_from_directory,
)
from capabilities.voice.observations.request_trace_summary import normalize_chain_type_for_query  # noqa: E402


@pytest.mark.skipif(not EX_DIR.exists(), reason="fixtures missing")
def test_load_and_filter_chain_type():
    chains = load_chains_from_directory(str(EX_DIR))
    assert len(chains) >= 2
    q = TraceQuery(chain_type="legacy_rollback")
    s = filter_summaries(chains, q)
    assert len(s) == 1
    assert s[0].request_id == "fixture_legacy_rb_003"


@pytest.mark.skipif(not EX_DIR.exists(), reason="fixtures missing")
def test_filter_piper_provider():
    chains = load_chains_from_directory(str(EX_DIR))
    q = TraceQuery(provider_name="piper")
    s = filter_summaries(chains, q)
    ids = {x.request_id for x in s}
    assert "fixture_piper_ok_001" in ids


def test_normalize_chain_type():
    assert normalize_chain_type_for_query("success_chain") == "success"
