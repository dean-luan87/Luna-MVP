#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Task Chain State Snapshot M0 — frame + scheduled + JSONL + aggregator."""

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
        "frame_seq": 9,
        "current_ts": 2.0,
        "trace_anchor_id": "smoke_tcs_m0",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 90, 90]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    tcs = frame.get("task_chain_state_snapshot")
    if not isinstance(tcs, dict) or not tcs.get("task_chain_state_snapshot_applied"):
        print("FAIL: task_chain_state_snapshot missing")
        return 1
    sched = frame.get("scheduled_source_state") or {}
    if "task_state" not in (sched.get("participating_sources") or []):
        print("FAIL: task_state not in participating_sources")
        return 1
    rsr = frame.get("run_summary_reference")
    if not isinstance(rsr, dict) or not (rsr.get("task_chain_progress_summary") or "").strip():
        print("FAIL: run_summary missing task_chain_progress_summary")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.snapshot_task_mode or "").strip():
        print("FAIL: aggregator snapshot_task_mode empty")
        return 1
    print("task_mode:", tcs.get("task_mode"), "stage:", tcs.get("task_chain_stage"))
    print("task_state_presence:", (sched.get("task_state_presence_summary") or "")[:120])
    print("task_chain_progress:", (rsr.get("task_chain_progress_summary") or "")[:160])

    out = ROOT / "logs" / "smoke_task_chain_state_snapshot.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
