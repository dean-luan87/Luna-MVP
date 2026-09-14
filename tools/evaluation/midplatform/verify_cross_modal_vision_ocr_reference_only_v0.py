#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR reference-only alignment."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_ACTION_KEYS = (
    "write_midplatform_fact",
    "write_scene_delta",
    "write_world_model",
    "invoke_ai_interpretation",
    "invoke_navigation_decision",
    "claim_fused_fact",
)


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

    cand_p = root / "cross_modal_vision_ocr_reference_candidates.json"
    matrix_p = root / "cross_modal_vision_ocr_reference_matrix.json"
    align_p = root / "cross_modal_vision_ocr_alignment_summary.json"
    aud_p = root / "cross_modal_vision_ocr_reference_only_audit_report.json"
    sum_p = root / "cross_modal_vision_ocr_reference_only_summary.json"

    for label, p in (
        ("candidates", cand_p),
        ("matrix", matrix_p),
        ("alignment", align_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_reference_only_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_vision_ocr_reference_only_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(cand_p)
    matrix = _read_json(matrix_p)
    align = _read_json(align_p)
    aud = _read_json(aud_p)
    summary = _read_json(sum_p)

    refs = cand_doc.get("references") if isinstance(cand_doc.get("references"), list) else []
    matched = int(align.get("matched_reference_count") or len(refs))

    if not refs:
        blockers.append("reference_candidates_empty")
    if matched <= 0:
        blockers.append("matched_reference_count_not_positive")

    for i, ref in enumerate(refs):
        if not isinstance(ref, dict):
            blockers.append(f"reference_invalid:{i}")
            continue
        prefix = f"reference[{i}]"
        if ref.get("reference_scope") != "reference_only":
            blockers.append(f"{prefix}:reference_scope_not_reference_only")
        for key in ("frame_id", "roi_id"):
            if not str(ref.get(key) or "").strip():
                blockers.append(f"{prefix}:missing_{key}")
        ocr_refs = ref.get("ocr_refs") if isinstance(ref.get("ocr_refs"), dict) else {}
        if not str(ocr_refs.get("ocr_request_candidate_id") or "").strip():
            blockers.append(f"{prefix}:missing_ocr_request_candidate_id")
        if not str(ocr_refs.get("ocr_bridge_pack_ref") or "").strip():
            blockers.append(f"{prefix}:missing_bridge_pack_ref")
        if ref.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fact_status_not_not_fact")
        if ref.get("fusion_status") != "not_fused":
            blockers.append(f"{prefix}:fusion_status_not_not_fused")
        if ref.get("ai_interpretation_status") != "not_invoked":
            blockers.append(f"{prefix}:ai_interpretation_status_not_not_invoked")
        forbidden = ref.get("forbidden_actions") if isinstance(ref.get("forbidden_actions"), dict) else {}
        for fk in FORBIDDEN_ACTION_KEYS:
            if forbidden.get(fk) is not True:
                blockers.append(f"{prefix}:forbidden_actions_missing_{fk}")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows and refs:
        blockers.append("matrix_empty")

    boundary_false = [
        "cross_modal_fusion_invoked",
        "ai_interpretation_invoked",
        "navigation_decision_invoked",
        "midplatform_fact_written",
        "scene_delta_written",
        "world_model_written",
        "rapidocr_invoked",
        "paddleocr_invoked",
    ]
    for key in boundary_false:
        if aud.get(key) is not False:
            blockers.append(f"audit:{key}_not_false")

    if aud.get("cross_modal_reference_only_executed") is not True:
        blockers.append("audit:cross_modal_reference_only_executed")

    unmatched_vis = int(align.get("unmatched_vision_roi_count") or 0)
    if unmatched_vis > 0 and matched > 0:
        soft.append("partial_vision_roi_unmatched_expected")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif matched <= 0:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "cross_modal_vision_ocr_reference_only_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Evidence-Reference-Only-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "matched_reference_count": matched,
        "unmatched_vision_roi_count": unmatched_vis,
        "input_roots": {
            "vision_roi_proposal_root": summary.get("vision_roi_proposal_root"),
            "vision_recognition_readonly_consumer_root": summary.get("vision_recognition_readonly_consumer_root"),
            "vision_triggered_ocr_readonly_consumer_root": summary.get("vision_triggered_ocr_readonly_consumer_root"),
            "vision_roi_to_ocr_bridge_root": summary.get("vision_roi_to_ocr_bridge_root"),
        },
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_vision_ocr_reference_only_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
