#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Real Dependency Check Authorization Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_authorization_next_route_decision_v1 import (
    FINAL_DECISION_GO as NEXT_ROUTE_FINAL,
    NEXT_PHASE_GO as NEXT_ROUTE_NEXT,
    SELECTED_ROUTE,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_planning_v1 import (
    ALLOWED_ACTIONS_LATER,
    AUTHORIZATION_SCOPE_IN,
    AUTHORIZATION_SCOPE_OUT,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    CURRENT_STATE,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO,
    FORBIDDEN_ACTIONS,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REQUEST_TYPE,
    ROLLBACK_POLICIES,
    SCOPE,
    TARGET_SCOPE,
)

MIN_CHECKS = 100

REQUIRED = (
    "real_dependency_check_authorization_planning_policy_v1.json",
    "ocr_authorization_next_route_input_review_v1.json",
    "real_dependency_check_authorization_scope_v1.json",
    "real_dependency_check_authorization_request_contract_v1.json",
    "real_dependency_check_grant_contract_v1.json",
    "real_dependency_check_execution_window_contract_v1.json",
    "allowed_dependency_check_action_matrix_v1.json",
    "forbidden_dependency_check_action_matrix_v1.json",
    "real_dependency_check_sandbox_boundary_plan_v1.json",
    "real_dependency_check_evidence_requirement_v1.json",
    "real_dependency_check_rollback_policy_v1.json",
    "owner_operator_approval_policy_v1.json",
    "provider_selection_non_finalize_binding_v1.json",
    "real_dependency_check_authorization_state_machine_v1.json",
    "real_dependency_check_authorization_blocked_path_matrix_v1.json",
    "real_dependency_check_authorization_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "real_dependency_check_authorization_planning_decision_v1.json",
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
            "ocr_provider_real_dependency_check_authorization_planning"
        ),
    )
    p.add_argument(
        "--ocr-authorization-next-route-decision-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_authorization_next_route_decision",
    )
    p.add_argument(
        "--ocr-provider-real-dependency-check-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_provider_real_dependency_check_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    route_root = Path(args.ocr_authorization_next_route_decision_root)
    real_dep_post_root = Path(args.ocr_provider_real_dependency_check_post_dryrun_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    route_review = _load(root / "ocr_authorization_next_route_input_review_v1.json")
    scope = _load(root / "real_dependency_check_authorization_scope_v1.json")
    request_contract = _load(root / "real_dependency_check_authorization_request_contract_v1.json")
    grant_contract = _load(root / "real_dependency_check_grant_contract_v1.json")
    window_contract = _load(root / "real_dependency_check_execution_window_contract_v1.json")
    allowed = _load(root / "allowed_dependency_check_action_matrix_v1.json")
    forbidden = _load(root / "forbidden_dependency_check_action_matrix_v1.json")
    sandbox = _load(root / "real_dependency_check_sandbox_boundary_plan_v1.json")
    evidence = _load(root / "real_dependency_check_evidence_requirement_v1.json")
    rollback = _load(root / "real_dependency_check_rollback_policy_v1.json")
    approval = _load(root / "owner_operator_approval_policy_v1.json")
    provider_binding = _load(root / "provider_selection_non_finalize_binding_v1.json")
    state_machine = _load(root / "real_dependency_check_authorization_state_machine_v1.json")
    blocked = _load(root / "real_dependency_check_authorization_blocked_path_matrix_v1.json")
    dryrun_plan = _load(root / "real_dependency_check_authorization_dryrun_plan_v1.json")
    decision = _load(root / "real_dependency_check_authorization_planning_decision_v1.json")

    route_vr = _load(route_root / "verifier_report.json")
    route_sm = _load(route_root / "summary.json")
    real_dep_closure = _load(real_dep_post_root / "real_dependency_check_closure_decision_v1.json")
    real_dep_post_sm = _load(real_dep_post_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_provider_real_dependency_check_authorization_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_state") == CURRENT_STATE)
    ok("summary.route", summary.get("selected_route") == SELECTED_ROUTE)

    ok("upstream.route_go", route_vr.get("verifier") == "GO")
    ok("upstream.route_final", route_sm.get("final_decision") == NEXT_ROUTE_FINAL)
    ok("upstream.route_next", route_sm.get("recommended_next_phase") == NEXT_ROUTE_NEXT)
    ok("upstream.flow_trusted", real_dep_post_sm.get("real_dependency_check_flow_trusted") is True)
    ok("upstream.evidence_trusted", real_dep_closure.get("evidence_package_candidate_trusted") is True)
    ok("route_review.pass", route_review.get("review_pass") is True)

    ok("scope.in8", len(scope.get("in_scope") or []) == len(AUTHORIZATION_SCOPE_IN))
    ok("scope.out7", len(scope.get("out_of_scope") or []) == len(AUTHORIZATION_SCOPE_OUT))
    ok("scope.target", scope.get("target_scope") == TARGET_SCOPE)

    ok("request.type", request_contract.get("request_type") == REQUEST_TYPE)
    ok("request.target", request_contract.get("target_scope") == TARGET_SCOPE)
    ok("request.no_gen", request_contract.get("request_generated_now") is False)
    ok("request.no_sent", request_contract.get("request_sent_now") is False)
    ok("request.sandbox", request_contract.get("sandbox_required") is True)
    ok("request.approval", request_contract.get("owner_operator_approval_required") is True)

    ok("grant.no_finalize", grant_contract.get("no_provider_selection_finalize") is True)
    ok("grant.no_trial", grant_contract.get("no_controlled_trial") is True)
    ok("grant.no_prod", grant_contract.get("no_production_runtime") is True)
    ok("grant.not_issued", grant_contract.get("grant_issued_now") is False)

    ok("window.no_open", window_contract.get("current_window_opened_now") is False)
    ok("window.no_install", window_contract.get("no_install") is True)
    ok("window.no_download", window_contract.get("no_download") is True)

    ok("allowed.count8", allowed.get("action_count") == len(ALLOWED_ACTIONS_LATER))
    for action in ALLOWED_ACTIONS_LATER:
        row = next((a for a in (allowed.get("actions") or []) if a.get("action_id") == action), None)
        ok(f"allowed.{action}", row is not None and row.get("current_executed_now") is False)
        if row:
            ok(f"allowed.{action}.sandbox", row.get("requires_sandbox") is True)

    ok("forbidden.count", forbidden.get("action_count") == len(FORBIDDEN_ACTIONS))
    for action in FORBIDDEN_ACTIONS:
        row = next((a for a in (forbidden.get("forbidden_actions") or []) if a.get("action_id") == action), None)
        ok(f"forbidden.{action}", row is not None and row.get("status") == "forbidden")

    ok("evidence.count", evidence.get("field_count") == len(EVIDENCE_REQUIREMENTS))
    ok("rollback.ready_later", rollback.get("rollback_plan_ready_later") is True)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)
    for pol in ROLLBACK_POLICIES:
        ok(f"rollback.policy.{pol[:20]}", pol in (rollback.get("policies") or []))

    ok("approval.required", approval.get("owner_operator_approval_required") is True)
    ok("approval.not_now", approval.get("approval_collected_now") is False)

    ok("provider.null", provider_binding.get("selected_provider_for_execution") is None)
    ok("provider.no_finalize", provider_binding.get("provider_selection_finalized_now") is False)
    ok("provider.cannot_finalize", provider_binding.get("current_phase_cannot_finalize_provider") is True)

    ok("state_machine.current", state_machine.get("current_state") == CURRENT_STATE)
    ok("state_machine.states", state_machine.get("states") == list(LIFECYCLE_STATES))

    ok("blocked.count", blocked.get("path_count") == len(BLOCKED_PATHS))
    ok("blocked.all", blocked.get("all_blocked") is True)
    for bp in BLOCKED_PATHS:
        row = next((r for r in (blocked.get("blocked_paths") or []) if r.get("path_id") == bp), None)
        ok(f"blocked.{bp}", row is not None and row.get("status") == "blocked")

    ok("dryrun.merged", dryrun_plan.get("dryrun_and_review_merged") is True)
    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.no_exec", dryrun_plan.get("real_dependency_check_executed_now") is False)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)

    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)
    ok("summary.no_import", summary.get("provider_imported_now") is False)

    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    ok("sandbox.required", sandbox.get("sandbox_required") is True)

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
