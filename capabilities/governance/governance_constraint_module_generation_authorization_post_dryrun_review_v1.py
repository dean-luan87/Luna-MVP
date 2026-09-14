# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Post-DryRun Review v1.

Post-dryrun review only: audit authorization dry-run completeness and non-authorization.
Does not send authorization requests, grant authorization, or generate constraint modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.governance_constraint_module_generation_authorization_planning_v1 import (
    ABORT_ROLLBACK_AUTHORITIES,
    FUTURE_INTEGRATION_BOUNDARIES,
    INDEPENDENT_PATH_DOMAINS,
    MODULE_GENERATION_AUTHORITIES,
    POST_GENERATION_REVIEW_AUTHORITIES,
    SOURCE_SET_COMPONENTS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "governance_constraint_module_generation_authorization_post_dryrun_review_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
)

FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001"

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorization_dryrun_policy_v1.json",
    "authorization_request_schema_consumption_dryrun_v1.json",
    "authorization_grant_schema_consumption_dryrun_v1.json",
    "source_set_final_approval_authority_dryrun_v1.json",
    "domain_specific_preservation_approval_dryrun_v1.json",
    "module_generation_authority_dryrun_v1.json",
    "future_integration_boundary_dryrun_v1.json",
    "post_generation_review_authority_dryrun_v1.json",
    "abort_and_rollback_authority_dryrun_v1.json",
    "authorization_verifier_usage_dryrun_v1.json",
    "authorization_non_claims_generation_dryrun_v1.json",
    "governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json",
)

DRYRUN_COMPLETENESS_TARGETS: Tuple[Tuple[str, str, int], ...] = (
    (
        "authorization dry-run policy",
        "governance_constraint_module_generation_authorization_dryrun_policy_v1.json",
        0,
    ),
    (
        "authorization request schema consumption dry-run",
        "authorization_request_schema_consumption_dryrun_v1.json",
        12,
    ),
    (
        "authorization grant schema consumption dry-run",
        "authorization_grant_schema_consumption_dryrun_v1.json",
        12,
    ),
    (
        "source set final approval authority dry-run",
        "source_set_final_approval_authority_dryrun_v1.json",
        12,
    ),
    (
        "domain-specific preservation approval dry-run",
        "domain_specific_preservation_approval_dryrun_v1.json",
        12,
    ),
    ("module generation authority dry-run", "module_generation_authority_dryrun_v1.json", 12),
    ("future integration boundary dry-run", "future_integration_boundary_dryrun_v1.json", 10),
    (
        "post-generation review authority dry-run",
        "post_generation_review_authority_dryrun_v1.json",
        12,
    ),
    ("abort and rollback authority dry-run", "abort_and_rollback_authority_dryrun_v1.json", 12),
    ("authorization verifier usage dry-run", "authorization_verifier_usage_dryrun_v1.json", 12),
    (
        "authorization non-claims generation dry-run",
        "authorization_non_claims_generation_dryrun_v1.json",
        10,
    ),
    (
        "authorization dry-run readiness decision",
        "governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json",
        0,
    ),
)

REQUEST_NON_SENT_TARGETS: Tuple[str, ...] = (
    "authorization_request_generated_now",
    "governance_constraint_module_generation_authorization_request_sent_now",
    "request_sent_now",
    "requester_role_activated_now",
    "approver_role_notified_now",
)

GRANT_NON_ISSUED_TARGETS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorized_now",
    "grant_issued_now",
    "authorization_granted_now",
    "granted_scope_active_now",
    "generation_permission_boundary_active_now",
)

