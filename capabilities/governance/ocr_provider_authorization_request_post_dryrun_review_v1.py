# -*- coding: utf-8 -*-
"""OCR Provider Authorization Request Post-DryRun Review v1 — closure only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
    DRYRUN_BLOCKED_PATHS,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO as REQUEST_DRYRUN_FINAL_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO as REQUEST_DRYRUN_NEXT_PHASE,
    PHASE_ID as REQUEST_DRYRUN_PHASE,
    SCOPE as REQUEST_DRYRUN_SCOPE,
    SEND_BOUNDARY_DRYRUN_CLAIMS,
    VALIDATION_RULE_IDS,
)
from capabilities.governance.ocr_provider_authorization_request_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as REQUEST_PLANNING_STATE,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-Request-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "ocr_provider_authorization_request_post_dryrun_review_only"
SOURCE_CHAIN = "ocr_provider_authorization_request_post_dryrun_review_v1"

UPSTREAM_REQUEST_DRYRUN_FINAL = REQUEST_DRYRUN_FINAL_GO
UPSTREAM_REQUEST_DRYRUN_NEXT = REQUEST_DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_FORMAL_REQUEST_ARTIFACT_GENERATION_PLANNING"
)
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Request-Issue-Review-v1-001"

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_request_artifact_candidate_generated_now",
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

NON_CLAIMS: Tuple[str, ...] = (
    "Post-DryRun Review GO ≠ formal request artifact generated",
    "request_artifact_candidate_ready ≠ request sent",
    "formal request artifact generation planning ≠ request generation",
    "request artifact candidate ≠ approval",
    "request artifact candidate ≠ grant",
    "next planning ≠ real dependency check allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_request_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_request_post_dryrun_review_only": True,
        "review_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_request_artifact_candidate_generated_now"] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_pass(row: Dict[str, Any]) -> bool:
    if row.get("pass") is True:
        return True
    if row.get("passed") is True:
        return True
    return False


def run_ocr_provider_authorization_request_post_dryrun_review_v1(
    *,
    ocr_provider_authorization_request_dryrun_root: str,
    ocr_provider_authorization_request_planning_root: Optional[str] = None,
    ocr_provider_authorization_post_dryrun_review_root: Optional[str] = None,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(ocr_provider_authorization_request_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    readiness = _try_read_json(dryrun_root / "request_dryrun_readiness_decision_v1.json") or {}

    planning_root = Path(
        ocr_provider_authorization_request_planning_root
        or dryrun_root.parent / "ocr_provider_authorization_request_planning"
    ).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}

    post_root = Path(
        ocr_provider_authorization_post_dryrun_review_root
        or dryrun_root.parent / "ocr_provider_authorization_post_dryrun_review"
    ).expanduser().resolve()
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}

    candidate = _try_read_json(dryrun_root / "request_artifact_candidate_v1.json") or {}
    schema_val = _try_read_json(dryrun_root / "request_artifact_schema_validation_result_v1.json") or {}
    precond = _try_read_json(dryrun_root / "generation_precondition_dryrun_result_v1.json") or {}
    bindings = _try_read_json(dryrun_root / "field_binding_dryrun_result_v1.json") or {}
    validation = _try_read_json(dryrun_root / "validation_rule_dryrun_result_v1.json") or {}
    send_boundary = _try_read_json(dryrun_root / "send_boundary_dryrun_result_v1.json") or {}
    lifecycle = _try_read_json(dryrun_root / "request_lifecycle_dryrun_result_v1.json") or {}
    evidence = _try_read_json(dryrun_root / "request_evidence_binding_dryrun_result_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "request_blocked_path_result_v1.json") or {}
    audit = _try_read_json(dryrun_root / "request_no_artifact_no_send_audit_v1.json") or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    )
    meta = {
        **_review_meta(),
        "upstream_request_dryrun_root": str(dryrun_root),
        "upstream_request_planning_root": str(planning_root),
        "upstream_post_dryrun_review_root": str(post_root),
        "review_output_root": str(out_root),
    }

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("request dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_REQUEST_DRYRUN_FINAL:
        blockers.append("request dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_REQUEST_DRYRUN_NEXT:
        blockers.append("request dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("request dryrun boundary_ok must be true")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("request dryrun simulated must be true")
    if dryrun_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("current_state must be request_artifact_candidate_ready")
    if dryrun_sm.get("request_artifact_candidate_generated_now") is not True:
        blockers.append("request_artifact_candidate_generated_now must be true")

    for field in (
        "authorization_request_artifact_generated_now",
        "authorization_request_persisted_now",
        "authorization_request_sent_now",
        "authorization_request_approved_now",
        "grant_issued_now",
        "provider_authorization_granted_now",
        "execution_window_opened_now",
        "real_dependency_check_executed_now",
    ):
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    if dryrun_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must remain null")

    if readiness.get("all_pass") is not True:
        blockers.append("request dryrun readiness all_pass required")

    if post_vr.get("verifier") != "GO":
        blockers.append("authorization post-dryrun review should be GO")
    if plan_sm.get("boundary_ok") is not True:
        blockers.append("request planning boundary_ok must be true")

    input_review = {
        "review_id": "authorization_request_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": REQUEST_DRYRUN_PHASE,
        "upstream_scope": REQUEST_DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "upstream_simulated": dryrun_sm.get("simulated"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    candidate_issues: List[Dict[str, Any]] = []
    for key, expected in (
        ("request_type", "ocr_provider_authorization_request"),
        ("lifecycle_state", CURRENT_REQUEST_DRYRUN_STATE),
        ("candidate_only", True),
        ("formal_artifact_generated_now", False),
        ("persisted_now", False),
        ("sent_now", False),
        ("approved_now", False),
        ("owner_operator_approval_required", True),
        ("verifier_required", True),
        ("post_execution_review_required", True),
    ):
        if candidate.get(key) != expected:
            candidate_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    for key in (
        "request_artifact_candidate_id",
        "related_authorization_request_candidate_ref",
        "target_scope",
        "provider_candidate_refs",
        "dependency_check_scope",
        "environment_scope",
        "requested_execution_window_ref",
        "sandbox_boundary_ref",
        "rollback_plan_ref",
        "evidence_requirement_ref",
    ):
        if not candidate.get(key):
            candidate_issues.append({"issue_id": key, "detail": "must be present"})

    candidate_review = {
        "review_id": "request_artifact_candidate_review_v1",
        "request_artifact_candidate_id": candidate.get("request_artifact_candidate_id"),
        "issues": candidate_issues,
        "review_pass": len(candidate_issues) == 0,
        **meta,
    }

    schema_checks = schema_val.get("checks") or []
    schema_issues: List[Dict[str, Any]] = []
    if schema_val.get("all_pass") is not True:
        schema_issues.append({"issue_id": "all_pass", "detail": "schema validation must pass"})
    if len(schema_checks) != 8:
        schema_issues.append({"issue_id": "count", "detail": "expected 8 checks"})
    for row in schema_checks:
        if not _check_pass(row):
            schema_issues.append({"issue_id": row.get("check_id"), "detail": "must pass"})

    schema_review = {
        "review_id": "request_artifact_schema_validation_review_v1",
        "check_count": len(schema_checks),
        "issues": schema_issues,
        "review_pass": len(schema_issues) == 0 and schema_val.get("all_pass") is True,
        **meta,
    }

    precond_issues: List[Dict[str, Any]] = []
    if precond.get("dryrun_pass") is not True:
        precond_issues.append({"issue_id": "dryrun_pass", "detail": "must be true"})
    precond_expected = {
        "authorization_post_dryrun_review_go": True,
        "request_candidate_ready": True,
        "grant_candidate_available": True,
        "execution_window_candidate_available": True,
        "sandbox_boundary_candidate_available": True,
        "rollback_candidate_available": True,
        "evidence_requirement_candidate_available": True,
        "provider_selection_finalized": False,
        "all_boundary_paths_blocked": True,
    }
    for key, expected in precond_expected.items():
        if precond.get(key) != expected:
            precond_issues.append({"issue_id": key, "detail": f"expected {expected}"})
    if precond.get("selected_provider_for_execution") is not None:
        precond_issues.append({"issue_id": "selected_provider", "detail": "must be null"})

    precond_review = {
        "review_id": "generation_precondition_review_v1",
        "issues": precond_issues,
        "review_pass": len(precond_issues) == 0,
        **meta,
    }

    binding_rows = bindings.get("bindings") or []
    binding_issues: List[Dict[str, Any]] = []
    if bindings.get("all_pass") is not True:
        binding_issues.append({"issue_id": "all_pass", "detail": "bindings must pass"})
    if len(binding_rows) != 7:
        binding_issues.append({"issue_id": "count", "detail": "expected 7 bindings"})
    for row in binding_rows:
        if not _check_pass(row):
            binding_issues.append({"issue_id": row.get("binding_id"), "detail": "must pass"})

    binding_review = {
        "review_id": "field_binding_review_v1",
        "binding_count": len(binding_rows),
        "issues": binding_issues,
        "review_pass": len(binding_issues) == 0 and bindings.get("all_pass") is True,
        **meta,
    }

    rule_rows = validation.get("rules") or []
    validation_issues: List[Dict[str, Any]] = []
    if validation.get("all_pass") is not True:
        validation_issues.append({"issue_id": "all_pass", "detail": "validation rules must pass"})
    if len(rule_rows) != len(VALIDATION_RULE_IDS):
        validation_issues.append({"issue_id": "count", "detail": f"expected {len(VALIDATION_RULE_IDS)} rules"})
    for row in rule_rows:
        if not _check_pass(row):
            validation_issues.append({"issue_id": row.get("rule_id"), "detail": "must pass"})

    validation_review = {
        "review_id": "validation_rule_review_v1",
        "rule_count": len(rule_rows),
        "issues": validation_issues,
        "review_pass": len(validation_issues) == 0 and validation.get("all_pass") is True,
        **meta,
    }

    send_issues: List[Dict[str, Any]] = []
    if send_boundary.get("dryrun_pass") is not True:
        send_issues.append({"issue_id": "dryrun_pass", "detail": "must be true"})
    claims = send_boundary.get("send_boundary_claims") or []
    if len(claims) != len(SEND_BOUNDARY_DRYRUN_CLAIMS):
        send_issues.append({"issue_id": "claims", "detail": f"expected {len(SEND_BOUNDARY_DRYRUN_CLAIMS)} claims"})
    for flag in (
        "candidate_not_formal_artifact",
        "formal_artifact_not_sent",
        "sent_not_grant",
        "grant_not_window",
        "window_not_invocation",
    ):
        if send_boundary.get(flag) is not True:
            send_issues.append({"issue_id": flag, "detail": "must be true"})

    send_review = {
        "review_id": "send_boundary_review_v1",
        "issues": send_issues,
        "review_pass": len(send_issues) == 0,
        **meta,
    }

    lifecycle_issues: List[Dict[str, Any]] = []
    if lifecycle.get("prior_state") != REQUEST_PLANNING_STATE:
        lifecycle_issues.append({"issue_id": "prior", "detail": "request_planning_defined"})
    if lifecycle.get("current_state") != CURRENT_REQUEST_DRYRUN_STATE:
        lifecycle_issues.append({"issue_id": "current", "detail": "request_artifact_candidate_ready"})
    if len(lifecycle.get("states") or []) != len(LIFECYCLE_STATES):
        lifecycle_issues.append({"issue_id": "states", "detail": f"expected {len(LIFECYCLE_STATES)}"})
    if lifecycle.get("lifecycle_dryrun_pass") is not True:
        lifecycle_issues.append({"issue_id": "lifecycle_pass", "detail": "must be true"})
    for flag in (
        "formal_artifact_generated_now",
        "request_sent_now",
        "grant_issued_now",
        "execution_window_opened_now",
    ):
        if lifecycle.get(flag) is not False:
            lifecycle_issues.append({"issue_id": flag, "detail": "must be false"})

    lifecycle_review = {
        "review_id": "request_lifecycle_review_v1",
        "prior_state": lifecycle.get("prior_state"),
        "current_state": lifecycle.get("current_state"),
        "state_count": len(lifecycle.get("states") or []),
        "issues": lifecycle_issues,
        "review_pass": len(lifecycle_issues) == 0,
        **meta,
    }

    evidence_issues: List[Dict[str, Any]] = []
    if evidence.get("dryrun_pass") is not True:
        evidence_issues.append({"issue_id": "dryrun_pass", "detail": "must be true"})
    if evidence.get("artifact_count") != len(EVIDENCE_REQUIREMENTS):
        evidence_issues.append({"issue_id": "count", "detail": f"expected {len(EVIDENCE_REQUIREMENTS)}"})
    if evidence.get("evidence_package_required") is not True:
        evidence_issues.append({"issue_id": "required", "detail": "must be true"})

    evidence_review = {
        "review_id": "request_evidence_binding_review_v1",
        "artifact_count": evidence.get("artifact_count"),
        "issues": evidence_issues,
        "review_pass": len(evidence_issues) == 0,
        **meta,
    }

    blocked_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in (blocked.get("paths") or [])}
    if blocked.get("all_blocked") is not True:
        blocked_issues.append({"issue_id": "all_blocked", "detail": "must be true"})
    if len(paths) != len(DRYRUN_BLOCKED_PATHS):
        blocked_issues.append({"issue_id": "count", "detail": f"expected {len(DRYRUN_BLOCKED_PATHS)}"})
    for pid in DRYRUN_BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            blocked_issues.append({"issue_id": pid, "detail": "must be blocked"})

    blocked_review = {
        "review_id": "request_blocked_path_review_v1",
        "paths_total": len(DRYRUN_BLOCKED_PATHS),
        "all_blocked": blocked.get("all_blocked"),
        "issues": blocked_issues,
        "review_pass": len(blocked_issues) == 0,
        **meta,
    }

    audit_issues: List[Dict[str, Any]] = []
    if audit.get("audit_pass") is not True:
        audit_issues.append({"issue_id": "audit_pass", "detail": "must be true"})
    for flag in (
        "no_formal_request_artifact",
        "no_persistence",
        "no_send",
        "no_approval",
        "no_grant",
        "no_execution_window",
        "no_provider_action",
        "no_ocr_action",
    ):
        if audit.get(flag) is not True:
            audit_issues.append({"issue_id": flag, "detail": "must be true"})

    audit_review = {
        "review_id": "request_no_artifact_no_send_review_v1",
        "issues": audit_issues,
        "review_pass": len(audit_issues) == 0 and audit.get("audit_pass") is True,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and candidate_review.get("review_pass")
        and schema_review.get("review_pass")
        and precond_review.get("review_pass")
        and binding_review.get("review_pass")
        and validation_review.get("review_pass")
        and send_review.get("review_pass")
        and lifecycle_review.get("review_pass")
        and evidence_review.get("review_pass")
        and blocked_review.get("review_pass")
        and audit_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "authorization_request_closure_decision_v1",
        "ocr_provider_authorization_request_dryrun_closed": boundary_ok,
        "request_artifact_candidate_trusted": boundary_ok,
        "ready_for_formal_request_artifact_generation_planning": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_formal_request_artifact_generation_planning": boundary_ok,
        "do_not_generate_formal_request_artifact_now": True,
        "do_not_persist_request_now": True,
        "do_not_send_request_now": True,
        "do_not_collect_approval_now": True,
        "do_not_grant_authorization_now": True,
        "do_not_open_execution_window_now": True,
        "do_not_execute_real_dependency_check_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        "rationale": (
            "After request dryrun closure, plan formal request artifact generation rules only — "
            "no artifact generation, no send, no grant, no real dependency check"
        ),
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(NON_CLAIMS),
        **meta,
    }

    all_issue_ids = (
        blockers
        + [i["issue_id"] for i in candidate_issues]
        + [i["issue_id"] for i in schema_issues]
        + [i["issue_id"] for i in precond_issues]
        + [i["issue_id"] for i in binding_issues]
        + [i["issue_id"] for i in validation_issues]
        + [i["issue_id"] for i in send_issues]
        + [i["issue_id"] for i in lifecycle_issues]
        + [i["issue_id"] for i in blocked_issues]
        + [i["issue_id"] for i in audit_issues]
    )

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": all_issue_ids,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "ocr_provider_authorization_request_dryrun_closed": boundary_ok,
        "current_lifecycle_state": CURRENT_REQUEST_DRYRUN_STATE,
        **meta,
    }

    return {
        "authorization_request_dryrun_input_review": input_review,
        "request_artifact_candidate_review": candidate_review,
        "request_artifact_schema_validation_review": schema_review,
        "generation_precondition_review": precond_review,
        "field_binding_review": binding_review,
        "validation_rule_review": validation_review,
        "send_boundary_review": send_review,
        "request_lifecycle_review": lifecycle_review,
        "request_evidence_binding_review": evidence_review,
        "request_blocked_path_review": blocked_review,
        "request_no_artifact_no_send_review": audit_review,
        "authorization_request_closure_decision": closure,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
