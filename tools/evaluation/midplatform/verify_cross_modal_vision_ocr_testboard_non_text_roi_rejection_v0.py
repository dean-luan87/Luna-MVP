#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for TestBoard NonText ROI rejection."""

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
        "summary": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_summary.json",
        "case_report": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_report.json",
        "rejection": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_matrix.json",
        "execution": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_execution_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_planned_only_matrix.json",
        "expected": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_risk_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_non_text_roi_rejection_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    case_report = _read_json(paths["case_report"])
    rejection = _read_json(paths["rejection"])
    execution = _read_json(paths["execution"])
    planned = _read_json(paths["planned"])
    risk = _read_json(paths["risk"])
    boundary = _read_json(paths["boundary"])
    aud = _read_json(paths["audit"])

    if int(summary.get("case_count") or 0) != 10:
        blockers.append("case_count_not_10")
    if int(summary.get("executed_case_count") or 0) != 10:
        blockers.append("executed_case_count_not_10")
    if int(summary.get("planned_only_case_count") or 0) != 0:
        blockers.append("planned_only_case_count_not_0")

    if case_report.get("rejection_status") != "rejected_before_ocr":
        blockers.append("case_report_rejection_status_mismatch")
    for flag in (
        "ocr_request_generated",
        "ocr_provider_invoked",
        "rapidocr_invoked",
        "paddleocr_invoked",
        "reference_generated",
        "fusion_candidate_generated",
        "scene_delta_candidate_generated",
    ):
        if case_report.get(flag) is not False:
            blockers.append(f"case_report_{flag}_not_false")

    run_rows = execution.get("rows") if isinstance(execution.get("rows"), list) else []
    non_text = next((r for r in run_rows if r.get("case_type") == "NON_TEXT_ROI_REJECTED"), None)
    if not non_text or not non_text.get("case_run_id"):
        blockers.append("non_text_not_executed")
    else:
        if non_text.get("rejection_status") != "rejected_before_ocr":
            blockers.append("non_text_rejection_status_mismatch")
        if non_text.get("ocr_request_generated") is not False:
            blockers.append("non_text_ocr_request_generated_not_false")
        if non_text.get("rapidocr_invoked") is not False:
            blockers.append("non_text_rapidocr_invoked_not_false")
        if non_text.get("paddleocr_invoked") is not False:
            blockers.append("non_text_paddleocr_invoked_not_false")
        if non_text.get("reference_generated") is not False:
            blockers.append("non_text_reference_generated_not_false")
        if non_text.get("fusion_candidate_generated") is not False:
            blockers.append("non_text_fusion_not_false")
        if non_text.get("scene_delta_candidate_generated") is not False:
            blockers.append("non_text_scene_delta_candidate_not_false")

    rej_codes = set(rejection.get("reason_codes_covered") or [])
    for code in ("center_roi_not_text_candidate", "ground_roi_not_ocr_candidate", "non_text_roi"):
        if code not in rej_codes:
            blockers.append(f"rejection_matrix_missing_reason:{code}")

    rej_rows = rejection.get("rows") if isinstance(rejection.get("rows"), list) else []
    if not rej_rows:
        blockers.append("rejection_matrix_empty")
    for rr in rej_rows[:5]:
        if isinstance(rr, dict) and rr.get("ocr_request_generated") is not False:
            blockers.append(f"rejection_row_ocr_request_true:{rr.get('roi_id')}")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 0:
        blockers.append("planned_only_matrix_not_empty")
    if planned_rows:
        blockers.append("planned_only_rows_present")

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
        "non_text_roi_rejected_before_ocr",
        "ocr_request_not_generated",
        "ocr_provider_not_invoked",
        "no_false_text_claim",
        "no_cross_modal_fusion",
        "no_scene_delta_candidate",
    )
    for flag in risk_flags:
        if risk.get(flag) is not True:
            blockers.append(f"risk_{flag}_false")

    audit_checks = (
        ("cross_modal_testboard_non_text_roi_rejection_executed", True),
        ("evaluation_only", True),
        ("executed_case_count", 10),
        ("planned_only_case_count", 0),
        ("non_text_roi_rejection_case_executed", True),
        ("ocr_request_generated_for_non_text", False),
        ("rapidocr_invoked_for_non_text", False),
        ("paddleocr_invoked_for_non_text", False),
        ("fusion_candidate_generated_for_non_text", False),
        ("scene_delta_candidate_generated_for_non_text", False),
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
        "schema": "cross_modal_vision_ocr_testboard_non_text_roi_rejection_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
