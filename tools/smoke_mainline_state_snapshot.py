#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Mainline State / Phase M0.4（短路径）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.run_summary_builder import build_run_summary_reference  # noqa: E402
from tools.reasoning_console_aggregator import aggregate_frame  # noqa: E402


def main() -> int:
    ctx = {
        "frame_seq": 5,
        "current_ts": 1.0,
        "trace_anchor_id": "smoke_mls_m04",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [0, 0, 20, 20]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    mss = frame.get("mainline_state_snapshot")
    if not isinstance(mss, dict) or not mss.get("mainline_state_snapshot_applied"):
        print("FAIL: mainline_state_snapshot missing")
        return 1
    rsr = build_run_summary_reference(frame).to_dict()
    if "state=" not in (rsr.get("mainline_state_summary") or ""):
        print("FAIL: mainline_state_summary missing")
        return 1
    if "; mls=" not in (rsr.get("summary_brief") or ""):
        print("FAIL: summary_brief missing mls segment")
        return 1
    snap = aggregate_frame(frame)
    if not snap.snapshot_mainline_state:
        print("FAIL: aggregator snapshot_mainline_state")
        return 1
    tv = frame.get("reasoning_timeline_view") or {}
    if hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    ev_types = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    if "mainline_state_snapshot_formed" not in ev_types:
        print("FAIL: timeline missing mainline_state_snapshot_formed")
        return 1
    print("state:", mss.get("mainline_state"), "phase:", mss.get("mainline_phase"))
    print("mainline_state_summary:", (rsr.get("mainline_state_summary") or "")[:120])

    out = ROOT / "logs" / "smoke_mainline_state_snapshot.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
