# -*- coding: utf-8 -*-
"""OCR Provider Real Dependency Check Authorization Planning v1 — authorization planning only."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DRYRUN_REVIEW_FINAL_GO,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_authorization_next_route_decision_v1 import (
    FINAL_DECISION_GO as NEXT_ROUTE_FINAL_GO,
    NEXT_PHASE_GO as NEXT_ROUTE_NEXT_PHASE,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_provider_real_dependency_check_dryrun_v1 import (
    FINAL_DECISION_GO as REAL_DEP_DRYRUN_FINAL_GO,
)
from capabilities.governance.ocr_provider_real_dependency_check_planning_v1 import (
    FINAL_DECISION_GO as REAL_DEP_PLANNING_FINAL_GO,
    ROLLBACK_RULES,
)
from capabilities.governance.ocr_provider_real_dependency_check_post_dryrun_review_v1 import (
    FINAL_DECISION_GO as REAL_DEP_POST_FINAL_GO,
)

PHASE_ID = "Phase-OCR-Provider-Real-Dependency-Check-Authorization-Planning-v1-001"
SCOPE = "ocr_provider_real_dependency_check_authorization_planning_only"
SOURCE_CHAIN = "ocr_provider_real_dependency_check_authorization_planning_v1"

UPSTREAM_NEXT_ROUTE_FINAL = NEXT_ROUTE_FINAL_GO
UPSTREAM_NEXT_ROUTE_NEXT = NEXT_ROUTE_NEXT_PHASE

FINAL_DECISION_GO = (
    "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_PROVIDER_REAL_DEPENDENCY_CHECK_AUTHORIZATION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Provider-Real-Dependency-Check-Authorization-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Provider-Real-Dependency-Check-Authorization-Issue-Review-v1-001"

CURRENT_STATE = "planning_defined"
REQUEST_TYPE = "ocr_real_dependency_check_authorization_request"
TARGET_SCOPE = "real_dependency_check"
GRANT_SCOPE = "real_dependency_check_only"

AUTHORIZATION_SCOPE_IN: Tuple[str, ...] = (
    "python package presence check",
    "model cache path check",
    "model file existence check",
    "model file hash check",
    "provider import check",
    "provider initialization dry check later",
    "runtime smoke check later",
    "sample OCR check later",
)

AUTHORIZATION_SCOPE_OUT: Tuple[str, ...] = (
    "provider selection finalize",
    "controlled trial",
    "production runtime",
    "OCRRequest submission",
    "user-facing OCR output",
    "OCR fact write",
    "Memory / WorldModel write",
)

ALLOWED_ACTIONS_LATER: Tuple[str, ...] = (
    "package_presence_check",
    "model_cache_path_check",
    "model_file_existence_check",
    "model_file_hash_check",
    "provider_import_check",
    "provider_initialization_dry_check_later",
    "runtime_smoke_check_later",
    "sample_ocr_check_later",
)

FORBIDDEN_ACTIONS: Tuple[str, ...] = (
    "pip install",
    "dependency auto-install",
    "model download",
    "cache mutation without approval",
    "provider runtime invocation",
    "OCRRequest submit",
    "image read",
    "crop",
    "OCR fact generation",
    "user output",
    "Memory / WorldModel write",
    "provider selection finalize",
    "controlled trial start",
)

EVIDENCE_REQUIREMENTS: Tuple[str, ...] = (
    "authorization_request",
    "authorization_grant",
    "execution_window",
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

LIFECYCLE_STATES: Tuple[str, ...] = (
    "planning_defined",
    "request_candidate_ready_later",
    "request_generated_later",
    "request_sent_later",
    "grant_pending_later",
    "grant_issued_later",
    "execution_window_opened_later",
    "real_dependency_check_executed_later",
    "post_execution_review_required",
    "closed",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_request_generation",
    "planning_to_request_send",
    "planning_to_grant_issue",
    "planning_to_execution_window_open",
    "planning_to_real_dependency_check",
    "planning_to_package_check",
    "planning_to_provider_import",
    "planning_to_dependency_install",
    "planning_to_model_download",
    "planning_to_model_cache_mutation",
    "planning_to_provider_smoke",
    "planning_to_sample_ocr",
    "planning_to_provider_selection_finalize",
    "planning_to_controlled_trial",
    "planning_to_ocr_request_submit",
    "planning_to_image_read",
    "planning_to_ocr_fact",
    "planning_to_user_output",
    "planning_to_memory_write",
    "planning_to_world_model_write",
)

ROLLBACK_POLICIES: Tuple[str, ...] = (
    "failed package check does not trigger install",
    "failed import does not trigger repair",
    "missing model file does not trigger download",
    "hash mismatch does not trigger cache mutation",
    "smoke failure does not trigger provider switch",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Authorization Planning GO ≠ real dependency check authorized",
    "Authorization Planning GO ≠ real dependency check executed",
    "request contract defined ≠ request generated",
    "grant contract defined ≠ grant issued",
    "allowed action matrix ≠ checks executed now",
    "DryRunAndReview next ≠ provider import allowed",
    "real dependency check authorization ≠ provider selected",
    "evidence requirement defined ≠ evidence collected now",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "real_dependency_check_authorization_request_generated_now",
    "real_dependency_check_authorization_request_sent_now",
    "real_dependency_check_authorization_granted_now",
    "real_dependency_execution_window_opened_now",
    "real_dependency_check_executed_now",
    "python_package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_path_check_executed_now",
    "model_file_existence_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_smoke_check_executed_now",
    "sample_ocr_executed_now",
    "provider_selection_finalized_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
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
    "ocr_provider_real_dependency_check_authorization_planning"
)

_EVAL_OUT = "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out"


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_provider_real_dependency_check_authorization_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
        "current_state": CURRENT_STATE,
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


def _allowed_action_row(action_id: str) -> Dict[str, Any]:
    return {
        "action_id": action_id,
        "future_allowed_later": True,
        "current_executed_now": False,
        "requires_execution_window": True,
        "requires_sandbox": True,
        "requires_evidence": True,
        "requires_post_execution_review": True,
    }


def run_ocr_provider_real_dependency_check_authorization_planning_v1(
    *,
    ocr_authorization_next_route_decision_root: str,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_dryrun_root: Optional[str] = None,
    ocr_provider_real_dependency_check_planning_root: Optional[str] = None,
    compressed_ocr_authorization_lifecycle_dryrun_and_review_root: Optional[str] = None,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    route_root = Path(ocr_authorization_next_route_decision_root).expanduser().resolve()
    route_sm = _try_read_json(route_root / "summary.json") or {}
    route_vr = _try_read_json(route_root / "verifier_report.json") or {}
    route_next = _try_read_json(route_root / "next_phase_readiness_decision_v1.json") or {}

    real_dep_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or route_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    real_dep_post_sm = _try_read_json(real_dep_post_root / "summary.json") or {}
    real_dep_post_vr = _try_read_json(real_dep_post_root / "verifier_report.json") or {}
    real_dep_closure = _try_read_json(real_dep_post_root / "real_dependency_check_closure_decision_v1.json") or {}

    real_dep_dryrun_root = Path(
        ocr_provider_real_dependency_check_dryrun_root
        or route_root.parent / "ocr_provider_real_dependency_check_dryrun"
    ).expanduser().resolve()
    real_dep_dryrun_sm = _try_read_json(real_dep_dryrun_root / "summary.json") or {}
    real_dep_dryrun_vr = _try_read_json(real_dep_dryrun_root / "verifier_report.json") or {}

    real_dep_plan_root = Path(
        ocr_provider_real_dependency_check_planning_root
        or route_root.parent / "ocr_provider_real_dependency_check_planning"
    ).expanduser().resolve()
    real_dep_plan_sm = _try_read_json(real_dep_plan_root / "summary.json") or {}
    real_dep_plan_vr = _try_read_json(real_dep_plan_root / "verifier_report.json") or {}

    lifecycle_dr_root = Path(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        or route_root.parent / "compressed_ocr_authorization_lifecycle_dryrun_and_review"
    ).expanduser().resolve()
    lifecycle_dr_vr = _try_read_json(lifecycle_dr_root / "verifier_report.json") or {}
    lifecycle_closure = _try_read_json(lifecycle_dr_root / "compressed_lifecycle_closure_decision_v1.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or route_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    factory_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or route_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    factory_post_vr = _try_read_json(factory_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_next_route_decision_root": str(route_root),
        "upstream_real_dep_post_root": str(real_dep_post_root),
        "upstream_real_dep_dryrun_root": str(real_dep_dryrun_root),
        "upstream_real_dep_planning_root": str(real_dep_plan_root),
        "upstream_lifecycle_dryrun_review_root": str(lifecycle_dr_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_factory_post_review_root": str(factory_post_root),
        "output_root": str(out_root),
    }

    if route_vr.get("verifier") != "GO" or route_vr.get("passed") is not True:
        blockers.append("next route decision verifier must be GO")
    if route_sm.get("final_decision") != UPSTREAM_NEXT_ROUTE_FINAL:
        blockers.append("next route final_decision mismatch")
    if route_sm.get("recommended_next_phase") != UPSTREAM_NEXT_ROUTE_NEXT:
        blockers.append("next route recommended_next_phase mismatch")
    if route_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("selected_route must be Route A")
    if route_next.get("ready_for_real_dependency_check_authorization_planning") is not True:
        blockers.append("next route must be ready for authorization planning")

    if real_dep_post_vr.get("verifier") != "GO":
        blockers.append("real dependency check post-review must be GO")
    if real_dep_post_sm.get("final_decision") != REAL_DEP_POST_FINAL_GO:
        blockers.append("real dep post-review final_decision mismatch")
    if real_dep_post_sm.get("real_dependency_check_flow_trusted") is not True:
        blockers.append("real_dependency_check_flow_trusted must be true")
    if real_dep_closure.get("evidence_package_candidate_trusted") is not True:
        blockers.append("evidence_package_candidate_trusted must be true")
    if real_dep_post_sm.get("real_dependency_check_executed_now") is True:
        blockers.append("real_dependency_check_executed_now must be false")

    if real_dep_dryrun_vr.get("verifier") != "GO":
        blockers.append("real dependency check dryrun must be GO")
    if real_dep_dryrun_sm.get("final_decision") != REAL_DEP_DRYRUN_FINAL_GO:
        blockers.append("real dep dryrun final_decision mismatch")

    if real_dep_plan_vr.get("verifier") != "GO":
        blockers.append("real dependency check planning must be GO")
    if real_dep_plan_sm.get("final_decision") != REAL_DEP_PLANNING_FINAL_GO:
        blockers.append("real dep planning final_decision mismatch")

    if lifecycle_dr_vr.get("verifier") != "GO":
        blockers.append("compressed lifecycle dryrun review must be GO")
    if lifecycle_closure.get("closure_pass") is not True:
        blockers.append("compressed lifecycle must be closed")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")
    if factory_post_vr.get("verifier") != "GO":
        blockers.append("harness factory registration must be GO")

    if meta.get("selected_provider_for_execution") is not None:
        blockers.append("selected_provider_for_execution must be null")
    if meta.get("provider_selection_finalized_now") is True:
        blockers.append("provider_selection_finalized_now must be false")

    for field in BOUNDARY_FALSE:
        if route_sm.get(field) is True or real_dep_post_sm.get(field) is True or real_dep_dryrun_sm.get(field) is True:
            blockers.append(f"{field} must be false upstream")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    route_input_review = {
        "review_id": "ocr_authorization_next_route_input_review_v1",
        "upstream_root": str(route_root),
        "upstream_verifier_go": route_vr.get("verifier") == "GO",
        "selected_route": route_sm.get("selected_route"),
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    auth_scope = {
        "scope_id": "real_dependency_check_authorization_scope_v1",
        "in_scope": list(AUTHORIZATION_SCOPE_IN),
        "out_of_scope": list(AUTHORIZATION_SCOPE_OUT),
        "target_scope": TARGET_SCOPE,
        **meta,
    }

    allowed_matrix = {
        "matrix_id": "allowed_dependency_check_action_matrix_v1",
        "actions": [_allowed_action_row(a) for a in ALLOWED_ACTIONS_LATER],
        "action_count": len(ALLOWED_ACTIONS_LATER),
        "all_executed_now_false": True,
        **meta,
    }

    forbidden_matrix = {
        "matrix_id": "forbidden_dependency_check_action_matrix_v1",
        "forbidden_actions": [
            {"action_id": a, "status": "forbidden", "executed_now": False} for a in FORBIDDEN_ACTIONS
        ],
        "action_count": len(FORBIDDEN_ACTIONS),
        **meta,
    }

    request_contract = {
        "contract_id": "real_dependency_check_authorization_request_contract_v1",
        "request_type": REQUEST_TYPE,
        "target_scope": TARGET_SCOPE,
        "provider_candidate_refs": "planned_candidate_refs_only",
        "allowed_check_matrix_ref": "allowed_dependency_check_action_matrix_v1",
        "forbidden_action_matrix_ref": "forbidden_dependency_check_action_matrix_v1",
        "execution_window_required": True,
        "sandbox_required": True,
        "rollback_required": True,
        "evidence_package_required": True,
        "verifier_required": True,
        "post_execution_review_required": True,
        "owner_operator_approval_required": True,
        "request_generated_now": False,
        "request_sent_now": False,
        **meta,
    }

    grant_contract = {
        "contract_id": "real_dependency_check_grant_contract_v1",
        "grant_scope": GRANT_SCOPE,
        "allowed_actions_later": list(ALLOWED_ACTIONS_LATER),
        "prohibited_actions": list(FORBIDDEN_ACTIONS),
        "expiration_or_ttl": "execution_window_bound",
        "revocation_conditions": "boundary_violation_or_verifier_no_go",
        "no_provider_selection_finalize": True,
        "no_controlled_trial": True,
        "no_production_runtime": True,
        "grant_issued_now": False,
        **meta,
    }

    execution_window = {
        "contract_id": "real_dependency_check_execution_window_contract_v1",
        "allowed_workspace_path": f"{_EVAL_OUT}/ocr_provider_real_dependency_check_dryrun/",
        "allowed_output_path": f"{_EVAL_OUT}/ocr_provider_real_dependency_check_dryrun/",
        "forbidden_paths": [
            "production_paths",
            "memory_world_model",
            "user_output_channels",
            "global_cache_mutation",
        ],
        "max_check_scope": TARGET_SCOPE,
        "timeout_limit": "execution_window_bound",
        "no_production_write": True,
        "no_network_by_default": True,
        "no_install": True,
        "no_download": True,
        "current_window_opened_now": False,
        **meta,
    }

    sandbox_boundary = {
        "plan_id": "real_dependency_check_sandbox_boundary_plan_v1",
        "sandbox_required": True,
        "no_production_path_write": True,
        "no_global_environment_modification": True,
        "evidence_only_output": True,
        **meta,
    }

    evidence_requirement = {
        "requirement_id": "real_dependency_check_evidence_requirement_v1",
        "required_on_future_execution": list(EVIDENCE_REQUIREMENTS),
        "field_count": len(EVIDENCE_REQUIREMENTS),
        **meta,
    }

    rollback_policy = {
        "policy_id": "real_dependency_check_rollback_policy_v1",
        "policies": list(ROLLBACK_POLICIES),
        "factory_rollback_rules": list(ROLLBACK_RULES),
        "rollback_plan_ready_later": True,
        "rollback_executed_now": False,
        **meta,
    }

    approval_policy = {
        "policy_id": "owner_operator_approval_policy_v1",
        "owner_operator_approval_required": True,
        "approval_collected_now": False,
        "approval_required_before_grant": True,
        **meta,
    }

    provider_binding = {
        "binding_id": "provider_selection_non_finalize_binding_v1",
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        "real_dep_authorization_not_provider_selection": True,
        "real_dep_evidence_may_inform_finalize_later": True,
        "current_phase_cannot_finalize_provider": True,
        **meta,
    }

    state_machine = {
        "machine_id": "real_dependency_check_authorization_state_machine_v1",
        "states": list(LIFECYCLE_STATES),
        "current_state": CURRENT_STATE,
        "transitions": [
            {"from": "planning_defined", "to": "request_candidate_ready_later", "requires_future_phase": True},
            {"from": "request_candidate_ready_later", "to": "request_generated_later", "requires_future_phase": True},
            {"from": "request_generated_later", "to": "request_sent_later", "requires_future_phase": True},
            {"from": "request_sent_later", "to": "grant_pending_later", "requires_future_phase": True},
            {"from": "grant_pending_later", "to": "grant_issued_later", "requires_future_phase": True},
            {"from": "grant_issued_later", "to": "execution_window_opened_later", "requires_future_phase": True},
            {
                "from": "execution_window_opened_later",
                "to": "real_dependency_check_executed_later",
                "requires_future_phase": True,
            },
            {
                "from": "real_dependency_check_executed_later",
                "to": "post_execution_review_required",
                "requires_future_phase": True,
            },
            {"from": "post_execution_review_required", "to": "closed", "requires_future_phase": True},
        ],
        **meta,
    }

    blocked_matrix = {
        "matrix_id": "real_dependency_check_authorization_blocked_path_matrix_v1",
        "blocked_paths": [
            {"path_id": p, "status": "blocked", "executed_now": False} for p in BLOCKED_PATHS
        ],
        "path_count": len(BLOCKED_PATHS),
        "all_blocked": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "real_dependency_check_authorization_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "objectives": [
            "generate real_dependency_check_authorization_request_candidate",
            "generate grant_candidate",
            "generate execution_window_candidate",
            "generate allowed/forbidden action matrix candidate",
            "verify all real check actions remain blocked",
            "no formal request generation",
            "no request send",
            "no grant",
            "no package/import/hash/smoke/sample OCR execution",
        ],
        "real_dependency_check_authorization_request_generated_now": False,
        "real_dependency_check_authorization_granted_now": False,
        "real_dependency_check_executed_now": False,
        **meta,
    }

    planning_decision = {
        "decision_id": "real_dependency_check_authorization_planning_decision_v1",
        "planning_pass": boundary_ok,
        "current_state": CURRENT_STATE,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "real_dependency_check_authorization_planning_policy_v1",
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
        "current_state": CURRENT_STATE,
        "selected_route": SELECTED_ROUTE,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "real_dependency_check_authorization_planning_policy": policy,
        "ocr_authorization_next_route_input_review": route_input_review,
        "real_dependency_check_authorization_scope": auth_scope,
        "real_dependency_check_authorization_request_contract": request_contract,
        "real_dependency_check_grant_contract": grant_contract,
        "real_dependency_check_execution_window_contract": execution_window,
        "allowed_dependency_check_action_matrix": allowed_matrix,
        "forbidden_dependency_check_action_matrix": forbidden_matrix,
        "real_dependency_check_sandbox_boundary_plan": sandbox_boundary,
        "real_dependency_check_evidence_requirement": evidence_requirement,
        "real_dependency_check_rollback_policy": rollback_policy,
        "owner_operator_approval_policy": approval_policy,
        "provider_selection_non_finalize_binding": provider_binding,
        "real_dependency_check_authorization_state_machine": state_machine,
        "real_dependency_check_authorization_blocked_path_matrix": blocked_matrix,
        "real_dependency_check_authorization_dryrun_plan": dryrun_plan,
        "real_dependency_check_authorization_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
