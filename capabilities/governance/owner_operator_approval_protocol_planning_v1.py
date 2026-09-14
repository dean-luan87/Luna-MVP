# -*- coding: utf-8 -*-
"""Owner/Operator Approval Protocol Planning v1.

Planning only: define owner approval, operator acknowledgement, execution window,
abort authority, scope/boundary acknowledgement, authorization dependencies.
Does not send approval requests, grant authorization, or generate evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001"
PLANNING_SCOPE = "owner_operator_approval_protocol_planning_only"
SOURCE_CHAIN = "owner_operator_approval_protocol_planning_v1"

SOURCE_PHASE = "Phase-Evidence-Chain-Governance-Roadmap-Decision-v1-001"
SELECTED_ROUTE = "Route A — Owner/Operator Approval Protocol Planning"
UPSTREAM_REQUIRED_FINAL = (
    "EVIDENCE_CHAIN_GOVERNANCE_ROADMAP_DECISION_READY_FOR_OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING"
)
FINAL_DECISION = "OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Owner-Operator-Approval-Protocol-DryRun-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "evidence_chain_roadmap_decision_policy_v1.json",
    "completed_evidence_chain_review_v1.json",
    "evidence_chain_roadmap_route_candidate_matrix_v1.json",
    "evidence_to_authorization_dependency_matrix_v1.json",
    "owner_operator_approval_protocol_planning_scope_v1.json",
    "evidence_chain_roadmap_non_release_matrix_v1.json",
    "owner_operator_entry_readiness_risk_matrix_v1.json",
    "evidence_chain_roadmap_decision_non_claims_register_v1.json",
    "evidence_chain_roadmap_readiness_decision_v1.json",
)

OWNER_IDENTITY_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("owner identity source", "canonical owner identity binding"),
    ("owner role", "owner role definition"),
    ("owner authority scope", "scope owner may approve"),
    ("owner approval artifact", "artifact bundle for owner approval"),
    ("owner approval timestamp", "iso8601 approval time"),
    ("owner approval revocation rule", "revocation conditions"),
    ("owner approval expiry rule", "expiry policy"),
    ("owner delegation rule", "delegation constraints"),
    ("owner conflict rule", "conflict-of-interest handling"),
    ("owner audit trail", "immutable approval audit trail"),
)

OPERATOR_ACK_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("operator identity", "operator identity binding"),
    ("operator role", "operator role definition"),
    ("operator acknowledgement artifact", "acknowledgement artifact bundle"),
    ("operator acknowledgement timestamp", "iso8601 acknowledgement time"),
    ("operator scope acknowledgement", "execution scope acknowledged"),
    ("operator risk acknowledgement", "risk disclosure acknowledged"),
    ("operator rollback acknowledgement", "rollback plan acknowledged"),
    ("operator evidence responsibility acknowledgement", "evidence duties acknowledged"),
    ("operator abort acknowledgement", "abort authority acknowledged"),
    ("operator audit trail", "immutable operator audit trail"),
)

EXECUTION_WINDOW_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("window open authority", "who may open execution window"),
    ("window close authority", "who may close execution window"),
    ("start time", "window start timestamp"),
    ("end time", "window end timestamp"),
    ("allowed operations", "operations permitted in window"),
    ("forbidden operations", "operations forbidden in window"),
    ("rollback trigger condition", "conditions triggering rollback"),
    ("abort trigger condition", "conditions triggering abort"),
    ("evidence capture scope", "evidence types captured in window"),
    ("verifier rerun scope", "verifier rerun allowed scope"),
    ("protected boundary scope", "protected assets in scope"),
    ("post-window review requirement", "post-window review mandatory"),
)

ABORT_AUTHORITY_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("abort authority owner", "owner abort authority"),
    ("abort authority operator", "operator abort authority"),
    ("abort trigger by boundary violation", "boundary violation abort"),
    ("abort trigger by verifier failure", "verifier failure abort"),
    ("abort trigger by evidence anomaly", "evidence anomaly abort"),
    ("abort trigger by protected asset risk", "protected asset risk abort"),
    ("abort trigger by HR / DnAE risk", "HR/DnAE risk abort"),
    ("abort trigger by missing checkpoint", "missing checkpoint abort"),
    ("abort notification rule", "abort notification protocol"),
    ("abort evidence capture rule", "evidence on abort"),
    ("abort rollback rule", "rollback after abort"),
    ("abort post-review rule", "post-review after abort"),
)

SCOPE_BOUNDARY_COMPONENTS: Tuple[Tuple[str, str], ...] = (
    ("execution scope confirmation", "confirm execution scope"),
    ("evidence generation scope", "evidence generation boundary"),
    ("verifier rerun scope", "verifier rerun boundary"),
    ("file operation scope", "file operation boundary"),
    ("protected asset boundary", "protected assets"),
    ("HR boundary", "human review queue"),
    ("DnAE boundary", "DnAE / permanent block"),
    ("eval_out boundary", "_eval_out writes"),
    ("docs boundary", "documentation scope"),
    ("capability boundary", "capability modules"),
    ("runner/verifier boundary", "runner and verifier tools"),
    ("rollback boundary", "rollback rehearsal scope"),
)

AUTHORIZATION_DEPENDENCIES: Tuple[Tuple[str, bool, bool, bool, bool], ...] = (
    ("verifier rerun authorization", True, True, True, True),
    ("evidence generation authorization", True, True, True, True),
    ("runtime evidence generation authorization", True, True, True, True),
    ("success evidence generation authorization", True, True, True, True),
    ("evidence acceptance authorization", True, True, True, False),
    ("evidence registry generation authorization", True, True, True, True),
    ("restore map generation authorization", True, True, True, True),
    ("sandbox creation authorization", True, True, True, True),
    ("branch creation authorization", True, True, True, True),
    ("rollback rehearsal authorization", True, True, True, True),
    ("migration execution authorization", True, True, True, True),
    ("success claim authority", True, True, True, True),
)

FORBIDDEN_SHORTCUTS: Tuple[Tuple[str, str, str, str], ...] = (
    (
        "owner approval planned does not mean owner approval granted",
        "owner_approval_granted_now",
        "planning GO ≠ approval granted",
        "P0",
    ),
    (
        "operator acknowledgement planned does not mean operator acknowledged",
        "operator_acknowledgement_granted_now",
        "planning GO ≠ operator acknowledged",
        "P0",
    ),
    (
        "execution window planned does not mean window opened",
        "execution_window_opened_now",
        "planning GO ≠ window opened",
        "P0",
    ),
    (
        "abort authority planned does not mean abort authority confirmed",
        "abort_authority_confirmed_now",
        "planning GO ≠ abort confirmed",
        "P0",
    ),
    (
        "scope confirmation planned does not mean scope accepted",
        "scope_confirmation_accepted_now",
        "planning GO ≠ scope accepted",
        "P0",
    ),
    (
        "owner approval granted does not replace operator acknowledgement",
        "operator_acknowledgement_granted_now",
        "both required for execution",
        "P0",
    ),
    (
        "operator acknowledgement does not replace owner approval",
        "owner_approval_granted_now",
        "both required for execution",
        "P0",
    ),
    (
        "execution window opened does not imply execution committed",
        "execution_committed",
        "window open ≠ execution done",
        "P0",
    ),
    (
        "evidence generation authorization does not imply evidence generated",
        "evidence_generated_now",
        "authorized ≠ generated",
        "P0",
    ),
    (
        "verifier rerun authorization does not imply verifier rerun executed",
        "verifier_rerun_executed_now",
        "authorized ≠ rerun done",
        "P0",
    ),
    (
        "success claim authority planned does not imply success claim allowed",
        "success_claim_allowed",
        "authority planned ≠ claim allowed",
        "P0",
    ),
    (
        "roadmap decision does not imply approval request",
        "owner_approval_request_sent_now",
        "roadmap GO ≠ request sent",
        "P0",
    ),
)

EVIDENCE_AUTH_LINKS: Tuple[Tuple[str, str], ...] = (
    ("evidence_candidate_generation", "owner + operator + scope"),
    ("runtime_evidence_generation", "execution window + evidence generation auth"),
    ("audit_evidence_acceptance", "operator acknowledgement + scope"),
    ("success_evidence_generation", "success claim authority prerequisites"),
    ("source_chain_validation", "scope confirmation + operator ack"),
    ("evidence_upgrade_path_authorization", "owner approval + evidence acceptance auth"),
    ("evidence_acceptance_for_success_claim", "success claim authority"),
    ("evidence_registry_generation", "owner + operator + registry auth"),
    ("verifier_report_as_audit_support", "verifier rerun not required for audit"),
    ("summary_as_audit_support", "never success evidence alone"),
    ("post_execution_review_evidence", "post-execution review authority"),
    ("rollback_or_migration_result_evidence", "rollback/migration authorization"),
)

VERIFIER_CHECKS: Tuple[Tuple[str, str, str, str, str], ...] = (
    ("O01", "owner_approval_request_not_sent_in_planning", "planning", "owner_approval_request_sent_now", "request sent in planning", "P0"),
    ("O02", "owner_approval_granted_requires_owner_identity", "all", "owner_identity", "grant without identity", "P0"),
    ("O03", "operator_acknowledgement_requires_operator_identity", "all", "operator_identity", "ack without identity", "P0"),
    ("O04", "execution_window_requires_owner_and_operator", "execution", "owner+operator", "window without dual ack", "P0"),
    ("O05", "abort_authority_required_before_execution", "execution,rehearsal,migration", "abort_authority_confirmed_now", "execution without abort plan", "P0"),
    ("O06", "evidence_generation_requires_authorization", "evidence", "evidence_generation_authorized_now", "evidence without auth", "P0"),
    ("O07", "verifier_rerun_requires_authorization", "verifier", "verifier_rerun_authorized_now", "rerun without auth", "P0"),
    ("O08", "success_claim_requires_success_claim_authority", "success_claim", "success_claim_authority_confirmed_now", "claim without authority", "P0"),
    ("O09", "owner_approval_does_not_replace_operator_acknowledgement", "all", "operator_acknowledgement_granted_now", "owner only shortcut", "P0"),
    ("O10", "execution_window_does_not_imply_execution_committed", "execution", "execution_committed", "window implies commit", "P0"),
    ("O11", "authorization_planned_does_not_imply_authorized", "planning", "authorization_granted_now", "planned implies granted", "P0"),
    ("O12", "approval_protocol_planning_does_not_release_execution", "planning", "real_rehearsal_execution_allowed", "planning releases execution", "P0"),
)

NON_CLAIM_SCENARIOS: Tuple[Tuple[str, str], ...] = (
    ("planning GO", "planning GO does not mean owner approval requested"),
    ("owner granted", "planning GO does not mean owner approval granted"),
    ("operator acknowledged", "planning GO does not mean operator acknowledged"),
    ("window opened", "planning GO does not mean execution window opened"),
    ("abort confirmed", "planning GO does not mean abort authority confirmed"),
    ("evidence auth", "planning GO does not mean evidence generation authorized"),
    ("verifier rerun auth", "planning GO does not mean verifier rerun authorized"),
    ("success claim authority", "planning GO does not mean success claim authority confirmed"),
    ("roadmap route", "roadmap selected route does not mean approval workflow started"),
    ("real rehearsal", "owner/operator protocol planned does not mean real rehearsal allowed"),
    ("authorization dependency", "authorization dependency planned does not mean authorization granted"),
    ("evidence authorization", "evidence authorization planned does not mean evidence generated"),
)

OUTPUT_PLAN_ARTIFACTS: Tuple[Tuple[str, str, bool, bool, bool], ...] = (
    ("owner_operator_protocol_policy_v1.json", "protocol policy", True, True, True),
    ("owner_approval_identity_matrix_v1.json", "owner identity", True, True, True),
    ("operator_acknowledgement_matrix_v1.json", "operator acknowledgement", True, True, True),
    ("execution_window_matrix_v1.json", "execution window", True, True, True),
    ("abort_authority_matrix_v1.json", "abort authority", True, True, True),
    ("scope_boundary_acknowledgement_matrix_v1.json", "scope and boundary", True, True, True),
    ("authorization_dependency_matrix_v1.json", "authorization dependencies", True, True, True),
    ("forbidden_shortcut_matrix_v1.json", "forbidden shortcuts", True, True, False),
    ("evidence_authorization_link_matrix_v1.json", "evidence authorization links", True, True, True),
    ("owner_operator_verifier_usage_matrix_v1.json", "verifier usage", True, False, True),
    ("owner_operator_non_claims_rules_v1.json", "non-claims rules", True, True, False),
    ("owner_operator_protocol_readiness_decision_v1.json", "readiness decision", True, True, True),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "owner_operator_protocol_planning_only": True,
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
    readiness = _try_read_json(root / "evidence_chain_roadmap_readiness_decision_v1.json") if root else None
    routes = _try_read_json(root / "evidence_chain_roadmap_route_candidate_matrix_v1.json") if root else None
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


def _build_owner_identity_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            identity_component=comp,
            why_required=why,
            required_for_owner_approval=True,
            required_for_evidence_generation=comp
            in ("owner authority scope", "owner approval artifact"),
            required_for_real_rehearsal=True,
            required_for_success_claim=comp in ("owner authority scope", "owner audit trail"),
            planned_field=f"owner.{comp.replace(' ', '_')}",
            satisfied_now=False,
            approval_granted_now=False,
        )
        for comp, why in OWNER_IDENTITY_COMPONENTS
    ]


def _build_operator_ack_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            ack_component=comp,
            why_required=why,
            required_for_execution=True,
            required_for_evidence_generation=comp
            in ("operator scope acknowledgement", "operator evidence responsibility acknowledgement"),
            required_for_verifier_rerun=comp == "operator scope acknowledgement",
            required_for_real_rehearsal=True,
            planned_field=f"operator.{comp.replace(' ', '_')}",
            acknowledged_now=False,
            operator_acknowledgement_granted_now=False,
        )
        for comp, why in OPERATOR_ACK_COMPONENTS
    ]


def _build_execution_window_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            window_component=comp,
            why_required=why,
            required_for_execution=comp not in ("post-window review requirement",),
            required_for_evidence_generation=comp in ("evidence capture scope", "allowed operations"),
            required_for_verifier_rerun=comp == "verifier rerun scope",
            required_for_success_claim=comp == "post-window review requirement",
            planned_field=f"window.{comp.replace(' ', '_')}",
            opened_now=False,
            execution_window_opened_now=False,
        )
        for comp, why in EXECUTION_WINDOW_COMPONENTS
    ]


def _build_abort_authority_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            abort_component=comp,
            why_required=why,
            required_for_execution=True,
            required_for_real_rehearsal=True,
            required_for_migration=True,
            planned_field=f"abort.{comp.replace(' ', '_')}",
            confirmed_now=False,
            abort_authority_confirmed_now=False,
        )
        for comp, why in ABORT_AUTHORITY_COMPONENTS
    ]


def _build_scope_boundary_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            scope_boundary_component=comp,
            why_required=why,
            required_for_owner_approval=comp in ("execution scope confirmation", "protected asset boundary"),
            required_for_operator_acknowledgement=True,
            required_for_execution=True,
            required_for_evidence_generation=comp
            in ("evidence generation scope", "eval_out boundary"),
            planned_field=f"scope.{comp.replace(' ', '_')}",
            acknowledged_now=False,
            scope_confirmation_accepted_now=False,
        )
        for comp, why in SCOPE_BOUNDARY_COMPONENTS
    ]


def _build_authorization_dependency_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            authorization_dependency=dep,
            required_owner_approval=ro,
            required_operator_acknowledgement=op,
            required_execution_window=win,
            required_scope_confirmation=True,
            required_abort_authority=abort,
            planned_authorization_field=f"auth.{dep.replace(' ', '_')}",
            authorized_now=False,
            authorization_granted_now=False,
        )
        for dep, ro, op, win, abort in AUTHORIZATION_DEPENDENCIES
    ]


def _build_forbidden_shortcut_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            forbidden_shortcut=shortcut,
            why_forbidden=f"prevents misread of {affected}",
            affected_terms=affected,
            required_non_claim=non_claim,
            severity=severity,
            planned_verifier_check=f"verify_{affected}",
            enforced_now=False,
        )
        for shortcut, affected, non_claim, severity in FORBIDDEN_SHORTCUTS
    ]


def _build_evidence_auth_link_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            evidence_authorization_link=link,
            required_owner_approval=True,
            required_operator_acknowledgement=True,
            required_execution_window=link
            in ("runtime_evidence_generation", "rollback_or_migration_result_evidence"),
            required_scope_confirmation=True,
            required_authority=authority,
            authorized_now=False,
            evidence_generated_now=False,
            success_claim_allowed_now=False,
        )
        for link, authority in EVIDENCE_AUTH_LINKS
    ]


def _build_verifier_usage_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            verifier_check_id=vid,
            check_name=name,
            target_phase_types=targets,
            required_fields=fields,
            failure_condition=fail,
            severity=sev,
            planned_now=True,
            verifier_modified_now=False,
            enforced_now=False,
        )
        for vid, name, targets, fields, fail, sev in VERIFIER_CHECKS
    ]


def _build_non_claims_matrix() -> List[Dict[str, Any]]:
    return [
        _row(
            scenario=scenario,
            required_non_claim=claim,
            risk_if_missing="authorization or evidence misread",
            must_be_in_summary=True,
            must_be_in_verifier_report=True,
            planned_now=True,
            generated_now=False,
        )
        for scenario, claim in NON_CLAIM_SCENARIOS
    ]


def _build_output_plan() -> List[Dict[str, Any]]:
    return [
        _row(
            planned_artifact=artifact,
            purpose=purpose,
            required=required,
            used_by_future_verifier=used_v,
            used_by_evidence_chain=used_e,
            used_by_real_rehearsal_chain=used_e,
            used_by_migration_chain=used_e,
            not_generated_now=True,
        )
        for artifact, purpose, required, used_v, used_e in OUTPUT_PLAN_ARTIFACTS
    ]


def run_owner_operator_approval_protocol_planning_v1(
    *,
    evidence_chain_governance_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(evidence_chain_governance_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    routes = upstream["routes"] or upstream["artifacts"].get(
        "evidence_chain_roadmap_route_candidate_matrix_v1.json", {}
    )

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream roadmap decision verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_summary.get("selected_route") != SELECTED_ROUTE:
        blockers.append("upstream selected_route is not Route A")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_readiness.get("ready_for_owner_operator_approval_protocol_planning") is not True:
        blockers.append("upstream not ready_for_owner_operator_approval_protocol_planning")
    for flag in (
        "owner_approval_granted_now",
        "operator_acknowledgement_granted_now",
        "execution_window_opened_now",
        "abort_authority_confirmed_now",
        "authorization_granted_now",
        "evidence_generated_now",
        "evidence_accepted_for_success_claim_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")
    for flag in (
        "ready_for_owner_approval_request",
        "ready_for_operator_acknowledgement_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation",
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

    route_a = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "A"), {})
    route_b = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "B"), {})
    route_h = next((r for r in (routes.get("rows") or []) if r.get("route_id") == "H"), {})
    if route_a.get("selected_now") is not True:
        blockers.append("Route A not selected in upstream matrix")
    if route_b.get("deferred") is not True:
        blockers.append("Route B must be deferred")
    if route_h.get("blocked_now") is not True:
        blockers.append("Route H must be blocked")

    owner_rows = _build_owner_identity_matrix()
    operator_rows = _build_operator_ack_matrix()
    window_rows = _build_execution_window_matrix()
    abort_rows = _build_abort_authority_matrix()
    scope_rows = _build_scope_boundary_matrix()
    auth_dep_rows = _build_authorization_dependency_matrix()
    shortcut_rows = _build_forbidden_shortcut_matrix()
    evidence_link_rows = _build_evidence_auth_link_matrix()
    verifier_rows = _build_verifier_usage_matrix()
    non_claims_rows = _build_non_claims_matrix()
    output_rows = _build_output_plan()

    all_frozen = all(
        r.get("approval_granted_now") is False and r.get("satisfied_now") is False for r in owner_rows
    ) and all(r.get("operator_acknowledgement_granted_now") is False for r in operator_rows)
    if not all_frozen:
        blockers.append("planning matrices must not show granted/acknowledged state")

    planning_pass = (
        len(owner_rows) >= 10
        and len(operator_rows) >= 10
        and len(window_rows) >= 12
        and len(abort_rows) >= 12
        and len(scope_rows) >= 12
        and len(auth_dep_rows) >= 12
        and len(shortcut_rows) >= 12
        and len(evidence_link_rows) >= 12
        and len(verifier_rows) >= 12
        and len(non_claims_rows) >= 12
        and len(output_rows) >= 12
        and all(r.get("not_generated_now") is True for r in output_rows)
        and all_frozen
        and not blockers
    )
    boundary_ok = planning_pass

    owner_operator_approval_protocol_planning_policy = _row(
        phase_name=PHASE_ID,
        owner_operator_protocol_planning_only=True,
        source_phase=SOURCE_PHASE,
        source_selected_route_observed=up_summary.get("selected_route"),
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
    )

    owner_approval_identity_planning_matrix = {
        "rows": owner_rows,
        "row_count": len(owner_rows),
        **_planning_meta(),
    }
    operator_acknowledgement_planning_matrix = {
        "rows": operator_rows,
        "row_count": len(operator_rows),
        **_planning_meta(),
    }
    execution_window_planning_matrix = {
        "rows": window_rows,
        "row_count": len(window_rows),
        **_planning_meta(),
    }
    abort_authority_planning_matrix = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        **_planning_meta(),
    }
    scope_boundary_acknowledgement_planning_matrix = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        **_planning_meta(),
    }
    authorization_dependency_planning_matrix = {
        "rows": auth_dep_rows,
        "row_count": len(auth_dep_rows),
        **_planning_meta(),
    }
    owner_operator_forbidden_shortcut_matrix = {
        "rows": shortcut_rows,
        "row_count": len(shortcut_rows),
        **_planning_meta(),
    }
    owner_operator_evidence_authorization_link_matrix = {
        "rows": evidence_link_rows,
        "row_count": len(evidence_link_rows),
        **_planning_meta(),
    }
    owner_operator_verifier_usage_planning_matrix = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        **_planning_meta(),
    }
    owner_operator_non_claims_planning_matrix = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        **_planning_meta(),
    }
    owner_operator_protocol_output_plan = {
        "rows": output_rows,
        "row_count": len(output_rows),
        **_planning_meta(),
    }

    owner_operator_approval_protocol_planning_readiness_decision = {
        "ready_for_owner_operator_approval_protocol_dryrun": boundary_ok,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_execution_window_opening": False,
        "ready_for_abort_authority_confirmation": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_verifier_rerun_authorization": False,
        "ready_for_success_claim_authority_confirmation": False,
        "ready_for_evidence_generation": False,
        "ready_for_evidence_registry_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "owner_operator_protocol_planning_completed": boundary_ok,
        "owner_identity_planned": True,
        "operator_acknowledgement_planned": True,
        "execution_window_planned": True,
        "abort_authority_planned": True,
        "scope_boundary_acknowledgement_planned": True,
        "authorization_dependency_planned": True,
        "forbidden_shortcuts_planned": True,
        "evidence_authorization_link_planned": True,
        "verifier_usage_planned": True,
        "non_claims_planned": True,
        "output_plan_generated": True,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "authorization_granted_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "evidence_chain_governance_roadmap_decision_input_loaded": upstream["loaded"],
        "source_selected_route_observed": up_summary.get("selected_route"),
        "owner_identity_component_count": len(owner_rows),
        "operator_ack_component_count": len(operator_rows),
        "execution_window_component_count": len(window_rows),
        "abort_authority_component_count": len(abort_rows),
        "scope_boundary_component_count": len(scope_rows),
        "authorization_dependency_count": len(auth_dep_rows),
        "forbidden_shortcut_count": len(shortcut_rows),
        "evidence_auth_link_count": len(evidence_link_rows),
        "verifier_check_count": len(verifier_rows),
        "non_claims_count": len(non_claims_rows),
        "output_plan_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "owner_operator_approval_protocol_planning_policy": owner_operator_approval_protocol_planning_policy,
        "owner_approval_identity_planning_matrix": owner_approval_identity_planning_matrix,
        "operator_acknowledgement_planning_matrix": operator_acknowledgement_planning_matrix,
        "execution_window_planning_matrix": execution_window_planning_matrix,
        "abort_authority_planning_matrix": abort_authority_planning_matrix,
        "scope_boundary_acknowledgement_planning_matrix": scope_boundary_acknowledgement_planning_matrix,
        "authorization_dependency_planning_matrix": authorization_dependency_planning_matrix,
        "owner_operator_forbidden_shortcut_matrix": owner_operator_forbidden_shortcut_matrix,
        "owner_operator_evidence_authorization_link_matrix": owner_operator_evidence_authorization_link_matrix,
        "owner_operator_verifier_usage_planning_matrix": owner_operator_verifier_usage_planning_matrix,
        "owner_operator_non_claims_planning_matrix": owner_operator_non_claims_planning_matrix,
        "owner_operator_protocol_output_plan": owner_operator_protocol_output_plan,
        "owner_operator_approval_protocol_planning_readiness_decision": owner_operator_approval_protocol_planning_readiness_decision,
    }
