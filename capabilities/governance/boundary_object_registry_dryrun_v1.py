# -*- coding: utf-8 -*-
"""Boundary Object Registry DryRun v1.

Dry-run only: simulate consumption of boundary object registry planning by future
registry, owner/operator approval, evidence chain, rollback rehearsal, and migration chains.
Does not generate registry, register objects, or execute file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.boundary_object_registry_planning_v1 import (
    BOUNDARY_CATEGORIES,
    FILE_OPERATIONS,
    FORBIDDEN_SHORTCUTS,
    NON_CLAIM_SCENARIOS,
    PROTECTED_OBJECT_TYPES,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-DryRun-v1-001"
DRYRUN_SCOPE = "boundary_object_registry_dryrun_only"
SOURCE_CHAIN = "boundary_object_registry_dryrun_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-Planning-v1-001"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("planning policy", "boundary_object_registry_planning_policy_v1.json", 0),
    ("category planning matrix", "boundary_object_category_planning_matrix_v1.json", 16),
    ("read/write policy planning matrix", "boundary_object_read_write_policy_planning_matrix_v1.json", 16),
    ("migration policy planning matrix", "boundary_object_migration_policy_planning_matrix_v1.json", 16),
    ("evidence policy planning matrix", "boundary_object_evidence_policy_planning_matrix_v1.json", 16),
    ("rollback policy planning matrix", "boundary_object_rollback_policy_planning_matrix_v1.json", 16),
    ("protected and blocked object planning matrix", "protected_and_blocked_object_planning_matrix_v1.json", 12),
    ("owner/operator dependency matrix", "boundary_object_owner_operator_dependency_matrix_v1.json", 16),
    ("file operation policy planning matrix", "boundary_object_file_operation_policy_planning_matrix_v1.json", 14),
    ("forbidden shortcut matrix", "boundary_object_forbidden_shortcut_matrix_v1.json", 12),
    ("verifier usage planning matrix", "boundary_object_verifier_usage_planning_matrix_v1.json", 12),
    ("non-claims planning matrix", "boundary_object_non_claims_planning_matrix_v1.json", 12),
    ("registry output plan", "boundary_object_registry_output_plan_v1.json", 13),
    ("planning readiness decision", "boundary_object_registry_planning_readiness_decision_v1.json", 0),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "boundary_object_registry_dryrun_only": True,
        "simulated": True,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "protected_asset_modified_now": False,
        "human_review_queue_modified_now": False,
        "dnae_or_permanent_block_modified_now": False,
        "file_operation_executed_now": False,
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
        root / "boundary_object_registry_planning_readiness_decision_v1.json"
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
        if filename == "boundary_object_category_planning_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("registered_now") is False and r.get("registry_generated_now") is False
                for r in (payload.get("rows") or [])
            )
        if filename == "protected_and_blocked_object_planning_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("write_allowed_now") is False
                and r.get("move_allowed_now") is False
                and r.get("delete_allowed_now") is False
                and r.get("merge_allowed_now") is False
                for r in (payload.get("rows") or [])
            )
        if filename == "boundary_object_registry_output_plan_v1.json" and isinstance(payload, dict):
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


def _build_category_consumption(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("boundary_object_category_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, meaning, _why in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = (
            bool(p.get("canonical_meaning") or meaning)
            and p.get("registered_now") is False
            and p.get("registry_generated_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                canonical_meaning=p.get("canonical_meaning") or meaning,
                default_risk_level=p.get("default_risk_level", "P1"),
                simulated_registry_consumption=ok_row,
                registered_now=False,
                registry_generated_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_read_write_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("boundary_object_read_write_policy_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, _, _ in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = (
            p.get("write_allowed_now") is False
            and p.get("file_operation_allowed_now") is False
            and p.get("write_requires_boundary_registry") is True
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                read_allowed_by_default=p.get("read_allowed_by_default", True),
                write_allowed_by_default=p.get("write_allowed_by_default", False),
                write_requires_owner_approval=p.get("write_requires_owner_approval", True),
                write_requires_operator_acknowledgement=p.get("write_requires_operator_acknowledgement", True),
                write_requires_execution_window=p.get("write_requires_execution_window", True),
                write_requires_boundary_registry=p.get("write_requires_boundary_registry", True),
                write_allowed_now=False,
                file_operation_allowed_now=False,
                simulated_policy_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_migration_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("boundary_object_migration_policy_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, _, _ in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = p.get("migration_allowed_now") is False and p.get("migration_requires_owner_approval") is True
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                migration_allowed_by_default=p.get("migration_allowed_by_default", False),
                migration_requires_owner_approval=p.get("migration_requires_owner_approval", True),
                migration_requires_operator_acknowledgement=p.get("migration_requires_operator_acknowledgement", True),
                migration_requires_restore_map=p.get("migration_requires_restore_map", True),
                migration_requires_rollback_plan=p.get("migration_requires_rollback_plan", True),
                migration_requires_evidence_chain=p.get("migration_requires_evidence_chain", True),
                migration_allowed_now=False,
                simulated_policy_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_evidence_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("boundary_object_evidence_policy_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, _, _ in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = (
            p.get("evidence_generation_allowed_now") is False
            and p.get("success_evidence_allowed_now") is False
        )
        if cat in ("verifier artifacts", "eval_out artifacts") and p.get("can_be_success_evidence_source") is True:
            ok_row = False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                can_generate_evidence=p.get("can_generate_evidence", False),
                can_be_evidence_source=p.get("can_be_evidence_source", False),
                can_be_success_evidence_source=False,
                requires_source_chain=p.get("requires_source_chain", True),
                requires_evidence_acceptance=p.get("requires_evidence_acceptance", True),
                requires_owner_operator_authorization=p.get("requires_owner_operator_authorization", True),
                evidence_generation_allowed_now=False,
                success_evidence_allowed_now=False,
                simulated_policy_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_rollback_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("boundary_object_rollback_policy_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, _, _ in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = (
            p.get("rollback_allowed_now") is False and p.get("restore_operation_allowed_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                requires_restore_map=p.get("requires_restore_map", True),
                requires_checkpoint=p.get("requires_checkpoint", True),
                requires_pre_change_snapshot=p.get("requires_pre_change_snapshot", True),
                requires_owner_operator_authorization=p.get("requires_owner_operator_authorization", True),
                rollback_allowed_now=False,
                restore_operation_allowed_now=False,
                simulated_policy_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_protected_blocked_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("protected_object_type"): r
        for r in (artifacts.get("protected_and_blocked_object_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for obj_type, _why in PROTECTED_OBJECT_TYPES:
        p = by.get(obj_type, {})
        ok_row = (
            p.get("write_allowed_now") is False
            and p.get("move_allowed_now") is False
            and p.get("delete_allowed_now") is False
            and p.get("merge_allowed_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                protected_object_type=obj_type,
                read_allowed=p.get("read_allowed", True),
                write_allowed_now=False,
                move_allowed_now=False,
                delete_allowed_now=False,
                merge_allowed_now=False,
                requires_owner_approval=p.get("requires_owner_approval", True),
                requires_operator_acknowledgement=p.get("requires_operator_acknowledgement", True),
                requires_boundary_registry=p.get("requires_boundary_registry", True),
                simulated_block_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_owner_operator_dependency_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("boundary_object_owner_operator_dependency_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, _, _ in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = (
            p.get("dependency_satisfied_now") is False and p.get("authorization_granted_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                requires_owner_approval_for_write=p.get("requires_owner_approval_for_write", True),
                requires_operator_acknowledgement_for_write=p.get("requires_operator_acknowledgement_for_write", True),
                requires_execution_window_for_write=p.get("requires_execution_window_for_write", True),
                requires_scope_confirmation=p.get("requires_scope_confirmation", True),
                requires_abort_authority=p.get("requires_abort_authority", True),
                requires_post_execution_review=p.get("requires_post_execution_review", False),
                dependency_satisfied_now=False,
                authorization_granted_now=False,
                simulated_dependency_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_file_operation_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("file_operation"): r
        for r in (artifacts.get("boundary_object_file_operation_policy_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for op in FILE_OPERATIONS:
        p = by.get(op, {})
        ok_row = p.get("allowed_now") is False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                file_operation=op,
                allowed_by_default=p.get("allowed_by_default", op == "read"),
                requires_boundary_registry=p.get("requires_boundary_registry", op != "read"),
                requires_owner_operator_approval=p.get("requires_owner_operator_approval", op != "read"),
                requires_execution_window=p.get("requires_execution_window", op not in ("read", "copy")),
                requires_restore_map=p.get("requires_restore_map", False),
                requires_checkpoint=p.get("requires_checkpoint", False),
                allowed_now=False,
                file_operation_executed_now=False,
                simulated_operation_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_forbidden_shortcut_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("forbidden_shortcut"): r
        for r in (artifacts.get("boundary_object_forbidden_shortcut_matrix_v1.json") or {}).get("rows") or []
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


def _build_verifier_usage_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("verifier_check_id"): r
        for r in (artifacts.get("boundary_object_verifier_usage_planning_matrix_v1.json") or {}).get("rows") or []
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
        for r in (artifacts.get("boundary_object_non_claims_planning_matrix_v1.json") or {}).get("rows") or []
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


def run_boundary_object_registry_dryrun_v1(
    *,
    boundary_object_registry_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_planning_root)
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
    if up_readiness.get("ready_for_boundary_object_registry_dryrun") is not True:
        blockers.append("not ready_for_boundary_object_registry_dryrun")
    if up_summary.get("boundary_object_registry_planning_only") is not True:
        blockers.append("upstream boundary_object_registry_planning_only not true")
    for flag in (
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
        "protected_asset_modified_now",
        "human_review_queue_modified_now",
        "dnae_or_permanent_block_modified_now",
        "file_operation_executed_now",
        "owner_approval_request_sent_now",
        "operator_acknowledgement_request_sent_now",
        "execution_window_opened_now",
        "evidence_generation_authorized_now",
        "evidence_generated_now",
        "success_claim_allowed",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must be false")
    for flag in (
        "ready_for_boundary_object_registry_generation",
        "ready_for_boundary_object_registration",
        "ready_for_owner_approval_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation_authorization",
        "ready_for_file_operation",
        "ready_for_restore_map_generation",
        "ready_for_rollback_execution",
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
    cat_rows, cat_pass = _build_category_consumption(artifacts)
    rw_rows, rw_pass = _build_read_write_dryrun(artifacts)
    mig_rows, mig_pass = _build_migration_dryrun(artifacts)
    ev_rows, ev_pass = _build_evidence_dryrun(artifacts)
    rb_rows, rb_pass = _build_rollback_dryrun(artifacts)
    prot_rows, prot_pass = _build_protected_blocked_dryrun(artifacts)
    oo_rows, oo_pass = _build_owner_operator_dependency_dryrun(artifacts)
    file_rows, file_pass = _build_file_operation_dryrun(artifacts)
    shortcut_rows, shortcut_pass = _build_forbidden_shortcut_dryrun(artifacts)
    verifier_rows, verifier_pass = _build_verifier_usage_dryrun(artifacts)
    nclaims_rows, nclaims_pass = _build_non_claims_dryrun(artifacts)

    dryrun_pass = (
        comp_pass
        and cat_pass
        and rw_pass
        and mig_pass
        and ev_pass
        and rb_pass
        and prot_pass
        and oo_pass
        and file_pass
        and shortcut_pass
        and verifier_pass
        and nclaims_pass
        and not blockers
    )
    boundary_ok = dryrun_pass

    boundary_object_registry_dryrun_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_boundary_object_registry_dryrun_observed=up_readiness.get(
            "ready_for_boundary_object_registry_dryrun"
        )
        is True,
    )

    boundary_object_planning_artifact_completeness_dryrun = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_dryrun_meta(),
    }
    boundary_object_category_consumption_dryrun = {
        "rows": cat_rows,
        "row_count": len(cat_rows),
        "all_pass": cat_pass,
        **_dryrun_meta(),
    }
    boundary_object_read_write_policy_dryrun = {
        "rows": rw_rows,
        "row_count": len(rw_rows),
        "all_pass": rw_pass,
        **_dryrun_meta(),
    }
    boundary_object_migration_policy_dryrun = {
        "rows": mig_rows,
        "row_count": len(mig_rows),
        "all_pass": mig_pass,
        **_dryrun_meta(),
    }
    boundary_object_evidence_policy_dryrun = {
        "rows": ev_rows,
        "row_count": len(ev_rows),
        "all_pass": ev_pass,
        **_dryrun_meta(),
    }
    boundary_object_rollback_policy_dryrun = {
        "rows": rb_rows,
        "row_count": len(rb_rows),
        "all_pass": rb_pass,
        **_dryrun_meta(),
    }
    protected_and_blocked_object_dryrun = {
        "rows": prot_rows,
        "row_count": len(prot_rows),
        "all_pass": prot_pass,
        **_dryrun_meta(),
    }
    boundary_object_owner_operator_dependency_dryrun = {
        "rows": oo_rows,
        "row_count": len(oo_rows),
        "all_pass": oo_pass,
        **_dryrun_meta(),
    }
    boundary_object_file_operation_policy_dryrun = {
        "rows": file_rows,
        "row_count": len(file_rows),
        "all_pass": file_pass,
        **_dryrun_meta(),
    }
    boundary_object_forbidden_shortcut_dryrun = {
        "rows": shortcut_rows,
        "row_count": len(shortcut_rows),
        "all_pass": shortcut_pass,
        **_dryrun_meta(),
    }
    boundary_object_verifier_usage_dryrun = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_pass": verifier_pass,
        **_dryrun_meta(),
    }
    boundary_object_non_claims_generation_dryrun = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_dryrun_meta(),
    }

    boundary_object_registry_dryrun_readiness_decision = {
        "ready_for_boundary_object_registry_post_dryrun_review": boundary_ok,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
        "ready_for_owner_approval_request": False,
        "ready_for_operator_acknowledgement_request": False,
        "ready_for_execution_window_opening": False,
        "ready_for_evidence_generation_authorization": False,
        "ready_for_file_operation": False,
        "ready_for_restore_map_generation": False,
        "ready_for_rollback_execution": False,
        "ready_for_real_rollback_rehearsal_execution": False,
        "ready_for_real_migration_execution": False,
        "ready_for_batch_arming": False,
        "boundary_object_registry_dryrun_completed": boundary_ok,
        "planning_artifact_completeness_dryrun_pass": comp_pass,
        "category_consumption_dryrun_pass": cat_pass,
        "read_write_policy_dryrun_pass": rw_pass,
        "migration_policy_dryrun_pass": mig_pass,
        "evidence_policy_dryrun_pass": ev_pass,
        "rollback_policy_dryrun_pass": rb_pass,
        "protected_blocked_object_dryrun_pass": prot_pass,
        "owner_operator_dependency_dryrun_pass": oo_pass,
        "file_operation_policy_dryrun_pass": file_pass,
        "forbidden_shortcut_dryrun_pass": shortcut_pass,
        "verifier_usage_dryrun_pass": verifier_pass,
        "non_claims_generation_dryrun_pass": nclaims_pass,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "file_operation_executed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_planning_input_loaded": upstream["loaded"],
        "completeness_count": len(comp_rows),
        "category_consumption_count": len(cat_rows),
        "read_write_policy_dryrun_count": len(rw_rows),
        "migration_policy_dryrun_count": len(mig_rows),
        "evidence_policy_dryrun_count": len(ev_rows),
        "rollback_policy_dryrun_count": len(rb_rows),
        "protected_blocked_dryrun_count": len(prot_rows),
        "owner_operator_dependency_dryrun_count": len(oo_rows),
        "file_operation_dryrun_count": len(file_rows),
        "forbidden_shortcut_dryrun_count": len(shortcut_rows),
        "verifier_usage_dryrun_count": len(verifier_rows),
        "non_claims_dryrun_count": len(nclaims_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_registry_dryrun_policy": boundary_object_registry_dryrun_policy,
        "boundary_object_planning_artifact_completeness_dryrun": boundary_object_planning_artifact_completeness_dryrun,
        "boundary_object_category_consumption_dryrun": boundary_object_category_consumption_dryrun,
        "boundary_object_read_write_policy_dryrun": boundary_object_read_write_policy_dryrun,
        "boundary_object_migration_policy_dryrun": boundary_object_migration_policy_dryrun,
        "boundary_object_evidence_policy_dryrun": boundary_object_evidence_policy_dryrun,
        "boundary_object_rollback_policy_dryrun": boundary_object_rollback_policy_dryrun,
        "protected_and_blocked_object_dryrun": protected_and_blocked_object_dryrun,
        "boundary_object_owner_operator_dependency_dryrun": boundary_object_owner_operator_dependency_dryrun,
        "boundary_object_file_operation_policy_dryrun": boundary_object_file_operation_policy_dryrun,
        "boundary_object_forbidden_shortcut_dryrun": boundary_object_forbidden_shortcut_dryrun,
        "boundary_object_verifier_usage_dryrun": boundary_object_verifier_usage_dryrun,
        "boundary_object_non_claims_generation_dryrun": boundary_object_non_claims_generation_dryrun,
        "boundary_object_registry_dryrun_readiness_decision": boundary_object_registry_dryrun_readiness_decision,
    }
