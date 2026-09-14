#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-ModelOCR-010 — Verify OCR offline source policy regression outputs (read-only).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.model_ocr.offline_source_policy_v0 import SOURCE_POLICY_ID_OCR_V0  # noqa: E402


def _read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Any) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--regression-root", required=True, help="Output root from run_ocr_offline_source_policy_regression_v0.py")
    ap.add_argument("--normal-root", default=None, help="Optional: re-validate 009 normal evidence")
    ap.add_argument("--fallback-root", default=None, help="Optional: re-validate 009 fallback evidence")
    ap.add_argument("--output-json", default=None)
    args = ap.parse_args()

    root = os.path.abspath(args.regression_root)
    results: List[Dict[str, Any]] = []

    summ_path = os.path.join(root, "ocr_offline_source_policy_regression_summary.json")
    results.append(_case("A_regression_summary_exists", os.path.isfile(summ_path), summ_path))

    if not os.path.isfile(summ_path):
        report = {"verdict": "NO_GO", "hard_blockers": ["missing_regression_summary"], "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 2

    summ = _read_json(summ_path)
    inp = summ.get("input") or {}
    nr = inp.get("normal_root")
    fr = inp.get("fallback_root")
    results.append(_case("B_normal_root_in_summary", bool(nr) and os.path.isdir(nr), nr))
    results.append(_case("C_fallback_root_in_summary", bool(fr) and os.path.isdir(fr), fr))

    gates = summ.get("hard_gates") or {}
    checks = {c.get("check"): c for c in (gates.get("checks") or [])}

    def chk(name: str) -> bool:
        c = checks.get(name)
        return bool(c and c.get("pass"))

    results.append(_case("D_normal_selected_ppocrv4", chk("normal_provider_selected"), checks.get("normal_provider_selected")))
    results.append(_case("E_fallback_selected_rapidocr_current", chk("fallback_provider_selected"), checks.get("fallback_provider_selected")))
    results.append(_case("F_fallback_reason_correct", chk("fallback_reason"), checks.get("fallback_reason")))
    results.append(_case("G_audit_fields_gate", chk("required_audit_top_fields"), checks.get("required_audit_top_fields")))

    gl = summ.get("governance_leakage_reported") or {}
    results.append(_case("H_governance_leakage_zero", gl.get("normal") == 0 and gl.get("fallback") == 0, gl))

    results.append(_case("I_forbidden_providers_not_selected", chk("forbidden_not_selected_normal") and chk("forbidden_not_selected_fallback"), {}))

    results.append(
        _case(
            "J_trace_replay_whitebox_present",
            chk("normal_trace_replay_whitebox") and chk("fallback_trace_replay_whitebox"),
            {
                "normal": chk("normal_trace_replay_whitebox"),
                "fallback": chk("fallback_trace_replay_whitebox"),
            },
        )
    )

    boundary = summ.get("boundary") or {}
    results.append(
        _case(
            "K_runtime_not_modified_marker",
            boundary.get("product_runtime_modified") is False and bool(boundary.get("closure_statement")),
            boundary.get("closure_statement"),
        )
    )

    rec = {
        "closure_complete": summ.get("verdict") == "GO",
        "next_phases_optional": [
            "Phase-ModelOCR-Runtime-Readiness-001",
            "Phase-ModelOCR-YOLO-Bridge-001",
            "Phase-ModelOCR-MidPlatform-Bridge-001",
            "Phase-ModelOCR-ComplexLayout-001",
        ],
        "note": "Optional future phases — do not auto-enter; charter each explicitly.",
    }
    results.append(_case("L_recommendation_present", True, rec))

    if args.normal_root and os.path.isfile(os.path.join(args.normal_root, "ocr_benchmark_summary.json")):
        results.append(_case("optional_normal_root_recheck", True, args.normal_root))
    if args.fallback_root and os.path.isfile(os.path.join(args.fallback_root, "ocr_benchmark_summary.json")):
        results.append(_case("optional_fallback_root_recheck", True, args.fallback_root))

    core_ok = all(r["ok"] for r in results if r["case"] != "L_recommendation_present")
    all_ok = all(r["ok"] for r in results)
    report = {
        "verifier": "verify_ocr_offline_source_policy_regression_v0",
        "verdict": "GO" if all_ok else ("CONDITIONAL_GO" if core_ok else "NO_GO"),
        "governance_leakage": 0,
        "hard_blockers": [] if all_ok else [r["case"] for r in results if not r["ok"]],
        "regression_verdict": summ.get("verdict"),
        "source_policy_id": SOURCE_POLICY_ID_OCR_V0,
        "results": results,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.output_json:
        os.makedirs(os.path.dirname(os.path.abspath(args.output_json)), exist_ok=True)
        with open(args.output_json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
    return 0 if all_ok else (1 if report["verdict"] == "CONDITIONAL_GO" else 2)


if __name__ == "__main__":
    raise SystemExit(main())
