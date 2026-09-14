#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Labeled-Set-Evaluation-001 — Verifier for run_paddleocr_labeled_set_evaluation_v0 outputs.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--labeled-set-root", required=True, help="Output root of run_paddleocr_labeled_set_evaluation_v0.py")
    args = ap.parse_args()

    root = _require_abs(args.labeled_set_root, "--labeled-set-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "paddleocr_labeled_set_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_labeled_set_summary")
    summary: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}

    mat_root = Path(str(summary.get("materialize_root") or "")).expanduser()
    if not mat_root.is_absolute() or not mat_root.is_dir():
        blockers.append("invalid_materialize_root_in_summary")
    else:
        mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
        if not mat_sum_p.is_file():
            blockers.append("missing_materialize_summary")
        else:
            ms = _read_json(mat_sum_p)
            if ms.get("materialize_verdict") != "GO":
                blockers.append("materialize_verdict_not_go")

    pinned = Path(str(summary.get("pinned_manifest") or ""))
    if not pinned.is_file():
        blockers.append("pinned_manifest_not_readable")

    n = int(summary.get("sample_count") or 0)
    if n == 0:
        blockers.append("sample_count_zero")
    if n > 50:
        blockers.append("sample_count_over_50")

    gt_cov = float(summary.get("ground_truth_coverage") or 0.0)
    if n >= 20 and gt_cov < 0.8:
        soft.append("ground_truth_coverage_below_0_8")

    for name in (
        "paddleocr_labeled_set_sample_matrix.json",
        "paddleocr_labeled_set_raw_results.json",
        "paddleocr_labeled_set_normalized_results.json",
        "paddleocr_labeled_set_evidence_results.json",
        "paddleocr_labeled_set_quality_metrics.json",
        "paddleocr_labeled_set_category_report.json",
        "paddleocr_labeled_set_error_report.json",
        "paddleocr_labeled_set_review_queue.json",
        "paddleocr_labeled_set_runtime_metrics.json",
        "paddleocr_labeled_set_audit_report.json",
    ):
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    qm_p = root / "paddleocr_labeled_set_quality_metrics.json"
    qm: Dict[str, Any] = _read_json(qm_p) if qm_p.is_file() else {}
    if qm.get("production_quality_deemed_pass") is True:
        blockers.append("production_quality_deemed_pass_must_remain_false_in_v0")

    aud_p = root / "paddleocr_labeled_set_audit_report.json"
    if aud_p.is_file():
        aud = _read_json(aud_p)
        for k in (
            "network_request_invoked",
            "model_cache_modified",
            "ocr_routing_changed",
            "rapidocr_replaced",
            "runtime_integration",
            "whitebox_integration",
            "midplatform_invoked",
        ):
            if aud.get(k) is True:
                blockers.append(f"audit_true:{k}")
        if aud.get("world_model_written") is True:
            blockers.append("world_model_written")
        if aud.get("midplatform_semantics_written") is True:
            blockers.append("midplatform_semantics_written")

    lv = str(summary.get("labeled_set_verdict") or "")
    cu = summary.get("category_undercovered") if isinstance(summary.get("category_undercovered"), list) else []

    if lv == "GO" and blockers:
        blockers.append("summary_go_inconsistent_with_verifier_checks")
    if lv == "GO" and summary.get("constructor_ok") is not True:
        blockers.append("summary_go_but_constructor_not_ok")
    if lv == "GO" and (n < 20 or n > 50):
        blockers.append("summary_go_but_sample_count_out_of_band")
    if lv == "GO" and gt_cov < 0.8:
        blockers.append("summary_go_but_ground_truth_coverage_below_0_8")

    if lv == "GO" and cu:
        blockers.append("summary_go_but_category_undercovered_non_empty")

    if blockers:
        verdict = "NO_GO"
    elif soft or lv == "CONDITIONAL_GO" or n < 20 or gt_cov < 0.8 or cu:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "paddleocr_labeled_set_verifier_report_v0",
        "phase": "Phase-PaddleOCR-Labeled-Set-Evaluation-001",
        "labeled_set_root": str(root),
        "verdict": verdict,
        "blockers": sorted(set(blockers)),
        "soft_warnings": sorted(set(soft)),
        "labeled_set_verdict_from_summary": lv,
    }
    (root / "paddleocr_labeled_set_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"labeled_set_root": str(root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
