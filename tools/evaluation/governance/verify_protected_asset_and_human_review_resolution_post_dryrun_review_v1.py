#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Protected Asset and Human Review Resolution Post-DryRun Review v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_POST_DRYRUN_REVIEW_READY_FOR_CLOSURE"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-Closure-v1-001"

MIN_CHECKS = 300
BASELINE_REQUIREMENT = 240

FORBIDDEN_DECISIONS = [
    "DELETE_NOW",
    "MOVE_NOW",
    "MERGE_NOW",
    "ARCHIVE_NOW",
    "ENABLE_RUNTIME",
    "CHANGE_PHASE_VERDICT",
    "REMOVE_VERIFIER_REPORT",
    "REMOVE_GO_NO_GO_PACK",
    "REMOVE_TEST_LOG",
    "REMOVE_CORRECTION_RECORD",
]
FORBIDDEN_STATES = {"auto_executed", "file_moved", "file_deleted", "module_merged", "runtime_enabled"}


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "protected_asset_and_human_review_resolution_post_dryrun_review_v1_smoke_v0"),
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
    input_review = _load_json(root / "resolution_dryrun_input_review.json")
    hr_review = _load_json(root / "human_review_case_post_review.json")
    dnae_review = _load_json(root / "permanent_dnae_post_review.json")
    forbidden_dec = _load_json(root / "forbidden_decision_post_review.json")
    forbidden_state = _load_json(root / "forbidden_state_post_review.json")
    owner_review = _load_json(root / "owner_assignment_post_review.json")
    audit_review = _load_json(root / "audit_trace_post_review.json")
    rollback_review = _load_json(root / "rollback_post_review.json")
    boundary_review = _load_json(root / "protected_asset_boundary_post_review.json")
    readiness = _load_json(root / "resolution_post_dryrun_readiness_decision.json")
    governance_debt = _load_json(root / "governance_debt_review.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")
    no_delete = _load_json(root / "no_delete_boundary_report.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    idx = {r.get("intake_id"): r for r in input_root_matrix.get("rows", [])}
    for intake_id in (
        "resolution_dryrun",
        "planning",
        "roadmap_decision",
        "consolidation_closure",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.review_scope", summary.get("review_scope") == "protected_asset_and_human_review_resolution_post_dryrun_review_only")

    for field in (
        "dryrun_input_loaded",
        "planning_input_loaded",
        "consolidation_roadmap_input_loaded",
        "consolidation_closure_input_loaded",
        "resolution_dryrun_input_review_generated",
        "human_review_case_post_review_generated",
        "permanent_dnae_post_review_generated",
        "forbidden_decision_post_review_generated",
        "forbidden_state_post_review_generated",
        "owner_assignment_post_review_generated",
        "audit_trace_post_review_generated",
        "rollback_post_review_generated",
        "protected_asset_boundary_post_review_generated",
        "resolution_post_dryrun_readiness_decision_generated",
        "all_forbidden_decisions_blocked",
        "forbidden_states_absent",
        "audit_trace_is_dryrun_only",
        "rollback_is_dryrun_only",
        "protected_asset_boundary_pass",
        "ready_for_closure",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    ok("summary.reviewed_human_review_case_count==240", summary.get("reviewed_human_review_case_count") == 240)
    ok("summary.closed_no_execution_count==240", summary.get("closed_no_execution_count") == 240)
    ok("summary.final_owner_human_confirmed_count==0", summary.get("final_owner_human_confirmed_count") == 0)
    ok("summary.reviewed_permanent_dnae_case_count==914", summary.get("reviewed_permanent_dnae_case_count") == 914)
    ok("summary.permanent_do_not_auto_execute_count==914", summary.get("permanent_do_not_auto_execute_count") == 914)
    ok("summary.protected_conflict_count==448", summary.get("protected_conflict_count") == 448)
    ok("summary.static_dnae_rule_count==466", summary.get("static_dnae_rule_count") == 466)
    ok("summary.high_risk_merge_case_count==5", summary.get("high_risk_merge_case_count") == 5)
    ok("summary.future_placeholder_current_code_case_count==35", summary.get("future_placeholder_current_code_case_count") == 35)
    ok("summary.target_module_unclear_case_count==200", summary.get("target_module_unclear_case_count") == 200)
    ok("summary.owner_assignment_case_count==240", summary.get("owner_assignment_case_count") == 240)
    ok("summary.owner_type_count>=10", summary.get("owner_type_count", 0) >= 10)
    ok("summary.audit_trace_generated_count==1154", summary.get("audit_trace_generated_count") == 1154)
    ok("summary.rollback_ref_generated_count==1154", summary.get("rollback_ref_generated_count") == 1154)
    ok("summary.forbidden_decision_count==10", summary.get("forbidden_decision_count") == 10)
    ok("summary.forbidden_decision_blocked_count>=10", summary.get("forbidden_decision_blocked_count", 0) >= 10)
    ok("summary.unexpected_allowed_forbidden_decision_count==0", summary.get("unexpected_allowed_forbidden_decision_count") == 0)
    ok("summary.forbidden_state_count==5", summary.get("forbidden_state_count") == 5)
    ok("summary.forbidden_state_absent_count>=5", summary.get("forbidden_state_absent_count", 0) >= 5)
    ok("summary.unexpected_forbidden_state_count==0", summary.get("unexpected_forbidden_state_count") == 0)
    ok("summary.block_released_count==0", summary.get("block_released_count") == 0)
    ok("summary.override_executed_count==0", summary.get("override_executed_count") == 0)

    for field in (
        "actual_human_review_executed",
        "human_review_execution_allowed",
        "final_owner_human_confirmed",
        "protected_assets_modified",
        "permanent_blocks_modified",
        "permanent_block_override_allowed",
        "audit_committed",
        "rollback_executed",
        "ready_for_real_human_review_execution",
        "ready_for_protected_asset_modification",
        "ready_for_permanent_block_override",
        "ready_for_real_migration",
        "protected_assets_auto_delete_allowed",
        "protected_assets_auto_archive_allowed",
        "protected_assets_auto_move_allowed",
        "protected_assets_auto_merge_allowed",
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
    ):
        ok(f"summary.{field}=false", summary.get(field) is False, summary.get(field))

    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)
    ok("summary.source_chain", summary.get("source_chain") == "protected_asset_and_human_review_resolution_post_dryrun_review_v1")

    ok("input_review.review_id", bool(input_review.get("review_id")))
    ok("input_review.dryrun_input_loaded", input_review.get("dryrun_input_loaded") is True)
    ok("input_review.planning_input_loaded", input_review.get("planning_input_loaded") is True)
    ok("input_review.roadmap_input_loaded", input_review.get("roadmap_input_loaded") is True)
    ok("input_review.consolidation_closure_input_loaded", input_review.get("consolidation_closure_input_loaded") is True)
    ok("input_review.required_artifacts_loaded", input_review.get("required_artifacts_loaded") is True)
    ok("input_review.input_status", input_review.get("input_status") == "loaded")
    ok("input_review.missing.empty", input_review.get("missing_required_artifacts") == [])

    ok("hr_review.count==240", hr_review.get("reviewed_human_review_case_count") == 240)
    ok("hr_review.closed==240", hr_review.get("closed_no_execution_count") == 240)
    ok("hr_review.owner_confirmed==0", hr_review.get("final_owner_human_confirmed_count") == 0)
    ok("hr_review.actual_hr=false", hr_review.get("actual_human_review_executed") is False)
    ok("hr_review.auto_execute==0", hr_review.get("auto_execute_allowed_count") == 0)
    ok("hr_review.file_op==0", hr_review.get("file_operation_allowed_count") == 0)
    ok("hr_review.runtime==0", hr_review.get("runtime_allowed_count") == 0)
    ok("hr_review.high_risk==5", hr_review.get("high_risk_merge_case_count") == 5)
    ok("hr_review.future==35", hr_review.get("future_placeholder_current_code_case_count") == 35)
    ok("hr_review.target_unclear==200", hr_review.get("target_module_unclear_case_count") == 200)
    ok("hr_review.verdict", hr_review.get("verdict") == "all_240_closed_no_execution")

    ok("dnae_review.count==914", dnae_review.get("reviewed_permanent_dnae_case_count") == 914)
    ok("dnae_review.permanent==914", dnae_review.get("permanent_do_not_auto_execute_count") == 914)
    ok("dnae_review.protected==448", dnae_review.get("protected_conflict_count") == 448)
    ok("dnae_review.static==466", dnae_review.get("static_dnae_rule_count") == 466)
    ok("dnae_review.block_released==0", dnae_review.get("block_released_count") == 0)
    ok("dnae_review.override==0", dnae_review.get("override_executed_count") == 0)
    ok("dnae_review.assets_modified=false", dnae_review.get("protected_assets_modified") is False)
    ok("dnae_review.blocks_modified=false", dnae_review.get("permanent_blocks_modified") is False)
    ok("dnae_review.verdict", dnae_review.get("verdict") == "all_914_permanent_block_held")

    ok("forbidden_dec.count==10", forbidden_dec.get("forbidden_decision_count") == 10)
    ok("forbidden_dec.blocked>=10", forbidden_dec.get("forbidden_decision_blocked_count", 0) >= 10)
    ok("forbidden_dec.all_blocked", forbidden_dec.get("all_forbidden_decisions_blocked") is True)
    ok("forbidden_dec.unexpected==0", forbidden_dec.get("unexpected_allowed_forbidden_decision_count") == 0)
    ok("forbidden_dec.verdict", forbidden_dec.get("verdict") == "all_forbidden_decisions_blocked")
    for fd in FORBIDDEN_DECISIONS:
        ok(f"forbidden_dec.{fd}.blocked", fd in (forbidden_dec.get("blocked_decisions") or []))

    ok("forbidden_state.count==5", forbidden_state.get("forbidden_state_count") == 5)
    ok("forbidden_state.absent>=5", forbidden_state.get("forbidden_state_absent_count", 0) >= 5)
    ok("forbidden_state.all_absent", forbidden_state.get("forbidden_states_absent") is True)
    ok("forbidden_state.unexpected==0", forbidden_state.get("unexpected_forbidden_state_count") == 0)
    ok("forbidden_state.verdict", forbidden_state.get("verdict") == "forbidden_states_absent")

    ok("owner_review.count==240", owner_review.get("owner_assignment_case_count") == 240)
    ok("owner_review.type_count>=10", owner_review.get("owner_type_count", 0) >= 10)
    ok("owner_review.human_confirmed=false", owner_review.get("final_owner_human_confirmed") is False)
    ok("owner_review.cannot_auto_assign", owner_review.get("cannot_auto_assign") is True)
    ok("owner_review.committed=false", owner_review.get("owner_assignment_committed") is False)
    ok("owner_review.verdict", owner_review.get("verdict") == "simulated_owner_assignment_only")

    ok("audit_review.count==1154", audit_review.get("audit_trace_generated_count") == 1154)
    ok("audit_review.committed=false", audit_review.get("audit_committed") is False)
    ok("audit_review.committed_count==0", audit_review.get("audit_committed_count") == 0)
    ok("audit_review.fields_present", audit_review.get("required_trace_fields_present") is True)
    ok("audit_review.dryrun_only", audit_review.get("audit_trace_is_dryrun_only") is True)
    ok("audit_review.verdict", audit_review.get("verdict") == "dryrun_audit_refs_only")

    ok("rollback_review.count==1154", rollback_review.get("rollback_ref_generated_count") == 1154)
    ok("rollback_review.executed=false", rollback_review.get("rollback_executed") is False)
    ok("rollback_review.executed_count==0", rollback_review.get("rollback_executed_count") == 0)
    ok("rollback_review.dryrun_only", rollback_review.get("rollback_is_dryrun_only") is True)
    ok("rollback_review.no_file_rollback", rollback_review.get("no_file_rollback_needed_current_phase") is True)
    ok("rollback_review.verdict", rollback_review.get("verdict") == "dryrun_rollback_refs_only")

    ok("boundary_review.auto_delete=false", boundary_review.get("protected_assets_auto_delete_allowed") is False)
    ok("boundary_review.auto_archive=false", boundary_review.get("protected_assets_auto_archive_allowed") is False)
    ok("boundary_review.auto_move=false", boundary_review.get("protected_assets_auto_move_allowed") is False)
    ok("boundary_review.auto_merge=false", boundary_review.get("protected_assets_auto_merge_allowed") is False)
    ok("boundary_review.modified=false", boundary_review.get("protected_assets_modified") is False)
    ok("boundary_review.pass", boundary_review.get("protected_asset_boundary_pass") is True)

    ok("readiness.verdict", readiness.get("review_verdict") == "GO")
    ok("readiness.blockers.empty", readiness.get("blockers") == [])
    ok("readiness.ready_for_closure", readiness.get("ready_for_closure") is True)
    ok("readiness.real_hr=false", readiness.get("ready_for_real_human_review_execution") is False)
    ok("readiness.real_migration=false", readiness.get("ready_for_real_migration") is False)
    ok("readiness.next_phase", readiness.get("recommended_next_phase") == NEXT_PHASE)

    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)
    ok("next.recommended_next_phase", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    ok("governance_debt.items>=4", len(governance_debt.get("debt_items") or []) >= 4)

    for report, name in (
        (no_move, "no_move"),
        (no_delete, "no_delete"),
        (no_runtime, "no_runtime"),
        (no_write, "no_write"),
    ):
        ok(f"{name}.review_only", report.get("review_only") is True)
        ok(f"{name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{name}.violations.empty", report.get("violations") == [])
        ok(f"{name}.actual_hr=false", report.get("actual_human_review_executed") is False)
        ok(f"{name}.no_runtime_executed", report.get("no_runtime_executed") is True)

    for i, row in enumerate(input_root_matrix.get("rows", [])):
        ok(f"input_row[{i}].intake_id", bool(row.get("intake_id")))
        ok(f"input_row[{i}].fact_status", row.get("fact_status") == "not_fact")

    for i, note in enumerate(readiness.get("conditional_notes") or []):
        ok(f"readiness.note[{i}]", bool(note))

    dryrun_path = idx.get("resolution_dryrun", {}).get("path")
    if dryrun_path and Path(dryrun_path).exists():
        dryrun_root = Path(dryrun_path)
        hr_cases = _load_json(dryrun_root / "human_review_dryrun_cases.json")
        dnae_cases = _load_json(dryrun_root / "permanent_dnae_dryrun_cases.json")
        sm_traces = _load_json(dryrun_root / "review_state_machine_dryrun_traces.json")
        audits = _load_json(dryrun_root / "audit_trace_dryrun_results.json")
        rollbacks = _load_json(dryrun_root / "rollback_dryrun_results.json")

        hr_list = hr_cases.get("cases") or []
        dnae_list = dnae_cases.get("cases") or []
        hr_trace_by_case = {
            t.get("case_ref"): t
            for t in (sm_traces.get("traces") or [])
            if str(t.get("case_ref", "")).startswith("HRDRY")
        }

        for i, c in enumerate(hr_list[:50]):
            trace = hr_trace_by_case.get(c.get("review_case_id"), {})
            ok(f"dryrun_hr[{i}].closed_no_execution", trace.get("final_state") == "closed_no_execution")
            ok(f"dryrun_hr[{i}].auto_execute=false", c.get("auto_execute_allowed") is False)
            ok(f"dryrun_hr[{i}].file_op=false", c.get("file_operation_allowed") is False)

        for i, c in enumerate(dnae_list[:50]):
            ok(f"dryrun_dnae[{i}].permanent", c.get("simulated_decision") == "PERMANENT_DO_NOT_AUTO_EXECUTE")
            ok(f"dryrun_dnae[{i}].block_released=false", c.get("block_released") is False)
            ok(f"dryrun_dnae[{i}].override=false", c.get("override_executed") is False)

        for i, t in enumerate((sm_traces.get("traces") or [])[:40]):
            visited = set(t.get("states_visited") or [])
            ok(f"dryrun_trace[{i}].no_forbidden", not (visited & FORBIDDEN_STATES))

        for i, a in enumerate((audits.get("traces") or [])[:30]):
            ok(f"dryrun_audit[{i}].not_committed", a.get("audit_committed") is False)

        for i, r in enumerate((rollbacks.get("results") or [])[:30]):
            ok(f"dryrun_rollback[{i}].not_executed", r.get("rollback_executed") is False)

    for obj_name, obj in (
        ("input_review", input_review),
        ("hr_review", hr_review),
        ("dnae_review", dnae_review),
        ("forbidden_dec", forbidden_dec),
        ("forbidden_state", forbidden_state),
        ("owner_review", owner_review),
        ("audit_review", audit_review),
        ("rollback_review", rollback_review),
        ("boundary_review", boundary_review),
        ("readiness", readiness),
    ):
        ok(f"{obj_name}.fact_status", obj.get("fact_status") == "not_fact")
        ok(f"{obj_name}.write_allowed=false", obj.get("write_allowed") is False)

    ok("summary.fact_status", summary.get("fact_status") == "not_fact")

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
