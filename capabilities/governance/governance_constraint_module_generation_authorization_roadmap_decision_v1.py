# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Roadmap Decision v1.

Roadmap decision only: select Route A — Authorization Request Planning.
Does not send authorization requests, grant authorization, or generate constraint modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001"
DECISION_SCOPE = "governance_constraint_module_generation_authorization_roadmap_decision_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

SELECTED_ROUTE = "Route A — Governance Constraint Module Generation Authorization Request Planning"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_ROADMAP_DECISION_READY_FOR_AUTHORIZATION_REQUEST_PLANNING"
)

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_generation_authorization_post_dryrun_review_policy_v1.json",
    "authorization_dryrun_completeness_review_v1.json",
    "authorization_request_non_sent_review_v1.json",
    "authorization_grant_non_issued_review_v1.json",
    "source_set_final_approval_non_execution_review_v1.json",
    "domain_preservation_non_approval_review_v1.json",
    "generation_authority_non_release_review_v1.json",
    "future_integration_boundary_non_confirmation_review_v1.json",
    "post_generation_review_non_execution_review_v1.json",
    "abort_rollback_authority_non_confirmation_review_v1.json",
    "authorization_non_claims_review_v1.json",
    "governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001",
        "governance_constraint_module_generation_authorization_planning_v1_smoke_v0",
    ),
    (
        "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001",
        "governance_constraint_module_generation_authorization_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001",
        "governance_constraint_module_generation_authorization_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Governance Constraint Module Generation Authorization Request Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "governance_constraint_module_generation_authorization_request_planning",
        "target_scope": "request identity, source set binding, domain preservation binding, excluded scope, non-grant statement, request lifecycle, abort/revoke linkage",
        "entry_reason": "authorization dry-run safe; real request structure not yet planned",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "authorization request planning allowed only; not authorization request sent; not authorization grant; not module generation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ authorization request sent",
            "≠ authorization granted",
            "≠ module generated",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Governance Constraint Module Generation Authorization Request",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "governance_constraint_module_generation_authorization_request",
        "target_scope": "send real authorization request",
        "entry_reason": "authorization request planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization request planning not complete"],
        "permission_impact": "deferred; not authorization request sent allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-Authorization-Request-v1-001",
        "non_claims": ["deferred ≠ authorization request sent"],
    },
    {
        "route_id": "C",
        "route_name": "Governance Constraint Module Generation Authorization Grant Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "governance_constraint_module_generation_authorization_grant_planning",
        "target_scope": "authorization grant planning",
        "entry_reason": "real request not planned or sent",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization request planning not complete"],
        "permission_impact": "deferred; not authorization grant allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-Authorization-Grant-Planning-v1-001",
        "non_claims": ["deferred ≠ authorization granted"],
    },
    {
        "route_id": "D",
        "route_name": "Governance Constraint Module Generation",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "governance_constraint_module_generation",
        "target_scope": "formal Governance Constraint Module generation",
        "entry_reason": "authorization request/grant chain incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization request planning not complete"],
        "permission_impact": "deferred; not module generation allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-v1-001",
        "non_claims": ["deferred ≠ module generated"],
    },
    {
        "route_id": "E",
        "route_name": "Canonical Phase Template Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "canonical_phase_template_planning",
        "target_scope": "canonical phase template planning",
        "entry_reason": "module generation authorization chain incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization request planning not complete"],
        "permission_impact": "deferred; not template generation allowed",
        "next_phase_candidate": "Phase-Canonical-Phase-Template-Planning-v1-001",
        "non_claims": ["deferred ≠ template generated"],
    },
    {
        "route_id": "F",
        "route_name": "Verifier Integration Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "verifier_integration_planning",
        "target_scope": "verifier integration planning",
        "entry_reason": "module not generated; authorization not granted",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization request planning not complete"],
        "permission_impact": "deferred; not verifier integration allowed",
        "next_phase_candidate": "Phase-Verifier-Integration-Planning-v1-001",
        "non_claims": ["deferred ≠ verifier integration"],
    },
    {
        "route_id": "G",
        "route_name": "Main Migration Chain Resume Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "main_migration_chain_resume_planning",
        "target_scope": "main migration chain resume planning",
        "entry_reason": "authorization chain incomplete; mainline must stay paused",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization request planning not complete"],
        "permission_impact": "deferred; not mainline resume allowed",
        "next_phase_candidate": MAIN_MIGRATION_RESUME_PHASE,
        "non_claims": ["deferred ≠ main_migration_chain_resumed_now"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Authorization Request / Grant / Module Generation / Mainline Resume",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_authorization_request_grant_module_generation_mainline_resume",
        "target_scope": "direct request / grant / module generation / mainline resume",
        "entry_reason": "authorization request planning not complete; bypasses request structure governance",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "authorization request planning not complete",
            "authorization not granted",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Authorization-Request-v1-001",
        "non_claims": ["blocked ≠ request sent", "≠ grant issued", "≠ mainline resumed"],
    },
]

