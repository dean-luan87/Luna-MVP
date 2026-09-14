# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Request Planning v1.

Authorization request planning only: plan formal authorization request structure and boundaries.
Does not generate request artifacts, send requests, or grant authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_authorization_roadmap_decision_v1 import (
    SELECTED_ROUTE as UPSTREAM_SELECTED_ROUTE,
)
from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    DOMAIN_CONSTRAINTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001"
PLANNING_SCOPE = "authorization_request_planning_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_request_planning_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_AUTHORIZATION_REQUEST_PLANNING"
)

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorization_roadmap_decision_policy_v1.json",
    "completed_authorization_governance_chain_review_v1.json",
    "authorization_roadmap_route_candidate_matrix_v1.json",
    "authorization_request_planning_dependency_matrix_v1.json",
    "authorization_request_planning_scope_v1.json",
    "authorization_roadmap_non_release_matrix_v1.json",
    "authorization_request_entry_readiness_risk_matrix_v1.json",
    "authorization_roadmap_decision_non_claims_register_v1.json",
    "authorization_roadmap_readiness_decision_v1.json",
)

REQUEST_IDENTITY_FIELDS: Tuple[Tuple[str, str], ...] = (
    ("request_id format", "canonical request identifier format for future artifact"),
    ("request_phase_ref", "phase reference anchoring request to authorization chain"),
    ("requester_identity", "identity of role that may submit request later"),
    ("approver_identity", "identity of role that may approve or reject request later"),
    ("operator_acknowledgement_ref", "operator acknowledgement reference before send"),
    ("requested_scope_id", "identifier for requested module generation scope"),
    ("source_set_ref", "reference to source set binding artifact"),
    ("domain_preservation_ref", "reference to domain preservation binding artifact"),
    ("excluded_scope_ref", "reference to excluded scope declaration"),
    ("non_grant_statement_ref", "reference to non-grant statement block"),
    ("non_generation_statement_ref", "reference to non-generation statement block"),
    ("request_lifecycle_ref", "reference to request lifecycle state machine"),
)

SOURCE_SET_BINDING_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("legacy chain inventory", "legacy_as_source_evidence"),
    ("phase-to-constraint mapping", "constraint_mapping_integrity"),
    ("canonical frozen field extraction", "frozen_field_shape"),
    ("phase lifecycle extraction", "lifecycle_shape"),
    ("domain constraint extraction", "domain_registry_shape"),
    ("generation planning output shape", "generation_planning_eval_out"),
    ("generation dry-run consumption result", "generation_dryrun_eval_out"),
    ("generation post-review result", "generation_post_review_eval_out"),
    ("authorization planning result", "authorization_planning_eval_out"),
    ("authorization dry-run result", "authorization_dryrun_eval_out"),
    ("authorization post-review result", "authorization_post_review_eval_out"),
    ("authorization roadmap decision result", "authorization_roadmap_decision_eval_out"),
)

SCOPE_AND_EXCLUSION_ITEMS: Tuple[Tuple[str, str, str], ...] = (
    ("requested module generation only", "requested", "only formal module outputs in requested scope"),
    ("source set approval not included", "excluded", "source set final approval is separate gate"),
    ("domain preservation approval not included", "excluded", "domain preservation approval is separate gate"),
    ("verifier integration excluded", "excluded", "verifier integration not in request scope"),
    ("phase template modification excluded", "excluded", "phase template modification not in request scope"),
    ("canonical phase template generation excluded", "excluded", "canonical template generation not in request scope"),
    ("automation implementation excluded", "excluded", "automation not in request scope"),
    ("documentation auto sync excluded", "excluded", "documentation auto sync not in request scope"),
    ("legacy document rewrite excluded", "excluded", "legacy document rewrite not in request scope"),
    ("main migration resume excluded", "excluded", "mainline resume not in request scope"),
    ("real migration excluded", "excluded", "real migration not in request scope"),
    ("rollback rehearsal excluded", "excluded", "rollback rehearsal not in request scope"),
    ("batch arming excluded", "excluded", "batch arming not in request scope"),
)

