#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for gated real YOLO smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

VISION_DETECTION_SCHEMA = "vision_detection_evidence_v0"


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

    gate_p = root / "yolo_real_gate_check.json"
    sel_p = root / "yolo_real_input_unit_selection.json"
    fixture_p = root / "yolo_real_vision_detection_evidence_fixture.json"
    aud_p = root / "yolo_real_smoke_audit_report.json"
    risk_p = root / "yolo_real_smoke_risk_report.json"
    summary_p = root / "yolo_real_smoke_summary.json"

    for label, p in (
        ("gate_check", gate_p),
        ("input_selection", sel_p),
        ("evidence_fixture", fixture_p),
        ("audit", aud_p),
        ("risk_report", risk_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "yolo_real_smoke_verifier_report_v0",
            "phase": "Phase-Vision-Gated-YOLO-Real-Smoke-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "yolo_real_smoke_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    gate = _read_json(gate_p)
    selection = _read_json(sel_p)
    fixture = _read_json(fixture_p)
    aud = _read_json(aud_p)
    risk = _read_json(risk_p)
    summary = _read_json(summary_p) if summary_p.is_file() else {}

    if gate.get("eval_only_gate") is not True:
        blockers.append("eval_only_gate_must_be_true")
    if gate.get("eval_provider_enabled") is not True:
        blockers.append("eval_provider_enabled_must_be_true")
    if gate.get("network_download_attempted") is True or aud.get("network_request_invoked") is True:
        blockers.append("network_request_must_not_be_invoked")

    if int(selection.get("selected_units_count") or 0) <= 0:
        blockers.append("selected_units_count_must_be_positive")
    if selection.get("full_frame_direct_forbidden") is not True:
        blockers.append("full_frame_direct_forbidden_required")

    for rid in selection.get("selected_roi_ids") or []:
        if any(x in str(rid).lower() for x in ("full_frame", "whole_frame", "entire_frame")):
            blockers.append("must_not_use_full_frame_roi")

    items = fixture.get("items") if isinstance(fixture.get("items"), list) else []
    if not items:
        if aud.get("real_detector_invoked") is True and aud.get("yolo_invoked") is True:
            soft.append("zero_detections_after_real_yolo_inference_conditional_go")
        else:
            blockers.append("evidence_fixture_empty")

    real_invoked = aud.get("real_detector_invoked") is True
    fixture_used = aud.get("fixture_used") is True

    for it in items:
        if not isinstance(it, dict):
            continue
        if str(it.get("schema_version") or "") != VISION_DETECTION_SCHEMA:
            blockers.append("evidence_schema_version_mismatch")
        if str(it.get("fact_status") or "") != "not_fact":
            blockers.append("evidence_fact_status_must_be_not_fact")
        if real_invoked and it.get("synthetic") is True and not fixture_used:
            blockers.append("real_detector_synthetic_must_be_false")
        if fixture_used and aud.get("real_detector_invoked") is not True:
            if it.get("synthetic") is not True:
                soft.append("fixture_path_expected_synthetic_true")

    if risk.get("yolo_label_not_fact") is not True:
        blockers.append("risk_yolo_label_not_fact_required")
    if risk.get("no_navigation_decision") is not True and risk.get("detector_output_not_navigation_decision") is not True:
        blockers.append("risk_no_navigation_decision_required")

    for k, must in (
        ("vision_mainline_modified", False),
        ("vision_provider_registry_default_changed", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("supervision_mainline_invoked", False),
        ("vlm_invoked", False),
        ("ocr_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if aud.get("yolo_real_smoke_executed") is not True:
        blockers.append("yolo_real_smoke_executed_must_be_true")
    if aud.get("evaluation_only") is not True:
        blockers.append("evaluation_only_must_be_true")

    phase_hint = str(summary.get("phase_verdict_hint") or "")

    if not blockers:
        if real_invoked and not fixture_used and len(items) > 0:
            verdict = "GO"
        elif fixture_used:
            verdict = "CONDITIONAL_GO"
            soft.append("fixture_used_fallback")
        elif real_invoked and not fixture_used:
            verdict = "CONDITIONAL_GO"
        elif phase_hint == "CONDITIONAL_GO":
            verdict = "CONDITIONAL_GO"
        else:
            verdict = "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    if fixture_used and verdict == "GO":
        blockers.append("fixture_used_verdict_cannot_be_go")
        verdict = "NO_GO"

    rep = {
        "schema": "yolo_real_smoke_verifier_report_v0",
        "phase": "Phase-Vision-Gated-YOLO-Real-Smoke-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "yolo_real_smoke_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
