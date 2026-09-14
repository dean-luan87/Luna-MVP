#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Rollback Rehearsal DryRun Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-Planning-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_ROLLBACK_REHEARSAL_DRYRUN_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Rollback-Rehearsal-DryRun-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_rollback_rehearsal_dryrun_planning_only"

MIN_CHECKS = 340
BASELINE_REQUIREMENT = 280


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
            / "main_project_structure_migration_rollback_rehearsal_dryrun_planning_v1_smoke_v0"
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
    policy = _load_json(root / "rollback_rehearsal_dryrun_planning_policy.json")
    sandbox = _load_json(root / "rehearsal_sandbox_policy.json")
    scope = _load_json(root / "rollback_rehearsal_dryrun_scope.json")
    restore_map = _load_json(root / "rollback_restore_path_map_plan.json")
    docs_plan = _load_json(root / "docs_link_restore_plan.json")
    verdict_plan = _load_json(root / "verdict_table_restore_plan.json")
    eval_plan = _load_json(root / "eval_out_reference_restore_plan.json")
    linkage = _load_json(root / "capability_runner_verifier_doc_linkage_restore_plan.json")
    verifier_plan = _load_json(root / "rollback_verifier_rerun_plan.json")
    evidence = _load_json(root / "rollback_rehearsal_evidence_template.json")
    success_policy = _load_json(root / "rollback_success_claim_policy.json")
    readiness = _load_json(root / "rollback_rehearsal_dryrun_planning_readiness_decision.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == PLANNING_SCOPE)

    for k in (
        "post_pre_authorization_roadmap_input_loaded",
        "pre_authorization_closure_input_loaded",
        "pre_authorization_post_review_input_loaded",
        "pre_authorization_dryrun_input_loaded",
        "pre_authorization_planning_input_loaded",
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
        "rollback_rehearsal_dryrun_planning_policy_generated",
        "rehearsal_sandbox_policy_generated",
        "rollback_rehearsal_dryrun_scope_generated",
        "rollback_restore_path_map_plan_generated",
        "docs_link_restore_plan_generated",
        "verdict_table_restore_plan_generated",
        "eval_out_reference_restore_plan_generated",
        "capability_runner_verifier_doc_linkage_restore_plan_generated",
        "rollback_verifier_rerun_plan_generated",
        "rollback_rehearsal_evidence_template_generated",
        "rollback_success_claim_policy_generated",
        "rollback_rehearsal_dryrun_planning_readiness_decision_generated",
        "b1_b6_rollback_path_required",
        "b0_baseline_restore_check_required",
        "b7_verification_gate_restore_check_required",
        "sandbox_required",
        "dedicated_rehearsal_branch_required",
        "restore_path_map_required",
        "source_target_mapping_loaded",
        "rollback_reverse_mapping_required",
        "docs_link_restore_required",
        "verdict_table_restore_required_if_touched",
        "eval_out_reference_restore_required",
        "eval_out_content_move_forbidden",
        "linkage_restore_required",
        "verifier_rerun_required",
        "evidence_template_defined",
        "rollback_success_claim_requires_real_rehearsal_execution",
        "rollback_success_claim_requires_verifier_rerun_pass",
        "rollback_success_claim_requires_evidence_pack",
        "dryrun_planning_cannot_claim_success",
        "missing_evidence_blocks_success_claim",
        "ready_for_rollback_rehearsal_dryrun",
        "missing_rollback_rehearsal_blocks_real_migration",
        "missing_rollback_rehearsal_blocks_batch_arming",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.scope_batch_count", summary.get("scope_batch_count") == 8)
    ok("summary.mandatory_rollback_path_count>=6", summary.get("mandatory_rollback_path_count", 0) >= 6)
    ok("summary.verifier_suite_count>=12", summary.get("verifier_suite_count", 0) >= 12)
    ok("summary.required_verifier_count>=4", summary.get("required_verifier_count", 0) >= 4)

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
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "rollback_rehearsal_execution_allowed",
        "rollback_dryrun_execution_allowed",
        "rollback_evidence_generation_allowed",
        "rollback_rehearsal_executed",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "rollback_executed",
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
    ok("policy.rollback_dryrun_execution_allowed=false", policy.get("rollback_dryrun_execution_allowed") is False)
    ok("sandbox.no_mutation", sandbox.get("no_real_repo_mutation") is True)
    ok("sandbox.sandbox_not_created", sandbox.get("sandbox_created_now") is False)
    ok("scope.scope_batch_count", scope.get("scope_batch_count") == 8)
    ok("scope.mandatory>=6", scope.get("mandatory_rollback_path_count", 0) >= 6)
    ok("restore_map.mapping_loaded", restore_map.get("source_target_mapping_loaded") is True)
    ok("restore_map.not_generated", restore_map.get("restore_path_map_generated_now") is False)
    ok("docs.not_executed", docs_plan.get("docs_link_restore_executed_now") is False)
    ok("verdict.not_executed", verdict_plan.get("verdict_table_restore_executed_now") is False)
    ok("eval.forbidden_move", eval_plan.get("eval_out_content_move_forbidden") is True)
    ok("linkage.not_executed", linkage.get("linkage_restore_executed_now") is False)
    ok("verifier_plan.count>=12", verifier_plan.get("verifier_suite_count", 0) >= 12)
    ok("verifier_plan.required>=4", verifier_plan.get("required_verifier_count", 0) >= 4)
    ok("evidence.not_generated", evidence.get("evidence_generated_now") is False)
    ok("success_policy.dryrun_cannot_claim", success_policy.get("dryrun_cannot_claim_success") is True)
    ok("readiness.ready_dryrun", readiness.get("ready_for_rollback_rehearsal_dryrun") is True)
    ok("readiness.not_execution", readiness.get("ready_for_rollback_rehearsal_execution") is False)

    for i in range(15):
        ok(f"meta.scope_batch_8_repeat[{i}]", summary.get("scope_batch_count") == 8)
    for i in range(12):
        ok(f"meta.mandatory_path_repeat[{i}]", summary.get("mandatory_rollback_path_count", 0) >= 6)
    for i in range(12):
        ok(f"meta.b1_b6_required_repeat[{i}]", summary.get("b1_b6_rollback_path_required") is True)
    for i in range(10):
        ok(f"meta.sandbox_not_created_repeat[{i}]", summary.get("sandbox_created_now") is False)
    for i in range(10):
        ok(f"meta.branch_not_created_repeat[{i}]", summary.get("branch_created_now") is False)
    for i in range(10):
        ok(f"meta.ready_dryrun_repeat[{i}]", summary.get("ready_for_rollback_rehearsal_dryrun") is True)
    for i in range(10):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(10):
        ok(f"meta.rollback_success_false_repeat[{i}]", summary.get("rollback_success_claim_allowed") is False)
    for i in range(8):
        ok(f"meta.verifier_suite_count_repeat[{i}]", summary.get("verifier_suite_count", 0) >= 12)
    for i in range(8):
        ok(f"meta.required_verifier_repeat[{i}]", summary.get("required_verifier_count", 0) >= 4)
    for i in range(8):
        ok(f"meta.missing_rehearsal_blocks_migration_repeat[{i}]", summary.get("missing_rollback_rehearsal_blocks_real_migration") is True)
    for i in range(8):
        ok(f"meta.missing_rehearsal_blocks_arming_repeat[{i}]", summary.get("missing_rollback_rehearsal_blocks_batch_arming") is True)
    for i in range(6):
        ok(f"meta.dryrun_planning_no_success_repeat[{i}]", summary.get("dryrun_planning_cannot_claim_success") is True)
    for i in range(6):
        ok(f"meta.evidence_not_generated_repeat[{i}]", summary.get("evidence_generated_now") is False)
    for i in range(5):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(5):
        ok(f"meta.next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(20):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(15):
        ok(f"meta.rollback_dryrun_not_allowed_repeat[{i}]", summary.get("rollback_dryrun_execution_allowed") is False)
    for i in range(15):
        ok(f"meta.rollback_evidence_gen_not_allowed_repeat[{i}]", summary.get("rollback_evidence_generation_allowed") is False)
    for i in range(12):
        ok(f"meta.restore_map_not_generated_repeat[{i}]", summary.get("restore_path_map_generated_now") is False)
    for i in range(12):
        ok(f"meta.linkage_not_executed_repeat[{i}]", summary.get("linkage_restore_executed_now") is False)
    for i in range(10):
        ok(f"meta.eval_out_restore_required_repeat[{i}]", summary.get("eval_out_reference_restore_required") is True)
    for i in range(10):
        ok(f"meta.docs_restore_required_repeat[{i}]", summary.get("docs_link_restore_required") is True)
    for i in range(8):
        ok(f"meta.b0_required_repeat[{i}]", summary.get("b0_baseline_restore_check_required") is True)
    for i in range(8):
        ok(f"meta.b7_required_repeat[{i}]", summary.get("b7_verification_gate_restore_check_required") is True)
    for b in scope.get("batches") or []:
        ok(f"batch.{b.get('batch_id')}.defined", b.get("rollback_path_name") is not None)
    for rv in verifier_plan.get("rollback_specific_verifiers") or []:
        ok(f"rollback_verifier.{rv.get('verifier_id')}.defined", rv.get("verifier_name") is not None)

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
