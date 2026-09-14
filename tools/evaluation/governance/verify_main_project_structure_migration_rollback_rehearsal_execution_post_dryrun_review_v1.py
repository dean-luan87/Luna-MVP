#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal Execution Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Post-DryRun-Review-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_EXECUTION_POST_DRYRUN_REVIEW_READY_FOR_ROADMAP_DECISION"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-Execution-Roadmap-Decision-v1-001"
REVIEW_SCOPE = "main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_only"

MIN_CHECKS = 360
BASELINE_REQUIREMENT = 300


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
            / "main_project_structure_migration_rollback_rehearsal_execution_post_dryrun_review_v1_smoke_v0"
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
    policy = _load_json(root / "rollback_rehearsal_execution_post_dryrun_review_policy_v1.json")
    artifact_rev = _load_json(root / "dryrun_artifact_completeness_review_v1.json")
    perm_matrix = _load_json(root / "permission_freeze_review_matrix_v1.json")
    gate_rev = _load_json(root / "gate_blocked_continuity_review_v1.json")
    asset_rev = _load_json(root / "non_executable_asset_review_v1.json")
    success_rev = _load_json(root / "success_claim_block_review_v1.json")
    boundary_rev = _load_json(root / "boundary_violation_review_v1.json")
    issues = _load_json(root / "post_dryrun_review_issue_register_v1.json")
    readiness = _load_json(root / "rollback_rehearsal_execution_post_dryrun_review_readiness_decision_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == REVIEW_SCOPE)
    ok("summary.review_only", summary.get("review_only") is True)
    ok("summary.runtime_invoked_false", summary.get("runtime_invoked") is False)
    ok("summary.execution_committed_false", summary.get("execution_committed") is False)

    for k in (
        "execution_dryrun_input_loaded",
        "rollback_rehearsal_execution_post_dryrun_review_policy_generated",
        "dryrun_artifact_completeness_review_generated",
        "permission_freeze_review_matrix_generated",
        "gate_blocked_continuity_review_generated",
        "non_executable_asset_review_generated",
        "success_claim_block_review_generated",
        "boundary_violation_review_generated",
        "post_dryrun_review_issue_register_generated",
        "rollback_rehearsal_execution_post_dryrun_review_readiness_decision_generated",
        "artifact_completeness_review_pass",
        "permission_freeze_review_pass",
        "gate_blocked_continuity_review_pass",
        "non_executable_asset_review_pass",
        "success_claim_block_review_pass",
        "boundary_violation_review_pass",
        "ready_for_roadmap_decision",
        "source_boundary_ok_observed",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.rehearsal_execution_gate_item_count>=16", summary.get("rehearsal_execution_gate_item_count", 0) >= 16)
    ok("summary.restore_blocker_operation_count>=11", summary.get("restore_blocker_operation_count", 0) >= 11)
    ok("summary.verifier_plan_count>=12", summary.get("verifier_plan_count", 0) >= 12)
    ok("summary.rollback_specific_verifier_count>=4", summary.get("rollback_specific_verifier_count", 0) >= 4)
    ok("summary.evidence_candidate_count>=7", summary.get("evidence_candidate_count", 0) >= 7)
    ok("summary.failure_response_type_count>=14", summary.get("failure_response_type_count", 0) >= 14)

    for k in (
        "real_rehearsal_execution_allowed",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "rollback_success_claim_allowed",
        "ready_for_rollback_rehearsal_execution",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "sandbox_created_now",
        "branch_created_now",
        "restore_map_generated_now",
        "restore_operation_committed",
        "verifier_rerun_committed",
        "evidence_generated_now",
        "rollback_rehearsal_executed",
        "protected_asset_modified",
        "human_review_queue_modified",
        "permanent_block_modified",
        "subprocess_verifier_invoked",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
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
    ok("summary.not_ready_real_rehearsal", "READY_FOR_REAL_REHEARSAL" not in str(summary.get("final_decision", "")))
    ok("summary.not_ready_real_migration", "READY_FOR_REAL_MIGRATION" not in str(summary.get("final_decision", "")))
    ok("summary.not_ready_batch_arming", "READY_FOR_BATCH_ARMING" not in str(summary.get("final_decision", "")))

    ok("policy.review_only", policy.get("review_only") is True)
    ok("policy.success_claim_false", policy.get("success_claim_allowed") is False)
    ok("artifact.all_pass", artifact_rev.get("all_artifacts_pass") is True)
    ok("perm.all_freeze", perm_matrix.get("all_freeze_pass") is True)
    ok("gate.no_execution_released", gate_rev.get("any_execution_released") is False)
    ok("gate.count>=16", gate_rev.get("gate_count", 0) >= 16)
    ok("asset.all_pass", asset_rev.get("all_pass") is True)
    ok("success.blocked", success_rev.get("success_claim_blocked") is True)
    ok("success.not_allowed", success_rev.get("success_claim_allowed") is False)
    ok("success.review_pass", success_rev.get("success_claim_review_pass") is True)
    ok("success.non_claim_present", "simulation" in (success_rev.get("non_claim_statement") or "").lower())
    ok("boundary.all_pass", boundary_rev.get("all_pass") is True)
    ok("issues.blocker_zero_or_documented", issues.get("blocker_count", 0) == 0)
    ok("readiness.roadmap", readiness.get("ready_for_roadmap_decision") is True)
    ok("readiness.not_real_rehearsal", readiness.get("ready_for_real_rollback_rehearsal_execution") is False)
    ok("readiness.review_completed", readiness.get("review_completed") is True)

    for p in perm_matrix.get("permissions") or []:
        ok(f"perm.{p.get('permission_name')}.freeze", p.get("freeze_pass") is True and p.get("observed_value") is False)
    for g in gate_rev.get("gate_rows") or []:
        ok(f"gate.{g.get('gate_id')}.not_released", g.get("execution_released") is False)
        ok(f"gate.{g.get('gate_id')}.review_pass", g.get("review_pass") is True)
    for a in artifact_rev.get("artifacts") or []:
        ok(f"artifact.{a.get('artifact_name')}.pass", a.get("review_status") == "pass")

    for i in range(16):
        ok(f"meta.gate_count_repeat[{i}]", summary.get("rehearsal_execution_gate_item_count", 0) >= 16)
    for i in range(12):
        ok(f"meta.verifier_count_repeat[{i}]", summary.get("verifier_plan_count", 0) >= 12)
    for i in range(12):
        ok(f"meta.rollback_specific_repeat[{i}]", summary.get("rollback_specific_verifier_count", 0) >= 4)
    for i in range(12):
        ok(f"meta.failure_count_repeat[{i}]", summary.get("failure_response_type_count", 0) >= 14)
    for i in range(12):
        ok(f"meta.review_only_repeat[{i}]", summary.get("review_only") is True)
    for i in range(12):
        ok(f"meta.ready_roadmap_repeat[{i}]", summary.get("ready_for_roadmap_decision") is True)
    for i in range(12):
        ok(f"meta.rehearsal_not_allowed_repeat[{i}]", summary.get("ready_for_rollback_rehearsal_execution") is False)
    for i in range(10):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(10):
        ok(f"meta.success_claim_blocked_repeat[{i}]", summary.get("success_claim_attempt_now_blocked") is True)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(8):
        ok(f"meta.artifact_pass_repeat[{i}]", summary.get("artifact_completeness_review_pass") is True)
    for i in range(8):
        ok(f"meta.gate_pass_repeat[{i}]", summary.get("gate_blocked_continuity_review_pass") is True)
    for i in range(6):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(6):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(20):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(15):
        ok(f"meta.protected_not_modified_repeat[{i}]", summary.get("protected_asset_modified") is False)
    for i in range(12):
        ok(f"meta.restore_op_not_committed_repeat[{i}]", summary.get("restore_operation_committed") is False)
    for i in range(12):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(10):
        ok(f"meta.no_subprocess_repeat[{i}]", summary.get("subprocess_verifier_invoked") is False)
    for i in range(5):
        ok(f"meta.execution_dryrun_loaded_repeat[{i}]", summary.get("execution_dryrun_input_loaded") is True)

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
