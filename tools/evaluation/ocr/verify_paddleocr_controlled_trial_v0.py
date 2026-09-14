#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Controlled-Trial-001 — Verifier for run_paddleocr_controlled_trial_v0 outputs.
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
    ap.add_argument("--trial-root", required=True, help="Output root of run_paddleocr_controlled_trial_v0.py")
    ap.add_argument("--materialize-root", default="", help="Optional; default read from trial summary.")
    args = ap.parse_args()

    root = _require_abs(args.trial_root, "--trial-root")
    blockers: List[str] = []

    sum_p = root / "paddleocr_controlled_trial_summary.json"
    if not sum_p.is_file():
        blockers.append("missing_trial_summary")
    summary: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}

    mat_root = Path(str(args.materialize_root or summary.get("materialize_root") or "")).expanduser()
    if not mat_root.is_absolute() or not mat_root.is_dir():
        blockers.append("missing_or_invalid_materialize_root")
    else:
        mat_sum_p = mat_root / "paddleocr_manifest_v1_cache_materialize_summary.json"
        if not mat_sum_p.is_file():
            blockers.append("missing_materialize_summary")
        else:
            ms = _read_json(mat_sum_p)
            if ms.get("materialize_verdict") != "GO":
                blockers.append("materialize_verdict_not_go")

    pinned_path = Path(str(summary.get("pinned_manifest") or ""))
    if not pinned_path.is_file():
        blockers.append("missing_pinned_manifest_path_in_summary")
    else:
        pinned = _read_json(pinned_path)
        if pinned.get("pinning_complete") is not True:
            blockers.append("pinning_incomplete")
        if (pinned.get("missing_ref_count") or 0) > 0:
            blockers.append("missing_ref_count_positive")
        sha = pinned.get("sha256_by_file") or {}
        if not isinstance(sha, dict) or len(sha) == 0:
            blockers.append("sha256_by_file_empty")

    for name in (
        "paddleocr_controlled_trial_constructor_report.json",
        "paddleocr_controlled_trial_audit_report.json",
        "paddleocr_controlled_trial_error_report.json",
        "paddleocr_controlled_trial_ocr_results_raw.json",
        "paddleocr_controlled_trial_ocr_results_normalized.json",
    ):
        if not (root / name).is_file():
            blockers.append(f"missing:{name}")

    audit_p = root / "paddleocr_controlled_trial_audit_report.json"
    audit: Dict[str, Any] = _read_json(audit_p) if audit_p.is_file() else {}
    if audit.get("network_request_invoked") is True:
        blockers.append("network_request_invoked")
    if audit.get("ocr_routing_changed") is True:
        blockers.append("ocr_routing_changed")
    if audit.get("rapidocr_replaced") is True:
        blockers.append("rapidocr_replaced")
    if audit.get("runtime_integration") is True:
        blockers.append("runtime_integration")
    if audit.get("whitebox_integration") is True:
        blockers.append("whitebox_integration")
    if audit.get("midplatform_invoked") is True:
        blockers.append("midplatform_invoked")
    if audit.get("model_cache_modified") is True:
        blockers.append("model_cache_modified")

    sc = int(audit.get("sample_count") or 0)
    if sc > 3:
        blockers.append("sample_count_gt_3")

    cons_p = root / "paddleocr_controlled_trial_constructor_report.json"
    cons: Dict[str, Any] = _read_json(cons_p) if cons_p.is_file() else {}
    tv = str(summary.get("trial_verdict") or "")

    if cons.get("constructor_ok") is not True and tv == "GO":
        blockers.append("constructor_failed_but_trial_go")

    if not audit.get("constructor_only") and tv == "GO":
        raw_doc = _read_json(root / "paddleocr_controlled_trial_ocr_results_raw.json") if (root / "paddleocr_controlled_trial_ocr_results_raw.json").is_file() else {}
        rows = raw_doc.get("results") if isinstance(raw_doc.get("results"), list) else []
        if not rows:
            blockers.append("ocr_trial_go_requires_results")
        elif not all(isinstance(r, dict) and r.get("ok") for r in rows):
            blockers.append("ocr_trial_not_all_ok")

    verdict = "NO_GO" if blockers or tv == "NO_GO" else ("GO" if tv == "GO" else "CONDITIONAL_GO")

    rep = {
        "schema": "paddleocr_controlled_trial_verifier_report_v0",
        "phase": "Phase-PaddleOCR-Controlled-Trial-001",
        "trial_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "trial_verdict_from_summary": tv,
    }
    (root / "paddleocr_controlled_trial_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"trial_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
