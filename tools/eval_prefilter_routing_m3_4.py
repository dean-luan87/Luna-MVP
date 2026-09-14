#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3.4 分档灰度验证（离线评估，Scheme A）

目的：验证 prefilter_v0 的路由建议是否“跟随已验证的 benchmark 边界”，
并估计若按建议选 turbo/plus/rule_or_reject，稳定性会不会变差。

不接入生产 dispatcher：只做静态评估。
不改 schema / validator / builder / provider：仅读取现有 M3 benchmark JSON。

错分审计（先判值不值得小修规则）：加 ``--audit-mismatches`` 只打印 expected≠suggested 的 case 及 prefilter 风险标签。
"""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent

import sys

sys.path.insert(0, str(ROOT))

from capabilities.voice.bridge.voice_long_input_prefilter_v0 import (  # noqa: E402
    prefilter_long_voice_text_v0,
)


DEFAULT_CASES_JSON = ROOT / "configs" / "voice" / "voice_long_voice_length_complexity_cases_m3.json"
DEFAULT_LOG_GLOB = "benchmark_long_voice_length_complexity_matrix_m3_*.json"


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


_TS_RE = re.compile(r"_(\d{8}T\d{6}Z)\.json$")


def _pick_latest_log(log_dir: Path) -> Path:
    paths = sorted(log_dir.glob(DEFAULT_LOG_GLOB), key=lambda p: p.stat().st_mtime)
    if not paths:
        raise FileNotFoundError(f"no logs matched: {log_dir}/{DEFAULT_LOG_GLOB}")
    return paths[-1]


def _row_by_case_id(rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    return {str(r.get("case_id")): r for r in rows if r.get("case_id") is not None}


def _is_good_row(r: Dict[str, Any]) -> bool:
    # 对齐 benchmark 口径：validator_ok==True 且 fallback==False。
    return bool(r.get("validator_ok") is True and r.get("fallback") is False)


def _route_expected_from_case(
    case: Dict[str, Any],
    *,
    plus_row: Dict[str, Any],
    turbo_row: Dict[str, Any],
) -> str:
    # 规则版预期（Scheme A 用于“路由命中准确率”的 reference）：
    # - 明确 unsupported 风险：期望 rule_or_reject
    # - 混合风险：期望 plus
    # - 否则优先 turbo（以 benchmark 的“可通过”作为硬条件）
    unsupported = bool((case.get("heuristic") or {}).get("unsupported_risk"))
    mixed_keywords = case.get("mixed_keywords") or []
    mixed = bool(mixed_keywords)

    if unsupported:
        return "route_to_rule_or_reject"
    if mixed:
        return "route_to_plus"

    turbo_good = _is_good_row(turbo_row)
    plus_good = _is_good_row(plus_row)
    if turbo_good:
        return "route_to_turbo"
    if plus_good:
        return "route_to_plus"
    return "route_to_rule_or_reject"


def _simulate_selected_route_metrics(route: str, plus_row: Dict[str, Any], turbo_row: Dict[str, Any]) -> Dict[str, Any]:
    if route == "route_to_turbo":
        sel = turbo_row
    elif route == "route_to_plus":
        sel = plus_row
    else:
        # rule_or_reject：本离线脚本没有 rules_chain 的直接观测，
        # 用“更可能成功”的模型链作为代理（优先 plus，其次 turbo）。
        plus_good = _is_good_row(plus_row)
        turbo_good = _is_good_row(turbo_row)
        if plus_good:
            sel = plus_row
        elif turbo_good:
            sel = turbo_row
        else:
            # 均失败：选 e2e 更短者仅用于速度估计
            sel = plus_row if float(plus_row.get("e2e_ms") or 0) <= float(turbo_row.get("e2e_ms") or 0) else turbo_row

    return {
        "json_ok": bool(sel.get("json_ok")),
        "validator_ok": bool(sel.get("validator_ok") is True),
        "fallback": bool(sel.get("fallback")),
        "e2e_ms": float(sel.get("e2e_ms") or 0.0),
        "provider_ms": float(sel.get("provider_ms") or 0.0),
        "primary_domain": str(sel.get("primary_domain") or ""),
    }


def _p95(xs: List[float]) -> float:
    if not xs:
        return 0.0
    s = sorted(xs)
    return float(s[int((len(s) - 1) * 0.95)])


def _summarize_selected(metrics: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not metrics:
        return {"n": 0}
    n = len(metrics)
    e2e = [float(m.get("e2e_ms") or 0.0) for m in metrics]
    return {
        "n": n,
        "json_rate": sum(1 for m in metrics if m["json_ok"]) / n,
        "val_rate": sum(1 for m in metrics if m["validator_ok"]) / n,
        "fallback_rate": sum(1 for m in metrics if m["fallback"]) / n,
        "avg_e2e_ms": sum(e2e) / n,
        "p95_e2e_ms": _p95(e2e),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases-json", type=Path, default=DEFAULT_CASES_JSON)
    ap.add_argument("--m3-log-json", type=Path, default=None, help="指定 M3 benchmark 输出 JSON（可选；不填则取最新）")
    ap.add_argument(
        "--audit-mismatches",
        action="store_true",
        help="仅打印 expected≠suggested 的 case（错分审计，便于决定是否小修规则）",
    )
    args = ap.parse_args()

    log_path = args.m3_log_json
    if log_path is None:
        log_path = _pick_latest_log(ROOT / "logs")

    cases = _load_json(args.cases_json)["cases"]
    m3 = _load_json(log_path)

    plus_map = _row_by_case_id(m3.get("plus_rows") or [])
    turbo_map = _row_by_case_id(m3.get("turbo_rows") or [])

    missing: List[str] = []
    for c in cases:
        cid = str(c.get("id"))
        if cid not in plus_map or cid not in turbo_map:
            missing.append(cid)
    if missing:
        raise KeyError(f"case_id missing in log: {missing[:10]}... total={len(missing)}")

    rows: List[Dict[str, Any]] = []
    confusion: Dict[str, Dict[str, int]] = {
        "route_to_turbo": {"route_to_turbo": 0, "route_to_plus": 0, "route_to_rule_or_reject": 0},
        "route_to_plus": {"route_to_turbo": 0, "route_to_plus": 0, "route_to_rule_or_reject": 0},
        "route_to_rule_or_reject": {"route_to_turbo": 0, "route_to_plus": 0, "route_to_rule_or_reject": 0},
    }

    for c in cases:
        cid = str(c.get("id"))
        text = str(c.get("text") or "")
        plus_row = plus_map[cid]
        turbo_row = turbo_map[cid]

        expected = _route_expected_from_case(c, plus_row=plus_row, turbo_row=turbo_row)
        pf = prefilter_long_voice_text_v0(text)
        suggested = str(pf.routing_suggestion)

        confusion[expected][suggested] += 1

        selected_metrics = _simulate_selected_route_metrics(suggested, plus_row, turbo_row)
        rows.append(
            {
                "case_id": cid,
                "length_tier": str(c.get("length_tier") or ""),
                "complexity": str(c.get("complexity") or ""),
                "text": text,
                "mixed_keywords": list(c.get("mixed_keywords") or []),
                "heuristic_unsupported": bool((c.get("heuristic") or {}).get("unsupported_risk")),
                "expected": expected,
                "suggested": suggested,
                "simple_or_complex": pf.simple_or_complex,
                "mixed_risk": pf.mixed_risk,
                "unsupported_risk": pf.unsupported_risk,
                "clarification_risk": pf.clarification_risk,
                "multi_step_risk": pf.multi_step_risk,
                "ordered_itinerary_hint": pf.ordered_itinerary_hint,
                "prefilter_notes": pf.notes,
                "selected": selected_metrics,
            }
        )

    # 总结命中率
    total = len(cases)
    hit = sum(confusion[e][e] for e in confusion.keys())

    selected_by_route: Dict[str, List[Dict[str, Any]]] = {"route_to_turbo": [], "route_to_plus": [], "route_to_rule_or_reject": []}
    for r in rows:
        selected_by_route[str(r["suggested"])].append(r["selected"])

    print(f"M3.4 prefilter eval (offline) | cases={total} | prefilter=v0 | m3_log={log_path}")
    print(f"Route hit accuracy: {hit}/{total} = {hit/total:.2%}")

    print("\nConfusion matrix (expected x suggested)")
    for e in ["route_to_turbo", "route_to_plus", "route_to_rule_or_reject"]:
        line = confusion[e]
        print(f"  expected={e}: turbo={line['route_to_turbo']} plus={line['route_to_plus']} reject={line['route_to_rule_or_reject']}")

    print("\nSelected-route stability proxy (simulated via plus/turbo rows)")
    for rt in ["route_to_turbo", "route_to_plus", "route_to_rule_or_reject"]:
        summary = _summarize_selected(selected_by_route[rt])
        print(f"  suggested={rt}: {summary}")

    if args.audit_mismatches:
        bad = [r for r in rows if r["expected"] != r["suggested"]]
        print(f"\n--- mismatch audit (n={len(bad)}) ---")
        for r in bad:
            tid = r["case_id"]
            print(f"\n[{tid}] {r['length_tier']}/{r['complexity']} expected={r['expected']} suggested={r['suggested']}")
            print(f"  text: {r['text'][:200]}{'…' if len(r['text']) > 200 else ''}")
            print(
                f"  case: mixed_kw={r['mixed_keywords']} heuristic_unsupported={r['heuristic_unsupported']}"
            )
            print(
                f"  prefilter: simple={r['simple_or_complex']}; "
                f"mixed={r['mixed_risk']} unsupported={r['unsupported_risk']} "
                f"multi_step={r['multi_step_risk']} clar={r['clarification_risk']} "
                f"ordered_itinerary={r['ordered_itinerary_hint']}"
            )
            print(f"  notes: {r['prefilter_notes']}")


if __name__ == "__main__":
    main()

