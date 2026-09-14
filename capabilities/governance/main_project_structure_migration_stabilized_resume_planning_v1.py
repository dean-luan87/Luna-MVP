# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Resume Planning v1.

Stabilized resume planning only: re-take engineering structure migration mainline after
governance branch closure. Does not move/delete/rename/merge files or execute real migration.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import (
    BATCH_DEFS,
    GATE_DEFS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Resume-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_stabilized_resume_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_resume_planning_v1"

RETURN_SOURCE_PHASE = "Phase-Return-To-Registry-Generation-Authorization-Planning-v1-001"
RETURN_REQUIRED_FINAL = "RETURN_TO_REGISTRY_GENERATION_AUTHORIZATION_PLANNING_READY"
CLOSURE_SOURCE_PHASE = "Phase-Governance-Constraint-Module-Branch-Closure-v1-001"
CLOSURE_REQUIRED_FINAL = "GOVERNANCE_CONSTRAINT_MODULE_BRANCH_CLOSED_FOR_CURRENT_MAINLINE"

PAUSED_REGISTRY_RESUME_POINT = "Phase-Registry-Generation-Authorization-Planning-v1-001"
PAUSED_REGISTRY_NEXT_WOULD_BE = "Phase-Registry-Generation-Authorization-DryRun-v1-001"
PAUSED_GC_ARTIFACT_PLANNING = (
    "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001"
)

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_RESUME_PLANNING_READY_FOR_EXECUTION_PLANNING"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-Planning-v1-001"

RETURN_UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "return_to_registry_generation_authorization_planning_policy_v1.json",
    "registry_generation_authorization_planning_reentry_scope_v1.json",
    "return_to_registry_generation_authorization_planning_readiness_decision_v1.json",
)

CLOSURE_UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "governance_constraint_module_branch_closure_policy_v1.json",
    "deferred_capability_register_v1.json",
    "recursive_expansion_stop_decision_v1.json",
    "governance_constraint_module_branch_closure_readiness_decision_v1.json",
)

MAIN_MIGRATION_CHAIN: Tuple[Tuple[str, str, str], ...] = (
    ("readiness", "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001", "main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0"),
    ("guarded", "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001", "main_project_structure_migration_guarded_planning_v1_smoke_v0"),
    ("guarded", "Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001", "main_project_structure_migration_guarded_dryrun_v1_smoke_v0"),
    ("guarded", "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001", "main_project_structure_migration_guarded_post_dryrun_review_v1_smoke_v0"),
    ("guarded", "Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001", "main_project_structure_migration_guarded_closure_v1_smoke_v0"),
    ("guarded", "Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001", "main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0"),
    ("execution_control", "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001", "main_project_structure_migration_execution_control_and_test_harness_planning_v1_smoke_v0"),
    ("execution_control", "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001", "main_project_structure_migration_execution_control_and_test_harness_dryrun_v1_smoke_v0"),
    ("execution_control", "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001", "main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1_smoke_v0"),
    ("execution_control", "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001", "main_project_structure_migration_execution_control_and_test_harness_closure_v1_smoke_v0"),
    ("execution_control", "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001", "main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1_smoke_v0"),
    ("controlled_execution", "Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001", "main_project_structure_migration_controlled_execution_planning_v1_smoke_v0"),
    ("controlled_execution", "Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001", "main_project_structure_migration_controlled_execution_dryrun_v1_smoke_v0"),
    ("controlled_execution", "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001", "main_project_structure_migration_controlled_execution_post_dryrun_review_v1_smoke_v0"),
    ("controlled_execution", "Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001", "main_project_structure_migration_controlled_execution_closure_v1_smoke_v0"),
    ("controlled_execution", "Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001", "main_project_structure_migration_controlled_execution_roadmap_decision_v1_smoke_v0"),
    ("pre_auth", "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001", "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0"),
    ("pre_auth", "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001", "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1_smoke_v0"),
    ("pre_auth", "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001", "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1_smoke_v0"),
    ("pre_auth", "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001", "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001", "main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001", "main_project_structure_migration_rollback_rehearsal_dryrun_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001", "main_project_structure_migration_rollback_rehearsal_post_dryrun_review_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001", "main_project_structure_migration_rollback_rehearsal_closure_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001", "main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001", "main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001", "main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001", "main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1_smoke_v0"),
    ("rollback_rehearsal", "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001", "main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1_smoke_v0"),
    ("real_rehearsal_pre_auth", "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001", "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_planning_v1_smoke_v0"),
    ("real_rehearsal_pre_auth", "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-DryRun-v1-001", "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_dryrun_v1_smoke_v0"),
    ("real_rehearsal_pre_auth", "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Post-DryRun-Review-v1-001", "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_post_dryrun_review_v1_smoke_v0"),
    ("real_rehearsal_pre_auth", "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Roadmap-Decision-v1-001", "main_project_structure_migration_real_rollback_rehearsal_pre_authorization_roadmap_decision_v1_smoke_v0"),
)

