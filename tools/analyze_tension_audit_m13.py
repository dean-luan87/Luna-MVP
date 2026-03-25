#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
离线分析：从 real_scenario_pack_m13.json 统计 narrative_evidence_tension_review 分布。
只读，不改运行逻辑、不改 benchmark。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

DIMS = (
    "narrative_trace_support_tension",
    "phase_closure_outcome_tension",
    "summary_backfill_tension",
    "local_global_progress_tension",
    "memory_bias_tension",
)
LEVELS = ("none", "low", "medium", "high", "unknown")
RANK = {"none": 0, "low": 1, "medium": 2, "high": 3, "unknown": -1}


def _net(row: Dict[str, Any]) -> Dict[str, Any]:
    n = row.get("narrative_evidence_tension_review")
    return n if isinstance(n, dict) else {}


def score_row(net: Dict[str, Any]) -> int:
    return sum(max(0, RANK.get(net.get(d), 0)) for d in DIMS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        type=str,
        default=str(ROOT / "logs" / "real_scenario_pack_m13.json"),
        help="Path to real_scenario_pack_m13.json",
    )
    ap.add_argument("--json-out", type=str, default=None, help="Optional JSON summary path")
    args = ap.parse_args()

    path = Path(args.input)
    if not path.is_file():
        print(f"missing: {path}", file=sys.stderr)
        return 1

    payload = json.loads(path.read_text(encoding="utf-8"))
    results: List[Dict[str, Any]] = payload.get("results") or []
    if not results:
        print("no results", file=sys.stderr)
        return 1

    per_dim: Dict[str, Counter] = {d: Counter() for d in DIMS}
    medium_high_count = 0
    rows_scored: List[Tuple[int, str, Dict[str, Any]]] = []

    for row in results:
        cid = row.get("case_id") or "?"
        net = _net(row)
        mh = False
        for d in DIMS:
            v = net.get(d) or "unknown"
            if v not in LEVELS:
                v = "unknown"
            per_dim[d][v] += 1
            if v in ("medium", "high"):
                mh = True
        if mh:
            medium_high_count += 1
        rows_scored.append((score_row(net), cid, net))

    rows_scored.sort(key=lambda x: -x[0])

    # multi high: count dims at high per case
    high_4plus = []
    all_high_like = []
    for s, cid, net in rows_scored:
        highs = sum(1 for d in DIMS if net.get(d) == "high")
        if highs >= 4:
            high_4plus.append(cid)
        if highs == 5:
            all_high_like.append(cid)

    low_tension = [cid for s, cid, net in rows_scored if score_row(net) <= 3]

    distinctiveness = {}
    for d in DIMS:
        c = per_dim[d]
        n = sum(c.values()) or 1
        # simple: fraction at mode (most common level) — high concentration = low distinctiveness
        mode_v, mode_n = c.most_common(1)[0]
        distinctiveness[d] = {
            "mode_level": mode_v,
            "mode_fraction": round(mode_n / n, 4),
            "high_fraction": round((c.get("high", 0)) / n, 4),
            "medium_high_fraction": round((c.get("medium", 0) + c.get("high", 0)) / n, 4),
        }

    out: Dict[str, Any] = {
        "source": str(path),
        "total_cases": len(results),
        "cases_with_any_medium_or_high": medium_high_count,
        "per_dimension_counts": {d: dict(per_dim[d]) for d in DIMS},
        "distinctiveness": distinctiveness,
        "top_10_by_tension_score": [{"case_id": cid, "score": s, "brief": net.get("tension_review_brief")} for s, cid, net in rows_scored[:10]],
        "cases_with_4plus_high_dims": high_4plus[:20],
        "cases_with_all_five_high": all_high_like,
        "low_tension_score_cases": low_tension[:15],
        "note": "score = sum rank(none=0,low=1,medium=2,high=3) per dimension; unknown treated as 0 for score",
    }

    text = json.dumps(out, ensure_ascii=False, indent=2)
    print(text)

    if args.json_out:
        outp = Path(args.json_out)
        outp.parent.mkdir(parents=True, exist_ok=True)
        outp.write_text(text, encoding="utf-8")
        print("wrote:", outp, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
