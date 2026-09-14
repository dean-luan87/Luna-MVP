# -*- coding: utf-8 -*-
"""Permission Semantics Canonicalization Post-DryRun Review v1.

Post-dryrun review only: audit dry-run completeness, non-enforcement, registry non-write,
forbidden non-enforce, template non-modification, verifier non-modification, non-claims non-write.
Does not enforce semantics, modify verifiers/templates, or release authorization.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Permission-Semantics-Canonicalization-Post-DryRun-Review-v1-001"
REVIEW_SCOPE = "permission_semantics_canonicalization_post_dryrun_review_only"
REVIEW_ID = "permission_semantics_canonicalization_post_dryrun_review_v1_001"
SOURCE_CHAIN = "permission_semantics_canonicalization_post_dryrun_review_v1"

SOURCE_PHASE = "Phase-Permission-Semantics-Canonicalization-DryRun-v1-001"
UPSTREAM_REQUIRED_FINAL = "PERMISSION_SEMANTICS_CANONICALIZATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"

FINAL_DECISION = "PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
NEXT_PHASE = "Phase-Permission-Semantics-Canonicalization-Roadmap-Decision-v1-001"

DRYRUN_ARTIFACTS: Tuple[Tuple[str, str, int], ...] = (
    ("dry-run policy", "permission_semantics_canonicalization_dryrun_policy_v1.json", 0),
    ("artifact completeness dry-run", "semantics_artifact_completeness_dryrun_v1.json", 14),
    ("semantic registry dry-run index", "semantic_registry_dryrun_index_v1.json", 8),
    ("forbidden combination verifier mapping dry-run", "forbidden_combination_verifier_mapping_dryrun_v1.json", 20),
    ("development norms phase template mapping dry-run", "development_norms_phase_template_mapping_dryrun_v1.json", 12),
    ("verifier checklist consumption dry-run", "verifier_checklist_consumption_dryrun_v1.json", 20),
    ("non-claims generation dry-run", "non_claims_generation_dryrun_v1.json", 20),
    ("readiness decision semantic validation dry-run", "readiness_decision_semantic_validation_dryrun_v1.json", 12),
    ("success claim semantic gate dry-run", "success_claim_semantic_gate_dryrun_v1.json", 8),
    ("cross-artifact consistency dry-run", "cross_artifact_consistency_dryrun_v1.json", 12),
    ("dry-run non-claims register", "semantics_dryrun_non_claims_register_v1.json", 9),
    ("dry-run readiness decision", "permission_semantics_canonicalization_dryrun_readiness_decision_v1.json", 0),
)

NON_ENFORCEMENT_TARGETS: Tuple[Tuple[str, str], ...] = (
    ("canonicalization execution", "canonicalization_executed_now"),
    ("semantics enforcement", "canonicalization_enforced_now"),
    ("semantic registry write", "registry_written_now"),
    ("forbidden combination enforcement", "forbidden_combinations_enforced_now"),
    ("development norms enforcement", "development_norms_enforced_now"),
    ("verifier checklist enforcement", "verifier_checklist_enforced_now"),
    ("non-claims auto-generation", "non_claims_generated_now"),
    ("phase template modification", "phase_template_modified_now"),
    ("verifier modification", "verifier_modified_now"),
    ("documentation auto-sync", "documentation_auto_sync_executed_now"),
    ("automation implementation", "automation_implemented_now"),
    ("debt fix execution", "debt_fix_executed_now"),
)

POST_REVIEW_NON_CLAIMS = [
    "Post-DryRun Review GO does not mean semantics are canonicalized.",
    "Post-DryRun Review GO does not mean semantics are enforced.",
    "Post-DryRun Review GO does not mean semantic registry has been written.",
    "Post-DryRun Review GO does not mean verifier has been modified.",
    "Post-DryRun Review GO does not mean phase template has been modified.",
    "Post-DryRun Review GO does not mean forbidden combinations are enforced.",
    "Post-DryRun Review GO does not mean non-claims are auto-generated.",
    "Post-DryRun Review GO does not mean governance debt is fixed.",
    "Post-DryRun Review GO does not mean real rehearsal / migration / batch arming is allowed.",
]


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _review_meta() -> Dict[str, Any]:
    return {
        "post_dryrun_review_only": True,
        "review_only": True,
        "canonicalization_executed_now": False,
        "canonicalization_enforced_now": False,
        "not_enforced_now": True,
        "registry_written_now": False,
        "forbidden_combinations_enforced_now": False,
        "development_norms_enforced_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "non_claims_generated_now": False,
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
        root / "permission_semantics_canonicalization_dryrun_readiness_decision_v1.json"
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


def _build_completeness_review(artifacts: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for name, filename, min_count in DRYRUN_ARTIFACTS:
        payload = artifacts.get(filename)
        observed = payload is not None
        count = _row_count(payload) if isinstance(payload, dict) else 0
        schema_ok = observed and isinstance(payload, dict)
        count_ok = min_count == 0 or count >= min_count
        semantic_ok = schema_ok
        if filename == "semantics_artifact_completeness_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True and count >= 14
        if filename == "forbidden_combination_verifier_mapping_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True
        if filename == "cross_artifact_consistency_dryrun_v1.json" and isinstance(payload, dict):
            semantic_ok = payload.get("all_pass") is True
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


def _build_non_enforcement_matrix(observed: Dict[str, bool]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for target, field in NON_ENFORCEMENT_TARGETS:
        obs = observed.get(field, False)
        ne_pass = obs is False
        violation = obs is True
        if violation:
            all_pass = False
        rows.append(
            _review_row(
                non_enforcement_target=target,
                expected_value=False,
                observed_value=obs,
                non_enforcement_pass=ne_pass,
                violation_detected=violation,
                review_status="pass" if ne_pass else "fail",
            )
        )
    return rows, all_pass


def _build_registry_write_review(registry: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in registry.get("rows") or []:
        written = row.get("registry_written_now") is True
        enforced = row.get("canonicalization_enforced_now") is True
        review_pass = not written and not enforced
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                registry_group=row.get("registry_group"),
                source_artifact=row.get("source_artifact"),
                indexable_in_dryrun=row.get("indexable_in_dryrun") is True,
                future_registry_candidate=row.get("future_registry_candidate") is True,
                registry_written_now=False,
                canonicalization_enforced_now=False,
                review_pass=review_pass,
                review_notes="no registry write observed" if review_pass else "registry write or enforce detected",
            )
        )
    return rows, all_pass and len(rows) >= 8


def _build_forbidden_enforcement_review(forbidden: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in forbidden.get("rows") or []:
        enforced = row.get("enforced_now") is True
        modified = row.get("verifier_modified_now") is True
        mapped = row.get("mapped_to_verifier_check") is True
        review_pass = mapped and not enforced and not modified
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                forbidden_combination_id=row.get("forbidden_combination_id"),
                mapped_to_verifier_check=mapped,
                verifier_modified_now=False,
                enforced_now=False,
                failure_condition_present=bool(row.get("failure_condition")),
                expected_error_level_present=bool(row.get("expected_error_level")),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 20


def _build_norms_template_review(norms: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in norms.get("rows") or []:
        modified = row.get("phase_template_modified_now") is True
        enforced = row.get("enforced_now") is True
        mapped = row.get("mapped_to_future_phase_template") is True
        review_pass = mapped and not modified and not enforced
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                norm_id=row.get("norm_id"),
                norm_name=row.get("norm_name"),
                mapped_to_future_phase_template=mapped,
                phase_template_modified_now=False,
                enforced_now=False,
                required_fields_present=bool(row.get("required_fields")),
                forbidden_patterns_present=bool(row.get("forbidden_patterns")),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 12


def _build_verifier_checklist_review(checklist: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in checklist.get("rows") or []:
        modified = row.get("verifier_modified_now") is True
        simulated = row.get("simulated_consumption") is True
        not_enforced = row.get("not_enforced_now") is True
        review_pass = simulated and not modified and not_enforced
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                check_id=row.get("check_id"),
                check_name=row.get("check_name"),
                simulated_consumption=simulated,
                verifier_modified_now=False,
                not_enforced_now=True,
                failure_condition_present=bool(row.get("failure_condition")),
                severity_present=bool(row.get("severity")),
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 20


def _build_non_claims_non_write_review(nclaims: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in nclaims.get("rows") or []:
        generated = row.get("generated_now") is True
        template_mod = row.get("template_modified_now") is True
        doc_sync = row.get("documentation_auto_sync_executed_now") is True
        simulated = row.get("simulated_generation") is True
        review_pass = simulated and not generated and not template_mod and not doc_sync
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                scenario=row.get("scenario"),
                required_non_claim=row.get("required_non_claim"),
                simulated_generation=simulated,
                generated_now=False,
                template_modified_now=False,
                documentation_auto_sync_executed_now=False,
                review_pass=review_pass,
            )
        )
    return rows, all_pass and len(rows) >= 20


def _build_cross_artifact_review(consistency: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for row in consistency.get("rows") or []:
        enforced = row.get("enforced_now") is True
        consistency_pass = row.get("consistency_pass") is True
        review_pass = consistency_pass and not enforced
        if not review_pass:
            all_pass = False
        rows.append(
            _review_row(
                consistency_check_id=row.get("consistency_check_id"),
                check_description=row.get("check_description"),
                source_artifacts=row.get("source_artifacts"),
                consistency_pass=consistency_pass,
                enforced_now=False,
                review_pass=review_pass,
                review_notes=row.get("dryrun_notes", "cross-artifact review only"),
            )
        )
    return rows, all_pass and len(rows) >= 12


def _compute_observed_non_enforcement(up_summary: Dict[str, Any], artifacts: Dict[str, Any]) -> Dict[str, bool]:
    registry_rows = (artifacts.get("semantic_registry_dryrun_index_v1.json") or {}).get("rows") or []
    registry_written = any(r.get("registry_written_now") is True for r in registry_rows)
    forbidden_rows = (artifacts.get("forbidden_combination_verifier_mapping_dryrun_v1.json") or {}).get("rows") or []
    forbidden_enforced = any(r.get("enforced_now") is True for r in forbidden_rows)
    norms_rows = (artifacts.get("development_norms_phase_template_mapping_dryrun_v1.json") or {}).get("rows") or []
    norms_enforced = any(r.get("enforced_now") is True for r in norms_rows)
    nclaims_rows = (artifacts.get("non_claims_generation_dryrun_v1.json") or {}).get("rows") or []
    nclaims_generated = any(r.get("generated_now") is True for r in nclaims_rows)

    return {
        "canonicalization_executed_now": up_summary.get("canonicalization_executed_now") is True,
        "canonicalization_enforced_now": up_summary.get("canonicalization_enforced_now") is True,
        "registry_written_now": registry_written,
        "forbidden_combinations_enforced_now": forbidden_enforced,
        "development_norms_enforced_now": norms_enforced,
        "verifier_checklist_enforced_now": up_summary.get("verifier_modified_now") is True,
        "non_claims_generated_now": nclaims_generated,
        "phase_template_modified_now": up_summary.get("phase_template_modified_now") is True,
        "verifier_modified_now": up_summary.get("verifier_modified_now") is True,
        "documentation_auto_sync_executed_now": up_summary.get("documentation_auto_sync_executed_now") is True,
        "automation_implemented_now": up_summary.get("automation_implemented_now") is True,
        "debt_fix_executed_now": up_summary.get("debt_fix_executed_now") is True,
    }


def run_permission_semantics_canonicalization_post_dryrun_review_v1(
    *,
    permission_semantics_canonicalization_dryrun_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(permission_semantics_canonicalization_dryrun_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    artifacts = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream dryrun verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream dryrun boundary_ok is not true")
    if up_readiness.get("ready_for_permission_semantics_canonicalization_post_dryrun_review") is not True:
        blockers.append("upstream not ready_for_permission_semantics_canonicalization_post_dryrun_review")
    if up_summary.get("canonicalization_dryrun_only") is not True:
        blockers.append("upstream canonicalization_dryrun_only is not true")
    if up_summary.get("simulated") is not True:
        blockers.append("upstream simulated is not true")
    if up_summary.get("canonicalization_enforced_now") is not False:
        blockers.append("upstream canonicalization_enforced_now is not false")
    if up_summary.get("not_enforced_now") is not True:
        blockers.append("upstream not_enforced_now is not true")
    if up_summary.get("governance_constraints_ref") != CONSTRAINT_DOC_ID:
        blockers.append("upstream governance_constraints_ref mismatch")

    observed_ne = _compute_observed_non_enforcement(up_summary, artifacts)
    if any(observed_ne.values()):
        blockers.append(f"non-enforcement violation detected: {[k for k, v in observed_ne.items() if v]}")

    completeness_rows, completeness_pass = _build_completeness_review(artifacts)
    ne_rows, ne_pass = _build_non_enforcement_matrix(observed_ne)
    registry_rows, registry_pass = _build_registry_write_review(
        artifacts.get("semantic_registry_dryrun_index_v1.json") or {}
    )
    forbidden_rows, forbidden_pass = _build_forbidden_enforcement_review(
        artifacts.get("forbidden_combination_verifier_mapping_dryrun_v1.json") or {}
    )
    norms_rows, norms_pass = _build_norms_template_review(
        artifacts.get("development_norms_phase_template_mapping_dryrun_v1.json") or {}
    )
    vcheck_rows, vcheck_pass = _build_verifier_checklist_review(
        artifacts.get("verifier_checklist_consumption_dryrun_v1.json") or {}
    )
    nclaims_rows, nclaims_pass = _build_non_claims_non_write_review(
        artifacts.get("non_claims_generation_dryrun_v1.json") or {}
    )
    cross_rows, cross_pass = _build_cross_artifact_review(
        artifacts.get("cross_artifact_consistency_dryrun_v1.json") or {}
    )

    post_non_claims_rows = [
        _review_row(
            non_claim=nc,
            required=True,
            present=True,
            risk_if_missing="post-dryrun review GO misread",
            review_pass=True,
        )
        for nc in POST_REVIEW_NON_CLAIMS
    ]

    review_pass = (
        completeness_pass
        and ne_pass
        and registry_pass
        and forbidden_pass
        and norms_pass
        and vcheck_pass
        and nclaims_pass
        and cross_pass
        and not blockers
    )
    boundary_ok = review_pass

    permission_semantics_canonicalization_post_dryrun_review_policy = _review_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_governance_constraints_ref_observed=up_summary.get("governance_constraints_ref"),
        source_ready_for_permission_semantics_canonicalization_post_dryrun_review_observed=up_readiness.get(
            "ready_for_permission_semantics_canonicalization_post_dryrun_review"
        )
        is True,
    )

    semantics_dryrun_completeness_review = {
        "rows": completeness_rows,
        "row_count": len(completeness_rows),
        "all_pass": completeness_pass,
        **_review_meta(),
    }
    semantics_non_enforcement_review_matrix = {
        "rows": ne_rows,
        "row_count": len(ne_rows),
        "all_pass": ne_pass,
        **_review_meta(),
    }
    semantic_registry_write_review = {
        "rows": registry_rows,
        "row_count": len(registry_rows),
        "all_pass": registry_pass,
        **_review_meta(),
    }
    forbidden_combination_enforcement_review = {
        "rows": forbidden_rows,
        "row_count": len(forbidden_rows),
        "all_pass": forbidden_pass,
        **_review_meta(),
    }
    development_norms_template_modification_review = {
        "rows": norms_rows,
        "row_count": len(norms_rows),
        "all_pass": norms_pass,
        **_review_meta(),
    }
    verifier_checklist_non_modification_review = {
        "rows": vcheck_rows,
        "row_count": len(vcheck_rows),
        "all_pass": vcheck_pass,
        **_review_meta(),
    }
    non_claims_generation_non_write_review = {
        "rows": nclaims_rows,
        "row_count": len(nclaims_rows),
        "all_pass": nclaims_pass,
        **_review_meta(),
    }
    semantic_dryrun_cross_artifact_review = {
        "rows": cross_rows,
        "row_count": len(cross_rows),
        "all_pass": cross_pass,
        **_review_meta(),
    }
    semantics_post_dryrun_review_non_claims_register = {
        "rows": post_non_claims_rows,
        "row_count": len(post_non_claims_rows),
        "all_present": True,
        **_review_meta(),
    }

    permission_semantics_canonicalization_post_dryrun_review_readiness_decision = {
        "ready_for_permission_semantics_canonicalization_roadmap_decision": boundary_ok,
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
        "post_dryrun_review_completed": boundary_ok,
        "semantics_dryrun_completeness_review_pass": completeness_pass,
        "semantics_non_enforcement_review_pass": ne_pass,
        "semantic_registry_write_review_pass": registry_pass,
        "forbidden_combination_enforcement_review_pass": forbidden_pass,
        "development_norms_template_modification_review_pass": norms_pass,
        "verifier_checklist_non_modification_review_pass": vcheck_pass,
        "non_claims_generation_non_write_review_pass": nclaims_pass,
        "semantic_cross_artifact_review_pass": cross_pass,
        "canonicalization_executed_now": False,
        "canonicalization_enforced_now": False,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "review_scope": REVIEW_SCOPE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "permission_semantics_canonicalization_dryrun_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_ready_for_post_review_observed": up_readiness.get(
            "ready_for_permission_semantics_canonicalization_post_dryrun_review"
        )
        is True,
        "completeness_review_count": len(completeness_rows),
        "non_enforcement_review_count": len(ne_rows),
        "registry_write_review_count": len(registry_rows),
        "forbidden_enforcement_review_count": len(forbidden_rows),
        "norms_template_review_count": len(norms_rows),
        "verifier_checklist_review_count": len(vcheck_rows),
        "non_claims_non_write_review_count": len(nclaims_rows),
        "cross_artifact_review_count": len(cross_rows),
        "post_review_non_claims_count": len(post_non_claims_rows),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_review_meta(),
    }

    input_root_matrix = {
        "rows": [
            {
                "intake_id": "permission_semantics_canonicalization_dryrun",
                "path": str(upstream["root"]) if upstream["root"] else "(not_provided)",
                "loaded": upstream["loaded"],
                "required": True,
                "missing_artifacts": upstream["missing"],
                "status": "loaded" if upstream["loaded"] else "missing_required",
                **_review_meta(),
            }
        ],
        "row_count": 1,
        **_review_meta(),
    }

    next_phase_recommendation = {
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "final_decision": FINAL_DECISION if boundary_ok else "PERMISSION_SEMANTICS_CANONICALIZATION_POST_DRYRUN_REVIEW_REQUIRES_FIXES",
        "reason": "post-dryrun review pass; semantics not enforced; roadmap decision next",
        **_review_meta(),
    }

    return {
        "summary": summary,
        "input_root_matrix": input_root_matrix,
        "permission_semantics_canonicalization_post_dryrun_review_policy": permission_semantics_canonicalization_post_dryrun_review_policy,
        "semantics_dryrun_completeness_review": semantics_dryrun_completeness_review,
        "semantics_non_enforcement_review_matrix": semantics_non_enforcement_review_matrix,
        "semantic_registry_write_review": semantic_registry_write_review,
        "forbidden_combination_enforcement_review": forbidden_combination_enforcement_review,
        "development_norms_template_modification_review": development_norms_template_modification_review,
        "verifier_checklist_non_modification_review": verifier_checklist_non_modification_review,
        "non_claims_generation_non_write_review": non_claims_generation_non_write_review,
        "semantic_dryrun_cross_artifact_review": semantic_dryrun_cross_artifact_review,
        "semantics_post_dryrun_review_non_claims_register": semantics_post_dryrun_review_non_claims_register,
        "permission_semantics_canonicalization_post_dryrun_review_readiness_decision": permission_semantics_canonicalization_post_dryrun_review_readiness_decision,
        "next_phase_recommendation": next_phase_recommendation,
    }
