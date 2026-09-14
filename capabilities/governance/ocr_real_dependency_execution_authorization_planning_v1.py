# -*- coding: utf-8 -*-
"""OCR Real Dependency Check Execution Authorization Planning v1."""

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
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_roadmap_decision_v1 import (
    FINAL_DECISION_GO as ROADMAP_FINAL_GO,
    NEXT_PHASE_GO as ROADMAP_NEXT_PHASE,
    SELECTED_ROUTE,
)

PHASE_ID = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-Planning-v1-001"
SCOPE = "ocr_real_dependency_execution_authorization_planning_only"
SOURCE_CHAIN = "ocr_real_dependency_execution_authorization_planning_v1"

UPSTREAM_ROADMAP_FINAL = ROADMAP_FINAL_GO
UPSTREAM_ROADMAP_NEXT = ROADMAP_NEXT_PHASE
UPSTREAM_VALIDATION_SEP_DR_FINAL = VALIDATION_SEP_DR_FINAL_GO

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_EXECUTION_AUTHORIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Execution-Authorization-Issue-Review-v1-001"

SCOPE_ALLOWED_CHECKS: Tuple[str, ...] = ALLOWED_CHECKS

SCOPE_NOT_COVERED: Tuple[str, ...] = (
    "provider_selection_finalize",
    "controlled_trial",
    "production_runtime",
    "OCRRequest_submission",
    "image_read_for_ocr",
    "crop_for_ocr",
    "OCR_fact_write",
    "user_facing_ocr_output",
    "memory_write",
    "world_model_write",
)

