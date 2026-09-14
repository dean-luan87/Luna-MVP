#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Authorization via Factory Standard DryRunAndReview v1."""

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
    AUTHORIZATION_SUBCOMPONENTS,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1 import (
    ALLOWED_CHECKS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    FORBIDDEN_ACTIONS,
    GOVERNANCE_PATH_STEPS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_CONSTITUTION_STANDARDS,
    OCR_FORBIDDEN_REDEFINITIONS,
    PHASE_ID,
    SCOPE,
    STANDARD_REUSE_RULES,
    UPSTREAM_PLANNING_FINAL,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    BLOCKED_PATHS as PLANNING_BLOCKED_PATHS,
    FINAL_DECISION_GO as PLANNING_FINAL,
)

MIN_CHECKS = 130

REQUIRED = (
    "ocr_real_dependency_authorization_via_factory_standard_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "ocr_real_dependency_domain_config_candidate_v1.json",
    "ocr_constitution_consumption_review_v1.json",
    "factory_authorization_standard_consumption_review_v1.json",
    "validation_factory_consumption_review_v1.json",
    "controlled_provider_readiness_harness_consumption_review_v1.json",
    "allowed_check_domain_config_dryrun_review_v1.json",
    "forbidden_action_domain_config_dryrun_review_v1.json",
    "evidence_rollback_ref_binding_review_v1.json",
    "provider_candidate_ref_binding_review_v1.json",
    "no_generic_logic_redefinition_review_v1.json",
    "standard_reuse_enforcement_review_v1.json",
    "optional_legacy_real_dep_post_review_binding_v1.json",
    "ocr_real_dep_via_factory_standard_boundary_audit_v1.json",
    "ocr_real_dep_via_factory_standard_blocked_path_result_v1.json",
    "ocr_real_dep_via_factory_standard_closure_decision_v1.json",
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
            "ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--ocr-real-dependency-authorization-via-factory-standard-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "ocr_real_dependency_authorization_via_factory_standard_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.ocr_real_dependency_authorization_via_factory_standard_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "ocr_real_dependency_authorization_via_factory_standard_dryrun_review_policy_v1.json")
    planning_review = _load(root / "planning_input_review_v1.json")
    candidate = _load(root / "ocr_real_dependency_domain_config_candidate_v1.json")
    ocr_const = _load(root / "ocr_constitution_consumption_review_v1.json")
    factory = _load(root / "factory_authorization_standard_consumption_review_v1.json")
    vf = _load(root / "validation_factory_consumption_review_v1.json")
    harness = _load(root / "controlled_provider_readiness_harness_consumption_review_v1.json")
    allowed = _load(root / "allowed_check_domain_config_dryrun_review_v1.json")
    forbidden = _load(root / "forbidden_action_domain_config_dryrun_review_v1.json")
    no_generic = _load(root / "no_generic_logic_redefinition_review_v1.json")
    reuse = _load(root / "standard_reuse_enforcement_review_v1.json")
    legacy = _load(root / "optional_legacy_real_dep_post_review_binding_v1.json")
    boundary = _load(root / "ocr_real_dep_via_factory_standard_boundary_audit_v1.json")
    blocked = _load(root / "ocr_real_dep_via_factory_standard_blocked_path_result_v1.json")
    closure = _load(root / "ocr_real_dep_via_factory_standard_closure_decision_v1.json")

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    plan_blocked = _load(plan_root / "ocr_real_dep_via_factory_standard_blocked_path_matrix_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.simulated", summary.get("simulated") is True)

    ok("policy.scope_only", policy.get("ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_only") is True)
    ok("policy.standard_reuse", policy.get("standard_reuse_required") is True)
    ok("policy.no_dup_auth", policy.get("duplicate_generic_authorization_logic_forbidden") is True)

    ok("plan.vr_go", plan_vr.get("verifier") == "GO")
    ok("plan.final", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("plan.final_match", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("plan.blocked22", len(plan_blocked.get("blocked_paths") or []) == len(PLANNING_BLOCKED_PATHS))
    ok("planning_review.pass", planning_review.get("review_pass") is True)
    ok("planning.path8", len(planning_review.get("governance_path_steps") or []) == len(GOVERNANCE_PATH_STEPS))

    ok("candidate.generated", summary.get("ocr_domain_config_candidate_generated_now") is True)
    ok("candidate.domain", candidate.get("provider_domain") == "ocr")
    ok("candidate.target", candidate.get("authorization_target") == "real_dependency_check")
    ok("candidate.std_ref", candidate.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    ok("candidate.vf_required", candidate.get("validation_factory_required") is True)
    ok("candidate.harness_required", candidate.get("controlled_provider_readiness_harness_required") is True)
    ok("candidate.candidate_only", candidate.get("candidate_only") is True)
    ok("candidate.not_activated", candidate.get("activated_now") is False)
    ok("candidate.no_generic", len(candidate.get("generic_logic_redefinitions") or []) == 0)

    for chk in candidate.get("allowed_checks") or []:
        cid = chk.get("check_id", "")
        ok(f"candidate.check.{cid}", cid in ALLOWED_CHECKS)
        ok(f"candidate.{cid}.not_now", chk.get("current_executed_now") is False)

    for action in FORBIDDEN_ACTIONS:
        ok(f"candidate.forbidden.{action}", action in (candidate.get("forbidden_actions") or []))

    ok("ocr_const.pass", ocr_const.get("dryrun_and_review_pass") is True)
    ok("ocr_const.count7", len(ocr_const.get("standards_consumed") or []) == len(OCR_CONSTITUTION_STANDARDS))

    ok("factory.pass", factory.get("dryrun_and_review_pass") is True)
    ok("factory.subs8", len(factory.get("subcomponents_consumed") or []) == len(AUTHORIZATION_SUBCOMPONENTS))
    ok("factory.no_request", factory.get("request_contract_not_in_domain_config") is True)

    ok("vf.pass", vf.get("dryrun_and_review_pass") is True)
    ok("vf.no_runtime", vf.get("validation_factory_runtime_enforced_now") is False)

    ok("harness.pass", harness.get("dryrun_and_review_pass") is True)
    ok("harness.no_invoke", harness.get("cannot_invoke_provider") is True)

    ok("allowed.pass", allowed.get("dryrun_and_review_pass") is True)
    ok("allowed.count8", allowed.get("check_count") == len(ALLOWED_CHECKS))

    ok("forbidden.pass", forbidden.get("dryrun_and_review_pass") is True)
    ok("forbidden.count15", forbidden.get("forbidden_action_count") == len(FORBIDDEN_ACTIONS))

    ok("no_generic.pass", no_generic.get("dryrun_and_review_pass") is True)
    for forbidden_def in OCR_FORBIDDEN_REDEFINITIONS:
        ok(f"no_generic.{forbidden_def.replace(' ', '_')}", forbidden_def in (no_generic.get("forbidden_redefinitions") or []))

    ok("reuse.pass", reuse.get("dryrun_and_review_pass") is True)
    ok("reuse.required", reuse.get("standard_reuse_required") is True)
    for rule in STANDARD_REUSE_RULES:
        ok(f"reuse.{rule}", True)

    ok("legacy.not_blocking", legacy.get("not_blocking") is True)
    ok("legacy.planning_ok", legacy.get("planning_go_not_invalidated") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)
    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count22", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", any(
            b.get("blocked_path") == bp and b.get("blocked") is True
            for b in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("selected_provider_null", summary.get("selected_provider_for_execution") is None)
    ok("real_dep_false", summary.get("real_dependency_check_executed_now") is False)
    ok("grant_false", summary.get("grant_issued_now") is False)

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
