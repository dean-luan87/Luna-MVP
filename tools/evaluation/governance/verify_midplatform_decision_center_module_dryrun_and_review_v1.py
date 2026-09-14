#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Decision Center Module DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_decision_center_module_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CONFLICT_RULES,
    DECISION_ACTIONS,
    FINAL_DECISION_GO,
    INPUT_CONTRACT_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CONTRACT_FIELDS,
    PHASE_ID,
    PRIORITY_LAYERS,
    RATIONALE_REQUIREMENTS,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)

MIN_CHECKS = 203

REQUIRED = (
    "decision_center_module_dryrun_review_policy_v1.json",
    "decision_center_planning_input_review_v1.json",
    "decision_center_model_candidate_v1.json",
    "sample_decision_request_candidate_v1.json",
    "sample_decision_candidate_v1.json",
    "constitution_binding_dryrun_review_v1.json",
    "validation_binding_dryrun_review_v1.json",
    "health_binding_dryrun_review_v1.json",
    "whitebox_binding_dryrun_review_v1.json",
    "factory_candidate_binding_dryrun_review_v1.json",
    "decision_priority_conflict_dryrun_review_v1.json",
    "decision_action_taxonomy_dryrun_review_v1.json",
    "decision_rationale_traceability_review_v1.json",
    "decision_to_task_response_boundary_review_v1.json",
    "decision_center_boundary_audit_v1.json",
    "decision_center_blocked_path_result_v1.json",
    "decision_center_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
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
            "midplatform_decision_center_module_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_decision_center_module_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    summary = _load(root / "summary.json")
    model = _load(root / "decision_center_model_candidate_v1.json")
    sample_req = _load(root / "sample_decision_request_candidate_v1.json")
    sample_dec = _load(root / "sample_decision_candidate_v1.json")
    constitution = _load(root / "constitution_binding_dryrun_review_v1.json")
    validation = _load(root / "validation_binding_dryrun_review_v1.json")
    health = _load(root / "health_binding_dryrun_review_v1.json")
    whitebox = _load(root / "whitebox_binding_dryrun_review_v1.json")
    factory = _load(root / "factory_candidate_binding_dryrun_review_v1.json")
    priority = _load(root / "decision_priority_conflict_dryrun_review_v1.json")
    actions = _load(root / "decision_action_taxonomy_dryrun_review_v1.json")
    rationale = _load(root / "decision_rationale_traceability_review_v1.json")
    task_boundary = _load(root / "decision_to_task_response_boundary_review_v1.json")
    boundary = _load(root / "decision_center_boundary_audit_v1.json")
    blocked = _load(root / "decision_center_blocked_path_result_v1.json")
    closure = _load(root / "decision_center_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("decision_center_module_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.module_id", model.get("module_id") == "midplatform_decision_center_v1")
    ok("model.type", model.get("module_type") == "core_midplatform_governance_module")
    ok("model.role", model.get("role") == "decision_arbitration_and_candidate_routing")
    ok("model.no_runtime", model.get("runtime_enabled_now") is False)
    ok("model.constitution", model.get("consumes_constitution") is True)
    ok("model.validation", model.get("consumes_validation") is True)
    ok("model.health", model.get("consumes_health") is True)
    ok("model.whitebox", model.get("consumes_whitebox_visibility") is True)
    ok("model.candidate", model.get("consumes_candidate_and_evidence") is True)
    ok("model.no_rulemaking", model.get("rulemaking_allowed") is False)
    ok("model.no_val_exec", model.get("validation_execution_allowed") is False)
    ok("model.no_health_auth", model.get("health_metric_authoring_allowed") is False)
    ok("model.no_provider", model.get("provider_invocation_allowed") is False)
    ok("model.no_user", model.get("user_output_allowed") is False)
    ok("model.no_memory", model.get("memory_write_allowed") is False)
    ok("model.no_wm", model.get("world_model_write_allowed") is False)
    ok("model.emit_decision", model.get("emits_decision_candidate") is True)
    ok("model.no_task_resp", model.get("emits_task_response_candidate") is False)
    ok("model.not_kingdom", model.get("not_independent_kingdom") is True)

    ok("req.candidate_only", sample_req.get("candidate_only") is True)
    for field in INPUT_CONTRACT_FIELDS:
        ok(f"req.{field[:15]}", field in sample_req)

    ok("dec.candidate_only", sample_dec.get("candidate_only") is True)
    ok("dec.no_task", sample_dec.get("task_response_generation_allowed") is False)
    ok("dec.no_user", sample_dec.get("user_output_allowed") is False)
    ok("dec.no_memory", sample_dec.get("memory_write_allowed") is False)
    ok("dec.no_wm", sample_dec.get("world_model_write_allowed") is False)
    ok("dec.rationale", len(sample_dec.get("rationale_refs") or []) > 0)
    ok("dec.whitebox_refs", len(sample_dec.get("whitebox_refs") or []) > 0)
    for field in OUTPUT_CONTRACT_FIELDS:
        ok(f"dec.{field[:15]}", field in sample_dec)

    ok("const.pass", constitution.get("dryrun_and_review_pass") is True)
    ok("const.no_write", constitution.get("decision_center_does_not_write_constitution") is True)
    ok("const.highest", constitution.get("general_constitution_highest_priority") is True)

    ok("val.pass", validation.get("dryrun_and_review_pass") is True)
    ok("val.no_gate", validation.get("decision_center_does_not_execute_validation_gate") is True)

    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    ok("health.reserved", health.get("health_metric_definition_status") == "reserved_not_defined")

    ok("wb.pass", whitebox.get("dryrun_and_review_pass") is True)
    ok("wb.no_decide", whitebox.get("whitebox_does_not_decide") is True)

    ok("factory.pass", factory.get("dryrun_and_review_pass") is True)
    ok("factory.domains5", len(factory.get("domain_binding_pattern") or []) >= 5)

    ok("priority.pass", priority.get("dryrun_and_review_pass") is True)
    ok("priority.layers9", priority.get("layer_count") == 9)
    for layer in PRIORITY_LAYERS:
        ok(f"priority.{layer['priority']}", any(
            l.get("priority") == layer["priority"] for l in (priority.get("priority_layers") or [])
        ))
    for rule in CONFLICT_RULES:
        ok(f"conflict.{rule[:18]}", rule in (priority.get("conflict_rules") or []))

    ok("actions.pass", actions.get("dryrun_and_review_pass") is True)
    ok("actions.count13", actions.get("action_count") == 13)
    for action in DECISION_ACTIONS:
        ok(f"action.{action[:18]}", action in (actions.get("actions") or []))

    ok("rationale.pass", rationale.get("dryrun_and_review_pass") is True)
    ok("rationale.sample", rationale.get("sample_decision_has_rationale_refs") is True)
    for req in RATIONALE_REQUIREMENTS:
        ok(f"rationale.{req[:18]}", req in (rationale.get("requirements") or []))

    ok("boundary.pass", task_boundary.get("dryrun_and_review_pass") is True)
    ok("boundary.dec_not_task", task_boundary.get("decision_candidate_not_task_response_candidate") is True)
    ok("boundary.no_speak", task_boundary.get("decision_center_cannot_directly_speak_to_user") is True)
    ok("boundary.sample_no_task", task_boundary.get("sample_task_response_allowed_false") is True)

    ok("audit.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("audit.forbidden", boundary.get("forbidden_actions_absent") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count14", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp[:20]}", any(
            x.get("blocked_path") == bp and x.get("blocked") is True
            for x in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.model", closure.get("model_candidate_valid") is True)
    ok("closure.bindings5", closure.get("five_bindings_verified") is True)

    ok("next.flow", next_route.get("ready_for_candidate_evidence_flow_integration_planning") is True)
    ok("next.no_runtime", next_route.get("decision_center_runtime_enabled") is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
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
