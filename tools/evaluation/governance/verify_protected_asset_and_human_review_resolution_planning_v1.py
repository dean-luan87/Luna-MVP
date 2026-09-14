#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Protected Asset and Human Review Resolution Planning v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-Planning-v1-001"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_PLANNING_READY_FOR_DRYRUN"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "protected_asset_and_human_review_resolution_planning_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    planning_policy = _load_json(root / "protected_asset_and_human_review_resolution_planning_policy.json")
    protected_policy = _load_json(root / "protected_asset_policy.json")
    human_policy = _load_json(root / "human_review_resolution_policy.json")
    dnae_policy = _load_json(root / "permanent_do_not_auto_execute_policy.json")
    owner_policy = _load_json(root / "manual_owner_assignment_policy.json")
    decision_schema = _load_json(root / "review_decision_schema.json")
    state_machine = _load_json(root / "review_resolution_state_machine.json")
    audit_policy = _load_json(root / "protected_asset_audit_trace_policy.json")
    rollback_policy = _load_json(root / "review_rollback_policy.json")
    asset_matrix = _load_json(root / "protected_asset_type_matrix.json")
    category_matrix = _load_json(root / "human_review_category_matrix.json")
    block_matrix = _load_json(root / "permanent_block_rule_matrix.json")
    readiness = _load_json(root / "resolution_planning_readiness_decision.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    ok("summary.planning_scope", summary.get("planning_scope") == "protected_asset_and_human_review_resolution_planning_only")

    for field in (
        "roadmap_decision_input_loaded",
        "consolidation_closure_input_loaded",
        "consolidation_post_review_input_loaded",
        "human_review_carryover_loaded",
        "permanent_dnae_carryover_loaded",
        "protected_asset_policy_generated",
        "human_review_resolution_policy_generated",
        "permanent_dnae_policy_generated",
        "manual_owner_assignment_policy_generated",
        "review_decision_schema_generated",
        "review_resolution_state_machine_generated",
        "audit_trace_policy_generated",
        "rollback_policy_generated",
        "ready_for_human_review_resolution_dryrun",
        "manual_owner_required",
        "audit_required",
        "rollback_required",
        "source_chain_required",
        "no_runtime_executed",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    ok("summary.protected_asset_type_count>=10", summary.get("protected_asset_type_count", 0) >= 10)
    ok("summary.human_review_category_count>=8", summary.get("human_review_category_count", 0) >= 8)
    ok("summary.permanent_block_rule_count>=8", summary.get("permanent_block_rule_count", 0) >= 8)
    ok("summary.allowed_review_decision_count>=10", summary.get("allowed_review_decision_count", 0) >= 10)
    ok("summary.forbidden_review_decision_count>=8", summary.get("forbidden_review_decision_count", 0) >= 8)
    ok("summary.review_state_count>=8", summary.get("review_state_count", 0) >= 8)
    ok("summary.human_review_required_count==240", summary.get("human_review_required_count") == 240)
    ok("summary.permanent_do_not_auto_execute_count==914", summary.get("permanent_do_not_auto_execute_count") == 914)
    ok("summary.protected_conflict_count==448", summary.get("protected_conflict_count") == 448)
    ok("summary.static_dnae_rule_count==466", summary.get("static_dnae_rule_count") == 466)

    for field in (
        "protected_assets_auto_delete_allowed",
        "protected_assets_auto_archive_allowed",
        "protected_assets_auto_move_allowed",
        "protected_assets_auto_merge_allowed",
        "human_review_execution_allowed",
        "permanent_block_override_allowed",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
    ):
        ok(f"summary.{field}=false", summary.get(field) is False, summary.get(field))

    for field in (
        "delete_now_decision_forbidden",
        "move_now_decision_forbidden",
        "merge_now_decision_forbidden",
        "archive_now_decision_forbidden",
        "enable_runtime_decision_forbidden",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    side_effect_false = (
        "actual_human_review_executed",
        "protected_assets_modified",
        "permanent_blocks_modified",
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
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("planning_policy.planning_only", planning_policy.get("planning_only") is True)
    ok("planning_policy.human_review_execution=false", planning_policy.get("human_review_execution_allowed") is False)
    ok("planning_policy.protected_modification=false", planning_policy.get("protected_asset_modification_allowed") is False)
    ok("planning_policy.permanent_override=false", planning_policy.get("permanent_block_override_allowed") is False)
    ok("planning_policy.real_migration=false", planning_policy.get("real_migration_allowed") is False)

    ok("protected_policy.type_count>=10", protected_policy.get("protected_asset_type_count", 0) >= 10)
    for i, row in enumerate(protected_policy.get("asset_types") or []):
        ok(f"protected_type[{i}].auto_delete=false", row.get("auto_delete_allowed") is False)
        ok(f"protected_type[{i}].auto_archive=false", row.get("auto_archive_allowed") is False)
        ok(f"protected_type[{i}].auto_move=false", row.get("auto_move_allowed") is False)
        ok(f"protected_type[{i}].auto_merge=false", row.get("auto_merge_allowed") is False)
        ok(f"protected_type[{i}].override=false", row.get("override_allowed") is False)

    ok("human_policy.count==240", human_policy.get("total_human_review_count") == 240)
    ok("human_policy.execution=false", human_policy.get("human_review_execution_allowed") is False)
    ok("human_policy.categories>=8", human_policy.get("human_review_category_count", 0) >= 8)
    for i, cat in enumerate(human_policy.get("categories") or []):
        ok(f"human_cat[{i}].auto_execute=false", cat.get("auto_execute_allowed") is False)
        ok(f"human_cat[{i}].must_record_reason", cat.get("must_record_reason") is True)
        ok(f"human_cat[{i}].category", bool(cat.get("review_category")))

    ok("dnae_policy.count==914", dnae_policy.get("total_permanent_block_count") == 914)
    ok("dnae_policy.override=false", dnae_policy.get("permanent_block_override_allowed") is False)
    ok("dnae_policy.rules>=8", dnae_policy.get("permanent_block_rule_count", 0) >= 8)
    for i, rule in enumerate(dnae_policy.get("rules") or []):
        ok(f"dnae_rule[{i}].audit", rule.get("audit_required") is True)
        ok(f"dnae_rule[{i}].rollback", rule.get("rollback_required") is True)
        ok(f"dnae_rule[{i}].auto_unblock=false", rule.get("auto_unblock_allowed") is False)

    ok("owner_policy.manual_required", owner_policy.get("manual_owner_required") is True)
    ok("owner_policy.auto_assign=false", owner_policy.get("auto_owner_assignment_allowed") is False)
    for i, owner in enumerate(owner_policy.get("owner_types") or []):
        ok(f"owner[{i}].cannot_auto_assign", owner.get("cannot_auto_assign") is True)
        ok(f"owner[{i}].type", bool(owner.get("owner_type")))

    ok("schema.allowed>=10", decision_schema.get("allowed_review_decision_count", 0) >= 10)
    ok("schema.forbidden>=8", decision_schema.get("forbidden_review_decision_count", 0) >= 8)
    ok("schema.delete_now_forbidden", decision_schema.get("delete_now_decision_forbidden") is True)
    ok("schema.move_now_forbidden", decision_schema.get("move_now_decision_forbidden") is True)
    ok("schema.merge_now_forbidden", decision_schema.get("merge_now_decision_forbidden") is True)
    ok("schema.archive_now_forbidden", decision_schema.get("archive_now_decision_forbidden") is True)
    ok("schema.runtime_forbidden", decision_schema.get("enable_runtime_decision_forbidden") is True)

    ok("state_machine.states>=8", state_machine.get("review_state_count", 0) >= 8)
    ok("state_machine.forbidden_states", "auto_executed" in (state_machine.get("forbidden_states") or []))
    ok("state_machine.audit", state_machine.get("transitions_require_audit") is True)

    ok("audit.audit_required", audit_policy.get("audit_required") is True)
    ok("audit.source_chain_required", audit_policy.get("source_chain_required") is True)
    ok("audit.trace_fields>=10", len(audit_policy.get("trace_fields") or []) >= 10)

    ok("rollback.rollback_required", rollback_policy.get("rollback_required") is True)
    ok("rollback.no_file_in_planning", rollback_policy.get("no_file_rollback_in_planning") is True)

    ok("readiness.all_policies_defined", readiness.get("protected_asset_policy_defined") is True)
    ok("readiness.ready_for_dryrun", readiness.get("ready_for_human_review_resolution_dryrun") is True)
    ok("readiness.real_migration=false", readiness.get("ready_for_real_migration") is False)

    ok("asset_matrix.row_count>=10", asset_matrix.get("row_count", 0) >= 10)
    ok("category_matrix.row_count>=8", category_matrix.get("row_count", 0) >= 8)
    ok("block_matrix.row_count>=8", block_matrix.get("row_count", 0) >= 8)

    for report, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
    ):
        ok(f"{name}.planning_only", report.get("planning_only") is True)
        ok(f"{name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{name}.human_review=false", report.get("actual_human_review_executed") is False)

    for i, row in enumerate(input_root_matrix.get("rows", [])):
        ok(f"input_row[{i}].loaded", row.get("loaded") is True)

    ok("summary.source_chain", summary.get("source_chain") == "protected_asset_and_human_review_resolution_planning_v1")

    check_count = len(checks)
    ok("meta.check_count>=baseline", check_count >= BASELINE_REQUIREMENT, check_count)
    ok("meta.check_count>=MIN_CHECKS", check_count >= MIN_CHECKS, check_count)

    passed = all(c["passed"] for c in checks) and check_count >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "output_root": str(root),
        "passed": bool(passed),
        "verifier": "GO" if passed else "NO_GO",
        "final_decision": FINAL_DECISION if passed else "NO_GO",
        "recommended_next_phase": NEXT_PHASE if passed else PHASE_ID,
        "check_count": check_count,
        "min_checks": MIN_CHECKS,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "verifier": report["verifier"], "check_count": check_count, "min_checks": MIN_CHECKS}, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
