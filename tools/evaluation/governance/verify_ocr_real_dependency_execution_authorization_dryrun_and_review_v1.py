#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Execution Authorization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_STANDARD_ID,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    EVIDENCE_ARTIFACTS,
    FINAL_DECISION_GO,
    FORBIDDEN_EXECUTION_ACTIONS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SCOPE_ALLOWED_CHECKS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT_PHASE,
    VALIDATION_GATE_PATH,
)
MIN_CHECKS = 120

CHECK_ITEM_KEYS = (
    "check_id",
    "allowed_later",
    "current_executed_now",
    "requires_execution_window",
    "requires_sandbox",
    "requires_evidence",
    "requires_validation_gate",
    "requires_post_execution_review",
    "failure_route_ref",
)

REQUIRED = (
    "ocr_real_dependency_execution_authorization_dryrun_review_policy_v1.json",
    "execution_authorization_planning_input_review_v1.json",
    "execution_authorization_request_candidate_v1.json",
    "execution_grant_candidate_v1.json",
    "execution_window_candidate_v1.json",
    "allowed_check_plan_candidate_v1.json",
    "forbidden_action_review_v1.json",
    "evidence_collection_candidate_v1.json",
    "rollback_failure_route_candidate_v1.json",
    "validation_gate_path_dryrun_review_v1.json",
    "provider_selection_non_finalize_review_v1.json",
    "state_machine_dryrun_review_v1.json",
    "execution_authorization_boundary_audit_v1.json",
    "execution_authorization_blocked_path_result_v1.json",
    "execution_authorization_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)

REQUEST_REQUIRED = (
    "request_candidate_id",
    "request_type",
    "provider_domain",
    "authorization_target",
    "source_domain_config_ref",
    "factory_authorization_standard_ref",
    "validation_engineering_ref",
    "requested_allowed_checks",
    "forbidden_actions_ref",
    "execution_window_required",
    "sandbox_required",
    "rollback_required",
    "evidence_collection_required",
    "validation_gate_required",
    "post_execution_review_required",
    "owner_operator_approval_required",
    "candidate_only",
    "formal_request_generated_now",
    "request_sent_now",
)

GRANT_REQUIRED = (
    "grant_candidate_id",
    "related_request_candidate_id",
    "grant_scope",
    "allowed_actions_later",
    "prohibited_actions",
    "expiration_or_ttl",
    "revocation_conditions",
    "no_provider_selection_finalize",
    "no_controlled_trial",
    "no_production_runtime",
    "no_ocr_fact",
    "candidate_only",
    "grant_issued_now",
)

WINDOW_REQUIRED = (
    "execution_window_candidate_id",
    "allowed_workspace_path",
    "allowed_output_path",
    "forbidden_paths",
    "max_check_scope",
    "timeout_limit",
    "no_production_write",
    "no_network_by_default",
    "no_install",
    "no_download",
    "no_cache_mutation_without_approval",
    "post_execution_review_required",
    "candidate_only",
    "execution_window_opened_now",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_authorization_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_authorization_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.ocr_real_dependency_execution_authorization_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    plan_sm_machine = _load(plan_root / "execution_authorization_state_machine_v1.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT_PHASE)
    ok("upstream.state", plan_sm_machine.get("current_state") == "planning_defined")

    summary = _load(root / "summary.json")
    policy = _load(root / "ocr_real_dependency_execution_authorization_dryrun_review_policy_v1.json")
    plan_in = _load(root / "execution_authorization_planning_input_review_v1.json")
    request = _load(root / "execution_authorization_request_candidate_v1.json")
    grant = _load(root / "execution_grant_candidate_v1.json")
    window = _load(root / "execution_window_candidate_v1.json")
    allowed = _load(root / "allowed_check_plan_candidate_v1.json")
    forbidden_rev = _load(root / "forbidden_action_review_v1.json")
    evidence = _load(root / "evidence_collection_candidate_v1.json")
    rollback = _load(root / "rollback_failure_route_candidate_v1.json")
    gate = _load(root / "validation_gate_path_dryrun_review_v1.json")
    provider = _load(root / "provider_selection_non_finalize_review_v1.json")
    blocked = _load(root / "execution_authorization_blocked_path_result_v1.json")
    closure = _load(root / "execution_authorization_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("ocr_real_dependency_execution_authorization_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("plan_in.pass", plan_in.get("review_pass") is True)
    ok("plan_in.blocked24", plan_in.get("blocked_path_count") == 24)

    ok("request.type", request.get("request_type") == "ocr_real_dependency_execution_authorization_request")
    ok("request.std", request.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    for key in REQUEST_REQUIRED:
        ok(f"request.{key}", key in request)
    ok("request.candidate_only", request.get("candidate_only") is True)
    ok("request.no_formal", request.get("formal_request_generated_now") is False)

    for key in GRANT_REQUIRED:
        ok(f"grant.{key}", key in grant)
    ok("grant.not_issued", grant.get("grant_issued_now") is False)

    for key in WINDOW_REQUIRED:
        ok(f"window.{key}", key in window)
    ok("window.not_open", window.get("execution_window_opened_now") is False)

    ok("allowed.count8", allowed.get("check_count") == 8)
    for item in allowed.get("checks") or []:
        cid = item.get("check_id")
        ok(f"allowed.{cid}", cid in SCOPE_ALLOWED_CHECKS)
        for k in CHECK_ITEM_KEYS:
            ok(f"allowed.{cid}.{k}", k in item)
        ok(f"allowed.{cid}.not_exec", item.get("current_executed_now") is False)

    ok("forbidden.pass", forbidden_rev.get("dryrun_and_review_pass") is True)

    for artifact in EVIDENCE_ARTIFACTS:
        ok(f"evidence.{artifact}", artifact in (evidence.get("collect_on_future_execution") or []))

    ok("rollback.no_install", rollback.get("failed_package_check_does_not_trigger_install") is True)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)

    ok("gate.pass", gate.get("dryrun_and_review_pass") is True)
    ok("gate.path_count", len(gate.get("path_mappings") or []) == len(VALIDATION_GATE_PATH))
    ok("gate.no_runtime", gate.get("validator_runtime_enabled_now") is False)
    ok("gate.no_exec", gate.get("no_gate_executed_now") is True)

    ok("provider.pass", provider.get("dryrun_and_review_pass") is True)
    ok("provider.null", provider.get("selected_provider_for_execution") is None)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", bp in blocked_ids)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("next.ready", next_route.get("ready_for_execution_request_generation_roadmap_decision") is True)
    ok("next.no_formal", next_route.get("do_not_generate_formal_request_now") is True)

    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    for action in FORBIDDEN_EXECUTION_ACTIONS:
        ok(f"forbidden_in_grant.{action}", action in (grant.get("prohibited_actions") or []))

    ok("non_claims", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

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
