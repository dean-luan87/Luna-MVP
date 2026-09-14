# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Request Post-DryRun Review v1.

Post-dryrun review only: audit authorization request dry-run completeness and non-execution.
Does not generate request artifacts, send requests, or grant authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_authorization_request_planning_v1 import (
    ABORT_REVOKE_LINKAGES,
    LIFECYCLE_STATES,
    SCOPE_AND_EXCLUSION_ITEMS,
    SOURCE_SET_BINDING_COMPONENTS,
)
from capabilities.governance.governance_constraint_module_legacy_extraction_planning_v1 import (
    DOMAIN_CONSTRAINTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "governance_constraint_module_generation_authorization_request_post_dryrun_review_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_request_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)

FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "authorization_request_dryrun_policy_v1.json",
    "authorization_request_identity_dryrun_v1.json",
    "authorization_request_source_set_binding_dryrun_v1.json",
    "authorization_request_domain_preservation_binding_dryrun_v1.json",
    "authorization_request_scope_and_exclusion_dryrun_v1.json",
    "authorization_request_non_grant_and_non_generation_statement_dryrun_v1.json",
    "authorization_request_lifecycle_dryrun_v1.json",
    "authorization_request_review_requirement_dryrun_v1.json",
    "authorization_request_abort_revoke_linkage_dryrun_v1.json",
    "authorization_request_verifier_usage_dryrun_v1.json",
    "authorization_request_non_claims_dryrun_v1.json",
    "authorization_request_dryrun_readiness_decision_v1.json",
)

DRYRUN_COMPLETENESS_TARGETS: Tuple[Tuple[str, str, int], ...] = (
    ("authorization request dry-run policy", "authorization_request_dryrun_policy_v1.json", 0),
    ("request identity dry-run", "authorization_request_identity_dryrun_v1.json", 12),
    ("source set binding dry-run", "authorization_request_source_set_binding_dryrun_v1.json", 12),
    ("domain preservation binding dry-run", "authorization_request_domain_preservation_binding_dryrun_v1.json", 12),
    ("scope and exclusion dry-run", "authorization_request_scope_and_exclusion_dryrun_v1.json", 13),
    (
        "non-grant and non-generation statement dry-run",
        "authorization_request_non_grant_and_non_generation_statement_dryrun_v1.json",
        10,
    ),
    ("request lifecycle dry-run", "authorization_request_lifecycle_dryrun_v1.json", 12),
    ("request review requirement dry-run", "authorization_request_review_requirement_dryrun_v1.json", 12),
    ("abort / revoke linkage dry-run", "authorization_request_abort_revoke_linkage_dryrun_v1.json", 12),
    ("request verifier usage dry-run", "authorization_request_verifier_usage_dryrun_v1.json", 12),
    ("request non-claims dry-run", "authorization_request_non_claims_dryrun_v1.json", 10),
    ("request dry-run readiness decision", "authorization_request_dryrun_readiness_decision_v1.json", 0),
)

ARTIFACT_NON_GENERATION_TARGETS: Tuple[str, ...] = (
    "authorization_request_artifact_generated_now",
    "governance_constraint_module_generation_authorization_request_generated_now",
    "request_artifact_generated_now",
    "request_draft_generated_now",
    "request_candidate_materialized_now",
)

REQUEST_NON_SENT_TARGETS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorization_request_sent_now",
    "request_sent_now",
    "requester_role_activated_now",
    "approver_role_notified_now",
    "operator_acknowledgement_requested_now",
)

GRANT_NON_ISSUED_TARGETS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorized_now",
    "governance_constraint_module_generation_authorization_grant_generated_now",
    "grant_issued_now",
    "authorization_granted_now",
    "granted_scope_active_now",
)

