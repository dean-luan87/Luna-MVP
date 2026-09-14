#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision-triggered RapidOCR evidence read-only consumer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List


def _require_abs(p: str, label: str) -> Path:
    pp = Path(p).expanduser()
    if not pp.is_absolute():
        raise SystemExit(f"ERROR: {label} must be absolute, got: {p}")
    return pp.resolve()


def _read_json(p: Path):
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

    view_p = root / "vision_triggered_rapidocr_evidence_readonly_consumer_view.json"
    matrix_p = root / "vision_triggered_rapidocr_evidence_matrix.json"
    cmp_p = root / "vision_triggered_rapidocr_provider_comparison_summary.json"
    chain_p = root / "vision_triggered_rapidocr_source_chain_summary.json"
    aud_p = root / "vision_triggered_rapidocr_evidence_readonly_consumer_audit_report.json"
    sum_p = root / "vision_triggered_rapidocr_evidence_readonly_consumer_summary.json"

    for label, p in (
        ("consumer_view", view_p),
        ("matrix", matrix_p),
        ("comparison", cmp_p),
        ("chain", chain_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "vision_triggered_rapidocr_evidence_readonly_consumer_verifier_report_v0",
            "phase": "Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "vision_triggered_rapidocr_evidence_readonly_consumer_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    view = _read_json(view_p)
    matrix = _read_json(matrix_p)
    cmp_doc = _read_json(cmp_p)
    aud = _read_json(aud_p)
    summary = _read_json(sum_p)

    submission_count = int(view.get("submission_count") or 0)
    success_count = int(view.get("success_count") or 0)
    rapidocr_success = int(view.get("rapidocr_success_count") or 0)
    stub_fallback = int(view.get("stub_fallback_count") or 0)
    empty_text = int(view.get("empty_text_count") or 0)

    if submission_count <= 0:
        blockers.append("submission_count_not_positive")
    if success_count <= 0:
        blockers.append("success_count_not_positive")
    if str(view.get("provider") or "") != "rapidocr_candidate":
        blockers.append("provider_not_rapidocr_candidate")
    if str(view.get("provider_level") or "") != "lightweight":
        blockers.append("provider_level_not_lightweight")
    if rapidocr_success <= 0:
        blockers.append("rapidocr_success_count_not_positive")
    if stub_fallback != 0:
        blockers.append("stub_fallback_count_not_zero")

    if empty_text == 10:
        soft.append("empty_text_count_10_valid_real_provider_result")

    for key in ("evidence_by_candidate", "evidence_by_frame", "evidence_by_roi"):
        val = view.get(key)
        if not isinstance(val, dict) or not val:
            blockers.append(f"missing_or_empty:{key}")

    if view.get("fusion_status") != "not_fused":
        blockers.append("fusion_status_not_not_fused")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows:
        blockers.append("matrix_empty")

    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        if row.get("fact_status") != "not_fact":
            blockers.append(f"row[{i}]:fact_status")
        if row.get("fusion_status") != "not_fused":
            blockers.append(f"row[{i}]:fusion_status")
        est = str(row.get("evidence_status") or "")
        if est not in ("evidence_available", "evidence_available_empty_text", "gate_rejected", "no_evidence"):
            blockers.append(f"row[{i}]:invalid_evidence_status")

    upstream_checks = [
        ("rapidocr_invoked_upstream", True),
        ("real_provider_invoked_upstream", True),
        ("fallback_to_stub_upstream", False),
        ("direct_rapidocr_invoked", False),
        ("paddleocr_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("cross_modal_fusion_invoked", False),
    ]
    for key, expected in upstream_checks:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("vision_triggered_rapidocr_readonly_consumer_executed") is not True:
        blockers.append("audit:vision_triggered_rapidocr_readonly_consumer_executed")
    if aud.get("rapidocr_submission_collection_read") is not True:
        blockers.append("audit:rapidocr_submission_collection_read")

    if cmp_doc.get("note") != "rapidocr_empty_text_is_valid_real_provider_result":
        blockers.append("comparison_note_missing")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif success_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "vision_triggered_rapidocr_evidence_readonly_consumer_verifier_report_v0",
        "phase": "Phase-Vision-Triggered-OCR-RapidOCR-ReadOnly-Consumer-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "empty_text_count": empty_text,
        "rapidocr_success_count": rapidocr_success,
        "rapidocr_submission_root": summary.get("rapidocr_submission_from_vision_roi_root"),
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_triggered_rapidocr_evidence_readonly_consumer_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
