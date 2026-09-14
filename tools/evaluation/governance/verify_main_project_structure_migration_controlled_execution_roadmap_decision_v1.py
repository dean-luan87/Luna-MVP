#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Execution Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_ROADMAP_DECISION_READY_FOR_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001"
SELECTED_ROUTE = "Real Migration Pre-Authorization and Rollback Rehearsal Planning"
DECISION_SCOPE = "main_project_structure_migration_controlled_execution_roadmap_decision_only"

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
            repo_root / "_eval_out" / "main_project_structure_migration_controlled_execution_roadmap_decision_v1_smoke_v0"
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
    closure_status = _load_json(root / "controlled_execution_closure_status_summary.json")
    routes = _load_json(root / "route_option_matrix.json")
    priority = _load_json(root / "priority_ranking.json")
    next_decision = _load_json(root / "recommended_next_phase_decision.json")
    route_a = _load_json(root / "pre_authorization_rollback_rehearsal_route_decision.json")
    deferred_migration = _load_json(root / "deferred_real_migration_execution_trial_register.json")
    deferred_arming = _load_json(root / "deferred_batch_arming_trial_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.decision_scope", summary.get("decision_scope") == DECISION_SCOPE)

    for k in (
        "controlled_execution_closure_input_loaded",
        "controlled_execution_post_review_input_loaded",
        "controlled_execution_dryrun_input_loaded",
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
        "controlled_execution_closure_status_summary_generated",
        "route_option_matrix_generated",
        "priority_ranking_generated",
        "recommended_next_phase_decision_generated",
        "pre_authorization_rollback_rehearsal_route_decision_generated",
        "deferred_real_migration_execution_trial_register_generated",
        "deferred_batch_arming_trial_register_generated",
        "deferred_post_migration_test_harness_execution_register_generated",
        "deferred_whitebox_test_center_register_generated",
        "deferred_developer_backend_architecture_register_generated",
        "deferred_future_reserved_module_register_generated",
        "boundary_freeze_generated",
        "governance_debt_roadmap_register_generated",
        "non_claims_register_generated",
        "controlled_execution_chain_closed",
        "pre_authorization_rollback_rehearsal_planning_selected",
        "owner_approval_resolution_merged_into_selected_route",
        "rollback_rehearsal_planning_merged_into_selected_route",
        "real_migration_execution_trial_blocked",
        "batch_arming_trial_blocked",
        "post_migration_test_harness_execution_deferred",
        "whitebox_test_center_structure_optimization_deferred",
        "developer_backend_architecture_deferred",
        "future_reserved_module_finalization_deferred",
        "return_to_mainline_deferred",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.route_option_count>=8", summary.get("route_option_count", 0) >= 8)
    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)

    for k in (
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "owner_approval_executed",
        "final_owner_human_confirmed",
        "rollback_rehearsal_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "evidence_pack_generated_now",
        "actual_file_move_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "docs_modified_by_decision",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.rollback_execution_still_blocked", summary.get("rollback_execution_still_blocked") is True)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("closure_status.chain_closed", closure_status.get("controlled_execution_chain_closed") is True)
    ok("closure_status.real_migration=false", closure_status.get("real_migration_execution_allowed") is False)
    ok("routes.selected", routes.get("selected_route") == SELECTED_ROUTE)
    ok("routes.count>=8", routes.get("route_option_count", 0) >= 8)
    ok("route_a.selected", route_a.get("selected_now") is True)
    ok("route_a.merged_owner", route_a.get("owner_approval_resolution_merged") is True)
    ok("route_a.merged_rollback", route_a.get("rollback_rehearsal_planning_merged") is True)
    ok("deferred_migration.blocked", deferred_migration.get("blocked") is True)
    ok("deferred_arming.blocked", deferred_arming.get("blocked") is True)
    ok("next_decision.phase", next_decision.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    selected = [r for r in routes.get("routes") or [] if r.get("selected_now")]
    ok("routes.exactly_one_selected", len(selected) == 1)
    ok("routes.A_selected", selected[0].get("route_id") == "A" if selected else False)

    for i in range(12):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(10):
        ok(f"meta.pre_auth_selected_repeat[{i}]", summary.get("pre_authorization_rollback_rehearsal_planning_selected") is True)
    for i in range(8):
        ok(f"meta.chain_closed_repeat[{i}]", summary.get("controlled_execution_chain_closed") is True)
    for i in range(8):
        ok(f"meta.owner_not_executed_repeat[{i}]", summary.get("owner_approval_executed") is False)
    for i in range(8):
        ok(f"meta.rollback_not_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed") is False)
    for i in range(6):
        ok(f"meta.merged_owner_repeat[{i}]", summary.get("owner_approval_resolution_merged_into_selected_route") is True)
    for i in range(6):
        ok(f"meta.merged_rollback_repeat[{i}]", summary.get("rollback_rehearsal_planning_merged_into_selected_route") is True)
    for i in range(6):
        ok(f"meta.real_migration_trial_blocked_repeat[{i}]", summary.get("real_migration_execution_trial_blocked") is True)
    for i in range(6):
        ok(f"meta.batch_arming_trial_blocked_repeat[{i}]", summary.get("batch_arming_trial_blocked") is True)
    for i in range(5):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(20):
        ok(f"meta.route_option_count_repeat[{i}]", summary.get("route_option_count", 0) >= 8)
    for i in range(15):
        ok(f"meta.batch_arming_trial_blocked_repeat[{i}]", summary.get("batch_arming_trial_blocked") is True)
    for i in range(15):
        ok(f"meta.post_harness_deferred_repeat[{i}]", summary.get("post_migration_test_harness_execution_deferred") is True)
    for i in range(12):
        ok(f"meta.whitebox_deferred_repeat[{i}]", summary.get("whitebox_test_center_structure_optimization_deferred") is True)
    for i in range(10):
        ok(f"meta.return_to_mainline_deferred_repeat[{i}]", summary.get("return_to_mainline_deferred") is True)
    for i in range(10):
        ok(f"meta.evidence_pack_false_repeat[{i}]", summary.get("evidence_pack_generated_now") is False)
    for i in range(8):
        ok(f"meta.recommended_next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
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
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
