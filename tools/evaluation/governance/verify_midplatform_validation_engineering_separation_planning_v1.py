#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Validation Engineering Separation Planning v1."""

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
from capabilities.governance.midplatform_validation_engineering_separation_planning_v1 import (
    CONSTITUTION_ENGINEERING_RESPONSIBILITIES,
    GATE_TYPES,
    ISSUE_TRACEBACK_FIELDS,
    NON_CLAIMS,
    NON_RULEMAKING_RULES,
    PHASE_ID,
    RULE_SOURCE_MAPPINGS,
    SCOPE,
    UPSTREAM_AUTH_EXT_DR_FINAL,
    UPSTREAM_EXPLANATION_DR_FINAL,
    UPSTREAM_OCR_VIA_FACTORY_PLANNING_FINAL,
    VALIDATION_ENGINEERING_RESPONSIBILITIES,
    VALIDATION_ENGINEERING_TYPES,
    VIOLATION_REPORT_FIELDS,
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    ALLOWED_CHECKS,
    FINAL_DECISION_GO as OCR_VIA_FACTORY_PLANNING_FINAL,
    FORBIDDEN_ACTIONS,
)

MIN_CHECKS = 100

REQUIRED = (
    "validation_engineering_separation_planning_policy_v1.json",
    "upstream_constitution_and_factory_input_review_v1.json",
    "constitution_engineering_role_definition_v1.json",
    "validation_engineering_role_definition_v1.json",
    "rule_source_to_validator_mapping_v1.json",
    "validation_engineering_scope_matrix_v1.json",
    "validation_gate_taxonomy_v1.json",
    "validation_issue_traceback_contract_v1.json",
    "validation_violation_report_contract_v1.json",
    "validation_health_check_boundary_plan_v1.json",
    "validation_authorization_check_boundary_plan_v1.json",
    "validation_to_constitution_feedback_loop_plan_v1.json",
    "validation_engineering_non_rulemaking_policy_v1.json",
    "ocr_real_dep_validation_engineering_mapping_v1.json",
    "validation_engineering_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "validation_engineering_separation_planning_decision_v1.json",
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
        "--capability-factory-authorization-standard-extension-dryrun-and-review-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "capability_factory_authorization_standard_extension_dryrun_and_review"
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
    explain_root = Path(args.midplatform_constitution_governance_explanation_dryrun_and_review_root)
    auth_ext_root = Path(args.capability_factory_authorization_standard_extension_dryrun_and_review_root)
    ocr_root = Path(args.ocr_real_dependency_authorization_via_factory_standard_planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "validation_engineering_separation_planning_policy_v1.json")
    upstream = _load(root / "upstream_constitution_and_factory_input_review_v1.json")
    const_eng = _load(root / "constitution_engineering_role_definition_v1.json")
    val_eng = _load(root / "validation_engineering_role_definition_v1.json")
    mapping = _load(root / "rule_source_to_validator_mapping_v1.json")
    scope_matrix = _load(root / "validation_engineering_scope_matrix_v1.json")
    gates = _load(root / "validation_gate_taxonomy_v1.json")
    traceback = _load(root / "validation_issue_traceback_contract_v1.json")
    violation = _load(root / "validation_violation_report_contract_v1.json")
    health = _load(root / "validation_health_check_boundary_plan_v1.json")
    auth_bound = _load(root / "validation_authorization_check_boundary_plan_v1.json")
    feedback = _load(root / "validation_to_constitution_feedback_loop_plan_v1.json")
    non_rule = _load(root / "validation_engineering_non_rulemaking_policy_v1.json")
    ocr_map = _load(root / "ocr_real_dep_validation_engineering_mapping_v1.json")
    dryrun = _load(root / "validation_engineering_dryrun_plan_v1.json")
    decision = _load(root / "validation_engineering_separation_planning_decision_v1.json")

    explain_vr = _load(explain_root / "verifier_report.json")
    explain_sm = _load(explain_root / "summary.json")
    auth_ext_vr = _load(auth_ext_root / "verifier_report.json")
    auth_ext_sm = _load(auth_ext_root / "summary.json")
    ocr_vr = _load(ocr_root / "verifier_report.json")
    ocr_sm = _load(ocr_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("policy.scope_only", policy.get("validation_engineering_separation_planning_only") is True)

    ok("explain.vr_go", explain_vr.get("verifier") == "GO")
    ok("explain.final", explain_sm.get("final_decision") == EXPLAIN_DR_FINAL)
    ok("explain.final_match", explain_sm.get("final_decision") == UPSTREAM_EXPLANATION_DR_FINAL)
    ok("auth_ext.vr_go", auth_ext_vr.get("verifier") == "GO")
    ok("auth_ext.final", auth_ext_sm.get("final_decision") == AUTH_EXT_DR_FINAL)
    ok("auth_ext.final_match", auth_ext_sm.get("final_decision") == UPSTREAM_AUTH_EXT_DR_FINAL)
    ok("ocr.vr_go", ocr_vr.get("verifier") == "GO")
    ok("ocr.final", ocr_sm.get("final_decision") == OCR_VIA_FACTORY_PLANNING_FINAL)
    ok("ocr.final_match", ocr_sm.get("final_decision") == UPSTREAM_OCR_VIA_FACTORY_PLANNING_FINAL)
    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.vf_compliance", upstream.get("validation_factory_compliance_layer") is True)

    ok("const.writes_rules", const_eng.get("writes_rules") is True)
    ok("const.owns_hierarchy", const_eng.get("owns_rule_hierarchy") is True)
    ok("const.no_runtime_checks", const_eng.get("executes_provider_runtime_checks") is False)
    ok("const.hive", const_eng.get("hive_highest_authority_for_general_constitution") is True)
    ok("const.resp10", len(const_eng.get("responsibilities") or []) == len(CONSTITUTION_ENGINEERING_RESPONSIBILITIES))

    ok("val.executes_rules", val_eng.get("executes_rules") is True)
    ok("val.no_write_constitution", val_eng.get("writes_general_constitution") is False)
    ok("val.no_parallel_std", val_eng.get("defines_parallel_domain_standard") is False)
    ok("val.no_override", val_eng.get("cannot_override_constitution") is True)
    ok("val.no_grant", val_eng.get("cannot_grant_authorization_by_itself") is True)
    ok("val.resp9", len(val_eng.get("responsibilities") or []) == len(VALIDATION_ENGINEERING_RESPONSIBILITIES))

    ok("mapping.count8", len(mapping.get("mappings") or []) == len(RULE_SOURCE_MAPPINGS))
    ok("mapping.constitution_source", mapping.get("validation_engineering_rule_sources_only_from_constitution_layer") is True)

    ok("scope.types9", scope_matrix.get("type_count") == len(VALIDATION_ENGINEERING_TYPES))

    ok("gates.count13", gates.get("gate_count") == len(GATE_TYPES))
    for g in gates.get("gates") or []:
        ok(f"gate.{g.get('gate_id')}.no_runtime", g.get("current_runtime_enabled") is False)

    ok("traceback.fields16", len(traceback.get("fields") or []) == len(ISSUE_TRACEBACK_FIELDS))
    ok("traceback.no_fix", traceback.get("traceback_does_not_auto_fix") is True)

    ok("violation.fields16", len(violation.get("fields") or []) == len(VIOLATION_REPORT_FIELDS))

    ok("health.no_score", health.get("no_numeric_health_score_invented") is True)
    ok("health.no_auto_repair", health.get("cannot_auto_repair") is True)

    ok("auth_bound.no_grant", auth_bound.get("does_not_grant") is True)
    ok("auth_bound.no_exec", auth_bound.get("does_not_execute_check") is True)
    ok("auth_bound.domain_config", auth_bound.get("ocr_submits_domain_config_only") is True)

    ok("feedback.no_amend", feedback.get("amendment_candidate_generated_now") is False)
    ok("feedback.no_hive", feedback.get("hive_review_submitted_now") is False)

    for rule in NON_RULEMAKING_RULES:
        ok(f"non_rule.{rule}", non_rule.get("rules", {}).get(rule) is True)

    ok("ocr_map.domain_config", ocr_map.get("ocr_domain_config_only") is True)
    ok("ocr_map.checks8", len(ocr_map.get("allowed_checks_from_planning") or []) == len(ALLOWED_CHECKS))
    ok("ocr_map.forbidden15", len(ocr_map.get("forbidden_actions_from_planning") or []) == len(FORBIDDEN_ACTIONS))

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("decision.separated", decision.get("legislation_vs_enforcement_separated") is True)

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
