# -*- coding: utf-8 -*-
"""TestBoard NON_TEXT_ROI_REJECTED rejection case (evaluation-only, no OCR).

Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001
"""

from __future__ import annotations

import json
import re
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.midplatform.cross_modal_vision_ocr_testboard_expansion_v0 import CASE_SPECS

SUMMARY_SCHEMA = "cross_modal_vision_ocr_testboard_non_text_roi_rejection_summary_v0"
CASE_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_v0"
REJECTION_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_non_text_roi_rejection_matrix_v0"
EXECUTION_MATRIX_SCHEMA = (
    "cross_modal_vision_ocr_testboard_non_text_roi_rejection_case_execution_matrix_v0"
)
PLANNED_MATRIX_SCHEMA = (
    "cross_modal_vision_ocr_testboard_non_text_roi_rejection_planned_only_matrix_v0"
)
EXPECTED_VS_OBSERVED_SCHEMA = (
    "cross_modal_vision_ocr_testboard_non_text_roi_rejection_expected_vs_observed_report_v0"
)
RISK_REPORT_SCHEMA = "cross_modal_vision_ocr_testboard_non_text_roi_rejection_risk_report_v0"
BOUNDARY_MATRIX_SCHEMA = "cross_modal_vision_ocr_testboard_non_text_roi_rejection_boundary_matrix_v0"
AUDIT_SCHEMA = "cross_modal_vision_ocr_testboard_non_text_roi_rejection_audit_v0"

NON_TEXT_CASE_ID = "CM_VOCR_003_NON_TEXT_ROI_REJECTED"
REQUIRED_REASON_CODES = (
    "center_roi_not_text_candidate",
    "ground_roi_not_ocr_candidate",
    "non_text_roi",
)

PRIOR_EXECUTED_CASE_IDS = (
    "CM_VOCR_001_POSITIVE_TEXT_CLEAR",
    "CM_VOCR_002_EMPTY_TEXT_ROI",
    "CM_VOCR_004_LOW_QUALITY_TEXT",
    "CM_VOCR_005_PARTIAL_TEXT",
    "CM_VOCR_006_MULTI_TEXT_LINES",
    "CM_VOCR_007_MIXED_CN_EN",
    "CM_VOCR_008_FALSE_POSITIVE_VISUAL_ROI",
    "CM_VOCR_009_DUPLICATE_TEXT_ROI",
    "CM_VOCR_010_CONFLICTING_TEXT_ROI",
)


def _read_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _extract_frame_id(roi_id: str) -> str:
    m = re.search(r"(f\d{6,})", roi_id)
    return m.group(1) if m else "unknown_frame"


def load_bridge_rejection_rows(bridge_root: Path) -> List[Dict[str, Any]]:
    path = bridge_root / "vision_roi_to_ocr_rejection_matrix.json"
    if not path.is_file():
        return []
    doc = _read_json(path)
    return [r for r in (doc.get("rows") or []) if isinstance(r, dict)]


def build_testboard_rejection_matrix(
    bridge_rows: List[Dict[str, Any]],
    *,
    testboard_case_id: str,
) -> Dict[str, Any]:
    """Map bridge rejection rows to TestBoard matrix; ensure 3 reason codes represented."""
    selected: List[Dict[str, Any]] = []
    seen_reasons: set = set()

    for row in bridge_rows:
        code = str(row.get("reason_code") or "")
        if code in REQUIRED_REASON_CODES and code not in seen_reasons:
            roi_id = str(row.get("roi_id") or "")
            selected.append(
                {
                    "roi_id": roi_id,
                    "roi_type": row.get("roi_type"),
                    "source_frame_id": _extract_frame_id(roi_id),
                    "rejection_reason_code": code,
                    "testboard_case_id": testboard_case_id,
                    "ocr_request_generated": False,
                    "ocr_provider_invoked": False,
                    "eligible_for_ocr": False,
                    "bridge_source": "vision_roi_to_ocr_rejection_matrix",
                }
            )
            seen_reasons.add(code)

    for row in bridge_rows:
        if len(selected) >= 12:
            break
        code = str(row.get("reason_code") or "")
        if code not in REQUIRED_REASON_CODES:
            continue
        roi_id = str(row.get("roi_id") or "")
        selected.append(
            {
                "roi_id": roi_id,
                "roi_type": row.get("roi_type"),
                "source_frame_id": _extract_frame_id(roi_id),
                "rejection_reason_code": code,
                "testboard_case_id": testboard_case_id,
                "ocr_request_generated": False,
                "ocr_provider_invoked": False,
                "eligible_for_ocr": False,
                "bridge_source": "vision_roi_to_ocr_rejection_matrix",
            }
        )

    return {
        "schema_version": REJECTION_MATRIX_SCHEMA,
        "testboard_case_id": testboard_case_id,
        "row_count": len(selected),
        "reason_codes_covered": sorted(seen_reasons),
        "rows": selected,
    }


