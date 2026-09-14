#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform User Output Constitution DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_user_output_constitution_dryrun_and_review_v1 import (
    ADMISSION_RULES,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CHANNEL_RULES,
    CONFLICT_PRIORITY_DRYRUN,
    CONFLICT_RULES,
    CONSTRAINT_BUNDLE_FIELDS,
    EXPLAINABILITY_REQUIREMENTS,
    FACT_UNCERTAINTY_RULES,
    FINAL_DECISION_GO,
    JURISDICTION_GOVERNED,
    JURISDICTION_NOT_GOVERNED,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PRIVACY_RULES,
    REFUSAL_HOLD_DEGRADE_RULES,
    SAFETY_RULES,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)

MIN_CHECKS = 226

REQUIRED = (
    "user_output_constitution_dryrun_review_policy_v1.json",
    "user_output_constitution_planning_input_review_v1.json",
    "user_output_constitution_candidate_v1.json",
    "user_output_scope_jurisdiction_review_v1.json",
    "user_output_admission_rule_dryrun_review_v1.json",
    "user_output_safety_rule_dryrun_review_v1.json",
    "user_output_fact_uncertainty_rule_dryrun_review_v1.json",
    "user_output_privacy_rule_dryrun_review_v1.json",
    "user_output_channel_rule_dryrun_review_v1.json",
    "user_output_tone_personalization_boundary_review_v1.json",
    "user_output_refusal_hold_degrade_rule_review_v1.json",
    "user_output_explainability_traceability_review_v1.json",
    "user_output_conflict_policy_review_v1.json",
    "constitution_resolver_binding_review_v1.json",
    "constitution_constraint_bundle_candidate_v1.json",
    "constitution_change_propagation_review_v1.json",
    "downstream_impact_boundary_review_v1.json",
    "user_output_speech_display_boundary_review_v1.json",
    "user_output_memory_worldmodel_taskstate_boundary_review_v1.json",
    "user_output_constitution_boundary_audit_v1.json",
    "user_output_constitution_blocked_path_result_v1.json",
    "user_output_constitution_closure_decision_v1.json",
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
            "midplatform_user_output_constitution_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_user_output_constitution_planning"
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
    constitution = _load(root / "user_output_constitution_candidate_v1.json")
    bundle = _load(root / "constitution_constraint_bundle_candidate_v1.json")
    resolver = _load(root / "constitution_resolver_binding_review_v1.json")
    propagation = _load(root / "constitution_change_propagation_review_v1.json")
    impact = _load(root / "downstream_impact_boundary_review_v1.json")
    scope = _load(root / "user_output_scope_jurisdiction_review_v1.json")
    admission = _load(root / "user_output_admission_rule_dryrun_review_v1.json")
    safety = _load(root / "user_output_safety_rule_dryrun_review_v1.json")
    fact = _load(root / "user_output_fact_uncertainty_rule_dryrun_review_v1.json")
    privacy = _load(root / "user_output_privacy_rule_dryrun_review_v1.json")
    channel = _load(root / "user_output_channel_rule_dryrun_review_v1.json")
    conflict = _load(root / "user_output_conflict_policy_review_v1.json")
    boundary = _load(root / "user_output_constitution_boundary_audit_v1.json")
    blocked = _load(root / "user_output_constitution_blocked_path_result_v1.json")
    closure = _load(root / "user_output_constitution_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("user_output_constitution_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("constitution.id", constitution.get("constitution_id") == "midplatform_user_output_constitution_v1")
    ok("constitution.type", constitution.get("constitution_type") == "domain_constitution")
    ok("constitution.domain", constitution.get("constitution_domain") == "user_output")
    ok("constitution.parent", constitution.get("parent_constitution") == "Luna General Constitution")
    ok("constitution.hive", constitution.get("managed_by") == "Hive")
    ok("constitution.local_candidate", constitution.get("local_module_can_only_generate_candidate") is True)
    ok("constitution.runtime_off", constitution.get("runtime_enabled_now") is False)
    ok("constitution.candidate", constitution.get("candidate_only") is True)
    ok("constitution.governs_user", constitution.get("governs_user_output_candidate") is True)

    for field in CONSTRAINT_BUNDLE_FIELDS:
        ok(f"bundle.{field[:18]}", field in bundle)
    ok("bundle.candidate", bundle.get("candidate_only") is True)
    ok("bundle.no_direct_binding", "direct_raw_constitution_clause_binding" in (bundle.get("forbidden_actions") or []))

    ok("resolver.pass", resolver.get("dryrun_and_review_pass") is True)
    ok("resolver.consume_bundle", resolver.get("downstream_gates_consume_constraint_bundle") is True)
    ok("resolver.no_raw", resolver.get("downstream_gates_do_not_bind_raw_clauses") is True)
    ok("resolver.general_prio", resolver.get("general_constitution_higher_priority") is True)

    ok("propagation.pass", propagation.get("dryrun_and_review_pass") is True)
    ok("propagation.hive", propagation.get("propagation_mechanism", {}).get("hive_approval_required_before_publication") is True)
    ok("propagation.no_self", propagation.get("propagation_mechanism", {}).get("local_module_cannot_self_activate") is True)

    ok("impact.pass", impact.get("dryrun_and_review_pass") is True)
    ok("impact.bundle", impact.get("impact_compression_principle") == "direct_impact_stops_at_constraint_bundle_contract")

    ok("scope.pass", scope.get("dryrun_and_review_pass") is True)
    for obj in JURISDICTION_GOVERNED:
        ok(f"gov.{obj[:18]}", obj in (scope.get("governed_objects") or []))
    for obj in JURISDICTION_NOT_GOVERNED:
        ok(f"notgov.{obj[:18]}", obj in (scope.get("not_governed_objects") or []))

    ok("admission.pass", admission.get("dryrun_and_review_pass") is True)
    ok("admission.count10", admission.get("rule_count") == 10)
    for rule in ADMISSION_RULES:
        ok(f"adm.{rule[:18]}", rule in (admission.get("rules") or []))

    ok("safety.pass", safety.get("dryrun_and_review_pass") is True)
    for rule in SAFETY_RULES:
        ok(f"safety.{rule[:18]}", rule in (safety.get("rules") or []))

    ok("fact.pass", fact.get("dryrun_and_review_pass") is True)
    for rule in FACT_UNCERTAINTY_RULES:
        ok(f"fact.{rule[:18]}", rule in (fact.get("rules") or []))

    ok("privacy.pass", privacy.get("dryrun_and_review_pass") is True)
    for rule in PRIVACY_RULES:
        ok(f"privacy.{rule[:18]}", rule in (privacy.get("rules") or []))

    ok("channel.pass", channel.get("dryrun_and_review_pass") is True)
    for rule in CHANNEL_RULES:
        ok(f"channel.{rule[:18]}", rule in (channel.get("rules") or []))

    ok("conflict.pass", conflict.get("dryrun_and_review_pass") is True)
    for layer in CONFLICT_PRIORITY_DRYRUN:
        ok(f"prio.{layer[:18]}", layer in (conflict.get("priority_layers") or []))
    for rule in CONFLICT_RULES:
        ok(f"conflict.{rule[:18]}", rule in (conflict.get("conflict_rules") or []))

    ok("explain.pass", _load(root / "user_output_explainability_traceability_review_v1.json").get("dryrun_and_review_pass") is True)
    for req in EXPLAINABILITY_REQUIREMENTS:
        ok(f"explain.{req[:18]}", req in (_load(root / "user_output_explainability_traceability_review_v1.json").get("requirements") or []))

    ok("refusal.pass", _load(root / "user_output_refusal_hold_degrade_rule_review_v1.json").get("dryrun_and_review_pass") is True)
    for route in REFUSAL_HOLD_DEGRADE_RULES:
        ok(
            f"refusal.{route['trigger'][:14]}",
            any(
                r.get("trigger") == route["trigger"]
                for r in (_load(root / "user_output_refusal_hold_degrade_rule_review_v1.json").get("rules") or [])
            ),
        )

    ok("audit.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("audit.forbidden", boundary.get("forbidden_actions_absent") is True)

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
    ok("closure.chain4", len(closure.get("constitution_propagation_chain_defined") or []) == 4)

    ok("next.ready", next_route.get("ready_for_safety_gate_planning") is True)
    ok("next.no_runtime", next_route.get("user_output_constitution_runtime_enabled") is False)
    ok("next.no_facing", next_route.get("user_facing_output_still_forbidden") is True)
    ok("next.not_published", next_route.get("constitution_not_published") is True)
    ok("next.phase", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("policy.resolver_bundle", _load(root / "user_output_constitution_dryrun_review_policy_v1.json").get("constitution_to_resolver_to_bundle") is True)

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
    print(
        json.dumps(
            {"verifier": report["verifier"], "checks_passed": passed, "checks_total": total},
            ensure_ascii=False,
        )
    )
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
