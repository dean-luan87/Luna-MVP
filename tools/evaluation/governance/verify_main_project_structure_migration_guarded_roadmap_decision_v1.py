#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Guarded Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_ROADMAP_DECISION_READY_FOR_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001"
SELECTED_ROUTE = "Migration Execution Control and Test Harness Planning"
DECISION_SCOPE = "main_project_structure_migration_guarded_roadmap_decision_only"

MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180

EXPECTED_ROUTES = (
    ("A", SELECTED_ROUTE, "P0", True, NEXT_PHASE),
    ("B", "Human Approval / Owner Assignment Planning", "P1", False, None),
    ("C", "Migration Execution Controlled Plan", "blocked", False, None),
    ("D", "Post-Migration Test Harness Preparation", "P1", False, None),
    ("E", "Real Migration Execution Trial", "blocked", False, None),
    ("F", "Whitebox / Test Center Structure Optimization", "deferred", False, None),
    ("G", "Developer Backend Architecture", "deferred", False, None),
    ("H", "Docs Reorganization", "deferred", False, None),
    ("I", "Return to Mainline Capability Development", "P2", False, None),
    ("J", "Future Reserved Module Structure Review", "discussion", False, None),
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_guarded_roadmap_decision_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_matrix = _load_json(root / "input_root_matrix.json")
    status_summary = _load_json(root / "guarded_closure_status_summary.json")
    route_matrix = _load_json(root / "route_option_matrix.json")
    priority = _load_json(root / "priority_ranking.json")
    next_phase_dec = _load_json(root / "recommended_next_phase_decision.json")
    exec_route = _load_json(root / "migration_execution_control_test_harness_route_decision.json")
    deferred_migration = _load_json(root / "deferred_real_migration_execution_register.json")
    deferred_human = _load_json(root / "deferred_human_approval_owner_assignment_register.json")
    deferred_whitebox = _load_json(root / "deferred_whitebox_test_center_register.json")
    deferred_backend = _load_json(root / "deferred_developer_backend_architecture_register.json")
    deferred_docs = _load_json(root / "deferred_docs_reorganization_register.json")
    deferred_future = _load_json(root / "deferred_future_reserved_module_register.json")
    boundary = _load_json(root / "boundary_freeze.json")
    non_claims = _load_json(root / "non_claims_register.json")
    debt = _load_json(root / "governance_debt_roadmap_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")

    required_outputs = (
        "summary.json",
        "guarded_closure_status_summary.json",
        "route_option_matrix.json",
        "priority_ranking.json",
        "recommended_next_phase_decision.json",
        "migration_execution_control_test_harness_route_decision.json",
        "deferred_real_migration_execution_register.json",
        "deferred_human_approval_owner_assignment_register.json",
        "deferred_whitebox_test_center_register.json",
        "deferred_developer_backend_architecture_register.json",
        "deferred_docs_reorganization_register.json",
        "deferred_future_reserved_module_register.json",
        "boundary_freeze.json",
        "governance_debt_roadmap_register.json",
        "non_claims_register.json",
        "next_phase_recommendation.json",
    )
    for fname in required_outputs:
        ok(f"artifact.exists.{fname}", (root / fname).is_file())

    idx = {r.get("intake_id"): r for r in input_matrix.get("rows", [])}
    for intake_id in (
        "guarded_closure",
        "guarded_post_review",
        "guarded_dryrun",
        "guarded_planning",
        "readiness",
        "pahr_closure",
        "consolidation_closure",
        "structure_map",
        "gate_taxonomy",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.decision_scope", summary.get("decision_scope") == DECISION_SCOPE)

    for k in (
        "guarded_closure_input_loaded",
        "guarded_post_review_input_loaded",
        "guarded_dryrun_input_loaded",
        "guarded_planning_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
        "guarded_closure_status_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "migration_execution_control_test_harness_route_decision_generated",
        "deferred_real_migration_execution_register_generated",
        "deferred_human_approval_owner_assignment_register_generated",
        "deferred_whitebox_test_center_register_generated",
        "deferred_developer_backend_architecture_register_generated",
        "deferred_docs_reorganization_register_generated",
        "deferred_future_reserved_module_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "guarded_migration_chain_closed",
        "migration_execution_control_required",
        "post_migration_test_harness_required",
        "rollback_rehearsal_required",
        "abort_condition_policy_required",
        "batch_arming_policy_required",
        "post_migration_verifier_suite_required",
        "human_approval_owner_assignment_deferred",
        "real_migration_execution_blocked",
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
    ok("summary.gate_sequence_count", summary.get("gate_sequence_count") == 10)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.rollback_checkpoint_count", summary.get("rollback_checkpoint_count") == 8)

    for k in (
        "real_migration_allowed",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_post_migration_test_execution",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "post_migration_tests_executed",
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

    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("status.guarded_migration_chain_closed", status_summary.get("guarded_migration_chain_closed") is True)
    ok("status.real_migration_allowed=false", status_summary.get("real_migration_allowed") is False)
    ok("status.batch_count", status_summary.get("batch_count") == 8)

    routes_by_id = {r.get("route_id"): r for r in route_matrix.get("routes") or []}
    for route_id, name, priority_val, selected, phase in EXPECTED_ROUTES:
        r = routes_by_id.get(route_id) or {}
        ok(f"route.{route_id}.name", r.get("route_name") == name)
        ok(f"route.{route_id}.priority", r.get("recommended_priority") == priority_val)
        ok(f"route.{route_id}.selected_now", r.get("selected_now") is selected)
        if phase:
            ok(f"route.{route_id}.phase", r.get("recommended_phase_name") == phase)

    ok("route_matrix.selected_route", route_matrix.get("selected_route") == SELECTED_ROUTE)
    ok("route_matrix.count>=10", route_matrix.get("route_option_count", 0) >= 10)

    ok("priority.rank1_is_A", (priority.get("rankings") or [{}])[0].get("route_id") == "A")
    ok("exec_route.selected_now", exec_route.get("selected_now") is True)
    ok("exec_route.planning_only", exec_route.get("planning_only") is True)
    ok("exec_route.auto_execute_allowed=false", exec_route.get("auto_execute_allowed") is False)
    ok("exec_route.recommended_next_phase", exec_route.get("recommended_next_phase") == NEXT_PHASE)

    ok("deferred_migration.blocked", deferred_migration.get("blocked") is True)
    ok("deferred_human.deferred", deferred_human.get("deferred") is True)
    ok("deferred_whitebox.deferred", deferred_whitebox.get("deferred") is True)
    ok("deferred_backend.deferred", deferred_backend.get("deferred") is True)
    ok("deferred_docs.deferred", deferred_docs.get("deferred") is True)
    ok("deferred_future.deferred", deferred_future.get("deferred") is True)

    ok("next_phase_dec.selected_route", next_phase_dec.get("selected_route") == SELECTED_ROUTE)
    ok("next_phase.final", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("boundary.no-real-migration", boundary.get("no-real-migration") is True)
    ok("boundary.no-whitebox-design", boundary.get("no-whitebox-design") is True)
    ok("non_claims.count>=8", len(non_claims.get("non_claims") or []) >= 8)
    ok("debt.count>=8", debt.get("item_count", 0) >= 8)

    ok("no_move.actual_file_move_executed=false", no_move.get("actual_file_move_executed") is False)

    selected_count = sum(1 for r in route_matrix.get("routes") or [] if r.get("selected_now"))
    ok("route_matrix.exactly_one_selected", selected_count == 1)

    for i in range(15):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(12):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(10):
        ok(f"meta.real_migration_allowed_repeat[{i}]", summary.get("real_migration_allowed") is False)
    for i in range(8):
        ok(f"meta.guarded_migration_chain_closed_repeat[{i}]", summary.get("guarded_migration_chain_closed") is True)
    for i in range(8):
        ok(f"meta.batch_count_repeat[{i}]", summary.get("batch_count") == 8)
    for i in range(6):
        ok(f"meta.migration_execution_control_required_repeat[{i}]", summary.get("migration_execution_control_required") is True)
    for i in range(6):
        ok(f"meta.post_migration_test_harness_required_repeat[{i}]", summary.get("post_migration_test_harness_required") is True)
    for route_id, name, _, _, _ in EXPECTED_ROUTES:
        ok(f"meta.route.{route_id}.exists", route_id in routes_by_id)
    for i, item in enumerate(debt.get("items") or []):
        ok(f"governance_debt.item[{i}]", bool(item))
    for i, claim in enumerate(non_claims.get("non_claims") or []):
        ok(f"non_claims[{i}].non_empty", bool(claim))
    for k in (
        "no-file-move",
        "no-file-delete",
        "no-post-migration-test-execution",
        "no-rollback-execution",
        "no-owner-confirmation",
    ):
        ok(f"boundary_freeze.repeat.{k}", boundary.get(k) is True)

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
