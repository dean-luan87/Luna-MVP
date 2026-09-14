# -*- coding: utf-8 -*-
"""OCR Real Dependency Execution Request Generation Roadmap Decision v1 — Route A."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_authorization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as UPSTREAM_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_DRYRUN_NEXT_PHASE,
    SCOPE_ALLOWED_CHECKS,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Execution-Request-Generation-Roadmap-Decision-v1-001"
SCOPE = "execution_request_generation_roadmap_decision_only"
SOURCE_CHAIN = "ocr_real_dependency_execution_request_generation_roadmap_decision_v1"

UPSTREAM_DRYRUN_FINAL = UPSTREAM_DRYRUN_FINAL_GO
UPSTREAM_DRYRUN_NEXT = UPSTREAM_DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_EXECUTION_REQUEST_GENERATION_ROADMAP_DECISION_"
    "READY_FOR_FORMAL_EXECUTION_REQUEST_GENERATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_EXECUTION_REQUEST_GENERATION_ROADMAP_DECISION_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Execution-Request-Generation-Issue-Review-v1-001"

ROUTE_A = "Route A — Formal Execution Request Generation Planning"
ROUTE_B = "Route B — Validation Runtime Readiness"
ROUTE_C = "Route C — Owner / Operator Approval Precheck"
ROUTE_D = "Route D — Provider Selection Evidence Precheck"
ROUTE_E = "Route E — Direct Real Dependency Execution"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = ROUTE_B
DEFERRED_ROUTE_C = ROUTE_C
DEFERRED_ROUTE_D = ROUTE_D
BLOCKED_ROUTE_E = ROUTE_E

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_execution_request_generation_started_now",
    "formal_execution_request_generated_now",
    "execution_request_sent_now",
    "execution_grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_hash_check_executed_now",
    "runtime_smoke_check_executed_now",
    "sample_ocr_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_selection_finalized_now",
    "controlled_trial_started_now",
    "ocr_fact_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Roadmap Decision GO ≠ formal execution request generated",
    "Route A selected ≠ request sent",
    "formal request generation planning ≠ grant issued",
    "request generation roadmap ≠ execution window opened",
    "direct execution blocked ≠ real-dep authorization completed",
    "next planning ≠ provider import allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_request_generation_roadmap_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "execution_request_generation_roadmap_decision_only": True,
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


def run_ocr_real_dependency_execution_request_generation_roadmap_decision_v1(
    *,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: str,
    ocr_real_dependency_execution_authorization_planning_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    dryrun_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    request_cand = _try_read_json(
        dryrun_root / "execution_authorization_request_candidate_v1.json"
    ) or {}
    grant_cand = _try_read_json(dryrun_root / "execution_grant_candidate_v1.json") or {}
    window_cand = _try_read_json(dryrun_root / "execution_window_candidate_v1.json") or {}
    allowed_cand = _try_read_json(dryrun_root / "allowed_check_plan_candidate_v1.json") or {}
    evidence_cand = _try_read_json(dryrun_root / "evidence_collection_candidate_v1.json") or {}
    gate_review = _try_read_json(dryrun_root / "validation_gate_path_dryrun_review_v1.json") or {}

    plan_root = Path(
        ocr_real_dependency_execution_authorization_planning_root
        or dryrun_root.parent / "ocr_real_dependency_execution_authorization_planning"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or dryrun_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or dryrun_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()
    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or dryrun_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()

    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_dryrun_and_review_root": str(dryrun_root),
        "upstream_planning_root": str(plan_root),
        "upstream_ocr_via_factory_dryrun_review_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_review_root": str(val_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_root),
        "output_root": str(out_root),
    }

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_DRYRUN_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_DRYRUN_NEXT:
        blockers.append("dryrun recommended_next_phase mismatch")
    if not request_cand.get("request_candidate_id"):
        blockers.append("execution_authorization_request_candidate required")
    if not grant_cand.get("grant_candidate_id"):
        blockers.append("execution_grant_candidate required")
    if not window_cand.get("execution_window_candidate_id"):
        blockers.append("execution_window_candidate required")
    if not allowed_cand.get("candidate_id"):
        blockers.append("allowed_check_plan_candidate required")
    if not evidence_cand.get("candidate_id"):
        blockers.append("evidence_collection_candidate required")
    if gate_review.get("simulated_gate_path_pass") is not True:
        blockers.append("validation gate path must simulated pass")
    if gate_review.get("dryrun_and_review_pass") is not True:
        blockers.append("validation gate path review must pass")

    if dryrun_sm.get("validator_runtime_enabled_now") is True:
        blockers.append("validator_runtime_enabled_now must be false")
    if dryrun_sm.get("validation_factory_runtime_enforced_now") is True:
        blockers.append("validation_factory_runtime_enforced_now must be false")
    if request_cand.get("formal_request_generated_now") is True:
        blockers.append("formal_request_generated_now must be false")
    if request_cand.get("request_sent_now") is True:
        blockers.append("request_sent_now must be false")
    if grant_cand.get("grant_issued_now") is True:
        blockers.append("grant_issued_now must be false")
    if window_cand.get("execution_window_opened_now") is True:
        blockers.append("execution_window_opened_now must be false")

    for item in allowed_cand.get("checks") or []:
        if item.get("current_executed_now") is True:
            blockers.append("all allowed checks must have current_executed_now=false")
            break
    if allowed_cand.get("check_count") != 8:
        blockers.append("allowed_check_plan must have 8 checks")

    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator runtime must not be enabled")
    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun should be GO")

    for field in (
        "provider_imported_now",
        "provider_invoked_now",
        "real_dependency_check_executed_now",
    ):
        if dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    readiness_checks = {
        "dryrun_go": dryrun_vr.get("verifier") == "GO",
        "request_candidate_present": bool(request_cand.get("request_candidate_id")),
        "grant_candidate_present": bool(grant_cand.get("grant_candidate_id")),
        "window_candidate_present": bool(window_cand.get("execution_window_candidate_id")),
        "allowed_check_candidate_present": bool(allowed_cand.get("candidate_id")),
        "evidence_candidate_present": bool(evidence_cand.get("candidate_id")),
        "gate_path_simulated_pass": gate_review.get("simulated_gate_path_pass") is True,
        "no_formal_request": request_cand.get("formal_request_generated_now") is False,
        "no_grant": grant_cand.get("grant_issued_now") is False,
        "no_window": window_cand.get("execution_window_opened_now") is False,
        "provider_null": meta.get("selected_provider_for_execution") is None,
    }
    readiness_review = {
        "review_id": "request_generation_readiness_review_v1",
        "readiness_checks": readiness_checks,
        "readiness_pass": all(readiness_checks.values()),
        **meta,
    }

    dryrun_input = {
        "review_id": "execution_authorization_dryrun_input_review_v1",
        "upstream_dryrun_root": str(dryrun_root),
        "verifier_go": dryrun_vr.get("verifier") == "GO",
        "final_decision": dryrun_sm.get("final_decision"),
        "dryrun_and_review_pass": dryrun_sm.get("dryrun_and_review_pass"),
        "review_pass": dryrun_vr.get("verifier") == "GO"
        and dryrun_sm.get("final_decision") == UPSTREAM_DRYRUN_FINAL,
        "blockers": blockers,
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_formal_execution_request_generation_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "execution_authorization_request_candidate / grant_candidate / window_candidate dryrun pass",
            "allowed_check_plan_candidate and evidence_collection_candidate exist",
            "validation gate path simulated pass",
            "next step is formal execution request generation planning (conditions + artifact schema)",
            "still no request send / grant / check execution",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_validation_runtime_readiness_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred",
        "defer_reasons": [
            "validator runtime not enabled now",
            "request generation planning only — no global runtime activation needed",
            "validation runtime readiness can be separate before real execution",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_owner_operator_approval_precheck_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred_until_formal_request_candidate",
        "defer_reasons": [
            "approval requires formal request artifact or finalized request candidate",
            "formal request generation planning can proceed first",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_provider_selection_evidence_precheck_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred_after_real_dependency_evidence",
        "defer_reasons": [
            "provider finalize still needs real dependency check evidence",
            "should not finalize provider before evidence",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_real_dependency_execution_direct_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "blocked",
        "block_reasons": [
            "no formal request generated yet",
            "no request sent",
            "no grant issued",
            "no execution window opened",
            "direct execution bypasses Authorization Standard",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "execution_request_generation_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred"},
            {"route": ROUTE_C, "status": "deferred_until_formal_request_candidate"},
            {"route": ROUTE_D, "status": "deferred_after_real_dependency_evidence"},
            {"route": ROUTE_E, "status": "blocked"},
        ],
        "selected_route": SELECTED_ROUTE,
        "deferred_route_b": DEFERRED_ROUTE_B,
        "deferred_route_c": DEFERRED_ROUTE_C,
        "deferred_route_d": DEFERRED_ROUTE_D,
        "blocked_route_e": BLOCKED_ROUTE_E,
        **meta,
    }

    preconditions = {
        "preconditions_id": "selected_route_preconditions_v1",
        "selected_route": SELECTED_ROUTE,
        "preconditions": [
            "execution authorization dryrun and review GO",
            "request / grant / window / allowed_check / evidence candidates present",
            "validation gate path simulated pass",
            "formal_request_generated_now=false",
            "grant_issued_now=false",
            "execution_window_opened_now=false",
            "all allowed checks current_executed_now=false",
            "selected_provider_for_execution=null",
        ],
        "forbidden_now": [
            "formal execution request generation",
            "request send",
            "grant issue",
            "execution window open",
            "real dependency check execution",
            "provider import / invoke",
        ],
        **meta,
    }

    deferred_register = {
        "register_id": "deferred_routes_register_v1",
        "deferred_items": [
            {
                "route": ROUTE_B,
                "status": "deferred",
                "resume_after": "validation_runtime_readiness_before_real_execution",
            },
            {
                "route": ROUTE_C,
                "status": "deferred_until_formal_request_candidate",
                "resume_after": "formal_request_candidate_ready",
            },
            {
                "route": ROUTE_D,
                "status": "deferred_after_real_dependency_evidence",
                "resume_after": "real_dependency_evidence_available",
            },
            {
                "route": ROUTE_E,
                "status": "blocked",
                "resume_after": "full_authorization_chain_complete",
            },
        ],
        **meta,
    }

    input_ok = len(blockers) == 0 and readiness_review.get("readiness_pass") is True
    boundary_ok = input_ok and dryrun_input.get("review_pass") is True

    next_readiness = {
        "readiness_id": "next_phase_readiness_decision_v1",
        "ready_for_formal_execution_request_generation_planning": boundary_ok,
        "ready_for_real_dependency_check_execution": False,
        "do_not_generate_formal_request_now": True,
        "do_not_send_request_now": True,
        "do_not_grant_now": True,
        "do_not_open_execution_window_now": True,
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "execution_request_generation_roadmap_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "allowed_checks_in_scope": list(SCOPE_ALLOWED_CHECKS),
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
        "blocked_route_e": BLOCKED_ROUTE_E,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "execution_request_generation_roadmap_policy": policy,
        "execution_authorization_dryrun_input_review": dryrun_input,
        "request_generation_readiness_review": readiness_review,
        "route_a_formal_execution_request_generation_planning_assessment": route_a,
        "route_b_validation_runtime_readiness_assessment": route_b,
        "route_c_owner_operator_approval_precheck_assessment": route_c,
        "route_d_provider_selection_evidence_precheck_assessment": route_d,
        "route_e_real_dependency_execution_direct_assessment": route_e,
        "execution_request_generation_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
