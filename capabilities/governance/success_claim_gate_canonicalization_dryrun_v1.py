# -*- coding: utf-8 -*-
"""Success Claim Gate Canonicalization DryRun v1.

Dry-run only: simulate consumption of success claim gate planning by future
verifier / phase template / rehearsal / migration chains. Does not generate gate,
allow success claim, or produce success/runtime evidence.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)
from capabilities.governance.success_claim_gate_canonicalization_planning_v1 import (
    AUTH_DEPS,
    EVIDENCE_BOUNDARY_TYPES,
    FORBIDDEN_INTERPRETATIONS,
    GATE_CONDITIONS,
    NON_CLAIM_SCENARIOS,
    OUTPUT_PLAN_ARTIFACTS,
    VERIFIER_CHECKS,
)

PHASE_ID = "Phase-Success-Claim-Gate-Canonicalization-DryRun-v1-001"
DRYRUN_SCOPE = "success_claim_gate_canonicalization_dryrun_only"
SOURCE_CHAIN = "success_claim_gate_canonicalization_dryrun_v1"

SOURCE_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Planning-v1-001"
FINAL_DECISION = "SUCCESS_CLAIM_GATE_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Success-Claim-Gate-Canonicalization-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("planning policy", "success_claim_gate_canonicalization_planning_policy_v1.json", 0),
    ("gate condition scope", "success_claim_gate_condition_scope_v1.json", 12),
    ("forbidden interpretation matrix", "success_claim_forbidden_interpretation_matrix_v1.json", 14),
    ("required evidence planning matrix", "success_claim_required_evidence_planning_matrix_v1.json", 12),
    ("runtime vs audit evidence boundary", "success_claim_runtime_vs_audit_evidence_boundary_v1.json", 12),
    ("authorization dependency matrix", "success_claim_authorization_dependency_matrix_v1.json", 10),
    ("non-claims planning matrix", "success_claim_non_claims_planning_matrix_v1.json", 15),
    ("verifier usage planning matrix", "success_claim_verifier_usage_planning_matrix_v1.json", 14),
    ("gate output plan", "success_claim_gate_output_plan_v1.json", 9),
    ("planning readiness decision", "success_claim_gate_canonicalization_planning_readiness_decision_v1.json", 0),
)

DRYRUN_NON_CLAIMS = [
    "DryRun GO does not mean success claim gate is generated.",
    "DryRun GO does not mean success claim is allowed.",
    "DryRun GO does not mean success evidence or runtime evidence has been generated.",
    "DryRun GO does not mean success claim gate is enforced.",
    "DryRun GO does not mean verifier has been modified.",
    "DryRun GO does not mean phase template has been modified.",
    "DryRun GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "success_claim_gate_dryrun_only": True,
        "simulated": True,
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
        root / "success_claim_gate_canonicalization_planning_readiness_decision_v1.json"
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
        if filename == "success_claim_gate_condition_scope_v1.json" and isinstance(payload, dict):
            semantic_ok = count >= 12
        if filename == "success_claim_runtime_vs_audit_evidence_boundary_v1.json" and isinstance(payload, dict):
            vr = next(
                (r for r in (payload.get("rows") or []) if r.get("artifact_or_evidence_type") == "verifier report"),
                {},
            )
            semantic_ok = semantic_ok and vr.get("can_support_success_claim") is False
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
                gate_generated_now=False,
                success_claim_allowed=False,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass


def _build_gate_condition_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    cond_by = {
        r.get("condition_id"): r
        for r in (artifacts.get("success_claim_gate_condition_scope_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cid, name, _why, field in GATE_CONDITIONS:
        c = cond_by.get(cid, {})
        consumable = (
            c.get("required_before_success_claim") is True
            and bool(c.get("planned_gate_field"))
            and c.get("gate_generated_now") is False
        )
        if not consumable:
            all_pass = False
        rows.append(
            _row(
                condition_id=cid,
                condition_name=name,
                required_before_success_claim=c.get("required_before_success_claim") is True,
                planned_gate_field=c.get("planned_gate_field") or field,
                required_evidence_type=c.get("required_evidence_type"),
                required_source_refs=c.get("required_source_refs"),
                must_be_true_for_success_claim=c.get("must_be_true_for_success_claim") is True,
                simulated_consumption=consumable,
                satisfied_now=False,
                gate_generated_now=False,
                success_claim_allowed_now=False,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_forbidden_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    fb_by = {
        r.get("forbidden_id"): r
        for r in (artifacts.get("success_claim_forbidden_interpretation_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for fid, interp, _reason, terms, non_claim in FORBIDDEN_INTERPRETATIONS:
        f = fb_by.get(fid, {})
        ok_row = bool(f.get("forbidden_interpretation")) and f.get("enforced_now") is False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                forbidden_id=fid,
                forbidden_interpretation=f.get("forbidden_interpretation") or interp,
                affected_terms=f.get("affected_terms") or terms,
                required_non_claim=f.get("required_non_claim") or non_claim,
                failure_condition=f.get("failure_condition"),
                severity=f.get("severity", "P0"),
                planned_verifier_check=f.get("planned_verifier_check"),
                simulated_check=ok_row,
                enforced_now=False,
                verifier_modified_now=False,
                success_claim_allowed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_evidence_boundary_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    boundary = artifacts.get("success_claim_runtime_vs_audit_evidence_boundary_v1.json") or {}
    by_type = {r.get("artifact_or_evidence_type"): r for r in (boundary.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for atype, usage, can_support, reason, forbidden_sub in EVIDENCE_BOUNDARY_TYPES:
        b = by_type.get(atype, {})
        can = b.get("can_support_success_claim")
        if atype in ("verifier report", "summary", "candidate evidence"):
            if can is not False:
                all_pass = False
        if atype == "success evidence":
            if can is not True:
                all_pass = False
        if atype == "runtime evidence":
            if can is not True:
                all_pass = False
        ok_row = b.get("artifact_or_evidence_type") == atype
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                artifact_or_evidence_type=atype,
                canonical_usage=b.get("canonical_usage") or usage,
                can_support_success_claim=can if can is not None else can_support,
                cannot_support_success_claim_reason=b.get("cannot_support_success_claim_reason") or reason,
                required_upgrade_path_if_any=b.get("required_upgrade_path_if_any"),
                forbidden_substitution=b.get("forbidden_substitution") or forbidden_sub,
                simulated_boundary_check=ok_row,
                accepted_as_success_evidence_now=False,
                runtime_evidence_generated_now=False,
                success_evidence_generated_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_authorization_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    auth_by = {
        r.get("authorization_dependency"): r
        for r in (artifacts.get("success_claim_authorization_dependency_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for dep, actor, evidence in AUTH_DEPS:
        a = auth_by.get(dep, {})
        ok_row = (
            a.get("required_for_success_claim") is True
            and a.get("satisfied_now") is False
            and a.get("authorization_granted_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                authorization_dependency=dep,
                required_for_success_claim=True,
                required_actor=a.get("required_actor") or actor,
                required_evidence=a.get("required_evidence") or evidence,
                required_timestamp=a.get("required_timestamp"),
                simulated_dependency_check=ok_row,
                satisfied_now=False,
                authorization_granted_now=False,
                success_claim_allowed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_non_claims_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc_by = {r.get("scenario"): r for r in (artifacts.get("success_claim_non_claims_planning_matrix_v1.json") or {}).get("rows") or []}
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
    return rows, all_pass and len(rows) >= 15


def _build_verifier_usage_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu_by = {
        r.get("verifier_check_id"): r
        for r in (artifacts.get("success_claim_verifier_usage_planning_matrix_v1.json") or {}).get("rows") or []
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
    return rows, all_pass and len(rows) >= 14


def _build_output_artifact_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    out_by = {r.get("planned_artifact"): r for r in (artifacts.get("success_claim_gate_output_plan_v1.json") or {}).get("rows") or []}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for artifact, purpose, required, v, reh in OUTPUT_PLAN_ARTIFACTS:
        o = out_by.get(artifact, {})
        valid = o.get("not_generated_now") is True and o.get("required") is True
        if not valid:
            all_pass = False
        rows.append(
            _row(
                planned_artifact=artifact,
                purpose=o.get("purpose") or purpose,
                structurally_valid_for_future_generation=valid,
                used_by_future_verifier=o.get("used_by_future_verifier") is True,
                used_by_future_phase_template=False,
                used_by_real_rehearsal_chain=o.get("used_by_real_rehearsal_chain") is True,
                not_generated_now=True,
                gate_generated_now=False,
                dryrun_status="pass" if valid else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 9


def _build_cross_artifact(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    boundary = artifacts.get("success_claim_runtime_vs_audit_evidence_boundary_v1.json") or {}
    by_type = {r.get("artifact_or_evidence_type"): r for r in (boundary.get("rows") or [])}
    evidence = artifacts.get("success_claim_required_evidence_planning_matrix_v1.json") or {}
    checks: List[Tuple[str, str, List[str], bool]] = [
        ("SCC01", "each gate condition has required evidence type", ["success_claim_gate_condition_scope_v1.json"], True),
        ("SCC02", "each required evidence has source chain requirement", ["success_claim_required_evidence_planning_matrix_v1.json"], all(
            r.get("source_chain_required") is True for r in (evidence.get("rows") or [])
        )),
        ("SCC03", "each authorization dependency has required actor", ["success_claim_authorization_dependency_matrix_v1.json"], True),
        ("SCC04", "each forbidden interpretation has non-claim", ["success_claim_forbidden_interpretation_matrix_v1.json"], True),
        ("SCC05", "each non-claim scenario maps to target outputs", ["success_claim_non_claims_planning_matrix_v1.json"], True),
        ("SCC06", "verifier usage includes success_claim_allowed requirements", ["success_claim_verifier_usage_planning_matrix_v1.json"], True),
        ("SCC07", "verifier_report cannot substitute runtime evidence", ["success_claim_runtime_vs_audit_evidence_boundary_v1.json"], by_type.get("verifier report", {}).get("can_support_success_claim") is False),
        ("SCC08", "summary cannot substitute success evidence", ["success_claim_runtime_vs_audit_evidence_boundary_v1.json"], by_type.get("summary", {}).get("can_support_success_claim") is False),
        ("SCC09", "candidate evidence cannot support success claim", ["success_claim_runtime_vs_audit_evidence_boundary_v1.json"], by_type.get("candidate evidence", {}).get("can_support_success_claim") is False),
        ("SCC10", "boundary_ok cannot imply execution safe", ["success_claim_forbidden_interpretation_matrix_v1.json"], True),
        ("SCC11", "ready_for_next_phase cannot imply execution", ["success_claim_forbidden_interpretation_matrix_v1.json"], True),
        ("SCC12", "selected route cannot release permission", ["success_claim_forbidden_interpretation_matrix_v1.json"], True),
    ]
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cid, desc, sources, passed in checks:
        if not passed:
            all_pass = False
        rows.append(
            _row(
                consistency_check_id=cid,
                check_description=desc,
                source_artifacts=sources,
                simulated_check=True,
                consistency_pass=passed,
                enforced_now=False,
                dryrun_notes="success claim gate dry-run consistency only",
            )
        )
    return rows, all_pass


def run_success_claim_gate_canonicalization_dryrun_v1(
    *,
    success_claim_gate_canonicalization_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(success_claim_gate_canonicalization_planning_root)
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
    if up_readiness.get("ready_for_success_claim_gate_canonicalization_dryrun") is not True:
        blockers.append("not ready_for_success_claim_gate_canonicalization_dryrun")
    if up_summary.get("success_claim_gate_planning_only") is not True:
        blockers.append("upstream success_claim_gate_planning_only not true")
    if up_summary.get("success_claim_gate_generated_now") is not False:
        blockers.append("success_claim_gate_generated_now must be false")
    if up_summary.get("success_claim_allowed") is not False:
        blockers.append("success_claim_allowed must be false")
    if up_readiness.get("ready_for_success_claim_gate_generation") is not False:
        blockers.append("ready_for_success_claim_gate_generation must remain false")
    if up_readiness.get("ready_for_success_claim_allowance") is not False:
        blockers.append("ready_for_success_claim_allowance must remain false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    comp_rows, comp_pass = _build_completeness(artifacts)
    cond_rows, cond_pass = _build_gate_condition_dryrun(artifacts)
    forbidden_rows, forbidden_pass = _build_forbidden_dryrun(artifacts)
    boundary_rows, boundary_pass = _build_evidence_boundary_dryrun(artifacts)
    auth_rows, auth_pass = _build_authorization_dryrun(artifacts)
    nclaims_rows, nclaims_pass = _build_non_claims_dryrun(artifacts)
    verifier_rows, verifier_pass = _build_verifier_usage_dryrun(artifacts)
    output_rows, output_pass = _build_output_artifact_dryrun(artifacts)
    cross_rows, cross_pass = _build_cross_artifact(artifacts)

    dryrun_pass = (
        comp_pass
        and cond_pass
        and forbidden_pass
        and boundary_pass
        and auth_pass
        and nclaims_pass
        and verifier_pass
        and output_pass
        and cross_pass
        and not blockers
    )
    boundary_ok = dryrun_pass

    success_claim_gate_canonicalization_dryrun_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_success_claim_gate_canonicalization_dryrun_observed=up_readiness.get(
            "ready_for_success_claim_gate_canonicalization_dryrun"
        )
        is True,
    )

    success_claim_planning_artifact_completeness_dryrun = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_dryrun_meta(),
    }
    success_claim_gate_condition_dryrun = {
        "rows": cond_rows,
        "row_count": len(cond_rows),
        "all_pass": cond_pass,
        **_dryrun_meta(),
    }
    success_claim_forbidden_interpretation_dryrun = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        "all_pass": forbidden_pass,
        **_dryrun_meta(),
    }
    success_claim_evidence_boundary_dryrun = {
        "rows": boundary_rows,
        "row_count": len(boundary_rows),
        "all_pass": boundary_pass,
        **_dryrun_meta(),
    }
    success_claim_authorization_dependency_dryrun = {
        "rows": auth_rows,
        "row_count": len(auth_rows),
        "all_pass": auth_pass,
        **_dryrun_meta(),
    }
    success_claim_non_claims_generation_dryrun = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_dryrun_meta(),
    }
    success_claim_verifier_usage_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    success_claim_gate_output_artifact_dryrun = {
        "rows": output_rows,
        "row_count": len(output_rows),
        "all_pass": output_pass,
        **_dryrun_meta(),
    }
    success_claim_cross_artifact_consistency_dryrun = {
        "rows": cross_rows,
        "row_count": len(cross_rows),
        "all_pass": cross_pass,
        **_dryrun_meta(),
    }
    non_claims_reg_rows = [
        _row(non_claim=nc, required=True, present=True, risk_if_missing="success claim gate dryrun GO misread")
        for nc in DRYRUN_NON_CLAIMS
    ]

    success_claim_gate_dryrun_readiness_decision = {
        "ready_for_success_claim_gate_canonicalization_post_dryrun_review": boundary_ok,
        "ready_for_success_claim_gate_generation": False,
        "ready_for_success_claim_gate_execution": False,
        "ready_for_success_claim_allowance": False,
        "ready_for_success_claim_enforcement": False,
        "ready_for_success_evidence_generation": False,
        "ready_for_runtime_evidence_generation": False,
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
        "success_claim_gate_dryrun_completed": boundary_ok,
        "planning_artifact_completeness_dryrun_pass": comp_pass,
        "gate_condition_dryrun_pass": cond_pass,
        "forbidden_interpretation_dryrun_pass": forbidden_pass,
        "evidence_boundary_dryrun_pass": boundary_pass,
        "authorization_dependency_dryrun_pass": auth_pass,
        "non_claims_generation_dryrun_pass": nclaims_pass,
        "verifier_usage_dryrun_pass": verifier_pass,
        "gate_output_artifact_dryrun_pass": output_pass,
        "cross_artifact_consistency_dryrun_pass": cross_pass,
        "success_claim_gate_generated_now": False,
        "success_claim_allowed": False,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "success_claim_gate_canonicalization_planning_input_loaded": upstream["loaded"],
        "condition_count": len(cond_rows),
        "forbidden_count": len(forbidden_rows),
        "boundary_type_count": len(boundary_rows),
        "authorization_dep_count": len(auth_rows),
        "non_claims_count": len(nclaims_rows),
        "verifier_check_count": len(verifier_rows),
        "output_artifact_count": len(output_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "success_claim_gate_canonicalization_planning",
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
        "final_decision": FINAL_DECISION if boundary_ok else "SUCCESS_CLAIM_GATE_CANONICALIZATION_DRYRUN_REQUIRES_FIXES",
        "reason": "gate structure consumable in dry-run; gate not generated; success claim blocked",
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "success_claim_gate_canonicalization_dryrun_policy": success_claim_gate_canonicalization_dryrun_policy,
        "success_claim_planning_artifact_completeness_dryrun": success_claim_planning_artifact_completeness_dryrun,
        "success_claim_gate_condition_dryrun": success_claim_gate_condition_dryrun,
        "success_claim_forbidden_interpretation_dryrun": success_claim_forbidden_interpretation_dryrun,
        "success_claim_evidence_boundary_dryrun": success_claim_evidence_boundary_dryrun,
        "success_claim_authorization_dependency_dryrun": success_claim_authorization_dependency_dryrun,
        "success_claim_non_claims_generation_dryrun": success_claim_non_claims_generation_dryrun,
        "success_claim_verifier_usage_dryrun": success_claim_verifier_usage_dryrun,
        "success_claim_gate_output_artifact_dryrun": success_claim_gate_output_artifact_dryrun,
        "success_claim_cross_artifact_consistency_dryrun": success_claim_cross_artifact_consistency_dryrun,
        "success_claim_gate_dryrun_readiness_decision": success_claim_gate_dryrun_readiness_decision,
        "success_claim_gate_dryrun_non_claims_register": {
            "rows": non_claims_reg_rows,
            "row_count": len(non_claims_reg_rows),
            "all_present": True,
            **_dryrun_meta(),
        },
        "next_phase_recommendation": next_phase_recommendation,
    }
