#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR reference-only (RapidOCR)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

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

    cand_p = root / "cross_modal_vision_ocr_reference_candidates_rapidocr.json"
    matrix_p = root / "cross_modal_vision_ocr_reference_matrix_rapidocr.json"
    align_p = root / "cross_modal_vision_ocr_alignment_summary_rapidocr.json"
    cmp_p = root / "cross_modal_vision_ocr_stub_vs_rapidocr_comparison.json"
    aud_p = root / "cross_modal_vision_ocr_reference_only_rapidocr_audit_report.json"
    sum_p = root / "cross_modal_vision_ocr_reference_only_rapidocr_summary.json"

    for label, p in (
        ("candidates", cand_p),
        ("matrix", matrix_p),
        ("alignment", align_p),
        ("comparison", cmp_p),
        ("audit", aud_p),
        ("summary", sum_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_reference_only_rapidocr_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Reference-Only-002",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_vision_ocr_reference_only_rapidocr_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(cand_p)
    matrix = _read_json(matrix_p)
    align = _read_json(align_p)
    cmp_doc = _read_json(cmp_p)
    aud = _read_json(aud_p)
    summary = _read_json(sum_p)

    refs = cand_doc.get("references") if isinstance(cand_doc.get("references"), list) else []
    matched = int(align.get("matched_reference_count") or len(refs))
    empty_text_refs = int(align.get("empty_text_reference_count") or 0)

    if not refs:
        blockers.append("reference_candidates_empty")
    if matched <= 0:
        blockers.append("matched_reference_count_not_positive")
    if str(align.get("provider") or "") != "rapidocr_candidate":
        blockers.append("alignment_provider_not_rapidocr_candidate")

    for i, ref in enumerate(refs):
        if not isinstance(ref, dict):
            blockers.append(f"reference_invalid:{i}")
            continue
        prefix = f"reference[{i}]"
        if ref.get("reference_scope") != "reference_only":
            blockers.append(f"{prefix}:reference_scope")
        if str(ref.get("source") or "") != "vision_roi_triggered_rapidocr":
            blockers.append(f"{prefix}:source")
        for key in ("frame_id", "roi_id"):
            if not str(ref.get(key) or "").strip():
                blockers.append(f"{prefix}:missing_{key}")
        ocr_refs = ref.get("ocr_refs") if isinstance(ref.get("ocr_refs"), dict) else {}
        if not str(ocr_refs.get("ocr_request_candidate_id") or "").strip():
            blockers.append(f"{prefix}:missing_ocr_request_candidate_id")
        if not str(ocr_refs.get("ocr_bridge_pack_ref") or "").strip():
            blockers.append(f"{prefix}:missing_bridge_pack_ref")
        if str(ocr_refs.get("ocr_provider") or "") != "rapidocr_candidate":
            blockers.append(f"{prefix}:ocr_provider")
        if ref.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fact_status")
        if ref.get("fusion_status") != "not_fused":
            blockers.append(f"{prefix}:fusion_status")
        if ref.get("ai_interpretation_status") != "not_invoked":
            blockers.append(f"{prefix}:ai_interpretation_status")
        forbidden = ref.get("forbidden_actions") if isinstance(ref.get("forbidden_actions"), dict) else {}
        for fk in FORBIDDEN_ACTION_KEYS:
            if forbidden.get(fk) is not True:
                blockers.append(f"{prefix}:forbidden_actions_{fk}")
        if ocr_refs.get("empty_text") is not True and empty_text_refs > 0:
            pass
        elif empty_text_refs == len(refs) and ocr_refs.get("empty_text") is not True:
            blockers.append(f"{prefix}:empty_text_should_be_true")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows and refs:
        blockers.append("matrix_empty")

    if cmp_doc.get("note") != "rapidocr_empty_text_is_valid_real_provider_result":
        blockers.append("comparison_note_missing")
    if cmp_doc.get("provider_changed_from_stub_to_rapidocr") is not True:
        blockers.append("provider_changed_from_stub_to_rapidocr_not_true")

    boundary = [
        ("cross_modal_fusion_invoked", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("rapidocr_invoked", False),
        ("paddleocr_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_rapidocr_reference_only_executed") is not True:
        blockers.append("audit:cross_modal_rapidocr_reference_only_executed")
    if aud.get("rapidocr_invoked_upstream") is not True:
        blockers.append("audit:rapidocr_invoked_upstream")
    if aud.get("real_provider_invoked_upstream") is not True:
        blockers.append("audit:real_provider_invoked_upstream")

    if empty_text_refs == matched and matched > 0:
        soft.append("all_references_empty_text_valid_real_provider")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif matched <= 0:
        verdict = "CONDITIONAL_GO"

    rep = {
        "schema": "cross_modal_vision_ocr_reference_only_rapidocr_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Reference-Only-002",
        "smoke_root": str(root),
        "verdict": verdict,
        "matched_reference_count": matched,
        "empty_text_reference_count": empty_text_refs,
        "input_roots": {
            "rapidocr_readonly_consumer_root": summary.get("rapidocr_readonly_consumer_root"),
            "stub_reference_root": summary.get("stub_reference_root"),
        },
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_vision_ocr_reference_only_rapidocr_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
