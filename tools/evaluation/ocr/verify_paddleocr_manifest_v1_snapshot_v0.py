#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-Snapshot-001 — Verifier for run_paddleocr_manifest_v1_snapshot_v0 outputs.
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
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--snapshot-root", required=True, help="Output root of run_paddleocr_manifest_v1_snapshot_v0.py")
    args = ap.parse_args()

    _require_abs(args.repo_root, "--repo-root")
    snap = _require_abs(args.snapshot_root, "--snapshot-root")

    blockers: List[str] = []
    paths = {
        "A_summary": snap / "paddleocr_manifest_v1_snapshot_summary.json",
        "B_field": snap / "paddleocr_manifest_v1_field_matrix.json",
        "C_cache": snap / "paddleocr_manifest_v1_model_cache_matrix.json",
        "D_sha": snap / "paddleocr_manifest_v1_sha256_matrix.json",
        "E_missing": snap / "paddleocr_manifest_v1_missing_cache_report.json",
        "F_pinned": snap / "paddleocr_manifest_v1_pinned_manifest_candidate.json",
        "G_notes": snap / "paddleocr_manifest_v1_snapshot_notes.md",
    }
    for tag, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing_output:{tag}")

    summary: Dict[str, Any] = {}
    pinned: Dict[str, Any] = {}
    if paths["A_summary"].is_file():
        summary = _read_json(paths["A_summary"])
    if paths["F_pinned"].is_file():
        pinned = _read_json(paths["F_pinned"])

    c = summary.get("constraints") or {}
    for key, expected in (
        ("network_download_invoked", False),
        ("paddleocr_constructor_invoked", False),
        ("paddleocr_inference_invoked", False),
        ("ocr_routing_changed", False),
        ("rapidocr_replaced", False),
        ("runtime_integration", False),
        ("whitebox_integration", False),
        ("midplatform_invoked", False),
        ("scene_delta_invoked", False),
        ("world_context_evidence_invoked", False),
    ):
        if c.get(key) is not expected:
            blockers.append(f"L-P_constraint_{key}:{c.get(key)!r}")

    if pinned:
        if pinned.get("runtime_default_enabled") is not False:
            blockers.append(f"H_runtime_default_not_false:{pinned.get('runtime_default_enabled')!r}")
        if pinned.get("mainline_provider") is not False:
            blockers.append(f"I_mainline_provider_not_false:{pinned.get('mainline_provider')!r}")
        if pinned.get("network_required") is not False:
            blockers.append(f"J_network_required_not_false:{pinned.get('network_required')!r}")
        if pinned.get("download_authorized") is not False:
            blockers.append(f"K_download_authorized_not_false:{pinned.get('download_authorized')!r}")

    sv = str(summary.get("verdict") or "")
    miss = pinned.get("missing_refs") if isinstance(pinned.get("missing_refs"), list) else []
    pin_ok = pinned.get("pinning_complete") is True

    if sv == "GO":
        if miss:
            blockers.append("Q_verdict_go_but_missing_refs_non_empty")
        if not pin_ok:
            blockers.append("Q_verdict_go_but_pinning_incomplete")

    if miss and sv != "CONDITIONAL_GO":
        blockers.append("R_non_empty_missing_requires_conditional_go_verdict")

    verdict = "GO" if not blockers else "NO_GO"
    report = {
        "schema": "paddleocr_manifest_v1_snapshot_verifier_report_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-Snapshot-001",
        "snapshot_root": str(snap),
        "verdict": verdict,
        "blockers": blockers,
        "checks": {
            "A_summary_exists": paths["A_summary"].is_file(),
            "B_field_matrix_exists": paths["B_field"].is_file(),
            "C_cache_matrix_exists": paths["C_cache"].is_file(),
            "D_sha256_matrix_exists": paths["D_sha"].is_file(),
            "E_missing_report_exists": paths["E_missing"].is_file(),
            "F_pinned_exists": paths["F_pinned"].is_file(),
            "G_notes_exists": paths["G_notes"].is_file(),
            "H_runtime_default_false": pinned.get("runtime_default_enabled") is False if pinned else False,
            "I_mainline_false": pinned.get("mainline_provider") is False if pinned else False,
            "J_network_required_false": pinned.get("network_required") is False if pinned else False,
            "K_download_authorized_false": pinned.get("download_authorized") is False if pinned else False,
            "L_no_constructor": c.get("paddleocr_constructor_invoked") is False,
            "M_no_inference": c.get("paddleocr_inference_invoked") is False,
            "N_no_runtime_integration": c.get("runtime_integration") is False,
            "O_no_whitebox": c.get("whitebox_integration") is False,
            "P_no_routing": c.get("ocr_routing_changed") is False,
            "Q_go_implies_no_missing": not (sv == "GO" and miss and len(miss) > 0),
            "R_missing_implies_conditional": not (miss and sv == "GO"),
        },
    }
    (snap / "paddleocr_manifest_v1_snapshot_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"snapshot_root": str(snap), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
