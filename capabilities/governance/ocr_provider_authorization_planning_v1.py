# -*- coding: utf-8 -*-
"""OCR Provider Authorization Planning v1 — lifecycle contracts only, no grant."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_authorization_return_roadmap_decision_v1 import (
    FINAL_DECISION_GO as RETURN_FINAL_GO,
    NEXT_PHASE_GO as RETURN_NEXT_PHASE,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Provider-Authorization-Planning-v1-001"
SCOPE = "ocr_provider_authorization_planning_only"
SOURCE_CHAIN = "ocr_provider_authorization_planning_v1"

UPSTREAM_RETURN_FINAL = RETURN_FINAL_GO
UPSTREAM_RETURN_NEXT = RETURN_NEXT_PHASE

FINAL_DECISION_GO = "OCR_PROVIDER_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION_HOLD = "OCR_PROVIDER_AUTHORIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
NEXT_PHASE_GO = "Phase-OCR-Provider-Authorization-DryRun-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Authorization-Issue-Review-v1-001"

AUTHORIZATION_SCOPE_COVERED: Tuple[str, ...] = (
    "real_dependency_check_authorization",
    "provider_import_check_authorization",
    "provider_smoke_check_authorization",
    "sample_ocr_check_authorization_later",
    "controlled_trial_authorization_later",
)

AUTHORIZATION_SCOPE_NOT_COVERED: Tuple[str, ...] = (
    "production_runtime",
    "user_facing_ocr_output",
    "ocr_fact_write",
    "memory_write",
    "world_model_write",
    "final_provider_selection",
)

EVIDENCE_REQUIREMENTS: Tuple[str, ...] = (
    "authorization_request",
    "authorization_grant",
    "execution_window",
    "environment_snapshot",
    "dependency_check_result",
    "import_check_result",
    "model_cache_check_result",
    "boundary_audit",
    "failure_route_result",
    "verifier_report",
    "post_execution_review",
)

BOUNDARY_BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_authorization_request_generation",
    "planning_to_authorization_grant",
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

LIFECYCLE_STATES: Tuple[str, ...] = (
    "planning_defined",
    "request_candidate_ready",
    "request_generated_later",
    "request_sent_later",
    "grant_pending",
    "grant_issued_later",
    "execution_window_opened_later",
    "execution_completed_later",
    "post_execution_review_required",
    "closed",
)

CURRENT_LIFECYCLE_STATE = "planning_defined"

BOUNDARY_FALSE: Tuple[str, ...] = (
    "authorization_request_generated_now",
    "authorization_request_sent_now",
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
    "Planning GO ≠ provider authorization granted",
    "authorization contract planned ≠ request generated",
    "grant contract planned ≠ grant issued",
    "execution window planned ≠ window opened",
    "DryRun next ≠ real dependency check executed",
    "authorization planning ≠ provider selected",
    "authorization planning ≠ OCRRequest submitted",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_authorization_planning_only": True,
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


def run_ocr_provider_authorization_planning_v1(
    *,
    ocr_provider_authorization_return_roadmap_decision_root: str,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_selection_dependency_environment_post_dryrun_review_root: Optional[str] = None,
    ocr_controlled_provider_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []
    return_root = Path(ocr_provider_authorization_return_roadmap_decision_root).expanduser().resolve()
    return_sm = _try_read_json(return_root / "summary.json") or {}
    return_vr = _try_read_json(return_root / "verifier_report.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or return_root.parent / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}
    factory_closure = _try_read_json(
        factory_post_root / "factory_registration_closure_decision_v1.json"
    ) or {}

    real_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or return_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    sel_post_root = Path(
        ocr_provider_selection_dependency_environment_post_dryrun_review_root
        or return_root.parent / "ocr_provider_selection_dependency_environment_post_dryrun_review"
    ).expanduser().resolve()
    ocr_post_root = Path(
        ocr_controlled_provider_post_dryrun_review_root
        or return_root.parent / "ocr_controlled_provider_post_dryrun_review"
    ).expanduser().resolve()

    real_post_vr = _try_read_json(real_post_root / "verifier_report.json") or {}
    sel_post_vr = _try_read_json(sel_post_root / "verifier_report.json") or {}
    ocr_post_vr = _try_read_json(ocr_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_return_roadmap_root": str(return_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "upstream_real_dep_post_root": str(real_post_root),
        "upstream_selection_post_root": str(sel_post_root),
        "upstream_ocr_controlled_post_root": str(ocr_post_root),
        "output_root": str(out_root),
    }

    return_go = return_vr.get("verifier") == "GO" and return_vr.get("passed") is True
    if not return_go:
        blockers.append("return roadmap verifier must be GO")
    if return_sm.get("final_decision") != UPSTREAM_RETURN_FINAL:
        blockers.append("return roadmap final_decision mismatch")
    if return_sm.get("recommended_next_phase") != UPSTREAM_RETURN_NEXT:
        blockers.append("return roadmap recommended_next_phase mismatch")
    if return_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")

    if factory_post_vr.get("verifier") != "GO":
        blockers.append("factory registration post-review must be GO")
    if factory_closure.get("validation_factory_registry_candidate_trusted") is not True:
        blockers.append("harness seventh module candidate must be trusted")

    for vr, label in (
        (real_post_vr, "real dependency post-review"),
        (sel_post_vr, "selection post-review"),
        (ocr_post_vr, "controlled provider post-review"),
    ):
        if vr.get("verifier") != "GO":
            blockers.append(f"{label} must be GO")

    if return_sm.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must remain null")

    for field in (
        "provider_imported_now",
        "provider_invoked_now",
        "dependency_install_executed_now",
        "model_download_executed_now",
        "provider_authorization_granted_now",
    ):
        if return_sm.get(field) is True:
            blockers.append(f"{field} must be false")

    input_review = {
        "review_id": "authorization_return_roadmap_input_review_v1",
        "upstream_root": str(return_root),
        "upstream_verifier_go": return_go,
        "upstream_final_decision": return_sm.get("final_decision"),
        "selected_route": return_sm.get("selected_route"),
        "factory_registration_closed": factory_closure.get("factory_registration_dryrun_closed"),
        "review_pass": len(blockers) == 0,
        "blockers": blockers,
        **meta,
    }

    scope = {
        "scope_id": "ocr_provider_authorization_scope_v1",
        "planning_only": True,
        "does_not_execute_authorization": True,
        "covered_future_authorizations": list(AUTHORIZATION_SCOPE_COVERED),
        "not_covered_now": list(AUTHORIZATION_SCOPE_NOT_COVERED),
        **meta,
    }

    request_contract = {
        "contract_id": "authorization_request_contract_v1",
        "request_id": "ocr_provider_authorization_request_candidate_later",
        "request_type": "ocr_provider_authorization_request",
        "target_scope": list(AUTHORIZATION_SCOPE_COVERED),
        "provider_candidate_refs": "planned_candidate_refs_only",
        "dependency_check_scope": "real_dependency_check_plan_candidate",
        "environment_scope": "sandbox_workspace_fallback_only",
        "execution_window_required": True,
        "sandbox_required": True,
        "rollback_required": True,
        "evidence_package_required": True,
        "verifier_required": True,
        "owner_operator_approval_required": True,
        "current_request_generated_now": False,
        "current_request_sent_now": False,
        **meta,
    }

    grant_contract = {
        "contract_id": "authorization_grant_contract_v1",
        "grant_id": "ocr_provider_authorization_grant_candidate_later",
        "related_request_id": "ocr_provider_authorization_request_candidate_later",
        "grant_scope": list(AUTHORIZATION_SCOPE_COVERED),
        "grant_conditions": [
            "owner_operator_approval_collected",
            "sandbox_boundary_confirmed",
            "rollback_plan_ready",
            "evidence_package_template_ready",
            "verifier_pass_required",
        ],
        "allowed_actions_later": [
            "real_dependency_check_dryrun",
            "provider_import_check",
            "provider_smoke_check",
            "sample_ocr_check_later",
        ],
        "prohibited_actions": [
            "production_runtime",
            "provider_selection_finalize",
            "ocr_fact_write",
            "memory_world_model_write",
            "user_facing_output",
        ],
        "expiration_ttl": "execution_window_bound",
        "revocation_condition": "boundary_violation_or_verifier_no_go",
        "post_execution_review_required": True,
        "current_grant_issued_now": False,
        "provider_authorization_granted_now": False,
        **meta,
    }

    execution_window = {
        "contract_id": "execution_window_contract_v1",
        "execution_window_id": "ocr_provider_authorization_execution_window_candidate_later",
        "allowed_phase_later": [
            "real_dependency_check_dryrun",
            "import_check",
            "smoke_check",
            "sample_ocr_check_later",
        ],
        "allowed_workspace_path": "_tmp_eval_out/ocr_provider_authorization_dryrun/",
        "allowed_output_path": "_tmp_eval_out/ocr_provider_authorization_dryrun/",
        "forbidden_paths": [
            "production_paths",
            "memory_world_model",
            "user_output_channels",
            "untracked_install_locations",
        ],
        "max_scope": "sandbox_single_provider_check",
        "timeout_limit": "bounded_execution_window",
        "no_production_write": True,
        "no_network_by_default": True,
        "current_window_opened_now": False,
        **meta,
    }

    sandbox_contract = {
        "contract_id": "sandbox_and_environment_boundary_contract_v1",
        "requirements": [
            "workspace_fallback_only",
            "no_production_path_write",
            "no_global_environment_modification",
            "no_untracked_install",
            "no_model_download_without_separate_authorization",
            "no_cache_mutation_without_approval",
            "no_real_ocr_invocation_without_controlled_trial_authorization",
        ],
        **meta,
    }

    rollback_contract = {
        "contract_id": "rollback_and_cleanup_contract_v1",
        "rules": [
            "failed_check_does_not_trigger_install",
            "failed_import_does_not_trigger_repair",
            "failed_model_cache_check_does_not_trigger_download",
            "failed_smoke_does_not_trigger_provider_switch",
            "all_outputs_evidence_only",
        ],
        "rollback_plan_ready_later": True,
        "rollback_executed_now": False,
        **meta,
    }

    evidence_requirement = {
        "requirement_id": "evidence_package_requirement_v1",
        "required_artifacts_on_future_execution": list(EVIDENCE_REQUIREMENTS),
        "evidence_only_outputs": True,
        **meta,
    }

    owner_operator = {
        "policy_id": "owner_operator_approval_policy_v1",
        "owner_operator_approval_required_for_real_dependency_check": True,
        "approval_required_for_import": True,
        "approval_required_for_install": True,
        "approval_required_for_model_download": True,
        "approval_required_for_controlled_trial": True,
        "approval_collected_now": False,
        **meta,
    }

    selection_binding = {
        "policy_id": "provider_selection_binding_policy_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "authorization_planning_not_provider_selected": True,
        "authorization_planning_not_provider_enabled": True,
        **meta,
    }

    real_dep_binding = {
        "binding_id": "real_dependency_check_authorization_binding_v1",
        "requires_authorization_grant": True,
        "requires_execution_window": True,
        "requires_owner_operator_approval": True,
        "real_dependency_check_executed_now": False,
        **meta,
    }

    trial_binding = {
        "binding_id": "controlled_trial_authorization_binding_v1",
        "requires_separate_controlled_trial_authorization": True,
        "controlled_trial_started_now": False,
        **meta,
    }

    boundary_matrix = {
        "matrix_id": "authorization_boundary_guard_matrix_v1",
        "paths": [{"path_id": p, "blocked": True, "default": True} for p in BOUNDARY_BLOCKED_PATHS],
        "path_count": len(BOUNDARY_BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    state_machine = {
        "machine_id": "authorization_lifecycle_state_machine_v1",
        "states": list(LIFECYCLE_STATES),
        "current_state": CURRENT_LIFECYCLE_STATE,
        "transitions_planned_only": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "authorization_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_objectives": [
            "generate authorization_request_candidate",
            "generate grant_candidate",
            "generate execution_window_candidate",
            "generate evidence_requirement_candidate",
            "verify grant/execution/provider actions remain blocked",
        ],
        "dryrun_forbidden": [
            "generate request artifact",
            "send request",
            "grant authorization",
            "execute real dependency check",
        ],
        **meta,
    }

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    planning_decision = {
        "decision_id": "ocr_provider_authorization_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ready_for_dryrun": boundary_ok,
        "current_lifecycle_state": CURRENT_LIFECYCLE_STATE,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_provider_authorization_planning_policy_v1",
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
        "boundary_path_count": len(BOUNDARY_BLOCKED_PATHS),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_provider_authorization_planning_policy": policy,
        "authorization_return_roadmap_input_review": input_review,
        "ocr_provider_authorization_scope": scope,
        "authorization_request_contract": request_contract,
        "authorization_grant_contract": grant_contract,
        "execution_window_contract": execution_window,
        "sandbox_and_environment_boundary_contract": sandbox_contract,
        "rollback_and_cleanup_contract": rollback_contract,
        "evidence_package_requirement": evidence_requirement,
        "owner_operator_approval_policy": owner_operator,
        "provider_selection_binding_policy": selection_binding,
        "real_dependency_check_authorization_binding": real_dep_binding,
        "controlled_trial_authorization_binding": trial_binding,
        "authorization_boundary_guard_matrix": boundary_matrix,
        "authorization_lifecycle_state_machine": state_machine,
        "authorization_dryrun_plan": dryrun_plan,
        "ocr_provider_authorization_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
