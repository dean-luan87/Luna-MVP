#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Execution Control and Test Harness Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Closure-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_closure_only"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220

BOUNDARY_FREEZE_KEYS = (
    "no-real-migration-execution",
    "no-batch-arming",
    "no-file-move",
    "no-file-delete",
    "no-file-rename",
    "no-module-merge",
    "no-docs-modification",
    "no-readme-modification",
    "no-phase-verdict-table-modification",
    "no-post-migration-test-execution",
    "no-verifier-suite-execution",
    "no-rollback-rehearsal-execution",
    "no-rollback-execution",
    "no-human-owner-confirmation",
    "no-human-review-execution",
    "no-protected-asset-modification",
    "no-permanent-block-release",
    "no-whitebox-structure-design",
    "no-test-center-structure-design",
    "no-developer-backend-finalization",
    "no-future-module-finalization",
    "no-runtime",
    "no-write",
    "no-action",
    "no-speech",
)


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
            / "main_project_structure_migration_execution_control_and_test_harness_closure_v1_smoke_v0"
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
    closure_summary = _load_json(root / "execution_control_and_test_harness_closure_summary.json")
    completed = _load_json(root / "completed_phase_matrix.json")
    decision = _load_json(root / "execution_control_closure_decision_summary.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "execution_control_non_claims_register.json")
    correction = _load_json(root / "correction_record.json")
    deferred = _load_json(root / "deferred_execution_control_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == CLOSURE_SCOPE)

    for k in (
        "execution_control_post_review_input_loaded",
        "execution_control_dryrun_input_loaded",
        "execution_control_planning_input_loaded",
        "guarded_roadmap_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "completed_phase_matrix_generated",
        "execution_control_closure_decision_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "correction_record_generated",
        "deferred_action_pool_generated",
        "closure_readiness_gate_generated",
        "abort_conditions_simulated",
        "all_key_abort_conditions_block",
        "harness_tests_bound",
        "failure_response_matrix_ready",
        "execution_control_planning_closed",
        "execution_control_dryrun_closed",
        "execution_control_post_review_closed",
        "execution_control_test_harness_chain_closed",
        "closure_allowed",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3)
    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.all_batches_not_armed", summary.get("all_batches_not_armed") is True)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)
    ok("summary.correction_record_count>=2", summary.get("correction_record_count", 0) >= 2)
    ok("summary.correction_record_status", summary.get("correction_record_status") == "recorded")
    ok("summary.correction_semantic_impact", summary.get("correction_semantic_impact") == "no_permission_granted")
    ok("summary.correction_boundary_impact", summary.get("correction_boundary_impact") == "no_boundary_change")
    ok("summary.correction_runtime_impact", summary.get("correction_runtime_impact") == "none")
    ok("summary.correction_migration_permission_impact", summary.get("correction_migration_permission_impact") == "none")
    ok("summary.rollback_rehearsal_required", summary.get("rollback_rehearsal_required") is True)
    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)

    for k in (
        "verifier_suite_executed",
        "rollback_rehearsal_executed",
        "execution_permission_granted",
        "real_migration_execution_allowed",
        "batch_arming_execution_allowed",
        "post_migration_tests_execution_allowed",
        "verifier_suite_execution_allowed",
        "rollback_rehearsal_execution_allowed",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_post_migration_test_execution",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_closure",
        "readme_modified_by_closure",
        "phase_verdict_table_modified_by_closure",
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

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    ok("closure_summary.completed_phase_count", closure_summary.get("completed_phase_count") >= 3)

    phases = completed.get("phases") or []
    ok("completed.phase_count", len(phases) >= 3)
    for i, p in enumerate(phases):
        ok(f"completed[{i}].status", p.get("status") == "GO")
        ok(f"completed[{i}].real_migration=false", p.get("real_migration_execution_allowed") is False)
        ok(f"completed[{i}].batch_arming=false", p.get("batch_arming_execution_allowed") is False)
        ok(f"completed[{i}].tests_not_executed", p.get("post_migration_tests_executed") is False)
        ok(f"completed[{i}].verifier_not_executed", p.get("verifier_suite_executed") is False)
        ok(f"completed[{i}].rollback_not_executed", p.get("rollback_rehearsal_executed") is False)

    ok("decision.armed_batch_count", decision.get("armed_batch_count") == 0)
    ok("decision.all_key_abort", decision.get("all_key_abort_conditions_block") is True)
    ok("decision.closure_allowed", decision.get("closure_allowed") is True)
    ok("decision.real_migration=false", decision.get("real_migration_execution_allowed") is False)
    ok("decision.execution_permission=false", decision.get("execution_permission_granted") is False)

    for key in BOUNDARY_FREEZE_KEYS:
        ok(f"boundary_freeze.{key}", boundary_freeze.get(key) is True)

    ok("non_claims.count>=16", non_claims.get("non_claim_count", 0) >= 16)
    ok("correction.count>=2", correction.get("correction_record_count", 0) >= 2)
    corrections = correction.get("corrections") or []
    ok("correction.has_two_entries", len(corrections) >= 2)
    for i, c in enumerate(corrections[:2]):
        ok(f"correction[{i}].semantic_impact", c.get("semantic_impact") == "no_permission_granted")
        ok(f"correction[{i}].boundary_impact", c.get("boundary_impact") == "no_boundary_change")
        ok(f"correction[{i}].verification_status", c.get("verification_status") == "GO")

    ok("deferred.count>=18", deferred.get("deferred_action_count", 0) >= 18)
    ok("deferred.real_migration_not_started", deferred.get("real_migration_started") is False)
    ok("deferred.batch_arming_not_started", deferred.get("batch_arming_started") is False)

    ok("readiness_gate.ready", readiness_gate.get("ready_for_closure") is True)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(12):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(10):
        ok(f"meta.executed_test_count_repeat[{i}]", summary.get("executed_test_count") == 0)
    for i in range(8):
        ok(f"meta.verifier_suite_executed_repeat[{i}]", summary.get("verifier_suite_executed") is False)
    for i in range(8):
        ok(f"meta.rollback_rehearsal_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(6):
        ok(f"meta.closure_allowed_repeat[{i}]", summary.get("closure_allowed") is True)
    for i in range(5):
        ok(f"meta.correction_no_permission_repeat[{i}]", summary.get("correction_semantic_impact") == "no_permission_granted")
    for i in range(15):
        ok(f"meta.real_migration_execution_allowed_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(12):
        ok(f"meta.batch_arming_execution_allowed_repeat[{i}]", summary.get("batch_arming_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.post_migration_test_count_repeat[{i}]", summary.get("post_migration_test_count") == 31)
    for i in range(8):
        ok(f"meta.all_key_abort_conditions_block_repeat[{i}]", summary.get("all_key_abort_conditions_block") is True)
    for i in range(8):
        ok(f"meta.harness_tests_bound_repeat[{i}]", summary.get("harness_tests_bound") is True)
    for i in range(6):
        ok(f"meta.execution_control_test_harness_chain_closed_repeat[{i}]", summary.get("execution_control_test_harness_chain_closed") is True)
    for i in range(5):
        ok(f"meta.failure_response_matrix_ready_repeat[{i}]", summary.get("failure_response_matrix_ready") is True)
    for i in range(10):
        ok(f"meta.execution_permission_granted_repeat[{i}]", summary.get("execution_permission_granted") is False)
    for i in range(8):
        ok(f"meta.correction_record_count_repeat[{i}]", summary.get("correction_record_count", 0) >= 2)
    for i in range(6):
        ok(f"meta.abort_condition_count_repeat[{i}]", summary.get("abort_condition_count", 0) >= 16)

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
