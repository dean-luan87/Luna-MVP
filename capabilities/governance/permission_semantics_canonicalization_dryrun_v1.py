# -*- coding: utf-8 -*-
"""Permission Semantics Canonicalization DryRun v1.

Dry-run only: simulate consumption of planning semantics blueprint by future
verifier / phase template / readiness / success claim / non-claims chains.
Does not enforce semantics, modify verifiers/templates, or release authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001"
DRYRUN_SCOPE = "permission_semantics_canonicalization_dryrun_only"
DRYRUN_ID = "permission_semantics_canonicalization_dryrun_v1_001"
SOURCE_CHAIN = "permission_semantics_canonicalization_dryrun_v1"

SOURCE_PHASE = "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "PERMISSION_SEMANTICS_CANONICALIZATION_PLANNING_READY_FOR_DRYRUN"

FINAL_DECISION = "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("planning policy", "permission_semantics_canonicalization_planning_policy_v1.json", 0),
    ("phase type semantics table", "phase_type_semantics_table_v1.json", 14),
    ("permission state semantics table", "permission_state_semantics_table_v1.json", 10),
    ("authorization state semantics table", "authorization_state_semantics_table_v1.json", 12),
    ("execution state semantics table", "execution_state_semantics_table_v1.json", 12),
    ("artifact state semantics table", "artifact_state_semantics_table_v1.json", 12),
    ("readiness state semantics table", "readiness_state_semantics_table_v1.json", 12),
    ("result state semantics table", "result_state_semantics_table_v1.json", 12),
    ("route state semantics table", "route_state_semantics_table_v1.json", 10),
    ("forbidden state combination matrix", "forbidden_state_combination_matrix_v1.json", 20),
    ("development norms matrix", "development_norms_matrix_v1.json", 12),
    ("verifier semantics checklist", "verifier_semantics_checklist_v1.json", 20),
    ("non-claims generation rules", "non_claims_generation_rules_v1.json", 20),
    ("readiness decision", "permission_semantics_canonicalization_planning_readiness_decision_v1.json", 0),
)

REGISTRY_GROUPS: Tuple[Tuple[str, str], ...] = (
    ("phase type", "phase_type_semantics_table_v1.json"),
    ("permission state", "permission_state_semantics_table_v1.json"),
    ("authorization state", "authorization_state_semantics_table_v1.json"),
    ("execution state", "execution_state_semantics_table_v1.json"),
    ("artifact state", "artifact_state_semantics_table_v1.json"),
    ("readiness state", "readiness_state_semantics_table_v1.json"),
    ("result state", "result_state_semantics_table_v1.json"),
    ("route state", "route_state_semantics_table_v1.json"),
)

READINESS_TERMS_REQUIRED = (
    "ready_for_planning",
    "ready_for_dryrun",
    "ready_for_review",
    "ready_for_post_review",
    "ready_for_roadmap_decision",
    "ready_for_register",
    "ready_for_post_register_review",
    "ready_for_authorization_planning",
    "ready_for_authorization_request",
    "ready_for_execution_planning",
    "ready_for_real_execution",
    "not_ready",
)

SUCCESS_CLAIM_RULES: Tuple[Tuple[str, str, str], ...] = (
    ("GO 不得 imply success", "GO", "success/succeeded"),
    ("completed 不得 imply succeeded", "completed", "succeeded"),
    ("reviewed 不得 imply accepted", "reviewed", "accepted"),
    ("boundary_ok 不得 imply execution safe", "boundary_ok", "execution safe"),
    ("success_claim_allowed 必须独立 gate", "success_claim_allowed", "auto from GO"),
    ("success_claim_blocked 必须保留 non-claim", "success_claim_blocked", "silent pass"),
    ("success evidence 必须不同于 summary", "success_claim_evidence", "summary text"),
    ("runtime evidence 必须不同于 verifier_report", "runtime_evidence", "verifier_report"),
)

DRYRUN_NON_CLAIMS = [
    "DryRun GO does not mean semantics are canonicalized.",
    "DryRun GO does not mean semantics are enforced.",
    "DryRun GO does not mean verifier has been modified.",
    "DryRun GO does not mean phase template has been modified.",
    "DryRun GO does not mean future phase outputs are auto-generated.",
    "DryRun GO does not mean forbidden combinations are enforced.",
    "DryRun GO does not mean non-claims are automatically generated.",
    "DryRun GO does not mean governance debt is fixed.",
    "DryRun GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "canonicalization_dryrun_only": True,
        "simulated": True,
        "canonicalization_executed_now": False,
        "canonicalization_enforced_now": False,
        "not_enforced_now": True,
        "debt_fix_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
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


def _dryrun_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_dryrun_meta()}


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
        root / "permission_semantics_canonicalization_planning_readiness_decision_v1.json"
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


def _row_count(payload: Dict[str, Any]) -> int:
    if "row_count" in payload:
        return int(payload["row_count"])
    rows = payload.get("rows")
    return len(rows) if isinstance(rows, list) else 0


def _build_artifact_completeness(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for name, filename, min_count in PLANNING_ARTIFACTS:
        payload = artifacts.get(filename)
        observed = payload is not None
        count = _row_count(payload) if isinstance(payload, dict) else 0
        schema_ok = observed and isinstance(payload, dict)
        count_ok = min_count == 0 or count >= min_count
        semantic_ok = schema_ok and (min_count == 0 or count_ok)
        consumable = observed and schema_ok and count_ok and semantic_ok
        if not consumable:
            all_pass = False
        rows.append(
            _dryrun_row(
                artifact_name=name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_ok,
                count_requirement_pass=count_ok,
                semantic_requirement_pass=semantic_ok,
                dryrun_consumable=consumable,
                enforced_now=False,
                dryrun_status="pass" if consumable else "fail",
                observed_count=count,
                minimum_count=min_count,
            )
        )
    return rows, all_pass


def _build_registry_index(artifacts: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for group, filename in REGISTRY_GROUPS:
        payload = artifacts.get(filename) or {}
        count = _row_count(payload)
        rows.append(
            _dryrun_row(
                registry_group=group,
                source_artifact=filename,
                term_count=count,
                indexable_in_dryrun=count > 0,
                registry_written_now=False,
                future_registry_candidate=True,
                canonicalization_enforced_now=False,
                dryrun_notes=f"simulated index for {group}; no registry write",
            )
        )
    return rows


def _build_forbidden_mapping(forbidden: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in forbidden.get("rows") or []:
        mapped = bool(row.get("required_verifier_check"))
        status = "pass" if mapped else "fail"
        if not mapped:
            all_pass = False
        rows.append(
            _dryrun_row(
                forbidden_combination_id=row.get("forbidden_combination_id"),
                state_a=row.get("state_a"),
                state_b=row.get("state_b"),
                failure_condition=row.get("failure_condition"),
                expected_error_level=row.get("expected_error_level"),
                mapped_to_verifier_check=mapped,
                verifier_modified_now=False,
                enforced_now=False,
                dryrun_check_behavior=f"simulate check {row.get('required_verifier_check')}",
                dryrun_status=status,
            )
        )
    return rows, all_pass and len(rows) >= 20


def _build_norms_mapping(norms: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in norms.get("rows") or []:
        mapped = bool(row.get("norm_id") and row.get("required_fields"))
        status = "pass" if mapped else "fail"
        if not mapped:
            all_pass = False
        rows.append(
            _dryrun_row(
                norm_id=row.get("norm_id"),
                norm_name=row.get("norm_name"),
                target_phase_types=row.get("target_phase_types"),
                required_fields=row.get("required_fields"),
                forbidden_patterns=row.get("forbidden_patterns"),
                mapped_to_future_phase_template=mapped,
                phase_template_modified_now=False,
                enforced_now=False,
                dryrun_status=status,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_consumption(checklist: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in checklist.get("rows") or []:
        consumable = bool(row.get("check_id") and row.get("check_name"))
        not_enforced = row.get("not_enforced_now") is True
        status = "pass" if consumable and not_enforced else "fail"
        if status != "pass":
            all_pass = False
        rows.append(
            _dryrun_row(
                check_id=row.get("check_id"),
                check_name=row.get("check_name"),
                target_phase_types=row.get("target_phase_types"),
                required_fields=row.get("required_fields"),
                failure_condition=row.get("failure_condition"),
                severity=row.get("severity"),
                simulated_consumption=consumable,
                verifier_modified_now=False,
                not_enforced_now=True,
                dryrun_status=status,
            )
        )
    return rows, all_pass and len(rows) >= 20


def _build_non_claims_dryrun(rules: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in rules.get("rows") or []:
        sim_ok = bool(row.get("scenario") and row.get("required_non_claim"))
        status = "pass" if sim_ok else "fail"
        if not sim_ok:
            all_pass = False
        rows.append(
            _dryrun_row(
                scenario=row.get("scenario"),
                required_non_claim=row.get("required_non_claim"),
                target_outputs={
                    "summary": row.get("must_be_in_summary") is True,
                    "verifier_report": row.get("must_be_in_verifier_report") is True,
                    "phase_documentation": row.get("used_by_future_phase_template") is True,
                },
                simulated_generation=sim_ok,
                generated_now=False,
                template_modified_now=False,
                not_enforced_now=True,
                dryrun_status=status,
            )
        )
    return rows, all_pass and len(rows) >= 20


def _build_readiness_validation(readiness_table: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by_term = {r.get("term"): r for r in (readiness_table.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for term in READINESS_TERMS_REQUIRED:
        row = by_term.get(term, {})
        observed = bool(row)
        meaning = row.get("canonical_meaning", "")
        next_types = row.get("allowed_next_phase_types", "")
        not_impl = row.get("must_not_imply", "")
        validation_ok = observed and bool(meaning) and bool(next_types)
        if term == "ready_for_roadmap_decision":
            validation_ok = validation_ok and "execution" in str(not_impl).lower()
        if term == "ready_for_authorization_request":
            validation_ok = validation_ok and "authorization" in str(not_impl).lower()
        if term == "ready_for_real_execution":
            validation_ok = validation_ok and bool(row.get("required_preconditions"))
        if not validation_ok:
            all_pass = False
        rows.append(
            _dryrun_row(
                readiness_term=term,
                canonical_meaning_observed=meaning,
                allowed_next_phase_types_observed=next_types,
                must_not_imply_observed=not_impl,
                simulated_validation=validation_ok,
                enforced_now=False,
                dryrun_status="pass" if validation_ok else "fail",
            )
        )
    return rows, all_pass


def _build_success_claim_gate(result_table: Dict[str, Any], artifact_table: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    result_by_term = {r.get("term"): r for r in (result_table.get("rows") or [])}
    artifact_by_term = {r.get("term"): r for r in (artifact_table.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for rule, source_term, forbidden in SUCCESS_CLAIM_RULES:
        source = result_by_term.get(source_term) or artifact_by_term.get(source_term) or {}
        gate_ok = bool(source) or source_term in ("success_claim_evidence", "runtime_evidence")
        if source_term == "success_claim_allowed":
            gate_ok = "gate" in str(source.get("must_not_imply", "")).lower() or bool(source)
        if not gate_ok:
            all_pass = False
        rows.append(
            _dryrun_row(
                success_semantic_rule=rule,
                source_result_term=source_term,
                forbidden_implication=forbidden,
                gate_required=True,
                simulated_gate_check=gate_ok,
                success_claim_allowed_now=False,
                enforced_now=False,
                dryrun_status="pass" if gate_ok else "fail",
            )
        )
    return rows, all_pass


def _build_cross_artifact_consistency(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    forbidden = artifacts.get("forbidden_state_combination_matrix_v1.json") or {}
    norms = artifacts.get("development_norms_matrix_v1.json") or {}
    checklist = artifacts.get("verifier_semantics_checklist_v1.json") or {}
    nrules = artifacts.get("non_claims_generation_rules_v1.json") or {}
    readiness = artifacts.get("readiness_state_semantics_table_v1.json") or {}
    result = artifacts.get("result_state_semantics_table_v1.json") or {}
    route = artifacts.get("route_state_semantics_table_v1.json") or {}
    artifact = artifacts.get("artifact_state_semantics_table_v1.json") or {}
    auth = artifacts.get("authorization_state_semantics_table_v1.json") or {}
    execution = artifacts.get("execution_state_semantics_table_v1.json") or {}
    phase = artifacts.get("phase_type_semantics_table_v1.json") or {}

    checks: List[Tuple[str, str, List[str], bool]] = []

    fc_rows = forbidden.get("rows") or []
    checks.append(
        (
            "CAC01",
            "term exists in semantics table and referenced by forbidden matrix",
            ["forbidden_state_combination_matrix_v1.json", "phase_type_semantics_table_v1.json"],
            len(fc_rows) >= 20 and _row_count(phase) >= 14,
        )
    )
    norm_rows = norms.get("rows") or []
    vcheck_rows = checklist.get("rows") or []
    checks.append(
        (
            "CAC02",
            "required flag exists in development norm and verifier checklist",
            ["development_norms_matrix_v1.json", "verifier_semantics_checklist_v1.json"],
            len(norm_rows) >= 12 and len(vcheck_rows) >= 20,
        )
    )
    nrule_rows = nrules.get("rows") or []
    high_risk = {"planning", "dry-run", "review", "roadmap decision", "register", "real execution"}
    phase_types = {r.get("phase_type") for r in (phase.get("rows") or [])}
    checks.append(
        (
            "CAC03",
            "non-claim scenario exists for each high-risk phase type",
            ["non_claims_generation_rules_v1.json", "phase_type_semantics_table_v1.json"],
            len(nrule_rows) >= 20 and high_risk.issubset(phase_types),
        )
    )
    ready_rows = readiness.get("rows") or []
    checks.append(
        (
            "CAC04",
            "readiness term has allowed_next_phase_types",
            ["readiness_state_semantics_table_v1.json"],
            all(r.get("allowed_next_phase_types") for r in ready_rows),
        )
    )
    result_rows = result.get("rows") or []
    checks.append(
        (
            "CAC05",
            "result term has scope_limit",
            ["result_state_semantics_table_v1.json"],
            all(r.get("scope_limit") for r in result_rows),
        )
    )
    route_rows = route.get("rows") or []
    checks.append(
        (
            "CAC06",
            "route term has permission_impact_rules",
            ["route_state_semantics_table_v1.json"],
            all(r.get("permission_impact_rules") for r in route_rows),
        )
    )
    artifact_rows = artifact.get("rows") or []
    checks.append(
        (
            "CAC07",
            "artifact state has can_support_success_claim",
            ["artifact_state_semantics_table_v1.json"],
            all("can_support_success_claim" in r for r in artifact_rows),
        )
    )
    auth_rows = auth.get("rows") or []
    checks.append(
        (
            "CAC08",
            "authorization term has required_actor",
            ["authorization_state_semantics_table_v1.json"],
            all(r.get("required_actor") for r in auth_rows),
        )
    )
    exec_rows = execution.get("rows") or []
    checks.append(
        (
            "CAC09",
            "execution term has required_evidence",
            ["execution_state_semantics_table_v1.json"],
            all(r.get("required_evidence") for r in exec_rows),
        )
    )
    boundary_row = next((r for r in result_rows if r.get("term") == "boundary_ok"), {})
    checks.append(
        (
            "CAC10",
            "boundary_ok does not release execution",
            ["result_state_semantics_table_v1.json"],
            "execution" in str(boundary_row.get("must_not_imply", "")).lower(),
        )
    )
    sel_row = next((r for r in route_rows if r.get("term") == "selected_route"), {})
    checks.append(
        (
            "CAC11",
            "selected route does not release permission",
            ["route_state_semantics_table_v1.json"],
            "permission" in str(sel_row.get("must_not_imply", "")).lower()
            or "release" in str(sel_row.get("must_not_imply", "")).lower(),
        )
    )
    cand_row = next((r for r in artifact_rows if r.get("term") == "candidate_artifact"), {})
    checks.append(
        (
            "CAC12",
            "candidate artifact does not become executable artifact",
            ["artifact_state_semantics_table_v1.json"],
            cand_row.get("can_support_execution") is False,
        )
    )

    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cid, desc, sources, passed in checks:
        if not passed:
            all_pass = False
        rows.append(
            _dryrun_row(
                consistency_check_id=cid,
                check_description=desc,
                source_artifacts=sources,
                simulated_check=True,
                consistency_pass=passed,
                enforced_now=False,
                dryrun_notes="simulated cross-artifact consistency only",
            )
        )
    return rows, all_pass


def run_permission_semantics_canonicalization_dryrun_v1(
    *,
    permission_semantics_canonicalization_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(permission_semantics_canonicalization_planning_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream planning verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream planning boundary_ok is not true")
    if up_readiness.get("ready_for_permission_semantics_canonicalization_dryrun") is not True:
        blockers.append("upstream not ready_for_permission_semantics_canonicalization_dryrun")
    if up_summary.get("canonicalization_planning_only") is not True:
        blockers.append("upstream canonicalization_planning_only is not true")
    if up_summary.get("canonicalization_executed_now") is not False:
        blockers.append("upstream canonicalization_executed_now is not false")
    if up_summary.get("not_enforced_now") is not True:
        blockers.append("upstream not_enforced_now is not true")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    completeness_rows, completeness_pass = _build_artifact_completeness(artifacts)
    registry_rows = _build_registry_index(artifacts)
    forbidden_rows, forbidden_pass = _build_forbidden_mapping(
        artifacts.get("forbidden_state_combination_matrix_v1.json") or {}
    )
    norms_rows, norms_pass = _build_norms_mapping(artifacts.get("development_norms_matrix_v1.json") or {})
    verifier_rows, verifier_pass = _build_verifier_consumption(
        artifacts.get("verifier_semantics_checklist_v1.json") or {}
    )
    nclaims_rows, nclaims_pass = _build_non_claims_dryrun(
        artifacts.get("non_claims_generation_rules_v1.json") or {}
    )
    readiness_val_rows, readiness_pass = _build_readiness_validation(
        artifacts.get("readiness_state_semantics_table_v1.json") or {}
    )
    success_rows, success_pass = _build_success_claim_gate(
        artifacts.get("result_state_semantics_table_v1.json") or {},
        artifacts.get("artifact_state_semantics_table_v1.json") or {},
    )
    consistency_rows, consistency_pass = _build_cross_artifact_consistency(artifacts)

    dryrun_non_claims_rows = [
        _dryrun_row(non_claim=nc, required=True, present=True, risk_if_missing="dry-run GO misread")
        for nc in DRYRUN_NON_CLAIMS
    ]

    dryrun_pass = (
        completeness_pass
        and forbidden_pass
        and norms_pass
        and verifier_pass
        and nclaims_pass
        and readiness_pass
        and success_pass
        and consistency_pass
        and not blockers
    )
    boundary_ok = dryrun_pass and not blockers

    permission_semantics_canonicalization_dryrun_policy = _dryrun_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_permission_semantics_canonicalization_dryrun_observed=up_readiness.get(
            "ready_for_permission_semantics_canonicalization_dryrun"
        )
        is True,
    )

    semantics_artifact_completeness_dryrun = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_dryrun_meta(),
    }
    semantic_registry_dryrun_index = {
        "rows": registry_rows,
        "row_count": len(registry_rows),
        "group_count": len(registry_rows),
        **_dryrun_meta(),
    }
    forbidden_combination_verifier_mapping_dryrun = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        "all_pass": forbidden_pass,
        **_dryrun_meta(),
    }
    development_norms_phase_template_mapping_dryrun = {
        "rows": norms_rows,
        "row_count": len(norms_rows),
        "all_pass": norms_pass,
        **_dryrun_meta(),
    }
    verifier_checklist_consumption_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    non_claims_generation_dryrun = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_dryrun_meta(),
    }
    readiness_decision_semantic_validation_dryrun = {
        "rows": readiness_val_rows,
        "row_count": len(readiness_val_rows),
        "all_pass": readiness_pass,
        **_dryrun_meta(),
    }
    success_claim_semantic_gate_dryrun = {
        "rows": success_rows,
        "row_count": len(success_rows),
        "all_pass": success_pass,
        **_dryrun_meta(),
    }
    cross_artifact_consistency_dryrun = {
        "rows": consistency_rows,
        "row_count": len(consistency_rows),
        "all_pass": consistency_pass,
        **_dryrun_meta(),
    }
    semantics_dryrun_non_claims_register = {
        "rows": dryrun_non_claims_rows,
        "row_count": len(dryrun_non_claims_rows),
        "all_present": True,
        **_dryrun_meta(),
    }

    permission_semantics_canonicalization_dryrun_readiness_decision = {
        "ready_for_permission_semantics_canonicalization_post_dryrun_review": boundary_ok,
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
        "canonicalization_dryrun_completed": boundary_ok,
        "semantics_artifact_completeness_dryrun_pass": completeness_pass,
        "semantic_registry_dryrun_index_generated": len(registry_rows) >= 8,
        "forbidden_combination_verifier_mapping_dryrun_pass": forbidden_pass,
        "development_norms_phase_template_mapping_dryrun_pass": norms_pass,
        "verifier_checklist_consumption_dryrun_pass": verifier_pass,
        "non_claims_generation_dryrun_pass": nclaims_pass,
        "readiness_decision_semantic_validation_dryrun_pass": readiness_pass,
        "success_claim_semantic_gate_dryrun_pass": success_pass,
        "cross_artifact_consistency_dryrun_pass": consistency_pass,
        "canonicalization_executed_now": False,
        "canonicalization_enforced_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "permission_semantics_canonicalization_planning_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_ready_for_dryrun_observed": up_readiness.get(
            "ready_for_permission_semantics_canonicalization_dryrun"
        )
        is True,
        "artifact_completeness_count": len(completeness_rows),
        "registry_group_count": len(registry_rows),
        "forbidden_mapping_count": len(forbidden_rows),
        "development_norms_mapping_count": len(norms_rows),
        "verifier_checklist_consumption_count": len(verifier_rows),
        "non_claims_generation_count": len(nclaims_rows),
        "readiness_validation_count": len(readiness_val_rows),
        "success_claim_gate_count": len(success_rows),
        "cross_artifact_consistency_count": len(consistency_rows),
        "dryrun_non_claims_count": len(dryrun_non_claims_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "permission_semantics_canonicalization_planning",
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
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_REQUIRES_FIXES",
        "reason": "dry-run consumption simulated; semantics not enforced; post-dryrun review next",
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "permission_semantics_canonicalization_dryrun_policy": permission_semantics_canonicalization_dryrun_policy,
        "semantics_artifact_completeness_dryrun": semantics_artifact_completeness_dryrun,
        "semantic_registry_dryrun_index": semantic_registry_dryrun_index,
        "forbidden_combination_verifier_mapping_dryrun": forbidden_combination_verifier_mapping_dryrun,
        "development_norms_phase_template_mapping_dryrun": development_norms_phase_template_mapping_dryrun,
        "verifier_checklist_consumption_dryrun": verifier_checklist_consumption_dryrun,
        "non_claims_generation_dryrun": non_claims_generation_dryrun,
        "readiness_decision_semantic_validation_dryrun": readiness_decision_semantic_validation_dryrun,
        "success_claim_semantic_gate_dryrun": success_claim_semantic_gate_dryrun,
        "cross_artifact_consistency_dryrun": cross_artifact_consistency_dryrun,
        "semantics_dryrun_non_claims_register": semantics_dryrun_non_claims_register,
        "permission_semantics_canonicalization_dryrun_readiness_decision": permission_semantics_canonicalization_dryrun_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