POST_DRYRUN_NON_CLAIMS: Tuple[Tuple[str, str], ...] = (
    ("Request artifact not generated", "Request DryRun GO does not mean request artifact is generated."),
    ("Request not sent", "Request DryRun GO does not mean request is sent."),
    ("Authorization not granted", "Request DryRun GO does not mean authorization is granted."),
    ("Source set not approved", "Request DryRun GO does not mean source set is final approved."),
    ("Domain not approved", "Request DryRun GO does not mean domain preservation is approved."),
    ("Authority not released", "Request DryRun GO does not mean module generation authority is released."),
    ("Module not generated", "Request DryRun GO does not mean Governance Constraint Module may be generated."),
    ("Verifier integration", "Request DryRun GO does not mean verifier/template integration may start."),
    ("Mainline not resumed", "Request DryRun GO does not mean main migration chain may resume."),
    ("Real execution blocked", "Request DryRun GO does not mean real migration / rollback / batch arming is allowed."),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
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
        "request_ready_now": False,
        "request_sent_now": False,
        "grant_issued_now": False,
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


def _review_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_review_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "authorization_request_dryrun_readiness_decision_v1.json") if root else None
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


def _all_rows_pass(payload: Dict[str, Any]) -> bool:
    rows = payload.get("rows") or []
    return bool(rows) and all(r.get("dryrun_status") == "pass" for r in rows)


def _build_completeness_review(art: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for artifact_name, filename, min_count in DRYRUN_COMPLETENESS_TARGETS:
        payload = art.get(filename, {})
        observed = filename in art
        row_count = payload.get("row_count", 0) if isinstance(payload, dict) else 0
        count_pass = row_count >= min_count if min_count > 0 else observed
        schema_pass = observed and isinstance(payload, dict)
        semantic_pass = True
        if min_count > 0 and isinstance(payload, dict):
            semantic_pass = _all_rows_pass(payload) or payload.get("all_pass") is True
        if filename == "authorization_request_dryrun_readiness_decision_v1.json":
            semantic_pass = payload.get("authorization_request_dryrun_completed") is True
        elif filename == "authorization_request_domain_preservation_binding_dryrun_v1.json":
            semantic_pass = (
                payload.get("all_pass") is True
                and payload.get("domain_differentiation_preserved") is True
            )
        elif filename == "authorization_request_lifecycle_dryrun_v1.json":
            semantic_pass = payload.get("all_pass") is True and payload.get("lifecycle_planning_defined_only") is True
        review_pass = observed and count_pass and schema_pass and semantic_pass
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                artifact_name=artifact_name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_pass,
                count_requirement_pass=count_pass,
                semantic_requirement_pass=semantic_pass,
                row_count_observed=row_count,
                min_count_required=min_count,
                review_status="pass" if review_pass else "fail",
                review_notes=f"authorization request dry-run artifact {filename} completeness check",
            )
        )
    return rows, all_pass


_OPTIONAL_FALSE_FLAGS = frozenset(
    {
        "authorization_request_artifact_generated_now",
        "request_artifact_generated_now",
        "request_draft_generated_now",
        "request_candidate_materialized_now",
        "request_sent_now",
        "requester_role_activated_now",
        "approver_role_notified_now",
        "operator_acknowledgement_requested_now",
        "grant_issued_now",
        "granted_scope_active_now",
    }
)


def _build_flag_non_execution_review(
    up_summary: Dict[str, Any],
    targets: Tuple[str, ...],
) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target in targets:
        observed = up_summary.get(target)
        if observed is None and target in _OPTIONAL_FALSE_FLAGS:
            observed = False
        violation = observed is not False
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                expected_value=False,
                observed_value=observed,
                violation_detected=violation,
                review_pass=review_pass,
            )
        )
    return rows, all_pass


