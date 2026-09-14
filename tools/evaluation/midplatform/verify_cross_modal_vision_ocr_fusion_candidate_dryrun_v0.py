#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR fusion candidate dry-run."""

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
    "claim_confirmed_fact",
)

RISK_FLAG_KEYS = (
    "ocr_text_not_fact",
    "vision_roi_not_fact",
    "spatial_association_not_semantic_truth",
    "fusion_candidate_not_confirmed",
    "no_ai_interpretation",
    "no_navigation_decision",
    "no_midplatform_fact_write",
    "no_scene_delta_write",
    "no_world_model_write",
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

    paths = {
        "candidates": root / "cross_modal_vision_ocr_fusion_candidates.json",
        "matrix": root / "cross_modal_vision_ocr_fusion_dryrun_matrix.json",
        "risk": root / "cross_modal_vision_ocr_fusion_risk_report.json",
        "chain": root / "cross_modal_vision_ocr_fusion_source_chain_summary.json",
        "audit": root / "cross_modal_vision_ocr_fusion_dryrun_audit_report.json",
        "summary": root / "cross_modal_vision_ocr_fusion_candidate_dryrun_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_fusion_dryrun_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_vision_ocr_fusion_dryrun_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(paths["candidates"])
    matrix = _read_json(paths["matrix"])
    risk = _read_json(paths["risk"])
    aud = _read_json(paths["audit"])
    summary = _read_json(paths["summary"])

    cands = cand_doc.get("candidates") if isinstance(cand_doc.get("candidates"), list) else []
    if not cands:
        blockers.append("fusion_candidates_empty")

    non_empty = 0
    for i, cand in enumerate(cands):
        if not isinstance(cand, dict):
            blockers.append(f"candidate_invalid:{i}")
            continue
        prefix = f"candidate[{i}]"
        if cand.get("candidate_scope") != "dry_run_only":
            blockers.append(f"{prefix}:candidate_scope_not_dry_run_only")
        ocr_ref = cand.get("ocr_reference") if isinstance(cand.get("ocr_reference"), dict) else {}
        text_joined = str(ocr_ref.get("text_joined") or "")
        if not text_joined.strip():
            soft.append(f"{prefix}:text_joined_empty")
        else:
            non_empty += 1
        hyp = cand.get("fusion_hypothesis") if isinstance(cand.get("fusion_hypothesis"), dict) else {}
        if not hyp:
            blockers.append(f"{prefix}:missing_fusion_hypothesis")
        if hyp.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fusion_hypothesis_fact_status_not_not_fact")
        if hyp.get("requires_review") is not True:
            blockers.append(f"{prefix}:requires_review_not_true")
        forbidden = cand.get("forbidden_actions") if isinstance(cand.get("forbidden_actions"), dict) else {}
        for key in FORBIDDEN_ACTION_KEYS:
            if forbidden.get(key) is not True:
                blockers.append(f"{prefix}:forbidden_actions_missing_{key}")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if not rows:
        blockers.append("dryrun_matrix_empty")
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            continue
        if row.get("dry_run_only") is not True:
            blockers.append(f"matrix_row[{i}]:dry_run_only_not_true")
        if row.get("fact_status") != "not_fact":
            blockers.append(f"matrix_row[{i}]:fact_status_not_not_fact")
        if row.get("requires_review") is not True:
            blockers.append(f"matrix_row[{i}]:requires_review_not_true")

    flags = risk.get("risk_flags") if isinstance(risk.get("risk_flags"), dict) else {}
    for key in RISK_FLAG_KEYS:
        if flags.get(key) is not True:
            blockers.append(f"risk_flags:{key}")

    boundary = [
        ("cross_modal_fusion_committed", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("rapidocr_invoked", False),
        ("paddleocr_invoked", False),
        ("yolo_invoked", False),
        ("vlm_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_fusion_candidate_dryrun_executed") is not True:
        blockers.append("audit:cross_modal_fusion_candidate_dryrun_executed")
    if aud.get("dry_run_only") is not True:
        blockers.append("audit:dry_run_only")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif non_empty <= 0:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_fusion_dryrun_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-DryRun-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "fusion_candidate_count": len(cands),
        "non_empty_text_candidate_count": non_empty,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_vision_ocr_fusion_dryrun_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
