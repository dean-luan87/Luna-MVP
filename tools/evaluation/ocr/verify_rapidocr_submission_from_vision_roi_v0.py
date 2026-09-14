#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for RapidOCR submission from Vision ROI."""

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

    plan_p = root / "rapidocr_submission_plan_from_vision_roi.json"
    matrix_p = root / "rapidocr_submission_result_matrix.json"
    coll_p = root / "rapidocr_submission_from_vision_roi_collection.json"
    prov_p = root / "rapidocr_submission_provider_summary.json"
    aud_p = root / "rapidocr_submission_from_vision_roi_audit_report.json"
    sum_p = root / "rapidocr_submission_from_vision_roi_summary.json"

    for label, p in (
        ("plan", plan_p),
        ("matrix", matrix_p),
        ("collection", coll_p),
        ("provider_summary", prov_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "rapidocr_submission_from_vision_roi_verifier_report_v0",
            "phase": "Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "rapidocr_submission_from_vision_roi_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    plan = _read_json(plan_p)
    matrix = _read_json(matrix_p)
    coll = _read_json(coll_p)
    aud = _read_json(aud_p)
    summary = _read_json(sum_p)

    if int(plan.get("candidate_count") or 0) <= 0:
        blockers.append("candidate_count_not_positive")
    if int(plan.get("selected_candidate_count") or 0) <= 0:
        blockers.append("selected_candidate_count_not_positive")
    if plan.get("submission_mode") != "gated_eval_only":
        blockers.append("submission_mode_not_gated_eval_only")
    if plan.get("real_provider_requested") is not True:
        blockers.append("real_provider_requested_not_true")
    if plan.get("rapidocr_runtime_provider_enabled") is not True:
        blockers.append("rapidocr_runtime_provider_enabled_not_true")
    if plan.get("paddleocr_runtime_provider_enabled") is not False:
        blockers.append("paddleocr_runtime_provider_enabled_not_false")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows:
        blockers.append("result_matrix_empty")

    bridge_invoked = False
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            blockers.append(f"row_invalid:{i}")
            continue
        for key in ("candidate_id", "roi_id", "ocr_request_id"):
            if not str(row.get(key) or "").strip():
                blockers.append(f"row[{i}]:missing_{key}")
        if row.get("ocr_bridge_status"):
            bridge_invoked = True
        if row.get("paddleocr_invoked") is True:
            blockers.append(f"row[{i}]:paddleocr_invoked_true")

    if int(plan.get("selected_candidate_count") or 0) > 0 and plan.get("submit_allowed") and not bridge_invoked:
        blockers.append("ocr_mainline_bridge_not_invoked")

    rapidocr_success = int(coll.get("rapidocr_success_count") or 0)
    stub_fallback = int(coll.get("stub_fallback_count") or 0)
    if rapidocr_success <= 0 and stub_fallback > 0:
        soft.append("rapidocr_unavailable_stub_fallback_observed")
    if rapidocr_success <= 0 and stub_fallback <= 0:
        soft.append("no_rapidocr_success_and_no_stub_fallback")

    boundary = [
        ("direct_rapidocr_invoked", False),
        ("paddleocr_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("cross_modal_fusion_invoked", False),
        ("vision_runtime_modified", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("rapidocr_submission_from_vision_roi_executed") is not True:
        blockers.append("audit:rapidocr_submission_from_vision_roi_executed")
    if aud.get("ocr_mainline_bridge_invoked") is not True and bridge_invoked:
        blockers.append("audit:ocr_mainline_bridge_invoked_mismatch")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif rapidocr_success <= 0:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "rapidocr_submission_from_vision_roi_verifier_report_v0",
        "phase": "Phase-OCR-Real-RapidOCR-Submission-From-Vision-ROI-Gated-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "rapidocr_success_count": rapidocr_success,
        "stub_fallback_count": stub_fallback,
        "vision_roi_to_ocr_bridge_root": summary.get("vision_roi_to_ocr_bridge_root"),
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "rapidocr_submission_from_vision_roi_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
