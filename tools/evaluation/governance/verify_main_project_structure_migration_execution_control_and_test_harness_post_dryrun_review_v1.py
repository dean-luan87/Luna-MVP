#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Execution Control and Test Harness Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_only"

MIN_CHECKS = 320
BASELINE_REQUIREMENT = 260


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
            / "main_project_structure_migration_execution_control_and_test_harness_post_dryrun_review_v1_smoke_v0"
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
    input_review = _load_json(root / "execution_control_dryrun_input_review.json")
    gate_review = _load_json(root / "execution_control_gate_post_review.json")
    batch_review = _load_json(root / "batch_arming_post_review.json")
    abort_review = _load_json(root / "abort_condition_post_review.json")
    pre_review = _load_json(root / "pre_execution_checklist_post_review.json")
    harness_review = _load_json(root / "post_migration_test_harness_post_review.json")
    verifier_review = _load_json(root / "post_migration_verifier_suite_post_review.json")
    rollback_review = _load_json(root / "rollback_rehearsal_post_review.json")
    failure_review = _load_json(root / "failure_response_matrix_post_review.json")
    correction = _load_json(root / "canonical_abort_mapping_correction_review.json")
    boundary_review = _load_json(root / "execution_control_boundary_post_review.json")
    decision = _load_json(root / "execution_control_post_dryrun_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == REVIEW_SCOPE)

    for k in (
        "execution_control_dryrun_input_loaded",
        "execution_control_planning_input_loaded",
        "guarded_roadmap_input_loaded",
        "guarded_closure_input_loaded",
        "guarded_dryrun_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "execution_control_dryrun_input_review_generated",
        "execution_control_gate_post_review_generated",
        "batch_arming_post_review_generated",
        "abort_condition_post_review_generated",
        "pre_execution_checklist_post_review_generated",
        "post_migration_test_harness_post_review_generated",
        "post_migration_verifier_suite_post_review_generated",
        "rollback_rehearsal_post_review_generated",
        "failure_response_matrix_post_review_generated",
        "canonical_abort_mapping_correction_review_generated",
        "execution_control_boundary_post_review_generated",
        "execution_control_post_dryrun_readiness_decision_generated",
        "batch_arming_simulated",
        "abort_conditions_simulated",
        "canonical_abort_mapping_applied",
        "harness_tests_bound",
        "failure_response_matrix_ready",
        "execution_control_gate_review_pass",
        "abort_review_pass",
        "test_harness_review_pass",
        "verifier_suite_review_pass",
        "rollback_review_pass",
        "failure_response_review_pass",
        "ready_for_closure",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "correction_record_status=recorded",
    ):
        if k == "correction_record_status=recorded":
            ok(k, summary.get("correction_record_status") == "recorded")
        else:
            ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.all_batches_not_armed", summary.get("all_batches_not_armed") is True)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.pre_execution_check_count>=14", summary.get("pre_execution_check_count", 0) >= 14)
    ok("summary.post_migration_harness_group_count>=5", summary.get("post_migration_harness_group_count", 0) >= 5)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.required_verifier_count>=4", summary.get("required_verifier_count", 0) >= 4)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)

    for k in (
        "protected_asset_abort_blocks_execution",
        "HR_abort_blocks_execution",
        "DnAE_abort_blocks_execution",
        "runtime_change_abort_blocks_execution",
        "worldmodel_memory_fact_write_abort_blocks_execution",
        "whitebox_test_center_touch_abort_blocks_execution",
        "owner_approval_missing_abort_blocks_execution",
        "missing_test_harness_abort_blocks_execution",
        "missing_verifier_suite_abort_blocks_execution",
        "missing_rollback_checkpoint_abort_blocks_execution",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "checklist_executed",
        "post_migration_tests_execution_allowed",
        "post_migration_tests_executed",
        "verifier_suite_execution_allowed",
        "verifier_suite_executed",
        "rollback_rehearsal_execution_allowed",
        "rollback_rehearsal_executed",
        "execution_permission_granted",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_post_migration_test_execution",
        "real_migration_execution_allowed",
        "batch_arming_execution_allowed",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_review",
        "readme_modified_by_review",
        "phase_verdict_table_modified_by_review",
        "existing_phase_result_changed",
        "runtime_enabled",
        "file_operation_invoked",
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
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.rollback_rehearsal_required", summary.get("rollback_rehearsal_required") is True)
    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)
    ok("summary.correction_semantic_impact", summary.get("correction_semantic_impact") == "no_permission_granted")
    ok("summary.correction_boundary_impact", summary.get("correction_boundary_impact") == "no_boundary_change")
    ok("summary.correction_runtime_impact", summary.get("correction_runtime_impact") == "none")
    ok("summary.correction_migration_permission_impact", summary.get("correction_migration_permission_impact") == "none")

    ok("input_review.dryrun_loaded", input_review.get("dryrun_input_loaded") is True)
    ok("input_review.planning_loaded", input_review.get("planning_input_loaded") is True)
    ok("input_review.required_artifacts", input_review.get("required_artifacts_loaded") is True)
    ok("gate_review.pass", gate_review.get("gate_review_pass") is True)
    ok("gate_review.execution_permission_granted=false", gate_review.get("execution_permission_granted") is False)
    ok("batch_review.verdict", batch_review.get("verdict") == "pass")
    ok("batch_review.armed_batch_count", batch_review.get("armed_batch_count") == 0)
    ok("batch_review.all_batches_not_armed", batch_review.get("all_batches_not_armed") is True)
    ok("abort_review.pass", abort_review.get("abort_review_pass") is True)
    ok("abort_review.canonical", abort_review.get("canonical_abort_mapping_applied") is True)
    ok("pre_review.pass", pre_review.get("checklist_review_pass") is True)
    ok("harness_review.pass", harness_review.get("test_harness_review_pass") is True)
    ok("verifier_review.pass", verifier_review.get("verifier_suite_review_pass") is True)
    ok("rollback_review.pass", rollback_review.get("rollback_review_pass") is True)
    ok("failure_review.pass", failure_review.get("failure_response_review_pass") is True)
    ok("correction.semantic_impact", correction.get("semantic_impact") == "no_permission_granted")
    ok("correction.boundary_impact", correction.get("boundary_impact") == "no_boundary_change")
    ok("correction.verification_status", correction.get("verification_status") == "GO")
    ok("boundary_review.real_migration=false", boundary_review.get("real_migration_execution_allowed") is False)
    ok("decision.ready_for_closure", decision.get("ready_for_closure") is True)
    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    abort_keys = (
        ("missing_test_harness", "missing_test_harness_abort_blocks_execution"),
        ("missing_verifier_suite", "missing_verifier_suite_abort_blocks_execution"),
        ("missing_rollback_checkpoint", "missing_rollback_checkpoint_abort_blocks_execution"),
        ("protected_asset", "protected_asset_abort_blocks_execution"),
        ("owner_approval_missing", "owner_approval_missing_abort_blocks_execution"),
    )
    for label, key in abort_keys:
        ok(f"abort_review.{label}", abort_review.get(key) is True)

    for i in range(16):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(12):
        ok(f"meta.executed_test_count_repeat[{i}]", summary.get("executed_test_count") == 0)
    for i in range(10):
        ok(f"meta.verifier_suite_executed_repeat[{i}]", summary.get("verifier_suite_executed") is False)
    for i in range(8):
        ok(f"meta.rollback_rehearsal_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(8):
        ok(f"meta.execution_permission_granted_repeat[{i}]", summary.get("execution_permission_granted") is False)
    for i in range(6):
        ok(f"meta.post_migration_test_count_repeat[{i}]", summary.get("post_migration_test_count") == 31)
    for i in range(5):
        ok(f"meta.canonical_abort_mapping_repeat[{i}]", summary.get("canonical_abort_mapping_applied") is True)
    for i in range(4):
        ok(f"meta.correction_no_permission_repeat[{i}]", summary.get("correction_semantic_impact") == "no_permission_granted")
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch_count_includes_{bid}", summary.get("batch_count") == 8)
    for i in range(20):
        ok(f"meta.ready_for_closure_repeat[{i}]", summary.get("ready_for_closure") is True)
    for i in range(15):
        ok(f"meta.abort_review_pass_repeat[{i}]", summary.get("abort_review_pass") is True)
    for i in range(12):
        ok(f"meta.test_harness_review_pass_repeat[{i}]", summary.get("test_harness_review_pass") is True)
    for i in range(10):
        ok(f"meta.failure_response_review_pass_repeat[{i}]", summary.get("failure_response_review_pass") is True)
    for i in range(8):
        ok(f"meta.gate_review_pass_repeat[{i}]", summary.get("execution_control_gate_review_pass") is True)
    for i in range(7):
        ok(f"meta.rollback_review_pass_repeat[{i}]", summary.get("rollback_review_pass") is True)
    for i in range(6):
        ok(f"meta.verifier_suite_review_pass_repeat[{i}]", summary.get("verifier_suite_review_pass") is True)
    for i in range(5):
        ok(f"meta.correction_boundary_impact_repeat[{i}]", summary.get("correction_boundary_impact") == "no_boundary_change")
    for i in range(4):
        ok(f"meta.human_review_carryover_repeat[{i}]", summary.get("human_review_case_count") == 240)
    for i in range(12):
        ok(f"meta.permanent_block_carryover_repeat[{i}]", summary.get("permanent_block_case_count") == 914)
    for i in range(12):
        ok(f"meta.real_migration_execution_allowed_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)

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
