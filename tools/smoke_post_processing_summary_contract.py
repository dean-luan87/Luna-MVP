#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Summary × Post-Processing Boundary Contract M0.5（短路径）。"""

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
        "frame_seq": 3,
        "current_ts": 1.0,
        "trace_anchor_id": "smoke_pp_m05",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [0, 0, 20, 20]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    ppe = frame.get("post_processing_summary_entry")
    if not isinstance(ppe, dict) or not ppe.get("post_processing_summary_entry_applied"):
        print("FAIL: post_processing_summary_entry missing")
        return 1
    ppi = frame.get("post_processing_intelligence_reserve")
    if hasattr(ppi, "to_dict"):
        ppi = ppi.to_dict()
    if not isinstance(ppi, dict) or not ppi.get("summary_post_processing_entry_id"):
        print("FAIL: summary_post_processing_entry_id not cross-linked")
        return 1
    snap = aggregate_frame(frame)
    if not snap.post_processing_entry_id:
        print("FAIL: aggregator post_processing_entry_id")
        return 1
    print("entry_id:", ppe.get("entry_id"))
    print("backfill:", ppe.get("requires_trace_backfill"), ppe.get("requires_event_backfill"), ppe.get("requires_whitebox_backfill"))
    out = ROOT / "logs" / "smoke_post_processing_summary_contract.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
