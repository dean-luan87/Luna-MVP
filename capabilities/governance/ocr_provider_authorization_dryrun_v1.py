# -*- coding: utf-8 -*-
"""OCR Provider Authorization DryRun v1 — authorization candidates only, no grant."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
    BOUNDARY_BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    CURRENT_LIFECYCLE_STATE as PLANNING_LIFECYCLE_STATE,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO as PLANNING_NEXT_PHASE,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-DryRun-v1-001"
SCOPE = "ocr_provider_authorization_dryrun_only"
SOURCE_CHAIN = "ocr_provider_authorization_dryrun_v1"

UPSTREAM_PLANNING_FINAL = PLANNING_FINAL_GO
UPSTREAM_PLANNING_NEXT = PLANNING_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_DRYRUN_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-Post-DryRun-Review-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Issue-Review-v1-001"

CURRENT_DRYRUN_STATE = "request_candidate_ready"

DRYRUN_BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_authorization_request_artifact_generation",
    "dryrun_to_authorization_request_send",
    "dryrun_to_authorization_grant",
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

NON_CLAIMS: Tuple[str, ...] = (
    "DryRun GO ≠ provider authorization granted",
    "request candidate ≠ request artifact generated",
    "grant candidate ≠ grant issued",
    "execution window candidate ≠ window opened",
    "Post-DryRun Review next ≠ real dependency check executed",
    "authorization candidate ≠ provider selected",
    "DryRun GO ≠ OCRRequest submitted",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
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

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_dryrun_only": True,
        "simulated": True,
        "authorization_request_candidate_generated_now": True,
        "grant_candidate_generated_now": True,
        "execution_window_candidate_generated_now": True,
        "sandbox_boundary_candidate_generated_now": True,
        "rollback_candidate_generated_now": True,
        "evidence_requirement_candidate_generated_now": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    meta["authorization_request_artifact_generated_now"] = False
    meta["provider_selection_finalized_now"] = False
    meta["selected_provider_for_execution"] = None
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def run_ocr_provider_authorization_dryrun_v1(
    *,
    ocr_provider_authorization_planning_root: str,
    ocr_provider_authorization_return_roadmap_decision_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    planning_root = Path(ocr_provider_authorization_planning_root).expanduser().resolve()
    plan_sm = _try_read_json(planning_root / "summary.json") or {}
    plan_vr = _try_read_json(planning_root / "verifier_report.json") or {}
    request_contract = _try_read_json(planning_root / "authorization_request_contract_v1.json") or {}
    grant_contract = _try_read_json(planning_root / "authorization_grant_contract_v1.json") or {}
    window_contract = _try_read_json(planning_root / "execution_window_contract_v1.json") or {}
    sandbox_contract = _try_read_json(planning_root / "sandbox_and_environment_boundary_contract_v1.json") or {}
    rollback_contract = _try_read_json(planning_root / "rollback_and_cleanup_contract_v1.json") or {}
    evidence_req = _try_read_json(planning_root / "evidence_package_requirement_v1.json") or {}
    owner_policy = _try_read_json(planning_root / "owner_operator_approval_policy_v1.json") or {}
    selection_policy = _try_read_json(planning_root / "provider_selection_binding_policy_v1.json") or {}
    boundary_plan = _try_read_json(planning_root / "authorization_boundary_guard_matrix_v1.json") or {}
    state_machine_plan = _try_read_json(planning_root / "authorization_lifecycle_state_machine_v1.json") or {}

    return_root = Path(
        ocr_provider_authorization_return_roadmap_decision_root
        or planning_root.parent / "ocr_provider_authorization_return_roadmap_decision"
    ).expanduser().resolve()
    return_sm = _try_read_json(return_root / "summary.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or planning_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    real_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or planning_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    real_post_vr = _try_read_json(real_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(planning_root),
        "upstream_return_roadmap_root": str(return_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_real_dep_post_root": str(real_post_root),
        "output_root": str(out_root),
    }

    planning_go = plan_vr.get("verifier") == "GO" and plan_vr.get("passed") is True
    if not planning_go:
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("recommended_next_phase") != UPSTREAM_PLANNING_NEXT:
        blockers.append("planning recommended_next_phase mismatch")
    if plan_sm.get("current_lifecycle_state") != PLANNING_LIFECYCLE_STATE:
        blockers.append("planning current_state must be planning_defined")
    if boundary_plan.get("path_count") != len(PLANNING_BLOCKED_PATHS):
        blockers.append("planning must have 14 blocked paths")

    if return_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if plan_sm.get("authorization_request_generated_now") is True:
        blockers.append("authorization_request_generated_now must be false")
    if plan_sm.get("provider_authorization_granted_now") is True:
        blockers.append("provider_authorization_granted_now must be false")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("factory registration post-review should be GO")
    if real_post_vr.get("verifier") != "GO":
        blockers.append("OCR real dependency post-review should be GO")

    if state_machine_plan.get("current_state") != PLANNING_LIFECYCLE_STATE:
        blockers.append("planning state machine must be planning_defined")

    input_review = {
        "review_id": "authorization_planning_input_review_v1",
        "upstream_planning_root": str(planning_root),
        "upstream_verifier_go": planning_go,
        "upstream_final_decision": plan_sm.get("final_decision"),
        "planning_lifecycle_state": plan_sm.get("current_lifecycle_state"),
        "planning_blocked_path_count": boundary_plan.get("path_count"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    request_candidate = {
        "candidate_id": "authorization_request_candidate_v1",
        "request_id": "ocr_provider_authorization_request_candidate_v1",
        "request_type": request_contract.get("request_type", "ocr_provider_authorization_request"),
        "target_scope": request_contract.get("target_scope", list(AUTHORIZATION_SCOPE_COVERED)),
        "provider_candidate_refs": request_contract.get("provider_candidate_refs"),
        "dependency_check_scope": request_contract.get("dependency_check_scope"),
        "environment_scope": request_contract.get("environment_scope"),
        "execution_window_required": True,
        "sandbox_required": True,
        "rollback_required": True,
        "evidence_package_required": True,
        "verifier_required": True,
        "owner_operator_approval_required": True,
        "candidate_only": True,
        "request_artifact_generated_now": False,
        "request_sent_now": False,
        **meta,
    }

    grant_candidate = {
        "candidate_id": "grant_candidate_v1",
        "grant_candidate_id": "ocr_provider_authorization_grant_candidate_v1",
        "related_request_candidate_id": "ocr_provider_authorization_request_candidate_v1",
        "grant_scope": grant_contract.get("grant_scope", list(AUTHORIZATION_SCOPE_COVERED)),
        "grant_conditions": grant_contract.get("grant_conditions"),
        "allowed_actions_later": grant_contract.get("allowed_actions_later"),
        "prohibited_actions": grant_contract.get("prohibited_actions"),
        "expiration_or_ttl": grant_contract.get("expiration_ttl"),
        "revocation_conditions": grant_contract.get("revocation_condition"),
        "post_execution_review_required": True,
        "candidate_only": True,
        "current_grant_issued_now": False,
        "provider_authorization_granted_now": False,
        **meta,
    }

    window_candidate = {
        "candidate_id": "execution_window_candidate_v1",
        "execution_window_candidate_id": "ocr_provider_authorization_execution_window_candidate_v1",
        "allowed_phase_later": window_contract.get("allowed_phase_later"),
        "allowed_workspace_path": window_contract.get("allowed_workspace_path"),
        "allowed_output_path": window_contract.get("allowed_output_path"),
        "forbidden_paths": window_contract.get("forbidden_paths"),
        "max_scope": window_contract.get("max_scope"),
        "timeout_limit": window_contract.get("timeout_limit"),
        "no_production_write": True,
        "no_network_by_default": True,
        "current_window_opened_now": False,
        "candidate_only": True,
        **meta,
    }

    sandbox_candidate = {
        "candidate_id": "sandbox_boundary_candidate_v1",
        "workspace_fallback_only": True,
        "no_production_path_write": True,
        "no_global_environment_modification": True,
        "no_untracked_install": True,
        "no_model_download_without_separate_authorization": True,
        "no_cache_mutation_without_approval": True,
        "no_real_ocr_invocation_without_controlled_trial_authorization": True,
        "requirements_from_planning": sandbox_contract.get("requirements"),
        "candidate_only": True,
        **meta,
    }

    rollback_candidate = {
        "candidate_id": "rollback_candidate_v1",
        "failed_check_does_not_trigger_install": True,
        "failed_import_does_not_trigger_repair": True,
        "failed_model_cache_check_does_not_trigger_download": True,
        "failed_smoke_does_not_trigger_provider_switch": True,
        "all_outputs_evidence_only": True,
        "rollback_plan_ready_later": rollback_contract.get("rollback_plan_ready_later", True),
        "rollback_executed_now": False,
        "candidate_only": True,
        **meta,
    }

    evidence_candidate = {
        "candidate_id": "evidence_requirement_candidate_v1",
        "required_artifacts_on_future_execution": evidence_req.get(
            "required_artifacts_on_future_execution", list(EVIDENCE_REQUIREMENTS)
        ),
        "evidence_only_outputs": True,
        "candidate_only": True,
        **meta,
    }

    owner_dryrun = {
        "result_id": "owner_operator_approval_dryrun_result_v1",
        "approval_required_for_real_dependency_check": owner_policy.get(
            "owner_operator_approval_required_for_real_dependency_check", True
        ),
        "approval_required_for_import": owner_policy.get("approval_required_for_import", True),
        "approval_required_for_install": owner_policy.get("approval_required_for_install", True),
        "approval_required_for_model_download": owner_policy.get("approval_required_for_model_download", True),
        "approval_required_for_controlled_trial": owner_policy.get(
            "approval_required_for_controlled_trial", True
        ),
        "approval_collected_now": False,
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    selection_dryrun = {
        "result_id": "provider_selection_binding_dryrun_result_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "authorization_candidate_not_provider_selected": selection_policy.get(
            "authorization_planning_not_provider_selected", True
        ),
        "authorization_candidate_not_provider_enabled": selection_policy.get(
            "authorization_planning_not_provider_enabled", True
        ),
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    real_dep_binding = {
        "result_id": "real_dependency_check_authorization_binding_dryrun_result_v1",
        "requires_authorization_grant": True,
        "requires_execution_window": True,
        "real_dependency_check_executed_now": False,
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    trial_binding = {
        "result_id": "controlled_trial_authorization_binding_dryrun_result_v1",
        "requires_separate_controlled_trial_authorization": True,
        "controlled_trial_started_now": False,
        "dryrun_pass": len(blockers) == 0,
        **meta,
    }

    lifecycle = {
        "result_id": "authorization_lifecycle_dryrun_result_v1",
        "states": list(LIFECYCLE_STATES),
        "simulated_progression": list(LIFECYCLE_STATES),
        "prior_state": PLANNING_LIFECYCLE_STATE,
        "current_state": CURRENT_DRYRUN_STATE,
        "request_generated_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        "lifecycle_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    boundary_guard = {
        "result_id": "authorization_boundary_guard_dryrun_result_v1",
        "paths": [{"path_id": p, "blocked": True, "executed_now": False} for p in DRYRUN_BLOCKED_PATHS],
        "path_count": len(DRYRUN_BLOCKED_PATHS),
        "all_blocked": True,
        "boundary_dryrun_pass": len(blockers) == 0,
        **meta,
    }

    blocked_result = {
        "result_id": "authorization_blocked_path_result_v1",
        "paths": boundary_guard["paths"],
        "path_count": boundary_guard["path_count"],
        "all_blocked": True,
        **meta,
    }

    checks_pass = (
        len(blockers) == 0
        and input_review.get("review_pass")
        and request_candidate.get("candidate_only")
        and grant_candidate.get("candidate_only")
        and window_candidate.get("current_window_opened_now") is False
        and sandbox_candidate.get("workspace_fallback_only")
        and rollback_candidate.get("rollback_executed_now") is False
        and lifecycle.get("lifecycle_dryrun_pass")
        and boundary_guard.get("boundary_dryrun_pass")
        and owner_dryrun.get("approval_collected_now") is False
    )

    readiness = {
        "decision_id": "authorization_dryrun_readiness_decision_v1",
        "request_candidate_pass": checks_pass,
        "grant_candidate_pass": checks_pass,
        "window_candidate_pass": checks_pass,
        "sandbox_pass": checks_pass,
        "rollback_pass": checks_pass,
        "evidence_pass": checks_pass,
        "approval_pass": checks_pass,
        "lifecycle_pass": checks_pass,
        "boundary_pass": checks_pass,
        "all_pass": checks_pass,
        "high_risk_count": 0 if checks_pass else 1,
        "final_decision": FINAL_DECISION_GO if checks_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if checks_pass else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_authorization_dryrun_policy_v1",
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
        "current_lifecycle_state": CURRENT_DRYRUN_STATE,
        "dryrun_blocked_path_count": len(DRYRUN_BLOCKED_PATHS),
        **meta,
    }

    return {
        "ocr_provider_authorization_dryrun_policy": policy,
        "authorization_planning_input_review": input_review,
        "authorization_request_candidate": request_candidate,
        "grant_candidate": grant_candidate,
        "execution_window_candidate": window_candidate,
        "sandbox_boundary_candidate": sandbox_candidate,
        "rollback_candidate": rollback_candidate,
        "evidence_requirement_candidate": evidence_candidate,
        "owner_operator_approval_dryrun_result": owner_dryrun,
        "provider_selection_binding_dryrun_result": selection_dryrun,
        "real_dependency_check_authorization_binding_dryrun_result": real_dep_binding,
        "controlled_trial_authorization_binding_dryrun_result": trial_binding,
        "authorization_lifecycle_dryrun_result": lifecycle,
        "authorization_boundary_guard_dryrun_result": boundary_guard,
        "authorization_blocked_path_result": blocked_result,
        "authorization_dryrun_readiness_decision": readiness,
        "non_claims_register": non_claims,
        "summary": summary,
    }
