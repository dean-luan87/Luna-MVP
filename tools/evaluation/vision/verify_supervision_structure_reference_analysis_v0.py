#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for Supervision structure reference analysis smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_RISK_CLAIMS = (
    "supervision replaces luna core",
    "production mainline default",
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


def _mapping_has_target(rows: List[Any], needle: str) -> bool:
    for row in rows:
        if not isinstance(row, dict):
            continue
        target = str(row.get("luna_target") or "")
        concept = str(row.get("supervision_concept") or "")
        if needle in target or needle in concept:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    ap.add_argument(
        "--supervision-experiment-root",
        default="",
        help="Original experiment root to verify exists",
    )
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    sum_p = root / "supervision_structure_reference_summary.json"
    cap_p = root / "supervision_capability_structure_report.json"
    map_p = root / "supervision_to_luna_mapping_matrix.json"
    reuse_p = root / "supervision_reuse_classification_report.json"
    risk_p = root / "supervision_architecture_risk_report.json"
    ab_p = root / "supervision_ab_test_plan.json"
    aud_p = root / "supervision_structure_reference_audit.json"

    for label, p in (
        ("summary", sum_p),
        ("capability_report", cap_p),
        ("mapping_matrix", map_p),
        ("reuse_classification", reuse_p),
        ("architecture_risk", risk_p),
        ("ab_test_plan", ab_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "supervision_structure_reference_verifier_report_v0",
            "phase": "Phase-Vision-Supervision-Structure-Reference-Analysis-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "supervision_structure_reference_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(sum_p)
    cap = _read_json(cap_p)
    mapping = _read_json(map_p)
    reuse = _read_json(reuse_p)
    risk = _read_json(risk_p)
    ab = _read_json(ab_p)
    aud = _read_json(aud_p)

    exp_root_s = str(summary.get("supervision_experiment_root") or args.supervision_experiment_root or "").strip()
    if exp_root_s and not Path(exp_root_s).is_dir():
        blockers.append("supervision_experiment_root_missing")
    elif not exp_root_s:
        blockers.append("supervision_experiment_root_not_recorded")

    if cap.get("supervision_installed") is not True:
        blockers.append("supervision_installed_must_be_true")
    if not str(cap.get("supervision_version") or "").strip():
        blockers.append("supervision_version_missing")

    rows = mapping.get("rows") if isinstance(mapping.get("rows"), list) else []
    if not rows:
        blockers.append("mapping_matrix_empty")
    if not _mapping_has_target(rows, "VisionDetectionEvidence"):
        blockers.append("mapping_missing_detections_to_vision_detection_evidence")
    if not _mapping_has_target(rows, "VisionTrackingEvidence"):
        blockers.append("mapping_missing_tracker_to_vision_tracking_evidence")
    if not _mapping_has_target(rows, "VisionZoneEvidence"):
        blockers.append("mapping_missing_zone_to_vision_zone_evidence")

    items = reuse.get("items") if isinstance(reuse.get("items"), list) else []
    if len(items) < 3:
        blockers.append("reuse_classification_insufficient")

    if risk.get("supervision_must_not_replace_luna_core") is not True:
        blockers.append("risk_must_state_supervision_must_not_replace_luna_core")
    if risk.get("must_not_write_midplatform_fact") is not True:
        blockers.append("risk_must_not_write_midplatform_fact")
    if risk.get("must_not_invoke_navigation_decision") is not True:
        blockers.append("risk_must_not_invoke_navigation_decision")

    narr = risk.get("narrative") if isinstance(risk.get("narrative"), list) else []
    joined = " ".join(str(x).lower() for x in narr)
    for bad in FORBIDDEN_RISK_CLAIMS:
        if bad in joined:
            blockers.append(f"risk_narrative_forbidden_phrase:{bad}")

    variants = ab.get("variants") if isinstance(ab.get("variants"), list) else []
    metrics = ab.get("metrics") if isinstance(ab.get("metrics"), list) else []
    if not variants or not metrics:
        blockers.append("ab_test_plan_incomplete")

    for k, must in (
        ("supervision_analysis_executed", True),
        ("supervision_mainline_invoked", False),
        ("yolo_invoked", False),
        ("real_detector_invoked", False),
        ("navigation_decision_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
    ):
        if aud.get(k) is not must:
            blockers.append(f"audit:{k}")

    if summary.get("errors"):
        blockers.append("summary_errors_non_empty")

    if not blockers:
        verdict = "GO"
        zla = cap.get("zone_line_annotation")
        if isinstance(zla, dict) and not zla.get("byte_track_available"):
            soft.append("byte_track_not_confirmed_extended_probe")
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "supervision_structure_reference_verifier_report_v0",
        "phase": "Phase-Vision-Supervision-Structure-Reference-Analysis-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "supervision_version": cap.get("supervision_version"),
    }
    _write_json(root / "supervision_structure_reference_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
