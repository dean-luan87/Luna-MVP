#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Capability Factory Authorization Standard Extension DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_admission_and_operation_standard_planning_v1 import (
    STANDARD_ID as FACTORY_STANDARD_ID,
)
from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    AUTHORIZATION_STANDARD_ID,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_DOMAIN_CONFIG_FIELDS,
    OCR_FORBIDDEN_REDEFINITIONS,
    PHASE_ID,
    PLANNING_DRYRUN_NEVER_AUTO_TRIGGER,
    SCOPE,
    TEN_STANDARDS,
    UPSTREAM_AUTH_EXT_PLANNING_FINAL,
    UPSTREAM_HIERARCHY_DR_FINAL,
)
from capabilities.governance.capability_factory_authorization_standard_extension_planning_v1 import (
    AUTHORIZATION_SUBCOMPONENTS,
    FINAL_DECISION_GO as AUTH_EXT_PLANNING_FINAL,
)
from capabilities.governance.midplatform_constitution_governance_hierarchy_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as HIERARCHY_DR_FINAL,
    OCR_REAL_DEP_AUTHORIZATION_CHAIN,
)

MIN_CHECKS = 130

REQUIRED = (
    "factory_authorization_standard_extension_dryrun_and_review_policy_v1.json",
    "authorization_standard_extension_planning_input_review_v1.json",
    "constitution_hierarchy_input_review_v1.json",
    "authorization_standard_extension_candidate_v1.json",
    "authorization_scope_standard_review_v1.json",
    "request_grant_execution_window_standard_review_v1.json",
    "allowed_forbidden_action_matrix_standard_review_v1.json",
    "owner_operator_approval_standard_review_v1.json",
    "post_execution_review_standard_review_v1.json",
    "revocation_rollback_standard_review_v1.json",
    "ocr_real_dep_domain_config_consumption_review_v1.json",
    "factory_standard_ten_category_integration_review_v1.json",
    "constitution_mapping_review_v1.json",
    "authorization_standard_boundary_audit_v1.json",
    "authorization_standard_blocked_path_result_v1.json",
    "authorization_standard_extension_closure_decision_v1.json",
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
            "capability_factory_authorization_standard_extension_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--capability-factory-authorization-standard-extension-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_authorization_standard_extension_planning"
        ),
    )
    p.add_argument(
        "--midplatform-constitution-governance-hierarchy-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_constitution_governance_hierarchy_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    auth_ext_root = Path(args.capability_factory_authorization_standard_extension_planning_root)
    hierarchy_root = Path(args.midplatform_constitution_governance_hierarchy_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "factory_authorization_standard_extension_dryrun_and_review_policy_v1.json")
    planning_review = _load(root / "authorization_standard_extension_planning_input_review_v1.json")
    hierarchy_review = _load(root / "constitution_hierarchy_input_review_v1.json")
    candidate = _load(root / "authorization_standard_extension_candidate_v1.json")
    scope = _load(root / "authorization_scope_standard_review_v1.json")
    rgw = _load(root / "request_grant_execution_window_standard_review_v1.json")
    matrix = _load(root / "allowed_forbidden_action_matrix_standard_review_v1.json")
    approval = _load(root / "owner_operator_approval_standard_review_v1.json")
    post = _load(root / "post_execution_review_standard_review_v1.json")
    rollback = _load(root / "revocation_rollback_standard_review_v1.json")
    ocr_consume = _load(root / "ocr_real_dep_domain_config_consumption_review_v1.json")
    ten_cat = _load(root / "factory_standard_ten_category_integration_review_v1.json")
    constitution = _load(root / "constitution_mapping_review_v1.json")
    boundary = _load(root / "authorization_standard_boundary_audit_v1.json")
    blocked = _load(root / "authorization_standard_blocked_path_result_v1.json")
    closure = _load(root / "authorization_standard_extension_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    auth_ext_vr = _load(auth_ext_root / "verifier_report.json")
    auth_ext_sm = _load(auth_ext_root / "summary.json")
    hierarchy_vr = _load(hierarchy_root / "verifier_report.json")
    hierarchy_sm = _load(hierarchy_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.simulated", summary.get("simulated") is True)

    ok("policy.scope_only", policy.get("factory_authorization_standard_extension_dryrun_and_review_only") is True)
    ok("policy.phase", policy.get("phase") == PHASE_ID)

    ok("auth_ext.vr_go", auth_ext_vr.get("verifier") == "GO")
    ok("auth_ext.final", auth_ext_sm.get("final_decision") == AUTH_EXT_PLANNING_FINAL)
    ok("auth_ext.final_match", auth_ext_sm.get("final_decision") == UPSTREAM_AUTH_EXT_PLANNING_FINAL)
    ok("planning_review.pass", planning_review.get("review_pass") is True)

    ok("hierarchy.vr_go", hierarchy_vr.get("verifier") == "GO")
    ok("hierarchy.final", hierarchy_sm.get("final_decision") == HIERARCHY_DR_FINAL)
    ok("hierarchy.final_match", hierarchy_sm.get("final_decision") == UPSTREAM_HIERARCHY_DR_FINAL)
    ok("hierarchy_review.pass", hierarchy_review.get("review_pass") is True)

    ok("candidate.std", candidate.get("standard_id") == AUTHORIZATION_STANDARD_ID)
    ok("candidate.parent", candidate.get("parent_standard") == FACTORY_STANDARD_ID)
    ok("candidate.index10", candidate.get("category_index") == 10)
    ok("candidate.mapped", candidate.get("mapped_to") == "Factory Governance Constitution")
    ok("candidate.domain_config", candidate.get("domain_config_required") is True)
    ok("candidate.no_redefine", candidate.get("domain_logic_redefinition_forbidden") is True)
    ok("candidate.runtime_false", candidate.get("runtime_enforced_now") is False)
    ok("candidate.subs8", candidate.get("subcomponent_count") == len(AUTHORIZATION_SUBCOMPONENTS))
    for sub in AUTHORIZATION_SUBCOMPONENTS:
        ok(f"candidate.sub.{sub}", sub in (candidate.get("subcomponents") or []))

    ok("scope.pass", scope.get("dryrun_and_review_pass") is True)
    ok("scope.required", scope.get("scope_required") is True)
    ok("scope.target", scope.get("target_scope_required") is True)
    ok("scope.out", scope.get("out_of_scope_required") is True)
    ok("scope.no_prod", scope.get("production_runtime_excluded_by_default") is True)
    ok("scope.no_user_output", scope.get("user_output_excluded_by_default") is True)
    ok("scope.no_fact", scope.get("fact_write_excluded_by_default") is True)
    ok("scope.no_memory", scope.get("memory_worldmodel_write_excluded_by_default") is True)
    ok("scope.domain_config", scope.get("domain_config_may_define_allowed_scope") is True)

    ok("rgw.pass", rgw.get("dryrun_and_review_pass") is True)
    ok("rgw.request_req", rgw.get("request_contract_required") is True)
    ok("rgw.grant_req", rgw.get("grant_contract_required") is True)
    ok("rgw.window_req", rgw.get("execution_window_contract_required") is True)
    ok("rgw.req_ne_grant", rgw.get("request_not_equal_grant") is True)
    ok("rgw.grant_ne_window", rgw.get("grant_not_equal_execution_window_open") is True)
    ok("rgw.window_ne_invoke", rgw.get("execution_window_open_not_equal_provider_invocation") is True)
    ok("rgw.no_request", rgw.get("request_generated_now") is False)
    ok("rgw.no_grant", rgw.get("grant_issued_now") is False)
    ok("rgw.no_window", rgw.get("execution_window_opened_now") is False)

    ok("matrix.pass", matrix.get("dryrun_and_review_pass") is True)
    ok("matrix.allowed_req", matrix.get("allowed_action_matrix_required") is True)
    ok("matrix.forbidden_req", matrix.get("forbidden_action_matrix_required") is True)
    ok("matrix.later_only", matrix.get("allowed_actions_are_later_only") is True)
    ok("matrix.forbidden_override", matrix.get("forbidden_actions_override_domain_config") is True)
    ok("matrix.no_trigger", matrix.get("planning_dryrun_cannot_trigger_actions") is True)
    ok("matrix.no_executed", matrix.get("all_current_executed_now") is False)

    ok("approval.pass", approval.get("dryrun_and_review_pass") is True)
    ok("approval.later", approval.get("approval_required_later") is True)
    ok("approval.scope", approval.get("approval_scope_defined") is True)
    ok("approval.not_now", approval.get("approval_collected_now") is False)
    ok("approval.not_grant", approval.get("approval_does_not_imply_grant") is True)
    ok("approval.not_window", approval.get("approval_does_not_open_execution_window") is True)

    ok("post.pass", post.get("dryrun_and_review_pass") is True)
    ok("post.required", post.get("post_execution_review_required") is True)
    ok("post.evidence", post.get("evidence_package_required") is True)
    ok("post.boundary", post.get("boundary_audit_required") is True)
    ok("post.verifier", post.get("verifier_required") is True)
    ok("post.closure", post.get("closure_decision_required") is True)
    ok("post.no_exec_without", post.get("execution_without_review_forbidden") is True)

    ok("rollback.pass", rollback.get("dryrun_and_review_pass") is True)
    ok("rollback.revocation", rollback.get("revocation_conditions_required") is True)
    ok("rollback.before_exec", rollback.get("rollback_required_before_execution") is True)
    ok("rollback.no_repair", rollback.get("failed_check_does_not_trigger_repair") is True)
    ok("rollback.no_install", rollback.get("failed_check_does_not_trigger_install") is True)
    ok("rollback.no_download", rollback.get("failed_check_does_not_trigger_download") is True)
    ok("rollback.not_now", rollback.get("rollback_executed_now") is False)

    ok("ocr.pass", ocr_consume.get("dryrun_and_review_pass") is True)
    ok("ocr.absorbed", ocr_consume.get("ocr_auth_planning_superseded_for_auth_logic_by") == AUTHORIZATION_STANDARD_ID)
    ok("ocr.evidence_preserved", ocr_consume.get("ocr_auth_planning_preserved_as_evidence") is True)
    ok("ocr.no_redefine", ocr_consume.get("domain_logic_redefinition_forbidden") is True)
    ocr_cfg = ocr_consume.get("domain_config") or {}
    ok("ocr.domain", ocr_cfg.get("provider_domain") == "ocr")
    ok("ocr.target", ocr_cfg.get("authorization_target") == "real_dependency_check")
    for field in OCR_DOMAIN_CONFIG_FIELDS:
        ok(f"ocr.config.{field}", field in ocr_cfg)
    for forbidden in OCR_FORBIDDEN_REDEFINITIONS:
        ok(f"ocr.forbidden.{forbidden.replace(' ', '_')}", forbidden in (ocr_consume.get("forbidden_redefinitions") or []))

    ok("ten.pass", ten_cat.get("dryrun_and_review_pass") is True)
    ok("ten.complete", ten_cat.get("ten_standards_complete") is True)
    ok("ten.nine_valid", ten_cat.get("prior_nine_still_valid") is True)
    ok("ten.count10", len(ten_cat.get("ten_standards") or []) == len(TEN_STANDARDS))

    ok("constitution.pass", constitution.get("dryrun_and_review_pass") is True)
    ok("constitution.ocr_path", constitution.get("ocr_real_dep_path") == OCR_REAL_DEP_AUTHORIZATION_CHAIN)
    ok("constitution.vf_no_rules", constitution.get("validation_factory_writes_rules") is False)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    ok("boundary.all_false", boundary.get("all_boundary_false") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field}", summary.get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count18", blocked.get("blocked_count") == len(BLOCKED_PATHS))
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", any(
            b.get("blocked_path") == bp and b.get("blocked") is True
            for b in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.no_high_risk", closure.get("high_risk") is False)

    ok("next_route.ocr_planning", next_route.get("ready_for_ocr_real_dep_via_factory_standard_planning") is True)
    ok("next_route.no_real_dep", next_route.get("ready_for_real_dependency_check") is False)
    ok("next_route.next", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))
    ok("selected_provider_null", summary.get("selected_provider_for_execution") is None)

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
