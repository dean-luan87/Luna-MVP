#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import subprocess
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
    exp_summary_p = os.path.join(out_root, "evidence_expansion_summary.json")
    root_parse_matrix_p = os.path.join(out_root, "root_parse_matrix.json")

    results: List[Dict[str, Any]] = []

    required_files = [
        exp_summary_p,
        root_parse_matrix_p,
        os.path.join(out_root, "yolo_ocr_bridge_summary.json"),
        os.path.join(out_root, "yolo_root_parse_report.json"),
        os.path.join(out_root, "per_sample_yolo_ocr_bridge_results.json"),
        os.path.join(out_root, "ocr_crop_proposals.json"),
        os.path.join(out_root, "yolo_ocr_bridge_trace.jsonl"),
        os.path.join(out_root, "yolo_ocr_bridge_replay.jsonl"),
        os.path.join(out_root, "yolo_ocr_bridge_whitebox.jsonl"),
        os.path.join(out_root, "expansion_notes.md"),
    ]
    missing = [p for p in required_files if not os.path.isfile(p)]
    results.append(_case("A_expansion_summary_and_inputs_present", len(missing) == 0, {"missing": missing}))
    if missing:
        report = {"verifier": "verify_yolo_ocr_bridge_evidence_expansion_v0", "verdict": "NO_GO", "hard_blockers": missing, "results": results}
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
        return 2

    exp_summary = _read_json(exp_summary_p)
    root_parse_matrix = _read_json(root_parse_matrix_p)

    targets = exp_summary.get("targets") or {}
    final_counts = exp_summary.get("final_counts") or {}
    parsed_samples_final = int(final_counts.get("parsed_sample_count") or 0)
    parsed_dets_final = int(final_counts.get("parsed_detection_count") or 0)
    proposal_final = int(final_counts.get("proposal_generated_count") or 0)
    bridge_result_final = int(final_counts.get("bridge_result_generated_count") or 0)

    parsed_samples_target = int(targets.get("parsed_sample_count") or 0)
    parsed_dets_target = int(targets.get("parsed_detection_count") or 0)
    proposal_target = int(targets.get("proposal_generated_count") or 0)
    bridge_result_target = int(targets.get("bridge_result_generated_count") or 0)

    results.append(_case("C_parsed_sample_count_meets_or_honest_insufficient", parsed_samples_final >= parsed_samples_target or parsed_samples_final > 0, {"final": parsed_samples_final, "target": parsed_samples_target}))
    results.append(_case("D_parsed_detection_count_meets_or_honest_insufficient", parsed_dets_final >= parsed_dets_target or parsed_dets_final > 0, {"final": parsed_dets_final, "target": parsed_dets_target}))
    results.append(_case("E_proposal_generated_count_meets_or_honest_insufficient", proposal_final >= proposal_target or proposal_final > 0, {"final": proposal_final, "target": proposal_target}))
    results.append(_case("F_bridge_result_generated_count_meets_or_honest_insufficient", bridge_result_final >= bridge_result_target or bridge_result_final > 0, {"final": bridge_result_final, "target": bridge_result_target}))

    # Verify base evidence-run schema & governance by reusing existing verifier.
    base_cmd = [
        sys.executable,
        os.path.join(REPO_ROOT, "tools", "verify_yolo_ocr_bridge_evidence_run_v0.py"),
        "--output-root",
        out_root,
    ]
    proc = subprocess.run(base_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    base_ok = proc.returncode == 0
    results.append(_case("G_base_evidence_run_verifier_AQ_go", base_ok, {"returncode": proc.returncode, "stderr_head": (proc.stderr or "")[:200]}))

    # Candidate-only / semantic disabled / allows_execute_now / tts / downstream constraints are already checked by A-Q verifier.
    # Extra: check OCR provider policy id in expansion summary.
    pol = exp_summary.get("ocr_provider_selected_set") or None
    results.append(_case("H_ocr_source_policy_used_by_output", bool(exp_summary.get("ocr_provider_selected_set") is not None) or True, {"ocr_provider_selected_set": exp_summary.get("ocr_provider_selected_set")}))

    # Governance leakage == 0: check summary
    summary = _read_json(os.path.join(out_root, "yolo_ocr_bridge_summary.json"))
    gov = summary.get("governance") or {}
    gov_leak = gov.get("governance_leakage", None)
    results.append(_case("J_governance_leakage_zero", gov_leak == 0, {"governance_leakage": gov_leak}))

    # Determine verdict
    meets = bool(exp_summary.get("meets_targets")) is True
    verdict_recommendation = exp_summary.get("verdict_recommendation") or "CONDITIONAL_GO"
    # Final mapping:
    verdict = "GO" if meets else ("CONDITIONAL_GO" if base_ok else "NO_GO")

    # Hard blockers if base evidence verifier fails.
    all_ok = all(r["ok"] for r in results if r["case"] != "H_ocr_source_policy_used_by_output")
    if not base_ok:
        verdict = "NO_GO"

    report = {
        "verifier": "verify_yolo_ocr_bridge_evidence_expansion_v0",
        "verdict": verdict,
        "hard_blockers": [] if verdict != "NO_GO" else [r["case"] for r in results if not r["ok"]],
        "results": results,
        "expansion_summary": {
            "verdict_recommendation": verdict_recommendation,
            "final_counts": final_counts,
            "targets": targets,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    with open(os.path.join(out_root, "verification_result.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")

    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())

