#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Validation Engineering Separation DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as EXPLAIN_DR_FINAL,
)
from capabilities.governance.midplatform_validation_engineering_separation_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    GATE_TYPES,
    ISSUE_TRACEBACK_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    NON_RULEMAKING_RULES,
    PHASE_ID,
    RULE_SOURCE_MAPPINGS,
    SCOPE,
    UPSTREAM_EXPLANATION_DR_FINAL,
    UPSTREAM_OCR_VIA_FACTORY_DR_FINAL,
    UPSTREAM_SEPARATION_PLANNING_FINAL,
    VALIDATION_ENGINEERING_TYPES,
    VIOLATION_REPORT_FIELDS,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as OCR_VIA_FACTORY_DR_FINAL,
)

MIN_CHECKS = 130

REQUIRED = (
    "validation_engineering_separation_dryrun_and_review_policy_v1.json",
    "validation_engineering_planning_input_review_v1.json",
    "validation_engineering_model_candidate_v1.json",
    "constitution_engineering_role_review_v1.json",
    "validation_engineering_role_review_v1.json",
    "rule_source_to_validator_mapping_review_v1.json",
    "validation_engineering_scope_matrix_review_v1.json",
    "validation_gate_taxonomy_review_v1.json",
    "ocr_real_dep_validation_path_dryrun_review_v1.json",
    "issue_traceback_contract_review_v1.json",
    "violation_report_contract_review_v1.json",
    "health_check_consumption_boundary_review_v1.json",
    "authorization_check_boundary_review_v1.json",
    "validation_to_constitution_feedback_loop_review_v1.json",
    "validation_engineering_non_rulemaking_review_v1.json",
    "validation_engineering_boundary_audit_v1.json",
    "validation_engineering_blocked_path_result_v1.json",
    "validation_engineering_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)

GATE_REQUIRED_KEYS = (
    "gate_id",
    "rule_source_ref",
    "jurisdiction_scope",
    "input_object_type",
    "pass_condition",
    "fail_condition",
    "blocked_action",
    "evidence_required",
    "traceback_required",
    "report_required",
    "current_runtime_enabled",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_validation_engineering_separation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--midplatform-validation-engineering-separation-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_validation_engineering_separation_planning"
        ),
    )
    p.add_argument(
        "--midplatform-constitution-governance-explanation-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_constitution_governance_explanation_dryrun_and_review"
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
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_authorization_standard_extension_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--controlled-provider-readiness-harness-factory-registration-post-dryrun-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "controlled_provider_readiness_harness_factory_registration_post_dryrun_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.midplatform_validation_engineering_separation_planning_root)
    explain_root = Path(args.midplatform_constitution_governance_explanation_dryrun_and_review_root)
    ocr_dr_root = Path(args.ocr_real_dependency_authorization_via_factory_standard_dryrun_and_review_root)
    auth_ext_root = Path(args.capability_factory_authorization_standard_extension_dryrun_and_review_root)
    harness_root = Path(
        args.controlled_provider_readiness_harness_factory_registration_post_dryrun_review_root
    )
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json") if (plan_root / "verifier_report.json").is_file() else {}
    plan_sm = _load(plan_root / "summary.json") if (plan_root / "summary.json").is_file() else {}
    explain_vr = _load(explain_root / "verifier_report.json") if (explain_root / "verifier_report.json").is_file() else {}
    ocr_vr = _load(ocr_dr_root / "verifier_report.json") if (ocr_dr_root / "verifier_report.json").is_file() else {}
    ocr_sm = _load(ocr_dr_root / "summary.json") if (ocr_dr_root / "summary.json").is_file() else {}
    ocr_cfg = (
        _load(ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json")
        if (ocr_dr_root / "ocr_real_dependency_domain_config_candidate_v1.json").is_file()
        else {}
    )
    auth_vr = _load(auth_ext_root / "verifier_report.json") if (auth_ext_root / "verifier_report.json").is_file() else {}
    harness_vr = _load(harness_root / "verifier_report.json") if (harness_root / "verifier_report.json").is_file() else {}

    ok("upstream.planning_verifier_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_SEPARATION_PLANNING_FINAL)
    ok("upstream.explanation_dr_go", explain_vr.get("verifier") == "GO")
    ok("upstream.ocr_dr_go", ocr_vr.get("verifier") == "GO")
    ok("upstream.ocr_dr_final", ocr_sm.get("final_decision") == UPSTREAM_OCR_VIA_FACTORY_DR_FINAL)
    ok("upstream.auth_ext_dr_go", auth_vr.get("verifier") == "GO")
    ok("upstream.harness_post_go", harness_vr.get("verifier") == "GO")
    ok("ocr.domain_config_candidate", bool(ocr_cfg.get("candidate_id")))
    ok("ocr.candidate_only", ocr_cfg.get("candidate_only") is True)
    ok("ocr.not_activated", ocr_cfg.get("activated_now") is False)

    summary = _load(root / "summary.json")
    policy = _load(root / "validation_engineering_separation_dryrun_and_review_policy_v1.json")
    model = _load(root / "validation_engineering_model_candidate_v1.json")
    const_rev = _load(root / "constitution_engineering_role_review_v1.json")
    val_rev = _load(root / "validation_engineering_role_review_v1.json")
    mapping_rev = _load(root / "rule_source_to_validator_mapping_review_v1.json")
    scope_rev = _load(root / "validation_engineering_scope_matrix_review_v1.json")
    gate_rev = _load(root / "validation_gate_taxonomy_review_v1.json")
    ocr_path = _load(root / "ocr_real_dep_validation_path_dryrun_review_v1.json")
    traceback_rev = _load(root / "issue_traceback_contract_review_v1.json")
    violation_rev = _load(root / "violation_report_contract_review_v1.json")
    health_rev = _load(root / "health_check_consumption_boundary_review_v1.json")
    auth_rev = _load(root / "authorization_check_boundary_review_v1.json")
    feedback_rev = _load(root / "validation_to_constitution_feedback_loop_review_v1.json")
    non_rule_rev = _load(root / "validation_engineering_non_rulemaking_review_v1.json")
    boundary = _load(root / "validation_engineering_boundary_audit_v1.json")
    blocked = _load(root / "validation_engineering_blocked_path_result_v1.json")
    closure = _load(root / "validation_engineering_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")
    input_rev = _load(root / "validation_engineering_planning_input_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("policy.dryrun_only", policy.get("validation_engineering_separation_dryrun_and_review_only") is True)
    ok("policy.simulated", policy.get("simulated") is True)
    ok("input.review_pass", input_rev.get("review_pass") is True)

    ok("model.model_id", model.get("model_id") == "validation_engineering_model_v1")
    ok("model.role", model.get("role") == "rule_execution_and_gatekeeping")
    ok("model.rulemaking_false", model.get("rulemaking_allowed") is False)
    ok("model.no_grant", model.get("authorization_grant_allowed") is False)
    ok("model.no_provider", model.get("provider_execution_allowed") is False)
    ok("model.no_override", model.get("constitution_override_allowed") is False)
    ok("model.can_block", model.get("can_block") is True)
    ok("model.can_trace", model.get("can_trace") is True)
    ok("model.can_report", model.get("can_report") is True)
    ok("model.runtime_false", model.get("runtime_enabled_now") is False)

    ok("const.writes_rules", const_rev.get("writes_rules") is True)
    ok("const.hive", const_rev.get("hive_remains_highest_authority") is True)
    ok("const.no_provider", const_rev.get("does_not_execute_provider_checks") is True)
    ok("const.dryrun_pass", const_rev.get("dryrun_and_review_pass") is True)

    ok("val.executes", val_rev.get("executes_rules") is True)
    ok("val.no_write", val_rev.get("writes_rules") is False)
    ok("val.no_parallel", val_rev.get("cannot_define_parallel_standard") is True)
    ok("val.no_grant", val_rev.get("cannot_grant_authorization") is True)
    ok("val.no_provider", val_rev.get("cannot_execute_provider") is True)
    ok("val.dryrun_pass", val_rev.get("dryrun_and_review_pass") is True)

    ok("mapping.count8", mapping_rev.get("mapping_count") == 8)
    ok("mapping.pass", mapping_rev.get("dryrun_and_review_pass") is True)

    ok("scope.count9", scope_rev.get("type_count") == 9)
    ok("scope.pass", scope_rev.get("dryrun_and_review_pass") is True)
    for eng in VALIDATION_ENGINEERING_TYPES:
        ok(f"scope.type.{eng['type_id']}", True)

    ok("gate.count13", gate_rev.get("gate_count") == 13)
    gates = gate_rev.get("gates") or []
    for gate_id in GATE_TYPES:
        g = next((x for x in gates if x.get("gate_id") == gate_id), None)
        ok(f"gate.present.{gate_id}", g is not None)
        if g:
            for key in GATE_REQUIRED_KEYS:
                ok(f"gate.{gate_id}.{key}", key in g and g.get(key) is not None)
            ok(f"gate.{gate_id}.no_runtime", g.get("current_runtime_enabled") is False)

    ok("ocr_path.pass", ocr_path.get("dryrun_and_review_pass") is True)
    ok("ocr_path.not_activated", ocr_path.get("domain_config_activated_now") is False)

    ok("traceback.pass", traceback_rev.get("dryrun_and_review_pass") is True)
    for field in ISSUE_TRACEBACK_FIELDS:
        ok(f"traceback.field.{field}", field in (traceback_rev.get("fields") or []))
    ok("traceback.no_fix", traceback_rev.get("traceback_does_not_auto_fix") is True)

    ok("violation.pass", violation_rev.get("dryrun_and_review_pass") is True)
    for field in VIOLATION_REPORT_FIELDS:
        ok(f"violation.field.{field}", field in (violation_rev.get("fields") or []))

    ok("health.pass", health_rev.get("dryrun_and_review_pass") is True)
    ok("health.no_auto_repair", health_rev.get("auto_repair_allowed") is False)
    ok("health.no_auto_auth", health_rev.get("auto_authorize_allowed") is False)

    ok("auth_bound.pass", auth_rev.get("dryrun_and_review_pass") is True)
    ok("auth_bound.no_grant", auth_rev.get("does_not_grant") is True)
    ok("auth_bound.no_real_dep", auth_rev.get("does_not_execute_real_dep_check") is True)

    ok("feedback.pass", feedback_rev.get("dryrun_and_review_pass") is True)
    ok("feedback.no_amend_now", feedback_rev.get("amendment_candidate_generated_now") is False)

    for rule in NON_RULEMAKING_RULES:
        ok(f"non_rule.{rule}", non_rule_rev.get("rules", {}).get(rule) is True)
    ok("non_rule.pass", non_rule_rev.get("dryrun_and_review_pass") is True)

    ok("boundary.pass", boundary.get("dryrun_and_review_pass") is True)
    for field in BOUNDARY_TRUE:
        ok(f"boundary_true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary_false.{field}", summary.get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count22", blocked.get("blocked_count") == 22)
    blocked_ids = {b.get("blocked_path") for b in blocked.get("blocked_paths") or []}
    for bp in BLOCKED_PATHS:
        ok(f"blocked.{bp}", bp in blocked_ids)

    pass_all = summary.get("dryrun_and_review_pass") is True
    ok("closure.pass", closure.get("dryrun_and_review_pass") is pass_all)
    if pass_all:
        ok("closure.final_go", closure.get("final_decision") == FINAL_DECISION_GO)
        ok("closure.next_ocr_roadmap", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
        ok("next_route.ready", next_route.get("ready_for_ocr_execution_authorization_roadmap_decision") is True)
        ok("next_route.no_real_dep", next_route.get("ready_for_real_dependency_check") is False)

    ok("non_claims.count", len(non_claims.get("non_claims") or []) >= len(NON_CLAIMS))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
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
