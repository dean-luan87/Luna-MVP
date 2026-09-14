# -*- coding: utf-8 -*-
"""OCR Real Minimal Execution Authorization Decision v1 — route decision, no execution."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UPSTREAM_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_DRYRUN_NEXT_PHASE,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    EVIDENCE_OUTPUT_ITEMS,
    FAILURE_ROUTES,
    MINIMAL_FORBIDDEN_ACTIONS,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Real-Minimal-Execution-Authorization-Decision-v1-001"
SCOPE = "real_minimal_execution_authorization_decision_only"
SOURCE_CHAIN = "ocr_real_dependency_real_minimal_execution_authorization_decision_v1"

UPSTREAM_DRYRUN_FINAL = UPSTREAM_DRYRUN_FINAL_GO
UPSTREAM_DRYRUN_NEXT = UPSTREAM_DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_EXECUTION_AUTHORIZATION_DECISION_"
    "READY_FOR_REAL_MINIMAL_CONTROLLED_EXECUTION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_EXECUTION_AUTHORIZATION_DECISION_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Real-Minimal-Execution-Authorization-Issue-Review-v1-001"

ROUTE_A = "Route A — Authorize Real Minimal Controlled Execution Planning"
ROUTE_B = "Route B — Hold for Owner Confirmation"
ROUTE_C = "Route C — Hold for Environment Precheck"
ROUTE_D = "Route D — Defer and Return to Provider Selection"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = "Owner Confirmation"
DEFERRED_ROUTE_C = "Environment Precheck"
BLOCKED_ROUTE_D = "Provider Selection Finalize"

NON_CLAIMS: Tuple[str, ...] = (
    "Authorization Decision GO ≠ real execution started",
    "Route A selected ≠ execution window opened",
    "allowed 5 checks ≠ checks executed",
    "provider import check authorized later ≠ provider runtime invocation",
    "next planning ≠ smoke/sample OCR allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_minimal_execution_authorized_now",
    "real_minimal_execution_started_now",
    "execution_window_opened_now",
    "package_presence_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_import_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
    "runtime_smoke_check_executed_now",
    "sample_ocr_check_executed_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
    "provider_selection_finalized_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_execution_authorization_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "real_minimal_execution_authorization_decision_only": True,
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


def run_ocr_real_dependency_real_minimal_execution_authorization_decision_v1(
    *,
    ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root: str,
    ocr_real_dependency_minimal_controlled_execution_planning_root: Optional[str] = None,
    ocr_real_dependency_execution_final_preflight_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    dryrun_root = Path(
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root
    ).expanduser().resolve()
    plan_root = Path(
        ocr_real_dependency_minimal_controlled_execution_planning_root
        or dryrun_root.parent / "ocr_real_dependency_minimal_controlled_execution_planning"
    ).expanduser().resolve()
    preflight_root = Path(
        ocr_real_dependency_execution_final_preflight_root
        or dryrun_root.parent / "ocr_real_dependency_execution_final_preflight"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or dryrun_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or dryrun_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()

    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    plan_cand = _try_read_json(
        dryrun_root / "minimal_controlled_execution_plan_candidate_v1.json"
    ) or {}
    allowed_review = _try_read_json(
        dryrun_root / "minimal_allowed_check_plan_dryrun_review_v1.json"
    ) or {}
    forbidden_review = _try_read_json(
        dryrun_root / "minimal_forbidden_action_dryrun_review_v1.json"
    ) or {}
    evidence_review = _try_read_json(
        dryrun_root / "minimal_evidence_output_dryrun_review_v1.json"
    ) or {}
    failure_review = _try_read_json(
        dryrun_root / "minimal_failure_route_dryrun_review_v1.json"
    ) or {}
    rollback_review = _try_read_json(dryrun_root / "minimal_rollback_dryrun_review_v1.json") or {}
    post_review = _try_read_json(
        dryrun_root / "minimal_post_execution_review_dryrun_review_v1.json"
    ) or {}
    verifier_review = _try_read_json(
        dryrun_root / "minimal_execution_verifier_plan_review_v1.json"
    ) or {}
    dryrun_blocked = _try_read_json(
        dryrun_root / "minimal_controlled_execution_blocked_path_result_v1.json"
    ) or {}

    plan_allowed = _try_read_json(plan_root / "minimal_allowed_check_plan_v1.json") or {}
    plan_forbidden = _try_read_json(plan_root / "minimal_forbidden_action_plan_v1.json") or {}
    plan_evidence = _try_read_json(plan_root / "minimal_evidence_output_plan_v1.json") or {}
    plan_failure = _try_read_json(plan_root / "minimal_failure_route_plan_v1.json") or {}
    plan_rollback = _try_read_json(plan_root / "minimal_rollback_plan_v1.json") or {}
    plan_post = _try_read_json(plan_root / "minimal_post_execution_review_plan_v1.json") or {}
    plan_verifier = _try_read_json(plan_root / "minimal_execution_verifier_plan_v1.json") or {}

    preflight_vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_dryrun_and_review_root": str(dryrun_root),
        "upstream_planning_root": str(plan_root),
        "upstream_final_preflight_root": str(preflight_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_dr_root),
        "output_root": str(out_root),
    }

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_DRYRUN_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_DRYRUN_NEXT:
        blockers.append("dryrun recommended_next_phase mismatch")
    if not plan_cand.get("plan_candidate_id"):
        blockers.append("minimal_controlled_execution_plan_candidate required")
    if allowed_review.get("dryrun_and_review_pass") is not True:
        blockers.append("allowed check dryrun review must pass")
    if forbidden_review.get("dryrun_and_review_pass") is not True:
        blockers.append("forbidden action dryrun review must pass")
    if evidence_review.get("dryrun_and_review_pass") is not True:
        blockers.append("evidence dryrun review must pass")
    if failure_review.get("dryrun_and_review_pass") is not True:
        blockers.append("failure route dryrun review must pass")
    if rollback_review.get("dryrun_and_review_pass") is not True:
        blockers.append("rollback dryrun review must pass")
    if post_review.get("dryrun_and_review_pass") is not True:
        blockers.append("post-review dryrun review must pass")
    if verifier_review.get("dryrun_and_review_pass") is not True:
        blockers.append("verifier plan dryrun review must pass")
    if dryrun_blocked.get("all_blocked") is not True:
        blockers.append("dryrun blocked paths must remain blocked")
    if plan_allowed.get("check_count") != 5:
        blockers.append("5 allowed checks must be planned")
    if plan_forbidden.get("forbidden_count") != len(MINIMAL_FORBIDDEN_ACTIONS):
        blockers.append("18 forbidden actions must be planned")
    if plan_evidence.get("evidence_count") != len(EVIDENCE_OUTPUT_ITEMS):
        blockers.append("13 evidence items must be planned")
    if plan_failure.get("route_count") != len(FAILURE_ROUTES):
        blockers.append("8 failure routes must be planned")
    if dryrun_sm.get("minimal_controlled_execution_started_now") is True:
        blockers.append("minimal_controlled_execution_started_now must be false")
    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if preflight_vr.get("verifier") != "GO":
        blockers.append("final preflight should be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun should be GO")
    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("ocr via factory dryrun should be GO")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator runtime must not be enabled")

    for item in allowed_review.get("check_plan_items") or plan_allowed.get("checks") or []:
        if item.get("current_executed_now") is True:
            blockers.append("all allowed checks must have current_executed_now=false")
            break

    readiness_checks = {
        "dryrun_go": dryrun_vr.get("verifier") == "GO",
        "plan_candidate_present": bool(plan_cand.get("plan_candidate_id")),
        "allowed_5_complete": plan_allowed.get("check_count") == 5,
        "forbidden_18_blocked": forbidden_review.get("dryrun_and_review_pass") is True,
        "evidence_13_complete": evidence_review.get("dryrun_and_review_pass") is True,
        "failure_8_complete": failure_review.get("dryrun_and_review_pass") is True,
        "rollback_complete": rollback_review.get("dryrun_and_review_pass") is True,
        "post_review_complete": post_review.get("dryrun_and_review_pass") is True,
        "verifier_plan_complete": verifier_review.get("dryrun_and_review_pass") is True,
        "not_started": dryrun_sm.get("minimal_controlled_execution_started_now") is False,
        "provider_null": meta.get("selected_provider_for_execution") is None,
        "no_window": meta.get("execution_window_opened_now") is False,
    }
    readiness_review = {
        "review_id": "real_execution_readiness_review_v1",
        "readiness_checks": readiness_checks,
        "readiness_pass": all(readiness_checks.values()),
        **meta,
    }

    dryrun_input = {
        "review_id": "minimal_execution_dryrun_input_review_v1",
        "upstream_dryrun_root": str(dryrun_root),
        "verifier_go": dryrun_vr.get("verifier") == "GO",
        "final_decision": dryrun_sm.get("final_decision"),
        "dryrun_and_review_pass": dryrun_sm.get("dryrun_and_review_pass"),
        "review_pass": dryrun_vr.get("verifier") == "GO"
        and dryrun_sm.get("final_decision") == UPSTREAM_DRYRUN_FINAL,
        "blockers": blockers,
        **meta,
    }

    allowed_scope_review = {
        "review_id": "allowed_scope_authorization_review_v1",
        "allowed_checks": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "allowed_check_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "all_current_executed_now_false": True,
        "review_pass": allowed_review.get("dryrun_and_review_pass") is True
        and plan_allowed.get("check_count") == 5,
        **meta,
    }

    forbidden_auth_review = {
        "review_id": "forbidden_action_authorization_review_v1",
        "forbidden_actions": list(MINIMAL_FORBIDDEN_ACTIONS),
        "forbidden_count": len(MINIMAL_FORBIDDEN_ACTIONS),
        "all_blocked": forbidden_review.get("dryrun_and_review_pass") is True,
        "review_pass": forbidden_review.get("dryrun_and_review_pass") is True,
        **meta,
    }

    evidence_bundle_review = {
        "review_id": "evidence_rollback_postreview_readiness_review_v1",
        "evidence_items": list(EVIDENCE_OUTPUT_ITEMS),
        "evidence_count": len(EVIDENCE_OUTPUT_ITEMS),
        "failure_route_count": len(FAILURE_ROUTES),
        "rollback_plan_present": plan_rollback.get("rollback_required_before_execution") is True,
        "post_review_required": plan_post.get("review_required") is True,
        "verifier_plan_present": plan_verifier.get("verifier_required_on_future_execution") is True,
        "review_pass": (
            evidence_review.get("dryrun_and_review_pass") is True
            and failure_review.get("dryrun_and_review_pass") is True
            and rollback_review.get("dryrun_and_review_pass") is True
            and post_review.get("dryrun_and_review_pass") is True
            and verifier_review.get("dryrun_and_review_pass") is True
        ),
        **meta,
    }

    risk_boundary_review = {
        "review_id": "execution_risk_boundary_review_v1",
        "real_minimal_execution_authorized_now": False,
        "real_minimal_execution_started_now": False,
        "execution_window_opened_now": False,
        "no_install_download_cache_mutation": True,
        "no_provider_runtime_invoke": True,
        "no_smoke_sample_ocr": True,
        "no_provider_finalize": True,
        "review_pass": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_authorize_real_minimal_execution_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "dryrun/review verified 5 minimal check plans",
            "forbidden actions, evidence, failure routes, rollback, post-review all complete",
            "enters real execution planning/authorization opening only — not direct execution",
            "execution scope must remain minimal 5 checks",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_hold_for_owner_confirmation_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_until_execution_window_open",
        "defer_reasons": [
            "owner/operator confirmation may occur before opening execution window",
            "current phase is authorization decision, not execution window open",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_hold_for_environment_precheck_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "environment snapshot is evidence collected during real execution",
            "do not read environment before authorization decision",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_defer_and_return_to_provider_selection_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "blocked_before_real_dependency_evidence",
        "block_reasons": [
            "provider selection finalize depends on real dependency check evidence",
            "cannot return to finalize before evidence exists",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "real_minimal_execution_authorization_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_until_execution_window_open"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "blocked_before_real_dependency_evidence"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "blocked_route_d": BLOCKED_ROUTE_D,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "minimal controlled execution dryrun and review GO",
            "plan_candidate with 5 allowed checks",
            "18 forbidden actions blocked",
            "13 evidence / 8 failure routes / rollback / post-review / verifier plans complete",
            "minimal_controlled_execution_started_now=false",
            "execution_window_opened_now=false",
            "selected_provider_for_execution=null",
        ],
        "forbidden_now": [
            "execution window open",
            "package / cache / file / hash / import check execution",
            "dependency install / model download / cache mutation",
            "provider runtime invoke",
            "runtime smoke / sample OCR",
            "provider selection finalize",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": ROUTE_B,
                "status": "deferred_until_execution_window_open",
                "resume_before": "execution_window_open",
            },
            {
                "route": ROUTE_C,
                "status": "deferred",
                "resume_during": "real_minimal_controlled_execution",
            },
            {
                "route": ROUTE_D,
                "status": "blocked_before_real_dependency_evidence",
                "resume_after": "real_dependency_evidence_available",
            },
        ],
        **meta,
    }

    input_ok = len(blockers) == 0 and readiness_review.get("readiness_pass") is True
    boundary_ok = (
        input_ok
        and dryrun_input.get("review_pass") is True
        and allowed_scope_review.get("review_pass") is True
        and forbidden_auth_review.get("review_pass") is True
        and evidence_bundle_review.get("review_pass") is True
        and risk_boundary_review.get("review_pass") is True
    )

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_real_minimal_controlled_execution_planning": boundary_ok,
        "ready_for_real_minimal_controlled_execution": False,
        "real_minimal_execution_authorized_now": False,
        "do_not_open_execution_window_now": True,
        "do_not_execute_checks_now": True,
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "real_minimal_execution_authorization_decision_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "minimal_allowed_checks": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
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
        "blocked_route_d": BLOCKED_ROUTE_D,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "real_minimal_execution_authorization_decision_policy": policy,
        "minimal_execution_dryrun_input_review": dryrun_input,
        "real_execution_readiness_review": readiness_review,
        "allowed_scope_authorization_review": allowed_scope_review,
        "forbidden_action_authorization_review": forbidden_auth_review,
        "evidence_rollback_postreview_readiness_review": evidence_bundle_review,
        "execution_risk_boundary_review": risk_boundary_review,
        "route_a_authorize_real_minimal_execution_assessment": route_a,
        "route_b_hold_for_owner_confirmation_assessment": route_b,
        "route_c_hold_for_environment_precheck_assessment": route_c,
        "route_d_defer_and_return_to_provider_selection_assessment": route_d,
        "real_minimal_execution_authorization_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
