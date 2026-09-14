# -*- coding: utf-8 -*-
"""Request trace extractor 最小单测（不跑主链）。"""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "docs" / "architecture" / "voice" / "fixtures" / "min_trace_samples.jsonl"

from capabilities.voice.observations.request_trace_extractor import (  # noqa: E402
    CHAIN_FALLBACK,
    CHAIN_ROLLBACK,
    CHAIN_SUCCESS,
    extract_trace_from_paths,
)


@pytest.mark.skipif(not FIXTURE.exists(), reason="fixture missing")
def test_fixture_piper_success():
    c = extract_trace_from_paths([FIXTURE], request_id="fixture_piper_ok_001")
    assert c.chain_type == CHAIN_SUCCESS
    assert c.final_execution_mode == "provider_chain"
    assert c.provider_name == "piper"


@pytest.mark.skipif(not FIXTURE.exists(), reason="fixture missing")
def test_fixture_provider_fallback():
    c = extract_trace_from_paths([FIXTURE], request_id="fixture_provider_fallback_002")
    assert c.chain_type == CHAIN_FALLBACK
    assert c.final_execution_mode == "provider_chain"
    assert c.provider_name == "piper"


@pytest.mark.skipif(not FIXTURE.exists(), reason="fixture missing")
def test_fixture_legacy_rollback():
    c = extract_trace_from_paths([FIXTURE], request_id="fixture_legacy_rb_003")
    assert c.chain_type == CHAIN_ROLLBACK
    assert c.final_execution_mode == "legacy_fallback"


@pytest.mark.skipif(not FIXTURE.exists(), reason="fixture missing")
def test_trace_id_filter():
    c = extract_trace_from_paths([FIXTURE], trace_id="trace_fixture_001")
    assert c.request_id == "fixture_piper_ok_001"
