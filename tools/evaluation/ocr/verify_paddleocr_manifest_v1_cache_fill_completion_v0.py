#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-ManifestV1-CacheFill-001 — Aggregate completion: prepare + fill + snapshot (+ snapshot verifier).
"""

from __future__ import annotations

import argparse
import datetime as _dt
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


def _write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _constraints_bad(c: Dict[str, Any]) -> List[str]:
    bad: List[str] = []
    for k, exp in (
        ("paddleocr_constructor_invoked", False),
        ("paddleocr_inference_invoked", False),
        ("ocr_routing_changed", False),
        ("rapidocr_replaced", False),
        ("runtime_integration", False),
        ("whitebox_integration", False),
        ("midplatform_invoked", False),
    ):
        if c.get(k) is not exp:
            bad.append(f"{k}:{c.get(k)!r}")
    return bad


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--prepare-root", required=True)
    ap.add_argument("--fill-root", required=True)
    ap.add_argument("--snapshot-root", required=True)
    ap.add_argument(
        "--snapshot-verifier-report",
        default="",
        help="Defaults to <snapshot-root>/paddleocr_manifest_v1_snapshot_verifier_report.json",
    )
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    _require_abs(args.repo_root, "--repo-root")
    prepare = _require_abs(args.prepare_root, "--prepare-root")
    fill = _require_abs(args.fill_root, "--fill-root")
    snap = _require_abs(args.snapshot_root, "--snapshot-root")

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_manifest_v1_cache_fill_completion_001_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    snap_ver = (
        Path(args.snapshot_verifier_report.strip()).resolve()
        if args.snapshot_verifier_report.strip()
        else snap / "paddleocr_manifest_v1_snapshot_verifier_report.json"
    )

    blockers: List[str] = []
    cand = prepare / "paddleocr_current_api_model_manifest_v1.candidate.json"
    if not cand.is_file():
        blockers.append("B_candidate_missing")
    if not prepare.is_dir():
        blockers.append("A_prepare_root_not_dir")

    fill_sum_p = fill / "paddleocr_manifest_v1_cache_fill_summary.json"
    if not fill_sum_p.is_file():
        blockers.append("C_fill_summary_missing")

    snap_sum_p = snap / "paddleocr_manifest_v1_snapshot_summary.json"
    pinned_p = snap / "paddleocr_manifest_v1_pinned_manifest_candidate.json"
    if not snap_sum_p.is_file():
        blockers.append("D_snapshot_summary_missing")
    if not pinned_p.is_file():
        blockers.append("E_pinned_missing")

    snap_summary: Dict[str, Any] = _read_json(snap_sum_p) if snap_sum_p.is_file() else {}
    pinned: Dict[str, Any] = _read_json(pinned_p) if pinned_p.is_file() else {}
    fill_sum: Dict[str, Any] = _read_json(fill_sum_p) if fill_sum_p.is_file() else {}

    snap_verdict = str(snap_summary.get("verdict") or "")
    pin_complete = pinned.get("pinning_complete") is True
    miss = pinned.get("missing_refs") if isinstance(pinned.get("missing_refs"), list) else []
    sha_map = pinned.get("sha256_by_file") if isinstance(pinned.get("sha256_by_file"), dict) else {}

    snap_v_report: Dict[str, Any] = {}
    if snap_ver.is_file():
        snap_v_report = _read_json(snap_ver)
    else:
        blockers.append("missing_snapshot_verifier_report")

    if snap_v_report.get("verdict") != "GO":
        blockers.append(f"snapshot_verifier_not_go:{snap_v_report.get('verdict')}")

    if snap_verdict != "GO":
        blockers.append("snapshot_verdict_not_go")

    if snap_verdict == "GO":
        if not pin_complete:
            blockers.append("F_snapshot_go_but_pinning_incomplete")
        if miss:
            blockers.append("F_snapshot_go_but_missing_refs_non_empty")
        if not sha_map:
            blockers.append("F_snapshot_go_but_sha256_empty")

    if miss and snap_verdict == "GO":
        blockers.append("G_missing_refs_but_snapshot_go")

    c_fill = fill_sum.get("constraints") or {}
    c_snap = snap_summary.get("constraints") or {}
    blockers.extend([f"H_fill:{x}" for x in _constraints_bad(c_fill)])
    blockers.extend([f"H_snap:{x}" for x in _constraints_bad(c_snap)])

    fraud = [b for b in blockers if b.startswith("F_") or b == "G_missing_refs_but_snapshot_go"]
    structural = [b for b in blockers if b not in fraud]

    if fraud:
        completion_verdict = "NO_GO"
    elif not structural:
        completion_verdict = "GO"
    else:
        completion_verdict = "CONDITIONAL_GO"

    summary = {
        "schema": "paddleocr_manifest_v1_cache_fill_completion_summary_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CacheFill-001",
        "completion_verdict": completion_verdict,
        "prepare_root": str(prepare),
        "fill_root": str(fill),
        "snapshot_root": str(snap),
        "snapshot_verifier_report": str(snap_ver),
        "snapshot_verdict": snap_verdict,
        "pinning_complete": pin_complete,
        "missing_ref_count": len(miss),
        "sha256_entry_count": len(sha_map),
        "blockers": blockers,
    }
    _write_json(out / "paddleocr_manifest_v1_cache_fill_completion_summary.json", summary)

    rep = {
        "schema": "paddleocr_manifest_v1_cache_fill_completion_verifier_report_v0",
        "phase": "Phase-PaddleOCR-ManifestV1-CacheFill-001",
        "completion_output_root": str(out),
        "verdict": "GO" if completion_verdict == "GO" else ("NO_GO" if completion_verdict == "NO_GO" else "CONDITIONAL_GO"),
        "blockers": blockers,
        "checks": {
            "A_prepare_readable": prepare.is_dir(),
            "B_candidate_exists": cand.is_file(),
            "C_fill_report_exists": fill_sum_p.is_file(),
            "D_snapshot_readable": snap.is_dir(),
            "E_pinned_exists": pinned_p.is_file(),
            "F_go_implies_pinning": not (snap_verdict == "GO" and not pin_complete),
            "G_missing_implies_not_go": not (len(miss) > 0 and snap_verdict == "GO"),
            "H_no_constructor": c_fill.get("paddleocr_constructor_invoked") is False
            and c_snap.get("paddleocr_constructor_invoked") is False,
            "I_no_inference": c_fill.get("paddleocr_inference_invoked") is False
            and c_snap.get("paddleocr_inference_invoked") is False,
            "J_no_rapidocr": c_fill.get("rapidocr_replaced") is False and c_snap.get("rapidocr_replaced") is False,
            "K_no_routing": c_fill.get("ocr_routing_changed") is False and c_snap.get("ocr_routing_changed") is False,
            "L_no_runtime_whitebox_midplatform": len(_constraints_bad(c_fill)) == 0 and len(_constraints_bad(c_snap)) == 0,
        },
    }
    _write_json(out / "paddleocr_manifest_v1_cache_fill_completion_verifier_report.json", rep)

    print(
        json.dumps(
            {"completion_output_root": str(out), "completion_verdict": completion_verdict, "blockers": blockers},
            ensure_ascii=False,
        )
    )
    if completion_verdict == "NO_GO":
        return 2
    if completion_verdict == "GO":
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
