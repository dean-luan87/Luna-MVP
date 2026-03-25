#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Post-Processing Intelligence Reserve M0 — frame + JSONL 一行 + Console 聚合可读。"""

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
        "trace_anchor_id": "smoke_pp_benchmark",
        "focus_object_label": "bottle",
        "confirmation_input_raw_text": "smoke post-processing",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 90, 90], "conf": 0.9}],
    }
    b = DecisionMonitorBuilder()
    frame = b.build(ctx).to_dict()
    pp = frame.get("post_processing_intelligence_reserve")
    if not isinstance(pp, dict) or not pp.get("post_processing_reserve_applied"):
        print("FAIL: post_processing_intelligence_reserve missing")
        return 1
    if not (pp.get("post_processing_summary") or "").strip():
        print("FAIL: empty post_processing_summary")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.post_processing_summary or "").strip():
        print("FAIL: snapshot post_processing_summary empty")
        return 1
    print("post_processing_summary:", (pp.get("post_processing_summary") or "")[:200])
    print("library_link_reserved:", pp.get("library_link_reserved"))
    print("memory_write_reserved:", pp.get("memory_write_reserved"))

    out = ROOT / "logs" / "smoke_post_processing_intelligence_reserve.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
