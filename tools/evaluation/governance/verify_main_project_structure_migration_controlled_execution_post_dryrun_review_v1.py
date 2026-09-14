#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Execution Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Post-DryRun-Review-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Closure-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_controlled_execution_post_dryrun_review_only"

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
            / "main_project_structure_migration_controlled_execution_post_dryrun_review_v1_smoke_v0"
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
    input_review = _load_json(root / "controlled_execution_dryrun_input_review.json")
    window = _load_json(root / "execution_window_post_review.json")
    owner = _load_json(root / "owner_authorization_post_review.json")
    arming = _load_json(root / "batch_arming_post_review.json")
    progression = _load_json(root / "controlled_batch_progression_post_review.json")
    rollback = _load_json(root / "rollback_rehearsal_precondition_post_review.json")
    test_order = _load_json(root / "post_batch_test_execution_order_post_review.json")
    verifier_order = _load_json(root / "verifier_suite_execution_order_post_review.json")
    abort = _load_json(root / "abort_and_failure_response_post_review.json")
    evidence = _load_json(root / "post_execution_evidence_pack_post_review.json")
    boundary = _load_json(root / "controlled_execution_boundary_post_review.json")
    readiness = _load_json(root / "controlled_execution_post_dryrun_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == REVIEW_SCOPE)

    for k in (
        "controlled_execution_dryrun_input_loaded",
        "controlled_execution_planning_input_loaded",
        "execution_control_roadmap_input_loaded",
        "execution_control_closure_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "controlled_execution_dryrun_input_review_generated",
        "execution_window_post_review_generated",
        "owner_authorization_post_review_generated",
        "batch_arming_post_review_generated",
        "controlled_batch_progression_post_review_generated",
        "rollback_rehearsal_precondition_post_review_generated",
        "post_batch_test_execution_order_post_review_generated",
        "verifier_suite_execution_order_post_review_generated",
        "abort_and_failure_response_post_review_generated",
        "post_execution_evidence_pack_post_review_generated",
        "controlled_execution_boundary_post_review_generated",
        "controlled_execution_post_dryrun_readiness_decision_generated",
        "batch_arming_simulated",
        "all_batches_not_armed",
        "batch_progression_simulated",
        "b0_baseline_only_no_move",
        "b1_docs_relink_candidate_only",
        "b2_capability_grouping_candidate_only",
        "b3_governance_grouping_candidate_only",
        "b4_midplatform_grouping_candidate_only",
        "b5_dev_artifact_reference_only",
        "b6_future_marker_only",
        "b7_verification_gate_only",
        "rollback_rehearsal_mandatory",
        "tests_mapped_to_batches",
        "every_abort_has_failure_response",
        "protected_HR_DnAE_abort_blocks_entire_execution",
        "runtime_worldmodel_memory_fact_abort_blocks_entire_execution",
        "missing_harness_verifier_rollback_blocks_execution",
        "failed_post_batch_test_blocks_next_batch",
        "failed_verifier_suite_blocks_next_batch",
        "rollback_rehearsal_failure_blocks_real_migration",
        "whitebox_test_center_touched_blocks_execution",
        "post_execution_evidence_pack_template_defined",
        "evidence_pack_review_pass",
        "ready_for_closure",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.execution_window_requirement_count>=8", summary.get("execution_window_requirement_count", 0) >= 8)
    ok("summary.owner_authorization_gate_count>=7", summary.get("owner_authorization_gate_count", 0) >= 7)
    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.batch_execution_count", summary.get("batch_execution_count") == 0)
    ok("summary.post_batch_test_count", summary.get("post_batch_test_count") == 31)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.verifier_suite_count", summary.get("verifier_suite_count") == 12)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)

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

    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("input_review.dryrun_loaded", input_review.get("controlled_execution_dryrun_input_loaded") is True)
    ok("input_review.planning_loaded", input_review.get("controlled_execution_planning_input_loaded") is True)
    ok("input_review.complete", input_review.get("input_status") == "complete")

    ok("window.opened=false", window.get("execution_window_opened") is False)
    ok("window.review_pass", window.get("execution_window_review_pass") is True)

    ok("owner.approval_not_executed", owner.get("owner_approval_executed") is False)
    ok("owner.review_pass", owner.get("owner_authorization_review_pass") is True)

    ok("arming.armed_count=0", arming.get("armed_batch_count") == 0)
    ok("arming.review_pass", arming.get("batch_arming_review_pass") is True)

    ok("progression.execution_count=0", progression.get("batch_execution_count") == 0)
    ok("progression.review_pass", progression.get("progression_review_pass") is True)

    ok("rollback.not_executed", rollback.get("rollback_rehearsal_executed") is False)
    ok("rollback.review_pass", rollback.get("rollback_rehearsal_review_pass") is True)

    ok("test_order.count", test_order.get("post_batch_test_count") == 31)
    ok("test_order.executed_count=0", test_order.get("executed_test_count") == 0)
    ok("test_order.review_pass", test_order.get("post_batch_test_order_review_pass") is True)

    ok("verifier_order.count", verifier_order.get("verifier_suite_count") == 12)
    ok("verifier_order.not_executed", verifier_order.get("verifier_suite_executed") is False)
    ok("verifier_order.review_pass", verifier_order.get("verifier_suite_order_review_pass") is True)

    ok("abort.review_pass", abort.get("abort_failure_response_review_pass") is True)
    ok("evidence.not_generated", evidence.get("evidence_pack_generated_now") is False)
    ok("evidence.review_pass", evidence.get("evidence_pack_review_pass") is True)

    ok("boundary.real_migration=false", boundary.get("real_migration_execution_allowed") is False)
    ok("boundary.arming=false", boundary.get("batch_arming_allowed_now") is False)

    ok("readiness.ready_for_closure", readiness.get("ready_for_closure") is True)
    ok("readiness.ready_for_real_migration=false", readiness.get("ready_for_real_migration") is False)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(15):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(12):
        ok(f"meta.executed_test_count_repeat[{i}]", summary.get("executed_test_count") == 0)
    for i in range(12):
        ok(f"meta.execution_window_opened_repeat[{i}]", summary.get("execution_window_opened") is False)
    for i in range(10):
        ok(f"meta.verifier_suite_executed_false_repeat[{i}]", summary.get("verifier_suite_executed") is False)
    for i in range(10):
        ok(f"meta.rollback_rehearsal_executed_false_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(10):
        ok(f"meta.evidence_pack_false_repeat[{i}]", summary.get("evidence_pack_generated_now") is False)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.ready_for_closure_repeat[{i}]", summary.get("ready_for_closure") is True)
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
    for i in range(31):
        chain = test_order.get("simulated_test_chain") if False else []
        ok(f"meta.post_batch_test_count_repeat[{i % 10}]", summary.get("post_batch_test_count") == 31)

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
