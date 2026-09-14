#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Guarded DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Post-DryRun-Review-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_guarded_dryrun_only"

MIN_CHECKS = 320
BASELINE_REQUIREMENT = 260


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_guarded_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    exec_plan = _load_json(root / "guarded_migration_dryrun_execution_plan.json")
    batch_results = _load_json(root / "batch_gate_dryrun_results.json")
    gate_report = _load_json(root / "gate_sequence_dryrun_report.json")
    exclusion_report = _load_json(root / "exclusion_scope_dryrun_report.json")
    candidate_report = _load_json(root / "candidate_scope_dryrun_report.json")
    test_report = _load_json(root / "post_migration_test_binding_dryrun_report.json")
    rollback_report = _load_json(root / "rollback_checkpoint_dryrun_report.json")
    human_report = _load_json(root / "human_approval_checkpoint_dryrun_report.json")
    boundary_review = _load_json(root / "guarded_dryrun_boundary_review.json")
    decision = _load_json(root / "guarded_dryrun_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "guarded_planning",
        "readiness",
        "roadmap_decision",
        "pahr_closure",
        "consolidation_closure",
        "structure_map",
        "gate_taxonomy",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)

    for k in (
        "guarded_planning_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    generated = (
        "guarded_migration_dryrun_execution_plan_generated",
        "batch_gate_dryrun_results_generated",
        "gate_sequence_dryrun_report_generated",
        "exclusion_scope_dryrun_report_generated",
        "candidate_scope_dryrun_report_generated",
        "post_migration_test_binding_dryrun_report_generated",
        "rollback_checkpoint_dryrun_report_generated",
        "human_approval_checkpoint_dryrun_report_generated",
        "guarded_dryrun_boundary_review_generated",
        "guarded_dryrun_readiness_decision_generated",
    )
    for k in generated:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.gate_sequence_count", summary.get("gate_sequence_count") == 10)
    ok("summary.migration_candidate_scope_count", summary.get("migration_candidate_scope_count") == 8)
    ok("summary.migration_exclusion_scope_count>=17", summary.get("migration_exclusion_scope_count", 0) >= 17)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.bound_test_count", summary.get("bound_test_count") == 31)
    ok("summary.unbound_test_count", summary.get("unbound_test_count") == 0)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.rollback_checkpoint_count>=8", summary.get("rollback_checkpoint_count", 0) >= 8)

    exclusion_flags = (
        "protected_assets_excluded_from_migration",
        "permanent_blocks_excluded_from_migration",
        "human_review_items_excluded_or_manual_only",
        "eval_out_outputs_excluded",
        "verifier_reports_excluded",
        "go_no_go_packs_excluded",
        "correction_records_excluded",
        "historical_test_logs_excluded",
        "phase_records_excluded",
        "whitebox_test_center_physical_restructure_excluded",
        "developer_backend_full_architecture_excluded",
        "future_reserved_module_finalization_excluded",
        "runtime_behavior_changes_excluded",
        "client_runtime_changes_excluded",
        "post_migration_tests_bound_to_batches",
        "rollback_checkpoint_per_batch",
        "human_approval_checkpoint_required",
        "ready_for_post_dryrun_review",
        "boundary_ok",
    )
    for k in exclusion_flags:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.post_migration_tests_executed=false", summary.get("post_migration_tests_executed") is False)
    ok("summary.rollback_executed=false", summary.get("rollback_executed") is False)
    ok("summary.final_owner_human_confirmed=false", summary.get("final_owner_human_confirmed") is False)
    ok("summary.approval_executed=false", summary.get("approval_executed") is False)
    ok("summary.candidate_scopes_execution_allowed=false", summary.get("candidate_scopes_execution_allowed") is False)

    for k in (
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "migration_execution_allowed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    for k in (
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_dryrun",
        "readme_modified_by_dryrun",
        "phase_verdict_table_modified_by_dryrun",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
        "world_model_written",
        "navigation_action_triggered",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("exec_plan.execution_mode", exec_plan.get("execution_mode") == "dryrun_only")
    ok("exec_plan.batch_count", exec_plan.get("batch_count") == 8)
    ok("exec_plan.actual_file_move_executed=false", exec_plan.get("actual_file_move_executed") is False)

    batches = batch_results.get("batch_results") or []
    ok("batch_results.all_batches_simulated_pass", batch_results.get("all_batches_simulated_pass") is True)
    for i, b in enumerate(batches):
        bid = b.get("batch_id")
        ok(f"batch[{i}].batch_id", bool(bid))
        ok(f"batch[{i}].simulated_pass", b.get("simulated_pass") is True)
        ok(f"batch[{i}].execution_allowed_now=false", b.get("execution_allowed_now") is False)
        ok(f"batch[{i}].file_move_allowed_now=false", b.get("file_move_allowed_now") is False)
        ok(f"batch[{i}].rollback_checkpoint_result.checkpoint_defined", b.get("rollback_checkpoint_result", {}).get("checkpoint_defined") is True)
        ok(f"batch[{i}].post_batch_test_binding.executed=false", b.get("post_batch_test_binding_result", {}).get("executed") is False)
        for j, gr in enumerate(b.get("gate_results") or []):
            if gr.get("applied"):
                ok(f"batch[{i}].gate[{j}].runtime_granted=false", gr.get("runtime_granted") is False)
    for expected in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"batches.has_{expected}", any(x.get("batch_id") == expected for x in batches))

    for i, g in enumerate(gate_report.get("gates") or []):
        ok(f"gate_report[{i}].gate_id", bool(g.get("gate_id")))
        ok(f"gate_report[{i}].execution_blocked_on_failure", g.get("execution_blocked_on_failure") is True)
        ok(f"gate_report[{i}].runtime_granted=false", g.get("runtime_granted") is False)

    for k in (
        "protected_assets_excluded_from_migration",
        "permanent_blocks_excluded_from_migration",
        "whitebox_test_center_physical_restructure_excluded",
        "developer_backend_full_architecture_excluded",
    ):
        ok(f"exclusion_report.{k}", exclusion_report.get(k) is True)

    ok("candidate_report.execution_allowed=false", candidate_report.get("candidate_scopes_execution_allowed") is False)
    for i, c in enumerate(candidate_report.get("candidates") or []):
        ok(f"candidate[{i}].execution_allowed_now=false", c.get("execution_allowed_now") is False)
        ok(f"candidate[{i}].simulated_pass", c.get("simulated_pass") is True)

    ok("test_report.test_count", test_report.get("test_count") == 31)
    ok("test_report.bound_test_count", test_report.get("bound_test_count") == 31)
    ok("test_report.unbound_test_count", test_report.get("unbound_test_count") == 0)
    ok("test_report.executed_test_count", test_report.get("executed_test_count") == 0)
    ok("test_report.structural_integrity_tests_bound", test_report.get("structural_integrity_tests_bound") is True)
    ok("test_report.governance_boundary_tests_bound", test_report.get("governance_boundary_tests_bound") is True)
    ok("test_report.functional_smoke_tests_bound", test_report.get("functional_smoke_tests_bound") is True)
    ok("test_report.no_runtime_regression_tests_bound", test_report.get("no_runtime_regression_tests_bound") is True)
    ok("test_report.developer_tooling_non_execution_tests_bound", test_report.get("developer_tooling_non_execution_tests_bound") is True)

    ok("rollback.rollback_checkpoint_per_batch", rollback_report.get("rollback_checkpoint_per_batch") is True)
    ok("rollback.rollback_executed=false", rollback_report.get("rollback_executed") is False)
    ok("rollback.verifier_rerun_required", rollback_report.get("verifier_rerun_after_rollback_required") is True)

    ok("human.approval_executed=false", human_report.get("approval_executed") is False)
    ok("human.final_owner_human_confirmed=false", human_report.get("final_owner_human_confirmed") is False)
    ok("human.approval_does_not_override_safety_gate", human_report.get("approval_does_not_override_safety_gate") is True)
    ok("human.approval_does_not_override_permanent_dnae", human_report.get("approval_does_not_override_permanent_dnae") is True)

    ok("boundary_review.no_post_migration_tests_executed", boundary_review.get("no_post_migration_tests_executed") is True)
    ok("boundary_review.boundary_ok", boundary_review.get("boundary_ok") is True)

    ok("decision.ready_for_post_dryrun_review", decision.get("ready_for_post_dryrun_review") is True)
    ok("decision.dryrun_verdict", decision.get("dryrun_verdict") == "GO")
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)

    ok("no_move.actual_file_move_executed=false", no_move.get("actual_file_move_executed") is False)

    for k in (
        "closure_boundary_files_excluded",
        "non_claims_registers_excluded",
        "eval_out_outputs_excluded",
        "correction_records_excluded",
        "historical_test_logs_excluded",
        "phase_records_excluded",
        "go_no_go_packs_excluded",
        "verifier_reports_excluded",
    ):
        ok(f"exclusion_report.{k}", exclusion_report.get(k) is True)

    for i, b in enumerate(batches):
        notes = b.get("batch_specific_notes") or {}
        for nk in notes:
            ok(f"batch[{i}].note.{nk}", notes.get(nk) is True)
        ok(f"batch[{i}].pre_batch.simulated_pass", b.get("pre_batch_check_result", {}).get("simulated_pass") is True)
        ok(f"batch[{i}].exclusion.simulated_pass", b.get("exclusion_scope_result", {}).get("simulated_pass") is True)
        ok(f"batch[{i}].human.approval_executed=false", b.get("human_approval_checkpoint_result", {}).get("approval_executed") is False)

    gate_names = (
        "PreBatchProtectedAssetGate",
        "HumanReviewExclusionGate",
        "PermanentDnaeExclusionGate",
        "ClientBackendBoundaryGate",
        "FutureReservedModuleGate",
        "RuntimeBehaviorNoChangeGate",
        "DocsLinkIntegrityGate",
        "PostBatchVerifierGate",
        "RollbackAvailabilityGate",
        "HumanApprovalCheckpointGate",
    )
    report_names = {g.get("gate_name") for g in gate_report.get("gates") or []}
    for gn in gate_names:
        ok(f"gate_report.has_{gn}", gn in report_names)

    ok("summary.no_runtime_executed", summary.get("no_runtime_executed") is True)
    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("summary.approval_does_not_override_safety_gate", summary.get("approval_does_not_override_safety_gate") is True)
    ok("summary.approval_does_not_override_permanent_dnae", summary.get("approval_does_not_override_permanent_dnae") is True)
    ok("exec_plan.migration_execution_allowed=false", exec_plan.get("migration_execution_allowed") is False)
    ok("exec_plan.post_migration_test_count", exec_plan.get("post_migration_test_count") == 31)
    ok("candidate_report.all_simulated_pass", candidate_report.get("all_candidates_simulated_pass") is True)
    ok("rollback.restore_path_map_defined", rollback_report.get("restore_path_map_defined") is True)
    ok("rollback.restore_eval_out_refs_defined", rollback_report.get("restore_eval_out_refs_defined") is True)
    ok("boundary_review.no_file_move_delete_rename_merge", boundary_review.get("no_file_move_delete_rename_merge") is True)
    ok("boundary_review.no_whitebox_restructuring", boundary_review.get("no_whitebox_test_center_restructuring") is True)
    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("decision.blockers_empty", decision.get("blockers") == [])

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
