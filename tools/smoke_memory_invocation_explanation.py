#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Memory Invocation Explanation M0.3（短路径）。"""

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
        "frame_seq": 3,
        "current_ts": 1.0,
        "trace_anchor_id": "smoke_mem_m03",
        "focus_object_label": "cup",
        "visual_audit_objects_main": [{"label": "cup", "bbox": [0, 0, 10, 10]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    mie = frame.get("memory_invocation_explanation")
    if not isinstance(mie, dict) or not mie.get("memory_invocation_explanation_applied"):
        print("FAIL: memory_invocation_explanation missing")
        return 1
    rsr = build_run_summary_reference(frame).to_dict()
    if "invoked=" not in (rsr.get("memory_usage_summary") or ""):
        print("FAIL: memory_usage_summary not enhanced")
        return 1
    if "; mem=" not in (rsr.get("summary_brief") or ""):
        print("FAIL: summary_brief missing mem segment")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.memory_invocation_readable or "").strip():
        print("FAIL: aggregator readable missing")
        return 1
    tv = frame.get("reasoning_timeline_view") or {}
    if hasattr(tv, "to_dict"):
        tv = tv.to_dict()
    ev_types = [e.get("event_type") for e in (tv.get("events") or []) if isinstance(e, dict)]
    if "memory_invocation_explained" not in ev_types:
        print("FAIL: timeline missing memory_invocation_explained", ev_types[-6:])
        return 1
    print("effect:", mie.get("memory_invocation_effect_summary"))
    print("memory_usage_summary:", (rsr.get("memory_usage_summary") or "")[:200])
    print("readable:", (snap.memory_invocation_readable or "")[:200])

    out = ROOT / "logs" / "smoke_memory_invocation_explanation.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
