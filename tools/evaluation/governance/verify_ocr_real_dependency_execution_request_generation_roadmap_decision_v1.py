#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Execution Request Generation Roadmap Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_real_dependency_execution_authorization_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as DRYRUN_FINAL,
    NEXT_PHASE_GO as DRYRUN_NEXT,
)
from capabilities.governance.ocr_real_dependency_execution_request_generation_roadmap_decision_v1 import (
    BLOCKED_ROUTE_E,
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_B,
    DEFERRED_ROUTE_C,
    DEFERRED_ROUTE_D,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SELECTED_ROUTE,
)

MIN_CHECKS = 75

REQUIRED = (
    "execution_request_generation_roadmap_policy_v1.json",
    "execution_authorization_dryrun_input_review_v1.json",
    "request_generation_readiness_review_v1.json",
    "route_a_formal_execution_request_generation_planning_assessment_v1.json",
    "route_b_validation_runtime_readiness_assessment_v1.json",
    "route_c_owner_operator_approval_precheck_assessment_v1.json",
    "route_d_provider_selection_evidence_precheck_assessment_v1.json",
    "route_e_real_dependency_execution_direct_assessment_v1.json",
    "execution_request_generation_route_selection_matrix_v1.json",
    "selected_route_preconditions_v1.json",
    "deferred_routes_register_v1.json",
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
            "ocr_real_dependency_execution_request_generation_roadmap_decision"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_authorization_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.ocr_real_dependency_execution_authorization_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    dryrun_sm = _load(dryrun_root / "summary.json")
    request_cand = _load(dryrun_root / "execution_authorization_request_candidate_v1.json")
    grant_cand = _load(dryrun_root / "execution_grant_candidate_v1.json")
    window_cand = _load(dryrun_root / "execution_window_candidate_v1.json")
    allowed_cand = _load(dryrun_root / "allowed_check_plan_candidate_v1.json")
    evidence_cand = _load(dryrun_root / "evidence_collection_candidate_v1.json")
    gate = _load(dryrun_root / "validation_gate_path_dryrun_review_v1.json")

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == DRYRUN_NEXT)
    ok("upstream.request_cand", bool(request_cand.get("request_candidate_id")))
    ok("upstream.grant_cand", bool(grant_cand.get("grant_candidate_id")))
    ok("upstream.window_cand", bool(window_cand.get("execution_window_candidate_id")))
    ok("upstream.allowed_cand", bool(allowed_cand.get("candidate_id")))
    ok("upstream.evidence_cand", bool(evidence_cand.get("candidate_id")))
    ok("upstream.gate_pass", gate.get("simulated_gate_path_pass") is True)
    ok("upstream.no_formal", request_cand.get("formal_request_generated_now") is False)
    ok("upstream.no_grant", grant_cand.get("grant_issued_now") is False)
    ok("upstream.no_window", window_cand.get("execution_window_opened_now") is False)

    summary = _load(root / "summary.json")
    matrix = _load(root / "execution_request_generation_route_selection_matrix_v1.json")
    route_a = _load(root / "route_a_formal_execution_request_generation_planning_assessment_v1.json")
    route_b = _load(root / "route_b_validation_runtime_readiness_assessment_v1.json")
    route_c = _load(root / "route_c_owner_operator_approval_precheck_assessment_v1.json")
    route_d = _load(root / "route_d_provider_selection_evidence_precheck_assessment_v1.json")
    route_e = _load(root / "route_e_real_dependency_execution_direct_assessment_v1.json")
    next_phase = _load(root / "next_phase_readiness_decision_v1.json")
    dryrun_in = _load(root / "execution_authorization_dryrun_input_review_v1.json")
    readiness = _load(root / "request_generation_readiness_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("execution_request_generation_roadmap_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.selected", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.defer_b", summary.get("deferred_route_b") == DEFERRED_ROUTE_B)
    ok("summary.defer_c", summary.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("summary.defer_d", summary.get("deferred_route_d") == DEFERRED_ROUTE_D)
    ok("summary.block_e", summary.get("blocked_route_e") == BLOCKED_ROUTE_E)
    ok("summary.provider_null", summary.get("selected_provider_for_execution") is None)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_b.deferred", route_b.get("status") == "deferred")
    ok("route_c.deferred", route_c.get("status") == "deferred_until_formal_request_candidate")
    ok("route_d.deferred", route_d.get("status") == "deferred_after_real_dependency_evidence")
    ok("route_e.blocked", route_e.get("status") == "blocked")
    ok("matrix.selected", matrix.get("selected_route") == SELECTED_ROUTE)

    ok("dryrun_in.pass", dryrun_in.get("review_pass") is True)
    ok("readiness.pass", readiness.get("readiness_pass") is True)

    ok("next.ready", next_phase.get("ready_for_formal_execution_request_generation_planning") is True)
    ok("next.no_formal", next_phase.get("do_not_generate_formal_request_now") is True)
    ok("next.no_send", next_phase.get("do_not_send_request_now") is True)
    ok("next.no_grant", next_phase.get("do_not_grant_now") is True)
    ok("next.no_window", next_phase.get("do_not_open_execution_window_now") is True)
    ok("next.no_real_dep", next_phase.get("ready_for_real_dependency_check_execution") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    boundary_ok = summary.get("boundary_ok") is True
    go = passed >= MIN_CHECKS and boundary_ok and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "boundary_ok": boundary_ok,
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
