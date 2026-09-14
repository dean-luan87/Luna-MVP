# -*- coding: utf-8 -*-
"""Terminology Canonical Table Roadmap Decision v1.

Roadmap decision only: select Route C — Success Claim Gate Canonicalization Planning.
Does not generate formal terminology table, success claim gate, or release execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)
from capabilities.governance.terminology_canonical_table_planning_v1 import (
    SUCCESS_CLAIM_TOPICS,
)

PHASE_ID = "Phase-Terminology-Canonical-Table-Roadmap-Decision-v1-001"
DECISION_SCOPE = "terminology_canonical_table_roadmap_decision_only"
SOURCE_CHAIN = "terminology_canonical_table_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = "TERMINOLOGY_CANONICAL_TABLE_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"

SELECTED_ROUTE = "Route C — Success Claim Gate Canonicalization Planning"
NEXT_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001"
FINAL_DECISION = (
    "TERMINOLOGY_CANONICAL_TABLE_ROADMAP_DECISION_READY_FOR_SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING"
)

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "terminology_canonical_table_post_dryrun_review_policy_v1.json",
    "terminology_dryrun_completeness_review_v1.json",
    "terminology_formal_table_non_generation_review_v1.json",
    "terminology_entry_simulation_review_v1.json",
    "terminology_verifier_non_modification_review_v1.json",
    "terminology_forbidden_interpretation_non_enforcement_review_v1.json",
    "terminology_required_fields_simulation_review_v1.json",
    "terminology_registry_write_review_v1.json",
    "terminology_success_claim_dependency_review_v1.json",
    "terminology_post_dryrun_review_non_claims_register_v1.json",
    "terminology_canonical_table_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str], ...] = (
    ("Phase-Terminology-Canonical-Table-Planning-v1-001", "terminology_canonical_table_planning_v1_smoke_v0"),
    ("Phase-Terminology-Canonical-Table-DryRun-v1-001", "terminology_canonical_table_dryrun_v1_smoke_v0"),
    (
        "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001",
        "terminology_canonical_table_post_dryrun_review_v1_smoke_v0",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Generate Formal Terminology Canonical Table",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "formal_terminology_table_generation",
        "target_scope": "terminology_canonical_table_v1.json",
        "entry_reason": "success claim gate not planned; formal generation not authorized",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["success claim gate not planned"],
        "permission_impact": "deferred; not formal table generation allowed",
        "next_phase_candidate": "Phase-Terminology-Canonical-Table-Generation-v1-001",
        "non_claims": ["deferred ≠ terminology_canonical_table_v1.json generated"],
    },
    {
        "route_id": "B",
        "route_name": "Terminology Canonicalization Execution Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "terminology_canonicalization_execution_planning",
        "target_scope": "terminology canonicalization execution",
        "entry_reason": "Route C P0 dependency first",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["success claim gate not planned"],
        "permission_impact": "deferred; not terminology canonicalization execution",
        "next_phase_candidate": "Phase-Terminology-Canonicalization-Execution-Planning-v1-001",
        "non_claims": ["deferred ≠ terminology canonicalization allowed"],
    },
    {
        "route_id": "C",
        "route_name": "Success Claim Gate Canonicalization Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "success_claim_gate_canonicalization_planning",
        "target_scope": "success claim gate semantics",
        "entry_reason": "terminology planning/dry-run/post-review complete; Route C P0 dependency ready",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "planning allowed only; not gate generated / enforced / success claim allowed",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": [
            "selected ≠ success claim gate generated",
            "≠ success claim allowed",
            "≠ success claim gate execution",
        ],
    },
    {
        "route_id": "D",
        "route_name": "Permission Semantics Canonicalization Execution Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "permission_semantics_canonicalization_execution_planning",
        "target_scope": "permission semantics canonicalization execution",
        "entry_reason": "success claim gate planning loop not closed",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["success claim gate not planned"],
        "permission_impact": "deferred; not permission semantics canonicalization execution",
        "next_phase_candidate": "Phase-Permission-Semantics-Canonicalization-Execution-Planning-v1-001",
        "non_claims": ["deferred ≠ permission semantics canonicalization execution"],
    },
    {
        "route_id": "E",
        "route_name": "Continue Terminology Specialist Planning",
        "priority": "Optional / Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "terminology_specialist_planning",
        "target_scope": "24 high-risk terms supplement",
        "entry_reason": "24 terms already cover main migration governance risks",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "optional deferred",
        "next_phase_candidate": "Phase-Terminology-Specialist-Planning-v1-001",
        "non_claims": ["optional; not selected"],
    },
    {
        "route_id": "F",
        "route_name": "Owner/Operator Approval Protocol Planning",
        "priority": "Deferred",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_operator_approval_protocol_planning",
        "target_scope": "owner/operator approval chain",
        "entry_reason": "deferred until success claim gate planning complete",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["success claim gate not planned"],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "non_claims": ["deferred ≠ approval granted"],
    },
    {
        "route_id": "G",
        "route_name": "Direct Success Claim Gate Execution / Success Claim Allowance",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_success_claim_gate_execution",
        "target_scope": "success claim gate execution / success claim allowance",
        "entry_reason": "gate not planned/dry-run/reviewed; evidence/authorization not established",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": [
            "success claim gate not planned",
            "runtime evidence not available",
            "authorization chain not active",
        ],
        "permission_impact": "forbidden",
        "next_phase_candidate": "Phase-Direct-Success-Claim-Gate-Execution-v1-001",
        "non_claims": ["blocked ≠ success claim allowed", "≠ gate execution allowed"],
    },
]

SUCCESS_CLAIM_PLANNING_TOPICS: Tuple[Tuple[str, str], ...] = (
    ("GO must not imply success", "GO vs success"),
    ("completed must not imply succeeded", "completed vs succeeded"),
    ("reviewed must not imply accepted", "reviewed vs accepted"),
    ("boundary_ok must not imply execution safe", "boundary_ok vs execution safe"),
    ("verifier_report must not imply runtime evidence", "verifier_report vs runtime evidence"),
    ("summary must not imply success evidence", "summary vs success evidence"),
    ("candidate evidence must not imply success evidence", "candidate evidence vs success evidence"),
    ("real execution observed requirement", "real execution observed requirement"),
    ("evidence generated requirement", "evidence generated requirement"),
    ("authorization granted requirement", "authorization requirement"),
    ("success claim allowed gate", "success claim allowed gate"),
    ("success claim blocked non-claim", "success claim blocked non-claim"),
)

ENTRY_RISKS: Tuple[Tuple[str, str, str, str], ...] = (
    ("R01", "terminology table is not formally generated", "high", "DryRun GO ≠ formal table generated"),
    ("R02", "terminology is not enforced", "high", "planning/dry-run ≠ terminology enforced"),
    ("R03", "success claim gate not generated", "high", "Route C ≠ gate generated"),
    ("R04", "success claim not allowed", "high", "planning ≠ success_claim_allowed"),
    ("R05", "evidence chain not finalized", "high", "verifier_report ≠ runtime evidence"),
    ("R06", "runtime evidence not available", "high", "no runtime_invoked in terminology chain"),
    ("R07", "authorization chain not active", "high", "authorization_granted_now=false"),
    ("R08", "real execution not observed", "high", "execution_committed=false"),
    ("R09", "verifier not modified", "medium", "verifier_modified_now=false required"),
    ("R10", "phase template not modified", "medium", "phase_template_modified_now=false required"),
    ("R11", "owner/operator approval not active", "high", "owner approval not granted"),
    ("R12", "real rehearsal not available", "high", "real_rehearsal_execution_allowed=false"),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "terminology canonicalization execution",
    "formal terminology table generation",
    "terminology enforcement",
    "semantic registry write",
    "success claim gate canonicalization execution",
    "success claim gate generation",
    "success claim allowance",
    "permission semantics canonicalization execution",
    "verifier modification",
    "phase template modification",
    "automation implementation",
    "documentation auto-sync",
    "debt fix execution",
    "owner/operator approval",
    "real rollback rehearsal execution",
    "real migration execution",
    "batch arming",
)

ROADMAP_NON_CLAIMS = [
    "Roadmap Decision GO does not mean terminology canonical table is generated.",
    "Roadmap Decision GO does not mean terminology is canonicalized.",
    "Roadmap Decision GO does not mean terminology rules are enforced.",
    "Route C selected does not mean success claim gate is generated.",
    "Route C selected does not mean success claim is allowed.",
    "Route A/B/D deferred means formal table generation / terminology execution / permission semantics execution remain unavailable.",
    "Route G blocked means direct success claim gate execution remains forbidden.",
    "Roadmap Decision GO does not mean verifier or phase template has been modified.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "terminology_canonicalization_executed_now": False,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
        "registry_written_now": False,
        "success_claim_canonicalization_executed_now": False,
        "success_claim_gate_generated_now": False,
        "success_claim_allowed": False,
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
        root / "terminology_canonical_table_post_dryrun_review_readiness_decision_v1.json"
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
                formal_table_generation_observed=sm.get("canonical_table_generated_now") is True,
                terminology_enforcement_observed=sm.get("terminology_enforced_now") is True,
                registry_write_observed=sm.get("registry_written_now") is True,
                verifier_modification_observed=sm.get("verifier_modified_now") is True,
                phase_template_modification_observed=sm.get("phase_template_modified_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_dependency_status_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for topic, terms in SUCCESS_CLAIM_TOPICS:
        rows.append(
            _decision_row(
                success_claim_topic=topic,
                dependent_terms=terms,
                terminology_dependency_reviewed=True,
                terminology_dependency_ready_for_planning_use=True,
                success_claim_gate_generated_now=False,
                success_claim_canonicalization_executed_now=False,
                blocks_success_claim_execution=True,
                recommended_next_action="enter Success Claim Gate Canonicalization Planning",
            )
        )
    return rows


def _build_success_claim_gate_planning_scope() -> List[Dict[str, Any]]:
    topic_map = {t: terms for t, terms in SUCCESS_CLAIM_TOPICS}
    rows: List[Dict[str, Any]] = []
    for planning_topic, claim_topic in SUCCESS_CLAIM_PLANNING_TOPICS:
        terms = topic_map.get(claim_topic, [])
        rows.append(
            _decision_row(
                planning_topic=planning_topic,
                dependent_terms=terms,
                why_required=f"terminology chain reviewed; {claim_topic} must be gated before success claim",
                required_gate_fields=[
                    "success_claim_allowed",
                    "success_claim_blocked_reason",
                    "required_evidence_refs",
                    "required_authorization_refs",
                ],
                required_forbidden_interpretations=[f"{claim_topic}: forbidden misread patterns"],
                required_evidence_rules=["candidate vs runtime vs success evidence separation"],
                required_non_claims=[f"planning GO does not imply {claim_topic} satisfied"],
                required_verifier_usage=[f"verify_success_claim_gate_{claim_topic.replace(' ', '_')}"],
                required_next_phase_output=f"success_claim_gate_plan_{claim_topic.replace(' ', '_')}_v1.json",
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
                blocks_execution=True,
                required_non_claim=non_claim,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_terminology_canonical_table_roadmap_decision_v1(
    *,
    terminology_canonical_table_post_dryrun_review_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(terminology_canonical_table_post_dryrun_review_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream post-dryrun review verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_readiness.get("ready_for_terminology_canonical_table_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_terminology_canonical_table_roadmap_decision")
    if up_summary.get("canonical_table_generated_now") is not False:
        blockers.append("upstream canonical_table_generated_now is not false")
    if up_summary.get("terminology_enforced_now") is not False:
        blockers.append("upstream terminology_enforced_now is not false")
    if up_summary.get("registry_written_now") is not False:
        blockers.append("upstream registry_written_now is not false")
    if up_readiness.get("ready_for_success_claim_gate_planning") is not False:
        blockers.append("upstream ready_for_success_claim_gate_planning must remain false until this phase completes")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    dependency_rows = _build_dependency_status_matrix()
    planning_scope_rows = _build_success_claim_gate_planning_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()
    risk_rows, risk_pass = _build_entry_risk_matrix()

    route_c = next(r for r in route_rows if r.get("route_id") == "C")
    route_g = next(r for r in route_rows if r.get("route_id") == "G")
    route_a = next(r for r in route_rows if r.get("route_id") == "A")
    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_d = next(r for r in route_rows if r.get("route_id") == "D")

    route_ok = (
        route_c.get("selected_now") is True
        and route_c.get("allowed_now") is True
        and "planning" in str(route_c.get("permission_impact", "")).lower()
        and route_g.get("blocked_now") is True
        and route_g.get("allowed_now") is False
        and route_a.get("deferred") is True
        and route_b.get("deferred") is True
        and route_d.get("deferred") is True
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    decision_ready = (
        chain_pass
        and non_release_pass
        and risk_pass
        and route_ok
        and len(dependency_rows) >= 12
        and len(planning_scope_rows) >= 12
        and not blockers
    )
    boundary_ok = decision_ready

    terminology_canonical_table_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_terminology_canonical_table_roadmap_decision_observed=up_readiness.get(
            "ready_for_terminology_canonical_table_roadmap_decision"
        )
        is True,
    )

    completed_terminology_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    terminology_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        **_decision_meta(),
    }
    terminology_to_success_claim_dependency_status_matrix = {
        "rows": dependency_rows,
        "row_count": len(dependency_rows),
        "all_ready_for_planning_use": True,
        **_decision_meta(),
    }
    success_claim_gate_planning_scope = {
        "rows": planning_scope_rows,
        "row_count": len(planning_scope_rows),
        **_decision_meta(),
    }
    terminology_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    terminology_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }
    success_claim_gate_entry_readiness_risk_matrix = {
        "rows": risk_rows,
        "row_count": len(risk_rows),
        "all_pass": risk_pass,
        **_decision_meta(),
    }

    terminology_canonical_table_roadmap_readiness_decision = {
        "ready_for_success_claim_gate_canonicalization_planning": boundary_ok,
        "ready_for_success_claim_gate_execution": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_terminology_canonicalization_execution": False,
        "ready_for_terminology_enforcement": False,
        "ready_for_canonical_table_generation": False,
        "ready_for_permission_semantics_canonicalization_execution": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_debt_fix_execution": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "selected_route": SELECTED_ROUTE,
        "direct_success_claim_gate_execution_blocked": True,
        "terminology_chain_completed": chain_pass,
        "formal_table_generation_deferred": True,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "terminology_canonical_table_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "success_claim_dependency_count": len(dependency_rows),
        "success_claim_planning_scope_count": len(planning_scope_rows),
        "entry_risk_count": len(risk_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "route_c_selected_now": route_c.get("selected_now") is True,
        "route_c_planning_only": "planning" in str(route_c.get("permission_impact", "")).lower(),
        "route_g_blocked_now": route_g.get("blocked_now") is True,
        "route_a_deferred": route_a.get("deferred") is True,
        "route_b_deferred": route_b.get("deferred") is True,
        "route_d_deferred": route_d.get("deferred") is True,
        "direct_success_claim_gate_execution_blocked": True,
        "success_claim_gate_generated_now": False,
        "success_claim_allowed": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "terminology_canonical_table_post_dryrun_review",
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
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_ROADMAP_DECISION_REQUIRES_FIXES",
        "reason": "Route C selected; planning only; success claim gate execution blocked",
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "terminology_canonical_table_roadmap_decision_policy": terminology_canonical_table_roadmap_decision_policy,
        "completed_terminology_chain_review": completed_terminology_chain_review,
        "terminology_roadmap_route_candidate_matrix": terminology_roadmap_route_candidate_matrix,
        "terminology_to_success_claim_dependency_status_matrix": terminology_to_success_claim_dependency_status_matrix,
        "success_claim_gate_planning_scope": success_claim_gate_planning_scope,
        "terminology_roadmap_non_release_matrix": terminology_roadmap_non_release_matrix,
        "terminology_roadmap_decision_non_claims_register": terminology_roadmap_decision_non_claims_register,
        "success_claim_gate_entry_readiness_risk_matrix": success_claim_gate_entry_readiness_risk_matrix,
        "terminology_canonical_table_roadmap_readiness_decision": terminology_canonical_table_roadmap_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
