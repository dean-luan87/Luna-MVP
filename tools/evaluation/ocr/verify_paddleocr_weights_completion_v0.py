#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Weights-003 — Aggregate completion: optional prepare audit + snapshot + snapshot verifier.

Does not run PaddleOCR or OCR inference. Does not copy or download weights.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

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


def _expected_rel_paths(repo: Path, mf_rel: str) -> List[str]:
    doc = _read_json(repo / mf_rel)
    out: List[str] = []
    for e in doc.get("expected_files") or []:
        if isinstance(e, dict):
            rel = str(e.get("relative_path") or "").strip()
            if rel:
                out.append(rel)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--snapshot-root", required=True, help="Output root of run_paddleocr_weights_snapshot_v0.py")
    ap.add_argument("--prepare-root", default="", help="Optional output root of prepare_paddleocr_evaluation_weights_v0.py")
    ap.add_argument("--model-files-manifest", default="configs/models/ocr/paddleocr_ppocrv5_model_files_manifest_v0.json")
    ap.add_argument("--output-root", default="")
    args = ap.parse_args()

    repo = _require_abs(args.repo_root, "--repo-root")
    snap = _require_abs(args.snapshot_root, "--snapshot-root")
    prepare_root: Optional[Path] = _require_abs(args.prepare_root, "--prepare-root") if args.prepare_root.strip() else None

    if args.output_root.strip():
        out = _require_abs(args.output_root, "--output-root")
    else:
        stamp = _dt.datetime.utcnow().strftime("%Y%m%d_%H%M%SZ")
        out = (Path.home() / "LunaRuntime" / "logs" / "evaluation" / f"paddleocr_weights_completion_003_{stamp}").resolve()
    out.mkdir(parents=True, exist_ok=True)

    blockers: List[str] = []
    snap_summary_path = snap / "paddleocr_weights_snapshot_summary.json"
    pinned_path = snap / "paddleocr_pinned_model_manifest_candidate.json"
    snap_ver_path = snap / "paddleocr_weights_snapshot_verifier_report.json"

    if not snap_summary_path.is_file():
        blockers.append("missing_snapshot_summary")
    if not pinned_path.is_file():
        blockers.append("missing_pinned_candidate")
    if not snap_ver_path.is_file():
        blockers.append("missing_snapshot_verifier_report")

    snap_summary: Dict[str, Any] = {}
    pinned: Dict[str, Any] = {}
    snap_ver: Dict[str, Any] = {}
    if snap_summary_path.is_file():
        snap_summary = _read_json(snap_summary_path)
    if pinned_path.is_file():
        pinned = _read_json(pinned_path)
    if snap_ver_path.is_file():
        snap_ver = _read_json(snap_ver_path)

    if snap_ver.get("verdict") != "GO":
        blockers.append(f"snapshot_verifier_not_go:{snap_ver.get('verdict')}")

    if snap_summary.get("missing_file_count", -1) != 0:
        blockers.append(f"missing_file_count_not_zero:{snap_summary.get('missing_file_count')}")
    if snap_summary.get("verdict") != "GO":
        blockers.append(f"snapshot_verdict_not_go:{snap_summary.get('verdict')}")
    if not snap_summary.get("all_planned_files_exist"):
        blockers.append("all_planned_files_exist_false")

    c = snap_summary.get("constraints") or {}
    for k in (
        "paddleocr_constructor_invoked",
        "paddleocr_inference_invoked",
        "ocr_routing_changed",
        "rapidocr_replaced",
    ):
        if c.get(k) is not False:
            blockers.append(f"snapshot_constraint:{k}")

    if pinned.get("runtime_default_enabled") is not False:
        blockers.append("pinned_runtime_default_not_false")
    if pinned.get("mainline_provider") is not False:
        blockers.append("pinned_mainline_provider_not_false")

    expected = _expected_rel_paths(repo, args.model_files_manifest.strip())
    sha_map = pinned.get("weights_sha256") if isinstance(pinned.get("weights_sha256"), dict) else {}
    sha_blockers: List[str] = []
    for rel in expected:
        h = sha_map.get(rel)
        if not isinstance(h, str) or len(h.strip()) < 32:
            sha_blockers.append(f"sha256_missing_or_short:{rel}")
    blockers.extend(sha_blockers)

    fake_go = snap_summary.get("verdict") == "GO" and bool(sha_blockers)
    if fake_go:
        blockers.append("NO_GO_inconsistent_snapshot_claims_go_but_sha_incomplete")

    prepare_info: Optional[Dict[str, Any]] = None
    if prepare_root is not None:
        pp = prepare_root / "paddleocr_weights_prepare_summary.json"
        if pp.is_file():
            prepare_info = _read_json(pp)

    if fake_go:
        verdict = "NO_GO"
    elif not blockers:
        verdict = "GO"
    else:
        verdict = "CONDITIONAL_GO"

    completion_summary: Dict[str, Any] = {
        "phase": "Phase-PaddleOCR-Weights-003",
        "repo_root": str(repo),
        "snapshot_root": str(snap),
        "prepare_root": str(prepare_root) if prepare_root else None,
        "completion_output_root": str(out),
        "snapshot_summary_excerpt": {
            "verdict": snap_summary.get("verdict"),
            "missing_file_count": snap_summary.get("missing_file_count"),
            "all_planned_files_exist": snap_summary.get("all_planned_files_exist"),
            "all_sha256_computed_for_existing": snap_summary.get("all_sha256_computed_for_existing"),
        },
        "pinned_sha256_entry_count": len(sha_map) if isinstance(sha_map, dict) else 0,
        "expected_file_count": len(expected),
        "snapshot_verifier_verdict": snap_ver.get("verdict"),
        "prepare_summary_present": prepare_info is not None,
        "prepare_summary_excerpt": prepare_info,
        "completion_verdict": verdict,
        "readiness_posture": "GO_weights_pinned_reproducible"
        if verdict == "GO"
        else ("NO_GO_integrity" if verdict == "NO_GO" else "CONDITIONAL_GO_weights_incomplete"),
    }

    rep = {
        "phase": "Phase-PaddleOCR-Weights-003",
        "verdict": verdict,
        "blockers": blockers,
        "snapshot_root": str(snap),
    }

    (out / "paddleocr_weights_completion_summary.json").write_text(
        json.dumps(completion_summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out / "paddleocr_weights_completion_verifier_report.json").write_text(
        json.dumps(rep, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({**rep, "completion_output_root": str(out)}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    if verdict == "CONDITIONAL_GO":
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
