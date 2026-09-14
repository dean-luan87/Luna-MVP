#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-CachePrepare-001 — Verifier for prepare_paddleocr_manifest_v1_cache_plan_v0 outputs.
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


def _is_placeholder(s: Any) -> bool:
    t = str(s or "").strip()
    return not t or "<PLACEHOLDER" in t


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--prepare-root", required=True, help="Output root of prepare_paddleocr_manifest_v1_cache_plan_v0.py")
    ap.add_argument(
        "--url-template-relative",
        default="configs/models/ocr/paddleocr_current_api_model_download_urls_v1.example.json",
    )
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    root = _require_abs(args.prepare_root, "--prepare-root")

    blockers: List[str] = []
    files = {
        "summary": root / "paddleocr_manifest_v1_cache_prepare_summary.json",
        "candidate": root / "paddleocr_current_api_model_manifest_v1.candidate.json",
        "acquisition": root / "paddleocr_manifest_v1_cache_acquisition_plan.json",
        "matrix": root / "paddleocr_manifest_v1_expected_directory_matrix.json",
        "manual_md": root / "paddleocr_manifest_v1_manual_copy_instructions.md",
        "notes_md": root / "paddleocr_manifest_v1_cache_prepare_notes.md",
    }
    for tag, p in files.items():
        if not p.is_file():
            blockers.append(f"A_missing_output:{tag}")

    cand: Dict[str, Any] = {}
    acq: Dict[str, Any] = {}
    summ: Dict[str, Any] = {}
    if files["candidate"].is_file():
        cand = _read_json(files["candidate"])
    if files["acquisition"].is_file():
        acq = _read_json(files["acquisition"])
    if files["summary"].is_file():
        summ = _read_json(files["summary"])

    if _is_placeholder(cand.get("model_root")):
        blockers.append("C_model_root_still_placeholder")
    for k in ("det_model_ref", "rec_model_ref", "cls_model_ref"):
        if _is_placeholder(cand.get(k)):
            blockers.append(f"D_placeholder_ref:{k}")

    for k, expected in (
        ("runtime_default_enabled", False),
        ("mainline_provider", False),
        ("network_required", False),
        ("download_authorized", False),
    ):
        if cand.get(k) is not expected:
            blockers.append(f"policy_{k}:{cand.get(k)!r}")

    if cand.get("evaluation_candidate") is not True:
        blockers.append("policy_evaluation_candidate_must_be_true")

    sb = cand.get("sha256_by_file")
    if isinstance(sb, dict) and len(sb) > 0:
        blockers.append("candidate_sha256_by_file_must_be_empty_at_prepare_phase")

    if cand.get("pinning_complete") is True:
        blockers.append("candidate_pinning_complete_must_not_be_true")

    if acq.get("download_completed") is True:
        blockers.append("I_download_marked_completed")
    if acq.get("pinning_complete") is True:
        blockers.append("I_pinning_marked_complete")
    if acq.get("authorized_download_required") is True:
        blockers.append("I_authorized_download_required_true")

    url_path = repo / args.url_template_relative.strip()
    if not url_path.is_file():
        blockers.append("J_url_template_missing_in_repo")

    c = summ.get("constraints") or {}
    for key, expected in (
        ("network_download_invoked", False),
        ("paddleocr_constructor_invoked", False),
        ("paddleocr_inference_invoked", False),
        ("ocr_routing_changed", False),
        ("rapidocr_replaced", False),
        ("runtime_integration", False),
        ("whitebox_integration", False),
        ("midplatform_invoked", False),
    ):
        if c.get(key) is not expected:
            blockers.append(f"K-N_constraint_{key}:{c.get(key)!r}")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema": "paddleocr_manifest_v1_cache_prepare_verifier_report_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CachePrepare-001",
        "prepare_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "checks": {
            "A_outputs": all(p.is_file() for p in files.values()),
            "B_candidate_exists": files["candidate"].is_file(),
            "C_model_root_concrete": not _is_placeholder(cand.get("model_root")),
            "D_refs_concrete": not any(_is_placeholder(cand.get(x)) for x in ("det_model_ref", "rec_model_ref", "cls_model_ref")),
            "E_runtime_default_false": cand.get("runtime_default_enabled") is False,
            "F_mainline_false": cand.get("mainline_provider") is False,
            "G_network_false": cand.get("network_required") is False,
            "H_download_auth_false": cand.get("download_authorized") is False,
            "I_acquisition_plan_ok": files["acquisition"].is_file() and acq.get("download_completed") is not True,
            "J_url_template_repo_exists": url_path.is_file(),
            "K_no_download_invoked": c.get("network_download_invoked") is False,
            "L_no_constructor": c.get("paddleocr_constructor_invoked") is False,
            "M_no_inference": c.get("paddleocr_inference_invoked") is False,
            "N_no_routing": c.get("ocr_routing_changed") is False,
        },
    }
    (root / "paddleocr_manifest_v1_cache_prepare_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"prepare_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
