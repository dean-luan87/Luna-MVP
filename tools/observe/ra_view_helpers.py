from typing import Any, Dict, List
import time

from luna_badge_v1_2.governance.observe.ra_view import (
    SCHEMA_VERSION,
    compute_metrics,
    segment_events,
    diagnose_overreaction,
    build_root_cause_summary,
    build_profile,
)


def build_ra_view(timeline: List[Dict[str, Any]], window: str, generated_at: float) -> Dict[str, Any]:
    metrics = compute_metrics(timeline)
    events = segment_events(timeline)
    diagnostics = diagnose_overreaction(timeline, events)
    root_cause = build_root_cause_summary(events, timeline)
    profile = build_profile(metrics)
    return {
        "schema_version": SCHEMA_VERSION,
        "window": window,
        "timeline": timeline,
        "metrics": metrics,
        "events": events,
        "diagnostics": diagnostics,
        "root_cause_summary": root_cause,
        "correlations": {
            "corr_risk_level_vs_authority_level": metrics.get("corr_risk_level_vs_authority_level", 0.0),
            "corr_gate_blocked_vs_authority_drop": metrics.get("corr_gate_blocked_vs_authority_drop", 0.0),
            "corr_distortion_vs_authority_blocked_recovery": metrics.get(
                "corr_distortion_vs_authority_blocked_recovery", 0.0
            ),
        },
        "behavior_profile": profile,
        "samples": len(timeline),
        "generated_at": generated_at,
    }
