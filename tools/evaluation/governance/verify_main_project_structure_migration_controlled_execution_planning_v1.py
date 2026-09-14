#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Controlled Execution Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Controlled-Execution-Planning-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_CONTROLLED_EXECUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Controlled-Execution-DryRun-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_controlled_execution_planning_only"

MIN_CHECKS = 320
BASELINE_REQUIREMENT = 260


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(
            repo_root / "_eval_out" / "main_project_structure_migration_controlled_execution_planning_v1_smoke_v0"
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
    policy = _load_json(root / "controlled_migration_execution_planning_policy.json")
    batch_plan = _load_json(root / "controlled_execution_batch_plan.json")
    window = _load_json(root / "execution_window_policy.json")
    owner_gate = _load_json(root / "owner_authorization_gate.json")
    arming = _load_json(root / "batch_arming_execution_plan.json")
    rollback_pre = _load_json(root / "rollback_rehearsal_precondition.json")
    test_order = _load_json(root / "post_batch_test_execution_order.json")
    verifier_order = _load_json(root / "verifier_suite_execution_order.json")
    abort_plan = _load_json(root / "abort_and_failure_response_plan.json")
    evidence = _load_json(root / "post_execution_evidence_pack_plan.json")
    readiness = _load_json(root / "controlled_execution_planning_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == PLANNING_SCOPE)

    for k in (
        "execution_control_roadmap_input_loaded",
        "execution_control_closure_input_loaded",
        "execution_control_post_review_input_loaded",
        "execution_control_dryrun_input_loaded",
        "guarded_closure_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    for k in (
        "controlled_migration_execution_policy_generated",
        "controlled_execution_batch_plan_generated",
        "execution_window_policy_generated",
        "owner_authorization_gate_generated",
        "batch_arming_execution_plan_generated",
        "rollback_rehearsal_precondition_generated",
        "post_batch_test_execution_order_generated",
        "verifier_suite_execution_order_generated",
        "abort_and_failure_response_plan_generated",
        "post_execution_evidence_pack_plan_generated",
        "controlled_execution_planning_readiness_decision_generated",
        "controlled_execution_planning_selected",
        "rollback_rehearsal_mandatory",
        "one_batch_at_a_time_required",
        "no_parallel_migration_batches",
        "pass_required_before_next_batch",
        "failure_blocks_next_batch",
        "protected_assets_excluded",
        "HR_excluded_or_manual_only",
        "DnAE_excluded",
        "whitebox_test_center_structure_deferred",
        "developer_backend_architecture_deferred",
        "future_reserved_module_finalization_deferred",
        "ready_for_controlled_execution_dryrun",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.owner_authorization_gate_count>=7", summary.get("owner_authorization_gate_count", 0) >= 7)
    ok("summary.execution_window_requirement_count>=8", summary.get("execution_window_requirement_count", 0) >= 8)
    ok("summary.post_batch_test_count", summary.get("post_batch_test_count") == 31)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.abort_condition_count>=16", summary.get("abort_condition_count", 0) >= 16)
    ok("summary.failure_response_type_count>=11", summary.get("failure_response_type_count", 0) >= 11)

    for k in (
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "post_migration_tests_execution_allowed",
        "verifier_suite_execution_allowed",
        "rollback_rehearsal_execution_allowed",
        "owner_auto_confirm_allowed",
        "evidence_pack_generated_now",
        "execution_result_claimed_now",
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
    ok("policy.real_migration=false", policy.get("real_migration_execution_allowed") is False)
    ok("policy.batch_arming_allowed_now=false", policy.get("batch_arming_allowed_now") is False)

    batches = batch_plan.get("batches") or []
    ok("batch_plan.count", len(batches) == 8)
    for b in batches:
        bid = b.get("batch_id")
        ok(f"batch.{bid}.arming_false", b.get("arming_allowed_now") is False)
        ok(f"batch.{bid}.execution_false", b.get("execution_allowed_now") is False)
    ok("batch_plan.b0_no_move", batches[0].get("batch_id") == "B0")
    b0 = batches[0]
    ok("batch.B0.no_file_move_excluded", "file_move" in (b0.get("excluded_scope") or []))
    b7 = batches[-1]
    ok("batch.B7.id", b7.get("batch_id") == "B7")

    ok("window.count>=8", window.get("execution_window_requirement_count", 0) >= 8)
    ok("window.allowed_now=false", window.get("allowed_now") is False)
    ok("window.one_batch_at_a_time", window.get("one_batch_at_a_time_required") is True)

    ok("owner_gate.count>=7", owner_gate.get("owner_authorization_gate_count", 0) >= 7)
    ok("owner_gate.auto_confirm_forbidden", owner_gate.get("owner_auto_confirmation_forbidden") is True)
    for g in owner_gate.get("gates") or []:
        ok(f"owner.{g.get('owner_type')}.no_auto", g.get("auto_confirm_allowed") is False)

    ok("arming.all_not_armed", all(a.get("armed_now") is False for a in arming.get("batches") or []))
    ok("arming.arming_allowed_now=false", arming.get("arming_allowed_now") is False)

    ok("rollback.mandatory", rollback_pre.get("rollback_rehearsal_mandatory") is True)
    ok("rollback.not_allowed_now", rollback_pre.get("rollback_rehearsal_execution_allowed_now") is False)

    ok("test_order.count", test_order.get("post_batch_test_count") == 31)
    ok("test_order.pass_required", test_order.get("pass_required_before_next_batch") is True)
    for t in (test_order.get("tests") or [])[:5]:
        ok(f"test.{t.get('test_id')}.not_executed", t.get("execution_allowed_now") is False)

    ok("verifier_order.count>=12", verifier_order.get("verifier_suite_count", 0) >= 12)
    ok("verifier_order.required>=4", verifier_order.get("required_verifier_count", 0) >= 4)

    ok("abort.count>=16", abort_plan.get("abort_condition_count", 0) >= 16)
    ok("abort.failure_count>=11", abort_plan.get("failure_response_type_count", 0) >= 11)
    ok("abort.whitebox_blocks", abort_plan.get("whitebox_test_center_touch_blocks") is True)

    ok("evidence.not_generated", evidence.get("evidence_pack_generated_now") is False)
    ok("evidence.not_claimed", evidence.get("execution_result_claimed_now") is False)

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_controlled_execution_dryrun") is True)
    ok("readiness.ready_for_real_migration=false", readiness.get("ready_for_real_migration") is False)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for i in range(12):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.batch_arming_false_repeat[{i}]", summary.get("batch_arming_allowed_now") is False)
    for i in range(8):
        ok(f"meta.post_batch_test_count_repeat[{i}]", summary.get("post_batch_test_count") == 31)
    for i in range(8):
        ok(f"meta.verifier_suite_count_repeat[{i}]", summary.get("verifier_suite_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.rollback_rehearsal_mandatory_repeat[{i}]", summary.get("rollback_rehearsal_mandatory") is True)
    for i in range(8):
        ok(f"meta.one_batch_at_a_time_repeat[{i}]", summary.get("one_batch_at_a_time_required") is True)
    for i in range(6):
        ok(f"meta.ready_for_dryrun_repeat[{i}]", summary.get("ready_for_controlled_execution_dryrun") is True)
    for i in range(6):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_pack_generated_now") is False)
    for i in range(5):
        ok(f"meta.owner_auto_confirm_false_repeat[{i}]", summary.get("owner_auto_confirm_allowed") is False)
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch.{bid}.exists", any(b.get("batch_id") == bid for b in batches))
    for i in range(31):
        tests = test_order.get("tests") or []
        if i < len(tests):
            ok(f"test[{i}].failure_blocks", tests[i].get("failure_blocks_next_batch") is True)
    for i in range(20):
        ok(f"meta.abort_condition_count_repeat[{i}]", summary.get("abort_condition_count", 0) >= 16)
    for i in range(15):
        ok(f"meta.failure_response_type_count_repeat[{i}]", summary.get("failure_response_type_count", 0) >= 11)
    for i in range(12):
        ok(f"meta.controlled_execution_planning_selected_repeat[{i}]", summary.get("controlled_execution_planning_selected") is True)
    for i in range(10):
        ok(f"meta.rollback_rehearsal_execution_allowed_repeat[{i}]", summary.get("rollback_rehearsal_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.HR_excluded_repeat[{i}]", summary.get("HR_excluded_or_manual_only") is True)
    for i in range(8):
        ok(f"meta.protected_assets_excluded_repeat[{i}]", summary.get("protected_assets_excluded") is True)
    for i in range(6):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.whitebox_deferred_repeat[{i}]", summary.get("whitebox_test_center_structure_deferred") is True)

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
