#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR TestBoard v0 closure."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


REQUIRED_CASE_TYPES = (
    "POSITIVE_TEXT_CLEAR",
    "EMPTY_TEXT_ROI",
    "NON_TEXT_ROI_REJECTED",
    "LOW_QUALITY_TEXT",
    "PARTIAL_TEXT",
    "MULTI_TEXT_LINES",
    "MIXED_CN_EN",
    "FALSE_POSITIVE_VISUAL_ROI",
    "DUPLICATE_TEXT_ROI",
    "CONFLICTING_TEXT_ROI",
)


def _find_ws_root() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "capabilities" / "midplatform").is_dir():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return here.parents[3]


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
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_v0_closure_summary.json",
        "coverage": root / "cross_modal_vision_ocr_testboard_v0_case_coverage_matrix.json",
        "risk": root / "cross_modal_vision_ocr_testboard_v0_risk_coverage_report.json",
        "rejection": root / "cross_modal_vision_ocr_testboard_v0_rejection_coverage_report.json",
        "full_chain": root / "cross_modal_vision_ocr_testboard_v0_full_chain_alignment_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix.json",
        "non_claims": root / "cross_modal_vision_ocr_testboard_v0_non_claims_report.json",
        "followups": root / "cross_modal_vision_ocr_testboard_v0_open_followups.json",
        "audit": root / "cross_modal_vision_ocr_testboard_v0_closure_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_v0_closure_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_v0_closure_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    coverage = _read_json(paths["coverage"])
    risk = _read_json(paths["risk"])
    rejection = _read_json(paths["rejection"])
    full_chain = _read_json(paths["full_chain"])
    non_claims = _read_json(paths["non_claims"])
    followups = _read_json(paths["followups"])
    boundary = _read_json(paths["boundary"])
    aud = _read_json(paths["audit"])

    if int(summary.get("case_count") or 0) != 10:
        blockers.append("case_count_not_10")
    if int(summary.get("executed_case_count") or 0) != 10:
        blockers.append("executed_case_count_not_10")
    if int(summary.get("planned_only_case_count") or 0) != 0:
        blockers.append("planned_only_case_count_not_0")
    if aud.get("all_cases_executed") is not True:
        blockers.append("audit_all_cases_executed_false")

    cov_rows = coverage.get("rows") if isinstance(coverage.get("rows"), list) else []
    if int(coverage.get("row_count") or len(cov_rows)) != 10:
        blockers.append("coverage_row_count_not_10")

    cov_types = {r.get("case_type") for r in cov_rows if isinstance(r, dict)}
    for ct in REQUIRED_CASE_TYPES:
        if ct not in cov_types:
            blockers.append(f"missing_case_type:{ct}")

    risk_flags = (
        "positive_text_case_covered",
        "empty_text_case_covered",
        "non_text_rejection_case_covered",
        "low_quality_text_case_covered",
        "partial_text_case_covered",
        "multi_line_text_case_covered",
        "mixed_language_text_case_covered",
        "false_positive_visual_roi_case_covered",
        "duplicate_text_case_covered",
        "conflicting_text_case_covered",
        "no_write_boundary_covered",
        "no_auto_approval_covered",
        "no_world_model_write_covered",
        "no_navigation_decision_covered",
    )
    for flag in risk_flags:
        if risk.get(flag) is not True:
            blockers.append(f"risk_{flag}_false")

    if rejection.get("non_text_roi_rejected_before_ocr") is not True:
        blockers.append("rejection_non_text_not_true")
    if rejection.get("ocr_request_generated_for_non_text") is not False:
        blockers.append("rejection_ocr_request_not_false")

    fc_status = full_chain.get("full_chain_10cases_runner_status")
    if fc_status == "aligned_10_cases":
        blockers.append("full_chain_10_falsely_claimed_generated")
    if fc_status != "not_generated_yet":
        blockers.append("full_chain_status_unexpected")

    claims = non_claims.get("claims") if isinstance(non_claims.get("claims"), dict) else {}
    if claims.get("scene_delta_may_write") is not False:
        blockers.append("non_claims_scene_delta_not_false")
    if claims.get("world_model_may_write") is not False:
        blockers.append("non_claims_world_model_not_false")
    if claims.get("usable_for_navigation_decisions") is not False:
        blockers.append("non_claims_navigation_not_false")

    items = followups.get("items") if isinstance(followups.get("items"), list) else []
    if len(items) < 5:
        blockers.append("followups_too_few")

    if boundary.get("boundary_all_ok") is not True:
        blockers.append("boundary_all_ok_false")

    for br in boundary.get("rows") or []:
        if not isinstance(br, dict):
            continue
        for k in (
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "scene_delta_executor_invoked",
            "navigation_decision_invoked",
            "auto_approve_invoked",
            "approval_granted",
        ):
            if br.get(k) is True:
                blockers.append(f"boundary_violation:{br.get('case_id')}:{k}")

    audit_checks = (
        ("cross_modal_vision_ocr_testboard_v0_closure_executed", True),
        ("evaluation_only", True),
        ("case_count", 10),
        ("executed_case_count", 10),
        ("planned_only_case_count", 0),
        ("all_cases_executed", True),
        ("no_write_boundary_verified", True),
        ("real_scene_delta_executor_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("auto_approve_invoked", False),
        ("approval_granted", False),
    )
    for key, expected in audit_checks:
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}_mismatch")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_v0_closure_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_v0_closure_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
