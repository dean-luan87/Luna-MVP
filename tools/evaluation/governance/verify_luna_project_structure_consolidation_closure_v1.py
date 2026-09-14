#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Project Structure Consolidation Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Luna-Project-Structure-Consolidation-Closure-v1-001"
FINAL_DECISION = "LUNA_PROJECT_STRUCTURE_CONSOLIDATION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Luna-Project-Structure-Consolidation-Roadmap-Decision-v1-001"

MIN_CHECKS = 260
BASELINE_REQUIREMENT = 220


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "luna_project_structure_consolidation_closure_v1_smoke_v0"),
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
    closure_summary = _load_json(root / "luna_project_structure_consolidation_closure_summary.json")
    completed = _load_json(root / "completed_phase_matrix.json")
    decision_summary = _load_json(root / "consolidation_closure_decision_summary.json")
    boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    non_claims = _load_json(root / "consolidation_non_claims_register.json")
    human_carry = _load_json(root / "human_review_carryover_register.json")
    permanent_carry = _load_json(root / "permanent_do_not_auto_execute_carryover.json")
    deferred_pool = _load_json(root / "deferred_consolidation_action_pool.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")
    no_action = _load_json(root / "no_action_boundary_report.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "consolidation_post_review",
        "consolidation_dryrun",
        "consolidation_planning",
        "structure_map_dryrun",
        "project_structure_governance_planning",
        "gate_taxonomy_planning",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.closure_scope", summary.get("closure_scope") == "luna_project_structure_consolidation_closure_only")

    input_loaded = (
        "consolidation_post_review_input_loaded",
        "consolidation_dryrun_input_loaded",
        "consolidation_planning_input_loaded",
        "structure_map_dryrun_input_loaded",
        "project_structure_governance_planning_input_loaded",
        "gate_taxonomy_input_loaded",
    )
    for k in input_loaded:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    closure_generated = (
        "completed_phase_matrix_generated",
        "consolidation_closure_decision_summary_generated",
        "closure_boundary_freeze_generated",
        "non_claims_register_generated",
        "human_review_carryover_register_generated",
        "permanent_do_not_auto_execute_carryover_generated",
        "deferred_consolidation_action_pool_generated",
        "closure_readiness_gate_generated",
    )
    for k in closure_generated:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    ok("summary.completed_phase_count>=5", summary.get("completed_phase_count", 0) >= 5)
    ok("summary.total_inventory_entries==7391", summary.get("total_inventory_entries") == 7391)
    ok("summary.total_conflict_count==1830", summary.get("total_conflict_count") == 1830)
    ok("summary.acceptable_conflicts==1382", summary.get("acceptable_conflicts") == 1382)
    ok("summary.plan_revision_required==0", summary.get("plan_revision_required") == 0)
    ok("summary.permanent_do_not_auto_execute==914", summary.get("permanent_do_not_auto_execute") == 914)
    ok("summary.human_review_required==240", summary.get("human_review_required") == 240)
    ok("summary.missing_life_system_mapping_count==0", summary.get("missing_life_system_mapping_count") == 0)
    ok("summary.plan_revision_required_register_empty", summary.get("plan_revision_required_register_empty") is True)
    ok("summary.all_high_risk_conflicts_blocked", summary.get("all_high_risk_conflicts_blocked") is True)

    closure_closed = (
        "consolidation_planning_closed",
        "consolidation_dryrun_closed",
        "consolidation_post_review_closed",
        "consolidation_closed",
        "closure_allowed",
    )
    for k in closure_closed:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    readiness_false = (
        "real_migration_allowed",
        "ready_for_real_migration",
        "ready_for_file_move",
        "ready_for_file_delete",
        "ready_for_module_merge",
    )
    for k in readiness_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.automatic_execution_forbidden", summary.get("automatic_execution_forbidden") is True)
    ok("summary.protected_assets_auto_archive_forbidden", summary.get("protected_assets_auto_archive_forbidden") is True)

    retention = (
        "historical_test_logs_retention_verified",
        "correction_records_retention_verified",
        "verifier_reports_retention_verified",
        "go_no_go_packs_retention_verified",
    )
    for k in retention:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    boundary_preserved = (
        "developer_backend_boundary_preserved",
        "client_boundary_preserved",
        "life_system_mapping_preserved",
        "cognition_placeholder_not_runtime_verified",
        "future_placeholder_not_runtime_verified",
        "capability_candidate_no_fact_authority_verified",
        "capability_candidate_no_action_authority_verified",
    )
    for k in boundary_preserved:
        ok(f"summary.{k}", summary.get(k) is True, summary.get(k))

    side_effect_false = (
        "actual_consolidation_execution",
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

    ok("summary.no_runtime_executed", summary.get("no_runtime_executed") is True)
    ok("summary.no_new_runtime_enabled", summary.get("no_new_runtime_enabled") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.violations.empty", summary.get("violations") == [])

    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("closure_summary.closure_id", bool(closure_summary.get("closure_id")))
    ok("closure_summary.completed_phase_count>=5", closure_summary.get("completed_phase_count", 0) >= 5)
    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)

    phases = completed.get("phases") or []
    ok("completed.phase_count>=5", len(phases) >= 5)
    for i, p in enumerate(phases):
        ok(f"completed[{i}].status", p.get("status") == "GO")
        ok(f"completed[{i}].actual_file_move=false", p.get("actual_file_move_executed") is False)
        ok(f"completed[{i}].actual_file_delete=false", p.get("actual_file_delete_executed") is False)
        ok(f"completed[{i}].actual_module_merge=false", p.get("actual_module_merge_executed") is False)
        ok(f"completed[{i}].runtime_enabled=false", p.get("runtime_enabled") is False)
        ok(f"completed[{i}].final_decision", bool(p.get("final_decision")))
        ok(f"completed[{i}].phase_id", bool(p.get("phase_id")))
        ok(f"completed[{i}].output_dir", bool(p.get("output_dir")))
        ok(f"completed[{i}].role_in_closure", bool(p.get("role_in_closure")))
        ok(f"completed[{i}].verifier_verdict", p.get("verifier_verdict") in {"GO", "COMPLETE", "PENDING"})

    ok("decision_summary.closure_allowed", decision_summary.get("closure_allowed") is True)
    ok("decision_summary.real_migration_allowed=false", decision_summary.get("real_migration_allowed") is False)
    ok("decision_summary.plan_revision==0", decision_summary.get("plan_revision_required") == 0)
    ok("decision_summary.acceptable==1382", decision_summary.get("acceptable_conflicts") == 1382)
    ok("decision_summary.permanent==914", decision_summary.get("permanent_do_not_auto_execute") == 914)
    ok("decision_summary.human==240", decision_summary.get("human_review_required") == 240)

    freeze_keys = (
        "no-real-migration",
        "no-file-move",
        "no-file-delete",
        "no-file-rename",
        "no-module-merge",
        "no-auto-archive",
        "no-auto-delete-test-logs",
        "no-auto-delete-verifier-report",
        "no-auto-delete-go-no-go-pack",
        "no-auto-delete-phase-records",
        "no-client-dev-backend-mix",
        "no-cognition-placeholder-runtime",
        "no-capability-fact-authority",
        "no-capability-action-authority",
        "no-runtime",
        "no-write",
        "no-action",
        "no-speech",
    )
    for k in freeze_keys:
        ok(f"boundary_freeze.{k}", boundary_freeze.get(k) is True)

    ok("non_claims.count>=10", len(non_claims.get("non_claims") or []) >= 10)
    for i, claim in enumerate((non_claims.get("non_claims") or [])[:11]):
        ok(f"non_claims[{i}]", bool(claim))

    ok("human_carry.count==240", human_carry.get("human_review_required_count") == 240)
    ok("human_carry.auto_execute=false", human_carry.get("auto_execute_allowed") is False)
    ok("human_carry.manual_owner", human_carry.get("manual_owner_assignment_required") is True)
    ok("human_carry.high_risk_merge", human_carry.get("high_risk_merge_items", 0) >= 1)
    ok("human_carry.future_placeholder", human_carry.get("future_placeholder_current_code_items", 0) >= 1)

    ok("permanent_carry.count==914", permanent_carry.get("permanent_do_not_auto_execute_count") == 914)
    ok("permanent_carry.static_dnae", permanent_carry.get("static_dnae_rule_count", 0) >= 1)
    ok("permanent_carry.dynamic_protected", permanent_carry.get("dynamic_protected_asset_count", 0) >= 400)
    ok("permanent_carry.protected_eval_out", permanent_carry.get("protected_eval_out_items", 0) >= 400)
    ok("permanent_carry.protected_verifier", permanent_carry.get("protected_verifier_items", 0) >= 1)
    ok("permanent_carry.protected_go_no_go", permanent_carry.get("protected_go_no_go_items", 0) >= 1)

    ok("decision_summary.inventory==7391", decision_summary.get("total_inventory_entries") == 7391)
    ok("decision_summary.conflicts==1830", decision_summary.get("total_conflict_count") == 1830)
    ok("decision_summary.register_empty", decision_summary.get("plan_revision_required_register_empty") is True)
    ok("decision_summary.all_high_risk_blocked", decision_summary.get("all_high_risk_conflicts_blocked") is True)

    for i, cond in enumerate(readiness_gate.get("go_conditions") or []):
        ok(f"readiness.go[{i}]", bool(cond))
    for i, cond in enumerate(readiness_gate.get("no_go_conditions") or []):
        ok(f"readiness.no_go[{i}]", bool(cond))

    ok("deferred_pool.count>=15", deferred_pool.get("deferred_action_count", 0) >= 15)
    ok("deferred_pool.real_migration_started=false", deferred_pool.get("real_migration_started") is False)
    for i, item in enumerate((deferred_pool.get("deferred_actions") or [])[:15]):
        ok(f"deferred[{i}].auto_execute=false", item.get("auto_execute_allowed") is False)
        ok(f"deferred[{i}].action", bool(item.get("action")))

    ok("readiness_gate.ready_for_closure", readiness_gate.get("ready_for_closure") is True)
    ok("readiness_gate.blockers.empty", readiness_gate.get("blockers") == [])

    for report, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
        (no_action, "no_action"),
    ):
        ok(f"{name}.closure_only", report.get("closure_only") is True)
        ok(f"{name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{name}.violations.empty", report.get("violations") == [])
        ok(f"{name}.no_runtime_executed", report.get("no_runtime_executed") is True)

    for i, row in enumerate(input_root_matrix.get("rows", [])):
        ok(f"input_row[{i}].intake_id", bool(row.get("intake_id")))
        ok(f"input_row[{i}].fact_status", row.get("fact_status") == "not_fact")

    for i, opt in enumerate(next_phase.get("roadmap_decision_options") or []):
        ok(f"roadmap_option[{i}]", bool(opt))

    ok("summary.source_chain", summary.get("source_chain") == "luna_project_structure_consolidation_closure_v1")
    ok("decision_summary.fact_status", decision_summary.get("fact_status") == "not_fact")
    ok("human_carry.fact_status", human_carry.get("fact_status") == "not_fact")

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
