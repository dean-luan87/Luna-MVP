#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for gated YOLO candidate adapter eval smoke."""

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

    probe_p = root / "yolo_availability_probe.json"
    sel_p = root / "yolo_input_unit_selection.json"
    fixture_p = root / "yolo_vision_detection_evidence_fixture.json"
    report_p = root / "yolo_candidate_adapter_report.json"
    risk_p = root / "yolo_candidate_adapter_risk_report.json"
    aud_p = root / "yolo_candidate_adapter_audit_report.json"

    for label, p in (
        ("availability_probe", probe_p),
        ("input_unit_selection", sel_p),
        ("evidence_fixture", fixture_p),
        ("adapter_report", report_p),
        ("risk_report", risk_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "yolo_candidate_adapter_verifier_report_v0",
            "phase": "Phase-Vision-Gated-YOLO-Candidate-Adapter-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "yolo_candidate_adapter_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    probe = _read_json(probe_p)
    selection = _read_json(sel_p)
    fixture = _read_json(fixture_p)
    report = _read_json(report_p)
    risk = _read_json(risk_p)
    aud = _read_json(aud_p)

    if int(selection.get("selected_units_count") or 0) <= 0:
        blockers.append("selected_units_count_must_be_positive")

    if selection.get("full_frame_direct_forbidden") is not True:
        blockers.append("full_frame_direct_forbidden_must_be_true")

    selected_roi_ids = selection.get("selected_roi_ids") if isinstance(selection.get("selected_roi_ids"), list) else []
    for rid in selected_roi_ids:
        rls = str(rid).lower()
        if any(x in rls for x in ("full_frame", "whole_frame", "entire_frame")):
            blockers.append("must_not_use_full_frame_roi")

    items = fixture.get("items") if isinstance(fixture.get("items"), list) else []
    if not items:
        blockers.append("evidence_fixture_empty")

    for it in items:
        if not isinstance(it, dict):
            continue
        if str(it.get("schema_version") or "") != VISION_DETECTION_SCHEMA:
            blockers.append("evidence_schema_version_mismatch")
        if str(it.get("fact_status") or "") != "not_fact":
            blockers.append("evidence_fact_status_must_be_not_fact")
        if str(it.get("label") or "") in ("confirmed_object", "confirmed_fact"):
            blockers.append("evidence_label_must_not_be_confirmed")
        if not it.get("source_frame_id"):
            blockers.append("evidence_missing_source_frame_id")
        if not it.get("roi_id") and not it.get("unit_id"):
            blockers.append("evidence_missing_roi_or_unit_id")
        if not isinstance(it.get("bbox_in_frame"), list) or len(it.get("bbox_in_frame") or []) != 4:
            blockers.append("evidence_missing_bbox_in_frame")

    if not report.get("detector_mode"):
        blockers.append("adapter_report_detector_mode_missing")

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

    if aud.get("yolo_candidate_adapter_eval_executed") is not True:
        blockers.append("yolo_candidate_adapter_eval_executed_must_be_true")
    if aud.get("evaluation_only") is not True:
        blockers.append("evaluation_only_must_be_true")

    summary_p = root / "yolo_candidate_adapter_eval_summary.json"
    if summary_p.is_file():
        summ = _read_json(summary_p)
        if summ.get("phase_verdict_hint") == "CONDITIONAL_GO" and not blockers:
            soft.append("phase_conditional_go_yolo_fixture_or_gate")

    if probe.get("ultralytics_installed") is not True and not blockers:
        soft.append("ultralytics_not_installed_fixture_path_expected")

    if not blockers:
        verdict = "GO" if not soft else "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "yolo_candidate_adapter_verifier_report_v0",
        "phase": "Phase-Vision-Gated-YOLO-Candidate-Adapter-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "yolo_candidate_adapter_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
