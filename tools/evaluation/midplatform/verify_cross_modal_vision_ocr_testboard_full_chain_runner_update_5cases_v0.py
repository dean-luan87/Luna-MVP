#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for TestBoard full-chain runner 5-case update."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


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
        "summary": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_summary.json",
        "run_plan": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_run_plan.json",
        "case_run": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_case_run_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_planned_only_matrix.json",
        "expected": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_risk_coverage_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_full_chain_5cases_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_full_chain_5cases_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-5Cases-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_full_chain_5cases_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    run_plan = _read_json(paths["run_plan"])
    case_run = _read_json(paths["case_run"])
    planned = _read_json(paths["planned"])
    risk = _read_json(paths["risk"])
    boundary = _read_json(paths["boundary"])
    aud = _read_json(paths["audit"])

    if int(summary.get("case_count") or 0) != 10:
        blockers.append("case_count_not_10")
    if int(summary.get("selected_case_count") or 0) != 5:
        blockers.append("selected_case_count_not_5")
    if int(summary.get("planned_only_case_count") or 0) != 5:
        blockers.append("planned_only_case_count_not_5")
    if int(run_plan.get("selected_case_count") or 0) != 5:
        blockers.append("run_plan_selected_not_5")

    run_rows = case_run.get("rows") if isinstance(case_run.get("rows"), list) else []
    if int(case_run.get("row_count") or len(run_rows)) != 5:
        blockers.append("case_run_matrix_row_count_not_5")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 5:
        blockers.append("planned_only_matrix_row_count_not_5")

    run_by_type = {r.get("case_type"): r for r in run_rows if isinstance(r, dict)}

    low = run_by_type.get("LOW_QUALITY_TEXT")
    if not low:
        blockers.append("missing_low_quality_in_matrix")
    else:
        if "low_quality_text_risk" not in (low.get("risk_codes") or []):
            blockers.append("low_quality_missing_risk_code")
        if low.get("no_forced_interpretation") is not True:
            blockers.append("no_forced_interpretation_not_true")
        if str(low.get("observed_text_joined") or "") != "":
            blockers.append("low_quality_observed_text_not_empty")
        if low.get("empty_text") is not True:
            blockers.append("low_quality_empty_text_not_true")

    partial = run_by_type.get("PARTIAL_TEXT")
    if not partial:
        blockers.append("missing_partial_in_matrix")
    else:
        if "partial_text_risk" not in (partial.get("risk_codes") or []):
            blockers.append("partial_missing_risk_code")
        if partial.get("no_forced_completion") is not True:
            blockers.append("no_forced_completion_not_true")
        joined = str(partial.get("observed_text_joined") or "")
        if "PARTIAL" not in joined and "残缺" not in joined:
            blockers.append("partial_text_joined_missing_fragment")

    for pr in planned_rows:
        if not isinstance(pr, dict):
            continue
        if pr.get("case_run_id"):
            blockers.append(f"planned_has_case_run_id:{pr.get('case_id')}")

    for er in run_rows:
        if not isinstance(er, dict):
            continue
        if er.get("final_fact_status") != "not_fact":
            blockers.append(f"fact_not_not_fact:{er.get('case_id')}")
        if er.get("final_write_status") != "no_write":
            blockers.append(f"write_not_no_write:{er.get('case_id')}")

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
            "database_write_invoked",
            "wal_append_invoked",
            "navigation_decision_invoked",
            "auto_approve_invoked",
            "approval_granted",
        ):
            if br.get(k) is True:
                blockers.append(f"boundary_violation:{br.get('case_id')}:{k}")

    risk_flags = (
        "positive_text_case_covered",
        "empty_text_case_covered",
        "multi_line_text_case_covered",
        "low_quality_text_case_covered",
        "partial_text_case_covered",
        "no_forced_interpretation_covered",
        "no_forced_completion_covered",
        "no_write_boundary_covered",
    )
    for flag in risk_flags:
        if risk.get(flag) is not True:
            blockers.append(f"risk_{flag}_false")

    audit_checks = (
        ("cross_modal_testboard_full_chain_runner_update_5cases_executed", True),
        ("evaluation_only", True),
        ("selected_case_count", 5),
        ("planned_only_case_count", 5),
        ("low_quality_text_case_included", True),
        ("partial_text_case_included", True),
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
    for key, expected in audit_checks:
        if aud.get(key) != expected:
            blockers.append(f"audit_{key}_mismatch")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_full_chain_5cases_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-5Cases-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_full_chain_5cases_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
