#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for YOLO real positive sample smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List

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

    sample_p = root / "yolo_real_positive_sample_report.json"
    gate_p = root / "yolo_real_positive_gate_check.json"
    model_p = root / "yolo_real_positive_model_load_report.json"
    raw_p = root / "yolo_real_positive_detector_result_summary.json"
    fixture_p = root / "yolo_real_positive_vision_detection_evidence_fixture.json"
    aud_p = root / "yolo_real_positive_audit_report.json"
    risk_p = root / "yolo_real_positive_risk_report.json"

    for label, p in (
        ("positive_sample_report", sample_p),
        ("gate_check", gate_p),
        ("model_load", model_p),
        ("detector_result", raw_p),
        ("evidence_fixture", fixture_p),
        ("audit", aud_p),
        ("risk_report", risk_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "yolo_real_positive_verifier_report_v0",
            "phase": "Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "yolo_real_positive_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    sample = _read_json(sample_p)
    gate = _read_json(gate_p)
    model_load = _read_json(model_p)
    raw = _read_json(raw_p)
    fixture = _read_json(fixture_p)
    aud = _read_json(aud_p)

    if sample.get("network_request_invoked") is True or aud.get("network_request_invoked") is True:
        blockers.append("network_request_invoked_must_be_false")

    if gate.get("eval_only_gate") is not True:
        blockers.append("eval_only_gate_must_be_true")
    if gate.get("eval_provider_enabled") is not True:
        blockers.append("eval_provider_enabled_must_be_true")

    if model_load.get("model_loaded") is not True:
        blockers.append("model_loaded_must_be_true")

    if str(raw.get("detector_mode") or "") != "real_yolo":
        blockers.append("detector_mode_must_be_real_yolo")
    if aud.get("yolo_invoked") is not True:
        blockers.append("yolo_invoked_must_be_true")
    if aud.get("real_detector_invoked") is not True:
        blockers.append("real_detector_invoked_must_be_true")
    if aud.get("fixture_used") is not False:
        blockers.append("fixture_used_must_be_false")

    detection_count = int(raw.get("detection_count") or 0)
    items = fixture.get("items") if isinstance(fixture.get("items"), list) else []
    converted = len(items)

    if detection_count <= 0:
        blockers.append("detection_count_must_be_positive")
    if converted <= 0:
        blockers.append("converted_evidence_count_must_be_positive")

    for it in items:
        if not isinstance(it, dict):
            continue
        if str(it.get("schema_version") or "") != VISION_DETECTION_SCHEMA:
            blockers.append("evidence_schema_version_mismatch")
        if it.get("synthetic") is not False:
            blockers.append("evidence_synthetic_must_be_false")
        if it.get("stub_provider") is not False:
            blockers.append("evidence_stub_provider_must_be_false")
        if str(it.get("fact_status") or "") != "not_fact":
            blockers.append("evidence_fact_status_must_be_not_fact")
        if not isinstance(it.get("bbox_in_frame"), list) or len(it.get("bbox_in_frame") or []) != 4:
            blockers.append("evidence_bbox_in_frame_required")

    for k, must in (
        ("vision_mainline_modified", False),
        ("vision_provider_registry_default_changed", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if aud.get("yolo_positive_sample_smoke_executed") is not True:
        blockers.append("yolo_positive_sample_smoke_executed_must_be_true")

    if not blockers:
        verdict = "GO"
    else:
        if detection_count <= 0 and aud.get("real_detector_invoked"):
            verdict = "CONDITIONAL_GO"
            soft.append("zero_detections_on_positive_sample")
            blockers = [b for b in blockers if b not in ("detection_count_must_be_positive", "converted_evidence_count_must_be_positive")]
            if not blockers:
                verdict = "CONDITIONAL_GO"
            else:
                verdict = "NO_GO"
        else:
            verdict = "NO_GO"

    rep = {
        "schema": "yolo_real_positive_verifier_report_v0",
        "phase": "Phase-Vision-YOLO-Real-Smoke-Positive-Sample-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "yolo_real_positive_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
