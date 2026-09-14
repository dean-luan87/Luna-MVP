#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal AI interpretation dry-run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

FORBIDDEN_ACTION_KEYS = (
    "write_midplatform_fact",
    "write_scene_delta",
    "write_world_model",
    "invoke_navigation_decision",
    "auto_approve",
    "claim_confirmed_fact",
)

RISK_FLAG_KEYS = (
    "ai_interpretation_not_fact",
    "template_interpretation_not_llm_truth",
    "ocr_text_not_fact",
    "visual_roi_not_fact",
    "fusion_candidate_not_confirmed",
    "no_auto_approval",
    "no_midplatform_fact_write",
    "no_scene_delta_write",
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
        "candidates": root / "cross_modal_ai_interpretation_candidates.json",
        "matrix": root / "cross_modal_ai_interpretation_matrix.json",
        "risk": root / "cross_modal_ai_interpretation_risk_report.json",
        "policy": root / "cross_modal_ai_interpretation_policy_report.json",
        "audit": root / "cross_modal_ai_interpretation_dryrun_audit_report.json",
        "summary": root / "cross_modal_ai_interpretation_dryrun_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_ai_interpretation_dryrun_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_ai_interpretation_dryrun_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(paths["candidates"])
    matrix = _read_json(paths["matrix"])
    risk = _read_json(paths["risk"])
    policy = _read_json(paths["policy"])
    aud = _read_json(paths["audit"])

    interps = cand_doc.get("interpretations") if isinstance(cand_doc.get("interpretations"), list) else []
    interp_count = int(cand_doc.get("interpretation_count") or len(interps))

    if not interps:
        soft.append("interpretation_count_zero")

    for i, interp in enumerate(interps):
        if not isinstance(interp, dict):
            blockers.append(f"interpretation_invalid:{i}")
            continue
        prefix = f"interpretation[{i}]"
        if interp.get("interpretation_scope") != "dry_run_only":
            blockers.append(f"{prefix}:interpretation_scope_not_dry_run_only")
        if interp.get("interpretation_mode") != "template_stub":
            blockers.append(f"{prefix}:interpretation_mode_not_template_stub")
        if interp.get("approval_status") != "not_approved":
            blockers.append(f"{prefix}:approval_status_not_not_approved")
        if interp.get("review_status") != "pending_review":
            blockers.append(f"{prefix}:review_status_not_pending_review")
        body = interp.get("interpretation_candidate") if isinstance(interp.get("interpretation_candidate"), dict) else {}
        if body.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fact_status_not_not_fact")
        if body.get("requires_review") is not True:
            blockers.append(f"{prefix}:requires_review_not_true")
        forbidden = interp.get("forbidden_actions") if isinstance(interp.get("forbidden_actions"), dict) else {}
        for key in FORBIDDEN_ACTION_KEYS:
            if forbidden.get(key) is not True:
                blockers.append(f"{prefix}:forbidden_actions_missing_{key}")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if interp_count > 0 and not rows:
        blockers.append("interpretation_matrix_empty")

    flags = risk.get("risk_flags") if isinstance(risk.get("risk_flags"), dict) else {}
    for key in RISK_FLAG_KEYS:
        if flags.get(key) is not True:
            blockers.append(f"risk_flags:{key}")

    if policy.get("auto_approve_allowed") is not False:
        blockers.append("policy:auto_approve_allowed_not_false")
    if policy.get("approval_status_unchanged") is not True:
        blockers.append("policy:approval_status_unchanged_not_true")
    if policy.get("external_llm_invoked") is not False:
        blockers.append("policy:external_llm_invoked_not_false")
    if interp_count > 0 and policy.get("all_interpretations_dry_run_only") is not True:
        blockers.append("policy:all_interpretations_dry_run_only_not_true")

    boundary = [
        ("external_llm_invoked", False),
        ("online_ai_invoked", False),
        ("approval_granted", False),
        ("auto_approve_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("rapidocr_invoked", False),
        ("yolo_invoked", False),
        ("vlm_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_ai_interpretation_dryrun_executed") is not True:
        blockers.append("audit:cross_modal_ai_interpretation_dryrun_executed")
    if aud.get("interpretation_mode") != "template_stub":
        blockers.append("audit:interpretation_mode_not_template_stub")
    if aud.get("ai_interpretation_committed") is not False:
        blockers.append("audit:ai_interpretation_committed_not_false")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif interp_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_ai_interpretation_dryrun_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-AI-Interpretation-DryRun-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "interpretation_count": interp_count,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_ai_interpretation_dryrun_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
