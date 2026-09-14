# -*- coding: utf-8 -*-
"""OCR Real Dependency Authorization via Factory Authorization Standard Planning v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL_GO,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    AUTHORIZATION_SUBCOMPONENTS,
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as EXPLANATION_DR_FINAL_GO,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_authorization_planning_v1 import (
    FINAL_DECISION_GO as LEGACY_OCR_AUTH_PLANNING_FINAL_GO,
)

PHASE_ID = (
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-Planning-v1-001"
)
SCOPE = "ocr_real_dependency_authorization_via_factory_standard_planning_only"
SOURCE_CHAIN = "ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1"

UPSTREAM_EXPLANATION_DR_FINAL = EXPLANATION_DR_FINAL_GO
UPSTREAM_AUTH_EXT_DR_FINAL = AUTH_EXT_DR_FINAL_GO

FINAL_DECISION_GO = (
    "OCR_REAL_DEPENDENCY_AUTHORIZATION_VIA_FACTORY_STANDARD_PLANNING_READY_FOR_DRYRUN_AND_REVIEW"
)
FINAL_DECISION_HOLD = (
    "OCR_REAL_DEPENDENCY_AUTHORIZATION_VIA_FACTORY_STANDARD_PLANNING_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = (
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Authorization-Standard-"
    "DryRunAndReview-v1-001"
)
NEXT_PHASE_HOLD = (
    "Phase-OCR-Provider-Real-Dependency-Check-Authorization-via-Factory-Standard-Issue-Review-v1-001"
)

GOVERNANCE_PATH_STEPS: Tuple[str, ...] = (
    "OCR Real Dependency Check Authorization",
    "via Luna General Constitution",
    "via OCR Constitution",
    "via OCR Authorization Standard",
    "via Factory Authorization Standard",
    "via ControlledProviderReadinessHarness",
    "via Validation Factory",
    "later consumable by Midplatform only after pass",
)

OCR_DOMAIN_CONFIG_ALLOWED_FIELDS: Tuple[str, ...] = (
    "provider_domain",
    "authorization_target",
    "provider_candidate_refs",
    "allowed_checks",
    "forbidden_actions",
    "evidence_requirement_refs",
    "rollback_refs",
    "health_binding_refs",
    "boundary_refs",
    "validation_factory_required",
    "constitution_refs",
    "factory_authorization_standard_ref",
)

OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS: Tuple[str, ...] = (
    "generic request contract",
    "generic grant contract",
    "generic execution window contract",
    "generic approval logic",
    "generic revocation logic",
    "generic rollback logic",
    "generic post-execution review logic",
    "generic lifecycle logic",
    "generic boundary standard",
)

ALLOWED_CHECKS: Tuple[str, ...] = (
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
    "install",
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

OCR_CONSTITUTION_STANDARDS: Tuple[str, ...] = (
    "OCR Input Standard",
    "OCR Output Standard",
    "OCR Evidence Standard",
    "OCR Authorization Standard",
    "OCR Provider Usage Standard",
    "OCR Boundary Standard",
    "OCR Transfer Standard",
)

STANDARD_REUSE_RULES: Tuple[str, ...] = (
    "standard_reuse_required",
    "domain_specific_rule_must_justify_why_not_reusing_existing_standard",
    "new_standard_requires_governance_review",
    "duplicate_generic_authorization_logic_forbidden",
    "duplicate_provider_readiness_chain_forbidden",
    "duplicate_boundary_nonclaim_evidence_lifecycle_forbidden",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "planning_to_domain_config_runtime_activation",
    "planning_to_authorization_request_generation",
    "planning_to_request_send",
    "planning_to_grant_issue",
    "planning_to_execution_window_open",
    "planning_to_real_dependency_check",
    "planning_to_package_check",
    "planning_to_provider_import",
    "planning_to_dependency_install",
    "planning_to_model_download",
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
    "planning_to_constitution_registry_update",
    "planning_to_validation_factory_runtime_enforcement",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Planning GO ≠ OCR authorization granted",
    "domain_config planned ≠ domain_config activated",
    "Factory Authorization Standard binding ≠ request generated",
    "Validation Factory binding ≠ validation runtime enforced",
    "allowed checks listed ≠ checks executed",
    "next DryRunAndReview ≠ real dependency check allowed",
    "standard_reuse_enforcement planned ≠ parallel OCR auth standard created",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "ocr_domain_config_generated_now",
    "authorization_request_generated_now",
    "authorization_request_sent_now",
    "grant_issued_now",
    "execution_window_opened_now",
    "real_dependency_check_executed_now",
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
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "ocr_real_dependency_authorization_via_factory_standard_planning"
)


def _planning_meta() -> Dict[str, Any]:
    meta = {
        "ocr_real_dependency_authorization_via_factory_standard_planning_only": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "factory_standard_ref": FACTORY_STANDARD_ID,
        "legacy_ocr_auth_planning_superseded_for_auth_logic": AUTHORIZATION_STANDARD_ID,
        "selected_provider_for_execution": None,
        "standard_reuse_required": True,
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


def _check_entry(check_id: str) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "current_executed_now": False,
        "requires_authorization_standard": True,
        "requires_execution_window_later": True,
        "requires_evidence_later": True,
        "requires_post_execution_review_later": True,
    }


def run_ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1(
    *,
    midplatform_constitution_governance_explanation_dryrun_and_review_root: str,
    capability_factory_authorization_standard_extension_dryrun_and_review_root: str,
    midplatform_constitution_governance_hierarchy_dryrun_and_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_authorization_planning_root: Optional[str] = None,
    ocr_authorization_next_route_decision_root: Optional[str] = None,
    ocr_provider_real_dependency_check_post_dryrun_review_root: Optional[str] = None,
    controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    explain_dr_root = Path(
        midplatform_constitution_governance_explanation_dryrun_and_review_root
    ).expanduser().resolve()
    explain_dr_sm = _try_read_json(explain_dr_root / "summary.json") or {}
    explain_dr_vr = _try_read_json(explain_dr_root / "verifier_report.json") or {}

    auth_ext_dr_root = Path(
        capability_factory_authorization_standard_extension_dryrun_and_review_root
    ).expanduser().resolve()
    auth_ext_dr_sm = _try_read_json(auth_ext_dr_root / "summary.json") or {}
    auth_ext_dr_vr = _try_read_json(auth_ext_dr_root / "verifier_report.json") or {}

    hierarchy_dr_root = Path(
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root
        or explain_dr_root.parent / "midplatform_constitution_governance_hierarchy_dryrun_and_review"
    ).expanduser().resolve()
    hierarchy_dr_vr = _try_read_json(hierarchy_dr_root / "verifier_report.json") or {}

    legacy_auth_root = Path(
        ocr_provider_real_dependency_check_authorization_planning_root
        or explain_dr_root.parent / "ocr_provider_real_dependency_check_authorization_planning"
    ).expanduser().resolve()
    legacy_auth_vr = _try_read_json(legacy_auth_root / "verifier_report.json") or {}
    legacy_auth_sm = _try_read_json(legacy_auth_root / "summary.json") or {}

    route_root = Path(
        ocr_authorization_next_route_decision_root
        or explain_dr_root.parent / "ocr_authorization_next_route_decision"
    ).expanduser().resolve()
    route_vr = _try_read_json(route_root / "verifier_report.json") or {}

    real_dep_post_root = Path(
        ocr_provider_real_dependency_check_post_dryrun_review_root
        or explain_dr_root.parent / "ocr_provider_real_dependency_check_post_dryrun_review"
    ).expanduser().resolve()
    real_dep_post_vr = _try_read_json(real_dep_post_root / "verifier_report.json") or {}

    harness_post_root = Path(
        controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
        or explain_dr_root.parent
        / "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
    ).expanduser().resolve()
    harness_post_vr = _try_read_json(harness_post_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_planning_meta(),
        "upstream_explanation_dryrun_review_root": str(explain_dr_root),
        "upstream_auth_extension_dryrun_review_root": str(auth_ext_dr_root),
        "upstream_hierarchy_dryrun_review_root": str(hierarchy_dr_root),
        "upstream_legacy_ocr_auth_planning_root": str(legacy_auth_root),
        "upstream_next_route_decision_root": str(route_root),
        "upstream_real_dep_post_dryrun_review_root": str(real_dep_post_root),
        "upstream_harness_post_review_root": str(harness_post_root),
        "output_root": str(out_root),
    }

    if explain_dr_vr.get("verifier") != "GO":
        blockers.append("explanation dryrun review must be GO")
    if explain_dr_sm.get("final_decision") != UPSTREAM_EXPLANATION_DR_FINAL:
        blockers.append("explanation dryrun final_decision mismatch")

    if auth_ext_dr_vr.get("verifier") != "GO":
        blockers.append("auth extension dryrun review must be GO")
    if auth_ext_dr_sm.get("final_decision") != UPSTREAM_AUTH_EXT_DR_FINAL:
        blockers.append("auth extension dryrun final_decision mismatch")

    if hierarchy_dr_vr.get("verifier") != "GO":
        blockers.append("hierarchy dryrun review must be GO")

    if legacy_auth_vr.get("verifier") != "GO":
        blockers.append("legacy ocr auth planning must exist as absorption source")
    if legacy_auth_sm.get("final_decision") != LEGACY_OCR_AUTH_PLANNING_FINAL_GO:
        blockers.append("legacy ocr auth planning final_decision mismatch")

    if route_vr.get("verifier") != "GO":
        blockers.append("next route decision must be GO")

    real_dep_post_go: Optional[bool] = None
    real_dep_post_vr_path = real_dep_post_root / "verifier_report.json"
    if real_dep_post_vr_path.is_file():
        if real_dep_post_vr.get("verifier") != "GO":
            blockers.append("real dep post dryrun review must be GO when present")
        real_dep_post_go = real_dep_post_vr.get("verifier") == "GO"

    if harness_post_vr.get("verifier") != "GO":
        blockers.append("harness post review must be GO")

    planning_ok = len(blockers) == 0
    boundary_ok = planning_ok

    explanation_input_review = {
        "review_id": "constitution_explanation_input_review_v1",
        "explanation_dryrun_go": explain_dr_vr.get("verifier") == "GO",
        "explanation_final_decision": explain_dr_sm.get("final_decision"),
        "real_dep_post_dryrun_go": real_dep_post_go,
        "real_dep_post_dryrun_optional_missing": real_dep_post_go is None,
        "unification_principle": "新模块不得自建平行标准；只提交 domain_config",
        "review_pass": explain_dr_vr.get("verifier") == "GO",
        **meta,
    }

    factory_auth_input_review = {
        "review_id": "factory_authorization_standard_input_review_v1",
        "auth_extension_dryrun_go": auth_ext_dr_vr.get("verifier") == "GO",
        "authorization_standard_id": AUTHORIZATION_STANDARD_ID,
        "tenth_factory_standard": True,
        "review_pass": auth_ext_dr_vr.get("verifier") == "GO",
        **meta,
    }

    governance_path = {
        "path_id": "ocr_real_dependency_authorization_governance_path_v1",
        "authorization_chain": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "steps": list(GOVERNANCE_PATH_STEPS),
        "ocr_submits_domain_config_only": True,
        "factory_authorization_standard_owns_auth_logic": True,
        **meta,
    }

    domain_config_contract = {
        "contract_id": "ocr_real_dependency_domain_config_contract_v1",
        "provider_domain": "ocr",
        "authorization_target": "real_dependency_check",
        "allowed_fields": list(OCR_DOMAIN_CONFIG_ALLOWED_FIELDS),
        "forbidden_fields": list(OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS),
        "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        "validation_factory_required": True,
        "ocr_domain_config_generated_now": False,
        **meta,
    }

    domain_config_candidate_plan = {
        "plan_id": "ocr_real_dependency_domain_config_candidate_plan_v1",
        "candidate_status": "planned_not_generated",
        "planned_fields": {
            "provider_domain": "ocr",
            "authorization_target": "real_dependency_check",
            "provider_candidate_refs": ["controlled_provider_readiness_harness_v1"],
            "allowed_checks": list(ALLOWED_CHECKS),
            "forbidden_actions": list(FORBIDDEN_ACTIONS),
            "evidence_requirement_refs": ["evidence_standard_v1", "ocr_evidence_standard"],
            "rollback_refs": ["sandbox_rollback_standard_v1", AUTHORIZATION_STANDARD_ID],
            "health_binding_refs": ["health_management_v1"],
            "boundary_refs": ["boundary_standard_v1", "ocr_boundary_standard"],
            "validation_factory_required": True,
            "constitution_refs": [
                "luna_general_constitution",
                "ocr_constitution",
                "ocr_authorization_standard",
            ],
            "factory_authorization_standard_ref": AUTHORIZATION_STANDARD_ID,
        },
        "ocr_domain_config_generated_now": False,
        **meta,
    }

    ocr_constitution_binding = {
        "plan_id": "ocr_constitution_binding_plan_v1",
        "ocr_constitution": "OCR Constitution / OCR 宪法",
        "standards": [
            {"standard": std, "applies": True, "simulated": True}
            for std in OCR_CONSTITUTION_STANDARDS
        ],
        "general_constitution_cannot_be_overridden": True,
        "personalized_constitution_cannot_relax_ocr_auth_boundary": True,
        **meta,
    }

    factory_auth_binding = {
        "plan_id": "factory_authorization_standard_binding_plan_v1",
        "standard_id": AUTHORIZATION_STANDARD_ID,
        "parent_standard": FACTORY_STANDARD_ID,
        "subcomponents": [
            {"subcomponent": sub, "consumed_by_ocr_domain_config": True}
            for sub in AUTHORIZATION_SUBCOMPONENTS
        ],
        "ocr_does_not_redefine": list(OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS),
        **meta,
    }

    validation_factory_binding = {
        "plan_id": "validation_factory_binding_plan_v1",
        "role": "compliance inspection layer",
        "writes_rules": False,
        "consumes_standards": True,
        "required_modules": [
            "CandidateOutputContract",
            "NoRuntimeBoundaryAudit",
            "ControlledProviderReadinessHarness",
        ],
        "validation_pass_required_before_midplatform": True,
        "midplatform_consumption_blocked_now": True,
        "validation_factory_runtime_enforced_now": False,
        **meta,
    }

    harness_binding = {
        "plan_id": "controlled_provider_readiness_harness_binding_plan_v1",
        "harness_id": "controlled_provider_readiness_harness_v1",
        "provider_model_readiness_path_exists": True,
        "consumers": [
            {"consumer": "ocr", "status": "validated_first_consumer"},
            {"consumer": "vision", "status": "validated"},
            {"consumer": "voice", "status": "validated"},
        ],
        "checks_readiness_not_grant": True,
        "cannot_invoke_provider": True,
        **meta,
    }

    allowed_checks_plan = {
        "plan_id": "allowed_check_domain_config_plan_v1",
        "checks": [_check_entry(c) for c in ALLOWED_CHECKS],
        "all_current_executed_now": False,
        **meta,
    }

    forbidden_actions_plan = {
        "plan_id": "forbidden_action_domain_config_plan_v1",
        "forbidden_actions": list(FORBIDDEN_ACTIONS),
        "forbidden_actions_override_domain_config": True,
        **meta,
    }

    evidence_rollback_binding = {
        "plan_id": "evidence_and_rollback_ref_binding_plan_v1",
        "evidence_requirement_refs": [
            "evidence_standard_v1",
            "ocr_evidence_standard",
            "factory_authorization_standard_evidence",
        ],
        "rollback_refs": [
            "sandbox_rollback_standard_v1",
            AUTHORIZATION_STANDARD_ID,
            "ocr_boundary_standard",
        ],
        **meta,
    }

    provider_candidate_binding = {
        "plan_id": "provider_candidate_ref_binding_plan_v1",
        "provider_candidate_refs": ["controlled_provider_readiness_harness_v1"],
        "selected_provider_for_execution": None,
        "provider_selection_finalized_now": False,
        **meta,
    }

    no_generic_redefinition = {
        "policy_id": "no_generic_logic_redefinition_policy_v1",
        "forbidden_redefinitions": list(OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS),
        "ocr_phase_role": "domain_config only",
        "auth_logic_owner": AUTHORIZATION_STANDARD_ID,
        "legacy_ocr_auth_planning_role": "evidence/absorption source only",
        "superseded_for_auth_logic_by": AUTHORIZATION_STANDARD_ID,
        **meta,
    }

    standard_reuse_enforcement = {
        "plan_id": "standard_reuse_enforcement_plan_v1",
        "hard_rule": "新模块不得自建平行标准；新模块只能提交 domain_config",
        "common_rules_path": "Constitution / Standard / Harness / Validation Factory",
        "rules": {rule: True for rule in STANDARD_REUSE_RULES},
        "duplicate_generic_authorization_logic_forbidden": True,
        **meta,
    }

    blocked_path_matrix = {
        "matrix_id": "ocr_real_dep_via_factory_standard_blocked_path_matrix_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        **meta,
    }

    dryrun_plan = {
        "plan_id": "ocr_real_dep_via_factory_standard_dryrun_plan_v1",
        "next_phase": NEXT_PHASE_GO,
        "dryrun_and_review_merged": True,
        "objectives": [
            "generate ocr real-dep domain_config_candidate",
            "verify domain_config consumes OCR Constitution / Factory Authorization Standard / VF / Harness",
            "verify OCR did not redefine generic authorization logic",
            "verify standard_reuse_required",
            "verify all real check actions remain blocked",
        ],
        "dryrun_forbids": [
            "request generation",
            "grant",
            "execution window open",
            "real dependency check",
            "import/install/download/invoke",
        ],
        **meta,
    }

    planning_decision = {
        "decision_id": "ocr_real_dependency_authorization_via_factory_standard_planning_decision_v1",
        "planning_pass": boundary_ok,
        "ocr_domain_config_only": True,
        "recommended_next_phase": NEXT_PHASE_GO if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION_GO if boundary_ok else FINAL_DECISION_HOLD,
        **meta,
    }

    policy = {
        "policy_id": "ocr_real_dependency_authorization_via_factory_standard_planning_policy_v1",
        "phase": PHASE_ID,
        "scope": SCOPE,
        **meta,
    }

    non_claims_reg = {
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
        "governance_path_steps": len(GOVERNANCE_PATH_STEPS),
        "allowed_check_count": len(ALLOWED_CHECKS),
        "forbidden_action_count": len(FORBIDDEN_ACTIONS),
        "blocked_path_count": len(BLOCKED_PATHS),
        "high_risk_count": 0 if boundary_ok else 1,
        **meta,
    }

    return {
        "ocr_real_dependency_authorization_via_factory_standard_planning_policy": policy,
        "constitution_explanation_input_review": explanation_input_review,
        "factory_authorization_standard_input_review": factory_auth_input_review,
        "ocr_real_dependency_authorization_governance_path": governance_path,
        "ocr_real_dependency_domain_config_contract": domain_config_contract,
        "ocr_real_dependency_domain_config_candidate_plan": domain_config_candidate_plan,
        "ocr_constitution_binding_plan": ocr_constitution_binding,
        "factory_authorization_standard_binding_plan": factory_auth_binding,
        "validation_factory_binding_plan": validation_factory_binding,
        "controlled_provider_readiness_harness_binding_plan": harness_binding,
        "allowed_check_domain_config_plan": allowed_checks_plan,
        "forbidden_action_domain_config_plan": forbidden_actions_plan,
        "evidence_and_rollback_ref_binding_plan": evidence_rollback_binding,
        "provider_candidate_ref_binding_plan": provider_candidate_binding,
        "no_generic_logic_redefinition_policy": no_generic_redefinition,
        "standard_reuse_enforcement_plan": standard_reuse_enforcement,
        "ocr_real_dep_via_factory_standard_blocked_path_matrix": blocked_path_matrix,
        "ocr_real_dep_via_factory_standard_dryrun_plan": dryrun_plan,
        "non_claims_register": non_claims_reg,
        "ocr_real_dependency_authorization_via_factory_standard_planning_decision": planning_decision,
        "summary": summary,
    }
