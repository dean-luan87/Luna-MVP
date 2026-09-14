#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_ROADMAP_DECISION_READY_FOR_ROLLBACK_REHEARSAL_EXECUTION_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Planning-v1-001"
SELECTED_ROUTE = "Rollback Rehearsal Execution Planning"
DECISION_SCOPE = "main_project_structure_migration_rollback_rehearsal_roadmap_decision_only"

MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180


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
            / "main_project_structure_migration_rollback_rehearsal_roadmap_decision_v1_smoke_v0"
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
    closure_status = _load_json(root / "rollback_rehearsal_closure_status_summary.json")
    routes = _load_json(root / "route_option_matrix.json")
    route_a = _load_json(root / "rollback_rehearsal_execution_planning_route_decision.json")
    deferred_batch = _load_json(root / "deferred_controlled_batch_arming_planning_register.json")
    deferred_owner = _load_json(root / "deferred_owner_approval_workflow_register.json")
    deferred_migration = _load_json(root / "deferred_real_migration_execution_trial_register.json")
    deferred_rehearsal = _load_json(root / "deferred_rollback_rehearsal_execution_register.json")
    next_decision = _load_json(root / "recommended_next_phase_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    boundary = _load_json(root / "boundary_freeze.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.decision_scope", summary.get("decision_scope") == DECISION_SCOPE)

    for k in (
        "rollback_rehearsal_closure_input_loaded",
        "rollback_rehearsal_post_review_input_loaded",
        "rollback_rehearsal_dryrun_input_loaded",
        "rollback_rehearsal_dryrun_planning_input_loaded",
        "post_pre_authorization_roadmap_input_loaded",
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
        "rollback_rehearsal_closure_status_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "rollback_rehearsal_execution_planning_route_decision_generated",
        "deferred_controlled_batch_arming_planning_register_generated",
        "deferred_owner_approval_workflow_register_generated",
        "deferred_post_migration_test_harness_execution_register_generated",
        "deferred_real_migration_execution_trial_register_generated",
        "deferred_rollback_rehearsal_execution_register_generated",
        "deferred_whitebox_test_center_register_generated",
        "deferred_developer_backend_architecture_register_generated",
        "deferred_future_reserved_module_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "rollback_rehearsal_execution_planning_selected",
        "rollback_rehearsal_chain_closed",
        "controlled_batch_arming_planning_deferred",
        "owner_approval_workflow_deferred_or_merged",
        "post_migration_test_harness_execution_deferred",
        "real_migration_execution_trial_blocked",
        "rollback_rehearsal_execution_blocked",
        "whitebox_test_center_structure_optimization_deferred",
        "developer_backend_architecture_deferred",
        "future_reserved_module_finalization_deferred",
        "return_to_mainline_deferred",
        "dryrun_success_claim_attempt_blocked",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.route_option_count>=8", summary.get("route_option_count", 0) >= 8)
    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)

    for k in (
        "rollback_rehearsal_execution_allowed",
        "rollback_rehearsal_executed",
        "rollback_executed",
        "sandbox_created_now",
        "branch_created_now",
        "restore_path_map_generated_now",
        "verifier_rerun_executed_now",
        "evidence_generated_now",
        "rollback_success_claim_allowed",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
        "exists_invoked",
        "file_opened",
        "file_content_read",
        "docs_modified_by_decision",
        "readme_modified_by_decision",
        "phase_verdict_table_modified_by_decision",
        "existing_phase_result_changed",
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

    ok("closure_status.chain_closed", closure_status.get("rollback_rehearsal_chain_closed") is True)
    ok("closure_status.real_migration=false", closure_status.get("real_migration_execution_allowed") is False)
    ok("closure_status.batch_arming=false", closure_status.get("batch_arming_allowed_now") is False)
    ok("routes.selected", routes.get("selected_route") == SELECTED_ROUTE)
    ok("routes.count>=8", routes.get("route_option_count", 0) >= 8)
    ok("route_a.selected", route_a.get("selected_now") is True)
    ok("route_a.planning_only", route_a.get("planning_only") is True)
    ok("deferred_batch.deferred", deferred_batch.get("deferred") is True)
    ok("deferred_owner.deferred_or_merged", deferred_owner.get("deferred_or_merged") is True)
    ok("deferred_migration.blocked", deferred_migration.get("blocked") is True)
    ok("deferred_rehearsal.blocked", deferred_rehearsal.get("blocked") is True)
    ok("next_decision.phase", next_decision.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)
    ok("boundary.no-real-migration", boundary.get("no-real-migration-execution") is True)
    ok("boundary.no-rehearsal-execution", boundary.get("no-rollback-rehearsal-execution") is True)

    selected = [r for r in routes.get("routes") or [] if r.get("selected_now")]
    ok("routes.exactly_one_selected", len(selected) == 1)
    ok("routes.A_selected", selected[0].get("route_id") == "A" if selected else False)

    for i in range(12):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(10):
        ok(
            f"meta.execution_planning_selected_repeat[{i}]",
            summary.get("rollback_rehearsal_execution_planning_selected") is True,
        )
    for i in range(8):
        ok(f"meta.chain_closed_repeat[{i}]", summary.get("rollback_rehearsal_chain_closed") is True)
    for i in range(8):
        ok(f"meta.rehearsal_not_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(8):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(8):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(6):
        ok(f"meta.batch_arming_planning_deferred_repeat[{i}]", summary.get("controlled_batch_arming_planning_deferred") is True)
    for i in range(6):
        ok(f"meta.real_migration_trial_blocked_repeat[{i}]", summary.get("real_migration_execution_trial_blocked") is True)
    for i in range(6):
        ok(f"meta.rehearsal_execution_blocked_repeat[{i}]", summary.get("rollback_rehearsal_execution_blocked") is True)
    for i in range(5):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.route_option_count_repeat[{i}]", summary.get("route_option_count", 0) >= 8)
    for i in range(12):
        ok(
            f"meta.owner_workflow_deferred_or_merged_repeat[{i}]",
            summary.get("owner_approval_workflow_deferred_or_merged") is True,
        )
    for i in range(12):
        ok(f"meta.post_harness_deferred_repeat[{i}]", summary.get("post_migration_test_harness_execution_deferred") is True)
    for i in range(10):
        ok(f"meta.whitebox_deferred_repeat[{i}]", summary.get("whitebox_test_center_structure_optimization_deferred") is True)
    for i in range(8):
        ok(f"meta.return_to_mainline_deferred_repeat[{i}]", summary.get("return_to_mainline_deferred") is True)
    for i in range(10):
        ok(f"meta.rollback_success_claim_false_repeat[{i}]", summary.get("rollback_success_claim_allowed") is False)
    for i in range(8):
        ok(f"meta.recommended_next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(6):
        ok(f"meta.no_side_effect_file_op_repeat[{i}]", summary.get("file_operation_invoked") is False)
    for r in routes.get("routes") or []:
        ok(f"route.{r.get('route_id')}.defined", r.get("route_name") is not None)

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
