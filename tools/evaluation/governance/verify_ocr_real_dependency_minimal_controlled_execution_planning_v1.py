#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Minimal Controlled Execution Planning v1."""

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
from capabilities.governance.ocr_real_dependency_minimal_controlled_execution_planning_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    EVIDENCE_OUTPUT_ITEMS,
    EXCLUDED_FROM_SCOPE,
    FAILURE_ROUTES,
    FINAL_DECISION_GO,
    MINIMAL_FORBIDDEN_ACTIONS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_PREFLIGHT_FINAL,
    UPSTREAM_PREFLIGHT_NEXT,
)

MIN_CHECKS = 100

REQUIRED = (
    "minimal_controlled_execution_planning_policy_v1.json",
    "final_preflight_input_review_v1.json",
    "minimal_execution_scope_v1.json",
    "minimal_execution_window_candidate_plan_v1.json",
    "minimal_execution_sandbox_plan_v1.json",
    "minimal_allowed_check_plan_v1.json",
    "minimal_forbidden_action_plan_v1.json",
    "minimal_evidence_output_plan_v1.json",
    "minimal_failure_route_plan_v1.json",
    "minimal_rollback_plan_v1.json",
    "minimal_post_execution_review_plan_v1.json",
    "minimal_execution_verifier_plan_v1.json",
    "provider_selection_non_finalize_plan_v1.json",
    "minimal_execution_blocked_path_matrix_v1.json",
    "minimal_controlled_execution_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "minimal_controlled_execution_planning_decision_v1.json",
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
            "ocr_real_dependency_minimal_controlled_execution_planning"
        ),
    )
    p.add_argument(
        "--final-preflight-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_final_preflight"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    preflight_root = Path(args.final_preflight_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    preflight_vr = _load(preflight_root / "verifier_report.json")
    preflight_sm = _load(preflight_root / "summary.json")
    summary = _load(root / "summary.json")
    scope = _load(root / "minimal_execution_scope_v1.json")
    window = _load(root / "minimal_execution_window_candidate_plan_v1.json")
    sandbox = _load(root / "minimal_execution_sandbox_plan_v1.json")
    allowed = _load(root / "minimal_allowed_check_plan_v1.json")
    forbidden = _load(root / "minimal_forbidden_action_plan_v1.json")
    evidence = _load(root / "minimal_evidence_output_plan_v1.json")
    failure = _load(root / "minimal_failure_route_plan_v1.json")
    rollback = _load(root / "minimal_rollback_plan_v1.json")
    post = _load(root / "minimal_post_execution_review_plan_v1.json")
    provider = _load(root / "provider_selection_non_finalize_plan_v1.json")
    blocked = _load(root / "minimal_execution_blocked_path_matrix_v1.json")
    dryrun = _load(root / "minimal_controlled_execution_dryrun_plan_v1.json")

    ok("upstream.preflight_go", preflight_vr.get("verifier") == "GO")
    ok("upstream.preflight_final", preflight_sm.get("final_decision") == UPSTREAM_PREFLIGHT_FINAL)
    ok("upstream.preflight_next", preflight_sm.get("recommended_next_phase") == UPSTREAM_PREFLIGHT_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("minimal_controlled_execution_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.not_started", summary.get("minimal_controlled_execution_started_now") is False)

    ok("scope.allowed5", scope.get("allowed_checks_later") == list(MINIMAL_SCOPE_ALLOWED_CHECKS))
    ok("scope.count5", scope.get("allowed_check_count") == 5)
    for ex in EXCLUDED_FROM_SCOPE:
        ok(f"scope.excluded.{ex[:12]}", ex in (scope.get("excluded_from_scope") or []))

    ok("window.id", bool(window.get("execution_window_candidate_id")))
    ok("window.scope", window.get("scope") == "minimal_real_dependency_check")
    ok("window.checks5", window.get("allowed_checks") == 5)
    ok("window.not_open", window.get("window_opened_now") is False)
    ok("window.no_prod", window.get("no_production_write") is True)
    ok("window.no_install", window.get("no_install") is True)

    ok("sandbox.controlled", sandbox.get("workspace_controlled_only") is True)
    ok("sandbox.no_prod", sandbox.get("no_production_path_write") is True)
    ok("sandbox.no_ocr", sandbox.get("no_ocr_runtime") is True)

    ok("allowed.count5", allowed.get("check_count") == 5)
    for cid in MINIMAL_SCOPE_ALLOWED_CHECKS:
        item = next((c for c in allowed.get("checks") or [] if c.get("check_id") == cid), {})
        ok(f"check.{cid}.later", item.get("execution_allowed_later") is True)
        ok(f"check.{cid}.false", item.get("current_executed_now") is False)
        ok(f"check.{cid}.evidence", item.get("evidence_required") is True)
        ok(f"check.{cid}.rollback", item.get("rollback_required") is True)

    ok("forbidden.18", forbidden.get("forbidden_count") == 18)
    ok("forbidden.list", forbidden.get("forbidden_actions") == list(MINIMAL_FORBIDDEN_ACTIONS))

    ok("evidence.13", evidence.get("evidence_count") == 13)
    for item in EVIDENCE_OUTPUT_ITEMS:
        ok(f"evidence.{item[:15]}", item in (evidence.get("future_execution_must_generate") or []))

    ok("failure.routes8", failure.get("route_count") == 8)
    conditions = {r.get("condition") for r in failure.get("routes") or []}
    for route in FAILURE_ROUTES:
        ok(f"failure.{route['condition']}", route["condition"] in conditions)

    ok("rollback.no_install", rollback.get("failed_package_check_does_not_trigger_install") is True)
    ok("rollback.not_executed", rollback.get("rollback_executed_now") is False)

    ok("post.required", post.get("review_required") is True)
    ok("post.verifier", post.get("verifier_required") is True)

    ok("provider.null", provider.get("selected_provider_for_execution") is None)
    ok("provider.no_finalize", provider.get("provider_selection_finalized_now") is False)
    ok("provider.cannot_finalize", provider.get("current_planning_cannot_finalize_provider") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count22", blocked.get("blocked_count") == 22)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp[:18]}", bp in blocked_ids)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    pass_all = summary.get("planning_pass") is True
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
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
