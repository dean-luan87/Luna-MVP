#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Minimal Execution Authorization Decision v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    MINIMAL_SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_real_minimal_execution_authorization_decision_v1 import (
    BLOCKED_ROUTE_D,
    BOUNDARY_FALSE,
    DEFERRED_ROUTE_B,
    DEFERRED_ROUTE_C,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    ROUTE_A,
    ROUTE_B,
    ROUTE_C,
    ROUTE_D,
    SCOPE,
    SELECTED_ROUTE,
    UPSTREAM_DRYRUN_FINAL,
    UPSTREAM_DRYRUN_NEXT,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    EVIDENCE_OUTPUT_ITEMS,
    FAILURE_ROUTES,
    MINIMAL_FORBIDDEN_ACTIONS,
)

MIN_CHECKS = 85

REQUIRED = (
    "real_minimal_execution_authorization_decision_policy_v1.json",
    "minimal_execution_dryrun_input_review_v1.json",
    "real_execution_readiness_review_v1.json",
    "allowed_scope_authorization_review_v1.json",
    "forbidden_action_authorization_review_v1.json",
    "evidence_rollback_postreview_readiness_review_v1.json",
    "execution_risk_boundary_review_v1.json",
    "route_a_authorize_real_minimal_execution_assessment_v1.json",
    "route_b_hold_for_owner_confirmation_assessment_v1.json",
    "route_c_hold_for_environment_precheck_assessment_v1.json",
    "route_d_defer_and_return_to_provider_selection_assessment_v1.json",
    "real_minimal_execution_authorization_route_selection_matrix_v1.json",
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
            "ocr_real_dependency_real_minimal_execution_authorization_decision"
        ),
    )
    p.add_argument(
        "--dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    dryrun_root = Path(args.dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    dryrun_vr = _load(dryrun_root / "verifier_report.json")
    dryrun_sm = _load(dryrun_root / "summary.json")
    summary = _load(root / "summary.json")
    readiness = _load(root / "real_execution_readiness_review_v1.json")
    allowed = _load(root / "allowed_scope_authorization_review_v1.json")
    forbidden = _load(root / "forbidden_action_authorization_review_v1.json")
    evidence = _load(root / "evidence_rollback_postreview_readiness_review_v1.json")
    risk = _load(root / "execution_risk_boundary_review_v1.json")
    route_a = _load(root / "route_a_authorize_real_minimal_execution_assessment_v1.json")
    route_b = _load(root / "route_b_hold_for_owner_confirmation_assessment_v1.json")
    route_c = _load(root / "route_c_hold_for_environment_precheck_assessment_v1.json")
    route_d = _load(root / "route_d_defer_and_return_to_provider_selection_assessment_v1.json")
    matrix = _load(root / "real_minimal_execution_authorization_route_selection_matrix_v1.json")
    next_route = _load(root / "next_phase_readiness_decision_v1.json")

    ok("upstream.dryrun_go", dryrun_vr.get("verifier") == "GO")
    ok("upstream.dryrun_final", dryrun_sm.get("final_decision") == UPSTREAM_DRYRUN_FINAL)
    ok("upstream.dryrun_next", dryrun_sm.get("recommended_next_phase") == UPSTREAM_DRYRUN_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.decision_only", summary.get("real_minimal_execution_authorization_decision_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.route_a", summary.get("selected_route") == SELECTED_ROUTE)
    ok("summary.not_authorized", summary.get("real_minimal_execution_authorized_now") is False)
    ok("summary.not_started", summary.get("real_minimal_execution_started_now") is False)

    ok("readiness.pass", readiness.get("readiness_pass") is True)
    ok("allowed.pass", allowed.get("review_pass") is True)
    ok("allowed.count5", allowed.get("allowed_check_count") == 5)
    ok("forbidden.pass", forbidden.get("review_pass") is True)
    ok("forbidden.18", forbidden.get("forbidden_count") == 18)
    ok("evidence.pass", evidence.get("review_pass") is True)
    ok("evidence.13", evidence.get("evidence_count") == 13)
    ok("evidence.failure8", evidence.get("failure_route_count") == 8)
    ok("risk.pass", risk.get("review_pass") is True)

    ok("route_a.selected", route_a.get("status") == "selected")
    ok("route_b.deferred", route_b.get("status") == "deferred_until_execution_window_open")
    ok("route_c.deferred", route_c.get("status") == "deferred")
    ok("route_d.blocked", route_d.get("status") == "blocked_before_real_dependency_evidence")

    ok("matrix.selected", matrix.get("selected_route") == ROUTE_A)
    ok("matrix.deferred_b", matrix.get("deferred_route_b") == DEFERRED_ROUTE_B)
    ok("matrix.deferred_c", matrix.get("deferred_route_c") == DEFERRED_ROUTE_C)
    ok("matrix.blocked_d", matrix.get("blocked_route_d") == BLOCKED_ROUTE_D)

    ok("next.planning", next_route.get("ready_for_real_minimal_controlled_execution_planning") is True)
    ok("next.no_exec", next_route.get("ready_for_real_minimal_controlled_execution") is False)
    ok("next.not_authorized", next_route.get("real_minimal_execution_authorized_now") is False)

    for cid in MINIMAL_SCOPE_ALLOWED_CHECKS:
        ok(f"allowed.{cid[:12]}", cid in (allowed.get("allowed_checks") or []))

    for action in MINIMAL_FORBIDDEN_ACTIONS:
        ok(f"forbidden.{action[:12]}", action in (forbidden.get("forbidden_actions") or []))

    for item in EVIDENCE_OUTPUT_ITEMS:
        ok(f"evidence.{item[:15]}", item in (evidence.get("evidence_items") or []))

    ok("failure.count8", evidence.get("failure_route_count") == len(FAILURE_ROUTES))

    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("provider.null", summary.get("selected_provider_for_execution") is None)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

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