PAUSED_BRANCHES: Tuple[Tuple[str, str, str], ...] = (
    ("governance_constraint_module", "GC branch closed; reference/source pack/deferred only", PAUSED_GC_ARTIFACT_PLANNING),
    ("registry_authorization", "Registry Authorization branch paused; structure migration priority", PAUSED_REGISTRY_NEXT_WOULD_BE),
    ("governance_debt_canonicalization", "Governance debt register Route A deferred; no new large governance recursion", "Phase-Permission-Semantics-Canonicalization-Planning-v1-001"),
)

STABILIZATION_PRINCIPLES: Tuple[Tuple[str, str], ...] = (
    ("SP01", "No new large governance recursion chains during structure migration"),
    ("SP02", "Completed governance branches are constraint reference only, not enforced modules"),
    ("SP03", "Target project structure frozen after this resume; changes only via small patch phases"),
    ("SP04", "Each migration batch requires before/after manifest"),
    ("SP05", "Each migration batch requires rollback route"),
    ("SP06", "Each migration batch requires verifier rerun list"),
    ("SP07", "Each batch single domain only; no mixed capability/docs/protected moves"),
    ("SP08", "eval_out historical outputs read-only; excluded from migration"),
    ("SP09", "protected assets / HR / DnAE never moved, rewritten, or merged"),
    ("SP10", "dry-run → review → controlled execution rhythm preserved"),
)

TARGET_STRUCTURE_RULES: Tuple[Tuple[str, bool, str], ...] = (
    ("capabilities/", True, "runtime and governance capabilities remain primary code home"),
    ("tools/evaluation/", True, "runners and verifiers stay colocated with evaluation governance"),
    ("docs/architecture/", True, "architecture docs index and phase packs"),
    ("_eval_out/", False, "historical eval outputs frozen read-only"),
    ("protected assets", False, "never migration targets"),
    ("human review queue", False, "never migration targets"),
    ("DnAE permanent block", False, "never migration targets"),
)

PROTECTED_AND_FORBIDDEN: Tuple[Tuple[str, str, bool], ...] = (
    ("protected_assets", "no move / no rewrite / no merge", True),
    ("human_review_queue", "no move / no rewrite / no merge", True),
    ("dnae_permanent_block", "no move / no rewrite / no merge", True),
    ("eval_out_historical", "read-only; no migration participation", True),
    ("verifier_reports_historical", "read-only reference", True),
    ("go_no_go_packs_historical", "read-only reference", True),
    ("governance_constraint_module_formal", "deferred; not enforced", True),
    ("boundary_object_registry_formal", "not generated on this resume path", True),
    ("file_delete", "forbidden until controlled batch authorization", True),
    ("file_rename", "forbidden until controlled batch authorization", True),
    ("file_merge", "forbidden until controlled batch authorization", True),
    ("batch_arming", "forbidden in resume planning", True),
    ("real_migration", "forbidden in resume planning", True),
    ("rollback_rehearsal_execution", "forbidden in resume planning", True),
)

