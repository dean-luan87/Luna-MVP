#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-Design-001 — Verifier for manifest v1 design outputs.

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


REQUIRED_EXAMPLE_FIELDS = (
    "provider_id",
    "provider_family",
    "model_format",
    "model_version",
    "language",
    "model_root",
    "det_model_ref",
    "rec_model_ref",
    "cls_model_ref",
    "offline_cache_required",
    "network_required",
    "download_authorized",
    "sha256_required",
    "runtime_default_enabled",
    "mainline_provider",
    "evaluation_candidate",
    "legacy_manifest_ref",
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--design-root", required=True, help="Output root of review_paddleocr_manifest_v1_design_v0.py")
    ap.add_argument(
        "--v1-example-relative",
        default="configs/models/ocr/paddleocr_current_api_model_manifest_v1.example.json",
    )
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    design = _require_abs(args.design_root, "--design-root")

    blockers: List[str] = []

    ex_path = repo / args.v1_example_relative.strip()
    ex_doc: Dict[str, Any] = {}
    if not ex_path.is_file():
        blockers.append("A_missing_v1_example_file")
    else:
        ex_doc = _read_json(ex_path)
        for k in REQUIRED_EXAMPLE_FIELDS:
            if k not in ex_doc:
                blockers.append(f"B_missing_required_field:{k}")
        if ex_doc.get("runtime_default_enabled") is not False:
            blockers.append(f"D_runtime_default_enabled_not_false:{ex_doc.get('runtime_default_enabled')!r}")
        if ex_doc.get("mainline_provider") is not False:
            blockers.append(f"E_mainline_provider_not_false:{ex_doc.get('mainline_provider')!r}")
        if ex_doc.get("network_required") is not False:
            blockers.append(f"F_network_required_not_false:{ex_doc.get('network_required')!r}")
        leg = str(ex_doc.get("legacy_manifest_ref") or "").strip()
        if not leg or not (repo / leg).is_file():
            blockers.append("C_legacy_manifest_ref_missing_or_not_found")

    required_design = {
        "summary": design / "paddleocr_manifest_v1_design_summary.json",
        "field_matrix": design / "paddleocr_manifest_v1_field_matrix.json",
        "legacy_matrix": design / "paddleocr_legacy_manifest_compatibility_matrix.json",
        "route_matrix": design / "paddleocr_manifest_route_decision_matrix.json",
        "notes": design / "paddleocr_manifest_v1_notes.md",
    }
    for tag, p in required_design.items():
        if not p.is_file():
            blockers.append(f"missing_design_artifact:{tag}")

    summary: Dict[str, Any] = {}
    if required_design["summary"].is_file():
        summary = _read_json(required_design["summary"])

    c = summary.get("constraints") or {}
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
        if c.get(key) is not expected:
            blockers.append(f"constraint_{key}_not_{expected}:{c.get(key)!r}")

    ac_ref = str(ex_doc.get("adapter_contract_ref") or "").strip()
    if ac_ref and not (repo / ac_ref).is_file():
        blockers.append(f"adapter_contract_ref_not_found:{ac_ref}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema": "paddleocr_manifest_v1_design_verifier_report_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-Design-001",
        "design_root": str(design),
        "verdict": verdict,
        "blockers": blockers,
        "checks": {
            "A_v1_example_exists": ex_path.is_file(),
            "B_required_fields_present": bool(ex_doc) and all(k in ex_doc for k in REQUIRED_EXAMPLE_FIELDS),
            "C_legacy_manifest_ref_resolves": bool(ex_doc)
            and bool(str(ex_doc.get("legacy_manifest_ref") or "").strip())
            and (repo / str(ex_doc.get("legacy_manifest_ref") or "").strip()).is_file(),
            "D_runtime_default_enabled_false": bool(ex_doc) and ex_doc.get("runtime_default_enabled") is False,
            "E_mainline_provider_false": bool(ex_doc) and ex_doc.get("mainline_provider") is False,
            "F_network_required_false": bool(ex_doc) and ex_doc.get("network_required") is False,
            "G_no_download_in_constraints": c.get("network_download_invoked") is False,
            "H_no_paddleocr_constructor": c.get("paddleocr_constructor_invoked") is False,
            "I_no_ocr_inference": c.get("paddleocr_inference_invoked") is False,
            "J_no_ocr_routing_changed": c.get("ocr_routing_changed") is False,
        },
    }
    out_path = design / "paddleocr_manifest_v1_design_verifier_report.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps({"design_root": str(design), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
