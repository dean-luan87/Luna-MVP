#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Decision Center Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_decision_center_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONFLICT_RULES,
    DECISION_ACTIONS,
    DECISION_CENTER_DUTIES,
    DECISION_CENTER_NOT,
    FAILURE_ESCALATION_ROUTES,
    FINAL_DECISION_GO,
    INPUT_CONTRACT_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CONTRACT_FIELDS,
    PHASE_ID,
    PRIORITY_LAYERS,
    RUNTIME_BOUNDARY_MATRIX_FALSE,
    SCOPE,
    UPSTREAM_CORE_RESUME_FINAL,
    UPSTREAM_CORE_RESUME_NEXT,
)

MIN_CHECKS = 191

REQUIRED = (
    "decision_center_planning_policy_v1.json",
    "midplatform_core_resume_input_review_v1.json",
    "decision_center_role_definition_v1.json",
    "decision_center_input_contract_v1.json",
    "decision_center_output_contract_v1.json",
    "decision_action_taxonomy_v1.json",
    "decision_priority_and_conflict_policy_v1.json",
    "constitution_constraint_consumption_plan_v1.json",
    "validation_result_consumption_plan_v1.json",
    "health_signal_consumption_plan_v1.json",
    "whitebox_visibility_consumption_plan_v1.json",
    "evidence_confidence_consumption_plan_v1.json",
    "task_context_consumption_plan_v1.json",
    "failure_route_and_escalation_decision_plan_v1.json",
    "decision_to_task_response_boundary_plan_v1.json",
    "decision_center_runtime_boundary_matrix_v1.json",
    "decision_center_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "decision_center_planning_decision_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_decision_center_planning"
        ),
    )
    p.add_argument(
        "--core-resume-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_core_architecture_resume"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    core_root = Path(args.core_resume_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    core_vr = _load(core_root / "verifier_report.json")
    core_sm = _load(core_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "decision_center_planning_policy_v1.json")
    resume_input = _load(root / "midplatform_core_resume_input_review_v1.json")
    role = _load(root / "decision_center_role_definition_v1.json")
    input_contract = _load(root / "decision_center_input_contract_v1.json")
    output_contract = _load(root / "decision_center_output_contract_v1.json")
    actions = _load(root / "decision_action_taxonomy_v1.json")
    priority = _load(root / "decision_priority_and_conflict_policy_v1.json")
    constitution = _load(root / "constitution_constraint_consumption_plan_v1.json")
    validation = _load(root / "validation_result_consumption_plan_v1.json")
    health = _load(root / "health_signal_consumption_plan_v1.json")
    whitebox = _load(root / "whitebox_visibility_consumption_plan_v1.json")
    evidence = _load(root / "evidence_confidence_consumption_plan_v1.json")
    task_ctx = _load(root / "task_context_consumption_plan_v1.json")
    failure = _load(root / "failure_route_and_escalation_decision_plan_v1.json")
    task_boundary = _load(root / "decision_to_task_response_boundary_plan_v1.json")
    runtime_matrix = _load(root / "decision_center_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "decision_center_dryrun_plan_v1.json")
    planning_decision = _load(root / "decision_center_planning_decision_v1.json")

    ok("upstream.core_go", core_vr.get("verifier") == "GO")
    ok("upstream.core_final", core_sm.get("final_decision") == UPSTREAM_CORE_RESUME_FINAL)
    ok("upstream.core_next", core_sm.get("recommended_next_phase") == UPSTREAM_CORE_RESUME_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("decision_center_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.planning", policy.get("planning_not_runtime") is True)

    ok("resume.pass", resume_input.get("review_pass") is True)
    ok("resume.ocr_sealed", resume_input.get("ocr_local_check_sealed") is True)
    ok("resume.whitebox", resume_input.get("whitebox_absorption_complete") is True)
    ok("resume.val_gate", resume_input.get("validation_engineering_remains_gatekeeper") is True)
    ok("resume.constitution", resume_input.get("constitution_remains_rule_source") is True)
    ok("resume.health", resume_input.get("health_remains_pressure_signal_source") is True)

    ok("role.duties10", len(role.get("decision_center_duties") or []) == 10)
    for duty in DECISION_CENTER_DUTIES:
        ok(f"duty.{duty[:18]}", duty in (role.get("decision_center_duties") or []))

    ok("role.not9", len(role.get("decision_center_is_not") or []) == 9)
    for not_role in DECISION_CENTER_NOT:
        ok(f"not.{not_role[:15]}", not_role in (role.get("decision_center_is_not") or []))

    ok("input.candidate", input_contract.get("candidate_only") is True)
    ok("input.fields15", len(input_contract.get("required_fields") or []) == 15)
    for field in INPUT_CONTRACT_FIELDS:
        ok(f"input.{field[:15]}", field in (input_contract.get("required_fields") or []))

    ok("output.type", output_contract.get("output_type") == "decision_candidate")
    ok("output.fields19", len(output_contract.get("required_fields") or []) == 19)
    for field in OUTPUT_CONTRACT_FIELDS:
        ok(f"output.{field[:15]}", field in (output_contract.get("required_fields") or []))
    defaults = output_contract.get("defaults") or {}
    ok("output.candidate", defaults.get("candidate_only") is True)
    ok("output.no_task_resp", defaults.get("task_response_generation_allowed") is False)
    ok("output.no_user", defaults.get("user_output_allowed") is False)
    ok("output.no_memory", defaults.get("memory_write_allowed") is False)
    ok("output.no_wm", defaults.get("world_model_write_allowed") is False)

    ok("actions.count12", len(actions.get("actions") or []) == 12)
    for action in DECISION_ACTIONS:
        ok(f"action.{action[:18]}", action in (actions.get("actions") or []))

    ok("priority.layers9", len(priority.get("priority_layers") or []) == 9)
    for layer in PRIORITY_LAYERS:
        ok(f"priority.{layer['priority']}", any(
            l.get("priority") == layer["priority"] for l in (priority.get("priority_layers") or [])
        ))
    for rule in CONFLICT_RULES:
        ok(f"conflict.{rule[:18]}", rule in (priority.get("conflict_rules") or []))

    ok("constitution.consume", constitution.get("consumes_rule_refs_not_writes_rules") is True)
    ok("constitution.highest", constitution.get("general_constitution_highest_priority") is True)
    ok("constitution.overlay", constitution.get("personalized_constitution_overlay_only") is True)
    ok("constitution.conservative", constitution.get("constitution_conflict_conservative_decision") is True)

    ok("validation.pass_cond", validation.get("validation_pass_allows_forward_if_no_higher_block") is True)
    ok("validation.fail_route", validation.get("validation_fail_triggers_block_hold_issue_trace") is True)
    ok("validation.no_exec", validation.get("decision_center_does_not_execute_validation_gates") is True)

    ok("health.pressure", health.get("health_signal_is_pressure_status_context") is True)
    ok("health.no_score", health.get("no_numeric_health_score_invented") is True)
    ok("health.reserved", health.get("health_metric_definition_status") == "reserved_not_defined")
    ok("health.no_auto_auth", health.get("health_does_not_auto_authorize_execution") is True)

    ok("whitebox.visibility", whitebox.get("whitebox_provides_explainability_visibility") is True)
    ok("whitebox.no_decide", whitebox.get("whitebox_does_not_decide") is True)
    ok("whitebox.node_not_global", whitebox.get("node_level_evidence_cannot_define_global_status") is True)

    ok("evidence.complete", evidence.get("evidence_completeness_required") is True)
    ok("evidence.source_chain", evidence.get("source_chain_required") is True)
    ok("evidence.low_conf", evidence.get("low_confidence_leads_reobserve_hold") is True)

    ok("task.influence", task_ctx.get("task_context_influences_action_preference") is True)
    ok("task.no_override", task_ctx.get("task_context_cannot_override_constitution_validation") is True)

    ok("failure.count7", len(failure.get("routes") or []) == 7)
    for route in FAILURE_ESCALATION_ROUTES:
        ok(f"fail.{route['trigger'][:12]}", any(
            x.get("trigger") == route["trigger"] for x in (failure.get("routes") or [])
        ))

    ok("boundary.dec_not_task", task_boundary.get("decision_candidate_not_task_response_candidate") is True)
    ok("boundary.allow_not_output", task_boundary.get("allow_candidate_forward_not_user_output") is True)
    ok("boundary.task_sep", task_boundary.get("task_response_requires_separate_integration_phase") is True)

    ok("runtime.all_false", runtime_matrix.get("all_runtime_actions_false") is True)
    for field in RUNTIME_BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:15]}", runtime_matrix.get("matrix", {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    ok("decision.pass", planning_decision.get("planning_pass") is True)
    ok("decision.final", planning_decision.get("final_decision") == FINAL_DECISION_GO)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "planning_not_runtime": True,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