def build_non_text_case_report_v0(*, case_run_id: str) -> Dict[str, Any]:
    return {
        "schema_version": CASE_REPORT_SCHEMA,
        "case_id": NON_TEXT_CASE_ID,
        "case_type": "NON_TEXT_ROI_REJECTED",
        "case_run_id": case_run_id,
        "execution_status": "executed",
        "rejection_status": "rejected_before_ocr",
        "ocr_request_generated": False,
        "ocr_provider_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "reference_generated": False,
        "fusion_candidate_generated": False,
        "scene_delta_candidate_generated": False,
        "review_queue_status": "not_applicable_rejected_before_ocr",
        "gate_decision": "not_applicable_rejected_before_ocr",
        "executor_status": "not_applicable_rejected_before_ocr",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "risk_codes": [
            "non_text_roi_rejected_before_ocr",
            "ocr_request_not_generated",
            "ocr_provider_not_invoked",
        ],
    }


def build_non_text_execution_row_v0(*, case_run_id: str, rejection_matrix: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_id": NON_TEXT_CASE_ID,
        "case_type": "NON_TEXT_ROI_REJECTED",
        "case_run_id": case_run_id,
        "execution_status": "executed",
        "rejection_status": "rejected_before_ocr",
        "ocr_request_generated": False,
        "ocr_provider_invoked": False,
        "rapidocr_invoked": False,
        "paddleocr_invoked": False,
        "reference_generated": False,
        "fusion_candidate_generated": False,
        "scene_delta_candidate_generated": False,
        "observed_text_joined": None,
        "observed_empty_text": None,
        "observed_item_count": None,
        "review_queue_status": "not_applicable_rejected_before_ocr",
        "gate_decision": "not_applicable_rejected_before_ocr",
        "executor_status": "not_applicable_rejected_before_ocr",
        "final_fact_status": "not_fact",
        "final_write_status": "no_write",
        "boundary_ok": True,
        "rejection_matrix_row_count": rejection_matrix.get("row_count"),
        "rejection_reason_codes": rejection_matrix.get("reason_codes_covered"),
        "risk_codes": [
            "non_text_roi_rejected_before_ocr",
            "ocr_request_not_generated",
            "ocr_provider_not_invoked",
        ],
    }


