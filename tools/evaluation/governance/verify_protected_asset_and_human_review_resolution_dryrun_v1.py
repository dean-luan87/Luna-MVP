#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Protected Asset and Human Review Resolution DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Protected-Asset-and-Human-Review-Resolution-DryRun-v1-001"
FINAL_DECISION = "PROTECTED_ASSET_AND_HUMAN_REVIEW_RESOLUTION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Protected-Asset-and-Human-Review-Resolution-Post-DryRun-Review-v1-001"

MIN_CHECKS = 320
BASELINE_REQUIREMENT = 260


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parents[3]
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-root",
        default=str(repo_root / "_eval_out" / "protected_asset_and_human_review_resolution_dryrun_v1_smoke_v0"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    exec_plan = _load_json(root / "resolution_dryrun_execution_plan.json")
    hr_cases = _load_json(root / "human_review_dryrun_cases.json")
    dnae_cases = _load_json(root / "permanent_dnae_dryrun_cases.json")
    owners = _load_json(root / "owner_assignment_dryrun_results.json")
    decisions = _load_json(root / "review_decision_dryrun_results.json")
    sm_traces = _load_json(root / "review_state_machine_dryrun_traces.json")
    audits = _load_json(root / "audit_trace_dryrun_results.json")
    rollbacks = _load_json(root / "rollback_dryrun_results.json")
    matrix = _load_json(root / "resolution_dryrun_summary_matrix.json")
    readiness = _load_json(root / "resolution_dryrun_readiness_decision.json")
    forbidden_dec = _load_json(root / "forbidden_decision_block_report.json")
    forbidden_state = _load_json(root / "forbidden_state_absence_report.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_move = _load_json(root / "no_file_move_boundary_report.json")

    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "protected_asset_and_human_review_resolution_dryrun_only")

    for field in (
        "planning_input_loaded",
        "consolidation_roadmap_input_loaded",
        "consolidation_closure_input_loaded",
        "consolidation_post_review_input_loaded",
        "protected_asset_policy_loaded",
        "human_review_resolution_policy_loaded",
        "permanent_dnae_policy_loaded",
        "manual_owner_assignment_policy_loaded",
        "review_decision_schema_loaded",
        "review_state_machine_loaded",
        "audit_trace_policy_loaded",
        "rollback_policy_loaded",
        "resolution_dryrun_execution_plan_generated",
        "human_review_dryrun_cases_generated",
        "permanent_dnae_dryrun_cases_generated",
        "owner_assignment_dryrun_results_generated",
        "review_decision_dryrun_results_generated",
        "review_state_machine_dryrun_traces_generated",
        "audit_trace_dryrun_results_generated",
        "rollback_dryrun_results_generated",
        "resolution_dryrun_summary_matrix_generated",
        "resolution_dryrun_readiness_decision_generated",
        "dryrun_simulated_execution",
        "ready_for_post_dryrun_review",
        "forbidden_states_absent",
        "auto_executed_state_absent",
        "file_moved_state_absent",
        "file_deleted_state_absent",
        "module_merged_state_absent",
        "runtime_enabled_state_absent",
        "no_runtime_executed",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    ok("summary.human_review_input_count==240", summary.get("human_review_input_count") == 240)
    ok("summary.human_review_case_count==240", summary.get("human_review_case_count") == 240)
    ok("summary.permanent_dnae_input_count==914", summary.get("permanent_dnae_input_count") == 914)
    ok("summary.permanent_dnae_case_count==914", summary.get("permanent_dnae_case_count") == 914)
    ok("summary.protected_conflict_count==448", summary.get("protected_conflict_count") == 448)
    ok("summary.static_dnae_rule_count==466", summary.get("static_dnae_rule_count") == 466)
    ok("summary.high_risk_merge_case_count==5", summary.get("high_risk_merge_case_count") == 5)
    ok("summary.future_placeholder_current_code_case_count==35", summary.get("future_placeholder_current_code_case_count") == 35)
    ok("summary.target_module_unclear_case_count==200", summary.get("target_module_unclear_case_count") == 200)
    ok("summary.owner_assignment_case_count==240", summary.get("owner_assignment_case_count") == 240)
    ok("summary.owner_type_count>=10", summary.get("owner_type_count", 0) >= 10)
    ok("summary.allowed_review_decision_count>=12", summary.get("allowed_review_decision_count", 0) >= 12)
    ok("summary.forbidden_review_decision_count>=10", summary.get("forbidden_review_decision_count", 0) >= 10)
    ok("summary.forbidden_decision_blocked_count>=10", summary.get("forbidden_decision_blocked_count", 0) >= 10)
    ok("summary.review_state_count>=9", summary.get("review_state_count", 0) >= 9)
    ok("summary.forbidden_state_absent_count>=5", summary.get("forbidden_state_absent_count", 0) >= 5)
    ok("summary.audit_trace_generated_count>=1154", summary.get("audit_trace_generated_count", 0) >= 1154)
    ok("summary.rollback_ref_generated_count>=1154", summary.get("rollback_ref_generated_count", 0) >= 1154)

    for field in (
        "actual_human_review_executed",
        "human_review_execution_allowed",
        "final_owner_human_confirmed",
        "protected_assets_modified",
        "permanent_blocks_modified",
        "permanent_block_override_allowed",
        "override_executed",
        "block_released",
        "protected_assets_auto_delete_allowed",
        "protected_assets_auto_archive_allowed",
        "protected_assets_auto_move_allowed",
        "protected_assets_auto_merge_allowed",
        "ready_for_real_human_review_execution",
        "ready_for_protected_asset_modification",
        "ready_for_permanent_block_override",
        "ready_for_real_migration",
        "audit_committed",
        "rollback_executed",
    ):
        ok(f"summary.{field}=false", summary.get(field) is False, summary.get(field))

    for field in (
        "delete_now_decision_blocked",
        "move_now_decision_blocked",
        "merge_now_decision_blocked",
        "archive_now_decision_blocked",
        "enable_runtime_decision_blocked",
        "change_phase_verdict_decision_blocked",
        "remove_verifier_report_decision_blocked",
        "remove_go_no_go_pack_decision_blocked",
        "remove_test_log_decision_blocked",
        "remove_correction_record_decision_blocked",
    ):
        ok(f"summary.{field}", summary.get(field) is True, summary.get(field))

    side_effect_false = (
        "actual_file_move_executed",
        "actual_file_delete_executed",
        "actual_file_rename_executed",
        "actual_module_merge_executed",
        "docs_modified_by_dryrun",
        "readme_modified_by_dryrun",
        "phase_verdict_table_modified_by_dryrun",
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
    )
    for k in side_effect_false:
        ok(f"summary.{k}=false", summary.get(k) is False, summary.get(k))

    ok("summary.violations.empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("exec_plan.dryrun_only", exec_plan.get("execution_mode") == "dryrun_only")
    ok("exec_plan.human==240", exec_plan.get("human_review_input_count") == 240)
    ok("exec_plan.dnae==914", exec_plan.get("permanent_dnae_input_count") == 914)
    ok("exec_plan.no_human_review", exec_plan.get("actual_human_review_executed") is False)

    ok("hr_cases.count==240", hr_cases.get("case_count") == 240)
    ok("dnae_cases.count==914", dnae_cases.get("case_count") == 914)
    ok("owners.count==240", owners.get("assignment_count") == 240)
    ok("decisions.count==240", decisions.get("result_count") == 240)
    ok("traces.count==1154", sm_traces.get("trace_count") == 1154)
    ok("audits.count==1154", audits.get("trace_count") == 1154)
    ok("rollbacks.count==1154", rollbacks.get("result_count") == 1154)

    hr_list = hr_cases.get("cases") or []
    dnae_list = dnae_cases.get("cases") or []

    for i, c in enumerate(hr_list[:60]):
        ok(f"hr[{i}].auto_execute=false", c.get("auto_execute_allowed") is False)
        ok(f"hr[{i}].file_op=false", c.get("file_operation_allowed") is False)
        ok(f"hr[{i}].runtime=false", c.get("runtime_allowed") is False)
        ok(f"hr[{i}].category", bool(c.get("review_category")))
        ok(f"hr[{i}].decision", bool(c.get("selected_simulated_decision")))

    for i, c in enumerate(dnae_list[:60]):
        ok(f"dnae[{i}].decision=PERMANENT", c.get("simulated_decision") == "PERMANENT_DO_NOT_AUTO_EXECUTE")
        ok(f"dnae[{i}].override=false", c.get("override_executed") is False)
        ok(f"dnae[{i}].block_released=false", c.get("block_released") is False)
        ok(f"dnae[{i}].auto_execute=false", c.get("auto_execute_allowed") is False)

    for i, o in enumerate((owners.get("assignments") or [])[:30]):
        ok(f"owner[{i}].cannot_auto_assign", o.get("cannot_auto_assign") is True)
        ok(f"owner[{i}].human_confirmed=false", o.get("final_owner_human_confirmed") is False)

    for i, d in enumerate((decisions.get("results") or [])[:30]):
        ok(f"decision[{i}].allowed", d.get("allowed") is True)

    forbidden_states = {"auto_executed", "file_moved", "file_deleted", "module_merged", "runtime_enabled"}
    for i, t in enumerate((sm_traces.get("traces") or [])[:40]):
        visited = set(t.get("states_visited") or [])
        ok(f"trace[{i}].no_forbidden", not (visited & forbidden_states))
        ok(f"trace[{i}].dryrun_only", t.get("execution_status") == "dryrun_only")

    for i, a in enumerate((audits.get("traces") or [])[:30]):
        ok(f"audit[{i}].not_committed", a.get("audit_committed") is False)
        ok(f"audit[{i}].source_chain", bool(a.get("source_chain")))

    for i, r in enumerate((rollbacks.get("results") or [])[:30]):
        ok(f"rollback[{i}].not_executed", r.get("rollback_executed") is False)
        ok(f"rollback[{i}].required", r.get("rollback_required") is True)

    for i, b in enumerate(forbidden_dec.get("blocks") or []):
        ok(f"forbidden_dec[{i}].blocked", b.get("allowed") is False)

    ok("forbidden_state.absent", forbidden_state.get("forbidden_states_absent") is True)
    ok("matrix.audit>=1154", matrix.get("audit_trace_generated_count", 0) >= 1154)
    ok("matrix.hr_by_cat.high_risk==5", matrix.get("human_review_by_category", {}).get("high_risk_merge") == 5)
    ok("matrix.hr_by_cat.future==35", matrix.get("human_review_by_category", {}).get("future_placeholder_current_code") == 35)
    ok("matrix.hr_by_cat.target==200", matrix.get("human_review_by_category", {}).get("target_module_unclear") == 200)

    ok("readiness.ready_for_post_dryrun", readiness.get("ready_for_post_dryrun_review") is True)
    ok("readiness.real_hr=false", readiness.get("ready_for_real_human_review_execution") is False)
    ok("next.final_decision", next_phase.get("final_decision") == FINAL_DECISION)

    ok("no_move.dryrun_only", no_move.get("dryrun_only") is True)
    ok("no_move.human_review=false", no_move.get("actual_human_review_executed") is False)

    ok("summary.source_chain", summary.get("source_chain") == "protected_asset_and_human_review_resolution_dryrun_v1")

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
