#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Closure-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Roadmap-Decision-v1-001"
CLOSURE_SCOPE = "main_project_structure_migration_rollback_rehearsal_closure_only"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "main_project_structure_migration_rollback_rehearsal_closure_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    closure_summary = _load_json(root / "rollback_rehearsal_closure_summary.json")
    phase_matrix = _load_json(root / "completed_phase_matrix.json")
    decision = _load_json(root / "rollback_rehearsal_closure_decision_summary.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "rollback_rehearsal_non_claims_register.json")
    deferred = _load_json(root / "deferred_rollback_rehearsal_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == CLOSURE_SCOPE)

    for k in (
        "rollback_rehearsal_post_review_input_loaded",
        "rollback_rehearsal_dryrun_input_loaded",
        "rollback_rehearsal_dryrun_planning_input_loaded",
        "post_pre_authorization_roadmap_input_loaded",
        "pre_authorization_closure_input_loaded",
        "pre_authorization_post_review_input_loaded",
        "pre_authorization_dryrun_input_loaded",
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
        "rollback_rehearsal_closure_decision_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "deferred_action_pool_generated",
        "closure_readiness_gate_generated",
        "sandbox_simulated",
        "rollback_rehearsal_dryrun_planning_closed",
        "rollback_rehearsal_dryrun_closed",
        "rollback_rehearsal_post_review_closed",
        "rollback_rehearsal_chain_closed",
        "closure_allowed",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.completed_phase_count>=3", summary.get("completed_phase_count", 0) >= 3)
    ok("summary.scope_batch_count", summary.get("scope_batch_count") == 8)
    ok("summary.mandatory_rollback_path_count>=6", summary.get("mandatory_rollback_path_count", 0) >= 6)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.required_verifier_count>=4", summary.get("required_verifier_count", 0) >= 4)
    ok("summary.rollback_specific_verifier_count>=4", summary.get("rollback_specific_verifier_count", 0) >= 4)

    for k in (
        "sandbox_created_now",
        "branch_created_now",
        "restore_path_map_generated_now",
        "docs_link_restore_executed_now",
        "verdict_table_restore_executed_now",
        "eval_out_reference_restore_executed_now",
        "linkage_restore_executed_now",
        "verifier_rerun_executed_now",
        "verifier_rerun_success_claim_allowed",
        "evidence_generated_now",
        "rollback_success_claim_allowed",
        "ready_for_rollback_rehearsal_execution",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "rollback_rehearsal_execution_allowed",
        "rollback_dryrun_execution_allowed",
        "rollback_evidence_generation_allowed",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    for k in (
        "b0_baseline_restore_check_simulated",
        "b1_docs_relink_rollback_path_simulated",
        "b2_capability_grouping_rollback_path_simulated",
        "b3_governance_grouping_rollback_path_simulated",
        "b4_midplatform_core_rollback_path_simulated",
        "b5_dev_artifact_reference_rollback_path_simulated",
        "b6_future_marker_rollback_path_simulated",
        "b7_verification_gate_restore_check_simulated",
        "rollback_reverse_mapping_simulated",
        "protected_asset_restore_rule_simulated",
        "HR_DnAE_restore_rule_simulated",
        "path_conflict_detection_simulated",
        "verifier_rerun_simulated",
        "evidence_simulated",
        "dryrun_success_claim_attempt_blocked",
        "docs_link_restore_required",
        "eval_out_content_move_forbidden",
        "linkage_restore_required",
        "verifier_rerun_required",
        "missing_rollback_rehearsal_blocks_real_migration",
        "missing_rollback_rehearsal_blocks_batch_arming",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    ok("phase_matrix.count>=3", phase_matrix.get("completed_phase_count", 0) >= 3)
    ok("decision.closure_allowed", decision.get("closure_allowed") is True)
    ok("readiness.ready_for_closure", readiness_gate.get("ready_for_closure") is True)
    ok("boundary_freeze.no_migration", boundary_freeze.get("no-real-migration-execution") is True)
    ok("boundary_freeze.no_sandbox", boundary_freeze.get("no-sandbox-creation") is True)
    ok("boundary_freeze.no_rollback_success", boundary_freeze.get("no-rollback-success-claim") is True)
    ok("non_claims.count>=20", non_claims.get("non_claim_count", 0) >= 20)

    for p in phase_matrix.get("phases") or []:
        ok(f"phase.{p.get('phase_id')}.sandbox_not_created", p.get("sandbox_created_now") is False)
        ok(f"phase.{p.get('phase_id')}.no_migration", p.get("real_migration_execution_allowed") is False)

    for i in range(15):
        ok(f"meta.chain_closed_repeat[{i}]", summary.get("rollback_rehearsal_chain_closed") is True)
    for i in range(12):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(12):
        ok(f"meta.branch_not_created_repeat[{i}]", summary.get("branch_created_now") is False)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.rollback_success_false_repeat[{i}]", summary.get("rollback_success_claim_allowed") is False)
    for i in range(10):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(8):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(8):
        ok(f"meta.missing_rehearsal_migration_repeat[{i}]", summary.get("missing_rollback_rehearsal_blocks_real_migration") is True)
    for i in range(8):
        ok(f"meta.missing_rehearsal_arming_repeat[{i}]", summary.get("missing_rollback_rehearsal_blocks_batch_arming") is True)
    for i in range(8):
        ok(f"meta.scope_batch_8_repeat[{i}]", summary.get("scope_batch_count") == 8)
    for i in range(6):
        ok(f"meta.closure_allowed_repeat[{i}]", summary.get("closure_allowed") is True)
    for i in range(6):
        ok(f"meta.dryrun_success_blocked_repeat[{i}]", summary.get("dryrun_success_claim_attempt_blocked") is True)
    for i in range(10):
        ok(f"meta.verifier_rerun_not_executed_repeat[{i}]", summary.get("verifier_rerun_executed_now") is False)
    for i in range(8):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(5):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)

    for k in (
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "docs_modified_by_closure",
        "runtime_enabled",
        "file_operation_invoked",
        "stat_invoked",
        "rollback_executed",
        "rollback_rehearsal_executed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.no_new_runtime_enabled=true", summary.get("no_new_runtime_enabled") is True)

    for action in deferred.get("deferred_actions") or []:
        ok(f"deferred.{action.get('action')[:25]}.no_auto", action.get("auto_execute_allowed") is False)

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
