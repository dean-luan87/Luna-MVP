# -*- coding: utf-8 -*-
"""
只读：从 logs/real_scenario_pack_m14.json 统计 severity / 原始张力 / 组合分布。
供 docs/SEVERITY_SIGNAL_GAP_REVIEW_M0.md 与后续复盘使用；不改评测规则。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.tension_severity_profile_map import map_severity_profile_m14  # noqa: E402


def _net_from_review(rv: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "narrative_evidence_tension_review_applied": True,
        "narrative_trace_support_tension": rv.get("narrative_trace_support_tension", "unknown"),
        "phase_closure_outcome_tension": rv.get("phase_closure_outcome_tension", "unknown"),
        "summary_backfill_tension": rv.get("summary_backfill_tension", "unknown"),
        "local_global_progress_tension": rv.get("local_global_progress_tension", "unknown"),
        "memory_bias_tension": rv.get("memory_bias_tension", "unknown"),
    }


def analyze_pack(path: Path) -> Dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    results: List[Dict[str, Any]] = data.get("results") or []

    overall_c = Counter()
    raw_pc_lg = Counter()
    raw_nt = Counter()
    raw_pc = Counter()
    raw_lg = Counter()
    nt_reason = Counter()
    pc_reason = Counter()
    lg_reason = Counter()

    cases_by_combo: Dict[str, List[str]] = defaultdict(list)
    review_drivers: Counter = Counter()

    mb_sb_both_high = 0
    cases_mb_sb_high: List[str] = []

    for r in results:
        cid = r.get("case_id") or "?"
        rv = r.get("narrative_evidence_tension_review")
        if not isinstance(rv, dict) or not rv.get("narrative_evidence_tension_review_applied"):
            overall_c["no_tension_object"] += 1
            cases_by_combo["no_tension_object"].append(cid)
            continue

        nt = str(rv.get("narrative_trace_support_tension") or "unknown")
        pc = str(rv.get("phase_closure_outcome_tension") or "unknown")
        lg = str(rv.get("local_global_progress_tension") or "unknown")
        sb = str(rv.get("summary_backfill_tension") or "unknown")
        mb = str(rv.get("memory_bias_tension") or "unknown")

        raw_pc_lg[(pc, lg)] += 1
        raw_nt[nt] += 1
        raw_pc[pc] += 1
        raw_lg[lg] += 1

        rs = rv.get("tension_reason_summaries") or {}
        if isinstance(rs, dict):
            nt_reason[str(rs.get("narrative_trace_support") or "")] += 1
            pc_reason[str(rs.get("phase_closure_outcome") or "")] += 1
            lg_reason[str(rs.get("local_global_progress") or "")] += 1

        if sb == "high" and mb == "high":
            mb_sb_both_high += 1
            cases_mb_sb_high.append(cid)

        net = _net_from_review(rv)
        prof = map_severity_profile_m14(net)
        if prof:
            ov = str(prof.get("overall_severity_profile") or "unknown")
            overall_c[ov] += 1
            per = prof.get("per_dimension") or {}
            if per.get("pc") == "review":
                review_drivers["pc_review"] += 1
            if per.get("lg") in ("review", "critical_candidate"):
                review_drivers["lg_review_or_higher"] += 1
            if per.get("nt") == "review":
                review_drivers["nt_review"] += 1
            if ov == "critical_candidate":
                review_drivers["overall_critical_candidate"] += 1

        key = f"pc={pc}|lg={lg}"
        cases_by_combo[key].append(cid)

    # 关键组合
    pc_high_lg_high = cases_by_combo.get("pc=high|lg=high", [])
    pc_high_lg_med = cases_by_combo.get("pc=high|lg=medium", [])
    pc_none_lg_high = cases_by_combo.get("pc=none|lg=high", [])

    special = {
        "R81_story_more_complete_than_trace_support_real": None,
        "R82_phase_closure_progress_pair_near_critical_candidate_real": None,
    }
    for r in results:
        cid = r.get("case_id")
        if cid in special:
            rv = r.get("narrative_evidence_tension_review") or {}
            special[cid] = {
                "narrative_trace_support_tension": rv.get("narrative_trace_support_tension"),
                "phase_closure_outcome_tension": rv.get("phase_closure_outcome_tension"),
                "local_global_progress_tension": rv.get("local_global_progress_tension"),
                "tension_review_brief": rv.get("tension_review_brief"),
                "nt_reason": (rv.get("tension_reason_summaries") or {}).get("narrative_trace_support"),
                "lg_reason": (rv.get("tension_reason_summaries") or {}).get("local_global_progress"),
            }

    rd = dict(review_drivers)
    for k in ("pc_review", "lg_review_or_higher", "nt_review", "overall_critical_candidate"):
        rd.setdefault(k, 0)

    return {
        "source": str(path),
        "total_results": len(results),
        "overall_severity_profile_counts": dict(overall_c),
        "raw_pair_pc_lg_counts": {f"{a}|{b}": c for (a, b), c in sorted(raw_pc_lg.items())},
        "raw_narrative_trace_support_tension": dict(raw_nt),
        "raw_phase_closure_outcome_tension": dict(raw_pc),
        "raw_local_global_progress_tension": dict(raw_lg),
        "top_nt_reasons": dict(nt_reason.most_common(12)),
        "top_pc_reasons": dict(pc_reason.most_common(12)),
        "top_lg_reasons": dict(lg_reason.most_common(12)),
        "count_mb_high_and_sb_high": mb_sb_both_high,
        "cases_pc_high_lg_high": pc_high_lg_high,
        "cases_pc_high_lg_medium": pc_high_lg_med,
        "cases_pc_none_lg_high": pc_none_lg_high,
        "review_driver_counts": rd,
        "special_cases_R81_R82": special,
        "mapping_note": (
            "critical_candidate in map_severity_profile_m14 requires raw "
            "phase_closure_outcome_tension==high AND local_global_progress_tension==high "
            "in the same frame (tools/tension_severity_profile_map.py)."
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        default="logs/real_scenario_pack_m14.json",
        help="real_scenario_pack m14 JSON",
    )
    ap.add_argument(
        "--out",
        default="logs/severity_signal_gap_m14_analysis.json",
        help="write structured analysis JSON",
    )
    args = ap.parse_args()
    inp = Path(args.input)
    out = Path(args.out)
    report = analyze_pack(inp)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
