#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Controlled Runtime Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.health_enforcement_supervisor_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HEALTH_SUPERVISOR_DR_FINAL,
    NEXT_PHASE_GO as HEALTH_SUPERVISOR_DR_NEXT,
)
from capabilities.governance.midplatform_controlled_runtime_planning_v1 import (
    ADMISSION_RULES,
    AUTHORIZATION_RULES,
    BOUNDARY_FALSE,
    BOUNDARY_MATRIX_FALSE,
    BOUNDARY_TRUE,
    CORE_CHAIN_BOUNDARY,
    DOMAIN_MATRIX,
    EVIDENCE_CAPTURE_FIELDS,
    EXCLUDED_RUNTIMES,
    EXECUTION_WINDOW_RULES,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    GATE_PRECONDITION_RULES,
    HEALTH_SUPERVISION_RULES,
    IN_SCOPE_RUNTIMES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    POST_EXECUTION_REVIEW_OUTCOMES,
    POST_EXECUTION_REVIEW_RULES,
    PROVIDER_READINESS_RULES,
    ROLLBACK_RULES,
    RUNTIME_CANDIDATE_FIELDS,
    RUNTIME_CANDIDATE_SPECS,
    SCOPE,
    SCOPE_DEFINITION_RULES,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_DR_FINAL,
)

MIN_CHECKS = 372

