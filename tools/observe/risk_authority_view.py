import argparse
import json
import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from luna_badge_v1_2.governance.observe.ra_view import (
    SCHEMA_VERSION,
    read_timeline,
    compute_metrics,
    segment_events,
    diagnose_overreaction,
    build_root_cause_summary,
    build_profile,
)


def _filter_window(timeline, window: str):
    if window.startswith("last_") and window.endswith("min"):
        minutes = float(window.replace("last_", "").replace("min", ""))
        cutoff = time.time() - minutes * 60
        return [item for item in timeline if item.get("ts", 0.0) >= cutoff]
    if window.startswith("last_"):
        count = int(window.replace("last_", ""))
        return timeline[-count:]
    return timeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="jsonl file containing decision_trace")
    parser.add_argument("--window", default="last_100", help="window spec: last_10min or last_100")
    parser.add_argument("--out", required=True, help="output json report")
    args = parser.parse_args()

    timeline = read_timeline(args.input)
    timeline = _filter_window(timeline, args.window)
    metrics = compute_metrics(timeline)
    events = segment_events(timeline)
    diagnostics = diagnose_overreaction(timeline, events)
    root_cause = build_root_cause_summary(events, timeline)
    profile = build_profile(metrics)

    report = {
        "schema_version": SCHEMA_VERSION,
        "window": args.window,
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
        "generated_at": time.time(),
    }

    with open(args.out, "w") as f:
        f.write(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
