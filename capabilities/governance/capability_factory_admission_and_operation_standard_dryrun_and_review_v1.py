# -*- coding: utf-8 -*-
"""Capability Factory Admission and Operation Standard DryRunAndReview v1 — merged validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    BOUNDARY_STANDARD_BLOCKED,
    COMPRESSED_PATH,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    LIFECYCLE_STATES,
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
    NON_CLAIMS,
    STANDARD_ID,
    STANDALONE_AUTHORIZATION_PHASES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_formal_request_artifact_generation_planning_v1 import (
    CURRENT_LIFECYCLE_STATE as FORMAL_PLANNING_STATE,
    FINAL_DECISION_GO as FORMAL_PLANNING_FINAL_GO,
)
from capabilities.governance.ocr_provider_authorization_request_dryrun_v1 import (
    CURRENT_REQUEST_DRYRUN_STATE,
)
from capabilities.governance.ocr_provider_authorization_request_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REQUEST_POST_REVIEW_FINAL_GO,
)

PHASE_ID = "Phase-Capability-Factory-Admission-and-Operation-Standard-DryRunAndReview-v1-001"
SCOPE = "capability_factory_standard_dryrun_and_review_only"
SOURCE_CHAIN = "capability_factory_admission_and_operation_standard_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = (
    "CAPABILITY_FACTORY_ADMISSION_AND_OPERATION_STANDARD_DRYRUN_AND_REVIEW_CLOSED_READY_FOR_COMPRESSED_OCR_AUTHORIZATION_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = (
    "CAPABILITY_FACTORY_ADMISSION_AND_OPERATION_STANDARD_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Compressed-OCR-Authorization-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-Capability-Factory-Admission-and-Operation-Standard-Issue-Review-v1-001"

FORBIDDEN_LATER_STATES: Tuple[str, ...] = (
    "formal_artifact_generated_later",
    "sent_later",
    "grant_issued_later",
    "execution_window_opened_later",
)

ALLOWED_CURRENT_STATES: Tuple[str, ...] = (
    CURRENT_REQUEST_DRYRUN_STATE,
    FORMAL_PLANNING_STATE,
)

COVERAGE_MATRIX_ITEMS: Tuple[str, ...] = (
    "authorization_request_candidate",
    "request_artifact_candidate",
    "formal_request_artifact_planning",
    "formal_request_artifact_candidate_later",
    "send_candidate_later",
    "grant_candidate",
    "execution_window_candidate",
    "evidence_requirement_candidate",
    "sandbox_boundary",
    "rollback_plan",
    "blocked_paths",
    "lifecycle_state_machine",
    "non_claims",
)

BOUNDARY_AUDIT_FIELDS: Tuple[str, ...] = (
    "formal_artifact_generation",
    "artifact_persist",
    "request_send",
    "approval_collect",
    "grant_issue",
    "execution_window_open",
    "provider_import",
    "provider_invoke",
    "dependency_install",
    "model_download",
    "ocr_request_submit",
    "image_read",
    "crop",
    "ocr_fact",
    "memory_write",
    "world_model_write",
    "user_output",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "factory_standard_runtime_enforced_now",
    "formal_request_artifact_generated_now",
    "formal_request_artifact_persisted_now",
    "authorization_request_sent_now",
    "authorization_request_approved_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DRYRUN_NON_CLAIMS: Tuple[str, ...] = (
    *NON_CLAIMS,
    "DryRunAndReview GO ≠ factory standard runtime enforced globally",
    "Standard coverage GO ≠ formal artifact generated",
    "Compressed lifecycle dryrun ≠ request sent",
    "Roadmap decision next ≠ real dependency check allowed",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_admission_and_operation_standard_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "capability_factory_standard_dryrun_and_review_only": True,
        "simulated": True,
        "standard_id": STANDARD_ID,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["factory_standard_runtime_enforced_now"] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def run_capability_factory_admission_and_operation_standard_dryrun_and_review_v1(
    *,
    capability_factory_admission_and_operation_standard_planning_root: str,
    ocr_provider_authorization_formal_request_artifact_generation_planning_root: Optional[str] = None,
    ocr_provider_authorization_request_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_authorization_request_dryrun_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    luna_validation_factory_consolidation_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(capability_factory_admission_and_operation_standard_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    candidate_plan = _try_read_json(planning_root / "candidate_standard_plan_v1.json") or {}
    artifact_plan = _try_read_json(planning_root / "artifact_standard_plan_v1.json") or {}
    lifecycle_plan = _try_read_json(planning_root / "lifecycle_standard_plan_v1.json") or {}
    boundary_plan = _try_read_json(planning_root / "boundary_standard_plan_v1.json") or {}
    evidence_plan = _try_read_json(planning_root / "evidence_standard_plan_v1.json") or {}
    approval_plan = _try_read_json(planning_root / "approval_grant_standard_plan_v1.json") or {}
    sandbox_plan = _try_read_json(planning_root / "sandbox_rollback_standard_plan_v1.json") or {}
    provider_plan = _try_read_json(planning_root / "provider_machine_standard_plan_v1.json") or {}
    transfer_plan = _try_read_json(planning_root / "upstream_downstream_transfer_standard_plan_v1.json") or {}
    roles_plan = _try_read_json(planning_root / "factory_role_responsibility_standard_plan_v1.json") or {}
    compression_plan = _try_read_json(planning_root / "compression_impact_assessment_v1.json") or {}

    formal_plan_root = Path(
        ocr_provider_authorization_formal_request_artifact_generation_planning_root
        or planning_root.parent / "ocr_provider_authorization_formal_request_artifact_generation_planning"
    ).expanduser().resolve()
    formal_plan_sm = _try_read_json(formal_plan_root / "summary.json") or {}
    formal_plan_vr = _try_read_json(formal_plan_root / "verifier_report.json") or {}

    req_post_root = Path(
        ocr_provider_authorization_request_post_dryrun_review_root
        or planning_root.parent / "ocr_provider_authorization_request_post_dryrun_review"
    ).expanduser().resolve()
    req_post_sm = _try_read_json(req_post_root / "summary.json") or {}
    req_post_vr = _try_read_json(req_post_root / "verifier_report.json") or {}
    req_post_closure = _try_read_json(req_post_root / "authorization_request_closure_decision_v1.json") or {}

    req_dryrun_root = Path(
        ocr_provider_authorization_request_dryrun_root
        or planning_root.parent / "ocr_provider_authorization_request_dryrun"
    ).expanduser().resolve()
    req_dryrun_sm = _try_read_json(req_dryrun_root / "summary.json") or {}
    artifact_candidate = _try_read_json(req_dryrun_root / "request_artifact_candidate_v1.json") or {}

    auth_dryrun_root = req_dryrun_root.parent / "ocr_provider_authorization_dryrun"
    auth_dryrun_sm = _try_read_json(auth_dryrun_root / "summary.json") or {}
    request_cand = _try_read_json(auth_dryrun_root / "authorization_request_candidate_v1.json") or {}
    grant_cand = _try_read_json(auth_dryrun_root / "grant_candidate_v1.json") or {}
    window_cand = _try_read_json(auth_dryrun_root / "execution_window_candidate_v1.json") or {}
    evidence_cand = _try_read_json(auth_dryrun_root / "evidence_requirement_candidate_v1.json") or {}
    sandbox_cand = _try_read_json(auth_dryrun_root / "sandbox_boundary_candidate_v1.json") or {}
    rollback_cand = _try_read_json(auth_dryrun_root / "rollback_candidate_v1.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or planning_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    vf_root = Path(
        luna_validation_factory_consolidation_root
        or planning_root.parent / "luna_validation_factory_consolidation"
    ).expanduser().resolve()
    vf_vr = _try_read_json(vf_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_standard_planning_root": str(planning_root),
        "upstream_formal_artifact_planning_root": str(formal_plan_root),
        "upstream_request_post_dryrun_review_root": str(req_post_root),
        "upstream_request_dryrun_root": str(req_dryrun_root),
        "upstream_authorization_dryrun_root": str(auth_dryrun_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_validation_factory_root": str(vf_root),
        "output_root": str(out_root),
    }

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("factory standard planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("standard_id") != STANDARD_ID:
        blockers.append("standard_id mismatch")

    if formal_plan_vr.get("verifier") != "GO":
        blockers.append("formal artifact generation planning must be GO")
    if formal_plan_sm.get("final_decision") != FORMAL_PLANNING_FINAL_GO:
        blockers.append("formal planning final_decision mismatch")
    if compression_plan.get("mergeable_phase_count", 0) < 9:
        blockers.append("formal artifact long chain must be superseded by factory standard compression")

    if req_post_vr.get("verifier") != "GO":
        blockers.append("request post-dryrun review must be GO")
    if req_post_sm.get("final_decision") != REQUEST_POST_REVIEW_FINAL_GO:
        blockers.append("request post-dryrun final_decision mismatch")
    if req_post_closure.get("request_artifact_candidate_trusted") is not True:
        blockers.append("request_artifact_candidate must be trusted")
    if req_post_sm.get("current_lifecycle_state") != CURRENT_REQUEST_DRYRUN_STATE:
        blockers.append("lifecycle must be request_artifact_candidate_ready")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration post-review must be GO")
    if vf_vr.get("verifier") != "GO":
        blockers.append("validation factory consolidation must be GO")

    for field in BOUNDARY_FALSE:
        if req_post_sm.get(field) is True or formal_plan_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    input_review = {
        "review_id": "factory_standard_planning_input_review_v1",
        "upstream_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "upstream_standard_id": plan_sm.get("standard_id"),
        "formal_planning_go": formal_plan_vr.get("verifier") == "GO",
        "compression_supersedes_long_chain": compression_plan.get("mergeable_phase_count", 0) >= 9,
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    candidate_blocked = {p["path_id"] for p in (boundary_plan.get("paths") or []) if p.get("blocked")}
    candidate_review = {
        "review_id": "candidate_standard_dryrun_review_v1",
        **_review_ok([
            ("candidate_only", candidate_plan.get("candidate_only") is True),
            ("fact_status", candidate_plan.get("fact_status") == "not_fact"),
            ("write_allowed", candidate_plan.get("write_allowed") is False),
            ("user_facing_output_allowed", candidate_plan.get("user_facing_output_allowed") is False),
            ("source_chain_required", candidate_plan.get("source_chain_required") is True),
            ("ttl_required", candidate_plan.get("ttl_required") is True),
            ("validation_required", candidate_plan.get("validation_required_before_promotion") is True),
            ("candidate_to_fact_blocked", "candidate_to_fact" in candidate_blocked),
            ("candidate_to_user_output_blocked", "candidate_to_user_output" in candidate_blocked),
            ("candidate_to_memory_write_blocked", "candidate_to_memory_write" in candidate_blocked),
            ("candidate_to_world_model_write_blocked", "candidate_to_world_model_write" in candidate_blocked),
            ("request_artifact_candidate", artifact_candidate.get("candidate_only") is True),
        ]),
        **meta,
    }

    artifact_review = {
        "review_id": "artifact_standard_dryrun_review_v1",
        **_review_ok([
            ("candidate_not_formal", artifact_plan.get("candidate_not_formal_artifact") is True),
            ("explicit_phase", artifact_plan.get("formal_artifact_generation_requires_explicit_phase") is True),
            ("generated_not_persisted", artifact_plan.get("generated_artifact_not_persisted") is True),
            ("persisted_not_sent", artifact_plan.get("persisted_artifact_not_sent") is True),
            ("required_fields", len(artifact_plan.get("required_fields") or []) == 4),
            ("no_formal_now", meta.get("formal_request_artifact_generated_now") is False),
            ("formal_planning_exists", formal_plan_vr.get("verifier") == "GO"),
        ]),
        **meta,
    }

    lifecycle_states = lifecycle_plan.get("states") or list(LIFECYCLE_STATES)
    lifecycle_review = {
        "review_id": "lifecycle_standard_dryrun_review_v1",
        "states": lifecycle_states,
        "state_count": len(lifecycle_states),
        "allowed_current_states": list(ALLOWED_CURRENT_STATES),
        "forbidden_later_states": list(FORBIDDEN_LATER_STATES),
        **_review_ok([
            ("states_13", len(lifecycle_states) == len(LIFECYCLE_STATES)),
            ("request_candidate_ready", req_post_sm.get("current_lifecycle_state") == CURRENT_REQUEST_DRYRUN_STATE),
            ("formal_planning_defined", formal_plan_sm.get("current_lifecycle_state") == FORMAL_PLANNING_STATE),
            ("no_formal_generated_later", meta.get("formal_request_artifact_generated_now") is False),
            ("no_sent_later", meta.get("authorization_request_sent_now") is False),
            ("no_grant_later", meta.get("grant_issued_now") is False),
            ("no_window_later", meta.get("execution_window_opened_now") is False),
        ]),
        **meta,
    }

    boundary_paths = {p.get("path_id"): p for p in (boundary_plan.get("paths") or [])}
    boundary_review = {
        "review_id": "boundary_standard_dryrun_review_v1",
        "path_count": len(BOUNDARY_STANDARD_BLOCKED),
        **_review_ok([
            (pid, boundary_paths.get(pid, {}).get("blocked") is True)
            for pid in BOUNDARY_STANDARD_BLOCKED
        ] + [("all_blocked_default", boundary_plan.get("all_blocked_by_default") is True)]),
        **meta,
    }

    evidence_types = evidence_plan.get("required_artifact_types") or []
    evidence_review = {
        "review_id": "evidence_standard_dryrun_review_v1",
        **_review_ok([
            ("source_phase_ref", "source_phase_ref" in evidence_types),
            ("source_candidate_ref", "source_candidate_ref" in evidence_types),
            ("boundary_audit", "boundary_audit" in evidence_types),
            ("validation_result", "validation_result" in evidence_types),
            ("failure_route_result", "failure_route_result" in evidence_types),
            ("rollback_plan_ref", "rollback_plan_ref" in evidence_types),
            ("verifier_report", "verifier_report" in evidence_types),
            ("post_execution_review", "post_execution_review_result" in evidence_types),
            ("ocr_chain_binding", bool(evidence_cand.get("candidate_id"))),
        ]),
        **meta,
    }

    approval_review = {
        "review_id": "approval_grant_standard_dryrun_review_v1",
        **_review_ok([
            ("approval_later", approval_plan.get("approval_required_later") is True),
            ("not_collected", approval_plan.get("approval_collected_now") is False),
            ("grant_chain", approval_plan.get("grant_candidate_not_grant_issued") is True),
            ("window_chain", approval_plan.get("grant_issued_not_execution_window_opened") is True),
            ("invocation_chain", approval_plan.get("execution_window_opened_not_provider_invocation") is True),
            ("revocation", approval_plan.get("revocation_condition_required") is True),
            ("grant_candidate", grant_cand.get("candidate_only") is True),
        ]),
        **meta,
    }

    sandbox_review = {
        "review_id": "sandbox_rollback_standard_dryrun_review_v1",
        **_review_ok([
            ("no_production_write", sandbox_plan.get("no_production_path_write") is True),
            ("workspace_only", sandbox_plan.get("workspace_controlled_output_only") is True),
            ("no_global_env", sandbox_plan.get("no_global_env_mutation") is True),
            ("no_untracked_install", sandbox_plan.get("no_untracked_install") is True),
            ("no_download_without_auth", sandbox_plan.get("no_model_download_without_separate_authorization") is True),
            ("failed_no_repair", sandbox_plan.get("failed_check_does_not_trigger_repair_install_download") is True),
            ("rollback_required", sandbox_plan.get("rollback_required_before_execution") is True),
            ("rollback_not_now", sandbox_plan.get("rollback_executed_now") is False),
            ("sandbox_candidate", sandbox_cand.get("no_production_path_write") is True),
            ("rollback_candidate", rollback_cand.get("rollback_executed_now") is False),
        ]),
        **meta,
    }

    provider_review = {
        "review_id": "provider_machine_standard_dryrun_review_v1",
        **_review_ok([
            ("candidate_id", provider_plan.get("provider_candidate_id_required") is True),
            ("domain", provider_plan.get("provider_domain_required") is True),
            ("family", provider_plan.get("provider_family_required") is True),
            ("status", provider_plan.get("provider_status") == "planned_candidate"),
            ("no_invoke", provider_plan.get("invocation_allowed") is False),
            ("dep_check", provider_plan.get("dependency_check_required") is True),
            ("env_check", provider_plan.get("environment_check_required") is True),
            ("health", provider_plan.get("health_binding_required") is True),
            ("constitution", provider_plan.get("constitution_gate_required") is True),
            ("evidence_pkg", provider_plan.get("evidence_package_required") is True),
            ("three_consumers", len(provider_plan.get("validated_consumers") or []) == 3),
        ]),
        **meta,
    }

    transfer_review = {
        "review_id": "upstream_downstream_transfer_standard_dryrun_review_v1",
        **_review_ok([
            ("upstream_contract", transfer_plan.get("upstream_input_contract_required") is True),
            ("downstream_contract", transfer_plan.get("downstream_output_contract_required") is True),
            ("no_direct_user", transfer_plan.get("no_direct_downstream_user_output") is True),
            ("no_direct_fact", transfer_plan.get("no_direct_fact_write_path") is True),
            ("market_validation", transfer_plan.get("market_validation_required") is True),
            ("vf_pass", transfer_plan.get("validation_factory_pass_required_before_midplatform_consumption") is True),
            ("vf_go", vf_vr.get("verifier") == "GO"),
        ]),
        **meta,
    }

    roles_review = {
        "review_id": "factory_role_responsibility_standard_review_v1",
        "roles": roles_plan.get("roles") or [],
        "role_count": len(roles_plan.get("roles") or []),
        "dryrun_and_review_pass": len(roles_plan.get("roles") or []) >= 5 and len(blockers) == 0,
        **meta,
    }

    coverage_rows = [
        {"item_id": "authorization_request_candidate", "covered": bool(request_cand.get("request_id")), "source": "ocr_provider_authorization_dryrun"},
        {"item_id": "request_artifact_candidate", "covered": bool(artifact_candidate.get("request_artifact_candidate_id")), "source": "ocr_provider_authorization_request_dryrun"},
        {"item_id": "formal_request_artifact_planning", "covered": formal_plan_vr.get("verifier") == "GO", "source": "formal_request_artifact_generation_planning"},
        {"item_id": "formal_request_artifact_candidate_later", "covered": True, "source": "compressed_lifecycle"},
        {"item_id": "send_candidate_later", "covered": True, "source": "compressed_lifecycle"},
        {"item_id": "grant_candidate", "covered": bool(grant_cand.get("grant_candidate_id")), "source": "ocr_provider_authorization_dryrun"},
        {"item_id": "execution_window_candidate", "covered": bool(window_cand.get("execution_window_candidate_id")), "source": "ocr_provider_authorization_dryrun"},
        {"item_id": "evidence_requirement_candidate", "covered": bool(evidence_cand.get("candidate_id")), "source": "ocr_provider_authorization_dryrun"},
        {"item_id": "sandbox_boundary", "covered": sandbox_cand.get("no_production_path_write") is True, "source": "ocr_provider_authorization_dryrun"},
        {"item_id": "rollback_plan", "covered": rollback_cand.get("rollback_executed_now") is False, "source": "ocr_provider_authorization_dryrun"},
        {"item_id": "blocked_paths", "covered": boundary_review.get("dryrun_and_review_pass") is True, "source": "boundary_standard"},
        {"item_id": "lifecycle_state_machine", "covered": lifecycle_review.get("dryrun_and_review_pass") is True, "source": "lifecycle_standard"},
        {"item_id": "non_claims", "covered": len(DRYRUN_NON_CLAIMS) >= len(NON_CLAIMS), "source": "factory_standard"},
    ]
    coverage_matrix = {
        "matrix_id": "ocr_authorization_chain_coverage_matrix_v1",
        "items": coverage_rows,
        "items_total": len(COVERAGE_MATRIX_ITEMS),
        "all_covered": all(r["covered"] for r in coverage_rows) and len(blockers) == 0,
        **meta,
    }

    compressed_steps = [
        {"step_id": step, "simulated": True, "executed_now": False}
        for step in COMPRESSED_PATH
    ]
    compressed_lifecycle = {
        "result_id": "compressed_authorization_lifecycle_dryrun_result_v1",
        "compressed_path": list(COMPRESSED_PATH),
        "steps": compressed_steps,
        "formal_request_artifact_generated_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "provider_invoked_now": False,
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    compression_review = {
        "review_id": "compression_impact_review_v1",
        "formal_artifact_triple_compressible": True,
        "send_triple_compressible": True,
        "grant_triple_compressible": True,
        "factory_standard_absorbs_rules": len(compression_plan.get("factory_level_defaults") or []) >= 7,
        "standalone_still_required": list(STANDALONE_AUTHORIZATION_PHASES),
        "mergeable_phases": list(MERGEABLE_OCR_AUTHORIZATION_PHASES),
        "dryrun_and_review_pass": len(blockers) == 0,
        **meta,
    }

    boundary_audit = {
        "audit_id": "factory_standard_boundary_audit_v1",
        "forbidden_actions": {field: False for field in BOUNDARY_AUDIT_FIELDS},
        "audit_pass": all(meta.get(f) is False for f in BOUNDARY_FALSE if f in meta) and len(blockers) == 0,
        **meta,
    }

    standard_reviews_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and candidate_review.get("dryrun_and_review_pass")
        and artifact_review.get("dryrun_and_review_pass")
        and lifecycle_review.get("dryrun_and_review_pass")
        and boundary_review.get("dryrun_and_review_pass")
        and evidence_review.get("dryrun_and_review_pass")
        and approval_review.get("dryrun_and_review_pass")
        and sandbox_review.get("dryrun_and_review_pass")
        and provider_review.get("dryrun_and_review_pass")
        and transfer_review.get("dryrun_and_review_pass")
        and roles_review.get("dryrun_and_review_pass")
        and coverage_matrix.get("all_covered")
        and compressed_lifecycle.get("dryrun_pass")
        and compression_review.get("dryrun_and_review_pass")
        and boundary_audit.get("audit_pass")
    )

    readiness = {
        "decision_id": "factory_standard_adoption_readiness_decision_v1",
        "nine_standards_pass": standard_reviews_pass,
        "ocr_chain_coverage_pass": coverage_matrix.get("all_covered"),
        "compressed_lifecycle_pass": compressed_lifecycle.get("dryrun_pass"),
        "compression_impact_pass": compression_review.get("dryrun_and_review_pass"),
        "boundary_audit_pass": boundary_audit.get("audit_pass"),
        "all_pass": standard_reviews_pass,
        "high_risk_count": 0 if standard_reviews_pass else 1,
        "final_decision": FINAL_DECISION_GO if standard_reviews_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if standard_reviews_pass else NEXT_PHASE_HOLD,
        "do_not_resume_formal_artifact_triple_chain": True,
        **meta,
    }

    policy = {
        "policy_id": "capability_factory_standard_dryrun_and_review_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims = {
        "register_id": "non_claims_register_v1",
        "non_claims": list(DRYRUN_NON_CLAIMS),
        **meta,
    }

    summary = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "boundary_ok": standard_reviews_pass,
        "violations": blockers,
        "final_decision": readiness["final_decision"],
        "recommended_next_phase": readiness["recommended_next_phase"],
        "standard_id": STANDARD_ID,
        "nine_standards_validated": standard_reviews_pass,
        "ocr_chain_coverage": coverage_matrix.get("all_covered"),
        "compression_validated": compression_review.get("dryrun_and_review_pass"),
        "high_risk_count": 0 if standard_reviews_pass else 1,
        **meta,
    }

    return {
        "capability_factory_standard_dryrun_and_review_policy": policy,
        "factory_standard_planning_input_review": input_review,
        "candidate_standard_dryrun_review": candidate_review,
        "artifact_standard_dryrun_review": artifact_review,
        "lifecycle_standard_dryrun_review": lifecycle_review,
        "boundary_standard_dryrun_review": boundary_review,
        "evidence_standard_dryrun_review": evidence_review,
        "approval_grant_standard_dryrun_review": approval_review,
        "sandbox_rollback_standard_dryrun_review": sandbox_review,
        "provider_machine_standard_dryrun_review": provider_review,
        "upstream_downstream_transfer_standard_dryrun_review": transfer_review,
        "factory_role_responsibility_standard_review": roles_review,
        "ocr_authorization_chain_coverage_matrix": coverage_matrix,
        "compressed_authorization_lifecycle_dryrun_result": compressed_lifecycle,
        "compression_impact_review": compression_review,
        "factory_standard_boundary_audit": boundary_audit,
        "factory_standard_adoption_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
