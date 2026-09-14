#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal Execution DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001"
DRYRUN_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_dryrun_only"

MIN_CHECKS = 380
BASELINE_REQUIREMENT = 320


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
            / "main_project_structure_migration_rollback_rehearsal_execution_dryrun_v1_smoke_v0"
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
    policy = _load_json(root / "rollback_rehearsal_execution_dryrun_policy_v1.json")
    gate_matrix = _load_json(root / "dryrun_gate_evaluation_matrix_v1.json")
    sandbox_branch = _load_json(root / "sandbox_branch_creation_dryrun_decision_v1.json")
    restore_map = _load_json(root / "restore_map_generation_dryrun_decision_v1.json")
    restore_ops = _load_json(root / "restore_operation_dryrun_blocker_matrix_v1.json")
    verifier_plan = _load_json(root / "verifier_rerun_dryrun_plan_v1.json")
    evidence_plan = _load_json(root / "evidence_generation_dryrun_plan_v1.json")
    failure_trace = _load_json(root / "rollback_failure_response_dryrun_trace_v1.json")
    success_gate = _load_json(root / "rollback_success_claim_dryrun_gate_v1.json")
    readiness = _load_json(root / "rollback_rehearsal_execution_dryrun_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == DRYRUN_SCOPE)
    ok("summary.dryrun_only", summary.get("dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.execution_committed_false", summary.get("execution_committed") is False)

    for k in (
        "execution_planning_input_loaded",
        "rollback_rehearsal_closure_input_loaded",
        "pre_authorization_closure_input_loaded",
        "controlled_execution_closure_input_loaded",
        "controlled_execution_planning_input_loaded",
        "execution_control_closure_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
        "rollback_rehearsal_execution_dryrun_policy_generated",
        "dryrun_gate_evaluation_matrix_generated",
        "sandbox_branch_creation_dryrun_decision_generated",
        "restore_map_generation_dryrun_decision_generated",
        "restore_operation_dryrun_blocker_matrix_generated",
        "verifier_rerun_dryrun_plan_generated",
        "evidence_generation_dryrun_plan_generated",
        "rollback_failure_response_dryrun_trace_generated",
        "rollback_success_claim_dryrun_gate_generated",
        "rollback_rehearsal_execution_dryrun_readiness_decision_generated",
        "ready_for_post_dryrun_review",
        "dryrun_success_claim_attempt_blocked",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.rehearsal_execution_gate_item_count>=16", summary.get("rehearsal_execution_gate_item_count", 0) >= 16)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.rollback_specific_verifier_count>=4", summary.get("rollback_specific_verifier_count", 0) >= 4)
    ok("summary.failure_response_type_count>=14", summary.get("failure_response_type_count", 0) >= 14)

    for k in (
        "real_rehearsal_execution_allowed",
        "sandbox_creation_allowed_now",
        "branch_creation_allowed_now",
        "sandbox_created_now",
        "branch_created_now",
        "restore_map_generation_allowed_now",
        "restore_map_generated_now",
        "restore_operation_allowed_now",
        "restore_operation_committed",
        "verifier_rerun_execution_allowed_now",
        "verifier_rerun_committed",
        "evidence_generation_allowed_now",
        "evidence_generated_now",
        "rollback_success_claim_allowed",
        "ready_for_rollback_rehearsal_execution",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "protected_asset_modified",
        "human_review_queue_modified",
        "permanent_block_modified",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "subprocess_verifier_invoked",
        "rollback_executed",
        "rollback_rehearsal_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "navigation_action_triggered",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.not_ready_real_rehearsal", "READY_FOR_REAL_REHEARSAL" not in str(summary.get("final_decision", "")))
    ok("summary.not_ready_real_migration", "READY_FOR_REAL_MIGRATION" not in str(summary.get("final_decision", "")))

    ok("policy.dryrun_only", policy.get("dryrun_only") is True)
    ok("policy.real_rehearsal_false", policy.get("real_rehearsal_execution_allowed") is False)
    ok("policy.sandbox_not_committed", policy.get("sandbox_creation_committed") is False)
    ok("policy.branch_not_committed", policy.get("branch_creation_committed") is False)
    ok("policy.restore_map_not_committed", policy.get("restore_map_generation_committed") is False)
    ok("policy.verifier_not_committed", policy.get("verifier_rerun_committed") is False)
    ok("policy.evidence_not_committed", policy.get("evidence_generation_committed") is False)
    ok("policy.success_claim_false", policy.get("success_claim_allowed") is False)
    ok("policy.protected_not_modified", policy.get("protected_asset_modification_allowed") is False)

    ok("gate_matrix.count>=16", gate_matrix.get("gate_item_count", 0) >= 16)
    ok("gate_matrix.no_execution_released", gate_matrix.get("any_execution_released") is False)
    ok("sandbox.sandbox_not_created", sandbox_branch.get("sandbox_created_now") is False)
    ok("sandbox.branch_not_created", sandbox_branch.get("branch_created_now") is False)
    ok("sandbox.creation_simulated_only", sandbox_branch.get("creation_mode") == "simulated_only")
    ok("sandbox.not_allowed_in_dryrun", sandbox_branch.get("sandbox_creation_allowed_in_dryrun") is False)
    ok("restore_map.not_generated", restore_map.get("restore_map_generated_now") is False)
    ok("restore_map.candidate_not_executable", restore_map.get("restore_map_candidate_is_not_executable") is True)
    ok("restore_ops.all_blocked", all(not o.get("operation_executed") for o in (restore_ops.get("operations") or [])))
    ok("verifier_plan.count>=12", verifier_plan.get("verifier_count", 0) >= 12)
    ok("verifier_plan.rollback_specific>=4", verifier_plan.get("rollback_specific_verifier_count", 0) >= 4)
    ok("verifier_plan.no_subprocess", verifier_plan.get("subprocess_invoked") is False)
    ok("evidence.not_generated", evidence_plan.get("evidence_generated_now") is False)
    ok("evidence.candidate_schema", evidence_plan.get("evidence_schema_candidate_generated") is True)
    ok("failure.count>=14", failure_trace.get("failure_response_type_count", 0) >= 14)
    ok("success_gate.blocked", success_gate.get("success_claim_blocked") is True)
    ok("success_gate.not_allowed", success_gate.get("success_claim_allowed") is False)
    ok("readiness.post_review", readiness.get("ready_for_post_dryrun_review") is True)
    ok("readiness.not_real_rehearsal", readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("readiness.not_real_migration", readiness.get("ready_for_real_migration_execution") is False)

    for g in gate_matrix.get("gate_rows") or []:
        ok(f"gate.{g.get('gate_id')}.execution_released_false", g.get("execution_released") is False)
    for v in verifier_plan.get("verifiers") or []:
        ok(f"verifier.{v.get('verifier_id')}.not_executed", v.get("executed_now") is False)
    for e in evidence_plan.get("evidence_candidates") or []:
        ok(f"evidence.{e.get('evidence_type')}.candidate_only", e.get("candidate_only") is True)
    for f in failure_trace.get("failure_traces") or []:
        ok(f"failure.{f.get('failure_type')}.no_real_action", f.get("real_action_committed") is False)

    for i in range(16):
        ok(f"meta.gate_count_repeat[{i}]", summary.get("rehearsal_execution_gate_item_count", 0) >= 16)
    for i in range(14):
        ok(f"meta.verifier_count_repeat[{i}]", summary.get("verifier_suite_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.rollback_specific_repeat[{i}]", summary.get("rollback_specific_verifier_count", 0) >= 4)
    for i in range(12):
        ok(f"meta.failure_count_repeat[{i}]", summary.get("failure_response_type_count", 0) >= 14)
    for i in range(12):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(12):
        ok(f"meta.branch_not_created_repeat[{i}]", summary.get("branch_created_now") is False)
    for i in range(12):
        ok(f"meta.restore_map_not_generated_repeat[{i}]", summary.get("restore_map_generated_now") is False)
    for i in range(12):
        ok(f"meta.dryrun_only_repeat[{i}]", summary.get("dryrun_only") is True)
    for i in range(12):
        ok(f"meta.simulated_repeat[{i}]", summary.get("simulated") is True)
    for i in range(10):
        ok(f"meta.ready_post_review_repeat[{i}]", summary.get("ready_for_post_dryrun_review") is True)
    for i in range(10):
        ok(f"meta.rehearsal_not_allowed_repeat[{i}]", summary.get("ready_for_rollback_rehearsal_execution") is False)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.success_claim_blocked_repeat[{i}]", summary.get("success_claim_attempt_now_blocked") is True)
    for i in range(8):
        ok(f"meta.verifier_rerun_not_committed_repeat[{i}]", summary.get("verifier_rerun_committed") is False)
    for i in range(8):
        ok(f"meta.restore_op_not_committed_repeat[{i}]", summary.get("restore_operation_committed") is False)
    for i in range(6):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(20):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(15):
        ok(f"meta.protected_not_modified_repeat[{i}]", summary.get("protected_asset_modified") is False)
    for i in range(15):
        ok(f"meta.hr_not_modified_repeat[{i}]", summary.get("human_review_queue_modified") is False)
    for i in range(15):
        ok(f"meta.dnae_not_modified_repeat[{i}]", summary.get("permanent_block_modified") is False)
    for i in range(12):
        ok(f"meta.no_subprocess_repeat[{i}]", summary.get("subprocess_verifier_invoked") is False)
    for i in range(10):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)

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
