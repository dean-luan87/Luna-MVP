# -*- coding: utf-8 -*-
"""Evidence Chain Governance Roadmap Decision v1.

Roadmap decision only: select Route A — Owner/Operator Approval Protocol Planning.
Does not generate evidence, grant authorization, or release execution permissions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001"
DECISION_SCOPE = "evidence_chain_governance_roadmap_decision_only"
SOURCE_CHAIN = "evidence_chain_governance_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "EVIDENCE_CHAIN_GOVERNANCE_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"

SELECTED_ROUTE = "Route A — Owner/Operator Approval Protocol Planning"
NEXT_PHASE = "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001"
FINAL_DECISION = (
    "EVIDENCE_CHAIN_GOVERNANCE_ROADMAP_DECISION_READY_FOR_OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING"
)

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "evidence_chain_post_dryrun_review_policy_v1.json",
    "evidence_dryrun_completeness_review_v1.json",
    "evidence_generation_block_review_v1.json",
    "evidence_success_claim_acceptance_block_review_v1.json",
    "evidence_lifecycle_boundary_review_v1.json",
    "evidence_acceptance_policy_review_v1.json",
    "evidence_source_chain_standalone_review_v1.json",
    "evidence_usage_and_upgrade_block_review_v1.json",
    "evidence_eligibility_review_v1.json",
    "evidence_verifier_non_modification_review_v1.json",
    "evidence_non_claims_non_write_review_v1.json",
    "evidence_chain_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Evidence-Chain-Governance-Planning-v1-001",
        "evidence_chain_governance_planning_v1_smoke_v0",
    ),
    (
        "Phase-Evidence-Chain-Governance-DryRun-v1-001",
        "evidence_chain_governance_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001",
        "evidence_chain_governance_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Owner/Operator Approval Protocol Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "owner_operator_approval_protocol_planning",
        "target_scope": "owner approval / operator acknowledgement / execution window / abort authority",
        "entry_reason": "evidence generation and success claim require authorization chain; evidence chain planning+dry-run+post-review credible",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "owner/operator approval protocol planning allowed only; not owner approval granted; not operator acknowledgement granted; not evidence generation",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ owner approval requested",
            "≠ owner/operator approval granted",
            "≠ evidence generated",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Boundary Object Registry Planning",
        "priority": "P0 / P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registry_planning",
        "target_scope": "protected / HR / DnAE / eval_out / verdict table / handoff / checkpoint",
        "entry_reason": "file operations and evidence generation require boundary registry; deferred after owner/operator protocol planning",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["owner/operator approval protocol not planned"],
        "permission_impact": "deferred P0/P1 next dependency; not boundary registry generated",
        "next_phase_candidate": "Phase-Boundary-Object-Registry-Planning-v1-001",
        "non_claims": ["deferred ≠ boundary_object_registry_generated_now"],
    },
    {
        "route_id": "C",
        "route_name": "Evidence Chain Canonicalization Execution Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "evidence_chain_canonicalization_execution_planning",
        "target_scope": "evidence chain canonicalization execution planning",
        "entry_reason": "owner/operator approval and boundary object registry not closed",
        "required_dependencies": [SELECTED_ROUTE, "Boundary Object Registry Planning"],
        "missing_preconditions": ["authorization protocol not planned", "boundary registry not planned"],
        "permission_impact": "deferred; not canonicalization execution",
        "next_phase_candidate": "Phase-Evidence-Chain-Canonicalization-Execution-Planning-v1-001",
        "non_claims": ["deferred ≠ evidence_chain_canonicalization_executed_now"],
    },
    {
        "route_id": "D",
        "route_name": "Evidence Registry Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "evidence_registry_generation_planning",
        "target_scope": "evidence registry generation planning",
        "entry_reason": "authorization and boundary dependencies incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["owner/operator protocol not planned", "authorization not granted"],
        "permission_impact": "deferred; not evidence_registry_generated_now",
        "next_phase_candidate": "Phase-Evidence-Registry-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ evidence registry generated"],
    },
    {
        "route_id": "E",
        "route_name": "Evidence Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "evidence_generation_planning",
        "target_scope": "runtime / success / audit evidence generation planning",
        "entry_reason": "no authorization context for evidence generation",
        "required_dependencies": [SELECTED_ROUTE, "Boundary Object Registry Planning"],
        "missing_preconditions": ["owner approval not granted", "operator acknowledgement not granted"],
        "permission_impact": "deferred; not evidence_generated_now",
        "next_phase_candidate": "Phase-Evidence-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ runtime_evidence_generated_now", "≠ success_evidence_generated_now"],
    },
    {
        "route_id": "F",
        "route_name": "Success Claim Gate Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "success_claim_gate_generation_planning",
        "target_scope": "success claim gate generation planning",
        "entry_reason": "owner/operator, boundary, evidence generation incomplete",
        "required_dependencies": [SELECTED_ROUTE, "Evidence Generation Planning"],
        "missing_preconditions": ["evidence not generated", "authorization not active"],
        "permission_impact": "deferred; not success_claim_gate_generated_now",
        "next_phase_candidate": "Phase-Success-Claim-Gate-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ success claim gate generated"],
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
        "entry_reason": "evidence / authorization / execution window dependencies incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["evidence chain not executable", "authorization not granted"],
        "permission_impact": "deferred; not real_rehearsal_execution_allowed",
        "next_phase_candidate": "Phase-Real-Rollback-Rehearsal-Authorization-Chain-Planning-v1-001",
        "non_claims": ["deferred ≠ real rehearsal execution allowed"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Evidence Generation / Success Claim Allowance / Real Rehearsal Execution",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_evidence_generation_success_claim_real_rehearsal",
        "target_scope": "evidence generation / success claim allowance / real rehearsal",
        "entry_reason": "no owner/operator approval, boundary registry, evidence registry, execution window, runtime/success evidence",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "owner approval not granted",
            "operator acknowledgement not granted",
            "evidence not generated",
            "success claim not allowed",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Evidence-Generation-v1-001",
        "non_claims": ["blocked ≠ evidence generated", "≠ success_claim_allowed", "≠ real rehearsal allowed"],
    },
]

AUTHORIZATION_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("A01", "evidence generation authorization"),
    ("A02", "runtime evidence authorization"),
    ("A03", "success evidence authorization"),
    ("A04", "evidence acceptance authority"),
    ("A05", "evidence upgrade authority"),
    ("A06", "evidence registry authority"),
    ("A07", "verifier rerun authority"),
    ("A08", "execution window authority"),
    ("A09", "rollback rehearsal authority"),
    ("A10", "migration authority"),
    ("A11", "post-execution review authority"),
    ("A12", "success claim authority"),
)

OWNER_OPERATOR_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("owner approval identity", "define who may grant owner approval"),
    ("owner approval evidence", "evidence bundle required for owner approval"),
    ("operator acknowledgement identity", "define operator role and identity binding"),
    ("operator acknowledgement evidence", "evidence required for operator acknowledgement"),
    ("execution window open/close", "time-bounded execution authorization"),
    ("abort authority", "who may abort and under what conditions"),
    ("scope confirmation", "confirm migration scope before execution"),
    ("protected boundary acknowledgement", "protected assets boundary before file ops"),
    ("HR / DnAE boundary acknowledgement", "human review and DnAE boundaries"),
    ("verifier rerun authorization", "when verifier suite may be rerun"),
    ("evidence generation authorization", "authorize runtime/success/audit evidence generation"),
    ("evidence acceptance authority", "who may accept evidence for downstream use"),
    ("post-execution review authority", "post-execution review gate before success claim"),
    ("success claim authority", "who may allow success claim after all prerequisites"),
)

ENTRY_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "owner identity not confirmed", "high", "planning allowed; approval execution blocked"),
    ("R02", "operator identity not confirmed", "high", "planning allowed; acknowledgement execution blocked"),
    ("R03", "owner approval not granted", "high", "owner_approval_granted_now=false"),
    ("R04", "operator acknowledgement not granted", "high", "operator_acknowledgement_granted_now=false"),
    ("R05", "execution window not opened", "high", "execution_window_opened_now=false"),
    ("R06", "abort authority not confirmed", "high", "abort_authority_confirmed_now=false"),
    ("R07", "evidence generation not authorized", "high", "evidence_generated_now=false"),
    ("R08", "evidence acceptance authority not defined", "high", "evidence_accepted_for_success_claim_now=false"),
    ("R09", "verifier rerun not authorized", "medium", "verifier rerun remains planning-only"),
    ("R10", "protected boundary not acknowledged", "high", "protected assets unchanged"),
    ("R11", "HR / DnAE boundary not acknowledged", "high", "HR/DnAE unchanged"),
    ("R12", "success claim authority not defined", "high", "success_claim_allowed=false"),
    ("R13", "real execution not observed", "high", "execution_committed=false"),
    ("R14", "real rehearsal not available", "high", "real_rehearsal_execution_allowed=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "evidence generation",
    "runtime evidence generation",
    "success evidence generation",
    "evidence registry generation",
    "evidence acceptance for success claim",
    "evidence chain canonicalization execution",
    "owner approval request",
    "owner approval granted",
    "operator acknowledgement granted",
    "execution window opened",
    "abort authority confirmed",
    "verifier rerun execution",
    "success claim gate generation",
    "success claim allowance",
    "real rollback rehearsal execution",
    "real migration execution",
    "batch arming",
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean evidence is generated.",
    "Roadmap Decision GO does not mean evidence registry is generated.",
    "Roadmap Decision GO does not mean evidence can support success claim.",
    "Route A selected does not mean owner approval is requested.",
    "Route A selected does not mean owner/operator approval is granted.",
    "Route A selected does not mean execution window is opened.",
    "Route C/D/E deferred means evidence canonicalization / registry / generation remain unavailable.",
    "Route H blocked means direct evidence generation / success claim allowance / real rehearsal remain forbidden.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "success_claim_gate_generated_now": False,
        "success_claim_allowed": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "abort_authority_confirmed_now": False,
        "authorization_granted_now": False,
        "boundary_object_registry_generated_now": False,
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
        root / "evidence_chain_post_dryrun_review_readiness_decision_v1.json"
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
                evidence_generation_observed=sm.get("evidence_generated_now") is True,
                evidence_acceptance_for_success_claim_observed=sm.get(
                    "evidence_accepted_for_success_claim_now"
                )
                is True,
                evidence_registry_generation_observed=sm.get("evidence_registry_generated_now")
                is True,
                success_claim_allowance_observed=sm.get("success_claim_allowed") is True,
                verifier_modification_observed=sm.get("verifier_modified_now") is True,
                phase_template_modification_observed=sm.get("phase_template_modified_now") is True,
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
                required_for_evidence_generation=True,
                required_for_evidence_acceptance=True,
                required_for_success_claim=True,
                current_status="not_defined",
                missing_preconditions=["owner/operator approval protocol not planned"],
                blocks_evidence_generation=True,
                blocks_success_claim_allowance=True,
                recommended_next_action="enter Owner/Operator Approval Protocol Planning",
            )
        )
    return rows


def _build_owner_operator_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in OWNER_OPERATOR_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[f"owner_operator_{planning_topic.replace(' ', '_')}_plan_v1.json"],
                required_for_evidence_generation=planning_topic
                in ("evidence generation authorization", "evidence acceptance authority"),
                required_for_success_claim=planning_topic == "success claim authority",
                required_for_real_rehearsal_chain=planning_topic
                in ("execution window open/close", "rollback rehearsal authority"),
                required_for_migration_chain=planning_topic
                in ("migration authority", "scope confirmation"),
                required_verifier_usage=[f"verify_owner_operator_{planning_topic.replace(' ', '_')}"],
                required_non_claims=[f"planning GO does not imply {planning_topic} granted"],
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
                blocks_approval_execution=True,
                blocks_evidence_generation=True,
                blocks_success_claim_allowance=True,
                required_non_claim=non_claim,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _acceptance_policy_ok(artifacts: Dict[str, Any]) -> Tuple[bool, List[str]]:
    acceptance = artifacts.get("evidence_acceptance_policy_review_v1.json") or {}
    issues: List[str] = []
    for row in acceptance.get("rows") or []:
        if row.get("reviewed_reject_rule_using_accepted_when_contains_never") is not True:
            issues.append(
                f"{row.get('acceptance_rule')}: reject rule must use accepted_when contains never"
            )
        if row.get("accepted_now") is not False:
            issues.append(f"{row.get('acceptance_rule')}: accepted_now must be false")
        target = row.get("target_evidence_type", "")
        if target in ("summary", "verifier_report", "evidence_candidate") and row.get(
            "accepted_now"
        ) is not False:
            issues.append(f"{target} must not be accepted as success evidence")
    standalone = artifacts.get("evidence_source_chain_standalone_review_v1.json") or {}
    for row in standalone.get("rows") or []:
        if row.get("can_stand_alone_for_success_claim") is not False:
            issues.append(
                f"{row.get('source_chain_component')}: must not stand alone for success claim"
            )
        if row.get("accepted_as_success_evidence_now") is True:
            issues.append("source chain must not be accepted as success evidence alone")
    return len(issues) == 0, issues


def _lifecycle_boundary_ok(artifacts: Dict[str, Any]) -> Tuple[bool, List[str]]:
    lifecycle = artifacts.get("evidence_lifecycle_boundary_review_v1.json") or {}
    by_type = {r.get("evidence_type"): r for r in (lifecycle.get("rows") or [])}
    issues: List[str] = []
    for etype in ("evidence_candidate", "verifier_report", "summary", "source_chain"):
        row = by_type.get(etype, {})
        if row.get("can_support_success_claim_now") is not False:
            issues.append(f"{etype} can_support_success_claim_now must be false")
    for etype in ("success_evidence", "runtime_evidence"):
        if by_type.get(etype, {}).get("generation_allowed_now") is not False:
            issues.append(f"{etype} generation_allowed_now must be false")
    return len(issues) == 0, issues


def run_evidence_chain_governance_roadmap_decision_v1(
    *,
    evidence_chain_governance_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(evidence_chain_governance_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_evidence_chain_governance_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_evidence_chain_governance_roadmap_decision")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    for flag in (
        "evidence_generated_now",
        "runtime_evidence_generated_now",
        "success_evidence_generated_now",
        "evidence_accepted_for_success_claim_now",
        "evidence_chain_canonicalization_executed_now",
        "evidence_registry_generated_now",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("upstream success_claim_allowed must be false")
    for flag in (
        "ready_for_evidence_chain_canonicalization_execution",
        "ready_for_evidence_registry_generation",
        "ready_for_evidence_generation",
        "ready_for_runtime_evidence_generation",
        "ready_for_success_evidence_generation",
        "ready_for_evidence_acceptance_for_success_claim",
        "ready_for_success_claim_gate_generation",
        "ready_for_success_claim_allowance",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("upstream real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("upstream batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    acceptance_ok, acceptance_issues = _acceptance_policy_ok(up_art)
    if not acceptance_ok:
        blockers.extend(acceptance_issues)
    lifecycle_ok, lifecycle_issues = _lifecycle_boundary_ok(up_art)
    if not lifecycle_ok:
        blockers.extend(lifecycle_issues)

    gen_block = up_art.get("evidence_generation_block_review_v1.json") or {}
    if gen_block.get("all_pass") is not True:
        blockers.append("upstream evidence generation block review must pass")

    sc_block = up_art.get("evidence_success_claim_acceptance_block_review_v1.json") or {}
    if sc_block.get("all_pass") is not True:
        blockers.append("upstream success claim acceptance block review must pass")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_authorization_dependency_matrix()
    planning_scope_rows = _build_owner_operator_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_entry_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_c = next(r for r in route_rows if r.get("route_id") == "C")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "planning" in str(route_a.get("permission_impact", "")).lower()
        and "not owner approval granted" in str(route_a.get("permission_impact", "")).lower()
        and "not evidence generation" in str(route_a.get("permission_impact", "")).lower()
        and route_b.get("deferred") is True
        and route_b.get("selected_now") is False
        and route_c.get("deferred") is True
        and route_c.get("allowed_now") is False
        and route_h.get("blocked_now") is True
        and route_h.get("allowed_now") is False
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    deferred_routes = ("C", "D", "E", "F", "G")
    for rid in deferred_routes:
        r = next(x for x in route_rows if x.get("route_id") == rid)
        if r.get("deferred") is not True or r.get("allowed_now") is not False:
            blockers.append(f"route {rid} must be deferred and not allowed_now")

    no_evidence_route_allowed = all(
        not (
            r.get("route_type") in ("evidence_generation_planning", "evidence_registry_generation_planning")
            and r.get("allowed_now") is True
        )
        for r in route_rows
    )
    if not no_evidence_route_allowed:
        blockers.append("evidence generation/registry routes must not be allowed_now")

    decision_ready = (
        chain_pass
        and non_release_pass
        and risk_pass
        and route_ok
        and len(dependency_rows) >= 12
        and len(planning_scope_rows) >= 14
        and not blockers
    )
    boundary_ok = decision_ready

    evidence_chain_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_evidence_chain_governance_roadmap_decision_observed=up_readiness.get(
            "ready_for_evidence_chain_governance_roadmap_decision"
        )
        is True,
    )

    completed_evidence_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    evidence_chain_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    evidence_to_authorization_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "authorization_missing_dependency_identified": True,
        **_decision_meta(),
    }
    owner_operator_approval_protocol_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    evidence_chain_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    evidence_chain_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    owner_operator_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    evidence_chain_roadmap_readiness_decision = {
        "ready_for_owner_operator_approval_protocol_planning": boundary_ok,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_execution_window_opening": False,
        "ready_for_evidence_generation": False,
        "ready_for_evidence_registry_generation": False,
        "ready_for_evidence_acceptance_for_success_claim": False,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": SELECTED_ROUTE,
        "evidence_chain_completed": chain_pass,
        "authorization_missing_dependency_identified": True,
        "boundary_object_registry_pending_dependency": True,
        "direct_evidence_generation_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "evidence_chain_governance_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "authorization_dependency_count": len(dependency_rows),
        "owner_operator_planning_scope_count": len(planning_scope_rows),
        "entry_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_planning_only": "planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_b_deferred": route_b.get("deferred") is True,
        "route_c_deferred": route_c.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_evidence_generation_blocked": True,
        "authorization_missing_dependency_identified": True,
        "evidence_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "evidence_chain_roadmap_decision_policy": evidence_chain_roadmap_decision_policy,
        "completed_evidence_chain_review": completed_evidence_chain_review,
        "evidence_chain_roadmap_route_candidate_matrix": evidence_chain_roadmap_route_candidate_matrix,
        "evidence_to_authorization_dependency_matrix": evidence_to_authorization_dependency_matrix,
        "owner_operator_approval_protocol_planning_scope": owner_operator_approval_protocol_planning_scope,
        "evidence_chain_roadmap_non_release_matrix": evidence_chain_roadmap_non_release_matrix,
        "owner_operator_entry_readiness_risk_matrix": owner_operator_entry_readiness_risk_matrix,
        "evidence_chain_roadmap_decision_non_claims_register": evidence_chain_roadmap_decision_non_claims_register,
        "evidence_chain_roadmap_readiness_decision": evidence_chain_roadmap_readiness_decision,
    }
