#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""短 smoke：打印 lg 档位与 tension_review_brief（不写长 trace）。"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from decision_monitor.builder import DecisionMonitorBuilder  # noqa: E402
from decision_monitor.narrative_evidence_tension_review import build_narrative_evidence_tension_review  # noqa: E402


def main() -> int:
    ctx_dir = ROOT / "tests" / "real_scenarios" / "ctx"
    samples = (
        "R1_container_real_ctx.json",
        "R57_summary_looks_ok_but_requires_backfill_real_ctx.json",
        "R4_feedback_effective_real_ctx.json",
    )
    lines = []
    for name in samples:
        p = ctx_dir / name
        if not p.is_file():
            print("missing", p, file=sys.stderr)
            return 1
        ctx = json.loads(p.read_text(encoding="utf-8"))
        d = DecisionMonitorBuilder().build(ctx).to_dict()
        r = build_narrative_evidence_tension_review(d)
        line = {
            "ctx": name,
            "lg": r.local_global_progress_tension,
            "pc": r.phase_closure_outcome_tension,
            "brief": r.tension_review_brief,
            "lg_reason": (r.tension_reason_summaries or {}).get("local_global_progress"),
        }
        lines.append(line)
    out = ROOT / "logs" / "smoke_local_global_progress_gradient.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in lines:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(json.dumps({"wrote": str(out), "samples": lines}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
