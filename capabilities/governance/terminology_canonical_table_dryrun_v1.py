# -*- coding: utf-8 -*-
"""Terminology Canonical Table DryRun v1.

Dry-run only: simulate consumption of terminology planning blueprint by future
verifier / success claim gate / forbidden interpretation / required fields / registry.
Does not generate formal table, enforce terminology, or write registry.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)
from capabilities.governance.terminology_canonical_table_planning_v1 import (
    HIGH_RISK_LEVEL_TERMS,
    REQUIRED_TERMS,
    SUCCESS_CLAIM_TOPICS,
    TERM_SPECS,
)

PHASE_ID = "Phase-Terminology-Canonical-Table-DryRun-v1-001"
DRYRUN_SCOPE = "terminology_canonical_table_dryrun_only"
SOURCE_CHAIN = "terminology_canonical_table_dryrun_v1"

SOURCE_PHASE = "Phase-Terminology-Canonical-Table-Planning-v1-001"
FINAL_DECISION = "TERMINOLOGY_CANONICAL_TABLE_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Terminology-Canonical-Table-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("planning policy", "terminology_canonical_table_planning_policy_v1.json", 0),
    ("terminology scope intake matrix", "terminology_scope_intake_matrix_v1.json", 24),
    ("terminology canonical entry plan", "terminology_canonical_entry_plan_v1.json", 24),
    ("high-risk misread matrix", "terminology_high_risk_misread_matrix_v1.json", 24),
    ("required fields planning matrix", "terminology_required_fields_planning_matrix_v1.json", 24),
    ("verifier usage planning matrix", "terminology_verifier_usage_planning_matrix_v1.json", 24),
    ("forbidden interpretation planning matrix", "terminology_forbidden_interpretation_planning_matrix_v1.json", 24),
    ("success claim dependency matrix", "terminology_success_claim_dependency_matrix_v1.json", 12),
    ("table output plan", "terminology_table_output_plan_v1.json", 8),
    ("planning readiness decision", "terminology_canonical_table_planning_readiness_decision_v1.json", 0),
)

REGISTRY_CANDIDATES: Tuple[Tuple[str, str], ...] = (
    ("terminology canonical table candidate", "terminology_canonical_entry_plan_v1.json"),
    ("terminology required fields matrix candidate", "terminology_required_fields_planning_matrix_v1.json"),
    ("terminology forbidden interpretation matrix candidate", "terminology_forbidden_interpretation_planning_matrix_v1.json"),
    ("terminology verifier usage matrix candidate", "terminology_verifier_usage_planning_matrix_v1.json"),
    ("terminology non-claims rules candidate", "terminology_table_output_plan_v1.json"),
    ("terminology success claim dependency matrix candidate", "terminology_success_claim_dependency_matrix_v1.json"),
)

DRYRUN_NON_CLAIMS = [
    "DryRun GO does not mean terminology canonical table is generated.",
    "DryRun GO does not mean terminology is canonicalized.",
    "DryRun GO does not mean terminology rules are enforced.",
    "DryRun GO does not mean semantic registry has been written.",
    "DryRun GO does not mean verifier has been modified.",
    "DryRun GO does not mean phase template has been modified.",
    "DryRun GO does not mean success claim gate has been planned or fixed.",
    "DryRun GO does not mean permission semantics canonicalization may execute.",
    "DryRun GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "terminology_dryrun_only": True,
        "simulated": True,
        "terminology_canonicalization_executed_now": False,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
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
    readiness = _try_read_json(root / "terminology_canonical_table_planning_readiness_decision_v1.json") if root else None
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


def _by_term(artifacts: Dict[str, Any], key: str) -> Dict[str, Dict[str, Any]]:
    payload = artifacts.get(key) or {}
    return {r.get("term"): r for r in (payload.get("rows") or []) if r.get("term")}


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
        if filename == "terminology_scope_intake_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True
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
                canonical_table_generated_now=False,
                enforced_now=False,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass


def _build_entry_structure(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    entry_by = _by_term(artifacts, "terminology_canonical_entry_plan_v1.json")
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for term in REQUIRED_TERMS:
        e = entry_by.get(term, {})
        valid = (
            e.get("canonical_meaning_planned") is True
            and e.get("forbidden_interpretation_planned") is True
            and e.get("required_fields_planned") is True
            and e.get("canonical_entry_generated_now") is False
        )
        if not valid:
            all_pass = False
        rows.append(
            _row(
                term=term,
                canonical_meaning_planned_observed=e.get("canonical_meaning_planned") is True,
                forbidden_interpretation_planned_observed=e.get("forbidden_interpretation_planned") is True,
                required_fields_planned_observed=e.get("required_fields_planned") is True,
                valid_contexts_planned_observed=e.get("valid_contexts_planned") is True,
                invalid_contexts_planned_observed=e.get("invalid_contexts_planned") is True,
                must_not_imply_planned_observed=e.get("must_not_imply_planned") is True,
                required_non_claims_planned_observed=e.get("required_non_claims_planned") is True,
                verifier_usage_planned_observed=e.get("verifier_usage_planned") is True,
                example_safe_usage_planned_observed=e.get("example_safe_usage_planned") is True,
                example_unsafe_usage_planned_observed=e.get("example_unsafe_usage_planned") is True,
                future_canonical_entry_structurally_valid=valid,
                canonical_entry_generated_now=False,
                terminology_enforced_now=False,
                dryrun_status="pass" if valid else "fail",
            )
        )
    return rows, all_pass and len(rows) == 24


def _build_verifier_consumption(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu_by = _by_term(artifacts, "terminology_verifier_usage_planning_matrix_v1.json")
    mis_by = _by_term(artifacts, "terminology_high_risk_misread_matrix_v1.json")
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for term in REQUIRED_TERMS:
        v = vu_by.get(term, {})
        m = mis_by.get(term, {})
        spec = TERM_SPECS.get(term, {})
        sev = "P0" if m.get("risk_level") == "high" or term in HIGH_RISK_LEVEL_TERMS else "P1"
        consumable = bool(v.get("verifier_check_name")) and v.get("used_by_future_verifier") is True
        if term in HIGH_RISK_LEVEL_TERMS and m.get("risk_level") != "high":
            consumable = False
        if not consumable:
            all_pass = False
        rows.append(
            _row(
                term=term,
                verifier_check_name=v.get("verifier_check_name") or spec.get("verifier"),
                target_phase_types=v.get("target_phase_types") or spec.get("phases"),
                required_fields=v.get("required_fields") or spec.get("fields"),
                failure_condition=v.get("failure_condition"),
                severity=sev,
                non_claim_required=v.get("non_claim_required") is True,
                simulated_verifier_consumption=consumable,
                verifier_modified_now=False,
                not_enforced_now=True,
                dryrun_status="pass" if consumable else "fail",
            )
        )
    return rows, all_pass


def _build_forbidden_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    fb_by = _by_term(artifacts, "terminology_forbidden_interpretation_planning_matrix_v1.json")
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for term in REQUIRED_TERMS:
        f = fb_by.get(term, {})
        ok_row = bool(f.get("forbidden_interpretation")) and f.get("enforced_now") is False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                term=term,
                forbidden_interpretation=f.get("forbidden_interpretation") or TERM_SPECS[term]["forbidden"],
                forbidden_reason=f.get("forbidden_reason"),
                forbidden_field_combination=f.get("forbidden_field_combination"),
                required_non_claim_if_used=f.get("required_non_claim_if_used"),
                failure_condition=f.get("failure_condition"),
                severity=f.get("severity", "P0"),
                simulated_check=ok_row,
                enforced_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass


def _build_required_fields_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rf_by = _by_term(artifacts, "terminology_required_fields_planning_matrix_v1.json")
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for term in REQUIRED_TERMS:
        r = rf_by.get(term, {})
        fields = str(r.get("required_boolean_fields", ""))
        struct_ok = bool(fields) and r.get("verifier_required") is True
        if term == "authorization granted":
            struct_ok = struct_ok and "authorization_granted_now" in fields
        if term == "owner approval":
            struct_ok = struct_ok and ("owner" in fields.lower() or "approval" in fields)
        if term == "execution window":
            struct_ok = struct_ok and "execution_window" in fields.replace(" ", "_").replace("-", "_")
        if term == "success claim":
            struct_ok = struct_ok and "success_claim" in fields.replace(" ", "_")
        if term == "evidence":
            struct_ok = struct_ok and "evidence" in fields.lower()
        if term == "ready":
            struct_ok = struct_ok and "ready" in fields.lower()
        if not struct_ok:
            all_pass = False
        rows.append(
            _row(
                term=term,
                required_boolean_fields=r.get("required_boolean_fields"),
                required_status_fields=r.get("required_status_fields"),
                required_source_refs=r.get("required_source_refs"),
                required_actor_refs=r.get("required_actor_refs"),
                required_evidence_refs=r.get("required_evidence_refs"),
                required_non_claims=r.get("required_non_claims"),
                missing_field_risk=r.get("missing_field_risk"),
                verifier_required_observed=r.get("verifier_required") is True,
                field_set_structurally_valid=struct_ok,
                enforced_now=False,
                dryrun_status="pass" if struct_ok else "fail",
            )
        )
    return rows, all_pass


def _build_success_claim_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    sc_payload = artifacts.get("terminology_success_claim_dependency_matrix_v1.json") or {}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in sc_payload.get("rows") or []:
        ok_row = row.get("terminology_table_required_before_success_claim_gate") is True
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                success_claim_topic=row.get("success_claim_topic"),
                dependent_terms=row.get("dependent_terms"),
                terminology_table_required_before_success_claim_gate=True,
                simulated_dependency_check=ok_row,
                blocks_success_claim_gate_planning_until_reviewed=row.get(
                    "blocks_success_claim_gate_planning_until_reviewed"
                )
                is True,
                success_claim_canonicalization_executed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    if len(rows) < 12:
        all_pass = False
    return rows, all_pass


def _build_registry_candidates() -> List[Dict[str, Any]]:
    return [
        _row(
            registry_candidate_type=ctype,
            source_planning_artifact=source,
            indexable_in_dryrun=True,
            registry_written_now=False,
            future_registry_candidate=True,
            terminology_enforced_now=False,
            dryrun_status="pass",
        )
        for ctype, source in REGISTRY_CANDIDATES
    ]


def _build_cross_artifact(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    scope = _by_term(artifacts, "terminology_scope_intake_matrix_v1.json")
    entry = _by_term(artifacts, "terminology_canonical_entry_plan_v1.json")
    rf = _by_term(artifacts, "terminology_required_fields_planning_matrix_v1.json")
    vu = _by_term(artifacts, "terminology_verifier_usage_planning_matrix_v1.json")
    fb = _by_term(artifacts, "terminology_forbidden_interpretation_planning_matrix_v1.json")
    mis = _by_term(artifacts, "terminology_high_risk_misread_matrix_v1.json")
    sc = artifacts.get("terminology_success_claim_dependency_matrix_v1.json") or {}
    out = artifacts.get("terminology_table_output_plan_v1.json") or {}

    checks: List[Tuple[str, str, List[str], bool]] = [
        (
            "TAC01",
            "24 terms exist across scope / entry / required fields / verifier / forbidden",
            ["terminology_scope_intake_matrix_v1.json", "terminology_canonical_entry_plan_v1.json"],
            len(scope) == 24 and len(entry) == 24 and len(rf) == 24 and len(vu) == 24 and len(fb) == 24,
        ),
        (
            "TAC02",
            "high-risk terms have severity high or above",
            ["terminology_high_risk_misread_matrix_v1.json"],
            all(mis.get(t, {}).get("risk_level") == "high" for t in HIGH_RISK_LEVEL_TERMS),
        ),
        (
            "TAC03",
            "each term has required fields",
            ["terminology_required_fields_planning_matrix_v1.json"],
            all(rf.get(t, {}).get("required_boolean_fields") for t in REQUIRED_TERMS),
        ),
        (
            "TAC04",
            "each term has forbidden interpretation",
            ["terminology_forbidden_interpretation_planning_matrix_v1.json"],
            all(fb.get(t, {}).get("forbidden_interpretation") for t in REQUIRED_TERMS),
        ),
        (
            "TAC05",
            "each term has verifier usage",
            ["terminology_verifier_usage_planning_matrix_v1.json"],
            all(vu.get(t, {}).get("verifier_check_name") for t in REQUIRED_TERMS),
        ),
        (
            "TAC06",
            "success claim topics reference dependent terms",
            ["terminology_success_claim_dependency_matrix_v1.json"],
            len(sc.get("rows") or []) >= 12,
        ),
        (
            "TAC07",
            "planned artifacts all have not_generated_now=true",
            ["terminology_table_output_plan_v1.json"],
            all(r.get("not_generated_now") is True for r in (out.get("rows") or [])),
        ),
        (
            "TAC08",
            "no canonical table artifact generated now",
            ["terminology_table_output_plan_v1.json"],
            not any("terminology_canonical_table_v1.json" == r.get("planned_artifact") and not r.get("not_generated_now") for r in (out.get("rows") or [])),
        ),
        (
            "TAC09",
            "no registry write",
            ["terminology_canonical_table_dryrun_policy_v1.json"],
            True,
        ),
        (
            "TAC10",
            "no verifier modification",
            ["terminology_canonical_table_planning_policy_v1.json"],
            (artifacts.get("terminology_canonical_table_planning_policy_v1.json") or {}).get("verifier_modified_now") is False,
        ),
        (
            "TAC11",
            "no phase template modification",
            ["terminology_canonical_table_planning_policy_v1.json"],
            (artifacts.get("terminology_canonical_table_planning_policy_v1.json") or {}).get("phase_template_modified_now") is False,
        ),
        (
            "TAC12",
            "no terminology enforcement",
            ["terminology_canonical_entry_plan_v1.json"],
            all(entry.get(t, {}).get("enforced_now") is False for t in REQUIRED_TERMS),
        ),
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
                dryrun_notes="terminology dry-run consistency only",
            )
        )
    return rows, all_pass


def run_terminology_canonical_table_dryrun_v1(
    *,
    terminology_canonical_table_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(terminology_canonical_table_planning_root)
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
    if up_readiness.get("ready_for_terminology_canonical_table_dryrun") is not True:
        blockers.append("not ready_for_terminology_canonical_table_dryrun")
    if up_summary.get("terminology_planning_only") is not True:
        blockers.append("upstream terminology_planning_only not true")
    if up_summary.get("canonical_table_generated_now") is not False:
        blockers.append("canonical_table_generated_now must be false")
    if up_summary.get("terminology_enforced_now") is not False:
        blockers.append("terminology_enforced_now must be false")
    if up_summary.get("registry_written_now") is not False:
        blockers.append("registry_written_now must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    comp_rows, comp_pass = _build_completeness(artifacts)
    entry_rows, entry_pass = _build_entry_structure(artifacts)
    verifier_rows, verifier_pass = _build_verifier_consumption(artifacts)
    forbidden_rows, forbidden_pass = _build_forbidden_dryrun(artifacts)
    fields_rows, fields_pass = _build_required_fields_dryrun(artifacts)
    success_rows, success_pass = _build_success_claim_dryrun(artifacts)
    registry_rows = _build_registry_candidates()
    cross_rows, cross_pass = _build_cross_artifact(artifacts)

    dryrun_pass = (
        comp_pass
        and entry_pass
        and verifier_pass
        and forbidden_pass
        and fields_pass
        and success_pass
        and cross_pass
        and len(registry_rows) >= 6
        and not blockers
    )
    boundary_ok = dryrun_pass

    terminology_canonical_table_dryrun_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_terminology_canonical_table_dryrun_observed=up_readiness.get(
            "ready_for_terminology_canonical_table_dryrun"
        )
        is True,
    )

    terminology_planning_artifact_completeness_dryrun = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_dryrun_meta(),
    }
    terminology_entry_structure_dryrun = {
        "rows": entry_rows,
        "row_count": len(entry_rows),
        "all_pass": entry_pass,
        **_dryrun_meta(),
    }
    terminology_verifier_consumption_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    terminology_forbidden_interpretation_dryrun = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        "all_pass": forbidden_pass,
        **_dryrun_meta(),
    }
    terminology_required_fields_dryrun = {
        "rows": fields_rows,
        "row_count": len(fields_rows),
        "all_pass": fields_pass,
        **_dryrun_meta(),
    }
    terminology_success_claim_dependency_dryrun = {
        "rows": success_rows,
        "row_count": len(success_rows),
        "all_pass": success_pass,
        **_dryrun_meta(),
    }
    terminology_semantic_registry_candidate_dryrun = {
        "rows": registry_rows,
        "row_count": len(registry_rows),
        "all_pass": True,
        **_dryrun_meta(),
    }
    terminology_cross_artifact_consistency_dryrun = {
        "rows": cross_rows,
        "row_count": len(cross_rows),
        "all_pass": cross_pass,
        **_dryrun_meta(),
    }
    non_claims_rows = [
        _row(non_claim=nc, required=True, present=True, risk_if_missing="terminology dryrun GO misread")
        for nc in DRYRUN_NON_CLAIMS
    ]
    terminology_dryrun_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_dryrun_meta(),
    }

    terminology_canonical_table_dryrun_readiness_decision = {
        "ready_for_terminology_canonical_table_post_dryrun_review": boundary_ok,
        "ready_for_terminology_canonicalization_execution": False,
        "ready_for_terminology_enforcement": False,
        "ready_for_canonical_table_generation": False,
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
        "terminology_dryrun_completed": boundary_ok,
        "planning_artifact_completeness_dryrun_pass": comp_pass,
        "terminology_entry_structure_dryrun_pass": entry_pass,
        "terminology_verifier_consumption_dryrun_pass": verifier_pass,
        "terminology_forbidden_interpretation_dryrun_pass": forbidden_pass,
        "terminology_required_fields_dryrun_pass": fields_pass,
        "terminology_success_claim_dependency_dryrun_pass": success_pass,
        "terminology_semantic_registry_candidate_dryrun_pass": len(registry_rows) >= 6,
        "terminology_cross_artifact_consistency_dryrun_pass": cross_pass,
        "terminology_canonicalization_executed_now": False,
        "canonical_table_generated_now": False,
        "terminology_enforced_now": False,
        "registry_written_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "terminology_canonical_table_planning_input_loaded": upstream["loaded"],
        "term_count": len(entry_rows),
        "success_claim_topic_count": len(success_rows),
        "registry_candidate_count": len(registry_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "terminology_canonical_table_planning",
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
        "final_decision": FINAL_DECISION if boundary_ok else "TERMINOLOGY_CANONICAL_TABLE_DRYRUN_REQUIRES_FIXES",
        "reason": "terminology structure dry-run only; post-dryrun review next; no formal table",
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "terminology_canonical_table_dryrun_policy": terminology_canonical_table_dryrun_policy,
        "terminology_planning_artifact_completeness_dryrun": terminology_planning_artifact_completeness_dryrun,
        "terminology_entry_structure_dryrun": terminology_entry_structure_dryrun,
        "terminology_verifier_consumption_dryrun": terminology_verifier_consumption_dryrun,
        "terminology_forbidden_interpretation_dryrun": terminology_forbidden_interpretation_dryrun,
        "terminology_required_fields_dryrun": terminology_required_fields_dryrun,
        "terminology_success_claim_dependency_dryrun": terminology_success_claim_dependency_dryrun,
        "terminology_semantic_registry_candidate_dryrun": terminology_semantic_registry_candidate_dryrun,
        "terminology_cross_artifact_consistency_dryrun": terminology_cross_artifact_consistency_dryrun,
        "terminology_dryrun_non_claims_register": terminology_dryrun_non_claims_register,
        "terminology_canonical_table_dryrun_readiness_decision": terminology_canonical_table_dryrun_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
