#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR evaluation chain closure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_WS = Path(__file__).resolve()
for _p in _WS.parents:
    if (_p / "capabilities" / "midplatform").is_dir():
        if str(_p) not in sys.path:
            sys.path.insert(0, str(_p))
        break

CRITICAL_PHASE_KEYS = (
    "Vision-ROI-to-OCR-Request-Bridge",
    "RapidOCR-Submission-From-Vision-ROI",
    "RapidOCR-ReadOnly-Consumer",
    "CrossModal-RapidOCR-Reference-Only",
    "Text-Bearing-OCR-Sample",
    "Fusion-Candidate-DryRun",
    "Review-Queue",
    "AI-Interpretation-DryRun",
    "Scene-Delta-Candidate-DryRun",
    "Gate-Evaluator-DryRun",
    "Executor-Trace-Stub",
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
        "summary": root / "cross_modal_vision_ocr_chain_closure_summary.json",
        "phase_matrix": root / "cross_modal_vision_ocr_phase_matrix.json",
        "lineage": root / "cross_modal_vision_ocr_lineage_matrix.json",
        "no_write": root / "cross_modal_vision_ocr_no_write_boundary_matrix.json",
        "capability": root / "cross_modal_vision_ocr_capability_closure_report.json",
        "non_claims": root / "cross_modal_vision_ocr_non_claims_report.json",
        "followups": root / "cross_modal_vision_ocr_open_followups.json",
        "audit": root / "cross_modal_vision_ocr_chain_closure_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_chain_closure_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-Evaluation-Chain-Closure-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_vision_ocr_chain_closure_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    phase_doc = _read_json(paths["phase_matrix"])
    lineage = _read_json(paths["lineage"])
    no_write = _read_json(paths["no_write"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    aud = _read_json(paths["audit"])

    input_roots = summary.get("input_roots") if isinstance(summary.get("input_roots"), dict) else {}
    for key in DEFAULT_CHAIN_ROOTS_KEYS():
        rp = Path(str(input_roots.get(key) or ""))
        if not rp.is_dir():
            blockers.append(f"input_root_missing:{key}")

    rows = phase_doc.get("rows") if isinstance(phase_doc.get("rows"), list) else []
    if len(rows) < 13:
        blockers.append("phase_matrix_incomplete")

    by_name = {r.get("phase_name"): r for r in rows if isinstance(r, dict)}
    for key in CRITICAL_PHASE_KEYS:
        row = by_name.get(key)
        if not row:
            blockers.append(f"critical_phase_missing:{key}")
            continue
        v = row.get("verifier_verdict")
        if v not in ("GO", "CONDITIONAL_GO"):
            blockers.append(f"critical_phase_not_go:{key}:{v}")

    primary = lineage.get("primary_lineage") if isinstance(lineage.get("primary_lineage"), dict) else {}
    if primary.get("final_execution_status") != "blocked_by_gate":
        blockers.append("lineage:final_execution_status_not_blocked_by_gate")
    if primary.get("final_fact_status") != "not_fact":
        blockers.append("lineage:final_fact_status_not_not_fact")

    if no_write.get("all_phases_boundary_ok") is not True:
        soft.append("no_write_boundary_not_all_phases_ok")

    final_closure = summary.get("final_closure") if isinstance(summary.get("final_closure"), dict) else {}
    if final_closure.get("final_write_status") != "no_write":
        blockers.append("final_closure:final_write_status_not_no_write")
    if final_closure.get("chain_status") != "closed_for_evaluation":
        blockers.append("final_closure:chain_status_not_closed")

    if non_claims.get("no_scene_delta_write") is not True:
        blockers.append("non_claims:no_scene_delta_write_not_true")
    if non_claims.get("no_world_model_write") is not True:
        blockers.append("non_claims:no_world_model_write_not_true")
    if non_claims.get("not_navigation_ready") is not True:
        blockers.append("non_claims:not_navigation_ready_not_true")
    if non_claims.get("not_cross_modal_fused_fact") is not True:
        blockers.append("non_claims:not_cross_modal_fused_fact_not_true")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 5:
        blockers.append("open_followups_insufficient")

    boundary = [
        ("scene_delta_executor_invoked", False),
        ("scene_delta_written", False),
        ("midplatform_fact_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("database_write_invoked", False),
        ("wal_append_invoked", False),
        ("auto_approve_invoked", False),
        ("approval_granted", False),
    ]
    for key, expected in boundary:
        if aud.get(key) is not expected:
            blockers.append(f"audit:{key}")

    if aud.get("cross_modal_vision_ocr_chain_closure_executed") is not True:
        blockers.append("audit:closure_not_executed")

    verdict = "GO"
    if blockers:
        verdict = "NO_GO"
    elif soft:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_chain_closure_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-Evaluation-Chain-Closure-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
    }
    _write_json(root / "cross_modal_vision_ocr_chain_closure_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


def DEFAULT_CHAIN_ROOTS_KEYS():
    from capabilities.midplatform.cross_modal_vision_ocr_chain_closure_v0 import DEFAULT_CHAIN_ROOTS

    return tuple(DEFAULT_CHAIN_ROOTS.keys())


if __name__ == "__main__":
    raise SystemExit(main())
