import json
import pytest
from pathlib import Path

from luna_badge_v1_2.governance.observe.ra_view.reader import read_timeline
from luna_badge_v1_2.governance.observe.ra_view.metrics import compute_metrics
from luna_badge_v1_2.governance.observe.ra_view.events import segment_events
from luna_badge_v1_2.governance.observe.ra_view.root_cause import build_root_cause_summary
from luna_badge_v1_2.governance.observe.ra_view.profile import build_profile


def test_v1_2_deterministic():
    timeline = [
        {"ts": 1.0, "authority_effective": "A1", "risk_level": "LOW", "envelope_status": "WITHIN_ENVELOPE"},
        {"ts": 2.0, "authority_effective": "A2", "risk_level": "MEDIUM", "envelope_status": "ADMISSIBLE"},
    ]
    metrics = compute_metrics(timeline)
    events = segment_events(timeline)
    r1 = build_root_cause_summary(events, timeline)
    r2 = build_root_cause_summary(events, timeline)
    assert metrics == compute_metrics(timeline)
    assert r1 == r2


def test_reader_rejects_forbidden_fields(tmp_path: Path):
    path = tmp_path / "run.jsonl"
    record = {"decision_trace": {"bc_snapshot": {"abilities": {"allow_output": True}, "debug_view": {}}}}
    path.write_text(json.dumps(record) + "\n")
    with pytest.raises(AssertionError):
        read_timeline(str(path))


def test_root_cause_hints_limit():
    timeline = [
        {
            "ts": 1.0,
            "risk_level": "LOW",
            "authority_effective": "A1",
            "envelope_status": "WITHIN_ENVELOPE",
            "gate": "BLOCK",
            "distortion_distorted": True,
            "c_decision": "STOP",
            "authority_blocked_by": "HYSTERESIS",
        },
        {
            "ts": 2.0,
            "risk_level": "HIGH",
            "authority_effective": "A1",
            "envelope_status": "ADMISSIBLE",
            "gate": "BLOCK",
            "distortion_distorted": True,
            "c_decision": "STOP",
            "authority_blocked_by": "HYSTERESIS",
        },
    ]
    summary = build_root_cause_summary(segment_events(timeline), timeline)
    for entry in summary:
        assert len(entry["cause_hints"]) <= 3


def test_profile_allowed_values():
    profile = build_profile(
        {
            "authority_overreaction_rate": 0.3,
            "envelope_boundary_alignment": 0.2,
            "risk_to_authority_lag_ms_p50": 1200,
        }
    )
    assert profile["stability_profile"] in {"calm", "oscillating", "degraded_like"}
    assert profile["safety_margin_profile"] in {"wide", "moderate", "tight"}
    assert profile["recovery_profile"] in {"fast", "delayed", "blocked_often"}
