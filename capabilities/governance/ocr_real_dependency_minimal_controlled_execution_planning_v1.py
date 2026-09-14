# -*- coding: utf-8 -*-
"""OCR Real Dependency Minimal Controlled Execution Planning v1 — planning-only, 5 checks."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    FINAL_DECISION_GO as UPSTREAM_PREFLIGHT_FINAL_GO,
    MINIMAL_SCOPE_ALLOWED_CHECKS,
    NEXT_PHASE_GO as UPSTREAM_PREFLIGHT_NEXT_PHASE,
)
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    BLOCKED_PATHS as PREFLIGHT_BLOCKED,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Minimal-Controlled-Execution-Planning-v1-001"
SCOPE = "minimal_controlled_execution_planning_only"
SOURCE_CHAIN = "ocr_real_dependency_minimal_controlled_execution_planning_v1"

UPSTREAM_PREFLIGHT_FINAL = UPSTREAM_PREFLIGHT_FINAL_GO
UPSTREAM_PREFLIGHT_NEXT = UPSTREAM_PREFLIGHT_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_MINIMAL_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_MINIMAL_CONTROLLED_EXECUTION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Minimal-Controlled-Execution-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Minimal-Controlled-Execution-Planning-Issue-Review-v1-001"

EXCLUDED_FROM_SCOPE: Tuple[str, ...] = (
    "provider_initialization_dry_check",
    "runtime_smoke_check",
    "sample_ocr_check",
    "OCRRequest_submit",
    "image_read",
    "crop",
    "OCR_fact_generation",
    "provider_selection_finalize",
    "controlled_trial",
    "production_runtime",
)

MINIMAL_FORBIDDEN_ACTIONS: Tuple[str, ...] = (
    "pip_install",
    "dependency_auto_install",
    "model_download",
    "cache_mutation_without_approval",
    "provider_runtime_invocation",
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
    "controlled_trial_start",
    "production_runtime",
)

EVIDENCE_OUTPUT_ITEMS: Tuple[str, ...] = (
    "execution_window_ref",
    "environment_snapshot",
    "python_version_snapshot",
    "package_presence_result",
    "model_cache_path_result",
    "model_file_existence_result",
    "model_file_hash_result",
    "provider_import_check_result",
    "boundary_audit_result",
    "failure_route_result",
    "rollback_result",
    "verifier_report",
    "post_execution_review",
)

FAILURE_ROUTES: Tuple[Dict[str, str], ...] = (
    {
        "condition": "package_missing",
        "action": "record_failure_only",
        "must_not": "install",
    },
    {
        "condition": "cache_path_missing",
        "action": "record_failure_only",
        "must_not": "create_production_cache",
    },
    {
        "condition": "model_file_missing",
        "action": "record_failure_only",
        "must_not": "download",
    },
    {
        "condition": "hash_mismatch",
        "action": "record_failure_only",
        "must_not": "modify_cache",
    },
    {
        "condition": "import_failed",
        "action": "record_failure_only",
        "must_not": "repair_or_install",
    },
    {
        "condition": "unexpected_runtime_invocation",
        "action": "hard_block",
        "emit": "violation_report_candidate",
    },
    {
        "condition": "unauthorized_network_access",
        "action": "hard_block",
        "emit": "violation_report_candidate",
    },
    {
        "condition": "production_write_attempt",
        "action": "hard_block",
        "emit": "rollback_required",
    },
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_execution_window_open",
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
    "Planning GO ≠ minimal controlled execution started",
    "allowed checks planned ≠ checks executed",
    "execution window candidate ≠ execution window opened",
    "provider import check planned ≠ provider imported",
    "next DryRunAndReview ≠ real execution allowed",
)

CHECK_TYPES: Dict[str, str] = {
    "package_presence_check": "package_presence",
    "model_cache_path_check": "model_cache_path",
    "model_file_existence_check": "model_file_existence",
    "model_file_hash_check": "model_file_hash",
    "provider_import_check": "provider_import",
}

BOUNDARY_FALSE: Tuple[str, ...] = (
    "minimal_controlled_execution_started_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_presence_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_import_check_executed_now",
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
    "ocr_real_dependency_minimal_controlled_execution_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "minimal_controlled_execution_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
        "controlled_execution_authorized_now": False,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _minimal_check_item(check_id: str) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "check_type": CHECK_TYPES[check_id],
        "execution_allowed_later": True,
        "current_executed_now": False,
        "evidence_required": True,
        "failure_route_required": True,
        "rollback_required": True,
        "post_execution_review_required": True,
        "failure_route_ref": f"minimal_failure_route_plan_v1#{check_id}",
    }


def run_ocr_real_dependency_minimal_controlled_execution_planning_v1(
    *,
    ocr_real_dependency_execution_final_preflight_root: str,
    ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root: str,
    ocr_real_dependency_execution_authorization_dryrun_and_review_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    preflight_root = Path(ocr_real_dependency_execution_final_preflight_root).expanduser().resolve()
    auth_dr_root = Path(
        ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    exec_auth_dr_root = Path(
        ocr_real_dependency_execution_authorization_dryrun_and_review_root
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()

    preflight_sm = _try_read_json(preflight_root / "summary.json") or {}
    preflight_vr = _try_read_json(preflight_root / "verifier_report.json") or {}
    preflight_blocked = _try_read_json(
        preflight_root / "final_preflight_blocked_path_result_v1.json"
    ) or {}
    minimal_scope_upstream = _try_read_json(
        preflight_root / "controlled_execution_minimal_scope_plan_v1.json"
    ) or {}
    auth_vr = _try_read_json(auth_dr_root / "verifier_report.json") or {}
    exec_auth_vr = _try_read_json(exec_auth_dr_root / "verifier_report.json") or {}
    ocr_dr_vr = _try_read_json(ocr_dr_root / "verifier_report.json") or {}
    val_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_final_preflight_root": str(preflight_root),
        "upstream_authorization_dryrun_root": str(auth_dr_root),
        "upstream_execution_authorization_dryrun_root": str(exec_auth_dr_root),
        "upstream_ocr_via_factory_dryrun_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_root": str(val_dr_root),
        "output_root": str(out_root),
    }

    if preflight_vr.get("verifier") != "GO":
        blockers.append("final preflight verifier must be GO")
    if preflight_sm.get("final_decision") != UPSTREAM_PREFLIGHT_FINAL:
        blockers.append("final preflight final_decision mismatch")
    if preflight_sm.get("recommended_next_phase") != UPSTREAM_PREFLIGHT_NEXT:
        blockers.append("final preflight recommended_next_phase mismatch")
    if preflight_sm.get("controlled_execution_authorized_now") is not False:
        blockers.append("controlled_execution_authorized_now must be false")
    if preflight_blocked.get("all_blocked") is not True or preflight_blocked.get("blocked_count") != 24:
        blockers.append("24 preflight blocked paths must remain blocked")
    if preflight_sm.get("provider_selection_finalized_now") is not False:
        blockers.append("provider_selection_finalized_now must be false")
    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if auth_vr.get("verifier") != "GO":
        blockers.append("authorization dryrun should be GO")
    if exec_auth_vr.get("verifier") != "GO":
        blockers.append("execution authorization dryrun should be GO")
    if ocr_dr_vr.get("verifier") != "GO":
        blockers.append("ocr via factory dryrun should be GO")
    if val_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun should be GO")
    if val_model.get("runtime_enabled_now") is True:
        blockers.append("validator runtime must not be enabled")

    upstream_allowed = minimal_scope_upstream.get("allowed_checks_if_controlled_execution_entered") or []
    if list(upstream_allowed) != list(MINIMAL_SCOPE_ALLOWED_CHECKS):
        blockers.append("upstream minimal scope must match 5 allowed checks")

    input_ok = len(blockers) == 0

    preflight_input = {
        "review_id": "final_preflight_input_review_v1",
        "upstream_root": str(preflight_root),
        "verifier_go": preflight_vr.get("verifier") == "GO",
        "final_decision": preflight_sm.get("final_decision"),
        "recommended_next_phase": preflight_sm.get("recommended_next_phase"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    execution_scope = {
        "scope_id": "minimal_execution_scope_v1",
        "scope": "minimal_real_dependency_check",
        "allowed_checks_later": list(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "allowed_check_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "excluded_from_scope": list(EXCLUDED_FROM_SCOPE),
        "planning_only": True,
        **meta,
    }

    window_plan = {
        "plan_id": "minimal_execution_window_candidate_plan_v1",
        "execution_window_candidate_id": "ocr_minimal_controlled_execution_window_candidate_v1",
        "scope": "minimal_real_dependency_check",
        "allowed_checks": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "allowed_workspace_path": "_tmp_eval_out/ocr_real_dependency_minimal_controlled_execution_sandbox",
        "allowed_output_path": "_tmp_eval_out/ocr_real_dependency_minimal_controlled_execution_evidence",
        "forbidden_paths": [
            "memory/",
            "world_model/",
            "production_runtime/",
            "user_facing_output/",
        ],
        "timeout_limit": "bounded_minimal_execution_window_ttl",
        "no_production_write": True,
        "no_network_by_default": True,
        "no_install": True,
        "no_download": True,
        "no_cache_mutation_without_approval": True,
        "post_execution_review_required": True,
        "window_opened_now": False,
        "candidate_only": True,
        **meta,
    }

    sandbox_plan = {
        "plan_id": "minimal_execution_sandbox_plan_v1",
        "workspace_controlled_only": True,
        "no_production_path_write": True,
        "no_global_registry_write": True,
        "no_external_transmission": True,
        "no_dependency_install": True,
        "no_model_download": True,
        "no_cache_mutation": True,
        "no_provider_runtime_invocation_beyond_import_check_planning": True,
        "no_ocr_runtime": True,
        "no_user_output": True,
        "allowed_workspace_path": window_plan["allowed_workspace_path"],
        **meta,
    }

    allowed_check_plan = {
        "plan_id": "minimal_allowed_check_plan_v1",
        "check_count": len(MINIMAL_SCOPE_ALLOWED_CHECKS),
        "checks": [_minimal_check_item(cid) for cid in MINIMAL_SCOPE_ALLOWED_CHECKS],
        "all_current_executed_now_false": True,
        **meta,
    }

    forbidden_plan = {
        "plan_id": "minimal_forbidden_action_plan_v1",
        "forbidden_actions": list(MINIMAL_FORBIDDEN_ACTIONS),
        "forbidden_count": len(MINIMAL_FORBIDDEN_ACTIONS),
        **meta,
    }

    evidence_plan = {
        "plan_id": "minimal_evidence_output_plan_v1",
        "future_execution_must_generate": list(EVIDENCE_OUTPUT_ITEMS),
        "evidence_count": len(EVIDENCE_OUTPUT_ITEMS),
        "evidence_collected_now": False,
        **meta,
    }

    failure_plan = {
        "plan_id": "minimal_failure_route_plan_v1",
        "routes": list(FAILURE_ROUTES),
        "route_count": len(FAILURE_ROUTES),
        **meta,
    }

    rollback_plan = {
        "plan_id": "minimal_rollback_plan_v1",
        "failed_package_check_does_not_trigger_install": True,
        "failed_import_does_not_trigger_repair": True,
        "missing_model_file_does_not_trigger_download": True,
        "hash_mismatch_does_not_trigger_cache_mutation": True,
        "rollback_required_before_execution": True,
        "rollback_executed_now": False,
        **meta,
    }

    post_review_plan = {
        "plan_id": "minimal_post_execution_review_plan_v1",
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
        "plan_id": "minimal_execution_verifier_plan_v1",
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
        "minimal_execution_evidence_may_inform_provider_selection_later": True,
        "current_planning_cannot_finalize_provider": True,
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "minimal_execution_blocked_path_matrix_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "planning_only": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        "preflight_blocked_count": len(PREFLIGHT_BLOCKED),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "minimal_controlled_execution_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_objectives": [
            "generate minimal_controlled_execution_plan_candidate",
            "verify 5 allowed check execution plans",
            "verify forbidden actions all blocked",
            "verify evidence / rollback / post-review plans",
            "no real package/import/cache/hash execution",
        ],
        **meta,
    }

    planning_pass = (
        input_ok
        and preflight_input.get("review_pass") is True
        and blocked_matrix.get("all_blocked") is True
        and allowed_check_plan.get("check_count") == 5
        and forbidden_plan.get("forbidden_count") == len(MINIMAL_FORBIDDEN_ACTIONS)
    )

    planning_decision = {
        "decision_id": "minimal_controlled_execution_planning_decision_v1",
        "planning_pass": planning_pass,
        "high_risk": not planning_pass,
        "final_decision": FINAL_DECISION_GO if planning_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if planning_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "minimal_controlled_execution_planning_policy_v1",
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
        "minimal_controlled_execution_planning_policy": policy,
        "final_preflight_input_review": preflight_input,
        "minimal_execution_scope": execution_scope,
        "minimal_execution_window_candidate_plan": window_plan,
        "minimal_execution_sandbox_plan": sandbox_plan,
        "minimal_allowed_check_plan": allowed_check_plan,
        "minimal_forbidden_action_plan": forbidden_plan,
        "minimal_evidence_output_plan": evidence_plan,
        "minimal_failure_route_plan": failure_plan,
        "minimal_rollback_plan": rollback_plan,
        "minimal_post_execution_review_plan": post_review_plan,
        "minimal_execution_verifier_plan": verifier_plan,
        "provider_selection_non_finalize_plan": provider_plan,
        "minimal_execution_blocked_path_matrix": blocked_matrix,
        "minimal_controlled_execution_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "minimal_controlled_execution_planning_decision": planning_decision,
        "summary": summary,
    }
