# -*- coding: utf-8 -*-
"""OCR Provider Authorization Request Planning v1 — artifact schema only, no generation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    CURRENT_DRYRUN_STATE,
    EVIDENCE_REQUIREMENTS,
)
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
)
from capabilities.governance.ocr_provider_authorization_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-Request-Planning-v1-001"
SCOPE = "ocr_provider_authorization_request_planning_only"
SOURCE_CHAIN = "ocr_provider_authorization_request_planning_v1"

UPSTREAM_POST_REVIEW_FINAL = POST_REVIEW_FINAL_GO
UPSTREAM_POST_REVIEW_NEXT = POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_REQUEST_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Request-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Issue-Review-v1-001"

REQUEST_ARTIFACT_SCHEMA_STATE = "request_artifact_planned"
CURRENT_LIFECYCLE_STATE = "request_planning_defined"

LIFECYCLE_STATES: Tuple[str, ...] = (
    "request_planning_defined",
    "request_artifact_candidate_ready",
    "request_artifact_generated_later",
    "request_review_pending_later",
    "request_sent_later",
    "grant_pending_later",
    "grant_issued_later",
    "execution_window_opened_later",
    "execution_completed_later",
    "post_execution_review_required",
    "closed",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_request_artifact_generation",
    "planning_to_request_send",
    "planning_to_grant_issue",
    "planning_to_execution_window_open",
    "planning_to_real_dependency_check",
    "planning_to_provider_import",
    "planning_to_dependency_install",
    "planning_to_model_download",
    "planning_to_provider_smoke",
    "planning_to_sample_ocr",
    "planning_to_provider_selection_finalize",
    "planning_to_controlled_trial",
    "planning_to_ocr_request_submit",
    "planning_to_image_read",
    "planning_to_ocr_fact",
)

VALIDATION_RULES: Tuple[Dict[str, str], ...] = (
    {"rule_id": "request_type_match", "detail": "request_type must equal ocr_provider_authorization_request"},
    {"rule_id": "target_scope_no_production", "detail": "target_scope must not include production runtime"},
    {"rule_id": "provider_refs_no_selection", "detail": "provider_candidate_refs must not imply selected provider"},
    {"rule_id": "execution_window_not_opened", "detail": "execution window must not be opened"},
    {"rule_id": "sandbox_no_production_write", "detail": "sandbox must require no production write"},
    {"rule_id": "evidence_required", "detail": "evidence package must be required"},
    {"rule_id": "approval_not_collected", "detail": "approval must not be collected now"},
    {"rule_id": "generated_now_false", "detail": "generated_now must remain false in planning"},
)

SEND_BOUNDARY_CLAIMS: Tuple[str, ...] = (
    "request artifact planned ≠ request artifact generated",
    "request artifact generated later ≠ request sent",
    "request sent later ≠ grant issued",
    "grant issued later ≠ execution window opened",
    "execution window opened later ≠ provider invocation",
)

NON_CLAIMS: Tuple[str, ...] = (
    *SEND_BOUNDARY_CLAIMS,
    "Request Planning GO ≠ request artifact generated",
    "request artifact schema planned ≠ request sent",
    "DryRun next ≠ real dependency check executed",
    "request planning ≠ provider selected",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "authorization_request_artifact_generated_now",
    "authorization_request_sent_now",
    "authorization_request_persisted_now",
    "authorization_request_approved_now",
    "grant_issued_now",
    "provider_authorization_granted_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "provider_selection_finalized_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "controlled_trial_started_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_request_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_request_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_provider_authorization_request_planning_v1(
    *,
    ocr_provider_authorization_post_dryrun_review_root: str,
    ocr_provider_authorization_dryrun_root: Optional[str] = None,
    ocr_provider_authorization_planning_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(ocr_provider_authorization_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    post_closure = _try_read_json(post_root / "authorization_closure_decision_v1.json") or {}

    dryrun_root = Path(
        ocr_provider_authorization_dryrun_root
        or post_root.parent / "ocr_provider_authorization_dryrun"
    ).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}

    planning_root = Path(
        ocr_provider_authorization_planning_root
        or post_root.parent / "ocr_provider_authorization_planning"
    ).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or post_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}
    factory_closure = _try_read_json(
        factory_post_root / "factory_registration_closure_decision_v1.json"
    ) or {}

    request_cand = _try_read_json(dryrun_root / "authorization_request_candidate_v1.json") or {}
    grant_cand = _try_read_json(dryrun_root / "grant_candidate_v1.json") or {}
    window_cand = _try_read_json(dryrun_root / "execution_window_candidate_v1.json") or {}
    sandbox_cand = _try_read_json(dryrun_root / "sandbox_boundary_candidate_v1.json") or {}
    rollback_cand = _try_read_json(dryrun_root / "rollback_candidate_v1.json") or {}
    evidence_cand = _try_read_json(dryrun_root / "evidence_requirement_candidate_v1.json") or {}
    blocked_dryrun = _try_read_json(dryrun_root / "authorization_blocked_path_result_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "output_root": str(out_root),
    }

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_POST_REVIEW_FINAL:
        blockers.append("post-dryrun review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_POST_REVIEW_NEXT:
        blockers.append("post-dryrun review recommended_next_phase mismatch")
    if post_sm.get("boundary_ok") is not True:
        blockers.append("post-dryrun review boundary_ok must be true")
    if post_closure.get("ocr_provider_authorization_dryrun_closed") is not True:
        blockers.append("ocr_provider_authorization_dryrun_closed must be true")
    if post_sm.get("current_lifecycle_state") != CURRENT_DRYRUN_STATE:
        blockers.append("current_lifecycle_state must be request_candidate_ready")

    if dryrun_vr.get("verifier") != "GO":
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("current_lifecycle_state") != CURRENT_DRYRUN_STATE:
        blockers.append("dryrun current_state must be request_candidate_ready")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("factory registration post-review must be GO")
    if factory_closure.get("validation_factory_registry_candidate_trusted") is not True:
        blockers.append("harness seventh module candidate must be trusted")

    for field in (
        "authorization_request_artifact_generated_now",
        "authorization_request_sent_now",
        "grant_issued_now",
        "provider_authorization_granted_now",
        "execution_window_opened_now",
        "real_dependency_check_executed_now",
    ):
        if post_sm.get(field) is True:
            blockers.append(f"post-review {field} must be false")

    if post_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must remain null")

    if blocked_dryrun.get("all_blocked") is not True:
        blockers.append("dryrun all_boundary_paths_blocked required")

    if plan_sm.get("boundary_ok") is not True:
        blockers.append("planning upstream boundary_ok must be true")

    input_review = {
        "review_id": "authorization_post_dryrun_review_input_review_v1",
        "upstream_root": str(post_root),
        "upstream_verifier_go": post_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "upstream_dryrun_closed": post_closure.get("ocr_provider_authorization_dryrun_closed"),
        "upstream_current_state": post_sm.get("current_lifecycle_state"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    request_candidate_ref = request_cand.get("request_id") or "ocr_provider_authorization_request_candidate_v1"
    grant_candidate_ref = grant_cand.get("grant_candidate_id") or "ocr_provider_authorization_grant_candidate_v1"
    window_candidate_ref = (
        window_cand.get("execution_window_candidate_id")
        or "ocr_provider_authorization_execution_window_candidate_v1"
    )
    sandbox_candidate_ref = sandbox_cand.get("candidate_id") or "sandbox_boundary_candidate_v1"
    rollback_candidate_ref = rollback_cand.get("candidate_id") or "rollback_candidate_v1"
    evidence_candidate_ref = evidence_cand.get("candidate_id") or "evidence_requirement_candidate_v1"

    artifact_schema = {
        "schema_id": "authorization_request_artifact_schema_v1",
        "request_artifact_id": "ocr_provider_authorization_request_artifact_v1",
        "request_type": "ocr_provider_authorization_request",
        "lifecycle_state": REQUEST_ARTIFACT_SCHEMA_STATE,
        "related_authorization_request_candidate_ref": request_candidate_ref,
        "target_scope": list(AUTHORIZATION_SCOPE_COVERED),
        "provider_candidate_refs": request_cand.get("provider_candidate_refs") or "planned_candidate_refs_only",
        "dependency_check_scope": request_cand.get("dependency_check_scope") or "real_dependency_check_plan_candidate",
        "environment_scope": request_cand.get("environment_scope") or "sandbox_workspace_fallback_only",
        "requested_execution_window_ref": window_candidate_ref,
        "sandbox_boundary_ref": sandbox_candidate_ref,
        "rollback_plan_ref": rollback_candidate_ref,
        "evidence_requirement_ref": evidence_candidate_ref,
        "owner_operator_approval_required": True,
        "verifier_required": True,
        "post_execution_review_required": True,
        "generated_now": False,
        "sent_now": False,
        "approved_now": False,
        "schema_only": True,
        "artifact_generated_now": False,
        **meta,
    }

    preconditions = {
        "precondition_id": "authorization_request_generation_precondition_v1",
        "authorization_post_dryrun_review_go": post_go,
        "request_candidate_ready": dryrun_sm.get("current_lifecycle_state") == CURRENT_DRYRUN_STATE,
        "grant_candidate_available": dryrun_sm.get("grant_candidate_generated_now") is True,
        "execution_window_candidate_available": dryrun_sm.get("execution_window_candidate_generated_now") is True,
        "sandbox_boundary_candidate_available": dryrun_sm.get("sandbox_boundary_candidate_generated_now") is True,
        "rollback_candidate_available": dryrun_sm.get("rollback_candidate_generated_now") is True,
        "evidence_requirement_candidate_available": dryrun_sm.get("evidence_requirement_candidate_generated_now") is True,
        "selected_provider_for_execution": None,
        "provider_selection_finalized": False,
        "all_boundary_paths_blocked": blocked_dryrun.get("all_blocked") is True,
        "artifact_generation_allowed_now": False,
        **meta,
    }

    field_bindings = {
        "binding_id": "authorization_request_field_binding_plan_v1",
        "bindings": [
            {
                "source": "authorization_request_candidate_v1",
                "source_ref": request_candidate_ref,
                "target": "authorization_request_artifact_schema_v1",
                "target_field": "related_authorization_request_candidate_ref",
            },
            {
                "source": "grant_candidate_v1",
                "source_ref": grant_candidate_ref,
                "target": "later_grant_workflow",
                "target_field": "grant_candidate_ref",
            },
            {
                "source": "execution_window_candidate_v1",
                "source_ref": window_candidate_ref,
                "target": "authorization_request_artifact_schema_v1",
                "target_field": "requested_execution_window_ref",
            },
            {
                "source": "sandbox_boundary_candidate_v1",
                "source_ref": sandbox_candidate_ref,
                "target": "authorization_request_artifact_schema_v1",
                "target_field": "sandbox_boundary_ref",
            },
            {
                "source": "rollback_candidate_v1",
                "source_ref": rollback_candidate_ref,
                "target": "authorization_request_artifact_schema_v1",
                "target_field": "rollback_plan_ref",
            },
            {
                "source": "evidence_requirement_candidate_v1",
                "source_ref": evidence_candidate_ref,
                "target": "authorization_request_artifact_schema_v1",
                "target_field": "evidence_requirement_ref",
            },
            {
                "source": "owner_operator_approval_dryrun_result_v1",
                "target": "authorization_request_artifact_schema_v1",
                "target_field": "owner_operator_approval_required",
            },
        ],
        "binding_count": 7,
        **meta,
    }

    validation_plan = {
        "plan_id": "authorization_request_validation_rule_plan_v1",
        "rules": list(VALIDATION_RULES),
        "rule_count": len(VALIDATION_RULES),
        "enforced_in_planning": True,
        "artifact_generation_blocked_in_planning": True,
        **meta,
    }

    approval_plan = {
        "plan_id": "authorization_request_owner_operator_approval_plan_v1",
        "owner_operator_approval_required": True,
        "approval_collected_now": False,
        "approval_required_for_real_dependency_check": True,
        "approval_required_for_request_send_later": True,
        "signature_placeholder": "owner_operator_signature_pending",
        **meta,
    }

    send_boundary = {
        "plan_id": "authorization_request_send_boundary_plan_v1",
        "send_boundary_claims": list(SEND_BOUNDARY_CLAIMS),
        "request_artifact_planned_not_generated": True,
        "request_artifact_generated_not_sent": True,
        "request_sent_not_grant": True,
        "grant_not_execution_window": True,
        "execution_window_not_provider_invocation": True,
        "authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        **meta,
    }

    lifecycle_plan = {
        "plan_id": "authorization_request_lifecycle_plan_v1",
        "states": list(LIFECYCLE_STATES),
        "current_state": CURRENT_LIFECYCLE_STATE,
        "transitions_planned_only": True,
        "prior_authorization_state": CURRENT_DRYRUN_STATE,
        **meta,
    }

    evidence_binding = {
        "plan_id": "authorization_request_evidence_binding_plan_v1",
        "evidence_requirement_ref": evidence_candidate_ref,
        "required_artifacts_on_future_execution": list(EVIDENCE_REQUIREMENTS),
        "artifact_count": len(EVIDENCE_REQUIREMENTS),
        "evidence_package_required": True,
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "authorization_request_blocked_path_matrix_v1",
        "paths": [{"path_id": p, "blocked": True, "default": True} for p in BLOCKED_PATHS],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "authorization_request_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate request_artifact_candidate",
            "verify schema / preconditions / field bindings / validation rules",
            "verify artifact generation remains blocked",
        ],
        "dryrun_forbidden": [
            "generate formal request artifact",
            "send request",
            "grant authorization",
            "execute real dependency check",
        ],
        **meta,
    }

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "authorization_request_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ready_for_dryrun": boundary_ok,
        "current_lifecycle_state": CURRENT_LIFECYCLE_STATE,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_authorization_request_planning_policy_v1",
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
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        "current_lifecycle_state": CURRENT_LIFECYCLE_STATE,
        "boundary_path_count": len(BLOCKED_PATHS),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_provider_authorization_request_planning_policy": policy,
        "authorization_post_dryrun_review_input_review": input_review,
        "authorization_request_artifact_schema": artifact_schema,
        "authorization_request_generation_precondition": preconditions,
        "authorization_request_field_binding_plan": field_bindings,
        "authorization_request_validation_rule_plan": validation_plan,
        "authorization_request_owner_operator_approval_plan": approval_plan,
        "authorization_request_send_boundary_plan": send_boundary,
        "authorization_request_lifecycle_plan": lifecycle_plan,
        "authorization_request_evidence_binding_plan": evidence_binding,
        "authorization_request_blocked_path_matrix": blocked_matrix,
        "authorization_request_dryrun_plan": dryrun_plan,
        "authorization_request_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