NON_GRANT_NON_GENERATION_STATEMENTS: Tuple[Tuple[str, str, str], ...] = (
    ("NG01", "request planning does not generate request", "request artifact mistaken as existing"),
    ("NG02", "request artifact does not mean request sent", "planning GO misread as request sent"),
    ("NG03", "request sent does not mean grant issued", "request sent misread as authorization granted"),
    ("NG04", "request sent does not approve source set", "source set final approval conflated with request"),
    ("NG05", "request sent does not approve domain preservation", "domain approval conflated with request"),
    ("NG06", "request sent does not release generation authority", "authority release conflated with request"),
    ("NG07", "request sent does not allow module generation", "module generation conflated with request"),
    ("NG08", "request sent does not allow verifier integration", "verifier integration conflated with request"),
    ("NG09", "request sent does not allow phase template modification", "template modification conflated with request"),
    ("NG10", "request sent does not resume mainline", "mainline resume conflated with request"),
)

LIFECYCLE_STATES: Tuple[Tuple[str, str, Tuple[str, ...], Tuple[str, ...]], ...] = (
    ("planned", "request structure planned only", (), ("request_sent", "grant_issued")),
    ("draft_candidate", "draft request candidate not materialized", ("planned",), ("request_sent", "grant_issued")),
    ("review_pending", "review pending before send", ("draft_candidate",), ("request_sent",)),
    ("request_ready", "ready to send after reviews", ("review_pending",), ("grant_issued",)),
    ("request_sent", "request transmitted to approver", ("request_ready",), ()),
    ("request_acknowledged", "request acknowledged by approver", ("request_sent",), ()),
    ("request_rejected", "request rejected", ("request_sent",), ("grant_issued",)),
    ("request_expired", "request expired", ("request_sent",), ("grant_issued",)),
    ("request_revoked", "request revoked", ("request_sent",), ("grant_issued",)),
    ("request_superseded", "request superseded", ("request_sent",), ("grant_issued",)),
    ("grant_pending", "grant decision pending", ("request_acknowledged",), ()),
    ("grant_issued", "authorization grant issued", ("grant_pending",), ()),
)

REVIEW_REQUIREMENTS: Tuple[str, ...] = (
    "request identity review",
    "source set binding review",
    "domain preservation binding review",
    "requested scope review",
    "excluded scope review",
    "non-grant statement review",
    "non-generation statement review",
    "lifecycle review",
    "abort linkage review",
    "revoke linkage review",
    "verifier usage review",
    "non-claims review",
)

ABORT_REVOKE_LINKAGES: Tuple[Tuple[str, str, str], ...] = (
    ("planning abort", "abort during request planning", "governance_authorization_request_planner"),
    ("draft request abort", "abort draft request preparation", "governance_authorization_request_planner"),
    ("request ready abort", "abort before request sent", "governance_authorization_request_approver"),
    ("request sent revoke", "revoke after request sent", "governance_authorization_request_approver"),
    ("source set conflict revoke", "source set conflict detected", "governance_source_set_approver"),
    ("domain preservation conflict revoke", "domain preservation conflict", "governance_domain_preservation_approver"),
    ("scope conflict revoke", "requested scope conflict", "governance_authorization_request_approver"),
    ("stale request revoke", "request stale or expired", "governance_authorization_request_approver"),
    ("superseded request revoke", "request superseded by newer request", "governance_authorization_request_approver"),
    ("grant mismatch revoke", "grant scope mismatch", "governance_authorization_grant_issuer"),
    ("module generation precondition failure revoke", "preconditions for generation not met", "governance_module_generation_authorizer"),
    ("mainline resume conflict revoke", "mainline resume conflict", "governance_mainline_resume_authority"),
)

