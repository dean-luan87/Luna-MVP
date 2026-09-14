# -*- coding: utf-8 -*-
"""OCR Real Dependency Execution Authorization Roadmap Decision v1 — Route A selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as EXPLANATION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_VIA_FACTORY_DR_FINAL_GO,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-Roadmap-Decision-v1-001"
SCOPE = "ocr_real_dependency_execution_authorization_roadmap_decision_only"
SOURCE_CHAIN = "ocr_real_dependency_execution_authorization_roadmap_decision_v1"

UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO
UPSTREAM_OCR_VIA_FACTORY_DR_FINAL = OCR_VIA_FACTORY_DR_FINAL_GO
UPSTREAM_EXPLANATION_DR_FINAL = EXPLANATION_DR_FINAL_GO

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_ROADMAP_DECISION_"
    "READY_FOR_EXECUTION_AUTHORIZATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Execution-Authorization-Roadmap-Issue-Review-v1-001"

ROUTE_A = "Route A — Real Dependency Check Execution Authorization Planning"
ROUTE_B = "Route B — Provider Selection Finalize"
ROUTE_C = "Route C — Validation Runtime Activation"
ROUTE_D = "Route D — Health Readiness Baseline"
ROUTE_E = "Route E — Return Visual Context Governance"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = ROUTE_B
DEFERRED_ROUTE_C = ROUTE_C
DEFERRED_ROUTE_D = ROUTE_D
DEFERRED_ROUTE_E = ROUTE_E

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_dependency_execution_authorization_planning_started_now",
    "domain_config_activated_now",
    "validation_runtime_enabled_now",
    "authorization_request_generated_now",
    "authorization_request_sent_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_selection_finalized_now",
    "controlled_trial_started_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ real dependency check authorized",
    "Route A selected ≠ package/import/cache/hash check executed",
    "execution authorization planning ≠ execution window opened",
    "domain_config candidate ≠ domain_config activated",
    "validation engineering closed ≠ validator runtime enabled",
    "next planning ≠ provider import allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "ocr_real_dependency_execution_authorization_roadmap_decision_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_real_dependency_execution_authorization_roadmap_decision_v1(
    *,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_planning_root: Optional[str] = None,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_plan_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_planning_root
        or ocr_dr_root.parent / "ocr_real_dependency_authorization_via_factory_standard_planning"
    ).expanduser().resolve()
    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or ocr_dr_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()
    explain_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
        or ocr_dr_root.parent / "midplatform_constitution_governance_explanation_dryrun_and_review"
    ).expanduser().resolve()
    harness_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or ocr_dr_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()

    val_dr_sm = _try_read_json(val_dr_root / "summary.json") or {}
    val_dr_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}

    ocr_dr_sm = _try_read_json(ocr_dr_root / "summary.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    ocr_domain_config = _try_read_json(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    ) or {}

    ocr_plan_sm = _try_read_json(ocr_plan_root / "summary.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}
    explain_vr = _try_read_json(explain_root / "verifier_report.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_validation_separation_dryrun_review_root": str(val_dr_root),
        "upstream_ocr_via_factory_dryrun_review_root": str(ocr_dr_root),
        "upstream_ocr_via_factory_planning_root": str(ocr_plan_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_root),
        "upstream_explanation_dryrun_review_root": str(explain_root),
        "upstream_harness_post_review_root": str(harness_root),
        "output_root": str(out_root),
    }

    if val_dr_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun review verifier must be GO")
    if val_dr_sm.get("final_decision") != UPSTREAM_VALIDATION_SEP_DR_FINAL:
        blockers.append("validation separation dryrun final_decision mismatch")
    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("ocr via factory dryrun review verifier must be GO")
    if ocr_dr_sm.get("final_decision") != UPSTREAM_OCR_VIA_FACTORY_DR_FINAL:
        blockers.append("ocr via factory dryrun final_decision mismatch")
    if not ocr_domain_config.get("candidate_id"):
        blockers.append("ocr_real_dependency_domain_config_candidate must exist")
    if ocr_domain_config.get("candidate_only") is not True:
        blockers.append("domain_config must be candidate_only")
    if ocr_domain_config.get("activated_now") is not False:
        blockers.append("domain_config must not be activated")
    if val_model.get("model_id") != "validation_engineering_model_v1":
        blockers.append("validation_engineering_model_candidate required")
    if val_model.get("runtime_enabled_now") is not False:
        blockers.append("validator runtime must not be enabled")
    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun review must be GO")
    if explain_vr.get("verifier") != "GO":
        blockers.append("constitution explanation dryrun review must be GO")
    if harness_vr.get("verifier") != "GO":
        blockers.append("harness post review must be GO")

    for field in (
        "grant_issued_now",
        "execution_window_opened_now",
        "real_dependency_check_executed_now",
        "provider_imported_now",
        "provider_invoked_now",
        "authorization_request_generated_now",
    ):
        if ocr_dr_sm.get(field) is True or ocr_domain_config.get(field) is True:
            blockers.append(f"{field} must be false across upstream")

    if ocr_plan_sm.get("boundary_ok") is not True:
        blockers.append("ocr via factory planning boundary_ok required")

    val_sep_input = {
        "review_id": "validation_engineering_separation_input_review_v1",
        "upstream_root": str(val_dr_root),
        "verifier_go": val_dr_vr.get("verifier") == "GO",
        "final_decision": val_dr_sm.get("final_decision"),
        "validation_engineering_model_candidate_present": bool(val_model.get("model_id")),
        "validator_runtime_enabled_now": val_model.get("runtime_enabled_now"),
        "review_pass": val_dr_vr.get("verifier") == "GO"
        and val_dr_sm.get("final_decision") == UPSTREAM_VALIDATION_SEP_DR_FINAL,
        **meta,
    }

    ocr_factory_input = {
        "review_id": "ocr_real_dep_via_factory_standard_input_review_v1",
        "upstream_dryrun_root": str(ocr_dr_root),
        "upstream_planning_root": str(ocr_plan_root),
        "verifier_go": ocr_dr_vr.get("verifier") == "GO",
        "final_decision": ocr_dr_sm.get("final_decision"),
        "domain_config_candidate_id": ocr_domain_config.get("candidate_id"),
        "candidate_only": ocr_domain_config.get("candidate_only"),
        "activated_now": ocr_domain_config.get("activated_now"),
        "selected_provider_for_execution": ocr_domain_config.get("selected_provider_for_execution"),
        "review_pass": ocr_dr_vr.get("verifier") == "GO"
        and ocr_dr_sm.get("final_decision") == UPSTREAM_OCR_VIA_FACTORY_DR_FINAL,
        **meta,
    }

    readiness_checks = {
        "domain_config_candidate_ready": ocr_domain_config.get("candidate_only") is True,
        "validation_engineering_separation_closed": val_dr_vr.get("verifier") == "GO",
        "factory_authorization_standard_available": auth_ext_vr.get("verifier") == "GO",
        "constitution_governance_explanation_available": explain_vr.get("verifier") == "GO",
        "harness_registration_closed": harness_vr.get("verifier") == "GO",
        "no_grant_or_window_yet": meta.get("grant_issued_now") is False,
        "no_real_dep_executed": meta.get("real_dependency_check_executed_now") is False,
        "selected_provider_null": meta.get("selected_provider_for_execution") is None,
    }
    readiness_review = {
        "review_id": "execution_authorization_readiness_review_v1",
        "readiness_checks": readiness_checks,
        "readiness_pass": all(readiness_checks.values()),
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_execution_authorization_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "OCR domain_config_candidate generated and passed Factory Standard / Constitution / Validation Engineering dryrun",
            "Validation Engineering separation closed — enforcement path can inspect domain_config",
            "real-dep not executed yet — next step is execution authorization planning",
            "execution authorization planning still does not equal real execution",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_provider_selection_finalize_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_after_real_dependency_evidence",
        "defer_reasons": [
            "selected_provider_for_execution=null",
            "missing real package/import/cache/hash evidence",
            "should not finalize provider before real dependency evidence",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_validation_runtime_activation_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "Validation Engineering model candidate exists but runtime not enabled",
            "authorization planning only — no global validator runtime activation needed now",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_health_readiness_baseline_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred_until_hardware_runtime_ready",
        "defer_reasons": [
            "health metrics reserved — no numeric health score invented",
            "hardware/runtime observation insufficient for baseline expansion",
            "health may inform later execution authorization risk but not now",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_return_visual_context_governance_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "deferred",
        "defer_reasons": [
            "Visual Context Governance remains important",
            "OCR real-dep execution authorization chain has conditions to proceed via Route A now",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "ocr_real_dependency_execution_authorization_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_after_real_dependency_evidence"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "deferred_until_hardware_runtime_ready"},
            {"route": ROUTE_E, "status": "deferred"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "deferred_route_e": DEFERRED_ROUTE_E,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "validation_engineering_separation_dryrun_and_review GO",
            "ocr_via_factory_standard_dryrun_and_review GO",
            "ocr_real_dependency_domain_config_candidate present (candidate_only, not activated)",
            "validation_engineering_model_candidate present (runtime_enabled_now=false)",
            "factory_authorization_standard_extension dryrun GO",
            "no grant / execution window / real-dep / provider import yet",
        ],
        "forbidden_now": [
            "real_dependency_check execution",
            "grant issue",
            "execution window open",
            "domain_config activation",
            "provider import / invoke",
            "dependency install / model download",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": ROUTE_B,
                "status": "deferred_after_real_dependency_evidence",
                "resume_after": "real_dependency_evidence_from_execution_authorization_chain",
            },
            {
                "route": ROUTE_C,
                "status": "deferred",
                "resume_after": "execution_authorization_planning_and_explicit_runtime_need",
            },
            {
                "route": ROUTE_D,
                "status": "deferred_until_hardware_runtime_ready",
                "resume_after": "hardware_runtime_observation_ready",
            },
            {
                "route": ROUTE_E,
                "status": "deferred",
                "resume_after": "visual_context_governance_scheduling",
            },
        ],
        **meta,
    }

    input_ok = len(blockers) == 0 and readiness_review.get("readiness_pass") is True
    boundary_ok = input_ok

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_execution_authorization_planning": boundary_ok,
        "ready_for_real_dependency_check_execution": False,
        "do_not_execute_real_dep_now": True,
        "do_not_grant_now": True,
        "do_not_open_execution_window_now": True,
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_execution_authorization_roadmap_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": next_readiness["final_decision"],
        "recommended_next_phase": next_readiness["recommended_next_phase"],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "deferred_route_e": DEFERRED_ROUTE_E,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_real_dependency_execution_authorization_roadmap_policy": policy,
        "validation_engineering_separation_input_review": val_sep_input,
        "ocr_real_dep_via_factory_standard_input_review": ocr_factory_input,
        "execution_authorization_readiness_review": readiness_review,
        "route_a_execution_authorization_planning_assessment": route_a,
        "route_b_provider_selection_finalize_assessment": route_b,
        "route_c_validation_runtime_activation_assessment": route_c,
        "route_d_health_readiness_baseline_assessment": route_d,
        "route_e_return_visual_context_governance_assessment": route_e,
        "ocr_real_dependency_execution_authorization_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
