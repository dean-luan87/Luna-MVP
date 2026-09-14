# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Request DryRun v1.

Authorization request dry-run only: simulate consumption of request planning outputs.
Does not generate request artifacts, send requests, or grant authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_authorization_request_planning_v1 import (
    ABORT_REVOKE_LINKAGES,
    LIFECYCLE_STATES,
    NON_CLAIMS_SCENARIOS,
    NON_GRANT_NON_GENERATION_STATEMENTS,
    REQUEST_IDENTITY_FIELDS,
    REVIEW_REQUIREMENTS,
    SCOPE_AND_EXCLUSION_ITEMS,
    SOURCE_SET_BINDING_COMPONENTS,
    VERIFIER_USAGE_CHECKS,
)
from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    DOMAIN_CONSTRAINTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001"
DRYRUN_SCOPE = "authorization_request_dryrun_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_request_dryrun_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN"
)

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "authorization_request_planning_policy_v1.json",
    "authorization_request_identity_planning_v1.json",
    "authorization_request_source_set_binding_planning_v1.json",
    "authorization_request_domain_preservation_binding_planning_v1.json",
    "authorization_request_scope_and_exclusion_planning_v1.json",
    "authorization_request_non_grant_and_non_generation_statement_planning_v1.json",
    "authorization_request_lifecycle_planning_v1.json",
    "authorization_request_review_requirement_planning_v1.json",
    "authorization_request_abort_revoke_linkage_planning_v1.json",
    "authorization_request_verifier_usage_planning_v1.json",
    "authorization_request_planning_non_claims_planning_v1.json",
    "authorization_request_planning_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "authorization_request_dryrun_only": True,
        "simulated": True,
        "governance_constraint_module_generation_authorization_request_generated_now": False,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generation_authorization_grant_generated_now": False,
        "source_set_final_approved_now": False,
        "domain_specific_preservation_approved_now": False,
        "module_generation_authority_released_now": False,
        "future_verifier_integration_boundary_confirmed_now": False,
        "future_phase_template_integration_boundary_confirmed_now": False,
        "post_generation_review_executed_now": False,
        "module_generation_abort_authority_confirmed_now": False,
        "module_generation_revoke_authority_confirmed_now": False,
        "module_generation_rollback_authority_confirmed_now": False,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "verifier_integration_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "legacy_phase_modified_now": False,
        "legacy_document_rewritten_now": False,
        "legacy_eval_out_modified_now": False,
        "legacy_verifier_rerun_now": False,
        "legacy_chain_deprecated_now": False,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        "domain_specific_rules_preserved": True,
        "frozen_fields_enforced_now": False,
        "verifier_baseline_integrated_now": False,
        "file_operation_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "success_claim_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "main_migration_chain_resumed_now": False,
        "main_migration_chain_paused": MAIN_MIGRATION_PAUSED,
        "main_migration_resume_phase": MAIN_MIGRATION_RESUME_PHASE,
        "lifecycle_planning_defined_only": True,
        "runtime_invoked": False,
        "execution_committed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _dryrun_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_dryrun_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "authorization_request_planning_readiness_decision_v1.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in UPSTREAM_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
    loaded = summary is not None and verifier is not None and readiness is not None and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary or {},
        "verifier": verifier or {},
        "readiness": readiness or {},
        "artifacts": art,
        "missing": missing,
    }


