#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Main Project Structure Migration Readiness and Test Plan v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Main-Project-Structure-Migration-Readiness-and-Test-Plan-v1-001"
FINAL_DECISION = (
    "MAIN_PROJECT_STRUCTURE_MIGRATION_READINESS_AND_TEST_PLAN_READY_FOR_GUARDED_MIGRATION_PLANNING"
)
NEXT_PHASE = "Phase-Main-Project-Structure-Migration-Guarded-Planning-v1-001"
PLANNING_SCOPE = "main_project_structure_migration_readiness_and_test_plan_only"
HUMAN_REVIEW_CARRYOVER = 240
PERMANENT_BLOCK_CARRYOVER = 914

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
            repo_root / "_eval_out" / "main_project_structure_migration_readiness_and_test_plan_v1_smoke_v0"
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
    policy = _load_json(root / "main_project_migration_readiness_policy.json")
    gate = _load_json(root / "migration_readiness_gate.json")
    allowed = _load_json(root / "migration_allowed_scope.json")
    forbidden = _load_json(root / "migration_forbidden_scope.json")
    pre_check = _load_json(root / "pre_migration_checklist.json")
    test_plan = _load_json(root / "post_migration_test_plan.json")
    rollback = _load_json(root / "migration_rollback_requirement.json")
    whitebox = _load_json(root / "whitebox_test_center_deferment_policy.json")
    future_mod = _load_json(root / "future_reserved_module_constraint.json")
    decision = _load_json(root / "migration_readiness_decision.json")
    debt = _load_json(root / "governance_debt_register.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "roadmap_decision",
        "pahr_closure",
        "pahr_post_review",
        "pahr_dryrun",
        "pahr_planning",
        "consolidation_roadmap",
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

    generated_flags = (
        "main_project_migration_readiness_policy_generated",
        "migration_readiness_gate_generated",
        "migration_allowed_scope_generated",
        "migration_forbidden_scope_generated",
        "pre_migration_checklist_generated",
        "post_migration_test_plan_generated",
        "migration_rollback_requirement_generated",
        "whitebox_test_center_deferment_policy_generated",
        "future_reserved_module_constraint_generated",
        "migration_readiness_decision_generated",
    )
    for k in generated_flags:
        ok(f"summary.{k}", summary.get(k) is True)

    input_flags = (
        "roadmap_decision_input_loaded",
        "protected_asset_resolution_closure_input_loaded",
        "consolidation_closure_input_loaded",
        "structure_map_input_loaded",
        "gate_taxonomy_input_loaded",
    )
    for k in input_flags:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.post_migration_test_group_count>=5", summary.get("post_migration_test_group_count", 0) >= 5)
    ok("summary.pre_migration_check_count>=10", summary.get("pre_migration_check_count", 0) >= 10)
    ok("summary.forbidden_scope_count>=10", summary.get("forbidden_scope_count", 0) >= 10)
    ok("summary.future_reserved_module_count>=10", summary.get("future_reserved_module_count", 0) >= 10)

    boundary_flags = (
        "protected_assets_excluded_from_migration",
        "permanent_blocks_excluded_from_migration",
        "human_review_items_excluded_or_manual_only",
        "post_migration_test_required",
        "rollback_required",
        "whitebox_test_center_structure_optimization_deferred",
        "whitebox_test_center_must_align_with_main_project_structure",
        "developer_backend_overall_structure_deferred",
        "backend_architecture_not_finalized_now",
        "worldmodel_future_reserved",
        "memory_center_future_reserved",
        "library_future_reserved",
        "emotion_engine_future_reserved",
        "exploration_drive_future_reserved",
        "ready_for_migration_guarded_planning",
        "boundary_ok",
    )
    for k in boundary_flags:
        ok(f"summary.{k}", summary.get(k) is True)

    ok("summary.forced_future_module_finalization_allowed=false", summary.get("forced_future_module_finalization_allowed") is False)

    readiness_false = (
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "migration_execution_allowed",
    )
    for k in readiness_false:
        ok(f"summary.{k}=false", summary.get(k) is False)

    side_effect_false = (
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
        "image_content_read",
        "video_content_read",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
        "navigation_action_triggered",
        "speech_gate_invoked",
        "tts_invoked",
    )
    for k in side_effect_false:
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.no_runtime_executed", summary.get("no_runtime_executed") is True)
    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.human_review_case_count", summary.get("human_review_case_count") == HUMAN_REVIEW_CARRYOVER)
    ok("summary.permanent_block_case_count", summary.get("permanent_block_case_count") == PERMANENT_BLOCK_CARRYOVER)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("policy.planning_id", bool(policy.get("planning_id")))
    ok("policy.planning_scope", policy.get("planning_scope") == PLANNING_SCOPE)
    ok("policy.planning_only", policy.get("planning_only") is True)
    ok("policy.migration_execution_allowed=false", policy.get("migration_execution_allowed") is False)
    ok("policy.file_move_allowed_now=false", policy.get("file_move_allowed_now") is False)
    ok("policy.file_delete_allowed_now=false", policy.get("file_delete_allowed_now") is False)
    ok("policy.module_merge_allowed_now=false", policy.get("module_merge_allowed_now") is False)
    ok("policy.post_migration_test_required", policy.get("post_migration_test_required") is True)
    for ref_key in (
        "source_roadmap_ref",
        "source_consolidation_closure_ref",
        "source_protected_asset_resolution_ref",
        "migration_readiness_gate_ref",
        "migration_allowed_scope_ref",
        "migration_forbidden_scope_ref",
        "pre_migration_checklist_ref",
        "post_migration_test_plan_ref",
        "rollback_requirement_ref",
        "whitebox_test_center_deferment_ref",
        "future_module_reserved_constraint_ref",
    ):
        ok(f"policy.{ref_key}", bool(policy.get(ref_key)))
    ok("policy.next_phase_recommendation", policy.get("next_phase_recommendation") == NEXT_PHASE)

    ok("gate.all_go_conditions_met", gate.get("all_go_conditions_met") is True)
    ok("gate.readiness_verdict", gate.get("readiness_verdict") == "GO")
    for cond, val in (gate.get("go_conditions") or {}).items():
        ok(f"gate.go.{cond}", val is True, val)

    for i, ng in enumerate(gate.get("nogo_triggers") or []):
        ok(f"gate.nogo[{i}].trigger_id", bool(ng.get("trigger_id")))

    ok("allowed.candidate_only", allowed.get("candidate_only") is True)
    ok("allowed.execution_allowed_now=false", allowed.get("execution_allowed_now") is False)
    ok("allowed.allowed_scope_count>=8", allowed.get("allowed_scope_count", 0) >= 8)
    for i, row in enumerate(allowed.get("allowed_scopes") or []):
        ok(f"allowed[{i}].candidate_only", row.get("candidate_only") is True)
        ok(f"allowed[{i}].execution_allowed_now=false", row.get("execution_allowed_now") is False)
        ok(f"allowed[{i}].requires_guarded_planning", row.get("requires_guarded_planning") is True)
        ok(f"allowed[{i}].requires_post_migration_test", row.get("requires_post_migration_test") is True)

    ok("forbidden.forbidden_scope_count>=10", forbidden.get("forbidden_scope_count", 0) >= 10)
    ok("forbidden.protected_assets_excluded", forbidden.get("protected_assets_excluded_from_migration") is True)
    ok("forbidden.permanent_blocks_excluded", forbidden.get("permanent_blocks_excluded_from_migration") is True)
    for i, row in enumerate(forbidden.get("forbidden_scopes") or []):
        ok(f"forbidden[{i}].included_in_migration_scope=false", row.get("included_in_migration_scope") is False)
        ok(f"forbidden[{i}].execution_allowed_now=false", row.get("execution_allowed_now") is False)

    ok("pre_check.pre_migration_check_count>=10", pre_check.get("pre_migration_check_count", 0) >= 10)
    ok("pre_check.rollback_required", pre_check.get("rollback_required") is True)
    for i, row in enumerate(pre_check.get("checks") or []):
        ok(f"pre_check[{i}].executed_in_this_phase=false", row.get("executed_in_this_phase") is False)
        ok(f"pre_check[{i}].planning_only_definition", row.get("planning_only_definition") is True)

    ok("test_plan.post_migration_test_group_count>=5", test_plan.get("post_migration_test_group_count", 0) >= 5)
    ok("test_plan.tests_executed=false", test_plan.get("tests_executed") is False)
    ok("test_plan.post_migration_test_required", test_plan.get("post_migration_test_required") is True)
    group_ids = set()
    for i, t in enumerate(test_plan.get("test_groups") or []):
        group_ids.add(t.get("test_group_id"))
        ok(f"test[{i}].required_after_migration", t.get("required_after_migration") is True)
        ok(f"test[{i}].rollback_required_if_failed", t.get("rollback_required_if_failed") is True)
        ok(f"test[{i}].execution_status", t.get("execution_status") == "plan_defined_not_executed")
    for gid in ("A", "B", "C", "D", "E"):
        ok(f"test_plan.group_{gid}_present", gid in group_ids)

    ok("rollback.rollback_required", rollback.get("rollback_required") is True)
    ok("rollback.rollback_executed_in_this_phase=false", rollback.get("rollback_executed_in_this_phase") is False)
    for i, req in enumerate(rollback.get("requirements") or []):
        ok(f"rollback.req[{i}].required", req.get("required") is True)

    ok("whitebox.deferred", whitebox.get("whitebox_test_center_structure_optimization_deferred") is True)
    ok(
        "whitebox.defer_reason",
        whitebox.get("reason") == "requires_post_migration_test_and_design_discussion",
    )
    ok("whitebox.must_align", whitebox.get("whitebox_test_center_must_align_with_main_project_structure") is True)
    ok("whitebox.not_finalized", whitebox.get("whitebox_structure_not_finalized_now") is True)
    ok("whitebox.test_center_not_finalized", whitebox.get("test_center_structure_not_finalized_now") is True)
    ok("whitebox.dev_backend_deferred", whitebox.get("developer_backend_overall_structure_deferred") is True)
    ok("whitebox.backend_not_finalized", whitebox.get("backend_architecture_not_finalized_now") is True)

    ok("future.future_reserved_module_count>=10", future_mod.get("future_reserved_module_count", 0) >= 10)
    ok("future.forced_finalization_allowed=false", future_mod.get("forced_future_module_finalization_allowed") is False)
    for i, m in enumerate(future_mod.get("modules") or []):
        ok(f"future[{i}].future_reserved_module", m.get("future_reserved_module") is True)
        ok(f"future[{i}].discussion_required", m.get("discussion_required") is True)
        ok(f"future[{i}].runtime_allowed_now=false", m.get("runtime_allowed_now") is False)
        ok(f"future[{i}].write_allowed_now=false", m.get("write_allowed_now") is False)
        ok(f"future[{i}].forced_structure_finalization_allowed=false", m.get("forced_structure_finalization_allowed") is False)

    ok("decision.readiness_verdict", decision.get("readiness_verdict") == "GO")
    ok("decision.ready_for_migration_guarded_planning", decision.get("ready_for_migration_guarded_planning") is True)
    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("decision.blockers_empty", decision.get("blockers") == [])

    ok("debt.debt_count>=6", debt.get("debt_count", 0) >= 6)

    for report_name, report in (
        ("no_move", no_move),
        ("no_delete", no_delete),
        ("no_runtime", no_runtime),
        ("no_write", no_write),
    ):
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{report_name}.planning_only", report.get("planning_only") is True)
        ok(f"{report_name}.violations_empty", report.get("violations") == [])

    ok("no_move.actual_file_move_executed=false", no_move.get("actual_file_move_executed") is False)
    ok("no_delete.actual_file_delete_executed=false", no_delete.get("actual_file_delete_executed") is False)
    ok("no_runtime.no_runtime_executed", no_runtime.get("no_runtime_executed") is True)
    ok("no_write.world_model_written=false", no_write.get("world_model_written") is False)

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
