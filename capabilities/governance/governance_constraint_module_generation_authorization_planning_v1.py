# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Planning v1.

Authorization planning only: plan module generation authorization mechanisms.
Does not send authorization requests, grant authorization, or generate constraint modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_roadmap_decision_v1 import (
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
)
from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    DOMAIN_CONSTRAINTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001"
PLANNING_SCOPE = "governance_constraint_module_generation_authorization_planning_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_planning_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_ROADMAP_DECISION_READY_FOR_GENERATION_AUTHORIZATION_PLANNING"
)

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_roadmap_decision_policy_v1.json",
    "completed_governance_constraint_module_generation_chain_review_v1.json",
    "governance_constraint_module_generation_roadmap_route_candidate_matrix_v1.json",
    "governance_constraint_module_generation_authorization_dependency_matrix_v1.json",
    "governance_constraint_module_generation_authorization_planning_scope_v1.json",
    "governance_constraint_module_generation_roadmap_non_release_matrix_v1.json",
    "governance_constraint_module_authorization_entry_readiness_risk_matrix_v1.json",
    "governance_constraint_module_generation_roadmap_decision_non_claims_register_v1.json",
    "governance_constraint_module_generation_roadmap_readiness_decision_v1.json",
)

REQUEST_SCHEMA_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("request identity", "unique authorization request identifier"),
    ("requested module outputs", "list of formal module artifacts requested for generation"),
    ("source evidence set", "legacy + generation chain source evidence references"),
    ("source set approval requirement", "source set must be final approved before grant"),
    ("domain preservation requirement", "domain-specific rules must be preservation-approved"),
    ("generation boundary statement", "explicit non-generation and planning-only boundary"),
    ("non-generation non-claim", "request schema planned ≠ module generated"),
    ("requester role", "role that may submit authorization request later"),
    ("approver role", "role that may grant authorization later"),
    ("operator acknowledgement requirement", "operator ack required before generation"),
    ("abort authority requirement", "abort authority must be declared in request"),
    ("rollback authority requirement", "rollback authority must be declared in request"),
)

GRANT_SCHEMA_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("grant identity", "unique authorization grant identifier"),
    ("granted scope", "explicit module outputs authorized for generation"),
    ("excluded scope", "template/verifier/automation/mainline excluded from grant"),
    ("source set final approval status", "must reference final approved source set"),
    ("domain-specific preservation approval status", "must reference preservation approval"),
    ("generation permission boundary", "generation allowed only within declared scope"),
    ("post-generation review requirement", "review required before enforcement"),
    ("verifier integration exclusion", "verifier integration not included in grant"),
    ("phase template modification exclusion", "phase template modification not included"),
    ("automation exclusion", "automation not included in grant"),
    ("expiration / TTL", "grant must have expiration semantics"),
    ("revocation rule", "grant may be revoked under declared conditions"),
)

SOURCE_SET_COMPONENTS: Tuple[str, ...] = (
    "legacy chain inventory",
    "phase-to-constraint mapping",
    "frozen field extraction",
    "phase lifecycle extraction",
    "domain constraint extraction",
    "inheritance policy",
    "legacy absorption policy",
    "generation planning output shape",
    "generation dry-run consumption results",
    "generation post-review results",
    "non-claims / forbidden shortcut library",
    "verifier baseline shape",
)

INDEPENDENT_PATH_DOMAINS: Tuple[str, ...] = (
    "Evidence Chain",
    "Owner/Operator Approval",
    "Boundary Object Registry",
    "Registry Generation",
    "Protected Asset / HR / DnAE",
    "File Operation",
)

MODULE_GENERATION_AUTHORITIES: Tuple[Tuple[str, str], ...] = (
    ("canonical contract generation authority", "governance_canonical_phase_contract_v1.json"),
    ("domain registry generation authority", "governance_domain_constraint_registry_v1.json"),
    ("phase inheritance matrix generation authority", "governance_phase_inheritance_matrix_v1.json"),
    ("frozen fields library generation authority", "governance_canonical_frozen_fields_v1.json"),
    ("phase lifecycle contract generation authority", "governance_phase_mode_lifecycle_contract_v1.json"),
    ("required fields schema generation authority", "governance_constraint_required_fields_v1.json"),
    ("verifier baseline generation authority", "governance_constraint_verifier_baseline_v1.json"),
    ("non-claims library generation authority", "governance_constraint_non_claims_library_v1.json"),
    ("forbidden shortcut library generation authority", "governance_constraint_forbidden_shortcut_library_v1.json"),
    ("extension rule generation authority", "governance_constraint_extension_rule_v1.json"),
    ("legacy absorption policy generation authority", "governance_legacy_absorption_policy_v1.json"),
    ("readiness decision generation authority", "governance_constraint_module_readiness_decision_v1.json"),
)