def _simulate_identity_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("identity_field"): r for r in (planning.get("rows") or [])}
    for field, _ in REQUEST_IDENTITY_FIELDS:
        pr = planning_rows.get(field, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("must_be_present_later") is True
            and pr.get("required_for_request_artifact") is True
            and pr.get("request_artifact_generated_now") is False
            and pr.get("request_sent_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                identity_field=field,
                simulated_identity_consumption=True,
                required_for_request_artifact=True,
                request_artifact_generated_now=False,
                request_sent_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_source_set_binding_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("source_component"): r for r in (planning.get("rows") or [])}
    for component, role in SOURCE_SET_BINDING_COMPONENTS:
        pr = planning_rows.get(component, {})
        review_pass = (
            pr.get("binding_required") is True
            and pr.get("not_generated_now") is True
            and pr.get("source_set_final_approved_now") is False
            and pr.get("source_bound_now") is False
            and pr.get("request_artifact_generated_now") is False
            and bool(pr.get("source_evidence_role") or role)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                source_component=component,
                simulated_binding_check=True,
                source_evidence_role=pr.get("source_evidence_role") or role,
                source_integrity_requirement=pr.get("source_integrity_requirement"),
                source_set_final_approved_now=False,
                source_bound_now=False,
                request_artifact_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_domain_preservation_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("domain_constraint_name"): r for r in (planning.get("rows") or [])}
    for name, _, _, _ in DOMAIN_CONSTRAINTS:
        pr = planning_rows.get(name, {})
        review_pass = (
            pr.get("binding_required") is True
            and pr.get("flattening_forbidden") is True
            and pr.get("independent_consumption_path_required") is True
            and pr.get("approved_now") is False
            and pr.get("not_generated_now") is True
            and pr.get("request_artifact_generated_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                domain_constraint_name=name,
                simulated_binding_check=True,
                independent_consumption_path_required=True,
                flattening_forbidden=True,
                approved_now=False,
                domain_bound_now=False,
                request_artifact_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_scope_exclusion_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("scope_item"): r for r in (planning.get("rows") or [])}
    for item, scope_type, _ in SCOPE_AND_EXCLUSION_ITEMS:
        pr = planning_rows.get(item, {})
        review_pass = (
            pr.get("scope_type") == scope_type
            and pr.get("not_generated_now") is True
            and pr.get("allowed_now") is False
            and pr.get("request_artifact_generated_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                scope_item=item,
                scope_type=scope_type,
                simulated_scope_consumption=True,
                allowed_by_request_later=pr.get("allowed_by_request_later", scope_type == "requested"),
                allowed_now=False,
                request_artifact_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 13


def _simulate_statements_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("statement_id"): r for r in (planning.get("rows") or [])}
    for sid, statement, _ in NON_GRANT_NON_GENERATION_STATEMENTS:
        pr = planning_rows.get(sid, {})
        review_pass = (
            pr.get("must_be_in_request_later") is True
            and pr.get("must_be_in_summary") is True
            and pr.get("must_be_in_verifier_report") is True
            and pr.get("generated_now") is False
            and pr.get("not_generated_now") is True
            and bool(pr.get("statement") or statement)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                statement_id=sid,
                statement=pr.get("statement") or statement,
                simulated_statement_consumption=True,
                must_be_in_request_later=True,
                must_be_in_summary=True,
                must_be_in_verifier_report=True,
                generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _simulate_lifecycle_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("lifecycle_state"): r for r in (planning.get("rows") or [])}
    for state, meaning, allowed, forbidden in LIFECYCLE_STATES:
        pr = planning_rows.get(state, {})
        review_pass = (
            pr.get("current_state_now") is False
            and pr.get("request_sent_now") is False
            and pr.get("grant_issued_now") is False
            and pr.get("planning_defined_only") is True
            and pr.get("not_generated_now") is True
            and bool(pr.get("canonical_meaning") or meaning)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                lifecycle_state=state,
                canonical_meaning=pr.get("canonical_meaning") or meaning,
                simulated_lifecycle_consumption=True,
                allowed_transitions=list(pr.get("allowed_transitions") or allowed),
                forbidden_transitions=list(pr.get("forbidden_transitions") or forbidden),
                current_state_now=False,
                request_sent_now=False,
                grant_issued_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_review_requirement_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("review_requirement"): r for r in (planning.get("rows") or [])}
    for req in REVIEW_REQUIREMENTS:
        pr = planning_rows.get(req, {})
        review_pass = (
            pr.get("review_required_before_request_sent") is True
            and pr.get("review_executed_now") is False
            and pr.get("request_ready_now") is False
            and pr.get("request_sent_now") is False
            and pr.get("not_generated_now") is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                review_requirement=req,
                simulated_review_requirement_consumption=True,
                review_required_before_request_sent=True,
                review_executed_now=False,
                request_ready_now=False,
                request_sent_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_abort_revoke_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("linkage_type"): r for r in (planning.get("rows") or [])}
    for linkage, trigger, holder in ABORT_REVOKE_LINKAGES:
        pr = planning_rows.get(linkage, {})
        review_pass = (
            pr.get("confirmed_now") is False
            and pr.get("abort_executed_now") is False
            and pr.get("revoke_executed_now") is False
            and pr.get("not_generated_now") is True
            and bool(pr.get("trigger_condition") or trigger)
            and bool(pr.get("authority_holder") or holder)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                linkage_type=linkage,
                trigger_condition=pr.get("trigger_condition") or trigger,
                simulated_linkage_consumption=True,
                authority_holder=pr.get("authority_holder") or holder,
                confirmed_now=False,
                abort_executed_now=False,
                revoke_executed_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_verifier_usage_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("verifier_check_id"): r for r in (planning.get("rows") or [])}
    for check_id, check_name, failure in VERIFIER_USAGE_CHECKS:
        pr = planning_rows.get(check_id, {})
        review_pass = (
            pr.get("planned_now") is True
            and pr.get("verifier_modified_now") is False
            and pr.get("not_generated_now") is True
            and bool(pr.get("check_name") or check_name)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                verifier_check_id=check_id,
                check_name=pr.get("check_name") or check_name,
                simulated_verifier_usage=True,
                required_fields=pr.get("required_fields") or ["authorization_request_planning_only"],
                failure_condition=pr.get("failure_condition") or failure,
                severity=pr.get("severity") or "critical",
                verifier_modified_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_non_claims_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("scenario"): r for r in (planning.get("rows") or [])}
    for scenario, statement in NON_CLAIMS_SCENARIOS:
        pr = planning_rows.get(scenario, {})
        review_pass = (
            pr.get("planned_now") is True
            and pr.get("generated_now") is False
            and pr.get("not_generated_now") is True
            and pr.get("must_be_in_summary") is True
            and pr.get("must_be_in_verifier_report") is True
            and bool(pr.get("required_non_claim") or statement)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                scenario=scenario,
                required_non_claim=pr.get("required_non_claim") or statement,
                simulated_generation=True,
                must_be_in_summary=True,
                must_be_in_verifier_report=True,
                generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def run_governance_constraint_module_generation_authorization_request_dryrun_v1(
    *,
    governance_constraint_module_generation_authorization_request_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_request_planning_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream authorization request planning verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_dryrun") is not True:
        blockers.append("upstream not ready_for_authorization_request_dryrun")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("authorization_request_planning_only") is not True:
        blockers.append("upstream must be authorization_request_planning_only")

    for flag in (
        "governance_constraint_module_generation_authorization_request_generated_now",
        "governance_constraint_module_generation_authorization_request_sent_now",
        "governance_constraint_module_generation_authorized_now",
        "governance_constraint_module_generation_authorization_grant_generated_now",
        "source_set_final_approved_now",
        "domain_specific_preservation_approved_now",
        "module_generation_authority_released_now",
        "future_verifier_integration_boundary_confirmed_now",
        "future_phase_template_integration_boundary_confirmed_now",
        "post_generation_review_executed_now",
        "module_generation_abort_authority_confirmed_now",
        "module_generation_revoke_authority_confirmed_now",
        "module_generation_rollback_authority_confirmed_now",
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "constraint_module_registered_now",
        "constraint_enforced_now",
        "verifier_integration_executed_now",
        "verifier_modified_now",
        "phase_template_modified_now",
        "automation_implemented_now",
        "documentation_auto_sync_executed_now",
        "legacy_phase_modified_now",
        "legacy_document_rewritten_now",
        "legacy_eval_out_modified_now",
        "legacy_verifier_rerun_now",
        "legacy_chain_deprecated_now",
        "main_migration_chain_resumed_now",
        "file_operation_executed_now",
        "authorization_granted_now",
        "success_claim_allowed",
        "frozen_fields_enforced_now",
        "verifier_baseline_integrated_now",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")

    if up_summary.get("legacy_as_source_evidence") is not True:
        blockers.append("upstream legacy_as_source_evidence must be true")
    if up_summary.get("legacy_as_template_source") is not False:
        blockers.append("upstream legacy_as_template_source must be false")
    if up_summary.get("domain_specific_rules_preserved") is not True:
        blockers.append("upstream domain_specific_rules_preserved must be true")
    if up_summary.get("all_not_generated_now") is not True:
        blockers.append("upstream all planned outputs must have not_generated_now=true")

    counts_ok_upstream = (
        up_summary.get("request_identity_field_count", 0) >= 12
        and up_summary.get("source_set_binding_component_count", 0) >= 12
        and up_summary.get("domain_preservation_binding_count", 0) >= 12
        and up_summary.get("scope_and_exclusion_item_count", 0) >= 13
        and up_summary.get("non_grant_statement_count", 0) >= 10
        and up_summary.get("lifecycle_state_count", 0) >= 12
        and up_summary.get("review_requirement_count", 0) >= 12
        and up_summary.get("abort_revoke_linkage_count", 0) >= 12
        and up_summary.get("verifier_usage_check_count", 0) >= 12
        and up_summary.get("non_claims_scenario_count", 0) >= 10
    )
    if not counts_ok_upstream:
        blockers.append("upstream authorization request planning coverage requirements not met")

    for flag in (
        "ready_for_governance_constraint_module_generation_authorization_request_artifact_generation",
        "ready_for_governance_constraint_module_generation_authorization_request",
        "ready_for_governance_constraint_module_generation_authorization_grant",
        "ready_for_source_set_final_approval",
        "ready_for_domain_specific_preservation_approval",
        "ready_for_module_generation_authority_release",
        "ready_for_governance_constraint_module_generation",
        "ready_for_canonical_phase_template_generation",
        "ready_for_constraint_module_registration",
        "ready_for_constraint_enforcement",
        "ready_for_verifier_integration",
        "ready_for_phase_template_modification",
        "ready_for_automation_implementation",
        "ready_for_documentation_auto_sync",
        "ready_for_legacy_document_rewrite",
        "ready_to_resume_main_migration_chain",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")

    identity_rows, identity_pass = _simulate_identity_consumption(
        up_art.get("authorization_request_identity_planning_v1.json", {})
    )
    source_rows, source_pass = _simulate_source_set_binding_consumption(
        up_art.get("authorization_request_source_set_binding_planning_v1.json", {})
    )
    domain_rows, domain_pass = _simulate_domain_preservation_consumption(
        up_art.get("authorization_request_domain_preservation_binding_planning_v1.json", {})
    )
    scope_rows, scope_pass = _simulate_scope_exclusion_consumption(
        up_art.get("authorization_request_scope_and_exclusion_planning_v1.json", {})
    )
    statement_rows, statement_pass = _simulate_statements_consumption(
        up_art.get("authorization_request_non_grant_and_non_generation_statement_planning_v1.json", {})
    )
    lifecycle_rows, lifecycle_pass = _simulate_lifecycle_consumption(
        up_art.get("authorization_request_lifecycle_planning_v1.json", {})
    )
    review_rows, review_pass = _simulate_review_requirement_consumption(
        up_art.get("authorization_request_review_requirement_planning_v1.json", {})
    )
    abort_rows, abort_pass = _simulate_abort_revoke_consumption(
        up_art.get("authorization_request_abort_revoke_linkage_planning_v1.json", {})
    )
    verifier_rows, verifier_pass = _simulate_verifier_usage_consumption(
        up_art.get("authorization_request_verifier_usage_planning_v1.json", {})
    )
    non_claims_rows, non_claims_pass = _simulate_non_claims_consumption(
        up_art.get("authorization_request_planning_non_claims_planning_v1.json", {})
    )

    sim_pass = all(
        (
            identity_pass,
            source_pass,
            domain_pass,
            scope_pass,
            statement_pass,
            lifecycle_pass,
            review_pass,
            abort_pass,
            verifier_pass,
            non_claims_pass,
        )
    )
    if not sim_pass:
        blockers.append("one or more authorization request consumption dry-run simulations failed")

    independent_ok = all(
        r.get("independent_consumption_path_required") is True and r.get("dryrun_status") == "pass"
        for r in domain_rows
    )
    if not independent_ok:
        blockers.append("independent domain preservation consumption paths must pass")

    lifecycle_ok = all(
        r.get("current_state_now") is False
        and r.get("request_sent_now") is False
        and r.get("grant_issued_now") is False
        for r in lifecycle_rows
    )
    if not lifecycle_ok:
        blockers.append("lifecycle must remain planning_defined only")

    if any(r.get("request_sent_now") for r in identity_rows + review_rows):
        blockers.append("authorization request must not be sent")
    if any(r.get("request_artifact_generated_now") for r in identity_rows + source_rows + domain_rows + scope_rows):
        blockers.append("authorization request artifact must not be generated")
    if any(r.get("source_set_final_approved_now") or r.get("source_bound_now") for r in source_rows):
        blockers.append("source set must not be final approved or bound")
    if any(r.get("approved_now") or r.get("domain_bound_now") for r in domain_rows):
        blockers.append("domain preservation must not be approved or bound")
    if any(r.get("confirmed_now") or r.get("abort_executed_now") or r.get("revoke_executed_now") for r in abort_rows):
        blockers.append("abort/revoke linkage must not be confirmed or executed")

    dryrun_ready = sim_pass and independent_ok and lifecycle_ok and not blockers
    boundary_ok = dryrun_ready

    authorization_request_dryrun_policy = _dryrun_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    authorization_request_identity_dryrun = {
        "rows": identity_rows,
        "row_count": len(identity_rows),
        "all_pass": identity_pass,
        **_dryrun_meta(),
    }
    authorization_request_source_set_binding_dryrun = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "all_pass": source_pass,
        **_dryrun_meta(),
    }
    authorization_request_domain_preservation_binding_dryrun = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        "domain_differentiation_preserved": domain_pass,
        "independent_consumption_paths_verified": independent_ok,
        **_dryrun_meta(),
    }
    authorization_request_scope_and_exclusion_dryrun = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "all_pass": scope_pass,
        **_dryrun_meta(),
    }
    authorization_request_non_grant_and_non_generation_statement_dryrun = {
        "rows": statement_rows,
        "row_count": len(statement_rows),
        "all_pass": statement_pass,
        **_dryrun_meta(),
    }
    authorization_request_lifecycle_dryrun = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_pass": lifecycle_pass,
        "lifecycle_planning_defined_only": lifecycle_ok,
        **_dryrun_meta(),
    }
    authorization_request_review_requirement_dryrun = {
        "rows": review_rows,
        "row_count": len(review_rows),
        "all_pass": review_pass,
        **_dryrun_meta(),
    }
    authorization_request_abort_revoke_linkage_dryrun = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_pass": abort_pass,
        **_dryrun_meta(),
    }
    authorization_request_verifier_usage_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    authorization_request_non_claims_dryrun = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_pass": non_claims_pass,
        **_dryrun_meta(),
    }

    authorization_request_dryrun_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_request_post_dryrun_review": boundary_ok,
        "ready_for_governance_constraint_module_generation_authorization_request_artifact_generation": False,
        "ready_for_governance_constraint_module_generation_authorization_request": False,
        "ready_for_governance_constraint_module_generation_authorization_grant": False,
        "ready_for_source_set_final_approval": False,
        "ready_for_domain_specific_preservation_approval": False,
        "ready_for_module_generation_authority_release": False,
        "ready_for_governance_constraint_module_generation": False,
        "ready_for_canonical_phase_template_generation": False,
        "ready_for_constraint_module_registration": False,
        "ready_for_constraint_enforcement": False,
        "ready_for_verifier_integration": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_legacy_document_rewrite": False,
        "ready_to_resume_main_migration_chain": False,
        "authorization_request_dryrun_completed": boundary_ok,
        "request_identity_dryrun_pass": identity_pass,
        "source_set_binding_dryrun_pass": source_pass,
        "domain_preservation_binding_dryrun_pass": domain_pass,
        "scope_and_exclusion_dryrun_pass": scope_pass,
        "non_grant_and_non_generation_statement_dryrun_pass": statement_pass,
        "request_lifecycle_dryrun_pass": lifecycle_pass,
        "request_review_requirement_dryrun_pass": review_pass,
        "abort_revoke_linkage_dryrun_pass": abort_pass,
        "verifier_usage_dryrun_pass": verifier_pass,
        "non_claims_dryrun_pass": non_claims_pass,
        "governance_constraint_module_generation_authorization_request_generated_now": False,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_request_planning_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "request_identity_field_count": len(identity_rows),
        "source_set_binding_component_count": len(source_rows),
        "domain_preservation_binding_count": len(domain_rows),
        "scope_and_exclusion_item_count": len(scope_rows),
        "non_grant_statement_count": len(statement_rows),
        "lifecycle_state_count": len(lifecycle_rows),
        "review_requirement_count": len(review_rows),
        "abort_revoke_linkage_count": len(abort_rows),
        "verifier_usage_check_count": len(verifier_rows),
        "non_claims_scenario_count": len(non_claims_rows),
        "domain_differentiation_preserved": domain_pass,
        "independent_consumption_paths_verified": independent_ok,
        "lifecycle_planning_defined_only": lifecycle_ok,
        "all_dryrun_pass": sim_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "authorization_request_dryrun_policy": authorization_request_dryrun_policy,
        "authorization_request_identity_dryrun": authorization_request_identity_dryrun,
        "authorization_request_source_set_binding_dryrun": authorization_request_source_set_binding_dryrun,
        "authorization_request_domain_preservation_binding_dryrun": authorization_request_domain_preservation_binding_dryrun,
        "authorization_request_scope_and_exclusion_dryrun": authorization_request_scope_and_exclusion_dryrun,
        "authorization_request_non_grant_and_non_generation_statement_dryrun": authorization_request_non_grant_and_non_generation_statement_dryrun,
        "authorization_request_lifecycle_dryrun": authorization_request_lifecycle_dryrun,
        "authorization_request_review_requirement_dryrun": authorization_request_review_requirement_dryrun,
        "authorization_request_abort_revoke_linkage_dryrun": authorization_request_abort_revoke_linkage_dryrun,
        "authorization_request_verifier_usage_dryrun": authorization_request_verifier_usage_dryrun,
        "authorization_request_non_claims_dryrun": authorization_request_non_claims_dryrun,
        "authorization_request_dryrun_readiness_decision": authorization_request_dryrun_readiness_decision,
    }
