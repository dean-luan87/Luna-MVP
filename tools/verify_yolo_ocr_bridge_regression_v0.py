#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Any) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = os.path.abspath(args.output_root)

    required_files = [
        "yolo_ocr_bridge_regression_summary.json",
        "yolo_ocr_bridge_regression_matrix.json",
        "yolo_ocr_bridge_schema_matrix.json",
        "yolo_ocr_bridge_boundary_summary.json",
        "yolo_ocr_bridge_attribution_summary.json",
        "regression_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    missing = [f for f in required_files if not os.path.isfile(os.path.join(out_root, f))]
    results.append(_case("A_regression_outputs_present", not missing, {"missing": missing}))

    if missing:
        report = {"verifier": "verify_yolo_ocr_bridge_regression_v0", "verdict": "NO_GO", "hard_blockers": missing, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return 2

    summary = _read_json(os.path.join(out_root, "yolo_ocr_bridge_regression_summary.json"))
    matrix = _read_json(os.path.join(out_root, "yolo_ocr_bridge_regression_matrix.json"))
    boundary = _read_json(os.path.join(out_root, "yolo_ocr_bridge_boundary_summary.json"))
    attribution = _read_json(os.path.join(out_root, "yolo_ocr_bridge_attribution_summary.json"))

    results.append(_case("B_regression_summary_verdict_allowed", summary.get("verdict") in ("GO", "CONDITIONAL_GO", "NO_GO"), {"verdict": summary.get("verdict")}))

    hard_blockers = summary.get("hard_blockers") or []
    results.append(_case("C_no_hard_blockers", len(hard_blockers) == 0 or summary.get("verdict") == "CONDITIONAL_GO", {"hard_blockers": hard_blockers, "verdict": summary.get("verdict")}))

    # skeleton/evidence verifier passed gates
    results.append(_case("D_skeleton_verifier_GO", bool(summary.get("skeleton_verifier_passed")), {"skeleton_verifier_passed": summary.get("skeleton_verifier_passed")}))
    results.append(_case("E_evidence_verifier_GO", bool(summary.get("evidence_verifier_passed")), {"evidence_verifier_passed": summary.get("evidence_verifier_passed")}))

    # Evidence proposal/result present gates
    pcnt = int(summary.get("proposal_generated_count_evidence") or 0)
    rcnt = int(summary.get("bridge_result_generated_count_evidence") or 0)
    results.append(_case("F_proposal_generated_gt0", pcnt > 0, {"proposal_generated_count_evidence": pcnt}))
    results.append(_case("G_bridge_result_generated_gt0", rcnt > 0, {"bridge_result_generated_count_evidence": rcnt}))

    # Governance leakage
    gov = summary.get("governance") or {}
    gov_ok = (gov.get("governance_leakage_skeleton") == 0 and gov.get("governance_leakage_evidence") == 0)
    results.append(_case("H_governance_leakage_zero", gov_ok, gov))

    # Candidate-only and semantic gates (indirectly from boundary scan)
    sk_ok = (boundary.get("candidate_only_and_raw_text_only") or {}).get("skeleton_ok")
    ev_ok = (boundary.get("candidate_only_and_raw_text_only") or {}).get("evidence_ok")
    results.append(_case("I_candidate_only_boundary_skeleton", sk_ok is True, {"skeleton_ok": sk_ok}))
    results.append(_case("J_candidate_only_boundary_evidence", ev_ok is True, {"evidence_ok": ev_ok}))

    # trace/replay/whitebox
    trace_detail = boundary.get("trace_replay_whitebox_nonempty") or {}
    trace_ok = all(bool(v) for v in trace_detail.values()) if trace_detail else False
    results.append(_case("K_trace_replay_whitebox_complete", trace_ok, trace_detail))

    # policy id
    pol_id = summary.get("ocr_source_policy_id")
    results.append(_case("L_ocr_source_policy_present", bool(pol_id), {"ocr_source_policy_id": pol_id}))

    # sample scale limitation recorded
    scale = summary.get("closure_recommendation", {}).get("evidence_scale_register") or {}
    scale_rec = bool(scale.get("parsed_sample_count")) or bool(scale.get("parsed_detection_count"))
    results.append(_case("M_sample_scale_limitation_recorded", scale_rec, scale))

    # closure recommendation exists
    closure_rec = summary.get("closure_recommendation") or {}
    results.append(_case("N_closure_recommendation_present", bool(closure_rec), closure_rec))

    verdict = "GO"
    if not all(r["ok"] for r in results if r["case"] not in ("C_no_hard_blockers",)):
        verdict = "NO_GO"
    else:
        if summary.get("verdict") == "CONDITIONAL_GO":
            verdict = "CONDITIONAL_GO"

    report = {
        "verifier": "verify_yolo_ocr_bridge_regression_v0",
        "verdict": verdict,
        "hard_blockers": [] if verdict != "NO_GO" else [r["case"] for r in results if not r["ok"]],
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())

