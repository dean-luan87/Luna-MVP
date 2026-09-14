# -*- coding: utf-8 -*-
"""Real model field construction hardening result assembler v1."""

from __future__ import annotations

import uuid
from typing import Any, Dict, List

from capabilities.midplatform.field_construction_failure_localizer_v1 import (
    localize_failure_points,
    summarize_recommended_fix_areas,
)


def _stability_status(
    *,
    dryrun_result: Dict[str, Any],
    hardening_case: Dict[str, Any],
    quality_assessment: Dict[str, Any],
) -> Dict[str, Any]:
    status = dryrun_result.get("success_path_status", "")
    expected = hardening_case.get("expected_success_path_status")
    unstable: List[str] = []
    if expected and status != expected and not hardening_case.get("allow_status_family"):
        unstable.append(f"status_mismatch_expected_{expected}_got_{status}")
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    asm = dryrun_result.get("field_assembly_result_candidate") or {}
    entities = scene.get("entity_candidates") or asm.get("enhanced_entity_candidates") or []
    if hardening_case.get("expect_entity_count") is not None:
        if len(entities) != hardening_case["expect_entity_count"]:
            unstable.append("entity_count_unstable")
    exec_boundary = dryrun_result.get("execution_boundary_summary") or {}
    if hardening_case.get("expect_mock_depth") and exec_boundary.get("depth_execution_mode") != "mock_adapter_with_real_frame_alignment":
        unstable.append("mock_depth_mode_not_distinguished")
    if hardening_case.get("expect_real_adapter") and exec_boundary.get("depth_execution_mode") != "real_adapter":
        unstable.append("real_adapter_mode_not_distinguished")

    if unstable:
        stab = "unstable"
    elif hardening_case.get("case_category") == "failure":
        stab = "not_applicable"
    else:
        stab = "stable" if quality_assessment.get("quality_score_discrete") in ("strong", "usable", "degraded_usable") else "mostly_stable"

    return {
        "stability_status": stab,
        "unstable_points": unstable,
        "repeatability_notes": hardening_case.get("repeatability_notes", "upstream_dryrun_artifact_reused_no_model_rerun"),
    }


def _explainability_status(dryrun_result: Dict[str, Any]) -> Dict[str, Any]:
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}
    trace = dryrun_result.get("traceability_refs") or []
    missing: List[str] = []
    for ref_key in ("frame_input_ref", "yolo_output_ref"):
        if not dryrun_result.get(ref_key):
            missing.append(f"missing_{ref_key}")
    if len(trace) < 3:
        missing.append("traceability_refs_incomplete")
    entities = scene.get("entity_candidates") or []
    asm = dryrun_result.get("field_assembly_result_candidate") or {}
    entities = entities or asm.get("enhanced_entity_candidates") or []
    for ent in entities:
        if not ent.get("source_refs") and not ent.get("observation_ref"):
            missing.append("entity_source_refs_missing")
            break
    degradation = dryrun_result.get("degradation_summary") or {}
    if degradation.get("degraded") and not (dryrun_result.get("warning_summary") or {}).get("warnings"):
        missing.append("degradation_without_warning")

    if not missing:
        status = "complete"
    elif len(missing) <= 2:
        status = "partial"
    else:
        status = "incomplete"

    reason_coverage = len(dryrun_result.get("missing_information") or []) + len(
        (dryrun_result.get("warning_summary") or {}).get("warnings") or []
    )
    return {
        "explainability_status": status,
        "missing_explanation_points": missing,
        "reason_code_coverage": reason_coverage,
    }


def assemble_hardened_field_construction_result(
    *,
    hardening_case: Dict[str, Any],
    dryrun_result: Dict[str, Any],
    quality_assessment: Dict[str, Any],
    reusable_case: Dict[str, Any] | None,
) -> Dict[str, Any]:
    warnings = (dryrun_result.get("warning_summary") or {}).get("warnings") or []
    failure_points = list(dryrun_result.get("failure_points") or [])
    localized = localize_failure_points(
        failure_points=failure_points,
        warnings=warnings,
        success_path_status=dryrun_result.get("success_path_status", ""),
    )
    stability = _stability_status(
        dryrun_result=dryrun_result, hardening_case=hardening_case, quality_assessment=quality_assessment,
    )
    explain = _explainability_status(dryrun_result)
    scene = dryrun_result.get("enhanced_field_scene_candidate") or {}

    reusability_status = "not_reusable"
    if reusable_case:
        if reusable_case.get("case_type") == "success_baseline":
            reusability_status = "reusable"
        elif reusable_case.get("case_type") == "degraded_baseline":
            reusability_status = "reusable_degraded"
        elif reusable_case.get("case_type") == "failure_localization_baseline":
            reusability_status = "failure_baseline"

    quality_status = quality_assessment.get("quality_score_discrete", "weak")
    readiness_core = (
        stability["stability_status"] in ("stable", "mostly_stable")
        and explain["explainability_status"] in ("complete", "partial")
        and reusability_status in ("reusable", "reusable_degraded")
        and quality_status in ("strong", "usable", "degraded_usable")
    )
    readiness_sim = (
        readiness_core
        and quality_status in ("strong", "usable", "degraded_usable")
        and "field_simulation_planning" in (reusable_case or {}).get("reusable_for", [])
    )

    return {
        "hardened_result_id": f"hfc_{uuid.uuid4().hex[:12]}",
        "source_dryrun_result_ref": dryrun_result.get("dryrun_result_id"),
        "enhanced_field_scene_ref": scene.get("field_scene_id"),
        "success_path_status": dryrun_result.get("success_path_status"),
        "stability_status": stability["stability_status"],
        "explainability_status": explain["explainability_status"],
        "reusability_status": reusability_status,
        "quality_status": quality_status,
        "localized_failure_points": localized,
        "warning_summary": dryrun_result.get("warning_summary"),
        "missing_information": dryrun_result.get("missing_information") or [],
        "recommended_fix_areas": summarize_recommended_fix_areas(localized),
        "stability_detail": stability,
        "explainability_detail": explain,
        "readiness_for_core_success_path": readiness_core,
        "readiness_for_field_simulation_planning": readiness_sim,
        "hardening_case_id": hardening_case.get("case_id"),
        "source_case_id": hardening_case.get("source_case_id"),
        "candidate_only": True,
    }