REQUEST_PLANNING_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("RD01", "request identity definition"),
    ("RD02", "requester role definition"),
    ("RD03", "approver role definition"),
    ("RD04", "requested module output list"),
    ("RD05", "source set binding"),
    ("RD06", "source evidence references"),
    ("RD07", "domain preservation binding"),
    ("RD08", "excluded scope statement"),
    ("RD09", "non-grant statement"),
    ("RD10", "non-generation statement"),
    ("RD11", "request lifecycle"),
    ("RD12", "request abort linkage"),
    ("RD13", "request revoke linkage"),
    ("RD14", "review requirement"),
    ("RD15", "verifier usage and non-claims"),
)

REQUEST_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("request identity", "unique authorization request identifier and lifecycle anchor"),
    ("requester role", "role permitted to submit authorization request later"),
    ("approver role", "role permitted to approve or reject request later"),
    ("requested module outputs", "explicit list of formal module artifacts requested"),
    ("source set binding", "bind request to final-approved source set when available"),
    ("source evidence references", "legacy + generation chain evidence references in request"),
    ("domain preservation binding", "bind domain-specific preservation approval requirements"),
    ("excluded scope", "template/verifier/automation/mainline excluded from request scope"),
    ("non-grant statement", "request sent ≠ authorization granted"),
    ("non-generation statement", "request planning ≠ module generated"),
    ("request lifecycle", "draft/submitted/approved/rejected/revoked lifecycle semantics"),
    ("request review requirement", "review gates before grant or generation"),
    ("request abort linkage", "abort authority linked to pending request"),
    ("request revoke linkage", "revoke authority linked to issued grant placeholder"),
    ("verifier usage and non-claims", "verifier checks and non-claims for request phase"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "authorization request generation",
    "authorization request sent",
    "authorization grant generation",
    "authorization grant issued",
    "source set final approval",
    "domain preservation approval",
    "generation authority release",
    "future verifier integration boundary confirmation",
    "future phase template integration boundary confirmation",
    "post-generation review execution",
    "abort authority confirmation",
    "rollback authority confirmation",
    "governance constraint module generation",
    "canonical phase template generation",
    "constraint module registration",
    "constraint enforcement",
    "verifier integration",
    "verifier modification",
    "phase template modification",
    "automation implementation",
    "main migration chain resume",
    "real migration execution",
    "rollback rehearsal execution",
    "batch arming",
)

REQUEST_PLANNING_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "request identity not defined", "high", "planning allowed; request sent blocked"),
    ("R02", "requester role not defined", "high", "requester_role_activated_now=false"),
    ("R03", "approver role not defined", "high", "authorization grant blocked"),
    ("R04", "requested module outputs not bound", "high", "module generation blocked"),
    ("R05", "source set not bound", "high", "source_set_final_approved_now=false"),
    ("R06", "source evidence refs not bound", "high", "source evidence misuse risk"),
    ("R07", "domain preservation not bound", "high", "domain_specific_rules_preserved must hold"),
    ("R08", "excluded scope not defined", "high", "verifier/template integration blocked"),
    ("R09", "non-grant statement not defined", "high", "request misread as grant risk"),
    ("R10", "non-generation statement not defined", "high", "module generation blocked"),
    ("R11", "request lifecycle not defined", "medium", "request abort path undefined"),
    ("R12", "review requirement not defined", "high", "post-generation review gate undefined"),
    ("R13", "abort linkage not defined", "medium", "abort authority undefined"),
    ("R14", "revoke linkage not defined", "medium", "rollback authority undefined"),
    ("R15", "verifier usage not defined", "high", "verifier_modified_now=false must hold"),
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean authorization request is sent.",
    "Route A selected does not mean authorization request artifact is generated.",
    "Route A selected does not mean authorization is granted.",
    "Route A selected does not mean source set is final approved.",
    "Route A selected does not mean domain preservation is approved.",
    "Route A selected does not mean module generation authority is released.",
    "Route A selected does not mean Governance Constraint Module may be generated.",
    "Route A selected does not mean verifier/template integration may start.",
    "Route A selected does not mean main migration chain may resume.",
    "Route H blocked means direct request / grant / module generation / mainline resume remain forbidden.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "selected_route": SELECTED_ROUTE,
        "governance_constraint_module_generation_authorization_request_planning_selected": True,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorization_request_generated_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generation_authorization_grant_generated_now": False,
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


