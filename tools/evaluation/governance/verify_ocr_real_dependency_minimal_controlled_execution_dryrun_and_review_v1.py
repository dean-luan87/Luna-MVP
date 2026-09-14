#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Minimal Controlled Execution DryRunAndReview v1."""

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
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    CHECK_TYPES,
    EVIDENCE_OUTPUT_ITEMS,
    EXCLUDED_FROM_SCOPE,
    FAILURE_ROUTES,
    MINIMAL_FORBIDDEN_ACTIONS,
)

MIN_CHECKS = 130

REQUIRED = (
    "minimal_controlled_execution_dryrun_review_policy_v1.json",
    "minimal_controlled_execution_planning_input_review_v1.json",
    "minimal_controlled_execution_plan_candidate_v1.json",
    "minimal_execution_scope_dryrun_review_v1.json",
    "minimal_execution_window_candidate_review_v1.json",
    "minimal_execution_sandbox_review_v1.json",
    "minimal_allowed_check_plan_dryrun_review_v1.json",
    "minimal_forbidden_action_dryrun_review_v1.json",
    "minimal_evidence_output_dryrun_review_v1.json",
    "minimal_failure_route_dryrun_review_v1.json",
    "minimal_rollback_dryrun_review_v1.json",
    "minimal_post_execution_review_dryrun_review_v1.json",
    "minimal_execution_verifier_plan_review_v1.json",
    "provider_selection_non_finalize_review_v1.json",
    "minimal_controlled_execution_boundary_audit_v1.json",
    "minimal_controlled_execution_blocked_path_result_v1.json",
    "minimal_controlled_execution_closure_decision_v1.json",
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
            "ocr_real_dependency_minimal_controlled_execution_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_minimal_controlled_execution_planning"
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
    candidate = _load(root / "minimal_controlled_execution_plan_candidate_v1.json")
    scope = _load(root / "minimal_execution_scope_dryrun_review_v1.json")
    window = _load(root / "minimal_execution_window_candidate_review_v1.json")
    sandbox = _load(root / "minimal_execution_sandbox_review_v1.json")
    allowed = _load(root / "minimal_allowed_check_plan_dryrun_review_v1.json")
    forbidden = _load(root / "minimal_forbidden_action_dryrun_review_v1.json")
    evidence = _load(root / "minimal_evidence_output_dryrun_review_v1.json")
    failure = _load(root / "minimal_failure_route_dryrun_review_v1.json")
    rollback = _load(root / "minimal_rollback_dryrun_review_v1.json")
    post = _load(root / "minimal_post_execution_review_dryrun_review_v1.json")
    verifier = _load(root / "minimal_execution_verifier_plan_review_v1.json")
    provider = _load(root / "provider_selection_non_finalize_review_v1.json")
    blocked = _load(root / "minimal_controlled_execution_blocked_path_result_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.dryrun_only", summary.get("minimal_controlled_execution_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.not_started", summary.get("minimal_controlled_execution_started_now") is False)

    ok("candidate.id", bool(candidate.get("plan_candidate_id")))
    ok("candidate.scope", candidate.get("execution_scope") == "minimal_real_dependency_check")
    ok("candidate.only", candidate.get("candidate_only") is True)
    ok("candidate.checks5", candidate.get("allowed_checks_count") == 5)
    ok("candidate.forbidden18", candidate.get("forbidden_actions_count") >= 18)
    ok("candidate.no_finalize", candidate.get("provider_selection_finalize_allowed_now") is False)

    ok("scope.pass", scope.get("dryrun_and_review_pass") is True)
    ok("window.pass", window.get("dryrun_and_review_pass") is True)
    ok("sandbox.pass", sandbox.get("dryrun_and_review_pass") is True)
    ok("allowed.pass", allowed.get("dryrun_and_review_pass") is True)
    ok("forbidden.pass", forbidden.get("dryrun_and_review_pass") is True)
    ok("evidence.pass", evidence.get("dryrun_and_review_pass") is True)
    ok("failure.pass", failure.get("dryrun_and_review_pass") is True)
    ok("rollback.pass", rollback.get("dryrun_and_review_pass") is True)
    ok("post.pass", post.get("dryrun_and_review_pass") is True)
    ok("verifier.pass", verifier.get("dryrun_and_review_pass") is True)
    ok("provider.pass", provider.get("dryrun_and_review_pass") is True)

    for cid in MINIMAL_SCOPE_ALLOWED_CHECKS:
        item = next((c for c in allowed.get("check_plan_items") or [] if c.get("check_id") == cid), {})
        ok(f"check.{cid}.type", item.get("check_type") == CHECK_TYPES[cid])
        ok(f"check.{cid}.later", item.get("execution_allowed_later") is True)
        ok(f"check.{cid}.false", item.get("current_executed_now") is False)

    for action in MINIMAL_FORBIDDEN_ACTIONS:
        ok(f"forbidden.{action[:12]}", action in (forbidden.get("forbidden_actions") or []))

    for item in EVIDENCE_OUTPUT_ITEMS:
        ok(f"evidence.{item[:15]}", item in (evidence.get("future_evidence_items") or []))

    conditions = {r.get("condition"): r for r in failure.get("routes") or []}
    for route in FAILURE_ROUTES:
        ok(f"failure.{route['condition']}", route["condition"] in conditions)

    for ex in EXCLUDED_FROM_SCOPE:
        ok(f"excluded.{ex[:12]}", scope.get("dryrun_and_review_pass") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count22", blocked.get("blocked_count") == 22)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp[:18]}", bp in blocked_ids)

    ok("next.auth_decision", next_route.get("ready_for_real_minimal_execution_authorization_decision") is True)
    ok("next.no_exec", next_route.get("ready_for_real_minimal_controlled_execution") is False)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("provider.null", summary.get("selected_provider_for_execution") is None)
    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("dryrun_and_review_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
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
