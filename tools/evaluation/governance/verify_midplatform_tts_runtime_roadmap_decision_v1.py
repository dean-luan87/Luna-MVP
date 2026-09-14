#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform TTS Runtime Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_voice_output_plane_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as VOICE_DR_FINAL,
    NEXT_PHASE_GO as VOICE_DR_NEXT,
)
from capabilities.governance.midplatform_tts_runtime_roadmap_decision_v1 import (
    BLOCKED_ROUTES,
    BOUNDARY_FALSE,
    DEFERRED_ROUTES,
    EXECUTION_RUNTIME_BOUNDARY_RULES,
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

MIN_CHECKS = 102

REQUIRED = (
    "tts_runtime_roadmap_policy_v1.json",
    "voice_output_plane_dryrun_input_review_v1.json",
    "tts_runtime_layer_position_review_v1.json",
    "route_a_tts_runtime_planning_assessment_v1.json",
    "route_b_hold_at_speech_request_candidate_assessment_v1.json",
    "route_c_return_to_display_gate_assessment_v1.json",
    "route_d_direct_tts_execution_assessment_v1.json",
    "route_e_end_to_end_simulation_before_tts_assessment_v1.json",
    "tts_runtime_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
    "execution_runtime_boundary_review_v1.json",
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
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_roadmap_decision",
    )
    p.add_argument(
        "--voice-output-plane-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_voice_output_plane_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    voice_dr_root = Path(args.voice_output_plane_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    voice_dr_vr = _load(voice_dr_root / "verifier_report.json")
    voice_dr_sm = _load(voice_dr_root / "summary.json")
    closure = _load(voice_dr_root / "voice_output_plane_closure_decision_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "tts_runtime_roadmap_policy_v1.json")
    input_review = _load(root / "voice_output_plane_dryrun_input_review_v1.json")
    layer = _load(root / "tts_runtime_layer_position_review_v1.json")
    route_a = _load(root / "route_a_tts_runtime_planning_assessment_v1.json")
    route_b = _load(root / "route_b_hold_at_speech_request_candidate_assessment_v1.json")
    route_c = _load(root / "route_c_return_to_display_gate_assessment_v1.json")
    route_d = _load(root / "route_d_direct_tts_execution_assessment_v1.json")
    route_e = _load(root / "route_e_end_to_end_simulation_before_tts_assessment_v1.json")
    matrix = _load(root / "tts_runtime_route_selection_matrix_v1.json")
    preconditions = _load(root / "selected_route_preconditions_v1.json")
    deferred = _load(root / "deferred_routes_register_v1.json")
    boundary = _load(root / "execution_runtime_boundary_review_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")

    ok("upstream.voice_dr_go", voice_dr_vr.get("verifier") == "GO")
    ok("upstream.voice_dr_final", voice_dr_sm.get("final_decision") == VOICE_DR_FINAL)
    ok("upstream.voice_dr_next", voice_dr_sm.get("recommended_next_phase") == VOICE_DR_NEXT)
    ok("upstream.execution", closure.get("execution_layer_validated") is True)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.display_defer", summary.get("display_gate_deferred_not_skipped") is True)
    ok("summary.e2e_defer", summary.get("end_to_end_simulation_deferred_not_cancelled") is True)

    ok("policy.decision_only", policy.get("roadmap_decision_not_planning") is True)
    ok("policy.tts_planning", policy.get("tts_runtime_planning_selected") is True)
    ok("policy.roadmap_only", policy.get("tts_runtime_roadmap_decision_only") is True)

    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.execution", input_review.get("execution_layer_validated") is True)
    ok("input.request_exists", input_review.get("speech_request_candidate_exists") is True)
    ok("input.not_real", input_review.get("speech_request_not_real") is True)
    ok("input.not_tts", input_review.get("speech_request_not_tts") is True)
    ok("input.no_bypass", input_review.get("speech_gate_not_bypassed") is True)
    ok("input.tts_blocked", input_review.get("direct_tts_not_opened") is True)

    ok("layer.pass", layer.get("review_pass") is True)
    for conf in LAYER_POSITION_CONFIRMATIONS:
        ok(f"layer.{conf[:18]}", conf in (layer.get("confirmations") or []))

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_a.label", route_a.get("route_label") == ROUTE_A)
    ok("route_b.deferred", route_b.get("status") == "deferred")
    ok("route_c.deferred", route_c.get("status") == "deferred")
    ok("route_d.blocked", route_d.get("status") == "blocked")
    ok("route_e.defer_after", route_e.get("status") == "deferred_after_tts_runtime_planning")

    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)
    for r in DEFERRED_ROUTES:
        if r == ROUTE_E:
            ok(
                f"matrix.defer.{r[:12]}",
                any(x.get("route") == r and x.get("status") == "deferred_after_tts_runtime_planning" for x in (matrix.get("routes") or [])),
            )
        else:
            ok(
                f"matrix.defer.{r[:12]}",
                any(x.get("route") == r and x.get("status") == "deferred" for x in (matrix.get("routes") or [])),
            )
    for r in BLOCKED_ROUTES:
        ok(
            f"matrix.block.{r[:12]}",
            any(x.get("route") == r and x.get("status") == "blocked" for x in (matrix.get("routes") or [])),
        )

    ok("precond.route", preconditions.get("selected_route") == SELECTED_ROUTE)
    ok("precond.tts_plan", "TTS Runtime planning only next" in " ".join(preconditions.get("preconditions") or []))

    ok("deferred.b", any(x.get("route") == ROUTE_B for x in (deferred.get("deferred_routes") or [])))
    ok("deferred.c", any(x.get("route") == ROUTE_C for x in (deferred.get("deferred_routes") or [])))
    ok(
        "deferred.e",
        any(
            x.get("route") == ROUTE_E and x.get("status") == "deferred_after_tts_runtime_planning"
            for x in (deferred.get("deferred_routes") or [])
        ),
    )
    ok("blocked.d", any(x.get("route") == ROUTE_D for x in (deferred.get("blocked_routes") or [])))

    ok("boundary.pass", boundary.get("review_pass") is True)
    ok("boundary.planning_first", boundary.get("tts_runtime_requires_planning_first") is True)
    for rule in EXECUTION_RUNTIME_BOUNDARY_RULES:
        ok(f"boundary.{rule[:18]}", rule in (boundary.get("rules") or []))

    ok("next.ready", next_phase.get("ready_for_tts_runtime_planning") is True)
    ok("next.no_tts_now", next_phase.get("do_not_open_tts_runtime_now") is True)
    ok("next.display_defer", next_phase.get("display_gate_deferred_not_skipped") is True)
    ok("next.e2e_defer", next_phase.get("end_to_end_simulation_deferred_not_cancelled") is True)
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
