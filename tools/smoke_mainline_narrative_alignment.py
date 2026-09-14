#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Mainline Narrative Alignment M0.6（短路径）。"""

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
        "frame_seq": 6,
        "current_ts": 1.2,
        "trace_anchor_id": "smoke_narr_m06",
        "focus_object_label": "bottle",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [0, 0, 20, 20]}],
    }
    frame = DecisionMonitorBuilder().build(ctx).to_dict()
    nar = frame.get("mainline_narrative_alignment")
    if not isinstance(nar, dict) or not nar.get("mainline_narrative_alignment_applied"):
        print("FAIL: mainline_narrative_alignment missing")
        return 1
    rsr = frame.get("run_summary_reference") or {}
    brief = rsr.get("summary_brief") or ""
    for key in ("ctx=", "source=", "task=", "mem=", "mainline=", "closure=", "risk="):
        if key not in brief:
            print("FAIL: summary_brief missing", key)
            return 1
    ppe = frame.get("post_processing_summary_entry") or {}
    if not ppe.get("narrative_readable"):
        print("FAIL: post_processing_summary_entry.narrative_readable missing")
        return 1
    snap = aggregate_frame(frame)
    if not snap.mainline_narrative_readable:
        print("FAIL: aggregator mainline_narrative_readable missing")
        return 1
    print("narrative:", (nar.get("narrative_brief") or "")[:180])

    out = ROOT / "logs" / "smoke_mainline_narrative_alignment.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
