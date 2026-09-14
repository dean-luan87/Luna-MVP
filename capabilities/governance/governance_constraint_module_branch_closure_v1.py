# -*- coding: utf-8 -*-
"""Governance Constraint Module Branch Closure v1.

Branch closure only: close governance constraint module branch for current mainline;
defer artifact generation planning continuation; return to registry generation authorization planning.
Does not generate request artifacts, grant authorization, or generate constraint modules.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Governance-Constraint-Module-Branch-Closure-v1-001"
CLOSURE_SCOPE = "governance_constraint_module_branch_closure_only"
SOURCE_CHAIN = "governance_constraint_module_branch_closure_v1"

SOURCE_PHASE = "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001"
UPSTREAM_REQUIRED_FINAL = (
    "GOVERNANCE_CONSTRAINT_MODULE_GENERATION_AUTHORIZATION_REQUEST_ROADMAP_DECISION_READY_FOR_ARTIFACT_GENERATION_PLANNING"
)
UPSTREAM_SELECTED_ROUTE = "Route A — Authorization Request Artifact Generation Planning"
UPSTREAM_DEFERRED_NEXT = (
    "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001"
)

FINAL_DECISION = "GOVERNANCE_CONSTRAINT_MODULE_BRANCH_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001"
MAIN_MIGRATION_RESUME_PHASE = "Phase-Registry-Generation-Authorization-Planning-v1-001"

UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "authorization_request_roadmap_decision_policy_v1.json",
    "completed_authorization_request_chain_review_v1.json",
    "authorization_request_roadmap_route_candidate_matrix_v1.json",
    "authorization_request_artifact_generation_planning_dependency_matrix_v1.json",
    "authorization_request_artifact_generation_planning_scope_v1.json",
    "authorization_request_roadmap_non_release_matrix_v1.json",
    "authorization_request_artifact_entry_readiness_risk_matrix_v1.json",
    "authorization_request_roadmap_decision_non_claims_register_v1.json",
    "authorization_request_roadmap_readiness_decision_v1.json",
)

BRANCH_CHAINS: Tuple[Tuple[str, str, str], ...] = (
    ("legacy_extraction", "Phase-Governance-Constraint-Module-Legacy-Extraction-Planning-v1-001", "governance_constraint_module_legacy_extraction_planning_v1_smoke_v0"),
    ("legacy_extraction", "Phase-Governance-Constraint-Module-Legacy-Extraction-DryRun-v1-001", "governance_constraint_module_legacy_extraction_dryrun_v1_smoke_v0"),
    ("legacy_extraction", "Phase-Governance-Constraint-Module-Legacy-Extraction-Post-DryRun-Review-v1-001", "governance_constraint_module_legacy_extraction_post_dryrun_review_v1_smoke_v0"),
    ("legacy_extraction", "Phase-Governance-Constraint-Module-Legacy-Extraction-Roadmap-Decision-v1-001", "governance_constraint_module_legacy_extraction_roadmap_decision_v1_smoke_v0"),
    ("module_generation", "Phase-Governance-Constraint-Module-Generation-Planning-v1-001", "governance_constraint_module_generation_planning_v1_smoke_v0"),
    ("module_generation", "Phase-Governance-Constraint-Module-Generation-DryRun-v1-001", "governance_constraint_module_generation_dryrun_v1_smoke_v0"),
    ("module_generation", "Phase-Governance-Constraint-Module-Generation-Post-DryRun-Review-v1-001", "governance_constraint_module_generation_post_dryrun_review_v1_smoke_v0"),
    ("module_generation", "Phase-Governance-Constraint-Module-Generation-Roadmap-Decision-v1-001", "governance_constraint_module_generation_roadmap_decision_v1_smoke_v0"),
    ("generation_authorization", "Phase-Governance-Constraint-Module-Generation-Authorization-Planning-v1-001", "governance_constraint_module_generation_authorization_planning_v1_smoke_v0"),
    ("generation_authorization", "Phase-Governance-Constraint-Module-Generation-Authorization-DryRun-v1-001", "governance_constraint_module_generation_authorization_dryrun_v1_smoke_v0"),
    ("generation_authorization", "Phase-Governance-Constraint-Module-Generation-Authorization-Post-DryRun-Review-v1-001", "governance_constraint_module_generation_authorization_post_dryrun_review_v1_smoke_v0"),
    ("generation_authorization", "Phase-Governance-Constraint-Module-Generation-Authorization-Roadmap-Decision-v1-001", "governance_constraint_module_generation_authorization_roadmap_decision_v1_smoke_v0"),
    ("authorization_request", "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Planning-v1-001", "governance_constraint_module_generation_authorization_request_planning_v1_smoke_v0"),
    ("authorization_request", "Phase-Governance-Constraint-Module-Generation-Authorization-Request-DryRun-v1-001", "governance_constraint_module_generation_authorization_request_dryrun_v1_smoke_v0"),
    ("authorization_request", "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Post-DryRun-Review-v1-001", "governance_constraint_module_generation_authorization_request_post_dryrun_review_v1_smoke_v0"),
    ("authorization_request", "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Roadmap-Decision-v1-001", "governance_constraint_module_generation_authorization_request_roadmap_decision_v1_smoke_v0"),
)

DEFERRED_CAPABILITIES: Tuple[Tuple[str, str, str], ...] = (
    (
        "DC01",
        "Authorization Request Artifact Generation Planning",
        "Superseded by branch closure; Route A from Request Roadmap Decision not pursued for current mainline",
    ),
    (
        "DC02",
        "Authorization Request Artifact Generation",
        "Deferred until explicit future branch reopen with new roadmap decision",
    ),
    ("DC03", "Authorization Request Send Planning", "Deferred; requires artifact generation planning completion first"),
    ("DC04", "Authorization Request Sent", "Deferred; no real authorization request for current mainline"),
    ("DC05", "Authorization Grant Planning", "Deferred; authorization request chain closed at planning boundary"),
    ("DC06", "Governance Constraint Module Formal Generation", "Deferred; branch delivers governance patterns as source pack only"),
    ("DC07", "Canonical Phase Template Generation", "Deferred; module generation not authorized on this branch"),
    ("DC08", "Verifier Integration on Constraint Module", "Deferred; verifier baseline not integrated on this branch"),
    ("DC09", "Phase Template Modification", "Deferred; phase templates unchanged on this branch"),
    ("DC10", "Main Migration Chain Resume via Constraint Module", "Deferred; return via Registry Generation Authorization Planning only"),
)

SOURCE_PACK_ENTRIES: Tuple[Tuple[str, str, str], ...] = (
    ("SP01", "legacy_extraction_eval_out", "governance_constraint_module_legacy_extraction_* smoke outputs"),
    ("SP02", "module_generation_planning_eval_out", "governance_constraint_module_generation_planning_* smoke outputs"),
    ("SP03", "module_generation_authorization_eval_out", "governance_constraint_module_generation_authorization_* smoke outputs"),
    ("SP04", "authorization_request_eval_out", "governance_constraint_module_generation_authorization_request_* smoke outputs"),
    ("SP05", "domain_constraint_registry", "12 domain constraints from legacy extraction planning"),
    ("SP06", "authorization_request_structure_planning", "request identity, binding, lifecycle, non-grant statements"),
    ("SP07", "authorization_request_dryrun_validation", "simulated consumption proofs for request structure"),
    ("SP08", "governance_constraints_ref", CONSTRAINT_DOC_ID),
)

RECURSIVE_STOP_REASONS: Tuple[Tuple[str, str], ...] = (
    ("recursive_chain_depth", "Four sub-chains × four phases each reached roadmap decision; further recursion is governance self-replication"),
    ("route_a_superseded", f"Upstream selected {UPSTREAM_SELECTED_ROUTE} but product decision stops before Artifact Generation Planning"),
    ("value_delivered", "Branch achieved governance commonality extraction and authorization boundary validation"),
    ("deferred_not_abandoned", "Outputs frozen as source pack and deferred capability for future explicit reopen"),
)

MAINLINE_RETURN_ITEMS: Tuple[Tuple[str, str, bool], ...] = (
    ("registry_generation_authorization_planning", MAIN_MIGRATION_RESUME_PHASE, True),
    ("return_phase_wrapper", NEXT_PHASE, True),
    ("artifact_generation_planning_continued", UPSTREAM_DEFERRED_NEXT, False),
    ("authorization_request_artifact_generation", "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-v1-001", False),
    ("real_migration_execution", "Phase-Main-Project-Structure-Migration-Real-Execution-v1-001", False),
    ("mainline_resume_via_constraint_module", "Phase-Governance-Constraint-Module-Mainline-Resume-v1-001", False),
)

BRANCH_NON_RELEASE: Tuple[str, ...] = (
    "artifact generation planning continued",
    "authorization request artifact generation",
    "authorization request generation",
    "authorization request sent",
    "authorization grant generation",
    "authorization grant issued",
    "source set final approval",
    "domain preservation approval",
    "generation authority release",
    "governance constraint module generation",
    "canonical phase template generation",
    "constraint module registration",
    "constraint enforcement",
    "verifier integration",
    "verifier modification",
    "phase template modification",
    "automation implementation",
    "documentation auto sync",
    "legacy document rewrite",
    "legacy eval_out modification",
    "legacy verifier rerun",
    "legacy chain deprecated",
    "legacy as template source restore",
    "main migration real execution resume",
    "real migration execution",
    "rollback rehearsal execution",
    "batch arming",
)

CLOSURE_NON_CLAIMS: Tuple[str, ...] = (
    "Branch Closure GO does not mean Authorization Request Artifact Generation Planning is started.",
    "Branch Closure GO does not mean authorization request artifact is generated.",
    "Branch Closure GO does not mean authorization request is sent.",
    "Branch Closure GO does not mean authorization is granted.",
    "Branch Closure GO does not mean Governance Constraint Module is formally generated.",
    "Branch Closure GO does not mean main migration chain executes real migration.",
    "Route A from Request Roadmap Decision is superseded by closure, not executed.",
    "Legacy extraction and request planning outputs remain source evidence only, not template source.",
    "Return to Registry Generation Authorization Planning does not auto-resume paused migration execution.",
    "Deferred capability register does not grant permission to reopen branch without new roadmap decision.",
)


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _closure_meta() -> Dict[str, Any]:
    return {
        "branch_closure_only": True,
        "artifact_generation_planning_continued_now": False,
        "authorization_request_artifact_generated_now": False,
        "governance_constraint_module_generation_authorization_request_artifact_generated_now": False,
        "authorization_request_sent_now": False,
        "governance_constraint_module_generation_authorization_request_sent_now": False,
        "authorization_granted_now": False,
        "governance_constraint_module_generation_authorized_now": False,
        "governance_constraint_module_generated_now": False,
        "canonical_phase_template_generated_now": False,
        "constraint_module_registered_now": False,
        "constraint_enforced_now": False,
        "verifier_integration_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "automation_implemented_now": False,
        "documentation_auto_sync_executed_now": False,
        "legacy_phase_modified_now": False,
        "legacy_document_rewritten_now": False,
        "legacy_eval_out_modified_now": False,
        "legacy_verifier_rerun_now": False,
        "legacy_chain_deprecated_now": False,
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
        "main_migration_resume_phase": MAIN_MIGRATION_RESUME_PHASE,
        "main_migration_resume_target": MAIN_MIGRATION_RESUME_PHASE,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "runtime_invoked": False,
        "execution_committed": False,
        "success_claim_allowed": False,
        "real_rehearsal_execution_allowed": False,
        "real_migration_execution_allowed": False,
        "batch_arming_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _closure_row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_closure_meta()}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _eval_out_root() -> Path:
    return Path(__file__).resolve().parents[2] / "_eval_out"


def _load_upstream(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    readiness = _try_read_json(root / "authorization_request_roadmap_readiness_decision_v1.json") if root else None
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


def _load_chain_phase(eval_out_name: str) -> Dict[str, Any]:
    root = _eval_out_root() / eval_out_name
    return {
        "summary": _try_read_json(root / "summary.json") or {},
        "verifier": _try_read_json(root / "verifier_report.json") or {},
    }


def _build_completed_branch_chain_review() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    all_pass = True
    for branch_id, phase_name, eval_out in BRANCH_CHAINS:
        data = _load_chain_phase(eval_out)
        sm = data["summary"]
        vr = data["verifier"]
        go = vr.get("verifier") == "GO" and vr.get("passed") is True
        boundary = sm.get("boundary_ok") is True
        review_pass = go and boundary
        if not review_pass:
            all_pass = False
        artifact_gen = sm.get("governance_constraint_module_generation_authorization_request_artifact_generated_now")
        if artifact_gen is None:
            artifact_gen = sm.get("authorization_request_artifact_generated_now")
        rows.append(
            _closure_row(
                branch_id=branch_id,
                phase_name=phase_name,
                eval_out_dir=eval_out,
                verifier_status=vr.get("verifier", "UNKNOWN"),
                boundary_ok=boundary,
                final_decision=sm.get("final_decision"),
                recommended_next_phase=sm.get("recommended_next_phase"),
                request_artifact_generation_observed=artifact_gen is True,
                request_sent_observed=sm.get("governance_constraint_module_generation_authorization_request_sent_now")
                is True
                or sm.get("authorization_request_sent_now") is True,
                authorization_grant_observed=sm.get("governance_constraint_module_generation_authorized_now") is True
                or sm.get("authorization_granted_now") is True,
                module_generation_observed=sm.get("governance_constraint_module_generated_now") is True,
                mainline_resume_observed=sm.get("main_migration_chain_resumed_now") is True,
                review_status="pass" if review_pass else "fail",
            )
        )
    return rows, all_pass


def run_governance_constraint_module_branch_closure_v1(
    *,
    governance_constraint_module_generation_authorization_request_roadmap_decision_root: str,
) -> Dict[str, Any]:
    upstream = _load_upstream(governance_constraint_module_generation_authorization_request_roadmap_decision_root)
    up_summary = upstream["summary"]
    up_verifier = upstream["verifier"]
    up_readiness = upstream["readiness"]
    up_art = upstream["artifacts"]

    blockers: List[str] = []
    if not upstream["loaded"]:
        blockers.append(f"missing upstream artifacts: {upstream['missing']}")
    if up_verifier.get("verifier") != "GO" or up_verifier.get("passed") is not True:
        blockers.append("upstream request roadmap decision verifier is not GO")
    if up_summary.get("boundary_ok") is not True:
        blockers.append("upstream boundary_ok is not true")
    if up_summary.get("final_decision") != UPSTREAM_REQUIRED_FINAL:
        blockers.append(f"upstream final_decision must be {UPSTREAM_REQUIRED_FINAL}")
    if up_readiness.get("ready_for_governance_constraint_module_generation_authorization_request_artifact_generation_planning") is not True:
        blockers.append("upstream roadmap not ready_for_artifact_generation_planning (GO prerequisite)")

    for flag in (
        "governance_constraint_module_generation_authorization_request_generated_now",
        "governance_constraint_module_generation_authorization_request_sent_now",
        "governance_constraint_module_generation_authorized_now",
        "governance_constraint_module_generated_now",
        "main_migration_chain_resumed_now",
    ):
        if up_summary.get(flag) is not False:
            blockers.append(f"upstream {flag} must remain false")

    artifact_flag = up_summary.get("governance_constraint_module_generation_authorization_request_artifact_generated_now")
    if artifact_flag is not None and artifact_flag is not False:
        blockers.append("upstream request artifact must not be generated")

    route_a = next(
        (r for r in (up_art.get("authorization_request_roadmap_route_candidate_matrix_v1.json", {}).get("rows") or []) if r.get("route_id") == "A"),
        {},
    )
    if route_a.get("selected_now") is not True:
        blockers.append("upstream Route A must have been selected (closure supersedes it)")

    chain_rows, chain_pass = _build_completed_branch_chain_review()
    if not chain_pass:
        blockers.append("not all branch chain phases are GO with boundary_ok")

    if any(r.get("request_artifact_generation_observed") for r in chain_rows):
        blockers.append("request artifact generation must not be observed in branch chain")
    if any(r.get("request_sent_observed") for r in chain_rows):
        blockers.append("request sent must not be observed in branch chain")
    if any(r.get("module_generation_observed") for r in chain_rows):
        blockers.append("formal module generation must not be observed in branch chain")

    deferred_rows = [
        _closure_row(
            deferred_id=did,
            capability_name=name,
            deferral_reason=reason,
            deferred_for_current_mainline=True,
            reopen_requires_new_roadmap_decision=True,
            artifact_generation_planning_continued_now=False,
        )
        for did, name, reason in DEFERRED_CAPABILITIES
    ]
    source_rows = [
        _closure_row(
            source_pack_id=spid,
            source_pack_name=name,
            source_pack_role=role,
            legacy_as_source_evidence=True,
            legacy_as_template_source=False,
            consumable_in_future_mainline_only=True,
        )
        for spid, name, role in SOURCE_PACK_ENTRIES
    ]
    stop_rows = [
        _closure_row(stop_reason_id=sid, stop_reason=reason, recursive_expansion_halted=True)
        for sid, reason in RECURSIVE_STOP_REASONS
    ]
    return_rows = [
        _closure_row(
            return_item=item,
            target_phase=target,
            allowed_now=allowed,
            artifact_generation_planning_continued_now=False,
        )
        for item, target, allowed in MAINLINE_RETURN_ITEMS
    ]
    non_release_rows = [
        _closure_row(
            permission_name=name,
            expected_released=False,
            released_by_branch_closure=False,
            review_pass=True,
        )
        for name in BRANCH_NON_RELEASE
    ]
    non_claims_rows = [
        _closure_row(non_claim=nc, required=True, present=True, risk_if_missing="closure GO misread")
        for nc in CLOSURE_NON_CLAIMS
    ]

    route_a_deferred = any(
        d.get("capability_name") == "Authorization Request Artifact Generation Planning"
        and d.get("deferred_for_current_mainline") is True
        for d in deferred_rows
    )
    mainline_return_ok = any(
        r.get("return_item") == "registry_generation_authorization_planning"
        and r.get("allowed_now") is True
        and r.get("target_phase") == MAIN_MIGRATION_RESUME_PHASE
        for r in return_rows
    )
    artifact_planning_blocked = all(
        r.get("allowed_now") is False
        for r in return_rows
        if "artifact_generation" in str(r.get("return_item", ""))
    )

    closure_ready = (
        chain_pass
        and route_a_deferred
        and mainline_return_ok
        and artifact_planning_blocked
        and not blockers
    )
    boundary_ok = closure_ready

    governance_constraint_module_branch_closure_policy = _closure_row(
        phase_name=PHASE_ID,
        source_phase=SOURCE_PHASE,
        source_verifier_go_observed=up_verifier.get("verifier") == "GO",
        source_boundary_ok_observed=up_summary.get("boundary_ok") is True,
        source_selected_route_observed=up_summary.get("selected_route"),
        upstream_recommended_next_phase_superseded=UPSTREAM_DEFERRED_NEXT,
        artifact_generation_planning_continued_now=False,
        authorization_request_artifact_generation_deferred=True,
    )

    completed_governance_constraint_module_branch_chain_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "all_pass": chain_pass,
        "branch_count": 4,
        "phase_count_per_branch": 4,
        **_closure_meta(),
    }
    deferred_capability_register = {
        "rows": deferred_rows,
        "row_count": len(deferred_rows),
        "authorization_request_artifact_generation_planning_deferred": route_a_deferred,
        "all_deferred_for_current_mainline": all(d.get("deferred_for_current_mainline") for d in deferred_rows),
        **_closure_meta(),
    }
    source_pack_register = {
        "rows": source_rows,
        "row_count": len(source_rows),
        "legacy_extraction_as_source_pack": True,
        "all_source_pack_not_template": all(r.get("legacy_as_template_source") is False for r in source_rows),
        **_closure_meta(),
    }
    recursive_expansion_stop_decision = {
        "rows": stop_rows,
        "row_count": len(stop_rows),
        "recursive_expansion_halted": True,
        "upstream_route_a_superseded_by_closure": True,
        "artifact_generation_planning_continued_now": False,
        **_closure_meta(),
    }
    mainline_return_readiness_matrix = {
        "rows": return_rows,
        "row_count": len(return_rows),
        "main_migration_resume_target": MAIN_MIGRATION_RESUME_PHASE,
        "artifact_generation_planning_return_blocked": artifact_planning_blocked,
        **_closure_meta(),
    }
    branch_non_release_matrix = {
        "rows": non_release_rows,
        "row_count": len(non_release_rows),
        "all_pass": all(r.get("review_pass") for r in non_release_rows),
        **_closure_meta(),
    }
    branch_closure_non_claims_register = {
        "rows": non_claims_rows,
        "row_count": len(non_claims_rows),
        "all_present": True,
        **_closure_meta(),
    }

    governance_constraint_module_branch_closure_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_BRANCH_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "branch_closed_for_current_mainline": boundary_ok,
        "governance_constraint_module_as_deferred_capability": boundary_ok,
        "legacy_extraction_as_source_pack": boundary_ok,
        "authorization_request_artifact_generation_deferred": boundary_ok,
        "artifact_generation_planning_continued_now": False,
        "branch_closure_completed": boundary_ok,
        "completed_branch_chain_review_pass": chain_pass,
        "deferred_capability_register_complete": route_a_deferred,
        "source_pack_register_complete": len(source_rows) >= 8,
        "recursive_expansion_stop_recorded": True,
        "mainline_return_ready": mainline_return_ok,
        "main_migration_resume_target": MAIN_MIGRATION_RESUME_PHASE,
        **_closure_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "closure_scope": CLOSURE_SCOPE,
        "governance_constraint_module_generation_authorization_request_roadmap_decision_input_loaded": upstream["loaded"],
        "source_verifier_go_observed": up_verifier.get("verifier") == "GO",
        "source_boundary_ok_observed": up_summary.get("boundary_ok") is True,
        "source_selected_route_observed": up_summary.get("selected_route"),
        "upstream_recommended_next_phase_superseded": UPSTREAM_DEFERRED_NEXT,
        "completed_branch_phase_count": len(chain_rows),
        "deferred_capability_count": len(deferred_rows),
        "source_pack_count": len(source_rows),
        "branch_non_release_count": len(non_release_rows),
        "artifact_generation_planning_continued_now": False,
        "authorization_request_artifact_generation_deferred": True,
        "branch_closed_for_current_mainline": boundary_ok,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "GOVERNANCE_CONSTRAINT_MODULE_BRANCH_CLOSURE_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_closure_meta(),
    }

    return {
        "summary": summary,
        "governance_constraint_module_branch_closure_policy": governance_constraint_module_branch_closure_policy,
        "completed_governance_constraint_module_branch_chain_review": completed_governance_constraint_module_branch_chain_review,
        "deferred_capability_register": deferred_capability_register,
        "source_pack_register": source_pack_register,
        "recursive_expansion_stop_decision": recursive_expansion_stop_decision,
        "mainline_return_readiness_matrix": mainline_return_readiness_matrix,
        "branch_non_release_matrix": branch_non_release_matrix,
        "branch_closure_non_claims_register": branch_closure_non_claims_register,
        "governance_constraint_module_branch_closure_readiness_decision": governance_constraint_module_branch_closure_readiness_decision,
    }
