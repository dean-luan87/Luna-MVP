import argparse
import json
import time
import sys
from pathlib import Path
from typing import Any, Dict, List

_ROOT = Path(__file__).resolve().parents[2]
if str(_ROOT) not in sys.path:
    sys.path.append(str(_ROOT))

from luna_badge_v1_2.governance.risk_center.evaluation.evaluator import evaluate_metrics
from luna_badge_v1_2.governance.observe.ra_view.metrics import compute_metrics as compute_ra_metrics
from luna_badge_v1_2.governance.observe.ra_view.events import segment_events
from luna_badge_v1_2.governance.observe.ra_view.diagnostics import diagnose_overreaction
from luna_badge_v1_2.governance.observe.ra_view.root_cause import build_root_cause_summary
from luna_badge_v1_2.governance.observe.ra_view.profile import build_profile
from luna_badge_v1_2.governance.observe.ra_view.schema import SCHEMA_VERSION as RA_SCHEMA_VERSION


def build_debug_view_payload(timeline: List[Dict[str, Any]], generated_at: float) -> Dict[str, Any]:
    evaluation = evaluate_metrics(timeline, f"last_{len(timeline)}")
    ra_view_timeline = [
        {
            "ts": item.get("authority_panel", {}).get("since", 0.0),
            "authority_effective": item.get("authority_panel", {}).get("effective"),
            "risk_level": item.get("risk_panel", {}).get("level"),
            "envelope_status": item.get("envelope", {}).get("status"),
            "risk_vo_level": item.get("risk_panel", {}).get("vo", {}).get("level"),
            "gate": item.get("gate"),
            "distortion_distorted": item.get("distortion", {}).get("distorted", False),
            "distortion_codes": item.get("distortion", {}).get("codes", []),
            "c_decision": item.get("c_decision"),
            "bc_action": item.get("bc_action"),
            "authority_blocked_by": item.get("authority_panel", {}).get("blocked_by"),
        }
        for item in timeline
    ]
    ra_events = segment_events(ra_view_timeline)
    ra_diagnostics = diagnose_overreaction(ra_view_timeline, ra_events)
    ra_root_cause = build_root_cause_summary(ra_events, ra_view_timeline)
    ra_profile = build_profile(compute_ra_metrics(ra_view_timeline))
    ra_view = {
        "schema_version": RA_SCHEMA_VERSION,
        "window": f"last_{len(ra_view_timeline)}",
        "timeline": ra_view_timeline,
        "metrics": compute_ra_metrics(ra_view_timeline),
        "events_summary": ra_events,
        "diagnostics_summary": ra_diagnostics,
        "root_cause_summary": ra_root_cause,
        "profile_summary": ra_profile,
        "samples": len(ra_view_timeline),
        "generated_at": generated_at,
    }
    return {
        "meta": {"schema_version": "debugview.v1", "generated_at": generated_at},
        "timeline": timeline,
        "evaluation": evaluation.__dict__,
        "risk_authority_view": ra_view,
    }


def load_debug_views(path: str) -> List[Dict[str, Any]]:
    views = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                continue
            bc_snapshot = record.get("decision_trace", {}).get("bc_snapshot")
            if not bc_snapshot:
                continue
            debug_view = bc_snapshot.get("debug_view")
            if debug_view is not None:
                views.append({"ts": bc_snapshot.get("authority", {}).get("since", 0.0), **debug_view})
    return views


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="jsonl file containing decision_trace")
    parser.add_argument("--last", type=int, default=20, help="number of recent snapshots")
    args = parser.parse_args()

    timeline = load_debug_views(args.path)[-args.last :]
    payload = build_debug_view_payload(timeline, time.time())
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