TEST_VERIFIER_ITEMS: Tuple[Tuple[str, str, str], ...] = (
    ("TV01", "test_before_batch", "run bound pre-migration tests for batch scope before arming"),
    ("TV02", "test_after_batch", "run bound post-migration tests for batch scope after simulated/controlled move"),
    ("TV03", "verifier_rerun_after_batch", "rerun verifiers listed in batch manifest"),
    ("TV04", "docs_link_check", "docs/architecture link integrity after doc batches"),
    ("TV05", "import_path_check", "python import paths after capability grouping batches"),
    ("TV06", "eval_out_immutability_check", "confirm eval_out not mutated by migration tooling"),
    ("TV07", "protected_asset_integrity_check", "confirm protected assets unchanged"),
    ("TV08", "hr_carryover_check", "confirm HR queue carryover unchanged"),
    ("TV09", "dnae_carryover_check", "confirm DnAE carryover unchanged"),
    ("TV10", "rollback_checkpoint_check", "confirm rollback checkpoint recorded per batch"),
)

ROLLBACK_REHEARSAL_REQUIREMENTS: Tuple[Tuple[str, str], ...] = (
    ("RR01", "rollback rehearsal remains mandatory before controlled batch execution authorization"),
    ("RR02", "rehearsal dry-run chain already completed; execution rehearsal still blocked until execution planning GO"),
    ("RR03", "sandbox restore map required before any real batch"),
    ("RR04", "verdict table and docs linkage must be restorable"),
    ("RR05", "no rollback success claim from planning or dry-run alone"),
    ("RR06", "8 rollback checkpoints from guarded chain remain binding"),
)

MINIMIZED_PHASE_TEMPLATE: Tuple[Tuple[str, str, str], ...] = (
    ("MPT01", "Stabilized Resume Planning", PHASE_ID),
    ("MPT02", "Stabilized Execution Planning", NEXT_PHASE),
    ("MPT03", "Stabilized Execution DryRun", "Phase-Main-Project-Structure-Migration-Stabilized-Execution-DryRun-v1-001"),
    ("MPT04", "Post-DryRun Review", "Phase-Main-Project-Structure-Migration-Stabilized-Execution-Post-DryRun-Review-v1-001"),
    ("MPT05", "Controlled Batch Execution Authorization", "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Execution-Authorization-v1-001"),
    ("MPT06", "Controlled Batch Execution", "Phase-Main-Project-Structure-Migration-Stabilized-Batch-Execution-v1-001"),
    ("MPT07", "Post-Migration Test + Verifier Closure", "Phase-Main-Project-Structure-Migration-Stabilized-Post-Migration-Closure-v1-001"),
)

