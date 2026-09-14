#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal fusion review queue."""

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
    "claim_confirmed_fact",
    "auto_approve",
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
        "candidates": root / "cross_modal_fusion_review_queue_candidates.json",
        "matrix": root / "cross_modal_fusion_review_queue_matrix.json",
        "risk": root / "cross_modal_fusion_review_risk_summary.json",
        "policy": root / "cross_modal_fusion_review_queue_policy_report.json",
        "audit": root / "cross_modal_fusion_review_queue_audit_report.json",
        "summary": root / "cross_modal_fusion_review_queue_summary.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_fusion_review_queue_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_fusion_review_queue_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    cand_doc = _read_json(paths["candidates"])
    matrix = _read_json(paths["matrix"])
    risk = _read_json(paths["risk"])
    policy = _read_json(paths["policy"])
    aud = _read_json(paths["audit"])
    summary = _read_json(paths["summary"])

    items = cand_doc.get("items") if isinstance(cand_doc.get("items"), list) else []
    queue_count = int(cand_doc.get("queue_item_count") or len(items))

    if queue_count <= 0:
        soft.append("queue_item_count_zero")
    if not items:
        blockers.append("review_queue_items_empty")

    for i, item in enumerate(items):
        if not isinstance(item, dict):
            blockers.append(f"item_invalid:{i}")
            continue
        prefix = f"item[{i}]"
        if item.get("queue_scope") != "review_queue_only":
            blockers.append(f"{prefix}:queue_scope_not_review_queue_only")
        if item.get("review_status") != "pending_review":
            blockers.append(f"{prefix}:review_status_not_pending_review")
        if item.get("approval_status") != "not_approved":
            blockers.append(f"{prefix}:approval_status_not_not_approved")
        if item.get("auto_approve_allowed") is not False:
            blockers.append(f"{prefix}:auto_approve_allowed_not_false")
        if item.get("fact_status") != "not_fact":
            blockers.append(f"{prefix}:fact_status_not_not_fact")
        forbidden = item.get("forbidden_actions") if isinstance(item.get("forbidden_actions"), dict) else {}
        for key in FORBIDDEN_ACTION_KEYS:
            if forbidden.get(key) is not True:
                blockers.append(f"{prefix}:forbidden_actions_missing_{key}")

    rows = matrix.get("rows") if isinstance(matrix.get("rows"), list) else []
    if queue_count > 0 and not rows:
        blockers.append("review_queue_matrix_empty")

    flags = risk.get("risk_flags") if isinstance(risk.get("risk_flags"), dict) else {}
    for key in RISK_FLAG_KEYS:
        if flags.get(key) is not True:
            blockers.append(f"risk_flags:{key}")

    if policy.get("all_candidates_pending_review") is not True and queue_count > 0:
        blockers.append("policy:all_candidates_pending_review_not_true")
    if policy.get("auto_approve_allowed") is not False:
        blockers.append("policy:auto_approve_allowed_not_false")
    if policy.get("write_actions_forbidden") is not True:
        blockers.append("policy:write_actions_forbidden_not_true")

    boundary = [
        ("auto_approve_invoked", False),
        ("approval_granted", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("ai_interpretation_invoked", False),
        ("navigation_decision_invoked", False),
        ("cross_modal_fusion_committed", False),
        ("rapidocr_invoked", False),
        ("yolo_invoked", False),
        ("vlm_invoked", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_fusion_review_queue_generated") is not True:
        blockers.append("audit:cross_modal_fusion_review_queue_generated")
    if aud.get("review_queue_only") is not True:
        blockers.append("audit:review_queue_only")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif queue_count <= 0:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_fusion_review_queue_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Fusion-Candidate-Review-Queue-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "queue_item_count": queue_count,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_fusion_review_queue_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
