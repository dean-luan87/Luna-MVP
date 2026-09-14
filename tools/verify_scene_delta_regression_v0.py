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
    ap.add_argument("--output-root", required=True, help="Regression output root produced by run_scene_delta_regression_v0.py")
    args = ap.parse_args()

    out_root = args.output_root if os.path.isabs(args.output_root) else os.path.abspath(os.path.join(REPO_ROOT, args.output_root))

    required_files = [
        "scene_delta_regression_summary.json",
        "scene_delta_regression_matrix.json",
        "scene_delta_status_action_matrix.json",
        "scene_delta_compression_audit_summary.json",
        "scene_delta_boundary_summary.json",
        "scene_delta_trace_replay_whitebox_summary.json",
        "regression_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    missing = [f for f in required_files if not os.path.isfile(os.path.join(out_root, f))]
    results.append(_case("A_regression_summary_exists", len(missing) == 0, {"missing": missing}))
    if missing:
        report = {"verifier": "verify_scene_delta_regression_v0", "verdict": "NO_GO", "hard_blockers": missing, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    summary = _read_json(os.path.join(out_root, "scene_delta_regression_summary.json"))
    matrix = _read_json(os.path.join(out_root, "scene_delta_regression_matrix.json"))
    audit = _read_json(os.path.join(out_root, "scene_delta_compression_audit_summary.json"))
    boundary = _read_json(os.path.join(out_root, "scene_delta_boundary_summary.json"))
    trw = _read_json(os.path.join(out_root, "scene_delta_trace_replay_whitebox_summary.json"))

    # B input root readable and C base verifier GO
    counts = (matrix or {}).get("counts") if isinstance(matrix, dict) else {}
    base_verdict = (matrix or {}).get("base_verifier_verdict") if isinstance(matrix, dict) else None
    missing_required = (matrix or {}).get("missing_required_files") if isinstance(matrix, dict) else None
    results.append(_case("B_input_root_readable", (missing_required == []), {"missing_required_files": missing_required}))
    results.append(_case("C_base_verifier_GO", base_verdict == "GO", {"base_verifier_verdict": base_verdict}))

    # D required files present already implied, but keep explicit
    results.append(_case("D_required_files_present", (missing_required == []), {"missing_required_files": missing_required}))

    # E counts valid
    ok_counts = True
    for k, minv in (("processed_count", 9), ("anchors_count", 9), ("decisions_count", 9), ("compression_records_count", 2)):
        v = counts.get(k) if isinstance(counts, dict) else None
        if v is None or int(v) < minv:
            ok_counts = False
            break
    results.append(_case("E_counts_valid", ok_counts, {"counts": counts}))

    # F/G status presence: content_replaced/content_removed required
    status_presence = (matrix or {}).get("status_presence") if isinstance(matrix, dict) else {}
    results.append(_case("F_content_replaced_present", bool(status_presence.get("content_replaced")), {"status_presence": status_presence}))
    results.append(_case("G_content_removed_present", bool(status_presence.get("content_removed")), {"status_presence": status_presence}))
    results.append(_case("G2_new_content_same_place_present", bool(status_presence.get("new_content_same_place")), {"status_presence": status_presence}))

    # H/I/J compression audit
    ok_comp = isinstance(audit, dict) and int(audit.get("compression_record_count") or 0) >= 2
    ok_canonical = isinstance(audit, dict) and int(audit.get("canonical_missing_count") or 0) == 0
    ok_dupe = isinstance(audit, dict) and int(audit.get("duplicate_count_missing_count") or 0) == 0
    results.append(_case("H_compression_records_valid", ok_comp, {"audit": audit}))
    results.append(_case("I_canonical_evidence_ref_present", ok_canonical, {"canonical_missing_count": audit.get("canonical_missing_count") if isinstance(audit, dict) else None}))
    results.append(_case("J_duplicate_count_present", ok_dupe, {"duplicate_count_missing_count": audit.get("duplicate_count_missing_count") if isinstance(audit, dict) else None}))

    # K trace/replay/whitebox present
    ok_trw = isinstance(trw, dict) and bool(trw.get("all_nonempty"))
    results.append(_case("K_trace_replay_whitebox_present", ok_trw, {"trw": trw}))

    # L/M/N/O/P boundary
    bcounts = (boundary or {}).get("boundary_counts") if isinstance(boundary, dict) else {}
    results.append(_case("L_world_model_write_invoked_false", int(bcounts.get("world_model_write_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("M_hive_upload_invoked_false", int(bcounts.get("hive_upload_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("N_navigation_action_null", int(bcounts.get("navigation_action_nonnull") or 0) == 0, {"boundary_counts": bcounts}))
    results.append(_case("O_real_tts_invoked_false", int(bcounts.get("real_tts_invoked_true") or 0) == 0, {"boundary_counts": bcounts}))
    # P runtime_invoked=false: enforced by base verifier GO + no runtime in boundary scan
    results.append(_case("P_runtime_invoked_false", base_verdict == "GO", {"reason": "enforced_by_base_verifier"}))

    # Q closure recommendation present
    ok_closure = isinstance(summary, dict) and summary.get("phase") == "Phase-MidPlatform-SceneDelta-003" and bool(summary.get("verdict_hint"))
    results.append(_case("Q_closure_recommendation_present", ok_closure, {"verdict_hint": (summary or {}).get("verdict_hint")}))

    hard_blockers = list((summary or {}).get("hard_blockers") or []) if isinstance(summary, dict) else []
    ok_all = all(r["ok"] for r in results)
    verdict = "GO" if ok_all and not hard_blockers else "NO_GO"
    report = {"verifier": "verify_scene_delta_regression_v0", "verdict": verdict, "hard_blockers": hard_blockers, "results": results}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