STRUCTURE_RESUME_POINT = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-Planning-v1-001"


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _planning_meta() -> Dict[str, Any]:
    return {
        "stabilized_resume_planning_only": True,
        "registry_generation_authorization_planning_only": False,
        "registry_generation_authorization_branch_paused": True,
        "governance_constraint_module_branch_closed": True,
        "governance_constraint_module_as_deferred_capability": True,
        "legacy_extraction_as_source_pack": True,
        "artifact_generation_planning_continued_now": False,
        "governance_constraint_module_generated_now": False,
        "governance_constraint_module_enforced_now": False,
        "boundary_object_registry_generated_now": False,
        "boundary_object_registered_now": False,
        "registry_entry_generated_now": False,
        "registry_entry_committed_now": False,
        "registry_generation_authorization_request_sent_now": False,
        "registry_generation_authorized_now": False,
        "file_operation_executed_now": False,
        "file_move_executed_now": False,
        "file_delete_executed_now": False,
        "file_rename_executed_now": False,
        "file_merge_executed_now": False,
        "batch_arming_allowed": False,
        "batch_arming_executed_now": False,
        "real_migration_execution_allowed": False,
        "real_migration_executed_now": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_rehearsal_executed_now": False,
        "verifier_modified_now": False,
        "phase_template_modified_now": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "eval_out_modified_now": False,
        "legacy_eval_out_modified_now": False,
        "main_migration_chain_resumed_execution_now": False,
        "structure_migration_resume_point": STRUCTURE_RESUME_POINT,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "runtime_invoked": False,
        "execution_committed": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_planning_meta(), "planned_now": True, "executed_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _eval_out_root() -> Path:
    return Path(__file__).resolve().parents[2] / "_eval_out"


def _load_upstream_pack(
    path_str: Optional[str],
    artifacts: Tuple[str, ...],
) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary = _try_read_json(root / "summary.json") if root else None
    verifier = _try_read_json(root / "verifier_report.json") if root else None
    art: Dict[str, Any] = {}
    missing: List[str] = []
    if root:
        for name in artifacts:
            payload = _try_read_json(root / name)
            if payload is None:
                missing.append(name)
            else:
                art[name] = payload
    loaded = summary is not None and verifier is not None and not missing
    return {"root": root, "loaded": loaded, "summary": summary or {}, "verifier": verifier or {}, "artifacts": art, "missing": missing}


def _review_migration_chain() -> Tuple[List[Dict[str, Any]], bool, int]:
    rows: List[Dict[str, Any]] = []
    go_count = 0
    all_pass = True
    for subchain, phase_name, eval_out in MAIN_MIGRATION_CHAIN:
        root = _eval_out_root() / eval_out
        sm = _try_read_json(root / "summary.json") or {}
        vr = _try_read_json(root / "verifier_report.json") or {}
        verifier_label = vr.get("verifier")
        go = vr.get("passed") is True and verifier_label != "NO_GO" and (
            verifier_label == "GO" or verifier_label is None
        )
        boundary = sm.get("boundary_ok") is True
        ok_row = go and boundary
        if ok_row:
            go_count += 1
        else:
            all_pass = False
        rows.append(
            _row(
                subchain_id=subchain,
                phase_name=phase_name,
                eval_out_dir=eval_out,
                verifier_status=vr.get("verifier", "MISSING"),
                boundary_ok=boundary,
                real_migration_observed=sm.get("real_migration_executed_now") is True
                or sm.get("real_migration_execution_allowed") is True,
                file_operation_observed=sm.get("file_operation_executed_now") is True,
                review_pass=ok_row,
            )
        )
    return rows, all_pass, go_count


def run_main_project_structure_migration_stabilized_resume_planning_v1(
    *,
    return_to_registry_generation_authorization_planning_root: str,
    governance_constraint_module_branch_closure_root: str,
) -> Dict[str, Any]:
    ret = _load_upstream_pack(return_to_registry_generation_authorization_planning_root, RETURN_UPSTREAM_ARTIFACTS)
    closure = _load_upstream_pack(governance_constraint_module_branch_closure_root, CLOSURE_UPSTREAM_ARTIFACTS)
    ret_sm = ret["summary"]
    ret_vr = ret["verifier"]
    closure_sm = closure["summary"]
    closure_vr = closure["verifier"]
    closure_rd = closure["artifacts"].get("governance_constraint_module_branch_closure_readiness_decision_v1.json", {})
    reentry = ret["artifacts"].get("registry_generation_authorization_planning_reentry_scope_v1.json", {})
    stop_dec = closure["artifacts"].get("recursive_expansion_stop_decision_v1.json", {})

    blockers: List[str] = []
    if not ret["loaded"]:
        blockers.append(f"missing return upstream: {ret['missing']}")
    if not closure["loaded"]:
        blockers.append(f"missing closure upstream: {closure['missing']}")
    if ret_vr.get("verifier") != "GO":
        blockers.append("return wrapper verifier not GO")
    if ret_sm.get("final_decision") != RETURN_REQUIRED_FINAL:
        blockers.append("return final_decision mismatch")
    if ret_sm.get("governance_constraint_module_branch_closed") is not True:
        blockers.append("return must confirm GC branch closed")
    if closure_vr.get("verifier") != "GO":
        blockers.append("GC branch closure verifier not GO")
    if closure_sm.get("final_decision") != CLOSURE_REQUIRED_FINAL:
        blockers.append("closure final_decision mismatch")
    if closure_rd.get("branch_closed_for_current_mainline") is not True:
        blockers.append("closure branch not closed")
    if reentry.get("artifact_generation_planning_recursion_blocked") is not True:
        blockers.append("artifact generation recursion must stay blocked")
    if stop_dec.get("recursive_expansion_halted") is not True:
        blockers.append("recursive expansion must be halted")

    chain_rows, chain_all_pass, chain_go_count = _review_migration_chain()
    if chain_go_count < len(MAIN_MIGRATION_CHAIN):
        blockers.append(
            f"main migration chain GO count too low: {chain_go_count}/{len(MAIN_MIGRATION_CHAIN)}"
        )

    closure_review_rows = [
        _row(check_id=cid, check_name=n, expected=True, observed=observed, review_pass=observed is True)
        for cid, n, observed in (
            ("GC01", "closure_verifier_go", closure_vr.get("verifier") == "GO"),
            ("GC02", "branch_closed", closure_rd.get("branch_closed_for_current_mainline") is True),
            ("GC03", "deferred_capability", closure_rd.get("governance_constraint_module_as_deferred_capability") is True),
            ("GC04", "source_pack", closure_rd.get("legacy_extraction_as_source_pack") is True),
            ("GC05", "artifact_not_continued", closure_sm.get("artifact_generation_planning_continued_now") is False),
            ("GC06", "return_go", ret_vr.get("verifier") == "GO"),
            ("GC07", "registry_branch_paused", ret_sm.get("recommended_next_phase") == PAUSED_REGISTRY_RESUME_POINT),
        )
    ]
    closure_review_pass = all(r.get("review_pass") for r in closure_review_rows)

    batch_rows = [
        _row(
            batch_id=bid,
            batch_name=bname,
            scope_key=scope,
            resume_order_index=idx,
            requires_before_manifest=True,
            requires_after_manifest=True,
            requires_rollback_route=True,
            requires_verifier_rerun_list=True,
            single_domain_only=True,
            human_approval_required=has_candidates,
            armed_now=False,
            executed_now=False,
        )
        for idx, (bid, bname, scope, has_candidates) in enumerate(BATCH_DEFS)
    ]

    stability_rows = [_row(rule_id=rid, principle=p) for rid, p in STABILIZATION_PRINCIPLES]
    target_rows = [
        _row(path_or_domain=path, migration_allowed=allowed, rationale=rat)
        for path, allowed, rat in TARGET_STRUCTURE_RULES
    ]
    protected_rows = [
        _row(asset_or_operation=name, rule=rule, forbidden_now=forbidden)
        for name, rule, forbidden in PROTECTED_AND_FORBIDDEN
    ]
    test_rows = [_row(item_id=i, item_name=n, requirement=r) for i, n, r in TEST_VERIFIER_ITEMS]
    rollback_rows = [_row(requirement_id=i, requirement=r) for i, r in ROLLBACK_REHEARSAL_REQUIREMENTS]
    template_rows = [
        _row(template_step_id=i, step_name=n, phase_id=pid, large_governance_recursion=False)
        for i, n, pid in MINIMIZED_PHASE_TEMPLATE
    ]
    paused_rows = [
        _row(branch_id=bid, pause_reason=reason, deferred_next_phase=deferred, continued_now=False)
        for bid, reason, deferred in PAUSED_BRANCHES
    ]

    target_frozen = all(
        r.get("migration_allowed") is False
        for r in target_rows
        if r.get("path_or_domain") in ("_eval_out/", "protected assets", "human review queue", "DnAE permanent block")
    )
    registry_paused = all(r.get("continued_now") is False for r in paused_rows if r.get("branch_id") == "registry_authorization")

    planning_ready = (
        closure_review_pass
        and chain_go_count >= 30
        and target_frozen
        and registry_paused
        and not blockers
    )
    boundary_ok = planning_ready

    stabilized_resume_policy = _row(
        phase_name=PHASE_ID,
        structure_migration_resume_point=STRUCTURE_RESUME_POINT,
        paused_registry_resume_point=PAUSED_REGISTRY_RESUME_POINT,
        registry_authorization_branch_paused=True,
        governance_debt_canonicalization_paused=True,
        target_structure_change_policy="freeze_after_resume; small_patch_only",
    )

    governance_branch_closure_input_review = {
        "rows": closure_review_rows,
        "paused_branch_rows": paused_rows,
        "row_count": len(closure_review_rows),
        "all_pass": closure_review_pass,
        **_planning_meta(),
    }
    main_structure_migration_chain_status_review = {
        "rows": chain_rows,
        "row_count": len(chain_rows),
        "go_count": chain_go_count,
        "all_pass": chain_all_pass,
        "subchain_count": len({r[0] for r in MAIN_MIGRATION_CHAIN}),
        **_planning_meta(),
    }
    target_project_structure_stability_policy = {
        "rows": target_rows,
        "stabilization_principle_rows": stability_rows,
        "row_count": len(target_rows),
        "structure_frozen_after_resume": target_frozen,
        **_planning_meta(),
    }
    migration_batch_resume_matrix = {
        "rows": batch_rows,
        "gate_definitions": [{"gate_id": g[0], "gate_name": g[1], "scope": g[2]} for g in GATE_DEFS],
        "row_count": len(batch_rows),
        "batch_count": len(BATCH_DEFS),
        **_planning_meta(),
    }
    protected_asset_and_forbidden_operation_matrix = {
        "rows": protected_rows,
        "row_count": len(protected_rows),
        "all_forbidden_now": all(r.get("forbidden_now") for r in protected_rows),
        **_planning_meta(),
    }
    test_and_verifier_resume_plan = {
        "rows": test_rows,
        "row_count": len(test_rows),
        **_planning_meta(),
    }
    rollback_rehearsal_resume_requirement = {
        "rows": rollback_rows,
        "row_count": len(rollback_rows),
        "rehearsal_mandatory_before_controlled_execution": True,
        **_planning_meta(),
    }
    minimized_future_phase_template_policy = {
        "rows": template_rows,
        "row_count": len(template_rows),
        "no_large_governance_recursion": all(r.get("large_governance_recursion") is False for r in template_rows),
        "shortest_route_step_count": len(template_rows),
        **_planning_meta(),
    }
    stabilized_resume_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_RESUME_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "stabilized_resume_planning_completed": boundary_ok,
        "main_migration_chain_go_count": chain_go_count,
        "registry_authorization_branch_paused": registry_paused,
        "ready_for_stabilized_execution_planning": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "ready_for_rollback_rehearsal_execution": False,
        **_planning_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "return_to_registry_input_loaded": ret["loaded"],
        "governance_constraint_module_branch_closure_input_loaded": closure["loaded"],
        "main_migration_chain_go_count": chain_go_count,
        "main_migration_chain_phase_count": len(chain_rows),
        "migration_batch_count": len(batch_rows),
        "registry_authorization_branch_paused": True,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_RESUME_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_planning_meta(),
    }

    return {
        "summary": summary,
        "stabilized_resume_policy": stabilized_resume_policy,
        "governance_branch_closure_input_review": governance_branch_closure_input_review,
        "main_structure_migration_chain_status_review": main_structure_migration_chain_status_review,
        "target_project_structure_stability_policy": target_project_structure_stability_policy,
        "migration_batch_resume_matrix": migration_batch_resume_matrix,
        "protected_asset_and_forbidden_operation_matrix": protected_asset_and_forbidden_operation_matrix,
        "test_and_verifier_resume_plan": test_and_verifier_resume_plan,
        "rollback_rehearsal_resume_requirement": rollback_rehearsal_resume_requirement,
        "minimized_future_phase_template_policy": minimized_future_phase_template_policy,
        "stabilized_resume_readiness_decision": stabilized_resume_readiness_decision,
    }
