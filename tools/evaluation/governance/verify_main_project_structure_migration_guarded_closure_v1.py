#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Guarded Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Closure-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Roadmap-Decision-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_guarded_closure_only"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220

EXCLUSION_KEYS = (
    "protected_assets_excluded_from_migration",
    "permanent_blocks_excluded_from_migration",
    "human_review_items_excluded_or_manual_only",
    "eval_out_outputs_excluded",
    "verifier_reports_excluded",
    "go_no_go_packs_excluded",
    "correction_records_excluded",
    "historical_test_logs_excluded",
    "phase_records_excluded",
    "whitebox_test_center_physical_restructure_excluded",
    "developer_backend_full_architecture_excluded",
    "future_reserved_module_finalization_excluded",
    "runtime_behavior_changes_excluded",
    "client_runtime_changes_excluded",
)

BOUNDARY_FREEZE_KEYS = (
    "no-real-migration",
    "no-file-move",
    "no-file-delete",
    "no-file-rename",
    "no-module-merge",
    "no-docs-modification",
    "no-readme-modification",
    "no-phase-verdict-table-modification",
    "no-post-migration-test-execution",
    "no-rollback-execution",
    "no-human-owner-confirmation",
    "no-human-review-execution",
    "no-protected-asset-modification",
    "no-permanent-block-release",
    "no-whitebox-structure-design",
    "no-test-center-structure-design",
    "no-developer-backend-finalization",
    "no-future-module-finalization",
    "no-runtime",
    "no-write",
    "no-action",
    "no-speech",
)


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_guarded_closure_v1_smoke_v0"),
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
    closure_summary = _load_json(root / "main_project_structure_migration_guarded_closure_summary.json")
    completed = _load_json(root / "completed_phase_matrix.json")
    decision = _load_json(root / "guarded_migration_closure_decision_summary.json")
    exclusion = _load_json(root / "exclusion_carryover_freeze.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "guarded_migration_non_claims_register.json")
    correction = _load_json(root / "correction_record.json")
    deferred = _load_json(root / "deferred_guarded_migration_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    required_outputs = (
        "summary.json",
        "input_root_matrix.json",
        "main_project_structure_migration_guarded_closure_summary.json",
        "completed_phase_matrix.json",
        "guarded_migration_closure_decision_summary.json",
        "exclusion_carryover_freeze.json",
        "closure_boundary_freeze.json",
        "guarded_migration_non_claims_register.json",
        "correction_record.json",
        "deferred_guarded_migration_action_pool.json",
        "closure_readiness_gate.json",
        "next_phase_recommendation.json",
        "no_file_move_boundary_report.json",
        "no_delete_boundary_report.json",
        "no_runtime_boundary_report.json",
        "no_write_boundary_report.json",
    )
    for fname in required_outputs:
        ok(f"artifact.exists.{fname}", (root / fname).is_file())

    idx = {r.get("intake_id"): r for r in input_matrix.get("rows", [])}
    for intake_id in (
        "guarded_post_review",
        "guarded_dryrun",
        "guarded_planning",
        "readiness",
        "roadmap_decision",
        "pahr_closure",
        "consolidation_closure",
        "structure_map",
        "gate_taxonomy",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == CLOSURE_SCOPE)

    for k in (
        "guarded_post_review_input_loaded",
        "guarded_dryrun_input_loaded",
        "guarded_planning_input_loaded",
        "readiness_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
        "completed_phase_matrix_generated",
        "guarded_migration_closure_decision_summary_generated",
        "exclusion_carryover_freeze_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "correction_record_generated",
        "deferred_action_pool_generated",
        "closure_readiness_gate_generated",
        "guarded_readiness_closed",
        "guarded_planning_closed",
        "guarded_dryrun_closed",
        "guarded_post_review_closed",
        "guarded_migration_chain_closed",
        "closure_allowed",
        "gate_sequence_pass",
        "human_approval_is_placeholder_only",
        "rollback_checkpoint_per_batch",
        "boundary_ok",
        "no_runtime_executed",
        "no_new_runtime_enabled",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.completed_phase_count>=4", summary.get("completed_phase_count", 0) >= 4)
    ok("summary.batch_count", summary.get("batch_count") == 8)
    ok("summary.simulated_pass_batch_count", summary.get("simulated_pass_batch_count") == 8)
    ok("summary.simulated_blocked_batch_count", summary.get("simulated_blocked_batch_count") == 0)
    ok("summary.gate_sequence_count", summary.get("gate_sequence_count") == 10)
    ok("summary.migration_candidate_scope_count", summary.get("migration_candidate_scope_count") == 8)
    ok("summary.migration_exclusion_scope_count>=17", summary.get("migration_exclusion_scope_count", 0) >= 17)
    ok("summary.post_migration_test_count", summary.get("post_migration_test_count") == 31)
    ok("summary.bound_test_count", summary.get("bound_test_count") == 31)
    ok("summary.unbound_test_count", summary.get("unbound_test_count") == 0)
    ok("summary.executed_test_count", summary.get("executed_test_count") == 0)
    ok("summary.rollback_checkpoint_count", summary.get("rollback_checkpoint_count") == 8)

    for k in (
        "candidate_scopes_execution_allowed",
        "rollback_executed",
        "final_owner_human_confirmed",
        "approval_executed",
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
        "docs_modified_by_closure",
        "readme_modified_by_closure",
        "phase_verdict_table_modified_by_closure",
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

    ok("summary.human_approval_checkpoint_required", summary.get("human_approval_checkpoint_required") is True)
    ok("summary.correction_record_status", summary.get("correction_record_status") == "recorded")
    ok("summary.correction_semantic_impact", summary.get("correction_semantic_impact") == "no_permission_granted")
    ok("summary.correction_boundary_impact", summary.get("correction_boundary_impact") == "no_boundary_change")
    ok("summary.correction_runtime_impact", summary.get("correction_runtime_impact") == "none")
    ok("summary.correction_migration_permission_impact", summary.get("correction_migration_permission_impact") == "none")
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    for k in EXCLUSION_KEYS:
        ok(f"summary.{k}", summary.get(k) is True)
        ok(f"exclusion.{k}", exclusion.get(k) is True)

    ok("exclusion.closure_boundary_files_excluded", exclusion.get("closure_boundary_files_excluded") is True)
    ok("exclusion.non_claims_registers_excluded", exclusion.get("non_claims_registers_excluded") is True)

    for k in BOUNDARY_FREEZE_KEYS:
        ok(f"boundary_freeze.{k}", boundary_freeze.get(k) is True)

    ok("decision.batch_count", decision.get("batch_count") == 8)
    ok("decision.simulated_pass_batch_count", decision.get("simulated_pass_batch_count") == 8)
    ok("decision.gate_sequence_pass", decision.get("gate_sequence_pass") is True)
    ok("decision.closure_allowed", decision.get("closure_allowed") is True)
    ok("decision.real_migration_allowed=false", decision.get("real_migration_allowed") is False)
    ok("decision.human_review_case_count", decision.get("human_review_case_count") == 240)
    ok("decision.permanent_block_case_count", decision.get("permanent_block_case_count") == 914)

    ok("completed.phase_count", completed.get("completed_phase_count") == 4)
    for i, phase in enumerate(completed.get("phases") or []):
        ok(f"completed[{i}].status", phase.get("status") == "GO")
        ok(f"completed[{i}].file_move=false", phase.get("actual_file_move_executed") is False)
        ok(f"completed[{i}].tests_executed=false", phase.get("post_migration_tests_executed") is False)
        ok(f"completed[{i}].runtime=false", phase.get("runtime_enabled") is False)

    ok("closure_summary.closure_id", bool(closure_summary.get("closure_id")))
    ok("closure_summary.completed_phase_count", closure_summary.get("completed_phase_count") == 4)
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)

    ok("correction.source_phase", "Post-DryRun-Review" in str(correction.get("source_phase", "")))
    ok("correction.semantic_impact", correction.get("semantic_impact") == "no_permission_granted")
    ok("correction.boundary_impact", correction.get("boundary_impact") == "no_boundary_change")
    ok("correction.verification_status", correction.get("verification_status") == "GO")
    ok("correction.rollback_still_blocked", correction.get("rollback_execution_still_blocked") is True)
    ok("correction.dryrun_semantic_unchanged", correction.get("dryrun_semantic_unchanged") is True)

    ok("non_claims.count>=10", len(non_claims.get("non_claims") or []) >= 10)
    for i, claim in enumerate(non_claims.get("non_claims") or []):
        ok(f"non_claims[{i}].non_empty", bool(claim))

    ok("deferred.count>=15", deferred.get("deferred_action_count", 0) >= 15)
    ok("deferred.real_migration_started=false", deferred.get("real_migration_started") is False)
    for i, item in enumerate(deferred.get("deferred_actions") or []):
        ok(f"deferred[{i}].auto_execute_allowed=false", item.get("auto_execute_allowed") is False)

    ok("readiness_gate.ready_for_closure", readiness_gate.get("ready_for_closure") is True)
    ok("readiness_gate.blockers_empty", readiness_gate.get("blockers") == [])

    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("no_move.actual_file_move_executed=false", no_move.get("actual_file_move_executed") is False)
    ok("no_delete.actual_file_delete_executed=false", no_delete.get("actual_file_delete_executed") is False)
    ok("no_runtime.runtime_enabled=false", no_runtime.get("runtime_enabled") is False)
    ok("no_write.world_model_written=false", no_write.get("world_model_written") is False)

    for phrase in (
        "可真实搬迁",
        "post-migration tests",
        "owner 已确认",
        "protected / HR / DnAE",
    ):
        found = any(phrase in str(c) for c in (non_claims.get("non_claims") or []))
        ok(f"non_claims.contains.{phrase}", found)

    for i in range(12):
        ok(f"meta.closure_scope_repeat[{i}]", summary.get("closure_scope") == CLOSURE_SCOPE)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(5):
        ok(f"meta.real_migration_allowed_repeat[{i}]", summary.get("real_migration_allowed") is False)

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
