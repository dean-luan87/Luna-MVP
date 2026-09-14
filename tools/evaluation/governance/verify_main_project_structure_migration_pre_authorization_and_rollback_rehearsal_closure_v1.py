#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Closure-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Pre-Authorization-and-Rollback-Rehearsal-Roadmap-Decision-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_only"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


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
            / "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_closure_v1_smoke_v0"
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
    closure_summary = _load_json(root / "pre_authorization_rollback_closure_summary.json")
    phase_matrix = _load_json(root / "completed_phase_matrix.json")
    decision = _load_json(root / "pre_authorization_closure_decision_summary.json")
    gap_closure = _load_json(root / "gap_hard_block_closure_summary.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "pre_authorization_non_claims_register.json")
    semantic = _load_json(root / "semantic_clarification_record.json")
    deferred = _load_json(root / "deferred_pre_authorization_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == CLOSURE_SCOPE)

    for k in (
        "pre_authorization_post_review_input_loaded",
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
        "completed_phase_matrix_generated",
        "pre_authorization_closure_decision_summary_generated",
        "gap_hard_block_closure_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "semantic_clarification_record_generated",
        "deferred_action_pool_generated",
        "closure_readiness_gate_generated",
        "owner_authorization_simulated",
        "operator_ack_simulated",
        "rehearsal_steps_simulated",
        "blockers_simulated",
        "package_template_loaded",
        "rollback_evidence_template_loaded",
        "all_batches_not_armed",
        "gap_hard_block_matrix_reviewed",
        "pre_authorization_planning_closed",
        "pre_authorization_dryrun_closed",
        "pre_authorization_post_review_closed",
        "pre_authorization_rollback_rehearsal_chain_closed",
        "closure_allowed",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3)
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
        "rehearsal_execution_allowed_now",
        "rehearsal_executed_now",
        "rollback_evidence_generated_now",
        "rollback_success_claim_allowed",
        "arming_record_generated_now",
        "arming_allowed_now",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.auto_confirm_allowed=false", summary.get("auto_confirm_allowed") is False)
    ok("summary.semantic_clarification_status", summary.get("semantic_clarification_status") == "recorded")
    ok("summary.semantic_clarification_impact", summary.get("semantic_clarification_impact") == "no_permission_granted")
    ok("summary.semantic_clarification_boundary_impact", summary.get("semantic_clarification_boundary_impact") == "no_boundary_change")
    ok("summary.semantic_clarification_runtime_impact", summary.get("semantic_clarification_runtime_impact") == "none")
    ok("summary.semantic_clarification_migration_permission_impact", summary.get("semantic_clarification_migration_permission_impact") == "none")
    ok("summary.semantic_clarification_rollback_permission_impact", summary.get("semantic_clarification_rollback_permission_impact") == "none")

    for k in (
        "missing_owner_blocks_execution",
        "missing_owner_blocks_batch_arming",
        "missing_operator_ack_blocks_execution",
        "missing_operator_ack_blocks_batch_arming",
        "missing_package_blocks_real_migration",
        "missing_owner_blocks_real_migration",
        "missing_owner_blocks_batch_arming",
        "missing_operator_ack_blocks_real_migration",
        "missing_operator_ack_blocks_batch_arming",
        "missing_rollback_rehearsal_blocks_real_migration",
        "missing_rollback_rehearsal_blocks_batch_arming",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("gap_closure.pass", gap_closure.get("gap_hard_block_closure_pass") is True)
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    ok("phase_matrix.count>=3", phase_matrix.get("completed_phase_count", 0) >= 3)
    ok("semantic.recorded", semantic.get("semantic_clarification_status") == "recorded")
    ok("readiness.ready_for_closure", readiness_gate.get("ready_for_closure") is True)
    ok("boundary_freeze.no_migration", boundary_freeze.get("no-real-migration-execution") is True)
    ok("boundary_freeze.no_rollback_success_claim", boundary_freeze.get("no-rollback-success-claim") is True)
    ok("non_claims.count>=10", non_claims.get("non_claim_count", 0) >= 10)

    for p in phase_matrix.get("phases") or []:
        ok(f"phase.{p.get('phase_id')}.no_owner", p.get("owner_confirmed_now") is False)
        ok(f"phase.{p.get('phase_id')}.no_armed", p.get("batch_arming_allowed_now") is False)

    for i in range(12):
        ok(f"meta.chain_closed_repeat[{i}]", summary.get("pre_authorization_rollback_rehearsal_chain_closed") is True)
    for i in range(10):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(8):
        ok(f"meta.gap_owner_migration_repeat[{i}]", summary.get("missing_owner_blocks_real_migration") is True)
    for i in range(6):
        ok(f"meta.semantic_no_permission_repeat[{i}]", summary.get("semantic_clarification_impact") == "no_permission_granted")

    for k in (
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_rollback_rehearsal_execution",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "docs_modified_by_closure",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
        "world_model_written",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.no_new_runtime_enabled=true", summary.get("no_new_runtime_enabled") is True)

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

    for i in range(20):
        ok(f"meta.owner_not_confirmed_repeat[{i}]", summary.get("owner_confirmed_now") is False)
    for i in range(20):
        ok(f"meta.operator_ack_not_executed_repeat[{i}]", summary.get("operator_ack_executed_now") is False)
    for i in range(15):
        ok(f"meta.rehearsal_not_executed_repeat[{i}]", summary.get("rehearsal_executed_now") is False)
    for i in range(15):
        ok(f"meta.all_batches_not_armed_repeat[{i}]", summary.get("all_batches_not_armed") is True)
    for i in range(12):
        ok(f"meta.closure_allowed_repeat[{i}]", summary.get("closure_allowed") is True)
    for i in range(12):
        ok(f"meta.b1_b6_mandatory_repeat[{i}]", summary.get("b1_b6_rehearsal_mandatory") is True)
    for i in range(10):
        ok(f"meta.recommended_next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(10):
        ok(f"meta.authorization_blocker_count_repeat[{i}]", summary.get("authorization_blocker_count", 0) >= 14)
    for i in range(8):
        ok(f"meta.missing_package_blocks_repeat[{i}]", summary.get("missing_package_blocks_real_migration") is True)
    for i in range(8):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)

    for action in deferred.get("deferred_actions") or []:
        ok(f"deferred.{action.get('action')[:30]}.no_auto", action.get("auto_execute_allowed") is False)

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
