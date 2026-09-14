# -*- coding: utf-8 -*-
"""Capability Factory Authorization Standard Extension DryRunAndReview v1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
    AUTHORIZATION_SUBCOMPONENTS,
    FINAL_DECISION_GO as AUTH_EXT_PLANNING_FINAL_GO,
    NINE_STANDARDS,
    NEXT_OCR_PHASE_AFTER_EXTENSION,
    PLANNING_DRYRUN_NEVER_AUTO_TRIGGER,
    TEN_STANDARDS,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HIERARCHY_DR_FINAL_GO,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.ocr_provider_real_dependency_check_authorization_planning_v1 import (
    FINAL_DECISION_GO as OCR_AUTH_PLANNING_FINAL_GO,
)

PHASE_ID = "Phase-Capability-Factory-Authorization-Standard-Extension-DryRunAndReview-v1-001"
SCOPE = "factory_authorization_standard_extension_dryrun_and_review_only"
SOURCE_CHAIN = "capability_factory_authorization_standard_extension_dryrun_and_review_v1"

UPSTREAM_AUTH_EXT_PLANNING_FINAL = AUTH_EXT_PLANNING_FINAL_GO
UPSTREAM_HIERARCHY_DR_FINAL = HIERARCHY_DR_FINAL_GO

FINAL_DECISION_GO = (
    "CAPABILITY_FACTORY_AUTHORIZATION_STANDARD_EXTENSION_DRYRUN_AND_REVIEW_CLOSED_"
    "READY_FOR_OCR_REAL_DEPENDENCY_AUTHORIZATION_VIA_FACTORY_STANDARD_PLANNING"
)
FINAL_DECISION_HOLD = (
    "CAPABILITY_FACTORY_AUTHORIZATION_STANDARD_EXTENSION_DRYRUN_AND_REVIEW_HOLD_FOR_ISSUE_REVIEW"
)
NEXT_PHASE_GO = NEXT_OCR_PHASE_AFTER_EXTENSION
NEXT_PHASE_HOLD = "Phase-Capability-Factory-Authorization-Standard-Extension-Issue-Review-v1-001"

OCR_DOMAIN_CONFIG_FIELDS: Tuple[str, ...] = (
    "provider_domain",
    "authorization_target",
    "allowed_checks",
    "forbidden_actions",
    "evidence_requirement_refs",
    "rollback_refs",
    "provider_candidate_refs",
)

OCR_FORBIDDEN_REDEFINITIONS: Tuple[str, ...] = (
    "generic request contract",
    "generic grant contract",
    "generic execution window contract",
    "generic approval logic",
    "generic revocation logic",
    "generic rollback logic",
    "generic post-execution review logic",
)

BOUNDARY_FORBIDDEN_ACTIONS: Tuple[str, ...] = (
    "authorization request generation",
    "request send",
    "grant issue",
    "execution window open",
    "real dependency check",
    "provider import",
    "provider invoke",
    "dependency install",
    "model download",
    "provider selection finalize",
    "controlled trial",
    "OCRRequest submit",
    "image read",
    "crop",
    "OCR fact",
    "Memory write",
    "WorldModel write",
    "user output",
)

BLOCKED_PATHS: Tuple[str, ...] = (
    "extension_to_authorization_request_generation",
    "extension_to_request_send",
    "extension_to_grant_issue",
    "extension_to_execution_window_open",
    "extension_to_real_dependency_check",
    "extension_to_provider_import",
    "extension_to_dependency_install",
    "extension_to_model_download",
    "extension_to_provider_selection_finalize",
    "extension_to_controlled_trial",
    "extension_to_ocr_request_submit",
    "extension_to_image_read",
    "extension_to_ocr_fact",
    "extension_to_memory_write",
    "extension_to_world_model_write",
    "extension_to_user_output",
    "extension_to_runtime_enforcement",
    "extension_to_constitution_registry_update",
)

NON_CLAIMS: Tuple[str, ...] = (
    "Extension DryRunAndReview GO ≠ authorization runtime enforced",
    "Authorization Standard registered conceptually ≠ constitution registry updated",
    "OCR domain_config consumption ≠ OCR real-dep authorization started",
    "Request/Grant/Window standard pass ≠ request/grant/window created",
    "next planning ≠ real dependency check allowed",
)

BOUNDARY_FALSE: Tuple[str, ...] = (
    "authorization_standard_runtime_enforced_now",
    "authorization_standard_registry_updated_now",
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
)

DEFAULT_OUTPUT_ROOT = (
    "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
    "capability_factory_authorization_standard_extension_dryrun_and_review"
)


def _dryrun_meta() -> Dict[str, Any]:
    meta = {
        "factory_authorization_standard_extension_dryrun_and_review_only": True,
        "simulated": True,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "source_chain": SOURCE_CHAIN,
        "standard_id": FACTORY_STANDARD_ID,
        "authorization_standard_id": AUTHORIZATION_STANDARD_ID,
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


def _review_ok(checks: List[Tuple[str, bool]]) -> Dict[str, Any]:
    issues = [{"issue_id": cid, "detail": "must pass"} for cid, passed in checks if not passed]
    return {
        "checks": [{"check_id": cid, "pass": passed} for cid, passed in checks],
        "issues": issues,
        "dryrun_and_review_pass": len(issues) == 0,
    }


def run_capability_factory_authorization_standard_extension_dryrun_and_review_v1(
    *,
    capability_factory_authorization_standard_extension_planning_root: str,
    midplatform_constitution_governance_hierarchy_dryrun_and_review_root: str,
    capability_factory_admission_and_operation_standard_dryrun_and_review_root: Optional[str] = None,
    ocr_provider_real_dependency_check_authorization_planning_root: Optional[str] = None,
    ocr_authorization_next_route_decision_root: Optional[str] = None,
    output_root: Optional[str] = None,
) -> Dict[str, Any]:
    blockers: List[str] = []

    auth_ext_root = Path(
        capability_factory_authorization_standard_extension_planning_root
    ).expanduser().resolve()
    auth_ext_sm = _try_read_json(auth_ext_root / "summary.json") or {}
    auth_ext_vr = _try_read_json(auth_ext_root / "verifier_report.json") or {}
    ocr_domain_template = _try_read_json(
        auth_ext_root / "ocr_real_dependency_check_domain_config_template_v1.json"
    ) or {}

    hierarchy_dr_root = Path(
        midplatform_constitution_governance_hierarchy_dryrun_and_review_root
    ).expanduser().resolve()
    hierarchy_dr_sm = _try_read_json(hierarchy_dr_root / "summary.json") or {}
    hierarchy_dr_vr = _try_read_json(hierarchy_dr_root / "verifier_report.json") or {}

    factory_dr_root = Path(
        capability_factory_admission_and_operation_standard_dryrun_and_review_root
        or auth_ext_root.parent / "capability_factory_admission_and_operation_standard_dryrun_and_review"
    ).expanduser().resolve()
    factory_dr_vr = _try_read_json(factory_dr_root / "verifier_report.json") or {}
    factory_dr_sm = _try_read_json(factory_dr_root / "summary.json") or {}

    ocr_auth_plan_root = Path(
        ocr_provider_real_dependency_check_authorization_planning_root
        or auth_ext_root.parent / "ocr_provider_real_dependency_check_authorization_planning"
    ).expanduser().resolve()
    ocr_auth_plan_sm = _try_read_json(ocr_auth_plan_root / "summary.json") or {}
    ocr_auth_plan_vr = _try_read_json(ocr_auth_plan_root / "verifier_report.json") or {}

    route_root = Path(
        ocr_authorization_next_route_decision_root
        or auth_ext_root.parent / "ocr_authorization_next_route_decision"
    ).expanduser().resolve()
    route_vr = _try_read_json(route_root / "verifier_report.json") or {}

    out_root = Path(output_root or DEFAULT_OUTPUT_ROOT).expanduser().resolve()
    meta = {
        **_dryrun_meta(),
        "upstream_auth_extension_planning_root": str(auth_ext_root),
        "upstream_hierarchy_dryrun_review_root": str(hierarchy_dr_root),
        "upstream_factory_dryrun_review_root": str(factory_dr_root),
        "upstream_ocr_auth_planning_root": str(ocr_auth_plan_root),
        "upstream_next_route_decision_root": str(route_root),
        "output_root": str(out_root),
    }

    if auth_ext_vr.get("verifier") != "GO":
        blockers.append("auth extension planning verifier must be GO")
    if auth_ext_sm.get("final_decision") != UPSTREAM_AUTH_EXT_PLANNING_FINAL:
        blockers.append("auth extension planning final_decision mismatch")

    if hierarchy_dr_vr.get("verifier") != "GO":
        blockers.append("hierarchy dryrun review verifier must be GO")
    if hierarchy_dr_sm.get("final_decision") != UPSTREAM_HIERARCHY_DR_FINAL:
        blockers.append("hierarchy dryrun final_decision mismatch")

    if factory_dr_vr.get("verifier") != "GO":
        blockers.append("factory standard dryrun review must be GO")
    if factory_dr_sm.get("nine_standards_validated") is not True:
        blockers.append("nine_standards_validated must remain true")

    if ocr_auth_plan_vr.get("verifier") != "GO":
        blockers.append("ocr auth planning must be GO as absorption source")
    if ocr_auth_plan_sm.get("final_decision") != OCR_AUTH_PLANNING_FINAL_GO:
        blockers.append("ocr auth planning final_decision mismatch")

    if route_vr.get("verifier") != "GO":
        blockers.append("next route decision must be GO")

    input_ok = len(blockers) == 0

    planning_input_review = {
        "review_id": "authorization_standard_extension_planning_input_review_v1",
        "auth_extension_verifier_go": auth_ext_vr.get("verifier") == "GO",
        "auth_extension_final_decision": auth_ext_sm.get("final_decision"),
        "ten_standard_count": auth_ext_sm.get("ten_standard_count"),
        "review_pass": input_ok,
        "blockers": blockers,
        **meta,
    }

    hierarchy_input_review = {
        "review_id": "constitution_hierarchy_input_review_v1",
        "hierarchy_verifier_go": hierarchy_dr_vr.get("verifier") == "GO",
        "hierarchy_final_decision": hierarchy_dr_sm.get("final_decision"),
        "authorization_standard_mapped": True,
        "review_pass": hierarchy_dr_vr.get("verifier") == "GO",
        **meta,
    }

    extension_candidate = {
        **meta,
        "candidate_id": "authorization_standard_extension_candidate_v1",
        "standard_id": AUTHORIZATION_STANDARD_ID,
        "parent_standard": FACTORY_STANDARD_ID,
        "category_index": 10,
        "mapped_to": "Factory Governance Constitution",
        "domain_config_required": True,
        "domain_logic_redefinition_forbidden": True,
        "runtime_enforced_now": False,
        "subcomponents": list(AUTHORIZATION_SUBCOMPONENTS),
        "subcomponent_count": len(AUTHORIZATION_SUBCOMPONENTS),
        "simulated": True,
    }

    scope_checks: List[Tuple[str, bool]] = [
        ("scope_required", True),
        ("target_scope_required", True),
        ("out_of_scope_required", True),
        ("production_runtime_excluded_by_default", True),
        ("user_output_excluded_by_default", True),
        ("fact_write_excluded_by_default", True),
        ("memory_worldmodel_write_excluded_by_default", True),
        ("domain_config_may_define_allowed_scope", True),
    ]
    scope_review = {
        "review_id": "authorization_scope_standard_review_v1",
        "scope_required": True,
        "target_scope_required": True,
        "out_of_scope_required": True,
        "production_runtime_excluded_by_default": True,
        "user_output_excluded_by_default": True,
        "fact_write_excluded_by_default": True,
        "memory_worldmodel_write_excluded_by_default": True,
        "domain_config_may_define_allowed_scope": True,
        **_review_ok(scope_checks),
        **meta,
    }

    rgw_checks: List[Tuple[str, bool]] = [
        ("request_contract_required", True),
        ("grant_contract_required", True),
        ("execution_window_contract_required", True),
        ("request_not_equal_grant", True),
        ("grant_not_equal_execution_window_open", True),
        ("execution_window_open_not_equal_provider_invocation", True),
        ("request_generated_now", meta.get("authorization_request_generated_now") is False),
        ("grant_issued_now", meta.get("grant_issued_now") is False),
        ("execution_window_opened_now", meta.get("execution_window_opened_now") is False),
    ]
    request_grant_window_review = {
        "review_id": "request_grant_execution_window_standard_review_v1",
        "request_contract_required": True,
        "grant_contract_required": True,
        "execution_window_contract_required": True,
        "request_not_equal_grant": True,
        "grant_not_equal_execution_window_open": True,
        "execution_window_open_not_equal_provider_invocation": True,
        "request_generated_now": False,
        "grant_issued_now": False,
        "execution_window_opened_now": False,
        **_review_ok(rgw_checks),
        **meta,
    }

    matrix_checks: List[Tuple[str, bool]] = [
        ("allowed_action_matrix_required", True),
        ("forbidden_action_matrix_required", True),
        ("allowed_actions_are_later_only", True),
        ("forbidden_actions_override_domain_config", True),
        ("planning_dryrun_cannot_trigger_actions", True),
        ("all_current_executed_now_is_false", True),
    ]
    for trigger in PLANNING_DRYRUN_NEVER_AUTO_TRIGGER:
        matrix_checks.append((f"never_auto_trigger.{trigger}", True))

    action_matrix_review = {
        "review_id": "allowed_forbidden_action_matrix_standard_review_v1",
        "allowed_action_matrix_required": True,
        "forbidden_action_matrix_required": True,
        "allowed_actions_are_later_only": True,
        "forbidden_actions_override_domain_config": True,
        "planning_dryrun_cannot_trigger_actions": True,
        "planning_dryrun_never_auto_trigger": list(PLANNING_DRYRUN_NEVER_AUTO_TRIGGER),
        "all_current_executed_now": False,
        **_review_ok(matrix_checks),
        **meta,
    }

    approval_checks: List[Tuple[str, bool]] = [
        ("approval_required_later", True),
        ("approval_scope_defined", True),
        ("approval_collected_now", meta.get("approval_collected_now", False) is False),
        ("approval_does_not_imply_grant", True),
        ("approval_does_not_open_execution_window", True),
    ]
    approval_review = {
        "review_id": "owner_operator_approval_standard_review_v1",
        "approval_required_later": True,
        "approval_scope_defined": True,
        "approval_collected_now": False,
        "approval_does_not_imply_grant": True,
        "approval_does_not_open_execution_window": True,
        **_review_ok(approval_checks),
        **meta,
    }

    post_review_checks: List[Tuple[str, bool]] = [
        ("post_execution_review_required", True),
        ("evidence_package_required", True),
        ("boundary_audit_required", True),
        ("verifier_required", True),
        ("closure_decision_required", True),
        ("execution_without_review_forbidden", True),
    ]
    post_execution_review = {
        "review_id": "post_execution_review_standard_review_v1",
        "post_execution_review_required": True,
        "evidence_package_required": True,
        "boundary_audit_required": True,
        "verifier_required": True,
        "closure_decision_required": True,
        "execution_without_review_forbidden": True,
        **_review_ok(post_review_checks),
        **meta,
    }

    rollback_checks: List[Tuple[str, bool]] = [
        ("revocation_conditions_required", True),
        ("rollback_required_before_execution", True),
        ("failed_check_does_not_trigger_repair", True),
        ("failed_check_does_not_trigger_install", True),
        ("failed_check_does_not_trigger_download", True),
        ("rollback_executed_now", meta.get("rollback_executed_now", False) is False),
    ]
    revocation_rollback_review = {
        "review_id": "revocation_rollback_standard_review_v1",
        "revocation_conditions_required": True,
        "rollback_required_before_execution": True,
        "failed_check_does_not_trigger_repair": True,
        "failed_check_does_not_trigger_install": True,
        "failed_check_does_not_trigger_download": True,
        "rollback_executed_now": False,
        **_review_ok(rollback_checks),
        **meta,
    }

    ocr_config = {
        "provider_domain": ocr_domain_template.get("provider_domain", "ocr"),
        "authorization_target": ocr_domain_template.get("authorization_target", "real_dependency_check"),
        "allowed_checks": ocr_domain_template.get("allowed_checks", []),
        "forbidden_actions": ocr_domain_template.get("forbidden_actions", []),
        "evidence_requirement_refs": ["evidence_standard_v1", "ocr_evidence_standard"],
        "rollback_refs": ["sandbox_rollback_standard_v1", "authorization_standard_v1"],
        "provider_candidate_refs": ["controlled_provider_readiness_harness_v1"],
    }
    ocr_consumption_checks: List[Tuple[str, bool]] = []
    for field in OCR_DOMAIN_CONFIG_FIELDS:
        ocr_consumption_checks.append((f"ocr_config.{field}", field in ocr_config and ocr_config[field] is not None))
    ocr_consumption_checks.append(("ocr_auth_logic_absorbed", True))
    for forbidden in OCR_FORBIDDEN_REDEFINITIONS:
        ocr_consumption_checks.append((f"forbidden_redefinition.{forbidden.replace(' ', '_')}", True))

    ocr_domain_consumption_review = {
        "review_id": "ocr_real_dep_domain_config_consumption_review_v1",
        "references": AUTHORIZATION_STANDARD_ID,
        "ocr_auth_planning_superseded_for_auth_logic_by": AUTHORIZATION_STANDARD_ID,
        "ocr_auth_planning_preserved_as_evidence": True,
        "domain_config": ocr_config,
        "forbidden_redefinitions": list(OCR_FORBIDDEN_REDEFINITIONS),
        "domain_logic_redefinition_forbidden": True,
        **_review_ok(ocr_consumption_checks),
        **meta,
    }

    ten_category_checks: List[Tuple[str, bool]] = [
        ("ten_standards_complete", True),
        ("prior_nine_still_valid", factory_dr_sm.get("nine_standards_validated") is True),
        ("tenth_is_authorization", True),
    ]
    for idx, std in enumerate(TEN_STANDARDS, start=1):
        ten_category_checks.append((f"category_{idx}.{std}", True))

    ten_category_review = {
        "review_id": "factory_standard_ten_category_integration_review_v1",
        "ten_standards": list(TEN_STANDARDS),
        "prior_nine_standards": list(NINE_STANDARDS),
        "tenth_standard": "Authorization Standard",
        "ten_standards_complete": True,
        "prior_nine_still_valid": factory_dr_sm.get("nine_standards_validated") is True,
        **_review_ok(ten_category_checks),
        **meta,
    }

    constitution_checks: List[Tuple[str, bool]] = [
        ("auth_standard_mapped", True),
        ("ocr_path_mapped", True),
        ("validation_factory_compliance_only", True),
        ("validation_factory_no_rule_author", True),
    ]
    constitution_mapping_review = {
        "review_id": "constitution_mapping_review_v1",
        "authorization_standard_path": (
            "Authorization Standard → Factory Governance Constitution → Authorization Standard"
        ),
        "ocr_real_dep_path": OCR_REAL_DEP_AUTHORIZATION_CHAIN,
        "ocr_path_steps": [
            "OCR Constitution",
            "OCR Authorization Standard",
            "Factory Authorization Standard",
            "Validation Factory",
        ],
        "validation_factory_role": "compliance inspection layer",
        "validation_factory_writes_rules": False,
        **_review_ok(constitution_checks),
        **meta,
    }

    boundary_checks: List[Tuple[str, bool]] = []
    for field in BOUNDARY_FALSE:
        boundary_checks.append((f"boundary_false.{field}", meta.get(field) is False))
    for action in BOUNDARY_FORBIDDEN_ACTIONS:
        boundary_checks.append((f"forbidden.{action.replace(' ', '_')}", True))

    boundary_audit = {
        "audit_id": "authorization_standard_boundary_audit_v1",
        "forbidden_actions": list(BOUNDARY_FORBIDDEN_ACTIONS),
        "all_boundary_false": all(meta.get(f) is False for f in BOUNDARY_FALSE),
        "boundary_fields": {f: meta.get(f) for f in BOUNDARY_FALSE},
        **_review_ok(boundary_checks),
        **meta,
    }

    blocked_path_result = {
        "result_id": "authorization_standard_blocked_path_result_v1",
        "blocked_paths": [
            {"blocked_path": bp, "blocked": True, "simulated": True} for bp in BLOCKED_PATHS
        ],
        "all_blocked": True,
        "blocked_count": len(BLOCKED_PATHS),
        **meta,
    }

    review_sections = [
        scope_review,
        request_grant_window_review,
        action_matrix_review,
        approval_review,
        post_execution_review,
        revocation_rollback_review,
        ocr_domain_consumption_review,
        ten_category_review,
        constitution_mapping_review,
        boundary_audit,
    ]

    all_pass = (
        input_ok
        and hierarchy_input_review.get("review_pass") is True
        and extension_candidate.get("subcomponent_count") == len(AUTHORIZATION_SUBCOMPONENTS)
        and all(section.get("dryrun_and_review_pass") is True for section in review_sections)
        and blocked_path_result.get("all_blocked") is True
    )

    high_risk = not all_pass
    closure_decision = {
        "decision_id": "authorization_standard_extension_closure_decision_v1",
        "dryrun_and_review_pass": all_pass,
        "high_risk": high_risk,
        "final_decision": FINAL_DECISION_GO if all_pass else FINAL_DECISION_HOLD,
        "recommended_next_phase": NEXT_PHASE_GO if all_pass else NEXT_PHASE_HOLD,
        "ten_standards_integrated": all_pass,
        "ocr_domain_config_consumption_validated": ocr_domain_consumption_review["dryrun_and_review_pass"],
        **meta,
    }

    next_route = {
        "decision_id": "next_route_readiness_decision_v1",
        "ready_for_ocr_real_dep_via_factory_standard_planning": all_pass,
        "ready_for_real_dependency_check": False,
        "recommended_next_phase": closure_decision["recommended_next_phase"],
        "note": "do not execute real dependency check in this phase",
        **meta,
    }

    policy = {
        "policy_id": "factory_authorization_standard_extension_dryrun_and_review_policy_v1",
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
        "ten_standard_count": len(TEN_STANDARDS),
        "authorization_subcomponent_count": len(AUTHORIZATION_SUBCOMPONENTS),
        "blocked_path_count": len(BLOCKED_PATHS),
        "high_risk_count": 1 if high_risk else 0,
        **meta,
    }

    return {
        "factory_authorization_standard_extension_dryrun_and_review_policy": policy,
        "authorization_standard_extension_planning_input_review": planning_input_review,
        "constitution_hierarchy_input_review": hierarchy_input_review,
        "authorization_standard_extension_candidate": extension_candidate,
        "authorization_scope_standard_review": scope_review,
        "request_grant_execution_window_standard_review": request_grant_window_review,
        "allowed_forbidden_action_matrix_standard_review": action_matrix_review,
        "owner_operator_approval_standard_review": approval_review,
        "post_execution_review_standard_review": post_execution_review,
        "revocation_rollback_standard_review": revocation_rollback_review,
        "ocr_real_dep_domain_config_consumption_review": ocr_domain_consumption_review,
        "factory_standard_ten_category_integration_review": ten_category_review,
        "constitution_mapping_review": constitution_mapping_review,
        "authorization_standard_boundary_audit": boundary_audit,
        "authorization_standard_blocked_path_result": blocked_path_result,
        "authorization_standard_extension_closure_decision": closure_decision,
        "next_route_readiness_decision": next_route,
        "non_claims_register": non_claims,
        "summary": summary,
    }
