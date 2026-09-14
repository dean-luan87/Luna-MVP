#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Execution Authorization Planning v1."""

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
from capabilities.governance.ocr_real_dependency_execution_authorization_planning_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    EVIDENCE_ARTIFACTS,
    FINAL_DECISION_GO,
    FORBIDDEN_EXECUTION_ACTIONS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SCOPE_ALLOWED_CHECKS,
    SCOPE_NOT_COVERED,
    STATE_MACHINE_STATES,
    UPSTREAM_ROADMAP_FINAL,
    UPSTREAM_ROADMAP_NEXT,
    UPSTREAM_VALIDATION_SEP_DR_FINAL,
    VALIDATION_GATE_PATH,
)
from capabilities.governance.ocr_real_dependency_execution_authorization_roadmap_decision_v1 import (
    SELECTED_ROUTE,
)

MIN_CHECKS = 95

REQUIRED = (
    "ocr_real_dependency_execution_authorization_planning_policy_v1.json",
    "roadmap_decision_input_review_v1.json",
    "domain_config_candidate_input_review_v1.json",
    "validation_engineering_input_review_v1.json",
    "execution_authorization_scope_v1.json",
    "execution_authorization_request_candidate_contract_v1.json",
    "execution_grant_candidate_contract_v1.json",
    "execution_window_candidate_contract_v1.json",
    "execution_sandbox_boundary_plan_v1.json",
    "allowed_real_dependency_check_plan_v1.json",
    "forbidden_execution_action_plan_v1.json",
    "evidence_collection_plan_v1.json",
    "rollback_and_failure_route_plan_v1.json",
    "validation_gate_execution_path_plan_v1.json",
    "provider_selection_non_finalize_plan_v1.json",
    "execution_authorization_state_machine_v1.json",
    "execution_authorization_blocked_path_matrix_v1.json",
    "execution_authorization_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "execution_authorization_planning_decision_v1.json",
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
    "request_generated_now",
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


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_authorization_planning"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-execution-authorization-roadmap-decision-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_execution_authorization_roadmap_decision"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--midplatform-validation-engineering-separation-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_validation_engineering_separation_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    roadmap_root = Path(args.ocr_real_dependency_execution_authorization_roadmap_decision_root)
    ocr_dr_root = Path(args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root)
    val_root = Path(args.midplatform_validation_engineering_separation_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    roadmap_vr = _load(roadmap_root / "verifier_report.json")
    roadmap_sm = _load(roadmap_root / "summary.json")
    ocr_cfg = _load(ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json")
    val_vr = _load(val_root / "verifier_report.json")
    val_sm = _load(val_root / "summary.json")
    val_model = _load(val_root / "validation_engineering_model_candidate_v1.json")

    ok("upstream.roadmap_go", roadmap_vr.get("verifier") == "GO")
    ok("upstream.roadmap_final", roadmap_sm.get("final_decision") == UPSTREAM_ROADMAP_FINAL)
    ok("upstream.roadmap_next", roadmap_sm.get("recommended_next_phase") == UPSTREAM_ROADMAP_NEXT)
    ok("upstream.route_a", roadmap_sm.get("selected_route") == SELECTED_ROUTE)
    ok("upstream.domain_config", bool(ocr_cfg.get("candidate_id")))
    ok("upstream.val_go", val_vr.get("verifier") == "GO")
    ok("upstream.val_final", val_sm.get("final_decision") == UPSTREAM_VALIDATION_SEP_DR_FINAL)

    summary = _load(root / "summary.json")
    policy = _load(root / "ocr_real_dependency_execution_authorization_planning_policy_v1.json")
    roadmap_in = _load(root / "roadmap_decision_input_review_v1.json")
    domain_in = _load(root / "domain_config_candidate_input_review_v1.json")
    val_in = _load(root / "validation_engineering_input_review_v1.json")
    scope = _load(root / "execution_authorization_scope_v1.json")
    request = _load(root / "execution_authorization_request_candidate_contract_v1.json")
    grant = _load(root / "execution_grant_candidate_contract_v1.json")
    window = _load(root / "execution_window_candidate_contract_v1.json")
    allowed = _load(root / "allowed_real_dependency_check_plan_v1.json")
    forbidden = _load(root / "forbidden_execution_action_plan_v1.json")
    evidence = _load(root / "evidence_collection_plan_v1.json")
    rollback = _load(root / "rollback_and_failure_route_plan_v1.json")
    val_gate = _load(root / "validation_gate_execution_path_plan_v1.json")
    provider_nf = _load(root / "provider_selection_non_finalize_plan_v1.json")
    sm_machine = _load(root / "execution_authorization_state_machine_v1.json")
    blocked = _load(root / "execution_authorization_blocked_path_matrix_v1.json")
    dryrun = _load(root / "execution_authorization_dryrun_plan_v1.json")
    decision = _load(root / "execution_authorization_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("ocr_real_dependency_execution_authorization_planning_only") is True)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.state", summary.get("current_state") == "planning_defined")

    ok("policy.scope", policy.get("scope") == SCOPE)
    ok("roadmap_in.pass", roadmap_in.get("review_pass") is True)
    ok("domain_in.pass", domain_in.get("review_pass") is True)
    ok("val_in.pass", val_in.get("review_pass") is True)

    ok("scope.checks8", len(scope.get("allowed_checks_in_scope") or []) == 8)
    for cid in SCOPE_ALLOWED_CHECKS:
        ok(f"scope.allowed.{cid}", cid in (scope.get("allowed_checks_in_scope") or []))
    for nc in SCOPE_NOT_COVERED:
        ok(f"scope.not_covered.{nc[:20]}", nc in (scope.get("not_covered_in_this_phase") or []))

    ok("request.type", request.get("request_type") == "ocr_real_dependency_execution_authorization_request")
    ok("request.target", request.get("authorization_target") == "real_dependency_check_execution")
    ok("request.std", request.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    for key in REQUEST_REQUIRED:
        ok(f"request.field.{key}", key in request)
    ok("request.candidate_only", request.get("candidate_only") is True)
    ok("request.not_generated", request.get("request_generated_now") is False)

    for key in GRANT_REQUIRED:
        ok(f"grant.field.{key}", key in grant)
    ok("grant.scope", grant.get("grant_scope") == "real_dependency_check_execution_only")
    ok("grant.not_issued", grant.get("grant_issued_now") is False)

    for key in WINDOW_REQUIRED:
        ok(f"window.field.{key}", key in window)
    ok("window.not_open", window.get("execution_window_opened_now") is False)

    ok("allowed.count8", allowed.get("check_count") == 8)
    for item in allowed.get("checks") or []:
        cid = item.get("check_id")
        ok(f"allowed.item.{cid}", cid in SCOPE_ALLOWED_CHECKS)
        for k in CHECK_ITEM_KEYS:
            ok(f"allowed.{cid}.{k}", k in item)
        ok(f"allowed.{cid}.not_executed", item.get("current_executed_now") is False)

    ok("forbidden.count15", forbidden.get("forbidden_count") == 15)
    for action in FORBIDDEN_EXECUTION_ACTIONS:
        ok(f"forbidden.{action}", action in (forbidden.get("forbidden_actions") or []))

    for artifact in EVIDENCE_ARTIFACTS:
        ok(f"evidence.{artifact}", artifact in (evidence.get("collect_on_future_execution") or []))

    ok("rollback.no_install_on_fail", rollback.get("failed_package_check_does_not_trigger_install") is True)
    ok("rollback.no_download", rollback.get("missing_model_file_does_not_trigger_download") is True)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)

    ok("val_gate.path_count", len(val_gate.get("path_mappings") or []) == len(VALIDATION_GATE_PATH))
    ok("val_gate.no_runtime", val_gate.get("validator_runtime_enabled_now") is False)
    ok("val_gate.no_exec", val_gate.get("no_gate_executed_now") is True)

    ok("provider.null", provider_nf.get("selected_provider_for_execution") is None)
    ok("provider.no_finalize", provider_nf.get("provider_selection_finalized_now") is False)

    ok("sm.current", sm_machine.get("current_state") == "planning_defined")
    for st in STATE_MACHINE_STATES:
        ok(f"sm.state.{st}", st in (sm_machine.get("states") or []))

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count24", blocked.get("blocked_count") == 24)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", bp in blocked_ids)

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.pass", decision.get("planning_pass") is True)

    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("non_claims", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

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