FORBIDDEN_EXECUTION_ACTIONS: Tuple[str, ...] = (
    "pip_install",
    "dependency_auto_install",
    "model_download",
    "cache_mutation_without_approval",
    "provider_runtime_invocation",
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

EVIDENCE_ARTIFACTS: Tuple[str, ...] = (
    "authorization_request_ref",
    "execution_grant_ref",
    "execution_window_ref",
    "domain_config_ref",
    "validation_gate_result",
    "environment_snapshot",
    "python_version_snapshot",
    "package_presence_result",
    "model_cache_path_result",
    "model_file_existence_result",
    "model_file_hash_result",
    "import_check_result",
    "boundary_audit_result",
    "failure_route_result",
    "rollback_result",
    "verifier_report",
    "post_execution_review",
)

STATE_MACHINE_STATES: Tuple[str, ...] = (
    "planning_defined",
    "request_candidate_ready_later",
    "grant_candidate_ready_later",
    "execution_window_candidate_ready_later",
    "validation_gate_ready_later",
    "execution_authorized_later",
    "real_dependency_check_executed_later",
    "post_execution_review_required_later",
    "closed_later",
)

VALIDATION_GATE_PATH: Tuple[Dict[str, str], ...] = (
    {"input": "domain_config_candidate", "gate": "AuthorizationValidationGate"},
    {"input": "allowed_checks", "gate": "Factory Authorization Standard validator"},
    {"input": "forbidden_actions", "gate": "BoundaryGate"},
    {"input": "provider_candidate_refs", "gate": "ControlledProviderReadinessHarness"},
    {"input": "evidence_refs", "gate": "EvidenceChainValidator"},
    {"input": "no-runtime requirements", "gate": "NoRuntimeBoundaryAudit"},
    {"input": "health_binding_refs", "gate": "HealthCheckValidator"},
    {"input": "aggregated", "gate": "Validation Factory"},
    {"input": "failed_gate", "gate": "IssueTracebackEngine + ViolationReportEngine"},
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_request_generation",
    "planning_to_request_send",
    "planning_to_grant_issue",
    "planning_to_execution_window_open",
    "planning_to_domain_config_activation",
    "planning_to_validation_runtime_enable",
    "planning_to_real_dependency_check",
    "planning_to_package_check",
    "planning_to_provider_import",
    "planning_to_model_cache_check",
    "planning_to_model_file_hash_check",
    "planning_to_dependency_install",
    "planning_to_model_download",
    "planning_to_cache_mutation",
    "planning_to_provider_invoke",
    "planning_to_provider_selection_finalize",
    "planning_to_controlled_trial",
    "planning_to_ocr_request_submit",
    "planning_to_image_read",
    "planning_to_crop",
    "planning_to_ocr_fact",
    "planning_to_user_output",
    "planning_to_memory_write",
    "planning_to_world_model_write",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Execution Authorization Planning GO ≠ execution authorized",
    "allowed checks planned ≠ checks executed",
    "execution window candidate ≠ execution window opened",
    "validation gate path planned ≠ validator runtime enabled",
    "next DryRunAndReview ≠ provider import allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "execution_authorization_request_generated_now",
    "execution_authorization_request_sent_now",
    "execution_grant_issued_now",
    "execution_window_opened_now",
    "domain_config_activated_now",
    "validation_runtime_enabled_now",
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
    "ocr_real_dependency_execution_authorization_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_real_dependency_execution_authorization_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_FALSE:
        meta[field] = False
    return meta


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _check_plan_item(check_id: str) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "allowed_later": True,
        "current_executed_now": False,
        "requires_execution_window": True,
        "requires_sandbox": True,
        "requires_evidence": True,
        "requires_validation_gate": True,
        "requires_post_execution_review": True,
        "failure_route_ref": f"rollback_and_failure_route_plan_v1#{check_id}",
    }


def run_ocr_real_dependency_execution_authorization_planning_v1(
    *,
    ocr_real_dependency_execution_authorization_roadmap_decision_root: str,
    ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root: str,
    midplatform_validation_engineering_separation_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    roadmap_root = Path(
        ocr_real_dependency_execution_authorization_roadmap_decision_root
    ).expanduser().resolve()
    ocr_dr_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root
    ).expanduser().resolve()
    val_dr_root = Path(
        midplatform_validation_engineering_separation_dryrun_and_review_root
    ).expanduser().resolve()
    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or roadmap_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()
    explain_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
        or roadmap_root.parent / "midplatform_constitution_governance_explanation_dryrun_and_review"
    ).expanduser().resolve()
    harness_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or roadmap_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()

    roadmap_sm = _try_read_json(roadmap_root / "summary.json") or {}
    roadmap_vr = _try_read_json(roadmap_root / "verifier_report.json") or {}
    ocr_domain_config = _try_read_json(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    ) or {}
    val_dr_vr = _try_read_json(val_dr_root / "verifier_report.json") or {}
    val_dr_sm = _try_read_json(val_dr_root / "summary.json") or {}
    val_model = _try_read_json(val_dr_root / "validation_engineering_model_candidate_v1.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}
    explain_vr = _try_read_json(explain_root / "verifier_report.json") or {}
    harness_vr = _try_read_json(harness_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_roadmap_decision_root": str(roadmap_root),
        "upstream_ocr_via_factory_dryrun_review_root": str(ocr_dr_root),
        "upstream_validation_separation_dryrun_review_root": str(val_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_root),
        "upstream_explanation_dryrun_review_root": str(explain_root),
        "upstream_harness_post_review_root": str(harness_root),
        "output_root": str(out_root),
    }

    if roadmap_vr.get("verifier") != "GO":
        blockers.append("roadmap decision verifier must be GO")
    if roadmap_sm.get("final_decision") != UPSTREAM_ROADMAP_FINAL:
        blockers.append("roadmap final_decision mismatch")
    if roadmap_sm.get("recommended_next_phase") != UPSTREAM_ROADMAP_NEXT:
        blockers.append("roadmap recommended_next_phase mismatch")
    if roadmap_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if not ocr_domain_config.get("candidate_id"):
        blockers.append("domain_config candidate required")
    if ocr_domain_config.get("candidate_only") is not True:
        blockers.append("domain_config must be candidate_only")
    if ocr_domain_config.get("activated_now") is not False:
        blockers.append("domain_config must not be activated")
    if val_dr_vr.get("verifier") != "GO":
        blockers.append("validation separation dryrun must be GO")
    if val_dr_sm.get("final_decision") != UPSTREAM_VALIDATION_SEP_DR_FINAL:
        blockers.append("validation separation final_decision mismatch")
    if val_model.get("runtime_enabled_now") is not False:
        blockers.append("validator runtime must not be enabled")
    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun must be GO")
    if explain_vr.get("verifier") != "GO":
        blockers.append("constitution explanation dryrun must be GO")
    if harness_vr.get("verifier") != "GO":
        blockers.append("harness post review must be GO")

    domain_config_ref = str(
        ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json"
    )

    roadmap_input = {
        "review_id": "roadmap_decision_input_review_v1",
        "upstream_root": str(roadmap_root),
        "verifier_go": roadmap_vr.get("verifier") == "GO",
        "final_decision": roadmap_sm.get("final_decision"),
        "selected_route": roadmap_sm.get("selected_route"),
        "review_pass": roadmap_vr.get("verifier") == "GO"
        and roadmap_sm.get("final_decision") == UPSTREAM_ROADMAP_FINAL
        and roadmap_sm.get("selected_route") == SELECTED_ROUTE,
        "blockers": blockers,
        **meta,
    }

    domain_input = {
        "review_id": "domain_config_candidate_input_review_v1",
        "domain_config_ref": domain_config_ref,
        "candidate_id": ocr_domain_config.get("candidate_id"),
        "candidate_only": ocr_domain_config.get("candidate_only"),
        "activated_now": ocr_domain_config.get("activated_now"),
        "factory_authorization_standard_ref": ocr_domain_config.get(
            "factory_authorization_standard_ref"
        ),
        "review_pass": ocr_domain_config.get("candidate_only") is True
        and ocr_domain_config.get("activated_now") is False,
        **meta,
    }

    val_input = {
        "review_id": "validation_engineering_input_review_v1",
        "validation_engineering_model_id": val_model.get("model_id"),
        "runtime_enabled_now": val_model.get("runtime_enabled_now"),
        "rulemaking_allowed": val_model.get("rulemaking_allowed"),
        "review_pass": val_dr_vr.get("verifier") == "GO"
        and val_model.get("runtime_enabled_now") is False,
        **meta,
    }

    execution_scope = {
        "scope_id": "execution_authorization_scope_v1",
        "planning_future_execution_authorization_only": True,
        "authorization_target": "real_dependency_check_execution",
        "allowed_checks_in_scope": list(SCOPE_ALLOWED_CHECKS),
        "not_covered_in_this_phase": list(SCOPE_NOT_COVERED),
        "provider_domain": "ocr",
        **meta,
    }

    request_candidate = {
        "contract_id": "execution_authorization_request_candidate_contract_v1",
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
        "request_generated_now": False,
        "request_sent_now": False,
        **meta,
    }

    grant_candidate = {
        "contract_id": "execution_grant_candidate_contract_v1",
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
        **meta,
    }

    window_candidate = {
        "contract_id": "execution_window_candidate_contract_v1",
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
        **meta,
    }

    sandbox_plan = {
        "plan_id": "execution_sandbox_boundary_plan_v1",
        "sandbox_required": True,
        "isolated_workspace": True,
        "read_only_domain_config": True,
        "no_production_paths": True,
        "no_memory_worldmodel_write": True,
        "evidence_output_only_to_allowed_output_path": True,
        **meta,
    }

    allowed_check_plan = {
        "plan_id": "allowed_real_dependency_check_plan_v1",
        "check_count": len(SCOPE_ALLOWED_CHECKS),
        "checks": [_check_plan_item(cid) for cid in SCOPE_ALLOWED_CHECKS],
        **meta,
    }

    forbidden_plan = {
        "plan_id": "forbidden_execution_action_plan_v1",
        "forbidden_actions": list(FORBIDDEN_EXECUTION_ACTIONS),
        "forbidden_count": len(FORBIDDEN_EXECUTION_ACTIONS),
        **meta,
    }

    evidence_plan = {
        "plan_id": "evidence_collection_plan_v1",
        "collect_on_future_execution": list(EVIDENCE_ARTIFACTS),
        "evidence_collected_now": False,
        **meta,
    }

    rollback_plan = {
        "plan_id": "rollback_and_failure_route_plan_v1",
        "failed_package_check_does_not_trigger_install": True,
        "failed_import_does_not_trigger_repair": True,
        "missing_model_file_does_not_trigger_download": True,
        "hash_mismatch_does_not_trigger_cache_mutation": True,
        "smoke_failure_does_not_trigger_provider_switch": True,
        "rollback_required_before_execution": True,
        "rollback_executed_now": False,
        **meta,
    }

    validation_gate_plan = {
        "plan_id": "validation_gate_execution_path_plan_v1",
        "path_mappings": list(VALIDATION_GATE_PATH),
        "validator_runtime_enabled_now": False,
        "validation_factory_runtime_enforced_now": False,
        "no_gate_executed_now": True,
        **meta,
    }

    provider_non_finalize = {
        "plan_id": "provider_selection_non_finalize_plan_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "real_dependency_execution_authorization_not_equal_provider_selected": True,
        "future_evidence_may_support_provider_finalize": True,
        "current_phase_cannot_finalize_provider": True,
        **meta,
    }

    state_machine = {
        "machine_id": "execution_authorization_state_machine_v1",
        "states": list(STATE_MACHINE_STATES),
        "current_state": "planning_defined",
        "transitions_planned_later": [
            {"from": "planning_defined", "to": "request_candidate_ready_later"},
            {"from": "request_candidate_ready_later", "to": "grant_candidate_ready_later"},
            {"from": "grant_candidate_ready_later", "to": "execution_window_candidate_ready_later"},
            {"from": "execution_window_candidate_ready_later", "to": "validation_gate_ready_later"},
            {"from": "validation_gate_ready_later", "to": "execution_authorized_later"},
            {"from": "execution_authorized_later", "to": "real_dependency_check_executed_later"},
            {
                "from": "real_dependency_check_executed_later",
                "to": "post_execution_review_required_later",
            },
            {"from": "post_execution_review_required_later", "to": "closed_later"},
        ],
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "execution_authorization_blocked_path_matrix_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "planning_only": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    dryrun_plan = {
        "plan_id": "execution_authorization_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_objectives": [
            "generate execution_authorization_request_candidate",
            "generate execution_grant_candidate",
            "generate execution_window_candidate",
            "generate allowed_check_plan_candidate",
            "generate evidence_collection_candidate",
            "verify validation gate path",
            "verify all real check actions remain blocked",
            "no formal request generation",
            "no grant",
            "no execution window open",
            "no package/import/cache/hash execution",
        ],
        **meta,
    }

    input_ok = len(blockers) == 0
    boundary_ok = (
        input_ok
        and domain_input.get("review_pass") is True
        and val_input.get("review_pass") is True
        and blocked_matrix.get("all_blocked") is True
        and state_machine.get("current_state") == "planning_defined"
    )

    planning_decision = {
        "decision_id": "execution_authorization_planning_decision_v1",
        "planning_pass": boundary_ok,
        "high_risk": not boundary_ok,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else NEXT_PHASE_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_execution_authorization_planning_policy_v1",
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
        "allowed_check_count": len(SCOPE_ALLOWED_CHECKS),
        "forbidden_action_count": len(FORBIDDEN_EXECUTION_ACTIONS),
        "blocked_path_count": len(BLOCKED_PATHS),
        "current_state": "planning_defined",
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_real_dependency_execution_authorization_planning_policy": policy,
        "roadmap_decision_input_review": roadmap_input,
        "domain_config_candidate_input_review": domain_input,
        "validation_engineering_input_review": val_input,
        "execution_authorization_scope": execution_scope,
        "execution_authorization_request_candidate_contract": request_candidate,
        "execution_grant_candidate_contract": grant_candidate,
        "execution_window_candidate_contract": window_candidate,
        "execution_sandbox_boundary_plan": sandbox_plan,
        "allowed_real_dependency_check_plan": allowed_check_plan,
        "forbidden_execution_action_plan": forbidden_plan,
        "evidence_collection_plan": evidence_plan,
        "rollback_and_failure_route_plan": rollback_plan,
        "validation_gate_execution_path_plan": validation_gate_plan,
        "provider_selection_non_finalize_plan": provider_non_finalize,
        "execution_authorization_state_machine": state_machine,
        "execution_authorization_blocked_path_matrix": blocked_matrix,
        "execution_authorization_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims,
        "execution_authorization_planning_decision": planning_decision,
        "summary": summary,
    }
