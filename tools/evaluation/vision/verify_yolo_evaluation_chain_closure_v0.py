#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for YOLO evaluation chain closure."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, List


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

    summary_p = root / "yolo_evaluation_chain_closure_summary.json"
    phase_p = root / "yolo_evaluation_phase_matrix.json"
    lineage_p = root / "yolo_evaluation_lineage_matrix.json"
    no_write_p = root / "yolo_evaluation_no_write_boundary_matrix.json"
    cap_p = root / "yolo_evaluation_capability_closure_report.json"
    non_p = root / "yolo_evaluation_non_claims_report.json"
    follow_p = root / "yolo_evaluation_open_followups.json"
    aud_p = root / "yolo_evaluation_chain_closure_audit_report.json"

    for label, p in (
        ("summary", summary_p),
        ("phase_matrix", phase_p),
        ("lineage", lineage_p),
        ("no_write", no_write_p),
        ("capability_closure", cap_p),
        ("non_claims", non_p),
        ("followups", follow_p),
        ("audit", aud_p),
    ):
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "yolo_evaluation_chain_closure_verifier_report_v0",
            "phase": "Phase-Vision-YOLO-Evaluation-Chain-Closure-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "yolo_evaluation_chain_closure_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(summary_p)
    phase_doc = _read_json(phase_p)
    lineage = _read_json(lineage_p)
    no_write = _read_json(no_write_p)
    non_claims = _read_json(non_p)
    aud = _read_json(aud_p)
    followups = _read_json(follow_p)

    input_roots = summary.get("input_roots") if isinstance(summary.get("input_roots"), dict) else {}
    for key in (
        "Gated-YOLO-Candidate-Adapter",
        "Gated-YOLO-Real-Smoke",
        "YOLO-Real-Smoke-Positive-Sample",
        "YOLO-Evidence-Pack-Integration-Stub",
        "YOLO-Evidence-Pack-ReadOnly-Consumer",
    ):
        rp = Path(str(input_roots.get(key) or ""))
        if not rp.is_dir():
            blockers.append(f"input_root_missing:{key}")

    rows = phase_doc.get("rows") if isinstance(phase_doc.get("rows"), list) else []
    if len(rows) < 5:
        blockers.append("phase_matrix_incomplete")

    expected = {
        "Gated-YOLO-Candidate-Adapter": "CONDITIONAL_GO",
        "Gated-YOLO-Real-Smoke": "CONDITIONAL_GO",
        "YOLO-Real-Smoke-Positive-Sample": "GO",
        "YOLO-Evidence-Pack-Integration-Stub": "GO",
        "YOLO-Evidence-Pack-ReadOnly-Consumer": "GO",
    }
    by_name = {str(r.get("phase_name")): r for r in rows if isinstance(r, dict)}
    for pname, exp in expected.items():
        row = by_name.get(pname)
        if not row:
            blockers.append(f"phase_missing:{pname}")
            continue
        if row.get("verifier_verdict") != exp:
            blockers.append(f"phase_verdict_mismatch:{pname}")

    if int(lineage.get("detection_count") or 0) <= 0:
        blockers.append("lineage_detection_count_not_positive")
    if int(lineage.get("evidence_count_observed") or 0) <= 0:
        blockers.append("lineage_evidence_count_observed_not_positive")

    if no_write.get("all_phases_boundary_ok") is not True:
        blockers.append("no_write_boundary_not_all_ok")

    if not isinstance(followups.get("items"), list) or len(followups.get("items") or []) < 1:
        blockers.append("open_followups_empty")

    if non_claims.get("not_mainline") is not True:
        blockers.append("non_claims_not_mainline_required")
    if non_claims.get("detections_not_fact") is not True:
        blockers.append("non_claims_not_fact_required")
    if non_claims.get("not_navigation_decision") is not True:
        blockers.append("non_claims_no_navigation_required")

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

    if aud.get("yolo_evaluation_chain_closure_executed") is not True:
        blockers.append("yolo_evaluation_chain_closure_executed_must_be_true")

    if not blockers:
        verdict = "GO" if not soft else "CONDITIONAL_GO"
    else:
        verdict = "NO_GO"

    rep = {
        "schema": "yolo_evaluation_chain_closure_verifier_report_v0",
        "phase": "Phase-Vision-YOLO-Evaluation-Chain-Closure-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "yolo_evaluation_chain_closure_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    if verdict == "NO_GO":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
