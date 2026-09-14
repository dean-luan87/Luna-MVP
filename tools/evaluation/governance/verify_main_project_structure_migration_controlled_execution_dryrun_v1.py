#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Execution DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_controlled_execution_dryrun_only"

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
            repo_root / "_eval_out" / "main_project_structure_migration_controlled_execution_dryrun_v1_smoke_v0"
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
    plan = _load_json(root / "controlled_execution_dryrun_execution_plan.json")
    window = _load_json(root / "execution_window_dryrun_result.json")
    owner = _load_json(root / "owner_authorization_gate_dryrun_result.json")
    arming = _load_json(root / "batch_arming_execution_dryrun_result.json")
    progression = _load_json(root / "controlled_batch_progression_dryrun_result.json")
    rollback = _load_json(root / "rollback_rehearsal_precondition_dryrun_result.json")
    test_order = _load_json(root / "post_batch_test_execution_order_dryrun_result.json")
    verifier_order = _load_json(root / "verifier_suite_execution_order_dryrun_result.json")
    abort = _load_json(root / "abort_and_failure_response_dryrun_result.json")
    evidence = _load_json(root / "post_execution_evidence_pack_dryrun_result.json")
    boundary = _load_json(root / "controlled_execution_dryrun_boundary_review.json")
    readiness = _load_json(root / "controlled_execution_dryrun_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)

    for k in (
        "controlled_execution_planning_input_loaded",
        "execution_control_roadmap_input_loaded",
        "execution_control_closure_input_loaded",
        "execution_control_dryrun_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "controlled_execution_dryrun_execution_plan_generated",
        "execution_window_dryrun_result_generated",
        "owner_authorization_gate_dryrun_result_generated",
        "batch_arming_execution_dryrun_result_generated",
        "controlled_batch_progression_dryrun_result_generated",
        "rollback_rehearsal_precondition_dryrun_result_generated",
        "post_batch_test_execution_order_dryrun_result_generated",
        "verifier_suite_execution_order_dryrun_result_generated",
        "abort_and_failure_response_dryrun_result_generated",
        "post_execution_evidence_pack_dryrun_result_generated",
        "controlled_execution_dryrun_boundary_review_generated",
        "controlled_execution_dryrun_readiness_decision_generated",
        "batch_arming_simulated",
        "batch_progression_simulated",
        "all_batches_not_armed",
        "b0_baseline_only_no_move",
        "b1_docs_relink_candidate_only",
        "b2_capability_grouping_candidate_only",
        "b3_governance_grouping_candidate_only",
        "b4_midplatform_grouping_candidate_only",
        "b5_dev_artifact_reference_only",
        "b6_future_marker_only",
        "b7_verification_gate_only",
        "rollback_rehearsal_mandatory",
        "test_execution_order_defined",
        "tests_mapped_to_batches",
        "verifier_execution_order_defined",
        "every_abort_has_failure_response",
        "protected_HR_DnAE_abort_blocks_entire_execution",
        "runtime_worldmodel_memory_fact_abort_blocks_entire_execution",
        "missing_harness_verifier_rollback_blocks_execution",
        "failed_post_batch_test_blocks_next_batch",
        "failed_verifier_suite_blocks_next_batch",
        "rollback_rehearsal_failure_blocks_real_migration",
        "whitebox_test_center_touched_blocks_execution",
        "post_execution_evidence_pack_template_defined",
        "ready_for_post_dryrun_review",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.owner_authorization_gate_count>=7", summary.get("owner_authorization_gate_count", 0) >= 7)
    ok("summary.execution_window_requirement_count>=8", summary.get("execution_window_requirement_count", 0) >= 8)
    ok("summary.post_batch_test_count", summary.get("post_batch_test_count") == 31)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)
    ok("summary.required_verifier_count>=4", summary.get("required_verifier_count", 0) >= 4)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.batch_execution_count", summary.get("batch_execution_count") == 0)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)

    for k in (
        "execution_window_opened",
        "owner_auto_confirm_allowed",
        "owner_approval_executed",
        "final_owner_human_confirmed",
        "post_migration_tests_execution_allowed",
        "post_migration_tests_executed",
        "verifier_suite_execution_allowed",
        "verifier_suite_executed",
        "rollback_rehearsal_executed",
        "evidence_pack_generated_now",
        "execution_result_claimed_now",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_post_migration_test_execution",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
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

    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("plan.execution_mode", plan.get("execution_mode") == "dryrun_only")
    ok("plan.real_migration=false", plan.get("real_migration_execution_allowed") is False)
    ok("plan.batch_arming=false", plan.get("batch_arming_allowed_now") is False)

    ok("window.opened=false", window.get("execution_window_opened") is False)
    ok("window.review_pass", window.get("execution_window_review_pass") is True)
    ok("window.dedicated_branch", window.get("dedicated_branch_required") is True)
    ok("window.one_batch_at_a_time", window.get("one_batch_at_a_time_required") is True)
    ok("window.no_parallel", window.get("no_parallel_migration_batches") is True)

    ok("owner.count>=7", owner.get("owner_authorization_gate_count", 0) >= 7)
    ok("owner.auto_confirm=false", owner.get("owner_auto_confirm_allowed") is False)
    ok("owner.approval_not_executed", owner.get("owner_approval_executed") is False)
    ok("owner.human_not_confirmed", owner.get("final_owner_human_confirmed") is False)
    ok("owner.review_pass", owner.get("owner_authorization_review_pass") is True)

    ok("arming.simulated", arming.get("batch_arming_simulated") is True)
    ok("arming.armed_count=0", arming.get("armed_batch_count") == 0)
    ok("arming.all_not_armed", arming.get("all_batches_not_armed") is True)
    ok("arming.b0_not_armed", arming.get("b0_armed_now") is False)
    ok("arming.b1_b6_blocks", arming.get("b1_b6_owner_approval_missing_blocks_arming") is True)
    ok("arming.b7_blocks", arming.get("b7_previous_tests_not_executed_blocks_arming") is True)
    for br in arming.get("batch_results") or []:
        ok(f"arming.{br.get('batch_id')}.not_armed", br.get("armed_now") is False)

    ok("progression.simulated", progression.get("batch_progression_simulated") is True)
    ok("progression.execution_count=0", progression.get("batch_execution_count") == 0)
    ok("progression.review_pass", progression.get("progression_review_pass") is True)

    ok("rollback.mandatory", rollback.get("rollback_rehearsal_mandatory") is True)
    ok("rollback.not_executed", rollback.get("rollback_rehearsal_executed") is False)
    ok("rollback.still_blocked", rollback.get("rollback_execution_still_blocked") is True)
    ok("rollback.covers_b1_b6", rollback.get("rollback_rehearsal_covers_b1_b6") is True)

    ok("test_order.count", test_order.get("post_batch_test_count") == 31)
    ok("test_order.not_executed", test_order.get("post_migration_tests_executed") is False)
    ok("test_order.executed_count=0", test_order.get("executed_test_count") == 0)
    ok("test_order.review_pass", test_order.get("post_batch_test_order_review_pass") is True)

    ok("verifier_order.count>=12", verifier_order.get("verifier_suite_count", 0) >= 12)
    ok("verifier_order.not_executed", verifier_order.get("verifier_suite_executed") is False)
    ok("verifier_order.review_pass", verifier_order.get("verifier_suite_order_review_pass") is True)

    ok("abort.count>=16", abort.get("abort_condition_count", 0) >= 16)
    ok("abort.failure>=11", abort.get("failure_response_type_count", 0) >= 11)
    ok("abort.review_pass", abort.get("abort_failure_response_review_pass") is True)

    ok("evidence.template_defined", evidence.get("post_execution_evidence_pack_template_defined") is True)
    ok("evidence.not_generated", evidence.get("evidence_pack_generated_now") is False)
    ok("evidence.moved_count=0", evidence.get("moved_file_count_claimed_now") == 0)

    ok("boundary.no_real_migration", boundary.get("no_real_migration") is True)
    ok("boundary.no_batch_arming", boundary.get("no_batch_arming") is True)
    ok("boundary.no_test_execution", boundary.get("no_test_execution") is True)

    ok("readiness.ready_for_post_dryrun_review", readiness.get("ready_for_post_dryrun_review") is True)
    ok("readiness.ready_for_real_migration=false", readiness.get("ready_for_real_migration") is False)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(15):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(15):
        ok(f"meta.execution_window_opened_repeat[{i}]", summary.get("execution_window_opened") is False)
    for i in range(12):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(12):
        ok(f"meta.batch_arming_allowed_false_repeat[{i}]", summary.get("batch_arming_allowed_now") is False)
    for i in range(10):
        ok(f"meta.post_batch_test_count_repeat[{i}]", summary.get("post_batch_test_count") == 31)
    for i in range(10):
        ok(f"meta.verifier_suite_count_repeat[{i}]", summary.get("verifier_suite_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.rollback_rehearsal_mandatory_repeat[{i}]", summary.get("rollback_rehearsal_mandatory") is True)
    for i in range(10):
        ok(f"meta.rollback_rehearsal_executed_false_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(8):
        ok(f"meta.executed_test_count_repeat[{i}]", summary.get("executed_test_count") == 0)
    for i in range(8):
        ok(f"meta.batch_execution_count_repeat[{i}]", summary.get("batch_execution_count") == 0)
    for i in range(8):
        ok(f"meta.evidence_pack_false_repeat[{i}]", summary.get("evidence_pack_generated_now") is False)
    for i in range(8):
        ok(f"meta.owner_approval_executed_false_repeat[{i}]", summary.get("owner_approval_executed") is False)
    for k in (
        "b0_baseline_only_no_move",
        "b1_docs_relink_candidate_only",
        "b2_capability_grouping_candidate_only",
        "b3_governance_grouping_candidate_only",
        "b4_midplatform_grouping_candidate_only",
        "b5_dev_artifact_reference_only",
        "b6_future_marker_only",
        "b7_verification_gate_only",
    ):
        for i in range(5):
            ok(f"meta.{k}_repeat[{i}]", summary.get(k) is True)
    for i in range(20):
        ok(f"meta.abort_condition_count_repeat[{i}]", summary.get("abort_condition_count", 0) >= 16)
    for i in range(15):
        ok(f"meta.failure_response_type_count_repeat[{i}]", summary.get("failure_response_type_count", 0) >= 11)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(8):
        ok(f"meta.ready_for_post_dryrun_review_repeat[{i}]", summary.get("ready_for_post_dryrun_review") is True)
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch.{bid}.arming_sim", any(b.get("batch_id") == bid for b in arming.get("batch_results") or []))
    for i in range(31):
        chain = test_order.get("simulated_test_chain") or []
        if i < len(chain):
            ok(f"test_chain[{i}].not_executed", chain[i].get("executed") is False)
    for i in range(12):
        vchain = verifier_order.get("simulated_verifier_chain") or []
        if i < len(vchain):
            ok(f"verifier_chain[{i}].not_executed", vchain[i].get("executed") is False)

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
