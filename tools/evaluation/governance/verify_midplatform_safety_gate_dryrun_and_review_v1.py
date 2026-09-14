#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Safety Gate DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_safety_gate_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_BOUNDARY_RULES,
    CONSTRAINT_BUNDLE_INTAKE_FIELDS,
    DOWNSTREAM_HANDOFF_MAPPINGS,
    ENFORCEMENT_LAYER_POSITIONING,
    ENFORCEMENT_RESULT_SAMPLE_FIELDS,
    EXECUTION_LAYER_BOUNDARY_RULES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NO_RAW_CONSTITUTION_RULES,
    PHASE_ID,
    REFUSAL_HOLD_DEGRADE_MAPPINGS,
    RULE_APPLICATION_RULES,
    SAFETY_ACTION_TAXONOMY,
    SCOPE,
    TRACEABILITY_REQUIREMENTS,
    UNCERTAINTY_RISK_RULES,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
    USER_OUTPUT_INTAKE_FIELDS,
)

MIN_CHECKS = 252

REQUIRED = (
    "safety_gate_dryrun_review_policy_v1.json",
    "safety_gate_planning_input_review_v1.json",
    "safety_gate_model_candidate_v1.json",
    "sample_constraint_bundle_intake_v1.json",
    "sample_user_output_candidate_intake_v1.json",
    "sample_safety_gate_result_candidate_v1.json",
    "enforcement_layer_role_review_v1.json",
    "bundle_only_consumption_review_v1.json",
    "no_raw_constitution_binding_review_v1.json",
    "safety_action_taxonomy_dryrun_review_v1.json",
    "safety_rule_application_dryrun_review_v1.json",
    "safety_uncertainty_risk_policy_review_v1.json",
    "safety_channel_boundary_review_v1.json",
    "refusal_hold_degrade_dryrun_review_v1.json",
    "enforcement_result_downstream_handoff_review_v1.json",
    "execution_layer_consumption_boundary_review_v1.json",
    "safety_gate_traceability_review_v1.json",
    "safety_gate_boundary_audit_v1.json",
    "safety_gate_blocked_path_result_v1.json",
    "safety_gate_closure_decision_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_dryrun_and_review",
    )
    p.add_argument(
        "--planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_safety_gate_planning",
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
    model = _load(root / "safety_gate_model_candidate_v1.json")
    sample_bundle = _load(root / "sample_constraint_bundle_intake_v1.json")
    sample_user = _load(root / "sample_user_output_candidate_intake_v1.json")
    sample_result = _load(root / "sample_safety_gate_result_candidate_v1.json")
    enforcement = _load(root / "enforcement_layer_role_review_v1.json")
    bundle_review = _load(root / "bundle_only_consumption_review_v1.json")
    no_raw = _load(root / "no_raw_constitution_binding_review_v1.json")
    actions = _load(root / "safety_action_taxonomy_dryrun_review_v1.json")
    rules = _load(root / "safety_rule_application_dryrun_review_v1.json")
    handoff = _load(root / "enforcement_result_downstream_handoff_review_v1.json")
    exec_boundary = _load(root / "execution_layer_consumption_boundary_review_v1.json")
    blocked = _load(root / "safety_gate_blocked_path_result_v1.json")
    closure = _load(root / "safety_gate_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok(
        "upstream.enforcement",
        _load(plan_root / "safety_gate_planning_policy_v1.json").get("safety_gate_is_enforcement_not_execution")
        is True,
    )

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("safety_gate_dryrun_and_review_only") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("model.id", model.get("module_id") == "midplatform_safety_gate_v1")
    ok("model.arch", model.get("architectural_layer") == "Enforcement")
    ok("model.layer", model.get("system_layer") == "Validation")
    ok("model.role", model.get("role") == "user_output_safety_enforcement_gate")
    ok("model.bundle", model.get("consumes_constraint_bundle") is True)
    ok("model.emits", model.get("emits_enforcement_result_candidate") is True)
    ok("model.no_raw", model.get("reads_raw_constitution_clauses") is False)
    ok("model.no_exec", model.get("invokes_execution_layer") is False)
    ok("model.no_facing", model.get("generates_user_facing_output") is False)
    ok("model.no_tts", model.get("tts_invocation_allowed") is False)

    for field in CONSTRAINT_BUNDLE_INTAKE_FIELDS:
        ok(f"bundle.{field[:15]}", field in sample_bundle)
    ok("bundle.candidate", sample_bundle.get("candidate_only") is True)

    for field in USER_OUTPUT_INTAKE_FIELDS:
        ok(f"user.{field[:15]}", field in sample_user)
    ok("user.no_facing", sample_user.get("user_facing_output_allowed") is False)

    for field in ENFORCEMENT_RESULT_SAMPLE_FIELDS:
        ok(f"result.{field[:15]}", field in sample_result)
    ok("result.layer", sample_result.get("enforcement_layer") == "SafetyGate")
    ok("result.no_facing", sample_result.get("user_facing_output_allowed") is False)
    ok(
        "result.bundle_ref",
        sample_result.get("source_constraint_bundle_ref") == sample_bundle.get("bundle_id"),
    )

    ok("enforcement.pass", enforcement.get("dryrun_and_review_pass") is True)
    for pos in ENFORCEMENT_LAYER_POSITIONING[:3]:
        ok(f"enforce.{pos[:18]}", pos in (enforcement.get("enforcement_layer_positioning") or []))

    ok("bundle_review.pass", bundle_review.get("dryrun_and_review_pass") is True)
    ok("bundle_review.only", bundle_review.get("consumes_constraint_bundle_only") is True)

    ok("no_raw.pass", no_raw.get("dryrun_and_review_pass") is True)
    for rule in NO_RAW_CONSTITUTION_RULES:
        ok(f"noraw.{rule[:18]}", rule in (no_raw.get("rules") or []))

    ok("actions.pass", actions.get("dryrun_and_review_pass") is True)
    ok("actions.count12", actions.get("action_count") == 12)
    ok("actions.all12", actions.get("all_twelve_actions_covered") is True)
    for action in SAFETY_ACTION_TAXONOMY:
        ok(f"action.{action[:18]}", any(a.get("safety_action") == action for a in (actions.get("actions") or [])))

    ok("rules.pass", rules.get("dryrun_and_review_pass") is True)
    for rule in RULE_APPLICATION_RULES:
        ok(f"ruleapp.{rule[:18]}", rule in (rules.get("rules") or []))

    ok("risk.pass", _load(root / "safety_uncertainty_risk_policy_review_v1.json").get("dryrun_and_review_pass") is True)
    for rule in UNCERTAINTY_RISK_RULES:
        ok(f"risk.{rule[:18]}", rule in (_load(root / "safety_uncertainty_risk_policy_review_v1.json").get("rules") or []))

    ok("channel.pass", _load(root / "safety_channel_boundary_review_v1.json").get("dryrun_and_review_pass") is True)
    for rule in CHANNEL_BOUNDARY_RULES:
        ok(f"channel.{rule[:18]}", rule in (_load(root / "safety_channel_boundary_review_v1.json").get("rules") or []))

    ok("refusal.pass", _load(root / "refusal_hold_degrade_dryrun_review_v1.json").get("dryrun_and_review_pass") is True)
    for m in REFUSAL_HOLD_DEGRADE_MAPPINGS:
        ok(
            f"refusal.{m['safety_action'][:16]}",
            any(
                x.get("safety_action") == m["safety_action"]
                for x in (_load(root / "refusal_hold_degrade_dryrun_review_v1.json").get("mappings") or [])
            ),
        )

    ok("handoff.pass", handoff.get("dryrun_and_review_pass") is True)
    ok("handoff.no_runtime", handoff.get("no_downstream_runtime_invoked_now") is True)
    for m in DOWNSTREAM_HANDOFF_MAPPINGS:
        ok(
            f"handoff.{m['safety_action'][:16]}",
            any(
                x.get("safety_action") == m["safety_action"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("exec.pass", exec_boundary.get("dryrun_and_review_pass") is True)
    ok("exec.not_const", exec_boundary.get("execution_layer_consumes_enforcement_result_not_constitution") is True)
    for rule in EXECUTION_LAYER_BOUNDARY_RULES:
        ok(f"exec.{rule[:18]}", rule in (exec_boundary.get("rules") or []))

    ok("trace.pass", _load(root / "safety_gate_traceability_review_v1.json").get("dryrun_and_review_pass") is True)
    for req in TRACEABILITY_REQUIREMENTS:
        ok(f"trace.{req[:18]}", req in (_load(root / "safety_gate_traceability_review_v1.json").get("requirements") or []))

    ok("audit.pass", _load(root / "safety_gate_boundary_audit_v1.json").get("dryrun_and_review_pass") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count18", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:22]}",
            any(
                x.get("blocked_path") == bp and x.get("blocked") is True
                for x in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.enforcement", closure.get("enforcement_layer_validated") is True)

    ok("next.ready", next_route.get("ready_for_speech_display_gate_roadmap_decision") is True)
    ok("next.no_voice_skip", next_route.get("do_not_skip_to_voice_output_plane") is True)
    ok("next.phase", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("policy.enforcement", _load(root / "safety_gate_dryrun_review_policy_v1.json").get("enforcement_not_execution") is True)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

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
