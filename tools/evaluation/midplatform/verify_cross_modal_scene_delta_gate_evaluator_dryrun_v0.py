#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Scene Delta gate evaluator dry-run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_REASON_CODES = (
    "candidate_not_fact",
    "gate_dryrun_only",
    "ai_interpretation_not_fact",
    "ocr_text_not_fact",
    "spatial_association_not_semantic_truth",
    "review_required_before_write",
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
        "result": root / "cross_modal_scene_delta_gate_evaluation_result.json",
        "reason_matrix": root / "cross_modal_scene_delta_gate_reason_matrix.json",
        "policy": root / "cross_modal_scene_delta_gate_policy_report.json",
        "chain": root / "cross_modal_scene_delta_gate_source_chain_summary.json",
        "audit": root / "cross_modal_scene_delta_gate_evaluator_audit_report.json",
        "summary": root / "cross_modal_scene_delta_gate_evaluation_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_scene_delta_gate_evaluator_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_scene_delta_gate_evaluator_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    result_doc = _read_json(paths["result"])
    reason_matrix = _read_json(paths["reason_matrix"])
    policy = _read_json(paths["policy"])
    aud = _read_json(paths["audit"])

    results = result_doc.get("results") if isinstance(result_doc.get("results"), list) else []
    eval_count = int(result_doc.get("evaluation_count") or len(results))

    if not results:
        soft.append("evaluation_count_zero")

    for i, res in enumerate(results):
        if not isinstance(res, dict):
            blockers.append(f"result_invalid:{i}")
            continue
        prefix = f"result[{i}]"
        if res.get("evaluation_scope") != "dry_run_only":
            blockers.append(f"{prefix}:evaluation_scope_not_dry_run_only")
        if res.get("gate_status") != "evaluated_dry_run":
            blockers.append(f"{prefix}:gate_status_not_evaluated_dry_run")
        if res.get("write_allowed") is not False:
            blockers.append(f"{prefix}:write_allowed_not_false")
        if res.get("approval_granted") is not False:
            blockers.append(f"{prefix}:approval_granted_not_false")
        if res.get("decision") != "hold_for_review":
            blockers.append(f"{prefix}:decision_not_hold_for_review")
        if res.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fact_status_not_not_fact")

    rows = reason_matrix.get("rows") if isinstance(reason_matrix.get("rows"), list) else []
    if eval_count > 0 and not rows:
        blockers.append("reason_matrix_empty")

    seen_codes = {str(r.get("reason_code") or "") for r in rows if isinstance(r, dict)}
    for code in REQUIRED_REASON_CODES:
        if code not in seen_codes:
            blockers.append(f"reason_matrix:missing_{code}")

    if policy.get("auto_approve_allowed") is not False:
        blockers.append("policy:auto_approve_allowed_not_false")
    if policy.get("scene_delta_executor_must_not_run") is not True:
        blockers.append("policy:scene_delta_executor_must_not_run_not_true")
    if eval_count > 0 and policy.get("gate_evaluated") is not True:
        blockers.append("policy:gate_evaluated_not_true")

    boundary = [
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("ai_interpretation_invoked", False),
        ("rapidocr_invoked", False),
        ("yolo_invoked", False),
        ("vlm_invoked", False),
        ("approval_granted", False),
        ("write_allowed", False),
        ("auto_approve_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_scene_delta_gate_evaluator_dryrun_executed") is not True:
        blockers.append("audit:cross_modal_scene_delta_gate_evaluator_dryrun_executed")
    if aud.get("gate_evaluated") is not True:
        blockers.append("audit:gate_evaluated")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif eval_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_scene_delta_gate_evaluator_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Scene-Delta-Gate-Evaluator-DryRun-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "evaluation_count": eval_count,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_scene_delta_gate_evaluator_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
