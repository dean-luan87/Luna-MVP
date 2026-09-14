#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001 — Verifier for batch recovery outputs.
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
    ap.add_argument("--batch-recovery-root", required=True, help="Output root of run_paddleocr_labeled_set_batch_recovery_v0.py")
    args = ap.parse_args()

    root = _require_abs(args.batch_recovery_root, "--batch-recovery-root")
    blockers: List[str] = []

    required = (
        "paddleocr_labeled_set_batch_recovery_summary.json",
        "paddleocr_labeled_set_batch_plan.json",
        "paddleocr_labeled_set_batch_results_matrix.json",
        "paddleocr_labeled_set_batch_crash_report.json",
        "paddleocr_labeled_set_batch_merged_quality_metrics.json",
        "paddleocr_labeled_set_batch_merged_runtime_metrics.json",
        "paddleocr_labeled_set_batch_resume_state.json",
        "paddleocr_labeled_set_batch_audit_report.json",
        "paddleocr_labeled_set_batch_recovery_notes.md",
    )
    for name in required:
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    sum_p = root / "paddleocr_labeled_set_batch_recovery_summary.json"
    summary: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}
    plan_p = root / "paddleocr_labeled_set_batch_plan.json"
    plan: Dict[str, Any] = _read_json(plan_p) if plan_p.is_file() else {}
    mat_p = Path(str(summary.get("materialize_root") or "")).expanduser()
    if not mat_p.is_absolute() or not mat_p.is_dir():
        blockers.append("invalid_materialize_root_in_summary")
    else:
        mat_sum_p = mat_p / "paddleocr_manifest_v1_cache_materialize_summary.json"
        if not mat_sum_p.is_file():
            blockers.append("missing_materialize_summary")
        else:
            ms = _read_json(mat_sum_p)
            if ms.get("materialize_verdict") != "GO":
                blockers.append("materialize_verdict_not_go")

    pinned = Path(str(summary.get("pinned_manifest") or ""))
    if not pinned.is_file():
        blockers.append("pinned_manifest_not_readable")

    crash_p = root / "paddleocr_labeled_set_batch_crash_report.json"
    crash: Dict[str, Any] = _read_json(crash_p) if crash_p.is_file() else {}
    entries = crash.get("crash_entries") if isinstance(crash.get("crash_entries"), list) else []
    for i, e in enumerate(entries):
        if not isinstance(e, dict):
            blockers.append(f"crash_entry_not_object:{i}")
            continue
        if "exit_code" not in e:
            blockers.append(f"crash_entry_missing_exit_code:{i}")
        if not e.get("last_sample_id"):
            blockers.append(f"crash_entry_missing_last_sample_id:{i}")

    mx_p = root / "paddleocr_labeled_set_batch_results_matrix.json"
    if mx_p.is_file():
        mx = _read_json(mx_p)
        rows = mx.get("rows") if isinstance(mx.get("rows"), list) else []
        for r in rows:
            if not isinstance(r, dict):
                blockers.append("matrix_row_not_object")
                break
            if "exit_code" not in r:
                blockers.append("matrix_row_missing_exit_code")
                break

    mq: Dict[str, Any] = {}
    mq_p = root / "paddleocr_labeled_set_batch_merged_quality_metrics.json"
    if mq_p.is_file():
        mq = _read_json(mq_p)
        if mq.get("production_quality_deemed_pass") is True:
            blockers.append("production_quality_deemed_pass_must_remain_false")

    aud_p = root / "paddleocr_labeled_set_batch_audit_report.json"
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

    rv = str(summary.get("batch_recovery_verdict") or "")
    if not plan.get("batches"):
        blockers.append("empty_batch_plan")

    n_exp = int(summary.get("merged_sample_count_expected") or 0)
    n_pres = int(summary.get("merged_sample_count_present") or 0)
    gt_cov = float(mq.get("ground_truth_coverage") or 0.0)

    verdict: str
    if blockers:
        verdict = "NO_GO"
    elif rv == "GO" and entries:
        blockers.append("summary_go_but_crash_entries_non_empty")
        verdict = "NO_GO"
    elif rv == "GO" and n_pres < n_exp:
        blockers.append("summary_go_but_incomplete_merge")
        verdict = "NO_GO"
    elif rv == "GO" and n_exp < 20:
        blockers.append("summary_go_but_sample_count_under_20")
        verdict = "NO_GO"
    elif rv == "GO" and gt_cov < 0.8:
        blockers.append("summary_go_but_gt_coverage_under_0_8")
        verdict = "NO_GO"
    elif rv == "GO":
        verdict = "GO"
    elif entries or n_pres < n_exp or n_exp < 20 or gt_cov < 0.8:
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "paddleocr_labeled_set_batch_recovery_verifier_report_v0",
        "phase": "Phase-PaddleOCR-Labeled-Set-Stability-Recovery-001",
        "batch_recovery_root": str(root),
        "verdict": verdict,
        "blockers": sorted(set(blockers)),
        "batch_recovery_verdict_from_summary": rv,
    }
    (root / "paddleocr_labeled_set_batch_recovery_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"batch_recovery_root": str(root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
