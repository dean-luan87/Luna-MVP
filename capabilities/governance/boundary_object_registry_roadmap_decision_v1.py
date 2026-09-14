# -*- coding: utf-8 -*-
"""Boundary Object Registry Roadmap Decision v1.

Roadmap decision only: select Route A — Boundary Object Registry Generation Planning.
Does not generate registry, register objects, or release execution permissions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Roadmap-Decision-v1-001"
DECISION_SCOPE = "boundary_object_registry_roadmap_decision_only"
SOURCE_CHAIN = "boundary_object_registry_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "BOUNDARY_OBJECT_REGISTRY_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"

SELECTED_ROUTE = "Route A — Boundary Object Registry Generation Planning"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Generation-Planning-v1-001"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_ROADMAP_DECISION_READY_FOR_REGISTRY_GENERATION_PLANNING"

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "boundary_object_post_dryrun_review_policy_v1.json",
    "boundary_object_dryrun_completeness_review_v1.json",
    "boundary_registry_non_generation_review_v1.json",
    "boundary_object_registration_block_review_v1.json",
    "protected_blocked_object_integrity_review_v1.json",
    "boundary_read_write_permission_review_v1.json",
    "boundary_migration_permission_review_v1.json",
    "boundary_evidence_permission_review_v1.json",
    "boundary_rollback_permission_review_v1.json",
    "boundary_owner_operator_dependency_review_v1.json",
    "boundary_file_operation_block_review_v1.json",
    "boundary_verifier_non_modification_review_v1.json",
    "boundary_non_claims_non_write_review_v1.json",
    "boundary_object_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Boundary-Object-Registry-Planning-v1-001",
        "boundary_object_registry_planning_v1_smoke_v0",
    ),
    (
        "Phase-Boundary-Object-Registry-DryRun-v1-001",
        "boundary_object_registry_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Boundary-Object-Registry-Post-DryRun-Review-v1-001",
        "boundary_object_registry_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Boundary Object Registry Generation Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "boundary_object_registry_generation_planning",
        "target_scope": "registry generation source / integrity / contamination / entry conversion / verifier integration",
        "entry_reason": "planning+dry-run+post-review prove rules consumable; generation strategy not yet defined",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "registry generation planning allowed only; not registry generation; not object registration; not file operation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ boundary_object_registry_generated_now",
            "≠ registry generation authorized",
            "≠ boundary objects registered",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Boundary Object Registry Generation",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registry_generation",
        "target_scope": "formal boundary object registry artifact generation",
        "entry_reason": "generation planning not complete; source whitelist and contamination prevention undefined",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry generation planning not complete"],
        "permission_impact": "deferred; not registry generation allowed",
        "next_phase_candidate": "Phase-Boundary-Object-Registry-Generation-v1-001",
        "non_claims": ["deferred ≠ registry generated"],
    },
    {
        "route_id": "C",
        "route_name": "Boundary Object Registration",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registration",
        "target_scope": "formal boundary object registration",
        "entry_reason": "registry not generated; registration gate undefined",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry not generated"],
        "permission_impact": "deferred; not object registration allowed",
        "next_phase_candidate": "Phase-Boundary-Object-Registration-v1-001",
        "non_claims": ["deferred ≠ objects registered"],
    },
    {
        "route_id": "D",
        "route_name": "Owner Approval Request Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_approval_request_planning",
        "target_scope": "owner approval request initiation chain",
        "entry_reason": "registry generation planning incomplete; scope not hard",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry generation planning not complete"],
        "permission_impact": "deferred; not owner approval request allowed",
        "next_phase_candidate": "Phase-Owner-Approval-Request-Planning-v1-001",
        "non_claims": ["deferred ≠ owner approval request sent"],
    },
    {
        "route_id": "E",
        "route_name": "File Operation Authorization Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "file_operation_authorization_planning",
        "target_scope": "file operation authorization chain",
        "entry_reason": "registry not generated; file operation boundary not registered",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry generation planning not complete"],
        "permission_impact": "deferred; not file operation allowed",
        "next_phase_candidate": "Phase-File-Operation-Authorization-Planning-v1-001",
        "non_claims": ["deferred ≠ file operation executed"],
    },
    {
        "route_id": "F",
        "route_name": "Restore Map Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "restore_map_generation_planning",
        "target_scope": "restore map generation planning",
        "entry_reason": "registry and rollback boundary not finalized",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry generation planning not complete"],
        "permission_impact": "deferred; not restore map generation",
        "next_phase_candidate": "Phase-Restore-Map-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ restore map generated"],
    },
    {
        "route_id": "G",
        "route_name": "Real Rollback Rehearsal Authorization Chain Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "real_rollback_rehearsal_authorization_chain_planning",
        "target_scope": "rollback rehearsal authorization chain",
        "entry_reason": "registry and authorization chain incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["registry not generated", "approval not granted"],
        "permission_impact": "deferred; not real_rehearsal_execution_allowed",
        "next_phase_candidate": "Phase-Real-Rollback-Rehearsal-Authorization-Chain-Planning-v1-001",
        "non_claims": ["deferred ≠ real rehearsal allowed"],
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
        "entry_reason": "registry generation planning not defined; direct generation bypasses gates",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "registry generation planning not complete",
            "registry not authorized",
            "objects not registered",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Registry-Generation-v1-001",
        "non_claims": ["blocked ≠ registry generated", "≠ file operation allowed"],
    },
]

REGISTRY_GENERATION_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("G01", "source planning artifacts"),
    ("G02", "source dry-run artifacts"),
    ("G03", "source post-review artifacts"),
    ("G04", "owner/operator dependency"),
    ("G05", "evidence chain dependency"),
    ("G06", "protected object dependency"),
    ("G07", "file operation boundary dependency"),
    ("G08", "rollback boundary dependency"),
    ("G09", "migration batch dependency"),
    ("G10", "verifier usage dependency"),
    ("G11", "non-claims dependency"),
    ("G12", "contamination prevention dependency"),
    ("G13", "source integrity dependency"),
    ("G14", "generation authorization dependency"),
)

REGISTRY_GENERATION_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("registry generation source inventory", "enumerate all allowed registry generation inputs"),
    ("registry source artifact whitelist", "define which planning/dry-run/review artifacts may feed registry"),
    ("registry source integrity check", "validate source artifacts before registry generation"),
    ("registry contamination prevention", "prevent polluted or unauthorized entries in registry"),
    ("category-to-entry conversion rule", "convert 16 boundary categories to registry entries"),
    ("protected object entry rule", "protected/blocked object entry constraints"),
    ("read/write policy entry rule", "read/write policy entry mapping"),
    ("migration policy entry rule", "migration policy entry mapping"),
    ("evidence policy entry rule", "evidence policy entry mapping"),
    ("rollback policy entry rule", "rollback policy entry mapping"),
    ("owner/operator dependency entry rule", "owner/operator dependency entry mapping"),
    ("file operation policy entry rule", "file operation policy entry mapping"),
    ("forbidden shortcut entry rule", "forbidden shortcut entry mapping"),
    ("verifier usage entry rule", "verifier usage entry mapping"),
    ("non-claims entry rule", "non-claims entry mapping"),
    ("registry readiness decision rule", "readiness gate before registry generation"),
)

ENTRY_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "registry generation source not finalized", "high", "planning allowed; generation blocked"),
    ("R02", "source whitelist not defined", "high", "registry_generation_source_validated_now=false"),
    ("R03", "source integrity check not defined", "high", "source integrity undefined"),
    ("R04", "contamination prevention not defined", "high", "registry_generation_contamination_checked_now=false"),
    ("R05", "category conversion rule not defined", "high", "entry conversion undefined"),
    ("R06", "protected object rule not finalized", "high", "protected assets unchanged"),
    ("R07", "policy entry rules not finalized", "medium", "policy entries undefined"),
    ("R08", "owner/operator dependency entry rule not finalized", "high", "dependency entry undefined"),
    ("R09", "file operation entry rule not finalized", "high", "file_operation_executed_now=false"),
    ("R10", "verifier usage entry rule not finalized", "medium", "verifier integration undefined"),
    ("R11", "non-claims entry rule not finalized", "medium", "non-claims entry undefined"),
    ("R12", "registry readiness decision rule not finalized", "high", "readiness gate undefined"),
    ("R13", "registry generation not authorized", "high", "registry_generation_authorized_now=false"),
    ("R14", "object registration still blocked", "high", "boundary_object_registered_now=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "boundary object registry generation",
    "boundary object registration",
    "registry generation authorization",
    "registry source validation",
    "registry contamination check",
    "protected object modification",
    "file operation execution",
    "write permission release",
    "migration permission release",
    "evidence permission release",
    "rollback permission release",
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
    "Roadmap Decision GO does not mean boundary object registry is generated.",
    "Route A selected does not mean registry generation is authorized.",
    "Route A selected does not mean registry source artifacts are validated.",
    "Route A selected does not mean boundary objects are registered.",
    "Route A selected does not mean file operation is allowed.",
    "Route B/C deferred means registry generation and object registration remain unavailable.",
    "Route H blocked means direct registry generation / object registration / file operation remain forbidden.",
    "Roadmap Decision GO does not mean owner approval request is allowed.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "boundary_object_registry_generation_planning_selected": True,
        "boundary_object_registry_generation_executed_now": False,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_generation_authorized_now": False,
        "registry_generation_source_validated_now": False,
        "registry_generation_contamination_checked_now": False,
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
        root / "boundary_object_post_dryrun_review_readiness_decision_v1.json"
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
                registry_generation_observed=sm.get("boundary_object_registry_generated_now") is True,
                object_registration_observed=sm.get("boundary_object_registered_now") is True,
                protected_object_modification_observed=sm.get("protected_asset_modified_now") is True
                or sm.get("human_review_queue_modified_now") is True
                or sm.get("dnae_or_permanent_block_modified_now") is True,
                file_operation_observed=sm.get("file_operation_executed_now") is True,
                permission_release_observed=sm.get("write_permission_released_now") is True
                or sm.get("migration_permission_released_now") is True
                or sm.get("evidence_permission_released_now") is True
                or sm.get("rollback_permission_released_now") is True,
                owner_approval_request_observed=sm.get("owner_approval_request_sent_now") is True,
                evidence_authorization_observed=sm.get("evidence_generation_authorized_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_generation_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in REGISTRY_GENERATION_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_registry_generation=True,
                current_status="planning_required",
                missing_preconditions=["registry generation planning not complete"],
                blocks_registry_generation=True,
                blocks_object_registration=True,
                recommended_next_action="enter Boundary Object Registry Generation Planning",
            )
        )
    return rows


def _build_generation_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in REGISTRY_GENERATION_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"registry_gen_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                required_for_registry_generation=True,
                required_for_object_registration="entry" in planning_topic or "conversion" in planning_topic,
                required_for_owner_approval="owner/operator" in planning_topic,
                required_for_evidence_generation="evidence" in planning_topic,
                required_for_real_rehearsal="rollback" in planning_topic,
                required_verifier_usage=[f"verify_registry_gen_{planning_topic.replace(' ', '_')}"],
                required_non_claims=[f"planning GO does not imply {planning_topic} executed"],
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


def _build_entry_risk_matrix() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for risk_id, desc, level, non_claim in ENTRY_RISKS:
        review_pass = True
        rows.append(
            _decision_row(
                risk_id=risk_id,
                risk_description=desc,
                risk_level=level,
                allowed_to_enter_planning=True,
                blocks_registry_generation=True,
                blocks_object_registration=True,
                blocks_file_operation=True,
                blocks_real_rehearsal=True,
                required_non_claim=non_claim,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def run_boundary_object_registry_roadmap_decision_v1(
    *,
    boundary_object_registry_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_boundary_object_registry_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_boundary_object_registry_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    for flag in (
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
        "protected_asset_modified_now",
        "human_review_queue_modified_now",
        "dnae_or_permanent_block_modified_now",
        "file_operation_executed_now",
        "write_permission_released_now",
        "migration_permission_released_now",
        "evidence_permission_released_now",
        "rollback_permission_released_now",
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
        "ready_for_owner_approval_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation_authorization",
        "ready_for_file_operation",
        "ready_for_restore_map_generation",
        "ready_for_rollback_execution",
        "ready_for_real_rollback_rehearsal_execution",
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
        "boundary_registry_non_generation_review_v1.json",
        "boundary_object_registration_block_review_v1.json",
        "protected_blocked_object_integrity_review_v1.json",
        "boundary_file_operation_block_review_v1.json",
    ):
        if up_art.get(art_name, {}).get("all_pass") is not True:
            blockers.append(f"upstream {art_name} must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_generation_dependency_matrix()
    planning_scope_rows = _build_generation_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_entry_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "planning" in str(route_a.get("permission_impact", "")).lower()
        and "not registry generation" in str(route_a.get("permission_impact", "")).lower()
        and route_b.get("deferred") is True
        and route_b.get("selected_now") is False
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
            "file_operation_authorization_planning",
            "direct_registry_registration_file_op_real_rehearsal",
        )
        for r in route_rows
        if r.get("route_id") != "A"
    )
    if forbidden_allowed:
        blockers.append("registry generation / registration / file operation routes must not be allowed_now")

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

    boundary_object_registry_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_boundary_object_registry_roadmap_decision_observed=up_readiness.get(
            "ready_for_boundary_object_registry_roadmap_decision"
        )
        is True,
    )

    completed_boundary_object_registry_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    boundary_object_registry_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    boundary_registry_generation_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "registry_generation_missing_dependency_identified": True,
        **_decision_meta(),
    }
    boundary_registry_generation_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    boundary_registry_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    boundary_registry_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    registry_generation_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    boundary_registry_roadmap_readiness_decision = {
        "ready_for_boundary_object_registry_generation_planning": boundary_ok,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
        "ready_for_registry_generation_authorization": False,
        "ready_for_registry_source_validation": False,
        "ready_for_registry_contamination_check": False,
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
        "boundary_object_registry_chain_completed": chain_pass,
        "registry_generation_missing_dependency_identified": True,
        "direct_registry_generation_blocked": True,
        "direct_object_registration_blocked": True,
        "direct_file_operation_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "generation_dependency_count": len(dependency_rows),
        "generation_planning_scope_count": len(planning_scope_rows),
        "entry_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_planning_only": "planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_registry_generation_blocked": True,
        "direct_object_registration_blocked": True,
        "direct_file_operation_blocked": True,
        "registry_generation_missing_dependency_identified": True,
        "boundary_object_registry_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_registry_roadmap_decision_policy": boundary_object_registry_roadmap_decision_policy,
        "completed_boundary_object_registry_chain_review": completed_boundary_object_registry_chain_review,
        "boundary_object_registry_roadmap_route_candidate_matrix": boundary_object_registry_roadmap_route_candidate_matrix,
        "boundary_registry_generation_dependency_matrix": boundary_registry_generation_dependency_matrix,
        "boundary_registry_generation_planning_scope": boundary_registry_generation_planning_scope,
        "boundary_registry_roadmap_non_release_matrix": boundary_registry_roadmap_non_release_matrix,
        "registry_generation_entry_readiness_risk_matrix": registry_generation_entry_readiness_risk_matrix,
        "boundary_registry_roadmap_decision_non_claims_register": boundary_registry_roadmap_decision_non_claims_register,
        "boundary_registry_roadmap_readiness_decision": boundary_registry_roadmap_readiness_decision,
    }
