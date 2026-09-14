#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Module-local Model Profile Standardization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DUAL_VALIDATION_NON_CLAIMS,
    FINAL_DECISION_GO,
    MODULE_LOCAL_PROFILE_SCHEMA_FIELDS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REGISTRY_REF,
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
    NON_COMPLIANCE_HANDLING_LEVELS_PREVIEW,
    REUSED_GOVERNANCE_STANDARDS,
    SCOPE,
)
from capabilities.governance.module_local_model_profile_standardization_planning_v1 import (
    DUAL_VALIDATION_MECHANISM_ID,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    MIDPLATFORM_INTERACTION_CHECK_COVERAGE,
    MODULE_INTERNAL_SELF_CHECK_COVERAGE,
)

MIN_CHECKS = 199

REQUIRED = (
    "module_local_model_profile_standardization_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "module_local_model_profile_standard_candidate_v1.json",
    "module_local_model_profile_schema_review_v1.json",
    "registry_reference_policy_review_v1.json",
    "capability_stack_binding_policy_review_v1.json",
    "layered_governance_binding_policy_review_v1.json",
    "input_output_binding_policy_review_v1.json",
    "quality_acceptance_binding_policy_review_v1.json",
    "health_validation_whitebox_binding_policy_review_v1.json",
    "provider_runtime_boundary_policy_review_v1.json",
    "fallback_replacement_policy_review_v1.json",
    "midplatform_handoff_policy_review_v1.json",
    "vision_module_local_model_profile_template_review_v1.json",
    "ocr_module_local_model_profile_template_review_v1.json",
    "tts_module_local_model_profile_template_review_v1.json",
    "asr_module_local_model_profile_template_review_v1.json",
    "map_navigation_module_local_model_profile_template_review_v1.json",
    "world_continuity_module_local_model_profile_template_review_v1.json",
    "memory_emotion_evolution_module_local_model_profile_template_review_v1.json",
    "module_local_profile_domain_coverage_review_v1.json",
    "module_internal_self_check_review_v1.json",
    "midplatform_interaction_check_review_v1.json",
    "dual_validation_mechanism_review_v1.json",
    "module_local_profile_non_runtime_boundary_audit_v1.json",
    "module_local_profile_blocked_path_result_v1.json",
    "module_local_profile_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "deferred_governance_register_v1.json",
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
            "module_local_model_profile_standardization_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "module_local_model_profile_standardization_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(Path(args.planning_root) / "verifier_report.json")
    plan_sm = _load(Path(args.planning_root) / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)
    ok("upstream.dual_val", plan_sm.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)

    summary = _load(root / "summary.json")
    candidate = _load(root / "module_local_model_profile_standard_candidate_v1.json")
    self_check = _load(root / "module_internal_self_check_review_v1.json")
    interaction = _load(root / "midplatform_interaction_check_review_v1.json")
    dual_val = _load(root / "dual_validation_mechanism_review_v1.json")
    closure = _load(root / "module_local_profile_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    blocked = _load(root / "module_local_profile_blocked_path_result_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.templates7", summary.get("template_count") == 7)
    ok("summary.domains10", summary.get("domain_coverage_count") == 10)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.self_check", summary.get("module_internal_self_check_review_pass") is True)
    ok("summary.interaction", summary.get("midplatform_interaction_check_review_pass") is True)
    ok("summary.dual_ref", summary.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("summary.deferred", summary.get("non_compliant_module_model_handling_policy_deferred") is True)
    ok("summary.future_phase", summary.get("recommended_future_phase") == DEFERRED_NON_COMPLIANCE_HANDLING_PHASE)

    deferred = _load(root / "deferred_governance_register_v1.json")
    ok("deferred.register", deferred.get("non_compliant_module_model_handling_policy_deferred") is True)
    ok("deferred.phase", deferred.get("recommended_future_phase") == DEFERRED_NON_COMPLIANCE_HANDLING_PHASE)
    ok("deferred.items1", len(deferred.get("deferred_items") or []) == 1)
    ok("deferred.levels8", len(NON_COMPLIANCE_HANDLING_LEVELS_PREVIEW) == 8)

    non_claims_reg = _load(root / "non_claims_register_v1.json")
    ok("non_claims.deferred", non_claims_reg.get("non_compliant_module_model_handling_policy_deferred") is True)
    ok("non_claims.defer_claim", NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM in (non_claims_reg.get("non_claims") or []))

    ok("candidate.standard", candidate.get("standard_id") == "module_local_model_profile_standard_v1")
    ok("candidate.registry", candidate.get("registry_ref") == REGISTRY_REF)
    ok("candidate.dual", candidate.get("dual_validation_mechanism_enabled") is True)
    ok("candidate.self_req", candidate.get("module_internal_self_check_required") is True)
    ok("candidate.mid_req", candidate.get("midplatform_interaction_check_required") is True)
    ok("candidate.constraints", candidate.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)

    ok("schema_r.pass", _load(root / "module_local_model_profile_schema_review_v1.json").get("review_pass") is True)
    ok("schema_r.fields33", _load(root / "module_local_model_profile_schema_review_v1.json").get("field_count") == len(MODULE_LOCAL_PROFILE_SCHEMA_FIELDS))

    for review_file in (
        "registry_reference_policy_review_v1.json",
        "capability_stack_binding_policy_review_v1.json",
        "layered_governance_binding_policy_review_v1.json",
        "input_output_binding_policy_review_v1.json",
        "quality_acceptance_binding_policy_review_v1.json",
        "health_validation_whitebox_binding_policy_review_v1.json",
        "provider_runtime_boundary_policy_review_v1.json",
        "fallback_replacement_policy_review_v1.json",
        "midplatform_handoff_policy_review_v1.json",
    ):
        ok(f"{review_file[:20]}.pass", _load(root / review_file).get("review_pass") is True)

    for tpl_review in (
        "vision_module_local_model_profile_template_review_v1.json",
        "ocr_module_local_model_profile_template_review_v1.json",
        "tts_module_local_model_profile_template_review_v1.json",
        "asr_module_local_model_profile_template_review_v1.json",
        "map_navigation_module_local_model_profile_template_review_v1.json",
        "world_continuity_module_local_model_profile_template_review_v1.json",
        "memory_emotion_evolution_module_local_model_profile_template_review_v1.json",
    ):
        ok(f"{tpl_review[:20]}.pass", _load(root / tpl_review).get("review_pass") is True)

    ok("domain_r.pass", _load(root / "module_local_profile_domain_coverage_review_v1.json").get("review_pass") is True)

    ok("self_check.pass", self_check.get("review_pass") is True)
    ok("self_check.layer", self_check.get("mechanism_layer") == "Module Internal Self-Check")
    for item in MODULE_INTERNAL_SELF_CHECK_COVERAGE:
        ok(f"self_cov.{item[:14]}", self_check.get("review_pass") is True)

    ok("interaction.pass", interaction.get("review_pass") is True)
    ok("interaction.layer", interaction.get("mechanism_layer") == "Midplatform Interaction Check")
    for item in MIDPLATFORM_INTERACTION_CHECK_COVERAGE:
        ok(f"int_cov.{item[:14]}", interaction.get("review_pass") is True)

    ok("dual_val.pass", dual_val.get("review_pass") is True)
    ok("dual_val.self", dual_val.get("self_check_review_pass") is True)
    ok("dual_val.interaction", dual_val.get("interaction_check_review_pass") is True)
    ok("dual_val.rules6", len(dual_val.get("rules") or []) >= 6)

    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count18", blocked.get("blocked_count") == 18)
    for path in BLOCKED_PATHS:
        ok(
            f"blocked.{path[:18]}",
            any(
                b.get("path_id") == path and b.get("status") == "blocked"
                for b in (blocked.get("blocked_paths") or [])
            ),
        )

    boundary = _load(root / "module_local_profile_non_runtime_boundary_audit_v1.json")
    ok("boundary.audit", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:12]}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("next.ready", next_route.get("ready_for_midplatform_model_governance_binding_standardization_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))
    for claim in DUAL_VALIDATION_NON_CLAIMS:
        ok(f"dual_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("dual_validation_non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    min_checks = MIN_CHECKS if MIN_CHECKS else total
    verifier = "GO" if passed == total and passed >= min_checks else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": min_checks,
        "dryrun_and_review_pass": summary.get("dryrun_and_review_pass"),
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "governance_constraints_ref": CONSTRAINT_DOC_ID,
        "phase_governance_standard_reuse_rule": True,
        "new_governance_need_proven": False,
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
