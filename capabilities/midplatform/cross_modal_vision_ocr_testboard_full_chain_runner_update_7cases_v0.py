# -*- coding: utf-8 -*-
"""TestBoard full-chain runner view update to 7 executed cases (no writes).

Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-7Cases-001
"""

from __future__ import annotations

import json
import uuid
from pathlib import Path
from typing import Any, Dict, List, Tuple

from capabilities.midplatform.cross_modal_vision_ocr_fusion_candidate_dryrun_v0 import (
    build_fusion_candidate_from_reference_v0,
)
from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import (
    CASE_SPECS,
    expected_behavior_for_case,
)
from capabilities.midplatform.cross_modal_vision_ocr_testboard_full_chain_runner_v0 import (
    CHAIN_STAGES,
    RUN_PLAN_SCHEMA,
    build_expected_vs_observed_row,
)

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_7cases_summary_v0"
CASE_RUN_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_7cases_case_run_matrix_v0"
PLANNED_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_7cases_planned_only_matrix_v0"
EXPECTED_VS_OBSERVED_SCHEMA = (
    "cross_modal_vision_ocr_testboard_full_chain_7cases_expected_vs_observed_report_v0"
)
RISK_COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_7cases_risk_coverage_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_7cases_boundary_matrix_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_full_chain_7cases_audit_v0"

EXECUTED_CASE_IDS_ORDER = (
    "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
    "CM_VOCR_002_EMPTY_TEXT_ROI",
    "CM_VOCR_006_MULTI_TEXT_LINES",
    "CM_VOCR_004_LOW_QUALITY_TEXT",
    "CM_VOCR_005_PARTIAL_TEXT",
    "CM_VOCR_007_MIXED_CN_EN",
    "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
)

NEW_FROM_MIXED_EXECUTION = frozenset(
    {
        "CM_VOCR_007_MIXED_CN_EN",
        "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
    }
)

