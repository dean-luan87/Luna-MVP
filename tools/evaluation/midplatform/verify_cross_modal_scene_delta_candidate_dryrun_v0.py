#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Scene Delta candidate dry-run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_ACTION_KEYS = (
    "write_scene_delta",
    "write_midplatform_fact",
    "write_world_model",
    "invoke_navigation_decision",
    "auto_approve",
    "claim_confirmed_fact",
)

RISK_FLAG_KEYS = (
    "scene_delta_candidate_not_write",
    "fusion_candidate_not_fact",
    "ai_interpretation_not_fact",
    "ocr_text_not_fact",
    "spatial_association_not_semantic_truth",
    "gate_not_evaluated",
    "approval_not_granted",
    "no_scene_delta_write",
    "no_midplatform_fact_write",
    "no_world_model_write",
    "no_navigation_decision",
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
        "candidates": root / "cross_modal_scene_delta_candidates.json",
        "matrix": root / "cross_modal_scene_delta_mapping_matrix.json",
        "gate": root / "cross_modal_scene_delta_gate_stub.json",
        "risk": root / "cross_modal_scene_delta_risk_report.json",
        "chain": root / "cross_modal_scene_delta_source_chain_summary.json",
        "audit": root / "cross_modal_scene_delta_dryrun_audit_report.json",
        "summary": root / "cross_modal_scene_delta_candidate_dryrun_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_scene_delta_dryrun_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_scene_delta_dryrun_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(paths["candidates"])
    matrix = _read_json(paths["matrix"])
    gate = _read_json(paths["gate"])
    risk = _read_json(paths["risk"])
    aud = _read_json(paths["audit"])

    cands = cand_doc.get("candidates") if isinstance(cand_doc.get("candidates"), list) else []
    cand_count = int(cand_doc.get("candidate_count") or len(cands))

    if not cands:
        soft.append("candidate_count_zero")

    for i, cand in enumerate(cands):
        if not isinstance(cand, dict):
            blockers.append(f"candidate_invalid:{i}")
            continue
        prefix = f"candidate[{i}]"
        if cand.get("candidate_scope") != "dry_run_only":
            blockers.append(f"{prefix}:candidate_scope_not_dry_run_only")
        if cand.get("source_type") != "cross_modal_vision_ocr_fusion_candidate":
            blockers.append(f"{prefix}:source_type_mismatch")
        if not str(cand.get("scene_delta_candidate_type") or "").strip():
            blockers.append(f"{prefix}:missing_scene_delta_candidate_type")
        if cand.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fact_status_not_not_fact")
        if cand.get("write_allowed") is not False:
            blockers.append(f"{prefix}:write_allowed_not_false")
        if cand.get("requires_gate_approval") is not True:
            blockers.append(f"{prefix}:requires_gate_approval_not_true")
        if cand.get("gate_status") != "not_evaluated":
            blockers.append(f"{prefix}:gate_status_not_not_evaluated")
        if cand.get("approval_status") != "not_approved":
            blockers.append(f"{prefix}:approval_status_not_not_approved")
        if cand.get("review_status") != "pending_review":
            blockers.append(f"{prefix}:review_status_not_pending_review")
        forbidden = cand.get("forbidden_actions") if isinstance(cand.get("forbidden_actions"), dict) else {}
        for key in FORBIDDEN_ACTION_KEYS:
            if forbidden.get(key) is not True:
                blockers.append(f"{prefix}:forbidden_actions_missing_{key}")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if cand_count > 0 and not rows:
        blockers.append("mapping_matrix_empty")

    if gate.get("gate_required") is not True:
        blockers.append("gate:gate_required_not_true")
    if gate.get("gate_status") != "not_evaluated":
        blockers.append("gate:gate_status_not_not_evaluated")
    if gate.get("write_allowed") is not False:
        blockers.append("gate:write_allowed_not_false")

    flags = risk.get("risk_flags") if isinstance(risk.get("risk_flags"), dict) else {}
    for key in RISK_FLAG_KEYS:
        if flags.get(key) is not True:
            blockers.append(f"risk_flags:{key}")

    boundary = [
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("auto_approve_invoked", False),
        ("approval_granted", False),
        ("rapidocr_invoked", False),
        ("yolo_invoked", False),
        ("vlm_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_scene_delta_candidate_dryrun_executed") is not True:
        blockers.append("audit:cross_modal_scene_delta_candidate_dryrun_executed")
    if aud.get("dry_run_only") is not True:
        blockers.append("audit:dry_run_only")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif cand_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_scene_delta_dryrun_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Candidate-DryRun-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "candidate_count": cand_count,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_scene_delta_dryrun_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
