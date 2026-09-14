#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for CrossModal Vision OCR TestBoard full-chain case runner."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

REQUIRED_EXECUTED_CASES = (
    "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
    "CM_VOCR_002_EMPTY_TEXT_ROI",
    "CM_VOCR_006_MULTI_TEXT_LINES",
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
    soft: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_full_chain_run_summary.json",
        "run_plan": root / "cross_modal_vision_ocr_testboard_full_chain_run_plan.json",
        "case_run": root / "cross_modal_vision_ocr_testboard_case_run_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_planned_only_case_matrix.json",
        "expected_vs_observed": root / "cross_modal_vision_ocr_testboard_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_risk_coverage_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_full_chain_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_full_chain_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_full_chain_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
            "soft_notes": [],
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_full_chain_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    run_plan = _read_json(paths["run_plan"])
    case_run = _read_json(paths["case_run"])
    planned = _read_json(paths["planned"])
    evo = _read_json(paths["expected_vs_observed"])
    risk = _read_json(paths["risk"])
    boundary = _read_json(paths["boundary"])
    aud = _read_json(paths["audit"])

    if int(run_plan.get("case_count") or 0) != 10:
        blockers.append("run_plan_case_count_not_10")
    if int(run_plan.get("selected_case_count") or 0) != 3:
        blockers.append("run_plan_selected_case_count_not_3")
    if int(run_plan.get("planned_only_case_count") or 0) != 7:
        blockers.append("run_plan_planned_only_case_count_not_7")

    run_rows = case_run.get("rows") if isinstance(case_run.get("rows"), list) else []
    if int(case_run.get("row_count") or len(run_rows)) != 3:
        blockers.append("case_run_matrix_row_count_not_3")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 7:
        blockers.append("planned_only_matrix_row_count_not_7")

    for pr in planned_rows:
        if not isinstance(pr, dict):
            continue
        if pr.get("execution_status") != "planned_only":
            blockers.append(f"planned_not_planned_only:{pr.get('case_id')}")
        if pr.get("case_run_id"):
            blockers.append(f"planned_has_case_run_id:{pr.get('case_id')}")
        if not pr.get("must_not_have_case_run_id"):
            blockers.append(f"planned_missing_must_not_flag:{pr.get('case_id')}")

    run_by_id = {r.get("case_id"): r for r in run_rows if isinstance(r, dict)}
    for cid in REQUIRED_EXECUTED_CASES:
        if cid not in run_by_id:
            blockers.append(f"missing_executed_case_run:{cid}")
        elif not run_by_id[cid].get("case_run_id"):
            blockers.append(f"missing_case_run_id:{cid}")

    pos = run_by_id.get("CM_VOCR_001_POSITIVE_TEXT_CLEAR") or {}
    if pos:
        if pos.get("fusion_candidate_generated") is not True:
            blockers.append("positive_fusion_candidate_not_generated")
        if pos.get("review_queue_status") != "pending_review":
            blockers.append("positive_review_queue_not_pending_review")
        if pos.get("gate_decision") != "hold_for_review":
            blockers.append("positive_gate_not_hold_for_review")
        if pos.get("executor_status") != "blocked_by_gate":
            blockers.append("positive_executor_not_blocked_by_gate")

    empty = run_by_id.get("CM_VOCR_002_EMPTY_TEXT_ROI") or {}
    if empty and empty.get("empty_text") is not True:
        blockers.append("empty_text_roi_not_empty")

    multi = run_by_id.get("CM_VOCR_006_MULTI_TEXT_LINES") or {}
    if multi and int(multi.get("text_item_count") or 0) < 2:
        blockers.append("multi_text_lines_item_count_below_2")

    evo_rows = evo.get("rows") if isinstance(evo.get("rows"), list) else []
    if not evo_rows:
        blockers.append("expected_vs_observed_empty")

    for er in evo_rows:
        if not isinstance(er, dict):
            continue
        if er.get("observed_final_fact_status") != "not_fact":
            blockers.append(f"evo_fact_not_not_fact:{er.get('case_id')}")
        if er.get("observed_final_write_status") != "no_write":
            blockers.append(f"evo_write_not_no_write:{er.get('case_id')}")

    pos_evo = next((r for r in evo_rows if r.get("case_id") == "CM_VOCR_001_POSITIVE_TEXT_CLEAR"), None)
    if pos_evo and pos_evo.get("observed_text_non_empty") is not True:
        blockers.append("positive_observed_text_non_empty_false")

    empty_evo = next((r for r in evo_rows if r.get("case_id") == "CM_VOCR_002_EMPTY_TEXT_ROI"), None)
    if empty_evo and empty_evo.get("observed_empty_text") is not True:
        blockers.append("empty_observed_empty_text_false")

    if not risk:
        blockers.append("risk_coverage_missing")
    else:
        for flag in (
            "empty_text_case_covered",
            "positive_text_case_covered",
            "multi_line_text_case_covered",
            "no_write_boundary_covered",
            "review_queue_covered",
            "gate_evaluator_covered",
            "executor_blocked_trace_covered",
        ):
            if risk.get(flag) is not True:
                blockers.append(f"risk_{flag}_false")

    b_rows = boundary.get("rows") if isinstance(boundary.get("rows"), list) else []
    for br in b_rows:
        if not isinstance(br, dict):
            continue
        for k in (
            "midplatform_fact_written",
            "scene_delta_written",
            "world_model_written",
            "scene_delta_executor_invoked",
            "database_write_invoked",
            "wal_append_invoked",
            "navigation_decision_invoked",
            "auto_approve_invoked",
            "approval_granted",
        ):
            if br.get(k) is True:
                blockers.append(f"boundary_violation:{br.get('case_id')}:{k}")

    if boundary.get("boundary_all_ok") is not True:
        blockers.append("boundary_all_ok_false")

    audit_flags = (
        ("cross_modal_testboard_full_chain_case_runner_executed", True),
        ("evaluation_only", True),
        ("selected_case_count", 3),
        ("planned_only_case_count", 7),
        ("real_scene_delta_executor_invoked", False),
        ("midplatform_fact_written", False),
        ("scene_delta_written", False),
        ("world_model_written", False),
        ("navigation_decision_invoked", False),
        ("auto_approve_invoked", False),
        ("approval_granted", False),
        ("database_write_invoked", False),
        ("wal_append_invoked", False),
    )
    for key, expected in audit_flags:
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}_mismatch")

    if int(summary.get("selected_case_count") or 0) < 3:
        soft.append("summary_selected_case_count_below_3")

    verdict = "GO" if not blockers else "NO_GO"
    if verdict == "GO" and soft:
        verdict = "CONDITIONAL_GO"

    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_full_chain_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Case-Runner-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
        "soft_notes": soft,
        "checks_passed": verdict == "GO",
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_full_chain_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict in ("GO", "CONDITIONAL_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
