# -*- coding: utf-8 -*-
"""OCR Formal Execution Request Generation Post-Route Decision v1 — Route A selected."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_v1 import (
    BLOCKED_PATHS as FORMAL_DRYRUN_BLOCKED_PATHS,
    FINAL_DECISION_GO as UPSTREAM_FORMAL_DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_FORMAL_DRYRUN_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Post-Route-Decision-v1-001"
SCOPE = "formal_execution_request_generation_post_route_decision_only"
SOURCE_CHAIN = "ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1"

UPSTREAM_FORMAL_DRYRUN_FINAL = UPSTREAM_FORMAL_DRYRUN_FINAL_GO
UPSTREAM_FORMAL_DRYRUN_NEXT = UPSTREAM_FORMAL_DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_FORMAL_EXECUTION_REQUEST_GENERATION_POST_ROUTE_DECISION_"
    "READY_FOR_FORMAL_REQUEST_GENERATION_AUTHORIZATION_PLANNING"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_FORMAL_EXECUTION_REQUEST_GENERATION_POST_ROUTE_DECISION_"
    "HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Authorization-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Formal-Execution-Request-Generation-Post-Route-Issue-Review-v1-001"

ROUTE_A = "Route A — Formal Request Generation Authorization Planning"
ROUTE_B = "Route B — Owner / Operator Approval Precheck"
ROUTE_C = "Route C — Validation Runtime Readiness"
ROUTE_D = "Route D — Evidence Readiness Review"
ROUTE_E = "Route E — Direct Formal Request Generation"

SELECTED_ROUTE = ROUTE_A
DEFERRED_ROUTE_B = ROUTE_B
DEFERRED_ROUTE_C = ROUTE_C
DEFERRED_ROUTE_D = ROUTE_D
BLOCKED_ROUTE_E = ROUTE_E

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_execution_request_generation_authorization_started_now",
    "owner_operator_approval_precheck_started_now",
    "validation_runtime_readiness_started_now",
    "evidence_readiness_review_started_now",
    "formal_execution_request_artifact_generated_now",
    "formal_execution_request_persisted_now",
    "formal_execution_request_sent_now",
    "formal_execution_request_approved_now",
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
    "cache_mutation_executed_now",
    "provider_selection_finalized_now",
    "controlled_trial_started_now",
    "ocr_fact_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "user_facing_output_generated_now",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Post-Route Decision GO ≠ formal request artifact generated",
    "Route A selected ≠ request generation authorized",
    "generation authorization planning ≠ request sent",
    "owner/operator approval deferred ≠ approval skipped",
    "direct generation blocked ≠ authorization chain completed",
    "next planning ≠ provider import allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_formal_execution_request_generation_post_route_decision"
)


def _boundary_meta() -> Dict[str, Any]:
    meta = {
        "formal_execution_request_generation_post_route_decision_only": True,
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


def run_ocr_real_dependency_formal_execution_request_generation_post_route_decision_v1(
    *,
    ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root: str,
    ocr_real_dependency_formal_execution_request_generation_planning_root: Optional[str] = None,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    formal_dr_root = Path(
        ocr_real_dependency_formal_execution_request_generation_dryrun_and_review_root
    ).expanduser().resolve()
    formal_dr_sm = _try_read_json(formal_dr_root / "summary.json") or {}
    formal_dr_vr = _try_read_json(formal_dr_root / "verifier_report.json") or {}
    formal_candidate = _try_read_json(
        formal_dr_root / "formal_execution_request_candidate_v1.json"
    ) or {}
    schema_val = _try_read_json(
        formal_dr_root / "formal_execution_request_schema_validation_result_v1.json"
    ) or {}
    precond = _try_read_json(
        formal_dr_root / "formal_execution_request_precondition_dryrun_result_v1.json"
    ) or {}
    field_map = _try_read_json(
        formal_dr_root / "formal_execution_request_field_source_map_dryrun_result_v1.json"
    ) or {}
    rules = _try_read_json(
        formal_dr_root / "formal_execution_request_validation_rule_dryrun_result_v1.json"
    ) or {}
    storage = _try_read_json(
        formal_dr_root / "formal_execution_request_storage_boundary_review_v1.json"
    ) or {}
    send = _try_read_json(
        formal_dr_root / "formal_execution_request_send_boundary_review_v1.json"
    ) or {}
    evidence = _try_read_json(
        formal_dr_root / "formal_execution_request_evidence_binding_review_v1.json"
    ) or {}
    gate_bind = _try_read_json(
        formal_dr_root / "formal_execution_request_validation_gate_binding_review_v1.json"
    ) or {}
    blocked = _try_read_json(
        formal_dr_root / "formal_execution_request_blocked_path_result_v1.json"
    ) or {}

    plan_root = Path(
        ocr_real_dependency_formal_execution_request_generation_planning_root
        or formal_dr_root.parent / "ocr_real_dependency_formal_execution_request_generation_planning"
    ).expanduser().resolve()
    auth_dryrun_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
        or formal_dr_root.parent / "ocr_real_dependency_execution_authorization_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or formal_dr_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or formal_dr_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()

    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_boundary_meta(),
        "upstream_formal_dryrun_and_review_root": str(formal_dr_root),
        "upstream_formal_planning_root": str(plan_root),
        "upstream_execution_authorization_dryrun_root": str(auth_dryrun_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_dr_root),
        "output_root": str(out_root),
    }

    if formal_dr_vr.get("verifier") != "GO":
        blockers.append("formal dryrun verifier must be GO")
    if formal_dr_sm.get("final_decision") != UPSTREAM_FORMAL_DRYRUN_FINAL:
        blockers.append("formal dryrun final_decision mismatch")
    if formal_dr_sm.get("recommended_next_phase") != UPSTREAM_FORMAL_DRYRUN_NEXT:
        blockers.append("formal dryrun recommended_next_phase mismatch")
    if not formal_candidate.get("formal_execution_request_candidate_id"):
        blockers.append("formal_execution_request_candidate required")
    if formal_candidate.get("lifecycle_state") != "formal_execution_request_candidate_ready":
        blockers.append("lifecycle_state must be formal_execution_request_candidate_ready")
    if formal_candidate.get("candidate_only") is not True:
        blockers.append("candidate_only must be true")
    if formal_candidate.get("formal_artifact_generated_now") is not False:
        blockers.append("formal_artifact_generated_now must be false")
    for field in ("persisted_now", "sent_now", "approved_now"):
        if formal_candidate.get(field) is not False:
            blockers.append(f"{field} must be false")

    if schema_val.get("dryrun_and_review_pass") is not True:
        blockers.append("schema validation must pass")
    if precond.get("preconditions_pass") is not True:
        blockers.append("preconditions must pass")
    if field_map.get("dryrun_and_review_pass") is not True:
        blockers.append("field source map must pass")
    if rules.get("dryrun_and_review_pass") is not True:
        blockers.append("validation rules must pass")
    if storage.get("dryrun_and_review_pass") is not True:
        blockers.append("storage boundary must pass")
    if send.get("dryrun_and_review_pass") is not True:
        blockers.append("send boundary must pass")
    if evidence.get("dryrun_and_review_pass") is not True:
        blockers.append("evidence binding must pass")
    if gate_bind.get("dryrun_and_review_pass") is not True:
        blockers.append("gate binding must pass")
    if blocked.get("all_blocked") is not True or blocked.get("blocked_count") != 24:
        blockers.append("24 blocked paths must be blocked")

    if formal_dr_sm.get("validator_runtime_enabled_now") is True:
        blockers.append("validator_runtime_enabled_now must be false")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator runtime must not be enabled")

    for field in (
        "package_check_executed_now",
        "provider_imported_now",
        "provider_invoked_now",
        "real_dependency_check_executed_now",
    ):
        if formal_dr_sm.get(field) is True or formal_candidate.get(field) is True:
            blockers.append(f"{field} must be false")

    dryrun_input = {
        "review_id": "formal_execution_request_dryrun_input_review_v1",
        "upstream_formal_dryrun_root": str(formal_dr_root),
        "verifier_go": formal_dr_vr.get("verifier") == "GO",
        "final_decision": formal_dr_sm.get("final_decision"),
        "dryrun_and_review_pass": formal_dr_sm.get("dryrun_and_review_pass"),
        "review_pass": formal_dr_vr.get("verifier") == "GO"
        and formal_dr_sm.get("final_decision") == UPSTREAM_FORMAL_DRYRUN_FINAL,
        "blockers": blockers,
        **meta,
    }

    readiness_checks = {
        "formal_candidate_present": bool(formal_candidate.get("formal_execution_request_candidate_id")),
        "lifecycle_ready": formal_candidate.get("lifecycle_state")
        == "formal_execution_request_candidate_ready",
        "schema_validation_pass": schema_val.get("dryrun_and_review_pass") is True,
        "preconditions_pass": precond.get("preconditions_pass") is True,
        "field_map_pass": field_map.get("dryrun_and_review_pass") is True,
        "validation_rules_pass": rules.get("dryrun_and_review_pass") is True,
        "storage_boundary_pass": storage.get("dryrun_and_review_pass") is True,
        "send_boundary_pass": send.get("dryrun_and_review_pass") is True,
        "evidence_binding_pass": evidence.get("dryrun_and_review_pass") is True,
        "gate_binding_pass": gate_bind.get("dryrun_and_review_pass") is True,
        "blocked_paths_ok": blocked.get("all_blocked") is True,
        "no_formal_artifact": formal_candidate.get("formal_artifact_generated_now") is False,
        "provider_null": meta.get("selected_provider_for_execution") is None,
    }
    readiness_review = {
        "review_id": "formal_execution_request_candidate_readiness_review_v1",
        "readiness_checks": readiness_checks,
        "readiness_pass": all(readiness_checks.values()),
        **meta,
    }

    route_a = {
        "assessment_id": "route_a_formal_request_generation_authorization_planning_assessment_v1",
        "route_id": "A",
        "route_label": ROUTE_A,
        "status": "selected",
        "selection_reasons": [
            "formal_execution_request_candidate generated and dryrun review passed",
            "schema / preconditions / field map / validation rules / evidence / gate binding all pass",
            "next step is formal request artifact generation authorization planning",
            "still no formal request generation / send / grant / check execution",
        ],
        **meta,
    }

    route_b = {
        "assessment_id": "route_b_owner_operator_approval_precheck_assessment_v1",
        "route_id": "B",
        "route_label": ROUTE_B,
        "status": "deferred_until_formal_generation_authorization_candidate",
        "defer_reasons": [
            "approval requires formal generation authorization candidate or formal request artifact candidate",
            "formal request generation authorization planning can proceed first",
            "approval precheck should not precede generation authorization path definition",
        ],
        **meta,
    }

    route_c = {
        "assessment_id": "route_c_validation_runtime_readiness_assessment_v1",
        "route_id": "C",
        "route_label": ROUTE_C,
        "status": "deferred",
        "defer_reasons": [
            "validator runtime not enabled now",
            "formal generation authorization planning only for this phase",
            "validation runtime readiness before real execution or window open later",
        ],
        **meta,
    }

    route_d = {
        "assessment_id": "route_d_evidence_readiness_review_assessment_v1",
        "route_id": "D",
        "route_label": ROUTE_D,
        "status": "deferred_until_generation_authorization_planning",
        "defer_reasons": [
            "evidence binding passed dryrun",
            "formal evidence readiness should be reviewed against generation authorization candidate",
        ],
        **meta,
    }

    route_e = {
        "assessment_id": "route_e_direct_request_generation_assessment_v1",
        "route_id": "E",
        "route_label": ROUTE_E,
        "status": "blocked",
        "block_reasons": [
            "formal generation authorization not entered",
            "owner/operator approval not obtained",
            "grant not issued",
            "direct formal request generation bypasses Authorization Standard and Validation Engineering",
        ],
        **meta,
    }

    selection_matrix = {
        "matrix_id": "formal_execution_request_post_route_selection_matrix_v1",
        "routes": [
            {"route": ROUTE_A, "status": "selected"},
            {"route": ROUTE_B, "status": "deferred_until_formal_generation_authorization_candidate"},
            {"route": ROUTE_C, "status": "deferred"},
            {"route": ROUTE_D, "status": "deferred_until_generation_authorization_planning"},
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
            "formal execution request generation dryrun and review GO",
            "formal_execution_request_candidate ready",
            "all dryrun reviews pass",
            "24 blocked paths remain blocked",
            "formal_artifact_generated_now=false",
            "selected_provider_for_execution=null",
        ],
        "forbidden_now": [
            "formal request artifact generation",
            "persist / send / approval",
            "grant / execution window",
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
                "status": "deferred_until_formal_generation_authorization_candidate",
                "resume_after": "generation_authorization_candidate_ready",
            },
            {
                "route": ROUTE_C,
                "status": "deferred",
                "resume_after": "before_real_execution_or_window_open",
            },
            {
                "route": ROUTE_D,
                "status": "deferred_until_generation_authorization_planning",
                "resume_after": "generation_authorization_planning_closed",
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
        "ready_for_formal_request_generation_authorization_planning": boundary_ok,
        "ready_for_formal_request_artifact_generation": False,
        "do_not_generate_formal_artifact_now": True,
        "do_not_persist_now": True,
        "do_not_send_now": True,
        "do_not_approve_now": True,
        "selected_route": SELECTED_ROUTE,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "formal_execution_request_generation_post_route_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        "formal_dryrun_blocked_path_count": len(FORMAL_DRYRUN_BLOCKED_PATHS),
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
        "formal_execution_request_generation_post_route_policy": policy,
        "formal_execution_request_dryrun_input_review": dryrun_input,
        "formal_execution_request_candidate_readiness_review": readiness_review,
        "route_a_formal_request_generation_authorization_planning_assessment": route_a,
        "route_b_owner_operator_approval_precheck_assessment": route_b,
        "route_c_validation_runtime_readiness_assessment": route_c,
        "route_d_evidence_readiness_review_assessment": route_d,
        "route_e_direct_request_generation_assessment": route_e,
        "formal_execution_request_post_route_selection_matrix": selection_matrix,
        "selected_route_preconditions": preconditions,
        "deferred_routes_register": deferred_register,
        "next_phase_readiness_decision": next_readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
