#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for TestBoard Duplicate Conflicting execution."""

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
        "summary": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_summary.json",
        "execution": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_case_execution_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_planned_only_matrix.json",
        "expected": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_risk_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_duplicate_conflicting_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Duplicate-Conflicting-Text-Execution-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_verifier_report.json", rep)
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
    if int(summary.get("executed_case_count") or 0) != 9:
        blockers.append("executed_case_count_not_9")
    if int(summary.get("planned_only_case_count") or 0) != 1:
        blockers.append("planned_only_case_count_not_1")

    run_rows = execution.get("rows") if isinstance(execution.get("rows"), list) else []
    run_by_type = {r.get("case_type"): r for r in run_rows if isinstance(r, dict)}

    dup = run_by_type.get("DUPLICATE_TEXT_ROI")
    if not dup or not dup.get("case_run_id"):
        blockers.append("duplicate_not_executed")
    else:
        if "duplicate_text_candidate" not in (dup.get("risk_codes") or []):
            blockers.append("duplicate_missing_risk_code")
        if dup.get("duplicate_detected") is not True:
            blockers.append("duplicate_detected_not_true")
        if dup.get("world_model_write_allowed") is not False:
            blockers.append("duplicate_world_model_write_allowed_not_false")

    conf = run_by_type.get("CONFLICTING_TEXT_ROI")
    if not conf or not conf.get("case_run_id"):
        blockers.append("conflicting_not_executed")
    else:
        if "conflicting_text_candidate" not in (conf.get("risk_codes") or []):
            blockers.append("conflicting_missing_risk_code")
        if conf.get("conflict_detected") is not True:
            blockers.append("conflict_detected_not_true")
        if conf.get("conflict_resolved") is not False:
            blockers.append("conflict_resolved_not_false")
        if conf.get("no_conflict_resolution") is not True:
            blockers.append("no_conflict_resolution_not_true")

    for er in run_rows:
        if not isinstance(er, dict):
            continue
        if er.get("confirmed_state_generated") is True:
            blockers.append(f"confirmed_state_generated_true:{er.get('case_id')}")
        if er.get("final_fact_status") != "not_fact":
            blockers.append(f"fact_not_not_fact:{er.get('case_id')}")
        if er.get("final_write_status") != "no_write":
            blockers.append(f"write_not_no_write:{er.get('case_id')}")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 1:
        blockers.append("planned_only_matrix_row_count_not_1")
    for pr in planned_rows:
        if isinstance(pr, dict) and pr.get("case_run_id"):
            blockers.append(f"planned_has_case_run_id:{pr.get('case_id')}")

    if risk.get("confirmed_state_generated_any") is True:
        blockers.append("risk_confirmed_state_any")
    if risk.get("world_model_write_allowed_any") is True:
        blockers.append("risk_world_model_write_allowed_any")
    if risk.get("conflict_resolved_any") is True:
        blockers.append("risk_conflict_resolved_any")

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
        ("cross_modal_testboard_duplicate_conflicting_execution_executed", True),
        ("evaluation_only", True),
        ("executed_case_count", 9),
        ("planned_only_case_count", 1),
        ("duplicate_text_case_executed", True),
        ("conflicting_text_case_executed", True),
        ("duplicate_detected", True),
        ("conflict_detected", True),
        ("conflict_resolved", False),
        ("confirmed_state_generated", False),
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
        "schema": "cross_modal_vision_ocr_testboard_duplicate_conflicting_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Duplicate-Conflicting-Text-Execution-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
