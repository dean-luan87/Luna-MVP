#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Speech / Display Gate Roadmap Decision v1."""

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
    FINAL_DECISION_GO as SAFETY_DR_FINAL,
    NEXT_PHASE_GO as SAFETY_DR_NEXT,
)
from capabilities.governance.midplatform_speech_display_gate_roadmap_decision_v1 import (
    BLOCKED_ROUTES,
    BOUNDARY_FALSE,
    DEFERRED_ROUTES,
    ENFORCEMENT_EXECUTION_BOUNDARY_RULES,
    FINAL_DECISION_GO,
    LAYER_POSITION_CONFIRMATIONS,
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
)

MIN_CHECKS = 93

REQUIRED = (
    "speech_display_gate_roadmap_policy_v1.json",
    "safety_gate_dryrun_input_review_v1.json",
    "speech_display_gate_layer_position_review_v1.json",
    "route_a_speech_gate_first_assessment_v1.json",
    "route_b_display_gate_first_assessment_v1.json",
    "route_c_parallel_speech_display_gate_assessment_v1.json",
    "route_d_voice_output_plane_direct_assessment_v1.json",
    "route_e_display_output_direct_assessment_v1.json",
    "speech_display_gate_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "enforcement_execution_layer_boundary_review_v1.json",
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
            "midplatform_speech_display_gate_roadmap_decision"
        ),
    )
    p.add_argument(
        "--safety-gate-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_safety_gate_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    safety_dr_root = Path(args.safety_gate_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    safety_dr_vr = _load(safety_dr_root / "verifier_report.json")
    safety_dr_sm = _load(safety_dr_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "speech_display_gate_roadmap_policy_v1.json")
    input_review = _load(root / "safety_gate_dryrun_input_review_v1.json")
    layer = _load(root / "speech_display_gate_layer_position_review_v1.json")
    route_a = _load(root / "route_a_speech_gate_first_assessment_v1.json")
    route_b = _load(root / "route_b_display_gate_first_assessment_v1.json")
    route_c = _load(root / "route_c_parallel_speech_display_gate_assessment_v1.json")
    route_d = _load(root / "route_d_voice_output_plane_direct_assessment_v1.json")
    route_e = _load(root / "route_e_display_output_direct_assessment_v1.json")
    matrix = _load(root / "speech_display_gate_route_selection_matrix_v1.json")
    preconditions = _load(root / "selected_route_preconditions_v1.json")
    deferred = _load(root / "deferred_routes_register_v1.json")
    boundary = _load(root / "enforcement_execution_layer_boundary_review_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    ok("upstream.safety_dr_go", safety_dr_vr.get("verifier") == "GO")
    ok("upstream.safety_dr_final", safety_dr_sm.get("final_decision") == SAFETY_DR_FINAL)
    ok("upstream.safety_dr_next", safety_dr_sm.get("recommended_next_phase") == SAFETY_DR_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)

    ok("policy.decision_only", policy.get("roadmap_decision_not_planning") is True)
    ok("policy.speech_first", policy.get("speech_gate_first_selected") is True)
    ok("policy.roadmap_only", policy.get("speech_display_gate_roadmap_decision_only") is True)

    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.enforcement", input_review.get("enforcement_layer_validated") is True)

    ok("layer.pass", layer.get("review_pass") is True)
    for conf in LAYER_POSITION_CONFIRMATIONS:
        ok(f"layer.{conf[:18]}", conf in (layer.get("confirmations") or []))

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.deferred", route_b.get("status") == "deferred")
    ok("route_c.deferred", route_c.get("status") == "deferred")
    ok("route_d.blocked", route_d.get("status") == "blocked")
    ok("route_e.blocked", route_e.get("status") == "blocked")

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    for r in DEFERRED_ROUTES:
        ok(f"matrix.defer.{r[:12]}", any(x.get("route") == r and x.get("status") == "deferred" for x in (matrix.get("routes") or [])))
    for r in BLOCKED_ROUTES:
        ok(f"matrix.block.{r[:12]}", any(x.get("route") == r and x.get("status") == "blocked" for x in (matrix.get("routes") or [])))

    ok("precond.route", preconditions.get("selected_route") == SELECTED_ROUTE)
    ok("precond.speech_gate", "Speech Gate planning only next" in " ".join(preconditions.get("preconditions") or []))

    ok("deferred.b", any(x.get("route") == ROUTE_B for x in (deferred.get("deferred_routes") or [])))
    ok("deferred.c", any(x.get("route") == ROUTE_C for x in (deferred.get("deferred_routes") or [])))
    ok("blocked.d", any(x.get("route") == ROUTE_D for x in (deferred.get("blocked_routes") or [])))
    ok("blocked.e", any(x.get("route") == ROUTE_E for x in (deferred.get("blocked_routes") or [])))

    ok("boundary.pass", boundary.get("review_pass") is True)
    ok("boundary.eligibility", boundary.get("enforcement_result_grants_eligibility_not_execution") is True)
    for rule in ENFORCEMENT_EXECUTION_BOUNDARY_RULES:
        ok(f"boundary.{rule[:18]}", rule in (boundary.get("rules") or []))

    ok("next.ready", next_phase.get("ready_for_speech_gate_planning") is True)
    ok("next.no_voice_skip", next_phase.get("do_not_skip_to_voice_output_plane") is True)
    ok("next.display_defer", next_phase.get("display_gate_deferred_not_skipped") is True)
    ok("next.phase", next_phase.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("next.final", next_phase.get("final_decision") == FINAL_DECISION_GO)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("boundary_ok") is True
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
