#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-EvaluationTools-OCR-002 — Verifier for Chinese font quality gate dataset v0.

Evaluation Tools only. Verifies manifest completeness + visible CJK flags + GT consistency.
Does NOT invoke OCR providers.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from capabilities.evaluation.ocr.ocr_synthetic_dataset_quality_gate_v0 import (
    build_chinese_dataset_quality_gate_report_v0,
)


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset-root", required=True)
    ap.add_argument("--expected-count", type=int, default=50)
    args = ap.parse_args()

    root = _require_abs(args.dataset_root, "--dataset-root")
    manifest = root / "manifest.jsonl"
    if not root.is_dir():
        raise SystemExit(f"NO_GO: dataset_root_missing:{root}")
    if not manifest.is_file():
        raise SystemExit("NO_GO: manifest_missing")

    rows = [ln for ln in manifest.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(rows) != int(args.expected_count):
        raise SystemExit(f"NO_GO: sample_count_mismatch expected={args.expected_count} actual={len(rows)}")

    blockers: List[str] = []
    category_counts: Dict[str, int] = {}
    for ln in rows:
        r = json.loads(ln)
        img = Path(str(r.get("image_path") or ""))
        gt = Path(str(r.get("ground_truth_path") or ""))
        if not img.is_file():
            blockers.append(f"missing_image:{r.get('sample_id')}")
        if not gt.is_file():
            blockers.append(f"missing_ground_truth:{r.get('sample_id')}")
        if not r.get("sha256"):
            blockers.append(f"missing_sha256:{r.get('sample_id')}")
        if not r.get("font_id"):
            blockers.append(f"missing_font_id:{r.get('sample_id')}")
        if not r.get("font_path"):
            blockers.append(f"missing_font_path:{r.get('sample_id')}")
        if r.get("visible_cjk_passed") is not True:
            blockers.append(f"visible_cjk_passed_not_true:{r.get('sample_id')}")
        if r.get("tofu_suspected") is True:
            blockers.append(f"tofu_suspected_true:{r.get('sample_id')}")
        cat = str(r.get("category") or "")
        category_counts[cat] = int(category_counts.get(cat, 0) + 1)

    gate = build_chinese_dataset_quality_gate_report_v0(dataset_root=root)
    if not gate.get("ok"):
        blockers.extend((gate.get("ground_truth_consistency") or {}).get("blockers") or [])
        blockers.extend((gate.get("cjk_visibility") or {}).get("blockers") or [])

    report: Dict[str, Any] = {
        "phase": "Phase-EvaluationTools-OCR-002",
        "verifier": "verify_ocr_chinese_font_quality_gate_dataset_v0",
        "dataset_root": str(root),
        "expected_count": int(args.expected_count),
        "actual_count": len(rows),
        "category_counts": category_counts,
        "quality_gate": gate,
        "hard_audit": {
            "ocr_provider_invoked": False,
            "runtime_integration": False,
            "whitebox_integration": False,
        },
        "verdict": "GO" if not blockers else "NO_GO",
        "blockers": blockers,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": report["verdict"], "blockers": blockers, "category_counts": category_counts}, ensure_ascii=False))
    return 0 if report["verdict"] == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())

