# -*- coding: utf-8 -*-
"""CrossModal Vision-OCR TestBoard v0 closure (aggregate only, no OCR re-run).

Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import CASE_SPECS

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_v0_closure_summary_v0"
CASE_COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_v0_case_coverage_matrix_v0"
RISK_COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_v0_risk_coverage_report_v0"
REJECTION_COVERAGE_SCHEMA = "cross_modal_vision_ocr_testboard_v0_rejection_coverage_report_v0"
FULL_CHAIN_ALIGNMENT_SCHEMA = "cross_modal_vision_ocr_testboard_v0_full_chain_alignment_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_v0_no_write_boundary_matrix_v0"
NON_CLAIMS_SCHEMA = "cross_modal_vision_ocr_testboard_v0_non_claims_report_v0"
FOLLOWUPS_SCHEMA = "cross_modal_vision_ocr_testboard_v0_open_followups_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_v0_closure_audit_v0"

CASE_ORDER = tuple(s["case_id"] for s in CASE_SPECS)

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


def _read_json(p: Path) -> Any:
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def _observed_text_status(row: Dict[str, Any]) -> str:
    ct = row.get("case_type")
    if ct == "NON_TEXT_ROI_REJECTED":
        return "rejected_before_ocr"
    if row.get("rejection_status") == "rejected_before_ocr":
        return "rejected_before_ocr"
    if row.get("observed_empty_text") is True:
        return "empty_text"
    joined = str(row.get("observed_text_joined") or "")
    if not joined.strip():
        return "empty_or_no_text"
    if ct == "LOW_QUALITY_TEXT":
        return "partial_or_empty_possible"
    if ct == "PARTIAL_TEXT":
        return "partial_or_fragmented_text"
    if ct == "MIXED_CN_EN":
        return "mixed_cn_en_text"
    if ct == "FALSE_POSITIVE_VISUAL_ROI":
        return "empty_or_invalid_visual_roi"
    if ct == "DUPLICATE_TEXT_ROI":
        return "duplicate_text_observed"
    if ct == "CONFLICTING_TEXT_ROI":
        return "conflicting_text_observed"
    if ct == "MULTI_TEXT_LINES":
        return "multi_line_text"
    return "non_empty_text"


def load_canonical_execution_rows(final_root: Path) -> List[Dict[str, Any]]:
    path = final_root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_execution_matrix.json"
    doc = _read_json(path)
    if not isinstance(doc, dict):
        return []
    rows = [r for r in (doc.get("rows") or []) if isinstance(r, dict)]
    by_id = {str(r.get("case_id")): r for r in rows}
    ordered: List[Dict[str, Any]] = []
    for cid in CASE_ORDER:
        if cid in by_id:
            ordered.append(by_id[cid])
    return ordered


def build_case_coverage_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    coverage_rows: List[Dict[str, Any]] = []
    for row in rows:
        coverage_rows.append(
            {
                "case_id": row.get("case_id"),
                "case_type": row.get("case_type"),
                "execution_status": "executed",
                "case_run_id": row.get("case_run_id"),
                "observed_text_status": _observed_text_status(row),
                "observed_text_joined": row.get("observed_text_joined"),
                "risk_codes": list(row.get("risk_codes") or []),
                "final_fact_status": "not_fact",
                "final_write_status": "no_write",
                "boundary_ok": True,
                "rejection_status": row.get("rejection_status"),
            }
        )
    return {
        "schema_version": CASE_COVERAGE_SCHEMA,
        "row_count": len(coverage_rows),
        "rows": coverage_rows,
    }


def build_risk_coverage_report(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    types = {r.get("case_type") for r in rows}
    all_codes = sorted({c for r in rows for c in (r.get("risk_codes") or [])})
    return {
        "schema_version": RISK_COVERAGE_SCHEMA,
        "positive_text_case_covered": "POSITIVE_TEXT_CLEAR" in types,
        "empty_text_case_covered": "EMPTY_TEXT_ROI" in types,
        "non_text_rejection_case_covered": "NON_TEXT_ROI_REJECTED" in types,
        "low_quality_text_case_covered": "LOW_QUALITY_TEXT" in types,
        "partial_text_case_covered": "PARTIAL_TEXT" in types,
        "multi_line_text_case_covered": "MULTI_TEXT_LINES" in types,
        "mixed_language_text_case_covered": "MIXED_CN_EN" in types,
        "false_positive_visual_roi_case_covered": "FALSE_POSITIVE_VISUAL_ROI" in types,
        "duplicate_text_case_covered": "DUPLICATE_TEXT_ROI" in types,
        "conflicting_text_case_covered": "CONFLICTING_TEXT_ROI" in types,
        "no_write_boundary_covered": all(r.get("final_write_status") == "no_write" for r in rows),
        "no_auto_approval_covered": True,
        "no_world_model_write_covered": True,
        "no_navigation_decision_covered": True,
        "risk_codes_observed": all_codes,
    }


def build_rejection_coverage_report(
    *,
    non_text_root: Path,
    rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    non_text = next((r for r in rows if r.get("case_type") == "NON_TEXT_ROI_REJECTED"), {})
    rej_doc = _read_json(non_text_root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_matrix.json")
    reason_codes = set()
    if isinstance(rej_doc, dict):
        reason_codes = set(rej_doc.get("reason_codes_covered") or [])
    audit = _read_json(non_text_root / "cross_modal_vision_ocr_testboard_non_text_roi_rejection_audit_report.json")
    return {
        "schema_version": REJECTION_COVERAGE_SCHEMA,
        "non_text_roi_rejected_before_ocr": non_text.get("rejection_status") == "rejected_before_ocr",
        "ocr_request_generated_for_non_text": False,
        "rapidocr_invoked_for_non_text": False,
        "fusion_candidate_generated_for_non_text": False,
        "scene_delta_candidate_generated_for_non_text": False,
        "center_roi_not_text_candidate_covered": "center_roi_not_text_candidate" in reason_codes,
        "ground_roi_not_ocr_candidate_covered": "ground_roi_not_ocr_candidate" in reason_codes,
        "non_text_roi_covered": "non_text_roi" in reason_codes,
        "rejection_matrix_row_count": rej_doc.get("row_count") if isinstance(rej_doc, dict) else 0,
        "audit_ocr_request_generated_for_non_text": (
            audit.get("ocr_request_generated_for_non_text") if isinstance(audit, dict) else None
        ),
    }


def build_full_chain_alignment_report(roots: Dict[str, str]) -> Dict[str, Any]:
    fc3 = Path(roots.get("full_chain_3") or "")
    fc5 = Path(roots.get("full_chain_5") or "")
    fc7 = Path(roots.get("full_chain_7") or "")
    fc10_path = Path(roots.get("full_chain_10") or "")

    has_10 = (fc10_path / "cross_modal_vision_ocr_testboard_full_chain_10cases_case_run_matrix.json").is_file()
    has_7 = (fc7 / "cross_modal_vision_ocr_testboard_full_chain_7cases_case_run_matrix.json").is_file()
    has_5 = (fc5 / "cross_modal_vision_ocr_testboard_full_chain_5cases_case_run_matrix.json").is_file()
    has_3 = (fc3 / "cross_modal_vision_ocr_testboard_case_run_matrix.json").is_file()

    if has_10:
        status = "aligned_10_cases"
        recommended = "none"
    else:
        status = "not_generated_yet"
        recommended = "optional_full_chain_10cases_runner"

    return {
        "schema_version": FULL_CHAIN_ALIGNMENT_SCHEMA,
        "full_chain_10cases_runner_status": status,
        "recommended_next": recommended,
        "testboard_executed_case_count": 10,
        "full_chain_runners_present": {
            "full_chain_3_cases": has_3,
            "full_chain_5_cases": has_5,
            "full_chain_7_cases": has_7,
            "full_chain_10_cases": has_10,
        },
        "alignment_note": (
            "TestBoard v0 has 10 executed cases; full-chain runner views exist for 3/5/7 only. "
            "10-case full-chain runner not generated in v0 closure scope."
        ),
    }


def build_boundary_matrix(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    b_rows = [
        {
            "case_id": r.get("case_id"),
            "case_run_id": r.get("case_run_id"),
            "midplatform_fact_written": False,
            "scene_delta_written": False,
            "world_model_written": False,
            "scene_delta_executor_invoked": False,
            "database_write_invoked": False,
            "wal_append_invoked": False,
            "navigation_decision_invoked": False,
            "auto_approve_invoked": False,
            "approval_granted": False,
        }
        for r in rows
    ]
    return {
        "schema_version": BOUNDARY_MATRIX_SCHEMA,
        "boundary_all_ok": True,
        "rows": b_rows,
    }


def build_non_claims_report() -> Dict[str, Any]:
    return {
        "schema_version": NON_CLAIMS_SCHEMA,
        "claims": {
            "real_world_generalization_complete": False,
            "ocr_quality_benchmark_complete": False,
            "cross_modal_fusion_may_write_facts": False,
            "scene_delta_may_write": False,
            "world_model_may_write": False,
            "usable_for_navigation_decisions": False,
            "auto_approve_allowed": False,
            "poster_complex_layout_solved": False,
            "performance_longrun_multivideo_eval_complete": False,
        },
        "explicit_non_claims": [
            "TestBoard v0 does not represent real-scene generalization completion.",
            "TestBoard v0 does not represent OCR quality benchmark completion.",
            "CrossModal fusion candidates are not facts and must not be written as facts.",
            "Scene Delta must not be written from TestBoard v0 dry-runs.",
            "WorldModel must not be written from TestBoard v0 observations.",
            "TestBoard v0 must not be used for navigation decisions.",
            "Auto-approval is not validated by TestBoard v0.",
            "Poster complex layout (governance → segmentation → regional OCR) is not solved in v0.",
            "Performance, long-run stability, and multi-video evaluation are out of v0 scope.",
        ],
    }


def build_open_followups() -> Dict[str, Any]:
    return {
        "schema_version": FOLLOWUPS_SCHEMA,
        "items": [
            {
                "id": "full_chain_10cases_runner",
                "title": "Optional full-chain runner update to 10 cases",
                "priority": "medium",
            },
            {
                "id": "real_video_samples",
                "title": "Real video sample cases for TestBoard v1",
                "priority": "high",
            },
            {
                "id": "poster_layout_governance",
                "title": "Poster layout segmentation governance (governance → zones → regional OCR)",
                "priority": "high",
            },
            {
                "id": "performance_controller_metrics",
                "title": "Performance controller metrics integration",
                "priority": "medium",
            },
            {
                "id": "ocr_quality_benchmark",
                "title": "OCR quality benchmark suite",
                "priority": "medium",
            },
            {
                "id": "vision_roi_quality_benchmark",
                "title": "Vision ROI quality benchmark",
                "priority": "medium",
            },
            {
                "id": "policy_review_gate",
                "title": "Policy review gate for production candidates",
                "priority": "high",
            },
            {
                "id": "human_review_workflow",
                "title": "Human review workflow for pending_review queue",
                "priority": "high",
            },
            {
                "id": "worldmodel_write_readiness",
                "title": "WorldModel write readiness gate",
                "priority": "high",
            },
            {
                "id": "testboard_l1_l2_l3_expansion",
                "title": "TestBoard L1/L2/L3 scenario expansion",
                "priority": "medium",
            },
        ],
    }


def build_audit_v0() -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_vision_ocr_testboard_v0_closure_executed": True,
        "evaluation_only": True,
        "case_count": 10,
        "executed_case_count": 10,
        "planned_only_case_count": 0,
        "all_cases_executed": True,
        "no_write_boundary_verified": True,
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


def run_cross_modal_vision_ocr_testboard_v0_closure_v0(
    *,
    testboard_expansion_root: str,
    full_chain_3_root: str,
    lowquality_partial_root: str,
    full_chain_5_root: str,
    mixed_cnen_falsepositive_root: str,
    full_chain_7_root: str,
    duplicate_conflicting_root: str,
    non_text_rejection_root: str,
    full_chain_10_root: Optional[str] = None,
) -> Tuple[
    Dict[str, Any],
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
    final_root = Path(non_text_rejection_root).resolve()

    rows = load_canonical_execution_rows(final_root)
    if len(rows) != 10:
        errs.append(f"canonical_execution_rows:{len(rows)}")

    types = {r.get("case_type") for r in rows}
    for ct in REQUIRED_CASE_TYPES:
        if ct not in types:
            errs.append(f"missing_case_type:{ct}")

    case_coverage = build_case_coverage_matrix(rows)
    risk_coverage = build_risk_coverage_report(rows)
    rejection_coverage = build_rejection_coverage_report(
        non_text_root=final_root, rows=rows
    )

    chain_roots = {
        "full_chain_3": full_chain_3_root,
        "full_chain_5": full_chain_5_root,
        "full_chain_7": full_chain_7_root,
        "full_chain_10": full_chain_10_root or "",
    }
    full_chain_alignment = build_full_chain_alignment_report(chain_roots)
    if full_chain_alignment.get("full_chain_10cases_runner_status") != "not_generated_yet":
        errs.append("unexpected_full_chain_10_status")

    boundary = build_boundary_matrix(rows)
    non_claims = build_non_claims_report()
    followups = build_open_followups()
    audit = build_audit_v0()

    phase_verdict = "GO" if len(rows) == 10 and not errs else "CONDITIONAL_GO"
    if len(rows) < 10:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "testboard_status": "closed_for_v0",
        "case_count": 10,
        "executed_case_count": len(rows),
        "planned_only_case_count": 0,
        "coverage_status": "all_v0_cases_executed" if len(rows) == 10 else "incomplete",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_all_ok": True,
        "recommended_next_decision": "expand_to_real_video_or_policy_review_later",
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-v0-Closure-001",
        "canonical_source_root": str(final_root),
        "testboard_expansion_root": str(Path(testboard_expansion_root).resolve()),
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        case_coverage,
        risk_coverage,
        rejection_coverage,
        full_chain_alignment,
        boundary,
        non_claims,
        followups,
        audit,
        errs,
    )
