#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier for TestBoard Mixed CN/EN + False Positive execution."""

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
        "summary": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_summary.json",
        "execution": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_case_execution_matrix.json",
        "planned": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_planned_only_matrix.json",
        "expected": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_expected_vs_observed_report.json",
        "risk": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_risk_report.json",
        "boundary": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_boundary_matrix.json",
        "audit": root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_audit_report.json",
    }

    for label, p in paths.items():
        if not p.is_file():
            blockers.append(f"missing:{label}")

    if blockers:
        rep = {
            "schema": "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_verifier_report_v0",
            "phase": "Phase-CrossModal-Vision-OCR-TestBoard-MixedCNEN-FalsePositive-Execution-001",
            "smoke_root": str(root),
            "verdict": "NO_GO",
            "blockers": blockers,
        }
        _write_json(root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_verifier_report.json", rep)
        print(json.dumps({"smoke_root": str(root), "verdict": "NO_GO", "blockers": blockers}, ensure_ascii=False))
        return 2

    summary = _read_json(paths["summary"])
    execution = _read_json(paths["execution"])
    planned = _read_json(paths["planned"])
    expected = _read_json(paths["expected"])
    risk = _read_json(paths["risk"])
    boundary = _read_json(paths["boundary"])
    aud = _read_json(paths["audit"])

    if int(summary.get("case_count") or 0) != 10:
        blockers.append("case_count_not_10")
    if int(summary.get("executed_case_count") or 0) != 7:
        blockers.append("executed_case_count_not_7")
    if int(summary.get("planned_only_case_count") or 0) != 3:
        blockers.append("planned_only_case_count_not_3")

    run_rows = execution.get("rows") if isinstance(execution.get("rows"), list) else []
    run_by_type = {r.get("case_type"): r for r in run_rows if isinstance(r, dict)}

    mixed = run_by_type.get("MIXED_CN_EN")
    if not mixed or not mixed.get("case_run_id"):
        blockers.append("mixed_cn_en_not_executed")
    else:
        if "mixed_language_text_risk" not in (mixed.get("risk_codes") or []):
            blockers.append("mixed_missing_risk_code")
        if mixed.get("translation_performed") is not False:
            blockers.append("mixed_translation_performed_not_false")
        if mixed.get("semantic_interpretation_performed") is not False:
            blockers.append("mixed_semantic_interpretation_not_false")
        if mixed.get("no_translation") is not True:
            blockers.append("mixed_no_translation_not_true")
        if mixed.get("no_semantic_interpretation") is not True:
            blockers.append("mixed_no_semantic_interpretation_not_true")

    fp = run_by_type.get("FALSE_POSITIVE_VISUAL_ROI")
    if not fp or not fp.get("case_run_id"):
        blockers.append("false_positive_not_executed")
    else:
        if "false_positive_visual_roi_risk" not in (fp.get("risk_codes") or []):
            blockers.append("false_positive_missing_risk_code")
        if fp.get("confirmed_sign") is not False:
            blockers.append("false_positive_confirmed_sign_not_false")
        if fp.get("visual_region_not_text") is not True:
            blockers.append("false_positive_visual_region_not_text_not_true")
        if fp.get("no_confirmed_sign") is not True:
            blockers.append("false_positive_no_confirmed_sign_not_true")

    evo_rows = expected.get("rows") if isinstance(expected.get("rows"), list) else []
    mixed_evo = next((r for r in evo_rows if r.get("case_type") == "MIXED_CN_EN"), None)
    if mixed_evo:
        if mixed_evo.get("translation_performed") is not False:
            blockers.append("evo_mixed_translation_not_false")
        if mixed_evo.get("semantic_interpretation_performed") is not False:
            blockers.append("evo_mixed_semantic_not_false")
    fp_evo = next((r for r in evo_rows if r.get("case_type") == "FALSE_POSITIVE_VISUAL_ROI"), None)
    if fp_evo and fp_evo.get("confirmed_sign") is not False:
        blockers.append("evo_false_positive_confirmed_sign_not_false")

    planned_rows = planned.get("rows") if isinstance(planned.get("rows"), list) else []
    if int(planned.get("row_count") or len(planned_rows)) != 3:
        blockers.append("planned_only_matrix_row_count_not_3")
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

    if risk.get("translation_performed_any") is True:
        blockers.append("risk_translation_performed_any")
    if risk.get("semantic_interpretation_performed_any") is True:
        blockers.append("risk_semantic_interpretation_any")
    if risk.get("confirmed_sign_any") is True:
        blockers.append("risk_confirmed_sign_any")

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
        ("cross_modal_testboard_mixed_cnen_falsepositive_execution_executed", True),
        ("evaluation_only", True),
        ("executed_case_count", 7),
        ("planned_only_case_count", 3),
        ("mixed_cn_en_case_executed", True),
        ("false_positive_visual_roi_case_executed", True),
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
    for key, expected_val in audit_checks:
        if aud.get(key) != expected_val:
            blockers.append(f"audit_{key}_mismatch")

    verdict = "GO" if not blockers else "NO_GO"
    rep: Dict[str, Any] = {
        "schema": "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_verifier_report_v0",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-MixedCNEN-FalsePositive-Execution-001",
        "smoke_root": str(root),
        "verdict": verdict,
        "blockers": blockers,
    }
    _write_json(root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_verifier_report.json", rep)
    print(json.dumps({"smoke_root": str(root), "verdict": verdict, "blockers": blockers}, ensure_ascii=False))
    return 0 if verdict == "GO" else 2


if __name__ == "__main__":
    raise SystemExit(main())
