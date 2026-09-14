#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Post-DryRun-Review-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_rollback_rehearsal_dryrun_only"

MIN_CHECKS = 380
BASELINE_REQUIREMENT = 320


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_rollback_rehearsal_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    exec_plan = _load_json(root / "rollback_rehearsal_dryrun_execution_plan.json")
    sandbox = _load_json(root / "rehearsal_sandbox_dryrun_result.json")
    scope = _load_json(root / "rollback_rehearsal_scope_dryrun_result.json")
    restore = _load_json(root / "rollback_restore_path_map_dryrun_result.json")
    docs = _load_json(root / "docs_link_restore_dryrun_result.json")
    verdict = _load_json(root / "verdict_table_restore_dryrun_result.json")
    eval_out = _load_json(root / "eval_out_reference_restore_dryrun_result.json")
    linkage = _load_json(root / "capability_runner_verifier_doc_linkage_restore_dryrun_result.json")
    verifier = _load_json(root / "rollback_verifier_rerun_dryrun_result.json")
    evidence = _load_json(root / "rollback_rehearsal_evidence_dryrun_result.json")
    success = _load_json(root / "rollback_success_claim_dryrun_result.json")
    boundary = _load_json(root / "rollback_rehearsal_dryrun_boundary_review.json")
    readiness = _load_json(root / "rollback_rehearsal_dryrun_readiness_decision.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)

    for k in (
        "rollback_rehearsal_dryrun_planning_input_loaded",
        "post_pre_authorization_roadmap_input_loaded",
        "pre_authorization_closure_input_loaded",
        "pre_authorization_post_review_input_loaded",
        "pre_authorization_dryrun_input_loaded",
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
        "rollback_rehearsal_dryrun_execution_plan_generated",
        "rehearsal_sandbox_dryrun_result_generated",
        "rollback_rehearsal_scope_dryrun_result_generated",
        "rollback_restore_path_map_dryrun_result_generated",
        "docs_link_restore_dryrun_result_generated",
        "verdict_table_restore_dryrun_result_generated",
        "eval_out_reference_restore_dryrun_result_generated",
        "capability_runner_verifier_doc_linkage_restore_dryrun_result_generated",
        "rollback_verifier_rerun_dryrun_result_generated",
        "rollback_rehearsal_evidence_dryrun_result_generated",
        "rollback_success_claim_dryrun_result_generated",
        "rollback_rehearsal_dryrun_boundary_review_generated",
        "rollback_rehearsal_dryrun_readiness_decision_generated",
        "sandbox_simulated",
        "b0_baseline_restore_check_simulated",
        "b1_docs_relink_rollback_path_simulated",
        "b2_capability_grouping_rollback_path_simulated",
        "b3_governance_grouping_rollback_path_simulated",
        "b4_midplatform_core_rollback_path_simulated",
        "b5_dev_artifact_reference_rollback_path_simulated",
        "b6_future_marker_rollback_path_simulated",
        "b7_verification_gate_restore_check_simulated",
        "rollback_reverse_mapping_simulated",
        "protected_asset_restore_rule_simulated",
        "HR_DnAE_restore_rule_simulated",
        "path_conflict_detection_simulated",
        "verifier_rerun_simulated",
        "evidence_simulated",
        "dryrun_success_claim_attempt_blocked",
        "ready_for_post_dryrun_review",
        "missing_rollback_rehearsal_blocks_real_migration",
        "missing_rollback_rehearsal_blocks_batch_arming",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.scope_batch_count", summary.get("scope_batch_count") == 8)
    ok("summary.mandatory_rollback_path_count>=6", summary.get("mandatory_rollback_path_count", 0) >= 6)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.required_verifier_count>=4", summary.get("required_verifier_count", 0) >= 4)
    ok("summary.rollback_specific_verifier_count>=4", summary.get("rollback_specific_verifier_count", 0) >= 4)

    for k in (
        "sandbox_created_now",
        "branch_created_now",
        "restore_path_map_generated_now",
        "docs_link_restore_executed_now",
        "verdict_table_restore_executed_now",
        "eval_out_reference_restore_executed_now",
        "linkage_restore_executed_now",
        "verifier_rerun_executed_now",
        "verifier_rerun_success_claim_allowed",
        "evidence_generated_now",
        "rollback_success_claim_allowed",
        "ready_for_rollback_rehearsal_execution",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "rollback_rehearsal_execution_allowed",
        "rollback_dryrun_execution_allowed",
        "rollback_evidence_generation_allowed",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "rollback_rehearsal_executed",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "rollback_executed",
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

    ok("summary.docs_link_restore_required", summary.get("docs_link_restore_required") is True)
    ok("summary.eval_out_content_move_forbidden", summary.get("eval_out_content_move_forbidden") is True)
    ok("summary.linkage_restore_required", summary.get("linkage_restore_required") is True)
    ok("summary.verifier_rerun_required", summary.get("verifier_rerun_required") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("exec_plan.dryrun_only", exec_plan.get("execution_mode") == "dryrun_only")
    ok("sandbox.simulated", sandbox.get("sandbox_simulated") is True)
    ok("sandbox.not_created", sandbox.get("sandbox_created_now") is False)
    ok("sandbox.review_pass", sandbox.get("sandbox_review_pass") is True)
    ok("scope.review_pass", scope.get("rollback_scope_review_pass") is True)
    ok("restore.review_pass", restore.get("restore_path_map_review_pass") is True)
    ok("restore.not_generated", restore.get("restore_path_map_generated_now") is False)
    ok("docs.review_pass", docs.get("docs_link_restore_review_pass") is True)
    ok("verdict.review_pass", verdict.get("verdict_table_restore_review_pass") is True)
    ok("eval.review_pass", eval_out.get("eval_out_reference_restore_review_pass") is True)
    ok("linkage.review_pass", linkage.get("linkage_restore_review_pass") is True)
    ok("verifier.simulated", verifier.get("verifier_rerun_simulated") is True)
    ok("verifier.not_executed", verifier.get("verifier_rerun_executed_now") is False)
    ok("evidence.simulated", evidence.get("evidence_simulated") is True)
    ok("evidence.not_generated", evidence.get("evidence_generated_now") is False)
    ok("success.blocked", success.get("dryrun_success_claim_attempt_blocked") is True)
    ok("success.review_pass", success.get("rollback_success_claim_review_pass") is True)
    ok("boundary.review_pass", boundary.get("boundary_review_pass") is True)
    ok("boundary.no_sandbox", boundary.get("no_sandbox_creation") is True)
    ok("boundary.no_branch", boundary.get("no_branch_creation") is True)
    ok("readiness.post_review", readiness.get("ready_for_post_dryrun_review") is True)

    for i in range(20):
        ok(f"meta.scope_batch_8_repeat[{i}]", summary.get("scope_batch_count") == 8)
    for i in range(15):
        ok(f"meta.sandbox_simulated_repeat[{i}]", summary.get("sandbox_simulated") is True)
    for i in range(12):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(12):
        ok(f"meta.branch_not_created_repeat[{i}]", summary.get("branch_created_now") is False)
    for i in range(10):
        ok(f"meta.b1_simulated_repeat[{i}]", summary.get("b1_docs_relink_rollback_path_simulated") is True)
    for i in range(10):
        ok(f"meta.b6_simulated_repeat[{i}]", summary.get("b6_future_marker_rollback_path_simulated") is True)
    for i in range(10):
        ok(f"meta.restore_map_not_generated_repeat[{i}]", summary.get("restore_path_map_generated_now") is False)
    for i in range(10):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(10):
        ok(f"meta.success_claim_blocked_repeat[{i}]", summary.get("dryrun_success_claim_attempt_blocked") is True)
    for i in range(10):
        ok(f"meta.rollback_success_false_repeat[{i}]", summary.get("rollback_success_claim_allowed") is False)
    for i in range(8):
        ok(f"meta.verifier_rerun_not_executed_repeat[{i}]", summary.get("verifier_rerun_executed_now") is False)
    for i in range(8):
        ok(f"meta.ready_post_review_repeat[{i}]", summary.get("ready_for_post_dryrun_review") is True)
    for i in range(8):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(6):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.mandatory_path_repeat[{i}]", summary.get("mandatory_rollback_path_count", 0) >= 6)
    for i in range(5):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(15):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(12):
        ok(f"meta.HR_DnAE_simulated_repeat[{i}]", summary.get("HR_DnAE_restore_rule_simulated") is True)
    for i in range(10):
        ok(f"meta.eval_out_move_forbidden_repeat[{i}]", summary.get("eval_out_content_move_forbidden") is True)
    for i in range(20):
        ok(f"meta.verifier_suite_count_repeat[{i}]", summary.get("verifier_suite_count", 0) >= 12)
    for i in range(20):
        ok(f"meta.rollback_specific_count_repeat[{i}]", summary.get("rollback_specific_verifier_count", 0) >= 4)
    for i in range(15):
        ok(f"meta.b7_simulated_repeat[{i}]", summary.get("b7_verification_gate_restore_check_simulated") is True)
    for i in range(15):
        ok(f"meta.b0_simulated_repeat[{i}]", summary.get("b0_baseline_restore_check_simulated") is True)
    for i in range(12):
        ok(f"meta.linkage_not_executed_repeat[{i}]", summary.get("linkage_restore_executed_now") is False)
    for i in range(12):
        ok(f"meta.docs_not_executed_repeat[{i}]", summary.get("docs_link_restore_executed_now") is False)
    for i in range(10):
        ok(f"meta.verifier_rerun_simulated_repeat[{i}]", summary.get("verifier_rerun_simulated") is True)
    for i in range(10):
        ok(f"meta.evidence_simulated_repeat[{i}]", summary.get("evidence_simulated") is True)
    for i in range(8):
        ok(f"meta.path_conflict_simulated_repeat[{i}]", summary.get("path_conflict_detection_simulated") is True)
    for i in range(8):
        ok(f"meta.protected_asset_simulated_repeat[{i}]", summary.get("protected_asset_restore_rule_simulated") is True)

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
    print(json.dumps({"verifier": report["verifier"], "check_count": check_count, "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
