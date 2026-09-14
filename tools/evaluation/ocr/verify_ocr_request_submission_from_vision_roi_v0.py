#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for OCR request submission from Vision ROI (Phase-OCR-Request-Submission-Gated-Smoke-001)."""

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

    plan_p = root / "ocr_request_submission_plan_from_vision_roi.json"
    matrix_p = root / "ocr_request_submission_result_matrix.json"
    coll_p = root / "ocr_submission_from_vision_roi_collection.json"
    aud_p = root / "ocr_request_submission_from_vision_roi_audit_report.json"
    sum_p = root / "ocr_request_submission_from_vision_roi_summary.json"

    for label, p in (
        ("plan", plan_p),
        ("matrix", matrix_p),
        ("collection", coll_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "ocr_request_submission_from_vision_roi_verifier_report_v0",
            "phase": "Phase-OCR-Request-Submission-Gated-Smoke-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "ocr_request_submission_from_vision_roi_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    plan = _read_json(plan_p)
    matrix = _read_json(matrix_p)
    coll = _read_json(coll_p)
    aud = _read_json(aud_p)
    summary = _read_json(sum_p)

    candidate_count = int(plan.get("candidate_count") or 0)
    selected = int(plan.get("selected_candidate_count") or 0)

    if candidate_count <= 0:
        blockers.append("candidate_count_not_positive")
    if selected <= 0:
        soft.append("selected_candidate_count_zero")

    if plan.get("submission_mode") != "gated_eval_only":
        blockers.append("submission_mode_not_gated_eval_only")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows and selected > 0:
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
        if row.get("rapidocr_invoked") is True:
            blockers.append(f"row[{i}]:rapidocr_invoked_true")
        if row.get("paddleocr_invoked") is True:
            blockers.append(f"row[{i}]:paddleocr_invoked_true")

    if selected > 0 and plan.get("submit_allowed") and not bridge_invoked:
        blockers.append("ocr_mainline_bridge_not_invoked")

    if aud.get("ocr_mainline_bridge_invoked") is not True and bridge_invoked:
        blockers.append("audit:ocr_mainline_bridge_invoked_mismatch")

    boundary_false = [
        "rapidocr_invoked",
        "paddleocr_invoked",
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "ai_interpretation_invoked",
        "navigation_decision_invoked",
        "cross_modal_fusion_invoked",
        "vision_runtime_modified",
    ]
    for key in boundary_false:
        if aud.get(key) is not False:
            blockers.append(f"audit:{key}_not_false")

    if aud.get("ocr_request_submission_executed") is not True:
        blockers.append("audit:ocr_request_submission_executed")
    if aud.get("eval_only") is not True:
        blockers.append("audit:eval_only")

    if not coll.get("schema_version"):
        blockers.append("collection_missing_schema")

    success_count = int(coll.get("success_count") or 0)
    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif success_count <= 0:
        verdict = "CONDITIONAL_GO"
        soft.append("no_successful_submissions")

    rep = {
        "schema": "ocr_request_submission_from_vision_roi_verifier_report_v0",
        "phase": "Phase-OCR-Request-Submission-Gated-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "candidate_count": candidate_count,
        "selected_candidate_count": selected,
        "success_count": success_count,
        "vision_roi_to_ocr_bridge_root": summary.get("vision_roi_to_ocr_bridge_root"),
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "ocr_request_submission_from_vision_roi_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
