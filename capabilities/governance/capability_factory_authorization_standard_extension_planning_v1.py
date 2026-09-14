# -*- coding: utf-8 -*-
"""Capability Factory Authorization Standard Extension Planning v1 — 10th factory standard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FACTORY_DR_FINAL_GO,
)
from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    MERGEABLE_OCR_AUTHORIZATION_PHASES,
    STANDARD_ID,
    STANDALONE_AUTHORIZATION_PHASES,
)
from capabilities.governance.compressed_ocr_authorization_lifecycle_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as LIFECYCLE_DR_FINAL_GO,
)
from capabilities.governance.factory_standard_historical_redundancy_cleanup_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CLEANUP_DR_FINAL_GO,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_authorization_next_route_decision_v1 import (
    FINAL_DECISION_GO as NEXT_ROUTE_FINAL_GO,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_planning_v1 import (
    ALLOWED_ACTIONS_LATER as OCR_REAL_DEP_ALLOWED,
    AUTHORIZATION_SCOPE_IN as OCR_REAL_DEP_SCOPE_IN,
    AUTHORIZATION_SCOPE_OUT as OCR_REAL_DEP_SCOPE_OUT,
    FINAL_DECISION_GO as OCR_AUTH_PLANNING_FINAL_GO,
    FORBIDDEN_ACTIONS as OCR_REAL_DEP_FORBIDDEN,
)

PHASE_ID = "Phase-Capability-Factory-Authorization-Standard-Extension-Planning-v1-001"
SCOPE = "capability_factory_authorization_standard_extension_planning_only"
SOURCE_CHAIN = "capability_factory_authorization_standard_extension_planning_v1"

AUTHORIZATION_STANDARD_ID = "authorization_standard_v1"
EXTENDED_STANDARD_ID = "capability_factory_admission_and_operation_standard_v1_with_authorization"

FINAL_DECISION_GO = (
    "CAPABILITY_FACTORY_AUTHORIZATION_STANDARD_EXTENSION_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "CAPABILITY_FACTORY_AUTHORIZATION_STANDARD_EXTENSION_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-Capability-Factory-Authorization-Standard-Extension-DryRunAndReview-v1-001"
NEXT_PHASE_HOLD = "Phase-Capability-Factory-Authorization-Standard-Issue-Review-v1-001"
NEXT_OCR_PHASE_AFTER_EXTENSION = (
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-Planning-v1-001"
)

NINE_STANDARDS: Tuple[str, ...] = (
    "Candidate Standard",
    "Artifact Standard",
    "Lifecycle Standard",
    "Boundary Standard",
    "Evidence Standard",
    "Approval/Grant Standard",
    "Sandbox/Rollback Standard",
    "Provider/Machine Standard",
    "Transfer Standard",
)

TEN_STANDARDS: Tuple[str, ...] = (*NINE_STANDARDS, "Authorization Standard")

AUTHORIZATION_SUBCOMPONENTS: Tuple[str, ...] = (
    "Authorization Scope",
    "Request Contract",
    "Grant Contract",
    "Execution Window Contract",
    "Allowed / Forbidden Action Matrix",
    "Owner / Operator Approval",
    "Post-Execution Review",
    "Revocation / Rollback",
)

FACTORY_AUTH_RESPONSIBILITIES: Tuple[str, ...] = (
    "what requires authorization",
    "evidence required before authorization",
    "request / grant / execution window relationship",
    "actions planning and dryrun must never auto-trigger",
    "post-execution review",
    "failure rollback",
)

PLANNING_DRYRUN_NEVER_AUTO_TRIGGER: Tuple[str, ...] = (
    "request_generation",
    "request_send",
    "grant_issue",
    "execution_window_open",
    "real_dependency_check",
    "provider_import",
    "dependency_install",
    "model_download",
    "provider_invoke",
    "controlled_trial_start",
    "provider_selection_finalize",
)

ABSORPTION_SOURCES: Tuple[str, ...] = (
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-Planning-v1-001",
    "compressed_ocr_authorization_lifecycle_planning",
    "approval_grant_standard_v1",
    "sandbox_rollback_standard_v1",
    "boundary_standard_v1",
    "evidence_standard_v1",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Authorization Standard extension planning GO ≠ authorization runtime enforced",
    "standard defined ≠ request generated",
    "standard defined ≠ grant issued",
    "OCR domain_config template ≠ real dependency check executed",
    "absorption inventory ≠ historical OCR auth planning deleted",
    "ten standards planned ≠ Midplatform consumption",
    "Extension DryRunAndReview next ≠ provider import allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "authorization_standard_runtime_enforced_now",
    "authorization_request_generated_now",
    "authorization_request_sent_now",
    "authorization_grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_selection_finalized_now",
    "controlled_trial_started_now",
    "ocr_request_submitted_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "capability_factory_authorization_standard_extension_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": STANDARD_ID,
        "authorization_standard_id": AUTHORIZATION_STANDARD_ID,
        "extended_standard_id": EXTENDED_STANDARD_ID,
        "ten_standard_count": len(TEN_STANDARDS),
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


def run_capability_factory_authorization_standard_extension_planning_v1(
    *,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: str,
    compressed_ocr_authorization_lifecycle_dryrun_and_review_root: Optional[str] = None,
    factory_standard_historical_redundancy_cleanup_dryrun_and_review_root: Optional[str] = None,
    ocr_authorization_next_route_decision_root: Optional[str] = None,
    ocr_provider_real_dependency_check_authorization_planning_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
    ).expanduser().resolve()
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}

    lifecycle_dr_root = Path(
        compressed_ocr_authorization_lifecycle_dryrun_and_review_root
        or factory_dr_root.parent / "compressed_ocr_authorization_lifecycle_dryrun_and_review"
    ).expanduser().resolve()
    lifecycle_dr_vr = _try_read_json(lifecycle_dr_root / "verifier_report.json") or {}
    lifecycle_closure = _try_read_json(lifecycle_dr_root / "compressed_lifecycle_closure_decision_v1.json") or {}

    cleanup_dr_root = Path(
        factory_standard_historical_redundancy_cleanup_dryrun_and_review_root
        or factory_dr_root.parent / "factory_standard_historical_redundancy_cleanup_dryrun_and_review"
    ).expanduser().resolve()
    cleanup_dr_vr = _try_read_json(cleanup_dr_root / "verifier_report.json") or {}

    route_root = Path(
        ocr_authorization_next_route_decision_root
        or factory_dr_root.parent / "ocr_authorization_next_route_decision"
    ).expanduser().resolve()
    route_sm = _try_read_json(route_root / "summary.json") or {}
    route_vr = _try_read_json(route_root / "verifier_report.json") or {}

    ocr_auth_plan_root = Path(
        ocr_provider_real_dependency_check_authorization_planning_root
        or factory_dr_root.parent / "ocr_provider_real_dependency_check_authorization_planning"
    ).expanduser().resolve()
    ocr_auth_plan_sm = _try_read_json(ocr_auth_plan_root / "summary.json") or {}
    ocr_auth_plan_vr = _try_read_json(ocr_auth_plan_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_lifecycle_dryrun_review_root": str(lifecycle_dr_root),
        "upstream_cleanup_dryrun_review_root": str(cleanup_dr_root),
        "upstream_next_route_decision_root": str(route_root),
        "upstream_ocr_auth_planning_root": str(ocr_auth_plan_root),
        "output_root": str(out_root),
    }

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")
    if factory_dr_sm.get("final_decision") != FACTORY_DR_FINAL_GO:
        blockers.append("factory dryrun final_decision mismatch")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must be true")

    if lifecycle_dr_vr.get("verifier") != "GO":
        blockers.append("compressed lifecycle dryrun review must be GO")
    if lifecycle_closure.get("closure_pass") is not True:
        blockers.append("compressed lifecycle must be closed")

    if cleanup_dr_vr.get("verifier") != "GO":
        blockers.append("cleanup dryrun review must be GO")

    if route_vr.get("verifier") != "GO":
        blockers.append("next route decision must be GO")
    if route_sm.get("final_decision") != NEXT_ROUTE_FINAL_GO:
        blockers.append("next route final_decision mismatch")
    if route_sm.get("selected_route") != SELECTED_ROUTE:
        blockers.append("Route A must remain selected intent")

    if ocr_auth_plan_vr.get("verifier") != "GO":
        blockers.append("ocr auth planning must exist as absorption source")
    if ocr_auth_plan_sm.get("final_decision") != OCR_AUTH_PLANNING_FINAL_GO:
        blockers.append("ocr auth planning final_decision mismatch")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    upstream_review = {
        "review_id": "factory_standard_upstream_input_review_v1",
        "factory_dryrun_go": factory_dr_vr.get("verifier") == "GO",
        "lifecycle_closed": lifecycle_closure.get("closure_pass") is True,
        "cleanup_go": cleanup_dr_vr.get("verifier") == "GO",
        "next_route_go": route_vr.get("verifier") == "GO",
        "ocr_auth_planning_go": ocr_auth_plan_vr.get("verifier") == "GO",
        "review_pass": planning_ok,
        "blockers": blockers,
        **meta,
    }

    contract_outline = {
        "outline_id": "authorization_standard_contract_outline_v1",
        "standard_name": "Factory Authorization Standard",
        "standard_alias": "Authorization Standard",
        "parent_standard": STANDARD_ID,
        "standard_id": AUTHORIZATION_STANDARD_ID,
        "responsibilities": list(FACTORY_AUTH_RESPONSIBILITIES),
        "subcomponents": list(AUTHORIZATION_SUBCOMPONENTS),
        "references_not_duplicates": [
            "Approval/Grant Standard",
            "Sandbox/Rollback Standard",
            "Boundary Standard",
            "Evidence Standard",
        ],
        **meta,
    }

    scope_plan = {
        "plan_id": "authorization_scope_standard_plan_v1",
        "defines": "what requires authorization vs out_of_scope",
        "domain_config_required": True,
        "standalone_authorization_targets": list(STANDALONE_AUTHORIZATION_PHASES),
        **meta,
    }

    request_contract_plan = {
        "plan_id": "authorization_request_contract_standard_plan_v1",
        "required_fields": [
            "request_type",
            "target_scope",
            "provider_domain",
            "authorization_target",
            "allowed_action_matrix_ref",
            "forbidden_action_matrix_ref",
            "execution_window_required",
            "sandbox_required",
            "rollback_required",
            "evidence_package_required",
            "verifier_required",
            "post_execution_review_required",
            "owner_operator_approval_required",
        ],
        "request_generated_now": False,
        "request_sent_now": False,
        **meta,
    }

    grant_contract_plan = {
        "plan_id": "authorization_grant_contract_standard_plan_v1",
        "grant_scope_pattern": "{authorization_target}_only",
        "required_fields": [
            "allowed_actions_later",
            "prohibited_actions",
            "expiration_or_ttl",
            "revocation_conditions",
        ],
        "grant_issued_now": False,
        **meta,
    }

    window_contract_plan = {
        "plan_id": "authorization_execution_window_contract_standard_plan_v1",
        "required_fields": [
            "allowed_workspace_path",
            "allowed_output_path",
            "forbidden_paths",
            "max_check_scope",
            "timeout_limit",
            "no_production_write",
            "no_network_by_default",
            "no_install",
            "no_download",
        ],
        "current_window_opened_now": False,
        **meta,
    }

    action_matrix_plan = {
        "plan_id": "authorization_action_matrix_standard_plan_v1",
        "allowed_action_fields": [
            "future_allowed_later",
            "current_executed_now",
            "requires_execution_window",
            "requires_sandbox",
            "requires_evidence",
            "requires_post_execution_review",
        ],
        "forbidden_action_default": "forbidden",
        "planning_dryrun_never_auto_trigger": list(PLANNING_DRYRUN_NEVER_AUTO_TRIGGER),
        **meta,
    }

    approval_plan = {
        "plan_id": "authorization_owner_operator_approval_standard_plan_v1",
        "owner_operator_approval_required": True,
        "approval_collected_now": False,
        "approval_before_grant": True,
        **meta,
    }

    post_review_plan = {
        "plan_id": "authorization_post_execution_review_standard_plan_v1",
        "post_execution_review_required": True,
        "closure_decision_required": True,
        "evidence_package_required": True,
        **meta,
    }

    revocation_rollback_plan = {
        "plan_id": "authorization_revocation_rollback_standard_plan_v1",
        "revocation_on_boundary_violation": True,
        "revocation_on_verifier_no_go": True,
        "failed_check_no_auto_repair": True,
        "rollback_plan_ready_before_execution": True,
        "rollback_executed_now": False,
        **meta,
    }

    absorption_inventory = {
        "inventory_id": "authorization_standard_absorption_inventory_v1",
        "sources": list(ABSORPTION_SOURCES),
        "ocr_auth_planning_superseded_for_auth_logic": True,
        "ocr_auth_planning_preserved_as_evidence": True,
        "mergeable_triple_chain_phases": list(MERGEABLE_OCR_AUTHORIZATION_PHASES),
        "absorbed_rule_categories": [
            "request_contract",
            "grant_contract",
            "execution_window_contract",
            "allowed_forbidden_matrix",
            "approval_policy",
            "rollback_policy",
            "evidence_requirement",
            "blocked_paths",
        ],
        **meta,
    }

    ocr_domain_template = {
        "template_id": "ocr_real_dependency_check_domain_config_template_v1",
        "references": AUTHORIZATION_STANDARD_ID,
        "provider_domain": "ocr",
        "authorization_target": "real_dependency_check",
        "allowed_checks": [
            "package_presence_check",
            "model_cache_path_check",
            "model_file_existence_check",
            "model_file_hash_check",
            "provider_import_check",
        ],
        "allowed_checks_later": [
            "provider_initialization_dry_check_later",
            "runtime_smoke_check_later",
            "sample_ocr_check_later",
        ],
        "forbidden_actions": [
            "install",
            "download",
            "provider_invoke",
            "OCRRequest_submit",
            "image_read",
            "fact_write",
            "user_output",
            "provider_selection_finalize",
            "controlled_trial_start",
        ],
        "scope_in_from_ocr_planning": list(OCR_REAL_DEP_SCOPE_IN),
        "scope_out_from_ocr_planning": list(OCR_REAL_DEP_SCOPE_OUT),
        "note": "OCR phases must only supply domain_config — not redefine authorization logic",
        **meta,
    }

    ten_standards_outline = {
        "outline_id": "ten_standards_contract_outline_v1",
        "prior_nine_standards": list(NINE_STANDARDS),
        "tenth_standard": "Authorization Standard",
        "ten_standards": list(TEN_STANDARDS),
        "authorization_standard_subcomponents": list(AUTHORIZATION_SUBCOMPONENTS),
        **meta,
    }

    route_adjustment = {
        "decision_id": "route_adjustment_decision_v1",
        "prior_ocr_phase": "Phase-OCR-Provider-Real-Dependency-Check-Authorization-Planning-v1-001",
        "prior_ocr_dryrun_phase_deferred": (
            "Phase-OCR-Provider-Real-Dependency-Check-Authorization-DryRunAndReview-v1-001"
        ),
        "superseded_for_auth_logic_by": AUTHORIZATION_STANDARD_ID,
        "preserved_as_evidence": True,
        "physical_delete": False,
        "next_ocr_phase_after_extension": NEXT_OCR_PHASE_AFTER_EXTENSION,
        "ocr_consumes_factory_standard_plus_domain_config": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "authorization_standard_extension_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "objectives": [
            "validate Authorization Standard as 10th factory standard",
            "simulate domain_config binding for OCR real_dependency_check",
            "verify planning/dryrun never auto-triggers authorization actions",
            "verify absorption from OCR auth planning without deleting evidence",
        ],
        **meta,
    }

    planning_decision = {
        "decision_id": "authorization_standard_extension_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ten_standards_defined": boundary_ok,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        "next_ocr_phase_after_extension": NEXT_OCR_PHASE_AFTER_EXTENSION,
        **meta,
    }

    policy = {
        "policy_id": "factory_authorization_standard_extension_planning_policy_v1",
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
        "ten_standard_count": len(TEN_STANDARDS),
        "authorization_subcomponent_count": len(AUTHORIZATION_SUBCOMPONENTS),
        "route_adjustment_applied": True,
        "next_ocr_phase_after_extension": NEXT_OCR_PHASE_AFTER_EXTENSION,
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "factory_authorization_standard_extension_planning_policy": policy,
        "factory_standard_upstream_input_review": upstream_review,
        "authorization_standard_contract_outline": contract_outline,
        "authorization_scope_standard_plan": scope_plan,
        "authorization_request_contract_standard_plan": request_contract_plan,
        "authorization_grant_contract_standard_plan": grant_contract_plan,
        "authorization_execution_window_contract_standard_plan": window_contract_plan,
        "authorization_action_matrix_standard_plan": action_matrix_plan,
        "authorization_owner_operator_approval_standard_plan": approval_plan,
        "authorization_post_execution_review_standard_plan": post_review_plan,
        "authorization_revocation_rollback_standard_plan": revocation_rollback_plan,
        "authorization_standard_absorption_inventory": absorption_inventory,
        "ocr_real_dependency_check_domain_config_template": ocr_domain_template,
        "ten_standards_contract_outline": ten_standards_outline,
        "route_adjustment_decision": route_adjustment,
        "authorization_standard_extension_dryrun_plan": dryrun_plan,
        "authorization_standard_extension_planning_decision": planning_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