REQUIRED = (
    "controlled_runtime_planning_policy_v1.json",
    "upstream_system_readiness_review_v1.json",
    "controlled_runtime_scope_definition_v1.json",
    "controlled_runtime_candidate_registry_v1.json",
    "controlled_runtime_admission_policy_v1.json",
    "controlled_runtime_authorization_policy_v1.json",
    "controlled_runtime_execution_window_policy_v1.json",
    "controlled_runtime_provider_readiness_policy_v1.json",
    "controlled_runtime_gate_precondition_policy_v1.json",
    "controlled_runtime_health_supervision_policy_v1.json",
    "controlled_runtime_evidence_capture_policy_v1.json",
    "controlled_runtime_rollback_policy_v1.json",
    "controlled_runtime_post_execution_review_policy_v1.json",
    "controlled_runtime_failure_route_policy_v1.json",
    "controlled_runtime_domain_matrix_v1.json",
    "controlled_runtime_boundary_matrix_v1.json",
    "controlled_runtime_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "controlled_runtime_planning_decision_v1.json",
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
            "midplatform_controlled_runtime_planning"
        ),
    )
    p.add_argument(
        "--health-supervisor-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "health_enforcement_supervisor_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--provider-abstraction-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--fmis-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_frontend_model_influence_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--e2e-simulation-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    health_dr_root = Path(args.health_supervisor_dryrun_root)
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    fmis_dr_root = Path(args.fmis_dryrun_root)
    e2e_dr_root = Path(args.e2e_simulation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    health_dr_vr = _load(health_dr_root / "verifier_report.json")
    health_dr_sm = _load(health_dr_root / "summary.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    fmis_dr_sm = _load(fmis_dr_root / "summary.json")
    e2e_dr_sm = _load(e2e_dr_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "controlled_runtime_planning_policy_v1.json")
    upstream = _load(root / "upstream_system_readiness_review_v1.json")
    scope_def = _load(root / "controlled_runtime_scope_definition_v1.json")
    registry = _load(root / "controlled_runtime_candidate_registry_v1.json")
    admission = _load(root / "controlled_runtime_admission_policy_v1.json")
    authorization = _load(root / "controlled_runtime_authorization_policy_v1.json")
    window = _load(root / "controlled_runtime_execution_window_policy_v1.json")
    readiness = _load(root / "controlled_runtime_provider_readiness_policy_v1.json")
    gate_pre = _load(root / "controlled_runtime_gate_precondition_policy_v1.json")
    health_pol = _load(root / "controlled_runtime_health_supervision_policy_v1.json")
    evidence = _load(root / "controlled_runtime_evidence_capture_policy_v1.json")
    rollback = _load(root / "controlled_runtime_rollback_policy_v1.json")
    post_review = _load(root / "controlled_runtime_post_execution_review_policy_v1.json")
    failure = _load(root / "controlled_runtime_failure_route_policy_v1.json")
    domain_matrix = _load(root / "controlled_runtime_domain_matrix_v1.json")
    boundary = _load(root / "controlled_runtime_boundary_matrix_v1.json")
    dryrun = _load(root / "controlled_runtime_dryrun_plan_v1.json")
    decision = _load(root / "controlled_runtime_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.health_dr_go", health_dr_vr.get("verifier") == "GO")
    ok("upstream.health_dr_final", health_dr_sm.get("final_decision") == HEALTH_SUPERVISOR_DR_FINAL)
    ok("upstream.health_dr_next", health_dr_sm.get("recommended_next_phase") == HEALTH_SUPERVISOR_DR_NEXT)
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_ABS_DR_FINAL)
    ok("upstream.fmis_final", fmis_dr_sm.get("final_decision") == FMIS_DR_FINAL)
    ok("upstream.e2e_final", e2e_dr_sm.get("final_decision") == E2E_DR_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("controlled_runtime_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.boundary", summary.get("core_chain_boundary") == CORE_CHAIN_BOUNDARY)
    ok("summary.simulated_go", summary.get("system_level_simulated_go") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_execution", policy.get("controlled_runtime_not_execution") is True)
    ok("policy.not_runtime", policy.get("planning_not_runtime_enable") is True)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.simulated_go", upstream.get("system_level_simulated_go") is True)
    ok("upstream.no_leakage", upstream.get("no_runtime_leakage_in_upstream") is True)

    ok("scope.rules5", scope_def.get("rule_count") == 5)
    for rule in SCOPE_DEFINITION_RULES:
        ok(f"scope.{rule[:18]}", rule in (scope_def.get("rules") or []))
    for runtime in IN_SCOPE_RUNTIMES:
        ok(f"scope.in.{runtime[:18]}", runtime in (scope_def.get("in_scope_runtimes") or []))
    for excluded in EXCLUDED_RUNTIMES:
        ok(f"scope.out.{excluded[:18]}", excluded in (scope_def.get("excluded_runtimes") or []))

    ok("registry.count8", registry.get("candidate_count") == 8)
    ok("registry.all_off", registry.get("all_runtime_enabled_now_false") is True)
    candidates = registry.get("candidates") or []
    for spec in RUNTIME_CANDIDATE_SPECS:
        ok(
            f"registry.{spec['runtime_candidate_id'][:18]}",
            any(c.get("runtime_candidate_id") == spec["runtime_candidate_id"] for c in candidates),
        )
    for c in candidates:
        for field in RUNTIME_CANDIDATE_FIELDS:
            ok(f"candidate.{c.get('runtime_candidate_id','')[:12]}.{field[:12]}", field in c)
        ok(f"candidate.{c.get('runtime_candidate_id','')[:12]}.off", c.get("runtime_enabled_now") is False)
        ok(f"candidate.{c.get('runtime_candidate_id','')[:12]}.nostart", c.get("execution_started_now") is False)

    ok("admission.count11", admission.get("rule_count") == 11)
    for rule in ADMISSION_RULES:
        ok(f"admission.{rule[:18]}", rule in (admission.get("rules") or []))

    ok("auth.count6", authorization.get("rule_count") == 6)
    ok("auth.not_granted", authorization.get("authorization_granted_now") is False)
    for rule in AUTHORIZATION_RULES:
        ok(f"auth.{rule[:18]}", rule in (authorization.get("rules") or []))

    ok("window.count6", window.get("rule_count") == 6)
    ok("window.not_open", window.get("runtime_execution_window_opened_now") is False)
    for rule in EXECUTION_WINDOW_RULES:
        ok(f"window.{rule[:18]}", rule in (window.get("rules") or []))

    ok("readiness.count7", readiness.get("rule_count") == 7)
    ok("readiness.std_required", readiness.get("provider_abstraction_standard_required") is True)
    for rule in PROVIDER_READINESS_RULES:
        ok(f"readiness.{rule[:18]}", rule in (readiness.get("rules") or []))

    ok("gate.count5", gate_pre.get("rule_count") == 5)
    for rule in GATE_PRECONDITION_RULES:
        ok(f"gate.{rule[:18]}", rule in (gate_pre.get("rules") or []))

    ok("health.count5", health_pol.get("rule_count") == 5)
    ok("health.supervisor_required", health_pol.get("health_enforcement_supervisor_required") is True)
    for rule in HEALTH_SUPERVISION_RULES:
        ok(f"health.{rule[:18]}", rule in (health_pol.get("rules") or []))

    ok("evidence.count14", evidence.get("field_count") == 14)
    ok("evidence.result_later", evidence.get("runtime_result_ref_later") is True)
    for field in EVIDENCE_CAPTURE_FIELDS:
        ok(f"evidence.{field[:18]}", field in (evidence.get("required_fields") or []))

    ok("rollback.count6", rollback.get("rule_count") == 6)
    for rule in ROLLBACK_RULES:
        ok(f"rollback.{rule[:18]}", rule in (rollback.get("rules") or []))

    ok("post.count4", post_review.get("rule_count") == 4)
    for outcome in POST_EXECUTION_REVIEW_OUTCOMES:
        ok(f"post.outcome.{outcome}", outcome in (post_review.get("allowed_outcomes") or []))
    for rule in POST_EXECUTION_REVIEW_RULES:
        ok(f"post.{rule[:18]}", rule in (post_review.get("rules") or []))

    ok("failure.count8", failure.get("route_count") == 8)
    for route in FAILURE_ROUTES:
        ok(
            f"failure.{route['trigger'][:18]}",
            any(
                r.get("trigger") == route["trigger"] and r.get("route") == route["route"]
                for r in (failure.get("routes") or [])
            ),
        )

    ok("domain.count8", domain_matrix.get("domain_count") == 8)
    for domain in DOMAIN_MATRIX:
        ok(
            f"domain.{domain['domain_id'][:18]}",
            any(d.get("domain_id") == domain["domain_id"] for d in (domain_matrix.get("domains") or [])),
        )
        entry = next(
            (d for d in (domain_matrix.get("domains") or []) if d.get("domain_id") == domain["domain_id"]),
            {},
        )
        ok(f"domain.{domain['domain_id'][:12]}.off", entry.get("runtime_enabled_now") is False)

    ok("boundary.matrix23", len(boundary.get("matrix") or {}) == 23)
    for field in BOUNDARY_MATRIX_FALSE:
        ok(f"matrix.{field[:18]}", (boundary.get("matrix") or {}).get(field) is False)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    ok("qianwen.candidate", summary.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    tts_candidate = next(
        (c for c in candidates if c.get("runtime_candidate_id") == "tts_provider_runtime_candidate_v1"),
        {},
    )
    ok(
        "tts.candidate_ref",
        CURRENT_PREFERRED_PROVIDER_CANDIDATE in (tts_candidate.get("provider_candidate_refs") or []),
    )

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    verifier = "GO" if passed == total and passed >= (MIN_CHECKS if MIN_CHECKS else total) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "planning_pass": summary.get("planning_pass"),
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