def _decision_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_decision_meta()}


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
        root
        / "governance_constraint_module_generation_authorization_post_dryrun_review_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in POST_REVIEW_ARTIFACTS:
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


def _load_chain_phase(eval_out_name: str) -> Dict[str, Any]:
    repo = Path(__file__).resolve().parents[2]
    root = repo / "_eval_out" / eval_out_name
    summary = _try_read_json(root / "summary.json") or {}
    verifier = _try_read_json(root / "verifier_report.json") or {}
    return {"summary": summary, "verifier": verifier}


def _build_completed_chain_review() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for phase_name, eval_out in COMPLETED_CHAIN:
        data = _load_chain_phase(eval_out)
        sm = data["summary"]
        vr = data["verifier"]
        go = vr.get("verifier") == "GO" and vr.get("passed") is True
        boundary = sm.get("boundary_ok") is True
        review_pass = go and boundary
        if not review_pass:
            all_pass = False
        rows.append(
            _decision_row(
                phase_name=phase_name,
                verifier_status=vr.get("verifier", "UNKNOWN"),
                boundary_ok=boundary,
                final_decision=sm.get("final_decision"),
                recommended_next_phase=sm.get("recommended_next_phase"),
                authorization_request_observed=sm.get(
                    "governance_constraint_module_generation_authorization_request_sent_now"
                )
                is True,
                authorization_grant_observed=sm.get("governance_constraint_module_generation_authorized_now")
                is True,
                source_set_final_approval_observed=sm.get("source_set_final_approved_now") is True,
                domain_preservation_approval_observed=sm.get("domain_specific_preservation_approved_now")
                is True,
                generation_authority_release_observed=sm.get("module_generation_authority_released_now")
                is True,
                module_generation_observed=sm.get("governance_constraint_module_generated_now") is True,
                mainline_resume_observed=sm.get("main_migration_chain_resumed_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_request_planning_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in REQUEST_PLANNING_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_request_planning=True,
                current_status="request_planning_required",
                missing_preconditions=["Authorization Request Planning not complete"],
                blocks_request_sent=True,
                blocks_authorization_grant=True,
                blocks_module_generation=True,
                recommended_next_action="enter Authorization Request Planning",
            )
        )
    return rows


def _build_request_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in REQUEST_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"authorization_request_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                required_for_request=True,
                required_for_future_grant=True,
                required_for_module_generation=True,
                required_for_future_verifier="verifier" in planning_topic,
                required_for_mainline_resume="mainline" in planning_topic or "lifecycle" in planning_topic,
                required_non_claims=[f"request planning GO does not imply {planning_topic} executed"],
            )
        )
    return rows


def _build_non_release_matrix() -> Tuple[List[Dict[str, Any]], bool]:
    rows = [
        _decision_row(
            permission_name=name,
            expected_released=False,
            released_by_roadmap_decision=False,
            review_pass=True,
        )
        for name in NON_RELEASE_PERMISSIONS
    ]
    return rows, all(r.get("review_pass") for r in rows)


def _build_risk_matrix() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    for risk_id, desc, level, non_claim in REQUEST_PLANNING_RISKS:
        rows.append(
            _decision_row(
                risk_id=risk_id,
                risk_description=desc,
                risk_level=level,
                allowed_to_enter_planning=True,
                blocks_request_sent=True,
                blocks_authorization_grant=True,
                blocks_module_generation=True,
                blocks_verifier_integration=True,
                blocks_mainline_resume=True,
                required_non_claim=non_claim,
                review_status="pass",
            )
        )
    return rows, len(rows) >= 15