FUTURE_INTEGRATION_BOUNDARIES: Tuple[Tuple[str, str], ...] = (
    ("future verifier integration boundary", "verifier may load constraint module only after separate authorization"),
    ("future verifier modification boundary", "verifier modification requires separate authorization"),
    ("future phase template integration boundary", "phase template may reference module only after separate authorization"),
    ("future phase template modification boundary", "phase template modification requires separate authorization"),
    ("future Cursor instruction reference boundary", "Cursor instruction may reference module only after planning chain complete"),
    ("future automation boundary", "automation requires separate authorization"),
    ("future documentation sync boundary", "documentation auto sync requires separate authorization"),
    ("future mainline phase consumption boundary", "mainline phases may consume module only after authorization chain complete"),
    ("future legacy absorption note boundary", "absorption notes require separate planning; no legacy rewrite"),
    ("future migration resume boundary", "main migration resume requires separate authorization"),
)

POST_GENERATION_REVIEW_AUTHORITIES: Tuple[Tuple[str, str], ...] = (
    ("module output completeness review", "all 12 formal module outputs present and complete"),
    ("canonical contract review", "governance_canonical_phase_contract_v1.json review"),
    ("domain registry review", "governance_domain_constraint_registry_v1.json review"),
    ("domain preservation review", "domain-specific rules not flattened"),
    ("frozen fields review", "governance_canonical_frozen_fields_v1.json review"),
    ("lifecycle contract review", "governance_phase_mode_lifecycle_contract_v1.json review"),
    ("required fields review", "governance_constraint_required_fields_v1.json review"),
    ("verifier baseline review", "governance_constraint_verifier_baseline_v1.json review"),
    ("non-claims library review", "non-claims and forbidden shortcut libraries review"),
    ("extension rule review", "governance_constraint_extension_rule_v1.json review"),
    ("legacy absorption policy review", "governance_legacy_absorption_policy_v1.json review"),
    ("non-enforcement review", "module generated ≠ constraint enforced"),
)

ABORT_ROLLBACK_AUTHORITIES: Tuple[Tuple[str, str], ...] = (
    ("authorization request abort", "abort pending authorization request"),
    ("authorization grant revoke", "revoke issued authorization grant"),
    ("source set approval abort", "abort source set final approval process"),
    ("domain preservation approval abort", "abort domain preservation approval process"),
    ("module generation abort", "abort module generation in progress"),
    ("generated module quarantine", "quarantine generated module pending review"),
    ("generated module rollback", "rollback generated module artifacts"),
    ("constraint enforcement rollback", "rollback constraint enforcement if attempted"),
    ("verifier integration rollback", "rollback verifier integration if attempted"),
    ("phase template integration rollback", "rollback phase template changes if attempted"),
    ("documentation sync rollback", "rollback documentation sync if attempted"),
    ("mainline resume rollback", "rollback mainline resume if attempted"),
)

VERIFIER_USAGE_CHECKS: Tuple[Tuple[str, str, str], ...] = (
    ("AV01", "authorization planning only check", "governance_constraint_module_generation_authorization_planning_only != true"),
    ("AV02", "request not sent check", "governance_constraint_module_generation_authorization_request_sent_now != false"),
    ("AV03", "grant not issued check", "governance_constraint_module_generation_authorized_now != false"),
    ("AV04", "module not generated check", "governance_constraint_module_generated_now != false"),
    ("AV05", "source set not final approved check", "source_set_final_approved_now != false"),
    ("AV06", "domain preservation not approved check", "domain_specific_preservation_approved_now != false"),
    ("AV07", "generation authority not released check", "authorization_granted_now != false"),
    ("AV08", "future integration not executed check", "verifier_integration_executed_now != false"),
    ("AV09", "post-generation review not executed check", "post_generation_review_authority_confirmed_now != false"),
    ("AV10", "abort authority not confirmed check", "module_generation_abort_authority_confirmed_now != false"),
    ("AV11", "rollback authority not confirmed check", "module_generation_rollback_authority_confirmed_now != false"),
    ("AV12", "mainline not resumed check", "main_migration_chain_resumed_now != false"),
)

NON_CLAIMS_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("Authorization Planning GO", "Authorization Planning GO does not mean authorization request is sent."),
    ("Authorization not granted", "Authorization Planning GO does not mean authorization is granted."),
    ("Module generation not allowed", "Authorization Planning GO does not mean module generation is allowed."),
    ("Source set not final approved", "Source set approval planned does not mean source set is final approved."),
    ("Domain registry not generated", "Domain preservation approval planned does not mean domain registry is generated."),
    ("Generation authority not released", "Generation authority planned does not mean generation authority released."),
    ("Future integration not executed", "Future integration boundary planned does not mean verifier/template integration executed."),
    ("Post-generation review not executed", "Post-generation review authority planned does not mean review executed."),
    ("Rollback not executed", "Abort/rollback authority planned does not mean rollback executed."),
    ("Mainline not resumed", "Authorization Planning GO does not mean mainline may resume."),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "governance_constraint_module_generation_authorization_planning_only": True,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "source_set_final_approved_now": False,
        "domain_specific_preservation_approved_now": False,
        "post_generation_review_authority_confirmed_now": False,
        "future_verifier_integration_boundary_confirmed_now": False,
        "future_phase_template_integration_boundary_confirmed_now": False,
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


