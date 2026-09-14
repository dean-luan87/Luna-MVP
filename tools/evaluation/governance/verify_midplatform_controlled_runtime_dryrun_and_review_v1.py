#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Controlled Runtime DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    ADMISSION_REVIEW_CHECKS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DOMAIN_LABELS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_controlled_runtime_planning_v1 import (
    ADMISSION_RULES,
    AUTHORIZATION_RULES,
    DOMAIN_MATRIX,
    EVIDENCE_CAPTURE_FIELDS,
    EXECUTION_WINDOW_RULES,
    FAILURE_ROUTES,
    GATE_PRECONDITION_RULES,
    HEALTH_SUPERVISION_RULES,
    POST_EXECUTION_REVIEW_OUTCOMES,
    POST_EXECUTION_REVIEW_RULES,
    PROVIDER_READINESS_RULES,
    ROLLBACK_RULES,
    RUNTIME_CANDIDATE_FIELDS,
    RUNTIME_CANDIDATE_SPECS,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL,
)

MIN_CHECKS = 383

REQUIRED = (
    "controlled_runtime_dryrun_review_policy_v1.json",
    "controlled_runtime_planning_input_review_v1.json",
    "controlled_runtime_framework_candidate_v1.json",
    "runtime_candidate_registry_sample_v1.json",
    "controlled_runtime_admission_review_v1.json",
    "controlled_runtime_authorization_review_v1.json",
    "controlled_runtime_execution_window_review_v1.json",
    "controlled_runtime_provider_readiness_review_v1.json",
    "controlled_runtime_gate_precondition_review_v1.json",
    "controlled_runtime_health_supervision_review_v1.json",
    "controlled_runtime_evidence_capture_review_v1.json",
    "controlled_runtime_rollback_review_v1.json",
    "controlled_runtime_post_execution_review_v1.json",
    "controlled_runtime_failure_route_review_v1.json",
    "controlled_runtime_domain_matrix_review_v1.json",
    "controlled_runtime_boundary_audit_v1.json",
    "controlled_runtime_blocked_path_result_v1.json",
    "controlled_runtime_closure_decision_v1.json",
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
            "midplatform_controlled_runtime_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_controlled_runtime_planning"
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
    policy = _load(root / "controlled_runtime_dryrun_review_policy_v1.json")
    input_review = _load(root / "controlled_runtime_planning_input_review_v1.json")
    framework = _load(root / "controlled_runtime_framework_candidate_v1.json")
    registry = _load(root / "runtime_candidate_registry_sample_v1.json")
    admission = _load(root / "controlled_runtime_admission_review_v1.json")
    authorization = _load(root / "controlled_runtime_authorization_review_v1.json")
    window = _load(root / "controlled_runtime_execution_window_review_v1.json")
    readiness = _load(root / "controlled_runtime_provider_readiness_review_v1.json")
    gate_pre = _load(root / "controlled_runtime_gate_precondition_review_v1.json")
    health = _load(root / "controlled_runtime_health_supervision_review_v1.json")
    evidence = _load(root / "controlled_runtime_evidence_capture_review_v1.json")
    rollback = _load(root / "controlled_runtime_rollback_review_v1.json")
    post_review = _load(root / "controlled_runtime_post_execution_review_v1.json")
    failure = _load(root / "controlled_runtime_failure_route_review_v1.json")
    domain_review = _load(root / "controlled_runtime_domain_matrix_review_v1.json")
    boundary = _load(root / "controlled_runtime_boundary_audit_v1.json")
    blocked = _load(root / "controlled_runtime_blocked_path_result_v1.json")
    closure = _load(root / "controlled_runtime_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("controlled_runtime_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_execution", policy.get("framework_not_execution") is True)
    ok("policy.not_runtime", policy.get("dryrun_not_runtime_enable") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.simulated_go", input_review.get("system_level_simulated_go") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("framework.id", framework.get("framework_id") == "midplatform_controlled_runtime_framework_v1")
    ok("framework.type", framework.get("framework_type") == "later_runtime_admission_framework")
    ok("framework.layer", framework.get("system_layer") == "RuntimeGovernance")
    ok("framework.runtime_off", framework.get("runtime_enabled_now") is False)
    ok("framework.exec_off", framework.get("execution_started_now") is False)
    ok("framework.window_off", framework.get("execution_window_opened_now") is False)
    ok("framework.provider_rt", framework.get("applies_to_provider_runtime") is True)
    ok("framework.model_rt", framework.get("applies_to_model_runtime") is True)
    ok("framework.output_rt", framework.get("applies_to_output_runtime") is True)
    ok("framework.tool_rt", framework.get("applies_to_tool_runtime") is True)
    ok("framework.no_memory", framework.get("excludes_memory_write_runtime") is True)
    ok("framework.no_worldmodel", framework.get("excludes_worldmodel_fact_write_runtime") is True)
    ok("framework.no_autonomous", framework.get("excludes_autonomous_action_execution") is True)
    ok("framework.no_production", framework.get("excludes_production_runtime") is True)
    ok("framework.candidate", framework.get("candidate_only") is True)
    ok("framework.constitution", framework.get("requires_constitution_refs") is True)
    ok("framework.resolver", framework.get("requires_resolver_or_constraint_refs") is True)
    ok("framework.gates", framework.get("requires_enforcement_gate_refs") is True)
    ok("framework.validation", framework.get("requires_validation_refs") is True)
    ok("framework.health", framework.get("requires_health_supervision_refs") is True)
    ok("framework.readiness", framework.get("requires_provider_readiness_refs") is True)
    ok("framework.whitebox", framework.get("requires_whitebox_trace_refs") is True)
    ok("framework.evidence", framework.get("requires_evidence_capture") is True)
    ok("framework.rollback", framework.get("requires_rollback") is True)
    ok("framework.post_review", framework.get("requires_post_execution_review") is True)

    ok("registry.count8", registry.get("candidate_count") == 8)
    ok("registry.all_off", registry.get("all_runtime_enabled_now_false") is True)
    candidates = registry.get("candidates") or []
    for label in DOMAIN_LABELS:
        ok(f"registry.label.{label[:18]}", label in (registry.get("domain_labels") or []))
    for spec in RUNTIME_CANDIDATE_SPECS:
        ok(
            f"registry.{spec['runtime_candidate_id'][:18]}",
            any(c.get("runtime_candidate_id") == spec["runtime_candidate_id"] for c in candidates),
        )
    for c in candidates:
        for field in RUNTIME_CANDIDATE_FIELDS:
            ok(f"candidate.{c.get('runtime_candidate_id','')[:12]}.{field[:12]}", field in c)
        ok(f"candidate.{c.get('runtime_candidate_id','')[:12]}.off", c.get("runtime_enabled_now") is False)

    ok("admission.pass", admission.get("dryrun_and_review_pass") is True)
    for check in ADMISSION_REVIEW_CHECKS:
        ok(f"admission.{check[:18]}", check in (admission.get("admission_check_items") or []))

    ok("auth.pass", authorization.get("dryrun_and_review_pass") is True)
    for rule in AUTHORIZATION_RULES:
        ok(f"auth.{rule[:18]}", rule in (authorization.get("rules") or []))

    ok("window.pass", window.get("dryrun_and_review_pass") is True)
    for rule in EXECUTION_WINDOW_RULES:
        ok(f"window.{rule[:18]}", rule in (window.get("rules") or []))

    ok("readiness.pass", readiness.get("dryrun_and_review_pass") is True)
    for rule in PROVIDER_READINESS_RULES:
        ok(f"readiness.{rule[:18]}", rule in (readiness.get("rules") or []))

    ok("gate.pass", gate_pre.get("dryrun_and_review_pass") is True)
    for rule in GATE_PRECONDITION_RULES:
        ok(f"gate.{rule[:18]}", rule in (gate_pre.get("rules") or []))

    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    for rule in HEALTH_SUPERVISION_RULES:
        ok(f"health.{rule[:18]}", rule in (health.get("rules") or []))

    ok("evidence.pass", evidence.get("dryrun_and_review_pass") is True)
    for field in EVIDENCE_CAPTURE_FIELDS:
        ok(f"evidence.{field[:18]}", field in (evidence.get("required_fields") or []))

    ok("rollback.pass", rollback.get("dryrun_and_review_pass") is True)
    for rule in ROLLBACK_RULES:
        ok(f"rollback.{rule[:18]}", rule in (rollback.get("rules") or []))

    ok("post.pass", post_review.get("dryrun_and_review_pass") is True)
    for rule in POST_EXECUTION_REVIEW_RULES:
        ok(f"post.{rule[:18]}", rule in (post_review.get("rules") or []))
    for outcome in POST_EXECUTION_REVIEW_OUTCOMES:
        ok(f"post.outcome.{outcome}", outcome in (post_review.get("allowed_outcomes") or []))

    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    for route in FAILURE_ROUTES:
        ok(
            f"failure.{route['trigger'][:18]}",
            any(
                r.get("trigger") == route["trigger"] and r.get("route") == route["route"]
                for r in (failure.get("routes") or [])
            ),
        )

    ok("domain.pass", domain_review.get("dryrun_and_review_pass") is True)
    ok("domain.count8", domain_review.get("domain_count") == 8)
    for domain in DOMAIN_MATRIX:
        entry = next(
            (d for d in (domain_review.get("domains") or []) if d.get("domain_id") == domain["domain_id"]),
            {},
        )
        ok(f"domain.{domain['domain_id'][:18]}.gates", len(entry.get("required_gates") or []) > 0)
        ok(f"domain.{domain['domain_id'][:18]}.auth", entry.get("authorization_required") is True)
        ok(f"domain.{domain['domain_id'][:18]}.off", entry.get("runtime_enabled_now") is False)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count23", blocked.get("blocked_count") == 23)
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:18]}",
            any(x.get("blocked_path") == bp and x.get("blocked") is True for x in (blocked.get("blocked_paths") or [])),
        )

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("next.ready_cognitive", next_route.get("ready_for_cognitive_zoning_architecture_planning") is True)
    ok("next.runtime_off", next_route.get("controlled_runtime_enabled") is False)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    verifier = "GO" if passed == total and passed >= (MIN_CHECKS if MIN_CHECKS else total) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