VERIFIER_USAGE_CHECKS: Tuple[Tuple[str, str, str], ...] = (
    ("AR01", "request planning only check", "authorization_request_planning_only != true"),
    ("AR02", "request artifact not generated check", "governance_constraint_module_generation_authorization_request_generated_now != false"),
    ("AR03", "request not sent check", "governance_constraint_module_generation_authorization_request_sent_now != false"),
    ("AR04", "grant not issued check", "governance_constraint_module_generation_authorized_now != false"),
    ("AR05", "source set not final approved check", "source_set_final_approved_now != false"),
    ("AR06", "domain preservation not approved check", "domain_specific_preservation_approved_now != false"),
    ("AR07", "generation authority not released check", "module_generation_authority_released_now != false"),
    ("AR08", "request lifecycle state check", "current lifecycle state must not be request_sent or grant_issued"),
    ("AR09", "excluded scope check", "excluded scope must not be activated in request planning phase"),
    ("AR10", "non-grant statement check", "non-grant statements must be present in summary and verifier"),
    ("AR11", "non-generation statement check", "non-generation statements must block module generation claims"),
    ("AR12", "mainline not resumed check", "main_migration_chain_resumed_now != false"),
)

NON_CLAIMS_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("Request Planning GO", "Request Planning GO does not mean request artifact is generated."),
    ("Request not sent", "Request Planning GO does not mean request is sent."),
    ("Authorization not granted", "Request Planning GO does not mean authorization is granted."),
    ("Source set not approved", "Request Planning GO does not mean source set is final approved."),
    ("Domain not approved", "Request Planning GO does not mean domain preservation is approved."),
    ("Authority not released", "Request Planning GO does not mean module generation authority is released."),
    ("Module not generated", "Request Planning GO does not mean Governance Constraint Module may be generated."),
    ("Verifier integration", "Request Planning GO does not mean verifier/template integration may start."),
    ("Mainline not resumed", "Request Planning GO does not mean main migration chain may resume."),
    ("Real execution blocked", "Request Planning GO does not mean real migration / rollback / batch arming is allowed."),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "authorization_request_planning_only": True,
        "governance_constraint_module_generation_authorization_request_planning_selected": True,
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
    readiness = _try_read_json(root / "authorization_roadmap_readiness_decision_v1.json") if root else None
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


def _build_identity_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            identity_field=field,
            why_required=why,
            required_for_request_artifact=True,
            must_be_present_later=True,
            request_artifact_generated_now=False,
            request_sent_now=False,
        )
        for field, why in REQUEST_IDENTITY_FIELDS
    ]


def _build_source_set_binding() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            source_component=component,
            binding_required=True,
            source_evidence_role=role,
            source_integrity_requirement="must remain legacy_as_source_evidence only",
            source_set_final_approved_now=False,
            source_bound_now=False,
            request_artifact_generated_now=False,
        )
        for component, role in SOURCE_SET_BINDING_COMPONENTS
    ]


def _build_domain_preservation_binding() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for name, _, _, _ in DOMAIN_CONSTRAINTS:
        rows.append(
            _planning_row(
                domain_constraint_name=name,
                binding_required=True,
                independent_consumption_path_required=True,
                flattening_forbidden=True,
                approval_required_later=True,
                approved_now=False,
                request_artifact_generated_now=False,
            )
        )
    return rows


def _build_scope_exclusion() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            scope_item=item,
            scope_type=scope_type,
            why_included_or_excluded=why,
            allowed_by_request_later=(scope_type == "requested"),
            allowed_now=False,
            request_artifact_generated_now=False,
        )
        for item, scope_type, why in SCOPE_AND_EXCLUSION_ITEMS
    ]


def _build_non_grant_statements() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            statement_id=sid,
            statement=statement,
            risk_if_missing=risk,
            must_be_in_request_later=True,
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            generated_now=False,
        )
        for sid, statement, risk in NON_GRANT_NON_GENERATION_STATEMENTS
    ]