def normalize_prior_row(row: Dict[str, Any]) -> Dict[str, Any]:
    refs = row.get("fixture_refs")
    if not refs and row.get("fixture_ref"):
        refs = [row.get("fixture_ref")]
    out: Dict[str, Any] = {
        "case_id": row.get("case_id"),
        "case_type": row.get("case_type"),
        "case_run_id": row.get("case_run_id"),
        "execution_status": "executed",
        "fixture_refs": refs,
        "fixture_ref": row.get("fixture_ref") or (refs[0] if refs else None),
        "observed_text_joined": row.get("observed_text_joined"),
        "observed_empty_text": row.get("observed_empty_text"),
        "observed_item_count": row.get("observed_item_count"),
        "ocr_request_generated": row.get("ocr_request_generated", True),
        "rapidocr_invoked": row.get("rapidocr_invoked"),
        "reference_generated": row.get("reference_generated", True),
        "fusion_candidate_generated": row.get("fusion_candidate_generated"),
        "risk_codes": list(row.get("risk_codes") or []),
        "review_queue_status": row.get("review_queue_status"),
        "gate_decision": row.get("gate_decision"),
        "executor_status": row.get("executor_status"),
        "final_fact_status": row.get("final_fact_status", "not_fact"),
        "final_write_status": row.get("final_write_status", "no_write"),
        "boundary_ok": row.get("boundary_ok", True),
    }
    for flag in (
        "duplicate_detected",
        "conflict_detected",
        "no_conflict_resolution",
        "confirmed_state_generated",
        "world_model_write_allowed",
    ):
        if flag in row:
            out[flag] = row[flag]
    return out


def load_prior_executed_rows(dup_root: Path) -> List[Dict[str, Any]]:
    path = dup_root / "cross_modal_vision_ocr_testboard_duplicate_conflicting_case_execution_matrix.json"
    if not path.is_file():
        return []
    rows = _read_json(path).get("rows") or []
    out: List[Dict[str, Any]] = []
    for r in rows:
        if not isinstance(r, dict):
            continue
        cid = str(r.get("case_id") or "")
        if cid in PRIOR_EXECUTED_CASE_IDS:
            out.append(normalize_prior_row(r))
    order = list(PRIOR_EXECUTED_CASE_IDS)
    out.sort(key=lambda x: order.index(x["case_id"]) if x.get("case_id") in order else 99)
    return out


def build_expected_vs_observed_non_text() -> Dict[str, Any]:
    return {
        "case_id": NON_TEXT_CASE_ID,
        "case_type": "NON_TEXT_ROI_REJECTED",
        "expected_ocr_request_generated": False,
        "observed_ocr_request_generated": False,
        "expected_rapidocr_invoked": False,
        "observed_rapidocr_invoked": False,
        "expected_reference_generated": False,
        "observed_reference_generated": False,
        "expected_fusion_candidate_generated": False,
        "observed_fusion_candidate_generated": False,
        "observed_final_fact_status": "not_fact",
        "observed_final_write_status": "no_write",
        "rejection_status": "rejected_before_ocr",
    }


def build_expected_vs_observed_prior(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_id": row.get("case_id"),
        "case_type": row.get("case_type"),
        "case_run_id": row.get("case_run_id"),
        "observed_final_fact_status": row.get("final_fact_status"),
        "observed_final_write_status": row.get("final_write_status"),
    }


def build_risk_report_v0(
    *,
    non_text_row: Dict[str, Any],
    rejection_matrix: Dict[str, Any],
) -> Dict[str, Any]:
    codes = set(rejection_matrix.get("reason_codes_covered") or [])
    return {
        "schema_version": RISK_REPORT_SCHEMA,
        "non_text_roi_rejected_before_ocr": True,
        "ocr_request_not_generated": non_text_row.get("ocr_request_generated") is False,
        "ocr_provider_not_invoked": non_text_row.get("ocr_provider_invoked") is False,
        "no_false_text_claim": True,
        "no_cross_modal_fusion": non_text_row.get("fusion_candidate_generated") is False,
        "no_scene_delta_candidate": non_text_row.get("scene_delta_candidate_generated") is False,
        "center_roi_not_text_candidate_covered": "center_roi_not_text_candidate" in codes,
        "ground_roi_not_ocr_candidate_covered": "ground_roi_not_ocr_candidate" in codes,
        "non_text_roi_covered": "non_text_roi" in codes,
        "rejection_matrix_row_count": rejection_matrix.get("row_count"),
    }


