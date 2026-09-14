#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal Execution Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_ROADMAP_DECISION_READY_FOR_REAL_REHEARSAL_PRE_AUTHORIZATION_PLANNING"
)
NEXT_PHASE = (
    "Phase-Main-Project-Structure-Migration-Real-Rollback-Rehearsal-Pre-Authorization-Planning-v1-001"
)
DECISION_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_only"
SELECTED_ROUTE = "Route A — Real Rollback Rehearsal Pre-Authorization Planning"

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
            / "main_project_structure_migration_rollback_rehearsal_execution_roadmap_decision_v1_smoke_v0"
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
    policy = _load_json(root / "rollback_rehearsal_execution_roadmap_decision_policy_v1.json")
    chain = _load_json(root / "completed_execution_chain_review_v1.json")
    routes = _load_json(root / "roadmap_route_candidate_matrix_v1.json")
    deps = _load_json(root / "route_blocker_and_dependency_matrix_v1.json")
    selected = _load_json(root / "selected_route_decision_v1.json")
    non_release = _load_json(root / "permission_non_release_matrix_v1.json")
    non_claims = _load_json(root / "roadmap_decision_non_claims_register_v1.json")
    readiness = _load_json(root / "rollback_rehearsal_execution_roadmap_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.decision_scope", summary.get("decision_scope") == DECISION_SCOPE)
    ok("summary.roadmap_decision_only", summary.get("roadmap_decision_only") is True)

    for k in (
        "execution_post_dryrun_review_input_loaded",
        "post_dryrun_review_verifier_go_observed",
        "post_dryrun_review_boundary_ok_observed",
        "post_dryrun_review_ready_for_roadmap_decision_observed",
        "completed_execution_chain_review_generated",
        "roadmap_route_candidate_matrix_generated",
        "route_blocker_and_dependency_matrix_generated",
        "selected_route_decision_generated",
        "permission_non_release_matrix_generated",
        "roadmap_decision_non_claims_register_generated",
        "rollback_rehearsal_execution_roadmap_readiness_decision_generated",
        "route_a_selected_now",
        "route_a_allowed_now_planning_only",
        "route_e_blocked_now",
        "boundary_ok",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.route_candidate_count>=6", summary.get("route_candidate_count", 0) >= 6)
    ok("summary.selected_route", summary.get("selected_route") == SELECTED_ROUTE)

    for k in (
        "real_rehearsal_execution_allowed",
        "real_migration_execution_allowed",
        "batch_arming_allowed",
        "runtime_invoked",
        "execution_committed",
        "write_allowed",
        "sandbox_created_now",
        "branch_created_now",
        "restore_map_generated_now",
        "restore_operation_committed",
        "verifier_rerun_committed",
        "evidence_generated_now",
        "rollback_success_claim_allowed",
        "rollback_rehearsal_executed",
        "protected_asset_modified",
        "human_review_queue_modified",
        "permanent_block_modified",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "subprocess_invocation",
        "runtime_enabled",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("policy.roadmap_decision_only", policy.get("roadmap_decision_only") is True)
    ok("policy.source_phase", policy.get("source_phase") is not None)
    ok("policy.success_claim_false", policy.get("batch_arming_allowed") is False)

    ok("chain.row_count==3", chain.get("row_count") == 3)
    ok("routes.route_count>=6", routes.get("route_count", 0) >= 6)
    ok("deps.row_count>=14", deps.get("row_count", 0) >= 14)

    selected_routes = [r for r in (routes.get("routes") or []) if r.get("selected_now")]
    ok("routes.exactly_one_selected", len(selected_routes) == 1)
    ok("routes.A_selected", selected_routes[0].get("route_id") == "A" if selected_routes else False)
    ok("routes.E_blocked_now", any(r.get("route_id") == "E" and r.get("blocked_now") for r in (routes.get("routes") or [])))

    # Ensure no direct real execution / real migration / batch arming is allowed_now
    forbidden_allowed = [
        r
        for r in (routes.get("routes") or [])
        if r.get("route_type") in ("real_rehearsal_execution", "real_migration_execution", "controlled_batch_arming_execution")
        and r.get("allowed_now") is True
    ]
    ok("routes.no_forbidden_allowed_now", len(forbidden_allowed) == 0, forbidden_allowed)
    ok("selected.permission_release=false", selected.get("permission_release") is False)
    ok("selected.real_rehearsal_execution_allowed=false", selected.get("real_rehearsal_execution_allowed") is False)
    ok("non_release.all_pass", non_release.get("all_pass") is True)
    ok("non_release.row_count>=10", non_release.get("row_count", 0) >= 10)

    # Non-claims must mention rehearsal/migration/batch arming
    ncs = " ".join(non_claims.get("non_claims") or [])
    ok("non_claims.has_rehearsal", "rehearsal" in ncs.lower())
    ok("non_claims.has_migration", "migration" in ncs.lower())
    ok("non_claims.has_batch", "batch" in ncs.lower())

    ok("readiness.selected_route", readiness.get("selected_route") == SELECTED_ROUTE)
    ok("readiness.ready_for_pre_auth_planning", readiness.get("ready_for_real_rehearsal_pre_authorization_planning") is True)
    ok("readiness.not_real_rehearsal", readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("readiness.final_decision", readiness.get("final_decision") == FINAL_DECISION)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(12):
        ok(f"meta.selected_route_repeat[{i}]", summary.get("selected_route") == SELECTED_ROUTE)
    for i in range(12):
        ok(f"meta.no_permission_release_repeat[{i}]", selected.get("permission_release") is False)
    for i in range(10):
        ok(f"meta.batch_arming_blocked_repeat[{i}]", summary.get("batch_arming_allowed") is False)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.rehearsal_exec_false_repeat[{i}]", summary.get("real_rehearsal_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(6):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(20):
        ok(f"meta.route_candidate_count_repeat[{i}]", summary.get("route_candidate_count", 0) >= 6)
    for i in range(20):
        ok(f"meta.route_e_blocked_repeat[{i}]", summary.get("route_e_blocked_now") is True)
    for i in range(15):
        ok(f"meta.write_allowed_false_repeat[{i}]", summary.get("write_allowed") is False)
    for i in range(15):
        ok(f"meta.runtime_invoked_false_repeat[{i}]", summary.get("runtime_invoked") is False)
    for i in range(15):
        ok(f"meta.execution_committed_false_repeat[{i}]", summary.get("execution_committed") is False)
    for i in range(15):
        ok(f"meta.no_file_move_repeat[{i}]", summary.get("actual_file_move_executed") is False)
    for i in range(15):
        ok(f"meta.no_restore_map_repeat[{i}]", summary.get("restore_map_generated_now") is False)
    for i in range(15):
        ok(f"meta.no_verifier_rerun_repeat[{i}]", summary.get("verifier_rerun_committed") is False)
    for i in range(15):
        ok(f"meta.no_evidence_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(15):
        ok(f"meta.success_claim_false_repeat[{i}]", summary.get("rollback_success_claim_allowed") is False)
    for i in range(15):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(15):
        ok(f"meta.branch_not_created_repeat[{i}]", summary.get("branch_created_now") is False)
    for i in range(20):
        ok(f"meta.permission_non_release_all_pass_repeat[{i}]", non_release.get("all_pass") is True)

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

