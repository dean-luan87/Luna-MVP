#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.environ.get("LUNA_REPO_ROOT") or os.getcwd())
if REPO_ROOT not in __import__("sys").path:
    __import__("sys").path.insert(0, REPO_ROOT)


def _resolve(p: str) -> str:
    return p if os.path.isabs(p) else os.path.abspath(os.path.join(REPO_ROOT, p))


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Any = None) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Regression output root produced by run_midplatform_ocr_bridge_regression_v0.py")
    args = ap.parse_args()

    out_root = _resolve(args.output_root)

    required_files = [
        "midplatform_ocr_bridge_regression_summary.json",
        "midplatform_ocr_bridge_regression_matrix.json",
        "midplatform_ocr_bridge_input_root_matrix.json",
        "midplatform_ocr_bridge_candidate_matrix.json",
        "midplatform_ocr_bridge_boundary_summary.json",
        "midplatform_ocr_bridge_trace_replay_whitebox_summary.json",
        "regression_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    missing = [f for f in required_files if not os.path.isfile(os.path.join(out_root, f))]
    results.append(_case("A_regression_summary_exists", len(missing) == 0, {"missing": missing}))
    if missing:
        report = {"verifier": "verify_midplatform_ocr_bridge_regression_v0", "verdict": "NO_GO", "hard_blockers": missing, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    summary = _read_json(os.path.join(out_root, "midplatform_ocr_bridge_regression_summary.json"))
    matrix = _read_json(os.path.join(out_root, "midplatform_ocr_bridge_regression_matrix.json"))
    boundary = _read_json(os.path.join(out_root, "midplatform_ocr_bridge_boundary_summary.json"))
    trw = _read_json(os.path.join(out_root, "midplatform_ocr_bridge_trace_replay_whitebox_summary.json"))

    rows = (matrix or {}).get("rows") if isinstance(matrix, dict) else None
    ok_rows = isinstance(rows, list) and len(rows) > 0
    results.append(_case("B_all_input_roots_listed", ok_rows, {"row_count": len(rows) if isinstance(rows, list) else None}))

    # C required output files per root (captured by missing_required_files_count)
    ok_required = True
    if ok_rows:
        for r in rows:
            if not isinstance(r, dict):
                ok_required = False
                break
            if int(r.get("missing_required_files_count") or 0) != 0:
                ok_required = False
                break
            if r.get("readable") is not True:
                ok_required = False
                break
    else:
        ok_required = False
    results.append(_case("C_all_input_roots_have_required_output_files", ok_required, {}))

    # D/E/F: evidence/delta/filter exist (counts not None)
    def _all_nonnull(key: str) -> bool:
        if not ok_rows:
            return False
        for r in rows:
            if r.get(key) is None:
                return False
        return True

    results.append(_case("D_evidence_inputs_generated", _all_nonnull("evidence_inputs"), {}))
    results.append(_case("E_delta_control_generated", _all_nonnull("delta_results"), {}))
    results.append(_case("F_filter_results_generated", _all_nonnull("filter_results"), {}))

    # G candidate files generated: counts non-null (may be 0)
    ok_candidates = _all_nonnull("text_candidates") and _all_nonnull("world_candidates") and _all_nonnull("ambient_candidates")
    results.append(_case("G_candidate_files_generated", ok_candidates, {}))

    # H trace/replay/whitebox present: must be >0 in each root
    ok_trw = True
    if ok_rows:
        for r in rows:
            if int(r.get("trace_lines") or 0) <= 0 or int(r.get("replay_lines") or 0) <= 0 or int(r.get("whitebox_lines") or 0) <= 0:
                ok_trw = False
                break
    else:
        ok_trw = False
    results.append(_case("H_trace_replay_whitebox_present", ok_trw, {"trw_rows": (trw or {}).get("rows") if isinstance(trw, dict) else None}))

    # I/J boundary: semantic_summary/navigation_action totals must be 0
    forbidden_totals = (boundary or {}).get("forbidden_nonnull_totals") if isinstance(boundary, dict) else {}
    ok_semantic = int((forbidden_totals or {}).get("semantic_summary") or 0) == 0
    ok_nav = int((forbidden_totals or {}).get("navigation_action") or 0) == 0
    results.append(_case("I_semantic_summary_always_null", ok_semantic, {"semantic_summary_nonnull": (forbidden_totals or {}).get("semantic_summary")}))
    results.append(_case("J_navigation_action_always_null", ok_nav, {"navigation_action_nonnull": (forbidden_totals or {}).get("navigation_action")}))

    # K/L/M: execution/TTS/downstream are checked in per-root verifier; regression requires all roots have verification_verdict=GO
    ok_verdicts = True
    if ok_rows:
        for r in rows:
            if r.get("verification_verdict") != "GO":
                ok_verdicts = False
                break
    else:
        ok_verdicts = False
    results.append(_case("K_all_input_roots_verifier_GO", ok_verdicts, {"roots": [r.get("root") for r in rows] if ok_rows else None}))

    # N no real world model write (definition-only): represented by boundary and per-root verifier GO
    results.append(_case("N_no_real_world_model_write", ok_verdicts and ok_semantic and ok_nav, {"reason": "enforced_by_per_root_verifier_and_boundary_scan"}))

    # O/P: relevance and blocking fields present for blocked rows (presence captured by per-root verifier + counts)
    ok_blocked_retained = True
    if ok_rows:
        for r in rows:
            if int(r.get("blocked_missing_retained_evidence_ref") or 0) != 0:
                ok_blocked_retained = False
                break
    else:
        ok_blocked_retained = False
    results.append(_case("P_blocked_evidence_retained", ok_blocked_retained, {}))

    # Q low-value uncertainty fields: not required in all rows, but regression must not crash and should report counts (matrix contains dict)
    ok_low_value_reporting = True
    if ok_rows:
        for r in rows:
            lv = r.get("low_value_fields_nonnull_in_filter_results")
            if lv is None:
                ok_low_value_reporting = False
                break
            if not isinstance(lv, dict):
                ok_low_value_reporting = False
                break
    else:
        ok_low_value_reporting = False
    results.append(_case("Q_low_value_uncertainty_fields_reported", ok_low_value_reporting, {}))

    # R TTL/revalidation: enforced by per-root verifier GO for world/ambient candidates (F/G cases there)
    results.append(_case("R_world_ambient_ttl_revalidation_preserved", ok_verdicts, {"reason": "enforced_by_per_root_verifier"}))

    # S no taskchain execution: enforced by boundary + per-root verifier evidence_inputs downstream_invocation_count=0
    results.append(_case("S_no_taskchain_execution", ok_verdicts, {"reason": "enforced_by_per_root_verifier"}))

    # T closure recommendation present: summary must include phase/tool and verdict_hint
    ok_closure = isinstance(summary, dict) and summary.get("phase") == "Phase-ModelOCR-MidPlatform-Bridge-003" and bool(summary.get("verdict_hint"))
    results.append(_case("T_closure_recommendation_present", ok_closure, {"verdict_hint": (summary or {}).get("verdict_hint")}))

    hard_blockers: List[str] = []
    if isinstance(summary, dict):
        hard_blockers = list(summary.get("hard_blockers") or [])

    ok_all = all(r.get("ok") for r in results)
    verdict = "GO" if ok_all and not hard_blockers else "NO_GO"
    report = {"verifier": "verify_midplatform_ocr_bridge_regression_v0", "verdict": verdict, "hard_blockers": hard_blockers, "results": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