def _build_source_and_domain_review(
    source: Dict[str, Any],
    domain: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_source = {r.get("source_component"): r for r in (source.get("rows") or [])}
    for component, _ in SOURCE_SET_BINDING_COMPONENTS:
        r = by_source.get(component, {})
        review_pass = (
            r.get("simulated_binding_check") is True
            and r.get("source_set_final_approved_now") is False
            and r.get("source_bound_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=f"source:{component}",
                simulated_binding_check=r.get("simulated_binding_check", True),
                source_set_final_approved_now=False,
                source_bound_now=False,
                domain_specific_preservation_approved_now=False,
                domain_bound_now=False,
                review_pass=review_pass,
            )
        )
    by_domain = {r.get("domain_constraint_name"): r for r in (domain.get("rows") or [])}
    for name, _, _, _ in DOMAIN_CONSTRAINTS:
        r = by_domain.get(name, {})
        review_pass = (
            r.get("simulated_binding_check") is True
            and r.get("flattening_forbidden") is True
            and r.get("approved_now") is False
            and r.get("domain_bound_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=f"domain:{name}",
                simulated_binding_check=r.get("simulated_binding_check", True),
                source_set_final_approved_now=False,
                source_bound_now=False,
                domain_specific_preservation_approved_now=False,
                domain_bound_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 24


def _build_lifecycle_non_advance_review(lifecycle: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_state = {r.get("lifecycle_state"): r for r in (lifecycle.get("rows") or [])}
    for state, _, _, _ in LIFECYCLE_STATES:
        r = by_state.get(state, {})
        review_pass = (
            r.get("simulated_lifecycle_consumption") is True
            and r.get("current_state_now") is False
            and r.get("request_sent_now") is False
            and r.get("grant_issued_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if state in ("request_ready", "request_sent", "grant_issued", "grant_pending"):
            if r.get("current_state_now") is True:
                review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                lifecycle_state=state,
                simulated_lifecycle_consumption=r.get("simulated_lifecycle_consumption", True),
                current_state_now=False,
                request_ready_now=False,
                request_sent_now=False,
                grant_issued_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_scope_boundary_review(scope: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_item = {r.get("scope_item"): r for r in (scope.get("rows") or [])}
    for item, scope_type, _ in SCOPE_AND_EXCLUSION_ITEMS:
        r = by_item.get(item, {})
        review_pass = (
            r.get("simulated_scope_consumption") is True
            and r.get("allowed_now") is False
            and r.get("request_artifact_generated_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                scope_item=item,
                scope_type=scope_type,
                simulated_scope_consumption=r.get("simulated_scope_consumption", True),
                allowed_now=False,
                request_artifact_generated_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 13


def _build_abort_revoke_review(abort: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_linkage = {r.get("linkage_type"): r for r in (abort.get("rows") or [])}
    for linkage, _, _ in ABORT_REVOKE_LINKAGES:
        r = by_linkage.get(linkage, {})
        review_pass = (
            r.get("simulated_linkage_consumption") is True
            and r.get("confirmed_now") is False
            and r.get("abort_executed_now") is False
            and r.get("revoke_executed_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                linkage_type=linkage,
                simulated_linkage_consumption=r.get("simulated_linkage_consumption", True),
                confirmed_now=False,
                abort_executed_now=False,
                revoke_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_usage_review(verifier_usage: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in verifier_usage.get("rows") or []:
        review_pass = (
            r.get("simulated_verifier_usage") is True
            and r.get("verifier_modified_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                verifier_check_id=r.get("verifier_check_id"),
                check_name=r.get("check_name"),
                simulated_verifier_usage=r.get("simulated_verifier_usage", True),
                verifier_modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_non_claims_review(
    non_claims: Dict[str, Any],
    up_summary: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    dryrun_rows = non_claims.get("rows") or []
    dryrun_base_pass = (
        non_claims.get("all_pass") is True
        and len(dryrun_rows) >= 10
        and all(
            r.get("simulated_generation") is True
            and r.get("dryrun_status") == "pass"
            and r.get("generated_now") is False
            for r in dryrun_rows
        )
    )
    summary_safe = (
        up_summary.get("governance_constraint_module_generation_authorization_request_generated_now") is False
        and up_summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False
        and up_summary.get("governance_constraint_module_generation_authorized_now") is False
        and up_summary.get("governance_constraint_module_generated_now") is False
        and up_summary.get("main_migration_chain_resumed_now") is False
        and up_summary.get("lifecycle_planning_defined_only") is True
    )
    all_pass = dryrun_base_pass and summary_safe
    for scenario, statement in POST_DRYRUN_NON_CLAIMS:
        review_pass = all_pass
        rows.append(
            _review_row(
                scenario=scenario,
                required_non_claim=statement,
                simulated_generation=True,
                generated_now=False,
                summary_coverage=True,
                verifier_report_coverage=True,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 10


def run_governance_constraint_module_generation_authorization_request_post_dryrun_review_v1(
    *,
    governance_constraint_module_generation_authorization_request_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_request_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream authorization request dryrun verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_post_dryrun_review") is not True:
        blockers.append("upstream not ready_for_authorization_request_post_dryrun_review")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("authorization_request_dryrun_only") is not True:
        blockers.append("upstream authorization_request_dryrun_only must be true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated must be true")

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
    if up_summary.get("all_dryrun_pass") is not True:
        blockers.append("upstream all_dryrun_pass must be true")
    if up_summary.get("lifecycle_planning_defined_only") is not True:
        blockers.append("upstream lifecycle_planning_defined_only must be true")

    lifecycle_dryrun = up_art.get("authorization_request_lifecycle_dryrun_v1.json", {})
    if any(r.get("current_state_now") for r in (lifecycle_dryrun.get("rows") or [])):
        blockers.append("upstream lifecycle current_state_now must all be false")
    if any(r.get("request_sent_now") for r in (lifecycle_dryrun.get("rows") or [])):
        blockers.append("upstream lifecycle request_sent_now must all be false")
    if any(r.get("grant_issued_now") for r in (lifecycle_dryrun.get("rows") or [])):
        blockers.append("upstream lifecycle grant_issued_now must all be false")

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

    completeness_rows, completeness_pass = _build_completeness_review(up_art)
    artifact_rows, artifact_pass = _build_flag_non_execution_review(up_summary, ARTIFACT_NON_GENERATION_TARGETS)
    non_sent_rows, non_sent_pass = _build_flag_non_execution_review(up_summary, REQUEST_NON_SENT_TARGETS)
    grant_rows, grant_pass = _build_flag_non_execution_review(up_summary, GRANT_NON_ISSUED_TARGETS)
    source_domain_rows, source_domain_pass = _build_source_and_domain_review(
        up_art.get("authorization_request_source_set_binding_dryrun_v1.json", {}),
        up_art.get("authorization_request_domain_preservation_binding_dryrun_v1.json", {}),
    )
    lifecycle_rows, lifecycle_pass = _build_lifecycle_non_advance_review(lifecycle_dryrun)
    scope_rows, scope_pass = _build_scope_boundary_review(
        up_art.get("authorization_request_scope_and_exclusion_dryrun_v1.json", {})
    )
    abort_rows, abort_pass = _build_abort_revoke_review(
        up_art.get("authorization_request_abort_revoke_linkage_dryrun_v1.json", {})
    )
    verifier_rows, verifier_pass = _build_verifier_usage_review(
        up_art.get("authorization_request_verifier_usage_dryrun_v1.json", {})
    )
    non_claims_rows, non_claims_pass = _build_non_claims_review(
        up_art.get("authorization_request_non_claims_dryrun_v1.json", {}),
        up_summary,
    )

    review_pass = all(
        (
            completeness_pass,
            artifact_pass,
            non_sent_pass,
            grant_pass,
            source_domain_pass,
            lifecycle_pass,
            scope_pass,
            abort_pass,
            verifier_pass,
            non_claims_pass,
        )
    )
    if not review_pass:
        blockers.append("one or more authorization request post-dryrun review matrices failed")

    if up_summary.get("main_migration_chain_resumed_now") is not False:
        blockers.append("main migration chain must not be resumed")

    review_ready = review_pass and not blockers
    boundary_ok = review_ready

    authorization_request_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_simulated_observed=up_summary.get("simulated") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    authorization_request_dryrun_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_review_meta(),
    }
    authorization_request_artifact_non_generation_review = {
        "rows": artifact_rows,
        "row_count": len(artifact_rows),
        "all_pass": artifact_pass,
        **_review_meta(),
    }
    authorization_request_non_sent_review = {
        "rows": non_sent_rows,
        "row_count": len(non_sent_rows),
        "all_pass": non_sent_pass,
        **_review_meta(),
    }
    authorization_grant_non_issued_review = {
        "rows": grant_rows,
        "row_count": len(grant_rows),
        "all_pass": grant_pass,
        **_review_meta(),
    }
    source_and_domain_approval_non_execution_review = {
        "rows": source_domain_rows,
        "row_count": len(source_domain_rows),
        "all_pass": source_domain_pass,
        **_review_meta(),
    }
    request_lifecycle_non_advance_review = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_pass": lifecycle_pass,
        "lifecycle_planning_defined_only": lifecycle_pass,
        **_review_meta(),
    }
    scope_and_exclusion_boundary_review = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "all_pass": scope_pass,
        **_review_meta(),
    }
    abort_revoke_linkage_non_execution_review = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_pass": abort_pass,
        **_review_meta(),
    }
    request_verifier_usage_non_modification_review = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_review_meta(),
    }
    authorization_request_non_claims_review = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_pass": non_claims_pass,
        **_review_meta(),
    }

    authorization_request_post_dryrun_review_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_request_roadmap_decision": boundary_ok,
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
        "post_dryrun_review_completed": boundary_ok,
        "authorization_request_dryrun_completeness_review_pass": completeness_pass,
        "authorization_request_artifact_non_generation_review_pass": artifact_pass,
        "authorization_request_non_sent_review_pass": non_sent_pass,
        "authorization_grant_non_issued_review_pass": grant_pass,
        "source_and_domain_approval_non_execution_review_pass": source_domain_pass,
        "request_lifecycle_non_advance_review_pass": lifecycle_pass,
        "scope_and_exclusion_boundary_review_pass": scope_pass,
        "abort_revoke_linkage_non_execution_review_pass": abort_pass,
        "request_verifier_usage_non_modification_review_pass": verifier_pass,
        "authorization_request_non_claims_review_pass": non_claims_pass,
        "governance_constraint_module_generation_authorization_request_generated_now": False,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generated_now": False,
        "main_migration_chain_resumed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_request_dryrun_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_simulated_observed": up_summary.get("simulated") is True,
        "authorization_request_dryrun_completeness_review_pass": completeness_pass,
        "authorization_request_artifact_non_generation_review_pass": artifact_pass,
        "authorization_request_non_sent_review_pass": non_sent_pass,
        "authorization_grant_non_issued_review_pass": grant_pass,
        "source_and_domain_approval_non_execution_review_pass": source_domain_pass,
        "request_lifecycle_non_advance_review_pass": lifecycle_pass,
        "scope_and_exclusion_boundary_review_pass": scope_pass,
        "abort_revoke_linkage_non_execution_review_pass": abort_pass,
        "request_verifier_usage_non_modification_review_pass": verifier_pass,
        "authorization_request_non_claims_review_pass": non_claims_pass,
        "lifecycle_state_count": len(lifecycle_rows),
        "scope_item_count": len(scope_rows),
        "non_claims_scenario_count": len(non_claims_rows),
        "all_review_pass": review_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "authorization_request_post_dryrun_review_policy": authorization_request_post_dryrun_review_policy,
        "authorization_request_dryrun_completeness_review": authorization_request_dryrun_completeness_review,
        "authorization_request_artifact_non_generation_review": authorization_request_artifact_non_generation_review,
        "authorization_request_non_sent_review": authorization_request_non_sent_review,
        "authorization_grant_non_issued_review": authorization_grant_non_issued_review,
        "source_and_domain_approval_non_execution_review": source_and_domain_approval_non_execution_review,
        "request_lifecycle_non_advance_review": request_lifecycle_non_advance_review,
        "scope_and_exclusion_boundary_review": scope_and_exclusion_boundary_review,
        "abort_revoke_linkage_non_execution_review": abort_revoke_linkage_non_execution_review,
        "request_verifier_usage_non_modification_review": request_verifier_usage_non_modification_review,
        "authorization_request_non_claims_review": authorization_request_non_claims_review,
        "authorization_request_post_dryrun_review_readiness_decision": authorization_request_post_dryrun_review_readiness_decision,
    }
