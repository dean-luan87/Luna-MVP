# -*- coding: utf-8 -*-
"""OCR Provider Authorization Post-DryRun Review v1 — closure only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    BOUNDARY_FALSE as DRYRUN_BOUNDARY_FALSE,
    CURRENT_DRYRUN_STATE,
    DRYRUN_BLOCKED_PATHS,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO as DRYRUN_FINAL_GO,
    NEXT_PHASE_GO as DRYRUN_NEXT_PHASE,
    PHASE_ID as DRYRUN_PHASE,
    SCOPE as DRYRUN_SCOPE,
)
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as PLANNING_LIFECYCLE_STATE,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "ocr_provider_authorization_post_dryrun_review_only"
SOURCE_CHAIN = "ocr_provider_authorization_post_dryrun_review_v1"

UPSTREAM_DRYRUN_FINAL = DRYRUN_FINAL_GO
UPSTREAM_DRYRUN_NEXT = DRYRUN_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_AUTHORIZATION_POST_DRYRUN_REVIEW_CLOSED_READY_FOR_AUTHORIZATION_REQUEST_PLANNING"
)
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_POST_DRYRUN_REVIEW_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Request-Planning-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Issue-Review-v1-001"

BOUNDARY_FALSE_REVIEW: Tuple[str, ...] = (
    "new_authorization_request_candidate_generated_now",
    "new_grant_candidate_generated_now",
    "new_execution_window_candidate_generated_now",
    "authorization_request_artifact_generated_now",
    "authorization_request_sent_now",
    "provider_authorization_granted_now",
    "grant_issued_now",
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
    "Post-DryRun Review GO ≠ request artifact generated",
    "request_candidate_ready ≠ request sent",
    "grant_candidate ≠ grant issued",
    "execution_window_candidate ≠ execution window opened",
    "authorization dryrun closure ≠ provider authorization granted",
    "next request planning ≠ real dependency check allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_post_dryrun_review"
)


def _review_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_post_dryrun_review_only": True,
        "review_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE_REVIEW:
        meta[field] = False
    meta["new_authorization_request_candidate_generated_now"] = False
    meta["new_grant_candidate_generated_now"] = False
    meta["new_execution_window_candidate_generated_now"] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_provider_authorization_post_dryrun_review_v1(
    *,
    ocr_provider_authorization_dryrun_root: str,
    ocr_provider_authorization_planning_root: Optional[str] = None,
    review_output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    dryrun_root = Path(ocr_provider_authorization_dryrun_root).expanduser().resolve()
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    readiness = _try_read_json(dryrun_root / "authorization_dryrun_readiness_decision_v1.json") or {}

    planning_root = Path(
        ocr_provider_authorization_planning_root
        or dryrun_root.parent / "ocr_provider_authorization_planning"
    ).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}

    request = _try_read_json(dryrun_root / "authorization_request_candidate_v1.json") or {}
    grant = _try_read_json(dryrun_root / "grant_candidate_v1.json") or {}
    window = _try_read_json(dryrun_root / "execution_window_candidate_v1.json") or {}
    sandbox = _try_read_json(dryrun_root / "sandbox_boundary_candidate_v1.json") or {}
    rollback = _try_read_json(dryrun_root / "rollback_candidate_v1.json") or {}
    evidence = _try_read_json(dryrun_root / "evidence_requirement_candidate_v1.json") or {}
    owner = _try_read_json(dryrun_root / "owner_operator_approval_dryrun_result_v1.json") or {}
    selection = _try_read_json(dryrun_root / "provider_selection_binding_dryrun_result_v1.json") or {}
    lifecycle = _try_read_json(dryrun_root / "authorization_lifecycle_dryrun_result_v1.json") or {}
    boundary = _try_read_json(dryrun_root / "authorization_boundary_guard_dryrun_result_v1.json") or {}
    blocked = _try_read_json(dryrun_root / "authorization_blocked_path_result_v1.json") or {}

    out_root = (
        Path(review_output_root).expanduser().resolve()
        if review_output_root
        else dryrun_root.parent / "ocr_provider_authorization_post_dryrun_review"
    )
    meta = {
        **_review_meta(),
        "upstream_dryrun_root": str(dryrun_root),
        "upstream_planning_root": str(planning_root),
        "review_output_root": str(out_root),
    }

    dryrun_go = dryrun_vr.get("verifier") == "GO" and dryrun_vr.get("passed") is True
    if not dryrun_go:
        blockers.append("dryrun verifier must be GO")
    if dryrun_sm.get("final_decision") != UPSTREAM_DRYRUN_FINAL:
        blockers.append("dryrun final_decision mismatch")
    if dryrun_sm.get("recommended_next_phase") != UPSTREAM_DRYRUN_NEXT:
        blockers.append("dryrun recommended_next_phase mismatch")
    if dryrun_sm.get("boundary_ok") is not True:
        blockers.append("dryrun boundary_ok must be true")
    if dryrun_sm.get("simulated") is not True:
        blockers.append("dryrun simulated must be true")

    candidate_flags = (
        "authorization_request_candidate_generated_now",
        "grant_candidate_generated_now",
        "execution_window_candidate_generated_now",
        "sandbox_boundary_candidate_generated_now",
        "rollback_candidate_generated_now",
        "evidence_requirement_candidate_generated_now",
    )
    for flag in candidate_flags:
        if dryrun_sm.get(flag) is not True:
            blockers.append(f"{flag} must be true in dryrun")

    if dryrun_sm.get("current_lifecycle_state") != CURRENT_DRYRUN_STATE:
        blockers.append("dryrun current_state must be request_candidate_ready")

    for field in DRYRUN_BOUNDARY_FALSE:
        if dryrun_sm.get(field) is True:
            blockers.append(f"dryrun {field} must be false")

    if plan_sm.get("current_lifecycle_state") != PLANNING_LIFECYCLE_STATE:
        blockers.append("planning should have been planning_defined")

    if readiness.get("all_pass") is not True:
        blockers.append("dryrun readiness all_pass required")

    input_review = {
        "review_id": "ocr_provider_authorization_dryrun_input_review_v1",
        "upstream_root": str(dryrun_root),
        "upstream_phase": DRYRUN_PHASE,
        "upstream_scope": DRYRUN_SCOPE,
        "upstream_verifier_go": dryrun_go,
        "upstream_final_decision": dryrun_sm.get("final_decision"),
        "upstream_simulated": dryrun_sm.get("simulated"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    request_issues: List[Dict[str, Any]] = []
    for key, expected in (
        ("request_type", "ocr_provider_authorization_request"),
        ("candidate_only", True),
        ("request_artifact_generated_now", False),
        ("request_sent_now", False),
        ("execution_window_required", True),
        ("sandbox_required", True),
        ("evidence_package_required", True),
    ):
        if request.get(key) != expected:
            request_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    request_review = {
        "review_id": "authorization_request_candidate_review_v1",
        "request_id": request.get("request_id"),
        "issues": request_issues,
        "review_pass": len(request_issues) == 0,
        **meta,
    }

    grant_issues: List[Dict[str, Any]] = []
    for key, expected in (
        ("candidate_only", True),
        ("current_grant_issued_now", False),
        ("provider_authorization_granted_now", False),
        ("post_execution_review_required", True),
    ):
        if grant.get(key) != expected:
            grant_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    grant_review = {
        "review_id": "grant_candidate_review_v1",
        "grant_candidate_id": grant.get("grant_candidate_id"),
        "issues": grant_issues,
        "review_pass": len(grant_issues) == 0,
        **meta,
    }

    window_issues: List[Dict[str, Any]] = []
    for key, expected in (
        ("current_window_opened_now", False),
        ("no_production_write", True),
        ("no_network_by_default", True),
        ("candidate_only", True),
    ):
        if window.get(key) != expected:
            window_issues.append({"issue_id": key, "detail": f"expected {expected}"})

    window_review = {
        "review_id": "execution_window_candidate_review_v1",
        "issues": window_issues,
        "review_pass": len(window_issues) == 0,
        **meta,
    }

    sandbox_issues: List[Dict[str, Any]] = []
    for key in (
        "workspace_fallback_only",
        "no_production_path_write",
        "no_global_environment_modification",
        "no_untracked_install",
        "no_model_download_without_separate_authorization",
        "no_cache_mutation_without_approval",
        "no_real_ocr_invocation_without_controlled_trial_authorization",
    ):
        if sandbox.get(key) is not True:
            sandbox_issues.append({"issue_id": key, "detail": "must be true"})

    sandbox_review = {
        "review_id": "sandbox_boundary_candidate_review_v1",
        "issues": sandbox_issues,
        "review_pass": len(sandbox_issues) == 0,
        **meta,
    }

    rollback_issues: List[Dict[str, Any]] = []
    for key in (
        "failed_check_does_not_trigger_install",
        "failed_import_does_not_trigger_repair",
        "failed_model_cache_check_does_not_trigger_download",
        "failed_smoke_does_not_trigger_provider_switch",
        "all_outputs_evidence_only",
    ):
        if rollback.get(key) is not True:
            rollback_issues.append({"issue_id": key, "detail": "must be true"})
    if rollback.get("rollback_executed_now") is not False:
        rollback_issues.append({"issue_id": "rollback_executed_now", "detail": "must be false"})

    rollback_review = {
        "review_id": "rollback_candidate_review_v1",
        "issues": rollback_issues,
        "review_pass": len(rollback_issues) == 0,
        **meta,
    }

    evidence_issues: List[Dict[str, Any]] = []
    artifacts = evidence.get("required_artifacts_on_future_execution") or []
    if len(artifacts) != len(EVIDENCE_REQUIREMENTS):
        evidence_issues.append({"issue_id": "count", "detail": f"expected {len(EVIDENCE_REQUIREMENTS)}"})
    if set(artifacts) != set(EVIDENCE_REQUIREMENTS):
        evidence_issues.append({"issue_id": "artifacts", "detail": "artifact set mismatch"})
    if evidence.get("candidate_only") is not True:
        evidence_issues.append({"issue_id": "candidate_only", "detail": "must be true"})

    evidence_review = {
        "review_id": "evidence_requirement_candidate_review_v1",
        "artifact_count": len(artifacts),
        "issues": evidence_issues,
        "review_pass": len(evidence_issues) == 0,
        **meta,
    }

    owner_issues: List[Dict[str, Any]] = []
    if owner.get("approval_collected_now") is not False:
        owner_issues.append({"issue_id": "collected", "detail": "must be false"})
    if owner.get("approval_required_for_real_dependency_check") is not True:
        owner_issues.append({"issue_id": "real_dep", "detail": "must be true"})

    owner_review = {
        "review_id": "owner_operator_approval_review_v1",
        "issues": owner_issues,
        "review_pass": len(owner_issues) == 0,
        **meta,
    }

    selection_issues: List[Dict[str, Any]] = []
    if selection.get("selected_provider_for_execution") is not None:
        selection_issues.append({"issue_id": "provider", "detail": "must be null"})
    if selection.get("provider_selection_finalized_now") is not False:
        selection_issues.append({"issue_id": "finalized", "detail": "must be false"})

    selection_review = {
        "review_id": "provider_selection_binding_review_v1",
        "issues": selection_issues,
        "review_pass": len(selection_issues) == 0,
        **meta,
    }

    lifecycle_issues: List[Dict[str, Any]] = []
    if lifecycle.get("prior_state") != PLANNING_LIFECYCLE_STATE:
        lifecycle_issues.append({"issue_id": "prior", "detail": "planning_defined"})
    if lifecycle.get("current_state") != CURRENT_DRYRUN_STATE:
        lifecycle_issues.append({"issue_id": "current", "detail": "request_candidate_ready"})
    for flag in ("request_generated_now", "request_sent_now", "grant_issued_now", "execution_window_opened_now"):
        if lifecycle.get(flag) is not False:
            lifecycle_issues.append({"issue_id": flag, "detail": "must be false"})

    lifecycle_review = {
        "review_id": "authorization_lifecycle_review_v1",
        "prior_state": lifecycle.get("prior_state"),
        "current_state": lifecycle.get("current_state"),
        "issues": lifecycle_issues,
        "review_pass": len(lifecycle_issues) == 0,
        **meta,
    }

    boundary_issues: List[Dict[str, Any]] = []
    paths = {p.get("path_id"): p for p in (boundary.get("paths") or blocked.get("paths") or [])}
    if boundary.get("all_blocked") is not True:
        boundary_issues.append({"issue_id": "all_blocked", "detail": "must be true"})
    if len(paths) != len(DRYRUN_BLOCKED_PATHS):
        boundary_issues.append({"issue_id": "count", "detail": f"expected {len(DRYRUN_BLOCKED_PATHS)}"})
    for pid in DRYRUN_BLOCKED_PATHS:
        row = paths.get(pid)
        if not row or row.get("blocked") is not True:
            boundary_issues.append({"issue_id": pid, "detail": "must be blocked"})

    boundary_review = {
        "review_id": "authorization_boundary_guard_review_v1",
        "path_count": len(DRYRUN_BLOCKED_PATHS),
        "all_blocked": boundary.get("all_blocked"),
        "issues": boundary_issues,
        "review_pass": len(boundary_issues) == 0,
        **meta,
    }

    blocked_review = {
        "review_id": "authorization_blocked_path_review_v1",
        "paths_total": len(DRYRUN_BLOCKED_PATHS),
        "all_blocked": blocked.get("all_blocked"),
        "issues": boundary_issues,
        "review_pass": len(boundary_issues) == 0,
        **meta,
    }

    reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and request_review.get("review_pass")
        and grant_review.get("review_pass")
        and window_review.get("review_pass")
        and sandbox_review.get("review_pass")
        and rollback_review.get("review_pass")
        and evidence_review.get("review_pass")
        and owner_review.get("review_pass")
        and selection_review.get("review_pass")
        and lifecycle_review.get("review_pass")
        and boundary_review.get("review_pass")
        and blocked_review.get("review_pass")
    )
    boundary_ok = reviews_pass

    closure = {
        "closure_id": "authorization_closure_decision_v1",
        "ocr_provider_authorization_dryrun_closed": boundary_ok,
        "authorization_request_candidate_trusted": boundary_ok,
        "grant_candidate_trusted": boundary_ok,
        "execution_window_candidate_trusted": boundary_ok,
        "ready_for_authorization_request_planning": boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "readiness_id": "next_route_readiness_decision_v1",
        "ready_for_authorization_request_planning": boundary_ok,
        "do_not_generate_request_artifact_now": True,
        "do_not_send_request_now": True,
        "do_not_grant_authorization_now": True,
        "do_not_open_execution_window_now": True,
        "do_not_execute_real_dependency_check_now": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": closure["final_decision"],
        "rationale": (
            "After authorization dryrun closure, plan request artifact structure only — "
            "no send, no grant, no real dependency check"
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
        + [i["issue_id"] for i in request_issues]
        + [i["issue_id"] for i in grant_issues]
        + [i["issue_id"] for i in window_issues]
        + [i["issue_id"] for i in sandbox_issues]
        + [i["issue_id"] for i in rollback_issues]
        + [i["issue_id"] for i in evidence_issues]
        + [i["issue_id"] for i in boundary_issues]
        + [i["issue_id"] for i in lifecycle_issues]
    )

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "boundary_ok": boundary_ok,
        "violations": all_issue_ids,
        "final_decision": closure["final_decision"],
        "recommended_next_phase": closure["recommended_next_phase"],
        "high_risk_count": 0 if boundary_ok else 1,
        "ocr_provider_authorization_dryrun_closed": boundary_ok,
        "current_lifecycle_state": CURRENT_DRYRUN_STATE,
        **meta,
    }

    return {
        "ocr_provider_authorization_dryrun_input_review": input_review,
        "authorization_request_candidate_review": request_review,
        "grant_candidate_review": grant_review,
        "execution_window_candidate_review": window_review,
        "sandbox_boundary_candidate_review": sandbox_review,
        "rollback_candidate_review": rollback_review,
        "evidence_requirement_candidate_review": evidence_review,
        "owner_operator_approval_review": owner_review,
        "provider_selection_binding_review": selection_review,
        "authorization_lifecycle_review": lifecycle_review,
        "authorization_boundary_guard_review": boundary_review,
        "authorization_blocked_path_review": blocked_review,
        "authorization_closure_decision": closure,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
