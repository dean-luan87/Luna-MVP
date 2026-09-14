#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Guarded Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001"
FINAL_DECISION = "MAIN_PROJECT_STRUCTURE_MIGRATION_GUARDED_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-DryRun-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_guarded_planning_only"

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
            repo_root / "_eval_out" / "main_project_structure_migration_guarded_planning_v1_smoke_v0"
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
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    policy = _load_json(root / "main_project_migration_guarded_planning_policy.json")
    batch_plan = _load_json(root / "guarded_migration_batch_plan.json")
    gate_seq = _load_json(root / "guarded_migration_gate_sequence.json")
    cand_scope = _load_json(root / "migration_candidate_scope.json")
    excl_scope = _load_json(root / "migration_exclusion_scope.json")
    pre_batch = _load_json(root / "pre_batch_check_policy.json")
    post_batch = _load_json(root / "post_batch_test_policy.json")
    rollback = _load_json(root / "rollback_checkpoint_policy.json")
    human_ap = _load_json(root / "human_approval_checkpoint_policy.json")
    matrix = _load_json(root / "post_migration_verification_matrix.json")
    decision = _load_json(root / "guarded_planning_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "readiness",
        "roadmap_decision",
        "pahr_closure",
        "consolidation_closure",
        "consolidation_post_review",
        "consolidation_dryrun",
        "consolidation_planning",
        "structure_map",
        "structure_governance",
        "gate_taxonomy",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.planning_scope", summary.get("planning_scope") == PLANNING_SCOPE)

    input_loaded = (
        "readiness_input_loaded",
        "roadmap_decision_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    )
    for k in input_loaded:
        ok(f"summary.{k}", summary.get(k) is True)

    generated = (
        "guarded_migration_policy_generated",
        "guarded_migration_batch_plan_generated",
        "guarded_migration_gate_sequence_generated",
        "migration_candidate_scope_generated",
        "migration_exclusion_scope_generated",
        "pre_batch_check_policy_generated",
        "post_batch_test_policy_generated",
        "rollback_checkpoint_policy_generated",
        "human_approval_checkpoint_policy_generated",
        "post_migration_verification_matrix_generated",
        "guarded_planning_readiness_decision_generated",
    )
    for k in generated:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.batch_count>=8", summary.get("batch_count", 0) >= 8)
    ok("summary.gate_sequence_count>=10", summary.get("gate_sequence_count", 0) >= 10)
    ok("summary.migration_candidate_scope_count>=8", summary.get("migration_candidate_scope_count", 0) >= 8)
    ok("summary.migration_exclusion_scope_count>=15", summary.get("migration_exclusion_scope_count", 0) >= 15)
    ok("summary.pre_batch_check_count>=10", summary.get("pre_batch_check_count", 0) >= 10)
    ok("summary.post_migration_test_count>=31", summary.get("post_migration_test_count", 0) >= 31)

    boundary_true = (
        "rollback_checkpoint_required",
        "human_approval_checkpoint_required",
        "protected_assets_excluded_from_migration",
        "permanent_blocks_excluded_from_migration",
        "human_review_items_excluded_or_manual_only",
        "whitebox_test_center_physical_restructure_excluded",
        "developer_backend_full_architecture_excluded",
        "future_reserved_module_finalization_excluded",
        "post_migration_tests_bound_to_batches",
        "ready_for_guarded_dryrun",
        "boundary_ok",
    )
    for k in boundary_true:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.post_migration_tests_executed=false", summary.get("post_migration_tests_executed") is False)

    for k in (
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "migration_execution_allowed",
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    for k in (
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
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

    ok("summary.no_runtime_executed", summary.get("no_runtime_executed") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.migration_execution_allowed=false", policy.get("migration_execution_allowed") is False)
    ok("policy.post_migration_tests_executed=false", policy.get("post_migration_tests_executed") is False)
    for ref in (
        "source_readiness_ref",
        "guarded_migration_batch_plan_ref",
        "guarded_migration_gate_sequence_ref",
        "post_migration_verification_matrix_ref",
    ):
        ok(f"policy.{ref}", bool(policy.get(ref)))

    batch_ids = set()
    for i, b in enumerate(batch_plan.get("batches") or []):
        bid = b.get("batch_id")
        batch_ids.add(bid)
        ok(f"batch[{i}].batch_id", bool(bid))
        ok(f"batch[{i}].execution_allowed_now=false", b.get("execution_allowed_now") is False)
        ok(f"batch[{i}].file_move_allowed_now=false", b.get("file_move_allowed_now") is False)
        ok(f"batch[{i}].delete_allowed_now=false", b.get("delete_allowed_now") is False)
        ok(f"batch[{i}].merge_allowed_now=false", b.get("merge_allowed_now") is False)
        ok(f"batch[{i}].rollback_checkpoint", bool(b.get("rollback_checkpoint")))
        ok(f"batch[{i}].required_post_tests", bool(b.get("required_post_tests")))
    for expected in ("B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"):
        ok(f"batch_plan.has_{expected}", expected in batch_ids)

    for i, g in enumerate(gate_seq.get("gates") or []):
        ok(f"gate[{i}].gate_id", bool(g.get("gate_id")))
        ok(f"gate[{i}].blocks_execution", g.get("blocks_execution") is True)
        ok(f"gate[{i}].audit_required", g.get("audit_required") is True)
        ok(f"gate[{i}].applies_to_batch", bool(g.get("applies_to_batch")))

    for i, c in enumerate(cand_scope.get("candidates") or []):
        ok(f"candidate[{i}].candidate_only", c.get("candidate_only") is True)
        ok(f"candidate[{i}].execution_allowed_now=false", c.get("execution_allowed_now") is False)
        ok(f"candidate[{i}].requires_guarded_execution_phase", c.get("requires_guarded_execution_phase") is True)

    ok("exclusion.protected_assets_excluded", excl_scope.get("protected_assets_excluded_from_migration") is True)
    ok("exclusion.whitebox_excluded", excl_scope.get("whitebox_test_center_physical_restructure_excluded") is True)
    for i, e in enumerate(excl_scope.get("exclusions") or []):
        ok(f"exclusion[{i}].included_in_migration_scope=false", e.get("included_in_migration_scope") is False)

    for i, c in enumerate(pre_batch.get("checks") or []):
        ok(f"pre_batch[{i}].executed_in_this_phase=false", c.get("executed_in_this_phase") is False)

    ok("post_batch.tests_executed=false", post_batch.get("post_migration_tests_executed") is False)
    for i, binding in enumerate(post_batch.get("batch_test_bindings") or []):
        ok(f"post_batch_binding[{i}].tests_executed=false", binding.get("tests_executed") is False)

    ok("rollback.rollback_checkpoint_required", rollback.get("rollback_checkpoint_required") is True)
    for i, cp in enumerate(rollback.get("checkpoints") or []):
        ok(f"rollback[{i}].rollback_executed=false", cp.get("rollback_executed") is False)
        ok(f"rollback[{i}].rerun_verifier_after_rollback", cp.get("rerun_verifier_after_rollback") is True)

    ok("human.no_automatic_owner_confirmation", human_ap.get("no_automatic_owner_confirmation") is True)
    ok("human.approval_required_before_real_migration", human_ap.get("approval_required_before_real_migration") is True)
    ok("human.hr_remain_excluded", human_ap.get("hr_unresolved_items_remain_excluded") is True)

    ok("matrix.post_migration_test_count>=31", matrix.get("post_migration_test_count", 0) >= 31)
    ok("matrix.tests_bound_to_batches", matrix.get("post_migration_tests_bound_to_batches") is True)
    group_ids = set()
    for i, t in enumerate(matrix.get("tests") or []):
        group_ids.add(t.get("test_group"))
        ok(f"matrix[{i}].execution_now=false", t.get("execution_now") is False)
        ok(f"matrix[{i}].required_after_migration", t.get("required_after_migration") is True)
        ok(f"matrix[{i}].related_batch", bool(t.get("related_batch")))
        ok(f"matrix[{i}].rollback_required_if_failed", t.get("rollback_required_if_failed") is True)
    for gid in ("A", "B", "C", "D", "E"):
        ok(f"matrix.group_{gid}_present", gid in group_ids)

    ok("decision.ready_for_guarded_dryrun", decision.get("ready_for_guarded_dryrun") is True)
    ok("decision.guarded_planning_verdict", decision.get("guarded_planning_verdict") == "GO")
    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("decision.blockers_empty", decision.get("blockers") == [])

    for report_name, report in (
        ("no_move", no_move),
        ("no_delete", no_delete),
        ("no_runtime", no_runtime),
        ("no_write", no_write),
    ):
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{report_name}.planning_only", report.get("planning_only") is True)

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
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
