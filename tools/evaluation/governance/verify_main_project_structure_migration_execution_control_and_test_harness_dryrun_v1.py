#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Execution Control and Test Harness DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Post-DryRun-Review-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_dryrun_only"

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
            / "main_project_structure_migration_execution_control_and_test_harness_dryrun_v1_smoke_v0"
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
    plan = _load_json(root / "execution_control_dryrun_execution_plan.json")
    gate = _load_json(root / "execution_control_gate_dryrun_result.json")
    batch_arm = _load_json(root / "batch_arming_dryrun_results.json")
    abort_res = _load_json(root / "abort_condition_dryrun_results.json")
    pre_exec = _load_json(root / "pre_execution_checklist_dryrun_result.json")
    harness = _load_json(root / "post_migration_test_harness_dryrun_result.json")
    verifier_dr = _load_json(root / "post_migration_verifier_suite_dryrun_result.json")
    rollback_dr = _load_json(root / "rollback_rehearsal_dryrun_result.json")
    failure_dr = _load_json(root / "failure_response_matrix_dryrun_result.json")
    decision = _load_json(root / "execution_control_dryrun_readiness_decision.json")
    forbidden = _load_json(root / "forbidden_execution_report.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    input_matrix = _load_json(root / "input_root_matrix.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)

    for k in (
        "execution_control_planning_input_loaded",
        "guarded_roadmap_input_loaded",
        "guarded_closure_input_loaded",
        "guarded_dryrun_input_loaded",
        "guarded_planning_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
        "execution_control_dryrun_execution_plan_generated",
        "execution_control_gate_dryrun_result_generated",
        "batch_arming_dryrun_results_generated",
        "abort_condition_dryrun_results_generated",
        "pre_execution_checklist_dryrun_result_generated",
        "post_migration_test_harness_dryrun_result_generated",
        "post_migration_verifier_suite_dryrun_result_generated",
        "rollback_rehearsal_dryrun_result_generated",
        "failure_response_matrix_dryrun_result_generated",
        "execution_control_dryrun_readiness_decision_generated",
        "execution_control_gate_simulated_pass",
        "batch_arming_simulated",
        "abort_conditions_simulated",
        "b1_b6_owner_approval_missing_blocks_arming",
        "b7_previous_tests_not_executed_blocks_arming",
        "protected_asset_abort_blocks_execution",
        "HR_abort_blocks_execution",
        "DnAE_abort_blocks_execution",
        "runtime_change_abort_blocks_execution",
        "worldmodel_memory_fact_write_abort_blocks_execution",
        "whitebox_test_center_touch_abort_blocks_execution",
        "owner_approval_missing_abort_blocks_execution",
        "failure_response_matrix_ready",
        "ready_for_post_dryrun_review",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.b0_armed_now", summary.get("b0_armed_now") is False)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.pre_execution_check_count>=14", summary.get("pre_execution_check_count", 0) >= 14)
    ok("summary.post_migration_harness_group_count>=5", summary.get("post_migration_harness_group_count", 0) >= 5)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.required_verifier_count>=4", summary.get("required_verifier_count", 0) >= 4)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)
    ok("summary.execution_permission_granted=false", summary.get("execution_permission_granted") is False)

    for k in (
        "execution_permission_granted",
        "checklist_executed",
        "post_migration_tests_execution_allowed",
        "post_migration_tests_executed",
        "verifier_suite_execution_allowed",
        "verifier_suite_executed",
        "rollback_rehearsal_execution_allowed",
        "rollback_rehearsal_executed",
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
        "docs_modified_by_dryrun",
        "readme_modified_by_dryrun",
        "phase_verdict_table_modified_by_dryrun",
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

    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.rollback_rehearsal_required", summary.get("rollback_rehearsal_required") is True)
    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("plan.execution_mode", plan.get("execution_mode") == "dryrun_only")
    ok("plan.real_migration_execution_allowed=false", plan.get("real_migration_execution_allowed") is False)
    ok("plan.batch_arming_execution_allowed=false", plan.get("batch_arming_execution_allowed") is False)

    ok("gate.gate_simulated_pass", gate.get("gate_simulated_pass") is True)
    ok("gate.execution_permission_granted=false", gate.get("execution_permission_granted") is False)
    ok("gate.guarded_migration_chain_closed", gate.get("guarded_migration_chain_closed") is True)
    ok("gate.owner_approval_not_auto_confirmed", gate.get("owner_approval_not_auto_confirmed") is True)

    ok("batch_arm.armed_batch_count", batch_arm.get("armed_batch_count") == 0)
    ok("batch_arm.batch_count", batch_arm.get("batch_count") == 8)
    for i, b in enumerate(batch_arm.get("batch_results") or []):
        ok(f"batch[{i}].armed_now=false", b.get("armed_now") is False)
        ok(f"batch[{i}].arming_allowed_now=false", b.get("arming_allowed_now") is False)
        ok(f"batch[{i}].execution_allowed_now=false", b.get("execution_allowed_now") is False)
        if b.get("batch_id") == "B0":
            ok(f"batch[{i}].owner_not_required", b.get("owner_approval_required") is False)
        if b.get("batch_id") in ("B1", "B2", "B3", "B4", "B5", "B6"):
            ok(f"batch[{i}].owner_required", b.get("owner_approval_required") is True)
            ok(f"batch[{i}].owner_not_present", b.get("owner_approval_present") is False)

    ok("abort.count>=16", abort_res.get("abort_condition_count", 0) >= 16)
    for i, a in enumerate(abort_res.get("conditions") or []):
        ok(f"abort[{i}].has_id", bool(a.get("abort_condition_id")))
        ok(f"abort[{i}].audit_required", a.get("audit_required") is True)
    for cond in (
        "protected_asset_touched",
        "hr_item_without_manual_decision",
        "dnae_item_included",
        "missing_test_harness",
        "missing_verifier_suite",
        "missing_rollback_checkpoint",
        "runtime_behavior_changed",
        "world_model_memory_fact_write",
        "client_backend_boundary_violation",
        "whitebox_test_center_touched",
        "future_reserved_module_finalized",
        "owner_approval_missing",
        "post_batch_test_failed",
    ):
        found = [a for a in abort_res.get("conditions") or [] if a.get("condition_name") == cond]
        ok(f"abort.{cond}.exists", len(found) == 1)
        if found:
            ok(f"abort.{cond}.blocks", found[0].get("blocks_execution") is True)
            ok(f"abort.{cond}.simulated_triggered", found[0].get("simulated_triggered") is True)

    ok("pre_exec.checklist_executed=false", pre_exec.get("checklist_executed") is False)
    ok("pre_exec.count>=14", pre_exec.get("checklist_item_count", 0) >= 14)

    ok("harness.test_count", harness.get("post_migration_test_count") == 31)
    ok("harness.executed_test_count", harness.get("executed_test_count") == 0)
    ok("harness.tests_execution_allowed_now=false", harness.get("tests_execution_allowed_now") is False)
    ok("harness.structural", harness.get("structural_integrity_harness_defined") is True)
    ok("harness.governance", harness.get("governance_boundary_harness_defined") is True)
    ok("harness.functional", harness.get("functional_smoke_verifier_harness_defined") is True)
    ok("harness.no_runtime", harness.get("no_runtime_regression_harness_defined") is True)
    ok("harness.developer", harness.get("developer_tooling_preservation_harness_defined") is True)

    ok("verifier_dr.executed=false", verifier_dr.get("verifier_suite_executed") is False)
    ok("verifier_dr.count>=12", verifier_dr.get("verifier_suite_count", 0) >= 12)
    ok("verifier_dr.required>=4", verifier_dr.get("required_verifier_count", 0) >= 4)
    ok("verifier_dr.execution_allowed_now=false", verifier_dr.get("verifier_suite_execution_allowed_now") is False)

    ok("rollback.rehearsal_required", rollback_dr.get("rehearsal_required_before_real_migration") is True)
    ok("rollback.rehearsal_not_executed", rollback_dr.get("rollback_rehearsal_executed") is False)
    ok("rollback.still_blocked", rollback_dr.get("rollback_execution_still_blocked") is True)
    ok("rollback.rehearsal_not_allowed_now", rollback_dr.get("rehearsal_execution_allowed_now") is False)

    ok("failure.ready", failure_dr.get("failure_response_matrix_ready") is True)
    ok("failure.count>=11", failure_dr.get("failure_response_type_count", 0) >= 11)

    ok("decision.ready_for_post_dryrun_review", decision.get("ready_for_post_dryrun_review") is True)
    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("forbidden.all_respected", forbidden.get("all_forbidden_respected") is True)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)

    idx = {r.get("intake_id"): r for r in input_matrix.get("rows", [])}
    for intake_id in (
        "execution_control_planning",
        "guarded_roadmap",
        "guarded_closure",
        "guarded_dryrun",
        "guarded_planning",
        "readiness",
        "pahr_closure",
        "structure_map",
        "gate_taxonomy",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    for i in range(12):
        ok(f"meta.dryrun_scope_repeat[{i}]", summary.get("dryrun_scope") == DRYRUN_SCOPE)
    for i in range(10):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(8):
        ok(f"meta.executed_test_count_repeat[{i}]", summary.get("executed_test_count") == 0)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.verifier_suite_executed_repeat[{i}]", summary.get("verifier_suite_executed") is False)
    for i in range(15):
        ok(f"meta.rollback_rehearsal_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(12):
        ok(f"meta.execution_permission_granted_repeat[{i}]", summary.get("execution_permission_granted") is False)
    for i in range(10):
        ok(f"meta.batch_arming_execution_allowed_repeat[{i}]", summary.get("batch_arming_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.post_migration_test_count_repeat[{i}]", summary.get("post_migration_test_count") == 31)
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch.{bid}.in_results", any(b.get("batch_id") == bid for b in batch_arm.get("batch_results") or []))
    for i in range(8):
        ok(f"meta.checklist_executed_repeat[{i}]", summary.get("checklist_executed") is False)
    for i in range(7):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

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
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
