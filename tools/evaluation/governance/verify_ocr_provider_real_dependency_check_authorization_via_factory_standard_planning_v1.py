#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify OCR Real Dependency Authorization via Factory Standard Planning v1."""

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
from capabilities.governance.capability_factory_authorization_standard_extension_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as AUTH_EXT_DR_FINAL,
)
from capabilities.governance.midplatform_constitution_governance_explanation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as EXPLAIN_DR_FINAL,
)
from capabilities.governance.ocr_provider_real_dependency_check_authorization_via_factory_standard_planning_v1 import (
    ALLOWED_CHECKS,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    FINAL_DECISION_GO,
    FORBIDDEN_ACTIONS,
    GOVERNANCE_PATH_STEPS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OCR_CONSTITUTION_STANDARDS,
    OCR_DOMAIN_CONFIG_ALLOWED_FIELDS,
    OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS,
    PHASE_ID,
    SCOPE,
    STANDARD_REUSE_RULES,
    UPSTREAM_AUTH_EXT_DR_FINAL,
    UPSTREAM_EXPLANATION_DR_FINAL,
)

MIN_CHECKS = 115

REQUIRED = (
    "ocr_real_dependency_authorization_via_factory_standard_planning_policy_v1.json",
    "constitution_explanation_input_review_v1.json",
    "factory_authorization_standard_input_review_v1.json",
    "ocr_real_dependency_authorization_governance_path_v1.json",
    "ocr_real_dependency_domain_config_contract_v1.json",
    "ocr_real_dependency_domain_config_candidate_plan_v1.json",
    "ocr_constitution_binding_plan_v1.json",
    "factory_authorization_standard_binding_plan_v1.json",
    "validation_factory_binding_plan_v1.json",
    "controlled_provider_readiness_harness_binding_plan_v1.json",
    "allowed_check_domain_config_plan_v1.json",
    "forbidden_action_domain_config_plan_v1.json",
    "evidence_and_rollback_ref_binding_plan_v1.json",
    "provider_candidate_ref_binding_plan_v1.json",
    "no_generic_logic_redefinition_policy_v1.json",
    "standard_reuse_enforcement_plan_v1.json",
    "ocr_real_dep_via_factory_standard_blocked_path_matrix_v1.json",
    "ocr_real_dep_via_factory_standard_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "ocr_real_dependency_authorization_via_factory_standard_planning_decision_v1.json",
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
            "ocr_real_dependency_authorization_via_factory_standard_planning"
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
    args = p.parse_args()
    root = Path(args.output_root)
    explain_root = Path(args.midplatform_constitution_governance_explanation_dryrun_and_review_root)
    auth_ext_root = Path(args.capability_factory_authorization_standard_extension_dryrun_and_review_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    summary = _load(root / "summary.json")
    policy = _load(root / "ocr_real_dependency_authorization_via_factory_standard_planning_policy_v1.json")
    explain_review = _load(root / "constitution_explanation_input_review_v1.json")
    factory_review = _load(root / "factory_authorization_standard_input_review_v1.json")
    gov_path = _load(root / "ocr_real_dependency_authorization_governance_path_v1.json")
    contract = _load(root / "ocr_real_dependency_domain_config_contract_v1.json")
    candidate_plan = _load(root / "ocr_real_dependency_domain_config_candidate_plan_v1.json")
    ocr_bind = _load(root / "ocr_constitution_binding_plan_v1.json")
    auth_bind = _load(root / "factory_authorization_standard_binding_plan_v1.json")
    vf_bind = _load(root / "validation_factory_binding_plan_v1.json")
    harness_bind = _load(root / "controlled_provider_readiness_harness_binding_plan_v1.json")
    allowed = _load(root / "allowed_check_domain_config_plan_v1.json")
    forbidden = _load(root / "forbidden_action_domain_config_plan_v1.json")
    no_generic = _load(root / "no_generic_logic_redefinition_policy_v1.json")
    reuse = _load(root / "standard_reuse_enforcement_plan_v1.json")
    blocked = _load(root / "ocr_real_dep_via_factory_standard_blocked_path_matrix_v1.json")
    dryrun = _load(root / "ocr_real_dep_via_factory_standard_dryrun_plan_v1.json")
    decision = _load(
        root / "ocr_real_dependency_authorization_via_factory_standard_planning_decision_v1.json"
    )

    explain_vr = _load(explain_root / "verifier_report.json")
    explain_sm = _load(explain_root / "summary.json")
    auth_ext_vr = _load(auth_ext_root / "verifier_report.json")
    auth_ext_sm = _load(auth_ext_root / "summary.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.boundary_ok", summary.get("boundary_ok") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("policy.scope_only", policy.get("ocr_real_dependency_authorization_via_factory_standard_planning_only") is True)
    ok("policy.standard_reuse", policy.get("standard_reuse_required") is True)

    ok("explain.vr_go", explain_vr.get("verifier") == "GO")
    ok("explain.final", explain_sm.get("final_decision") == EXPLAIN_DR_FINAL)
    ok("explain.final_match", explain_sm.get("final_decision") == UPSTREAM_EXPLANATION_DR_FINAL)
    ok("explain_review.pass", explain_review.get("review_pass") is True)

    ok("auth_ext.vr_go", auth_ext_vr.get("verifier") == "GO")
    ok("auth_ext.final", auth_ext_sm.get("final_decision") == AUTH_EXT_DR_FINAL)
    ok("auth_ext.final_match", auth_ext_sm.get("final_decision") == UPSTREAM_AUTH_EXT_DR_FINAL)
    ok("factory_review.tenth", factory_review.get("tenth_factory_standard") is True)
    ok("factory_review.std", factory_review.get("authorization_standard_id") == AUTHORIZATION_STANDARD_ID)

    ok("gov_path.steps8", len(gov_path.get("steps") or []) == len(GOVERNANCE_PATH_STEPS))
    ok("gov_path.domain_config_only", gov_path.get("ocr_submits_domain_config_only") is True)
    ok("gov_path.factory_owns", gov_path.get("factory_authorization_standard_owns_auth_logic") is True)

    ok("contract.domain", contract.get("provider_domain") == "ocr")
    ok("contract.target", contract.get("authorization_target") == "real_dependency_check")
    ok("contract.std_ref", contract.get("factory_authorization_standard_ref") == AUTHORIZATION_STANDARD_ID)
    ok("contract.vf_required", contract.get("validation_factory_required") is True)
    ok("contract.fields12", len(contract.get("allowed_fields") or []) == len(OCR_DOMAIN_CONFIG_ALLOWED_FIELDS))
    ok("contract.forbidden9", len(contract.get("forbidden_fields") or []) == len(OCR_DOMAIN_CONFIG_FORBIDDEN_FIELDS))

    ok("candidate.not_generated", candidate_plan.get("ocr_domain_config_generated_now") is False)
    ok("candidate.planned_domain", candidate_plan.get("planned_fields", {}).get("provider_domain") == "ocr")

    ok("ocr_bind.standards7", len(ocr_bind.get("standards") or []) == len(OCR_CONSTITUTION_STANDARDS))
    ok("ocr_bind.general", ocr_bind.get("general_constitution_cannot_be_overridden") is True)

    ok("auth_bind.subs8", len(auth_bind.get("subcomponents") or []) == len(AUTHORIZATION_SUBCOMPONENTS))

    ok("vf.no_rules", vf_bind.get("writes_rules") is False)
    ok("vf.before_midplatform", vf_bind.get("validation_pass_required_before_midplatform") is True)
    ok("vf.blocked_now", vf_bind.get("midplatform_consumption_blocked_now") is True)

    ok("harness.readiness", harness_bind.get("checks_readiness_not_grant") is True)
    ok("harness.no_invoke", harness_bind.get("cannot_invoke_provider") is True)
    ok("harness.ocr_first", any(
        c.get("consumer") == "ocr" for c in (harness_bind.get("consumers") or [])
    ))

    ok("allowed.count8", len(allowed.get("checks") or []) == len(ALLOWED_CHECKS))
    for chk in allowed.get("checks") or []:
        ok(f"allowed.{chk.get('check_id')}.not_now", chk.get("current_executed_now") is False)
        ok(f"allowed.{chk.get('check_id')}.auth_std", chk.get("requires_authorization_standard") is True)

    ok("forbidden.count15", len(forbidden.get("forbidden_actions") or []) == len(FORBIDDEN_ACTIONS))

    ok("no_generic.superseded", no_generic.get("superseded_for_auth_logic_by") == AUTHORIZATION_STANDARD_ID)
    ok("no_generic.ocr_only", no_generic.get("ocr_phase_role") == "domain_config only")

    ok("reuse.required", reuse.get("rules", {}).get("standard_reuse_required") is True)
    ok("reuse.no_dup_auth", reuse.get("duplicate_generic_authorization_logic_forbidden") is True)
    for rule in STANDARD_REUSE_RULES:
        ok(f"reuse.{rule}", reuse.get("rules", {}).get(rule) is True)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count22", len(blocked.get("blocked_paths") or []) == len(BLOCKED_PATHS))

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.merged", dryrun.get("dryrun_and_review_merged") is True)

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.domain_config_only", decision.get("ocr_domain_config_only") is True)

    ok("selected_provider_null", summary.get("selected_provider_for_execution") is None)
    ok("real_dep_false", summary.get("real_dependency_check_executed_now") is False)
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
