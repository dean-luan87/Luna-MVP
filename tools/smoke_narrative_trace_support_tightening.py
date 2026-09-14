#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: Narrative-Trace Support Heuristic Tightening M0（短路径，不写长 trace）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402


def _ctx(name: str) -> dict:
    p = ROOT / "tests" / "real_scenarios" / "ctx" / name
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    frame = DecisionMonitorBuilder().build(_ctx("R1_container_real_ctx.json")).to_dict()
    netr = frame.get("narrative_evidence_tension_review")
    if netr is None:
        print("FAIL: narrative_evidence_tension_review missing")
        return 1
    nd = netr.to_dict() if hasattr(netr, "to_dict") else netr
    nt = (nd.get("narrative_trace_support_tension") if isinstance(nd, dict) else None) or "unknown"
    rs = (nd.get("tension_reason_summaries") if isinstance(nd, dict) else None) or {}
    reason = (rs.get("narrative_trace_support") if isinstance(rs, dict) else None) or ""
    readable = (nd.get("tension_review_readable") if isinstance(nd, dict) else None) or ""

    if nt == "unknown":
        print("FAIL: nt is unknown (unexpected for ctx_json)")
        return 1
    if len(str(readable).strip()) < 20:
        print("FAIL: tension_review_readable too short")
        return 1

    out = ROOT / "logs" / "smoke_narrative_trace_support_tightening.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(frame, ensure_ascii=False) + "\n", encoding="utf-8")
    print("wrote:", out)
    print("nt:", nt)
    print("nt_reason:", str(reason)[:200])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

