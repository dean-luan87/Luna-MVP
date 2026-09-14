# -*- coding: utf-8 -*-
"""OCR Real Minimal Controlled Execution Planning v1 — final pre-execution planning."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    CHECK_TYPES,
    EVIDENCE_OUTPUT_ITEMS,
    FAILURE_ROUTES,
    MINIMAL_FORBIDDEN_ACTIONS,
)
from capabilities.governance.ocr_real_dependency_real_minimal_execution_authorization_decision_v1 import (
    FINAL_DECISION_GO as UPSTREAM_AUTH_DECISION_FINAL_GO,
    NEXT_PHASE_GO as UPSTREAM_AUTH_DECISION_NEXT_PHASE,
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Planning-v1-001"
SCOPE = "real_minimal_controlled_execution_planning_only"
SOURCE_CHAIN = "ocr_real_dependency_real_minimal_controlled_execution_planning_v1"

UPSTREAM_AUTH_DECISION_FINAL = UPSTREAM_AUTH_DECISION_FINAL_GO
UPSTREAM_AUTH_DECISION_NEXT = UPSTREAM_AUTH_DECISION_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_REAL_MINIMAL_CONTROLLED_EXECUTION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Real-Minimal-Controlled-Execution-Planning-Issue-Review-v1-001"

REAL_EXCLUDED_FROM_SCOPE: Tuple[str, ...] = (
    "provider_initialization_dry_check",
    "runtime_smoke_check",
    "sample_ocr_check",
    "OCRRequest_submit",
    "image_read",
    "crop",
    "OCR_fact_generation",
    "user_output",
    "memory_write",
    "world_model_write",
    "provider_selection_finalize",
    "controlled_trial",
    "production_runtime",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_execution_window_open",
    "planning_to_owner_confirmation_collect",
    "planning_to_package_check",
    "planning_to_model_cache_check",
    "planning_to_model_file_existence_check",
    "planning_to_model_file_hash_check",
    "planning_to_provider_import_check",
    "planning_to_dependency_install",
    "planning_to_model_download",
    "planning_to_cache_mutation",
    "planning_to_provider_runtime_invoke",
    "planning_to_provider_initialization_dry_check",
    "planning_to_runtime_smoke_check",
    "planning_to_sample_ocr_check",
    "planning_to_ocr_request_submit",
    "planning_to_image_read",
    "planning_to_crop",
    "planning_to_ocr_fact",
    "planning_to_user_output",
    "planning_to_memory_write",
    "planning_to_world_model_write",
    "planning_to_provider_selection_finalize",
    "planning_to_controlled_trial",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ real minimal execution started",
    "execution window plan ≠ window opened",
    "owner confirmation plan ≠ confirmation collected",
    "allowed checks planned ≠ checks executed",
    "provider import check planned ≠ provider imported",
    "next DryRunAndReview ≠ execution automatically allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_minimal_execution_started_now",
    "real_execution_window_opened_now",
    "owner_confirmation_collected_now",
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

SANDBOX_WORKSPACE = "_tmp_eval_out/ocr_real_dependency_real_minimal_controlled_execution_sandbox"
SANDBOX_OUTPUT = "_tmp_eval_out/ocr_real_dependency_real_minimal_controlled_execution_evidence"

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_real_minimal_controlled_execution_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "real_minimal_controlled_execution_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "real_minimal_execution_authorized_now": False,
        "execution_window_opened_now": False,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _real_check_item(check_id: str) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "check_type": CHECK_TYPES[check_id],
        "execution_allowed_later": True,
        "current_executed_now": False,
        "evidence_required": True,
        "failure_route_required": True,
        "rollback_required": True,
        "post_execution_review_required": True,
        "failure_route_ref": f"real_execution_failure_route_plan_v1#{check_id}",
    }


def run_ocr_real_dependency_real_minimal_controlled_execution_planning_v1(
    *,
    ocr_real_dependency_real_minimal_execution_authorization_decision_root: str,
    ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root: str,
    ocr_real_dependency_minimal_controlled_execution_planning_root: str,
    ocr_real_dependency_execution_final_preflight_root: Optional[str] = None,
    midplatform_validation_engineering_separation_dryrun_and_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    auth_dec_root = Path(
        ocr_real_dependency_real_minimal_execution_authorization_decision_root
    ).expanduser().resolve()
    dryrun_root = Path(
        ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_root
    ).expanduser().resolve()
    prior_plan_root = Path(
        ocr_real_dependency_minimal_controlled_execution_planning_root
    ).expanduser().resolve()
    preflight_root = Path(
        ocr_real_dependency_execution_final_preflight_root
        or auth_dec_root.parent / "ocr_real_dependency_execution_final_preflight"
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
        or auth_dec_root.parent / "midplatform_validation_engineering_separation_dryrun_and_review"
    ).expanduser().resolve()

    auth_sm = _try_read_json(auth_dec_root / "summary.json") or {}
    auth_vr = _try_read_json(auth_dec_root / "verifier_report.json") or {}
    dryrun_sm = _try_read_json(dryrun_root / "summary.json") or {}
    dryrun_vr = _try_read_json(dryrun_root / "verifier_report.json") or {}
    plan_cand = _try_read_json(
        dryrun_root / "minimal_controlled_execution_plan_candidate_v1.json"
    ) or {}
    prior_allowed = _try_read_json(prior_plan_root / "minimal_allowed_check_plan_v1.json") or {}
    preflight_vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_authorization_decision_root": str(auth_dec_root),
        "upstream_minimal_dryrun_root": str(dryrun_root),
        "upstream_minimal_planning_root": str(prior_plan_root),
        "upstream_final_preflight_root": str(preflight_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "output_root": str(out_root),
    }

    if auth_vr.get("verifier") != "GO":
        blockers.append("authorization decision verifier must be GO")
    if auth_sm.get("final_decision") != UPSTREAM_AUTH_DECISION_FINAL:
        blockers.append("authorization decision final_decision mismatch")
    if auth_sm.get("recommended_next_phase") != UPSTREAM_AUTH_DECISION_NEXT:
        blockers.append("authorization decision recommended_next_phase mismatch")
    if auth_sm.get("selected_route") != UPSTREAM_SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if auth_sm.get("real_minimal_execution_authorized_now") is not False:
        blockers.append("real_minimal_execution_authorized_now must be false")
    if auth_sm.get("real_minimal_execution_started_now") is not False:
        blockers.append("real_minimal_execution_started_now must be false")
    if auth_sm.get("execution_window_opened_now") is not False:
        blockers.append("execution_window_opened_now must be false")
    if dryrun_vr.get("verifier") != "GO":
        blockers.append("minimal dryrun should be GO")
    if not plan_cand.get("plan_candidate_id"):
        blockers.append("minimal_controlled_execution_plan_candidate required")
    if prior_allowed.get("check_count") != 5:
        blockers.append("5 allowed checks must be planned upstream")
    if dryrun_sm.get("minimal_controlled_execution_started_now") is True:
        blockers.append("minimal_controlled_execution_started_now must be false")
    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if preflight_vr.get("verifier") != "GO":
        blockers.append("final preflight should be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun should be GO")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator runtime must not be enabled")

    for item in prior_allowed.get("checks") or []:
        if item.get("current_executed_now") is True:
            blockers.append("all allowed checks must have current_executed_now=false")
            break

    input_ok = len(blockers) == 0

    auth_input = {
        "review_id": "authorization_decision_input_review_v1",
        "upstream_root": str(auth_dec_root),
        "verifier_go": auth_vr.get("verifier") == "GO",
        "final_decision": auth_sm.get("final_decision"),
        "selected_route": auth_sm.get("selected_route"),
        "recommended_next_phase": auth_sm.get("recommended_next_phase"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    scope_lock = {
        "lock_id": "real_execution_scope_lock_v1",
        "execution_scope": "minimal_real_dependency_check",
        "allowed_checks_later": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "allowed_check_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "excluded_from_scope": list(REAL_EXCLUDED_FROM_SCOPE),
        "scope_locked": True,
        "planning_only": True,
        **meta,
    }

    window_opening_plan = {
        "plan_id": "real_execution_window_opening_plan_v1",
        "execution_window_scope": "minimal_real_dependency_check",
        "allowed_checks_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "window_opening_requires_owner_confirmation": True,
        "window_opening_requires_sandbox": True,
        "window_opening_requires_evidence_output_path": True,
        "window_opening_requires_rollback_plan": True,
        "window_opening_requires_post_execution_review": True,
        "allowed_workspace_path": SANDBOX_WORKSPACE,
        "allowed_output_path": SANDBOX_OUTPUT,
        "window_opened_now": False,
        "real_execution_window_opened_now": False,
        **meta,
    }

    sandbox_plan = {
        "plan_id": "real_execution_sandbox_plan_v1",
        "workspace_controlled_only": True,
        "allowed_workspace_path": SANDBOX_WORKSPACE,
        "allowed_output_path": SANDBOX_OUTPUT,
        "forbidden_paths": [
            "memory/",
            "world_model/",
            "production_runtime/",
            "user_facing_output/",
        ],
        "no_production_write": True,
        "no_global_registry_write": True,
        "no_external_transmission": True,
        "no_network_by_default": True,
        "no_install": True,
        "no_download": True,
        "no_cache_mutation_without_approval": True,
        **meta,
    }

    allowed_check_plan = {
        "plan_id": "real_execution_allowed_check_plan_v1",
        "check_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "checks": [_real_check_item(cid) for cid in MINIMAL_SCOPE_ALLOWED_CHECKS],
        "all_current_executed_now_false": True,
        **meta,
    }

    forbidden_plan = {
        "plan_id": "real_execution_forbidden_action_plan_v1",
        "forbidden_actions": list(MINIMAL_FORBIDDEN_ACTIONS),
        "forbidden_count": len(MINIMAL_FORBIDDEN_ACTIONS),
        **meta,
    }

    evidence_plan = {
        "plan_id": "real_execution_evidence_capture_plan_v1",
        "future_execution_must_output": list(EVIDENCE_OUTPUT_ITEMS),
        "evidence_count": len(EVIDENCE_OUTPUT_ITEMS),
        "evidence_captured_now": False,
        **meta,
    }

    failure_plan = {
        "plan_id": "real_execution_failure_route_plan_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    rollback_plan = {
        "plan_id": "real_execution_rollback_boundary_plan_v1",
        "failed_package_check_does_not_trigger_install": True,
        "failed_import_does_not_trigger_repair": True,
        "missing_model_file_does_not_trigger_download": True,
        "hash_mismatch_does_not_trigger_cache_mutation": True,
        "rollback_required_before_execution": True,
        "rollback_executed_now": False,
        **meta,
    }

    owner_confirmation_plan = {
        "plan_id": "real_execution_owner_confirmation_plan_v1",
        "owner_confirmation_required_before_window_open": True,
        "owner_confirmation_scope": "minimal_real_dependency_check_only",
        "owner_confirmation_does_not_allow_smoke": True,
        "owner_confirmation_does_not_allow_sample_ocr": True,
        "owner_confirmation_does_not_finalize_provider": True,
        "owner_confirmation_collected_now": False,
        **meta,
    }

    post_review_plan = {
        "plan_id": "real_execution_post_review_plan_v1",
        "review_required": True,
        "evidence_completeness_check": True,
        "boundary_violation_check": True,
        "failure_route_check": True,
        "rollback_status_check": True,
        "verifier_required": True,
        "next_route_decision_required": True,
        **meta,
    }

    verifier_plan = {
        "plan_id": "real_execution_verifier_plan_v1",
        "verifier_required_on_future_execution": True,
        "verifier_emits_go_or_no_go": True,
        "verifier_checks_evidence_completeness": True,
        "verifier_checks_boundary": True,
        "verifier_checks_blocked_paths": True,
        "verifier_executed_now": False,
        **meta,
    }

    provider_plan = {
        "plan_id": "provider_selection_non_finalize_plan_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "real_minimal_execution_evidence_may_inform_provider_selection_later": True,
        "current_planning_cannot_finalize_provider": True,
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "real_execution_blocked_path_matrix_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "planning_only": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "real_execution_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_objectives": [
            "generate real_minimal_execution_plan_candidate",
            "verify execution window opening plan",
            "verify owner confirmation plan",
            "verify 5 real check execution plans",
            "verify evidence / failure / rollback / post-review / verifier",
            "verify forbidden actions all blocked",
            "no real check execution",
        ],
        **meta,
    }

    planning_pass = (
        input_ok
        and auth_input.get("review_pass") is True
        and blocked_matrix.get("all_blocked") is True
        and allowed_check_plan.get("check_count") == 5
        and forbidden_plan.get("forbidden_count") == len(MINIMAL_FORBIDDEN_ACTIONS)
        and owner_confirmation_plan.get("owner_confirmation_collected_now") is False
    )

    planning_decision = {
        "decision_id": "real_minimal_controlled_execution_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "real_minimal_controlled_execution_planning_policy_v1",
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
        "boundary_ok": planning_pass,
        "violations": blockers,
        "planning_pass": planning_pass,
        "final_decision": planning_decision["final_decision"],
        "recommended_next_phase": planning_decision["recommended_next_phase"],
        **meta,
    }

    return {
        "real_minimal_controlled_execution_planning_policy": policy,
        "authorization_decision_input_review": auth_input,
        "real_execution_scope_lock": scope_lock,
        "real_execution_window_opening_plan": window_opening_plan,
        "real_execution_sandbox_plan": sandbox_plan,
        "real_execution_allowed_check_plan": allowed_check_plan,
        "real_execution_forbidden_action_plan": forbidden_plan,
        "real_execution_evidence_capture_plan": evidence_plan,
        "real_execution_failure_route_plan": failure_plan,
        "real_execution_rollback_boundary_plan": rollback_plan,
        "real_execution_owner_confirmation_plan": owner_confirmation_plan,
        "real_execution_post_review_plan": post_review_plan,
        "real_execution_verifier_plan": verifier_plan,
        "provider_selection_non_finalize_plan": provider_plan,
        "real_execution_blocked_path_matrix": blocked_matrix,
        "real_execution_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "real_minimal_controlled_execution_planning_decision": planning_decision,
        "summary": summary,
    }
