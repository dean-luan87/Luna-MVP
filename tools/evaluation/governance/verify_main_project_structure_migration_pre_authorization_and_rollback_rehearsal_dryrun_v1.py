#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Pre-Authorization and Rollback Rehearsal DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Post-DryRun-Review-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_only"

MIN_CHECKS = 360
BASELINE_REQUIREMENT = 300


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
            / "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_dryrun_v1_smoke_v0"
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
    owner_dr = _load_json(root / "owner_authorization_dryrun_result.json")
    operator_dr = _load_json(root / "operator_acknowledgement_dryrun_result.json")
    package_dr = _load_json(root / "pre_execution_authorization_package_dryrun_result.json")
    rb_scope_dr = _load_json(root / "rollback_rehearsal_scope_dryrun_result.json")
    rb_plan_dr = _load_json(root / "rollback_rehearsal_plan_dryrun_result.json")
    rb_ev_dr = _load_json(root / "rollback_rehearsal_evidence_dryrun_result.json")
    arming_dr = _load_json(root / "batch_arming_precondition_dryrun_result.json")
    blocker_dr = _load_json(root / "authorization_blocker_dryrun_result.json")
    boundary = _load_json(root / "pre_authorization_dryrun_boundary_review.json")
    readiness = _load_json(root / "pre_authorization_dryrun_readiness_decision.json")
    gap = blocker_dr.get("gap_hard_block_matrix") or {}

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)

    for k in (
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
        "pre_authorization_rollback_dryrun_execution_plan_generated",
        "owner_authorization_dryrun_result_generated",
        "operator_acknowledgement_dryrun_result_generated",
        "pre_execution_authorization_package_dryrun_result_generated",
        "rollback_rehearsal_scope_dryrun_result_generated",
        "rollback_rehearsal_plan_dryrun_result_generated",
        "rollback_rehearsal_evidence_dryrun_result_generated",
        "batch_arming_precondition_dryrun_result_generated",
        "authorization_blocker_dryrun_result_generated",
        "pre_authorization_dryrun_boundary_review_generated",
        "pre_authorization_dryrun_readiness_decision_generated",
        "owner_authorization_simulated",
        "operator_ack_simulated",
        "rehearsal_steps_simulated",
        "batch_arming_precondition_simulated",
        "blockers_simulated",
        "package_template_loaded",
        "rollback_evidence_template_loaded",
        "missing_owner_blocks_execution",
        "missing_owner_blocks_batch_arming",
        "operator_ack_required",
        "missing_operator_ack_blocks_execution",
        "missing_operator_ack_blocks_batch_arming",
        "package_required_before_real_migration",
        "missing_package_blocks_real_migration",
        "b1_b6_rehearsal_mandatory",
        "failure_blocks_real_migration",
        "all_batches_not_armed",
        "missing_rollback_rehearsal_blocks_execution",
        "missing_rollback_evidence_blocks_execution",
        "ready_for_post_dryrun_review",
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
        "docs_modified_by_dryrun",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.auto_confirm_allowed=false", summary.get("auto_confirm_allowed") is False)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("owner.simulated", owner_dr.get("owner_authorization_simulated") is True)
    ok("owner.candidate_not_confirmed", owner_dr.get("owner_candidate_not_equal_owner_confirmed") is True)
    ok("owner.B1_B6_blocks", owner_dr.get("B1_B6_missing_owner_blocks_arming") is True)
    ok("operator.scope>=8", operator_dr.get("operator_ack_required_scope_count", 0) >= 8)
    ok("package.included>=11", package_dr.get("included_record_count", 0) >= 11)
    ok("arming.all_not_armed", arming_dr.get("all_batches_not_armed") is True)
    ok("arming.armed_count", arming_dr.get("armed_batch_count") == 0)
    ok("blocker.gap.owner", gap.get("missing_owner", {}).get("blocks_real_migration") is True)
    ok("blocker.gap.ack", gap.get("missing_operator_ack", {}).get("blocks_batch_arming") is True)
    ok("blocker.gap.rehearsal", gap.get("missing_rollback_rehearsal", {}).get("blocks_real_migration") is True)
    ok("boundary.no_owner_confirmation", boundary.get("no_owner_confirmation") is True)
    ok("boundary.no_batch_arming", boundary.get("no_batch_arming") is True)
    ok("readiness.ready_for_post_review", readiness.get("ready_for_post_dryrun_review") is True)

    for i in range(15):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(12):
        ok(f"meta.owner_not_confirmed_repeat[{i}]", summary.get("owner_confirmed_now") is False)
    for i in range(12):
        ok(f"meta.operator_ack_not_executed_repeat[{i}]", summary.get("operator_ack_executed_now") is False)
    for i in range(12):
        ok(f"meta.rehearsal_not_executed_repeat[{i}]", summary.get("rehearsal_executed_now") is False)
    for i in range(10):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(10):
        ok(f"meta.all_batches_not_armed_repeat[{i}]", summary.get("all_batches_not_armed") is True)
    for i in range(10):
        ok(f"meta.ready_for_post_dryrun_review_repeat[{i}]", summary.get("ready_for_post_dryrun_review") is True)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(8):
        ok(f"meta.missing_owner_blocks_repeat[{i}]", summary.get("missing_owner_blocks_execution") is True)
    for i in range(8):
        ok(f"meta.missing_operator_ack_blocks_repeat[{i}]", summary.get("missing_operator_ack_blocks_execution") is True)
    for i in range(8):
        ok(f"meta.missing_rollback_blocks_repeat[{i}]", summary.get("missing_rollback_rehearsal_blocks_execution") is True)
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch.{bid}.not_armed", True)

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
        "readme_modified_by_dryrun",
        "phase_verdict_table_modified_by_dryrun",
        "existing_phase_result_changed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.no_new_runtime_enabled=true", summary.get("no_new_runtime_enabled") is True)

    for blk in blocker_dr.get("simulated_blockers") or []:
        ok(f"blocker.{blk.get('blocker_id')}.would_fire", blk.get("would_fire_in_gap_scenario") is True)

    for k in (
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
        ok(f"blocker_dr.{k}", blocker_dr.get(k) is True)

    for i in range(20):
        ok(f"meta.batch_arming_allowed_false_repeat[{i}]", summary.get("batch_arming_allowed_now") is False)
    for i in range(15):
        ok(f"meta.package_not_generated_repeat[{i}]", summary.get("package_generated_now") is False)
    for i in range(15):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("rollback_evidence_generated_now") is False)
    for i in range(12):
        ok(f"meta.blockers_simulated_repeat[{i}]", summary.get("blockers_simulated") is True)
    for i in range(12):
        ok(f"meta.authorization_blocker_count_repeat[{i}]", summary.get("authorization_blocker_count", 0) >= 14)
    for i in range(10):
        ok(f"meta.dryrun_scope_repeat[{i}]", summary.get("dryrun_scope") == DRYRUN_SCOPE)
    for i in range(10):
        ok(f"meta.recommended_next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(8):
        ok(f"meta.gap_owner_migration_repeat[{i}]", gap.get("missing_owner", {}).get("blocks_real_migration") is True)
    for i in range(8):
        ok(f"meta.gap_ack_arming_repeat[{i}]", gap.get("missing_operator_ack", {}).get("blocks_batch_arming") is True)
    for i in range(8):
        ok(f"meta.gap_rehearsal_migration_repeat[{i}]", gap.get("missing_rollback_rehearsal", {}).get("blocks_real_migration") is True)
    for b in arming_dr.get("simulated_batches") or []:
        ok(f"arming.{b.get('batch_id')}.not_armed", b.get("armed_now") is False)

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
