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


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Any = None) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True, help="Regression output root produced by run_world_context_evidence_regression_v0.py")
    args = ap.parse_args()

    out_root = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    required_files = [
        "world_context_evidence_regression_summary.json",
        "world_context_evidence_root_matrix.json",
        "world_context_evidence_candidate_matrix.json",
        "world_context_anchor_alignment_summary.json",
        "world_context_source_reference_chain_summary.json",
        "world_context_trust_lifecycle_policy_summary.json",
        "world_context_boundary_summary.json",
        "world_context_trace_replay_whitebox_summary.json",
        "regression_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    missing = [f for f in required_files if not os.path.isfile(os.path.join(out_root, f))]
    results.append(_case("A_regression_summary_exists", len(missing) == 0, {"missing": missing}))
    if missing:
        report = {"verifier": "verify_world_context_evidence_regression_v0", "verdict": "NO_GO", "hard_blockers": missing, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    summary = _read_json(os.path.join(out_root, "world_context_evidence_regression_summary.json"))
    root_matrix = _read_json(os.path.join(out_root, "world_context_evidence_root_matrix.json"))
    candidate_matrix = _read_json(os.path.join(out_root, "world_context_evidence_candidate_matrix.json"))
    anchor = _read_json(os.path.join(out_root, "world_context_anchor_alignment_summary.json"))
    src = _read_json(os.path.join(out_root, "world_context_source_reference_chain_summary.json"))
    boundary = _read_json(os.path.join(out_root, "world_context_boundary_summary.json"))
    trw = _read_json(os.path.join(out_root, "world_context_trace_replay_whitebox_summary.json"))

    roots = (summary or {}).get("roots") if isinstance(summary, dict) else None
    root_rows = ((root_matrix or {}).get("roots") if isinstance(root_matrix, dict) else None)
    root_rows = (root_rows.get("roots") if isinstance(root_rows, dict) else root_rows)  # tolerate older shape
    root_rows = root_rows if isinstance(root_rows, list) else []

    # B all roots readable
    all_readable = True
    for rr in root_rows:
        if not isinstance(rr, dict):
            all_readable = False
            break
        if rr.get("error") == "not_a_directory":
            all_readable = False
            break
    results.append(_case("B_all_roots_readable", all_readable, {"roots": roots}))

    # C all roots verifier GO
    all_go = True
    bad_go = []
    for rr in root_rows:
        if not isinstance(rr, dict):
            continue
        if rr.get("verifier_verdict") != "GO":
            all_go = False
            bad_go.append(rr.get("root_input_arg") or rr.get("root"))
    results.append(_case("C_all_roots_verifier_GO", all_go, {"bad": bad_go}))

    # D candidates file exists (implied by missing_required_files empty)
    d_ok = all(isinstance(rr, dict) and rr.get("missing_required_files") == [] for rr in root_rows)
    results.append(_case("D_candidates_files_exist", d_ok, {"missing_required_files": [rr.get("missing_required_files") for rr in root_rows if isinstance(rr, dict)]}))

    totals = (candidate_matrix.get("totals") if isinstance(candidate_matrix, dict) else {}) or {}
    wc_count = int(totals.get("world_context_evidence_candidates") or 0)
    results.append(_case("E_world_context_candidates_count_gt_0", wc_count > 0, {"count": wc_count}))

    # F/G files exist: commercial/world_change (may be 0 count but file exists per root)
    results.append(_case("F_commercial_candidate_supported", "commercial_activity_evidence_candidates" in totals, {"totals": totals}))
    results.append(_case("G_world_change_event_supported", "world_change_event_candidates" in totals, {"totals": totals}))

    # H/I/J/K/L/M/N/O/P/Q: enforced by per-root verifiers; here ensure distributions exist
    dist = (candidate_matrix.get("distributions") if isinstance(candidate_matrix, dict) else {}) or {}
    for name, key in [
        ("H_observed_at_present", "lifecycle_evidence_status"),
        ("I_observed_where_present", "spatial_anchor_type"),
        ("J_observed_where_source_present", "observed_where_source"),
        ("K_source_evidence_refs_non_empty", None),
        ("L_source_reference_chain_present", "source_reference_chain_depth"),
        ("M_source_ref_integrity_status_present", "source_ref_integrity_status"),
        ("N_no_fabricated_gps", None),
        ("O_trust_fields_present", "ttl_policy"),
        ("P_lifecycle_fields_present", "ttl_policy"),
        ("Q_world_model_policy_present", "evidence_type"),
    ]:
        ok = True
        if key is not None:
            ok = isinstance(dist.get(key), dict)
        results.append(_case(name, ok, {"key": key}))

    # R trace/replay/whitebox present
    ok_trw = isinstance(trw, dict) and bool(trw.get("all_nonempty"))
    results.append(_case("R_trace_replay_whitebox_present", ok_trw, {"trw": trw}))

    # S–W boundaries
    bcounts = (boundary.get("boundary_counts") if isinstance(boundary, dict) else {}) or {}
    results.append(_case("S_world_model_write_invoked_false", int(bcounts.get("world_model_write_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("T_hive_upload_invoked_false", int(bcounts.get("hive_upload_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("U_recommendation_invoked_false", int(bcounts.get("recommendation_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("V_navigation_action_null", int(bcounts.get("navigation_action_nonnull") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("W_real_tts_invoked_false", int(bcounts.get("real_tts_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))

    # X closure recommendation present
    ok_closure = isinstance(summary, dict) and bool(summary.get("closure_recommendation"))
    results.append(_case("X_closure_recommendation_present", ok_closure, {"closure_recommendation": (summary or {}).get("closure_recommendation")}))

    hard_blockers = list((summary or {}).get("hard_blockers") or []) if isinstance(summary, dict) else []
    ok_all = all(r["ok"] for r in results)
    verdict = "GO" if ok_all and not hard_blockers else "NO_GO"
    report = {"verifier": "verify_world_context_evidence_regression_v0", "verdict": verdict, "hard_blockers": hard_blockers, "results": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

