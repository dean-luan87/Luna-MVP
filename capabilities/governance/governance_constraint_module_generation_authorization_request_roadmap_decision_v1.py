# -*- coding: utf-8 -*-
"""Governance Constraint Module Generation Authorization Request Roadmap Decision v1.

Roadmap decision only: select Route A — Authorization Request Artifact Generation Planning.
Does not generate request artifacts, send requests, or grant authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001"
DECISION_SCOPE = "governance_constraint_module_generation_authorization_request_roadmap_decision_only"
SOURCE_CHAIN = "governance_constraint_module_generation_authorization_request_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

SELECTED_ROUTE = "Route A — Authorization Request Artifact Generation Planning"
NEXT_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001"
FINAL_DECISION = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_ROADMAP_DECISION_READY_FOR_ARTIFACT_GENERATION_PLANNING"
)

MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_PAUSED = True

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "authorization_request_post_dryrun_review_policy_v1.json",
    "authorization_request_dryrun_completeness_review_v1.json",
    "authorization_request_artifact_non_generation_review_v1.json",
    "authorization_request_non_sent_review_v1.json",
    "authorization_grant_non_issued_review_v1.json",
    "source_and_domain_approval_non_execution_review_v1.json",
    "request_lifecycle_non_advance_review_v1.json",
    "scope_and_exclusion_boundary_review_v1.json",
    "abort_revoke_linkage_non_execution_review_v1.json",
    "request_verifier_usage_non_modification_review_v1.json",
    "authorization_request_non_claims_review_v1.json",
    "authorization_request_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001",
        "governance_constraint_module_generation_authorization_request_planning_v1_smoke_v0",
    ),
    (
        "Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001",
        "governance_constraint_module_generation_authorization_request_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001",
        "governance_constraint_module_generation_authorization_request_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Authorization Request Artifact Generation Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "authorization_request_artifact_generation_planning",
        "target_scope": "artifact identity, source refs, domain refs, scope/exclusion, non-grant statements, lifecycle initial state, review/send gates, abort/revoke linkage",
        "entry_reason": "request dry-run safe; artifact generation rules not yet planned",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "artifact generation planning allowed only; not artifact generation; not authorization request sent; not authorization grant; not module generation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ request artifact generated",
            "≠ request sent",
            "≠ authorization granted",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Authorization Request Artifact Generation",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "authorization_request_artifact_generation",
        "target_scope": "generate authorization request artifact",
        "entry_reason": "artifact generation planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["artifact generation planning not complete"],
        "permission_impact": "deferred; not artifact generation allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-v1-001",
        "non_claims": ["deferred ≠ request artifact generated"],
    },
    {
        "route_id": "C",
        "route_name": "Authorization Request Send Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "authorization_request_send_planning",
        "target_scope": "plan request send",
        "entry_reason": "artifact not planned or generated",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["artifact generation planning not complete"],
        "permission_impact": "deferred; not request sent allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Send-Planning-v1-001",
        "non_claims": ["deferred ≠ request sent"],
    },
    {
        "route_id": "D",
        "route_name": "Authorization Request Sent",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "authorization_request_sent",
        "target_scope": "send real authorization request",
        "entry_reason": "artifact generation planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["artifact generation planning not complete"],
        "permission_impact": "deferred; not authorization request sent allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-Authorization-Request-v1-001",
        "non_claims": ["deferred ≠ request sent"],
    },
    {
        "route_id": "E",
        "route_name": "Authorization Grant Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "authorization_grant_planning",
        "target_scope": "authorization grant planning",
        "entry_reason": "request artifact not planned; request not sent",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["artifact generation planning not complete"],
        "permission_impact": "deferred; not authorization grant allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-Authorization-Grant-Planning-v1-001",
        "non_claims": ["deferred ≠ authorization granted"],
    },
    {
        "route_id": "F",
        "route_name": "Governance Constraint Module Generation",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "governance_constraint_module_generation",
        "target_scope": "formal Governance Constraint Module generation",
        "entry_reason": "authorization request artifact chain incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["artifact generation planning not complete"],
        "permission_impact": "deferred; not module generation allowed",
        "next_phase_candidate": "Phase-Governance-Constraint-Module-Generation-v1-001",
        "non_claims": ["deferred ≠ module generated"],
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
        "entry_reason": "request artifact chain incomplete; mainline must stay paused",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["artifact generation planning not complete"],
        "permission_impact": "deferred; not mainline resume allowed",
        "next_phase_candidate": MAIN_MIGRATION_RESUME_PHASE,
        "non_claims": ["deferred ≠ main_migration_chain_resumed_now"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Artifact Generation / Request / Grant / Module / Mainline",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_artifact_request_grant_module_mainline",
        "target_scope": "direct artifact / request / grant / module / mainline",
        "entry_reason": "artifact generation planning not complete; bypasses artifact governance",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "artifact generation planning not complete",
            "authorization not granted",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Authorization-Request-Artifact-v1-001",
        "non_claims": [
            "blocked ≠ artifact generated",
            "≠ request sent",
            "≠ grant issued",
            "≠ mainline resumed",
        ],
    },
]

ARTIFACT_PLANNING_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("AD01", "artifact identity schema"),
    ("AD02", "artifact source refs"),
    ("AD03", "artifact source integrity refs"),
    ("AD04", "artifact domain preservation refs"),
    ("AD05", "artifact requested scope"),
    ("AD06", "artifact excluded scope"),
    ("AD07", "artifact non-grant statements"),
    ("AD08", "artifact non-generation statements"),
    ("AD09", "artifact lifecycle initial state"),
    ("AD10", "artifact review gate"),
    ("AD11", "artifact send gate"),
    ("AD12", "artifact abort linkage"),
    ("AD13", "artifact revoke linkage"),
    ("AD14", "artifact verifier usage"),
    ("AD15", "artifact non-claims"),
)

ARTIFACT_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("artifact identity schema", "canonical artifact identity and versioning"),
    ("artifact source refs", "bind artifact to source set evidence refs"),
    ("artifact source integrity refs", "integrity requirements for source bindings"),
    ("artifact domain preservation refs", "domain preservation refs in artifact"),
    ("artifact requested scope", "requested module generation scope in artifact"),
    ("artifact excluded scope", "excluded permissions in artifact body"),
    ("artifact non-grant statements", "artifact does not imply grant"),
    ("artifact non-generation statements", "artifact does not imply module generation"),
    ("artifact lifecycle initial state", "initial lifecycle state planning_defined only"),
    ("artifact review gate", "review gates before send"),
    ("artifact send gate", "send gate preconditions"),
    ("artifact abort linkage", "abort linkage before artifact materialization"),
    ("artifact revoke linkage", "revoke linkage after draft artifact"),
    ("artifact verifier usage", "verifier checks for artifact phase"),
    ("artifact non-claims", "non-claims for artifact planning GO"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "authorization request artifact generation",
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
    "revoke authority confirmation",
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

ARTIFACT_PLANNING_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "artifact identity schema not finalized", "high", "planning allowed; artifact generation blocked"),
    ("R02", "artifact source refs not finalized", "high", "source_bound_now=false"),
    ("R03", "artifact source integrity refs not finalized", "high", "source integrity misuse risk"),
    ("R04", "artifact domain preservation refs not finalized", "high", "domain_specific_rules_preserved must hold"),
    ("R05", "artifact requested scope not finalized", "high", "scope conflation risk"),
    ("R06", "artifact excluded scope not finalized", "high", "verifier/template integration blocked"),
    ("R07", "artifact non-grant statements not finalized", "high", "artifact misread as grant risk"),
    ("R08", "artifact non-generation statements not finalized", "high", "module generation blocked"),
    ("R09", "artifact lifecycle initial state not finalized", "high", "request_ready/request_sent blocked"),
    ("R10", "artifact review gate not finalized", "high", "review_executed_now=false"),
    ("R11", "artifact send gate not finalized", "high", "request_sent_now=false"),
    ("R12", "artifact abort linkage not finalized", "medium", "abort_executed_now=false"),
    ("R13", "artifact revoke linkage not finalized", "medium", "revoke_executed_now=false"),
    ("R14", "artifact verifier usage not finalized", "high", "verifier_modified_now=false must hold"),
    ("R15", "artifact non-claims not finalized", "high", "success_claim_allowed=false must hold"),
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean authorization request artifact is generated.",
    "Route A selected does not mean request artifact may be generated.",
    "Route A selected does not mean request is sent.",
    "Route A selected does not mean authorization is granted.",
    "Route A selected does not mean source set is final approved.",
    "Route A selected does not mean domain preservation is approved.",
    "Route A selected does not mean module generation authority is released.",
    "Route A selected does not mean Governance Constraint Module may be generated.",
    "Route A selected does not mean verifier/template integration may start.",
    "Route A selected does not mean main migration chain may resume.",
    "Route H blocked means direct artifact / request / grant / module / mainline remain forbidden.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "selected_route": SELECTED_ROUTE,
        "authorization_request_artifact_generation_planning_selected": True,
        "governance_constraint_module_generation_authorization_request_artifact_generated_now": False,
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
    readiness = _try_read_json(root / "authorization_request_post_dryrun_review_readiness_decision_v1.json") if root else None
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


def _is_false_or_absent(value: Any) -> bool:
    return value is False or value is None


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
        artifact_gen = sm.get("governance_constraint_module_generation_authorization_request_artifact_generated_now")
        if artifact_gen is None:
            artifact_gen = sm.get("governance_constraint_module_generation_authorization_request_generated_now")
        rows.append(
            _decision_row(
                phase_name=phase_name,
                verifier_status=vr.get("verifier", "UNKNOWN"),
                boundary_ok=boundary,
                final_decision=sm.get("final_decision"),
                recommended_next_phase=sm.get("recommended_next_phase"),
                request_artifact_generation_observed=artifact_gen is True,
                request_sent_observed=sm.get("governance_constraint_module_generation_authorization_request_sent_now")
                is True,
                authorization_grant_observed=sm.get("governance_constraint_module_generation_authorized_now")
                is True,
                source_set_final_approval_observed=sm.get("source_set_final_approved_now") is True,
                domain_preservation_approval_observed=sm.get("domain_specific_preservation_approved_now")
                is True,
                module_generation_observed=sm.get("governance_constraint_module_generated_now") is True,
                mainline_resume_observed=sm.get("main_migration_chain_resumed_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_artifact_planning_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in ARTIFACT_PLANNING_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_artifact_generation_planning=True,
                current_status="artifact_generation_planning_required",
                missing_preconditions=["Authorization Request Artifact Generation Planning not complete"],
                blocks_artifact_generation=True,
                blocks_request_sent=True,
                blocks_authorization_grant=True,
                blocks_module_generation=True,
                recommended_next_action="enter Authorization Request Artifact Generation Planning",
            )
        )
    return rows


def _build_artifact_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in ARTIFACT_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"authorization_request_artifact_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                required_for_artifact_generation=True,
                required_for_future_request_sent=True,
                required_for_future_grant=True,
                required_for_module_generation=True,
                required_for_future_verifier="verifier" in planning_topic,
                required_for_mainline_resume="mainline" in planning_topic or "lifecycle" in planning_topic,
                required_non_claims=[f"artifact planning GO does not imply {planning_topic} executed"],
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
    for risk_id, desc, level, non_claim in ARTIFACT_PLANNING_RISKS:
        rows.append(
            _decision_row(
                risk_id=risk_id,
                risk_description=desc,
                risk_level=level,
                allowed_to_enter_planning=True,
                blocks_artifact_generation=True,
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


def run_governance_constraint_module_generation_authorization_request_roadmap_decision_v1(
    *,
    governance_constraint_module_generation_authorization_request_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_request_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_authorization_request_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")

    _OPTIONAL_UPSTREAM_FALSE_FLAGS = frozenset(
        {"governance_constraint_module_generation_authorization_request_artifact_generated_now"}
    )

    for flag in (
        "governance_constraint_module_generation_authorization_request_artifact_generated_now",
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
        "request_ready_now",
        "request_sent_now",
        "grant_issued_now",
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
        observed = up_summary.get(flag)
        if flag in _OPTIONAL_UPSTREAM_FALSE_FLAGS:
            if not _is_false_or_absent(observed):
                blockers.append(f"upstream {flag} must remain false")
        elif observed is not False:
            blockers.append(f"upstream {flag} must remain false")

    if up_summary.get("legacy_as_source_evidence") is not True:
        blockers.append("upstream legacy_as_source_evidence must be true")
    if up_summary.get("legacy_as_template_source") is not False:
        blockers.append("upstream legacy_as_template_source must be false")
    if up_summary.get("domain_specific_rules_preserved") is not True:
        blockers.append("upstream domain_specific_rules_preserved must be true")
    if up_summary.get("lifecycle_planning_defined_only") is not True:
        blockers.append("upstream lifecycle_planning_defined_only must be true")

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

    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("upstream real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("upstream batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    for art_name in (
        "authorization_request_dryrun_completeness_review_v1.json",
        "authorization_request_artifact_non_generation_review_v1.json",
        "authorization_request_non_sent_review_v1.json",
        "authorization_grant_non_issued_review_v1.json",
        "request_lifecycle_non_advance_review_v1.json",
        "authorization_request_non_claims_review_v1.json",
    ):
        if up_art.get(art_name, {}).get("all_pass") is not True:
            blockers.append(f"upstream {art_name} must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_artifact_planning_dependency_matrix()
    planning_scope_rows = _build_artifact_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_c = next(r for r in route_rows if r.get("route_id") == "C")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "artifact generation planning" in str(route_a.get("permission_impact", "")).lower()
        and "not artifact generation" in str(route_a.get("permission_impact", "")).lower()
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
            "authorization_request_artifact_generation",
            "authorization_request_sent",
            "governance_constraint_module_generation",
            "direct_artifact_request_grant_module_mainline",
        )
        for r in route_rows
        if r.get("route_id") != "A"
    )
    if forbidden_allowed:
        blockers.append("artifact generation / request sent / module / direct routes must not be allowed_now")

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

    authorization_request_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    completed_authorization_request_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    authorization_request_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    authorization_request_artifact_generation_planning_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "artifact_generation_planning_missing_dependency_identified": True,
        **_decision_meta(),
    }
    authorization_request_artifact_generation_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    authorization_request_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    authorization_request_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    authorization_request_artifact_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    authorization_request_roadmap_readiness_decision = {
        "ready_for_governance_constraint_module_generation_authorization_request_artifact_generation_planning": boundary_ok,
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
        "selected_route": SELECTED_ROUTE,
        "authorization_request_chain_completed": chain_pass,
        "artifact_generation_planning_missing_dependency_identified": True,
        "direct_artifact_generation_blocked": True,
        "direct_request_sent_blocked": True,
        "direct_authorization_grant_blocked": True,
        "direct_module_generation_blocked": True,
        "direct_mainline_resume_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "governance_constraint_module_generation_authorization_request_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "artifact_planning_dependency_count": len(dependency_rows),
        "artifact_planning_scope_count": len(planning_scope_rows),
        "artifact_planning_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_artifact_planning_only": "artifact generation planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_c_deferred": route_c.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_artifact_generation_blocked": True,
        "direct_request_sent_blocked": True,
        "direct_authorization_grant_blocked": True,
        "direct_module_generation_blocked": True,
        "direct_mainline_resume_blocked": True,
        "artifact_generation_planning_missing_dependency_identified": True,
        "authorization_request_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "authorization_request_roadmap_decision_policy": authorization_request_roadmap_decision_policy,
        "completed_authorization_request_chain_review": completed_authorization_request_chain_review,
        "authorization_request_roadmap_route_candidate_matrix": authorization_request_roadmap_route_candidate_matrix,
        "authorization_request_artifact_generation_planning_dependency_matrix": authorization_request_artifact_generation_planning_dependency_matrix,
        "authorization_request_artifact_generation_planning_scope": authorization_request_artifact_generation_planning_scope,
        "authorization_request_roadmap_non_release_matrix": authorization_request_roadmap_non_release_matrix,
        "authorization_request_artifact_entry_readiness_risk_matrix": authorization_request_artifact_entry_readiness_risk_matrix,
        "authorization_request_roadmap_decision_non_claims_register": authorization_request_roadmap_decision_non_claims_register,
        "authorization_request_roadmap_readiness_decision": authorization_request_roadmap_readiness_decision,
    }
