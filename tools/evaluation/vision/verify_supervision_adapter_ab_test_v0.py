#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Supervision adapter A/B test smoke."""

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

    summary_p = root / "supervision_adapter_ab_test_summary.json"
    input_p = root / "supervision_adapter_ab_input_summary.json"
    fixture_p = root / "supervision_synthetic_to_vision_detection_fixture.json"
    matrix_p = root / "supervision_adapter_ab_comparison_matrix.json"
    score_p = root / "supervision_adapter_structure_score_report.json"
    risk_p = root / "supervision_adapter_ab_risk_report.json"
    aud_p = root / "supervision_adapter_ab_audit_report.json"

    for label, p in (
        ("summary", summary_p),
        ("input_summary", input_p),
        ("fixture", fixture_p),
        ("comparison_matrix", matrix_p),
        ("structure_score", score_p),
        ("risk_report", risk_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "supervision_adapter_ab_verifier_report_v0",
            "phase": "Phase-Vision-Supervision-Adapter-AB-Test-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "supervision_adapter_ab_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(summary_p)
    inp = _read_json(input_p)
    fixture = _read_json(fixture_p)
    matrix = _read_json(matrix_p)
    score = _read_json(score_p)
    risk = _read_json(risk_p)
    aud = _read_json(aud_p)

    for root_key in (
        "supervision_structure_reference_root",
        "vision_detection_schema_alignment_root",
        "rule_stub_roi_root",
        "external_supervision_experiment_root",
    ):
        rp = Path(str(inp.get(root_key) or summary.get(root_key) or ""))
        if not rp.is_dir():
            blockers.append(f"input_root_missing:{root_key}")

    if inp.get("supervision_installed") is not True:
        blockers.append("supervision_installed_must_be_true")

    if str(inp.get("vision_detection_schema_version") or summary.get("vision_detection_schema_version") or "") != VISION_DETECTION_SCHEMA:
        blockers.append("vision_detection_schema_version_mismatch")

    if int(inp.get("rule_stub_roi_items_count") or summary.get("rule_stub_roi_count") or 0) <= 0:
        blockers.append("rule_stub_roi_count_must_be_positive")

    if int(inp.get("supervision_roi_items_count") or summary.get("supervision_roi_count") or 0) <= 0:
        blockers.append("supervision_roi_count_must_be_positive")

    items = fixture.get("items") if isinstance(fixture.get("items"), list) else []
    if not items:
        blockers.append("supervision_fixture_empty")
    for it in items:
        if not isinstance(it, dict):
            continue
        if it.get("synthetic") is not True:
            blockers.append("fixture_synthetic_must_be_true")
        if str(it.get("fact_status") or "") != "not_fact":
            blockers.append("fixture_fact_status_must_be_not_fact")
        if str(it.get("provider") or "") != "supervision_synthetic_adapter":
            blockers.append("fixture_provider_must_be_supervision_synthetic_adapter")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows:
        blockers.append("comparison_matrix_empty")

    if not score.get("recommendation"):
        blockers.append("structure_score_recommendation_missing")
    for arm_key in ("rule_stub", "supervision_synthetic"):
        arm = score.get(arm_key) if isinstance(score.get(arm_key), dict) else {}
        for sk in ("schema_fit_score", "coordinate_fit_score", "lineage_fit_score", "governance_fit_score"):
            if sk not in arm:
                soft.append(f"score_optional_missing:{arm_key}.{sk}")

    if risk.get("not_luna_core") is not True:
        blockers.append("risk_not_luna_core_required")
    if risk.get("no_midplatform_fact_write") is not True:
        blockers.append("risk_no_midplatform_fact_write_required")
    if risk.get("no_navigation_decision") is not True:
        blockers.append("risk_no_navigation_decision_required")

    for k, must in (
        ("supervision_mainline_invoked", False),
        ("yolo_invoked", False),
        ("real_detector_invoked", False),
        ("navigation_decision_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("vlm_invoked", False),
        ("ocr_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if aud.get("supervision_ab_test_executed") is not True:
        blockers.append("supervision_ab_test_executed_must_be_true")

    if not blockers:
        verdict = "GO" if not soft else "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "supervision_adapter_ab_verifier_report_v0",
        "phase": "Phase-Vision-Supervision-Adapter-AB-Test-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "supervision_adapter_ab_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
