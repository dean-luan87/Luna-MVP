#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase-PaddleOCR-Weights-001 — Verifier for weights snapshot outputs (no inference checks via flags only).
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


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=REPO_ROOT)
    ap.add_argument("--snapshot-root", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).expanduser().resolve()
    root = Path(args.snapshot_root).expanduser().resolve()
    blockers: List[str] = []

    rm_path = repo / "configs" / "models" / "ocr" / "paddleocr_evaluation_readiness_manifest_v0.json"
    mf_path = repo / "configs" / "models" / "ocr" / "paddleocr_ppocrv5_model_files_manifest_v0.json"
    if not rm_path.is_file():
        blockers.append("A_readiness_manifest_unreadable")
    else:
        _read_json(rm_path)
    if not mf_path.is_file():
        blockers.append("B_model_files_manifest_unreadable")
    else:
        mf = _read_json(mf_path)
        expected = mf.get("expected_files") or []
        if not isinstance(expected, list):
            blockers.append("B_expected_files_not_list")
        else:
            roles = {str(e.get("role") or "") for e in expected if isinstance(e, dict)}
            if not {"det", "rec", "cls"}.issubset(roles):
                blockers.append("C_det_rec_cls_not_represented")

    required_out = [
        "paddleocr_weights_snapshot_summary.json",
        "paddleocr_model_file_existence_matrix.json",
        "paddleocr_model_sha256_matrix.json",
        "paddleocr_model_missing_files_report.json",
        "paddleocr_pinned_model_manifest_candidate.json",
        "paddleocr_weights_snapshot_notes.md",
    ]
    for fn in required_out:
        if not (root / fn).is_file():
            blockers.append(f"missing_output:{fn}")

    if not blockers and mf_path.is_file():
        mf = _read_json(mf_path)
        expected_n = len([x for x in (mf.get("expected_files") or []) if isinstance(x, dict)])
        ex_m = _read_json(root / "paddleocr_model_file_existence_matrix.json")
        rows = ex_m.get("rows") if isinstance(ex_m, dict) else None
        if not isinstance(rows, list) or len(rows) != expected_n:
            blockers.append("D_existence_row_count_mismatch")

        sha_m = _read_json(root / "paddleocr_model_sha256_matrix.json")
        sha_rows = sha_m.get("rows") if isinstance(sha_m, dict) else None
        if isinstance(sha_rows, list):
            for r in sha_rows:
                if not isinstance(r, dict):
                    continue
                if r.get("exists") and not str(r.get("sha256") or "").strip():
                    blockers.append(f"E_missing_sha256:{r.get('relative_path')}")

    miss_path = root / "paddleocr_model_missing_files_report.json"
    if miss_path.is_file():
        miss = _read_json(miss_path)
        if not isinstance(miss, dict) or "missing" not in miss:
            blockers.append("F_missing_report_incomplete")
    elif not blockers:
        blockers.append("F_missing_report_missing")

    pin_path = root / "paddleocr_pinned_model_manifest_candidate.json"
    if pin_path.is_file():
        pin = _read_json(pin_path)
        if pin.get("runtime_default_enabled") is not False:
            blockers.append("G_runtime_default")
        if pin.get("mainline_provider") is not False:
            blockers.append("H_mainline_provider")
        if pin.get("network_required") is not False:
            blockers.append("I_network_required")

    summ_path = root / "paddleocr_weights_snapshot_summary.json"
    if summ_path.is_file():
        sm = _read_json(summ_path)
        c = sm.get("constraints") or {}
        if c.get("paddleocr_constructor_invoked") is not False:
            blockers.append("J_constructor")
        if c.get("paddleocr_inference_invoked") is not False:
            blockers.append("K_inference")
        if c.get("runtime_integration") is not False:
            blockers.append("L_runtime")
        if c.get("whitebox_integration") is not False:
            blockers.append("M_whitebox")
        if c.get("ocr_routing_changed") is not False:
            blockers.append("N_routing")

    verdict = "NO_GO" if blockers else "GO"
    report = {
        "phase": "Phase-PaddleOCR-Weights-001",
        "verdict": verdict,
        "blockers": blockers,
        "snapshot_root": str(root),
        "repo_root": str(repo),
    }
    (root / "paddleocr_weights_snapshot_verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
