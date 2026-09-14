# -*- coding: utf-8 -*-
"""Boundary Object Registry Generation Post-DryRun Review v1.

Post-dryrun review only: audit generation dry-run completeness, non-execution,
source validation non-final, contamination non-final, entry non-generation,
source misuse, protected integrity, and permission non-release.
Does not generate registry, validate source finally, or generate entries.
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
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Generation-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "boundary_object_registry_generation_post_dryrun_review_only"
SOURCE_CHAIN = "boundary_object_registry_generation_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-Generation-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = "BOUNDARY_OBJECT_REGISTRY_GENERATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_GENERATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Generation-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("generation dry-run policy", "boundary_object_registry_generation_dryrun_policy_v1.json", 0),
    (
        "planning artifact completeness dry-run",
        "registry_generation_planning_artifact_completeness_dryrun_v1.json",
        13,
    ),
    ("source inventory dry-run", "registry_generation_source_inventory_dryrun_v1.json", 16),
    ("source artifact whitelist dry-run", "registry_source_artifact_whitelist_dryrun_v1.json", 16),
    ("source integrity check dry-run", "registry_source_integrity_check_dryrun_v1.json", 14),
    ("contamination prevention dry-run", "registry_contamination_prevention_dryrun_v1.json", 14),
    ("entry conversion rule dry-run", "registry_entry_conversion_rule_dryrun_v1.json", 16),
    ("protected object entry rule dry-run", "registry_protected_object_entry_rule_dryrun_v1.json", 12),
    ("policy entry rule dry-run", "registry_policy_entry_rule_dryrun_v1.json", 10),
    ("owner/operator dependency dry-run", "registry_owner_operator_dependency_dryrun_v1.json", 10),
    ("verifier usage dry-run", "registry_generation_verifier_usage_dryrun_v1.json", 16),
    ("non-claims generation dry-run", "registry_generation_non_claims_generation_dryrun_v1.json", 12),
    (
        "generation dry-run readiness decision",
        "boundary_object_registry_generation_dryrun_readiness_decision_v1.json",
        0,
    ),
)

GENERATION_NON_EXECUTION_TARGETS: Tuple[str, ...] = (
    "boundary_object_registry_generation_executed_now",
    "boundary_object_registry_generated_now",
    "boundary_object_registered_now",
    "registry_generation_authorized_now",
    "registry_generation_source_validated_now",
    "registry_generation_contamination_checked_now",
)

SOURCE_MISUSE_CASES: Tuple[Tuple[str, str], ...] = (
    ("summary as primary source", "summary must not be registry primary source"),
    ("verifier_report as entry single source", "verifier_report must not be entry single source"),
    ("non_claims_register as object entry", "non-claims register must not be object entry"),
    ("protected object inferred from summary only", "protected object must not be inferred from summary only"),
    ("failed verifier source", "failed verifier outputs must not be used as source"),
    ("non-GO source", "non-GO upstream must not be used as source"),
    ("stale source", "stale artifacts must not be used as source"),
    ("deprecated source", "deprecated phase outputs must not be used as source"),
    ("runtime artifact source", "runtime-generated artifacts must not be used as source"),
    ("auto-generated-doc source", "auto-sync documentation must not be used as source"),
    ("duplicate entry source", "duplicate entry derivation must be blocked"),
    ("conflicting category source", "conflicting category sources must be blocked"),
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
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


def _review_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_review_meta()}


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
        root / "boundary_object_registry_generation_dryrun_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for _, filename, _ in DRYRUN_ARTIFACTS:
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


def _observed_flag(up_summary: Dict[str, Any], target: str) -> bool:
    return up_summary.get(target) is True


def _build_completeness_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for name, filename, min_count in DRYRUN_ARTIFACTS:
        payload = artifacts.get(filename)
        observed = payload is not None
        count = _row_count(payload) if isinstance(payload, dict) else 0
        schema_ok = observed and isinstance(payload, dict)
        count_ok = min_count == 0 or count >= min_count
        semantic_ok = schema_ok and count_ok
        if isinstance(payload, dict) and "all_pass" in payload:
            semantic_ok = semantic_ok and payload.get("all_pass") is True
        review_pass = observed and schema_ok and count_ok and semantic_ok
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                artifact_name=name,
                expected=True,
                observed=observed,
                schema_minimum_pass=schema_ok,
                count_requirement_pass=count_ok,
                semantic_requirement_pass=semantic_ok,
                review_status="pass" if review_pass else "fail",
                review_notes=f"count={count} min={min_count}",
            )
        )
    return rows, all_pass


def _build_non_execution_review(up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target in GENERATION_NON_EXECUTION_TARGETS:
        obs = _observed_flag(up_summary, target)
        violation = obs is True
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                review_target=target,
                expected_value=False,
                observed_value=obs,
                violation_detected=violation,
                review_pass=review_pass,
                review_notes="generation not executed" if review_pass else f"{target} violation detected",
            )
        )
    return rows, all_pass


def _build_source_validation_non_final_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    integrity = artifacts.get("registry_source_integrity_check_dryrun_v1.json") or {}
    by = {r.get("integrity_check"): r for r in (integrity.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for check, _why, _fail in INTEGRITY_CHECKS:
        p = by.get(check, {})
        review_pass = (
            p.get("simulated_integrity_check") is True
            and p.get("final_check_executed_now") is False
            and p.get("source_final_validated_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                integrity_check=check,
                simulated_integrity_check=p.get("simulated_integrity_check") is True,
                final_check_executed_now=False,
                source_final_validated_now=False,
                registry_source_final_validated_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_contamination_non_final_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    contamination = artifacts.get("registry_contamination_prevention_dryrun_v1.json") or {}
    by = {r.get("contamination_risk"): r for r in (contamination.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for risk, _why, _prevention in CONTAMINATION_RISKS:
        p = by.get(risk, {})
        review_pass = (
            p.get("simulated_contamination_check") is True
            and p.get("contamination_checked_now") is False
            and p.get("final_generation_allowed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                contamination_risk=risk,
                simulated_contamination_check=p.get("simulated_contamination_check") is True,
                contamination_checked_now=False,
                registry_contamination_check_final_executed_now=False,
                final_generation_allowed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_entry_non_generation_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    conv = artifacts.get("registry_entry_conversion_rule_dryrun_v1.json") or {}
    prot = artifacts.get("registry_protected_object_entry_rule_dryrun_v1.json") or {}
    pol = artifacts.get("registry_policy_entry_rule_dryrun_v1.json") or {}
    rows: List[Dict[str, Any]] = []
    all_pass = True

    for cat, _, _ in BOUNDARY_CATEGORIES:
        c = next((r for r in (conv.get("rows") or []) if r.get("boundary_object_category") == cat), {})
        review_pass = (
            c.get("simulated_entry_conversion") is True
            and c.get("entry_generated_now") is False
            and c.get("entry_committed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                entry_type=cat,
                entry_group="category_entry_conversion",
                simulated_conversion_observed=c.get("simulated_entry_conversion") is True,
                entry_generated_now=False,
                entry_committed_now=False,
                review_pass=review_pass,
            )
        )

    for obj_type, _why in PROTECTED_OBJECT_TYPES:
        p = next((r for r in (prot.get("rows") or []) if r.get("protected_object_type") == obj_type), {})
        review_pass = (
            p.get("simulated_block_check") is True
            and p.get("entry_generated_now") is False
            and p.get("entry_committed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                entry_type=obj_type,
                entry_group="protected_object_entry",
                simulated_conversion_observed=p.get("simulated_block_check") is True,
                entry_generated_now=False,
                entry_committed_now=False,
                review_pass=review_pass,
            )
        )

    for pet in POLICY_ENTRY_TYPES:
        pe = next((r for r in (pol.get("rows") or []) if r.get("policy_entry_type") == pet), {})
        review_pass = (
            pe.get("simulated_policy_entry_conversion") is True
            and pe.get("entry_generated_now") is False
            and pe.get("entry_committed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                entry_type=pet,
                entry_group="policy_entry",
                simulated_conversion_observed=pe.get("simulated_policy_entry_conversion") is True,
                entry_generated_now=False,
                entry_committed_now=False,
                review_pass=review_pass,
            )
        )

    return rows, all_pass and len(rows) >= 38


def _build_source_misuse_review(
    artifacts: Dict[str, Any], up_summary: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], bool]:
    whitelist = artifacts.get("registry_source_artifact_whitelist_dryrun_v1.json") or {}
    summary_wl = next(
        (r for r in (whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
        {},
    )
    verifier_wl = next(
        (r for r in (whitelist.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
        {},
    )
    rows: List[Dict[str, Any]] = []
    all_pass = True

    misuse_observed: Dict[str, bool] = {
        "summary as primary source": summary_wl.get("allowed_as_primary_source") is True,
        "verifier_report as entry single source": verifier_wl.get("allowed_as_registry_source") is True,
        "non_claims_register as object entry": up_summary.get("registry_entry_generated_now") is True,
        "protected object inferred from summary only": False,
        "failed verifier source": up_summary.get("boundary_ok") is not True,
        "non-GO source": up_summary.get("boundary_ok") is not True,
        "stale source": False,
        "deprecated source": False,
        "runtime artifact source": up_summary.get("runtime_invoked") is True,
        "auto-generated-doc source": up_summary.get("documentation_auto_sync_executed_now") is True,
        "duplicate entry source": up_summary.get("registry_entry_generated_now") is True,
        "conflicting category source": False,
    }

    for case, forbidden in SOURCE_MISUSE_CASES:
        observed = misuse_observed.get(case, False)
        violation = observed is True
        review_pass = not violation
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                misuse_case=case,
                forbidden_usage=forbidden,
                observed=observed,
                violation_detected=violation,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_protected_integrity_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    prot = artifacts.get("registry_protected_object_entry_rule_dryrun_v1.json") or {}
    prot_by = {r.get("protected_object_type"): r for r in (prot.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for obj_type, _why in PROTECTED_OBJECT_TYPES:
        p = prot_by.get(obj_type, {})
        review_pass = (
            p.get("entry_generated_now") is False
            and p.get("entry_committed_now") is False
            and p.get("write_allowed_now") is False
            and p.get("move_allowed_now") is False
            and p.get("delete_allowed_now") is False
            and p.get("merge_allowed_now") is False
            and p.get("protected_asset_modified_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                protected_object_type=obj_type,
                entry_generated_now=False,
                entry_committed_now=False,
                write_allowed_now=False,
                move_allowed_now=False,
                delete_allowed_now=False,
                merge_allowed_now=False,
                modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_policy_entry_boundary_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    pol = artifacts.get("registry_policy_entry_rule_dryrun_v1.json") or {}
    pol_by = {r.get("policy_entry_type"): r for r in (pol.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for pet in POLICY_ENTRY_TYPES:
        p = pol_by.get(pet, {})
        release = p.get("entry_generated_now") is True or p.get("entry_committed_now") is True
        review_pass = (
            not release
            and p.get("simulated_policy_entry_conversion") is True
            and p.get("entry_generated_now") is False
            and p.get("entry_committed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                policy_entry_type=pet,
                simulated_policy_entry_conversion=p.get("simulated_policy_entry_conversion") is True,
                entry_generated_now=False,
                entry_committed_now=False,
                permission_released_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_owner_operator_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    oo = artifacts.get("registry_owner_operator_dependency_dryrun_v1.json") or {}
    oo_by = {r.get("dependency"): r for r in (oo.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for dep, _ro, _op, _win, _scope, _abort in OWNER_OPERATOR_DEPS:
        o = oo_by.get(dep, {})
        satisfied = o.get("satisfied_now") is True or o.get("authorization_granted_now") is True
        review_pass = not satisfied and o.get("simulated_dependency_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                dependency=dep,
                simulated_dependency_check=o.get("simulated_dependency_check") is True,
                satisfied_now=False,
                authorization_granted_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 10


def _build_verifier_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu = artifacts.get("registry_generation_verifier_usage_dryrun_v1.json") or {}
    vu_by = {r.get("verifier_check_id"): r for r in (vu.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, _phases, _fields, _fail, _sev in VERIFIER_CHECKS:
        v = vu_by.get(vid, {})
        review_pass = (
            v.get("simulated_verifier_consumption") is True
            and v.get("verifier_modified_now") is False
            and v.get("enforced_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                verifier_check_id=vid,
                check_name=v.get("check_name") or name,
                simulated_verifier_consumption=v.get("simulated_verifier_consumption") is True,
                verifier_modified_now=False,
                enforced_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_non_claims_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc = artifacts.get("registry_generation_non_claims_generation_dryrun_v1.json") or {}
    nc_by = {r.get("scenario"): r for r in (nc.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scenario, non_claim in NON_CLAIM_SCENARIOS:
        n = nc_by.get(scenario, {})
        review_pass = (
            bool(n.get("required_non_claim"))
            and n.get("simulated_generation") is True
            and n.get("generated_now") is False
            and n.get("template_modified_now") is False
            and n.get("documentation_auto_sync_executed_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                scenario=scenario,
                required_non_claim=n.get("required_non_claim") or non_claim,
                simulated_generation=n.get("simulated_generation") is True,
                generated_now=False,
                template_modified_now=False,
                documentation_auto_sync_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def run_boundary_object_registry_generation_post_dryrun_review_v1(
    *,
    boundary_object_registry_generation_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_generation_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream dryrun verifier not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok not true")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_readiness.get("ready_for_boundary_object_registry_generation_post_dryrun_review") is not True:
        blockers.append("not ready_for_boundary_object_registry_generation_post_dryrun_review")
    if up_summary.get("boundary_object_registry_generation_dryrun_only") is not True:
        blockers.append("upstream boundary_object_registry_generation_dryrun_only not true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated not true")
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

    inv = artifacts.get("registry_generation_source_inventory_dryrun_v1.json") or {}
    wl = artifacts.get("registry_source_artifact_whitelist_dryrun_v1.json") or {}
    integrity = artifacts.get("registry_source_integrity_check_dryrun_v1.json") or {}
    contamination = artifacts.get("registry_contamination_prevention_dryrun_v1.json") or {}
    conv = artifacts.get("registry_entry_conversion_rule_dryrun_v1.json") or {}
    prot = artifacts.get("registry_protected_object_entry_rule_dryrun_v1.json") or {}
    pol = artifacts.get("registry_policy_entry_rule_dryrun_v1.json") or {}
    oo = artifacts.get("registry_owner_operator_dependency_dryrun_v1.json") or {}

    if any(r.get("used_for_generation_now") is True for r in (inv.get("rows") or [])):
        blockers.append("used_for_generation_now must remain false")
    if any(r.get("whitelisted_now") is True for r in (wl.get("rows") or [])):
        blockers.append("whitelisted_now must remain false")
    if any(r.get("final_validated_now") is True for r in (wl.get("rows") or [])):
        blockers.append("whitelist final_validated_now must remain false")
    if any(r.get("final_check_executed_now") is True for r in (integrity.get("rows") or [])):
        blockers.append("final_check_executed_now must remain false")
    if any(r.get("contamination_checked_now") is True for r in (contamination.get("rows") or [])):
        blockers.append("contamination_checked_now must remain false")
    if any(r.get("entry_generated_now") is True for r in (conv.get("rows") or [])):
        blockers.append("entry_generated_now must remain false in conversion")
    if any(r.get("entry_committed_now") is True for r in (conv.get("rows") or [])):
        blockers.append("entry_committed_now must remain false in conversion")
    if any(r.get("entry_generated_now") is True for r in (prot.get("rows") or [])):
        blockers.append("protected entry_generated_now must remain false")
    if any(r.get("entry_generated_now") is True for r in (pol.get("rows") or [])):
        blockers.append("policy entry_generated_now must remain false")
    if any(r.get("satisfied_now") is True for r in (oo.get("rows") or [])):
        blockers.append("owner/operator dependency_satisfied_now must remain false")

    summary_wl = next(
        (r for r in (wl.get("rows") or []) if r.get("source_artifact_type") == "phase_summary"),
        {},
    )
    verifier_wl = next(
        (r for r in (wl.get("rows") or []) if r.get("source_artifact_type") == "phase_verifier_report"),
        {},
    )
    if summary_wl.get("allowed_as_primary_source") is not False:
        blockers.append("summary must not be primary source")
    if verifier_wl.get("allowed_as_registry_source") is not False:
        blockers.append("verifier_report must not be registry source")

    comp_rows, comp_pass = _build_completeness_review(artifacts)
    non_exec_rows, non_exec_pass = _build_non_execution_review(up_summary)
    src_val_rows, src_val_pass = _build_source_validation_non_final_review(artifacts)
    cont_rows, cont_pass = _build_contamination_non_final_review(artifacts)
    entry_rows, entry_pass = _build_entry_non_generation_review(artifacts)
    misuse_rows, misuse_pass = _build_source_misuse_review(artifacts, up_summary)
    prot_rows, prot_pass = _build_protected_integrity_review(artifacts)
    pol_rows, pol_pass = _build_policy_entry_boundary_review(artifacts)
    oo_rows, oo_pass = _build_owner_operator_review(artifacts)
    vu_rows, vu_pass = _build_verifier_review(artifacts)
    nc_rows, nc_pass = _build_non_claims_review(artifacts)

    review_pass = (
        comp_pass
        and non_exec_pass
        and src_val_pass
        and cont_pass
        and entry_pass
        and misuse_pass
        and prot_pass
        and pol_pass
        and oo_pass
        and vu_pass
        and nc_pass
        and not blockers
    )
    boundary_ok = review_pass

    boundary_object_registry_generation_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_boundary_object_registry_generation_post_dryrun_review_observed=up_readiness.get(
            "ready_for_boundary_object_registry_generation_post_dryrun_review"
        )
        is True,
    )

    registry_generation_dryrun_completeness_review = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_review_meta(),
    }
    registry_generation_non_execution_review = {
        "rows": non_exec_rows,
        "row_count": len(non_exec_rows),
        "all_pass": non_exec_pass,
        **_review_meta(),
    }
    registry_source_validation_non_final_review = {
        "rows": src_val_rows,
        "row_count": len(src_val_rows),
        "all_pass": src_val_pass,
        **_review_meta(),
    }
    registry_contamination_check_non_final_review = {
        "rows": cont_rows,
        "row_count": len(cont_rows),
        "all_pass": cont_pass,
        **_review_meta(),
    }
    registry_entry_non_generation_review = {
        "rows": entry_rows,
        "row_count": len(entry_rows),
        "all_pass": entry_pass,
        **_review_meta(),
    }
    registry_source_misuse_review = {
        "rows": misuse_rows,
        "row_count": len(misuse_rows),
        "all_pass": misuse_pass,
        **_review_meta(),
    }
    registry_protected_object_integrity_review = {
        "rows": prot_rows,
        "row_count": len(prot_rows),
        "all_pass": prot_pass,
        **_review_meta(),
    }
    registry_policy_entry_boundary_review = {
        "rows": pol_rows,
        "row_count": len(pol_rows),
        "all_pass": pol_pass,
        **_review_meta(),
    }
    registry_owner_operator_dependency_review = {
        "rows": oo_rows,
        "row_count": len(oo_rows),
        "all_pass": oo_pass,
        **_review_meta(),
    }
    registry_verifier_non_modification_review = {
        "rows": vu_rows,
        "row_count": len(vu_rows),
        "all_pass": vu_pass,
        **_review_meta(),
    }
    registry_non_claims_non_write_review = {
        "rows": nc_rows,
        "row_count": len(nc_rows),
        "all_pass": nc_pass,
        **_review_meta(),
    }

    boundary_object_registry_generation_post_dryrun_review_readiness_decision = {
        "ready_for_boundary_object_registry_generation_roadmap_decision": boundary_ok,
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
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": comp_pass,
        "generation_non_execution_review_pass": non_exec_pass,
        "source_validation_non_final_review_pass": src_val_pass,
        "contamination_check_non_final_review_pass": cont_pass,
        "entry_non_generation_review_pass": entry_pass,
        "source_misuse_review_pass": misuse_pass,
        "protected_object_integrity_review_pass": prot_pass,
        "policy_entry_boundary_review_pass": pol_pass,
        "owner_operator_dependency_review_pass": oo_pass,
        "verifier_non_modification_review_pass": vu_pass,
        "non_claims_non_write_review_pass": nc_pass,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_generation_dryrun_input_loaded": upstream["loaded"],
        "completeness_review_count": len(comp_rows),
        "non_execution_review_count": len(non_exec_rows),
        "source_validation_non_final_count": len(src_val_rows),
        "contamination_non_final_count": len(cont_rows),
        "entry_non_generation_count": len(entry_rows),
        "source_misuse_review_count": len(misuse_rows),
        "protected_integrity_count": len(prot_rows),
        "policy_entry_boundary_count": len(pol_rows),
        "owner_operator_review_count": len(oo_rows),
        "verifier_review_count": len(vu_rows),
        "non_claims_review_count": len(nc_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_GENERATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_registry_generation_post_dryrun_review_policy": boundary_object_registry_generation_post_dryrun_review_policy,
        "registry_generation_dryrun_completeness_review": registry_generation_dryrun_completeness_review,
        "registry_generation_non_execution_review": registry_generation_non_execution_review,
        "registry_source_validation_non_final_review": registry_source_validation_non_final_review,
        "registry_contamination_check_non_final_review": registry_contamination_check_non_final_review,
        "registry_entry_non_generation_review": registry_entry_non_generation_review,
        "registry_source_misuse_review": registry_source_misuse_review,
        "registry_protected_object_integrity_review": registry_protected_object_integrity_review,
        "registry_policy_entry_boundary_review": registry_policy_entry_boundary_review,
        "registry_owner_operator_dependency_review": registry_owner_operator_dependency_review,
        "registry_verifier_non_modification_review": registry_verifier_non_modification_review,
        "registry_non_claims_non_write_review": registry_non_claims_non_write_review,
        "boundary_object_registry_generation_post_dryrun_review_readiness_decision": boundary_object_registry_generation_post_dryrun_review_readiness_decision,
    }
