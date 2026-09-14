#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Execution Final Preflight v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.health_management_layer_integration_planning_v1 import (
    HEALTH_METRIC_DEFINITION_STATUS,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_planning_v1 import (
    FORBIDDEN_EXECUTION_ACTIONS,
    SCOPE_ALLOWED_CHECKS,
)
from capabilities.governance.ocr_real_dependency_execution_final_preflight_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    MINIMAL_SCOPE_ALLOWED_CHECKS,
    MINIMAL_SCOPE_STILL_FORBIDDEN,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    UPSTREAM_AUTH_FINAL,
    UPSTREAM_AUTH_NEXT,
)
from capabilities.governance.ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review_v1 import (
    VALIDATION_GATES_PLANNED,
)

MIN_CHECKS = 120

REQUIRED = (
    "ocr_real_dependency_execution_final_preflight_policy_v1.json",
    "authorization_dryrun_input_review_v1.json",
    "formal_request_authorization_candidate_review_v1.json",
    "owner_operator_approval_precheck_review_v1.json",
    "evidence_readiness_review_v1.json",
    "validation_gate_readiness_review_v1.json",
    "sandbox_boundary_readiness_review_v1.json",
    "allowed_check_final_preflight_review_v1.json",
    "forbidden_action_final_preflight_review_v1.json",
    "rollback_readiness_review_v1.json",
    "provider_selection_non_finalize_review_v1.json",
    "health_signal_reserved_boundary_review_v1.json",
    "no_runtime_boundary_final_audit_v1.json",
    "controlled_execution_minimal_scope_plan_v1.json",
    "final_preflight_blocked_path_result_v1.json",
    "final_preflight_closure_decision_v1.json",
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
            "ocr_real_dependency_execution_final_preflight"
        ),
    )
    p.add_argument(
        "--authorization-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_formal_request_generation_authorization_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    auth_root = Path(args.authorization_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    auth_vr = _load(auth_root / "verifier_report.json")
    auth_sm = _load(auth_root / "summary.json")
    summary = _load(root / "summary.json")
    minimal = _load(root / "controlled_execution_minimal_scope_plan_v1.json")
    blocked = _load(root / "final_preflight_blocked_path_result_v1.json")
    health = _load(root / "health_signal_reserved_boundary_review_v1.json")
    allowed = _load(root / "allowed_check_final_preflight_review_v1.json")
    auth_review = _load(root / "formal_request_authorization_candidate_review_v1.json")
    approval = _load(root / "owner_operator_approval_precheck_review_v1.json")
    evidence = _load(root / "evidence_readiness_review_v1.json")
    gate = _load(root / "validation_gate_readiness_review_v1.json")
    sandbox = _load(root / "sandbox_boundary_readiness_review_v1.json")
    next_route = _load(root / "next_phase_readiness_decision_v1.json")

    ok("upstream.auth_go", auth_vr.get("verifier") == "GO")
    ok("upstream.auth_final", auth_sm.get("final_decision") == UPSTREAM_AUTH_FINAL)
    ok("upstream.auth_next", auth_sm.get("recommended_next_phase") == UPSTREAM_AUTH_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.preflight_only", summary.get("ocr_real_dependency_execution_final_preflight_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.not_authorized", summary.get("controlled_execution_authorized_now") is False)

    ok("auth_review.pass", auth_review.get("dryrun_and_review_pass") is True)
    ok("approval.pass", approval.get("dryrun_and_review_pass") is True)
    ok("evidence.pass", evidence.get("dryrun_and_review_pass") is True)
    ok("gate.pass", gate.get("dryrun_and_review_pass") is True)
    ok("sandbox.pass", sandbox.get("dryrun_and_review_pass") is True)
    ok("allowed.pass", allowed.get("dryrun_and_review_pass") is True)
    ok("allowed.count8", allowed.get("check_count") == 8)

    for cid in SCOPE_ALLOWED_CHECKS:
        item = next((c for c in allowed.get("check_plan_items") or [] if c.get("check_id") == cid), {})
        ok(f"check.{cid}.false", item.get("current_executed_now") is False)
        ok(f"check.{cid}.later", item.get("allowed_later") is True)

    ok("gate.review_pass", gate.get("dryrun_and_review_pass") is True)

    ok("sandbox.workspace", sandbox.get("workspace_controlled_output_only") is True)
    ok("sandbox.no_prod", sandbox.get("no_production_write") is True)
    ok("sandbox.no_install", sandbox.get("no_install") is True)

    ok("minimal.allowed5", minimal.get("allowed_checks_if_controlled_execution_entered") == list(
        MINIMAL_SCOPE_ALLOWED_CHECKS
    ))
    ok("minimal.forbidden", len(minimal.get("still_forbidden_in_next_phase") or []) >= len(
        MINIMAL_SCOPE_STILL_FORBIDDEN
    ))

    ok("health.reserved", health.get("health_metric_definition_status") == HEALTH_METRIC_DEFINITION_STATUS)
    ok("health.no_score", health.get("no_numeric_health_score_invented") is True)
    ok("health.no_auto_auth", health.get("health_does_not_auto_authorize_execution") is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp[:20]}", bp in blocked_ids)

    ok("forbidden.15", len(_load(root / "forbidden_action_final_preflight_review_v1.json").get("forbidden_actions") or []) == 15)
    ok("forbidden.match", list(_load(root / "forbidden_action_final_preflight_review_v1.json").get("forbidden_actions") or []) == list(FORBIDDEN_EXECUTION_ACTIONS))

    ok("next.planning", next_route.get("ready_for_minimal_controlled_execution_planning") is True)
    ok("next.no_exec", next_route.get("ready_for_minimal_controlled_execution") is False)

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