def _build_lifecycle_planning() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            lifecycle_state=state,
            canonical_meaning=meaning,
            allowed_transitions=list(allowed),
            forbidden_transitions=list(forbidden),
            current_state_now=False,
            planning_defined_only=True,
            request_sent_now=False,
            grant_issued_now=False,
        )
        for state, meaning, allowed, forbidden in LIFECYCLE_STATES
    ]


def _build_review_requirements() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            review_requirement=req,
            review_required_before_request_sent=True,
            reviewer_role="governance_authorization_request_reviewer",
            review_executed_now=False,
            request_ready_now=False,
            request_sent_now=False,
        )
        for req in REVIEW_REQUIREMENTS
    ]


def _build_abort_revoke_linkage() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            linkage_type=linkage,
            trigger_condition=trigger,
            authority_holder=holder,
            required_before_request_sent=True,
            confirmed_now=False,
            abort_executed_now=False,
            revoke_executed_now=False,
        )
        for linkage, trigger, holder in ABORT_REVOKE_LINKAGES
    ]


def _build_verifier_usage() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            verifier_check_id=check_id,
            check_name=check_name,
            required_fields=["authorization_request_planning_only"],
            failure_condition=failure,
            severity="critical",
            planned_now=True,
            verifier_modified_now=False,
        )
        for check_id, check_name, failure in VERIFIER_USAGE_CHECKS
    ]


def _build_non_claims() -> List[Dict[str, Any]]:
    return [
        _planning_row(
            scenario=scenario,
            required_non_claim=statement,
            risk_if_missing="request planning GO misread as permission release",
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            planned_now=True,
            generated_now=False,
        )
        for scenario, statement in NON_CLAIMS_SCENARIOS
    ]


