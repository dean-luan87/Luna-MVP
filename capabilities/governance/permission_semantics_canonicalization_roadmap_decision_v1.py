# -*- coding: utf-8 -*-
"""Permission Semantics Canonicalization Roadmap Decision v1.

Roadmap decision only: select Terminology Canonical Table Planning (Route B)
with Route C as pending P0 dependency. Does not execute canonicalization,
enforce semantics, or release real authorization/execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001"
DECISION_SCOPE = "permission_semantics_canonicalization_roadmap_decision_only"
DECISION_ID = "permission_semantics_canonicalization_roadmap_decision_v1_001"
SOURCE_CHAIN = "permission_semantics_canonicalization_roadmap_decision_v1"

SOURCE_PHASE = "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)

FINAL_DECISION = (
    "PERMISSION_SEMANTICS_CANONICALIZATION_ROADMAP_DECISION_READY_FOR_TERMINOLOGY_CANONICAL_TABLE_PLANNING"
)
NEXT_PHASE = "Phase-Terminology-Canonical-Table-Planning-v1-001"

SELECTED_ROUTE = "Route B — Terminology Canonical Table Planning"
DEFERRED_P0 = "Route C — Success Claim Gate Canonicalization Planning"

POST_REVIEW_ARTIFACTS: Tuple[str, ...] = (
    "permission_semantics_canonicalization_post_dryrun_review_policy_v1.json",
    "semantics_dryrun_completeness_review_v1.json",
    "semantics_non_enforcement_review_matrix_v1.json",
    "semantic_registry_write_review_v1.json",
    "forbidden_combination_enforcement_review_v1.json",
    "development_norms_template_modification_review_v1.json",
    "verifier_checklist_non_modification_review_v1.json",
    "non_claims_generation_non_write_review_v1.json",
    "semantic_dryrun_cross_artifact_review_v1.json",
    "semantics_post_dryrun_review_non_claims_register_v1.json",
    "permission_semantics_canonicalization_post_dryrun_review_readiness_decision_v1.json",
)

COMPLETED_CHAIN: Tuple[Tuple[str, str, str], ...] = (
    (
        "Phase-Permission-Semantics-Canonicalization-Planning-v1-001",
        "permission_semantics_canonicalization_planning_v1_smoke_v0",
        "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN",
    ),
    (
        "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001",
        "permission_semantics_canonicalization_dryrun_v1_smoke_v0",
        "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW",
    ),
    (
        "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001",
        "permission_semantics_canonicalization_post_dryrun_review_v1_smoke_v0",
        "PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION",
    ),
)

ROUTE_OPTIONS: List[Dict[str, Any]] = [
    {
        "route_id": "A",
        "route_name": "Canonicalization Execution Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "canonicalization_execution_planning",
        "target_scope": "permission semantics canonicalization execution planning",
        "entry_reason": "Route B/C dependency loop not closed; terminology table not planned",
        "required_dependencies": [SELECTED_ROUTE, DEFERRED_P0],
        "missing_preconditions": ["terminology canonical table not planned", "success claim gate not planned"],
        "permission_impact": "deferred; not canonicalization execution allowed",
        "next_phase_candidate": "Phase-Permission-Semantics-Canonicalization-Execution-Planning-v1-001",
        "non_claims": ["deferred ≠ canonicalization execution allowed"],
    },
    {
        "route_id": "B",
        "route_name": "Terminology Canonical Table Planning",
        "priority": "P0",
        "selected_now": True,
        "allowed_now": True,
        "blocked_now": False,
        "deferred": False,
        "route_type": "terminology_canonical_table_planning",
        "target_scope": "high-risk governance terminology",
        "entry_reason": "permission semantics planned/dry-run/reviewed; terminology still fragmented",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "planning allowed only; not terminology canonicalization execution",
        "next_phase_candidate": NEXT_PHASE,
        "non_claims": ["selected ≠ terminology table generated", "≠ terminology canonicalized"],
    },
    {
        "route_id": "C",
        "route_name": "Success Claim Gate Canonicalization Planning",
        "priority": "P0",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "success_claim_gate_canonicalization_planning",
        "target_scope": "success claim gate semantics",
        "entry_reason": "pending P0 dependency after Route B",
        "required_dependencies": [SELECTED_ROUTE],
        "missing_preconditions": ["terminology canonical table not planned"],
        "permission_impact": "deferred P0 dependency; planning not allowed until Route B complete",
        "next_phase_candidate": "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001",
        "non_claims": ["deferred ≠ success claim gate fixed", "≠ canonicalization execution allowed"],
    },
    {
        "route_id": "D",
        "route_name": "Owner/Operator Approval Protocol Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "owner_operator_approval_protocol_planning",
        "target_scope": "owner/operator approval chain",
        "entry_reason": "deferred until terminology and success claim planning complete",
        "required_dependencies": [SELECTED_ROUTE, DEFERRED_P0],
        "missing_preconditions": ["terminology not canonicalized", "success claim gate not planned"],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001",
        "non_claims": ["deferred ≠ approval granted"],
    },
    {
        "route_id": "E",
        "route_name": "Boundary Object Registry Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "boundary_object_registry_planning",
        "target_scope": "protected/HR/DnAE/eval_out boundary objects",
        "entry_reason": "deferred",
        "required_dependencies": [],
        "missing_preconditions": [],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Boundary-Object-Registry-Planning-v1-001",
        "non_claims": ["planning deferred"],
    },
    {
        "route_id": "F",
        "route_name": "Evidence Chain Governance Planning",
        "priority": "P1",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": False,
        "deferred": True,
        "route_type": "evidence_chain_governance_planning",
        "target_scope": "evidence candidate/runtime/success-claim lifecycle",
        "entry_reason": "deferred",
        "required_dependencies": [DEFERRED_P0],
        "missing_preconditions": ["success claim gate not planned"],
        "permission_impact": "deferred",
        "next_phase_candidate": "Phase-Evidence-Chain-Governance-Planning-v1-001",
        "non_claims": ["planning deferred"],
    },
    {
        "route_id": "G",
        "route_name": "Direct Canonicalization Execution",
        "priority": "Blocked",
        "selected_now": False,
        "allowed_now": False,
        "blocked_now": True,
        "deferred": False,
        "route_type": "direct_canonicalization_execution",
        "target_scope": "permission semantics canonicalization execution",
        "entry_reason": "forbidden: terminology and success claim planning not closed",
        "required_dependencies": [SELECTED_ROUTE, DEFERRED_P0],
        "missing_preconditions": ["terminology table not planned", "success claim gate not planned"],
        "permission_impact": "not allowed",
        "next_phase_candidate": "Phase-Direct-Canonicalization-Execution-v1-001",
        "non_claims": ["blocked ≠ canonicalization execution allowed"],
    },
]

TERMINOLOGY_TERMS: Tuple[Tuple[str, str, str], ...] = (
    ("planning", "phase type vs execution", "planning GO misread as execution allowed"),
    ("dry-run", "simulation vs real action", "dry-run GO misread as real success"),
    ("review", "audit vs authorization", "review GO misread as authorization granted"),
    ("post-review", "audit vs fix", "post-review GO misread as debt fixed"),
    ("roadmap decision", "route selection vs permission release", "route selected misread as execution allowed"),
    ("register", "registration vs remediation", "register GO misread as fix executed"),
    ("authorization", "auth state vs planning", "authorization term used without chain"),
    ("authorization planning", "plan vs grant", "planned misread as granted"),
    ("authorization request", "request vs grant", "requested misread as granted"),
    ("authorization granted", "explicit grant vs allowed", "granted without evidence chain"),
    ("owner approval", "owner vs operator", "owner approval conflated with operator ack"),
    ("operator acknowledgement", "ack vs execution window", "ack misread as execution allowed"),
    ("execution window", "window vs commit", "window opened misread as execution committed"),
    ("allowed", "scope permission vs executed", "allowed misread as committed"),
    ("granted", "explicit grant vs deferred", "granted used for planning phase"),
    ("committed", "side effect vs planned", "committed inferred from summary text"),
    ("generated", "artifact vs executable", "generated misread as runtime evidence"),
    ("executed", "real action vs simulated", "executed inferred from dry-run GO"),
    ("enforced", "blueprint vs active rule", "planning artifact misread as enforced"),
    ("GO", "phase pass vs success", "GO misread as migration/rehearsal success"),
    ("ready", "readiness vs authorization", "ready_for_* misread as execution allowed"),
    ("evidence", "candidate vs runtime", "verifier_report misread as runtime evidence"),
    ("success", "claim vs phase completion", "completed misread as succeeded"),
    ("success claim", "gated claim vs summary", "summary text used as success evidence"),
)

SUCCESS_CLAIM_TOPICS: Tuple[Tuple[str, str, bool], ...] = (
    ("GO vs success", "GO must not imply success claim allowed", True),
    ("completed vs succeeded", "completion ≠ success claim", True),
    ("reviewed vs accepted", "review ≠ acceptance for success", True),
    ("boundary_ok vs execution safe", "boundary_ok ≠ execution safe", True),
    ("verifier_report vs runtime evidence", "verifier report ≠ runtime evidence", True),
    ("summary vs success evidence", "summary ≠ success evidence", True),
    ("candidate evidence vs success evidence", "candidate ≠ success claim evidence", True),
    ("real execution observed requirement", "success claim requires real execution", True),
    ("evidence generated requirement", "success claim requires evidence chain", True),
    ("authorization requirement", "success claim requires authorization chain", True),
    ("success claim allowed gate", "success_claim_allowed requires independent gate", True),
    ("success claim blocked non-claim", "blocked state must retain non-claim", True),
)

NON_RELEASE_PERMISSIONS: Tuple[str, ...] = (
    "canonicalization execution",
    "semantics enforcement",
    "terminology canonicalization execution",
    "success claim gate canonicalization execution",
    "semantic registry write",
    "forbidden combination enforcement",
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
    "Roadmap Decision GO does not mean permission semantics are canonicalized.",
    "Roadmap Decision GO does not mean semantics are enforced.",
    "Route B selected does not mean terminology table has been generated.",
    "Route C deferred does not mean success claim gate debt is fixed.",
    "Route A deferred does not mean canonicalization execution is allowed.",
    "Route G blocked means direct canonicalization execution remains forbidden.",
    "Roadmap Decision GO does not mean verifier or phase template has been modified.",
    "Roadmap Decision GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _decision_meta() -> Dict[str, Any]:
    return {
        "roadmap_decision_only": True,
        "canonicalization_executed_now": False,
        "canonicalization_enforced_now": False,
        "terminology_canonicalization_executed_now": False,
        "success_claim_canonicalization_executed_now": False,
        "registry_written_now": False,
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
        root / "permission_semantics_canonicalization_post_dryrun_review_readiness_decision_v1.json"
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
    for phase_name, eval_out, expected_final in COMPLETED_CHAIN:
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
                canonicalization_release_observed=False,
                enforcement_observed=sm.get("canonicalization_enforced_now") is True,
                verifier_modification_observed=sm.get("verifier_modified_now") is True,
                phase_template_modification_observed=sm.get("phase_template_modified_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def _build_route_matrix() -> List[Dict[str, Any]]:
    return [_decision_row(**r) for r in ROUTE_OPTIONS]


def _build_bound_dependency_matrix() -> List[Dict[str, Any]]:
    return [
        _decision_row(
            dependency_route=SELECTED_ROUTE,
            required_by_previous_route_a=True,
            planning_completed=False,
            dryrun_completed=False,
            post_review_completed=False,
            execution_completed=False,
            current_status="selected_next",
            blocks_canonicalization_execution_planning=True,
            recommended_next_action="enter Terminology Canonical Table Planning",
        ),
        _decision_row(
            dependency_route=DEFERRED_P0,
            required_by_previous_route_a=True,
            planning_completed=False,
            dryrun_completed=False,
            post_review_completed=False,
            execution_completed=False,
            current_status="pending_p0_dependency",
            blocks_canonicalization_execution_planning=True,
            recommended_next_action="defer until Route B planning complete",
        ),
    ]


def _build_terminology_scope() -> List[Dict[str, Any]]:
    return [
        _decision_row(
            term=term,
            why_high_risk=why,
            current_misread_risk=risk,
            must_define_canonical_meaning=True,
            must_define_forbidden_interpretation=True,
            must_define_required_fields=True,
            must_define_verifier_usage=True,
            required_next_phase_output=f"terminology_canonical_table_entry_{term.replace(' ', '_')}",
        )
        for term, why, risk in TERMINOLOGY_TERMS
    ]


def _build_success_claim_scope() -> List[Dict[str, Any]]:
    return [
        _decision_row(
            success_claim_topic=topic,
            why_required=why,
            depends_on_terminology_table=depends,
            must_be_planned_before_canonicalization_execution=True,
            required_future_phase="Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001",
        )
        for topic, why, depends in SUCCESS_CLAIM_TOPICS
    ]


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


def run_permission_semantics_canonicalization_roadmap_decision_v1(
    *,
    permission_semantics_canonicalization_post_dryrun_review_root: str,
    eval_out_root: Optional[str] = None,
) -> Dict[str, Any]:
    upstream = _load_upstream(permission_semantics_canonicalization_post_dryrun_review_root)
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
    if up_readiness.get("ready_for_permission_semantics_canonicalization_roadmap_decision") is not True:
        blockers.append("upstream not ready_for_permission_semantics_canonicalization_roadmap_decision")
    if up_summary.get("canonicalization_enforced_now") is not False:
        blockers.append("upstream canonicalization_enforced_now is not false")
    if up_summary.get("registry_written_now") is not False:
        blockers.append("upstream registry_written_now is not false")
    if up_summary.get("forbidden_combinations_enforced_now") is not False:
        blockers.append("upstream forbidden_combinations_enforced_now is not false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    chain_rows, chain_pass = _build_completed_chain_review()
    route_rows = _build_route_matrix()
    bound_rows = _build_bound_dependency_matrix()
    terminology_rows = _build_terminology_scope()
    success_rows = _build_success_claim_scope()
    non_release_rows, non_release_pass = _build_non_release_matrix()

    route_b = next(r for r in route_rows if r.get("route_id") == "B")
    route_c = next(r for r in route_rows if r.get("route_id") == "C")
    route_g = next(r for r in route_rows if r.get("route_id") == "G")
    route_a = next(r for r in route_rows if r.get("route_id") == "A")

    route_ok = (
        route_b.get("selected_now") is True
        and route_b.get("allowed_now") is True
        and route_c.get("deferred") is True
        and route_g.get("blocked_now") is True
        and route_a.get("allowed_now") is False
    )
    if not route_ok:
        blockers.append("route selection matrix invalid")

    decision_ready = chain_pass and non_release_pass and route_ok and not blockers
    boundary_ok = decision_ready

    permission_semantics_canonicalization_roadmap_decision_policy = _decision_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_permission_semantics_canonicalization_roadmap_decision_observed=up_readiness.get(
            "ready_for_permission_semantics_canonicalization_roadmap_decision"
        )
        is True,
    )

    completed_permission_semantics_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        **_decision_meta(),
    }
    permission_semantics_roadmap_route_candidate_matrix = {
        "rows": route_rows,
        "row_count": len(route_rows),
        "selected_route": SELECTED_ROUTE,
        "deferred_p0_dependency": DEFERRED_P0,
        **_decision_meta(),
    }
    bound_dependency_status_matrix = {
        "rows": bound_rows,
        "row_count": len(bound_rows),
        **_decision_meta(),
    }
    terminology_planning_scope = {
        "rows": terminology_rows,
        "row_count": len(terminology_rows),
        **_decision_meta(),
    }
    success_claim_dependency_planning_scope = {
        "rows": success_rows,
        "row_count": len(success_rows),
        **_decision_meta(),
    }
    permission_semantics_roadmap_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": non_release_pass,
        **_decision_meta(),
    }
    non_claims_rows = [
        _decision_row(non_claim=nc, required=True, present=True, risk_if_missing="roadmap GO misread")
        for nc in ROADMAP_NON_CLAIMS
    ]
    permission_semantics_roadmap_decision_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_decision_meta(),
    }

    permission_semantics_canonicalization_roadmap_readiness_decision = {
        "ready_for_terminology_canonical_table_planning": boundary_ok,
        "ready_for_success_claim_gate_canonicalization_planning": False,
        "ready_for_canonicalization_execution_planning": False,
        "ready_for_canonicalization_execution": False,
        "ready_for_semantics_enforcement": False,
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
        "deferred_p0_dependency": DEFERRED_P0,
        "direct_canonicalization_execution_blocked": True,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "decision_scope": DECISION_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "permission_semantics_canonicalization_post_dryrun_review_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "completed_chain_count": len(chain_rows),
        "route_candidate_count": len(route_rows),
        "terminology_scope_count": len(terminology_rows),
        "success_claim_scope_count": len(success_rows),
        "non_release_count": len(non_release_rows),
        "selected_route": SELECTED_ROUTE,
        "deferred_p0_dependency": DEFERRED_P0,
        "route_b_selected_now": route_b.get("selected_now") is True,
        "route_c_deferred": route_c.get("deferred") is True,
        "route_g_blocked_now": route_g.get("blocked_now") is True,
        "direct_canonicalization_execution_blocked": True,
        "bound_dependencies": [SELECTED_ROUTE, DEFERRED_P0],
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_decision_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "permission_semantics_canonicalization_post_dryrun_review",
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
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_ROADMAP_DECISION_REQUIRES_FIXES",
        "reason": "terminology table planning first; Route C pending P0; direct canonicalization blocked",
        **_decision_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "permission_semantics_canonicalization_roadmap_decision_policy": permission_semantics_canonicalization_roadmap_decision_policy,
        "completed_permission_semantics_chain_review": completed_permission_semantics_chain_review,
        "permission_semantics_roadmap_route_candidate_matrix": permission_semantics_roadmap_route_candidate_matrix,
        "bound_dependency_status_matrix": bound_dependency_status_matrix,
        "terminology_planning_scope": terminology_planning_scope,
        "success_claim_dependency_planning_scope": success_claim_dependency_planning_scope,
        "permission_semantics_roadmap_non_release_matrix": permission_semantics_roadmap_non_release_matrix,
        "permission_semantics_roadmap_decision_non_claims_register": permission_semantics_roadmap_decision_non_claims_register,
        "permission_semantics_canonicalization_roadmap_readiness_decision": permission_semantics_canonicalization_roadmap_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
