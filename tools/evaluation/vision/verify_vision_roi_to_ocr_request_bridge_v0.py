#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision ROI → OCRRequest bridge v0."""

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


def _audit_bool(aud: Dict[str, Any], key: str) -> bool:
    return aud.get(key) is True


def _audit_false(aud: Dict[str, Any], key: str) -> bool:
    return aud.get(key) is False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    cand_p = root / "vision_roi_to_ocr_request_candidates.json"
    matrix_p = root / "vision_roi_to_ocr_request_candidate_matrix.json"
    reject_p = root / "vision_roi_to_ocr_rejection_matrix.json"
    aud_p = root / "vision_roi_to_ocr_request_bridge_audit_report.json"
    summary_p = root / "vision_roi_to_ocr_request_bridge_summary.json"

    for label, p in (
        ("candidates", cand_p),
        ("candidate_matrix", matrix_p),
        ("rejection_matrix", reject_p),
        ("audit", aud_p),
        ("summary", summary_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "vision_roi_to_ocr_request_bridge_verifier_report_v0",
            "phase": "Phase-Vision-ROI-to-OCR-Request-Bridge-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "vision_roi_to_ocr_request_bridge_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(cand_p)
    aud = _read_json(aud_p)
    reject_doc = _read_json(reject_p)
    summary = _read_json(summary_p)

    candidates = cand_doc.get("candidates") if isinstance(cand_doc.get("candidates"), list) else []
    candidate_count = int(cand_doc.get("candidate_count") or len(candidates))

    if candidate_count <= 0:
        soft.append("candidate_count_zero_conditional_go_path")
    elif candidate_count != len(candidates):
        blockers.append("candidate_count_mismatch")

    reject_rows = reject_doc.get("rows") if isinstance(reject_doc.get("rows"), list) else []
    if not reject_rows and candidate_count <= 0:
        blockers.append("rejection_matrix_empty")

    for i, c in enumerate(candidates):
        if not isinstance(c, dict):
            blockers.append(f"candidate_invalid:{i}")
            continue
        prefix = f"candidate[{i}]"
        for key in ("source_frame_id", "roi_id", "crop_image_ref", "ocr_request"):
            if not c.get(key):
                blockers.append(f"{prefix}:missing_{key}")
        ocr = c.get("ocr_request") if isinstance(c.get("ocr_request"), dict) else {}
        if ocr.get("input_type") != "roi":
            blockers.append(f"{prefix}:ocr_input_type_not_roi")
        if ocr.get("allow_full_image") is not False:
            blockers.append(f"{prefix}:allow_full_image_not_false")
        if c.get("candidate_status") != "not_submitted":
            blockers.append(f"{prefix}:candidate_status_not_not_submitted")
        for flag in ("ocr_provider_invoked", "ocr_runtime_invoked"):
            if c.get(flag) is not False:
                blockers.append(f"{prefix}:{flag}_not_false")

    audit_checks = [
        ("vision_roi_to_ocr_request_bridge_executed", True, _audit_bool),
        ("ocr_provider_invoked", False, _audit_false),
        ("ocr_runtime_invoked", False, _audit_false),
        ("rapidocr_invoked", False, _audit_false),
        ("paddleocr_invoked", False, _audit_false),
        ("ai_interpretation_invoked", False, _audit_false),
        ("navigation_decision_invoked", False, _audit_false),
        ("midplatform_fact_written", False, _audit_false),
        ("scene_delta_written", False, _audit_false),
        ("world_model_written", False, _audit_false),
    ]
    for key, expected, fn in audit_checks:
        ok = fn(aud, key) if expected else _audit_false(aud, key)
        if not ok:
            blockers.append(f"audit:{key}")

    if candidate_count > 0 and not _audit_bool(aud, "ocr_request_candidates_generated"):
        blockers.append("audit:ocr_request_candidates_generated")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif candidate_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "vision_roi_to_ocr_request_bridge_verifier_report_v0",
        "phase": "Phase-Vision-ROI-to-OCR-Request-Bridge-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "candidate_count": candidate_count,
        "rejection_count": int(reject_doc.get("rejection_count") or len(reject_rows)),
        "vision_roi_proposal_root": summary.get("vision_roi_proposal_root"),
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_roi_to_ocr_request_bridge_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
