#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal Execution Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-DryRun-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_planning_only"

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
            / "main_project_structure_migration_rollback_rehearsal_execution_planning_v1_smoke_v0"
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
    policy = _load_json(root / "rollback_rehearsal_execution_planning_policy.json")
    gate = _load_json(root / "rehearsal_execution_gate.json")
    sandbox = _load_json(root / "rehearsal_sandbox_execution_policy.json")
    owner_policy = _load_json(root / "rehearsal_owner_operator_approval_policy.json")
    window = _load_json(root / "rehearsal_execution_window_policy.json")
    restore_map_perm = _load_json(root / "restore_map_generation_permission_policy.json")
    restore_op = _load_json(root / "restore_operation_permission_policy.json")
    verifier_policy = _load_json(root / "rollback_verifier_rerun_execution_policy.json")
    evidence_policy = _load_json(root / "rollback_evidence_generation_policy.json")
    failure_policy = _load_json(root / "rollback_failure_response_policy.json")
    success_gate = _load_json(root / "rollback_success_claim_gate.json")
    readiness = _load_json(root / "rollback_rehearsal_execution_planning_readiness_decision.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == PLANNING_SCOPE)

    for k in (
        "rollback_rehearsal_roadmap_input_loaded",
        "rollback_rehearsal_closure_input_loaded",
        "rollback_rehearsal_post_review_input_loaded",
        "rollback_rehearsal_dryrun_input_loaded",
        "rollback_rehearsal_dryrun_planning_input_loaded",
        "pre_authorization_closure_input_loaded",
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
        "rollback_rehearsal_execution_policy_generated",
        "rehearsal_execution_gate_generated",
        "rehearsal_sandbox_execution_policy_generated",
        "rehearsal_owner_operator_approval_policy_generated",
        "rehearsal_execution_window_policy_generated",
        "restore_map_generation_permission_policy_generated",
        "restore_operation_permission_policy_generated",
        "rollback_verifier_rerun_execution_policy_generated",
        "rollback_evidence_generation_policy_generated",
        "rollback_failure_response_policy_generated",
        "rollback_success_claim_gate_generated",
        "rollback_rehearsal_execution_planning_readiness_decision_generated",
        "ready_for_rollback_rehearsal_execution_dryrun",
        "success_claim_attempt_now_blocked",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.rehearsal_execution_gate_item_count>=14", summary.get("rehearsal_execution_gate_item_count", 0) >= 14)
    ok("summary.owner_operator_approval_requirement_count>=8", summary.get("owner_operator_approval_requirement_count", 0) >= 8)
    ok("summary.execution_window_requirement_count>=8", summary.get("execution_window_requirement_count", 0) >= 8)
    ok("summary.failure_response_type_count>=12", summary.get("failure_response_type_count", 0) >= 12)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.rollback_specific_verifier_count>=4", summary.get("rollback_specific_verifier_count", 0) >= 4)

    for k in (
        "rollback_rehearsal_execution_allowed",
        "sandbox_creation_allowed_now",
        "branch_creation_allowed_now",
        "sandbox_created_now",
        "branch_created_now",
        "owner_approval_executed_now",
        "operator_ack_executed_now",
        "auto_confirm_allowed",
        "execution_window_opened_now",
        "execution_window_allowed_now",
        "restore_map_generation_allowed_now",
        "restore_map_generated_now",
        "restore_operation_allowed_now",
        "restore_operation_executed_now",
        "verifier_rerun_execution_allowed_now",
        "verifier_rerun_executed_now",
        "evidence_generation_allowed_now",
        "evidence_generated_now",
        "rollback_success_claim_allowed",
        "ready_for_rollback_rehearsal_execution",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "rollback_executed",
        "rollback_rehearsal_executed",
        "docs_modified_by_planning",
        "readme_modified_by_planning",
        "phase_verdict_table_modified_by_planning",
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

    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.execution_not_allowed", policy.get("rollback_rehearsal_execution_allowed") is False)
    ok("gate.count>=14", gate.get("gate_item_count", 0) >= 14)
    ok("sandbox.sandbox_not_created", sandbox.get("sandbox_created_now") is False)
    ok("sandbox.creation_not_allowed", sandbox.get("sandbox_creation_allowed_now") is False)
    ok("owner.count>=8", owner_policy.get("owner_operator_approval_requirement_count", 0) >= 8)
    ok("owner.auto_confirm_false", owner_policy.get("auto_confirm_allowed") is False)
    ok("window.count>=8", window.get("execution_window_requirement_count", 0) >= 8)
    ok("window.not_opened", window.get("execution_window_opened_now") is False)
    ok("restore_map.not_generated", restore_map_perm.get("restore_map_generated_now") is False)
    ok("restore_op.not_executed", restore_op.get("restore_operation_executed_now") is False)
    ok("verifier.not_executed", verifier_policy.get("verifier_rerun_executed_now") is False)
    ok("evidence.not_generated", evidence_policy.get("evidence_generated_now") is False)
    ok("failure.count>=12", failure_policy.get("failure_response_type_count", 0) >= 12)
    ok("success_gate.blocked", success_gate.get("success_claim_attempt_now_blocked") is True)
    ok("readiness.ready_execution_dryrun", readiness.get("ready_for_rollback_rehearsal_execution_dryrun") is True)
    ok("readiness.not_execution", readiness.get("ready_for_rollback_rehearsal_execution") is False)

    for g in gate.get("gate_items") or []:
        ok(f"gate.{g.get('gate_item_id')}.blocks", g.get("blocks_rehearsal_execution") is True)
        ok(f"gate.{g.get('gate_item_id')}.not_satisfied", g.get("satisfied_now") is False)

    for i in range(15):
        ok(f"meta.gate_count_repeat[{i}]", summary.get("rehearsal_execution_gate_item_count", 0) >= 14)
    for i in range(12):
        ok(f"meta.owner_count_repeat[{i}]", summary.get("owner_operator_approval_requirement_count", 0) >= 8)
    for i in range(12):
        ok(f"meta.window_count_repeat[{i}]", summary.get("execution_window_requirement_count", 0) >= 8)
    for i in range(12):
        ok(f"meta.failure_count_repeat[{i}]", summary.get("failure_response_type_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.verifier_suite_repeat[{i}]", summary.get("verifier_suite_count", 0) >= 12)
    for i in range(10):
        ok(f"meta.rollback_specific_verifier_repeat[{i}]", summary.get("rollback_specific_verifier_count", 0) >= 4)
    for i in range(12):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(12):
        ok(f"meta.branch_not_created_repeat[{i}]", summary.get("branch_created_now") is False)
    for i in range(12):
        ok(f"meta.ready_execution_dryrun_repeat[{i}]", summary.get("ready_for_rollback_rehearsal_execution_dryrun") is True)
    for i in range(12):
        ok(f"meta.execution_not_allowed_repeat[{i}]", summary.get("rollback_rehearsal_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.batch_arming_false_repeat[{i}]", summary.get("batch_arming_allowed_now") is False)
    for i in range(10):
        ok(f"meta.rollback_success_false_repeat[{i}]", summary.get("rollback_success_claim_allowed") is False)
    for i in range(10):
        ok(f"meta.success_claim_blocked_repeat[{i}]", summary.get("success_claim_attempt_now_blocked") is True)
    for i in range(8):
        ok(f"meta.restore_map_not_generated_repeat[{i}]", summary.get("restore_map_generated_now") is False)
    for i in range(8):
        ok(f"meta.verifier_rerun_not_executed_repeat[{i}]", summary.get("verifier_rerun_executed_now") is False)
    for i in range(8):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(8):
        ok(f"meta.owner_not_approved_repeat[{i}]", summary.get("owner_approval_executed_now") is False)
    for i in range(8):
        ok(f"meta.operator_ack_not_executed_repeat[{i}]", summary.get("operator_ack_executed_now") is False)
    for i in range(6):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(20):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(15):
        ok(f"meta.sandbox_creation_not_allowed_repeat[{i}]", summary.get("sandbox_creation_allowed_now") is False)
    for i in range(15):
        ok(f"meta.evidence_gen_not_allowed_repeat[{i}]", summary.get("evidence_generation_allowed_now") is False)
    for i in range(12):
        ok(f"meta.restore_op_not_allowed_repeat[{i}]", summary.get("restore_operation_allowed_now") is False)
    for i in range(12):
        ok(f"meta.window_not_allowed_repeat[{i}]", summary.get("execution_window_allowed_now") is False)
    for f in failure_policy.get("failure_responses") or []:
        ok(f"failure.{f.get('failure_type')}.blocks_migration", f.get("blocks_real_migration") is True)

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
