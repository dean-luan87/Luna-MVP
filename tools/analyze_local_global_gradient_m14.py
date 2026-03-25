# -*- coding: utf-8 -*-
"""
只读：对比两份 real_scenario_pack JSON 中 local_global_progress_tension 分布（tightening 前后）。
不改运行逻辑。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _lg_dist(payload: Dict[str, Any]) -> Dict[str, Any]:
    c: Counter = Counter()
    pc_lg: Counter = Counter()
    for r in payload.get("results") or []:
        n = r.get("narrative_evidence_tension_review") or {}
        if not n or not n.get("narrative_evidence_tension_review_applied"):
            c["(no_tension)"] += 1
            continue
        lg = str(n.get("local_global_progress_tension") or "unknown")
        pc = str(n.get("phase_closure_outcome_tension") or "unknown")
        c[lg] += 1
        pc_lg[(pc, lg)] += 1
    return {
        "local_global_progress_tension": dict(c),
        "pair_pc_lg": {f"{a}|{b}": n for (a, b), n in sorted(pc_lg.items())},
        "pc_high_lg_high_cases": [
            r.get("case_id")
            for r in payload.get("results") or []
            if (r.get("narrative_evidence_tension_review") or {}).get("phase_closure_outcome_tension") == "high"
            and (r.get("narrative_evidence_tension_review") or {}).get("local_global_progress_tension") == "high"
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--before",
        default="logs/real_scenario_pack_m14_pre_lg_gradient.json",
        help="收紧前快照（预先用 cp 保存的 m14）",
    )
    ap.add_argument("--after", default="logs/real_scenario_pack_m14.json")
    ap.add_argument("--out", default="logs/local_global_gradient_analysis_m14.json")
    args = ap.parse_args()
    before_p = Path(args.before)
    after_p = Path(args.after)
    if not before_p.is_file() or not after_p.is_file():
        print("missing before/after json", file=sys.stderr)
        return 1
    b = json.loads(before_p.read_text(encoding="utf-8"))
    a = json.loads(after_p.read_text(encoding="utf-8"))
    report: Dict[str, Any] = {
        "before_path": str(before_p),
        "after_path": str(after_p),
        "before": _lg_dist(b),
        "after": _lg_dist(a),
        "note": "before 应为 Local-Global Gradient Tightening 之前的 m14 快照；after 为收紧后的重跑结果。",
    }
    outp = Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print("wrote:", outp, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
