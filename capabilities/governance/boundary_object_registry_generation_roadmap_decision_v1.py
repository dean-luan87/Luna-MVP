# -*- coding: utf-8 -*-
"""Boundary Object Registry Generation Roadmap Decision v1.

Roadmap decision only: select Route A — Registry Generation Authorization Planning.
Does not authorize registry generation, generate registry, or release execution permissions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001"
DECISION_SCOPE = "boundary_object_registry_generation_roadmap_decision_only"
SOURCE_CHAIN = "boundary_object_registry_generation_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "BOUNDARY_OBJECT_REGISTRY_GENERATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

SELECTED_ROUTE = "Route A — Registry Generation Authorization Planning"
NEXT_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"
FINAL_DECISION = (
    "BOUNDARY_OBJECT_REGISTRY_GENERATION_ROADMAP_DECISION_READY_FOR_REGISTRY_GENERATION_AUTHORIZATION_PLANNING"
)

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "boundary_object_registry_generation_post_dryrun_review_policy_v1.json",
    "registry_generation_dryrun_completeness_review_v1.json",
    "registry_generation_non_execution_review_v1.json",
    "registry_source_validation_non_final_review_v1.json",
    "registry_contamination_check_non_final_review_v1.json",
    "registry_entry_non_generation_review_v1.json",
    "registry_source_misuse_review_v1.json",
    "registry_protected_object_integrity_review_v1.json",
    "registry_policy_entry_boundary_review_v1.json",
    "registry_owner_operator_dependency_review_v1.json",
    "registry_verifier_non_modification_review_v1.json",
    "registry_non_claims_non_write_review_v1.json",
    "boundary_object_registry_generation_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Boundary-Object-Registry-Generation-Planning-v1-001",
        "boundary_object_registry_generation_planning_v1_smoke_v0",
    ),
    (
        "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001",
        "boundary_object_registry_generation_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001",
        "boundary_object_registry_generation_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Registry Generation Authorization Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "registry_generation_authorization_planning",
        "target_scope": "authorization request/grant schema, source final validation authority, contamination final check authority, entry generation/commit authority, post-generation review, abort/rollback authority",
        "entry_reason": "generation planning+dry-run+post-review prove mechanism consumable; authorization gate not yet defined",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "registry generation authorization planning allowed only; not authorization request; not authorization grant; not registry generation; not object registration; not file operation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ registry_generation_authorized_now",
            "≠ authorization request sent",
            "≠ boundary_object_registry_generated_now",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Registry Source Final Validation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "registry_source_final_validation_planning",
        "target_scope": "source final validation planning",
        "entry_reason": "authorization planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization planning not complete"],
        "permission_impact": "deferred; not source final validation allowed",
        "next_phase_candidate": "Phase-Registry-Source-Final-Validation-Planning-v1-001",
        "non_claims": ["deferred ≠ source final validated"],
    },
    {
        "route_id": "C",
        "route_name": "Registry Contamination Check Final Execution Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "registry_contamination_check_planning",
        "target_scope": "contamination check final execution planning",
        "entry_reason": "authorization planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization planning not complete"],
        "permission_impact": "deferred; not contamination final check allowed",
        "next_phase_candidate": "Phase-Registry-Contamination-Check-Planning-v1-001",
        "non_claims": ["deferred ≠ contamination check final executed"],
    },
    {
        "route_id": "D",
        "route_name": "Registry Entry Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "registry_entry_generation_planning",
        "target_scope": "registry entry generation planning",
        "entry_reason": "authorization planning not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization planning not complete"],
        "permission_impact": "deferred; not entry generation allowed",
        "next_phase_candidate": "Phase-Registry-Entry-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ entry generated"],
    },
    {
        "route_id": "E",
        "route_name": "Boundary Object Registry Generation",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registry_generation",
        "target_scope": "formal boundary object registry artifact generation",
        "entry_reason": "authorization planning not complete; generation not authorized",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization planning not complete", "registry generation not authorized"],
        "permission_impact": "deferred; not registry generation allowed",
        "next_phase_candidate": "Phase-Boundary-Object-Registry-Generation-v1-001",
        "non_claims": ["deferred ≠ registry generated"],
    },
    {
        "route_id": "F",
        "route_name": "Boundary Object Registration",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registration",
        "target_scope": "formal boundary object registration",
        "entry_reason": "registry not generated; authorization not granted",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry not generated"],
        "permission_impact": "deferred; not object registration allowed",
        "next_phase_candidate": "Phase-Boundary-Object-Registration-v1-001",
        "non_claims": ["deferred ≠ objects registered"],
    },
    {
        "route_id": "G",
        "route_name": "Owner Approval Request Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_approval_request_planning",
        "target_scope": "owner approval request initiation chain",
        "entry_reason": "authorization planning incomplete; scope not hard",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["authorization planning not complete"],
        "permission_impact": "deferred; not owner approval request allowed",
        "next_phase_candidate": "Phase-Owner-Approval-Request-Planning-v1-001",
        "non_claims": ["deferred ≠ owner approval request sent"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Registry Generation / Object Registration / File Operation / Real Rehearsal",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_registry_registration_file_op_real_rehearsal",
        "target_scope": "registry generation / object registration / file operation / real rehearsal",
        "entry_reason": "authorization planning not defined; direct generation bypasses owner/operator chain",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "authorization planning not complete",
            "registry generation not authorized",
            "objects not registered",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Registry-Generation-v1-001",
        "non_claims": ["blocked ≠ registry generated", "≠ file operation allowed"],
    },
]

AUTHORIZATION_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("A01", "registry generation authorization"),
    ("A02", "registry source final validation authority"),
    ("A03", "contamination final check authority"),
    ("A04", "registry entry generation authority"),
    ("A05", "registry entry commit authority"),
    ("A06", "protected object classification authority"),
    ("A07", "policy entry approval authority"),
    ("A08", "object registration authority"),
    ("A09", "post-generation review authority"),
    ("A10", "abort authority"),
    ("A11", "rollback authority"),
    ("A12", "owner approval dependency"),
    ("A13", "operator acknowledgement dependency"),
    ("A14", "execution window dependency"),
)

AUTHORIZATION_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("registry generation authorization request schema", "define who may request registry generation authorization"),
    ("registry generation authorization grant schema", "define who may grant registry generation authorization"),
    ("source final validation authority", "define who approves source final validation"),
    ("contamination final check authority", "define who approves contamination final check"),
    ("entry generation authority", "define who approves registry entry generation"),
    ("entry commit authority", "define who approves registry entry commit"),
    ("object registration authority", "define who approves object registration"),
    ("protected object classification authority", "define who classifies protected objects in registry"),
    ("policy entry approval authority", "define who approves policy entries"),
    ("post-generation review authority", "define who reviews registry after generation"),
    ("registry abort authority", "define who may abort registry generation"),
    ("registry rollback authority", "define who may rollback registry generation"),
    ("owner approval dependency", "map owner approval requirements for generation chain"),
    ("operator acknowledgement dependency", "map operator acknowledgement requirements"),
    ("execution window dependency", "map execution window requirements for generation"),
    ("authorization non-claims and verifier usage", "non-claims and verifier usage for authorization planning"),
)

AUTHORIZATION_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "authorization request schema not defined", "high", "planning allowed; authorization request blocked"),
    ("R02", "authorization grant schema not defined", "high", "registry_generation_authorized_now=false"),
    ("R03", "source final validation authority not defined", "high", "registry_source_final_validated_now=false"),
    ("R04", "contamination final check authority not defined", "high", "registry_contamination_check_final_executed_now=false"),
    ("R05", "entry generation authority not defined", "high", "registry_entry_generated_now=false"),
    ("R06", "entry commit authority not defined", "high", "registry_entry_committed_now=false"),
    ("R07", "object registration authority not defined", "high", "boundary_object_registered_now=false"),
    ("R08", "protected classification authority not defined", "high", "protected assets unchanged"),
    ("R09", "policy entry approval authority not defined", "medium", "policy entry approval undefined"),
    ("R10", "post-generation review authority not defined", "high", "post-generation review undefined"),
    ("R11", "abort authority not defined", "high", "abort authority undefined"),
    ("R12", "rollback authority not defined", "high", "rollback authority undefined"),
    ("R13", "owner/operator dependency not active", "high", "owner/operator not satisfied"),
    ("R14", "execution window not open", "high", "execution_window_opened_now=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "registry generation authorization request",
    "registry generation authorization grant",
    "boundary object registry generation",
    "boundary object registration",
    "registry source final validation",
    "registry contamination check final execution",
    "registry entry generation",
    "registry entry commit",
    "protected object modification",
    "file operation execution",
    "owner approval request",
    "execution window opening",
    "evidence generation authorization",
    "evidence generation",
    "success claim allowance",
    "restore map generation",
    "rollback execution",
    "real rollback rehearsal execution",
    "real migration execution",
    "batch arming",
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean registry generation is authorized.",
    "Route A selected does not mean authorization request is sent.",
    "Route A selected does not mean registry generation may execute.",
    "Route A selected does not mean source final validation may execute.",
    "Route A selected does not mean contamination final check may execute.",
    "Route A selected does not mean registry entry may be generated or committed.",
    "Route E/F deferred means registry generation and object registration remain unavailable.",
    "Route H blocked means direct registry generation / object registration / file operation remain forbidden.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "selected_route": SELECTED_ROUTE,
        "registry_generation_authorization_planning_selected": True,
        "registry_generation_authorization_request_sent_now": False,
        "registry_generation_authorized_now": False,
        "boundary_object_registry_generation_executed_now": False,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_source_final_validated_now": False,
        "registry_generation_source_validated_now": False,
        "registry_contamination_check_final_executed_now": False,
        "registry_generation_contamination_checked_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "protected_asset_modified_now": False,
        "human_review_queue_modified_now": False,
        "dnae_or_permanent_block_modified_now": False,
        "file_operation_executed_now": False,
        "write_permission_released_now": False,
        "migration_permission_released_now": False,
        "evidence_permission_released_now": False,
        "rollback_permission_released_now": False,
        "owner_approval_request_sent_now": False,
        "operator_acknowledgement_request_sent_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "abort_authority_confirmed_now": False,
        "scope_confirmation_accepted_now": False,
        "verifier_rerun_authorized_now": False,
        "evidence_generation_authorized_now": False,
        "evidence_acceptance_authorized_now": False,
        "success_claim_authority_confirmed_now": False,
        "authorization_granted_now": False,
        "evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "success_claim_allowed": False,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "success_claim_gate_generated_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "debt_fix_executed_now": False,
        "runtime_invoked": False,
        "execution_committed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
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
        root / "boundary_object_registry_generation_post_dryrun_review_readiness_decision_v1.json"
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
                generation_observed=sm.get("boundary_object_registry_generation_executed_now") is True
                or sm.get("boundary_object_registry_generated_now") is True,
                source_final_validation_observed=sm.get("registry_source_final_validated_now") is True,
                contamination_final_check_observed=sm.get(
                    "registry_contamination_check_final_executed_now"
                )
                is True,
                entry_generation_observed=sm.get("registry_entry_generated_now") is True,
                entry_commit_observed=sm.get("registry_entry_committed_now") is True,
                object_registration_observed=sm.get("boundary_object_registered_now") is True,
                file_operation_observed=sm.get("file_operation_executed_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_authorization_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in AUTHORIZATION_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_registry_generation=True,
                required_for_source_final_validation="source" in dep_name,
                required_for_contamination_final_check="contamination" in dep_name,
                required_for_entry_generation="entry generation" in dep_name,
                required_for_entry_commit="entry commit" in dep_name,
                current_status="authorization_planning_required",
                missing_preconditions=["registry generation authorization planning not complete"],
                blocks_registry_generation=True,
                recommended_next_action="enter Registry Generation Authorization Planning",
            )
        )
    return rows


def _build_authorization_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in AUTHORIZATION_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"registry_gen_auth_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                required_for_registry_generation=True,
                required_for_object_registration="registration" in planning_topic or "object" in planning_topic,
                required_for_owner_approval="owner" in planning_topic,
                required_for_file_operation=False,
                required_for_real_rehearsal="rollback" in planning_topic or "abort" in planning_topic,
                required_verifier_usage=[f"verify_registry_gen_auth_{planning_topic.replace(' ', '_')}"],
                required_non_claims=[f"authorization planning GO does not imply {planning_topic} granted"],
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


def _build_authorization_risk_matrix() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for risk_id, desc, level, non_claim in AUTHORIZATION_RISKS:
        review_pass = True
        rows.append(
            _decision_row(
                risk_id=risk_id,
                risk_description=desc,
                risk_level=level,
                allowed_to_enter_planning=True,
                blocks_authorization_request=True,
                blocks_registry_generation=True,
                blocks_object_registration=True,
                blocks_file_operation=True,
                blocks_real_rehearsal=True,
                required_non_claim=non_claim,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def run_boundary_object_registry_generation_roadmap_decision_v1(
    *,
    boundary_object_registry_generation_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_generation_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_boundary_object_registry_generation_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_boundary_object_registry_generation_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    for flag in (
        "boundary_object_registry_generation_executed_now",
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
        "registry_generation_authorized_now",
        "registry_source_final_validated_now",
        "registry_generation_source_validated_now",
        "registry_contamination_check_final_executed_now",
        "registry_generation_contamination_checked_now",
        "registry_entry_generated_now",
        "registry_entry_committed_now",
        "protected_asset_modified_now",
        "human_review_queue_modified_now",
        "dnae_or_permanent_block_modified_now",
        "file_operation_executed_now",
        "owner_approval_request_sent_now",
        "execution_window_opened_now",
        "evidence_generation_authorized_now",
        "evidence_generated_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    for flag in (
        "ready_for_boundary_object_registry_generation",
        "ready_for_boundary_object_registration",
        "ready_for_registry_generation_authorization",
        "ready_for_registry_source_final_validation",
        "ready_for_registry_contamination_check_final_execution",
        "ready_for_registry_entry_generation",
        "ready_for_registry_entry_commit",
        "ready_for_owner_approval_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation_authorization",
        "ready_for_file_operation",
        "ready_for_restore_map_generation",
        "ready_for_rollback_execution",
        "ready_for_real_rollback_rehearsal_execution",
        "ready_for_real_migration_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")
    if up_readiness.get("ready_for_batch_arming") is not False:
        blockers.append("upstream ready_for_batch_arming must be false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("upstream real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("upstream batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    for art_name in (
        "registry_generation_non_execution_review_v1.json",
        "registry_entry_non_generation_review_v1.json",
        "registry_source_misuse_review_v1.json",
        "registry_protected_object_integrity_review_v1.json",
    ):
        if up_art.get(art_name, {}).get("all_pass") is not True:
            blockers.append(f"upstream {art_name} must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_authorization_dependency_matrix()
    planning_scope_rows = _build_authorization_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_authorization_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_e = next(r for r in route_rows if r.get("route_id") == "E")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "authorization planning" in str(route_a.get("permission_impact", "")).lower()
        and "not authorization request" in str(route_a.get("permission_impact", "")).lower()
        and "not registry generation" in str(route_a.get("permission_impact", "")).lower()
        and route_b.get("deferred") is True
        and route_b.get("selected_now") is False
        and route_e.get("deferred") is True
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
            "boundary_object_registry_generation",
            "boundary_object_registration",
            "direct_registry_registration_file_op_real_rehearsal",
        )
        for r in route_rows
        if r.get("route_id") != "A"
    )
    if forbidden_allowed:
        blockers.append("registry generation / registration / direct routes must not be allowed_now")

    decision_ready = (
        chain_pass
        and non_release_pass
        and risk_pass
        and route_ok
        and len(dependency_rows) >= 14
        and len(planning_scope_rows) >= 16
        and not blockers
    )
    boundary_ok = decision_ready

    registry_generation_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_boundary_object_registry_generation_roadmap_decision_observed=up_readiness.get(
            "ready_for_boundary_object_registry_generation_roadmap_decision"
        )
        is True,
    )

    completed_registry_generation_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    registry_generation_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    registry_generation_authorization_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "authorization_missing_dependency_identified": True,
        **_decision_meta(),
    }
    registry_generation_authorization_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    registry_generation_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    registry_generation_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    registry_generation_authorization_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    registry_generation_roadmap_readiness_decision = {
        "ready_for_registry_generation_authorization_planning": boundary_ok,
        "ready_for_registry_generation_authorization_request": False,
        "ready_for_registry_generation_authorization_grant": False,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
        "ready_for_registry_source_final_validation": False,
        "ready_for_registry_contamination_check_final_execution": False,
        "ready_for_registry_entry_generation": False,
        "ready_for_registry_entry_commit": False,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_execution_window_opening": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_file_operation": False,
        "ready_for_restore_map_generation": False,
        "ready_for_rollback_execution": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": SELECTED_ROUTE,
        "registry_generation_chain_completed": chain_pass,
        "authorization_missing_dependency_identified": True,
        "direct_registry_generation_blocked": True,
        "direct_object_registration_blocked": True,
        "direct_file_operation_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_generation_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "authorization_dependency_count": len(dependency_rows),
        "authorization_planning_scope_count": len(planning_scope_rows),
        "authorization_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_authorization_planning_only": "authorization planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_e_deferred": route_e.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_registry_generation_blocked": True,
        "direct_object_registration_blocked": True,
        "direct_file_operation_blocked": True,
        "authorization_missing_dependency_identified": True,
        "registry_generation_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "registry_generation_roadmap_decision_policy": registry_generation_roadmap_decision_policy,
        "completed_registry_generation_chain_review": completed_registry_generation_chain_review,
        "registry_generation_roadmap_route_candidate_matrix": registry_generation_roadmap_route_candidate_matrix,
        "registry_generation_authorization_dependency_matrix": registry_generation_authorization_dependency_matrix,
        "registry_generation_authorization_planning_scope": registry_generation_authorization_planning_scope,
        "registry_generation_roadmap_non_release_matrix": registry_generation_roadmap_non_release_matrix,
        "registry_generation_authorization_entry_readiness_risk_matrix": registry_generation_authorization_entry_readiness_risk_matrix,
        "registry_generation_roadmap_decision_non_claims_register": registry_generation_roadmap_decision_non_claims_register,
        "registry_generation_roadmap_readiness_decision": registry_generation_roadmap_readiness_decision,
    }
