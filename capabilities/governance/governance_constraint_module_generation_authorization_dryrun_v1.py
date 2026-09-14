# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization DryRun v1.

Authorization dry-run only: simulate consumption of authorization planning outputs.
Does not send authorization requests, grant authorization, or generate constraint modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_authorization_planning_v1 import (
    ABORT_ROLLBACK_AUTHORITIES,
    FUTURE_INTEGRATION_BOUNDARIES,
    GRANT_SCHEMA_FIELDS,
    INDEPENDENT_PATH_DOMAINS,
    MODULE_GENERATION_AUTHORITIES,
    NON_CLAIMS_SCENARIOS,
    POST_GENERATION_REVIEW_AUTHORITIES,
    REQUEST_SCHEMA_FIELDS,
    SOURCE_SET_COMPONENTS,
    VERIFIER_USAGE_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001"
DRYRUN_SCOPE = "governance_constraint_module_generation_authorization_dryrun_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_dryrun_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
)

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorization_planning_policy_v1.json",
    "module_generation_authorization_request_schema_planning_v1.json",
    "module_generation_authorization_grant_schema_planning_v1.json",
    "source_set_final_approval_authority_planning_v1.json",
    "domain_specific_preservation_approval_planning_v1.json",
    "module_generation_authority_planning_matrix_v1.json",
    "future_integration_boundary_planning_v1.json",
    "post_generation_review_authority_planning_v1.json",
    "module_generation_abort_and_rollback_authority_planning_v1.json",
    "module_generation_authorization_verifier_usage_planning_v1.json",
    "module_generation_authorization_non_claims_planning_v1.json",
    "governance_constraint_module_generation_authorization_planning_readiness_decision_v1.json",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "governance_constraint_module_generation_authorization_dryrun_only": True,
        "simulated": True,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "source_set_final_approved_now": False,
        "domain_specific_preservation_approved_now": False,
        "module_generation_authority_released_now": False,
        "future_verifier_integration_boundary_confirmed_now": False,
        "future_phase_template_integration_boundary_confirmed_now": False,
        "post_generation_review_executed_now": False,
        "module_generation_abort_authority_confirmed_now": False,
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
    readiness = _try_read_json(
        root / "governance_constraint_module_generation_authorization_planning_readiness_decision_v1.json"
    ) if root else None
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


