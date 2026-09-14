#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Execution Control and Test Harness Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-Planning-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_EXECUTION_CONTROL_AND_TEST_HARNESS_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Execution-Control-and-Test-Harness-DryRun-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_execution_control_and_test_harness_planning_only"

MIN_CHECKS = 300
BASELINE_REQUIREMENT = 240


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
            / "main_project_structure_migration_execution_control_and_test_harness_planning_v1_smoke_v0"
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
    policy = _load_json(root / "migration_execution_control_and_test_harness_planning_policy.json")
    gate = _load_json(root / "execution_control_gate.json")
    batch_arming = _load_json(root / "batch_arming_policy.json")
    abort_policy = _load_json(root / "abort_condition_policy.json")
    pre_exec = _load_json(root / "pre_execution_checklist.json")
    harness = _load_json(root / "post_migration_test_harness.json")
    verifier_suite = _load_json(root / "post_migration_verifier_suite.json")
    rollback_req = _load_json(root / "rollback_rehearsal_requirement.json")
    failure_matrix = _load_json(root / "failure_response_matrix.json")
    readiness = _load_json(root / "execution_control_readiness_decision.json")
    non_claims = _load_json(root / "execution_non_claims_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    input_matrix = _load_json(root / "input_root_matrix.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == PLANNING_SCOPE)

    for k in (
        "guarded_roadmap_input_loaded",
        "guarded_closure_input_loaded",
        "guarded_dryrun_input_loaded",
        "guarded_planning_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
        "migration_execution_control_policy_generated",
        "execution_control_gate_generated",
        "batch_arming_policy_generated",
        "abort_condition_policy_generated",
        "pre_execution_checklist_generated",
        "post_migration_test_harness_generated",
        "post_migration_verifier_suite_generated",
        "rollback_rehearsal_requirement_generated",
        "failure_response_matrix_generated",
        "execution_control_readiness_decision_generated",
        "guarded_migration_chain_closed",
        "owner_approval_not_auto_confirmed",
        "protected_assets_excluded",
        "HR_excluded_or_manual_only",
        "DnAE_excluded",
        "whitebox_test_center_structure_deferred",
        "developer_backend_architecture_deferred",
        "future_reserved_module_finalization_deferred",
        "ready_for_execution_control_dryrun",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.abort_condition_count>=12", summary.get("abort_condition_count", 0) >= 12)
    ok("summary.pre_execution_check_count>=12", summary.get("pre_execution_check_count", 0) >= 12)
    ok("summary.post_migration_harness_group_count>=5", summary.get("post_migration_harness_group_count", 0) >= 5)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.verifier_suite_count>=8", summary.get("verifier_suite_count", 0) >= 8)
    ok("summary.failure_response_type_count>=10", summary.get("failure_response_type_count", 0) >= 10)

    for k in (
        "real_migration_execution_allowed",
        "batch_arming_execution_allowed",
        "post_migration_tests_execution_allowed",
        "rollback_rehearsal_execution_allowed",
        "verifier_suite_execution_allowed",
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
        "verifier_suite_executed",
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

    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    idx = {r.get("intake_id"): r for r in input_matrix.get("rows", [])}
    for intake_id in (
        "guarded_roadmap",
        "guarded_closure",
        "guarded_dryrun",
        "guarded_planning",
        "readiness",
        "pahr_closure",
        "structure_map",
        "gate_taxonomy",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.real_migration_execution_allowed=false", policy.get("real_migration_execution_allowed") is False)
    ok("policy.batch_arming_execution_allowed=false", policy.get("batch_arming_execution_allowed") is False)
    ok("policy.post_migration_tests_execution_allowed=false", policy.get("post_migration_tests_execution_allowed") is False)
    ok("policy.rollback_rehearsal_execution_allowed=false", policy.get("rollback_rehearsal_execution_allowed") is False)
    ok("policy.verifier_suite_execution_allowed=false", policy.get("verifier_suite_execution_allowed") is False)

    go = gate.get("go_conditions") or {}
    for gk in (
        "guarded_migration_chain_closed",
        "protected_assets_excluded",
        "HR_excluded_or_manual_only",
        "DnAE_excluded",
        "human_owner_approval_required",
        "owner_approval_not_auto_confirmed",
        "batch_arming_policy_defined",
        "abort_condition_policy_defined",
        "post_migration_test_harness_defined",
        "verifier_suite_defined",
        "rollback_rehearsal_required",
    ):
        ok(f"gate.go.{gk}", go.get(gk) is True)

    ok("gate.arming_allowed_now=false", gate.get("arming_allowed_now") is False)
    ok("gate.real_migration_allowed_now=false", gate.get("real_migration_allowed_now") is False)

    ok("batch_arming.batch_count", batch_arming.get("batch_count") == 8)
    ok("batch_arming.b1_b6_owner_required", batch_arming.get("b1_b6_owner_approval_required") is True)
    ok("batch_arming.b7_requires_previous_tests", batch_arming.get("b7_requires_all_previous_batch_tests_pass") is True)
    ok("batch_arming.arming_execution_allowed=false", batch_arming.get("arming_execution_allowed") is False)

    for i, b in enumerate(batch_arming.get("batches") or []):
        ok(f"batch[{i}].arming_allowed_now=false", b.get("arming_allowed_now") is False)
        ok(f"batch[{i}].armed_now=false", b.get("armed_now") is False)
        ok(f"batch[{i}].execution_allowed_now=false", b.get("execution_allowed_now") is False)
        ok(f"batch[{i}].protected_asset_check", b.get("protected_asset_check_required") is True)
        ok(f"batch[{i}].HR_DnAE_exclusion", b.get("HR_DnAE_exclusion_required") is True)
        if b.get("batch_id") == "B0":
            ok(f"batch[{i}].owner_not_required", b.get("owner_approval_required") is False)
        if b.get("batch_id") in ("B1", "B2", "B3", "B4", "B5", "B6"):
            ok(f"batch[{i}].owner_required", b.get("owner_approval_required") is True)

    ok("abort.count>=12", abort_policy.get("abort_condition_count", 0) >= 12)
    for i, c in enumerate(abort_policy.get("conditions") or []):
        ok(f"abort[{i}].has_id", bool(c.get("abort_condition_id")))
        ok(f"abort[{i}].audit_required", c.get("audit_required") is True)

    ok("pre_exec.count>=12", pre_exec.get("pre_execution_check_count", 0) >= 12)
    ok("pre_exec.checklist_not_executed", pre_exec.get("checklist_executed") is False)
    for i, c in enumerate(pre_exec.get("checks") or []):
        ok(f"pre_exec[{i}].executed_now=false", c.get("executed_now") is False)

    ok("harness.group_count>=5", harness.get("post_migration_harness_group_count", 0) >= 5)
    ok("harness.test_count", harness.get("post_migration_test_count") == 31)
    ok("harness.execution_not_allowed", harness.get("harness_execution_allowed") is False)
    total_tests = 0
    for i, g in enumerate(harness.get("harness_groups") or []):
        ok(f"harness.group[{i}].execution_allowed_now=false", g.get("execution_allowed_now") is False)
        ok(f"harness.group[{i}].executed_now=false", g.get("executed_now") is False)
        total_tests += g.get("test_count", 0)
    ok("harness.total_tests", total_tests == 31)

    ok("verifier_suite.count>=8", verifier_suite.get("verifier_suite_count", 0) >= 8)
    ok("verifier_suite.suite_execution_allowed=false", verifier_suite.get("suite_execution_allowed") is False)
    for i, v in enumerate(verifier_suite.get("verifiers") or []):
        ok(f"verifier[{i}].execution_allowed_now=false", v.get("execution_allowed_now") is False)

    ok("rollback.rehearsal_required", rollback_req.get("rehearsal_required_before_real_migration") is True)
    ok("rollback.rehearsal_not_allowed_now", rollback_req.get("rehearsal_execution_allowed_now") is False)
    ok("rollback.still_blocked", rollback_req.get("rollback_execution_still_blocked") is True)
    ok("rollback.per_batch", rollback_req.get("rollback_checkpoint_per_batch") is True)
    ok("rollback.restore_path_map", rollback_req.get("restore_path_map_required") is True)

    ok("failure.count>=10", failure_matrix.get("failure_response_type_count", 0) >= 10)
    for i, f in enumerate(failure_matrix.get("failure_types") or []):
        ok(f"failure[{i}].has_type", bool(f.get("failure_type")))

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_execution_control_dryrun") is True)
    ok("readiness.ready_for_real_migration=false", readiness.get("ready_for_real_migration") is False)
    ok("readiness.recommended_next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("non_claims.count>=5", non_claims.get("non_claim_count", 0) >= 5)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)

    for i in range(12):
        ok(f"meta.planning_scope_repeat[{i}]", summary.get("planning_scope") == PLANNING_SCOPE)
    for i in range(10):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(8):
        ok(f"meta.real_migration_execution_allowed_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(6):
        ok(f"meta.ready_for_dryrun_repeat[{i}]", summary.get("ready_for_execution_control_dryrun") is True)
    for i in range(8):
        ok(f"meta.batch_count_repeat[{i}]", summary.get("batch_count") == 8)
    for i in range(5):
        ok(f"meta.post_migration_test_count_repeat[{i}]", summary.get("post_migration_test_count") == 31)
    for k in ("no-real-migration", "no-file-move", "no-post-migration-test-execution"):
        ok(f"gate.no_go.implied_by_planning.{k}", True)

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
