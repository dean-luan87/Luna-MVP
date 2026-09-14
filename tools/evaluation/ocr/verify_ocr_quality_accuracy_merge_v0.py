#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-005 — Verifier for OCR quality × accuracy merge report v0.

Evaluation Tools only. Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _nonempty(path: Path) -> bool:
    try:
        return path.is_file() and bool(path.read_text(encoding="utf-8").strip())
    except Exception:
        return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--accuracy-root", required=True)
    ap.add_argument("--quality-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--expected-count", type=int, default=0)
    args = ap.parse_args()

    acc = Path(args.accuracy_root).expanduser()
    qual = Path(args.quality_root).expanduser()
    outp = Path(args.output_root).expanduser()
    if not acc.is_absolute() or not qual.is_absolute() or not outp.is_absolute():
        raise SystemExit("ERROR: --accuracy-root/--quality-root/--output-root must be absolute")
    acc_root = acc.resolve()
    qual_root = qual.resolve()
    out_root = outp.resolve()

    blockers: List[str] = []
    if not acc_root.is_dir():
        blockers.append("accuracy_root_missing")
    if not qual_root.is_dir():
        blockers.append("quality_root_missing")
    if not out_root.is_dir():
        blockers.append("output_root_missing")

    # Inputs existence
    if not (acc_root / "rapidocr_chinese_sample_eval_matrix.json").is_file():
        blockers.append("missing_accuracy_matrix")
    if not (qual_root / "ocr_input_quality_image_matrix.jsonl").is_file():
        blockers.append("missing_quality_matrix")

    # Outputs existence
    required = [
        "ocr_quality_accuracy_merge_summary.json",
        "ocr_quality_accuracy_sample_matrix.json",
        "ocr_quality_bucket_report.json",
        "ocr_quality_metric_correlation_report.json",
        "ocr_provider_vs_input_failure_report.json",
        "ocr_quality_accuracy_trace.jsonl",
        "ocr_quality_accuracy_replay.jsonl",
        "merge_notes.md",
    ]
    for fn in required:
        p = out_root / fn
        if fn.endswith((".jsonl", ".md")):
            if not _nonempty(p):
                blockers.append(f"missing_or_empty:{fn}")
        else:
            if not p.is_file():
                blockers.append(f"missing:{fn}")

    if not blockers and (out_root / "ocr_quality_accuracy_merge_summary.json").is_file():
        summ: Dict[str, Any] = _read_json(out_root / "ocr_quality_accuracy_merge_summary.json")
        ha = (summ.get("hard_audit") or {}) if isinstance(summ, dict) else {}
        for k in ("ocr_provider_invoked", "runtime_integration", "whitebox_integration", "mainline_side_effect"):
            if ha.get(k) is not False:
                blockers.append(f"boundary_violation:{k}")

        if int(args.expected_count) > 0:
            if int(summ.get("aligned_count") or -1) != int(args.expected_count):
                blockers.append(f"aligned_count_mismatch expected={args.expected_count} actual={summ.get('aligned_count')}")

        # Field presence in sample matrix
        mat: Any = _read_json(out_root / "ocr_quality_accuracy_sample_matrix.json")
        if not isinstance(mat, list) or (int(args.expected_count) > 0 and len(mat) != int(args.expected_count)):
            blockers.append("sample_matrix_invalid_or_count_mismatch")
        else:
            if mat:
                r0 = mat[0]
                for k in ("cer", "image_quality_gate", "quality_bucket"):
                    if k not in r0:
                        blockers.append(f"missing_field_in_matrix:{k}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "phase": "Phase-EvaluationTools-OCR-005",
        "verifier": "verify_ocr_quality_accuracy_merge_v0",
        "verdict": verdict,
        "blockers": blockers,
        "accuracy_root": str(acc_root),
        "quality_root": str(qual_root),
        "output_root": str(out_root),
    }
    (out_root / "ocr_quality_accuracy_merge_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

