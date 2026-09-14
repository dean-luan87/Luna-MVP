#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for TestBoard LowQuality PartialText execution."""

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


def _risk_codes_from_rows(rows: List[Dict[str, Any]]) -> List[str]:
    codes: List[str] = []
    for r in rows:
        if isinstance(r, dict):
            codes.extend(r.get("risk_codes") or [])
    return codes


def main() -> int:
    _find_ws_root()
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke-root", required=True)
    args = ap.parse_args()

    root = _require_abs(args.smoke_root, "--smoke-root")
    blockers: List[str] = []

    paths = {
        "summary": root / "cross_modal_vision_ocr_testboard_lowquality_partial_summary.json",
        "execution": root / "cross_modal_vision_ocr_testboard_lowquality_partial_case_execution_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_lowquality_partial_planned_only_matrix.json",
        "expected": root / "cross_modal_vision_ocr_testboard_lowquality_partial_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_lowquality_partial_risk_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_lowquality_partial_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_lowquality_partial_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_lowquality_partial_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-LowQuality-PartialText-Execution-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_lowquality_partial_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    execution = _read_json(paths["execution"])
    planned = _read_json(paths["planned"])
    risk = _read_json(paths["risk"])
    boundary = _read_json(paths["boundary"])
    aud = _read_json(paths["audit"])

    if int(summary.get("case_count") or 0) != 10:
        blockers.append("case_count_not_10")
    if int(summary.get("executed_case_count") or 0) != 5:
        blockers.append("executed_case_count_not_5")
    if int(summary.get("planned_only_case_count") or 0) != 5:
        blockers.append("planned_only_case_count_not_5")

    exec_rows = execution.get("rows") if isinstance(execution.get("rows"), list) else []
    exec_by_type = {r.get("case_type"): r for r in exec_rows if isinstance(r, dict)}

    low = exec_by_type.get("LOW_QUALITY_TEXT")
    if not low or not low.get("case_run_id"):
        blockers.append("low_quality_text_not_executed")
    partial = exec_by_type.get("PARTIAL_TEXT")
    if not partial or not partial.get("case_run_id"):
        blockers.append("partial_text_not_executed")

    all_risk = _risk_codes_from_rows(exec_rows)
    if "low_quality_text_risk" not in all_risk:
        blockers.append("missing_low_quality_text_risk")
    if "partial_text_risk" not in all_risk:
        blockers.append("missing_partial_text_risk")
    if "forced_interpretation" in all_risk:
        blockers.append("forced_interpretation_present")
    if "forced_completion" in all_risk:
        blockers.append("forced_completion_present")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 5:
        blockers.append("planned_only_matrix_row_count_not_5")
    for pr in planned_rows:
        if not isinstance(pr, dict):
            continue
        if pr.get("case_run_id"):
            blockers.append(f"planned_has_case_run_id:{pr.get('case_id')}")

    for er in exec_rows:
        if not isinstance(er, dict):
            continue
        if er.get("final_fact_status") != "not_fact":
            blockers.append(f"fact_not_not_fact:{er.get('case_id')}")
        if er.get("final_write_status") != "no_write":
            blockers.append(f"write_not_no_write:{er.get('case_id')}")

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

    audit_checks = (
        ("cross_modal_testboard_lowquality_partial_execution_executed", True),
        ("evaluation_only", True),
        ("executed_case_count", 5),
        ("planned_only_case_count", 5),
        ("low_quality_text_case_executed", True),
        ("partial_text_case_executed", True),
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
        "schema": "cross_modal_vision_ocr_testboard_lowquality_partial_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-LowQuality-PartialText-Execution-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_lowquality_partial_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
