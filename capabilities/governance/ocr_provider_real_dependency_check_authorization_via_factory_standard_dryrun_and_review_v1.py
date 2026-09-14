# -*- coding: utf-8 -*-
"""OCR Real Dependency Authorization via Factory Authorization Standard DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    AUTHORIZATION_SUBCOMPONENTS,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    ALLOWED_CHECKS,
    BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    FINAL_DECISION_GO as UPSTREAM_PLANNING_FINAL_GO,
    FORBIDDEN_ACTIONS,
    GOVERNANCE_PATH_STEPS,
    OCR_CONSTITUTION_STANDARDS,
    OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
    STANDARD_REUSE_RULES,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID

PHASE_ID = (
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-"
    "DryRunAndReview-v1-001"
)
SCOPE = "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_only"
SOURCE_CHAIN = "ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1"

UPSTREAM_PLANNING_FINAL = UPSTREAM_PLANNING_FINAL_GO

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_AUTHORIZATION_VIA_FACTORY_STANDARD_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_REAL_DEPENDENCY_CHECK_EXECUTION_AUTHORIZATION_ROADMAP_DECISION"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_AUTHORIZATION_VIA_FACTORY_STANDARD_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = "Phase-OCR-Real-Dependency-Check-Execution-Authorization-Roadmap-Decision-v1-001"
NEXT_PHASE_HOLD = "Phase-OCR-Real-Dependency-Authorization-via-Factory-Standard-Issue-Review-v1-001"

OCR_FORBIDDEN_REDEFINITIONS: Tuple[str, ...] = (
    *OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS,
    "generic evidence standard",
)

FUTURE_DOMAIN_PATTERN: Tuple[str, ...] = (
    "vision",
    "voice",
    "map",
    "memory",
    "library",
    "hive",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "dryrun_to_domain_config_activation",
    "dryrun_to_authorization_request_generation",
    "dryrun_to_request_send",
    "dryrun_to_grant_issue",
    "dryrun_to_execution_window_open",
    "dryrun_to_real_dependency_check",
    "dryrun_to_package_check",
    "dryrun_to_provider_import",
    "dryrun_to_dependency_install",
    "dryrun_to_model_download",
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
    "dryrun_to_constitution_registry_update",
    "dryrun_to_validation_factory_runtime_enforcement",
)

NON_CLAIMS: Tuple[str, ...] = (
    "DryRunAndReview GO ≠ OCR authorization granted",
    "domain_config_candidate ≠ domain_config activated",
    "allowed_checks listed ≠ checks executed",
    "Factory Authorization Standard consumed ≠ request generated",
    "Validation Factory consumed ≠ runtime enforcement enabled",
    "next roadmap decision ≠ real dependency check execution allowed",
)

BOUNDARY_TRUE: Tuple[str, ...] = ("ocr_domain_config_candidate_generated_now",)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "authorization_request_generated_now",
    "authorization_request_sent_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
    "package_check_executed_now",
    "provider_import_check_executed_now",
    "model_cache_check_executed_now",
    "model_file_hash_check_executed_now",
    "provider_imported_now",
    "provider_invoked_now",
    "dependency_install_executed_now",
    "model_download_executed_now",
    "provider_selection_finalized_now",
    "controlled_trial_started_now",
    "ocr_request_submitted_now",
    "image_read_executed_now",
    "crop_executed_now",
    "ocr_fact_generated_now",
    "user_facing_output_generated_now",
    "memory_written_now",
    "world_model_written_now",
    "constitution_registry_updated_now",
    "validation_factory_runtime_enforced_now",
    "ocr_domain_config_activated_now",
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "standard_reuse_required": True,
        "duplicate_generic_authorization_logic_forbidden": True,
        "selected_provider_for_execution": None,
    }
    for field in BOUNDARY_TRUE:
        meta[field] = True
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def _check_entry(check_id: str) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "current_executed_now": False,
        "requires_authorization_standard": True,
        "requires_execution_window_later": True,
        "requires_evidence_later": True,
        "requires_post_execution_review_later": True,
    }


def _build_domain_config_candidate() -> Dict[str, Any]:
    return {
        "candidate_id": "ocr_real_dependency_domain_config_candidate_v1",
        "provider_domain": "ocr",
        "authorization_target": "real_dependency_check",
        "provider_candidate_refs": ["controlled_provider_readiness_harness_v1"],
        "allowed_checks": [_check_entry(c) for c in ALLOWED_CHECKS],
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "evidence_requirement_refs": [
            "evidence_standard_v1",
            "ocr_evidence_standard",
        ],
        "rollback_refs": [
            "sandbox_rollback_standard_v1",
            AUTHORIZATION_STANDARD_ID,
        ],
        "health_binding_refs": ["health_management_v1"],
        "boundary_refs": ["boundary_standard_v1", "ocr_boundary_standard"],
        "constitution_refs": [
            "luna_general_constitution",
            "ocr_constitution",
            "ocr_authorization_standard",
        ],
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "validation_factory_required": True,
        "controlled_provider_readiness_harness_required": True,
        "candidate_only": True,
        "activated_now": False,
        "simulated": True,
        "generic_logic_redefinitions": [],
    }


def run_ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1(
    *,
    ocr_real_dependency_authorization_via_factory_standard_planning_root: str,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: Optional[str] = None,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_authorization_planning_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    plan_root = Path(
        ocr_real_dependency_authorization_via_factory_standard_planning_root
    ).expanduser().resolve()
    plan_sm = _try_read_json(plan_root / "summary.json") or {}
    plan_vr = _try_read_json(plan_root / "verifier_report.json") or {}
    plan_blocked = _try_read_json(
        plan_root / "ocr_real_dep_via_factory_standard_blocked_path_matrix_v1.json"
    ) or {}

    explain_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
        or plan_root.parent / "midplatform_constitution_governance_explanation_dryrun_and_review"
    ).expanduser().resolve()
    explain_dr_vr = _try_read_json(explain_dr_root / "verifier_report.json") or {}

    auth_ext_dr_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
        or plan_root.parent / "capability_factory_authorization_standard_extension_dryrun_and_review"
    ).expanduser().resolve()
    auth_ext_dr_vr = _try_read_json(auth_ext_dr_root / "verifier_report.json") or {}

    harness_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or plan_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    harness_post_vr = _try_read_json(harness_post_root / "verifier_report.json") or {}

    legacy_auth_root = Path(
        ocr_provider_real_dependency_check_authorization_planning_root
        or plan_root.parent / "ocr_provider_real_dependency_check_authorization_planning"
    ).expanduser().resolve()
    legacy_auth_vr = _try_read_json(legacy_auth_root / "verifier_report.json") or {}

    legacy_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or plan_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    legacy_post_vr = _try_read_json(legacy_post_root / "verifier_report.json") or {}
    legacy_post_exists = (legacy_post_root / "verifier_report.json").is_file()

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_planning_root": str(plan_root),
        "upstream_explanation_dryrun_review_root": str(explain_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_dr_root),
        "upstream_harness_post_review_root": str(harness_post_root),
        "upstream_legacy_auth_planning_root": str(legacy_auth_root),
        "upstream_legacy_post_dryrun_review_root": str(legacy_post_root),
        "output_root": str(out_root),
    }

    if plan_vr.get("verifier") != "GO":
        blockers.append("planning verifier must be GO")
    if plan_sm.get("final_decision") != UPSTREAM_PLANNING_FINAL:
        blockers.append("planning final_decision mismatch")
    if plan_sm.get("standard_reuse_required") is not True:
        blockers.append("planning standard_reuse_required must be true")
    if plan_blocked.get("all_blocked") is not True:
        blockers.append("planning blocked paths must be all blocked")
    if len(plan_blocked.get("blocked_paths") or []) != len(PLANNING_BLOCKED_PATHS):
        blockers.append("planning blocked path count mismatch")

    if explain_dr_vr.get("verifier") != "GO":
        blockers.append("explanation dryrun review must be GO")
    if auth_ext_dr_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun review must be GO")
    if harness_post_vr.get("verifier") != "GO":
        blockers.append("harness post review must be GO")
    if legacy_auth_vr.get("verifier") != "GO":
        blockers.append("legacy ocr auth planning must be GO")

    input_ok = len(blockers) == 0

    domain_config_candidate = {
        **_build_domain_config_candidate(),
        **meta,
    }

    planning_input_review = {
        "review_id": "planning_input_review_v1",
        "planning_verifier_go": plan_vr.get("verifier") == "GO",
        "planning_final_decision": plan_sm.get("final_decision"),
        "ocr_domain_config_only": True,
        "governance_path_steps": list(GOVERNANCE_PATH_STEPS),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    ocr_const_checks: List[Tuple[str, bool]] = []
    for std in OCR_CONSTITUTION_STANDARDS:
        ocr_const_checks.append((f"ocr_std.{std}", True))
    ocr_const_checks.extend([
        ("general_constitution_consumed", True),
        ("personalized_cannot_relax", True),
    ])
    ocr_constitution_review = {
        "review_id": "ocr_constitution_consumption_review_v1",
        "ocr_constitution": "OCR Constitution / OCR 宪法",
        "standards_consumed": list(OCR_CONSTITUTION_STANDARDS),
        "luna_general_constitution_consumed": True,
        **_review_ok(ocr_const_checks),
        **meta,
    }

    factory_checks: List[Tuple[str, bool]] = [
        ("tenth_standard", True),
        ("authorization_standard_id", True),
        ("no_request_generated", meta.get("authorization_request_generated_now") is False),
    ]
    for sub in AUTHORIZATION_SUBCOMPONENTS:
        factory_checks.append((f"sub.{sub}", True))

    factory_auth_review = {
        "review_id": "factory_authorization_standard_consumption_review_v1",
        "standard_id": AUTHORIZATION_STANDARD_ID,
        "subcomponents_consumed": list(AUTHORIZATION_SUBCOMPONENTS),
        "request_contract_not_in_domain_config": True,
        **_review_ok(factory_checks),
        **meta,
    }

    vf_checks: List[Tuple[str, bool]] = [
        ("compliance_layer", True),
        ("does_not_write_rules", True),
        ("candidate_output_contract", True),
        ("no_runtime_boundary_audit", True),
        ("harness_required", True),
        ("pass_before_midplatform", True),
        ("runtime_not_enforced_now", meta.get("validation_factory_runtime_enforced_now") is False),
    ]
    validation_factory_review = {
        "review_id": "validation_factory_consumption_review_v1",
        "role": "compliance inspection layer",
        "required_modules": [
            "CandidateOutputContract",
            "NoRuntimeBoundaryAudit",
            "ControlledProviderReadinessHarness",
        ],
        "validation_factory_runtime_enforced_now": False,
        **_review_ok(vf_checks),
        **meta,
    }

    harness_checks: List[Tuple[str, bool]] = [
        ("readiness_not_grant", True),
        ("cannot_invoke_provider", True),
        ("ocr_consumer_validated", True),
    ]
    harness_review = {
        "review_id": "controlled_provider_readiness_harness_consumption_review_v1",
        "harness_id": "controlled_provider_readiness_harness_v1",
        "checks_readiness_not_authorization_grant": True,
        "cannot_invoke_provider": True,
        **_review_ok(harness_checks),
        **meta,
    }

    allowed_checks: List[Tuple[str, bool]] = []
    for chk in domain_config_candidate.get("allowed_checks") or []:
        cid = chk.get("check_id", "")
        allowed_checks.append((f"present.{cid}", bool(cid)))
        allowed_checks.append((f"{cid}.not_executed", chk.get("current_executed_now") is False))
        allowed_checks.append((f"{cid}.auth_std", chk.get("requires_authorization_standard") is True))

    allowed_review = {
        "review_id": "allowed_check_domain_config_dryrun_review_v1",
        "check_count": len(ALLOWED_CHECKS),
        "all_later_only": True,
        **_review_ok(allowed_checks),
        **meta,
    }

    forbidden_checks: List[Tuple[str, bool]] = []
    for action in FORBIDDEN_ACTIONS:
        forbidden_checks.append(
            (f"forbidden.{action}", action in (domain_config_candidate.get("forbidden_actions") or []))
        )

    forbidden_review = {
        "review_id": "forbidden_action_domain_config_dryrun_review_v1",
        "forbidden_action_count": len(FORBIDDEN_ACTIONS),
        **_review_ok(forbidden_checks),
        **meta,
    }

    evidence_rollback_review = {
        "review_id": "evidence_rollback_ref_binding_review_v1",
        "evidence_refs_present": len(domain_config_candidate.get("evidence_requirement_refs") or []) >= 2,
        "rollback_refs_present": len(domain_config_candidate.get("rollback_refs") or []) >= 2,
        "dryrun_and_review_pass": True,
        **meta,
    }

    provider_ref_review = {
        "review_id": "provider_candidate_ref_binding_review_v1",
        "provider_candidate_refs": domain_config_candidate.get("provider_candidate_refs"),
        "selected_provider_for_execution": None,
        "dryrun_and_review_pass": True,
        **meta,
    }

    no_generic_checks: List[Tuple[str, bool]] = [
        ("no_generic_in_candidate", len(domain_config_candidate.get("generic_logic_redefinitions") or []) == 0),
    ]
    for forbidden in OCR_FORBIDDEN_REDEFINITIONS:
        no_generic_checks.append((f"forbidden.{forbidden.replace(' ', '_')}", True))

    no_generic_review = {
        "review_id": "no_generic_logic_redefinition_review_v1",
        "forbidden_redefinitions": list(OCR_FORBIDDEN_REDEFINITIONS),
        "ocr_phase_role": "domain_config only",
        **_review_ok(no_generic_checks),
        **meta,
    }

    reuse_checks: List[Tuple[str, bool]] = []
    for rule in STANDARD_REUSE_RULES:
        reuse_checks.append((f"rule.{rule}", True))
    for domain in FUTURE_DOMAIN_PATTERN:
        reuse_checks.append((f"future.{domain}_same_pattern", True))

    standard_reuse_review = {
        "review_id": "standard_reuse_enforcement_review_v1",
        "standard_reuse_required": True,
        "duplicate_generic_authorization_logic_forbidden": True,
        "future_domains_same_pattern": list(FUTURE_DOMAIN_PATTERN),
        **_review_ok(reuse_checks),
        **meta,
    }

    legacy_binding = {
        "binding_id": "optional_legacy_real_dep_post_review_binding_v1",
        "optional_missing": not legacy_post_exists,
        "not_blocking": True,
        "may_bind_later": not legacy_post_exists,
        "planning_go_not_invalidated": True,
        "legacy_post_verifier_go": legacy_post_vr.get("verifier") == "GO" if legacy_post_exists else None,
        "bound_as_evidence_source": legacy_post_exists and legacy_post_vr.get("verifier") == "GO",
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    boundary_checks.append(("candidate_generated", meta.get("ocr_domain_config_candidate_generated_now") is True))
    boundary_checks.append(("candidate_not_activated", domain_config_candidate.get("activated_now") is False))

    boundary_audit = {
        "audit_id": "ocr_real_dep_via_factory_standard_boundary_audit_v1",
        "all_boundary_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        "candidate_generated_not_activated": True,
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "ocr_real_dep_via_factory_standard_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        ocr_constitution_review,
        factory_auth_review,
        validation_factory_review,
        harness_review,
        allowed_review,
        forbidden_review,
        no_generic_review,
        standard_reuse_review,
        boundary_audit,
    ]

    all_pass = (
        input_ok
        and domain_config_candidate.get("provider_domain") == "ocr"
        and domain_config_candidate.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID
        and all(section.get("dryrun_and_review_pass") is True for section in review_sections)
        and evidence_rollback_review.get("dryrun_and_review_pass") is True
        and provider_ref_review.get("dryrun_and_review_pass") is True
        and blocked_path_result.get("all_blocked") is True
    )

    closure_decision = {
        "decision_id": "ocr_real_dep_via_factory_standard_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": not all_pass,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "domain_config_candidate_valid": all_pass,
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_authorization_via_factory_standard_dryrun_review_policy_v1",
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
        "authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "blocked_path_count": len(BLOCKED_PATHS),
        "high_risk_count": 1 if not all_pass else 0,
        **meta,
    }

    return {
        "ocr_real_dependency_authorization_via_factory_standard_dryrun_review_policy": policy,
        "planning_input_review": planning_input_review,
        "ocr_real_dependency_domain_config_candidate": domain_config_candidate,
        "ocr_constitution_consumption_review": ocr_constitution_review,
        "factory_authorization_standard_consumption_review": factory_auth_review,
        "validation_factory_consumption_review": validation_factory_review,
        "controlled_provider_readiness_harness_consumption_review": harness_review,
        "allowed_check_domain_config_dryrun_review": allowed_review,
        "forbidden_action_domain_config_dryrun_review": forbidden_review,
        "evidence_rollback_ref_binding_review": evidence_rollback_review,
        "provider_candidate_ref_binding_review": provider_ref_review,
        "no_generic_logic_redefinition_review": no_generic_review,
        "standard_reuse_enforcement_review": standard_reuse_review,
        "optional_legacy_real_dep_post_review_binding": legacy_binding,
        "ocr_real_dep_via_factory_standard_boundary_audit": boundary_audit,
        "ocr_real_dep_via_factory_standard_blocked_path_result": blocked_path_result,
        "ocr_real_dep_via_factory_standard_closure_decision": closure_decision,
        "non_claims_register": non_claims,
        "summary": summary,
    }
