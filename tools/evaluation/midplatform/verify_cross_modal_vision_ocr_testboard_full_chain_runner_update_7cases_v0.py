#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for TestBoard full-chain runner 7-case update."""

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
        "summary": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_summary.json",
        "run_plan": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_run_plan.json",
        "case_run": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_case_run_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_planned_only_matrix.json",
        "expected": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_risk_coverage_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_full_chain_7cases_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_full_chain_7cases_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-7Cases-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_full_chain_7cases_verifier_report.json", rep)
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
    if int(summary.get("selected_case_count") or 0) != 7:
        blockers.append("selected_case_count_not_7")
    if int(summary.get("planned_only_case_count") or 0) != 3:
        blockers.append("planned_only_case_count_not_3")
    if run_plan.get("run_scope") != "executed_cases_only_updated_7_cases":
        blockers.append("run_scope_not_updated_7_cases")

    run_rows = case_run.get("rows") if isinstance(case_run.get("rows"), list) else []
    if int(case_run.get("row_count") or len(run_rows)) != 7:
        blockers.append("case_run_matrix_row_count_not_7")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 3:
        blockers.append("planned_only_matrix_row_count_not_3")

    run_by_type = {r.get("case_type"): r for r in run_rows if isinstance(r, dict)}

    mixed = run_by_type.get("MIXED_CN_EN")
    if not mixed:
        blockers.append("missing_mixed_cn_en")
    else:
        if "mixed_language_text_risk" not in (mixed.get("risk_codes") or []):
            blockers.append("mixed_missing_risk_code")
        if mixed.get("translation_performed") is not False:
            blockers.append("mixed_translation_performed_not_false")
        if mixed.get("semantic_interpretation_performed") is not False:
            blockers.append("mixed_semantic_not_false")
        if mixed.get("no_translation") is not True:
            blockers.append("mixed_no_translation_not_true")
        if mixed.get("no_semantic_interpretation") is not True:
            blockers.append("mixed_no_semantic_not_true")
        joined = str(mixed.get("observed_text_joined") or "")
        if not any(x in joined for x in ("SALE", "中文优惠", "LUNAA1", "LUNA")):
            blockers.append("mixed_observed_text_missing_hint")

    fp = run_by_type.get("FALSE_POSITIVE_VISUAL_ROI")
    if not fp:
        blockers.append("missing_false_positive")
    else:
        if "false_positive_visual_roi_risk" not in (fp.get("risk_codes") or []):
            blockers.append("false_positive_missing_risk_code")
        if fp.get("confirmed_sign") is not False:
            blockers.append("false_positive_confirmed_sign_not_false")
        if fp.get("visual_region_not_text") is not True:
            blockers.append("false_positive_visual_region_not_text_not_true")
        if fp.get("no_confirmed_sign") is not True:
            blockers.append("false_positive_no_confirmed_sign_not_true")
        if str(fp.get("observed_text_joined") or "") != "":
            blockers.append("false_positive_observed_text_not_empty")
        if fp.get("empty_text") is not True and fp.get("observed_empty_text") is not True:
            blockers.append("false_positive_empty_text_not_true")

    for pr in planned_rows:
        if isinstance(pr, dict) and pr.get("case_run_id"):
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
        "mixed_language_text_case_covered",
        "false_positive_visual_roi_case_covered",
        "no_forced_interpretation_covered",
        "no_forced_completion_covered",
        "no_translation_covered",
        "no_semantic_interpretation_covered",
        "no_confirmed_sign_covered",
        "no_write_boundary_covered",
    )
    for flag in risk_flags:
        if risk.get(flag) is not True:
            blockers.append(f"risk_{flag}_false")

    if risk.get("translation_performed_any") is True:
        blockers.append("risk_translation_performed_any")
    if risk.get("semantic_interpretation_performed_any") is True:
        blockers.append("risk_semantic_any")
    if risk.get("confirmed_sign_any") is True:
        blockers.append("risk_confirmed_sign_any")

    audit_checks = (
        ("cross_modal_testboard_full_chain_runner_update_7cases_executed", True),
        ("evaluation_only", True),
        ("selected_case_count", 7),
        ("planned_only_case_count", 3),
        ("mixed_cn_en_case_included", True),
        ("false_positive_visual_roi_case_included", True),
        ("translation_performed", False),
        ("semantic_interpretation_performed", False),
        ("confirmed_sign_generated", False),
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
        "schema": "cross_modal_vision_ocr_testboard_full_chain_7cases_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-7Cases-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_full_chain_7cases_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
