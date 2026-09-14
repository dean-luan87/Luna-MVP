# -*- coding: utf-8 -*-
"""Return To Registry Generation Authorization Planning v1.

Return-to-mainline wrapper only: bind mainline resume target after Governance Constraint Module
branch closure. Does not execute registry generation authorization planning, registry generation,
request/grant/module generation, or real migration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001"
RETURN_SCOPE = "return_to_registry_generation_authorization_planning_only"
SOURCE_CHAIN = "return_to_registry_generation_authorization_planning_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Branch-Closure-v1-001"
UPSTREAM_REQUIRED_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_BRANCH_CLOSED_FOR_CURRENT_MAINLINE"
UPSTREAM_REQUIRED_NEXT = "Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001"
MAINLINE_RESUME_TARGET = "Phase-Registry-Generation-Authorization-Planning-v1-001"
ARTIFACT_PLANNING_DEFERRED_PHASE = (
    "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001"
)

FINAL_DECISION = "RETURN_TO_REGISTRY_GENERATION_AUTHORIZATION_PLANNING_READY"
NEXT_PHASE = MAINLINE_RESUME_TARGET

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_branch_closure_policy_v1.json",
    "completed_governance_constraint_module_branch_chain_review_v1.json",
    "deferred_capability_register_v1.json",
    "source_pack_register_v1.json",
    "recursive_expansion_stop_decision_v1.json",
    "mainline_return_readiness_matrix_v1.json",
    "branch_non_release_matrix_v1.json",
    "branch_closure_non_claims_register_v1.json",
    "governance_constraint_module_branch_closure_readiness_decision_v1.json",
)

SOURCE_PACK_REFS: Tuple[Tuple[str, str, str], ...] = (
    ("REF01", "governance_constraint_module_branch_closure_v1_smoke_v0", "branch closure verdict and non-release matrix"),
    ("REF02", "governance_constraint_module_legacy_extraction_*", "legacy extraction source pack"),
    ("REF03", "governance_constraint_module_generation_*", "module generation planning/dryrun/review artifacts"),
    ("REF04", "governance_constraint_module_generation_authorization_*", "generation authorization chain artifacts"),
    ("REF05", "governance_constraint_module_generation_authorization_request_*", "authorization request chain artifacts"),
    ("REF06", "deferred_capability_register_v1", "deferred capabilities; not enforced on mainline"),
    ("REF07", "migration_governance_development_constraints_v1", CONSTRAINT_DOC_ID),
)

REENTRY_SCOPE_RULES: Tuple[Tuple[str, bool, str], ...] = (
    ("only_resume_target_phase_registry_generation_authorization_planning", True, MAINLINE_RESUME_TARGET),
    ("inherit_governance_constraint_module_formal_generation_authority", False, "module generation remains deferred"),
    ("auto_generate_authorization_request_artifact", False, "artifact generation planning chain remains closed"),
    ("auto_enable_verifier_template_integration", False, "verifier/template unchanged on return"),
    ("governance_constraint_module_outputs_as_reference_only", True, "reference / source pack / deferred capability only"),
    ("mainline_may_reference_non_claims_domain_preservation_legacy_evidence", True, "read-only reference; no enforcement"),
    ("resume_artifact_generation_planning_recursion", False, "Route A superseded by branch closure"),
)

RETURN_NON_RELEASE: Tuple[str, ...] = (
    "registry generation authorization planning executed",
    "registry generation",
    "registry generation authorization request sent",
    "registry generation authorized",
    "boundary object registry generated",
    "governance constraint module generated",
    "authorization request artifact generated",
    "authorization request sent",
    "authorization grant issued",
    "canonical phase template generated",
    "verifier integration",
    "verifier modification",
    "phase template modification",
    "file operation",
    "real migration execution",
    "rollback rehearsal execution",
    "batch arming",
    "artifact generation planning continued",
    "main migration chain real execution resumed",
)

RETURN_NON_CLAIMS: Tuple[str, ...] = (
    "Branch Closure GO does not mean Governance Constraint Module is generated.",
    "Return-To-Mainline GO does not mean registry generation authorization planning has executed.",
    "Return-To-Mainline GO does not mean registry generation is authorized.",
    "Governance Constraint Module source pack does not mean formal module is active.",
    "Deferred capability does not mean current mainline may use it as enforced constraint.",
    "Returning to mainline does not release real migration / rollback / batch arming.",
    "Returning to mainline does not modify verifier or phase template.",
    "Returning to mainline does not resume artifact generation recursion.",
    "Return wrapper GO does not open execution window or owner/operator approval.",
    "Binding to Registry Generation Authorization Planning does not auto-run that phase.",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _return_meta() -> Dict[str, Any]:
    return {
        "return_to_mainline_wrapper_only": True,
        "registry_generation_authorization_planning_executed_now": False,
        "registry_generation_authorization_request_sent_now": False,
        "registry_generation_authorized_now": False,
        "boundary_object_registry_generated_now": False,
        "governance_constraint_module_generated_now": False,
        "authorization_request_artifact_generated_now": False,
        "governance_constraint_module_generation_authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "authorization_granted_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "verifier_integration_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "artifact_generation_planning_continued_now": False,
        "authorization_request_artifact_generation_deferred": True,
        "branch_closure_only": False,
        "governance_constraint_module_branch_closed": True,
        "governance_constraint_module_as_deferred_capability": True,
        "legacy_extraction_as_source_pack": True,
        "legacy_as_source_evidence": True,
        "legacy_as_template_source": False,
        "domain_specific_rules_preserved": True,
        "frozen_fields_enforced_now": False,
        "verifier_baseline_integrated_now": False,
        "file_operation_executed_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "main_migration_chain_resumed_now": False,
        "main_migration_chain_paused": True,
        "main_migration_resume_phase": MAINLINE_RESUME_TARGET,
        "mainline_resume_target": MAINLINE_RESUME_TARGET,
        "main_migration_resume_target": MAINLINE_RESUME_TARGET,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "runtime_invoked": False,
        "execution_committed": False,
        "success_claim_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _return_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_return_meta()}


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
        root / "governance_constraint_module_branch_closure_readiness_decision_v1.json"
    ) if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in UPSTREAM_ARTIFACTS:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
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


def run_return_to_registry_generation_authorization_planning_v1(
    *,
    governance_constraint_module_branch_closure_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_branch_closure_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream branch closure verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_summary.get("branch_closure_only") is not True:
        blockers.append("upstream branch_closure_only must be true")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_summary.get("recommended_next_phase") != UPSTREAM_REQUIRED_NEXT:
        blockers.append(f"upstream recommended_next_phase must be {UPSTREAM_REQUIRED_NEXT}")
    if up_summary.get("main_migration_resume_target") != MAINLINE_RESUME_TARGET:
        blockers.append(f"upstream main_migration_resume_target must be {MAINLINE_RESUME_TARGET}")
    if up_readiness.get("branch_closed_for_current_mainline") is not True:
        blockers.append("upstream branch not closed for current mainline")

    for flag in (
        "artifact_generation_planning_continued_now",
        "authorization_request_artifact_generated_now",
        "authorization_request_sent_now",
        "authorization_granted_now",
        "governance_constraint_module_generated_now",
        "canonical_phase_template_generated_now",
        "verifier_modified_now",
        "phase_template_modified_now",
        "main_migration_chain_resumed_now",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")

    deferred_reg = up_art.get("deferred_capability_register_v1.json", {})
    source_reg = up_art.get("source_pack_register_v1.json", {})
    stop_dec = up_art.get("recursive_expansion_stop_decision_v1.json", {})
    mainline_mat = up_art.get("mainline_return_readiness_matrix_v1.json", {})

    if deferred_reg.get("authorization_request_artifact_generation_planning_deferred") is not True:
        blockers.append("upstream artifact generation planning must be deferred")
    if source_reg.get("legacy_extraction_as_source_pack") is not True:
        blockers.append("upstream legacy extraction must be source pack")
    if stop_dec.get("artifact_generation_planning_continued_now") is not False:
        blockers.append("upstream recursive stop must block artifact planning continuation")
    if stop_dec.get("recursive_expansion_halted") is not True:
        blockers.append("upstream recursive expansion must be halted")

    reg_row = next(
        (r for r in (mainline_mat.get("rows") or []) if r.get("return_item") == "registry_generation_authorization_planning"),
        {},
    )
    if reg_row.get("allowed_now") is not True or reg_row.get("target_phase") != MAINLINE_RESUME_TARGET:
        blockers.append("upstream mainline return matrix must allow registry planning target")

    branch_review = up_art.get("completed_governance_constraint_module_branch_chain_review_v1.json", {})
    if branch_review.get("all_pass") is not True:
        blockers.append("upstream branch chain review must be all_pass")

    input_review_rows = [
        _return_row(
            check_id=cid,
            check_name=name,
            expected=expected,
            observed=observed,
            review_pass=observed == expected,
        )
        for cid, name, expected, observed in (
            ("IR01", "verifier_go", True, up_verifier.get("verifier") == "GO" and up_verifier.get("passed") is True),
            ("IR02", "boundary_ok", True, up_summary.get("boundary_ok") is True),
            ("IR03", "branch_closure_only", True, up_summary.get("branch_closure_only") is True),
            ("IR04", "final_decision", UPSTREAM_REQUIRED_FINAL, up_summary.get("final_decision")),
            ("IR05", "recommended_next_phase", UPSTREAM_REQUIRED_NEXT, up_summary.get("recommended_next_phase")),
            ("IR06", "main_migration_resume_target", MAINLINE_RESUME_TARGET, up_summary.get("main_migration_resume_target")),
            ("IR07", "artifact_planning_not_continued", False, up_summary.get("artifact_generation_planning_continued_now")),
            ("IR08", "branch_closed", True, up_summary.get("branch_closed_for_current_mainline")),
            ("IR09", "artifact_deferred", True, up_summary.get("authorization_request_artifact_generation_deferred")),
            ("IR10", "main_not_resumed", False, up_summary.get("main_migration_chain_resumed_now")),
        )
    ]
    input_review_pass = all(r.get("review_pass") for r in input_review_rows) and not blockers

    source_ref_rows = [
        _return_row(
            reference_id=rid,
            reference_path=path,
            reference_role=role,
            formal_module_active=False,
            enforced_on_mainline=False,
        )
        for rid, path, role in SOURCE_PACK_REFS
    ]

    reentry_rows = [
        _return_row(
            scope_rule_id=rule_id,
            allowed=allowed,
            rationale=rationale,
            registry_generation_authorization_planning_executed_now=False,
        )
        for rule_id, allowed, rationale in REENTRY_SCOPE_RULES
    ]

    target_binding = _return_row(
        mainline_resume_target=MAINLINE_RESUME_TARGET,
        recommended_next_phase_after_return=NEXT_PHASE,
        governance_constraint_module_branch_closed=True,
        return_wrapper_phase=PHASE_ID,
        artifact_generation_planning_recursion_blocked=True,
        blocked_resume_phase=ARTIFACT_PLANNING_DEFERRED_PHASE,
    )

    non_release_rows = [
        _return_row(
            permission_name=name,
            expected_released=False,
            released_by_return_wrapper=False,
            review_pass=True,
        )
        for name in RETURN_NON_RELEASE
    ]

    non_claims_rows = [
        _return_row(non_claim=nc, required=True, present=True, risk_if_missing="return GO misread")
        for nc in RETURN_NON_CLAIMS
    ]

    only_registry_resume = any(
        r.get("scope_rule_id") == "only_resume_target_phase_registry_generation_authorization_planning"
        and r.get("allowed") is True
        and MAINLINE_RESUME_TARGET in str(r.get("rationale", ""))
        for r in reentry_rows
    )
    no_artifact_recursion = any(
        r.get("scope_rule_id") == "resume_artifact_generation_planning_recursion" and r.get("allowed") is False
        for r in reentry_rows
    )
    reference_only = any(
        r.get("scope_rule_id") == "governance_constraint_module_outputs_as_reference_only" and r.get("allowed") is True
        for r in reentry_rows
    )

    return_ready = (
        input_review_pass
        and only_registry_resume
        and no_artifact_recursion
        and reference_only
        and not blockers
    )
    boundary_ok = return_ready

    return_to_registry_generation_authorization_planning_policy = _return_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        mainline_resume_target=MAINLINE_RESUME_TARGET,
        registry_generation_authorization_planning_executed_now=False,
    )

    branch_closure_input_review = {
        "rows": input_review_rows,
        "row_count": len(input_review_rows),
        "all_pass": input_review_pass,
        **_return_meta(),
    }
    deferred_governance_constraint_module_source_pack_reference = {
        "rows": source_ref_rows,
        "row_count": len(source_ref_rows),
        "governance_constraint_module_as_deferred_capability": True,
        "legacy_extraction_as_source_pack": True,
        "formal_module_active": False,
        **_return_meta(),
    }
    mainline_resume_target_binding = target_binding
    return_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": all(r.get("review_pass") for r in non_release_rows),
        **_return_meta(),
    }
    registry_generation_authorization_planning_reentry_scope = {
        "rows": reentry_rows,
        "row_count": len(reentry_rows),
        "only_allowed_resume_target": MAINLINE_RESUME_TARGET,
        "artifact_generation_planning_recursion_blocked": no_artifact_recursion,
        "governance_constraint_module_reference_only": reference_only,
        **_return_meta(),
    }
    return_to_mainline_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_return_meta(),
    }

    return_to_registry_generation_authorization_planning_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "RETURN_TO_REGISTRY_GENERATION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "mainline_resume_target": MAINLINE_RESUME_TARGET,
        "governance_constraint_module_branch_closed": boundary_ok,
        "governance_constraint_module_as_deferred_capability": boundary_ok,
        "legacy_extraction_as_source_pack": boundary_ok,
        "return_to_mainline_completed": boundary_ok,
        "branch_closure_input_review_pass": input_review_pass,
        "mainline_resume_target_bound": boundary_ok,
        "registry_generation_authorization_planning_executed_now": False,
        **_return_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "return_scope": RETURN_SCOPE,
        "governance_constraint_module_branch_closure_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "governance_constraint_module_branch_closed": boundary_ok,
        "governance_constraint_module_as_deferred_capability": True,
        "legacy_extraction_as_source_pack": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "RETURN_TO_REGISTRY_GENERATION_AUTHORIZATION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_return_meta(),
    }

    return {
        "summary": summary,
        "return_to_registry_generation_authorization_planning_policy": return_to_registry_generation_authorization_planning_policy,
        "branch_closure_input_review": branch_closure_input_review,
        "deferred_governance_constraint_module_source_pack_reference": deferred_governance_constraint_module_source_pack_reference,
        "mainline_resume_target_binding": mainline_resume_target_binding,
        "return_non_release_matrix": return_non_release_matrix,
        "registry_generation_authorization_planning_reentry_scope": registry_generation_authorization_planning_reentry_scope,
        "return_to_mainline_non_claims_register": return_to_mainline_non_claims_register,
        "return_to_registry_generation_authorization_planning_readiness_decision": return_to_registry_generation_authorization_planning_readiness_decision,
    }
