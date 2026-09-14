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


def _read_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _case(name: str, ok: bool, details: Any) -> Dict[str, Any]:
    return {"case": name, "ok": bool(ok), "details": details}


def _write_verification_result(out_root: str, report: Dict[str, Any]) -> None:
    p = os.path.join(out_root, "verification_result.json")
    os.makedirs(out_root, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output-root", required=True)
    args = ap.parse_args()

    out_root = os.path.abspath(args.output_root)

    required_files = [
        "yolo_ocr_bridge_summary.json",
        "yolo_root_parse_report.json",
        "per_sample_yolo_ocr_bridge_results.json",
        "ocr_crop_proposals.json",
        "yolo_ocr_bridge_trace.jsonl",
        "yolo_ocr_bridge_replay.jsonl",
        "yolo_ocr_bridge_whitebox.jsonl",
        "evaluation_notes.md",
    ]

    results: List[Dict[str, Any]] = []
    existing = {f: os.path.isfile(os.path.join(out_root, f)) for f in required_files}
    missing = [k for k, v in existing.items() if not v]
    results.append(_case("A_required_files_present", not missing, {"missing": missing, **existing}))

    if missing:
        report = {
            "verifier": "verify_yolo_ocr_bridge_evidence_run_v0",
            "verdict": "NO_GO",
            "governance_leakage": 0,
            "hard_blockers": missing,
            "results": results,
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        _write_verification_result(out_root, report)
        return 2

    parse_report = _read_json(os.path.join(out_root, "yolo_root_parse_report.json"))
    summary = _read_json(os.path.join(out_root, "yolo_ocr_bridge_summary.json"))

    results.append(
        _case(
            "B_parse_report_status_ok",
            str(parse_report.get("yolo_root_parse_status") or "") in ("ok", "ok_no_data"),
            {"yolo_root_parse_status": parse_report.get("yolo_root_parse_status")},
        )
    )

    parsed_det_cnt = int(parse_report.get("parsed_detection_count") or 0)
    results.append(_case("C_parsed_detection_count_gt0", parsed_det_cnt > 0, {"parsed_detection_count": parsed_det_cnt}))

    results.append(
        _case(
            "D_parsed_frame_refs_present",
            bool(parse_report.get("parsed_frame_refs")),
            {"parsed_frame_refs": parse_report.get("parsed_frame_refs")},
        )
    )

    # No sample-matrix masquerading: yolo_root must be non-empty and parse status must not be sample_matrix_mode.
    input_mode_ok = str(parse_report.get("yolo_root") or "") not in ("None", "", None) and str(parse_report.get("yolo_root_parse_status")) != "sample_matrix_mode"
    results.append(
        _case(
            "E_no_sample_matrix_masquerade",
            input_mode_ok,
            {"yolo_root": parse_report.get("yolo_root"), "yolo_root_parse_status": parse_report.get("yolo_root_parse_status")},
        )
    )

    gov_leak = (summary.get("governance") or {}).get("governance_leakage", 0)
    results.append(_case("F_governance_leakage_zero", gov_leak == 0, {"governance_leakage": gov_leak}))

    # Reuse A-Q verifier.
    base_verifier_cmd = [
        sys.executable,
        os.path.join(REPO_ROOT, "tools", "verify_yolo_ocr_offline_bridge_v0.py"),
        "--output-root",
        out_root,
    ]
    proc = subprocess.run(base_verifier_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    base_ok = proc.returncode == 0
    results.append(
        _case(
            "G_base_bridge_verifier_AQ_go",
            base_ok,
            {"returncode": proc.returncode, "stderr_head": (proc.stderr or "")[:200]},
        )
    )

    # Trace/replay/whitebox non-empty already checked in base verifier; still add smoke check.
    for f in ("yolo_ocr_bridge_trace.jsonl", "yolo_ocr_bridge_replay.jsonl", "yolo_ocr_bridge_whitebox.jsonl"):
        p = os.path.join(out_root, f)
        results.append(_case(f"I_{f}_nonempty", os.path.isfile(p) and os.path.getsize(p) > 0, {"size": os.path.getsize(p) if os.path.isfile(p) else None}))

    all_ok = all(r["ok"] for r in results)
    verdict = "GO" if all_ok else "NO_GO"

    report = {
        "verifier": "verify_yolo_ocr_bridge_evidence_run_v0",
        "verdict": verdict,
        "governance_leakage": 0,
        "hard_blockers": [] if all_ok else [r["case"] for r in results if not r["ok"]],
        "parsed_detection_count": parsed_det_cnt,
        "source_policy_id": summary.get("ocr_source_policy_id"),
        "yolo_root_parse_report": {
            "yolo_root": parse_report.get("yolo_root"),
            "yolo_root_type": parse_report.get("yolo_root_type"),
            "yolo_root_parse_status": parse_report.get("yolo_root_parse_status"),
        },
        "results": results,
    }

    print(json.dumps(report, ensure_ascii=False, indent=2))
    _write_verification_result(out_root, report)
    return 0 if all_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
