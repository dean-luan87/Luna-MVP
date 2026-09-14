#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Vision ROI text-bearing OCR sample."""

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

    paths = {
        "sample_report": root / "vision_roi_text_bearing_sample_report.json",
        "ocr_candidate": root / "vision_roi_text_bearing_ocr_request_candidate.json",
        "submission": root / "vision_roi_text_bearing_rapidocr_submission_result.json",
        "consumer": root / "vision_roi_text_bearing_rapidocr_consumer_view.json",
        "reference": root / "vision_roi_text_bearing_cross_modal_reference_candidate.json",
        "audit": root / "vision_roi_text_bearing_ocr_sample_audit_report.json",
        "summary": root / "vision_roi_text_bearing_ocr_sample_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "vision_roi_text_bearing_ocr_sample_verifier_report_v0",
            "phase": "Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "vision_roi_text_bearing_ocr_sample_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    sample = _read_json(paths["sample_report"])
    cand = _read_json(paths["ocr_candidate"])
    sub = _read_json(paths["submission"])
    consumer = _read_json(paths["consumer"])
    ref = _read_json(paths["reference"])
    aud = _read_json(paths["audit"])

    if sample.get("network_request_invoked") is not False:
        blockers.append("sample:network_request_invoked_not_false")
    if sample.get("source_type") != "text_bearing_fixture":
        blockers.append("sample:source_type_not_text_bearing_fixture")
    if sample.get("roi_type") != "upper_sign_roi":
        blockers.append("sample:roi_type_not_upper_sign_roi")

    ocr_req = cand.get("ocr_request") if isinstance(cand.get("ocr_request"), dict) else {}
    if cand.get("candidate_status") != "not_submitted":
        blockers.append("ocr_candidate:candidate_status_not_not_submitted")
    if ocr_req.get("input_type") != "roi":
        blockers.append("ocr_candidate:input_type_not_roi")
    if ocr_req.get("allow_full_image") is not False:
        blockers.append("ocr_candidate:allow_full_image_not_false")
    if ocr_req.get("expected_output") != "ocr_evidence":
        blockers.append("ocr_candidate:expected_output_not_ocr_evidence")

    if not str(sub.get("ocr_bridge_status") or "").strip():
        blockers.append("submission:ocr_bridge_not_invoked")
    if sub.get("direct_rapidocr_invoked") is True:
        blockers.append("submission:direct_rapidocr_invoked_true")
    if str(sub.get("selected_provider") or "") != "rapidocr_candidate":
        if "rapidocr" not in str(sub.get("selected_provider") or "").lower():
            blockers.append("submission:selected_provider_not_rapidocr")
    if sub.get("real_provider_invoked") is not True:
        blockers.append("submission:real_provider_invoked_not_true")
    if sub.get("rapidocr_invoked") is not True:
        blockers.append("submission:rapidocr_invoked_not_true")
    if sub.get("paddleocr_invoked") is True:
        blockers.append("submission:paddleocr_invoked_true")
    if sub.get("fallback_to_stub") is True:
        blockers.append("submission:fallback_to_stub_true")

    text_joined = str(sub.get("text_joined") or sub.get("evidence_text_joined") or "")
    empty_text = not text_joined.strip()
    if empty_text:
        soft.append("text_joined_empty")

    if consumer.get("fact_status") != "not_fact":
        blockers.append("consumer:fact_status_not_not_fact")
    if consumer.get("fusion_status") != "not_fused":
        blockers.append("consumer:fusion_status_not_not_fused")

    if not paths["reference"].is_file():
        blockers.append("missing:reference_candidate")
    if ref.get("fact_status") != "not_fact":
        blockers.append("reference:fact_status_not_not_fact")
    if ref.get("fusion_status") != "not_fused":
        blockers.append("reference:fusion_status_not_not_fused")
    if ref.get("ai_interpretation_status") != "not_invoked":
        blockers.append("reference:ai_interpretation_status_not_not_invoked")

    boundary = [
        ("direct_rapidocr_invoked", False),
        ("paddleocr_invoked", False),
        ("cross_modal_fusion_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("text_bearing_ocr_sample_executed") is not True:
        blockers.append("audit:text_bearing_ocr_sample_executed")
    if aud.get("eval_only") is not True:
        soft.append("audit:eval_only_not_true")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif empty_text or sub.get("fallback_to_stub"):
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "vision_roi_text_bearing_ocr_sample_verifier_report_v0",
        "phase": "Phase-Vision-ROI-Text-Bearing-Sample-For-OCR-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "text_joined": text_joined,
        "empty_text": empty_text,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_roi_text_bearing_ocr_sample_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