def _planning_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta(), "not_generated_now": True}


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
        root / "governance_constraint_module_generation_roadmap_readiness_decision_v1.json"
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


def _build_request_schema_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            schema_field=field,
            why_required=why,
            required_for_authorization_request=True,
            must_be_present_later=True,
            request_sent_now=False,
        )
        for field, why in REQUEST_SCHEMA_FIELDS
    ]


def _build_grant_schema_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            schema_field=field,
            why_required=why,
            required_for_authorization_grant=True,
            grant_allowed_later=True,
            grant_issued_now=False,
            authorization_granted_now=False,
        )
        for field, why in GRANT_SCHEMA_FIELDS
    ]


def _build_source_set_approval_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            source_set_component=component,
            approval_required=True,
            approver_role="governance_module_generation_authorizer",
            final_approved_now=False,
            source_set_locked_now=False,
            source_set_mutation_allowed_now=False,
        )
        for component in SOURCE_SET_COMPONENTS
    ]


def _build_domain_preservation_planning() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for name, _, _, _ in DOMAIN_CONSTRAINTS:
        rows.append(
            _planning_row(
                domain_constraint_name=name,
                preservation_required=True,
                independent_consumption_path_required=name in INDEPENDENT_PATH_DOMAINS,
                flattening_forbidden=True,
                approval_required=True,
                approved_now=False,
                domain_constraint_generated_now=False,
            )
        )
    return rows


def _build_generation_authority_matrix() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            authority_name=name,
            scope=artifact,
            requires_authorization_grant=True,
            requires_source_set_final_approval=True,
            requires_domain_preservation_approval=True,
            authorized_now=False,
            generated_now=False,
        )
        for name, artifact in MODULE_GENERATION_AUTHORITIES
    ]


def _build_future_integration_boundary_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            integration_boundary=boundary,
            why_required=why,
            allowed_in_this_phase=False,
            requires_separate_planning=True,
            requires_separate_authorization=True,
            confirmed_now=False,
            integration_executed_now=False,
        )
        for boundary, why in FUTURE_INTEGRATION_BOUNDARIES
    ]


def _build_post_generation_review_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            review_authority=authority,
            review_required_after_generation=True,
            review_scope=scope,
            reviewer_role="governance_module_generation_reviewer",
            confirmed_now=False,
            review_executed_now=False,
        )
        for authority, scope in POST_GENERATION_REVIEW_AUTHORITIES
    ]


def _build_abort_rollback_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            authority=authority,
            trigger_condition=trigger,
            authority_holder="governance_module_generation_abort_authority",
            required_for_module_generation=True,
            confirmed_now=False,
            rollback_executed_now=False,
        )
        for authority, trigger in ABORT_ROLLBACK_AUTHORITIES
    ]


def _build_verifier_usage_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            verifier_check_id=check_id,
            check_name=check_name,
            required_fields=["governance_constraint_module_generation_authorization_planning_only"],
            failure_condition=failure,
            severity="critical",
            planned_now=True,
        )
        for check_id, check_name, failure in VERIFIER_USAGE_CHECKS
    ]


def _build_non_claims_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            scenario=scenario,
            required_non_claim=statement,
            risk_if_missing="authorization planning GO misread as permission release",
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            planned_now=True,
            generated_now=False,
        )
        for scenario, statement in NON_CLAIMS_SCENARIOS
    ]


