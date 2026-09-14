# -*- coding: utf-8 -*-
"""Boundary Object Registry Post-DryRun Review v1.

Post-dryrun review only: audit dry-run completeness, registry non-generation,
registration blocks, protected/blocked integrity, permission non-release.
Does not generate registry or execute file operations.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.boundary_object_registry_planning_v1 import (
    BOUNDARY_CATEGORIES,
    FILE_OPERATIONS,
    NON_CLAIM_SCENARIOS,
    PROTECTED_OBJECT_TYPES,
    VERIFIER_CHECKS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Boundary-Object-Registry-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "boundary_object_registry_post_dryrun_review_only"
SOURCE_CHAIN = "boundary_object_registry_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Boundary-Object-Registry-DryRun-v1-001"
FINAL_DECISION = "BOUNDARY_OBJECT_REGISTRY_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Boundary-Object-Registry-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "boundary_object_registry_dryrun_policy_v1.json", 0),
    ("planning artifact completeness dry-run", "boundary_object_planning_artifact_completeness_dryrun_v1.json", 14),
    ("category consumption dry-run", "boundary_object_category_consumption_dryrun_v1.json", 16),
    ("read/write policy dry-run", "boundary_object_read_write_policy_dryrun_v1.json", 16),
    ("migration policy dry-run", "boundary_object_migration_policy_dryrun_v1.json", 16),
    ("evidence policy dry-run", "boundary_object_evidence_policy_dryrun_v1.json", 16),
    ("rollback policy dry-run", "boundary_object_rollback_policy_dryrun_v1.json", 16),
    ("protected/blocked object dry-run", "protected_and_blocked_object_dryrun_v1.json", 12),
    ("owner/operator dependency dry-run", "boundary_object_owner_operator_dependency_dryrun_v1.json", 16),
    ("file operation policy dry-run", "boundary_object_file_operation_policy_dryrun_v1.json", 14),
    ("forbidden shortcut dry-run", "boundary_object_forbidden_shortcut_dryrun_v1.json", 12),
    ("verifier usage dry-run", "boundary_object_verifier_usage_dryrun_v1.json", 12),
    ("non-claims generation dry-run", "boundary_object_non_claims_generation_dryrun_v1.json", 12),
    ("dry-run readiness decision", "boundary_object_registry_dryrun_readiness_decision_v1.json", 0),
)

REGISTRY_NON_GENERATION_TARGETS: Tuple[str, ...] = (
    "boundary_object_registry_generated_now",
    "boundary_object_registered_now",
    "registry_artifact_generated_now",
    "boundary_object_registry_policy_generated_now",
    "boundary_object_category_matrix_generated_now",
    "boundary_object_registry_readiness_decision_generated_now",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
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
        root / "boundary_object_registry_dryrun_readiness_decision_v1.json"
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


def _observed_registry_target(target: str, up_summary: Dict[str, Any]) -> bool:
    direct = {
        "boundary_object_registry_generated_now": up_summary.get("boundary_object_registry_generated_now"),
        "boundary_object_registered_now": up_summary.get("boundary_object_registered_now"),
        "registry_artifact_generated_now": up_summary.get("boundary_object_registry_generated_now"),
        "boundary_object_registry_policy_generated_now": up_summary.get("boundary_object_registry_generated_now"),
        "boundary_object_category_matrix_generated_now": up_summary.get("boundary_object_registry_generated_now"),
        "boundary_object_registry_readiness_decision_generated_now": up_summary.get(
            "boundary_object_registry_generated_now"
        ),
    }
    return direct.get(target) is True


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


def _build_registry_non_generation_review(up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target in REGISTRY_NON_GENERATION_TARGETS:
        obs = _observed_registry_target(target, up_summary)
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
                review_notes="registry not generated" if review_pass else "registry generation detected",
            )
        )
    return rows, all_pass


def _build_registration_block_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    cat = artifacts.get("boundary_object_category_consumption_dryrun_v1.json") or {}
    cat_by = {r.get("boundary_object_category"): r for r in (cat.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for category, _meaning, _why in BOUNDARY_CATEGORIES:
        c = cat_by.get(category, {})
        review_pass = (
            c.get("simulated_registry_consumption") is True
            and c.get("registered_now") is False
            and c.get("registry_generated_now") is False
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                boundary_object_category=category,
                simulated_registry_consumption=c.get("simulated_registry_consumption") is True,
                registered_now=False,
                registry_generated_now=False,
                formal_object_id_generated_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_protected_integrity_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    prot = artifacts.get("protected_and_blocked_object_dryrun_v1.json") or {}
    prot_by = {r.get("protected_object_type"): r for r in (prot.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for obj_type, _why in PROTECTED_OBJECT_TYPES:
        p = prot_by.get(obj_type, {})
        review_pass = (
            p.get("write_allowed_now") is False
            and p.get("move_allowed_now") is False
            and p.get("delete_allowed_now") is False
            and p.get("merge_allowed_now") is False
            and p.get("simulated_block_check") is True
        )
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                protected_object_type=obj_type,
                write_allowed_now=False,
                move_allowed_now=False,
                delete_allowed_now=False,
                merge_allowed_now=False,
                modified_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_read_write_permission_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rw = artifacts.get("boundary_object_read_write_policy_dryrun_v1.json") or {}
    rw_by = {r.get("boundary_object_category"): r for r in (rw.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for category, _, _ in BOUNDARY_CATEGORIES:
        r = rw_by.get(category, {})
        release = r.get("write_allowed_now") is True or r.get("file_operation_allowed_now") is True
        review_pass = not release and r.get("simulated_policy_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                boundary_object_category=category,
                read_allowed_by_default=r.get("read_allowed_by_default", True),
                write_allowed_by_default=r.get("write_allowed_by_default", False),
                write_allowed_now=False,
                file_operation_allowed_now=False,
                permission_release_detected=release,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_migration_permission_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    mig = artifacts.get("boundary_object_migration_policy_dryrun_v1.json") or {}
    mig_by = {r.get("boundary_object_category"): r for r in (mig.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for category, _, _ in BOUNDARY_CATEGORIES:
        m = mig_by.get(category, {})
        release = m.get("migration_allowed_now") is True
        review_pass = not release and m.get("simulated_policy_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                boundary_object_category=category,
                migration_allowed_by_default=m.get("migration_allowed_by_default", False),
                migration_allowed_now=False,
                restore_map_required=m.get("migration_requires_restore_map", True),
                rollback_plan_required=m.get("migration_requires_rollback_plan", True),
                permission_release_detected=release,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_evidence_permission_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    ev = artifacts.get("boundary_object_evidence_policy_dryrun_v1.json") or {}
    ev_by = {r.get("boundary_object_category"): r for r in (ev.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for category, _, _ in BOUNDARY_CATEGORIES:
        e = ev_by.get(category, {})
        release = (
            e.get("evidence_generation_allowed_now") is True or e.get("success_evidence_allowed_now") is True
        )
        if category in ("verifier artifacts", "eval_out artifacts") and e.get("can_be_success_evidence_source") is True:
            release = True
        review_pass = not release and e.get("simulated_policy_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                boundary_object_category=category,
                can_be_evidence_source=e.get("can_be_evidence_source", False),
                can_be_success_evidence_source=False,
                evidence_generation_allowed_now=False,
                success_evidence_allowed_now=False,
                evidence_permission_release_detected=release,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_rollback_permission_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rb = artifacts.get("boundary_object_rollback_policy_dryrun_v1.json") or {}
    rb_by = {r.get("boundary_object_category"): r for r in (rb.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for category, _, _ in BOUNDARY_CATEGORIES:
        r = rb_by.get(category, {})
        release = r.get("rollback_allowed_now") is True or r.get("restore_operation_allowed_now") is True
        review_pass = not release and r.get("simulated_policy_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                boundary_object_category=category,
                requires_restore_map=r.get("requires_restore_map", True),
                requires_checkpoint=r.get("requires_checkpoint", True),
                rollback_allowed_now=False,
                restore_operation_allowed_now=False,
                permission_release_detected=release,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_owner_operator_dependency_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    oo = artifacts.get("boundary_object_owner_operator_dependency_dryrun_v1.json") or {}
    oo_by = {r.get("boundary_object_category"): r for r in (oo.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for category, _, _ in BOUNDARY_CATEGORIES:
        o = oo_by.get(category, {})
        satisfied = o.get("dependency_satisfied_now") is True or o.get("authorization_granted_now") is True
        review_pass = not satisfied and o.get("simulated_dependency_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                boundary_object_category=category,
                dependency_satisfied_now=False,
                authorization_granted_now=False,
                owner_approval_required=o.get("requires_owner_approval_for_write", True),
                operator_acknowledgement_required=o.get("requires_operator_acknowledgement_for_write", True),
                execution_window_required=o.get("requires_execution_window_for_write", True),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 16


def _build_file_operation_block_review(artifacts: Dict[str, Any], up_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    fo = artifacts.get("boundary_object_file_operation_policy_dryrun_v1.json") or {}
    fo_by = {r.get("file_operation"): r for r in (fo.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for op in FILE_OPERATIONS:
        f = fo_by.get(op, {})
        executed = f.get("file_operation_executed_now") is True or up_summary.get("file_operation_executed_now") is True
        allowed = f.get("allowed_now") is True
        review_pass = not allowed and not executed and f.get("simulated_operation_check") is True
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                file_operation=op,
                allowed_now=False,
                file_operation_executed_now=False,
                requires_boundary_registry=f.get("requires_boundary_registry", op != "read"),
                requires_owner_operator_approval=f.get("requires_owner_operator_approval", op != "read"),
                requires_execution_window=f.get("requires_execution_window", op not in ("read", "copy")),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 14


def _build_verifier_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    vu = artifacts.get("boundary_object_verifier_usage_dryrun_v1.json") or {}
    vu_by = {r.get("verifier_check_id"): r for r in (vu.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for vid, name, phases, fields, fail, sev in VERIFIER_CHECKS:
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
    return rows, all_pass and len(rows) >= 12


def _build_non_claims_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    nc = artifacts.get("boundary_object_non_claims_generation_dryrun_v1.json") or {}
    nc_by = {r.get("scenario"): r for r in (nc.get("rows") or [])}
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for scenario, non_claim in NON_CLAIM_SCENARIOS:
        n = nc_by.get(scenario, {})
        review_pass = (
            bool(n.get("required_non_claim"))
            and n.get("simulated_generation") is True
            and n.get("generated_now") is False
            and n.get("template_modified_now", n.get("phase_template_modified_now")) is False
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


def run_boundary_object_registry_post_dryrun_review_v1(
    *,
    boundary_object_registry_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(boundary_object_registry_dryrun_root)
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
    if up_readiness.get("ready_for_boundary_object_registry_post_dryrun_review") is not True:
        blockers.append("not ready_for_boundary_object_registry_post_dryrun_review")
    if up_summary.get("boundary_object_registry_dryrun_only") is not True:
        blockers.append("upstream boundary_object_registry_dryrun_only not true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated not true")
    for flag in (
        "boundary_object_registry_generated_now",
        "boundary_object_registered_now",
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

    rw = artifacts.get("boundary_object_read_write_policy_dryrun_v1.json") or {}
    mig = artifacts.get("boundary_object_migration_policy_dryrun_v1.json") or {}
    ev = artifacts.get("boundary_object_evidence_policy_dryrun_v1.json") or {}
    rb = artifacts.get("boundary_object_rollback_policy_dryrun_v1.json") or {}
    oo = artifacts.get("boundary_object_owner_operator_dependency_dryrun_v1.json") or {}
    if any(r.get("write_allowed_now") is True for r in (rw.get("rows") or [])):
        blockers.append("write_allowed_now must remain false")
    if any(r.get("migration_allowed_now") is True for r in (mig.get("rows") or [])):
        blockers.append("migration_allowed_now must remain false")
    if any(r.get("evidence_generation_allowed_now") is True for r in (ev.get("rows") or [])):
        blockers.append("evidence_generation_allowed_now must remain false")
    if any(r.get("rollback_allowed_now") is True for r in (rb.get("rows") or [])):
        blockers.append("rollback_allowed_now must remain false")
    if any(r.get("dependency_satisfied_now") is True for r in (oo.get("rows") or [])):
        blockers.append("dependency_satisfied_now must remain false")

    comp_rows, comp_pass = _build_completeness_review(artifacts)
    reg_rows, reg_pass = _build_registry_non_generation_review(up_summary)
    reg_block_rows, reg_block_pass = _build_registration_block_review(artifacts)
    prot_rows, prot_pass = _build_protected_integrity_review(artifacts)
    rw_rows, rw_pass = _build_read_write_permission_review(artifacts)
    mig_rows, mig_pass = _build_migration_permission_review(artifacts)
    ev_rows, ev_pass = _build_evidence_permission_review(artifacts)
    rb_rows, rb_pass = _build_rollback_permission_review(artifacts)
    oo_rows, oo_pass = _build_owner_operator_dependency_review(artifacts)
    file_rows, file_pass = _build_file_operation_block_review(artifacts, up_summary)
    vu_rows, vu_pass = _build_verifier_review(artifacts)
    nc_rows, nc_pass = _build_non_claims_review(artifacts)

    review_pass = (
        comp_pass
        and reg_pass
        and reg_block_pass
        and prot_pass
        and rw_pass
        and mig_pass
        and ev_pass
        and rb_pass
        and oo_pass
        and file_pass
        and vu_pass
        and nc_pass
        and not blockers
    )
    boundary_ok = review_pass

    boundary_object_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_boundary_object_registry_post_dryrun_review_observed=up_readiness.get(
            "ready_for_boundary_object_registry_post_dryrun_review"
        )
        is True,
    )

    boundary_object_dryrun_completeness_review = {
        "rows": comp_rows,
        "row_count": len(comp_rows),
        "all_pass": comp_pass,
        **_review_meta(),
    }
    boundary_registry_non_generation_review = {
        "rows": reg_rows,
        "row_count": len(reg_rows),
        "all_pass": reg_pass,
        **_review_meta(),
    }
    boundary_object_registration_block_review = {
        "rows": reg_block_rows,
        "row_count": len(reg_block_rows),
        "all_pass": reg_block_pass,
        **_review_meta(),
    }
    protected_blocked_object_integrity_review = {
        "rows": prot_rows,
        "row_count": len(prot_rows),
        "all_pass": prot_pass,
        **_review_meta(),
    }
    boundary_read_write_permission_review = {
        "rows": rw_rows,
        "row_count": len(rw_rows),
        "all_pass": rw_pass,
        **_review_meta(),
    }
    boundary_migration_permission_review = {
        "rows": mig_rows,
        "row_count": len(mig_rows),
        "all_pass": mig_pass,
        **_review_meta(),
    }
    boundary_evidence_permission_review = {
        "rows": ev_rows,
        "row_count": len(ev_rows),
        "all_pass": ev_pass,
        **_review_meta(),
    }
    boundary_rollback_permission_review = {
        "rows": rb_rows,
        "row_count": len(rb_rows),
        "all_pass": rb_pass,
        **_review_meta(),
    }
    boundary_owner_operator_dependency_review = {
        "rows": oo_rows,
        "row_count": len(oo_rows),
        "all_pass": oo_pass,
        **_review_meta(),
    }
    boundary_file_operation_block_review = {
        "rows": file_rows,
        "row_count": len(file_rows),
        "all_pass": file_pass,
        **_review_meta(),
    }
    boundary_verifier_non_modification_review = {
        "rows": vu_rows,
        "row_count": len(vu_rows),
        "all_pass": vu_pass,
        **_review_meta(),
    }
    boundary_non_claims_non_write_review = {
        "rows": nc_rows,
        "row_count": len(nc_rows),
        "all_pass": nc_pass,
        **_review_meta(),
    }

    boundary_object_post_dryrun_review_readiness_decision = {
        "ready_for_boundary_object_registry_roadmap_decision": boundary_ok,
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
        "post_dryrun_review_completed": boundary_ok,
        "dryrun_completeness_review_pass": comp_pass,
        "registry_non_generation_review_pass": reg_pass,
        "object_registration_block_review_pass": reg_block_pass,
        "protected_blocked_object_integrity_review_pass": prot_pass,
        "read_write_permission_review_pass": rw_pass,
        "migration_permission_review_pass": mig_pass,
        "evidence_permission_review_pass": ev_pass,
        "rollback_permission_review_pass": rb_pass,
        "owner_operator_dependency_review_pass": oo_pass,
        "file_operation_block_review_pass": file_pass,
        "verifier_non_modification_review_pass": vu_pass,
        "non_claims_non_write_review_pass": nc_pass,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "file_operation_executed_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "boundary_object_registry_dryrun_input_loaded": upstream["loaded"],
        "completeness_review_count": len(comp_rows),
        "registration_block_count": len(reg_block_rows),
        "protected_integrity_count": len(prot_rows),
        "read_write_permission_review_count": len(rw_rows),
        "migration_permission_review_count": len(mig_rows),
        "evidence_permission_review_count": len(ev_rows),
        "rollback_permission_review_count": len(rb_rows),
        "owner_operator_dependency_review_count": len(oo_rows),
        "file_operation_block_count": len(file_rows),
        "verifier_review_count": len(vu_rows),
        "non_claims_review_count": len(nc_rows),
        "write_permission_released_now": False,
        "migration_permission_released_now": False,
        "evidence_permission_released_now": False,
        "rollback_permission_released_now": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "BOUNDARY_OBJECT_REGISTRY_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    return {
        "summary": summary,
        "boundary_object_post_dryrun_review_policy": boundary_object_post_dryrun_review_policy,
        "boundary_object_dryrun_completeness_review": boundary_object_dryrun_completeness_review,
        "boundary_registry_non_generation_review": boundary_registry_non_generation_review,
        "boundary_object_registration_block_review": boundary_object_registration_block_review,
        "protected_blocked_object_integrity_review": protected_blocked_object_integrity_review,
        "boundary_read_write_permission_review": boundary_read_write_permission_review,
        "boundary_migration_permission_review": boundary_migration_permission_review,
        "boundary_evidence_permission_review": boundary_evidence_permission_review,
        "boundary_rollback_permission_review": boundary_rollback_permission_review,
        "boundary_owner_operator_dependency_review": boundary_owner_operator_dependency_review,
        "boundary_file_operation_block_review": boundary_file_operation_block_review,
        "boundary_verifier_non_modification_review": boundary_verifier_non_modification_review,
        "boundary_non_claims_non_write_review": boundary_non_claims_non_write_review,
        "boundary_object_post_dryrun_review_readiness_decision": boundary_object_post_dryrun_review_readiness_decision,
    }
