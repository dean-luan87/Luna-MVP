#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    AUTHORIZATION_SCOPE_COVERED,
    AUTHORIZATION_SCOPE_NOT_COVERED,
    BOUNDARY_BLOCKED_PATHS,
    BOUNDARY_FALSE,
    CURRENT_LIFECYCLE_STATE,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.ocr_provider_authorization_return_roadmap_decision_v1 import (
    FINAL_DECISION_GO as RETURN_FINAL,
    NEXT_PHASE_GO as RETURN_NEXT,
    SELECTED_ROUTE,
)

MIN_CHECKS = 80

REQUIRED = (
    "ocr_provider_authorization_planning_policy_v1.json",
    "authorization_return_roadmap_input_review_v1.json",
    "ocr_provider_authorization_scope_v1.json",
    "authorization_request_contract_v1.json",
    "authorization_grant_contract_v1.json",
    "execution_window_contract_v1.json",
    "sandbox_and_environment_boundary_contract_v1.json",
    "rollback_and_cleanup_contract_v1.json",
    "evidence_package_requirement_v1.json",
    "owner_operator_approval_policy_v1.json",
    "provider_selection_binding_policy_v1.json",
    "real_dependency_check_authorization_binding_v1.json",
    "controlled_trial_authorization_binding_v1.json",
    "authorization_boundary_guard_matrix_v1.json",
    "authorization_lifecycle_state_machine_v1.json",
    "authorization_dryrun_plan_v1.json",
    "ocr_provider_authorization_planning_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning",
    )
    p.add_argument(
        "--ocr-provider-authorization-return-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_authorization_return_roadmap_decision"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    return_root = Path(args.ocr_provider_authorization_return_roadmap_decision_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "authorization_return_roadmap_input_review_v1.json")
    scope = _load(root / "ocr_provider_authorization_scope_v1.json")
    request = _load(root / "authorization_request_contract_v1.json")
    grant = _load(root / "authorization_grant_contract_v1.json")
    window = _load(root / "execution_window_contract_v1.json")
    sandbox = _load(root / "sandbox_and_environment_boundary_contract_v1.json")
    rollback = _load(root / "rollback_and_cleanup_contract_v1.json")
    evidence = _load(root / "evidence_package_requirement_v1.json")
    owner = _load(root / "owner_operator_approval_policy_v1.json")
    selection = _load(root / "provider_selection_binding_policy_v1.json")
    boundary = _load(root / "authorization_boundary_guard_matrix_v1.json")
    state_machine = _load(root / "authorization_lifecycle_state_machine_v1.json")
    dryrun_plan = _load(root / "authorization_dryrun_plan_v1.json")
    decision = _load(root / "ocr_provider_authorization_planning_decision_v1.json")

    return_vr = _load(return_root / "verifier_report.json")
    return_sm = _load(return_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_provider_authorization_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_LIFECYCLE_STATE)
    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)

    ok("upstream.return_go", return_vr.get("verifier") == "GO")
    ok("upstream.return_final", return_sm.get("final_decision") == RETURN_FINAL)
    ok("upstream.return_next", return_sm.get("recommended_next_phase") == RETURN_NEXT)
    ok("upstream.route_a", return_sm.get("selected_route") == SELECTED_ROUTE)
    ok("input.pass", input_review.get("review_pass") is True)

    ok("scope.planning_only", scope.get("planning_only") is True)
    ok("scope.no_exec", scope.get("does_not_execute_authorization") is True)
    ok("scope.covered5", len(scope.get("covered_future_authorizations") or []) == len(AUTHORIZATION_SCOPE_COVERED))

    ok("request.type", request.get("request_type") == "ocr_provider_authorization_request")
    ok("request.no_gen", request.get("current_request_generated_now") is False)
    ok("request.no_sent", request.get("current_request_sent_now") is False)
    ok("request.window", request.get("execution_window_required") is True)
    ok("request.sandbox", request.get("sandbox_required") is True)
    ok("request.evidence", request.get("evidence_package_required") is True)

    ok("grant.no_grant", grant.get("current_grant_issued_now") is False)
    ok("grant.no_auth", grant.get("provider_authorization_granted_now") is False)
    ok("grant.post_review", grant.get("post_execution_review_required") is True)

    ok("window.no_open", window.get("current_window_opened_now") is False)
    ok("window.no_prod", window.get("no_production_write") is True)
    ok("window.no_net", window.get("no_network_by_default") is True)

    ok("sandbox.req7", len(sandbox.get("requirements") or []) >= 7)
    ok("rollback.ready_later", rollback.get("rollback_plan_ready_later") is True)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)

    ok("evidence.count11", len(evidence.get("required_artifacts_on_future_execution") or []) == len(EVIDENCE_REQUIREMENTS))

    ok("owner.real_dep", owner.get("owner_operator_approval_required_for_real_dependency_check") is True)
    ok("owner.not_collected", owner.get("approval_collected_now") is False)

    ok("selection.null", selection.get("selected_provider_for_execution") is None)
    ok("selection.not_final", selection.get("provider_selection_finalized_now") is False)

    ok("boundary.count14", boundary.get("path_count") == len(BOUNDARY_BLOCKED_PATHS))
    ok("boundary.all", boundary.get("all_blocked") is True)

    ok("state.current", state_machine.get("current_state") == CURRENT_LIFECYCLE_STATE)
    ok("state.count10", len(state_machine.get("states") or []) == len(LIFECYCLE_STATES))

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.ready", decision.get("ready_for_dryrun") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    for item in AUTHORIZATION_SCOPE_NOT_COVERED:
        ok(f"not_covered.{item}", item in AUTHORIZATION_SCOPE_NOT_COVERED)

    ok("summary.no_grant", summary.get("provider_authorization_granted_now") is False)
    ok("summary.no_window", summary.get("execution_window_opened_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.no_ocr_req", summary.get("ocr_request_submitted_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = all(c["passed"] for c in checks) and len(checks) >= MIN_CHECKS
    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if passed else "NO_GO",
        "passed": passed,
        "check_count": len(checks),
        "final_decision": summary.get("final_decision"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": report["verifier"], "check_count": len(checks), "passed": passed}, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
