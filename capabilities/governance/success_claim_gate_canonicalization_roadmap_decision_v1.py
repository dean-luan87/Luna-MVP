# -*- coding: utf-8 -*-
"""Success Claim Gate Canonicalization Roadmap Decision v1.

Roadmap decision only: select Route A — Evidence Chain Governance Planning.
Does not generate success claim gate, evidence, or release execution permissions.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001"
DECISION_SCOPE = "success_claim_gate_canonicalization_roadmap_decision_only"
SOURCE_CHAIN = "success_claim_gate_canonicalization_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "SUCCESS_CLAIM_GATE_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"

SELECTED_ROUTE = "Route A — Evidence Chain Governance Planning"
NEXT_PHASE = "Phase-Evidence-Chain-Governance-Planning-v1-001"
FINAL_DECISION = (
    "SUCCESS_CLAIM_GATE_CANONICALIZATION_ROADMAP_DECISION_READY_FOR_EVIDENCE_CHAIN_GOVERNANCE_PLANNING"
)

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "success_claim_gate_post_dryrun_review_policy_v1.json",
    "success_claim_dryrun_completeness_review_v1.json",
    "success_claim_gate_non_generation_review_v1.json",
    "success_claim_allowance_block_review_v1.json",
    "success_claim_evidence_boundary_review_v1.json",
    "success_claim_authorization_dependency_review_v1.json",
    "success_claim_forbidden_interpretation_review_v1.json",
    "success_claim_verifier_non_modification_review_v1.json",
    "success_claim_non_claims_non_write_review_v1.json",
    "success_claim_cross_artifact_consistency_review_v1.json",
    "success_claim_gate_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    (
        "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001",
        "success_claim_gate_canonicalization_planning_v1_smoke_v0",
    ),
    (
        "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001",
        "success_claim_gate_canonicalization_dryrun_v1_smoke_v0",
    ),
    (
        "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001",
        "success_claim_gate_canonicalization_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Evidence Chain Governance Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "evidence_chain_governance_planning",
        "target_scope": "evidence candidate / runtime / audit / success evidence / source chain lifecycle",
        "entry_reason": "success claim gate chain complete; evidence lifecycle not unified; gate generation would be empty without evidence chain",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "evidence chain planning allowed only; not evidence generation / registry / canonicalization",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ evidence generated",
            "≠ evidence chain canonicalized",
            "≠ evidence can support success claim alone",
        ],
    },
    {
        "route_id": "B",
        "route_name": "Owner/Operator Approval Protocol Planning",
        "priority": "P0 / P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_operator_approval_protocol_planning",
        "target_scope": "owner approval / operator acknowledgement / execution window",
        "entry_reason": "success claim requires authorization chain; deferred until evidence chain planned",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["evidence chain not planned"],
        "permission_impact": "deferred; not approval granted",
        "next_phase_candidate": "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "non_claims": ["deferred ≠ owner/operator approval granted"],
    },
    {
        "route_id": "C",
        "route_name": "Boundary Object Registry Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registry_planning",
        "target_scope": "protected / HR / DnAE / eval_out / verdict table registry",
        "entry_reason": "real file operations require boundary registry; deferred after evidence chain",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["evidence chain not planned"],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Boundary-Object-Registry-Planning-v1-001",
        "non_claims": ["deferred ≠ boundary registry generated"],
    },
    {
        "route_id": "D",
        "route_name": "Success Claim Gate Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "success_claim_gate_generation_planning",
        "target_scope": "success claim gate formal generation",
        "entry_reason": "evidence chain not closed; owner/operator and boundary object incomplete",
        "required_dependencies": [SELECTED_ROUTE, "Owner/Operator Approval Protocol Planning"],
        "missing_preconditions": [
            "evidence chain not planned",
            "evidence registry not generated",
            "authorization chain not active",
        ],
        "permission_impact": "deferred; not gate generation allowed",
        "next_phase_candidate": "Phase-Success-Claim-Gate-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ success claim gate generated"],
    },
    {
        "route_id": "E",
        "route_name": "Permission Semantics Canonicalization Execution Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "permission_semantics_canonicalization_execution_planning",
        "target_scope": "permission semantics canonicalization execution",
        "entry_reason": "evidence chain and success claim gate dependencies incomplete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["evidence chain not planned"],
        "permission_impact": "deferred; not permission semantics execution",
        "next_phase_candidate": "Phase-Permission-Semantics-Canonicalization-Execution-Planning-v1-001",
        "non_claims": ["deferred ≠ permission semantics canonicalization execution"],
    },
    {
        "route_id": "F",
        "route_name": "Terminology Canonical Table Generation Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "terminology_canonical_table_generation_planning",
        "target_scope": "formal terminology canonical table generation",
        "entry_reason": "terminology planning/dry-run/post-review complete; formal generation deferred",
        "required_dependencies": [],
        "missing_preconditions": ["evidence chain P0 first"],
        "permission_impact": "deferred; not formal table generation",
        "next_phase_candidate": "Phase-Terminology-Canonical-Table-Generation-Planning-v1-001",
        "non_claims": ["deferred ≠ terminology_canonical_table_v1.json generated"],
    },
    {
        "route_id": "G",
        "route_name": "Real Rehearsal Authorization Chain Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "real_rehearsal_authorization_chain_planning",
        "target_scope": "rollback rehearsal authorization chain",
        "entry_reason": "evidence / authorization / gate dependencies not complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["evidence chain not planned", "success claim gate not generated"],
        "permission_impact": "deferred; not real rehearsal execution",
        "next_phase_candidate": "Phase-Real-Rehearsal-Authorization-Chain-Planning-v1-001",
        "non_claims": ["deferred ≠ real rehearsal execution allowed"],
    },
    {
        "route_id": "H",
        "route_name": "Direct Success Claim Gate Execution / Success Claim Allowance",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_success_claim_gate_execution",
        "target_scope": "success claim gate execution / success claim allowance",
        "entry_reason": "no real evidence chain / runtime evidence / success evidence / authorization / post-execution review",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "evidence chain not planned",
            "runtime evidence not available",
            "success evidence not generated",
            "authorization chain not active",
            "real execution not observed",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Success-Claim-Gate-Execution-v1-001",
        "non_claims": ["blocked ≠ success claim allowed", "≠ gate execution allowed"],
    },
]

EVIDENCE_CHAIN_DEPENDENCIES: Tuple[Tuple[str, str], ...] = (
    ("D01", "evidence candidate lifecycle"),
    ("D02", "runtime evidence lifecycle"),
    ("D03", "audit evidence lifecycle"),
    ("D04", "success evidence lifecycle"),
    ("D05", "source chain lifecycle"),
    ("D06", "evidence source quality"),
    ("D07", "evidence acceptance policy"),
    ("D08", "evidence usage scope"),
    ("D09", "verifier_report boundary"),
    ("D10", "summary boundary"),
    ("D11", "post-review report boundary"),
    ("D12", "boundary matrix boundary"),
)

EVIDENCE_CHAIN_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("evidence candidate lifecycle", "define candidate tier before acceptance"),
    ("runtime evidence lifecycle", "runtime-captured artifacts require real execution + source chain"),
    ("audit evidence lifecycle", "audit pass ≠ success claim"),
    ("success evidence lifecycle", "gated bundle only after runtime + authorization + post-review"),
    ("source chain lifecycle", "provenance required; source chain alone cannot imply success claim"),
    ("evidence source quality", "quality gates before acceptance"),
    ("evidence acceptance policy", "candidate → accepted evidence rules"),
    ("evidence usage scope", "per-phase usage boundaries"),
    ("evidence upgrade path", "upgrade via gate when prerequisites met"),
    ("verifier_report boundary", "verifier report ≠ runtime evidence; cannot support success claim alone"),
    ("summary boundary", "summary ≠ success evidence"),
    ("post-review report boundary", "review pass ≠ success claim allowed"),
    ("boundary matrix boundary", "boundary_ok alone insufficient"),
    ("evidence-to-success-claim eligibility", "eligibility matrix tying evidence types to success claim"),
)

ENTRY_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "evidence chain not planned", "high", "Route A selected ≠ evidence generated"),
    ("R02", "evidence registry not generated", "high", "planning ≠ evidence_registry_generated_now"),
    ("R03", "evidence candidate not accepted", "high", "candidate evidence cannot support success claim"),
    ("R04", "runtime evidence not generated", "high", "runtime_evidence_generated_now=false"),
    ("R05", "success evidence not generated", "high", "success_evidence_generated_now=false"),
    ("R06", "source chain not sufficient alone", "high", "source chain component ≠ success claim allowed"),
    ("R07", "verifier_report cannot support success claim", "high", "verifier_report.can_support_success_claim=false"),
    ("R08", "summary cannot support success claim", "high", "summary.can_support_success_claim=false"),
    ("R09", "boundary matrix cannot support success claim alone", "medium", "boundary_ok ≠ success claim"),
    ("R10", "authorization chain not active", "high", "authorization_granted_now=false"),
    ("R11", "real execution not observed", "high", "execution_committed=false"),
    ("R12", "post-execution review not available", "high", "post-review ≠ success claim"),
    ("R13", "owner/operator approval not active", "high", "owner approval not granted"),
    ("R14", "real rehearsal not available", "high", "real_rehearsal_execution_allowed=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "success claim gate generation",
    "success claim gate enforcement",
    "success claim allowance",
    "success evidence generation",
    "runtime evidence generation",
    "evidence chain canonicalization",
    "evidence registry generation",
    "verifier modification",
    "phase template modification",
    "automation implementation",
    "documentation auto-sync",
    "debt fix execution",
    "owner/operator approval",
    "execution window opening",
    "real rollback rehearsal execution",
    "real migration execution",
    "batch arming",
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean success claim gate is generated.",
    "Roadmap Decision GO does not mean success claim is allowed.",
    "Route A selected does not mean evidence is generated.",
    "Route A selected does not mean evidence chain is canonicalized.",
    "Route A selected does not mean evidence can support success claim.",
    "Route D deferred means success claim gate generation remains unavailable.",
    "Route H blocked means direct success claim gate execution and allowance remain forbidden.",
    "Roadmap Decision GO does not mean verifier or phase template has been modified.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "success_claim_gate_generated_now": False,
        "success_claim_gate_enforced_now": False,
        "success_claim_allowed": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "success_claim_canonicalization_executed_now": False,
        "terminology_canonicalization_executed_now": False,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
        "registry_written_now": False,
        "permission_semantics_canonicalization_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "debt_fix_executed_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
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
        root / "success_claim_gate_post_dryrun_review_readiness_decision_v1.json"
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
                gate_generation_observed=sm.get("success_claim_gate_generated_now") is True,
                success_claim_allowance_observed=sm.get("success_claim_allowed") is True,
                success_evidence_generation_observed=sm.get("success_evidence_generated_now") is True,
                runtime_evidence_generation_observed=sm.get("runtime_evidence_generated_now") is True,
                verifier_modification_observed=sm.get("verifier_modified_now") is True,
                phase_template_modification_observed=sm.get("phase_template_modified_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_evidence_chain_dependency_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for dep_id, dep_name in EVIDENCE_CHAIN_DEPENDENCIES:
        rows.append(
            _decision_row(
                dependency_id=dep_id,
                dependency_name=dep_name,
                required_for_success_claim_gate_generation=True,
                required_for_success_claim_allowance=True,
                current_status="not_planned",
                missing_preconditions=["evidence chain governance planning not completed"],
                blocks_gate_generation=True,
                blocks_success_claim_allowance=True,
                recommended_next_action="enter Evidence Chain Governance Planning",
                source_chain_alone_insufficient=dep_name == "source chain lifecycle",
            )
        )
    return rows


def _build_evidence_chain_planning_scope() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for planning_topic, why_required in EVIDENCE_CHAIN_PLANNING_TOPICS:
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                why_required=why_required,
                required_outputs=[
                    f"evidence_chain_{planning_topic.replace(' ', '_')}_plan_v1.json",
                ],
                required_for_success_claim_gate_generation=True,
                required_for_real_rehearsal_chain=True,
                required_for_migration_chain=True,
                required_verifier_usage=[f"verify_evidence_chain_{planning_topic.replace(' ', '_')}"],
                required_non_claims=[f"planning GO does not imply {planning_topic} satisfied"],
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
                blocks_generation=True,
                blocks_execution=True,
                blocks_success_claim_allowance=True,
                required_non_claim=non_claim,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _evidence_boundary_ok(artifacts: Dict[str, Any]) -> Tuple[bool, List[str]]:
    boundary = artifacts.get("success_claim_evidence_boundary_review_v1.json") or {}
    by_type = {r.get("artifact_or_evidence_type"): r for r in (boundary.get("rows") or [])}
    issues: List[str] = []
    for atype in ("verifier report", "summary", "candidate evidence"):
        if by_type.get(atype, {}).get("can_support_success_claim") is not False:
            issues.append(f"{atype} can_support_success_claim must be false")
    sc = by_type.get("source chain", {})
    if sc.get("can_support_success_claim") is not True:
        issues.append("source chain must be evidence chain component (can_support true at planning tier)")
    if sc.get("boundary_release_detected") is True:
        issues.append("source chain boundary_release_detected must be false")
    return len(issues) == 0, issues


def run_success_claim_gate_canonicalization_roadmap_decision_v1(
    *,
    success_claim_gate_canonicalization_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(success_claim_gate_canonicalization_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_success_claim_gate_canonicalization_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_success_claim_gate_canonicalization_roadmap_decision")
    if up_summary.get("success_claim_gate_generated_now") is not False:
        blockers.append("upstream success_claim_gate_generated_now is not false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("upstream success_claim_allowed is not false")
    if up_summary.get("success_evidence_generated_now") is not False:
        blockers.append("upstream success_evidence_generated_now is not false")
    if up_summary.get("runtime_evidence_generated_now") is not False:
        blockers.append("upstream runtime_evidence_generated_now is not false")
    for flag in (
        "ready_for_success_claim_gate_generation",
        "ready_for_success_claim_gate_execution",
        "ready_for_success_claim_allowance",
        "ready_for_success_evidence_generation",
        "ready_for_runtime_evidence_generation",
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

    boundary_ok_upstream, boundary_issues = _evidence_boundary_ok(up_art)
    if not boundary_ok_upstream:
        blockers.extend(boundary_issues)

    auth = up_art.get("success_claim_authorization_dependency_review_v1.json") or {}
    if any(r.get("satisfied_now") is True for r in (auth.get("rows") or [])):
        blockers.append("authorization dependencies must all be unsatisfied")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_evidence_chain_dependency_matrix()
    planning_scope_rows = _build_evidence_chain_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_entry_risk_matrix()

    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_d = next(r for r in route_rows if r.get("route_id") == "D")
    route_h = next(r for r in route_rows if r.get("route_id") == "H")

    route_ok = (
        route_a.get("selected_now") is True
        and route_a.get("allowed_now") is True
        and "planning" in str(route_a.get("permission_impact", "")).lower()
        and "not evidence generation" in str(route_a.get("permission_impact", "")).lower()
        and route_d.get("deferred") is True
        and route_d.get("allowed_now") is False
        and route_h.get("blocked_now") is True
        and route_h.get("allowed_now") is False
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    no_gate_route_allowed = all(
        not (r.get("route_type") == "success_claim_gate_generation_planning" and r.get("allowed_now") is True)
        for r in route_rows
    )
    if not no_gate_route_allowed:
        blockers.append("success claim gate generation must not be allowed_now")

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

    success_claim_gate_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_success_claim_gate_canonicalization_roadmap_decision_observed=up_readiness.get(
            "ready_for_success_claim_gate_canonicalization_roadmap_decision"
        )
        is True,
    )

    completed_success_claim_gate_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    success_claim_gate_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    success_claim_to_evidence_chain_dependency_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "evidence_chain_missing_dependency_identified": True,
        **_decision_meta(),
    }
    evidence_chain_governance_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    success_claim_gate_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    success_claim_gate_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    evidence_chain_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    success_claim_gate_roadmap_readiness_decision = {
        "ready_for_evidence_chain_governance_planning": boundary_ok,
        "ready_for_evidence_generation": False,
        "ready_for_evidence_registry_generation": False,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_gate_execution": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_success_claim_enforcement": False,
        "ready_for_success_evidence_generation": False,
        "ready_for_runtime_evidence_generation": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": SELECTED_ROUTE,
        "success_claim_gate_chain_completed": chain_pass,
        "evidence_chain_missing_dependency_identified": True,
        "direct_success_claim_execution_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "success_claim_gate_canonicalization_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "evidence_chain_dependency_count": len(dependency_rows),
        "evidence_chain_planning_scope_count": len(planning_scope_rows),
        "entry_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_a_selected_now": route_a.get("selected_now") is True,
        "route_a_planning_only": "planning" in str(route_a.get("permission_impact", "")).lower(),
        "route_d_deferred": route_d.get("deferred") is True,
        "route_h_blocked_now": route_h.get("blocked_now") is True,
        "direct_success_claim_execution_blocked": True,
        "evidence_chain_missing_dependency_identified": True,
        "success_claim_gate_chain_completed": chain_pass,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "success_claim_gate_canonicalization_post_dryrun_review",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_decision_meta(),
            }
        ],
        "row_count": 1,
        **_decision_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "selected_route": SELECTED_ROUTE,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "reason": "Route A selected; evidence chain planning only; gate generation and success claim blocked",
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "success_claim_gate_roadmap_decision_policy": success_claim_gate_roadmap_decision_policy,
        "completed_success_claim_gate_chain_review": completed_success_claim_gate_chain_review,
        "success_claim_gate_roadmap_route_candidate_matrix": success_claim_gate_roadmap_route_candidate_matrix,
        "success_claim_to_evidence_chain_dependency_matrix": success_claim_to_evidence_chain_dependency_matrix,
        "evidence_chain_governance_planning_scope": evidence_chain_governance_planning_scope,
        "success_claim_gate_roadmap_non_release_matrix": success_claim_gate_roadmap_non_release_matrix,
        "evidence_chain_entry_readiness_risk_matrix": evidence_chain_entry_readiness_risk_matrix,
        "success_claim_gate_roadmap_decision_non_claims_register": success_claim_gate_roadmap_decision_non_claims_register,
        "success_claim_gate_roadmap_readiness_decision": success_claim_gate_roadmap_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
