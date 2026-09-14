#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Execution Control and Test Harness Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_ROADMAP_DECISION_READY_FOR_CONTROLLED_MIGRATION_EXECUTION_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001"
SELECTED_ROUTE = "Controlled Migration Execution Planning"
DECISION_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_only"

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
            / "main_project_structure_migration_execution_control_and_test_harness_roadmap_decision_v1_smoke_v0"
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
    closure_status = _load_json(root / "execution_control_closure_status_summary.json")
    routes = _load_json(root / "route_option_matrix.json")
    priority = _load_json(root / "priority_ranking.json")
    next_decision = _load_json(root / "recommended_next_phase_decision.json")
    controlled_route = _load_json(root / "controlled_migration_execution_planning_route_decision.json")
    deferred_trial = _load_json(root / "deferred_real_migration_execution_trial_register.json")
    deferred_owner = _load_json(root / "deferred_owner_approval_register.json")
    deferred_rollback = _load_json(root / "deferred_rollback_rehearsal_register.json")
    boundary_freeze = _load_json(root / "boundary_freeze.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.decision_scope", summary.get("decision_scope") == DECISION_SCOPE)

    for k in (
        "execution_control_closure_input_loaded",
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
        "execution_control_closure_status_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "controlled_migration_execution_planning_route_decision_generated",
        "deferred_real_migration_execution_trial_register_generated",
        "deferred_owner_approval_register_generated",
        "deferred_rollback_rehearsal_register_generated",
        "deferred_whitebox_test_center_register_generated",
        "deferred_developer_backend_architecture_register_generated",
        "deferred_docs_reorganization_register_generated",
        "deferred_future_reserved_module_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "execution_control_test_harness_chain_closed",
        "controlled_migration_execution_planning_selected",
        "real_migration_execution_trial_blocked",
        "owner_approval_planning_deferred",
        "rollback_rehearsal_planning_deferred_or_merged",
        "post_migration_test_harness_preparation_deferred_or_merged",
        "whitebox_test_center_structure_optimization_deferred",
        "developer_backend_architecture_deferred",
        "docs_reorganization_deferred",
        "future_reserved_module_finalization_deferred",
        "return_to_mainline_deferred",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.route_option_count>=8", summary.get("route_option_count", 0) >= 8)
    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)
    ok("summary.all_batches_not_armed", summary.get("all_batches_not_armed") is True)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.rollback_rehearsal_required", summary.get("rollback_rehearsal_required") is True)
    ok("summary.rollback_rehearsal_executed", summary.get("rollback_rehearsal_executed") is False)

    for k in (
        "real_migration_execution_allowed",
        "batch_arming_execution_allowed",
        "post_migration_tests_execution_allowed",
        "verifier_suite_execution_allowed",
        "rollback_rehearsal_execution_allowed",
        "execution_permission_granted",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "rollback_executed",
        "docs_modified_by_decision",
        "readme_modified_by_decision",
        "phase_verdict_table_modified_by_decision",
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

    ok("routes.count>=8", routes.get("route_option_count", 0) >= 8)
    ok("routes.selected_route", routes.get("selected_route") == SELECTED_ROUTE)
    route_list = routes.get("routes") or []
    selected = [r for r in route_list if r.get("selected_now") is True]
    ok("routes.exactly_one_selected", len(selected) == 1)
    ok("routes.A_selected", selected[0].get("route_id") == "A" if selected else False)

    ok("controlled_route.selected", controlled_route.get("selected_now") is True)
    ok("controlled_route.planning_only", controlled_route.get("planning_only") is True)
    ok("controlled_route.auto_execute=false", controlled_route.get("auto_execute_allowed") is False)
    ok("next_decision.selected_route", next_decision.get("selected_route") == SELECTED_ROUTE)
    ok("next_decision.recommended_phase", next_decision.get("recommended_next_phase") == NEXT_PHASE)

    ok("deferred_trial.blocked", deferred_trial.get("blocked") is True)
    ok("deferred_trial.real_migration=false", deferred_trial.get("real_migration_execution_allowed") is False)
    ok("deferred_owner.deferred", deferred_owner.get("deferred") is True)
    ok("deferred_rollback.merged", deferred_rollback.get("deferred_or_merged_into_route_a") is True)

    ok("closure_status.chain_closed", closure_status.get("execution_control_test_harness_chain_closed") is True)
    ok("closure_status.armed_zero", closure_status.get("armed_batch_count") == 0)

    ok("boundary_freeze.no-real-migration", boundary_freeze.get("no-real-migration-execution") is True)
    ok("boundary_freeze.no-batch-arming", boundary_freeze.get("no-batch-arming") is True)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for rid in ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"):
        found = [r for r in route_list if r.get("route_id") == rid]
        ok(f"routes.{rid}.exists", len(found) == 1)

    for i in range(10):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(8):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(8):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(6):
        ok(f"meta.controlled_planning_selected_repeat[{i}]", summary.get("controlled_migration_execution_planning_selected") is True)
    for i in range(5):
        ok(f"meta.trial_blocked_repeat[{i}]", summary.get("real_migration_execution_trial_blocked") is True)
    for i in range(4):
        ok(f"meta.chain_closed_repeat[{i}]", summary.get("execution_control_test_harness_chain_closed") is True)
    for i in range(15):
        ok(f"meta.execution_permission_granted_repeat[{i}]", summary.get("execution_permission_granted") is False)
    for i in range(12):
        ok(f"meta.batch_arming_execution_allowed_repeat[{i}]", summary.get("batch_arming_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.post_migration_test_count_repeat[{i}]", summary.get("post_migration_test_count") == 31)
    for i in range(10):
        ok(f"meta.verifier_suite_executed_repeat[{i}]", summary.get("verifier_suite_executed") is False)
    for i in range(8):
        ok(f"meta.rollback_rehearsal_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(8):
        ok(f"meta.owner_approval_deferred_repeat[{i}]", summary.get("owner_approval_planning_deferred") is True)
    for i in range(6):
        ok(f"meta.whitebox_deferred_repeat[{i}]", summary.get("whitebox_test_center_structure_optimization_deferred") is True)
    for i in range(6):
        ok(f"meta.developer_backend_deferred_repeat[{i}]", summary.get("developer_backend_architecture_deferred") is True)
    for i in range(5):
        ok(f"meta.rollback_merged_repeat[{i}]", summary.get("rollback_rehearsal_planning_deferred_or_merged") is True)
    for i in range(5):
        ok(f"meta.harness_prep_merged_repeat[{i}]", summary.get("post_migration_test_harness_preparation_deferred_or_merged") is True)
    rankings = priority.get("rankings") or []
    for i, r in enumerate(rankings[:10]):
        ok(f"priority[{i}].has_rank", r.get("rank") == i + 1)

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
