#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Task Chain Position Explanation M0.1（短路径，不长 trace）。"""

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
        "frame_seq": 2,
        "current_ts": 0.5,
        "trace_anchor_id": "smoke_tc_pos_m01",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [5, 5, 50, 50]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    tcs = frame.get("task_chain_state_snapshot")
    if not isinstance(tcs, dict) or not tcs.get("task_chain_state_snapshot_applied"):
        print("FAIL: task_chain_state_snapshot missing")
        return 1
    if not (tcs.get("task_position_reason_summary") or "").strip():
        print("FAIL: task_position_reason_summary missing")
        return 1
    tv = frame.get("reasoning_timeline_view") or {}
    if hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    ev_types = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    if "task_chain_position_interpreted" not in ev_types:
        print("FAIL: task_chain_position_interpreted not in timeline", ev_types[-8:])
        return 1
    rsr = build_run_summary_reference(frame).to_dict()
    if "main_push_hint=" not in (rsr.get("task_chain_progress_summary") or ""):
        print("FAIL: task_chain_progress_summary not enhanced")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.snapshot_task_position_readable or "").strip():
        print("FAIL: snapshot_task_position_readable missing")
        return 1
    print("task_position_reason:", (tcs.get("task_position_reason_summary") or "")[:120])
    print("task_chain_progress:", (rsr.get("task_chain_progress_summary") or "")[:200])
    print("readable:", (snap.snapshot_task_position_readable or "")[:200])

    out = ROOT / "logs" / "smoke_task_chain_position_explanation_alignment.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