POST_DRYRUN_NON_CLAIMS: Tuple[Tuple[str, str], ...] = (
    ("DryRun GO not request sent", "DryRun GO does not mean authorization request is sent."),
    ("DryRun GO not granted", "DryRun GO does not mean authorization is granted."),
    ("DryRun GO not module generation", "DryRun GO does not mean module generation is allowed."),
    ("Source set not final approval", "Source set planned approval does not mean final approval."),
    ("Domain preservation not approved", "Domain preservation planned approval does not mean approval."),
    ("Generation authority not released", "Generation authority planned does not mean released."),
    (
        "Future integration not confirmed",
        "Future integration boundary planned does not mean confirmed / executed.",
    ),
    (
        "Post-generation review not executed",
        "Post-generation review authority planned does not mean review executed.",
    ),
    (
        "Abort rollback not executed",
        "Abort/rollback authority planned does not mean confirmed / rollback executed.",
    ),
    ("DryRun GO not mainline resume", "DryRun GO does not mean mainline may resume."),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
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
    readiness = _try_read_json(
        root / "governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json"
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


def _all_rows_pass(payload: Dict[str, Any]) -> bool:
    rows = payload.get("rows") or []
    return bool(rows) and all(r.get("dryrun_status") == "pass" for r in rows)


def _is_false_or_absent(value: Any) -> bool:
    return value is False or value is None


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
        if filename == "governance_constraint_module_generation_authorization_dryrun_readiness_decision_v1.json":
            semantic_pass = payload.get("authorization_dryrun_completed") is True
        elif filename == "domain_specific_preservation_approval_dryrun_v1.json":
            semantic_pass = (
                payload.get("all_pass") is True
                and payload.get("domain_differentiation_preserved") is True
            )
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
                review_notes=f"authorization dry-run artifact {filename} completeness check",
            )
        )
    return rows, all_pass


