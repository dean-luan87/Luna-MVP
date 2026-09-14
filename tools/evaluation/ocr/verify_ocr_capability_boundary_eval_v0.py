#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-006 — Verifier for OCR capability boundary eval v0.

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
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--output-root", required=True)
    ap.add_argument("--min-cases", type=int, default=120)
    args = ap.parse_args()

    dr = Path(args.dataset_root).expanduser()
    outp = Path(args.output_root).expanduser()
    if not dr.is_absolute() or not outp.is_absolute():
        raise SystemExit("ERROR: --dataset-root and --output-root must be absolute")
    dataset_root = dr.resolve()
    out_root = outp.resolve()

    blockers: List[str] = []
    if not dataset_root.is_dir():
        blockers.append("dataset_root_missing")
    if not (dataset_root / "boundary_case_manifest.jsonl").is_file():
        blockers.append("dataset_manifest_missing")
    if not out_root.is_dir():
        blockers.append("output_root_missing")

    required = [
        "ocr_capability_boundary_eval_summary.json",
        "ocr_capability_boundary_sample_matrix.json",
        "ocr_content_type_performance_report.json",
        "ocr_quality_perturbation_report.json",
        "ocr_expected_routing_report.json",
        "ocr_failure_mode_report.json",
        "ocr_provider_boundary_map.json",
        "ocr_capability_boundary_map.json",
        "ocr_false_text_risk_report.json",
        "ocr_eligibility_accuracy_report.json",
        "ocr_recommended_routing_policy_draft.json",
        "ocr_boundary_quality_vs_accuracy_report.json",
        "ocr_capability_boundary_trace.jsonl",
        "ocr_capability_boundary_replay.jsonl",
        "boundary_eval_notes.md",
    ]
    for fn in required:
        p = out_root / fn
        if fn.endswith((".jsonl", ".md")):
            if not _nonempty(p):
                blockers.append(f"missing_or_empty:{fn}")
        else:
            if not p.is_file():
                blockers.append(f"missing:{fn}")

    if not blockers and (out_root / "ocr_capability_boundary_eval_summary.json").is_file():
        summ: Dict[str, Any] = _read_json(out_root / "ocr_capability_boundary_eval_summary.json")
        ha = (summ.get("hard_audit") or {}) if isinstance(summ, dict) else {}
        for k in ("runtime_integration", "whitebox_integration", "mainline_side_effect"):
            if ha.get(k) is not False:
                blockers.append(f"boundary_violation:{k}")

        mat: Any = _read_json(out_root / "ocr_capability_boundary_sample_matrix.json")
        if not isinstance(mat, list):
            blockers.append("sample_matrix_not_list")
        else:
            if len(mat) < int(args.min_cases):
                blockers.append(f"too_few_cases:{len(mat)}<{args.min_cases}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {"phase": "Phase-EvaluationTools-OCR-006", "verdict": verdict, "blockers": blockers, "dataset_root": str(dataset_root), "output_root": str(out_root)}
    (out_root / "boundary_eval_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

