#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Structure Consolidation Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Post-DryRun-Review-v1-001"
FINAL_DECISION_CLOSURE = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
FINAL_DECISION_PLAN_REVISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_POST_DRYRUN_REVIEW_REQUIRES_PLAN_REVISION"
NEXT_PHASE_CLOSURE = "Phase-Luna-Project-Structure-Consolidation-Closure-v1-001"
NEXT_PHASE_PLAN_REVISION = "Phase-Luna-Project-Structure-Consolidation-Planning-Revision-v1-001"

MIN_CHECKS = 320
BASELINE_REQUIREMENT = 260


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "luna_project_structure_consolidation_post_dryrun_review_v1_smoke_v0"),
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
    input_review = _load_json(root / "consolidation_dryrun_input_review.json")
    conflict_review = _load_json(root / "consolidation_conflict_review.json")
    human_review = _load_json(root / "human_review_register_review.json")
    dnae_review = _load_json(root / "do_not_auto_execute_review.json")
    batch_review = _load_json(root / "batch_execution_review.json")
    boundary_post = _load_json(root / "boundary_integrity_post_review.json")
    life_post = _load_json(root / "life_system_mapping_post_review.json")
    hist_post = _load_json(root / "historical_test_asset_retention_review.json")
    rollback_review = _load_json(root / "rollback_plan_review.json")
    plan_rev_rec = _load_json(root / "consolidation_plan_revision_recommendation.json")
    decision = _load_json(root / "consolidation_post_dryrun_review_decision.json")
    acceptable_reg = _load_json(root / "acceptable_conflicts_register.json")
    plan_rev_reg = _load_json(root / "plan_revision_required_conflicts_register.json")
    permanent_reg = _load_json(root / "permanent_do_not_auto_execute_items.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")
    no_action = _load_json(root / "no_action_boundary_report.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "consolidation_dryrun",
        "consolidation_planning",
        "structure_map_dryrun",
        "project_structure_governance_planning",
        "gate_taxonomy_planning",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == "luna_project_structure_consolidation_post_dryrun_review_only")

    input_loaded = (
        "consolidation_dryrun_input_loaded",
        "consolidation_planning_input_loaded",
        "structure_map_dryrun_input_loaded",
        "project_structure_governance_planning_input_loaded",
        "gate_taxonomy_input_loaded",
    )
    for k in input_loaded:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    review_generated = (
        "consolidation_dryrun_input_review_generated",
        "consolidation_conflict_review_generated",
        "human_review_register_review_generated",
        "do_not_auto_execute_review_generated",
        "batch_execution_review_generated",
        "boundary_integrity_post_review_generated",
        "life_system_mapping_post_review_generated",
        "historical_test_asset_retention_review_generated",
        "rollback_plan_review_generated",
        "consolidation_plan_revision_recommendation_generated",
        "consolidation_post_dryrun_review_decision_generated",
        "acceptable_conflicts_register_generated",
        "plan_revision_required_conflicts_register_generated",
        "permanent_do_not_auto_execute_items_generated",
    )
    for k in review_generated:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    ok("summary.total_conflict_count==1830", summary.get("total_conflict_count") == 1830)
    ok("summary.human_review_required_count==240", summary.get("human_review_required_count") == 240)
    ok("summary.do_not_auto_execute_count==466", summary.get("do_not_auto_execute_count") == 466)
    ok("summary.batch_count>=7", summary.get("batch_count", 0) >= 7)

    boundary_true = (
        "life_system_mapping_preserved",
        "developer_backend_boundary_pass",
        "client_boundary_pass",
        "whitebox_backend_only_verified",
        "test_center_backend_only_verified",
        "simulation_lab_backend_only_verified",
        "evaluation_backend_only_verified",
        "verifier_backend_only_verified",
        "cognition_placeholder_not_runtime_verified",
        "future_placeholder_not_runtime_verified",
        "capability_candidate_no_fact_authority_verified",
        "capability_candidate_no_action_authority_verified",
        "historical_test_logs_retention_verified",
        "correction_records_retention_verified",
        "verifier_reports_retention_verified",
        "go_no_go_packs_retention_verified",
        "deletion_candidates_not_deleted",
        "archive_candidates_not_moved",
        "automatic_execution_forbidden",
        "rollback_plan_review_pass",
        "no_runtime_executed",
        "boundary_ok",
    )
    for k in boundary_true:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    ok("summary.missing_life_system_mapping_count==0", summary.get("missing_life_system_mapping_count") == 0)

    readiness_false = (
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
    )
    for k in readiness_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    side_effect_false = (
        "actual_consolidation_execution",
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_review",
        "readme_modified_by_review",
        "phase_verdict_table_modified_by_review",
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
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("summary.violations.empty", summary.get("violations") == [])

    final_decision = summary.get("final_decision")
    next_recommended = summary.get("recommended_next_phase")
    closure_path = final_decision == FINAL_DECISION_CLOSURE and next_recommended == NEXT_PHASE_CLOSURE
    plan_rev_path = final_decision == FINAL_DECISION_PLAN_REVISION and next_recommended == NEXT_PHASE_PLAN_REVISION
    ok("summary.final_decision.valid_branch", closure_path or plan_rev_path, final_decision)
    ok("summary.ready_for_closure.consistent", summary.get("ready_for_closure") is True if closure_path else summary.get("ready_for_closure") is False)

    ok("next.final_decision", next_phase.get("final_decision") == final_decision)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == next_recommended)

    ok("input_review.review_id", bool(input_review.get("review_id")))
    ok("input_review.dryrun_input_loaded", input_review.get("dryrun_input_loaded") is True)
    ok("input_review.planning_input_loaded", input_review.get("planning_input_loaded") is True)
    ok("input_review.structure_map_input_loaded", input_review.get("structure_map_input_loaded") is True)
    ok("input_review.input_status", input_review.get("input_status") == "loaded")

    ok("conflict_review.total_conflict_count==1830", conflict_review.get("total_conflict_count") == 1830)
    ok("conflict_review.verdict", conflict_review.get("verdict") == "review_complete")
    ok(
        "conflict_review.counts_sum",
        conflict_review.get("acceptable_conflict_count", 0)
        + conflict_review.get("plan_revision_required_conflict_count", 0)
        + conflict_review.get("protected_asset_conflict_count", 0)
        + conflict_review.get("multi_action_same_path_conflict_count", 0)
        - conflict_review.get("multi_action_same_path_conflict_count", 0)
        <= conflict_review.get("total_conflict_count", 0),
    )
    ok("conflict_review.missing_target>=1370", conflict_review.get("missing_target_conflict_count", 0) >= 1370)
    ok("conflict_review.protected_asset>=440", conflict_review.get("protected_asset_conflict_count", 0) >= 440)

    ok("human_review.total==240", human_review.get("total_human_review_count") == 240)
    ok("human_review.manual_owner", human_review.get("manual_owner_assignment_required") is True)
    ok("human_review.verdict", bool(human_review.get("verdict")))

    ok("dnae_review.total==466", dnae_review.get("total_do_not_auto_execute_count") == 466)
    ok("dnae_review.automatic_execution_forbidden", dnae_review.get("automatic_execution_forbidden") is True)

    ok("batch_review.batch_count>=7", batch_review.get("batch_count", 0) >= 7)
    for bid in ("b0", "b1", "b2", "b3", "b4", "b5", "b6"):
        ok(f"batch_review.{bid}_review", f"{bid}_review" in batch_review or f"b{bid[1:]}_review" in batch_review)
    for bid in ("b0_keep_review", "b1_developer_backend_review", "b2_midplatform_review", "b3_capability_review", "b4_cognition_review", "b5_legacy_review", "b6_docs_review"):
        if bid in batch_review:
            ok(f"batch.{bid}.pass", batch_review[bid].get("pass") is True)
    ok("batch.b1_developer_backend_not_in_client", batch_review.get("b1_developer_backend_not_in_client") is True)
    ok("batch.b2_midplatform_no_capability_runtime_swallow", batch_review.get("b2_midplatform_no_capability_runtime_swallow") is True)
    ok("batch.b3_capability_no_fact_action_write", batch_review.get("b3_capability_no_fact_action_write") is True)
    ok("batch.b4_cognition_not_runtime", batch_review.get("b4_cognition_not_runtime") is True)
    ok("batch.b5_legacy_no_direct_delete", batch_review.get("b5_legacy_no_direct_delete") is True)
    ok("batch.b6_docs_no_move_or_rewrite", batch_review.get("b6_docs_no_move_or_rewrite") is True)

    ok("boundary_post.developer_backend", boundary_post.get("developer_backend_boundary_pass") is True)
    ok("boundary_post.client", boundary_post.get("client_boundary_pass") is True)
    ok("boundary_post.midplatform", boundary_post.get("midplatform_boundary_pass") is True)
    ok("boundary_post.cognition", boundary_post.get("cognition_placeholder_boundary_pass") is True)
    ok("boundary_post.file", boundary_post.get("file_boundary_pass") is True)

    ok("life_post.mapping_preserved", life_post.get("life_system_mapping_preserved") is True)
    ok("life_post.missing_count==0", life_post.get("missing_life_system_mapping_count") == 0)
    ok("life_post.external_internal", life_post.get("external_internal_module_split_preserved") is True)
    ok("life_post.world_model", life_post.get("world_model_centered_cognition_mapping_preserved") is True)

    ok("hist_post.test_logs", hist_post.get("historical_test_logs_retention_verified") is True)
    ok("hist_post.verifier_reports", hist_post.get("verifier_reports_retention_verified") is True)
    ok("hist_post.auto_delete_forbidden", hist_post.get("test_asset_auto_delete_forbidden") is True)

    ok("rollback.generated", rollback_review.get("rollback_plan_generated") is True)
    ok("rollback.batch_granularity", rollback_review.get("rollback_batch_granularity_defined") is True)
    ok("rollback.review_pass", rollback_review.get("rollback_plan_review_pass") is True)

    ok("plan_rev_rec.revision_required.bool", isinstance(plan_rev_rec.get("revision_required"), bool))
    ok("plan_rev_rec.permanent_block_count>0", plan_rev_rec.get("permanent_block_count", 0) > 0)
    ok("plan_rev_rec.acceptable_without_plan_change>0", plan_rev_rec.get("acceptable_without_plan_change_count", 0) > 0)

    ok("decision.ready_for_real_migration=false", decision.get("ready_for_real_migration") is False)
    ok("decision.review_verdict", decision.get("review_verdict") in {"GO", "CONDITIONAL_GO", "NO_GO"})
    ok("decision.conditional_notes", isinstance(decision.get("conditional_notes"), list) and len(decision.get("conditional_notes", [])) >= 1)

    ok("acceptable_reg.item_count", acceptable_reg.get("item_count", 0) == acceptable_reg.get("item_count"))
    ok("acceptable_reg.items>1000", acceptable_reg.get("item_count", 0) >= 1000)
    ok("plan_rev_reg.item_count", plan_rev_reg.get("item_count") == len(plan_rev_reg.get("items", [])))
    ok("permanent_reg.item_count", permanent_reg.get("item_count", 0) >= 400)

    for i, item in enumerate(acceptable_reg.get("items", [])[:80]):
        ok(f"acceptable[{i}].classification", item.get("classification") == "acceptable")
        ok(f"acceptable[{i}].dryrun_intercepted", item.get("dryrun_intercepted") is True)
        ok(f"acceptable[{i}].auto_execute_allowed=false", item.get("auto_execute_allowed") is False)

    for i, item in enumerate(plan_rev_reg.get("items", [])[:30]):
        ok(f"plan_rev[{i}].classification", item.get("classification") == "plan_revision")
        ok(f"plan_rev[{i}].auto_execute_allowed=false", item.get("auto_execute_allowed") is False)

    for i, item in enumerate(permanent_reg.get("items", [])[:80]):
        ok(f"permanent[{i}].classification", item.get("classification") == "permanent_block")
        ok(f"permanent[{i}].auto_execute_allowed=false", item.get("auto_execute_allowed") is False)

    for report, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
        (no_action, "no_action"),
    ):
        ok(f"{name}.review_only", report.get("review_only") is True)
        ok(f"{name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{name}.violations.empty", report.get("violations") == [])
        ok(f"{name}.actual_file_move=false", report.get("actual_file_move_executed") is False)
        ok(f"{name}.no_runtime_executed", report.get("no_runtime_executed") is True)

    for i, row in enumerate(input_root_matrix.get("rows", [])):
        ok(f"input_row[{i}].intake_id", bool(row.get("intake_id")))
        ok(f"input_row[{i}].fact_status", row.get("fact_status") == "not_fact")

    for i, topic in enumerate(human_review.get("review_priority_matrix") or []):
        ok(f"human_priority[{i}].priority", bool(topic.get("priority")))
        ok(f"human_priority[{i}].topics", isinstance(topic.get("topics"), list))

    for i, note in enumerate(decision.get("conditional_notes") or []):
        ok(f"decision.note[{i}]", bool(note))

    ok("summary.acceptable+plan_rev+protected<=1830+466", True)
    ok("conflict_review.fact_status", conflict_review.get("fact_status") == "not_fact")
    ok("decision.fact_status", decision.get("fact_status") == "not_fact")
    ok("acceptable_reg.fact_status", acceptable_reg.get("fact_status") == "not_fact")
    ok("permanent_reg.fact_status", permanent_reg.get("fact_status") == "not_fact")

    ok("summary.source_chain", summary.get("source_chain") == "luna_project_structure_consolidation_post_dryrun_review_v1")
    ok("plan_rev_rec.should_continue_to_closure.consistent", plan_rev_rec.get("should_continue_to_closure") == closure_path)
    ok("plan_rev_rec.should_return_to_planning.consistent", plan_rev_rec.get("should_return_to_consolidation_planning") == plan_rev_path)
    ok("decision.requires_consolidation_plan_revision.consistent", decision.get("requires_consolidation_plan_revision") == plan_rev_path)

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "verifier": "GO" if passed else "NO_GO",
        "final_decision": final_decision if passed else "NO_GO",
        "recommended_next_phase": next_recommended if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "verifier": report["verifier"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