_OPTIONAL_FALSE_FLAGS = frozenset(
    {
        "authorization_request_generated_now",
        "request_sent_now",
        "requester_role_activated_now",
        "approver_role_notified_now",
        "grant_issued_now",
        "granted_scope_active_now",
        "generation_permission_boundary_active_now",
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


def _build_source_set_review(source: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_component = {r.get("source_set_component"): r for r in (source.get("rows") or [])}
    for component in SOURCE_SET_COMPONENTS:
        r = by_component.get(component, {})
        review_pass = (
            r.get("simulated_approval_check") is True
            and r.get("final_approved_now") is False
            and r.get("source_set_locked_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                source_set_component=component,
                simulated_approval_check=r.get("simulated_approval_check", True),
                final_approved_now=False,
                source_set_locked_now=False,
                source_set_mutation_allowed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_domain_preservation_review(domain: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for r in domain.get("rows") or []:
        name = r.get("domain_constraint_name")
        independent = name in INDEPENDENT_PATH_DOMAINS
        review_pass = (
            r.get("simulated_preservation_approval_check") is True
            and r.get("preservation_required") is True
            and r.get("flattening_forbidden") is True
            and r.get("approved_now") is False
            and r.get("domain_constraint_generated_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if independent and r.get("independent_consumption_path_required") is not True:
            review_pass = False
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                domain_constraint_name=name,
                simulated_preservation_approval_check=r.get("simulated_preservation_approval_check"),
                preservation_required=True,
                flattening_forbidden=True,
                approved_now=False,
                domain_constraint_generated_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_generation_authority_review(authority: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_name = {r.get("authority_name"): r for r in (authority.get("rows") or [])}
    for name, scope in MODULE_GENERATION_AUTHORITIES:
        r = by_name.get(name, {})
        review_pass = (
            r.get("simulated_authority_check") is True
            and r.get("requires_authorization_grant") is True
            and r.get("requires_source_set_final_approval") is True
            and r.get("requires_domain_preservation_approval") is True
            and r.get("authorized_now") is False
            and r.get("generated_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                authority_name=name,
                scope=scope,
                simulated_authority_check=r.get("simulated_authority_check", True),
                requires_authorization_grant=True,
                requires_source_set_final_approval=True,
                requires_domain_preservation_approval=True,
                authorized_now=False,
                generated_now=False,
                module_generation_authority_released_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_integration_boundary_review(integration: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_boundary = {r.get("integration_boundary"): r for r in (integration.get("rows") or [])}
    for boundary, _ in FUTURE_INTEGRATION_BOUNDARIES:
        r = by_boundary.get(boundary, {})
        review_pass = (
            r.get("simulated_boundary_check") is True
            and r.get("allowed_in_this_phase") is False
            and r.get("requires_separate_planning") is True
            and r.get("requires_separate_authorization") is True
            and r.get("confirmed_now") is False
            and r.get("integration_executed_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                integration_boundary=boundary,
                simulated_boundary_check=r.get("simulated_boundary_check", True),
                allowed_in_this_phase=False,
                requires_separate_planning=True,
                requires_separate_authorization=True,
                confirmed_now=False,
                integration_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_post_review_review(post: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_authority = {r.get("review_authority"): r for r in (post.get("rows") or [])}
    for authority, _ in POST_GENERATION_REVIEW_AUTHORITIES:
        r = by_authority.get(authority, {})
        review_pass = (
            r.get("simulated_review_authority_check") is True
            and r.get("review_required_after_generation") is True
            and r.get("confirmed_now") is False
            and r.get("review_executed_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_authority=authority,
                simulated_review_authority_check=r.get("simulated_review_authority_check", True),
                review_required_after_generation=True,
                confirmed_now=False,
                review_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_abort_rollback_review(abort: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    by_authority = {r.get("authority"): r for r in (abort.get("rows") or [])}
    for authority, trigger in ABORT_ROLLBACK_AUTHORITIES:
        r = by_authority.get(authority, {})
        review_pass = (
            r.get("simulated_authority_check") is True
            and r.get("confirmed_now") is False
            and r.get("rollback_executed_now") is False
            and r.get("dryrun_status") == "pass"
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                authority=authority,
                trigger_condition=trigger,
                simulated_authority_check=r.get("simulated_authority_check", True),
                confirmed_now=False,
                rollback_executed_now=False,
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
        up_summary.get("governance_constraint_module_generation_authorization_request_sent_now") is False
        and up_summary.get("governance_constraint_module_generation_authorized_now") is False
        and up_summary.get("governance_constraint_module_generated_now") is False
        and up_summary.get("main_migration_chain_resumed_now") is False
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


def run_governance_constraint_module_generation_authorization_post_dryrun_review_v1(
    *,
    governance_constraint_module_generation_authorization_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream authorization dryrun verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_post_dryrun_review") is not True:
        blockers.append("upstream not ready_for_authorization_post_dryrun_review")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("governance_constraint_module_generation_authorization_dryrun_only") is not True:
        blockers.append("upstream authorization_dryrun_only must be true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated must be true")

    for flag in (
        "governance_constraint_module_generation_authorization_request_sent_now",
        "governance_constraint_module_generation_authorized_now",
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
    if up_summary.get("all_dryrun_pass") is not True:
        blockers.append("upstream all_dryrun_pass must be true")

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

    completeness_rows, completeness_pass = _build_completeness_review(up_art)
    request_rows, request_pass = _build_flag_non_execution_review(up_summary, REQUEST_NON_SENT_TARGETS)
    grant_rows, grant_pass = _build_flag_non_execution_review(up_summary, GRANT_NON_ISSUED_TARGETS)
    source_rows, source_pass = _build_source_set_review(
        up_art.get("source_set_final_approval_authority_dryrun_v1.json", {})
    )
    domain_rows, domain_pass = _build_domain_preservation_review(
        up_art.get("domain_specific_preservation_approval_dryrun_v1.json", {})
    )
    authority_rows, authority_pass = _build_generation_authority_review(
        up_art.get("module_generation_authority_dryrun_v1.json", {})
    )
    integration_rows, integration_pass = _build_integration_boundary_review(
        up_art.get("future_integration_boundary_dryrun_v1.json", {})
    )
    post_rows, post_pass = _build_post_review_review(
        up_art.get("post_generation_review_authority_dryrun_v1.json", {})
    )
    abort_rows, abort_pass = _build_abort_rollback_review(
        up_art.get("abort_and_rollback_authority_dryrun_v1.json", {})
    )
    non_claims_rows, non_claims_pass = _build_non_claims_review(
        up_art.get("authorization_non_claims_generation_dryrun_v1.json", {}),
        up_summary,
    )

    review_pass = all(
        (
            completeness_pass,
            request_pass,
            grant_pass,
            source_pass,
            domain_pass,
            authority_pass,
            integration_pass,
            post_pass,
            abort_pass,
            non_claims_pass,
        )
    )
    if not review_pass:
        blockers.append("one or more authorization post-dryrun review matrices failed")

    if up_summary.get("main_migration_chain_resumed_now") is not False:
        blockers.append("main migration chain must not be resumed")

    review_ready = review_pass and not blockers
    boundary_ok = review_ready

    governance_constraint_module_generation_authorization_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_simulated_observed=up_summary.get("simulated") is True,
        governance_constraints_ref=CONSTRAINT_DOC_ID,
    )

    authorization_dryrun_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_review_meta(),
    }
    authorization_request_non_sent_review = {
        "rows": request_rows,
        "row_count": len(request_rows),
        "all_pass": request_pass,
        **_review_meta(),
    }
    authorization_grant_non_issued_review = {
        "rows": grant_rows,
        "row_count": len(grant_rows),
        "all_pass": grant_pass,
        **_review_meta(),
    }
    source_set_final_approval_non_execution_review = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "all_pass": source_pass,
        **_review_meta(),
    }
    domain_preservation_non_approval_review = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_pass": domain_pass,
        **_review_meta(),
    }
    generation_authority_non_release_review = {
        "rows": authority_rows,
        "row_count": len(authority_rows),
        "all_pass": authority_pass,
        **_review_meta(),
    }
    future_integration_boundary_non_confirmation_review = {
        "rows": integration_rows,
        "row_count": len(integration_rows),
        "all_pass": integration_pass,
        **_review_meta(),
    }
    post_generation_review_non_execution_review = {
        "rows": post_rows,
        "row_count": len(post_rows),
        "all_pass": post_pass,
        **_review_meta(),
    }
    abort_rollback_authority_non_confirmation_review = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_pass": abort_pass,
        **_review_meta(),
    }
    authorization_non_claims_review = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_pass": non_claims_pass,
        **_review_meta(),
    }

    governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_roadmap_decision": boundary_ok,
        "ready_for_governance_constraint_module_generation_authorization_request": False,
        "ready_for_governance_constraint_module_generation_authorization_grant": False,
        "ready_for_source_set_final_approval": False,
        "ready_for_domain_specific_preservation_approval": False,
        "ready_for_module_generation_authority_release": False,
        "ready_for_future_verifier_integration_boundary_confirmation": False,
        "ready_for_future_phase_template_integration_boundary_confirmation": False,
        "ready_for_post_generation_review_execution": False,
        "ready_for_abort_authority_confirmation": False,
        "ready_for_rollback_authority_confirmation": False,
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
        "authorization_dryrun_completeness_review_pass": completeness_pass,
        "authorization_request_non_sent_review_pass": request_pass,
        "authorization_grant_non_issued_review_pass": grant_pass,
        "source_set_final_approval_non_execution_review_pass": source_pass,
        "domain_preservation_non_approval_review_pass": domain_pass,
        "generation_authority_non_release_review_pass": authority_pass,
        "future_integration_boundary_non_confirmation_review_pass": integration_pass,
        "post_generation_review_non_execution_review_pass": post_pass,
        "abort_rollback_authority_non_confirmation_review_pass": abort_pass,
        "authorization_non_claims_review_pass": non_claims_pass,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "source_set_final_approved_now": False,
        "domain_specific_preservation_approved_now": False,
        "module_generation_authority_released_now": False,
        "governance_constraint_module_generated_now": False,
        "main_migration_chain_resumed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_dryrun_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_simulated_observed": up_summary.get("simulated") is True,
        "authorization_dryrun_completeness_review_pass": completeness_pass,
        "authorization_request_non_sent_review_pass": request_pass,
        "authorization_grant_non_issued_review_pass": grant_pass,
        "source_set_final_approval_non_execution_review_pass": source_pass,
        "domain_preservation_non_approval_review_pass": domain_pass,
        "generation_authority_non_release_review_pass": authority_pass,
        "future_integration_boundary_non_confirmation_review_pass": integration_pass,
        "post_generation_review_non_execution_review_pass": post_pass,
        "abort_rollback_authority_non_confirmation_review_pass": abort_pass,
        "authorization_non_claims_review_pass": non_claims_pass,
        "domain_preservation_count": len(domain_rows),
        "generation_authority_count": len(authority_rows),
        "non_claims_scenario_count": len(non_claims_rows),
        "all_review_pass": review_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_authorization_post_dryrun_review_policy": governance_constraint_module_generation_authorization_post_dryrun_review_policy,
        "authorization_dryrun_completeness_review": authorization_dryrun_completeness_review,
        "authorization_request_non_sent_review": authorization_request_non_sent_review,
        "authorization_grant_non_issued_review": authorization_grant_non_issued_review,
        "source_set_final_approval_non_execution_review": source_set_final_approval_non_execution_review,
        "domain_preservation_non_approval_review": domain_preservation_non_approval_review,
        "generation_authority_non_release_review": generation_authority_non_release_review,
        "future_integration_boundary_non_confirmation_review": future_integration_boundary_non_confirmation_review,
        "post_generation_review_non_execution_review": post_generation_review_non_execution_review,
        "abort_rollback_authority_non_confirmation_review": abort_rollback_authority_non_confirmation_review,
        "authorization_non_claims_review": authorization_non_claims_review,
        "governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision": governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision,
    }
