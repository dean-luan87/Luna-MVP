#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision-triggered OCR evidence read-only consumer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    view_p = root / "vision_triggered_ocr_evidence_readonly_consumer_view.json"
    matrix_p = root / "vision_triggered_ocr_evidence_matrix.json"
    chain_p = root / "vision_triggered_ocr_source_chain_summary.json"
    aud_p = root / "vision_triggered_ocr_evidence_readonly_consumer_audit_report.json"
    sum_p = root / "vision_triggered_ocr_evidence_readonly_consumer_summary.json"

    for label, p in (
        ("consumer_view", view_p),
        ("matrix", matrix_p),
        ("chain", chain_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "vision_triggered_ocr_evidence_readonly_consumer_verifier_report_v0",
            "phase": "Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "vision_triggered_ocr_evidence_readonly_consumer_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    view = _read_json(view_p)
    matrix = _read_json(matrix_p)
    aud = _read_json(aud_p)
    summary = _read_json(sum_p)

    submission_count = int(view.get("submission_count") or 0)
    success_count = int(view.get("success_count") or 0)

    if submission_count <= 0:
        blockers.append("submission_count_not_positive")
    if success_count <= 0:
        soft.append("success_count_zero")

    if str(view.get("provider") or "") != "ocr_stub":
        blockers.append("provider_not_ocr_stub")

    for key in ("evidence_by_candidate", "evidence_by_frame", "evidence_by_roi"):
        val = view.get(key)
        if not isinstance(val, dict) or not val:
            blockers.append(f"missing_or_empty:{key}")

    if view.get("fusion_status") != "not_fused":
        blockers.append("fusion_status_not_not_fused")
    if view.get("ai_interpretation_status") != "not_invoked":
        blockers.append("ai_interpretation_status_not_not_invoked")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows and submission_count > 0:
        blockers.append("matrix_empty")

    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            blockers.append(f"matrix_row_invalid:{i}")
            continue
        if row.get("fact_status") != "not_fact":
            blockers.append(f"matrix_row[{i}]:fact_status_not_not_fact")
        if row.get("fusion_status") != "not_fused":
            blockers.append(f"matrix_row[{i}]:fusion_status_not_not_fused")

    boundary_false = [
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "ai_interpretation_invoked",
        "navigation_decision_invoked",
        "cross_modal_fusion_invoked",
        "rapidocr_invoked",
        "paddleocr_invoked",
    ]
    for key in boundary_false:
        if aud.get(key) is not False:
            blockers.append(f"audit:{key}_not_false")

    if aud.get("vision_triggered_ocr_readonly_consumer_executed") is not True:
        blockers.append("audit:vision_triggered_ocr_readonly_consumer_executed")
    if aud.get("ocr_submission_collection_read") is not True:
        blockers.append("audit:ocr_submission_collection_read")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif success_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "vision_triggered_ocr_evidence_readonly_consumer_verifier_report_v0",
        "phase": "Phase-Vision-OCR-Evidence-ReadOnly-Consumer-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "submission_count": submission_count,
        "success_count": success_count,
        "provider": view.get("provider"),
        "ocr_submission_root": summary.get("ocr_submission_from_vision_roi_root"),
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_triggered_ocr_evidence_readonly_consumer_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
