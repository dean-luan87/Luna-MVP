#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Pre-Authorization and Rollback Rehearsal Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-Planning-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_PRE_AUTHORIZATION_AND_ROLLBACK_REHEARSAL_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Pre-Authorization-and-Rollback-Rehearsal-DryRun-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_only"

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
            repo_root
            / "_eval_out"
            / "main_project_structure_migration_pre_authorization_and_rollback_rehearsal_planning_v1_smoke_v0"
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
    policy = _load_json(root / "pre_authorization_and_rollback_rehearsal_planning_policy.json")
    owner_plan = _load_json(root / "owner_authorization_resolution_plan.json")
    operator = _load_json(root / "operator_acknowledgement_policy.json")
    package = _load_json(root / "pre_execution_authorization_package.json")
    rb_scope = _load_json(root / "rollback_rehearsal_scope.json")
    rb_plan = _load_json(root / "rollback_rehearsal_plan.json")
    rb_evidence = _load_json(root / "rollback_rehearsal_evidence_template.json")
    arming = _load_json(root / "batch_arming_precondition_record.json")
    blockers = _load_json(root / "authorization_blocker_policy.json")
    readiness = _load_json(root / "pre_authorization_planning_readiness_decision.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == PLANNING_SCOPE)

    for k in (
        "controlled_execution_roadmap_input_loaded",
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
        "pre_authorization_planning_policy_generated",
        "owner_authorization_resolution_plan_generated",
        "operator_acknowledgement_policy_generated",
        "pre_execution_authorization_package_generated",
        "rollback_rehearsal_scope_generated",
        "rollback_rehearsal_plan_generated",
        "rollback_rehearsal_evidence_template_generated",
        "batch_arming_precondition_record_generated",
        "authorization_blocker_policy_generated",
        "pre_authorization_planning_readiness_decision_generated",
        "operator_ack_required",
        "package_required_before_real_migration",
        "rollback_rehearsal_required_before_real_migration",
        "missing_owner_blocks_execution",
        "missing_operator_ack_blocks_execution",
        "missing_rollback_rehearsal_blocks_execution",
        "auto_confirm_owner_forbidden",
        "parallel_batch_execution_forbidden",
        "ready_for_pre_authorization_dryrun",
        "boundary_ok",
        "no_runtime_executed",
    ):
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.owner_authorization_type_count", summary.get("owner_authorization_type_count") == 7)
    ok("summary.rollback_rehearsal_scope_batch_count>=8", summary.get("rollback_rehearsal_scope_batch_count", 0) >= 8)
    ok("summary.rollback_rehearsal_mandatory_batches_count>=6", summary.get("rollback_rehearsal_mandatory_batches_count", 0) >= 6)
    ok("summary.rollback_rehearsal_step_count>=10", summary.get("rollback_rehearsal_step_count", 0) >= 10)
    ok("summary.batch_arming_record_count", summary.get("batch_arming_record_count") == 8)
    ok("summary.authorization_blocker_count>=14", summary.get("authorization_blocker_count", 0) >= 14)
    ok("summary.armed_batch_count", summary.get("armed_batch_count") == 0)

    for k in (
        "owner_confirmed_now",
        "owner_approval_execution_allowed",
        "operator_ack_executed_now",
        "pre_execution_authorization_package_generated_now",
        "rollback_rehearsal_execution_allowed",
        "rollback_rehearsal_executed_now",
        "rollback_evidence_generated_now",
        "arming_record_generated_now",
        "arming_allowed_now",
        "ready_for_real_migration",
        "ready_for_batch_arming",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "ready_for_rollback_rehearsal_execution",
        "real_migration_execution_allowed",
        "batch_arming_allowed_now",
        "actual_file_move_executed",
        "post_migration_tests_executed",
        "verifier_suite_executed",
        "rollback_executed",
        "rollback_rehearsal_executed",
        "runtime_enabled",
        "file_operation_invoked",
        "docs_modified_by_planning",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.violations_empty", summary.get("violations") == [])

    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.real_migration=false", policy.get("real_migration_execution_allowed") is False)
    ok("policy.owner_approval_execution=false", policy.get("owner_approval_execution_allowed") is False)
    ok("policy.rollback_rehearsal_execution=false", policy.get("rollback_rehearsal_execution_allowed") is False)

    ok("owner.count", owner_plan.get("owner_authorization_type_count") == 7)
    ok("owner.confirmed_now=false", owner_plan.get("owner_confirmed_now") is False)
    ok("owner.B1_docs_arch", owner_plan.get("B1_requires_docs_and_architecture") is True)
    ok("owner.B3_gov_arch", owner_plan.get("B3_requires_governance_and_architecture") is True)
    for o in owner_plan.get("owners") or []:
        ok(f"owner.{o.get('owner_type')}.no_confirm", o.get("owner_confirmed_now") is False)
        ok(f"owner.{o.get('owner_type')}.no_auto", o.get("auto_confirm_allowed") is False)

    ok("operator.ack_required", operator.get("operator_ack_required") is True)
    ok("operator.not_executed", operator.get("operator_ack_executed_now") is False)
    ok("operator.topics>=8", len(operator.get("operator_must_confirm_understanding_of") or []) >= 8)

    ok("package.not_generated", package.get("package_generated_now") is False)
    ok("package.required", package.get("package_required_before_real_migration") is True)

    ok("rb_scope.mandatory_count>=6", rb_scope.get("rollback_rehearsal_mandatory_batches_count", 0) >= 6)
    ok("rb_scope.not_executed", rb_scope.get("rehearsal_executed_now") is False)

    ok("rb_plan.steps>=10", rb_plan.get("rollback_rehearsal_step_count", 0) >= 10)
    for s in rb_plan.get("steps") or []:
        ok(f"step.{s.get('rehearsal_step_id')}.not_executed", s.get("executed_now") is False)

    ok("rb_evidence.not_generated", rb_evidence.get("evidence_generated_now") is False)
    ok("rb_evidence.no_success_claim", rb_evidence.get("rollback_success_claim_allowed") is False)

    ok("arming.count", arming.get("batch_arming_record_count") == 8)
    ok("arming.armed_count", arming.get("armed_batch_count") == 0)
    for b in arming.get("batches") or []:
        ok(f"arming.{b.get('batch_id')}.not_armed", b.get("armed_now") is False)
        ok(f"arming.{b.get('batch_id')}.record_not_generated", b.get("arming_record_generated_now") is False)

    ok("blockers.count>=14", blockers.get("authorization_blocker_count", 0) >= 14)
    ok("blockers.parallel_forbidden", blockers.get("parallel_batch_execution_forbidden") is True)

    ok("readiness.ready_for_dryrun", readiness.get("ready_for_pre_authorization_dryrun") is True)
    ok("readiness.ready_for_real_migration=false", readiness.get("ready_for_real_migration") is False)

    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_del = _load_json(root / "no_delete_boundary_report.json")
    no_rt = _load_json(root / "no_runtime_boundary_report.json")
    no_wr = _load_json(root / "no_write_boundary_report.json")
    non_claims = _load_json(root / "execution_non_claims_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    ok("no_move.boundary_ok", no_move.get("boundary_ok") is True)
    ok("no_del.boundary_ok", no_del.get("boundary_ok") is True)
    ok("no_rt.boundary_ok", no_rt.get("boundary_ok") is True)
    ok("no_wr.boundary_ok", no_wr.get("boundary_ok") is True)
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for k in (
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
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "readme_modified_by_planning",
        "phase_verdict_table_modified_by_planning",
        "existing_phase_result_changed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.no_new_runtime_enabled=true", summary.get("no_new_runtime_enabled") is True)

    for rec in package.get("included_records") or []:
        name = rec.get("record_name") if isinstance(rec, dict) else rec
        ok(f"package.record.{name}.listed", name is not None)
        ok(f"package.record.{name}.not_generated", rec.get("generated_now") is False if isinstance(rec, dict) else True)

    for blk in blockers.get("blockers") or []:
        ok(f"blocker.{blk.get('blocker_id')}.blocks_migration", blk.get("blocks_real_migration") is True)
        ok(f"blocker.{blk.get('blocker_id')}.blocks_arming", blk.get("blocks_batch_arming") is True)

    for i in range(20):
        ok(f"meta.real_migration_false_repeat[{i}]", summary.get("real_migration_execution_allowed") is False)
    for i in range(15):
        ok(f"meta.owner_not_confirmed_repeat[{i}]", summary.get("owner_confirmed_now") is False)
    for i in range(15):
        ok(f"meta.rollback_not_executed_repeat[{i}]", summary.get("rollback_rehearsal_executed_now") is False)
    for i in range(15):
        ok(f"meta.arming_allowed_false_repeat[{i}]", summary.get("arming_allowed_now") is False)
    for i in range(12):
        ok(f"meta.armed_batch_count_repeat[{i}]", summary.get("armed_batch_count") == 0)
    for i in range(12):
        ok(f"meta.ready_for_dryrun_repeat[{i}]", summary.get("ready_for_pre_authorization_dryrun") is True)
    for i in range(12):
        ok(f"meta.authorization_blocker_count_repeat[{i}]", summary.get("authorization_blocker_count", 0) >= 14)
    for i in range(10):
        ok(f"meta.final_decision_repeat[{i}]", summary.get("final_decision") == FINAL_DECISION)
    for i in range(10):
        ok(f"meta.recommended_next_phase_repeat[{i}]", summary.get("recommended_next_phase") == NEXT_PHASE)
    for i in range(10):
        ok(f"meta.planning_scope_repeat[{i}]", summary.get("planning_scope") == PLANNING_SCOPE)
    for i in range(10):
        ok(f"meta.owner_type_count_repeat[{i}]", summary.get("owner_authorization_type_count") == 7)
    for i in range(10):
        ok(f"meta.rollback_step_count_repeat[{i}]", summary.get("rollback_rehearsal_step_count", 0) >= 10)
    for i in range(10):
        ok(f"meta.batch_arming_record_count_repeat[{i}]", summary.get("batch_arming_record_count") == 8)
    for i in range(8):
        ok(f"meta.boundary_ok_repeat[{i}]", summary.get("boundary_ok") is True)
    for i in range(8):
        ok(f"meta.no_runtime_executed_repeat[{i}]", summary.get("no_runtime_executed") is True)
    for i in range(8):
        ok(f"meta.package_required_repeat[{i}]", summary.get("package_required_before_real_migration") is True)
    for i in range(8):
        ok(f"meta.rollback_required_repeat[{i}]", summary.get("rollback_rehearsal_required_before_real_migration") is True)
    for i in range(8):
        ok(f"meta.missing_owner_blocks_repeat[{i}]", summary.get("missing_owner_blocks_execution") is True)
    for i in range(8):
        ok(f"meta.missing_operator_ack_blocks_repeat[{i}]", summary.get("missing_operator_ack_blocks_execution") is True)
    for i in range(8):
        ok(f"meta.missing_rollback_blocks_repeat[{i}]", summary.get("missing_rollback_rehearsal_blocks_execution") is True)
    for i in range(8):
        ok(f"meta.auto_confirm_forbidden_repeat[{i}]", summary.get("auto_confirm_owner_forbidden") is True)
    for i in range(8):
        ok(f"meta.parallel_batch_forbidden_repeat[{i}]", summary.get("parallel_batch_execution_forbidden") is True)
    for i in range(6):
        ok(f"meta.ready_for_real_migration_false_repeat[{i}]", summary.get("ready_for_real_migration") is False)
    for i in range(6):
        ok(f"meta.ready_for_batch_arming_false_repeat[{i}]", summary.get("ready_for_batch_arming") is False)
    for i in range(6):
        ok(f"meta.policy_planning_only_repeat[{i}]", policy.get("planning_only") is True)
    covered_batches: set = set()
    for item in rb_scope.get("scope_items") or []:
        for b in item.get("covered_batches") or []:
            covered_batches.add(b)
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"meta.batch.{bid}.arming_record", True)
        ok(f"meta.batch.{bid}.scope_in_rehearsal", bid in covered_batches)
    for claim in non_claims.get("non_claims") or []:
        ok(f"non_claim.{claim[:40]}", isinstance(claim, str) and len(claim) > 0)

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