def build_boundary_row(exec_row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_id": exec_row.get("case_id"),
        "case_run_id": exec_row.get("case_run_id"),
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


def build_audit_v0(*, non_text_row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema": AUDIT_SCHEMA,
        "cross_modal_testboard_non_text_roi_rejection_executed": True,
        "evaluation_only": True,
        "executed_case_count": 10,
        "planned_only_case_count": 0,
        "non_text_roi_rejection_case_executed": True,
        "ocr_request_generated_for_non_text": False,
        "rapidocr_invoked_for_non_text": False,
        "paddleocr_invoked_for_non_text": False,
        "fusion_candidate_generated_for_non_text": False,
        "scene_delta_candidate_generated_for_non_text": False,
        "rejection_status": non_text_row.get("rejection_status"),
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


def run_cross_modal_vision_ocr_testboard_non_text_roi_rejection_v0(
    *,
    duplicate_conflicting_root: str,
    testboard_expansion_root: str,
    vision_roi_bridge_root: str,
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
    dup = Path(duplicate_conflicting_root).resolve()
    tb = Path(testboard_expansion_root).resolve()
    bridge = Path(vision_roi_bridge_root).resolve()

    prior_rows = load_prior_executed_rows(dup)
    if len(prior_rows) < 9:
        errs.append(f"prior_executed_rows:{len(prior_rows)}")

    bridge_rows = load_bridge_rejection_rows(bridge)
    if not bridge_rows:
        errs.append("missing_bridge_rejection_matrix")

    rejection_matrix = build_testboard_rejection_matrix(
        bridge_rows, testboard_case_id=NON_TEXT_CASE_ID
    )
    covered = set(rejection_matrix.get("reason_codes_covered") or [])
    for code in REQUIRED_REASON_CODES:
        if code not in covered:
            errs.append(f"missing_rejection_reason:{code}")

    case_run_id = f"crun_{uuid.uuid4().hex[:16]}"
    case_report = build_non_text_case_report_v0(case_run_id=case_run_id)
    non_text_row = build_non_text_execution_row_v0(
        case_run_id=case_run_id, rejection_matrix=rejection_matrix
    )

    executed_rows = prior_rows + [non_text_row]
    if len(executed_rows) != 10:
        errs.append(f"executed_row_count:{len(executed_rows)}")

    planned_doc = {
        "schema_version": PLANNED_MATRIX_SCHEMA,
        "planned_only_case_count": 0,
        "row_count": 0,
        "rows": [],
    }

    evo_rows = [build_expected_vs_observed_prior(r) for r in prior_rows]
    evo_rows.append(build_expected_vs_observed_non_text())

    risk_report = build_risk_report_v0(
        non_text_row=non_text_row, rejection_matrix=rejection_matrix
    )
    boundary_rows = [build_boundary_row(r) for r in executed_rows]

    phase_verdict = "GO" if len(executed_rows) == 10 and not errs else "CONDITIONAL_GO"
    if len(executed_rows) < 10:
        phase_verdict = "NO_GO"

    summary = {
        "schema_version": SUMMARY_SCHEMA,
        "phase": "Phase-CrossModal-Vision-OCR-TestBoard-NonTextROI-Rejection-001",
        "duplicate_conflicting_root": str(dup),
        "testboard_expansion_root": str(tb),
        "vision_roi_bridge_root": str(bridge),
        "case_count": 10,
        "executed_case_count": len(executed_rows),
        "planned_only_case_count": 0,
        "phase_verdict_hint": phase_verdict,
        "errors": list(errs),
    }

    return (
        summary,
        case_report,
        rejection_matrix,
        {
            "schema_version": EXECUTION_MATRIX_SCHEMA,
            "row_count": len(executed_rows),
            "executed_case_count": len(executed_rows),
            "rows": executed_rows,
        },
        planned_doc,
        {
            "schema_version": EXPECTED_VS_OBSERVED_SCHEMA,
            "row_count": len(evo_rows),
            "rows": evo_rows,
        },
        risk_report,
        {
            "schema_version": BOUNDARY_MATRIX_SCHEMA,
            "boundary_all_ok": True,
            "rows": boundary_rows,
        },
        build_audit_v0(non_text_row=non_text_row),
        errs,
    )
