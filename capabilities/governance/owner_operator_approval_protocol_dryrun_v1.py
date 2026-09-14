# -*- coding: utf-8 -*-
"""Owner/Operator Approval Protocol DryRun v1.

Dry-run only: simulate consumption of owner/operator protocol planning by future
verifier, evidence chain, rehearsal, and migration chains. Does not grant
authorization or generate evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.owner_operator_approval_protocol_planning_v1 import (
    ABORT_AUTHORITY_COMPONENTS,
    AUTHORIZATION_DEPENDENCIES,
    EVIDENCE_AUTH_LINKS,
    EXECUTION_WINDOW_COMPONENTS,
    FORBIDDEN_SHORTCUTS,
    NON_CLAIM_SCENARIOS,
    OPERATOR_ACK_COMPONENTS,
    OWNER_IDENTITY_COMPONENTS,
    SCOPE_BOUNDARY_COMPONENTS,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Owner-Operator-Approval-Protocol-DryRun-v1-001"
DRYRUN_SCOPE = "owner_operator_approval_protocol_dryrun_only"
SOURCE_CHAIN = "owner_operator_approval_protocol_dryrun_v1"

SOURCE_PHASE = "Phase-Owner-Operator-Approval-Protocol-Planning-v1-001"
FINAL_DECISION = "OWNER_OPERATOR_APPROVAL_PROTOCOL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Owner-Operator-Approval-Protocol-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("planning policy", "owner_operator_approval_protocol_planning_policy_v1.json", 0),
    ("owner approval identity matrix", "owner_approval_identity_planning_matrix_v1.json", 10),
    ("operator acknowledgement matrix", "operator_acknowledgement_planning_matrix_v1.json", 10),
    ("execution window matrix", "execution_window_planning_matrix_v1.json", 12),
    ("abort authority matrix", "abort_authority_planning_matrix_v1.json", 12),
    ("scope boundary acknowledgement matrix", "scope_boundary_acknowledgement_planning_matrix_v1.json", 12),
    ("authorization dependency matrix", "authorization_dependency_planning_matrix_v1.json", 12),
    ("forbidden shortcut matrix", "owner_operator_forbidden_shortcut_matrix_v1.json", 12),
    ("evidence authorization link matrix", "owner_operator_evidence_authorization_link_matrix_v1.json", 12),
    ("verifier usage matrix", "owner_operator_verifier_usage_planning_matrix_v1.json", 12),
    ("non-claims matrix", "owner_operator_non_claims_planning_matrix_v1.json", 12),
    ("output plan", "owner_operator_protocol_output_plan_v1.json", 12),
    ("planning readiness decision", "owner_operator_approval_protocol_planning_readiness_decision_v1.json", 0),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "owner_operator_protocol_dryrun_only": True,
        "simulated": True,
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
    return {**kwargs, **_dryrun_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _row_count(payload: Dict[str, Any]) -> int:
    if "row_count" in payload:
        return int(payload["row_count"])
    rows = payload.get("rows")
    return len(rows) if isinstance(rows, list) else 0


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(
        root / "owner_operator_approval_protocol_planning_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for _, filename, _ in PLANNING_ARTIFACTS:
            payload = _try_read_json(root / filename)
            if payload is None:
                missing.append(filename)
            else:
                art[filename] = payload
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


def _build_completeness(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for name, filename, min_count in PLANNING_ARTIFACTS:
        payload = artifacts.get(filename)
        observed = payload is not None
        count = _row_count(payload) if isinstance(payload, dict) else 0
        schema_ok = observed and isinstance(payload, dict)
        count_ok = min_count == 0 or count >= min_count
        semantic_ok = schema_ok and count_ok
        if filename == "owner_approval_identity_planning_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("approval_granted_now") is False for r in (payload.get("rows") or [])
            )
        if filename == "owner_operator_protocol_output_plan_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("not_generated_now") is True for r in (payload.get("rows") or [])
            )
        consumable = observed and semantic_ok
        if not consumable:
            all_pass = False
        rows.append(
            _row(
                artifact_name=name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_ok,
                count_requirement_pass=count_ok,
                semantic_requirement_pass=semantic_ok,
                dryrun_consumable=consumable,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass


def _build_owner_identity_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("identity_component"): r
        for r in (artifacts.get("owner_approval_identity_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in OWNER_IDENTITY_COMPONENTS:
        p = by.get(comp, {})
        ok_row = (
            bool(p.get("planned_field"))
            and p.get("approval_granted_now") is False
            and p.get("satisfied_now", False) is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                identity_component=comp,
                required_for_owner_approval=p.get("required_for_owner_approval", True),
                required_for_evidence_generation=p.get("required_for_evidence_generation", False),
                required_for_real_rehearsal=p.get("required_for_real_rehearsal", False),
                required_for_success_claim=p.get("required_for_success_claim", False),
                simulated_consumption=ok_row,
                satisfied_now=False,
                approval_granted_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_operator_ack_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("ack_component"): r
        for r in (artifacts.get("operator_acknowledgement_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in OPERATOR_ACK_COMPONENTS:
        p = by.get(comp, {})
        ok_row = (
            bool(p.get("planned_field"))
            and p.get("operator_acknowledgement_granted_now") is False
            and p.get("acknowledged_now", False) is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                ack_component=comp,
                required_for_execution=p.get("required_for_execution", True),
                required_for_evidence_generation=p.get("required_for_evidence_generation", False),
                required_for_verifier_rerun=p.get("required_for_verifier_rerun", False),
                required_for_real_rehearsal=p.get("required_for_real_rehearsal", False),
                simulated_consumption=ok_row,
                acknowledged_now=False,
                operator_acknowledgement_granted_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_execution_window_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("window_component"): r
        for r in (artifacts.get("execution_window_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in EXECUTION_WINDOW_COMPONENTS:
        p = by.get(comp, {})
        ok_row = (
            bool(p.get("planned_field"))
            and p.get("execution_window_opened_now") is False
            and p.get("opened_now", False) is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                window_component=comp,
                required_for_execution=p.get("required_for_execution", True),
                required_for_evidence_generation=p.get("required_for_evidence_generation", False),
                required_for_verifier_rerun=p.get("required_for_verifier_rerun", False),
                required_for_success_claim=p.get("required_for_success_claim", False),
                simulated_consumption=ok_row,
                opened_now=False,
                execution_window_opened_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_abort_authority_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("abort_component"): r
        for r in (artifacts.get("abort_authority_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in ABORT_AUTHORITY_COMPONENTS:
        p = by.get(comp, {})
        ok_row = (
            bool(p.get("planned_field"))
            and p.get("abort_authority_confirmed_now") is False
            and p.get("confirmed_now", False) is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                abort_component=comp,
                required_for_execution=p.get("required_for_execution", True),
                required_for_real_rehearsal=p.get("required_for_real_rehearsal", True),
                required_for_migration=p.get("required_for_migration", True),
                simulated_consumption=ok_row,
                confirmed_now=False,
                abort_authority_confirmed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_scope_boundary_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("scope_boundary_component"): r
        for r in (artifacts.get("scope_boundary_acknowledgement_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in SCOPE_BOUNDARY_COMPONENTS:
        p = by.get(comp, {})
        ok_row = (
            bool(p.get("planned_field"))
            and p.get("scope_confirmation_accepted_now") is False
            and p.get("acknowledged_now", False) is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                scope_boundary_component=comp,
                required_for_owner_approval=p.get("required_for_owner_approval", False),
                required_for_operator_acknowledgement=p.get("required_for_operator_acknowledgement", True),
                required_for_execution=p.get("required_for_execution", True),
                required_for_evidence_generation=p.get("required_for_evidence_generation", False),
                simulated_consumption=ok_row,
                acknowledged_now=False,
                scope_confirmation_accepted_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_authorization_dependency_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("authorization_dependency"): r
        for r in (artifacts.get("authorization_dependency_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for dep, _ro, _op, _win, _abort in AUTHORIZATION_DEPENDENCIES:
        p = by.get(dep, {})
        ok_row = (
            bool(p.get("planned_authorization_field"))
            and p.get("authorized_now") is False
            and p.get("authorization_granted_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                authorization_dependency=dep,
                required_owner_approval=p.get("required_owner_approval", True),
                required_operator_acknowledgement=p.get("required_operator_acknowledgement", True),
                required_execution_window=p.get("required_execution_window", True),
                required_scope_confirmation=p.get("required_scope_confirmation", True),
                required_abort_authority=p.get("required_abort_authority", True),
                simulated_dependency_check=ok_row,
                authorized_now=False,
                authorization_granted_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_forbidden_shortcut_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("forbidden_shortcut"): r
        for r in (artifacts.get("owner_operator_forbidden_shortcut_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for shortcut, affected, non_claim, severity in FORBIDDEN_SHORTCUTS:
        p = by.get(shortcut, {})
        ok_row = (
            bool(p.get("required_non_claim"))
            and p.get("enforced_now") is False
            and p.get("verifier_modified_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                forbidden_shortcut=shortcut,
                affected_terms=p.get("affected_terms") or affected,
                required_non_claim=p.get("required_non_claim") or non_claim,
                severity=p.get("severity") or severity,
                simulated_check=ok_row,
                enforced_now=False,
                verifier_modified_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_evidence_link_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("evidence_authorization_link"): r
        for r in (artifacts.get("owner_operator_evidence_authorization_link_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for link, authority in EVIDENCE_AUTH_LINKS:
        p = by.get(link, {})
        ok_row = (
            bool(p.get("required_authority") or authority)
            and p.get("authorized_now") is False
            and p.get("evidence_generated_now") is False
            and p.get("success_claim_allowed_now", False) is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                evidence_authorization_link=link,
                required_owner_approval=p.get("required_owner_approval", True),
                required_operator_acknowledgement=p.get("required_operator_acknowledgement", True),
                required_execution_window=p.get("required_execution_window", False),
                required_scope_confirmation=p.get("required_scope_confirmation", True),
                required_authority=p.get("required_authority") or authority,
                simulated_link_check=ok_row,
                authorized_now=False,
                evidence_generated_now=False,
                success_claim_allowed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_usage_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("verifier_check_id"): r
        for r in (artifacts.get("owner_operator_verifier_usage_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, phases, fields, fail, sev in VERIFIER_CHECKS:
        v = by.get(vid, {})
        consumable = (
            v.get("planned_now") is True
            and v.get("verifier_modified_now") is False
            and v.get("enforced_now") is False
            and bool(v.get("failure_condition") or fail)
        )
        if not consumable:
            all_pass = False
        rows.append(
            _row(
                verifier_check_id=vid,
                check_name=v.get("check_name") or name,
                target_phase_types=v.get("target_phase_types") or phases,
                required_fields=v.get("required_fields") or fields,
                failure_condition=v.get("failure_condition") or fail,
                severity=v.get("severity") or sev,
                simulated_verifier_consumption=consumable,
                verifier_modified_now=False,
                enforced_now=False,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_non_claims_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc_by = {
        r.get("scenario"): r
        for r in (artifacts.get("owner_operator_non_claims_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scenario, non_claim in NON_CLAIM_SCENARIOS:
        n = nc_by.get(scenario, {})
        ok_row = (
            bool(n.get("required_non_claim"))
            and n.get("generated_now") is False
            and n.get("planned_now") is True
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                scenario=scenario,
                required_non_claim=n.get("required_non_claim") or non_claim,
                target_outputs=["summary", "verifier_report", "phase_documentation"],
                simulated_generation=ok_row,
                generated_now=False,
                template_modified_now=False,
                documentation_auto_sync_executed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_owner_operator_approval_protocol_dryrun_v1(
    *,
    owner_operator_approval_protocol_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(owner_operator_approval_protocol_planning_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream planning verifier not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok not true")
    if up_readiness.get("ready_for_owner_operator_approval_protocol_dryrun") is not True:
        blockers.append("not ready_for_owner_operator_approval_protocol_dryrun")
    if up_summary.get("owner_operator_protocol_planning_only") is not True:
        blockers.append("upstream owner_operator_protocol_planning_only not true")
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
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must be false")
    for flag in (
        "ready_for_owner_approval_request",
        "ready_for_operator_acknowledgement_request",
        "ready_for_execution_window_opening",
        "ready_for_abort_authority_confirmation",
        "ready_for_evidence_generation_authorization",
        "ready_for_verifier_rerun_authorization",
        "ready_for_success_claim_authority_confirmation",
        "ready_for_real_rollback_rehearsal_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    comp_rows, comp_pass = _build_completeness(artifacts)
    owner_rows, owner_pass = _build_owner_identity_dryrun(artifacts)
    operator_rows, operator_pass = _build_operator_ack_dryrun(artifacts)
    window_rows, window_pass = _build_execution_window_dryrun(artifacts)
    abort_rows, abort_pass = _build_abort_authority_dryrun(artifacts)
    scope_rows, scope_pass = _build_scope_boundary_dryrun(artifacts)
    auth_rows, auth_pass = _build_authorization_dependency_dryrun(artifacts)
    shortcut_rows, shortcut_pass = _build_forbidden_shortcut_dryrun(artifacts)
    evidence_rows, evidence_pass = _build_evidence_link_dryrun(artifacts)
    verifier_rows, verifier_pass = _build_verifier_usage_dryrun(artifacts)
    nclaims_rows, nclaims_pass = _build_non_claims_dryrun(artifacts)

    dryrun_pass = (
        comp_pass
        and owner_pass
        and operator_pass
        and window_pass
        and abort_pass
        and scope_pass
        and auth_pass
        and shortcut_pass
        and evidence_pass
        and verifier_pass
        and nclaims_pass
        and not blockers
    )
    boundary_ok = dryrun_pass

    owner_operator_approval_protocol_dryrun_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_owner_operator_approval_protocol_dryrun_observed=up_readiness.get(
            "ready_for_owner_operator_approval_protocol_dryrun"
        )
        is True,
    )

    owner_operator_planning_artifact_completeness_dryrun = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_dryrun_meta(),
    }
    owner_identity_consumption_dryrun = {
        "rows": owner_rows,
        "row_count": len(owner_rows),
        "all_pass": owner_pass,
        **_dryrun_meta(),
    }
    operator_acknowledgement_consumption_dryrun = {
        "rows": operator_rows,
        "row_count": len(operator_rows),
        "all_pass": operator_pass,
        **_dryrun_meta(),
    }
    execution_window_consumption_dryrun = {
        "rows": window_rows,
        "row_count": len(window_rows),
        "all_pass": window_pass,
        **_dryrun_meta(),
    }
    abort_authority_consumption_dryrun = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "all_pass": abort_pass,
        **_dryrun_meta(),
    }
    scope_boundary_acknowledgement_consumption_dryrun = {
        "rows": scope_rows,
        "row_count": len(scope_rows),
        "all_pass": scope_pass,
        **_dryrun_meta(),
    }
    authorization_dependency_consumption_dryrun = {
        "rows": auth_rows,
        "row_count": len(auth_rows),
        "all_pass": auth_pass,
        **_dryrun_meta(),
    }
    owner_operator_forbidden_shortcut_dryrun = {
        "rows": shortcut_rows,
        "row_count": len(shortcut_rows),
        "all_pass": shortcut_pass,
        **_dryrun_meta(),
    }
    evidence_authorization_link_dryrun = {
        "rows": evidence_rows,
        "row_count": len(evidence_rows),
        "all_pass": evidence_pass,
        **_dryrun_meta(),
    }
    owner_operator_verifier_usage_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    owner_operator_non_claims_generation_dryrun = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_dryrun_meta(),
    }

    owner_operator_approval_protocol_dryrun_readiness_decision = {
        "ready_for_owner_operator_approval_protocol_post_dryrun_review": boundary_ok,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_owner_approval_grant": False,
        "ready_for_operator_acknowledgement_grant": False,
        "ready_for_execution_window_opening": False,
        "ready_for_abort_authority_confirmation": False,
        "ready_for_scope_confirmation_acceptance": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_verifier_rerun_authorization": False,
        "ready_for_success_claim_authority_confirmation": False,
        "ready_for_evidence_generation": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "owner_operator_protocol_dryrun_completed": boundary_ok,
        "planning_artifact_completeness_dryrun_pass": comp_pass,
        "owner_identity_consumption_dryrun_pass": owner_pass,
        "operator_acknowledgement_consumption_dryrun_pass": operator_pass,
        "execution_window_consumption_dryrun_pass": window_pass,
        "abort_authority_consumption_dryrun_pass": abort_pass,
        "scope_boundary_acknowledgement_consumption_dryrun_pass": scope_pass,
        "authorization_dependency_consumption_dryrun_pass": auth_pass,
        "forbidden_shortcut_dryrun_pass": shortcut_pass,
        "evidence_authorization_link_dryrun_pass": evidence_pass,
        "verifier_usage_dryrun_pass": verifier_pass,
        "non_claims_generation_dryrun_pass": nclaims_pass,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "authorization_granted_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "owner_operator_approval_protocol_planning_input_loaded": upstream["loaded"],
        "owner_identity_component_count": len(owner_rows),
        "operator_ack_component_count": len(operator_rows),
        "execution_window_component_count": len(window_rows),
        "abort_authority_component_count": len(abort_rows),
        "scope_boundary_component_count": len(scope_rows),
        "authorization_dependency_count": len(auth_rows),
        "forbidden_shortcut_count": len(shortcut_rows),
        "evidence_auth_link_count": len(evidence_rows),
        "verifier_check_count": len(verifier_rows),
        "non_claims_count": len(nclaims_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "OWNER_OPERATOR_APPROVAL_PROTOCOL_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "owner_operator_approval_protocol_dryrun_policy": owner_operator_approval_protocol_dryrun_policy,
        "owner_operator_planning_artifact_completeness_dryrun": owner_operator_planning_artifact_completeness_dryrun,
        "owner_identity_consumption_dryrun": owner_identity_consumption_dryrun,
        "operator_acknowledgement_consumption_dryrun": operator_acknowledgement_consumption_dryrun,
        "execution_window_consumption_dryrun": execution_window_consumption_dryrun,
        "abort_authority_consumption_dryrun": abort_authority_consumption_dryrun,
        "scope_boundary_acknowledgement_consumption_dryrun": scope_boundary_acknowledgement_consumption_dryrun,
        "authorization_dependency_consumption_dryrun": authorization_dependency_consumption_dryrun,
        "owner_operator_forbidden_shortcut_dryrun": owner_operator_forbidden_shortcut_dryrun,
        "evidence_authorization_link_dryrun": evidence_authorization_link_dryrun,
        "owner_operator_verifier_usage_dryrun": owner_operator_verifier_usage_dryrun,
        "owner_operator_non_claims_generation_dryrun": owner_operator_non_claims_generation_dryrun,
        "owner_operator_approval_protocol_dryrun_readiness_decision": owner_operator_approval_protocol_dryrun_readiness_decision,
    }
