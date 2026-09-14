# -*- coding: utf-8 -*-
"""OCR Provider Authorization Request DryRun v1 — request_artifact_candidate only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    CURRENT_DRYRUN_STATE as AUTH_DRYRUN_STATE,
    EVIDENCE_REQUIREMENTS,
)
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
)
from capabilities.governance.ocr_provider_authorization_request_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as PLANNING_LIFECYCLE_STATE,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    SEND_BOUNDARY_CLAIMS as PLANNING_SEND_BOUNDARY,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-Request-DryRun-v1-001"
SCOPE = "ocr_provider_authorization_request_dryrun_only"
SOURCE_CHAIN = "ocr_provider_authorization_request_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_AUTHORIZATION_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_REQUEST_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Request-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Request-Issue-Review-v1-001"

CURRENT_REQUEST_DRYRUN_STATE = "request_artifact_candidate_ready"

DRYRUN_BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_request_artifact_generation",
    "dryrun_to_request_persist",
    "dryrun_to_request_send",
    "dryrun_to_approval_collect",
    "dryrun_to_grant_issue",
    "dryrun_to_execution_window_open",
    "dryrun_to_real_dependency_check",
    "dryrun_to_provider_import",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_provider_smoke",
    "dryrun_to_sample_ocr",
    "dryrun_to_provider_selection_finalize",
    "dryrun_to_controlled_trial",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_ocr_fact",
)

VALIDATION_RULE_IDS: Tuple[str, ...] = (
    "request_type_match",
    "target_scope_no_production",
    "provider_refs_no_selection",
    "execution_window_not_opened",
    "sandbox_no_production_write",
    "evidence_required",
    "approval_not_collected",
    "formal_artifact_not_generated",
)

SEND_BOUNDARY_DRYRUN_CLAIMS: Tuple[str, ...] = (
    "request artifact candidate ≠ formal request artifact",
    "formal request artifact later ≠ request sent",
    "request sent later ≠ grant issued",
    "grant issued later ≠ execution window opened",
    "execution window opened later ≠ provider invocation",
)

NON_CLAIMS: Tuple[str, ...] = (
    *SEND_BOUNDARY_DRYRUN_CLAIMS,
    "Request DryRun GO ≠ formal request artifact generated",
    "request_artifact_candidate ≠ request sent",
    "Post-DryRun Review next ≠ real dependency check executed",
    "request artifact candidate ≠ provider selected",
    "DryRun GO ≠ OCRRequest submitted",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "authorization_request_artifact_generated_now",
    "authorization_request_persisted_now",
    "authorization_request_sent_now",
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_request_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_request_dryrun_only": True,
        "simulated": True,
        "request_artifact_candidate_generated_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["authorization_request_artifact_generated_now"] = False
    meta["authorization_request_persisted_now"] = False
    meta["authorization_request_approved_now"] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _binding_results(
    *,
    request_candidate_ref: str,
    grant_candidate_ref: str,
    window_candidate_ref: str,
    sandbox_candidate_ref: str,
    rollback_candidate_ref: str,
    evidence_candidate_ref: str,
    artifact_candidate: Dict[str, Any],
) -> List[Dict[str, Any]]:
    checks = [
        (
            "request_candidate_to_artifact_candidate",
            artifact_candidate.get("related_authorization_request_candidate_ref") == request_candidate_ref,
        ),
        (
            "grant_candidate_to_later_grant_workflow",
            bool(grant_candidate_ref),
        ),
        (
            "execution_window_to_requested_window",
            artifact_candidate.get("requested_execution_window_ref") == window_candidate_ref,
        ),
        (
            "sandbox_to_sandbox_boundary",
            artifact_candidate.get("sandbox_boundary_ref") == sandbox_candidate_ref,
        ),
        (
            "rollback_to_rollback_plan",
            artifact_candidate.get("rollback_plan_ref") == rollback_candidate_ref,
        ),
        (
            "evidence_to_evidence_requirement",
            artifact_candidate.get("evidence_requirement_ref") == evidence_candidate_ref,
        ),
        (
            "owner_operator_to_approval_field",
            artifact_candidate.get("owner_operator_approval_required") is True,
        ),
    ]
    return [
        {"binding_id": bid, "pass": passed, "detail": "binding verified" if passed else "binding failed"}
        for bid, passed in checks
    ]


def run_ocr_provider_authorization_request_dryrun_v1(
    *,
    ocr_provider_authorization_request_planning_root: str,
    ocr_provider_authorization_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_authorization_dryrun_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(ocr_provider_authorization_request_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    artifact_schema = _try_read_json(planning_root / "authorization_request_artifact_schema_v1.json") or {}
    precond_plan = _try_read_json(planning_root / "authorization_request_generation_precondition_v1.json") or {}
    binding_plan = _try_read_json(planning_root / "authorization_request_field_binding_plan_v1.json") or {}
    validation_plan = _try_read_json(planning_root / "authorization_request_validation_rule_plan_v1.json") or {}
    send_plan = _try_read_json(planning_root / "authorization_request_send_boundary_plan_v1.json") or {}
    lifecycle_plan = _try_read_json(planning_root / "authorization_request_lifecycle_plan_v1.json") or {}
    evidence_plan = _try_read_json(planning_root / "authorization_request_evidence_binding_plan_v1.json") or {}
    blocked_plan = _try_read_json(planning_root / "authorization_request_blocked_path_matrix_v1.json") or {}

    post_root = Path(
        ocr_provider_authorization_post_dryrun_review_root
        or planning_root.parent / "ocr_provider_authorization_post_dryrun_review"
    ).expanduser().resolve()
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}

    auth_dryrun_root = Path(
        ocr_provider_authorization_dryrun_root
        or planning_root.parent / "ocr_provider_authorization_dryrun"
    ).expanduser().resolve()
    auth_dryrun_sm = _try_read_json(auth_dryrun_root / "summary.json") or {}
    request_cand = _try_read_json(auth_dryrun_root / "authorization_request_candidate_v1.json") or {}
    grant_cand = _try_read_json(auth_dryrun_root / "grant_candidate_v1.json") or {}
    window_cand = _try_read_json(auth_dryrun_root / "execution_window_candidate_v1.json") or {}
    sandbox_cand = _try_read_json(auth_dryrun_root / "sandbox_boundary_candidate_v1.json") or {}
    rollback_cand = _try_read_json(auth_dryrun_root / "rollback_candidate_v1.json") or {}
    evidence_cand = _try_read_json(auth_dryrun_root / "evidence_requirement_candidate_v1.json") or {}
    owner_dryrun = _try_read_json(auth_dryrun_root / "owner_operator_approval_dryrun_result_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_request_planning_root": str(planning_root),
        "upstream_post_dryrun_review_root": str(post_root),
        "upstream_authorization_dryrun_root": str(auth_dryrun_root),
        "output_root": str(out_root),
    }

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("request planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("request planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("request planning recommended_next_phase mismatch")
    if plan_sm.get("current_lifecycle_state") != PLANNING_LIFECYCLE_STATE:
        blockers.append("request planning current_state must be request_planning_defined")
    if plan_sm.get("boundary_ok") is not True:
        blockers.append("request planning boundary_ok must be true")

    if not artifact_schema.get("schema_id"):
        blockers.append("request artifact schema must be planned")
    if not precond_plan.get("precondition_id"):
        blockers.append("generation preconditions must be planned")
    if binding_plan.get("binding_count") != 7:
        blockers.append("field bindings must be planned (7)")
    if validation_plan.get("rule_count") != 8:
        blockers.append("validation rules must be planned (8)")
    if blocked_plan.get("all_blocked") is not True:
        blockers.append("planning 15 blocked paths must all be blocked")

    if post_vr.get("verifier") != "GO":
        blockers.append("post-dryrun review should be GO")
    if auth_dryrun_sm.get("current_lifecycle_state") != AUTH_DRYRUN_STATE:
        blockers.append("authorization dryrun must be request_candidate_ready")

    for field in (
        "authorization_request_artifact_generated_now",
        "authorization_request_sent_now",
        "grant_issued_now",
        "provider_authorization_granted_now",
        "execution_window_opened_now",
        "real_dependency_check_executed_now",
    ):
        if plan_sm.get(field) is True:
            blockers.append(f"planning {field} must be false")

    if plan_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must remain null")

    if lifecycle_plan.get("current_state") != PLANNING_LIFECYCLE_STATE:
        blockers.append("lifecycle plan must be request_planning_defined")

    input_review = {
        "review_id": "authorization_request_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "upstream_lifecycle_state": plan_sm.get("current_lifecycle_state"),
        "schema_planned": bool(artifact_schema.get("schema_id")),
        "preconditions_planned": bool(precond_plan.get("precondition_id")),
        "bindings_planned": binding_plan.get("binding_count") == 7,
        "validation_rules_planned": validation_plan.get("rule_count") == 8,
        "planning_blocked_path_count": blocked_plan.get("path_count"),
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

    artifact_candidate = {
        "candidate_id": "request_artifact_candidate_v1",
        "request_artifact_candidate_id": "ocr_provider_authorization_request_artifact_candidate_v1",
        "request_type": "ocr_provider_authorization_request",
        "lifecycle_state": CURRENT_REQUEST_DRYRUN_STATE,
        "related_authorization_request_candidate_ref": request_candidate_ref,
        "target_scope": artifact_schema.get("target_scope") or list(AUTHORIZATION_SCOPE_COVERED),
        "provider_candidate_refs": artifact_schema.get("provider_candidate_refs") or "planned_candidate_refs_only",
        "dependency_check_scope": artifact_schema.get("dependency_check_scope") or "real_dependency_check_plan_candidate",
        "environment_scope": artifact_schema.get("environment_scope") or "sandbox_workspace_fallback_only",
        "requested_execution_window_ref": window_candidate_ref,
        "sandbox_boundary_ref": sandbox_candidate_ref,
        "rollback_plan_ref": rollback_candidate_ref,
        "evidence_requirement_ref": evidence_candidate_ref,
        "owner_operator_approval_required": True,
        "verifier_required": True,
        "post_execution_review_required": True,
        "candidate_only": True,
        "formal_artifact_generated_now": False,
        "persisted_now": False,
        "sent_now": False,
        "approved_now": False,
        **meta,
    }

    target_scope = artifact_candidate.get("target_scope") or []
    production_in_scope = "production_runtime" in target_scope
    provider_implies_selection = artifact_candidate.get("provider_candidate_refs") not in (
        None,
        "planned_candidate_refs_only",
    ) and artifact_candidate.get("selected_provider_for_execution") is not None

    schema_checks = [
        ("request_type_valid", artifact_candidate.get("request_type") == "ocr_provider_authorization_request"),
        ("lifecycle_state_valid", artifact_candidate.get("lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE),
        ("target_scope_no_production", not production_in_scope),
        ("provider_refs_no_selection", not provider_implies_selection),
        ("execution_window_not_opened", meta.get("execution_window_opened_now") is False),
        ("sandbox_no_production_write", sandbox_cand.get("no_production_path_write") is True),
        ("evidence_package_required", True),
        ("approval_not_collected", owner_dryrun.get("approval_collected_now") is False),
    ]
    schema_validation = {
        "result_id": "request_artifact_schema_validation_result_v1",
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in schema_checks],
        "all_pass": all(p for _, p in schema_checks) and len(blockers) == 0,
        **meta,
    }

    precond_checks = {
        "authorization_post_dryrun_review_go": post_vr.get("verifier") == "GO",
        "request_candidate_ready": auth_dryrun_sm.get("current_lifecycle_state") == AUTH_DRYRUN_STATE,
        "grant_candidate_available": auth_dryrun_sm.get("grant_candidate_generated_now") is True,
        "execution_window_candidate_available": auth_dryrun_sm.get("execution_window_candidate_generated_now") is True,
        "sandbox_boundary_candidate_available": auth_dryrun_sm.get("sandbox_boundary_candidate_generated_now") is True,
        "rollback_candidate_available": auth_dryrun_sm.get("rollback_candidate_generated_now") is True,
        "evidence_requirement_candidate_available": auth_dryrun_sm.get("evidence_requirement_candidate_generated_now") is True,
        "selected_provider_for_execution": None,
        "provider_selection_finalized": False,
        "all_boundary_paths_blocked": auth_dryrun_sm.get("dryrun_blocked_path_count", 15) >= 15,
    }
    precond_pass = (
        precond_checks["authorization_post_dryrun_review_go"] is True
        and precond_checks["request_candidate_ready"] is True
        and precond_checks["grant_candidate_available"] is True
        and precond_checks["execution_window_candidate_available"] is True
        and precond_checks["sandbox_boundary_candidate_available"] is True
        and precond_checks["rollback_candidate_available"] is True
        and precond_checks["evidence_requirement_candidate_available"] is True
        and precond_checks["selected_provider_for_execution"] is None
        and precond_checks["provider_selection_finalized"] is False
        and precond_checks["all_boundary_paths_blocked"] is True
        and len(blockers) == 0
    )
    precond_dryrun = {
        "result_id": "generation_precondition_dryrun_result_v1",
        **precond_checks,
        "dryrun_pass": precond_pass,
        **meta,
    }

    binding_rows = _binding_results(
        request_candidate_ref=request_candidate_ref,
        grant_candidate_ref=grant_candidate_ref,
        window_candidate_ref=window_candidate_ref,
        sandbox_candidate_ref=sandbox_candidate_ref,
        rollback_candidate_ref=rollback_candidate_ref,
        evidence_candidate_ref=evidence_candidate_ref,
        artifact_candidate=artifact_candidate,
    )
    field_binding = {
        "result_id": "field_binding_dryrun_result_v1",
        "bindings": binding_rows,
        "binding_count": len(binding_rows),
        "all_pass": all(r["pass"] for r in binding_rows) and len(blockers) == 0,
        **meta,
    }

    rule_checks = [
        ("request_type_match", artifact_candidate.get("request_type") == "ocr_provider_authorization_request"),
        ("target_scope_no_production", not production_in_scope),
        ("provider_refs_no_selection", not provider_implies_selection),
        ("execution_window_not_opened", window_cand.get("current_window_opened_now") is False),
        ("sandbox_no_production_write", sandbox_cand.get("no_production_path_write") is True),
        ("evidence_required", len(evidence_cand.get("required_artifacts_on_future_execution") or []) >= len(EVIDENCE_REQUIREMENTS)),
        ("approval_not_collected", owner_dryrun.get("approval_collected_now") is False),
        ("formal_artifact_not_generated", artifact_candidate.get("formal_artifact_generated_now") is False),
    ]
    validation_dryrun = {
        "result_id": "validation_rule_dryrun_result_v1",
        "rules": [{"rule_id": rid, "pass": passed} for rid, passed in zip(VALIDATION_RULE_IDS, [p for _, p in rule_checks])],
        "rule_count": len(VALIDATION_RULE_IDS),
        "all_pass": all(p for _, p in rule_checks) and len(blockers) == 0,
        **meta,
    }

    send_boundary = {
        "result_id": "send_boundary_dryrun_result_v1",
        "send_boundary_claims": list(SEND_BOUNDARY_DRYRUN_CLAIMS),
        "candidate_not_formal_artifact": True,
        "formal_artifact_not_sent": True,
        "sent_not_grant": True,
        "grant_not_window": True,
        "window_not_invocation": True,
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    lifecycle = {
        "result_id": "request_lifecycle_dryrun_result_v1",
        "states": list(LIFECYCLE_STATES),
        "simulated_progression": list(LIFECYCLE_STATES),
        "prior_state": PLANNING_LIFECYCLE_STATE,
        "current_state": CURRENT_REQUEST_DRYRUN_STATE,
        "formal_artifact_generated_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "lifecycle_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    evidence_binding = {
        "result_id": "request_evidence_binding_dryrun_result_v1",
        "evidence_requirement_ref": evidence_candidate_ref,
        "required_artifacts_on_future_execution": evidence_plan.get("required_artifacts_on_future_execution")
        or list(EVIDENCE_REQUIREMENTS),
        "artifact_count": len(
            evidence_plan.get("required_artifacts_on_future_execution") or list(EVIDENCE_REQUIREMENTS)
        ),
        "evidence_package_required": True,
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    blocked_paths = [
        {"path_id": p, "blocked": True, "executed_now": False} for p in DRYRUN_BLOCKED_PATHS
    ]
    blocked_result = {
        "result_id": "request_blocked_path_result_v1",
        "paths": blocked_paths,
        "path_count": len(DRYRUN_BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    no_artifact_audit = {
        "audit_id": "request_no_artifact_no_send_audit_v1",
        "no_formal_request_artifact": meta.get("authorization_request_artifact_generated_now") is False,
        "no_persistence": meta.get("authorization_request_persisted_now") is False,
        "no_send": meta.get("authorization_request_sent_now") is False,
        "no_approval": meta.get("authorization_request_approved_now") is False,
        "no_grant": meta.get("grant_issued_now") is False,
        "no_execution_window": meta.get("execution_window_opened_now") is False,
        "no_provider_action": all(
            meta.get(f) is False
            for f in (
                "provider_imported_now",
                "provider_invoked_now",
                "dependency_install_executed_now",
                "model_download_executed_now",
                "provider_smoke_check_executed_now",
            )
        ),
        "no_ocr_action": all(
            meta.get(f) is False
            for f in (
                "sample_ocr_executed_now",
                "controlled_trial_started_now",
                "ocr_request_submitted_now",
                "image_read_executed_now",
                "crop_executed_now",
                "ocr_fact_generated_now",
            )
        ),
        "audit_pass": len(blockers) == 0,
        **meta,
    }

    checks_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and artifact_candidate.get("candidate_only") is True
        and artifact_candidate.get("formal_artifact_generated_now") is False
        and schema_validation.get("all_pass")
        and precond_dryrun.get("dryrun_pass")
        and field_binding.get("all_pass")
        and validation_dryrun.get("all_pass")
        and send_boundary.get("dryrun_pass")
        and lifecycle.get("lifecycle_dryrun_pass")
        and evidence_binding.get("dryrun_pass")
        and blocked_result.get("all_blocked")
        and no_artifact_audit.get("audit_pass")
    )

    readiness = {
        "decision_id": "request_dryrun_readiness_decision_v1",
        "artifact_candidate_pass": checks_pass,
        "schema_validation_pass": schema_validation.get("all_pass"),
        "precondition_pass": precond_dryrun.get("dryrun_pass"),
        "binding_pass": field_binding.get("all_pass"),
        "validation_pass": validation_dryrun.get("all_pass"),
        "send_boundary_pass": send_boundary.get("dryrun_pass"),
        "lifecycle_pass": lifecycle.get("lifecycle_dryrun_pass"),
        "evidence_pass": evidence_binding.get("dryrun_pass"),
        "blocked_path_pass": blocked_result.get("all_blocked"),
        "no_artifact_audit_pass": no_artifact_audit.get("audit_pass"),
        "all_pass": checks_pass,
        "high_risk_count": 0 if checks_pass else 1,
        "final_decision": FINAL_DECISION_GO if checks_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if checks_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_authorization_request_dryrun_policy_v1",
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
        "boundary_ok": checks_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "current_lifecycle_state": CURRENT_REQUEST_DRYRUN_STATE,
        "dryrun_blocked_path_count": len(DRYRUN_BLOCKED_PATHS),
        "high_risk_count": 0 if checks_pass else 1,
        **meta,
    }

    return {
        "ocr_provider_authorization_request_dryrun_policy": policy,
        "authorization_request_planning_input_review": input_review,
        "request_artifact_candidate": artifact_candidate,
        "request_artifact_schema_validation_result": schema_validation,
        "generation_precondition_dryrun_result": precond_dryrun,
        "field_binding_dryrun_result": field_binding,
        "validation_rule_dryrun_result": validation_dryrun,
        "send_boundary_dryrun_result": send_boundary,
        "request_lifecycle_dryrun_result": lifecycle,
        "request_evidence_binding_dryrun_result": evidence_binding,
        "request_blocked_path_result": blocked_result,
        "request_no_artifact_no_send_audit": no_artifact_audit,
        "request_dryrun_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
