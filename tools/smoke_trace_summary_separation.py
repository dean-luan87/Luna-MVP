#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Trace × Summary Separation M0.2 — run_summary_reference + JSONL + aggregator."""

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
        "frame_seq": 7,
        "current_ts": 1.0,
        "trace_anchor_id": "smoke_trace_summary_m02",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "确认",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 90, 90], "conf": 0.9}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    rsr = frame.get("run_summary_reference")
    if not isinstance(rsr, dict) or not rsr.get("summary_reference_applied"):
        print("FAIL: run_summary_reference missing or not applied")
        return 1
    if not (rsr.get("raw_trace_layer_snapshot") or {}).get("layer") == "raw_trace":
        print("FAIL: raw_trace_layer_snapshot missing")
        return 1
    if not (rsr.get("structured_event_layer_snapshot") or {}).get("layer") == "structured_event":
        print("FAIL: structured_event_layer_snapshot missing")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.run_summary_brief or "").strip():
        print("FAIL: snapshot run_summary_brief empty")
        return 1
    if not (snap.raw_trace_layer_one_liner or "").strip():
        print("FAIL: raw_trace_layer_one_liner empty")
        return 1
    print("summary_id:", rsr.get("summary_id"))
    print("summary_brief:", (rsr.get("summary_brief") or "")[:200])
    print("raw one-liner:", (snap.raw_trace_layer_one_liner or "")[:160])
    print("event one-liner:", (snap.structured_event_layer_one_liner or "")[:160])

    out = ROOT / "logs" / "smoke_trace_summary_separation.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
