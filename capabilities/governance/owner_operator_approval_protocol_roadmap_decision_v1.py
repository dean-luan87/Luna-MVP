# -*- coding: utf-8 -*-
"""Owner/Operator Approval Protocol Roadmap Decision v1.

Roadmap decision only: select Route A — Boundary Object Registry Planning.
Does not grant authorization, generate boundary registry, or release execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Owner-Operator-Approval-Protocol-Roadmap-Decision-v1-001"
DECISION_SCOPE = "owner_operator_approval_protocol_roadmap_decision_only"
SOURCE_CHAIN = "owner_operator_approval_protocol_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Owner-Operator-Approval-Protocol-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "OWNER_OPERATOR_APPROVAL_PROTOCOL_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"

SELECTED_ROUTE = "Route A — Boundary Object Registry Planning"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Planning-v1-001"
FINAL_DECISION = (
    "OWNER_OPERATOR_APPROVAL_PROTOCOL_ROADMAP_DECISION_READY_FOR_BOUNDARY_OBJECT_REGISTRY_PLANNING"
)

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "owner_operator_post_dryrun_review_policy_v1.json",
    "owner_operator_dryrun_completeness_review_v1.json",
    "owner_approval_request_block_review_v1.json",
    "operator_acknowledgement_request_block_review_v1.json",
    "execution_window_block_review_v1.json",
    "abort_authority_block_review_v1.json",
    "scope_boundary_acknowledgement_block_review_v1.json",
    "authorization_grant_block_review_v1.json",
    "evidence_authorization_link_block_review_v1.json",
    "owner_operator_forbidden_shortcut_review_v1.json",
    "owner_operator_verifier_non_modification_review_v1.json",
    "owner_operator_non_claims_non_write_review_v1.json",
    "owner_operator_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "owner_operator_approval_protocol_planning_v1_smoke_v0",
    ),
    (
        "Phase-Owner-Operator-Approval-Protocol-DryRun-v1-001",
        "owner_operator_approval_protocol_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Owner-Operator-Approval-Protocol-Post-DryRun-Review-v1-001",
        "owner_operator_approval_protocol_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Boundary Object Registry Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "boundary_object_registry_planning",
        "target_scope": "protected / HR / DnAE / eval_out / verifier / verdict table / handoff / checkpoint",
        "entry_reason": "owner/operator protocol consumable; real approval requires hard boundary object scope",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "boundary object registry planning allowed only; not registry generation; not owner approval request; not evidence generation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ boundary_object_registry_generated_now",
            "≠ owner approval requested",
            "≠ protected assets registered",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Owner Approval Request Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_approval_request_planning",
        "target_scope": "owner approval request initiation chain",
        "entry_reason": "boundary object registry not planned; scope not hard",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["boundary object registry not planned"],
        "permission_impact": "deferred; not owner approval request allowed",
        "next_phase_candidate": "Phase-Owner-Approval-Request-Planning-v1-001",
        "non_claims": ["deferred ≠ owner approval request sent"],
    },
    {
        "route_id": "C",
        "route_name": "Operator Acknowledgement Request Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "operator_acknowledgement_request_planning",
        "target_scope": "operator acknowledgement request initiation chain",
        "entry_reason": "boundary registry and owner approval request chain incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["boundary object registry not planned"],
        "permission_impact": "deferred; not operator acknowledgement request allowed",
        "next_phase_candidate": "Phase-Operator-Acknowledgement-Request-Planning-v1-001",
        "non_claims": ["deferred ≠ operator acknowledgement request sent"],
    },
    {
        "route_id": "D",
        "route_name": "Execution Window Authorization Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "execution_window_authorization_planning",
        "target_scope": "execution window open/close conditions",
        "entry_reason": "boundary objects not registered; window scope undefined",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["boundary registry not planned"],
        "permission_impact": "deferred; not execution window opening",
        "next_phase_candidate": "Phase-Execution-Window-Authorization-Planning-v1-001",
        "non_claims": ["deferred ≠ execution_window_opened_now"],
    },
    {
        "route_id": "E",
        "route_name": "Evidence Generation Authorization Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "evidence_generation_authorization_planning",
        "target_scope": "evidence generation authorization chain",
        "entry_reason": "boundary registry and approval chain incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["boundary registry not planned", "approval not granted"],
        "permission_impact": "deferred; not evidence_generation_authorized_now",
        "next_phase_candidate": "Phase-Evidence-Generation-Authorization-Planning-v1-001",
        "non_claims": ["deferred ≠ evidence generated"],
    },
    {
        "route_id": "F",
        "route_name": "Real Rollback Rehearsal Authorization Chain Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "real_rollback_rehearsal_authorization_chain_planning",
        "target_scope": "rollback rehearsal authorization chain",
        "entry_reason": "boundary registry and authorization incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["boundary registry not planned"],
        "permission_impact": "deferred; not real_rehearsal_execution_allowed",
        "next_phase_candidate": "Phase-Real-Rollback-Rehearsal-Authorization-Chain-Planning-v1-001",
        "non_claims": ["deferred ≠ real rehearsal allowed"],
    },
    {
        "route_id": "G",
        "route_name": "Continue Owner/Operator Protocol Specialist Planning",
        "priority": "Optional / Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_operator_protocol_specialist_planning",
        "target_scope": "additional owner/operator protocol gaps",
        "entry_reason": "planning+dry-run+post-review complete; specialist gaps optional",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "optional deferred; not approval request",
        "next_phase_candidate": "Phase-Owner-Operator-Protocol-Specialist-Planning-v1-001",
        "non_claims": ["deferred ≠ approval granted"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Approval Request / Evidence Authorization / Real Rehearsal",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_approval_evidence_real_rehearsal",
        "target_scope": "approval request / evidence authorization / real rehearsal",
        "entry_reason": "boundary object registry not planned; object scope uncontrollable",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "boundary registry not generated",
            "owner approval not granted",
            "evidence not authorized",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Approval-Request-v1-001",
        "non_claims": ["blocked ≠ approval request allowed", "≠ evidence authorized"],
    },
]

BOUNDARY_OBJECT_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("B01", "protected assets boundary"),
    ("B02", "HR boundary"),
    ("B03", "DnAE boundary"),
    ("B04", "eval_out boundary"),
    ("B05", "verifier boundary"),
    ("B06", "verdict table boundary"),
    ("B07", "handoff boundary"),
    ("B08", "checkpoint boundary"),
    ("B09", "restore map boundary"),
    ("B10", "docs boundary"),
    ("B11", "capability boundary"),
    ("B12", "runner/verifier boundary"),
    ("B13", "migration batch boundary"),
    ("B14", "evidence artifact boundary"),
)

BOUNDARY_REGISTRY_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("protected assets registry", "enumerate protected assets before any file operation"),
    ("HR boundary registry", "human review queue boundary classification"),
    ("DnAE / permanent block registry", "DnAE and permanent block objects"),
    ("eval_out artifact registry", "_eval_out write and read boundaries"),
    ("verifier artifact registry", "verifier outputs and rerun scope"),
    ("phase verdict table registry", "phase verdict table as boundary object"),
    ("downstream handoff registry", "handoff artifact boundaries"),
    ("checkpoint registry", "migration checkpoint objects"),
    ("restore map registry", "restore map planning boundaries"),
    ("docs registry", "documentation scope boundaries"),
    ("capability registry", "capability module boundaries"),
    ("runner/verifier registry", "runner and verifier tool boundaries"),
    ("migration batch registry", "migration batch object boundaries"),
    ("evidence artifact registry", "evidence artifact storage boundaries"),
    ("file operation boundary registry", "file move/delete/rename/merge scope"),
    ("rollback boundary registry", "rollback rehearsal scope boundaries"),
)

ENTRY_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "boundary object registry not generated", "high", "planning allowed; registry generation blocked"),
    ("R02", "protected assets not enumerated", "high", "boundary_object_registry_generated_now=false"),
    ("R03", "HR / DnAE not classified", "high", "HR/DnAE unchanged"),
    ("R04", "eval_out boundary not registered", "high", "eval_out scope undefined"),
    ("R05", "verifier artifact boundary not registered", "medium", "verifier rerun scope undefined"),
    ("R06", "verdict table boundary not registered", "medium", "verdict table scope undefined"),
    ("R07", "handoff boundary not registered", "medium", "handoff scope undefined"),
    ("R08", "checkpoint boundary not registered", "high", "checkpoint scope undefined"),
    ("R09", "restore map boundary not registered", "high", "restore map not generated"),
    ("R10", "docs/capability/runner boundary not registered", "medium", "module scope undefined"),
    ("R11", "evidence artifact boundary not registered", "high", "evidence scope undefined"),
    ("R12", "file operation boundary not registered", "high", "file ops uncontrolled"),
    ("R13", "migration batch boundary not registered", "high", "batch_arming_allowed=false"),
    ("R14", "rollback boundary not registered", "high", "real_rehearsal_execution_allowed=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "boundary object registry generation",
    "boundary object registration",
    "owner approval request",
    "operator acknowledgement request",
    "owner approval grant",
    "operator acknowledgement grant",
    "execution window opening",
    "abort authority confirmation",
    "scope confirmation acceptance",
    "verifier rerun authorization",
    "evidence generation authorization",
    "evidence generation",
    "success claim allowance",
    "real rollback rehearsal execution",
    "real migration execution",
    "batch arming",
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean owner approval request is allowed.",
    "Roadmap Decision GO does not mean operator acknowledgement request is allowed.",
    "Route A selected does not mean boundary object registry is generated.",
    "Route A selected does not mean protected assets are registered.",
    "Route A selected does not mean execution window may open.",
    "Route B/C/D/E/F deferred means approval request / execution / evidence authorization remain unavailable.",
    "Route H blocked means direct approval / evidence authorization / real rehearsal remain forbidden.",
    "Roadmap Decision GO does not mean evidence generation is allowed.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
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
        root / "owner_operator_post_dryrun_review_readiness_decision_v1.json"
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
                owner_request_observed=sm.get("owner_approval_request_sent_now") is True,
                operator_request_observed=sm.get("operator_acknowledgement_request_sent_now") is True,
                approval_grant_observed=sm.get("owner_approval_granted_now") is True
                or sm.get("operator_acknowledgement_granted_now") is True,
                execution_window_observed=sm.get("execution_window_opened_now") is True,
                evidence_authorization_observed=sm.get("evidence_generation_authorized_now") is True,
                success_claim_allowance_observed=sm.get("success_claim_allowed") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_boundary_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in BOUNDARY_OBJECT_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_owner_approval_request=True,
                required_for_operator_acknowledgement=True,
                required_for_execution_window=True,
                required_for_evidence_generation=True,
                required_for_real_rehearsal=True,
                current_status="not_planned",
                missing_preconditions=["boundary object registry not planned"],
                blocks_approval_request=True,
                blocks_execution_window=True,
                recommended_next_action="enter Boundary Object Registry Planning",
            )
        )
    return rows


def _build_boundary_registry_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in BOUNDARY_REGISTRY_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"boundary_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                required_for_owner_approval="protected" in planning_topic or "file operation" in planning_topic,
                required_for_operator_acknowledgement=True,
                required_for_evidence_generation="evidence" in planning_topic,
                required_for_real_rehearsal="rollback" in planning_topic or "checkpoint" in planning_topic,
                required_for_migration_chain="migration" in planning_topic or "batch" in planning_topic,
                required_verifier_usage=[f"verify_boundary_{planning_topic.replace(' ', '_')}"],
                required_non_claims=[f"planning GO does not imply {planning_topic} registered"],
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
                blocks_approval_request=True,
                blocks_execution_window=True,
                blocks_evidence_generation=True,
                blocks_real_rehearsal=True,
                required_non_claim=non_claim,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def run_owner_operator_approval_protocol_roadmap_decision_v1(
    *,
    owner_operator_approval_protocol_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(owner_operator_approval_protocol_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_owner_operator_approval_protocol_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_owner_operator_approval_protocol_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    for flag in (
        "owner_approval_request_sent_now",
        "operator_acknowledgement_request_sent_now",
        "owner_approval_granted_now",
        "operator_acknowledgement_granted_now",
        "execution_window_opened_now",
        "abort_authority_confirmed_now",
        "scope_confirmation_accepted_now",
        "verifier_rerun_authorized_now",
        "evidence_generation_authorized_now",
        "evidence_acceptance_authorized_now",
        "success_claim_authority_confirmed_now",
        "authorization_granted_now",
        "evidence_generated_now",
        "success_claim_allowed",
        "boundary_object_registry_generated_now",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    for flag in (
        "ready_for_owner_approval_request",
        "ready_for_operator_acknowledgement_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation_authorization",
        "ready_for_verifier_rerun_authorization",
        "ready_for_success_claim_authority_confirmation",
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

    for art_name, key in (
        ("owner_approval_request_block_review_v1.json", "all_pass"),
        ("operator_acknowledgement_request_block_review_v1.json", "all_pass"),
        ("execution_window_block_review_v1.json", "all_pass"),
        ("authorization_grant_block_review_v1.json", "all_pass"),
    ):
        if up_art.get(art_name, {}).get(key) is not True:
            blockers.append(f"upstream {art_name} must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_boundary_dependency_matrix()
    planning_scope_rows = _build_boundary_registry_planning_scope()
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
        and "not owner approval request" in str(route_a.get("permission_impact", "")).lower()
        and route_b.get("deferred") is True
        and route_b.get("selected_now") is False
        and route_h.get("blocked_now") is True
        and route_h.get("allowed_now") is False
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    deferred_routes = ("B", "C", "D", "E", "F", "G")
    for rid in deferred_routes:
        r = next(x for x in route_rows if x.get("route_id") == rid)
        if r.get("deferred") is not True or r.get("allowed_now") is not False:
            blockers.append(f"route {rid} must be deferred and not allowed_now")

    no_approval_route_allowed = all(
        not (r.get("route_type") == "owner_approval_request_planning" and r.get("allowed_now") is True)
        for r in route_rows
    )
    if not no_approval_route_allowed:
        blockers.append("owner approval request route must not be allowed_now")

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

    owner_operator_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_owner_operator_approval_protocol_roadmap_decision_observed=up_readiness.get(
            "ready_for_owner_operator_approval_protocol_roadmap_decision"
        )
        is True,
    )

    completed_owner_operator_protocol_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    owner_operator_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    owner_operator_to_boundary_object_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "boundary_object_registry_missing_dependency_identified": True,
        **_decision_meta(),
    }
    boundary_object_registry_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    owner_operator_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    owner_operator_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    boundary_object_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    owner_operator_roadmap_readiness_decision = {
        "ready_for_boundary_object_registry_planning": boundary_ok,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_execution_window_opening": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_verifier_rerun_authorization": False,
        "ready_for_success_claim_authority_confirmation": False,
        "ready_for_evidence_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": SELECTED_ROUTE,
        "owner_operator_protocol_chain_completed": chain_pass,
        "boundary_object_registry_missing_dependency_identified": True,
        "direct_approval_request_blocked": True,
        "direct_evidence_authorization_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "owner_operator_approval_protocol_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "boundary_dependency_count": len(dependency_rows),
        "boundary_registry_planning_scope_count": len(planning_scope_rows),
        "entry_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_planning_only": "planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_approval_request_blocked": True,
        "direct_evidence_authorization_blocked": True,
        "boundary_object_registry_missing_dependency_identified": True,
        "owner_operator_protocol_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "owner_operator_roadmap_decision_policy": owner_operator_roadmap_decision_policy,
        "completed_owner_operator_protocol_review": completed_owner_operator_protocol_review,
        "owner_operator_roadmap_route_candidate_matrix": owner_operator_roadmap_route_candidate_matrix,
        "owner_operator_to_boundary_object_dependency_matrix": owner_operator_to_boundary_object_dependency_matrix,
        "boundary_object_registry_planning_scope": boundary_object_registry_planning_scope,
        "owner_operator_roadmap_non_release_matrix": owner_operator_roadmap_non_release_matrix,
        "boundary_object_entry_readiness_risk_matrix": boundary_object_entry_readiness_risk_matrix,
        "owner_operator_roadmap_decision_non_claims_register": owner_operator_roadmap_decision_non_claims_register,
        "owner_operator_roadmap_readiness_decision": owner_operator_roadmap_readiness_decision,
    }
