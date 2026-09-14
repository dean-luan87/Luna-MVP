#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NT Coordination Review M0: 只读分析脚本

输入: logs/real_scenario_pack_m18.json
输出: logs/nt_coordination_m18_analysis.json

用途:
- 统计 nt 命中/未命中结构
- 统计与 pc/lg/advisory 的交叉关系
- 产出代表样本，支撑文档复盘
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]


def _s(x: Any) -> str:
    if x is None:
        return ""
    return str(x).strip()


def _read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _row_view(row: Dict[str, Any]) -> Dict[str, Any]:
    net = row.get("narrative_evidence_tension_review") or {}
    if not isinstance(net, dict):
        net = {}
    rs = net.get("tension_reason_summaries") or {}
    if not isinstance(rs, dict):
        rs = {}
    adv = row.get("advisory_sf1_prime_observation") or {}
    if not isinstance(adv, dict):
        adv = {}

    rsr = row.get("run_summary_reference") or {}
    if not isinstance(rsr, dict):
        rsr = {}

    return {
        "case_id": _s(row.get("case_id")),
        "nt": _s(net.get("narrative_trace_support_tension")) or "unknown",
        "pc": _s(net.get("phase_closure_outcome_tension")) or "unknown",
        "lg": _s(net.get("local_global_progress_tension")) or "unknown",
        "severity": _s((row.get("severity_profile") or {}).get("overall_severity_profile")) or "unknown",
        "advisory_hit": bool(adv.get("soft_fail_candidate_observed")),
        "nt_reason": _s(rs.get("narrative_trace_support")),
        "tension_review_readable": _s(net.get("tension_review_readable"))[:260],
        "summary_brief": _s(rsr.get("summary_brief"))[:260],
        "scenario_passed": bool(row.get("scenario_passed")),
    }


def _pick_examples(rows: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    nt_hit = [r for r in rows if r["nt"] in ("low", "medium", "high")]
    pc_lg_tense_nt_none = [r for r in rows if r["nt"] == "none" and (r["pc"] == "high" or r["lg"] == "high")]
    healthy = [r for r in rows if r["nt"] in ("none", "low") and not r["advisory_hit"] and r["severity"] in ("watch", "review")]

    wanted_a = {"R101_long_narrative_sparse_key_anchors_should_raise_nt_real", "R106_entry_summary_smooth_but_key_support_thin_review_only_real"}
    wanted_b = {"R103_nt_supports_pc_lg_but_not_primary_driver_real", "R104_advisory_strong_but_nt_still_none_should_be_acceptable_real"}
    wanted_c = {"R102_long_narrative_with_sufficient_key_support_should_not_raise_nt_real", "R105_complex_healthy_narrative_dense_support_real", "R97_complex_recovery_chain_but_terminal_aligned_real"}

    def first_by_ids(pool: List[Dict[str, Any]], ids: set, fallback_n: int) -> List[Dict[str, Any]]:
        out = [r for r in pool if r["case_id"] in ids]
        if len(out) < fallback_n:
            seen = {r["case_id"] for r in out}
            for r in pool:
                if r["case_id"] in seen:
                    continue
                out.append(r)
                if len(out) >= fallback_n:
                    break
        return out[:fallback_n]

    return {
        "nt_hit_examples": first_by_ids(nt_hit, wanted_a, 4),
        "pc_lg_tense_nt_none_examples": first_by_ids(pc_lg_tense_nt_none, wanted_b, 4),
        "healthy_control_examples": first_by_ids(healthy, wanted_c, 4),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--input",
        type=str,
        default=str(ROOT / "logs" / "real_scenario_pack_m18.json"),
    )
    ap.add_argument(
        "--out",
        type=str,
        default=str(ROOT / "logs" / "nt_coordination_m18_analysis.json"),
    )
    args = ap.parse_args()

    payload = _read_json(Path(args.input))
    results = payload.get("results") or []
    rows = [_row_view(r) for r in results if isinstance(r, dict)]

    nt_counter = Counter(r["nt"] for r in rows)

    cross = {
        "pc_high_nt_none": sum(1 for r in rows if r["pc"] == "high" and r["nt"] == "none"),
        "pc_high_nt_hit": sum(1 for r in rows if r["pc"] == "high" and r["nt"] in ("low", "medium", "high")),
        "lg_high_nt_none": sum(1 for r in rows if r["lg"] == "high" and r["nt"] == "none"),
        "lg_medium_nt_hit": sum(1 for r in rows if r["lg"] == "medium" and r["nt"] in ("low", "medium", "high")),
        "advisory_hit_nt_none": sum(1 for r in rows if r["advisory_hit"] and r["nt"] == "none"),
        "advisory_hit_nt_hit": sum(1 for r in rows if r["advisory_hit"] and r["nt"] in ("low", "medium", "high")),
    }

    nt_hit_rows = [r for r in rows if r["nt"] in ("low", "medium", "high")]
    nt_reason_counter = Counter(r["nt_reason"] for r in nt_hit_rows)

    out = {
        "input": str(args.input),
        "summary": {
            "total_cases": len(rows),
            "nt_distribution": dict(nt_counter),
            "nt_hit_count": len(nt_hit_rows),
            "nt_none_count": nt_counter.get("none", 0),
        },
        "cross_nt_pc_lg_advisory": cross,
        "nt_hit_reason_distribution": dict(nt_reason_counter),
        "examples": _pick_examples(rows),
    }

    out_path = Path(args.out)
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