def run_governance_constraint_module_generation_authorization_roadmap_decision_v1(
    *,
    governance_constraint_module_generation_authorization_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_post_dryrun_review_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream post-dryrun review verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_authorization_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")

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

    for flag in (
        "ready_for_governance_constraint_module_generation_authorization_request",
        "ready_for_governance_constraint_module_generation_authorization_grant",
        "ready_for_source_set_final_approval",
        "ready_for_domain_specific_preservation_approval",
        "ready_for_module_generation_authority_release",
        "ready_for_future_verifier_integration_boundary_confirmation",
        "ready_for_future_phase_template_integration_boundary_confirmation",
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

    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("upstream real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("upstream batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    for art_name in (
        "authorization_dryrun_completeness_review_v1.json",
        "authorization_request_non_sent_review_v1.json",
        "authorization_grant_non_issued_review_v1.json",
        "generation_authority_non_release_review_v1.json",
        "authorization_non_claims_review_v1.json",
    ):
        if up_art.get(art_name, {}).get("all_pass") is not True:
            blockers.append(f"upstream {art_name} must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_request_planning_dependency_matrix()
    planning_scope_rows = _build_request_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_c = next(r for r in route_rows if r.get("route_id") == "C")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "request planning" in str(route_a.get("permission_impact", "")).lower()
        and "not authorization request sent" in str(route_a.get("permission_impact", "")).lower()
        and "not authorization grant" in str(route_a.get("permission_impact", "")).lower()
        and "not module generation" in str(route_a.get("permission_impact", "")).lower()
        and route_b.get("deferred") is True
        and route_b.get("selected_now") is False
        and route_c.get("deferred") is True
        and route_h.get("blocked_now") is True
        and route_h.get("allowed_now") is False
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    for rid in ("B", "C", "D", "E", "F", "G"):
        r = next(x for x in route_rows if x.get("route_id") == rid)
        if r.get("deferred") is not True or r.get("allowed_now") is not False:
            blockers.append(f"route {rid} must be deferred and not allowed_now")

    forbidden_allowed = any(
        r.get("allowed_now") is True
        and r.get("route_type")
        in (
            "governance_constraint_module_generation_authorization_request",
            "governance_constraint_module_generation",
            "direct_authorization_request_grant_module_generation_mainline_resume",
        )
        for r in route_rows
        if r.get("route_id") != "A"
    )
    if forbidden_allowed:
        blockers.append("request / module generation / direct routes must not be allowed_now")

    decision_ready = (
        chain_pass
        and non_release_pass
        and risk_pass
        and route_ok
        and len(dependency_rows) >= 15
        and len(planning_scope_rows) >= 15
        and not blockers
    )
    boundary_ok = decision_ready

    governance_constraint_module_generation_authorization_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    completed_authorization_governance_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    authorization_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    authorization_request_planning_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "authorization_request_planning_missing_dependency_identified": True,
        **_decision_meta(),
    }
    authorization_request_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    authorization_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    authorization_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    authorization_request_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    authorization_roadmap_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_request_planning": boundary_ok,
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
        "selected_route": SELECTED_ROUTE,
        "authorization_chain_completed": chain_pass,
        "authorization_request_planning_missing_dependency_identified": True,
        "direct_authorization_request_blocked": True,
        "direct_authorization_grant_blocked": True,
        "direct_module_generation_blocked": True,
        "direct_mainline_resume_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "request_planning_dependency_count": len(dependency_rows),
        "request_planning_scope_count": len(planning_scope_rows),
        "request_planning_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_request_planning_only": "request planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_c_deferred": route_c.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_authorization_request_blocked": True,
        "direct_authorization_grant_blocked": True,
        "direct_module_generation_blocked": True,
        "direct_mainline_resume_blocked": True,
        "authorization_request_planning_missing_dependency_identified": True,
        "authorization_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_generation_authorization_roadmap_decision_policy": governance_constraint_module_generation_authorization_roadmap_decision_policy,
        "completed_authorization_governance_chain_review": completed_authorization_governance_chain_review,
        "authorization_roadmap_route_candidate_matrix": authorization_roadmap_route_candidate_matrix,
        "authorization_request_planning_dependency_matrix": authorization_request_planning_dependency_matrix,
        "authorization_request_planning_scope": authorization_request_planning_scope,
        "authorization_roadmap_non_release_matrix": authorization_roadmap_non_release_matrix,
        "authorization_request_entry_readiness_risk_matrix": authorization_request_entry_readiness_risk_matrix,
        "authorization_roadmap_decision_non_claims_register": authorization_roadmap_decision_non_claims_register,
        "authorization_roadmap_readiness_decision": authorization_roadmap_readiness_decision,
    }
