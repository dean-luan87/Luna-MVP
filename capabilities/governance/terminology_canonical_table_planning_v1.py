# -*- coding: utf-8 -*-
"""Terminology Canonical Table Planning v1.

Planning only: define high-risk terminology canonical table blueprint.
Does not execute terminology canonicalization, generate formal table, or enforce rules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Terminology-Canonical-Table-Planning-v1-001"
PLANNING_SCOPE = "terminology_canonical_table_planning_only"
PLANNING_ID = "terminology_canonical_table_planning_v1_001"
SOURCE_CHAIN = "terminology_canonical_table_planning_v1"

SOURCE_PHASE = "Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001"
SELECTED_ROUTE = "Route B — Terminology Canonical Table Planning"
SUCCESS_CLAIM_DEP = "Route C — Success Claim Gate Canonicalization Planning"

FINAL_DECISION = "TERMINOLOGY_CANONICAL_TABLE_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Terminology-Canonical-Table-DryRun-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "permission_semantics_canonicalization_roadmap_decision_policy_v1.json",
    "completed_permission_semantics_chain_review_v1.json",
    "permission_semantics_roadmap_route_candidate_matrix_v1.json",
    "bound_dependency_status_matrix_v1.json",
    "terminology_planning_scope_v1.json",
    "success_claim_dependency_planning_scope_v1.json",
    "permission_semantics_roadmap_non_release_matrix_v1.json",
    "permission_semantics_roadmap_decision_non_claims_register_v1.json",
    "permission_semantics_canonicalization_roadmap_readiness_decision_v1.json",
)

REQUIRED_TERMS: Tuple[str, ...] = (
    "planning",
    "dry-run",
    "review",
    "post-review",
    "roadmap decision",
    "register",
    "authorization",
    "authorization planning",
    "authorization request",
    "authorization granted",
    "owner approval",
    "operator acknowledgement",
    "execution window",
    "allowed",
    "granted",
    "committed",
    "generated",
    "executed",
    "enforced",
    "GO",
    "ready",
    "evidence",
    "success",
    "success claim",
)

HIGH_RISK_LEVEL_TERMS = frozenset(
    {
        "GO",
        "ready",
        "allowed",
        "granted",
        "generated",
        "executed",
        "enforced",
        "success",
        "success claim",
        "authorization request",
        "authorization granted",
        "owner approval",
        "operator acknowledgement",
        "execution window",
        "evidence",
    }
)

TERM_SPECS: Dict[str, Dict[str, Any]] = {
    "planning": {
        "why": "phase type vs execution",
        "misread": "planning GO misread as execution allowed",
        "risk": "high",
        "phases": "planning",
        "forbidden": "planning GO does not mean execution authorized",
        "fields": "planning_only=true",
        "verifier": "phase_type_flag_check",
    },
    "dry-run": {
        "why": "simulation vs real action",
        "misread": "dry-run GO misread as real success",
        "risk": "high",
        "phases": "dry-run",
        "forbidden": "dry-run does not mean real action succeeded",
        "fields": "dryrun_only=true,simulated=true",
        "verifier": "dryrun_non_real_action_check",
    },
    "review": {
        "why": "audit vs authorization",
        "misread": "review GO misread as authorization granted",
        "risk": "high",
        "phases": "review,post-review",
        "forbidden": "review does not mean accepted or authorized",
        "fields": "review_only=true",
        "verifier": "review_non_authorization_check",
    },
    "post-review": {
        "why": "audit vs fix",
        "misread": "post-review GO misread as debt fixed",
        "risk": "high",
        "phases": "post-review",
        "forbidden": "post-review does not mean remediation executed",
        "fields": "post_dryrun_review_only=true",
        "verifier": "post_review_non_fix_check",
    },
    "roadmap decision": {
        "why": "route selection vs permission release",
        "misread": "selected route misread as execution allowed",
        "risk": "high",
        "phases": "roadmap decision",
        "forbidden": "roadmap decision does not mean authorization release",
        "fields": "roadmap_decision_only=true,selected_route",
        "verifier": "route_non_release_check",
    },
    "register": {
        "why": "registration vs remediation",
        "misread": "register GO misread as fix executed",
        "risk": "medium",
        "phases": "register",
        "forbidden": "register does not mean debt fixed",
        "fields": "register_only=true",
        "verifier": "register_non_fix_check",
    },
    "authorization": {
        "why": "auth concept umbrella",
        "misread": "authorization term used without chain",
        "risk": "high",
        "phases": "authorization planning,authorization dry-run",
        "forbidden": "authorization mentioned without granted_now flag context",
        "fields": "authorization_granted_now",
        "verifier": "authorization_context_check",
    },
    "authorization planning": {
        "why": "plan vs grant",
        "misread": "planned misread as granted",
        "risk": "high",
        "phases": "authorization planning",
        "forbidden": "authorization planning does not mean authorization granted",
        "fields": "authorization_granted_now=false",
        "verifier": "auth_planned_not_granted_check",
    },
    "authorization request": {
        "why": "request vs grant",
        "misread": "requested misread as granted",
        "risk": "high",
        "phases": "authorization planning",
        "forbidden": "authorization request does not mean authorization granted",
        "fields": "authorization_requested,authorization_granted_now=false",
        "verifier": "auth_request_not_granted_check",
    },
    "authorization granted": {
        "why": "explicit grant vs allowed",
        "misread": "granted without evidence chain",
        "risk": "high",
        "phases": "authorization review,real execution",
        "forbidden": "authorization granted without owner/operator chain",
        "fields": "authorization_granted_now,source_approval_ref,actor_ref",
        "verifier": "authorization_granted_evidence_check",
    },
    "owner approval": {
        "why": "owner vs operator",
        "misread": "owner approval conflated with operator ack",
        "risk": "high",
        "phases": "authorization",
        "forbidden": "owner approval does not mean operator acknowledgement",
        "fields": "owner_approval_granted_now,owner_identity,approval_evidence,timestamp",
        "verifier": "owner_approval_check",
    },
    "operator acknowledgement": {
        "why": "ack vs execution window",
        "misread": "ack misread as execution allowed",
        "risk": "high",
        "phases": "authorization",
        "forbidden": "operator acknowledgement does not mean execution window opened",
        "fields": "operator_acknowledgement_granted_now,operator_identity",
        "verifier": "operator_ack_check",
    },
    "execution window": {
        "why": "window vs commit",
        "misread": "window opened misread as execution committed",
        "risk": "high",
        "phases": "execution planning,real execution",
        "forbidden": "execution window opened does not mean execution committed",
        "fields": "execution_window_opened_now,window_start,window_end,scope",
        "verifier": "execution_window_check",
    },
    "allowed": {
        "why": "scope permission vs executed",
        "misread": "allowed misread as committed",
        "risk": "high",
        "phases": "all non-execution",
        "forbidden": "allowed does not mean execution committed",
        "fields": "*_allowed flags",
        "verifier": "allowed_not_committed_check",
    },
    "granted": {
        "why": "explicit grant vs deferred",
        "misread": "granted used in planning phase",
        "risk": "high",
        "phases": "authorization,execution",
        "forbidden": "granted in summary without authorization_granted_now",
        "fields": "authorization_granted_now,owner_approval_granted_now",
        "verifier": "granted_field_check",
    },
    "committed": {
        "why": "side effect vs planned",
        "misread": "committed inferred from summary text",
        "risk": "high",
        "phases": "execution",
        "forbidden": "committed cannot be implied by GO or summary alone",
        "fields": "execution_committed,commit_evidence",
        "verifier": "execution_committed_check",
    },
    "generated": {
        "why": "artifact vs executable",
        "misread": "generated misread as executable",
        "risk": "high",
        "phases": "planning,dry-run",
        "forbidden": "generated does not mean executable artifact",
        "fields": "generated_artifact,candidate_artifact",
        "verifier": "candidate_not_executable_check",
    },
    "executed": {
        "why": "real action vs simulated",
        "misread": "executed inferred from dry-run GO",
        "risk": "high",
        "phases": "dry-run,execution",
        "forbidden": "executed does not apply to dry-run phases",
        "fields": "execution_committed,runtime_invoked",
        "verifier": "executed_real_only_check",
    },
    "enforced": {
        "why": "blueprint vs active rule",
        "misread": "planning artifact misread as enforced",
        "risk": "high",
        "phases": "planning,dry-run",
        "forbidden": "enforced_now=true forbidden in planning/dry-run",
        "fields": "enforced_now,not_enforced_now",
        "verifier": "enforced_now_check",
    },
    "GO": {
        "why": "phase pass vs success",
        "misread": "GO misread as migration/rehearsal success",
        "risk": "high",
        "phases": "all",
        "forbidden": "GO does not mean success",
        "fields": "verifier,boundary_ok",
        "verifier": "go_not_success_claim",
    },
    "ready": {
        "why": "readiness vs authorization",
        "misread": "ready_for_* misread as execution allowed",
        "risk": "high",
        "phases": "readiness decision",
        "forbidden": "ready does not mean ready_for_execution without gate",
        "fields": "ready_for_* specific target",
        "verifier": "readiness_implication_check",
    },
    "evidence": {
        "why": "candidate vs runtime",
        "misread": "verifier_report misread as runtime evidence",
        "risk": "high",
        "phases": "dry-run,execution",
        "forbidden": "evidence does not mean success evidence unless usage_scope set",
        "fields": "evidence_type,source_chain,usage_scope",
        "verifier": "evidence_usability_check",
    },
    "success": {
        "why": "claim vs phase completion",
        "misread": "completed misread as succeeded",
        "risk": "high",
        "phases": "execution,review",
        "forbidden": "success term requires success_claim_allowed gate",
        "fields": "success_claim_allowed,success_evidence",
        "verifier": "success_claim_gate_check",
    },
    "success claim": {
        "why": "gated claim vs summary",
        "misread": "summary text used as success evidence",
        "risk": "high",
        "phases": "execution,review",
        "forbidden": "success claim requires real execution and evidence chain",
        "fields": "success_claim_allowed,real_execution_observed,evidence_generated",
        "verifier": "success_claim_gate_check",
    },
}

SUCCESS_CLAIM_TOPICS: Tuple[Tuple[str, List[str]], ...] = (
    ("GO vs success", ["GO", "success", "success claim"]),
    ("completed vs succeeded", ["success", "executed", "committed"]),
    ("reviewed vs accepted", ["review", "post-review"]),
    ("boundary_ok vs execution safe", ["GO", "ready", "allowed"]),
    ("verifier_report vs runtime evidence", ["evidence", "GO"]),
    ("summary vs success evidence", ["success claim", "generated", "evidence"]),
    ("candidate evidence vs success evidence", ["evidence", "generated"]),
    ("real execution observed requirement", ["executed", "execution window", "committed"]),
    ("evidence generated requirement", ["evidence", "generated"]),
    ("authorization requirement", ["authorization granted", "owner approval", "operator acknowledgement"]),
    ("success claim allowed gate", ["success claim", "success", "GO"]),
    ("success claim blocked non-claim", ["success claim", "success"]),
)

OUTPUT_PLAN_ARTIFACTS: Tuple[Tuple[str, str, bool, bool, bool, bool], ...] = (
    ("terminology_canonical_table_policy_v1.json", "table policy", True, True, True, True),
    ("terminology_canonical_table_v1.json", "canonical entries", True, True, True, True),
    ("terminology_required_fields_matrix_v1.json", "required fields", True, True, False, True),
    ("terminology_forbidden_interpretation_matrix_v1.json", "forbidden interpretations", True, True, False, True),
    ("terminology_verifier_usage_matrix_v1.json", "verifier usage", True, False, True, True),
    ("terminology_non_claims_rules_v1.json", "non-claims rules", True, True, False, False),
    ("terminology_success_claim_dependency_matrix_v1.json", "success claim deps", True, True, True, False),
    ("terminology_canonical_table_readiness_decision_v1.json", "readiness decision", True, True, True, True),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "terminology_planning_only": True,
        "terminology_canonicalization_executed_now": False,
        "terminology_enforced_now": False,
        "canonical_table_generated_now": False,
        "registry_written_now": False,
        "success_claim_canonicalization_executed_now": False,
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


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta()}


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
        root / "permission_semantics_canonicalization_roadmap_readiness_decision_v1.json"
    ) if root else None
    routes = _try_read_json(root / "permission_semantics_roadmap_route_candidate_matrix_v1.json") if root else None
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
        "routes": routes or {},
        "artifacts": art,
        "missing": missing,
    }


def _upstream_scope_by_term(artifacts: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    scope = artifacts.get("terminology_planning_scope_v1.json") or {}
    return {r.get("term"): r for r in (scope.get("rows") or [])}


def _build_scope_intake(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by_term = _upstream_scope_by_term(artifacts)
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for term in REQUIRED_TERMS:
        up = by_term.get(term, {})
        observed = term in by_term
        included = observed and up.get("must_define_canonical_meaning") is True
        if not included:
            all_pass = False
        spec = TERM_SPECS.get(term, {})
        rows.append(
            _row(
                term=term,
                observed_from_upstream_scope=observed,
                why_high_risk=up.get("why_high_risk") or spec.get("why", ""),
                current_misread_risk=up.get("current_misread_risk") or spec.get("misread", ""),
                included_in_planning=included,
                canonical_table_entry_planned=True,
                canonical_table_generated_now=False,
                verifier_usage_planned=True,
                planning_status="pass" if included else "fail",
            )
        )
    return rows, all_pass and len(rows) == 24


def _build_entry_plan() -> List[Dict[str, Any]]:
    return [
        _row(
            term=term,
            canonical_meaning_planned=True,
            forbidden_interpretation_planned=True,
            required_fields_planned=True,
            valid_contexts_planned=True,
            invalid_contexts_planned=True,
            must_not_imply_planned=True,
            required_non_claims_planned=True,
            verifier_usage_planned=True,
            example_safe_usage_planned=True,
            example_unsafe_usage_planned=True,
            canonical_entry_generated_now=False,
            enforced_now=False,
        )
        for term in REQUIRED_TERMS
    ]


def _build_misread_matrix() -> List[Dict[str, Any]]:
    rows = []
    for term in REQUIRED_TERMS:
        spec = TERM_SPECS[term]
        risk = spec["risk"]
        rows.append(
            _row(
                term=term,
                misread_risk=spec["misread"],
                misread_example=f"{term} used in wrong phase context",
                risk_level=risk,
                affected_phase_types=spec["phases"],
                affected_fields=spec["fields"],
                potential_failure_mode="NO_GO or false authorization",
                blocks_canonicalization_execution=risk == "high",
                blocks_success_claim_gate=term in ("success", "success claim", "GO", "evidence"),
                blocks_owner_operator_approval=term
                in ("owner approval", "operator acknowledgement", "authorization granted"),
                recommended_priority="P0" if risk == "high" else "P1",
            )
        )
    return rows


def _build_required_fields_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            term=term,
            required_boolean_fields=TERM_SPECS[term]["fields"],
            required_status_fields="phase,final_decision,boundary_ok",
            required_source_refs="governance_constraints_ref,source_chain",
            required_actor_refs="owner_identity,operator_identity" if "approval" in term or "acknowledgement" in term else "n/a",
            required_evidence_refs="approval_evidence,commit_evidence" if term in ("authorization granted", "committed", "evidence") else "n/a",
            required_non_claims=f"{term} must not be misread across phase boundaries",
            missing_field_risk="field omission causes verifier false pass",
            verifier_required=True,
        )
        for term in REQUIRED_TERMS
    ]


def _build_verifier_usage_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            term=term,
            verifier_check_name=TERM_SPECS[term]["verifier"],
            target_phase_types=TERM_SPECS[term]["phases"],
            required_fields=TERM_SPECS[term]["fields"],
            failure_condition=f"{term} misused in summary or readiness",
            severity="P0" if TERM_SPECS[term]["risk"] == "high" else "P1",
            non_claim_required=True,
            used_by_future_verifier=True,
            verifier_modified_now=False,
        )
        for term in REQUIRED_TERMS
    ]


def _build_forbidden_interpretation_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            term=term,
            forbidden_interpretation=TERM_SPECS[term]["forbidden"],
            forbidden_reason=TERM_SPECS[term]["misread"],
            forbidden_field_combination=f"{term} without required flags",
            required_non_claim_if_used=f"{term} GO does not imply downstream execution",
            failure_condition="forbidden interpretation detected",
            severity="P0" if TERM_SPECS[term]["risk"] == "high" else "P1",
            enforced_now=False,
        )
        for term in REQUIRED_TERMS
    ]


def _build_success_claim_dependency_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            success_claim_topic=topic,
            dependent_terms=terms,
            terminology_table_required_before_success_claim_gate=True,
            blocks_success_claim_gate_planning_until_reviewed=True,
            required_future_phase="Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001",
            success_claim_canonicalization_executed_now=False,
        )
        for topic, terms in SUCCESS_CLAIM_TOPICS
    ]


def _build_output_plan() -> List[Dict[str, Any]]:
    return [
        _row(
            planned_artifact=artifact,
            purpose=purpose,
            required=required,
            used_by_future_verifier=v,
            used_by_success_claim_gate=sc,
            used_by_permission_semantics_canonicalization=ps,
            not_generated_now=True,
        )
        for artifact, purpose, required, v, sc, ps in OUTPUT_PLAN_ARTIFACTS
    ]


def run_terminology_canonical_table_planning_v1(
    *,
    permission_semantics_canonicalization_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(permission_semantics_canonicalization_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    routes = upstream["routes"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream roadmap verifier not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok not true")
    if up_summary.get("selected_route") != SELECTED_ROUTE:
        blockers.append("Route B not selected")
    if up_readiness.get("ready_for_terminology_canonical_table_planning") is not True:
        blockers.append("not ready_for_terminology_canonical_table_planning")
    if up_summary.get("terminology_canonicalization_executed_now") is not False:
        blockers.append("terminology_canonicalization_executed_now not false")
    if up_summary.get("registry_written_now") is not False:
        blockers.append("registry_written_now not false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    route_g = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "G"), {})
    if route_g.get("blocked_now") is not True:
        blockers.append("Route G not blocked")

    scope_rows, scope_pass = _build_scope_intake(upstream["artifacts"])
    entry_rows = _build_entry_plan()
    misread_rows = _build_misread_matrix()
    fields_rows = _build_required_fields_matrix()
    verifier_rows = _build_verifier_usage_matrix()
    forbidden_rows = _build_forbidden_interpretation_matrix()
    success_rows = _build_success_claim_dependency_matrix()
    output_rows = _build_output_plan()

    high_ok = all(
        next(r for r in misread_rows if r["term"] == t)["risk_level"] == "high" for t in HIGH_RISK_LEVEL_TERMS
    )
    if not high_ok:
        blockers.append("high-risk level terms not all high")

    planning_pass = (
        scope_pass
        and len(entry_rows) == 24
        and len(misread_rows) == 24
        and len(success_rows) >= 12
        and len(output_rows) >= 8
        and high_ok
        and not blockers
    )
    boundary_ok = planning_pass

    terminology_canonical_table_planning_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        source_success_claim_dependency_observed=SUCCESS_CLAIM_DEP,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    terminology_scope_intake_matrix = {"rows": scope_rows, "row_count": len(scope_rows), "all_pass": scope_pass, **_planning_meta()}
    terminology_canonical_entry_plan = {"rows": entry_rows, "row_count": len(entry_rows), **_planning_meta()}
    terminology_high_risk_misread_matrix = {"rows": misread_rows, "row_count": len(misread_rows), **_planning_meta()}
    terminology_required_fields_planning_matrix = {"rows": fields_rows, "row_count": len(fields_rows), **_planning_meta()}
    terminology_verifier_usage_planning_matrix = {"rows": verifier_rows, "row_count": len(verifier_rows), **_planning_meta()}
    terminology_forbidden_interpretation_planning_matrix = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        **_planning_meta(),
    }
    terminology_success_claim_dependency_matrix = {
        "rows": success_rows,
        "row_count": len(success_rows),
        **_planning_meta(),
    }
    terminology_table_output_plan = {"rows": output_rows, "row_count": len(output_rows), **_planning_meta()}

    terminology_canonical_table_planning_readiness_decision = {
        "ready_for_terminology_canonical_table_dryrun": boundary_ok,
        "ready_for_terminology_canonicalization_execution": False,
        "ready_for_terminology_enforcement": False,
        "ready_for_success_claim_gate_planning": False,
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
        "terminology_planning_completed": boundary_ok,
        "terminology_scope_intake_completed": scope_pass,
        "terminology_canonical_entry_plan_generated": len(entry_rows) == 24,
        "terminology_high_risk_misread_matrix_generated": len(misread_rows) == 24,
        "terminology_required_fields_planning_matrix_generated": len(fields_rows) == 24,
        "terminology_verifier_usage_planning_matrix_generated": len(verifier_rows) == 24,
        "terminology_forbidden_interpretation_planning_matrix_generated": len(forbidden_rows) == 24,
        "terminology_success_claim_dependency_matrix_generated": len(success_rows) >= 12,
        "terminology_table_output_plan_generated": len(output_rows) >= 8,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "permission_semantics_canonicalization_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route": SELECTED_ROUTE,
        "source_success_claim_dependency": SUCCESS_CLAIM_DEP,
        "term_count": len(scope_rows),
        "success_claim_topic_count": len(success_rows),
        "output_plan_artifact_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "permission_semantics_canonicalization_roadmap_decision",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_planning_meta(),
            }
        ],
        "row_count": 1,
        **_planning_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_PLANNING_REQUIRES_FIXES",
        "reason": "terminology table planning blueprint only; dry-run next; not formal table",
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "terminology_canonical_table_planning_policy": terminology_canonical_table_planning_policy,
        "terminology_scope_intake_matrix": terminology_scope_intake_matrix,
        "terminology_canonical_entry_plan": terminology_canonical_entry_plan,
        "terminology_high_risk_misread_matrix": terminology_high_risk_misread_matrix,
        "terminology_required_fields_planning_matrix": terminology_required_fields_planning_matrix,
        "terminology_verifier_usage_planning_matrix": terminology_verifier_usage_planning_matrix,
        "terminology_forbidden_interpretation_planning_matrix": terminology_forbidden_interpretation_planning_matrix,
        "terminology_success_claim_dependency_matrix": terminology_success_claim_dependency_matrix,
        "terminology_table_output_plan": terminology_table_output_plan,
        "terminology_canonical_table_planning_readiness_decision": terminology_canonical_table_planning_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
