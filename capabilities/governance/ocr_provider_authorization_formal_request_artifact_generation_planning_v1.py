# -*- coding: utf-8 -*-
"""OCR Provider Authorization Formal Request Artifact Generation Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    EVIDENCE_REQUIREMENTS,
)
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
    NEXT_PHASE_GO as REQUEST_POST_REVIEW_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-Planning-v1-001"
SCOPE = "ocr_provider_authorization_formal_request_artifact_generation_planning_only"
SOURCE_CHAIN = "ocr_provider_authorization_formal_request_artifact_generation_planning_v1"

UPSTREAM_REQUEST_POST_REVIEW_FINAL = REQUEST_POST_REVIEW_FINAL_GO
UPSTREAM_REQUEST_POST_REVIEW_NEXT = REQUEST_POST_REVIEW_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_AUTHORIZATION_FORMAL_REQUEST_ARTIFACT_GENERATION_PLANNING_READY_FOR_DRYRUN"
)
FINAL_DECISION_HOLD = (
    "OCR_PROVIDER_AUTHORIZATION_FORMAL_REQUEST_ARTIFACT_GENERATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Formal-Request-Artifact-Generation-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Request-Issue-Review-v1-001"

FORMAL_SCHEMA_STATE = "formal_request_artifact_planned"
CURRENT_LIFECYCLE_STATE = "formal_generation_planning_defined"
ARTIFACT_SCHEMA_VERSION = "formal_request_artifact_schema_v1"
GENERATION_POLICY_VERSION = "formal_request_artifact_generation_policy_v1"

LIFECYCLE_STATES: Tuple[str, ...] = (
    "formal_generation_planning_defined",
    "formal_request_artifact_candidate_ready_later",
    "formal_request_artifact_generated_later",
    "formal_request_artifact_review_pending_later",
    "formal_request_artifact_persisted_later",
    "request_send_precheck_later",
    "request_sent_later",
    "grant_pending_later",
    "grant_issued_later",
    "execution_window_opened_later",
    "post_execution_review_required",
    "closed",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_formal_artifact_generation",
    "planning_to_artifact_persist",
    "planning_to_request_send",
    "planning_to_approval_collect",
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
    {"rule_id": "request_type_valid", "detail": "request_type must be valid"},
    {"rule_id": "artifact_version_present", "detail": "artifact_version must be present"},
    {"rule_id": "lifecycle_state_valid", "detail": "lifecycle_state must be valid"},
    {"rule_id": "target_scope_no_production", "detail": "target_scope excludes production runtime"},
    {"rule_id": "provider_refs_no_finalize", "detail": "provider_candidate_refs do not finalize provider"},
    {"rule_id": "execution_window_not_opened", "detail": "no execution window opened"},
    {"rule_id": "sandbox_no_production_write", "detail": "sandbox requires no production write"},
    {"rule_id": "evidence_required", "detail": "evidence package required"},
    {"rule_id": "approval_not_collected", "detail": "approval not collected now"},
    {"rule_id": "formal_artifact_not_generated", "detail": "formal artifact generated remains false in planning"},
)

GENERATION_RULES: Tuple[str, ...] = (
    "source request_artifact_candidate must be trusted",
    "post_dryrun_review_go required",
    "lifecycle_state must be request_artifact_candidate_ready",
    "all schema validation must pass",
    "all field bindings must pass",
    "all blocked paths must remain blocked",
    "selected_provider_for_execution must remain null",
    "provider_selection_finalized must remain false",
    "generation requires explicit future generation phase",
    "current planning phase cannot generate artifact",
)

SEND_PRECHECK_REQUIREMENTS: Tuple[str, ...] = (
    "formal artifact generated",
    "artifact review passed",
    "owner/operator approval collected",
    "grant path available",
    "execution window still closed",
    "provider still not selected for execution unless authorized",
    "boundary audit pass",
    "verifier pass",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Formal Generation Planning GO ≠ formal request artifact generated",
    "formal_request_artifact_planned ≠ request sent",
    "DryRun next ≠ formal artifact generation",
    "formal artifact generation planning ≠ approval collected",
    "formal artifact generation planning ≠ grant issued",
    "next dryrun ≠ real dependency check allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_request_artifact_generated_now",
    "formal_request_artifact_persisted_now",
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
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_provider_authorization_formal_request_artifact_generation_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_formal_request_artifact_generation_planning_only": True,
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


def run_ocr_provider_authorization_formal_request_artifact_generation_planning_v1(
    *,
    ocr_provider_authorization_request_post_dryrun_review_root: str,
    ocr_provider_authorization_request_dryrun_root: Optional[str] = None,
    ocr_provider_authorization_request_planning_root: Optional[str] = None,
    ocr_provider_authorization_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    post_root = Path(ocr_provider_authorization_request_post_dryrun_review_root).expanduser().resolve()
    post_sm = _try_read_json(post_root / "summary.json") or {}
    post_vr = _try_read_json(post_root / "verifier_report.json") or {}
    post_closure = _try_read_json(post_root / "authorization_request_closure_decision_v1.json") or {}

    req_dryrun_root = Path(
        ocr_provider_authorization_request_dryrun_root
        or post_root.parent / "ocr_provider_authorization_request_dryrun"
    ).expanduser().resolve()
    req_dryrun_sm = _try_read_json(req_dryrun_root / "summary.json") or {}
    req_dryrun_vr = _try_read_json(req_dryrun_root / "verifier_report.json") or {}
    artifact_candidate = _try_read_json(req_dryrun_root / "request_artifact_candidate_v1.json") or {}

    req_planning_root = Path(
        ocr_provider_authorization_request_planning_root
        or post_root.parent / "ocr_provider_authorization_request_planning"
    ).expanduser().resolve()

    auth_post_root = Path(
        ocr_provider_authorization_post_dryrun_review_root
        or post_root.parent / "ocr_provider_authorization_post_dryrun_review"
    ).expanduser().resolve()
    auth_post_vr = _try_read_json(auth_post_root / "verifier_report.json") or {}

    auth_dryrun_root = req_dryrun_root.parent / "ocr_provider_authorization_dryrun"
    request_cand = _try_read_json(auth_dryrun_root / "authorization_request_candidate_v1.json") or {}
    grant_cand = _try_read_json(auth_dryrun_root / "grant_candidate_v1.json") or {}
    window_cand = _try_read_json(auth_dryrun_root / "execution_window_candidate_v1.json") or {}
    sandbox_cand = _try_read_json(auth_dryrun_root / "sandbox_boundary_candidate_v1.json") or {}
    rollback_cand = _try_read_json(auth_dryrun_root / "rollback_candidate_v1.json") or {}
    evidence_cand = _try_read_json(auth_dryrun_root / "evidence_requirement_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_request_post_dryrun_review_root": str(post_root),
        "upstream_request_dryrun_root": str(req_dryrun_root),
        "upstream_request_planning_root": str(req_planning_root),
        "upstream_post_dryrun_review_root": str(auth_post_root),
        "output_root": str(out_root),
    }

    post_go = post_vr.get("verifier") == "GO" and post_vr.get("passed") is True
    if not post_go:
        blockers.append("request post-dryrun review verifier must be GO")
    if post_sm.get("final_decision") != UPSTREAM_REQUEST_POST_REVIEW_FINAL:
        blockers.append("request post-dryrun review final_decision mismatch")
    if post_sm.get("recommended_next_phase") != UPSTREAM_REQUEST_POST_REVIEW_NEXT:
        blockers.append("request post-dryrun review recommended_next_phase mismatch")
    if post_closure.get("ocr_provider_authorization_request_dryrun_closed") is not True:
        blockers.append("ocr_provider_authorization_request_dryrun_closed must be true")
    if post_closure.get("request_artifact_candidate_trusted") is not True:
        blockers.append("request_artifact_candidate must be trusted")
    if post_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("current_lifecycle_state must be request_artifact_candidate_ready")

    if req_dryrun_vr.get("verifier") != "GO":
        blockers.append("request dryrun verifier must be GO")
    if not artifact_candidate.get("request_artifact_candidate_id"):
        blockers.append("request_artifact_candidate must exist")
    if artifact_candidate.get("candidate_only") is not True:
        blockers.append("request_artifact_candidate candidate_only must be true")
    if artifact_candidate.get("formal_artifact_generated_now") is not False:
        blockers.append("formal_artifact_generated_now must be false")

    for field in (
        "formal_request_artifact_generated_now",
        "authorization_request_sent_now",
        "grant_issued_now",
        "execution_window_opened_now",
        "real_dependency_check_executed_now",
    ):
        if post_sm.get(field) is True or req_dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    if post_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must remain null")

    if auth_post_vr.get("verifier") != "GO":
        blockers.append("authorization post-dryrun review should be GO")

    input_review = {
        "review_id": "request_post_dryrun_review_input_review_v1",
        "upstream_root": str(post_root),
        "upstream_verifier_go": post_go,
        "upstream_final_decision": post_sm.get("final_decision"),
        "upstream_dryrun_closed": post_closure.get("ocr_provider_authorization_request_dryrun_closed"),
        "upstream_candidate_trusted": post_closure.get("request_artifact_candidate_trusted"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    candidate_ref = (
        artifact_candidate.get("request_artifact_candidate_id")
        or "ocr_provider_authorization_request_artifact_candidate_v1"
    )
    request_candidate_ref = (
        artifact_candidate.get("related_authorization_request_candidate_ref")
        or request_cand.get("request_id")
        or "ocr_provider_authorization_request_candidate_v1"
    )
    grant_candidate_ref = grant_cand.get("grant_candidate_id") or "ocr_provider_authorization_grant_candidate_v1"
    window_candidate_ref = (
        window_cand.get("execution_window_candidate_id")
        or artifact_candidate.get("requested_execution_window_ref")
        or "ocr_provider_authorization_execution_window_candidate_v1"
    )
    sandbox_candidate_ref = (
        sandbox_cand.get("candidate_id")
        or artifact_candidate.get("sandbox_boundary_ref")
        or "sandbox_boundary_candidate_v1"
    )
    rollback_candidate_ref = (
        rollback_cand.get("candidate_id")
        or artifact_candidate.get("rollback_plan_ref")
        or "rollback_candidate_v1"
    )
    evidence_candidate_ref = (
        evidence_cand.get("candidate_id")
        or artifact_candidate.get("evidence_requirement_ref")
        or "evidence_requirement_candidate_v1"
    )

    formal_schema = {
        "schema_id": "formal_request_artifact_schema_v1",
        "formal_request_artifact_id": "ocr_provider_authorization_formal_request_artifact_v1",
        "request_type": "ocr_provider_authorization_request",
        "artifact_version": ARTIFACT_SCHEMA_VERSION,
        "lifecycle_state": FORMAL_SCHEMA_STATE,
        "source_request_artifact_candidate_ref": candidate_ref,
        "source_authorization_request_candidate_ref": request_candidate_ref,
        "target_scope": artifact_candidate.get("target_scope") or list(AUTHORIZATION_SCOPE_COVERED),
        "provider_candidate_refs": artifact_candidate.get("provider_candidate_refs") or "planned_candidate_refs_only",
        "dependency_check_scope": artifact_candidate.get("dependency_check_scope") or "real_dependency_check_plan_candidate",
        "environment_scope": artifact_candidate.get("environment_scope") or "sandbox_workspace_fallback_only",
        "requested_execution_window_ref": window_candidate_ref,
        "sandbox_boundary_ref": sandbox_candidate_ref,
        "rollback_plan_ref": rollback_candidate_ref,
        "evidence_requirement_ref": evidence_candidate_ref,
        "owner_operator_approval_required": True,
        "verifier_required": True,
        "post_execution_review_required": True,
        "generated_now": False,
        "persisted_now": False,
        "sent_now": False,
        "approved_now": False,
        "schema_only": True,
        **meta,
    }

    generation_rules = {
        "rule_id": "formal_request_artifact_generation_rule_v1",
        "rules": list(GENERATION_RULES),
        "rule_count": len(GENERATION_RULES),
        "source_request_artifact_candidate_trusted": post_closure.get("request_artifact_candidate_trusted") is True,
        "post_dryrun_review_go": post_go,
        "lifecycle_state_request_artifact_candidate_ready": (
            post_sm.get("current_lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE
        ),
        "selected_provider_for_execution": None,
        "provider_selection_finalized": False,
        "artifact_generation_allowed_now": False,
        "requires_explicit_future_generation_phase": True,
        "current_planning_cannot_generate_artifact": True,
        **meta,
    }

    field_source_map = {
        "map_id": "formal_request_artifact_field_source_map_v1",
        "bindings": [
            {
                "source": "request_artifact_candidate_v1",
                "source_ref": candidate_ref,
                "target": "formal_request_artifact_schema_v1",
            },
            {
                "source": "authorization_request_candidate_v1",
                "source_ref": request_candidate_ref,
                "target_field": "source_authorization_request_candidate_ref",
            },
            {
                "source": "grant_candidate_v1",
                "source_ref": grant_candidate_ref,
                "target": "later_grant_workflow",
            },
            {
                "source": "execution_window_candidate_v1",
                "source_ref": window_candidate_ref,
                "target_field": "requested_execution_window_ref",
            },
            {
                "source": "sandbox_boundary_candidate_v1",
                "source_ref": sandbox_candidate_ref,
                "target_field": "sandbox_boundary_ref",
            },
            {
                "source": "rollback_candidate_v1",
                "source_ref": rollback_candidate_ref,
                "target_field": "rollback_plan_ref",
            },
            {
                "source": "evidence_requirement_candidate_v1",
                "source_ref": evidence_candidate_ref,
                "target_field": "evidence_requirement_ref",
            },
            {
                "source": "authorization_request_owner_operator_approval_plan_v1",
                "target_field": "owner_operator_approval_required",
            },
        ],
        "binding_count": 8,
        **meta,
    }

    validation_rules = {
        "plan_id": "formal_request_artifact_validation_rule_v1",
        "rules": list(VALIDATION_RULES),
        "rule_count": len(VALIDATION_RULES),
        "enforced_in_planning": True,
        "formal_artifact_generation_blocked_in_planning": True,
        **meta,
    }

    versioning_policy = {
        "policy_id": "formal_request_artifact_versioning_policy_v1",
        "artifact_schema_version": ARTIFACT_SCHEMA_VERSION,
        "generation_policy_version": GENERATION_POLICY_VERSION,
        "source_candidate_version_ref": candidate_ref,
        "backward_compatibility_required": True,
        "version_bump_required_on_schema_change": True,
        **meta,
    }

    signature_policy = {
        "policy_id": "formal_request_artifact_signature_placeholder_policy_v1",
        "signature_required_later": True,
        "signer_identity_later": "owner_operator_identity_pending",
        "approval_record_later": "approval_record_pending",
        "signature_generated_now": False,
        "approval_collected_now": False,
        **meta,
    }

    storage_boundary = {
        "plan_id": "formal_request_artifact_storage_boundary_plan_v1",
        "planning_does_not_persist_artifact": True,
        "future_artifact_workspace_controlled_output_only": True,
        "no_production_path_write": True,
        "no_global_registry_write": True,
        "no_external_transmission": True,
        "persisted_now": False,
        **meta,
    }

    lifecycle_plan = {
        "plan_id": "formal_request_artifact_lifecycle_plan_v1",
        "states": list(LIFECYCLE_STATES),
        "current_state": CURRENT_LIFECYCLE_STATE,
        "prior_request_state": CURRENT_REQUEST_DRYRUN_STATE,
        "transitions_planned_only": True,
        **meta,
    }

    send_precheck = {
        "plan_id": "formal_request_artifact_send_precheck_plan_v1",
        "future_send_precheck_requirements": list(SEND_PRECHECK_REQUIREMENTS),
        "requirement_count": len(SEND_PRECHECK_REQUIREMENTS),
        "send_allowed_now": False,
        "approval_collected_now": False,
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "formal_request_artifact_blocked_path_matrix_v1",
        "paths": [{"path_id": p, "blocked": True, "default": True} for p in BLOCKED_PATHS],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "formal_request_artifact_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate formal_request_artifact_candidate",
            "verify schema / generation rules / field source map / validation rules / versioning / storage boundary",
            "verify formal artifact generation remains blocked",
        ],
        "dryrun_forbidden": [
            "generate formal request artifact",
            "persist artifact",
            "send request",
            "collect approval",
            "grant authorization",
            "execute real dependency check",
        ],
        **meta,
    }

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "formal_request_artifact_generation_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ready_for_dryrun": boundary_ok,
        "current_lifecycle_state": CURRENT_LIFECYCLE_STATE,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "formal_request_artifact_generation_planning_policy_v1",
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
        "formal_request_artifact_generation_planning_policy": policy,
        "request_post_dryrun_review_input_review": input_review,
        "formal_request_artifact_schema": formal_schema,
        "formal_request_artifact_generation_rule": generation_rules,
        "formal_request_artifact_field_source_map": field_source_map,
        "formal_request_artifact_validation_rule": validation_rules,
        "formal_request_artifact_versioning_policy": versioning_policy,
        "formal_request_artifact_signature_placeholder_policy": signature_policy,
        "formal_request_artifact_storage_boundary_plan": storage_boundary,
        "formal_request_artifact_lifecycle_plan": lifecycle_plan,
        "formal_request_artifact_send_precheck_plan": send_precheck,
        "formal_request_artifact_blocked_path_matrix": blocked_matrix,
        "formal_request_artifact_dryrun_plan": dryrun_plan,
        "formal_request_artifact_generation_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
