#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Smoke：Resume Progress Summary Alignment M0（JSONL）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.run_summary_builder import build_run_summary_reference  # noqa: E402
from decision_monitor.task_chain_state_snapshot import build_task_chain_progress_summary  # noqa: E402


def main() -> int:
    ctx_dir = ROOT / "tests" / "real_scenarios" / "ctx"
    samples = (
        "R60_recovery_declared_but_resume_chain_fragile_real_ctx.json",
        "R1_container_real_ctx.json",
    )
    rows = []
    for name in samples:
        ctx = json.loads((ctx_dir / name).read_text(encoding="utf-8"))
        d = DecisionMonitorBuilder().build(ctx).to_dict()
        tcs = d.get("task_chain_state_snapshot")
        if hasattr(tcs, "to_dict"):
            tcs = tcs.to_dict()
        rsr = build_run_summary_reference(d)
        if hasattr(rsr, "to_dict"):
            rsr = rsr.to_dict()
        rows.append(
            {
                "ctx": name,
                "task_resume_target": tcs.get("task_resume_target"),
                "resume_main_align": tcs.get("resume_main_progress_alignment_summary"),
                "task_chain_progress_summary_tail": (build_task_chain_progress_summary(tcs) or "")[-240:],
                "resume_chain_fragility_summary": rsr.get("resume_chain_fragility_summary"),
                "process_observation_head": (rsr.get("process_observation_summary") or "")[:200],
            }
        )
    out = ROOT / "logs" / "smoke_resume_progress_summary_alignment.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(json.dumps({"wrote": str(out), "rows": rows}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
