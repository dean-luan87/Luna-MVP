#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Provider Authorization DryRun v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.ocr_provider_authorization_dryrun_v1 import (
    BOUNDARY_FALSE,
    CURRENT_DRYRUN_STATE,
    DRYRUN_BLOCKED_PATHS,
    FINAL_DECISION_GO,
    LIFECYCLE_STATES,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
)
from capabilities.governance.ocr_provider_authorization_planning_v1 import (
    BOUNDARY_BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    CURRENT_LIFECYCLE_STATE as PLANNING_LIFECYCLE_STATE,
    EVIDENCE_REQUIREMENTS,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 85

REQUIRED = (
    "ocr_provider_authorization_dryrun_policy_v1.json",
    "authorization_planning_input_review_v1.json",
    "authorization_request_candidate_v1.json",
    "grant_candidate_v1.json",
    "execution_window_candidate_v1.json",
    "sandbox_boundary_candidate_v1.json",
    "rollback_candidate_v1.json",
    "evidence_requirement_candidate_v1.json",
    "owner_operator_approval_dryrun_result_v1.json",
    "provider_selection_binding_dryrun_result_v1.json",
    "real_dependency_check_authorization_binding_dryrun_result_v1.json",
    "controlled_trial_authorization_binding_dryrun_result_v1.json",
    "authorization_lifecycle_dryrun_result_v1.json",
    "authorization_boundary_guard_dryrun_result_v1.json",
    "authorization_blocked_path_result_v1.json",
    "authorization_dryrun_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_dryrun",
    )
    p.add_argument(
        "--ocr-provider-authorization-planning-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/ocr_provider_authorization_planning",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.ocr_provider_authorization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    input_review = _load(root / "authorization_planning_input_review_v1.json")
    request = _load(root / "authorization_request_candidate_v1.json")
    grant = _load(root / "grant_candidate_v1.json")
    window = _load(root / "execution_window_candidate_v1.json")
    sandbox = _load(root / "sandbox_boundary_candidate_v1.json")
    rollback = _load(root / "rollback_candidate_v1.json")
    evidence = _load(root / "evidence_requirement_candidate_v1.json")
    owner = _load(root / "owner_operator_approval_dryrun_result_v1.json")
    selection = _load(root / "provider_selection_binding_dryrun_result_v1.json")
    lifecycle = _load(root / "authorization_lifecycle_dryrun_result_v1.json")
    boundary = _load(root / "authorization_boundary_guard_dryrun_result_v1.json")
    blocked = _load(root / "authorization_blocked_path_result_v1.json")
    readiness = _load(root / "authorization_dryrun_readiness_decision_v1.json")

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("ocr_provider_authorization_dryrun_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_lifecycle_state") == CURRENT_DRYRUN_STATE)

    ok("summary.req_cand", summary.get("authorization_request_candidate_generated_now") is True)
    ok("summary.grant_cand", summary.get("grant_candidate_generated_now") is True)
    ok("summary.window_cand", summary.get("execution_window_candidate_generated_now") is True)

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.plan_state", plan_sm.get("current_lifecycle_state") == PLANNING_LIFECYCLE_STATE)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.blocked14", input_review.get("planning_blocked_path_count") == len(PLANNING_BLOCKED_PATHS))

    ok("request.type", request.get("request_type") == "ocr_provider_authorization_request")
    ok("request.candidate", request.get("candidate_only") is True)
    ok("request.no_artifact", request.get("request_artifact_generated_now") is False)
    ok("request.no_sent", request.get("request_sent_now") is False)
    ok("request.window", request.get("execution_window_required") is True)

    ok("grant.candidate", grant.get("candidate_only") is True)
    ok("grant.no_grant", grant.get("current_grant_issued_now") is False)
    ok("grant.no_auth", grant.get("provider_authorization_granted_now") is False)
    ok("grant.post_review", grant.get("post_execution_review_required") is True)

    ok("window.no_open", window.get("current_window_opened_now") is False)
    ok("window.no_prod", window.get("no_production_write") is True)

    ok("sandbox.fallback", sandbox.get("workspace_fallback_only") is True)
    ok("sandbox.no_prod", sandbox.get("no_production_path_write") is True)
    ok("sandbox.no_ocr", sandbox.get("no_real_ocr_invocation_without_controlled_trial_authorization") is True)

    ok("rollback.no_install", rollback.get("failed_check_does_not_trigger_install") is True)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)

    ok("evidence.count11", len(evidence.get("required_artifacts_on_future_execution") or []) == len(EVIDENCE_REQUIREMENTS))

    ok("owner.no_collect", owner.get("approval_collected_now") is False)
    ok("owner.real_dep", owner.get("approval_required_for_real_dependency_check") is True)

    ok("selection.null", selection.get("selected_provider_for_execution") is None)
    ok("selection.not_final", selection.get("provider_selection_finalized_now") is False)

    ok("lifecycle.state", lifecycle.get("current_state") == CURRENT_DRYRUN_STATE)
    ok("lifecycle.prior", lifecycle.get("prior_state") == PLANNING_LIFECYCLE_STATE)
    ok("lifecycle.no_gen", lifecycle.get("request_generated_now") is False)
    ok("lifecycle.no_grant", lifecycle.get("grant_issued_now") is False)
    ok("lifecycle.states10", len(lifecycle.get("states") or []) == len(LIFECYCLE_STATES))

    ok("boundary.count15", boundary.get("path_count") == len(DRYRUN_BLOCKED_PATHS))
    ok("boundary.all", boundary.get("all_blocked") is True)
    ok("blocked.count15", blocked.get("path_count") == len(DRYRUN_BLOCKED_PATHS))

    ok("readiness.all", readiness.get("all_pass") is True)
    ok("readiness.final", readiness.get("final_decision") == FINAL_DECISION_GO)

    ok("summary.null_provider", summary.get("selected_provider_for_execution") is None)
    ok("summary.no_artifact", summary.get("authorization_request_artifact_generated_now") is False)
    ok("summary.no_grant", summary.get("provider_authorization_granted_now") is False)
    ok("summary.no_grant_issued", summary.get("grant_issued_now") is False)
    ok("summary.no_real_dep", summary.get("real_dependency_check_executed_now") is False)

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