def _simulate_request_schema_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("schema_field"): r for r in (planning.get("rows") or [])}
    for field, _ in REQUEST_SCHEMA_FIELDS:
        pr = planning_rows.get(field, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("must_be_present_later") is True
            and pr.get("required_for_authorization_request") is True
            and pr.get("request_sent_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                schema_field=field,
                must_be_present_later=True,
                simulated_schema_consumption=True,
                request_sent_now=False,
                authorization_request_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_grant_schema_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("schema_field"): r for r in (planning.get("rows") or [])}
    for field, _ in GRANT_SCHEMA_FIELDS:
        pr = planning_rows.get(field, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("grant_allowed_later") is True
            and pr.get("required_for_authorization_grant") is True
            and pr.get("grant_issued_now") is False
            and pr.get("authorization_granted_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                schema_field=field,
                grant_allowed_later=True,
                simulated_schema_consumption=True,
                grant_issued_now=False,
                authorization_granted_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_source_set_approval_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("source_set_component"): r for r in (planning.get("rows") or [])}
    for component in SOURCE_SET_COMPONENTS:
        pr = planning_rows.get(component, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("approval_required") is True
            and pr.get("final_approved_now") is False
            and pr.get("source_set_locked_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                source_set_component=component,
                approval_required=True,
                simulated_approval_check=True,
                final_approved_now=False,
                source_set_locked_now=False,
                source_set_mutation_allowed_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_domain_preservation_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in planning.get("rows") or []:
        name = r.get("domain_constraint_name")
        independent_path = name in INDEPENDENT_PATH_DOMAINS
        review_pass = (
            r.get("not_generated_now") is True
            and r.get("preservation_required") is True
            and r.get("flattening_forbidden") is True
            and r.get("approved_now") is False
            and r.get("domain_constraint_generated_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                domain_constraint_name=name,
                preservation_required=True,
                independent_consumption_path_required=independent_path,
                flattening_forbidden=True,
                simulated_preservation_approval_check=True,
                approved_now=False,
                domain_constraint_generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_generation_authority_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("authority_name"): r for r in (planning.get("rows") or [])}
    for name, scope in MODULE_GENERATION_AUTHORITIES:
        pr = planning_rows.get(name, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("requires_authorization_grant") is True
            and pr.get("requires_source_set_final_approval") is True
            and pr.get("requires_domain_preservation_approval") is True
            and pr.get("authorized_now") is False
            and pr.get("generated_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                authority_name=name,
                scope=scope,
                requires_authorization_grant=True,
                requires_source_set_final_approval=True,
                requires_domain_preservation_approval=True,
                simulated_authority_check=True,
                authorized_now=False,
                generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_integration_boundary_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("integration_boundary"): r for r in (planning.get("rows") or [])}
    for boundary, _ in FUTURE_INTEGRATION_BOUNDARIES:
        pr = planning_rows.get(boundary, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("allowed_in_this_phase") is False
            and pr.get("requires_separate_authorization") is True
            and pr.get("confirmed_now") is False
            and pr.get("integration_executed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                integration_boundary=boundary,
                allowed_in_this_phase=False,
                requires_separate_planning=True,
                requires_separate_authorization=True,
                simulated_boundary_check=True,
                confirmed_now=False,
                integration_executed_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _simulate_post_review_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("review_authority"): r for r in (planning.get("rows") or [])}
    for authority, _ in POST_GENERATION_REVIEW_AUTHORITIES:
        pr = planning_rows.get(authority, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("review_required_after_generation") is True
            and pr.get("confirmed_now") is False
            and pr.get("review_executed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                review_authority=authority,
                review_required_after_generation=True,
                simulated_review_authority_check=True,
                confirmed_now=False,
                review_executed_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_abort_rollback_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("authority"): r for r in (planning.get("rows") or [])}
    for authority, trigger in ABORT_ROLLBACK_AUTHORITIES:
        pr = planning_rows.get(authority, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("required_for_module_generation") is True
            and pr.get("confirmed_now") is False
            and pr.get("rollback_executed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                authority=authority,
                trigger_condition=trigger,
                authority_holder=pr.get("authority_holder") or "governance_module_generation_abort_authority",
                simulated_authority_check=True,
                confirmed_now=False,
                rollback_executed_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _simulate_verifier_usage_consumption(planning: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    planning_rows = {r.get("verifier_check_id"): r for r in (planning.get("rows") or [])}
    for check_id, check_name, _ in VERIFIER_USAGE_CHECKS:
        pr = planning_rows.get(check_id, {})
        review_pass = (
            pr.get("not_generated_now") is True
            and pr.get("planned_now") is True
            and pr.get("verifier_modified_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                verifier_check_id=check_id,
                check_name=check_name,
                simulated_verifier_usage=True,
                planned_now=True,
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
            pr.get("not_generated_now") is True
            and pr.get("planned_now") is True
            and pr.get("must_be_in_summary") is True
            and pr.get("must_be_in_verifier_report") is True
            and pr.get("generated_now") is False
            and bool(pr.get("required_non_claim") or statement)
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _dryrun_row(
                scenario=scenario,
                required_non_claim=pr.get("required_non_claim") or statement,
                simulated_generation=True,
                generated_now=False,
                dryrun_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def run_governance_constraint_module_generation_authorization_dryrun_v1(
    *,
    governance_constraint_module_generation_authorization_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_planning_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream authorization planning verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_dryrun") is not True:
        blockers.append("upstream not ready_for_authorization_dryrun")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("governance_constraint_module_generation_authorization_planning_only") is not True:
        blockers.append("upstream must be authorization_planning_only")

    for flag in (
        "governance_constraint_module_generation_authorization_request_sent_now",
        "governance_constraint_module_generation_authorized_now",
        "source_set_final_approved_now",
        "domain_specific_preservation_approved_now",
        "post_generation_review_authority_confirmed_now",
        "future_verifier_integration_boundary_confirmed_now",
        "future_phase_template_integration_boundary_confirmed_now",
        "module_generation_abort_authority_confirmed_now",
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
        up_summary.get("request_schema_field_count", 0) >= 12
        and up_summary.get("grant_schema_field_count", 0) >= 12
        and up_summary.get("source_set_component_count", 0) >= 12
        and up_summary.get("domain_preservation_count", 0) >= 12
        and up_summary.get("generation_authority_count", 0) >= 12
        and up_summary.get("future_integration_boundary_count", 0) >= 10
        and up_summary.get("post_generation_review_count", 0) >= 12
        and up_summary.get("abort_rollback_authority_count", 0) >= 12
        and up_summary.get("verifier_usage_check_count", 0) >= 12
        and up_summary.get("non_claims_scenario_count", 0) >= 10
    )
    if not counts_ok_upstream:
        blockers.append("upstream authorization planning coverage requirements not met")

    for flag in (
        "ready_for_governance_constraint_module_generation_authorization_request",
        "ready_for_governance_constraint_module_generation_authorization_grant",
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

    request_rows, request_pass = _simulate_request_schema_consumption(
        up_art.get("module_generation_authorization_request_schema_planning_v1.json", {})
    )
    grant_rows, grant_pass = _simulate_grant_schema_consumption(
        up_art.get("module_generation_authorization_grant_schema_planning_v1.json", {})
    )
    source_rows, source_pass = _simulate_source_set_approval_consumption(
        up_art.get("source_set_final_approval_authority_planning_v1.json", {})
    )
    domain_rows, domain_pass = _simulate_domain_preservation_consumption(
        up_art.get("domain_specific_preservation_approval_planning_v1.json", {})
    )
    authority_rows, authority_pass = _simulate_generation_authority_consumption(
        up_art.get("module_generation_authority_planning_matrix_v1.json", {})
    )
    integration_rows, integration_pass = _simulate_integration_boundary_consumption(
        up_art.get("future_integration_boundary_planning_v1.json", {})
    )
    review_rows, review_pass = _simulate_post_review_consumption(
        up_art.get("post_generation_review_authority_planning_v1.json", {})
    )
    abort_rows, abort_pass = _simulate_abort_rollback_consumption(
        up_art.get("module_generation_abort_and_rollback_authority_planning_v1.json", {})
    )
    verifier_rows, verifier_pass = _simulate_verifier_usage_consumption(
        up_art.get("module_generation_authorization_verifier_usage_planning_v1.json", {})
    )
    non_claims_rows, non_claims_pass = _simulate_non_claims_consumption(
        up_art.get("module_generation_authorization_non_claims_planning_v1.json", {})
    )

    sim_pass = all(
        (
            request_pass,
            grant_pass,
            source_pass,
            domain_pass,
            authority_pass,
            integration_pass,
            review_pass,
            abort_pass,
            verifier_pass,
            non_claims_pass,
        )
    )
    if not sim_pass:
        blockers.append("one or more authorization consumption dry-run simulations failed")

    independent_ok = all(
        r.get("independent_consumption_path_required") is True and r.get("dryrun_status") == "pass"
        for r in domain_rows
        if r.get("domain_constraint_name") in INDEPENDENT_PATH_DOMAINS
    )
    if not independent_ok:
        blockers.append("independent domain preservation consumption paths must pass")

    if any(r.get("request_sent_now") for r in request_rows):
        blockers.append("authorization request must not be sent")
    if any(r.get("grant_issued_now") or r.get("authorization_granted_now") for r in grant_rows):
        blockers.append("authorization grant must not be issued")
    if any(r.get("final_approved_now") for r in source_rows):
        blockers.append("source set must not be final approved")
    if any(r.get("approved_now") for r in domain_rows):
        blockers.append("domain preservation must not be approved")
    if any(r.get("authorized_now") or r.get("generated_now") for r in authority_rows):
        blockers.append("generation authority must not be released")
    if any(r.get("confirmed_now") for r in integration_rows + review_rows + abort_rows):
        blockers.append("future integration / post-review / abort authority must not be confirmed")

    dryrun_ready = sim_pass and independent_ok and not blockers
    boundary_ok = dryrun_ready

    governance_constraint_module_generation_authorization_dryrun_policy = _dryrun_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    authorization_request_schema_consumption_dryrun = {
        "rows": request_rows,
        "row_count": len(request_rows),
        "all_pass": request_pass,
        **_dryrun_meta(),
    }
    authorization_grant_schema_consumption_dryrun = {
        "rows": grant_rows,
        "row_count": len(grant_rows),
        "all_pass": grant_pass,
        **_dryrun_meta(),
    }
    source_set_final_approval_authority_dryrun = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "all_pass": source_pass,
        **_dryrun_meta(),
    }
    domain_specific_preservation_approval_dryrun = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        "domain_differentiation_preserved": domain_pass,
        "independent_consumption_paths_verified": independent_ok,
        **_dryrun_meta(),
    }
    module_generation_authority_dryrun = {
        "rows": authority_rows,
        "row_count": len(authority_rows),
        "all_pass": authority_pass,
        **_dryrun_meta(),
    }
    future_integration_boundary_dryrun = {
        "rows": integration_rows,
        "row_count": len(integration_rows),
        "all_pass": integration_pass,
        **_dryrun_meta(),
    }
    post_generation_review_authority_dryrun = {
        "rows": review_rows,
        "row_count": len(review_rows),
        "all_pass": review_pass,
        **_dryrun_meta(),
    }
    abort_and_rollback_authority_dryrun = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_pass": abort_pass,
        **_dryrun_meta(),
    }
    authorization_verifier_usage_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        "verifier_modified_now": False,
        **_dryrun_meta(),
    }
    authorization_non_claims_generation_dryrun = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_pass": non_claims_pass,
        **_dryrun_meta(),
    }

    governance_constraint_module_generation_authorization_dryrun_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_post_dryrun_review": boundary_ok,
        "ready_for_governance_constraint_module_generation_authorization_request": False,
        "ready_for_governance_constraint_module_generation_authorization_grant": False,
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
        "authorization_dryrun_completed": boundary_ok,
        "authorization_request_schema_dryrun_pass": request_pass,
        "authorization_grant_schema_dryrun_pass": grant_pass,
        "source_set_final_approval_authority_dryrun_pass": source_pass,
        "domain_specific_preservation_approval_dryrun_pass": domain_pass,
        "module_generation_authority_dryrun_pass": authority_pass,
        "future_integration_boundary_dryrun_pass": integration_pass,
        "post_generation_review_authority_dryrun_pass": review_pass,
        "abort_and_rollback_authority_dryrun_pass": abort_pass,
        "verifier_usage_dryrun_pass": verifier_pass,
        "non_claims_generation_dryrun_pass": non_claims_pass,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "source_set_final_approved_now": False,
        "domain_specific_preservation_approved_now": False,
        "governance_constraint_module_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_planning_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "request_schema_field_count": len(request_rows),
        "grant_schema_field_count": len(grant_rows),
        "source_set_component_count": len(source_rows),
        "domain_preservation_count": len(domain_rows),
        "generation_authority_count": len(authority_rows),
        "future_integration_boundary_count": len(integration_rows),
        "post_generation_review_count": len(review_rows),
        "abort_rollback_authority_count": len(abort_rows),
        "verifier_usage_check_count": len(verifier_rows),
        "non_claims_scenario_count": len(non_claims_rows),
        "domain_differentiation_preserved": domain_pass,
        "independent_consumption_paths_verified": independent_ok,
        "all_dryrun_pass": sim_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_authorization_dryrun_policy": governance_constraint_module_generation_authorization_dryrun_policy,
        "authorization_request_schema_consumption_dryrun": authorization_request_schema_consumption_dryrun,
        "authorization_grant_schema_consumption_dryrun": authorization_grant_schema_consumption_dryrun,
        "source_set_final_approval_authority_dryrun": source_set_final_approval_authority_dryrun,
        "domain_specific_preservation_approval_dryrun": domain_specific_preservation_approval_dryrun,
        "module_generation_authority_dryrun": module_generation_authority_dryrun,
        "future_integration_boundary_dryrun": future_integration_boundary_dryrun,
        "post_generation_review_authority_dryrun": post_generation_review_authority_dryrun,
        "abort_and_rollback_authority_dryrun": abort_and_rollback_authority_dryrun,
        "authorization_verifier_usage_dryrun": authorization_verifier_usage_dryrun,
        "authorization_non_claims_generation_dryrun": authorization_non_claims_generation_dryrun,
        "governance_constraint_module_generation_authorization_dryrun_readiness_decision": governance_constraint_module_generation_authorization_dryrun_readiness_decision,
    }
