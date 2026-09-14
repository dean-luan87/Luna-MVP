#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Post-Output-Chain-Simulation Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL,
    NEXT_PHASE_GO as E2E_DR_NEXT,
)
from capabilities.governance.midplatform_post_output_chain_simulation_roadmap_decision_v1 import (
    BLOCKED_ROUTES,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DEFERRED_ROUTES,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    ROUTE_D,
    ROUTE_E,
    SCOPE,
    SELECTED_ROUTE,
    SYSTEM_LEVEL_GO_NONCLAIMS,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)

MIN_CHECKS = 104

REQUIRED = (
    "post_output_chain_simulation_roadmap_policy_v1.json",
    "system_level_simulation_input_review_v1.json",
    "route_a_provider_abstraction_alignment_assessment_v1.json",
    "route_b_display_gate_planning_assessment_v1.json",
    "route_c_controlled_runtime_planning_assessment_v1.json",
    "route_d_direct_real_tts_audio_assessment_v1.json",
    "route_e_health_enforcement_supervisor_assessment_v1.json",
    "post_simulation_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "blocked_routes_register_v1.json",
    "system_level_go_nonclaims_review_v1.json",
    "next_phase_readiness_decision_v1.json",
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
            "midplatform_post_output_chain_simulation_roadmap_decision"
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
    e2e_root = Path(args.e2e_simulation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    e2e_vr = _load(e2e_root / "verifier_report.json")
    e2e_sm = _load(e2e_root / "summary.json")
    exp_actual = _load(e2e_root / "expected_vs_actual_decision_matrix_v1.json")
    boundary_v = _load(e2e_root / "boundary_violation_matrix_v1.json")
    trace = _load(e2e_root / "traceability_matrix_v1.json")
    closure_review = _load(e2e_root / "system_level_chain_closure_review_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "post_output_chain_simulation_roadmap_policy_v1.json")
    input_review = _load(root / "system_level_simulation_input_review_v1.json")
    route_a = _load(root / "route_a_provider_abstraction_alignment_assessment_v1.json")
    route_b = _load(root / "route_b_display_gate_planning_assessment_v1.json")
    route_c = _load(root / "route_c_controlled_runtime_planning_assessment_v1.json")
    route_d = _load(root / "route_d_direct_real_tts_audio_assessment_v1.json")
    route_e = _load(root / "route_e_health_enforcement_supervisor_assessment_v1.json")
    matrix = _load(root / "post_simulation_route_selection_matrix_v1.json")
    preconditions = _load(root / "selected_route_preconditions_v1.json")
    deferred = _load(root / "deferred_routes_register_v1.json")
    blocked = _load(root / "blocked_routes_register_v1.json")
    nonclaims = _load(root / "system_level_go_nonclaims_review_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    ok("upstream.e2e_go", e2e_vr.get("verifier") == "GO")
    ok("upstream.e2e_final", e2e_sm.get("final_decision") == E2E_DR_FINAL)
    ok("upstream.e2e_next", e2e_sm.get("recommended_next_phase") == E2E_DR_NEXT)
    ok("upstream.cases8", e2e_sm.get("cases_passed") == 8)
    ok("upstream.exp_actual", exp_actual.get("all_match") is True)
    ok("upstream.boundary", boundary_v.get("all_boundaries_clear") is True)
    ok("upstream.trace", trace.get("all_preserved") is True)
    ok("upstream.no_leak", closure_review.get("no_runtime_leakage") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)
    ok("summary.system_go", summary.get("system_level_simulated_go") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.roadmap_only", policy.get("roadmap_decision_not_runtime") is True)
    ok("policy.route_a", policy.get("provider_abstraction_alignment_selected") is True)
    ok("policy.system_go", policy.get("system_level_simulated_go_acknowledged") is True)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.cases8", input_review.get("cases_passed") == 8)
    ok("input.exp_actual", input_review.get("expected_vs_actual_pass") is True)
    ok("input.boundary", input_review.get("boundary_violation_pass") is True)
    ok("input.trace", input_review.get("traceability_pass") is True)
    ok("input.no_leak", input_review.get("no_runtime_leakage") is True)
    ok("input.tts_abstract", input_review.get("tts_runtime_abstraction") is True)
    ok("input.qianwen", input_review.get("qianwen_registered_not_invoked") is True)
    ok("input.display_defer", input_review.get("display_gate_deferred_not_skipped") is True)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.deferred", route_b.get("status") == "deferred_next")
    ok("route_b.label", route_b.get("route_label") == ROUTE_B)
    ok("route_c.deferred", route_c.get("status") == "deferred_after_alignment_and_display_gate")
    ok("route_c.label", route_c.get("route_label") == ROUTE_C)
    ok("route_d.blocked", route_d.get("status") == "blocked")
    ok("route_d.label", route_d.get("route_label") == ROUTE_D)
    ok("route_e.deferred", route_e.get("status") == "deferred_but_registered")
    ok("route_e.label", route_e.get("route_label") == ROUTE_E)

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    ok("matrix.routes5", len(matrix.get("routes") or []) == 5)
    for route in (ROUTE_A, ROUTE_B, ROUTE_C, ROUTE_D, ROUTE_E):
        ok(f"matrix.{route[:12]}", any(x.get("route") == route for x in (matrix.get("routes") or [])))

    ok("pre.selected", preconditions.get("selected_route") == SELECTED_ROUTE)
    ok("pre.no_runtime", "real TTS / audio runtime" in (preconditions.get("forbidden_now") or []))

    ok("deferred.count3", len(deferred.get("deferred_routes") or []) == 3)
    for route in DEFERRED_ROUTES:
        ok(
            f"deferred.{route[:12]}",
            any(x.get("route") == route for x in (deferred.get("deferred_routes") or [])),
        )

    ok("blocked.count1", len(blocked.get("blocked_routes") or []) == 1)
    for route in BLOCKED_ROUTES:
        ok(
            f"blocked.{route[:12]}",
            any(x.get("route") == route and x.get("status") == "blocked" for x in (blocked.get("blocked_routes") or [])),
        )

    ok("nonclaims.pass", nonclaims.get("review_pass") is True)
    for claim in SYSTEM_LEVEL_GO_NONCLAIMS:
        ok(f"sysclaim.{claim[:18]}", claim in (nonclaims.get("non_claims") or []))

    ok("next.ready", next_phase.get("ready_for_provider_abstraction_standard_alignment_planning") is True)
    ok("next.no_runtime", next_phase.get("do_not_open_real_runtime_now") is True)
    ok("next.display_defer", next_phase.get("display_gate_deferred_not_skipped") is True)
    ok("next.tts_blocked", next_phase.get("direct_real_tts_blocked") is True)
    ok("next.final", next_phase.get("final_decision") == FINAL_DECISION_GO)
    ok("next.phase", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    ok("qianwen_candidate", summary.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("no_qianwen_invoke", summary.get("qianwen_tts_invoked_now") is False)

    pass_all = summary.get("boundary_ok") is True
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "boundary_ok": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "selected_route": summary.get("selected_route"),
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
