#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Information Source Scheduler M0 — frame + JSONL + aggregator."""

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
        "trace_anchor_id": "smoke_sched",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "不是这个位置",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 90, 90], "conf": 0.9}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    sss = frame.get("scheduled_source_state")
    if not isinstance(sss, dict) or not sss.get("scheduled_source_state_applied"):
        print("FAIL: scheduled_source_state missing")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.scheduled_dominant_source or "").strip():
        print("FAIL: aggregator missing scheduled_dominant_source")
        return 1
    print("dominant_source:", sss.get("dominant_source"))
    print("conflict:", sss.get("source_conflict_summary"))
    print("override:", sss.get("priority_override_summary"))

    out = ROOT / "logs" / "smoke_information_source_scheduler.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

