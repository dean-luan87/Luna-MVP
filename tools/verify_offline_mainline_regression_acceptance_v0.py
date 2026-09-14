#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EngineeringFlow-006
Verify regression acceptance outputs and thresholds.
"""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List


def _exists(p: str) -> bool:
    try:
        return os.path.exists(p)
    except Exception:
        return False


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _req(cond: bool, code: str, details: Dict[str, Any]) -> Dict[str, Any]:
    return {"check": code, "pass": bool(cond), **details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="logs/offline_mainline_regression_ef006_<timestamp>")
    args = ap.parse_args()

    out_root = os.path.abspath(args.output_root)
    p_summary = os.path.join(out_root, "regression_acceptance_summary.json")
    p_matrix = os.path.join(out_root, "regression_acceptance_matrix.json")
    p_gates = os.path.join(out_root, "regression_gate_results.json")
    p_notes = os.path.join(out_root, "regression_notes.md")

    results: List[Dict[str, Any]] = []
    results.append(_req(_exists(p_summary), "summary_exists", {"path": p_summary}))
    results.append(_req(_exists(p_matrix), "matrix_exists", {"path": p_matrix}))
    results.append(_req(_exists(p_gates), "gates_exists", {"path": p_gates}))
    results.append(_req(_exists(p_notes), "notes_exists", {"path": p_notes}))

    summary = _read_json(p_summary) if _exists(p_summary) else {}
    gates = _read_json(p_gates) if _exists(p_gates) else {}

    # Must include fields
    for k in ["phase", "run_id", "inputs", "outputs", "hard_thresholds_total", "hard_thresholds_passed", "hard_thresholds_failed", "hard_blockers", "recommendation"]:
        results.append(_req(k in summary, f"summary_has_{k}", {"missing": k if k not in summary else ""}))

    all_gates = gates.get("gates") if isinstance(gates, dict) else None
    if not isinstance(all_gates, list):
        all_gates = []
    all_pass = bool(gates.get("all_pass") is True)
    results.append(_req(all_pass, "all_hard_gates_pass", {"all_pass": gates.get("all_pass"), "failed": gates.get("hard_failures")}))

    rec = str(summary.get("recommendation") or "")
    results.append(_req(rec in ["go", "conditional_go", "no_go"], "recommendation_enum_valid", {"recommendation": rec}))
    if all_pass:
        results.append(_req(rec != "no_go", "recommendation_not_no_go_when_all_pass", {"recommendation": rec}))

    ok = all(bool(r.get("pass")) for r in results)
    verification = {
        "phase": "Phase-EngineeringFlow-006",
        "tool": "verify_offline_mainline_regression_acceptance_v0.py",
        "output_root": out_root,
        "checks_total": len(results),
        "checks_passed": int(sum(1 for r in results if r.get("pass"))),
        "all_pass": ok,
        "results": results,
    }

    out_p = os.path.join(out_root, "verification_result.json")
    with open(out_p, "w", encoding="utf-8") as f:
        json.dump(verification, f, ensure_ascii=False, indent=2)

    print(json.dumps({"verification_result": out_p, "all_pass": ok}, ensure_ascii=False, indent=2))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())

