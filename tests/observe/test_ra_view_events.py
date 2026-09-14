from luna_badge_v1_2.governance.observe.ra_view.events import segment_events
from luna_badge_v1_2.governance.observe.ra_view.diagnostics import diagnose_overreaction
from luna_badge_v1_2.governance.observe.ra_view.root_cause import build_root_cause_summary
from luna_badge_v1_2.governance.observe.ra_view.profile import build_profile


def test_segment_events_empty():
    assert segment_events([]) == []


def test_segment_events_risk_rise():
    timeline = [
        {"ts": 1.0, "risk_level": "LOW", "authority_effective": "A1", "envelope_status": "WITHIN_ENVELOPE"},
        {"ts": 2.0, "risk_level": "MEDIUM", "authority_effective": "A1", "envelope_status": "WITHIN_ENVELOPE"},
    ]
    events = segment_events(timeline)
    assert any(event["type"] == "RISK_RISE" for event in events)


def test_diagnostics_deterministic():
    timeline = [
        {"ts": 1.0, "risk_level": "LOW", "authority_effective": "A1", "envelope_status": "WITHIN_ENVELOPE"},
        {"ts": 2.0, "risk_level": "LOW", "authority_effective": "A3", "envelope_status": "WITHIN_ENVELOPE"},
    ]
    events = segment_events(timeline)
    d1 = diagnose_overreaction(timeline, events)
    d2 = diagnose_overreaction(timeline, events)
    assert d1 == d2


def test_root_cause_hint_limit():
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
    events = segment_events(timeline)
    summary = build_root_cause_summary(events, timeline)
    for entry in summary:
        assert len(entry["cause_hints"]) <= 3


def test_profile_allowed_values():
    profile = build_profile(
        {
            "authority_overreaction_rate": 0.1,
            "envelope_boundary_alignment": 0.9,
            "risk_to_authority_lag_ms_p50": 100,
        }
    )
    assert profile["stability_profile"] in {"calm", "oscillating", "degraded_like"}
    assert profile["safety_margin_profile"] in {"wide", "moderate", "tight"}
    assert profile["recovery_profile"] in {"fast", "delayed", "blocked_often"}
