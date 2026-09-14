# -*- coding: utf-8 -*-
"""Boundary Object Registry Generation DryRun v1.

Dry-run only: simulate consumption of registry generation planning by future
registry generation, owner/operator approval, evidence chain, and migration chains.
Does not generate registry, register objects, validate source finally, or generate entries.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.boundary_object_registry_generation_planning_v1 import (
    BOUNDARY_CATEGORIES,
    CONTAMINATION_RISKS,
    INTEGRITY_CHECKS,
    NON_CLAIM_SCENARIOS,
    OWNER_OPERATOR_DEPS,
    POLICY_ENTRY_TYPES,
    PROTECTED_OBJECT_TYPES,
    SOURCE_ARTIFACT_WHITELIST,
    SOURCE_TYPES,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001"
DRYRUN_SCOPE = "boundary_object_registry_generation_dryrun_only"
SOURCE_CHAIN = "boundary_object_registry_generation_dryrun_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-Generation-Planning-v1-001"
UPSTREAM_REQUIRED_FINAL = "BOUNDARY_OBJECT_REGISTRY_GENERATION_PLANNING_READY_FOR_DRYRUN"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001"

PLANNING_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("generation planning policy", "boundary_object_registry_generation_planning_policy_v1.json", 0),
    ("source inventory planning matrix", "registry_generation_source_inventory_planning_matrix_v1.json", 16),
    ("source artifact whitelist planning matrix", "registry_source_artifact_whitelist_planning_matrix_v1.json", 16),
    ("source integrity check planning matrix", "registry_source_integrity_check_planning_matrix_v1.json", 14),
    ("contamination prevention planning matrix", "registry_contamination_prevention_planning_matrix_v1.json", 14),
    ("entry conversion rule planning matrix", "registry_entry_conversion_rule_planning_matrix_v1.json", 16),
    ("protected object entry rule planning matrix", "registry_protected_object_entry_rule_planning_matrix_v1.json", 12),
    ("policy entry rule planning matrix", "registry_policy_entry_rule_planning_matrix_v1.json", 10),
    ("owner/operator dependency planning matrix", "registry_owner_operator_dependency_planning_matrix_v1.json", 10),
    ("verifier usage planning matrix", "registry_generation_verifier_usage_planning_matrix_v1.json", 16),
    ("non-claims planning matrix", "registry_generation_non_claims_planning_matrix_v1.json", 12),
    ("output plan", "registry_generation_output_plan_v1.json", 12),
    ("readiness decision", "boundary_object_registry_generation_planning_readiness_decision_v1.json", 0),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _dryrun_meta() -> Dict[str, Any]:
    return {
        "boundary_object_registry_generation_dryrun_only": True,
        "simulated": True,
        "boundary_object_registry_generation_executed_now": False,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_generation_authorized_now": False,
        "registry_source_final_validated_now": False,
        "registry_generation_source_validated_now": False,
        "registry_contamination_check_final_executed_now": False,
        "registry_generation_contamination_checked_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "protected_asset_modified_now": False,
        "human_review_queue_modified_now": False,
        "dnae_or_permanent_block_modified_now": False,
        "file_operation_executed_now": False,
        "write_permission_released_now": False,
        "migration_permission_released_now": False,
        "evidence_permission_released_now": False,
        "rollback_permission_released_now": False,
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
        root / "boundary_object_registry_generation_planning_readiness_decision_v1.json"
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
        if filename == "registry_generation_source_inventory_planning_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("used_for_generation_now") is False and r.get("source_final_validated_now") is False
                for r in (payload.get("rows") or [])
            )
        if filename == "registry_source_artifact_whitelist_planning_matrix_v1.json" and isinstance(payload, dict):
            summary_row = next(
                (r for r in (payload.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
                {},
            )
            verifier_row = next(
                (r for r in (payload.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
                {},
            )
            semantic_ok = (
                semantic_ok
                and summary_row.get("allowed_as_primary_source") is False
                and verifier_row.get("allowed_as_registry_source") is False
            )
        if filename == "registry_entry_conversion_rule_planning_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("entry_generated_now") is False and r.get("entry_committed_now") is False
                for r in (payload.get("rows") or [])
            )
        if filename == "registry_protected_object_entry_rule_planning_matrix_v1.json" and isinstance(payload, dict):
            semantic_ok = semantic_ok and all(
                r.get("write_allowed_now") is False
                and r.get("move_allowed_now") is False
                and r.get("entry_generated_now") is False
                for r in (payload.get("rows") or [])
            )
        if filename == "registry_generation_output_plan_v1.json" and isinstance(payload, dict):
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


def _build_source_inventory_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("source_type"): r
        for r in (artifacts.get("registry_generation_source_inventory_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for st, desc, allowed in SOURCE_TYPES:
        p = by.get(st, {})
        ok_row = (
            bool(p.get("source_description") or desc)
            and p.get("source_write_allowed_now") is False
            and p.get("source_final_validated_now") is False
            and p.get("used_for_generation_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                source_type=st,
                source_description=p.get("source_description") or desc,
                candidate_source_allowed=p.get("candidate_source_allowed", allowed),
                required_for_registry_generation=p.get("required_for_registry_generation", allowed),
                source_trust_level=p.get("source_trust_level", "high" if allowed else "auxiliary"),
                source_read_allowed=p.get("source_read_allowed", True),
                source_write_allowed_now=False,
                source_final_validated_now=False,
                used_for_generation_now=False,
                simulated_source_inventory_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_whitelist_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("source_artifact_type"): r
        for r in (artifacts.get("registry_source_artifact_whitelist_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for atype, _reason, primary, secondary, forbidden in SOURCE_ARTIFACT_WHITELIST:
        p = by.get(atype, {})
        ok_row = (
            p.get("whitelisted_now") is False
            and p.get("final_validated_now") is False
            and (p.get("forbidden_as_source_reason") or forbidden) == forbidden
            if atype in ("phase_summary", "phase_verifier_report")
            else p.get("whitelisted_now") is False
        )
        if atype == "phase_summary" and p.get("allowed_as_primary_source") is not False:
            ok_row = False
        if atype == "phase_verifier_report" and p.get("allowed_as_registry_source") is not False:
            ok_row = False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                source_artifact_type=atype,
                allowed_as_registry_source=p.get("allowed_as_registry_source", primary or secondary),
                allowed_as_primary_source=p.get("allowed_as_primary_source", primary),
                allowed_as_secondary_source=p.get("allowed_as_secondary_source", secondary),
                forbidden_as_source_reason=p.get("forbidden_as_source_reason") or forbidden,
                requires_integrity_check=p.get("requires_integrity_check", True),
                requires_contamination_check=p.get("requires_contamination_check", True),
                whitelisted_now=False,
                final_validated_now=False,
                simulated_whitelist_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_integrity_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("integrity_check"): r
        for r in (artifacts.get("registry_source_integrity_check_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for check, _why, fail in INTEGRITY_CHECKS:
        p = by.get(check, {})
        ok_row = (
            p.get("final_check_executed_now") is False
            and p.get("source_final_validated_now") is False
            and bool(p.get("failure_condition") or fail)
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                integrity_check=check,
                required_for_generation=p.get("required_for_generation", True),
                failure_condition=p.get("failure_condition") or fail,
                simulated_integrity_check=ok_row,
                final_check_executed_now=False,
                source_final_validated_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_contamination_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("contamination_risk"): r
        for r in (artifacts.get("registry_contamination_prevention_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for risk, _why, prevention in CONTAMINATION_RISKS:
        p = by.get(risk, {})
        ok_row = (
            p.get("contamination_checked_now") is False
            and p.get("final_generation_allowed_now") is False
            and bool(p.get("prevention_rule") or prevention)
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                contamination_risk=risk,
                prevention_rule=p.get("prevention_rule") or f"block generation when {risk}",
                required_detection=p.get("required_detection", True),
                simulated_contamination_check=ok_row,
                contamination_checked_now=False,
                final_generation_allowed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_entry_conversion_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("boundary_object_category"): r
        for r in (artifacts.get("registry_entry_conversion_rule_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for cat, _meaning, _why in BOUNDARY_CATEGORIES:
        p = by.get(cat, {})
        ok_row = (
            bool(p.get("entry_required_fields"))
            and p.get("entry_generated_now") is False
            and p.get("entry_committed_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                boundary_object_category=cat,
                entry_required_fields=p.get("entry_required_fields", []),
                source_requirements=p.get("source_requirements", []),
                risk_level_mapping=p.get("risk_level_mapping", "P1"),
                read_write_policy_mapping=p.get("read_write_policy_mapping"),
                migration_policy_mapping=p.get("migration_policy_mapping"),
                evidence_policy_mapping=p.get("evidence_policy_mapping"),
                rollback_policy_mapping=p.get("rollback_policy_mapping"),
                owner_operator_dependency_mapping=p.get("owner_operator_dependency_mapping"),
                simulated_entry_conversion=ok_row,
                entry_generated_now=False,
                entry_committed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_protected_entry_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("protected_object_type"): r
        for r in (artifacts.get("registry_protected_object_entry_rule_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for obj_type, why in PROTECTED_OBJECT_TYPES:
        p = by.get(obj_type, {})
        ok_row = (
            p.get("write_allowed_now") is False
            and p.get("move_allowed_now") is False
            and p.get("delete_allowed_now") is False
            and p.get("merge_allowed_now") is False
            and p.get("entry_generated_now") is False
            and p.get("entry_committed_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                protected_object_type=obj_type,
                required_registry_fields=p.get("required_registry_fields", []),
                protection_reason=p.get("protection_reason") or why,
                required_source_chain=p.get("required_source_chain", []),
                write_allowed_now=False,
                move_allowed_now=False,
                delete_allowed_now=False,
                merge_allowed_now=False,
                entry_generated_now=False,
                entry_committed_now=False,
                protected_asset_modified_now=False,
                simulated_block_check=ok_row,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_policy_entry_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("policy_entry_type"): r
        for r in (artifacts.get("registry_policy_entry_rule_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for pet in POLICY_ENTRY_TYPES:
        p = by.get(pet, {})
        ok_row = (
            bool(p.get("conversion_rule"))
            and p.get("entry_generated_now") is False
            and p.get("entry_committed_now") is False
        )
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                policy_entry_type=pet,
                required_source_artifacts=p.get("required_source_artifacts", []),
                required_fields=p.get("required_fields", []),
                conversion_rule=p.get("conversion_rule"),
                required_integrity_checks=p.get("required_integrity_checks", []),
                required_contamination_checks=p.get("required_contamination_checks", []),
                simulated_policy_entry_conversion=ok_row,
                entry_generated_now=False,
                entry_committed_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_owner_operator_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("dependency"): r
        for r in (artifacts.get("registry_owner_operator_dependency_planning_matrix_v1.json") or {}).get("rows") or []
    }
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for dep, ro, op, win, scope, abort in OWNER_OPERATOR_DEPS:
        p = by.get(dep, {})
        ok_row = p.get("satisfied_now") is False and p.get("authorization_granted_now") is False
        if not ok_row:
            all_pass = False
        rows.append(
            _row(
                dependency=dep,
                required_owner_approval=p.get("required_owner_approval", ro),
                required_operator_acknowledgement=p.get("required_operator_acknowledgement", op),
                required_execution_window=p.get("required_execution_window", win),
                required_scope_confirmation=p.get("required_scope_confirmation", scope),
                required_abort_authority=p.get("required_abort_authority", abort),
                simulated_dependency_check=ok_row,
                satisfied_now=False,
                authorization_granted_now=False,
                dryrun_status="pass" if ok_row else "fail",
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_verifier_usage_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    by = {
        r.get("verifier_check_id"): r
        for r in (artifacts.get("registry_generation_verifier_usage_planning_matrix_v1.json") or {}).get("rows") or []
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
    return rows, all_pass and len(rows) >= 16


def _build_non_claims_dryrun(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc_by = {
        r.get("scenario"): r
        for r in (artifacts.get("registry_generation_non_claims_planning_matrix_v1.json") or {}).get("rows") or []
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


def run_boundary_object_registry_generation_dryrun_v1(
    *,
    boundary_object_registry_generation_planning_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_generation_planning_root)
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
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_readiness.get("ready_for_boundary_object_registry_generation_dryrun") is not True:
        blockers.append("not ready_for_boundary_object_registry_generation_dryrun")
    if up_summary.get("boundary_object_registry_generation_planning_only") is not True:
        blockers.append("upstream boundary_object_registry_generation_planning_only not true")
    for flag in (
        "boundary_object_registry_generation_executed_now",
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
        "registry_generation_authorized_now",
        "registry_source_final_validated_now",
        "registry_generation_source_validated_now",
        "registry_contamination_check_final_executed_now",
        "registry_generation_contamination_checked_now",
        "registry_entry_generated_now",
        "registry_entry_committed_now",
        "protected_asset_modified_now",
        "human_review_queue_modified_now",
        "dnae_or_permanent_block_modified_now",
        "file_operation_executed_now",
        "owner_approval_request_sent_now",
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
        "ready_for_registry_generation_authorization",
        "ready_for_registry_source_final_validation",
        "ready_for_registry_contamination_check_final_execution",
        "ready_for_registry_entry_generation",
        "ready_for_registry_entry_commit",
        "ready_for_owner_approval_request",
        "ready_for_execution_window_opening",
        "ready_for_evidence_generation_authorization",
        "ready_for_file_operation",
        "ready_for_restore_map_generation",
        "ready_for_rollback_execution",
        "ready_for_real_rollback_rehearsal_execution",
        "ready_for_real_migration_execution",
    ):
        if up_readiness.get(flag) is not False:
            blockers.append(f"upstream readiness {flag} must remain false")
    if up_readiness.get("ready_for_batch_arming") is not False:
        blockers.append("ready_for_batch_arming must be false")
    if up_summary.get("real_migration_execution_allowed") is not False:
        blockers.append("real_migration_execution_allowed must be false")
    if up_summary.get("batch_arming_allowed") is not False:
        blockers.append("batch_arming_allowed must be false")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("governance_constraints_ref mismatch")

    whitelist_payload = artifacts.get("registry_source_artifact_whitelist_planning_matrix_v1.json") or {}
    summary_wl = next(
        (r for r in (whitelist_payload.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
        {},
    )
    verifier_wl = next(
        (r for r in (whitelist_payload.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
        {},
    )
    if summary_wl.get("allowed_as_primary_source") is not False:
        blockers.append("summary must not be primary source")
    if verifier_wl.get("allowed_as_registry_source") is not False:
        blockers.append("verifier_report must not be registry source")

    comp_rows, comp_pass = _build_completeness(artifacts)
    inv_rows, inv_pass = _build_source_inventory_dryrun(artifacts)
    wl_rows, wl_pass = _build_whitelist_dryrun(artifacts)
    int_rows, int_pass = _build_integrity_dryrun(artifacts)
    cont_rows, cont_pass = _build_contamination_dryrun(artifacts)
    conv_rows, conv_pass = _build_entry_conversion_dryrun(artifacts)
    prot_rows, prot_pass = _build_protected_entry_dryrun(artifacts)
    pol_rows, pol_pass = _build_policy_entry_dryrun(artifacts)
    oo_rows, oo_pass = _build_owner_operator_dryrun(artifacts)
    ver_rows, ver_pass = _build_verifier_usage_dryrun(artifacts)
    nc_rows, nc_pass = _build_non_claims_dryrun(artifacts)

    dryrun_pass = (
        comp_pass
        and inv_pass
        and wl_pass
        and int_pass
        and cont_pass
        and conv_pass
        and prot_pass
        and pol_pass
        and oo_pass
        and ver_pass
        and nc_pass
        and not blockers
    )
    boundary_ok = dryrun_pass

    boundary_object_registry_generation_dryrun_policy = _row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_boundary_object_registry_generation_dryrun_observed=up_readiness.get(
            "ready_for_boundary_object_registry_generation_dryrun"
        )
        is True,
    )

    registry_generation_planning_artifact_completeness_dryrun = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_dryrun_meta(),
    }
    registry_generation_source_inventory_dryrun = {
        "rows": inv_rows,
        "row_count": len(inv_rows),
        "all_pass": inv_pass,
        **_dryrun_meta(),
    }
    registry_source_artifact_whitelist_dryrun = {
        "rows": wl_rows,
        "row_count": len(wl_rows),
        "all_pass": wl_pass,
        **_dryrun_meta(),
    }
    registry_source_integrity_check_dryrun = {
        "rows": int_rows,
        "row_count": len(int_rows),
        "all_pass": int_pass,
        **_dryrun_meta(),
    }
    registry_contamination_prevention_dryrun = {
        "rows": cont_rows,
        "row_count": len(cont_rows),
        "all_pass": cont_pass,
        **_dryrun_meta(),
    }
    registry_entry_conversion_rule_dryrun = {
        "rows": conv_rows,
        "row_count": len(conv_rows),
        "all_pass": conv_pass,
        **_dryrun_meta(),
    }
    registry_protected_object_entry_rule_dryrun = {
        "rows": prot_rows,
        "row_count": len(prot_rows),
        "all_pass": prot_pass,
        **_dryrun_meta(),
    }
    registry_policy_entry_rule_dryrun = {
        "rows": pol_rows,
        "row_count": len(pol_rows),
        "all_pass": pol_pass,
        **_dryrun_meta(),
    }
    registry_owner_operator_dependency_dryrun = {
        "rows": oo_rows,
        "row_count": len(oo_rows),
        "all_pass": oo_pass,
        **_dryrun_meta(),
    }
    registry_generation_verifier_usage_dryrun = {
        "rows": ver_rows,
        "row_count": len(ver_rows),
        "all_pass": ver_pass,
        **_dryrun_meta(),
    }
    registry_generation_non_claims_generation_dryrun = {
        "rows": nc_rows,
        "row_count": len(nc_rows),
        "all_pass": nc_pass,
        **_dryrun_meta(),
    }

    boundary_object_registry_generation_dryrun_readiness_decision = {
        "ready_for_boundary_object_registry_generation_post_dryrun_review": boundary_ok,
        "ready_for_boundary_object_registry_generation": False,
        "ready_for_boundary_object_registration": False,
        "ready_for_registry_generation_authorization": False,
        "ready_for_registry_source_final_validation": False,
        "ready_for_registry_contamination_check_final_execution": False,
        "ready_for_registry_entry_generation": False,
        "ready_for_registry_entry_commit": False,
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
        "registry_generation_dryrun_completed": boundary_ok,
        "planning_artifact_completeness_dryrun_pass": comp_pass,
        "source_inventory_dryrun_pass": inv_pass,
        "source_whitelist_dryrun_pass": wl_pass,
        "source_integrity_dryrun_pass": int_pass,
        "contamination_prevention_dryrun_pass": cont_pass,
        "entry_conversion_rule_dryrun_pass": conv_pass,
        "protected_object_entry_rule_dryrun_pass": prot_pass,
        "policy_entry_rule_dryrun_pass": pol_pass,
        "owner_operator_dependency_dryrun_pass": oo_pass,
        "verifier_usage_dryrun_pass": ver_pass,
        "non_claims_generation_dryrun_pass": nc_pass,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_generation_planning_input_loaded": upstream["loaded"],
        "completeness_count": len(comp_rows),
        "source_inventory_dryrun_count": len(inv_rows),
        "source_whitelist_dryrun_count": len(wl_rows),
        "source_integrity_dryrun_count": len(int_rows),
        "contamination_prevention_dryrun_count": len(cont_rows),
        "entry_conversion_dryrun_count": len(conv_rows),
        "protected_entry_dryrun_count": len(prot_rows),
        "policy_entry_dryrun_count": len(pol_rows),
        "owner_operator_dependency_dryrun_count": len(oo_rows),
        "verifier_usage_dryrun_count": len(ver_rows),
        "non_claims_dryrun_count": len(nc_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_dryrun_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_registry_generation_dryrun_policy": boundary_object_registry_generation_dryrun_policy,
        "registry_generation_planning_artifact_completeness_dryrun": registry_generation_planning_artifact_completeness_dryrun,
        "registry_generation_source_inventory_dryrun": registry_generation_source_inventory_dryrun,
        "registry_source_artifact_whitelist_dryrun": registry_source_artifact_whitelist_dryrun,
        "registry_source_integrity_check_dryrun": registry_source_integrity_check_dryrun,
        "registry_contamination_prevention_dryrun": registry_contamination_prevention_dryrun,
        "registry_entry_conversion_rule_dryrun": registry_entry_conversion_rule_dryrun,
        "registry_protected_object_entry_rule_dryrun": registry_protected_object_entry_rule_dryrun,
        "registry_policy_entry_rule_dryrun": registry_policy_entry_rule_dryrun,
        "registry_owner_operator_dependency_dryrun": registry_owner_operator_dependency_dryrun,
        "registry_generation_verifier_usage_dryrun": registry_generation_verifier_usage_dryrun,
        "registry_generation_non_claims_generation_dryrun": registry_generation_non_claims_generation_dryrun,
        "boundary_object_registry_generation_dryrun_readiness_decision": boundary_object_registry_generation_dryrun_readiness_decision,
    }
