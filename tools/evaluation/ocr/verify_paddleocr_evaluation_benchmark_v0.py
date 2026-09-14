#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Evaluation-Benchmark-001 — Verifier for run_paddleocr_evaluation_benchmark_v0 outputs.
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
    ap.add_argument("--benchmark-root", required=True, help="Output root of run_paddleocr_evaluation_benchmark_v0.py")
    args = ap.parse_args()

    root = _require_abs(args.benchmark_root, "--benchmark-root")
    blockers: List[str] = []

    sum_p = root / "paddleocr_benchmark_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_benchmark_summary")
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

    sm_path = Path(str(summary.get("sample_manifest") or ""))
    if not sm_path.is_file():
        blockers.append("sample_manifest_not_readable")
    else:
        sm = _read_json(sm_path)
        samples = sm.get("samples") if isinstance(sm.get("samples"), list) else []
        if len(samples) == 0:
            blockers.append("sample_count_zero")
        if len(samples) > 20:
            blockers.append("sample_count_exceeds_20")
        for i, row in enumerate(samples):
            if not isinstance(row, dict):
                blockers.append(f"sample_not_object:{i}")
                continue
            ip = Path(str(row.get("image_path") or ""))
            if not ip.is_file():
                blockers.append(f"image_not_readable:{i}:{ip}")

    sc = int(summary.get("sample_count") or 0)
    if sc <= 0:
        blockers.append("summary_sample_count_not_positive")
    if sc > 20:
        blockers.append("summary_sample_count_over_20")

    for name in (
        "paddleocr_benchmark_sample_matrix.json",
        "paddleocr_benchmark_raw_results.json",
        "paddleocr_benchmark_normalized_results.json",
        "paddleocr_benchmark_evidence_results.json",
        "paddleocr_benchmark_quality_metrics.json",
        "paddleocr_benchmark_runtime_metrics.json",
        "paddleocr_benchmark_error_report.json",
        "paddleocr_benchmark_audit_report.json",
    ):
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    qm_p = root / "paddleocr_benchmark_quality_metrics.json"
    if qm_p.is_file():
        qm = _read_json(qm_p)
        if qm.get("accuracy_pass_claimed") is True and int(qm.get("ground_truth_evaluated_count") or 0) <= 0:
            blockers.append("accuracy_claimed_without_ground_truth")

    aud_p = root / "paddleocr_benchmark_audit_report.json"
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

    if summary.get("benchmark_verdict") == "GO" and summary.get("constructor_ok") is not True:
        blockers.append("summary_go_but_constructor_not_ok")

    verdict = "NO_GO" if blockers else "GO"

    rep = {
        "schema": "paddleocr_benchmark_verifier_report_v0",
        "phase": "Phase-PaddleOCR-Evaluation-Benchmark-001",
        "benchmark_root": str(root),
        "verdict": verdict,
        "blockers": sorted(set(blockers)),
    }
    (root / "paddleocr_benchmark_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"benchmark_root": str(root), "verdict": verdict, "blockers": rep["blockers"]}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
