#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Source Scheduling × Whitebox alignment M0.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from tools.reasoning_console_aggregator import aggregate_frame  # noqa: E402


def main() -> int:
    ctx = {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "smoke_sched_align",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "不是这个，重看",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 90, 90], "conf": 0.9}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    sss = frame.get("scheduled_source_state")
    if not isinstance(sss, dict) or not sss.get("scheduled_source_state_applied"):
        print("FAIL: scheduled_source_state missing")
        return 1
    tv = frame.get("reasoning_timeline_view") or {}
    ev_types = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    if "dominant_source_selected" not in ev_types:
        print("FAIL: dominant_source_selected not in timeline")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.scheduled_source_readable_summary or "").strip():
        print("FAIL: readable summary missing in aggregator")
        return 1
    print("readable_summary:", snap.scheduled_source_readable_summary)
    print("warning_summary:", snap.scheduled_source_warning_summary)
    print("events:", "; ".join((sss.get("source_scheduling_event_summaries") or [])[:4]))

    out = ROOT / "logs" / "smoke_source_scheduling_whitebox_alignment.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