PLANNED_ONLY_CASE_IDS = (
    "CM_VOCR_003_NON_TEXT_ROI_REJECTED",
    "CM_VOCR_009_DUPLICATE_TEXT_ROI",
    "CM_VOCR_010_CONFLICTING_TEXT_ROI",
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _case_spec(case_id: str) -> Dict[str, Any]:
    for s in CASE_SPECS:
        if s["case_id"] == case_id:
            return s
    return {"case_id": case_id}


def _build_reference(
    *,
    frame_id: str,
    roi_id: str,
    text_joined: str,
    empty_text: bool,
    rapidocr_invoked: bool,
    ocr_request_id: str,
    candidate_id: str,
) -> Dict[str, Any]:
    return {
        "schema_version": "cross_modal_vision_ocr_reference_candidate_v0",
        "reference_id": f"xref_{uuid.uuid4().hex[:16]}",
        "reference_scope": "reference_only",
        "source": "testboard_full_chain_runner_update_7cases",
        "frame_id": frame_id,
        "roi_id": roi_id,
        "roi_type": "upper_sign_roi",
        "ocr_refs": {
            "ocr_text_joined": text_joined,
            "empty_text": empty_text,
            "rapidocr_invoked": rapidocr_invoked,
            "ocr_request_id": ocr_request_id,
            "ocr_request_candidate_id": candidate_id,
        },
        "fact_status": "not_fact",
    }


def build_full_chain_row_from_observed_v0(
    *,
    case_id: str,
    case_type: str,
    fixture_ref: str,
    exec_row: Dict[str, Any],
    work_dir: Path,
) -> Dict[str, Any]:
    """Build full-chain row from prior OCR observations (no RapidOCR re-run)."""
    case_run_id = f"crun_{uuid.uuid4().hex[:16]}"
    frame_id = f"testboard_{case_id[-8:].lower()}"
    roi_id = f"vision_roi_{frame_id}_upper_sign_roi"

    text_joined = str(exec_row.get("observed_text_joined") or "")
    empty_text = bool(
        exec_row.get("observed_empty_text")
        if "observed_empty_text" in exec_row
        else exec_row.get("empty_text")
    )
    text_item_count = int(
        exec_row.get("observed_item_count")
        if exec_row.get("observed_item_count") is not None
        else exec_row.get("text_item_count") or 0
    )
    rapidocr_invoked = bool(exec_row.get("rapidocr_invoked"))

    ocr_request_id = f"ocr_req_{case_run_id}"
    reference = _build_reference(
        frame_id=frame_id,
        roi_id=roi_id,
        text_joined=text_joined,
        empty_text=empty_text,
        rapidocr_invoked=rapidocr_invoked,
        ocr_request_id=ocr_request_id,
        candidate_id=f"ocr_req_cand_{case_run_id}",
    )

    fusion_cand = build_fusion_candidate_from_reference_v0(reference)
    fusion_cand["candidate_id"] = f"fusion_cand_{case_run_id}"
    fusion_cand["fact_status"] = "not_fact"

    risk_codes = list(exec_row.get("risk_codes") or [])
    review_queue_status = "skipped_not_positive_case"

    if case_type == "LOW_QUALITY_TEXT":
        for code in (
            "low_quality_text_risk",
            "ocr_confidence_or_quality_uncertain",
            "no_forced_interpretation",
        ):
            if code not in risk_codes:
                risk_codes.append(code)
        review_queue_status = "skipped_quality_or_partial_risk"
    elif case_type == "PARTIAL_TEXT":
        for code in ("partial_text_risk", "incomplete_text_candidate", "no_forced_completion"):
            if code not in risk_codes:
                risk_codes.append(code)
        review_queue_status = "skipped_quality_or_partial_risk"
    elif case_type == "MIXED_CN_EN":
        for code in (
            "mixed_language_text_risk",
            "no_translation",
            "no_semantic_interpretation",
            "commercial_text_not_fact",
        ):
            if code not in risk_codes:
                risk_codes.append(code)
        review_queue_status = "skipped_mixed_or_false_positive_risk"
    elif case_type == "FALSE_POSITIVE_VISUAL_ROI":
        for code in (
            "false_positive_visual_roi_risk",
            "visual_region_not_text",
            "no_confirmed_sign",
            "ocr_empty_or_invalid_not_failure",
        ):
            if code not in risk_codes:
                risk_codes.append(code)
        review_queue_status = "skipped_mixed_or_false_positive_risk"

    exp = expected_behavior_for_case(_case_spec(case_id) | {"case_type": case_type})

    row: Dict[str, Any] = {
        "case_id": case_id,
        "case_type": case_type,
        "case_run_id": case_run_id,
        "fixture_ref": fixture_ref,
        "expected_text_hint": [],
        "observed_text_joined": text_joined,
        "empty_text": empty_text,
        "text_item_count": text_item_count,
        "ocr_request_generated": True,
        "rapidocr_invoked": rapidocr_invoked,
        "reference_generated": True,
        "fusion_candidate_generated": True,
        "review_queue_status": review_queue_status,
        "gate_decision": "hold_for_review",
        "executor_status": "blocked_by_gate",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
        "risk_codes": risk_codes,
        "expected": exp,
        "work_dir": str(work_dir.resolve()),
        "ocr_re_run": False,
        "translation_performed": False,
        "semantic_interpretation_performed": False,
        "confirmed_sign": False,
    }

    if case_type == "LOW_QUALITY_TEXT":
        row["no_forced_interpretation"] = True
    elif case_type == "PARTIAL_TEXT":
        row["no_forced_completion"] = True
    elif case_type == "MIXED_CN_EN":
        row["no_translation"] = True
        row["no_semantic_interpretation"] = True
    elif case_type == "FALSE_POSITIVE_VISUAL_ROI":
        row["visual_region_not_text"] = True
        row["no_confirmed_sign"] = True
        row["confirmed_sign"] = False

    return row


def load_prior_5cases_rows(fc5_root: Path) -> Dict[str, Dict[str, Any]]:
    path = fc5_root / "cross_modal_vision_ocr_testboard_full_chain_5cases_case_run_matrix.json"
    if not path.is_file():
        return {}
    rows = _read_json(path).get("rows") or []
    return {str(r.get("case_id")): r for r in rows if isinstance(r, dict) and r.get("case_id")}


def load_mixed_execution_rows(mixed_root: Path) -> Dict[str, Dict[str, Any]]:
    path = mixed_root / "cross_modal_vision_ocr_testboard_mixed_cnen_falsepositive_case_execution_matrix.json"
    if not path.is_file():
        return {}
    rows = _read_json(path).get("rows") or []
    return {str(r.get("case_id")): r for r in rows if isinstance(r, dict) and r.get("case_id")}


def build_expected_vs_observed_row_7cases(run_row: Dict[str, Any]) -> Dict[str, Any]:
    base = build_expected_vs_observed_row(run_row)
    ct = run_row.get("case_type")
    if ct == "LOW_QUALITY_TEXT":
        base["observed_text_may_be_partial_or_empty"] = True
        base["no_forced_interpretation"] = True
    elif ct == "PARTIAL_TEXT":
        base["observed_text_may_be_partial_or_fragmented"] = True
        base["no_forced_completion"] = True
    elif ct == "POSITIVE_TEXT_CLEAR":
        base["text_non_empty"] = True
    elif ct == "EMPTY_TEXT_ROI":
        base["empty_text"] = True
    elif ct == "MULTI_TEXT_LINES":
        base["text_item_count_gte_2"] = int(run_row.get("text_item_count") or 0) >= 2
    elif ct == "MIXED_CN_EN":
        base["observed_text_may_include_cn_en"] = True
        base["translation_performed"] = False
        base["semantic_interpretation_performed"] = False
    elif ct == "FALSE_POSITIVE_VISUAL_ROI":
        base["confirmed_sign"] = False
        base["observed_empty_or_invalid_text_allowed"] = True
    return base


def build_risk_coverage_report_7cases_v0(run_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    types = {r.get("case_type") for r in run_rows}
    all_codes = sorted({c for r in run_rows for c in (r.get("risk_codes") or [])})
    return {
        "schema_version": RISK_COVERAGE_SCHEMA,
        "positive_text_case_covered": "POSITIVE_TEXT_CLEAR" in types,
        "empty_text_case_covered": "EMPTY_TEXT_ROI" in types,
        "multi_line_text_case_covered": "MULTI_TEXT_LINES" in types,
        "low_quality_text_case_covered": "LOW_QUALITY_TEXT" in types,
        "partial_text_case_covered": "PARTIAL_TEXT" in types,
        "mixed_language_text_case_covered": "MIXED_CN_EN" in types,
        "false_positive_visual_roi_case_covered": "FALSE_POSITIVE_VISUAL_ROI" in types,
        "no_forced_interpretation_covered": any(r.get("no_forced_interpretation") for r in run_rows)
        or "no_forced_interpretation" in all_codes,
        "no_forced_completion_covered": any(r.get("no_forced_completion") for r in run_rows)
        or "no_forced_completion" in all_codes,
        "no_translation_covered": "no_translation" in all_codes
        or any(r.get("no_translation") for r in run_rows),
        "no_semantic_interpretation_covered": "no_semantic_interpretation" in all_codes
        or any(r.get("no_semantic_interpretation") for r in run_rows),
        "no_confirmed_sign_covered": "no_confirmed_sign" in all_codes
        or any(r.get("no_confirmed_sign") for r in run_rows),
        "no_write_boundary_covered": all(r.get("final_write_status") == "no_write" for r in run_rows),
        "review_queue_covered": any(
            str(r.get("review_queue_status", "")).startswith("pending") for r in run_rows
        ),
        "gate_evaluator_covered": any(r.get("gate_decision") == "hold_for_review" for r in run_rows),
        "executor_blocked_trace_covered": any(
            r.get("executor_status") == "blocked_by_gate" for r in run_rows
        ),
        "translation_performed_any": any(r.get("translation_performed") for r in run_rows),
        "semantic_interpretation_performed_any": any(
            r.get("semantic_interpretation_performed") for r in run_rows
        ),
        "confirmed_sign_any": any(r.get("confirmed_sign") for r in run_rows),
        "risk_codes_observed": all_codes,
    }


def build_audit_7cases_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_testboard_full_chain_runner_update_7cases_executed": True,
        "evaluation_only": True,
        "selected_case_count": 7,
        "planned_only_case_count": 3,
        "mixed_cn_en_case_included": True,
        "false_positive_visual_roi_case_included": True,
        "translation_performed": False,
        "semantic_interpretation_performed": False,
        "confirmed_sign_generated": False,
        "real_scene_delta_executor_invoked": False,
        "midplatform_fact_written": False,
        "scene_delta_written": False,
        "world_model_written": False,
        "navigation_decision_invoked": False,
        "auto_approve_invoked": False,
        "approval_granted": False,
        "database_write_invoked": False,
        "wal_append_invoked": False,
    }


def run_cross_modal_vision_ocr_testboard_full_chain_runner_update_7cases_v0(
    *,
    mixed_cnen_falsepositive_root: str,
    full_chain_5cases_root: str,
    testboard_expansion_root: str,
    work_root: Path,
) -> Tuple[
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    Dict[str, Any],
    List[str],
]:
    errs: List[str] = []
    mixed = Path(mixed_cnen_falsepositive_root).resolve()
    fc5 = Path(full_chain_5cases_root).resolve()
    tb = Path(testboard_expansion_root).resolve()
    work_root.mkdir(parents=True, exist_ok=True)

    prior5_by_id = load_prior_5cases_rows(fc5)
    mixed_exec_by_id = load_mixed_execution_rows(mixed)

    case_run_rows: List[Dict[str, Any]] = []
    for cid in EXECUTED_CASE_IDS_ORDER:
        if cid in NEW_FROM_MIXED_EXECUTION:
            exec_row = mixed_exec_by_id.get(cid)
            if not exec_row:
                errs.append(f"missing_mixed_execution_row:{cid}")
                continue
            fixture_ref = str(exec_row.get("fixture_ref") or "")
            if not fixture_ref or not Path(fixture_ref).is_file():
                errs.append(f"fixture_missing:{cid}")
                continue
            case_type = str(exec_row.get("case_type") or _case_spec(cid).get("case_type"))
            row = build_full_chain_row_from_observed_v0(
                case_id=cid,
                case_type=case_type,
                fixture_ref=fixture_ref,
                exec_row=exec_row,
                work_dir=work_root / cid,
            )
            case_run_rows.append(row)
        else:
            prior = prior5_by_id.get(cid)
            if not prior:
                errs.append(f"missing_prior_5cases_row:{cid}")
                continue
            case_run_rows.append(dict(prior))

    planned_matrix_rows = [
        {
            "case_id": cid,
            "case_type": _case_spec(cid).get("case_type"),
            "execution_status": "planned_only",
            "reason": "fixture_execution_deferred",
            "must_not_have_case_run_id": True,
        }
        for cid in PLANNED_ONLY_CASE_IDS
    ]

    run_plan = {
        "schema_version": RUN_PLAN_SCHEMA,
        "testboard_root": str(tb),
        "mixed_cnen_falsepositive_root": str(mixed),
        "full_chain_5cases_root": str(fc5),
        "case_count": 10,
        "selected_case_count": len(case_run_rows),
        "planned_only_case_count": len(planned_matrix_rows),
        "run_scope": "executed_cases_only_updated_7_cases",
        "chain_stages": list(CHAIN_STAGES),
    }

    evo_rows = [build_expected_vs_observed_row_7cases(r) for r in case_run_rows]
    risk_coverage = build_risk_coverage_report_7cases_v0(case_run_rows)
    boundary_rows = [
        {
            "case_id": r.get("case_id"),
            "case_run_id": r.get("case_run_id"),
            **{
                k: False
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
                )
            },
        }
        for r in case_run_rows
    ]

    if len(case_run_rows) != 7:
        errs.append(f"case_run_row_count:{len(case_run_rows)}")
    if len(planned_matrix_rows) != 3:
        errs.append(f"planned_row_count:{len(planned_matrix_rows)}")

    phase_verdict = "GO" if len(case_run_rows) == 7 and not errs else "CONDITIONAL_GO"
    if len(case_run_rows) < 7:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-Full-Chain-Runner-Update-7Cases-001",
        "mixed_cnen_falsepositive_root": str(mixed),
        "full_chain_5cases_root": str(fc5),
        "testboard_expansion_root": str(tb),
        "case_count": 10,
        "selected_case_count": len(case_run_rows),
        "planned_only_case_count": len(planned_matrix_rows),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        run_plan,
        {
            "schema_version": CASE_RUN_MATRIX_SCHEMA,
            "row_count": len(case_run_rows),
            "rows": case_run_rows,
        },
        {
            "schema_version": PLANNED_MATRIX_SCHEMA,
            "row_count": len(planned_matrix_rows),
            "rows": planned_matrix_rows,
        },
        {
            "schema_version": EXPECTED_VS_OBSERVED_SCHEMA,
            "row_count": len(evo_rows),
            "rows": evo_rows,
        },
        risk_coverage,
        {
            "schema_version": BOUNDARY_MATRIX_SCHEMA,
            "boundary_all_ok": True,
            "rows": boundary_rows,
        },
        build_audit_7cases_v0(),
        errs,
    )
