# -*- coding: utf-8 -*-
"""OCR Real Dependency Execution Authorization DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VALIDATION_SEP_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_authorization_planning_v1 import (
    BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    EVIDENCE_ARTIFACTS,
    FINAL_DECISION_GO as UPSTREAM_PLANNING_FINAL_GO,
    FORBIDDEN_EXECUTION_ACTIONS,
    NEXT_PHASE_GO as UPSTREAM_PLANNING_NEXT_PHASE,
    SCOPE_ALLOWED_CHECKS,
    VALIDATION_GATE_PATH,
    _check_plan_item,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-DryRunAndReview-v1-001"
SCOPE = "ocr_real_dependency_execution_authorization_dryrun_and_review_only"
SOURCE_CHAIN = "ocr_real_dependency_execution_authorization_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = UPSTREAM_PLANNING_FINAL_GO
UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_EXECUTION_REQUEST_GENERATION_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Execution-Request-Generation-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Execution-Authorization-Issue-Review-v1-001"

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_formal_execution_request_generation",
    "dryrun_to_request_send",
    "dryrun_to_grant_issue",
    "dryrun_to_execution_window_open",
    "dryrun_to_domain_config_activation",
    "dryrun_to_validation_runtime_enable",
    "dryrun_to_real_dependency_check",
    "dryrun_to_package_check",
    "dryrun_to_provider_import",
    "dryrun_to_model_cache_check",
    "dryrun_to_model_file_hash_check",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
    "dryrun_to_cache_mutation",
    "dryrun_to_provider_invoke",
    "dryrun_to_provider_selection_finalize",
    "dryrun_to_controlled_trial",
    "dryrun_to_ocr_request_submit",
    "dryrun_to_image_read",
    "dryrun_to_crop",
    "dryrun_to_ocr_fact",
    "dryrun_to_user_output",
    "dryrun_to_memory_write",
    "dryrun_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRunAndReview GO ≠ execution request generated",
    "request_candidate ≠ request sent",
    "grant_candidate ≠ grant issued",
    "execution_window_candidate ≠ execution window opened",
    "allowed checks candidate ≠ checks executed",
    "next roadmap decision ≠ provider import allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = (
    "execution_authorization_request_candidate_generated_now",
    "execution_grant_candidate_generated_now",
    "execution_window_candidate_generated_now",
    "allowed_check_plan_candidate_generated_now",
    "evidence_collection_candidate_generated_now",
    "rollback_candidate_generated_now",
    "validation_gate_path_candidate_generated_now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "formal_execution_request_generated_now",
    "execution_authorization_request_sent_now",
    "execution_grant_issued_now",
    "execution_window_opened_now",
    "domain_config_activated_now",
    "validator_runtime_enabled_now",
    "validation_factory_runtime_enforced_now",
    "real_dependency_check_executed_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_initialization_dry_check_executed_now",
    "runtime_smoke_check_executed_now",
    "sample_ocr_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "cache_mutation_executed_now",
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

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_execution_authorization_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_real_dependency_execution_authorization_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
    for field in BOUNDARY_FALSE:
        meta[field] = False
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


def run_ocr_real_dependency_execution_authorization_dryrun_and_review_v1(
    *,
    ocr_real_dependency_execution_authorization_planning_root: str,
    ocr_real_dependency_execution_authorization_roadmap_decision_root: Optional[str] = None,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(ocr_real_dependency_execution_authorization_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_sm_machine = _try_read_json(plan_root / "execution_authorization_state_machine_v1.json") or {}
    plan_blocked = _try_read_json(plan_root / "execution_authorization_blocked_path_matrix_v1.json") or {}
    plan_allowed = _try_read_json(plan_root / "allowed_real_dependency_check_plan_v1.json") or {}
    plan_forbidden = _try_read_json(plan_root / "forbidden_execution_action_plan_v1.json") or {}
    plan_rollback = _try_read_json(plan_root / "rollback_and_failure_route_plan_v1.json") or {}

    roadmap_root = Path(
        ocr_real_dependency_execution_authorization_roadmap_decision_root
        or plan_root.parent / "ocr_real_dependency_execution_authorization_roadmap_decision"
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
        or plan_root.parent / "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or plan_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()
    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or plan_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()
    explain_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
        or plan_root.parent / "midplatform_constitution_governance_explanation_dryrun_and_review"
    ).expanduser().resolve()

    ocr_domain_config = _try_read_json(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    ) or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}
    val_dr_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}
    explain_vr = _try_read_json(explain_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    domain_config_ref = str(ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json")

    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_ocr_via_factory_dryrun_review_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_review_root": str(val_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_root),
        "upstream_explanation_dryrun_review_root": str(explain_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT_PHASE:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm_machine.get("current_state") != "planning_defined":
        blockers.append("planning current_state must be planning_defined")
    if plan_blocked.get("blocked_count") != 24:
        blockers.append("planning must have 24 blocked paths")
    if plan_allowed.get("check_count") != 8:
        blockers.append("planning must have 8 allowed checks")
    for item in plan_allowed.get("checks") or []:
        if item.get("current_executed_now") is True:
            blockers.append("all planned checks must have current_executed_now=false")
            break
    if ocr_domain_config.get("candidate_only") is not True:
        blockers.append("domain_config must be candidate_only")
    if ocr_domain_config.get("activated_now") is not False:
        blockers.append("domain_config must not be activated")
    if val_model.get("runtime_enabled_now") is not False:
        blockers.append("validator runtime must not be enabled")
    if val_dr_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun must be GO")
    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun must be GO")
    if explain_vr.get("verifier") != "GO":
        blockers.append("explanation dryrun must be GO")

    input_ok = len(blockers) == 0

    planning_input = {
        "review_id": "execution_authorization_planning_input_review_v1",
        "upstream_planning_root": str(plan_root),
        "verifier_go": plan_vr.get("verifier") == "GO",
        "final_decision": plan_sm.get("final_decision"),
        "current_state": plan_sm_machine.get("current_state"),
        "blocked_path_count": plan_blocked.get("blocked_count"),
        "allowed_check_count": plan_allowed.get("check_count"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    request_candidate = {
        "candidate_id": "execution_authorization_request_candidate_v1",
        "request_candidate_id": "ocr_real_dependency_execution_authorization_request_candidate_v1",
        "request_type": "ocr_real_dependency_execution_authorization_request",
        "provider_domain": "ocr",
        "authorization_target": "real_dependency_check_execution",
        "source_domain_config_ref": domain_config_ref,
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "validation_engineering_ref": "validation_engineering_model_v1",
        "requested_allowed_checks": list(SCOPE_ALLOWED_CHECKS),
        "forbidden_actions_ref": "forbidden_execution_action_plan_v1",
        "execution_window_required": True,
        "sandbox_required": True,
        "rollback_required": True,
        "evidence_collection_required": True,
        "validation_gate_required": True,
        "post_execution_review_required": True,
        "owner_operator_approval_required": True,
        "candidate_only": True,
        "formal_request_generated_now": False,
        "request_sent_now": False,
        "simulated_validation_pass": True,
        **meta,
    }

    grant_candidate = {
        "candidate_id": "execution_grant_candidate_v1",
        "grant_candidate_id": "ocr_real_dependency_execution_grant_candidate_v1",
        "related_request_candidate_id": request_candidate["request_candidate_id"],
        "grant_scope": "real_dependency_check_execution_only",
        "allowed_actions_later": list(SCOPE_ALLOWED_CHECKS),
        "prohibited_actions": list(FORBIDDEN_EXECUTION_ACTIONS),
        "expiration_or_ttl": "execution_window_bounded_ttl_later",
        "revocation_conditions": [
            "validation_gate_fail",
            "boundary_violation",
            "owner_operator_revoke",
            "execution_window_expired",
        ],
        "no_provider_selection_finalize": True,
        "no_controlled_trial": True,
        "no_production_runtime": True,
        "no_ocr_fact": True,
        "candidate_only": True,
        "grant_issued_now": False,
        "simulated_validation_pass": True,
        **meta,
    }

    window_candidate = {
        "candidate_id": "execution_window_candidate_v1",
        "execution_window_candidate_id": "ocr_real_dependency_execution_window_candidate_v1",
        "allowed_workspace_path": "_tmp_eval_out/ocr_real_dependency_execution_sandbox_later",
        "allowed_output_path": "_tmp_eval_out/ocr_real_dependency_execution_evidence_later",
        "forbidden_paths": [
            "memory/",
            "world_model/",
            "production_runtime/",
            "user_facing_output/",
        ],
        "max_check_scope": "real_dependency_check_execution_only",
        "timeout_limit": "bounded_by_execution_window_policy_later",
        "no_production_write": True,
        "no_network_by_default": True,
        "no_install": True,
        "no_download": True,
        "no_cache_mutation_without_approval": True,
        "post_execution_review_required": True,
        "candidate_only": True,
        "execution_window_opened_now": False,
        "simulated_validation_pass": True,
        **meta,
    }

    allowed_check_candidate = {
        "candidate_id": "allowed_check_plan_candidate_v1",
        "check_count": len(SCOPE_ALLOWED_CHECKS),
        "checks": [_check_plan_item(cid) for cid in SCOPE_ALLOWED_CHECKS],
        "all_current_executed_now_false": True,
        **meta,
    }

    forbidden_review = {
        "review_id": "forbidden_action_review_v1",
        "forbidden_actions": list(FORBIDDEN_EXECUTION_ACTIONS),
        "forbidden_count": len(FORBIDDEN_EXECUTION_ACTIONS),
        "matches_planning": (plan_forbidden.get("forbidden_actions") or []) == list(
            FORBIDDEN_EXECUTION_ACTIONS
        ),
        **_review_ok([("forbidden_count_15", len(FORBIDDEN_EXECUTION_ACTIONS) == 15)]),
        **meta,
    }

    evidence_candidate = {
        "candidate_id": "evidence_collection_candidate_v1",
        "collect_on_future_execution": list(EVIDENCE_ARTIFACTS),
        "evidence_collected_now": False,
        "artifact_count": len(EVIDENCE_ARTIFACTS),
        **meta,
    }

    rollback_candidate = {
        "candidate_id": "rollback_failure_route_candidate_v1",
        "failed_package_check_does_not_trigger_install": plan_rollback.get(
            "failed_package_check_does_not_trigger_install", True
        ),
        "failed_import_does_not_trigger_repair": plan_rollback.get(
            "failed_import_does_not_trigger_repair", True
        ),
        "missing_model_file_does_not_trigger_download": plan_rollback.get(
            "missing_model_file_does_not_trigger_download", True
        ),
        "hash_mismatch_does_not_trigger_cache_mutation": plan_rollback.get(
            "hash_mismatch_does_not_trigger_cache_mutation", True
        ),
        "smoke_failure_does_not_trigger_provider_switch": plan_rollback.get(
            "smoke_failure_does_not_trigger_provider_switch", True
        ),
        "rollback_required_before_execution": True,
        "rollback_executed_now": False,
        **meta,
    }

    gate_checks: List[Tuple[str, bool]] = [
        ("domain_config_to_auth_gate", True),
        ("allowed_to_factory_std", True),
        ("forbidden_to_boundary", True),
        ("provider_refs_to_harness", True),
        ("evidence_to_evidence_validator", True),
        ("no_runtime_to_audit", True),
        ("health_to_health_validator", True),
        ("vf_aggregated", True),
        ("failed_to_trace_report", True),
        ("no_runtime_now", meta.get("validator_runtime_enabled_now") is False),
        ("no_vf_runtime", meta.get("validation_factory_runtime_enforced_now") is False),
        ("no_gate_executed", True),
    ]
    gate_path_review = {
        "review_id": "validation_gate_path_dryrun_review_v1",
        "path_mappings": list(VALIDATION_GATE_PATH),
        "domain_config_ref": domain_config_ref,
        "validator_runtime_enabled_now": False,
        "validation_factory_runtime_enforced_now": False,
        "no_gate_executed_now": True,
        "simulated_gate_path_pass": True,
        **_review_ok(gate_checks),
        **meta,
    }

    provider_review = {
        "review_id": "provider_selection_non_finalize_review_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "real_dependency_execution_authorization_not_equal_provider_selected": True,
        **_review_ok([
            ("provider_null", True),
            ("no_finalize", meta.get("provider_selection_finalized_now") is False),
        ]),
        **meta,
    }

    sm_checks: List[Tuple[str, bool]] = [
        ("current_planning_defined", plan_sm_machine.get("current_state") == "planning_defined"),
        ("dryrun_simulated_only", True),
    ]
    state_machine_review = {
        "review_id": "state_machine_dryrun_review_v1",
        "planning_state": plan_sm_machine.get("current_state"),
        "dryrun_does_not_advance_to_execution_authorized": True,
        "next_states_remain_later_only": True,
        **_review_ok(sm_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    for field in BOUNDARY_TRUE:
        boundary_checks.append((f"boundary_true.{field}", meta.get(field) is True))

    boundary_audit = {
        "audit_id": "execution_authorization_boundary_audit_v1",
        "all_boundary_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        "all_boundary_true": all(meta.get(f) is True for f in BOUNDARY_TRUE),
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "execution_authorization_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "planning_blocked_count": len(PLANNING_BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        forbidden_review,
        gate_path_review,
        provider_review,
        state_machine_review,
        boundary_audit,
    ]

    candidates_ok = (
        request_candidate.get("candidate_only") is True
        and grant_candidate.get("grant_issued_now") is False
        and window_candidate.get("execution_window_opened_now") is False
        and allowed_check_candidate.get("all_current_executed_now_false") is True
        and len(allowed_check_candidate.get("checks") or []) == 8
    )

    all_pass = (
        input_ok
        and candidates_ok
        and blocked_path_result.get("all_blocked") is True
        and all(s.get("dryrun_and_review_pass") is True for s in review_sections)
    )

    closure_decision = {
        "decision_id": "execution_authorization_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_execution_request_generation_roadmap_decision": all_pass,
        "ready_for_real_dependency_check_execution": False,
        "do_not_generate_formal_request_now": True,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_execution_authorization_dryrun_review_policy_v1",
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
        "boundary_ok": all_pass,
        "violations": blockers,
        "dryrun_and_review_pass": all_pass,
        "final_decision": closure_decision["final_decision"],
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "ocr_real_dependency_execution_authorization_dryrun_review_policy": policy,
        "execution_authorization_planning_input_review": planning_input,
        "execution_authorization_request_candidate": request_candidate,
        "execution_grant_candidate": grant_candidate,
        "execution_window_candidate": window_candidate,
        "allowed_check_plan_candidate": allowed_check_candidate,
        "forbidden_action_review": forbidden_review,
        "evidence_collection_candidate": evidence_candidate,
        "rollback_failure_route_candidate": rollback_candidate,
        "validation_gate_path_dryrun_review": gate_path_review,
        "provider_selection_non_finalize_review": provider_review,
        "state_machine_dryrun_review": state_machine_review,
        "execution_authorization_boundary_audit": boundary_audit,
        "execution_authorization_blocked_path_result": blocked_path_result,
        "execution_authorization_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
