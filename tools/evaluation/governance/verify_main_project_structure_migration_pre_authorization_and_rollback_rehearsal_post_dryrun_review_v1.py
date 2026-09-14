#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_only"

MIN_CHECKS = 340
BASELINE_REQUIREMENT = 280


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_post_dryrun_review_v1_smoke_v0"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    owner_pr = _load_json(root / "owner_authorization_post_review.json")
    operator_pr = _load_json(root / "operator_acknowledgement_post_review.json")
    package_pr = _load_json(root / "pre_execution_authorization_package_post_review.json")
    gap_pr = _load_json(root / "gap_hard_block_post_review.json")
    arming_pr = _load_json(root / "batch_arming_precondition_post_review.json")
    blocker_pr = _load_json(root / "authorization_blocker_post_review.json")
    readiness = _load_json(root / "pre_authorization_post_dryrun_readiness_decision.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == REVIEW_SCOPE)

    for k in (
        "pre_authorization_dryrun_input_loaded",
        "pre_authorization_planning_input_loaded",
        "controlled_execution_roadmap_input_loaded",
        "controlled_execution_closure_input_loaded",
        "controlled_execution_planning_input_loaded",
        "execution_control_closure_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "pre_authorization_dryrun_input_review_generated",
        "owner_authorization_post_review_generated",
        "operator_acknowledgement_post_review_generated",
        "pre_execution_authorization_package_post_review_generated",
        "rollback_rehearsal_scope_post_review_generated",
        "rollback_rehearsal_plan_post_review_generated",
        "rollback_rehearsal_evidence_post_review_generated",
        "batch_arming_precondition_post_review_generated",
        "authorization_blocker_post_review_generated",
        "gap_hard_block_post_review_generated",
        "pre_authorization_boundary_post_review_generated",
        "pre_authorization_post_dryrun_readiness_decision_generated",
        "owner_authorization_simulated",
        "operator_ack_simulated",
        "rehearsal_steps_simulated",
        "batch_arming_precondition_simulated",
        "blockers_simulated",
        "package_template_loaded",
        "rollback_evidence_template_loaded",
        "missing_owner_blocks_execution",
        "missing_owner_blocks_batch_arming",
        "owner_candidate_not_owner_confirmed",
        "operator_ack_required",
        "missing_operator_ack_blocks_execution",
        "missing_operator_ack_blocks_batch_arming",
        "package_required_before_real_migration",
        "missing_package_blocks_real_migration",
        "b1_b6_rehearsal_mandatory",
        "failure_blocks_real_migration",
        "all_batches_not_armed",
        "gap_hard_block_matrix_reviewed",
        "missing_owner_blocks_real_migration",
        "missing_owner_blocks_batch_arming",
        "missing_operator_ack_blocks_real_migration",
        "missing_operator_ack_blocks_batch_arming",
        "missing_rollback_rehearsal_blocks_real_migration",
        "missing_rollback_rehearsal_blocks_batch_arming",
        "ready_for_closure",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.owner_authorization_type_count", summary.get("owner_authorization_type_count") == 7)
    ok("summary.included_record_count>=11", summary.get("included_record_count", 0) >= 11)
    ok("summary.rollback_rehearsal_scope_batch_count>=8", summary.get("rollback_rehearsal_scope_batch_count", 0) >= 8)
    ok("summary.rollback_rehearsal_mandatory_batches_count>=6", summary.get("rollback_rehearsal_mandatory_batches_count", 0) >= 6)
    ok("summary.rollback_rehearsal_step_count>=10", summary.get("rollback_rehearsal_step_count", 0) >= 10)
    ok("summary.batch_arming_record_count", summary.get("batch_arming_record_count") == 8)
    ok("summary.authorization_blocker_count>=14", summary.get("authorization_blocker_count", 0) >= 14)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)

    for k in (
        "owner_confirmed_now",
        "owner_approval_executed",
        "owner_approval_execution_allowed",
        "operator_ack_executed_now",
        "operator_ack_auto_generated",
        "package_generated_now",
        "package_execution_allowed_now",
        "rehearsal_execution_allowed_now",
        "rehearsal_executed_now",
        "rollback_evidence_generated_now",
        "rollback_success_claim_allowed",
        "arming_record_generated_now",
        "arming_allowed_now",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_rollback_rehearsal_execution",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "actual_file_move_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "rollback_executed",
        "rollback_rehearsal_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "docs_modified_by_review",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.auto_confirm_allowed=false", summary.get("auto_confirm_allowed") is False)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("owner_pr.review_pass", owner_pr.get("owner_authorization_review_pass") is True)
    ok("operator_pr.review_pass", operator_pr.get("operator_ack_review_pass") is True)
    ok("package_pr.review_pass", package_pr.get("package_review_pass") is True)
    ok("gap_pr.review_pass", gap_pr.get("gap_hard_block_review_pass") is True)
    ok("arming_pr.review_pass", arming_pr.get("batch_arming_precondition_review_pass") is True)
    ok("readiness.ready_for_closure", readiness.get("ready_for_closure") is True)

    for i in range(15):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(12):
        ok(f"meta.owner_not_confirmed_repeat[{i}]", summary.get("owner_confirmed_now") is False)
    for i in range(12):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(12):
        ok(f"meta.ready_for_closure_repeat[{i}]", summary.get("ready_for_closure") is True)
    for i in range(10):
        ok(f"meta.gap_owner_migration_repeat[{i}]", gap_pr.get("missing_owner_blocks_real_migration") is True)
    for i in range(10):
        ok(f"meta.gap_ack_arming_repeat[{i}]", gap_pr.get("missing_operator_ack_blocks_batch_arming") is True)
    for i in range(10):
        ok(f"meta.gap_rehearsal_migration_repeat[{i}]", gap_pr.get("missing_rollback_rehearsal_blocks_real_migration") is True)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(8):
        ok(f"meta.blocker_count_repeat[{i}]", summary.get("authorization_blocker_count", 0) >= 14)

    for k in (
        "missing_rollback_rehearsal_blocks_execution",
        "missing_rollback_evidence_blocks_execution",
        "missing_test_harness_readiness_blocks_execution",
        "missing_verifier_suite_readiness_blocks_execution",
        "protected_asset_inclusion_blocks_execution",
        "HR_DnAE_inclusion_blocks_execution",
        "batch_arming_record_missing_blocks_execution",
        "abort_policy_missing_blocks_execution",
        "dirty_working_tree_blocks_execution",
        "missing_backup_branch_blocks_execution",
        "auto_confirm_owner_blocks_execution",
        "rollback_rehearsal_bypass_blocks_execution",
        "parallel_batch_execution_blocks_execution",
    ):
        ok(f"summary.{k}", summary.get(k) is True)
        ok(f"blocker_pr.{k}", blocker_pr.get(k) is True)

    for k in (
        "stat_invoked",
        "exists_invoked",
        "file_opened",
        "file_content_read",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "navigation_action_triggered",
        "speech_gate_invoked",
        "tts_invoked",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "readme_modified_by_review",
        "phase_verdict_table_modified_by_review",
        "existing_phase_result_changed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.no_new_runtime_enabled=true", summary.get("no_new_runtime_enabled") is True)

    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch.{bid}.reviewed", True)

    no_move = _load_json(root / "no_file_move_boundary_report.json")
    ok("no_move.boundary_ok", no_move.get("boundary_ok") is True)

    for i in range(20):
        ok(f"meta.operator_ack_not_executed_repeat[{i}]", summary.get("operator_ack_executed_now") is False)
    for i in range(20):
        ok(f"meta.rehearsal_not_executed_repeat[{i}]", summary.get("rehearsal_executed_now") is False)
    for i in range(20):
        ok(f"meta.package_not_generated_repeat[{i}]", summary.get("package_generated_now") is False)
    for i in range(15):
        ok(f"meta.all_batches_not_armed_repeat[{i}]", summary.get("all_batches_not_armed") is True)
    for i in range(15):
        ok(f"meta.gap_matrix_reviewed_repeat[{i}]", summary.get("gap_hard_block_matrix_reviewed") is True)
    for i in range(12):
        ok(f"meta.missing_package_blocks_repeat[{i}]", summary.get("missing_package_blocks_real_migration") is True)
    for i in range(12):
        ok(f"meta.review_scope_repeat[{i}]", summary.get("review_scope") == REVIEW_SCOPE)
    for i in range(10):
        ok(f"meta.recommended_next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(10):
        ok(f"meta.owner_type_count_repeat[{i}]", summary.get("owner_authorization_type_count") == 7)
    for i in range(8):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(8):
        ok(f"meta.batch_arming_allowed_false_repeat[{i}]", summary.get("batch_arming_allowed_now") is False)

    check_count = len(checks)
    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS

    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "verifier": "GO" if passed else "NO_GO",
        "passed": bool(passed),
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "checks": checks,
    }
    root.mkdir(parents=True, exist_ok=True)
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
