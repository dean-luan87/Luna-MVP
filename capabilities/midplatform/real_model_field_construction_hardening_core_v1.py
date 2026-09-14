# -*- coding: utf-8 -*-
"""Real model field construction hardening core v1."""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from capabilities.midplatform.field_construction_reusable_case_builder_v1 import (
    build_reusable_field_construction_case,
)
from capabilities.midplatform.field_construction_success_path_quality_assessor_v1 import (
    assess_success_path_quality,
)
from capabilities.midplatform.real_model_field_construction_hardening_result_assembler_v1 import (
    assemble_hardened_field_construction_result,
)
from capabilities.midplatform.real_model_field_construction_hardening_static_validators_v1 import (
    validate_hardened_result,
    validate_quality_assessment,
    validate_reusable_case,
)


def _index_dryrun_results(
    dryrun_results: List[Dict[str, Any]],
    case_results: List[Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    by_source: Dict[str, Dict[str, Any]] = {}
    case_status = {r["case_id"]: r for r in case_results}
    for dr in dryrun_results:
        dryrun_id = dr.get("dryrun_result_id", "")
        for cid, row in case_status.items():
            frame_ref = dr.get("frame_input_ref", "")
            if frame_ref == f"rfi_{cid}":
                by_source[cid] = dr
                break
    return by_source


def _evaluate_hardening_case(
    hardening_case: Dict[str, Any],
    hardened: Dict[str, Any],
    quality: Dict[str, Any],
    reusable: Dict[str, Any] | None,
) -> bool:
    if hardening_case.get("optional_meta"):
        return True

    expected_status = hardening_case.get("expected_success_path_status")
    if expected_status and not hardening_case.get("allow_status_family"):
        if hardened.get("success_path_status") != expected_status:
            return False
    elif hardening_case.get("allow_status_family"):
        family = hardening_case["allow_status_family"]
        if not str(hardened.get("success_path_status", "")).startswith(family):
            return False

    if hardening_case.get("expect_entity_count") is not None:
        scene_ref = hardened.get("enhanced_field_scene_ref")
        if scene_ref is None and hardening_case.get("case_category") != "failure":
            return False

    if hardening_case.get("expect_localization_area"):
        areas = [lp.get("recommended_fix_area") for lp in hardened.get("localized_failure_points") or []]
        if hardening_case["expect_localization_area"] not in areas:
            if hardening_case.get("case_category") == "failure" and not areas:
                return hardened.get("success_path_status", "").startswith("failed")
            if hardening_case["expect_localization_area"] not in areas:
                return False

    if hardening_case.get("expect_invalid_bbox_localized"):
        localized = hardened.get("localized_failure_points") or []
        if not any(lp.get("pattern_matched") == "invalid_bbox" for lp in localized):
            return False
        if reusable and reusable.get("case_type") != "failure_localization_baseline":
            return False
        return True

    if hardening_case.get("expect_traceability_min"):
        dr_refs = hardened.get("explainability_detail", {})
        if hardened.get("explainability_status") == "incomplete":
            return False

    if hardening_case.get("expect_quality_summaries"):
        for key in ("scene_quality_status", "depth_quality_status", "geometry_quality_status", "zone_summary_status"):
            if quality.get(key) != "complete":
                return False

    valid_h, _ = validate_hardened_result(hardened)
    valid_q, _ = validate_quality_assessment(quality)
    if not valid_h or not valid_q:
        return False
    if reusable:
        valid_r, _ = validate_reusable_case(reusable)
        if not valid_r:
            return False

    if hardening_case.get("case_category") == "pass":
        if hardened.get("reusability_status") not in ("reusable",):
            return False
    if hardening_case.get("case_category") == "degraded":
        if reusable and not reusable.get("limitations"):
            return False
    if hardening_case.get("case_category") == "failure":
        if hardened.get("reusability_status") != "failure_baseline" and reusable:
            if reusable.get("case_type") != "failure_localization_baseline":
                return False

    return True


def run_hardening_case(
    hardening_case: Dict[str, Any],
    dryrun_result: Dict[str, Any],
) -> Dict[str, Any]:
    enriched = dict(dryrun_result)
    extra_warnings: List[str] = []
    for aligned in dryrun_result.get("aligned_observation_candidates") or []:
        extra_warnings.extend(aligned.get("warning_codes") or [])
        extra_warnings.extend(aligned.get("degradation_reason_codes") or [])
    if extra_warnings:
        ws = dict(enriched.get("warning_summary") or {"warnings": [], "warning_count": 0})
        merged = sorted(set((ws.get("warnings") or []) + extra_warnings))
        enriched["warning_summary"] = {"warnings": merged, "warning_count": len(merged)}

    quality = assess_success_path_quality(dryrun_result=enriched)
    reusable = build_reusable_field_construction_case(
        hardening_case_id=hardening_case["case_id"],
        source_case_id=hardening_case["source_case_id"],
        dryrun_result=enriched,
        quality_assessment=quality,
    )
    hardened = assemble_hardened_field_construction_result(
        hardening_case=hardening_case,
        dryrun_result=enriched,
        quality_assessment=quality,
        reusable_case=reusable,
    )
    passed = _evaluate_hardening_case(hardening_case, hardened, quality, reusable)
    return {
        "case_id": hardening_case["case_id"],
        "source_case_id": hardening_case["source_case_id"],
        "case_passed": passed,
        "hardened_result": hardened,
        "quality_assessment": quality,
        "reusable_case": reusable,
    }


def run_all_hardening_cases(
    *,
    hardening_cases: Tuple[Dict[str, Any], ...],
    dryrun_results: List[Dict[str, Any]],
    case_results: List[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], bool]:
    indexed = _index_dryrun_results(dryrun_results, case_results)
    results: List[Dict[str, Any]] = []
    all_passed = True
    for hc in hardening_cases:
        dr = indexed.get(hc["source_case_id"])
        if not dr:
            results.append({
                "case_id": hc["case_id"],
                "source_case_id": hc["source_case_id"],
                "case_passed": False,
                "error": "source_dryrun_result_not_found",
            })
            all_passed = False
            continue
        row = run_hardening_case(hc, dr)
        results.append(row)
        if not row.get("case_passed") and not hc.get("optional_meta"):
            all_passed = False
    return results, all_passed
