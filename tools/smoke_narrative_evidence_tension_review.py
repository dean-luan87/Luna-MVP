#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Narrative / Evidence Tension Review M0（短路径，不写长 trace）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from tools.reasoning_console_aggregator import aggregate_frame  # noqa: E402


def _ctx(name: str) -> dict:
    p = ROOT / "tests" / "real_scenarios" / "ctx" / name
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    frame = DecisionMonitorBuilder().build(_ctx("R68_narrative_smooth_but_trace_support_weak_real_ctx.json")).to_dict()
    netr = frame.get("narrative_evidence_tension_review")
    if netr is None:
        print("FAIL: narrative_evidence_tension_review missing")
        return 1
    if hasattr(netr, "to_dict"):
        nd = netr.to_dict()
    else:
        nd = netr
    if not nd.get("narrative_evidence_tension_review_applied"):
        print("FAIL: review not applied")
        return 1
    tr = (nd.get("tension_review_readable") or "").strip()
    if len(tr) < 20:
        print("FAIL: tension_review_readable too short")
        return 1
    snap = aggregate_frame(frame)
    if not (snap.tension_review_readable or "").strip():
        print("FAIL: aggregator missing tension_review_readable")
        return 1

    out = ROOT / "logs" / "smoke_narrative_evidence_tension_review.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    print("tension_review_readable (head):", tr[:200].replace("\n", " / "))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
