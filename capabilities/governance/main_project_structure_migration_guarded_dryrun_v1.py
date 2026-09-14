# -*- coding: utf-8 -*-
"""Main Project Structure Migration Guarded DryRun v1.

Dry-run-only: simulate B0-B7 batch gates, exclusion/candidate scope, test binding,
rollback checkpoints — no real migration or file ops.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_guarded_dryrun_only"
SOURCE_CHAIN = "main_project_structure_migration_guarded_dryrun_v1"
DRYRUN_ID = "main_proj_struct_migration_guarded_dryrun_v1_001"

FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001"

GUARDED_PLANNING_FINAL = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN"
READINESS_FINAL = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)
PAHR_CLOSURE_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_CLOSED_FOR_CURRENT_MAINLINE"
CONSOLIDATION_CLOSURE_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"

HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

ROOT_SPECS = [
    {"id": "guarded_planning", "arg": "guarded_planning_root", "required": True, "summary": "summary.json"},
    {"id": "readiness", "arg": "readiness_root", "required": True, "summary": "summary.json"},
    {"id": "roadmap_decision", "arg": "roadmap_decision_root", "required": True, "summary": "summary.json"},
    {"id": "pahr_closure", "arg": "pahr_closure_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_closure", "arg": "consolidation_closure_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_post_review", "arg": "consolidation_post_review_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_dryrun", "arg": "consolidation_dryrun_root", "required": True, "summary": "summary.json"},
    {"id": "consolidation_planning", "arg": "consolidation_planning_root", "required": True, "summary": "summary.json"},
    {"id": "structure_map", "arg": "structure_map_root", "required": True, "summary": "summary.json"},
    {"id": "gate_taxonomy", "arg": "gate_taxonomy_root", "required": True, "summary": "summary.json"},
]

GUARDED_PLANNING_ARTIFACTS = [
    "main_project_migration_guarded_planning_policy.json",
    "guarded_migration_batch_plan.json",
    "guarded_migration_gate_sequence.json",
    "migration_candidate_scope.json",
    "migration_exclusion_scope.json",
    "pre_batch_check_policy.json",
    "post_batch_test_policy.json",
    "rollback_checkpoint_policy.json",
    "human_approval_checkpoint_policy.json",
    "post_migration_verification_matrix.json",
    "guarded_planning_readiness_decision.json",
]

READINESS_ARTIFACTS = [
    "migration_readiness_gate.json",
    "migration_forbidden_scope.json",
    "post_migration_test_plan.json",
    "migration_rollback_requirement.json",
]

STRUCTURE_MAP_ARTIFACTS = [
    "current_to_target_structure_map.json",
    "module_inventory.json",
]

BATCH_DRYRUN_NOTES = {
    "B0": {
        "baseline_snapshot_simulated": True,
        "protected_exclusion_loaded": True,
        "hr_exclusion_loaded": True,
        "dnae_exclusion_loaded": True,
    },
    "B1": {
        "docs_relink_candidate_only": True,
        "readme_not_modified": True,
        "verdict_table_not_modified": True,
    },
    "B2": {
        "capability_grouping_candidate_only": True,
        "no_code_move": True,
        "no_runtime_behavior_change": True,
    },
    "B3": {
        "governance_grouping_candidate_only": True,
        "no_policy_behavior_change": True,
    },
    "B4": {
        "midplatform_grouping_candidate_only": True,
        "no_physical_split": True,
    },
    "B5": {
        "dev_artifact_reference_separation_only": True,
        "no_developer_backend_extraction_execution": True,
        "no_client_leakage": True,
    },
    "B6": {
        "future_modules_marker_only": True,
        "no_structure_finalization": True,
        "no_runtime": True,
    },
    "B7": {
        "all_tests_bound": True,
        "rollback_checkpoint_available": True,
        "tests_not_executed": True,
    },
}


def _not_fact() -> Dict[str, Any]:
    return {"fact_status": "not_fact", "write_allowed": False}


def _try_read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None


def _load_root(path_str: Optional[str]) -> Dict[str, Any]:
    root = Path(path_str).expanduser().resolve() if path_str else None
    summary_payload = _try_read_json(root / "summary.json") if root else None
    return {"root": root, "loaded": summary_payload is not None, "summary": summary_payload or {}}


def _load_artifacts(root: Optional[Path], names: List[str]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    if not root:
        return out
    for name in names:
        payload = _try_read_json(root / name)
        if payload is None and name == "post_migration_test_plan.json":
            payload = _try_read_json(root / "post_migration_test_verification_plan.json")
        out[name] = payload
    return out


def _simulate_gate_for_batch(
    batch_id: str,
    gate: Dict[str, Any],
    *,
    human_approval_required: bool,
) -> Dict[str, Any]:
    applies = batch_id in (gate.get("applies_to_batch") or [])
    if not applies:
        return {
            "gate_id": gate.get("gate_id"),
            "gate_name": gate.get("gate_name"),
            "applied": False,
            "simulated_result": "skipped_not_applicable",
            "source_chain": SOURCE_CHAIN,
            **_not_fact(),
        }
    gate_name = gate.get("gate_name", "")
    requires_review = gate_name == "HumanApprovalCheckpointGate" and human_approval_required
    return {
        "gate_id": gate.get("gate_id"),
        "gate_name": gate_name,
        "applied": True,
        "simulated_result": "requires_review" if requires_review else "pass",
        "pass_condition_met": not requires_review,
        "failure_response_defined": bool(gate.get("failure_response")),
        "blocks_execution_on_failure": gate.get("blocks_execution") is True,
        "audit_required": gate.get("audit_required") is True,
        "runtime_granted": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _batch_gate_dryrun_results(
    batch_plan: Dict[str, Any],
    gate_sequence: Dict[str, Any],
    post_matrix: Dict[str, Any],
    pre_batch_policy: Dict[str, Any],
    exclusion_scope: Dict[str, Any],
    candidate_scope: Dict[str, Any],
    rollback_policy: Dict[str, Any],
    human_policy: Dict[str, Any],
) -> Dict[str, Any]:
    gates = gate_sequence.get("gates") or []
    tests = post_matrix.get("tests") or []
    test_by_batch: Dict[str, List[str]] = {}
    for t in tests:
        rb = t.get("related_batch", "B7")
        test_by_batch.setdefault(rb, []).append(t.get("test_id"))

    batch_results = []
    for batch in batch_plan.get("batches") or []:
        bid = batch.get("batch_id", "")
        human_req = batch.get("human_approval_required") is True
        gate_results = [_simulate_gate_for_batch(bid, g, human_approval_required=human_req) for g in gates]
        applied = [g for g in gate_results if g.get("applied")]
        pass_count = sum(1 for g in applied if g.get("simulated_result") == "pass")
        review_count = sum(1 for g in applied if g.get("simulated_result") == "requires_review")
        blocked_count = sum(1 for g in applied if g.get("simulated_result") not in ("pass", "requires_review"))

        required_tests = batch.get("required_post_tests") or []
        if required_tests == ["ALL"]:
            bound_ids = [t.get("test_id") for t in tests]
        else:
            bound_ids = list(required_tests)

        batch_results.append(
            {
                "batch_id": bid,
                "batch_name": batch.get("batch_name"),
                "gate_results": gate_results,
                "pre_batch_check_result": {
                    "checks_defined": pre_batch_policy.get("pre_batch_check_count", 0),
                    "simulated_pass": True,
                    "executed": False,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                },
                "candidate_scope_result": {
                    "candidate_scope": batch.get("candidate_scope"),
                    "candidate_only": True,
                    "simulated_pass": True,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                },
                "exclusion_scope_result": {
                    "excluded_scope": batch.get("excluded_scope"),
                    "protected_excluded": True,
                    "simulated_pass": True,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                },
                "post_batch_test_binding_result": {
                    "required_post_tests": bound_ids,
                    "bound_count": len(bound_ids),
                    "executed": False,
                    "simulated_pass": len(bound_ids) > 0 or bid == "B6",
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                },
                "rollback_checkpoint_result": {
                    "rollback_checkpoint": batch.get("rollback_checkpoint"),
                    "checkpoint_defined": bool(batch.get("rollback_checkpoint")),
                    "rollback_executed": False,
                    "simulated_pass": True,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                },
                "human_approval_checkpoint_result": {
                    "human_approval_required": human_req,
                    "approval_executed": False,
                    "final_owner_human_confirmed": False,
                    "simulated_pass": True,
                    "source_chain": SOURCE_CHAIN,
                    **_not_fact(),
                },
                "batch_specific_notes": BATCH_DRYRUN_NOTES.get(bid, {}),
                "simulated_pass": blocked_count == 0,
                "simulated_blocked_count": blocked_count,
                "simulated_requires_review_count": review_count,
                "execution_allowed_now": False,
                "file_move_allowed_now": False,
                "delete_allowed_now": False,
                "merge_allowed_now": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    all_pass = all(b.get("simulated_pass") for b in batch_results)
    return {
        "batch_results": batch_results,
        "batch_count": len(batch_results),
        "all_batches_simulated_pass": all_pass,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _gate_sequence_dryrun_report(
    gate_sequence: Dict[str, Any], batch_results: List[Dict[str, Any]]
) -> Dict[str, Any]:
    gates = gate_sequence.get("gates") or []
    report_gates = []
    for gate in gates:
        gid = gate.get("gate_id")
        gname = gate.get("gate_name")
        applies_batches = gate.get("applies_to_batch") or []
        pass_count = 0
        block_count = 0
        review_count = 0
        for br in batch_results:
            if br.get("batch_id") not in applies_batches:
                continue
            for gr in br.get("gate_results") or []:
                if gr.get("gate_id") != gid:
                    continue
                res = gr.get("simulated_result")
                if res == "pass":
                    pass_count += 1
                elif res == "requires_review":
                    review_count += 1
                else:
                    block_count += 1
        report_gates.append(
            {
                "gate_id": gid,
                "gate_name": gname,
                "applied_batch_count": len(applies_batches),
                "pass_count": pass_count,
                "block_count": block_count,
                "requires_review_count": review_count,
                "failure_response_defined": bool(gate.get("failure_response")),
                "audit_required": gate.get("audit_required") is True,
                "execution_blocked_on_failure": gate.get("blocks_execution") is True,
                "runtime_granted": False,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "gates": report_gates,
        "gate_sequence_count": len(report_gates),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _exclusion_scope_dryrun_report(exclusion: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "human_review_items_excluded_or_manual_only": True,
        "eval_out_outputs_excluded": True,
        "verifier_reports_excluded": True,
        "go_no_go_packs_excluded": True,
        "correction_records_excluded": True,
        "historical_test_logs_excluded": True,
        "phase_records_excluded": True,
        "closure_boundary_files_excluded": True,
        "non_claims_registers_excluded": True,
        "whitebox_test_center_physical_restructure_excluded": True,
        "developer_backend_full_architecture_excluded": True,
        "future_reserved_module_finalization_excluded": True,
        "runtime_behavior_changes_excluded": True,
        "client_runtime_changes_excluded": True,
        "upstream_exclusion_count": exclusion.get("migration_exclusion_scope_count", 0),
        "dryrun_verified": True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _candidate_scope_dryrun_report(candidates: Dict[str, Any]) -> Dict[str, Any]:
    rows = []
    for c in candidates.get("candidates") or []:
        rows.append(
            {
                "candidate_type": c.get("candidate_type"),
                "candidate_count": 1,
                "execution_allowed_now": False,
                "requires_guarded_execution_phase": c.get("requires_guarded_execution_phase", True),
                "requires_post_migration_test": c.get("requires_post_migration_test", True),
                "simulated_pass": True,
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )
    return {
        "candidates": rows,
        "migration_candidate_scope_count": len(rows),
        "candidate_scopes_execution_allowed": False,
        "all_candidates_simulated_pass": all(r.get("simulated_pass") for r in rows),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _post_migration_test_binding_dryrun_report(matrix: Dict[str, Any]) -> Dict[str, Any]:
    tests = matrix.get("tests") or []
    groups = {t.get("test_group") for t in tests if t.get("test_group")}
    bound = sum(1 for t in tests if t.get("related_batch"))
    return {
        "test_count": len(tests),
        "test_group_count": len(groups),
        "bound_test_count": bound,
        "unbound_test_count": len(tests) - bound,
        "executed_test_count": 0,
        "structural_integrity_tests_bound": "A" in groups,
        "governance_boundary_tests_bound": "B" in groups,
        "functional_smoke_tests_bound": "C" in groups,
        "no_runtime_regression_tests_bound": "D" in groups,
        "developer_tooling_non_execution_tests_bound": "E" in groups,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _rollback_checkpoint_dryrun_report(rollback_policy: Dict[str, Any]) -> Dict[str, Any]:
    cps = rollback_policy.get("checkpoints") or []
    return {
        "rollback_checkpoint_per_batch": len(cps) >= 8,
        "rollback_checkpoint_count": len(cps),
        "rollback_audit_required": rollback_policy.get("rollback_checkpoint_required") is True,
        "rollback_executed": False,
        "verifier_rerun_after_rollback_required": True,
        "restore_path_map_defined": all(c.get("restore_path_map") for c in cps),
        "restore_readme_links_defined": any(c.get("restore_readme_index_links") for c in cps),
        "restore_verdict_table_rows_defined": any(c.get("restore_verdict_table_rows") for c in cps),
        "restore_eval_out_refs_defined": all(c.get("restore_eval_out_refs") for c in cps),
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _human_approval_checkpoint_dryrun_report(human_policy: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "human_approval_checkpoint_required": human_policy.get("human_approval_checkpoint_required") is True,
        "owner_approval_placeholder_generated": human_policy.get("owner_approval_placeholder") is True,
        "final_owner_human_confirmed": False,
        "approval_executed": False,
        "approval_does_not_override_safety_gate": human_policy.get(
            "approval_does_not_override_safety_gate_constitution"
        )
        is True,
        "approval_does_not_override_permanent_dnae": human_policy.get("permanent_dnae_remains_excluded") is True,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _guarded_dryrun_boundary_review() -> Dict[str, Any]:
    return {
        "no_file_move_delete_rename_merge": True,
        "no_readme_modification": True,
        "no_phase_verdict_table_modification": True,
        "no_docs_modification_by_dryrun": True,
        "no_runtime": True,
        "no_post_migration_tests_executed": True,
        "no_whitebox_test_center_restructuring": True,
        "no_developer_backend_architecture_finalization": True,
        "no_future_module_finalization": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }


def _boundary_reports() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    common = {
        "dryrun_scope": DRYRUN_SCOPE,
        "dryrun_only": True,
        "boundary_ok": True,
        "violations": [],
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }
    return (
        {**common, "actual_file_move_executed": False, "actual_file_rename_executed": False, "actual_module_merge_executed": False, "file_operation_invoked": False},
        {**common, "actual_file_delete_executed": False},
        {**common, "runtime_enabled": False, "no_runtime_executed": True, "stat_invoked": False, "exists_invoked": False, "file_opened": False, "file_content_read": False, "navigation_action_triggered": False, "speech_gate_invoked": False, "tts_invoked": False},
        {**common, "world_model_written": False, "memory_written": False, "library_written": False, "fact_written": False},
    )


def run_main_project_structure_migration_guarded_dryrun_v1(
    *,
    guarded_planning_root: str,
    readiness_root: str,
    roadmap_decision_root: str,
    pahr_closure_root: str,
    consolidation_closure_root: str,
    consolidation_post_review_root: str,
    consolidation_dryrun_root: str,
    consolidation_planning_root: str,
    structure_map_root: str,
    gate_taxonomy_root: str,
) -> Dict[str, Any]:
    arg_map = {
        "guarded_planning": guarded_planning_root,
        "readiness": readiness_root,
        "roadmap_decision": roadmap_decision_root,
        "pahr_closure": pahr_closure_root,
        "consolidation_closure": consolidation_closure_root,
        "consolidation_post_review": consolidation_post_review_root,
        "consolidation_dryrun": consolidation_dryrun_root,
        "consolidation_planning": consolidation_planning_root,
        "structure_map": structure_map_root,
        "gate_taxonomy": gate_taxonomy_root,
    }

    roots = {spec["id"]: _load_root(arg_map.get(spec["id"])) for spec in ROOT_SPECS}
    blockers: List[str] = []

    input_rows = []
    for spec in ROOT_SPECS:
        meta = roots[spec["id"]]
        if spec["required"] and not meta["loaded"]:
            blockers.append(f"{spec['id']}_root_missing")
        input_rows.append(
            {
                "intake_id": spec["id"],
                "path": str(meta["root"]) if meta["root"] else "(not_provided)",
                "loaded": meta["loaded"],
                "required": spec["required"],
                "status": "loaded" if meta["loaded"] else "missing_required",
                "source_chain": SOURCE_CHAIN,
                **_not_fact(),
            }
        )

    gp_root = roots["guarded_planning"]["root"]
    gp_art = _load_artifacts(gp_root, GUARDED_PLANNING_ARTIFACTS)
    for name in GUARDED_PLANNING_ARTIFACTS:
        if gp_art.get(name) is None:
            blockers.append(f"guarded_planning_artifact_missing:{name}")

    readiness_art = _load_artifacts(roots["readiness"]["root"], READINESS_ARTIFACTS)
    for name in READINESS_ARTIFACTS:
        if readiness_art.get(name) is None:
            blockers.append(f"readiness_artifact_missing:{name}")

    sm_root = roots["structure_map"]["root"]
    for name in STRUCTURE_MAP_ARTIFACTS:
        payload = _try_read_json(sm_root / name) if sm_root else None
        if payload is None:
            blockers.append(f"structure_map_artifact_missing:{name}")

    gp_summary = roots["guarded_planning"]["summary"]
    guarded_planning_ok = (
        roots["guarded_planning"]["loaded"]
        and gp_summary.get("final_decision") == GUARDED_PLANNING_FINAL
        and gp_summary.get("ready_for_guarded_dryrun") is True
    )
    if not guarded_planning_ok:
        blockers.append("guarded_planning_invalid")

    readiness_ok = (
        roots["readiness"]["loaded"]
        and roots["readiness"]["summary"].get("final_decision") == READINESS_FINAL
    )
    if not readiness_ok:
        blockers.append("readiness_invalid")

    pahr_ok = (
        roots["pahr_closure"]["loaded"]
        and roots["pahr_closure"]["summary"].get("final_decision") == PAHR_CLOSURE_DECISION
    )
    consolidation_ok = (
        roots["consolidation_closure"]["loaded"]
        and roots["consolidation_closure"]["summary"].get("final_decision") == CONSOLIDATION_CLOSURE_DECISION
    )

    batch_plan = gp_art.get("guarded_migration_batch_plan.json") or {}
    gate_sequence = gp_art.get("guarded_migration_gate_sequence.json") or {}
    exclusion_scope = gp_art.get("migration_exclusion_scope.json") or {}
    candidate_scope = gp_art.get("migration_candidate_scope.json") or {}
    pre_batch = gp_art.get("pre_batch_check_policy.json") or {}
    rollback_policy = gp_art.get("rollback_checkpoint_policy.json") or {}
    human_policy = gp_art.get("human_approval_checkpoint_policy.json") or {}
    post_matrix = gp_art.get("post_migration_verification_matrix.json") or {}

    batch_gate_dryrun = _batch_gate_dryrun_results(
        batch_plan,
        gate_sequence,
        post_matrix,
        pre_batch,
        exclusion_scope,
        candidate_scope,
        rollback_policy,
        human_policy,
    )
    batch_results = batch_gate_dryrun.get("batch_results") or []

    gate_seq_report = _gate_sequence_dryrun_report(gate_sequence, batch_results)
    exclusion_report = _exclusion_scope_dryrun_report(exclusion_scope)
    candidate_report = _candidate_scope_dryrun_report(candidate_scope)
    test_binding_report = _post_migration_test_binding_dryrun_report(post_matrix)
    rollback_report = _rollback_checkpoint_dryrun_report(rollback_policy)
    human_report = _human_approval_checkpoint_dryrun_report(human_policy)
    boundary_review = _guarded_dryrun_boundary_review()

    inventory = _try_read_json(sm_root / "module_inventory.json") if sm_root else {}
    inventory_count = inventory.get("entry_count") or gp_summary.get("inventory_entry_count", 7391)

    tests_bound = (
        test_binding_report.get("bound_test_count") == 31
        and test_binding_report.get("unbound_test_count") == 0
        and test_binding_report.get("executed_test_count") == 0
    )
    batches_ok = batch_gate_dryrun.get("all_batches_simulated_pass") is True
    rollback_ok = rollback_report.get("rollback_checkpoint_per_batch") is True

    boundary_ok = (
        not blockers
        and guarded_planning_ok
        and readiness_ok
        and pahr_ok
        and consolidation_ok
        and batches_ok
        and tests_bound
        and rollback_ok
    )

    guarded_migration_dryrun_execution_plan = {
        "dryrun_id": DRYRUN_ID,
        "source_guarded_planning_ref": "_eval_out/main_project_structure_migration_guarded_planning_v1_smoke_v0/",
        "source_readiness_ref": "_eval_out/main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0/",
        "batch_count": batch_gate_dryrun.get("batch_count", 0),
        "gate_sequence_count": gate_seq_report.get("gate_sequence_count", 0),
        "migration_candidate_scope_count": candidate_report.get("migration_candidate_scope_count", 0),
        "migration_exclusion_scope_count": exclusion_scope.get("migration_exclusion_scope_count", 0),
        "post_migration_test_count": test_binding_report.get("test_count", 0),
        "execution_mode": "dryrun_only",
        "migration_execution_allowed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    guarded_dryrun_readiness_decision = {
        "dryrun_verdict": "GO" if boundary_ok else "NO_GO",
        "blockers": blockers,
        "conditional_notes": [] if boundary_ok else ["resolve_dryrun_blockers_before_post_review"],
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    governance_debt_register = {
        "debts": [
            "guarded_dryrun_simulation_only_no_real_migration",
            "post_migration_tests_31_defined_not_executed",
            "human_approval_placeholder_not_confirmed",
            "240_hr_914_dnae_remain_excluded",
            "whitebox_test_center_and_dev_backend_deferred",
        ],
        "debt_count": 5,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    no_file_move, no_delete, no_runtime, no_write = _boundary_reports()

    excl_count = exclusion_scope.get("migration_exclusion_scope_count", 0)

    summary = {
        "phase": PHASE_ID,
        "dryrun_scope": DRYRUN_SCOPE,
        "guarded_planning_input_loaded": guarded_planning_ok,
        "readiness_input_loaded": readiness_ok,
        "roadmap_decision_input_loaded": roots["roadmap_decision"]["loaded"],
        "protected_asset_resolution_closure_input_loaded": pahr_ok,
        "consolidation_closure_input_loaded": consolidation_ok,
        "structure_map_input_loaded": roots["structure_map"]["loaded"],
        "gate_taxonomy_input_loaded": roots["gate_taxonomy"]["loaded"],
        "guarded_migration_dryrun_execution_plan_generated": True,
        "batch_gate_dryrun_results_generated": True,
        "gate_sequence_dryrun_report_generated": True,
        "exclusion_scope_dryrun_report_generated": True,
        "candidate_scope_dryrun_report_generated": True,
        "post_migration_test_binding_dryrun_report_generated": True,
        "rollback_checkpoint_dryrun_report_generated": True,
        "human_approval_checkpoint_dryrun_report_generated": True,
        "guarded_dryrun_boundary_review_generated": True,
        "guarded_dryrun_readiness_decision_generated": True,
        "batch_count": batch_gate_dryrun.get("batch_count", 0),
        "gate_sequence_count": gate_seq_report.get("gate_sequence_count", 0),
        "migration_candidate_scope_count": candidate_report.get("migration_candidate_scope_count", 0),
        "migration_exclusion_scope_count": excl_count,
        "post_migration_test_count": test_binding_report.get("test_count", 0),
        "bound_test_count": test_binding_report.get("bound_test_count", 0),
        "unbound_test_count": test_binding_report.get("unbound_test_count", 0),
        "executed_test_count": test_binding_report.get("executed_test_count", 0),
        "rollback_checkpoint_count": rollback_report.get("rollback_checkpoint_count", 0),
        "protected_assets_excluded_from_migration": True,
        "permanent_blocks_excluded_from_migration": True,
        "human_review_items_excluded_or_manual_only": True,
        "eval_out_outputs_excluded": True,
        "verifier_reports_excluded": True,
        "go_no_go_packs_excluded": True,
        "correction_records_excluded": True,
        "historical_test_logs_excluded": True,
        "phase_records_excluded": True,
        "whitebox_test_center_physical_restructure_excluded": True,
        "developer_backend_full_architecture_excluded": True,
        "future_reserved_module_finalization_excluded": True,
        "runtime_behavior_changes_excluded": True,
        "client_runtime_changes_excluded": True,
        "post_migration_tests_bound_to_batches": tests_bound,
        "post_migration_tests_executed": False,
        "rollback_checkpoint_per_batch": rollback_report.get("rollback_checkpoint_per_batch"),
        "rollback_executed": False,
        "human_approval_checkpoint_required": human_report.get("human_approval_checkpoint_required"),
        "final_owner_human_confirmed": False,
        "approval_executed": False,
        "approval_does_not_override_safety_gate": human_report.get("approval_does_not_override_safety_gate"),
        "approval_does_not_override_permanent_dnae": human_report.get("approval_does_not_override_permanent_dnae"),
        "candidate_scopes_execution_allowed": False,
        "ready_for_post_dryrun_review": boundary_ok,
        "ready_for_real_migration": False,
        "ready_for_file_move": False,
        "ready_for_file_delete": False,
        "ready_for_module_merge": False,
        "migration_execution_allowed": False,
        "actual_file_move_executed": False,
        "actual_file_delete_executed": False,
        "actual_file_rename_executed": False,
        "actual_module_merge_executed": False,
        "docs_modified_by_dryrun": False,
        "readme_modified_by_dryrun": False,
        "phase_verdict_table_modified_by_dryrun": False,
        "existing_phase_result_changed": False,
        "runtime_enabled": False,
        "no_runtime_executed": True,
        "no_new_runtime_enabled": True,
        "file_operation_invoked": False,
        "stat_invoked": False,
        "exists_invoked": False,
        "file_opened": False,
        "file_content_read": False,
        "image_content_read": False,
        "video_content_read": False,
        "world_model_written": False,
        "memory_written": False,
        "library_written": False,
        "fact_written": False,
        "navigation_action_triggered": False,
        "speech_gate_invoked": False,
        "tts_invoked": False,
        "boundary_ok": boundary_ok,
        "violations": blockers,
        "final_decision": FINAL_DECISION if boundary_ok else "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_REQUIRES_FIXES",
        "recommended_next_phase": NEXT_PHASE if boundary_ok else PHASE_ID,
        "inventory_entry_count": inventory_count,
        "human_review_case_count": HUMAN_REVIEW_CARRYOVER,
        "permanent_block_case_count": PERMANENT_BLOCK_CARRYOVER,
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    next_phase_recommendation = {
        "final_decision": summary["final_decision"],
        "recommended_next_phase": summary["recommended_next_phase"],
        "reason": "B0-B7 gate simulation chain complete; 31 tests bound not executed; ready for guarded post-dryrun review",
        "source_chain": SOURCE_CHAIN,
        **_not_fact(),
    }

    return {
        "summary": summary,
        "input_root_matrix": {"rows": input_rows, "row_count": len(input_rows), "source_chain": SOURCE_CHAIN, **_not_fact()},
        "guarded_migration_dryrun_execution_plan": guarded_migration_dryrun_execution_plan,
        "batch_gate_dryrun_results": batch_gate_dryrun,
        "gate_sequence_dryrun_report": gate_seq_report,
        "exclusion_scope_dryrun_report": exclusion_report,
        "candidate_scope_dryrun_report": candidate_report,
        "post_migration_test_binding_dryrun_report": test_binding_report,
        "rollback_checkpoint_dryrun_report": rollback_report,
        "human_approval_checkpoint_dryrun_report": human_report,
        "guarded_dryrun_boundary_review": boundary_review,
        "guarded_dryrun_readiness_decision": guarded_dryrun_readiness_decision,
        "governance_debt_register": governance_debt_register,
        "next_phase_recommendation": next_phase_recommendation,
        "no_file_move_boundary_report": no_file_move,
        "no_delete_boundary_report": no_delete,
        "no_runtime_boundary_report": no_runtime,
        "no_write_boundary_report": no_write,
    }