def run_governance_constraint_module_generation_authorization_request_planning_v1(
    *,
    governance_constraint_module_generation_authorization_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_roadmap_decision_root)
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
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_planning") is not True:
        blockers.append("upstream not ready_for_authorization_request_planning")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("selected_route") != UPSTREAM_SELECTED_ROUTE:
        blockers.append(f"upstream selected_route must be {UPSTREAM_SELECTED_ROUTE}")
    if up_summary.get("governance_constraint_module_generation_authorization_request_planning_selected") is not True:
        blockers.append("upstream governance_constraint_module_generation_authorization_request_planning_selected must be true")

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

    for flag in (
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

    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    identity_rows = _build_identity_planning()
    source_rows = _build_source_set_binding()
    domain_rows = _build_domain_preservation_binding()
    scope_rows = _build_scope_exclusion()
    statement_rows = _build_non_grant_statements()
    lifecycle_rows = _build_lifecycle_planning()
    review_rows = _build_review_requirements()
    abort_rows = _build_abort_revoke_linkage()
    verifier_rows = _build_verifier_usage()
    non_claims_rows = _build_non_claims()

    all_row_lists = (
        identity_rows,
        source_rows,
        domain_rows,
        scope_rows,
        statement_rows,
        lifecycle_rows,
        review_rows,
        abort_rows,
        verifier_rows,
        non_claims_rows,
    )
    if any(not all(r.get("not_generated_now") for r in rows) for rows in all_row_lists):
        blockers.append("all planned outputs must have not_generated_now=true")

    counts_ok = (
        len(identity_rows) >= 12
        and len(source_rows) >= 12
        and len(domain_rows) >= 12
        and len(scope_rows) >= 13
        and len(statement_rows) >= 10
        and len(lifecycle_rows) >= 12
        and len(review_rows) >= 12
        and len(abort_rows) >= 12
        and len(verifier_rows) >= 12
        and len(non_claims_rows) >= 10
    )
    if not counts_ok:
        blockers.append("authorization request planning coverage requirements not met")

    lifecycle_ok = all(
        r.get("current_state_now") is False
        and r.get("request_sent_now") is False
        and r.get("grant_issued_now") is False
        for r in lifecycle_rows
    )
    if not lifecycle_ok:
        blockers.append("lifecycle must remain planning_defined only")

    planning_ready = counts_ok and lifecycle_ok and not blockers
    boundary_ok = planning_ready

    authorization_request_planning_policy = _planning_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    authorization_request_identity_planning = {
        "rows": identity_rows,
        "row_count": len(identity_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in identity_rows),
        **_planning_meta(),
    }
    authorization_request_source_set_binding_planning = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in source_rows),
        **_planning_meta(),
    }
    authorization_request_domain_preservation_binding_planning = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in domain_rows),
        **_planning_meta(),
    }
    authorization_request_scope_and_exclusion_planning = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in scope_rows),
        **_planning_meta(),
    }
    authorization_request_non_grant_and_non_generation_statement_planning = {
        "rows": statement_rows,
        "row_count": len(statement_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in statement_rows),
        **_planning_meta(),
    }
    authorization_request_lifecycle_planning = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in lifecycle_rows),
        "lifecycle_planning_defined_only": True,
        **_planning_meta(),
    }
    authorization_request_review_requirement_planning = {
        "rows": review_rows,
        "row_count": len(review_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in review_rows),
        **_planning_meta(),
    }
    authorization_request_abort_revoke_linkage_planning = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in abort_rows),
        **_planning_meta(),
    }
    authorization_request_verifier_usage_planning = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in verifier_rows),
        **_planning_meta(),
    }
    authorization_request_planning_non_claims_planning = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_not_generated_now": all(r.get("not_generated_now") for r in non_claims_rows),
        **_planning_meta(),
    }

    authorization_request_planning_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_request_dryrun": boundary_ok,
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
        "authorization_request_planning_completed": boundary_ok,
        "request_identity_planned": len(identity_rows) >= 12,
        "source_set_binding_planned": len(source_rows) >= 12,
        "domain_preservation_binding_planned": len(domain_rows) >= 12,
        "scope_and_exclusion_planned": len(scope_rows) >= 13,
        "non_grant_and_non_generation_statement_planned": len(statement_rows) >= 10,
        "request_lifecycle_planned": len(lifecycle_rows) >= 12,
        "request_review_requirement_planned": len(review_rows) >= 12,
        "abort_revoke_linkage_planned": len(abort_rows) >= 12,
        "verifier_usage_planned": len(verifier_rows) >= 12,
        "non_claims_planned": len(non_claims_rows) >= 10,
        "governance_constraint_module_generation_authorization_request_generated_now": False,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
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
        "all_authorization_request_planning_complete": counts_ok,
        "all_not_generated_now": all(
            r.get("not_generated_now") for rows in all_row_lists for r in rows
        ),
        "lifecycle_planning_defined_only": lifecycle_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "authorization_request_planning_policy": authorization_request_planning_policy,
        "authorization_request_identity_planning": authorization_request_identity_planning,
        "authorization_request_source_set_binding_planning": authorization_request_source_set_binding_planning,
        "authorization_request_domain_preservation_binding_planning": authorization_request_domain_preservation_binding_planning,
        "authorization_request_scope_and_exclusion_planning": authorization_request_scope_and_exclusion_planning,
        "authorization_request_non_grant_and_non_generation_statement_planning": authorization_request_non_grant_and_non_generation_statement_planning,
        "authorization_request_lifecycle_planning": authorization_request_lifecycle_planning,
        "authorization_request_review_requirement_planning": authorization_request_review_requirement_planning,
        "authorization_request_abort_revoke_linkage_planning": authorization_request_abort_revoke_linkage_planning,
        "authorization_request_verifier_usage_planning": authorization_request_verifier_usage_planning,
        "authorization_request_planning_non_claims_planning": authorization_request_planning_non_claims_planning,
        "authorization_request_planning_readiness_decision": authorization_request_planning_readiness_decision,
    }
