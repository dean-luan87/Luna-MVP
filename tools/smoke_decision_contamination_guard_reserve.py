#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Decision Contamination Guard Reserve M0 — frame + JSONL 一行."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402


def main() -> int:
    ctx = {
        "frame_seq": 1,
        "current_ts": 0.0,
        "trace_anchor_id": "smoke_dc",
        "focus_object_label": "bottle",
        "confirmation_input_type": "unknown",
        "confirmation_input_raw_text": "smoke contamination guard",
        "visual_audit_objects_main": [{"label": "bottle", "bbox": [10, 10, 90, 90], "conf": 0.9}],
    }
    b = DecisionMonitorBuilder()
    frame = b.build(ctx).to_dict()
    dcg = frame.get("decision_contamination_guard_reserve")
    if not isinstance(dcg, dict) or not dcg.get("contamination_guard_applied"):
        print("FAIL: decision_contamination_guard_reserve missing")
        return 1
    if not (dcg.get("contamination_observation_summary") or "").strip():
        print("FAIL: empty contamination_observation_summary")
        return 1
    print("contamination_observation_summary:", (dcg.get("contamination_observation_summary") or "")[:200])
    print("entry_points:", len(dcg.get("potential_entry_points") or []))

    out = ROOT / "logs" / "smoke_decision_contamination_guard_reserve.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"frame": frame}, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
