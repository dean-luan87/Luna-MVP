# -*- coding: utf-8 -*-
"""Evidence Chain Governance Planning v1.

Planning only: define evidence lifecycle, source chain, usage scope, upgrade paths,
acceptance policy, non-substitution, success claim eligibility, verifier usage.
Does not generate evidence, registry, or allow success claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Evidence-Chain-Governance-Planning-v1-001"
PLANNING_SCOPE = "evidence_chain_governance_planning_only"
SOURCE_CHAIN = "evidence_chain_governance_planning_v1"

SOURCE_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Roadmap-Decision-v1-001"
SELECTED_ROUTE = "Route A — Evidence Chain Governance Planning"
FINAL_DECISION = "EVIDENCE_CHAIN_GOVERNANCE_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Evidence-Chain-Governance-DryRun-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "success_claim_gate_roadmap_decision_policy_v1.json",
    "completed_success_claim_gate_chain_review_v1.json",
    "success_claim_gate_roadmap_route_candidate_matrix_v1.json",
    "success_claim_to_evidence_chain_dependency_matrix_v1.json",
    "evidence_chain_governance_planning_scope_v1.json",
    "success_claim_gate_roadmap_non_release_matrix_v1.json",
    "evidence_chain_entry_readiness_risk_matrix_v1.json",
    "success_claim_gate_roadmap_decision_non_claims_register_v1.json",
    "success_claim_gate_roadmap_readiness_decision_v1.json",
)

EVIDENCE_TYPE_LIFECYCLE: Tuple[Tuple[str, str, str, str, str, bool, bool], ...] = (
    ("evidence_candidate", "pre-acceptance candidate tier", "phase runner", "planning/dryrun/review", "pre-acceptance only", "success_evidence", False, False),
    ("runtime_evidence", "runtime-captured execution artifacts", "runtime + recorder", "real execution observed", "runtime chain only", "verifier_report", True, False),
    ("audit_evidence", "phase audit / review artifacts", "reviewer", "post-phase review", "audit support", "success_evidence", False, False),
    ("success_evidence", "gated bundle for success claim", "evidence gate", "all prerequisites met", "success claim only", "summary", True, False),
    ("verifier_report", "verifier JSON output", "verifier runner", "phase verify", "verifier consumption", "runtime_evidence", False, False),
    ("summary", "phase summary.json", "phase runner", "phase complete", "human-readable summary", "success_evidence", False, False),
    ("boundary_matrix", "boundary violation matrix", "phase capability", "boundary check", "boundary audit", "boundary_clearance_evidence", False, False),
    ("non_claims_register", "explicit non-claims list", "phase capability", "phase complete", "non-claims only", "evidence", False, False),
    ("readiness_decision", "readiness decision artifact", "phase capability", "readiness gate", "readiness routing", "authorization_evidence", False, False),
    ("post_review_report", "post-execution review output", "review authority", "post-execution review", "review audit", "success_evidence", False, False),
    ("execution_log", "execution log when real run", "runtime", "execution committed", "runtime support", "summary", True, False),
    ("source_chain", "provenance references", "all evidence producers", "evidence creation", "provenance component", "success_evidence alone", True, False),
    ("rollback_result_evidence", "rollback rehearsal outcome", "rehearsal chain", "rehearsal complete", "rehearsal result", "success_evidence shortcut", True, False),
    ("migration_result_evidence", "migration outcome", "migration chain", "migration complete", "migration result", "success_evidence shortcut", True, False),
)

SOURCE_CHAIN_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("source origin", "where evidence was produced"),
    ("source phase", "governance phase id"),
    ("source artifact", "artifact path or id"),
    ("source actor", "human or system actor"),
    ("source timestamp", "iso8601 capture time"),
    ("source operation", "operation type"),
    ("source runtime context", "runtime invocation context"),
    ("source verifier context", "verifier id and version"),
    ("source authorization context", "authorization refs"),
    ("source boundary context", "boundary flags at capture"),
    ("source quality", "quality tier / integrity"),
    ("source integrity", "hash or signature ref"),
    ("source review status", "review state"),
    ("source retention policy", "retention class"),
)

USAGE_SCOPES: Tuple[Tuple[str, List[str], List[str]], ...] = (
    ("planning_support", ["evidence_candidate", "audit_evidence"], ["success_evidence"]),
    ("dryrun_support", ["evidence_candidate", "audit_evidence"], ["success_evidence"]),
    ("review_support", ["audit_evidence", "post_review_report"], ["success_evidence"]),
    ("roadmap_decision_support", ["audit_evidence", "readiness_decision"], ["success_evidence"]),
    ("audit_support", ["audit_evidence", "verifier_report", "summary"], ["success_evidence"]),
    ("runtime_support", ["runtime_evidence", "execution_log"], ["verifier_report", "summary"]),
    ("success_claim_support", ["success_evidence"], ["verifier_report", "summary", "source_chain"]),
    ("rollback_rehearsal_support", ["runtime_evidence", "rollback_result_evidence"], ["success_evidence without upgrade"]),
    ("migration_support", ["runtime_evidence", "migration_result_evidence"], ["success_evidence without upgrade"]),
    ("owner_operator_review_support", ["audit_evidence", "authorization_evidence"], ["success_evidence"]),
    ("boundary_clearance_support", ["boundary_matrix", "audit_evidence"], ["success_evidence"]),
    ("verifier_rerun_support", ["verifier_report", "runtime_evidence"], ["summary as success evidence"]),
)

UPGRADE_PATHS: Tuple[Tuple[str, str, str, str], ...] = (
    ("candidate_to_review_evidence", "evidence_candidate", "audit_evidence", "review completed"),
    ("review_evidence_to_audit_evidence", "audit_evidence", "audit_evidence", "audit sign-off"),
    ("runtime_log_to_runtime_evidence", "execution_log", "runtime_evidence", "runtime_invoked and source chain"),
    ("runtime_evidence_to_success_evidence", "runtime_evidence", "success_evidence", "authorization + post-review"),
    ("verifier_report_to_audit_support_only", "verifier_report", "audit_evidence", "never upgrade to runtime/success"),
    ("summary_to_audit_support_only", "summary", "audit_evidence", "never upgrade to success evidence"),
    ("source_chain_to_evidence_component_only", "source_chain", "source_chain", "component only; not success alone"),
    ("post_review_report_to_audit_evidence", "post_review_report", "audit_evidence", "review authority"),
    ("rollback_result_to_success_evidence", "rollback_result_evidence", "success_evidence", "full eligibility chain"),
    ("migration_result_to_success_evidence", "migration_result_evidence", "success_evidence", "full eligibility chain"),
)

ACCEPTANCE_RULES: Tuple[Tuple[str, str, str, str], ...] = (
    ("accept_candidate_evidence", "evidence_candidate", "review pass + source chain", "used as success evidence"),
    ("accept_runtime_evidence", "runtime_evidence", "runtime_invoked + source chain", "verifier_report only"),
    ("accept_audit_evidence", "audit_evidence", "review authority", "success claim without upgrade"),
    ("accept_success_evidence", "success_evidence", "full eligibility matrix", "partial prerequisites"),
    ("reject_summary_as_success_evidence", "summary", "never", "always as success evidence"),
    ("reject_verifier_report_as_runtime_evidence", "verifier_report", "never", "as runtime evidence"),
    ("reject_candidate_as_success_evidence", "evidence_candidate", "never", "direct to success evidence"),
    ("reject_source_chain_alone_as_success_evidence", "source_chain", "never alone", "as sole success evidence"),
    ("accept_post_execution_review_evidence", "post_review_report", "review completed", "as success evidence alone"),
    ("accept_authorization_evidence", "authorization_evidence", "authorization granted", "substitute for runtime"),
    ("accept_boundary_clearance_evidence", "boundary_clearance_evidence", "boundary cleared", "substitute for audit"),
    ("accept_rollback_result_evidence", "rollback_result_evidence", "rehearsal complete + chain", "without runtime"),
)

NON_SUBSTITUTION: Tuple[Tuple[str, str, str, str], ...] = (
    ("summary cannot substitute success_evidence", "success_evidence", "summary is not success evidence", "P0"),
    ("verifier_report cannot substitute runtime_evidence", "runtime_evidence", "verifier output ≠ runtime capture", "P0"),
    ("verifier_report cannot substitute success_evidence", "success_evidence", "verifier GO ≠ success claim", "P0"),
    ("candidate_evidence cannot substitute success_evidence", "success_evidence", "candidate tier blocked", "P0"),
    ("source_chain cannot substitute success_evidence", "success_evidence", "provenance alone insufficient", "P0"),
    ("boundary_matrix cannot substitute boundary_clearance_evidence", "boundary_clearance_evidence", "matrix pass ≠ clearance", "P0"),
    ("non_claims_register cannot substitute evidence", "evidence", "non-claims are not evidence", "P1"),
    ("readiness_decision cannot substitute authorization_evidence", "authorization_evidence", "readiness ≠ approval", "P0"),
    ("post_review_report cannot substitute real_execution_evidence", "runtime_evidence", "review ≠ execution", "P0"),
    ("audit_evidence cannot substitute success_evidence without upgrade", "success_evidence", "audit requires upgrade path", "P0"),
)

ELIGIBILITY_CONDITIONS: Tuple[Tuple[str, List[str], str], ...] = (
    ("real_execution_observed", ["runtime_evidence", "execution_log"], "execution_committed"),
    ("runtime_evidence_generated", ["runtime_evidence"], "runtime_invoked"),
    ("success_evidence_generated", ["success_evidence"], "upgrade path complete"),
    ("evidence_source_chain_valid", ["source_chain"], "all evidence refs linked"),
    ("evidence_accepted", ["success_evidence"], "acceptance policy pass"),
    ("evidence_usage_scope_success_claim", ["success_evidence"], "usage_scope=success_claim_support"),
    ("post_execution_review_completed", ["post_review_report"], "review authority sign-off"),
    ("authorization_granted", ["authorization_evidence"], "authorization_granted_now"),
    ("owner_operator_approval_valid", ["owner_operator_approval_evidence"], "owner + operator ack"),
    ("execution_window_valid", ["execution_window_evidence"], "window open during execution"),
    ("boundary_violation_absent", ["boundary_clearance_evidence"], "boundary_matrix pass + clearance"),
    ("rollback_or_migration_result_confirmed", ["rollback_result_evidence", "migration_result_evidence"], "result confirmed"),
)

VERIFIER_CHECKS: Tuple[Tuple[str, str, str, str, str], ...] = (
    ("E01", "evidence_candidate_not_success_evidence", "all", "evidence_type", "candidate used as success evidence", "P0"),
    ("E02", "verifier_report_not_runtime_evidence", "all", "verifier_report", "verifier report as runtime", "P0"),
    ("E03", "summary_not_success_evidence", "all", "summary", "summary as success evidence", "P0"),
    ("E04", "source_chain_not_success_alone", "all", "source_chain", "source chain alone for success", "P0"),
    ("E05", "success_evidence_requires_runtime_evidence", "execution,rehearsal,migration", "runtime_evidence_refs", "success without runtime", "P0"),
    ("E06", "success_evidence_requires_post_execution_review", "post-execution", "post_review_report", "success without review", "P0"),
    ("E07", "runtime_evidence_requires_runtime_invoked", "execution", "runtime_invoked", "runtime evidence without runtime", "P0"),
    ("E08", "evidence_acceptance_requires_source_chain", "all", "source_chain", "accepted without chain", "P0"),
    ("E09", "evidence_usage_scope_required", "all", "usage_scope", "wrong scope for evidence type", "P0"),
    ("E10", "evidence_upgrade_path_required", "all", "upgrade_path", "shortcut upgrade detected", "P0"),
    ("E11", "evidence_registry_required_before_generation", "generation", "evidence_registry", "generation before registry plan", "P0"),
    ("E12", "success_claim_requires_accepted_success_evidence", "success_claim", "success_evidence,accepted", "success claim without accepted evidence", "P0"),
)

NON_CLAIM_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("evidence candidate generated", "evidence candidate generated does not mean success evidence"),
    ("verifier report generated", "verifier report generated does not mean runtime evidence"),
    ("summary generated", "summary generated does not mean success evidence"),
    ("source chain present", "source chain present does not mean success claim allowed"),
    ("audit evidence", "audit evidence does not mean success evidence"),
    ("runtime evidence generated", "runtime evidence generated does not mean success claim allowed"),
    ("post-review report generated", "post-review report generated does not mean real execution succeeded"),
    ("boundary matrix pass", "boundary matrix pass does not mean boundary clearance evidence accepted"),
    ("evidence chain planning GO", "evidence chain planning GO does not mean evidence generated"),
    ("evidence chain dry-run GO", "evidence chain dry-run GO does not mean evidence accepted"),
    ("evidence registry candidate", "evidence registry candidate does not mean evidence registry generated"),
    ("evidence eligibility planned", "evidence eligibility planned does not mean eligibility satisfied"),
)

OUTPUT_PLAN_ARTIFACTS: Tuple[Tuple[str, str, bool, bool, bool], ...] = (
    ("evidence_chain_policy_v1.json", "evidence chain policy", True, True, True),
    ("evidence_type_lifecycle_matrix_v1.json", "evidence type lifecycle", True, True, True),
    ("evidence_source_chain_matrix_v1.json", "source chain rules", True, True, True),
    ("evidence_usage_scope_matrix_v1.json", "usage scope", True, True, True),
    ("evidence_upgrade_path_matrix_v1.json", "upgrade paths", True, True, True),
    ("evidence_acceptance_policy_matrix_v1.json", "acceptance policy", True, True, True),
    ("evidence_boundary_non_substitution_matrix_v1.json", "non-substitution", True, True, True),
    ("evidence_success_claim_eligibility_matrix_v1.json", "success claim eligibility", True, True, True),
    ("evidence_verifier_usage_matrix_v1.json", "verifier usage", True, False, True),
    ("evidence_chain_non_claims_rules_v1.json", "non-claims rules", True, True, False),
    ("evidence_chain_readiness_decision_v1.json", "readiness decision", True, True, True),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "evidence_chain_planning_only": True,
        "evidence_chain_canonicalization_executed_now": False,
        "evidence_registry_generated_now": False,
        "evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "success_claim_gate_generated_now": False,
        "success_claim_gate_enforced_now": False,
        "success_claim_allowed": False,
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
    readiness = _try_read_json(root / "success_claim_gate_roadmap_readiness_decision_v1.json") if root else None
    routes = _try_read_json(root / "success_claim_gate_roadmap_route_candidate_matrix_v1.json") if root else None
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


def _build_lifecycle_matrix() -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for etype, meaning, created_by, created_when, allowed, forbidden, can_support, gen_now in EVIDENCE_TYPE_LIFECYCLE:
        stand_alone = False if etype in (
            "evidence_candidate",
            "verifier_report",
            "summary",
            "audit_evidence",
            "boundary_matrix",
            "non_claims_register",
            "readiness_decision",
            "post_review_report",
        ) else etype != "source_chain"
        if etype == "source_chain":
            stand_alone = False
        rows.append(
            _row(
                evidence_type=etype,
                canonical_meaning=meaning,
                created_by=created_by,
                created_when=created_when,
                allowed_usage=allowed,
                forbidden_usage=forbidden,
                can_support_success_claim=can_support,
                can_support_success_claim_now=False,
                can_stand_alone_for_success_claim=stand_alone and can_support,
                required_upgrade_path="upgrade via gate" if not can_support else "runtime + authorization + post-review",
                source_chain_required=True,
                generation_allowed_now=False,
                accepted_now=False,
            )
        )
    return rows


def _build_source_chain_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            source_chain_component=comp,
            why_required=why,
            required_for_runtime_evidence=comp in ("source origin", "source phase", "source artifact", "source timestamp", "source runtime context"),
            required_for_success_evidence=True,
            required_for_audit_evidence=comp in ("source origin", "source phase", "source artifact", "source review status"),
            required_for_success_claim=True,
            can_stand_alone_for_success_claim=False,
            planned_verifier_check=f"verify_source_chain_{comp.replace(' ', '_')}",
            generated_now=False,
        )
        for comp, why in SOURCE_CHAIN_COMPONENTS
    ]


def _build_usage_scope_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            usage_scope=scope,
            allowed_evidence_types=allowed,
            forbidden_evidence_types=forbidden,
            required_preconditions="source_chain + phase boundary frozen",
            required_source_chain=True,
            required_authorization=scope in ("success_claim_support", "rollback_rehearsal_support", "migration_support"),
            allowed_now=False,
            planned_verifier_check=f"verify_usage_scope_{scope}",
        )
        for scope, allowed, forbidden in USAGE_SCOPES
    ]


def _build_upgrade_path_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            upgrade_path=path,
            from_type=from_t,
            to_type=to_t,
            required_preconditions=pre,
            required_authorization="authorization_granted" if to_t == "success_evidence" else "n/a",
            required_review="post_execution_review" if to_t == "success_evidence" else "phase_review",
            allowed_now=False,
            forbidden_shortcut=f"direct {from_t} to {to_t} without preconditions",
            planned_verifier_check=f"verify_upgrade_{path}",
        )
        for path, from_t, to_t, pre in UPGRADE_PATHS
    ]


def _build_acceptance_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            acceptance_rule=rule,
            target_evidence_type=target,
            accepted_when=accepted,
            rejected_when=rejected,
            required_source_chain=True,
            required_review="review authority" in rule or "review" in accepted,
            required_authorization="authorization" in rule,
            accepted_now=False,
            planned_verifier_check=f"verify_acceptance_{rule}",
        )
        for rule, target, accepted, rejected in ACCEPTANCE_RULES
    ]


def _build_non_substitution_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            non_substitution_rule=rule,
            forbidden_substitution=forbidden,
            why_forbidden=why,
            required_non_claim=rule,
            severity=sev,
            planned_verifier_check=f"verify_non_sub_{forbidden.replace(' ', '_')}",
            enforced_now=False,
        )
        for rule, forbidden, why, sev in NON_SUBSTITUTION
    ]


def _build_eligibility_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            eligibility_condition=cond,
            required_for_success_claim=True,
            required_evidence_types=types,
            required_authorization=auth,
            required_review="post_execution_review" in cond or "review" in cond,
            satisfied_now=False,
            success_claim_allowed_now=False,
            planned_gate_link=f"success_claim_gate_{cond}",
        )
        for cond, types, auth in ELIGIBILITY_CONDITIONS
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


def _build_non_claims_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            scenario=scenario,
            required_non_claim=non_claim,
            risk_if_missing="evidence misread enables false success claim",
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            planned_now=True,
            generated_now=False,
        )
        for scenario, non_claim in NON_CLAIM_SCENARIOS
    ]


def _build_output_plan() -> List[Dict[str, Any]]:
    return [
        _row(
            planned_artifact=artifact,
            purpose=purpose,
            required=required,
            used_by_future_verifier=v,
            used_by_success_claim_gate=True,
            used_by_real_rehearsal_chain=reh,
            used_by_migration_chain=reh,
            not_generated_now=True,
        )
        for artifact, purpose, required, v, reh in OUTPUT_PLAN_ARTIFACTS
    ]


def run_evidence_chain_governance_planning_v1(
    *,
    success_claim_gate_canonicalization_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(success_claim_gate_canonicalization_roadmap_decision_root)
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
        blockers.append("Route A not selected")
    if up_readiness.get("ready_for_evidence_chain_governance_planning") is not True:
        blockers.append("not ready_for_evidence_chain_governance_planning")
    if up_summary.get("success_claim_gate_generated_now") is not False:
        blockers.append("success_claim_gate_generated_now must be false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("success_claim_allowed must be false")
    if up_summary.get("success_evidence_generated_now") is not False:
        blockers.append("success_evidence_generated_now must be false")
    if up_summary.get("runtime_evidence_generated_now") is not False:
        blockers.append("runtime_evidence_generated_now must be false")
    if up_summary.get("evidence_chain_canonicalization_executed_now") is not False:
        blockers.append("evidence_chain_canonicalization_executed_now must be false")
    if up_summary.get("evidence_registry_generated_now") is not False:
        blockers.append("evidence_registry_generated_now must be false")
    for flag in (
        "ready_for_evidence_generation",
        "ready_for_evidence_registry_generation",
        "ready_for_success_claim_gate_generation",
        "ready_for_success_claim_allowance",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})
    route_h = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "H"), {})
    if route_a.get("selected_now") is not True:
        blockers.append("Route A not selected_now in matrix")
    if route_h.get("blocked_now") is not True:
        blockers.append("Route H not blocked")

    lifecycle_rows = _build_lifecycle_matrix()
    source_chain_rows = _build_source_chain_matrix()
    usage_scope_rows = _build_usage_scope_matrix()
    upgrade_path_rows = _build_upgrade_path_matrix()
    acceptance_rows = _build_acceptance_matrix()
    non_sub_rows = _build_non_substitution_matrix()
    eligibility_rows = _build_eligibility_matrix()
    verifier_rows = _build_verifier_usage_matrix()
    non_claims_rows = _build_non_claims_matrix()
    output_rows = _build_output_plan()

    cand = next((r for r in lifecycle_rows if r.get("evidence_type") == "evidence_candidate"), {})
    vr = next((r for r in lifecycle_rows if r.get("evidence_type") == "verifier_report"), {})
    sm = next((r for r in lifecycle_rows if r.get("evidence_type") == "summary"), {})
    sc = next((r for r in lifecycle_rows if r.get("evidence_type") == "source_chain"), {})
    se = next((r for r in lifecycle_rows if r.get("evidence_type") == "success_evidence"), {})

    boundary_checks_ok = (
        cand.get("can_support_success_claim") is False
        and cand.get("can_support_success_claim_now") is False
        and vr.get("can_support_success_claim") is False
        and sm.get("can_support_success_claim") is False
        and sc.get("can_stand_alone_for_success_claim") is False
        and se.get("can_support_success_claim") is True
        and se.get("generation_allowed_now") is False
    )
    if not boundary_checks_ok:
        blockers.append("evidence lifecycle boundary invariants failed")

    planning_pass = (
        len(lifecycle_rows) >= 14
        and len(source_chain_rows) >= 14
        and len(usage_scope_rows) >= 12
        and len(upgrade_path_rows) >= 10
        and len(acceptance_rows) >= 12
        and len(non_sub_rows) >= 10
        and len(eligibility_rows) >= 12
        and len(verifier_rows) >= 12
        and len(non_claims_rows) >= 12
        and len(output_rows) >= 11
        and boundary_checks_ok
        and not blockers
    )
    boundary_ok = planning_pass

    evidence_chain_governance_planning_policy = _row(
        phase_name=PHASE_ID,
        evidence_chain_planning_only=True,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    evidence_type_lifecycle_planning_matrix = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        **_planning_meta(),
    }
    evidence_source_chain_planning_matrix = {
        "rows": source_chain_rows,
        "row_count": len(source_chain_rows),
        **_planning_meta(),
    }
    evidence_usage_scope_planning_matrix = {
        "rows": usage_scope_rows,
        "row_count": len(usage_scope_rows),
        **_planning_meta(),
    }
    evidence_upgrade_path_planning_matrix = {
        "rows": upgrade_path_rows,
        "row_count": len(upgrade_path_rows),
        **_planning_meta(),
    }
    evidence_acceptance_policy_planning_matrix = {
        "rows": acceptance_rows,
        "row_count": len(acceptance_rows),
        **_planning_meta(),
    }
    evidence_boundary_non_substitution_matrix = {
        "rows": non_sub_rows,
        "row_count": len(non_sub_rows),
        **_planning_meta(),
    }
    evidence_to_success_claim_eligibility_planning_matrix = {
        "rows": eligibility_rows,
        "row_count": len(eligibility_rows),
        **_planning_meta(),
    }
    evidence_verifier_usage_planning_matrix = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        **_planning_meta(),
    }
    evidence_chain_non_claims_planning_matrix = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        **_planning_meta(),
    }
    evidence_chain_output_plan = {
        "rows": output_rows,
        "row_count": len(output_rows),
        **_planning_meta(),
    }

    evidence_chain_governance_planning_readiness_decision = {
        "ready_for_evidence_chain_governance_dryrun": boundary_ok,
        "ready_for_evidence_chain_canonicalization_execution": False,
        "ready_for_evidence_registry_generation": False,
        "ready_for_evidence_generation": False,
        "ready_for_runtime_evidence_generation": False,
        "ready_for_success_evidence_generation": False,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_owner_operator_approval_workflow": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "evidence_chain_planning_completed": boundary_ok,
        "evidence_type_lifecycle_planned": True,
        "source_chain_planned": True,
        "usage_scope_planned": True,
        "upgrade_path_planned": True,
        "acceptance_policy_planned": True,
        "non_substitution_planned": True,
        "success_claim_eligibility_planned": True,
        "verifier_usage_planned": True,
        "non_claims_planned": True,
        "output_plan_generated": True,
        "evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "success_claim_gate_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
        "lifecycle_type_count": len(lifecycle_rows),
        "source_chain_component_count": len(source_chain_rows),
        "usage_scope_count": len(usage_scope_rows),
        "upgrade_path_count": len(upgrade_path_rows),
        "acceptance_rule_count": len(acceptance_rows),
        "non_substitution_count": len(non_sub_rows),
        "eligibility_count": len(eligibility_rows),
        "verifier_check_count": len(verifier_rows),
        "non_claims_count": len(non_claims_rows),
        "output_plan_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "success_claim_gate_canonicalization_roadmap_decision",
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
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_PLANNING_REQUIRES_FIXES",
        "reason": "evidence chain planning complete; no evidence generated; dry-run next",
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "evidence_chain_governance_planning_policy": evidence_chain_governance_planning_policy,
        "evidence_type_lifecycle_planning_matrix": evidence_type_lifecycle_planning_matrix,
        "evidence_source_chain_planning_matrix": evidence_source_chain_planning_matrix,
        "evidence_usage_scope_planning_matrix": evidence_usage_scope_planning_matrix,
        "evidence_upgrade_path_planning_matrix": evidence_upgrade_path_planning_matrix,
        "evidence_acceptance_policy_planning_matrix": evidence_acceptance_policy_planning_matrix,
        "evidence_boundary_non_substitution_matrix": evidence_boundary_non_substitution_matrix,
        "evidence_to_success_claim_eligibility_planning_matrix": evidence_to_success_claim_eligibility_planning_matrix,
        "evidence_verifier_usage_planning_matrix": evidence_verifier_usage_planning_matrix,
        "evidence_chain_non_claims_planning_matrix": evidence_chain_non_claims_planning_matrix,
        "evidence_chain_output_plan": evidence_chain_output_plan,
        "evidence_chain_governance_planning_readiness_decision": evidence_chain_governance_planning_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
