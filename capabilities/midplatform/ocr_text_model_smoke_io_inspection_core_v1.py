# -*- coding: utf-8 -*-
"""OCR / Text Model smoke IO inspection core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.ocr_text_candidate_mapping_reviewer_v1 import (
    review_ocr_text_candidate_mapping_feasibility,
)
from capabilities.midplatform.ocr_text_io_inspector_v1 import inspect_ocr_text_model_io
from capabilities.midplatform.ocr_text_model_smoke_io_inspection_items_v1 import DEFAULT_OCR_TEXT_AVAILABILITY
from capabilities.midplatform.ocr_text_model_smoke_io_inspection_static_validators_v1 import (
    validate_mapping_feasibility_candidate,
    validate_model_io_inspection_candidate,
    validate_model_smoke_run_candidate,
)
from capabilities.midplatform.ocr_text_model_smoke_runner_v1 import run_ocr_text_model_smoke


def run_smoke_io_case(
    case: Dict[str, Any],
    *,
    matrix: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    case_id = case["case_id"]
    base_matrix = dict(matrix or DEFAULT_OCR_TEXT_AVAILABILITY)
    overrides = dict(case.get("availability_override") or {})
    subtype = case.get("inspect_subtype", "ocr")
    focus = case.get("expect_mapping_target")

    smoke_run, auth, warnings, failure_points = run_ocr_text_model_smoke(
        case_id=case_id,
        matrix=base_matrix,
        case_overrides=overrides,
        inspect_subtype=subtype,
    )
    validate_model_smoke_run_candidate(smoke_run)
    io_inspection = inspect_ocr_text_model_io(smoke_run=smoke_run)
    validate_model_io_inspection_candidate(io_inspection)
    mappings = review_ocr_text_candidate_mapping_feasibility(
        smoke_run=smoke_run, io_inspection=io_inspection, focus_target=focus,
    )
    for m in mappings:
        validate_mapping_feasibility_candidate(m)

    traceability_refs = (
        smoke_run.get("input_refs", [])
        + smoke_run.get("output_refs", [])
        + [smoke_run.get("smoke_run_id"), io_inspection.get("io_inspection_id")]
        + [m.get("mapping_feasibility_id") for m in mappings]
    )
    return {
        "case_id": case_id,
        "case_passed": False,
        "smoke_run": smoke_run,
        "authorization_candidate": auth,
        "io_inspection": io_inspection,
        "mapping_feasibilities": mappings,
        "traceability_refs": [r for r in traceability_refs if r],
        "warnings": warnings,
        "failure_points": failure_points,
    }


def _evaluate_case(case: Dict[str, Any], row: Dict[str, Any]) -> bool:
    smoke = row.get("smoke_run") or {}
    io = row.get("io_inspection") or {}
    mappings = row.get("mapping_feasibilities") or []
    mode = smoke.get("execution_mode")
    runtime = smoke.get("runtime_environment_summary") or {}
    raw = smoke.get("_raw_output") or {}

    if case.get("expect_execution_mode") and mode != case["expect_execution_mode"]:
        return False
    if case.get("expect_smoke_completed") and smoke.get("execution_status") != "completed":
        return False
    if case.get("expect_not_real_run"):
        if mode == "cached_output" and "cached_output_inspection_not_real_run" not in (smoke.get("warning_codes") or []):
            return False
        if mode == "adapter_stub" and "adapter_stub_inspection_not_real_run" not in (smoke.get("warning_codes") or []):
            return False
    if case.get("expect_no_download"):
        if runtime.get("download_attempted") or runtime.get("dependency_install_attempted"):
            return False
        if not mode.startswith("blocked"):
            return False
    if case.get("expect_parseable") and io.get("parseability_status") not in ("parseable", "partial", "design_parseable"):
        return False
    if case.get("expect_region_output"):
        outputs = raw.get("outputs") or {}
        if not outputs.get("bbox") and not outputs.get("polygon"):
            return False
    if case.get("expect_mapping_feasible") and io.get("candidate_mapping_feasibility") != "feasible":
        return False
    if case.get("expect_mapping_target"):
        target = case["expect_mapping_target"]
        row_map = next((m for m in mappings if target in (m.get("candidate_mapping_targets") or [])), None)
        if not row_map:
            return False
        if case.get("expect_mapping_status") and row_map.get("mapping_status") != case["expect_mapping_status"]:
            return False
    if case.get("expect_traceability"):
        refs = row.get("traceability_refs") or []
        if len(refs) < 4 or not smoke.get("smoke_run_id"):
            return False
    if case.get("expect_cached_not_real"):
        if mode != "cached_output":
            return False
        if "cached_output_inspection_not_real_run" not in (smoke.get("warning_codes") or []):
            return False
    if case.get("expect_stub_not_real"):
        if mode != "adapter_stub":
            return False
        if "adapter_stub_inspection_not_real_run" not in (smoke.get("warning_codes") or []):
            return False
    if case.get("expect_new_protocol") is False:
        if any(m.get("owner_approval_required_for_new_protocol") for m in mappings):
            return False
    return True


def run_all_smoke_io_cases(
    cases: Tuple[Dict[str, Any], ...],
    *,
    matrix: Dict[str, Any] | None = None,
) -> Tuple[List[Dict[str, Any]], bool]:
    results: List[Dict[str, Any]] = []
    all_passed = True
    for case in cases:
        row = run_smoke_io_case(case, matrix=matrix)
        row["case_passed"] = _evaluate_case(case, row)
        results.append(row)
        if not row.get("case_passed"):
            all_passed = False
    return results, all_passed
