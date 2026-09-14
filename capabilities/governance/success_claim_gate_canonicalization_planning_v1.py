# -*- coding: utf-8 -*-
"""Success Claim Gate Canonicalization Planning v1.

Planning only: define success claim gate blueprint (conditions, evidence, forbidden
interpretations, non-claims, verifier usage). Does not generate gate, enforce gate,
or allow success claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001"
PLANNING_SCOPE = "success_claim_gate_planning_only"
SOURCE_CHAIN = "success_claim_gate_canonicalization_planning_v1"

SOURCE_PHASE = "Phase-Terminology-Canonical-Table-Roadmap-Decision-v1-001"
SELECTED_ROUTE = "Route C — Success Claim Gate Canonicalization Planning"
FINAL_DECISION = "SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "terminology_canonical_table_roadmap_decision_policy_v1.json",
    "completed_terminology_chain_review_v1.json",
    "terminology_roadmap_route_candidate_matrix_v1.json",
    "terminology_to_success_claim_dependency_status_matrix_v1.json",
    "success_claim_gate_planning_scope_v1.json",
    "terminology_roadmap_non_release_matrix_v1.json",
    "terminology_roadmap_decision_non_claims_register_v1.json",
    "success_claim_gate_entry_readiness_risk_matrix_v1.json",
    "terminology_canonical_table_roadmap_readiness_decision_v1.json",
)

GATE_CONDITIONS: Tuple[Tuple[str, str, str, str], ...] = (
    ("C01", "real execution observed", "success claim requires observed real execution", "real_execution_observed"),
    ("C02", "execution completed and not aborted", "aborted runs cannot success-claim", "execution_completed_not_aborted"),
    ("C03", "required verifier rerun executed", "post-execution verifier suite must rerun", "verifier_rerun_executed"),
    ("C04", "verifier rerun result accepted", "rerun GO is not sufficient without acceptance record", "verifier_rerun_accepted"),
    ("C05", "runtime evidence generated", "runtime evidence distinct from audit artifacts", "runtime_evidence_generated"),
    ("C06", "success evidence generated", "success evidence with source chain", "success_evidence_generated"),
    ("C07", "evidence source chain valid", "candidate evidence cannot substitute", "evidence_source_chain_valid"),
    ("C08", "authorization granted", "authorization chain must be explicit", "authorization_granted"),
    ("C09", "owner/operator approval valid", "owner and operator gates separate", "owner_operator_approval_valid"),
    ("C10", "execution window valid", "window scope and timing must match execution", "execution_window_valid"),
    ("C11", "boundary violation absent", "protected/HR/DnAE boundaries clear", "boundary_violation_absent"),
    ("C12", "post-execution review completed", "post-execution review before success claim", "post_execution_review_completed"),
)

FORBIDDEN_INTERPRETATIONS: Tuple[Tuple[str, str, str, List[str], str], ...] = (
    ("F01", "GO must not imply success", "phase pass ≠ migration/rehearsal success", ["GO", "success"], "GO GO does not mean success claim allowed"),
    ("F02", "completed must not imply succeeded", "completion ≠ success claim", ["completed", "success"], "completed does not mean succeeded"),
    ("F03", "reviewed must not imply accepted", "audit ≠ acceptance", ["review", "post-review"], "reviewed does not mean accepted for success"),
    ("F04", "boundary_ok must not imply execution safe", "boundary_ok ≠ execution safe", ["boundary_ok", "GO"], "boundary_ok does not mean execution safe"),
    ("F05", "verifier_report must not imply runtime evidence", "verifier output ≠ runtime capture", ["verifier_report", "evidence"], "verifier_report is not runtime evidence"),
    ("F06", "summary must not imply success evidence", "summary text ≠ success evidence", ["summary", "success claim"], "summary is not success evidence"),
    ("F07", "candidate evidence must not imply success evidence", "candidate tier cannot upgrade implicitly", ["evidence", "generated"], "candidate evidence is not success evidence"),
    ("F08", "dry-run GO must not imply real execution success", "simulation ≠ real execution", ["dry-run", "GO"], "dry-run GO does not mean real execution success"),
    ("F09", "roadmap decision GO must not imply execution permission", "route selection ≠ permission release", ["roadmap decision", "GO"], "roadmap GO does not release execution"),
    ("F10", "selected route must not imply permission release", "Route C ≠ batch arming / migration", ["selected route", "ready"], "selected route does not imply permission release"),
    ("F11", "ready_for_next_phase must not imply ready_for_execution", "readiness for planning ≠ execution", ["ready", "ready_for_next_phase"], "ready_for_next_phase ≠ ready_for_execution"),
    ("F12", "no violation observed must not imply success", "absence of violation ≠ success", ["boundary_ok", "violations"], "no violation observed does not imply success"),
    ("F13", "evidence candidate generated must not imply evidence accepted", "generation ≠ acceptance", ["generated", "evidence"], "evidence candidate generated ≠ accepted"),
    ("F14", "post-review GO must not imply success claim allowed", "post-review pass ≠ success claim", ["post-review", "GO"], "post-review GO does not allow success claim"),
)

EVIDENCE_TYPES: Tuple[Tuple[str, str, bool, bool, bool], ...] = (
    ("real_execution_evidence", "observed real execution", True, True, True),
    ("runtime_evidence", "runtime-captured artifacts", True, True, False),
    ("success_evidence", "gated success claim evidence bundle", True, False, True),
    ("verifier_rerun_evidence", "post-execution verifier rerun record", True, False, False),
    ("authorization_evidence", "authorization granted chain", True, False, False),
    ("owner_operator_approval_evidence", "owner + operator approval records", True, False, False),
    ("execution_window_evidence", "window open/close with scope", True, False, False),
    ("boundary_clearance_evidence", "protected/HR/DnAE clearance", True, False, False),
    ("post_execution_review_evidence", "post-execution review sign-off", True, False, False),
    ("rollback_rehearsal_result_evidence", "rehearsal outcome when applicable", True, True, False),
    ("migration_result_evidence", "migration outcome when applicable", True, True, False),
    ("evidence_source_chain", "provenance chain for all evidence tiers", True, False, True),
)

EVIDENCE_BOUNDARY_TYPES: Tuple[Tuple[str, str, bool, str, str], ...] = (
    ("runtime evidence", "runtime-captured execution artifacts", True, "requires real execution + source chain", "verifier_report"),
    ("audit evidence", "phase audit / review artifacts", False, "audit pass ≠ success claim", "success evidence"),
    ("success evidence", "gated bundle for success claim only", True, "requires runtime + authorization + post-review", "summary"),
    ("candidate evidence", "pre-acceptance evidence tier", False, "candidate cannot support success claim", "success evidence"),
    ("verifier report", "verifier JSON output", False, "verifier report ≠ runtime evidence", "runtime evidence"),
    ("summary", "phase summary.json", False, "summary ≠ success evidence", "success evidence"),
    ("non-claims register", "explicit non-claims list", False, "non-claims are not evidence", "success evidence"),
    ("readiness decision", "readiness decision artifact", False, "readiness ≠ success claim allowed", "success claim"),
    ("boundary matrix", "boundary violation matrix", False, "boundary_ok alone insufficient", "execution safe"),
    ("execution log", "execution log when real run exists", True, "must link to source chain", "summary"),
    ("source chain", "provenance references", True, "required upgrade path for all evidence", "candidate evidence"),
    ("post-review report", "post-execution review output", False, "review pass ≠ success claim", "success claim"),
)

AUTH_DEPS: Tuple[Tuple[str, str, str], ...] = (
    ("authorization granted", "authorization_actor", "authorization_evidence_ref"),
    ("owner approval granted", "owner_identity", "owner_approval_evidence"),
    ("operator acknowledgement granted", "operator_identity", "operator_ack_evidence"),
    ("execution window opened", "execution_window_scope", "window_open_timestamp"),
    ("abort authority confirmed", "abort_authority_actor", "abort_authority_record"),
    ("scope confirmation accepted", "scope_confirmation_actor", "scope_confirmation_evidence"),
    ("protected boundary acknowledged", "protected_boundary_ack_actor", "protected_boundary_ack"),
    ("HR / DnAE boundary acknowledged", "hr_dnae_ack_actor", "hr_dnae_boundary_ack"),
    ("post-execution review authority", "review_authority_actor", "post_execution_review_signoff"),
    ("success claim authority", "success_claim_authority_actor", "success_claim_authority_evidence"),
)

NON_CLAIM_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("planning GO", "Planning GO does not mean success claim gate is generated or success claim allowed"),
    ("dry-run GO", "DryRun GO does not mean real execution success or success claim allowed"),
    ("review GO", "Review GO does not mean success claim allowed"),
    ("roadmap decision GO", "Roadmap Decision GO does not mean execution permission or success claim allowed"),
    ("verifier GO", "Verifier GO does not mean success claim allowed"),
    ("boundary_ok", "boundary_ok does not mean execution safe or success claim allowed"),
    ("completed", "completed does not mean succeeded"),
    ("reviewed", "reviewed does not mean accepted for success claim"),
    ("selected route", "selected route does not imply permission release"),
    ("ready_for_next_phase", "ready_for_next_phase does not imply ready_for_execution"),
    ("evidence candidate generated", "evidence candidate generated does not mean evidence accepted"),
    ("verifier report generated", "verifier report generated does not mean runtime evidence exists"),
    ("summary generated", "summary generated does not mean success evidence exists"),
    ("no violation observed", "no violation observed does not imply success"),
    ("post-review pass", "post-review pass does not imply success claim allowed"),
)

VERIFIER_CHECKS: Tuple[Tuple[str, str, str, str, str], ...] = (
    ("V01", "success_claim_allowed_requires_real_execution_evidence", "execution,rehearsal,migration", "real_execution_observed", "missing real execution evidence", "P0"),
    ("V02", "success_claim_allowed_requires_success_evidence", "execution,rehearsal,migration", "success_evidence_refs", "missing success evidence", "P0"),
    ("V03", "success_claim_allowed_requires_authorization_granted", "execution,rehearsal,migration", "authorization_granted_now", "authorization not granted", "P0"),
    ("V04", "success_claim_allowed_requires_owner_operator_approval", "execution,rehearsal,migration", "owner_approval,operator_ack", "approval chain incomplete", "P0"),
    ("V05", "success_claim_allowed_requires_execution_window", "execution,rehearsal,migration", "execution_window_opened", "execution window invalid", "P0"),
    ("V06", "success_claim_allowed_requires_verifier_rerun", "post-execution", "verifier_rerun_executed", "verifier rerun missing", "P0"),
    ("V07", "success_claim_allowed_requires_post_execution_review", "post-execution", "post_execution_review_completed", "post-execution review missing", "P0"),
    ("V08", "GO_does_not_imply_success", "all", "final_decision,GO", "GO interpreted as success", "P0"),
    ("V09", "summary_does_not_imply_success_evidence", "all", "summary", "summary used as success evidence", "P0"),
    ("V10", "verifier_report_does_not_imply_runtime_evidence", "all", "verifier_report", "verifier report substituted for runtime", "P0"),
    ("V11", "candidate_evidence_does_not_imply_success_evidence", "all", "candidate_evidence", "candidate upgraded without gate", "P0"),
    ("V12", "boundary_ok_does_not_imply_execution_safe", "all", "boundary_ok", "boundary_ok misread as execution safe", "P0"),
    ("V13", "selected_route_does_not_imply_permission_release", "roadmap,planning", "selected_route", "route misread as permission release", "P0"),
    ("V14", "ready_for_next_phase_does_not_imply_ready_for_execution", "all", "ready_for_next_phase", "readiness misread as execution allowed", "P0"),
)

OUTPUT_PLAN_ARTIFACTS: Tuple[Tuple[str, str, bool, bool, bool], ...] = (
    ("success_claim_gate_policy_v1.json", "gate policy", True, True, True),
    ("success_claim_condition_matrix_v1.json", "gate conditions", True, True, True),
    ("success_claim_forbidden_interpretation_matrix_v1.json", "forbidden interpretations", True, True, False),
    ("success_claim_required_evidence_matrix_v1.json", "required evidence", True, True, True),
    ("success_claim_evidence_boundary_matrix_v1.json", "evidence boundaries", True, True, True),
    ("success_claim_authorization_dependency_matrix_v1.json", "authorization deps", True, True, True),
    ("success_claim_non_claims_rules_v1.json", "non-claims rules", True, True, False),
    ("success_claim_verifier_usage_matrix_v1.json", "verifier usage", True, False, True),
    ("success_claim_gate_readiness_decision_v1.json", "readiness decision", True, True, True),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "success_claim_gate_planning_only": True,
        "success_claim_canonicalization_executed_now": False,
        "success_claim_gate_generated_now": False,
        "success_claim_gate_enforced_now": False,
        "success_claim_allowed": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
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
        root / "terminology_canonical_table_roadmap_readiness_decision_v1.json"
    ) if root else None
    routes = _try_read_json(root / "terminology_roadmap_route_candidate_matrix_v1.json") if root else None
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


def _build_condition_scope() -> List[Dict[str, Any]]:
    return [
        _row(
            condition_id=cid,
            condition_name=name,
            why_required=why,
            required_before_success_claim=True,
            planned_gate_field=field,
            required_evidence_type="success_evidence" if "evidence" in field else "authorization_evidence",
            required_source_refs="source_chain,governance_constraints_ref",
            must_be_true_for_success_claim=True,
            planned_now=True,
            satisfied_now=False,
            success_claim_allowed_now=False,
            gate_generated_now=False,
        )
        for cid, name, why, field in GATE_CONDITIONS
    ]


def _build_forbidden_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            forbidden_id=fid,
            forbidden_interpretation=interp,
            forbidden_reason=reason,
            affected_terms=terms,
            required_non_claim=non_claim,
            failure_condition=f"forbidden: {interp}",
            severity="P0",
            planned_verifier_check=f"verify_forbidden_{fid.lower()}",
            enforced_now=False,
            gate_generated_now=False,
        )
        for fid, interp, reason, terms, non_claim in FORBIDDEN_INTERPRETATIONS
    ]


def _build_required_evidence_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            evidence_type=etype,
            why_required=why,
            required_for_success_claim=req,
            candidate_evidence_allowed=False,
            runtime_evidence_required=runtime_req,
            success_evidence_required=success_req,
            source_chain_required=True,
            accepted_now=False,
            generated_now=False,
            success_claim_allowed_now=False,
        )
        for etype, why, req, runtime_req, success_req in EVIDENCE_TYPES
    ]


def _build_evidence_boundary() -> List[Dict[str, Any]]:
    return [
        _row(
            artifact_or_evidence_type=atype,
            canonical_usage=usage,
            can_support_success_claim=can_support,
            cannot_support_success_claim_reason=reason if not can_support else "n/a",
            required_upgrade_path_if_any="real execution + source chain + post-review" if can_support else "upgrade via gate",
            forbidden_substitution=forbidden_sub,
            planned_verifier_check=f"verify_evidence_boundary_{atype.replace(' ', '_')}",
            enforced_now=False,
        )
        for atype, usage, can_support, reason, forbidden_sub in EVIDENCE_BOUNDARY_TYPES
    ]


def _build_authorization_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            authorization_dependency=dep,
            required_for_success_claim=True,
            required_actor=actor,
            required_evidence=evidence,
            required_timestamp="iso8601_required",
            satisfied_now=False,
            authorization_granted_now=False,
            success_claim_allowed_now=False,
            planned_verifier_check=f"verify_auth_dep_{dep.replace(' ', '_')}",
        )
        for dep, actor, evidence in AUTH_DEPS
    ]


def _build_non_claims_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            scenario=scenario,
            required_non_claim=non_claim,
            risk_if_missing="success claim misread from phase artifact",
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            must_be_in_phase_docs=True,
            planned_now=True,
            generated_now=False,
        )
        for scenario, non_claim in NON_CLAIM_SCENARIOS
    ]


def _build_verifier_usage_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            verifier_check_id=vid,
            check_name=name,
            target_phase_types=phases,
            required_fields=fields,
            failure_condition=fail,
            severity=sev,
            planned_now=True,
            verifier_modified_now=False,
            enforced_now=False,
        )
        for vid, name, phases, fields, fail, sev in VERIFIER_CHECKS
    ]


def _build_output_plan() -> List[Dict[str, Any]]:
    return [
        _row(
            planned_artifact=artifact,
            purpose=purpose,
            required=required,
            used_by_future_verifier=v,
            used_by_future_phase_template=False,
            used_by_real_rehearsal_chain=reh,
            not_generated_now=True,
        )
        for artifact, purpose, required, v, reh in OUTPUT_PLAN_ARTIFACTS
    ]


def run_success_claim_gate_canonicalization_planning_v1(
    *,
    terminology_canonical_table_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(terminology_canonical_table_roadmap_decision_root)
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
        blockers.append("Route C not selected")
    if up_readiness.get("ready_for_success_claim_gate_canonicalization_planning") is not True:
        blockers.append("not ready_for_success_claim_gate_canonicalization_planning")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("success_claim_allowed must be false")
    if up_summary.get("success_claim_gate_generated_now") is not False:
        blockers.append("success_claim_gate_generated_now must be false")
    if up_summary.get("success_claim_canonicalization_executed_now") is not False:
        blockers.append("success_claim_canonicalization_executed_now must be false")
    if up_readiness.get("ready_for_success_claim_gate_execution") is not False:
        blockers.append("ready_for_success_claim_gate_execution must remain false")
    if up_readiness.get("ready_for_success_claim_allowance") is not False:
        blockers.append("ready_for_success_claim_allowance must remain false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    route_g = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "G"), {})
    if route_g.get("blocked_now") is not True:
        blockers.append("Route G not blocked")

    condition_rows = _build_condition_scope()
    forbidden_rows = _build_forbidden_matrix()
    evidence_rows = _build_required_evidence_matrix()
    boundary_rows = _build_evidence_boundary()
    auth_rows = _build_authorization_matrix()
    non_claims_rows = _build_non_claims_matrix()
    verifier_rows = _build_verifier_usage_matrix()
    output_rows = _build_output_plan()

    vr_row = next((r for r in boundary_rows if r.get("artifact_or_evidence_type") == "verifier report"), {})
    summary_row = next((r for r in boundary_rows if r.get("artifact_or_evidence_type") == "summary"), {})
    candidate_row = next((r for r in boundary_rows if r.get("artifact_or_evidence_type") == "candidate evidence"), {})
    go_forbidden = next((r for r in forbidden_rows if r.get("forbidden_id") == "F01"), {})

    boundary_checks_ok = (
        vr_row.get("can_support_success_claim") is False
        and summary_row.get("can_support_success_claim") is False
        and candidate_row.get("can_support_success_claim") is False
        and evidence_rows[0].get("candidate_evidence_allowed") is False
    )
    if not boundary_checks_ok:
        blockers.append("evidence boundary invariants failed")

    planning_pass = (
        len(condition_rows) >= 12
        and len(forbidden_rows) >= 14
        and len(evidence_rows) >= 12
        and len(boundary_rows) >= 12
        and len(auth_rows) >= 10
        and len(non_claims_rows) >= 15
        and len(verifier_rows) >= 14
        and len(output_rows) >= 9
        and go_forbidden.get("forbidden_interpretation") == "GO must not imply success"
        and boundary_checks_ok
        and not blockers
    )
    boundary_ok = planning_pass

    success_claim_gate_canonicalization_planning_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    success_claim_gate_condition_scope = {
        "rows": condition_rows,
        "row_count": len(condition_rows),
        **_planning_meta(),
    }
    success_claim_forbidden_interpretation_matrix = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        **_planning_meta(),
    }
    success_claim_required_evidence_planning_matrix = {
        "rows": evidence_rows,
        "row_count": len(evidence_rows),
        **_planning_meta(),
    }
    success_claim_runtime_vs_audit_evidence_boundary = {
        "rows": boundary_rows,
        "row_count": len(boundary_rows),
        **_planning_meta(),
    }
    success_claim_authorization_dependency_matrix = {
        "rows": auth_rows,
        "row_count": len(auth_rows),
        **_planning_meta(),
    }
    success_claim_non_claims_planning_matrix = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        **_planning_meta(),
    }
    success_claim_verifier_usage_planning_matrix = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        **_planning_meta(),
    }
    success_claim_gate_output_plan = {
        "rows": output_rows,
        "row_count": len(output_rows),
        **_planning_meta(),
    }

    success_claim_gate_canonicalization_planning_readiness_decision = {
        "ready_for_success_claim_gate_canonicalization_dryrun": boundary_ok,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_gate_execution": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_success_claim_enforcement": False,
        "ready_for_verifier_modification": False,
        "ready_for_phase_template_modification": False,
        "ready_for_automation_implementation": False,
        "ready_for_documentation_auto_sync": False,
        "ready_for_debt_fix_execution": False,
        "ready_for_permission_semantics_canonicalization_execution": False,
        "ready_for_terminology_canonicalization_execution": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "success_claim_gate_planning_completed": boundary_ok,
        "condition_scope_generated": True,
        "forbidden_interpretation_matrix_generated": True,
        "required_evidence_planning_matrix_generated": True,
        "runtime_vs_audit_evidence_boundary_generated": True,
        "authorization_dependency_matrix_generated": True,
        "non_claims_planning_matrix_generated": True,
        "verifier_usage_planning_matrix_generated": True,
        "gate_output_plan_generated": True,
        "success_claim_gate_generated_now": False,
        "success_claim_allowed": False,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "terminology_canonical_table_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
        "condition_count": len(condition_rows),
        "forbidden_count": len(forbidden_rows),
        "evidence_type_count": len(evidence_rows),
        "boundary_type_count": len(boundary_rows),
        "authorization_dep_count": len(auth_rows),
        "non_claims_count": len(non_claims_rows),
        "verifier_check_count": len(verifier_rows),
        "output_plan_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "terminology_canonical_table_roadmap_decision",
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
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_PLANNING_REQUIRES_FIXES",
        "reason": "gate planning complete; gate not generated; success claim not allowed; dry-run next",
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "success_claim_gate_canonicalization_planning_policy": success_claim_gate_canonicalization_planning_policy,
        "success_claim_gate_condition_scope": success_claim_gate_condition_scope,
        "success_claim_forbidden_interpretation_matrix": success_claim_forbidden_interpretation_matrix,
        "success_claim_required_evidence_planning_matrix": success_claim_required_evidence_planning_matrix,
        "success_claim_runtime_vs_audit_evidence_boundary": success_claim_runtime_vs_audit_evidence_boundary,
        "success_claim_authorization_dependency_matrix": success_claim_authorization_dependency_matrix,
        "success_claim_non_claims_planning_matrix": success_claim_non_claims_planning_matrix,
        "success_claim_verifier_usage_planning_matrix": success_claim_verifier_usage_planning_matrix,
        "success_claim_gate_output_plan": success_claim_gate_output_plan,
        "success_claim_gate_canonicalization_planning_readiness_decision": success_claim_gate_canonicalization_planning_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
