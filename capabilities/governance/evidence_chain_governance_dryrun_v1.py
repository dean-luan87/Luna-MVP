# -*- coding: utf-8 -*-
"""Evidence Chain Governance DryRun v1.

Dry-run only: simulate consumption of evidence chain planning by future verifier,
success claim gate, rehearsal, and migration chains. Does not generate evidence
or allow success claim.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.evidence_chain_governance_planning_v1 import (
    ACCEPTANCE_RULES,
    ELIGIBILITY_CONDITIONS,
    NON_CLAIM_SCENARIOS,
    NON_SUBSTITUTION,
    SOURCE_CHAIN_COMPONENTS,
    UPGRADE_PATHS,
    USAGE_SCOPES,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Evidence-Chain-Governance-DryRun-v1-001"
DRYRUN_SCOPE = "evidence_chain_governance_dryrun_only"
SOURCE_CHAIN = "evidence_chain_governance_dryrun_v1"

SOURCE_PHASE = "Phase-Evidence-Chain-Governance-Planning-v1-001"
FINAL_DECISION = "EVIDENCE_CHAIN_GOVERNANCE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Evidence-Chain-Governance-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("planning policy", "evidence_chain_governance_planning_policy_v1.json", 0),
    ("evidence type lifecycle matrix", "evidence_type_lifecycle_planning_matrix_v1.json", 14),
    ("source chain matrix", "evidence_source_chain_planning_matrix_v1.json", 14),
    ("usage scope matrix", "evidence_usage_scope_planning_matrix_v1.json", 12),
    ("upgrade path matrix", "evidence_upgrade_path_planning_matrix_v1.json", 10),
    ("acceptance policy matrix", "evidence_acceptance_policy_planning_matrix_v1.json", 12),
    ("non-substitution matrix", "evidence_boundary_non_substitution_matrix_v1.json", 10),
    ("success claim eligibility matrix", "evidence_to_success_claim_eligibility_planning_matrix_v1.json", 12),
    ("verifier usage matrix", "evidence_verifier_usage_planning_matrix_v1.json", 12),
    ("non-claims planning matrix", "evidence_chain_non_claims_planning_matrix_v1.json", 12),
    ("output plan", "evidence_chain_output_plan_v1.json", 11),
    ("planning readiness decision", "evidence_chain_governance_planning_readiness_decision_v1.json", 0),
)

BLOCK_SUCCESS_CLAIM_NOW_TYPES = frozenset(
    {"evidence_candidate", "verifier_report", "summary", "source_chain"}
)

REJECT_ACCEPTANCE_RULES = frozenset(
    {
        "reject_summary_as_success_evidence",
        "reject_verifier_report_as_runtime_evidence",
        "reject_candidate_as_success_evidence",
        "reject_source_chain_alone_as_success_evidence",
    }
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "evidence_chain_dryrun_only": True,
        "simulated": True,
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
        root / "evidence_chain_governance_planning_readiness_decision_v1.json"
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
        if filename == "evidence_type_lifecycle_planning_matrix_v1.json" and isinstance(payload, dict):
            lc = payload.get("rows") or []
            cand = next((r for r in lc if r.get("evidence_type") == "evidence_candidate"), {})
            semantic_ok = (
                semantic_ok
                and cand.get("can_support_success_claim") is False
                and cand.get("can_support_success_claim_now") is False
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
                evidence_generated_now=False,
                evidence_accepted_for_success_claim_now=False,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass


def _build_lifecycle_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    lc_by = {
        r.get("evidence_type"): r
        for r in (artifacts.get("evidence_type_lifecycle_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for etype, row in lc_by.items():
        can = row.get("can_support_success_claim")
        can_now = row.get("can_support_success_claim_now")
        gen_now = row.get("generation_allowed_now")
        if etype in BLOCK_SUCCESS_CLAIM_NOW_TYPES:
            ok_row = can_now is False
            if etype in ("evidence_candidate", "verifier_report", "summary"):
                ok_row = ok_row and can is False
            if etype == "source_chain":
                ok_row = ok_row and row.get("can_stand_alone_for_success_claim") is False
        elif etype == "success_evidence":
            ok_row = can is True and gen_now is False
        elif etype == "runtime_evidence":
            ok_row = gen_now is False
        else:
            ok_row = can_now is False and gen_now is False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                evidence_type=etype,
                canonical_meaning=row.get("canonical_meaning"),
                allowed_usage=row.get("allowed_usage"),
                forbidden_usage=row.get("forbidden_usage"),
                can_support_success_claim=can,
                can_support_success_claim_now=False,
                generation_allowed_now=False,
                accepted_now=False,
                simulated_consumption=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_source_chain_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    sc_by = {
        r.get("source_chain_component"): r
        for r in (artifacts.get("evidence_source_chain_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for comp, _why in SOURCE_CHAIN_COMPONENTS:
        s = sc_by.get(comp, {})
        ok_row = (
            s.get("can_stand_alone_for_success_claim") is False
            and s.get("generated_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                source_chain_component=comp,
                required_for_runtime_evidence=s.get("required_for_runtime_evidence") is True,
                required_for_success_evidence=s.get("required_for_success_evidence") is True,
                required_for_audit_evidence=s.get("required_for_audit_evidence") is True,
                required_for_success_claim=s.get("required_for_success_claim") is True,
                can_stand_alone_for_success_claim=False,
                simulated_consumption=ok_row,
                generated_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_usage_scope_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    us_by = {
        r.get("usage_scope"): r
        for r in (artifacts.get("evidence_usage_scope_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scope, allowed, forbidden in USAGE_SCOPES:
        u = us_by.get(scope, {})
        ok_row = u.get("allowed_now") is False and bool(u.get("allowed_evidence_types"))
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                usage_scope=scope,
                allowed_evidence_types=u.get("allowed_evidence_types") or allowed,
                forbidden_evidence_types=u.get("forbidden_evidence_types") or forbidden,
                required_preconditions=u.get("required_preconditions"),
                required_source_chain=u.get("required_source_chain") is True,
                required_authorization=u.get("required_authorization") is True,
                allowed_now=False,
                simulated_usage_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_upgrade_path_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    up_by = {
        r.get("upgrade_path"): r
        for r in (artifacts.get("evidence_upgrade_path_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for path, from_t, to_t, pre in UPGRADE_PATHS:
        u = up_by.get(path, {})
        ok_row = u.get("allowed_now") is False and bool(u.get("forbidden_shortcut"))
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                upgrade_path=path,
                from_type=u.get("from_type") or from_t,
                to_type=u.get("to_type") or to_t,
                required_preconditions=u.get("required_preconditions") or pre,
                required_authorization=u.get("required_authorization"),
                required_review=u.get("required_review"),
                allowed_now=False,
                forbidden_shortcut=u.get("forbidden_shortcut"),
                simulated_upgrade_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_acceptance_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    ac_by = {
        r.get("acceptance_rule"): r
        for r in (artifacts.get("evidence_acceptance_policy_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for rule, target, accepted, rejected in ACCEPTANCE_RULES:
        a = ac_by.get(rule, {})
        ok_row = a.get("accepted_now") is False
        if rule in REJECT_ACCEPTANCE_RULES:
            ok_row = ok_row and "never" in str(a.get("accepted_when") or accepted).lower()
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                acceptance_rule=rule,
                target_evidence_type=a.get("target_evidence_type") or target,
                accepted_when=a.get("accepted_when") or accepted,
                rejected_when=a.get("rejected_when") or rejected,
                required_source_chain=a.get("required_source_chain") is True,
                required_review=a.get("required_review") is True,
                required_authorization=a.get("required_authorization") is True,
                accepted_now=False,
                simulated_acceptance_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_non_substitution_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    ns_by = {
        r.get("non_substitution_rule"): r
        for r in (artifacts.get("evidence_boundary_non_substitution_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for rule, forbidden, why, sev in NON_SUBSTITUTION:
        n = ns_by.get(rule, {})
        ok_row = n.get("enforced_now") is False and bool(n.get("forbidden_substitution") or forbidden)
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                non_substitution_rule=rule,
                forbidden_substitution=n.get("forbidden_substitution") or forbidden,
                required_non_claim=n.get("required_non_claim") or rule,
                severity=n.get("severity") or sev,
                simulated_check=ok_row,
                enforced_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_eligibility_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    el_by = {
        r.get("eligibility_condition"): r
        for r in (
            artifacts.get("evidence_to_success_claim_eligibility_planning_matrix_v1.json") or {}
        ).get("rows")
        or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cond, types, auth in ELIGIBILITY_CONDITIONS:
        e = el_by.get(cond, {})
        ok_row = (
            e.get("satisfied_now") is False
            and e.get("success_claim_allowed_now") is False
            and e.get("required_for_success_claim") is True
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                eligibility_condition=cond,
                required_for_success_claim=True,
                required_evidence_types=e.get("required_evidence_types") or types,
                required_authorization=e.get("required_authorization") or auth,
                required_review=e.get("required_review") is True,
                satisfied_now=False,
                success_claim_allowed_now=False,
                simulated_eligibility_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_usage_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu_by = {
        r.get("verifier_check_id"): r
        for r in (artifacts.get("evidence_verifier_usage_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, phases, fields, fail, sev in VERIFIER_CHECKS:
        v = vu_by.get(vid, {})
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
        for r in (artifacts.get("evidence_chain_non_claims_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scenario, non_claim in NON_CLAIM_SCENARIOS:
        n = nc_by.get(scenario, {})
        ok_row = (
            bool(n.get("required_non_claim"))
            and n.get("generated_now") is False
            and n.get("template_modified_now", n.get("phase_template_modified_now")) is False
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


def run_evidence_chain_governance_dryrun_v1(
    *,
    evidence_chain_governance_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(evidence_chain_governance_planning_root)
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
    if up_readiness.get("ready_for_evidence_chain_governance_dryrun") is not True:
        blockers.append("not ready_for_evidence_chain_governance_dryrun")
    if up_summary.get("evidence_chain_planning_only") is not True:
        blockers.append("upstream evidence_chain_planning_only not true")
    if up_summary.get("evidence_generated_now") is not False:
        blockers.append("evidence_generated_now must be false")
    if up_summary.get("runtime_evidence_generated_now") is not False:
        blockers.append("runtime_evidence_generated_now must be false")
    if up_summary.get("success_evidence_generated_now") is not False:
        blockers.append("success_evidence_generated_now must be false")
    if up_summary.get("evidence_accepted_for_success_claim_now") is not False:
        blockers.append("evidence_accepted_for_success_claim_now must be false")
    if up_summary.get("evidence_registry_generated_now") is not False:
        blockers.append("evidence_registry_generated_now must be false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("success_claim_allowed must be false")
    for flag in (
        "ready_for_evidence_generation",
        "ready_for_evidence_registry_generation",
        "ready_for_runtime_evidence_generation",
        "ready_for_success_evidence_generation",
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

    comp_rows, comp_pass = _build_completeness(artifacts)
    lifecycle_rows, lifecycle_pass = _build_lifecycle_dryrun(artifacts)
    source_rows, source_pass = _build_source_chain_dryrun(artifacts)
    usage_rows, usage_pass = _build_usage_scope_dryrun(artifacts)
    upgrade_rows, upgrade_pass = _build_upgrade_path_dryrun(artifacts)
    acceptance_rows, acceptance_pass = _build_acceptance_dryrun(artifacts)
    nonsub_rows, nonsub_pass = _build_non_substitution_dryrun(artifacts)
    eligibility_rows, eligibility_pass = _build_eligibility_dryrun(artifacts)
    verifier_rows, verifier_pass = _build_verifier_usage_dryrun(artifacts)
    nclaims_rows, nclaims_pass = _build_non_claims_dryrun(artifacts)

    dryrun_pass = (
        comp_pass
        and lifecycle_pass
        and source_pass
        and usage_pass
        and upgrade_pass
        and acceptance_pass
        and nonsub_pass
        and eligibility_pass
        and verifier_pass
        and nclaims_pass
        and not blockers
    )
    boundary_ok = dryrun_pass

    evidence_chain_governance_dryrun_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_evidence_chain_governance_dryrun_observed=up_readiness.get(
            "ready_for_evidence_chain_governance_dryrun"
        )
        is True,
    )

    evidence_planning_artifact_completeness_dryrun = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_dryrun_meta(),
    }
    evidence_lifecycle_consumption_dryrun = {
        "rows": lifecycle_rows,
        "row_count": len(lifecycle_rows),
        "all_pass": lifecycle_pass,
        **_dryrun_meta(),
    }
    evidence_source_chain_consumption_dryrun = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "all_pass": source_pass,
        **_dryrun_meta(),
    }
    evidence_usage_scope_dryrun = {
        "rows": usage_rows,
        "row_count": len(usage_rows),
        "all_pass": usage_pass,
        **_dryrun_meta(),
    }
    evidence_upgrade_path_dryrun = {
        "rows": upgrade_rows,
        "row_count": len(upgrade_rows),
        "all_pass": upgrade_pass,
        **_dryrun_meta(),
    }
    evidence_acceptance_policy_dryrun = {
        "rows": acceptance_rows,
        "row_count": len(acceptance_rows),
        "all_pass": acceptance_pass,
        **_dryrun_meta(),
    }
    evidence_non_substitution_dryrun = {
        "rows": nonsub_rows,
        "row_count": len(nonsub_rows),
        "all_pass": nonsub_pass,
        **_dryrun_meta(),
    }
    evidence_success_claim_eligibility_dryrun = {
        "rows": eligibility_rows,
        "row_count": len(eligibility_rows),
        "all_pass": eligibility_pass,
        **_dryrun_meta(),
    }
    evidence_verifier_usage_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    evidence_chain_non_claims_generation_dryrun = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_dryrun_meta(),
    }

    evidence_chain_dryrun_readiness_decision = {
        "ready_for_evidence_chain_governance_post_dryrun_review": boundary_ok,
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
        "evidence_chain_dryrun_completed": boundary_ok,
        "planning_artifact_completeness_dryrun_pass": comp_pass,
        "evidence_lifecycle_consumption_dryrun_pass": lifecycle_pass,
        "source_chain_consumption_dryrun_pass": source_pass,
        "usage_scope_dryrun_pass": usage_pass,
        "upgrade_path_dryrun_pass": upgrade_pass,
        "acceptance_policy_dryrun_pass": acceptance_pass,
        "non_substitution_dryrun_pass": nonsub_pass,
        "success_claim_eligibility_dryrun_pass": eligibility_pass,
        "verifier_usage_dryrun_pass": verifier_pass,
        "non_claims_generation_dryrun_pass": nclaims_pass,
        "evidence_generated_now": False,
        "success_evidence_generated_now": False,
        "runtime_evidence_generated_now": False,
        "evidence_accepted_for_success_claim_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "evidence_chain_governance_planning_input_loaded": upstream["loaded"],
        "lifecycle_type_count": len(lifecycle_rows),
        "source_chain_component_count": len(source_rows),
        "usage_scope_count": len(usage_rows),
        "upgrade_path_count": len(upgrade_rows),
        "acceptance_rule_count": len(acceptance_rows),
        "eligibility_count": len(eligibility_rows),
        "verifier_check_count": len(verifier_rows),
        "non_claims_count": len(nclaims_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "evidence_chain_governance_planning",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_dryrun_meta(),
            }
        ],
        "row_count": 1,
        **_dryrun_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "EVIDENCE_CHAIN_GOVERNANCE_DRYRUN_REQUIRES_FIXES",
        "reason": "evidence chain rules consumable in dry-run; no evidence generated; success claim blocked",
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "evidence_chain_governance_dryrun_policy": evidence_chain_governance_dryrun_policy,
        "evidence_planning_artifact_completeness_dryrun": evidence_planning_artifact_completeness_dryrun,
        "evidence_lifecycle_consumption_dryrun": evidence_lifecycle_consumption_dryrun,
        "evidence_source_chain_consumption_dryrun": evidence_source_chain_consumption_dryrun,
        "evidence_usage_scope_dryrun": evidence_usage_scope_dryrun,
        "evidence_upgrade_path_dryrun": evidence_upgrade_path_dryrun,
        "evidence_acceptance_policy_dryrun": evidence_acceptance_policy_dryrun,
        "evidence_non_substitution_dryrun": evidence_non_substitution_dryrun,
        "evidence_success_claim_eligibility_dryrun": evidence_success_claim_eligibility_dryrun,
        "evidence_verifier_usage_dryrun": evidence_verifier_usage_dryrun,
        "evidence_chain_non_claims_generation_dryrun": evidence_chain_non_claims_generation_dryrun,
        "evidence_chain_dryrun_readiness_decision": evidence_chain_dryrun_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
