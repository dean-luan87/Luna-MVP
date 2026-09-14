#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ModelFormat-001 — Verifier for review_paddleocr_model_format_compatibility_v0 outputs.

Does not download models, construct PaddleOCR, or run OCR.
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
    ap.add_argument("--review-root", required=True, help="Output root of review_paddleocr_model_format_compatibility_v0.py")
    ap.add_argument("--repo-root", default=REPO_ROOT)
    args = ap.parse_args()

    root = _require_abs(args.review_root, "--review-root")
    _require_abs(args.repo_root, "--repo-root")

    required = {
        "A": root / "paddleocr_model_format_review_summary.json",
        "B": root / "paddleocr_installed_version_report.json",
        "C": root / "paddleocr_api_signature_report.json",
        "D": root / "paddleocr_manifest_format_compatibility_matrix.json",
        "E": root / "paddleocr_model_format_route_options.json",
    }
    required_md = root / "paddleocr_model_format_review_notes.md"

    blockers: List[str] = []
    for tag, p in required.items():
        if not p.is_file():
            blockers.append(f"missing_output_{tag}:{p.name}")

    if not required_md.is_file():
        blockers.append("missing_review_notes_md")

    summary: Dict[str, Any] = {}
    if required["A"].is_file():
        summary = _read_json(required["A"])

    constraints = summary.get("constraints") or {}
    for key, expected in (
        ("network_download_invoked", False),
        ("paddleocr_constructor_invoked", False),
        ("paddleocr_inference_invoked", False),
        ("ocr_routing_changed", False),
        ("rapidocr_replaced", False),
        ("runtime_integration", False),
        ("whitebox_integration", False),
        ("mainline_side_effect", False),
        ("midplatform_invoked", False),
    ):
        if constraints.get(key) is not expected:
            blockers.append(f"constraint_{key}_not_{expected}:{constraints.get(key)!r}")

    if required["E"].is_file():
        routes_doc = _read_json(required["E"])
        rts = routes_doc.get("routes")
        if not isinstance(rts, list) or len(rts) < 3:
            blockers.append("route_options_incomplete")
        ids = {str(x.get("id")) for x in rts if isinstance(x, dict)} if isinstance(rts, list) else set()
        if not {"A", "B", "C"}.issubset(ids):
            blockers.append("route_options_missing_ABC")

    if required["D"].is_file():
        mtx = _read_json(required["D"])
        rows = mtx.get("rows")
        if not isinstance(rows, list) or len(rows) < 2:
            blockers.append("compatibility_matrix_too_thin")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema": "paddleocr_model_format_review_verifier_report_v0",
        "phase": "Phase-PaddleOCR-ModelFormat-001",
        "review_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "checks": {
            "A_review_summary_exists": required["A"].is_file(),
            "B_installed_version_report_exists": required["B"].is_file(),
            "C_api_signature_report_exists": required["C"].is_file(),
            "D_manifest_compatibility_matrix_exists": required["D"].is_file(),
            "E_route_options_exists": required["E"].is_file(),
            "F_no_download_invoked": constraints.get("network_download_invoked") is False,
            "G_no_paddleocr_constructor_invoked": constraints.get("paddleocr_constructor_invoked") is False,
            "H_no_ocr_inference_invoked": constraints.get("paddleocr_inference_invoked") is False,
            "I_no_runtime_integration": constraints.get("runtime_integration") is False,
            "J_no_ocr_routing_changed": constraints.get("ocr_routing_changed") is False,
            "K_no_rapidocr_replaced": constraints.get("rapidocr_replaced") is False,
            "L_no_whitebox_integration": constraints.get("whitebox_integration") is False,
            "M_no_midplatform_invoked": constraints.get("midplatform_invoked") is False,
            "N_no_mainline_side_effect": constraints.get("mainline_side_effect") is False,
        },
    }
    out_path = root / "paddleocr_model_format_review_verifier_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({"review_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
