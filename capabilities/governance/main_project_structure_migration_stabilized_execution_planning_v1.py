# -*- coding: utf-8 -*-
"""Main Project Structure Migration Stabilized Execution Planning v1.

Execution planning only: freeze B0–B7 order, per-batch I/O, pre-gates, rollback, tests,
verifier rerun lists. No real file operations, batch arming, or migration execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from capabilities.governance.main_project_structure_migration_guarded_planning_v1 import GATE_DEFS
from capabilities.governance.migration_governance_development_constraints_v1 import (
    CONSTRAINT_DOC_ID,
)

PHASE_ID = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_stabilized_execution_planning_only"
SOURCE_CHAIN = "main_project_structure_migration_stabilized_execution_planning_v1"

RESUME_SOURCE_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Resume-Planning-v1-001"
RESUME_REQUIRED_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_RESUME_PLANNING_READY_FOR_EXECUTION_PLANNING"
)
RESUME_REQUIRED_NEXT = PHASE_ID

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Stabilized-Execution-DryRun-v1-001"

PAUSED_REGISTRY_NEXT = "Phase-Registry-Generation-Authorization-DryRun-v1-001"
PAUSED_GC_ARTIFACT = (
    "Phase-Governance-Constraint-Module-Generation-Authorization-Request-Artifact-Generation-Planning-v1-001"
)

RESUME_UPSTREAM_ARTIFACTS: Tuple[str, ...] = (
    "stabilized_resume_policy_v1.json",
    "migration_batch_resume_matrix_v1.json",
    "protected_asset_and_forbidden_operation_matrix_v1.json",
    "test_and_verifier_resume_plan_v1.json",
    "rollback_rehearsal_resume_requirement_v1.json",
    "minimized_future_phase_template_policy_v1.json",
    "stabilized_resume_readiness_decision_v1.json",
)

# B0–B7: single-domain stable placement planning (frozen for dry-run simulation)
STABILIZED_BATCH_DEFS: Tuple[Tuple[str, str, str, str, List[str], List[str]], ...] = (
    (
        "B0",
        "Documentation Index / README / phase table alignment planning",
        "docs_index_readme_phase_table",
        "docs_index_only",
        ["docs/architecture/README.md", "docs/architecture/evaluation/README.md"],
        ["docs_index_alignment_manifest_v1", "phase_table_crosslink_checklist_v1"],
    ),
    (
        "B1",
        "Governance docs stable placement planning",
        "governance_docs_placement",
        "governance_docs_only",
        ["docs/architecture/governance/"],
        ["governance_docs_placement_manifest_v1"],
    ),
    (
        "B2",
        "Architecture docs stable placement planning",
        "architecture_docs_placement",
        "architecture_docs_only",
        ["docs/architecture/evaluation/", "docs/architecture/governance/"],
        ["architecture_docs_placement_manifest_v1"],
    ),
    (
        "B3",
        "Capability modules stable placement planning",
        "capability_modules_placement",
        "capabilities_only",
        ["capabilities/"],
        ["capability_module_placement_manifest_v1"],
    ),
    (
        "B4",
        "Runner / verifier stable placement planning",
        "runner_verifier_placement",
        "runners_verifiers_only",
        ["tools/evaluation/"],
        ["runner_verifier_placement_manifest_v1"],
    ),
    (
        "B5",
        "Config / schema / examples stable placement planning",
        "config_schema_examples_placement",
        "config_schema_only",
        ["config/", "schemas/", "examples/"],
        ["config_schema_placement_manifest_v1"],
    ),
    (
        "B6",
        "Tools / scripts / tests stable placement planning",
        "tools_scripts_tests_placement",
        "tools_scripts_tests_only",
        ["tools/", "scripts/", "tests/"],
        ["tools_scripts_tests_placement_manifest_v1"],
    ),
    (
        "B7",
        "Final cross-reference / import / path consistency planning",
        "cross_reference_import_path_consistency",
        "verification_gate_only",
        ["docs/architecture/", "capabilities/", "tools/evaluation/"],
        ["import_path_consistency_report_v1", "cross_reference_integrity_report_v1"],
    ),
)

COMMON_ABORT_CONDITIONS: Tuple[str, ...] = (
    "protected_asset_intersection_detected",
    "eval_out_write_attempted",
    "cross_domain_batch_mix_detected",
    "before_manifest_missing",
    "rollback_route_missing",
    "verifier_rerun_list_missing",
    "runtime_behavior_change_detected",
    "model_ocr_voice_navigation_routing_change_detected",
    "gc_registry_recursion_attempted",
    "batch_arming_without_authorization",
)

GLOBAL_EXECUTION_RULES: Tuple[str, ...] = (
    "_eval_out read-only; no migrate merge delete",
    "protected assets / HR / DnAE permanently frozen",
    "verifier_report and summary are review inputs only, not migration targets",
    "no automatic cleanup of legacy phase docs",
    "no bulk delete",
    "no cross-domain merge in one batch",
    "no migrate-and-refactor logic in same batch",
    "no runtime behavior change via migration",
    "no model/OCR/voice/navigation routing change via migration",
    "no Governance Constraint Module or Registry Authorization recursion",
)

VERIFIER_RERUN_BY_BATCH: Dict[str, List[str]] = {
    "B0": ["verify_docs_link_integrity_v1", "verify_phase_table_alignment_v1"],
    "B1": ["verify_governance_docs_placement_v1"],
    "B2": ["verify_architecture_docs_placement_v1"],
    "B3": ["verify_capability_import_paths_v1", "verify_capability_module_inventory_v1"],
    "B4": ["verify_runner_verifier_colocation_v1", "verify_evaluation_governance_suite_v1"],
    "B5": ["verify_config_schema_examples_v1"],
    "B6": ["verify_tools_scripts_tests_placement_v1"],
    "B7": [
        "verify_cross_reference_integrity_v1",
        "verify_import_path_consistency_v1",
        "verify_stabilized_execution_planning_closure_v1",
    ],
}

TEST_CHECKLIST_BY_BATCH: Dict[str, List[str]] = {
    "B0": ["docs_readme_link_check", "phase_table_row_count_check"],
    "B1": ["governance_doc_path_check"],
    "B2": ["architecture_doc_path_check", "evaluation_readme_check"],
    "B3": ["capability_import_smoke", "protected_asset_unchanged_check"],
    "B4": ["runner_invocation_smoke", "verifier_min_checks_baseline"],
    "B5": ["config_schema_parse_check"],
    "B6": ["tools_script_syntax_check", "test_discovery_check"],
    "B7": ["full_import_graph_check", "eval_out_immutability_check", "protected_hr_dnae_integrity_check"],
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _boundary_meta() -> Dict[str, Any]:
    return {
        "execution_planning_only": True,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_file_merge_executed": False,
        "actual_file_copy_executed": False,
        "actual_archive_executed": False,
        "batch_arming_allowed": False,
        "batch_arming_executed_now": False,
        "real_migration_execution_allowed": False,
        "real_migration_executed_now": False,
        "real_rehearsal_execution_allowed": False,
        "rollback_rehearsal_execution_allowed": False,
        "rollback_rehearsal_executed_now": False,
        "verifier_rerun_executed_now": False,
        "eval_out_modified_now": False,
        "protected_asset_modified_now": False,
        "hr_modified_now": False,
        "dnae_modified_now": False,
        "file_operation_executed_now": False,
        "registry_generation_authorization_branch_paused": True,
        "registry_generation_authorization_continued_now": False,
        "governance_constraint_module_branch_closed": True,
        "governance_constraint_module_as_deferred_capability": True,
        "governance_constraint_module_enforced_now": False,
        "artifact_generation_planning_continued_now": False,
        "boundary_object_registry_generated_now": False,
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "runtime_invoked": False,
        "execution_committed": False,
        "authorization_granted_now": False,
        "owner_approval_granted_now": False,
        "operator_acknowledgement_granted_now": False,
        "execution_window_opened_now": False,
        "success_claim_allowed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _row(**kwargs: Any) -> Dict[str, Any]:
    return {**kwargs, **_boundary_meta(), "planned_now": True, "executed_now": False, "touched_now": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_resume_upstream(path_str: str) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve()
    summary = _try_read_json(root / "summary.json")
    verifier = _try_read_json(root / "verifier_report.json")
    artifacts: Dict[str, Any] = {}
    missing: List[str] = []
    for name in RESUME_UPSTREAM_ARTIFACTS:
        payload = _try_read_json(root / name)
        if payload is None:
            missing.append(name)
        else:
            artifacts[name] = payload
    loaded = summary is not None and verifier is not None and not missing
    return {
        "root": root,
        "loaded": loaded,
        "summary": summary or {},
        "verifier": verifier or {},
        "artifacts": artifacts,
        "missing": missing,
    }


def run_main_project_structure_migration_stabilized_execution_planning_v1(
    *,
    stabilized_resume_planning_root: str,
) -> Dict[str, Any]:
    resume = _load_resume_upstream(stabilized_resume_planning_root)
    sm = resume["summary"]
    vr = resume["verifier"]
    readiness = resume["artifacts"].get("stabilized_resume_readiness_decision_v1.json", {})

    blockers: List[str] = []
    if not resume["loaded"]:
        blockers.append(f"resume upstream incomplete: {resume['missing']}")
    if vr.get("verifier") != "GO" or vr.get("passed") is not True:
        blockers.append("resume verifier must be GO")
    if sm.get("boundary_ok") is not True:
        blockers.append("resume boundary_ok must be true")
    if sm.get("final_decision") != RESUME_REQUIRED_FINAL:
        blockers.append("resume final_decision mismatch")
    if sm.get("recommended_next_phase") != RESUME_REQUIRED_NEXT:
        blockers.append("resume recommended_next_phase must point to this phase")
    if sm.get("governance_constraint_module_branch_closed") is not True:
        blockers.append("GC branch must be closed")
    if sm.get("governance_constraint_module_enforced_now") is True:
        blockers.append("GC must be reference/deferred only, not enforced")
    if sm.get("registry_generation_authorization_branch_paused") is not True:
        blockers.append("Registry Authorization must stay paused")
    if sm.get("file_operation_executed_now") is True:
        blockers.append("resume must have no file operations")
    if readiness.get("ready_for_stabilized_execution_planning") is not True:
        blockers.append("resume not ready for execution planning")

    review_rows = [
        _row(check_id=cid, check_name=n, expected=exp, observed=obs, review_pass=obs == exp)
        for cid, n, exp, obs in (
            ("R01", "verifier_go", "GO", vr.get("verifier")),
            ("R02", "boundary_ok", True, sm.get("boundary_ok")),
            ("R03", "final_decision", RESUME_REQUIRED_FINAL, sm.get("final_decision")),
            ("R04", "next_phase", RESUME_REQUIRED_NEXT, sm.get("recommended_next_phase")),
            ("R05", "gc_closed", True, sm.get("governance_constraint_module_branch_closed")),
            ("R06", "gc_deferred_not_enforced", True, sm.get("governance_constraint_module_enforced_now") is False),
            ("R07", "registry_paused", True, sm.get("registry_generation_authorization_branch_paused")),
            ("R08", "eval_out_not_modified", False, sm.get("eval_out_modified_now")),
            ("R09", "no_file_operation", False, sm.get("file_operation_executed_now")),
            ("R10", "readiness_exec_planning", True, readiness.get("ready_for_stabilized_execution_planning")),
        )
    ]
    review_pass = all(r["review_pass"] for r in review_rows) and not blockers

    batch_plan_rows: List[Dict[str, Any]] = []
    pre_gate_rows: List[Dict[str, Any]] = []
    manifest_rows: List[Dict[str, Any]] = []
    rollback_rows: List[Dict[str, Any]] = []
    verifier_rows: List[Dict[str, Any]] = []
    protected_rows: List[Dict[str, Any]] = []
    eval_out_rows: List[Dict[str, Any]] = []
    domain_rows: List[Dict[str, Any]] = []
    abort_rows: List[Dict[str, Any]] = []

    for idx, (bid, bname, scope_key, domain, touched_candidates, planned_outputs) in enumerate(
        STABILIZED_BATCH_DEFS
    ):
        batch_plan_rows.append(
            _row(
                batch_id=bid,
                batch_name=bname,
                execution_order_index=idx,
                scope_key=scope_key,
                single_domain=domain,
                batch_inputs={
                    "upstream_resume_artifacts": list(RESUME_UPSTREAM_ARTIFACTS),
                    "prior_batch_outputs": [f"{STABILIZED_BATCH_DEFS[i][0]}_output" for i in range(idx)],
                },
                batch_outputs=planned_outputs,
                touched_paths_candidate=touched_candidates,
                path_actually_touched_now=False,
                protected_path_intersection=False,
                eval_out_write_allowed=False,
                cross_domain_mix_forbidden=True,
            )
        )

        for gid, gname, gscope in GATE_DEFS:
            pre_gate_rows.append(
                _row(
                    batch_id=bid,
                    gate_id=gid,
                    gate_name=gname,
                    gate_scope=gscope,
                    must_pass_before_batch_execution=True,
                    satisfied_in_planning=False,
                )
            )

        manifest_rows.append(
            _row(
                batch_id=bid,
                before_manifest_plan_id=f"before_manifest_{bid.lower()}_v1",
                after_manifest_plan_id=f"after_manifest_{bid.lower()}_v1",
                before_manifest_fields=["path", "sha256_placeholder", "size_bytes_placeholder"],
                after_manifest_fields=["path", "sha256_placeholder", "size_bytes_placeholder"],
                manifest_generated_now=False,
            )
        )

        rollback_rows.append(
            _row(
                batch_id=bid,
                rollback_route_id=f"rollback_route_{bid.lower()}_v1",
                rollback_steps=[
                    "restore_from_before_manifest",
                    "rerun_batch_verifiers",
                    "confirm_protected_assets_unchanged",
                ],
                rollback_executed_now=False,
            )
        )

        verifier_rows.append(
            _row(
                batch_id=bid,
                verifier_rerun_list=VERIFIER_RERUN_BY_BATCH[bid],
                test_checklist=TEST_CHECKLIST_BY_BATCH[bid],
                verifier_rerun_executed_now=False,
            )
        )

        protected_rows.append(
            _row(
                batch_id=bid,
                protected_assets_frozen=True,
                human_review_queue_frozen=True,
                dnae_permanent_block_frozen=True,
                protected_path_intersection=False,
                guard_pass=True,
            )
        )

        eval_out_rows.append(
            _row(
                batch_id=bid,
                eval_out_paths=["_eval_out/"],
                eval_out_readonly=True,
                eval_out_migrate_allowed=False,
                eval_out_merge_allowed=False,
                eval_out_delete_allowed=False,
                eval_out_write_allowed=False,
                guard_pass=True,
            )
        )

        domain_rows.append(
            _row(
                batch_id=bid,
                allowed_domain=domain,
                forbidden_domains=[
                    d
                    for _, _, _, d, _, _ in STABILIZED_BATCH_DEFS
                    if d != domain
                ],
                single_domain_only=True,
                cross_domain_merge_forbidden=True,
                isolation_pass=True,
            )
        )

        for ac in COMMON_ABORT_CONDITIONS:
            abort_rows.append(
                _row(
                    batch_id=bid,
                    abort_condition_id=ac,
                    abort_on_trigger=True,
                    triggered_now=False,
                )
            )

    boundary_ok = review_pass and len(batch_plan_rows) == 8

    stabilized_execution_planning_policy = _row(
        phase_id=PHASE_ID,
        planning_scope=PLANNING_SCOPE,
        batch_count=len(STABILIZED_BATCH_DEFS),
        gate_count_per_batch=len(GATE_DEFS),
        global_execution_rules=list(GLOBAL_EXECUTION_RULES),
        registry_authorization_paused=True,
        gc_branch_reference_only=True,
    )

    resume_planning_input_review = {
        "upstream_root": str(resume["root"]),
        "rows": review_rows,
        "row_count": len(review_rows),
        "all_pass": review_pass,
        **_boundary_meta(),
    }

    b0_b7_execution_batch_plan = {
        "rows": batch_plan_rows,
        "batch_count": len(batch_plan_rows),
        "sequential_execution_required": True,
        "all_batches_untouched": all(not r.get("touched_now") for r in batch_plan_rows),
        **_boundary_meta(),
    }

    batch_pre_gate_matrix = {
        "rows": pre_gate_rows,
        "row_count": len(pre_gate_rows),
        "gate_definitions": [{"gate_id": g[0], "gate_name": g[1], "scope": g[2]} for g in GATE_DEFS],
        **_boundary_meta(),
    }

    batch_before_after_manifest_plan = {
        "rows": manifest_rows,
        "row_count": len(manifest_rows),
        "all_have_before_and_after": all(
            r.get("before_manifest_plan_id") and r.get("after_manifest_plan_id") for r in manifest_rows
        ),
        **_boundary_meta(),
    }

    batch_rollback_route_plan = {
        "rows": rollback_rows,
        "row_count": len(rollback_rows),
        "all_have_rollback_route": len(rollback_rows) == len(STABILIZED_BATCH_DEFS),
        **_boundary_meta(),
    }

    batch_verifier_rerun_plan = {
        "rows": verifier_rows,
        "row_count": len(verifier_rows),
        "all_have_verifier_list": all(r.get("verifier_rerun_list") for r in verifier_rows),
        **_boundary_meta(),
    }

    batch_protected_asset_guard_matrix = {
        "rows": protected_rows,
        "row_count": len(protected_rows),
        "all_guard_pass": all(r.get("guard_pass") for r in protected_rows),
        **_boundary_meta(),
    }

    batch_eval_out_readonly_guard = {
        "rows": eval_out_rows,
        "row_count": len(eval_out_rows),
        "all_readonly_guard_pass": all(r.get("guard_pass") for r in eval_out_rows),
        **_boundary_meta(),
    }

    batch_domain_isolation_matrix = {
        "rows": domain_rows,
        "row_count": len(domain_rows),
        "all_isolation_pass": all(r.get("isolation_pass") for r in domain_rows),
        **_boundary_meta(),
    }

    batch_abort_condition_matrix = {
        "rows": abort_rows,
        "row_count": len(abort_rows),
        "common_abort_condition_count": len(COMMON_ABORT_CONDITIONS),
        **_boundary_meta(),
    }

    stabilized_execution_planning_readiness_decision = {
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "ready_for_stabilized_execution_dryrun": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_batch_arming": False,
        "execution_planning_completed": boundary_ok,
        **_boundary_meta(),
    }

    summary = {
        "phase": PHASE_ID,
        "planning_scope": PLANNING_SCOPE,
        "resume_input_loaded": resume["loaded"],
        "batch_count": len(STABILIZED_BATCH_DEFS),
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_STABILIZED_EXECUTION_PLANNING_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        **_boundary_meta(),
    }

    return {
        "summary": summary,
        "stabilized_execution_planning_policy": stabilized_execution_planning_policy,
        "resume_planning_input_review": resume_planning_input_review,
        "b0_b7_execution_batch_plan": b0_b7_execution_batch_plan,
        "batch_pre_gate_matrix": batch_pre_gate_matrix,
        "batch_before_after_manifest_plan": batch_before_after_manifest_plan,
        "batch_rollback_route_plan": batch_rollback_route_plan,
        "batch_verifier_rerun_plan": batch_verifier_rerun_plan,
        "batch_protected_asset_guard_matrix": batch_protected_asset_guard_matrix,
        "batch_eval_out_readonly_guard": batch_eval_out_readonly_guard,
        "batch_domain_isolation_matrix": batch_domain_isolation_matrix,
        "batch_abort_condition_matrix": batch_abort_condition_matrix,
        "stabilized_execution_planning_readiness_decision": stabilized_execution_planning_readiness_decision,
    }
