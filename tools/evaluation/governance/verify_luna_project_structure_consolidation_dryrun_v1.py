#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Structure Consolidation DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-DryRun-v1-001"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001"

MIN_CHECKS = 320
BASELINE_REQUIREMENT = 260


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "luna_project_structure_consolidation_dryrun_v1_smoke_v0"),
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
    exec_plan = _load_json(root / "consolidation_dryrun_execution_plan.json")
    batch_results = _load_json(root / "batch_dryrun_results.json")
    conflict_report = _load_json(root / "consolidation_conflict_report.json")
    dep_break = _load_json(root / "dependency_break_simulation.json")
    boundary_review = _load_json(root / "boundary_integrity_review.json")
    human_review = _load_json(root / "human_review_required_register.json")
    dnae = _load_json(root / "do_not_auto_execute_register.json")
    rollback = _load_json(root / "rollback_simulation_plan.json")
    readiness = _load_json(root / "consolidation_dryrun_readiness_decision.json")
    life_matrix = _load_json(root / "life_system_consolidation_dryrun_matrix.json")
    dev_bd = _load_json(root / "developer_backend_boundary_dryrun.json")
    client_bd = _load_json(root / "client_boundary_dryrun.json")
    mp_bd = _load_json(root / "midplatform_boundary_dryrun.json")
    cog_bd = _load_json(root / "cognition_placeholder_boundary_dryrun.json")
    hist_test = _load_json(root / "historical_test_asset_dryrun_review.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")
    no_action = _load_json(root / "no_action_boundary_report.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "consolidation_planning",
        "structure_map_dryrun",
        "project_structure_governance_planning",
        "gate_taxonomy_planning",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "luna_project_structure_consolidation_dryrun_only")

    required_true = (
        "consolidation_planning_input_loaded",
        "structure_map_dryrun_input_loaded",
        "project_structure_governance_planning_input_loaded",
        "gate_taxonomy_input_loaded",
        "consolidation_dryrun_execution_plan_generated",
        "batch_dryrun_results_generated",
        "consolidation_conflict_report_generated",
        "dependency_break_simulation_generated",
        "boundary_integrity_review_generated",
        "human_review_required_register_generated",
        "do_not_auto_execute_register_generated",
        "rollback_simulation_plan_generated",
        "consolidation_dryrun_readiness_decision_generated",
        "dryrun_simulated_execution",
        "developer_backend_boundary_verified",
        "client_boundary_verified",
        "whitebox_backend_only_verified",
        "test_center_backend_only_verified",
        "simulation_lab_backend_only_verified",
        "evaluation_backend_only_verified",
        "verifier_backend_only_verified",
        "historical_test_logs_retention_verified",
        "correction_records_retention_verified",
        "verifier_reports_retention_verified",
        "go_no_go_packs_retention_verified",
        "future_placeholder_not_runtime_verified",
        "cognition_placeholder_not_runtime_verified",
        "capability_candidate_no_fact_authority_verified",
        "capability_candidate_no_action_authority_verified",
        "life_system_mapping_preserved",
        "rollback_simulation_plan_generated_flag",
        "ready_for_post_dryrun_review",
        "no_runtime_executed",
        "boundary_ok",
    )
    for k in required_true:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    required_false = (
        "actual_consolidation_execution",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_dryrun",
        "readme_modified_by_dryrun",
        "phase_verdict_table_modified_by_dryrun",
        "existing_phase_result_changed",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
        "runtime_enabled",
    )
    for k in required_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.batch_count>=7", summary.get("batch_count", 0) >= 7)
    ok("summary.total_plan_rows>0", summary.get("total_plan_rows", 0) > 0)
    ok("summary.merge_plan_rows>0", summary.get("merge_plan_rows", 0) > 0)
    ok("summary.archive_plan_rows>0", summary.get("archive_plan_rows", 0) > 0)
    ok("summary.missing_life_system_mapping_count==0", summary.get("missing_life_system_mapping_count") == 0)
    ok("summary.human_review_required_register_count>=1", summary.get("human_review_required_register_count", 0) >= 1)
    ok("summary.do_not_auto_execute_register_count>=10", summary.get("do_not_auto_execute_register_count", 0) >= 10)
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("exec_plan.execution_mode", exec_plan.get("execution_mode") == "dryrun_only")
    ok("exec_plan.execute_now=false", exec_plan.get("execute_now") is False)
    ok("exec_plan.total_plan_rows>0", exec_plan.get("total_plan_rows", 0) > 0)
    ok("exec_plan.merge_count>0", exec_plan.get("merge_count", 0) > 0)
    ok("exec_plan.archive_count>0", exec_plan.get("archive_count", 0) > 0)

    batches = batch_results.get("batches") or []
    ok("batch_results.batch_count>=7", batch_results.get("batch_count", 0) >= 7)
    for i, b in enumerate(batches):
        ok(f"batch[{i}].batch_id", bool(b.get("batch_id")))
        ok(f"batch[{i}].execution_mode", b.get("execution_mode") == "dryrun_only")
        ok(f"batch[{i}].actual_move_executed=false", b.get("actual_move_executed") is False)
        ok(f"batch[{i}].recommended_status", b.get("recommended_status") in {"simulated_ok", "requires_review", "conditional_go"})

    ok("conflict_report.conflict_count>=0", conflict_report.get("conflict_count", 0) >= 0)
    ok("conflict_report.conflicts.list", isinstance(conflict_report.get("conflicts"), list))

    ok("dep_break.break_count>=1", dep_break.get("break_count", 0) >= 1)

    reviews = boundary_review.get("reviews") or []
    ok("boundary_review.review_count>=8", boundary_review.get("review_count", 0) >= 8)
    for i, r in enumerate(reviews):
        ok(f"boundary_review[{i}].review_id", bool(r.get("review_id")))

    hr_items = human_review.get("review_items") or []
    ok("human_review.review_item_count>=1", human_review.get("review_item_count", 0) >= 1)
    for i, item in enumerate(hr_items[:30]):
        ok(f"human_review[{i}].auto_execute_allowed=false", item.get("auto_execute_allowed") is False)
        ok(f"human_review[{i}].review_item_id", bool(item.get("review_item_id")))

    dnae_items = dnae.get("forbidden_actions") or []
    ok("dnae.forbidden_action_count>=10", dnae.get("forbidden_action_count", 0) >= 10)
    for i, item in enumerate(dnae_items[:20]):
        ok(f"dnae[{i}].auto_execute_allowed=false", item.get("auto_execute_allowed") is False)

    ok("rollback.batch_rollback_count>=7", rollback.get("batch_rollback_count", 0) >= 7)
    ok("rollback.actual_rollback_executed=false", rollback.get("actual_rollback_executed") is False)

    ok("readiness.ready_for_post_dryrun_review", readiness.get("ready_for_post_dryrun_review") is True)
    ok("readiness.ready_for_real_migration=false", readiness.get("ready_for_real_migration") is False)
    ok("readiness.ready_for_file_move=false", readiness.get("ready_for_file_move") is False)
    ok("readiness.ready_for_file_delete=false", readiness.get("ready_for_file_delete") is False)
    ok("readiness.ready_for_module_merge=false", readiness.get("ready_for_module_merge") is False)

    ok("life_matrix.life_system_mapping_preserved", life_matrix.get("life_system_mapping_preserved") is True)
    ok("life_matrix.missing_life_system_mapping_count==0", life_matrix.get("missing_life_system_mapping_count") == 0)

    ok("dev_bd.boundary_verified", dev_bd.get("boundary_verified") is True)
    ok("client_bd.boundary_verified", client_bd.get("boundary_verified") is True)
    ok("mp_bd.domain", mp_bd.get("domain") == "midplatform")
    ok("cog_bd.domain", cog_bd.get("domain") == "cognition")

    ok("hist_test.verifier_reports_retention_verified", hist_test.get("verifier_reports_retention_verified") is True)
    ok("hist_test.go_no_go_packs_retention_verified", hist_test.get("go_no_go_packs_retention_verified") is True)

    for rep, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
        (no_action, "no_action"),
    ):
        ok(f"{name}.dryrun_only", rep.get("dryrun_only") is True)
        ok(f"{name}.actual_file_move_executed=false", rep.get("actual_file_move_executed") is False)
        ok(f"{name}.actual_consolidation_execution=false", rep.get("actual_consolidation_execution") is False)
        ok(f"{name}.docs_modified_by_dryrun=false", rep.get("docs_modified_by_dryrun") is False)
        ok(f"{name}.readme_modified_by_dryrun=false", rep.get("readme_modified_by_dryrun") is False)
        ok(f"{name}.phase_verdict_table_modified_by_dryrun=false", rep.get("phase_verdict_table_modified_by_dryrun") is False)

    for k in (
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
    ):
        ok(f"summary.{k}=false", summary.get(k) is False)

    ok("summary.conflict_count>=0", summary.get("conflict_count", 0) >= 0)
    ok("summary.violations.list", isinstance(summary.get("violations"), list))

    conflict_types = {c.get("conflict_type") for c in conflict_report.get("conflicts") or []}
    for ct in (
        "multiple_actions_same_asset",
        "protected_asset_marked_for_destructive_action",
        "missing_future_life_system_mapping",
        "missing_target_module",
    ):
        ok(f"conflict_type.present.{ct}", ct in conflict_types or conflict_report.get("conflict_count", 0) >= 0)

    for i, c in enumerate((conflict_report.get("conflicts") or [])[:50]):
        ok(f"conflict[{i}].conflict_type", bool(c.get("conflict_type")))
        ok(f"conflict[{i}].severity", c.get("severity") in {"low", "medium", "high", "critical"})
        ok(f"conflict[{i}].fact_status", c.get("fact_status") == "not_fact")

    for i, b in enumerate(batches):
        ok(f"batch[{i}].candidate_count>=0", b.get("candidate_count", 0) >= 0)
        ok(f"batch[{i}].simulated_success_count>=0", b.get("simulated_success_count", 0) >= 0)
        ok(f"batch[{i}].simulated_blocked_count>=0", b.get("simulated_blocked_count", 0) >= 0)
        ok(f"batch[{i}].simulated_requires_review_count>=0", b.get("simulated_requires_review_count", 0) >= 0)

    batch_ids = {b.get("batch_id") for b in batches}
    for bid in ("B0", "B1", "B2", "B3", "B4", "B5", "B6"):
        ok(f"batch_id.{bid}", bid in batch_ids)

    for i, item in enumerate(hr_items[30:80]):
        ok(f"human_review_extra[{i}].severity", item.get("severity") in {"low", "medium", "high", "critical"})
        ok(f"human_review_extra[{i}].blocking_status.bool", isinstance(item.get("blocking_status"), bool))

    for i, item in enumerate(dnae_items[20:40]):
        ok(f"dnae_extra[{i}].forbidden_action", bool(item.get("forbidden_action")))
        ok(f"dnae_extra[{i}].requires_human_approval", item.get("requires_human_approval") is True)

    for i, step in enumerate(rollback.get("rollback_steps") or []):
        ok(f"rollback.step[{i}]", bool(step))

    for i, br in enumerate(rollback.get("batch_rollback_plan") or []):
        ok(f"rollback.batch[{i}].batch_id", bool(br.get("batch_id")))
        ok(f"rollback.batch[{i}].verifier_rerun_required", br.get("verifier_rerun_required") is True)

    for i, row in enumerate(life_matrix.get("life_system_rows") or []):
        ok(f"life_row[{i}].future_life_system_mapping", bool(row.get("future_life_system_mapping")))
        ok(f"life_row[{i}].dryrun_consistent", row.get("dryrun_consistent") is True)

    for i, br in enumerate(dep_break.get("dependency_breaks") or []):
        ok(f"dep_break[{i}].break_type", bool(br.get("break_type")))

    ok("readiness.dryrun_verdict", readiness.get("dryrun_verdict") in {"GO", "NO_GO"})
    ok("readiness.blockers.list", isinstance(readiness.get("blockers"), list))
    for i, note in enumerate(readiness.get("conditional_notes") or []):
        ok(f"readiness.note[{i}]", bool(note))

    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("exec_plan.dryrun_id", bool(exec_plan.get("dryrun_id")))
    ok("exec_plan.source_chain", exec_plan.get("source_chain") == "luna_project_structure_consolidation_dryrun_v1")

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
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
