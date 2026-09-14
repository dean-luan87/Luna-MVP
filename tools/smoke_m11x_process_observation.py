#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke: M1.1.x-A 过程观察增强（短路径）。"""

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


def _check(frame: dict, key: str) -> bool:
    rsr = frame.get("run_summary_reference") or {}
    pse = frame.get("post_processing_summary_entry") or {}
    tv = frame.get("reasoning_timeline_view") or {}
    events = tv.get("events") or []
    etypes = [e.get("event_type") for e in events if isinstance(e, dict)]
    return bool(
        rsr.get("process_observation_summary")
        and rsr.get(key)
        and pse.get("process_observation_summary")
        and len(etypes) > 0
    )


def main() -> int:
    c60 = DecisionMonitorBuilder().build(_ctx("R60_recovery_declared_but_resume_chain_fragile_real_ctx.json")).to_dict()
    c61 = DecisionMonitorBuilder().build(_ctx("R61_memory_bias_accumulated_under_familiar_context_real_ctx.json")).to_dict()
    c64 = DecisionMonitorBuilder().build(_ctx("R64_phase_correct_but_closure_semantics_misaligned_real_ctx.json")).to_dict()

    ok60 = _check(c60, "resume_chain_fragility_summary")
    ok61 = _check(c61, "memory_bias_accumulation_summary")
    ok64 = _check(c64, "closure_semantics_misalignment_summary")
    if not (ok60 and ok61 and ok64):
        print("FAIL: process observation anchors missing", ok60, ok61, ok64)
        return 1

    out = ROOT / "logs" / "smoke_m11x_process_observation.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "\n".join(
            [
                json.dumps(c60, ensure_ascii=False),
                json.dumps(c61, ensure_ascii=False),
                json.dumps(c64, ensure_ascii=False),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print("wrote:", out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
