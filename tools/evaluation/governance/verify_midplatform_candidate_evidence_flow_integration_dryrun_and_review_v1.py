#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Candidate Evidence Flow Integration DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_candidate_evidence_flow_integration_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SAMPLE_CANDIDATE_TYPES,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_candidate_evidence_flow_integration_planning_v1 import (
    CANDIDATE_REQUIRED_FIELDS,
    DECISION_REQUEST_FIELDS,
    FLOW_INTEGRITY_RULES,
    VALIDATION_RESULT_STATES,
)

MIN_CHECKS = 189

REQUIRED = (
    "candidate_evidence_flow_dryrun_review_policy_v1.json",
    "candidate_evidence_flow_planning_input_review_v1.json",
    "candidate_evidence_flow_model_candidate_v1.json",
    "sample_candidate_intake_result_v1.json",
    "sample_domain_config_binding_result_v1.json",
    "sample_evidence_pack_binding_result_v1.json",
    "sample_validation_result_binding_result_v1.json",
    "sample_health_signal_binding_result_v1.json",
    "sample_whitebox_visibility_binding_result_v1.json",
    "sample_issue_trace_violation_binding_result_v1.json",
    "sample_decision_request_candidate_v1.json",
    "flow_integrity_dryrun_review_v1.json",
    "stale_missing_conflicting_evidence_dryrun_review_v1.json",
    "decision_center_handoff_boundary_review_v1.json",
    "candidate_evidence_flow_boundary_audit_v1.json",
    "candidate_evidence_flow_blocked_path_result_v1.json",
    "candidate_evidence_flow_closure_decision_v1.json",
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
            "midplatform_candidate_evidence_flow_integration_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_candidate_evidence_flow_integration_planning"
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
    model = _load(root / "candidate_evidence_flow_model_candidate_v1.json")
    intake = _load(root / "sample_candidate_intake_result_v1.json")
    domain = _load(root / "sample_domain_config_binding_result_v1.json")
    evidence = _load(root / "sample_evidence_pack_binding_result_v1.json")
    validation = _load(root / "sample_validation_result_binding_result_v1.json")
    health = _load(root / "sample_health_signal_binding_result_v1.json")
    whitebox = _load(root / "sample_whitebox_visibility_binding_result_v1.json")
    trace = _load(root / "sample_issue_trace_violation_binding_result_v1.json")
    decision_req = _load(root / "sample_decision_request_candidate_v1.json")
    integrity = _load(root / "flow_integrity_dryrun_review_v1.json")
    stale = _load(root / "stale_missing_conflicting_evidence_dryrun_review_v1.json")
    handoff = _load(root / "decision_center_handoff_boundary_review_v1.json")
    boundary = _load(root / "candidate_evidence_flow_boundary_audit_v1.json")
    blocked = _load(root / "candidate_evidence_flow_blocked_path_result_v1.json")
    closure = _load(root / "candidate_evidence_flow_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("candidate_evidence_flow_integration_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.module_id", model.get("module_id") == "midplatform_candidate_evidence_flow_integration_v1")
    ok("model.layer", model.get("system_layer") == "Assembly")
    ok("model.assembles", model.get("assembles_decision_request_candidate") is True)
    ok("model.no_decision", model.get("executes_decision") is False)
    ok("model.no_task", model.get("generates_task_response") is False)
    ok("model.no_user", model.get("generates_user_output") is False)
    ok("model.no_provider", model.get("provider_invocation_allowed") is False)
    ok("model.no_memory", model.get("memory_write_allowed") is False)
    ok("model.downstream_dc", "midplatform_decision_center_v1" in (model.get("downstream_modules") or []))

    ok("intake.count3", intake.get("candidate_count") == 3)
    ok("intake.valid", intake.get("all_fields_valid") is True)
    for ct in SAMPLE_CANDIDATE_TYPES:
        ok(f"intake.{ct[:15]}", ct in (intake.get("required_types_present") or []))
    candidates = intake.get("candidates") or []
    for c in candidates:
        for field in CANDIDATE_REQUIRED_FIELDS:
            ok(f"cand.{c.get('candidate_type','')[:10]}.{field[:10]}", field in c)
        ok(f"cand.{c.get('candidate_type','')[:10]}.not_fact", c.get("fact_status") == "not_fact")

    ok("domain.refs", len(domain.get("domain_config_refs") or []) > 0)
    ok("domain.constraints", domain.get("domain_config_domain_constraints_only") is True)
    ok("domain.no_runtime", domain.get("domain_config_runtime_activation") is False)

    ok("evidence.id", evidence.get("evidence_pack_id") is not None)
    ok("evidence.chain", evidence.get("source_chain") is not None)
    ok("evidence.provenance", evidence.get("provenance") is not None)
    ok("evidence.val_req", evidence.get("validation_required") is True)
    ok("evidence.wb_req", evidence.get("whitebox_visibility_required") is True)
    ok("evidence.not_fact", evidence.get("fact_status") == "not_fact")

    ok("validation.states6", len(validation.get("states") or []) == 6)
    for state in VALIDATION_RESULT_STATES:
        ok(f"val.{state['state'][:12]}", any(
            s.get("state") == state["state"] for s in (validation.get("states") or [])
        ))
    ok("validation.no_exec", validation.get("does_not_execute_validation") is True)

    ok("health.pressure", health.get("health_signal_is_pressure_context") is True)
    ok("health.reserved", health.get("health_metric_definition_status") == "reserved_not_defined")
    ok("health.no_auth", health.get("health_cannot_authorize_by_itself") is True)

    ok("wb.refs", len(whitebox.get("whitebox_visibility_refs") or []) > 0)
    ok("wb.layers5", len(whitebox.get("visibility_layers") or []) == 5)
    ok("wb.no_decide", whitebox.get("whitebox_does_not_decide") is True)

    ok("trace.no_mutate", trace.get("trace_report_do_not_mutate_candidate") is True)
    ok("trace.no_output", trace.get("trace_report_do_not_authorize_output") is True)

    ok("req.candidate_only", decision_req.get("candidate_only") is True)
    ok("req.handoff", decision_req.get("handoff_target") == "midplatform_decision_center_v1")
    for field in DECISION_REQUEST_FIELDS:
        ok(f"req.{field[:15]}", field in decision_req)

    ok("integrity.pass", integrity.get("dryrun_and_review_pass") is True)
    ok("integrity.rules8", integrity.get("rule_count") == 8)
    for rule in FLOW_INTEGRITY_RULES:
        ok(f"integrity.{rule[:18]}", rule in (integrity.get("rules") or []))

    ok("stale.pass", stale.get("dryrun_and_review_pass") is True)

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.not_decision", handoff.get("decision_request_not_decision_candidate") is True)
    ok("handoff.no_exec", handoff.get("handoff_does_not_execute_decision") is True)
    ok("handoff.no_task", handoff.get("task_response_not_generated") is True)

    ok("audit.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("audit.forbidden", boundary.get("forbidden_actions_absent") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count13", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp[:20]}", any(
            x.get("blocked_path") == bp and x.get("blocked") is True
            for x in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.handoff", closure.get("decision_request_handoff_ready") is True)

    ok("next.task_resp", next_route.get("ready_for_task_response_candidate_integration_planning") is True)
    ok("next.no_runtime", next_route.get("flow_runtime_enabled") is False)

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