def run_governance_constraint_module_generation_authorization_planning_v1(
    *,
    governance_constraint_module_generation_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream roadmap decision verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_planning") is not True:
        blockers.append("upstream not ready_for_authorization_planning")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("selected_route") != UPSTREAM_SELECTED_ROUTE:
        blockers.append(f"upstream selected_route must be {UPSTREAM_SELECTED_ROUTE}")
    if up_summary.get("governance_constraint_module_generation_authorization_planning_selected") is not True:
        blockers.append("upstream governance_constraint_module_generation_authorization_planning_selected must be true")

    for flag in (
        "governance_constraint_module_generation_authorization_request_sent_now",
        "governance_constraint_module_generation_authorized_now",
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

    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    request_rows = _build_request_schema_planning()
    grant_rows = _build_grant_schema_planning()
    source_rows = _build_source_set_approval_planning()
    domain_rows = _build_domain_preservation_planning()
    authority_rows = _build_generation_authority_matrix()
    integration_rows = _build_future_integration_boundary_planning()
    review_rows = _build_post_generation_review_planning()
    abort_rows = _build_abort_rollback_planning()
    verifier_rows = _build_verifier_usage_planning()
    non_claims_rows = _build_non_claims_planning()

    all_rows = (
        request_rows,
        grant_rows,
        source_rows,
        domain_rows,
        authority_rows,
        integration_rows,
        review_rows,
        abort_rows,
        verifier_rows,
        non_claims_rows,
    )
    if any(not all(r.get("not_generated_now") for r in rows) for rows in all_rows):
        blockers.append("all planned outputs must have not_generated_now=true")

    counts_ok = (
        len(request_rows) >= 12
        and len(grant_rows) >= 12
        and len(source_rows) >= 12
        and len(domain_rows) >= 12
        and len(authority_rows) >= 12
        and len(integration_rows) >= 10
        and len(review_rows) >= 12
        and len(abort_rows) >= 12
        and len(verifier_rows) >= 12
        and len(non_claims_rows) >= 10
    )
    if not counts_ok:
        blockers.append("authorization planning coverage requirements not met")

    planning_ready = counts_ok and not blockers
    boundary_ok = planning_ready

    governance_constraint_module_generation_authorization_planning_policy = _planning_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    module_generation_authorization_request_schema_planning = {
        "rows": request_rows,
        "row_count": len(request_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in request_rows),
        **_planning_meta(),
    }
    module_generation_authorization_grant_schema_planning = {
        "rows": grant_rows,
        "row_count": len(grant_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in grant_rows),
        **_planning_meta(),
    }
    source_set_final_approval_authority_planning = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in source_rows),
        **_planning_meta(),
    }
    domain_specific_preservation_approval_planning = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in domain_rows),
        **_planning_meta(),
    }
    module_generation_authority_planning_matrix = {
        "rows": authority_rows,
        "row_count": len(authority_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in authority_rows),
        **_planning_meta(),
    }
    future_integration_boundary_planning = {
        "rows": integration_rows,
        "row_count": len(integration_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in integration_rows),
        **_planning_meta(),
    }
    post_generation_review_authority_planning = {
        "rows": review_rows,
        "row_count": len(review_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in review_rows),
        **_planning_meta(),
    }
    module_generation_abort_and_rollback_authority_planning = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in abort_rows),
        **_planning_meta(),
    }
    module_generation_authorization_verifier_usage_planning = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in verifier_rows),
        **_planning_meta(),
    }
    module_generation_authorization_non_claims_planning = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in non_claims_rows),
        **_planning_meta(),
    }

    governance_constraint_module_generation_authorization_planning_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_dryrun": boundary_ok,
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
        "authorization_planning_completed": boundary_ok,
        "authorization_request_schema_planned": len(request_rows) >= 12,
        "authorization_grant_schema_planned": len(grant_rows) >= 12,
        "source_set_final_approval_authority_planned": len(source_rows) >= 12,
        "domain_specific_preservation_approval_planned": len(domain_rows) >= 12,
        "module_generation_authority_planned": len(authority_rows) >= 12,
        "future_integration_boundary_planned": len(integration_rows) >= 10,
        "post_generation_review_authority_planned": len(review_rows) >= 12,
        "abort_and_rollback_authority_planned": len(abort_rows) >= 12,
        "verifier_usage_planned": len(verifier_rows) >= 12,
        "non_claims_planned": len(non_claims_rows) >= 10,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
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
        "all_authorization_planning_complete": counts_ok,
        "all_not_generated_now": all(
            r.get("not_generated_now")
            for rows in all_rows
            for r in rows
        ),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_authorization_planning_policy": governance_constraint_module_generation_authorization_planning_policy,
        "module_generation_authorization_request_schema_planning": module_generation_authorization_request_schema_planning,
        "module_generation_authorization_grant_schema_planning": module_generation_authorization_grant_schema_planning,
        "source_set_final_approval_authority_planning": source_set_final_approval_authority_planning,
        "domain_specific_preservation_approval_planning": domain_specific_preservation_approval_planning,
        "module_generation_authority_planning_matrix": module_generation_authority_planning_matrix,
        "future_integration_boundary_planning": future_integration_boundary_planning,
        "post_generation_review_authority_planning": post_generation_review_authority_planning,
        "module_generation_abort_and_rollback_authority_planning": module_generation_abort_and_rollback_authority_planning,
        "module_generation_authorization_verifier_usage_planning": module_generation_authorization_verifier_usage_planning,
        "module_generation_authorization_non_claims_planning": module_generation_authorization_non_claims_planning,
        "governance_constraint_module_generation_authorization_planning_readiness_decision": governance_constraint_module_generation_authorization_planning_readiness_decision,
    }
