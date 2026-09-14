#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-CacheMaterialize-001 — Verifier for run_paddleocr_manifest_v1_cache_materialize_v0 output.
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


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--materialize-root", required=True, help="Output root of run_paddleocr_manifest_v1_cache_materialize_v0.py")
    args = ap.parse_args()

    root = _require_abs(args.materialize_root, "--materialize-root")
    sum_p = root / "paddleocr_manifest_v1_cache_materialize_summary.json"
    blockers: List[str] = []
    if not sum_p.is_file():
        blockers.append("missing_materialize_summary")

    doc: Dict[str, Any] = _read_json(sum_p) if sum_p.is_file() else {}

    for sub, label in (
        ("fill", "fill_root"),
        ("snapshot", "snapshot_root"),
        ("completion", "completion_root"),
    ):
        p = root / sub
        if not p.is_dir():
            blockers.append(f"missing_subdir:{sub}")

    mv = str(doc.get("materialize_verdict") or "")
    if mv == "GO":
        if doc.get("completion_verdict") != "GO":
            blockers.append("materialize_go_but_completion_not_go")
        if doc.get("snapshot_summary_verdict") != "GO":
            blockers.append("materialize_go_but_snapshot_summary_not_go")
        if doc.get("pinning_complete") is not True:
            blockers.append("materialize_go_but_pinning_incomplete")
        if (doc.get("sha256_entry_count") or 0) <= 0:
            blockers.append("materialize_go_but_sha256_empty")
        if (doc.get("missing_ref_count") or 0) > 0:
            blockers.append("materialize_go_but_missing_refs")

    c = doc.get("constraints") or {}
    for k, exp in (
        ("paddleocr_constructor_invoked", False),
        ("paddleocr_inference_invoked", False),
        ("ocr_routing_changed", False),
        ("rapidocr_replaced", False),
    ):
        if c.get(k) is not exp:
            blockers.append(f"constraint_{k}")

    if blockers:
        verdict = "NO_GO"
    elif doc.get("materialize_verdict") != "GO":
        verdict = "CONDITIONAL_GO"
    else:
        verdict = "GO"

    rep = {
        "schema": "paddleocr_manifest_v1_cache_materialize_verifier_report_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CacheMaterialize-001",
        "materialize_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "materialize_verdict_from_summary": doc.get("materialize_verdict"),
    }
    (root / "paddleocr_manifest_v1_cache_materialize_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"materialize_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict != "NO_GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
