#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for VisionDetectionEvidence schema alignment smoke."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

SCHEMA_VERSION = "vision_detection_evidence_v0"


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


def _mapping_has(rows: List[Any], supervision_field: str) -> bool:
    for row in rows:
        if not isinstance(row, dict):
            continue
        if str(row.get("supervision_field") or "") == supervision_field:
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []
    soft: List[str] = []

    schema_p = root / "vision_detection_evidence_schema_v0.json"
    ex_p = root / "vision_detection_evidence_schema_example.json"
    fix_p = root / "vision_detection_evidence_stub_compat_fixture.json"
    map_p = root / "vision_detection_evidence_supervision_mapping_matrix.json"
    bnd_p = root / "vision_detection_evidence_boundary_report.json"
    aud_p = root / "vision_detection_evidence_schema_alignment_audit_report.json"

    for label, p in (
        ("schema", schema_p),
        ("schema_example", ex_p),
        ("stub_compat_fixture", fix_p),
        ("supervision_mapping", map_p),
        ("boundary_report", bnd_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    verdict = "NO_GO"
    if blockers:
        rep = {
            "schema": "vision_detection_evidence_schema_alignment_verifier_report_v0",
            "phase": "Phase-VisionDetectionEvidence-Schema-Alignment-001",
            "smoke_root": str(root),
            "verdict": verdict,
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "vision_detection_evidence_schema_alignment_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
        return 2

    schema = _read_json(schema_p)
    example = _read_json(ex_p)
    fixture = _read_json(fix_p)
    mapping = _read_json(map_p)
    boundary = _read_json(bnd_p)
    aud = _read_json(aud_p)

    if str(schema.get("schema_version") or example.get("schema_version") or "") != SCHEMA_VERSION:
        blockers.append("schema_version_mismatch")

    required = schema.get("required_fields") if isinstance(schema.get("required_fields"), list) else []
    for fname in (
        "source_frame_id",
        "roi_id",
        "unit_id",
        "provider",
        "label",
        "confidence",
        "bbox_in_frame",
        "fact_status",
    ):
        if fname not in required:
            blockers.append(f"required_fields_missing:{fname}")

    rows = mapping.get("rows") if isinstance(mapping.get("rows"), list) else []
    if not rows:
        blockers.append("mapping_matrix_empty")
    for sf in ("xyxy", "confidence", "class_id", "tracker_id"):
        if not _mapping_has(rows, sf):
            blockers.append(f"mapping_missing:{sf}")

    items = fixture.get("items") if isinstance(fixture.get("items"), list) else []
    if not items:
        blockers.append("stub_compat_fixture_empty")
    for it in items:
        if not isinstance(it, dict):
            continue
        if it.get("synthetic") is not True:
            blockers.append("fixture_synthetic_must_be_true")
        if str(it.get("fact_status") or "") != "not_fact":
            blockers.append("fixture_fact_status_must_be_not_fact")
        if str(it.get("label") or "") == "confirmed_object":
            blockers.append("fixture_label_must_not_be_confirmed_object")

    if boundary.get("label_not_fact") is not True:
        blockers.append("boundary_label_not_fact_required")
    if boundary.get("tracker_id_not_identity") is not True:
        blockers.append("boundary_tracker_id_not_identity_required")
    if boundary.get("no_navigation_decision") is not True:
        blockers.append("boundary_no_navigation_decision_required")

    for k, must in (
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

    if aud.get("vision_detection_schema_alignment_executed") is not True:
        blockers.append("vision_detection_schema_alignment_executed_must_be_true")

    gaps = mapping.get("gaps") if isinstance(mapping.get("gaps"), list) else []
    if gaps and not blockers:
        soft.extend([f"mapping_gap:{g}" for g in gaps])

    if not blockers:
        verdict = "GO" if not soft else "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "vision_detection_evidence_schema_alignment_verifier_report_v0",
        "phase": "Phase-VisionDetectionEvidence-Schema-Alignment-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "vision_detection_evidence_schema_alignment_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
