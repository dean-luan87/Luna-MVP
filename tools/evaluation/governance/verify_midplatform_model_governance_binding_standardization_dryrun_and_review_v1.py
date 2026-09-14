#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Model Governance Binding Standardization DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_model_governance_binding_standardization_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    DUAL_VALIDATION_NON_CLAIMS,
    FINAL_DECISION_GO,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    REGISTRY_REF,
    SCOPE,
    STANDARD_ID,
)
from capabilities.governance.midplatform_model_governance_binding_standardization_planning_v1 import (
    BINDING_SCHEMA_FIELDS,
    DUAL_VALIDATION_MECHANISM_ID,
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
    MODULE_LOCAL_PROFILE_STANDARD_REF,
    REUSED_GOVERNANCE_STANDARDS,
)
from capabilities.governance.migration_governance_development_constraints_v1 import CONSTRAINT_DOC_ID
from capabilities.governance.module_local_model_profile_standardization_dryrun_and_review_v1 import (
    DEFERRED_NON_COMPLIANCE_HANDLING_PHASE,
    NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM,
)

MIN_CHECKS = 171

REQUIRED = (
    "midplatform_model_governance_binding_standardization_dryrun_review_policy_v1.json",
    "planning_input_review_v1.json",
    "governance_standard_reuse_review_v1.json",
    "midplatform_model_governance_binding_standard_candidate_v1.json",
    "midplatform_model_governance_binding_schema_review_v1.json",
    "constitution_bus_binding_policy_review_v1.json",
    "capability_bus_binding_policy_review_v1.json",
    "provider_abstraction_binding_policy_review_v1.json",
    "validation_binding_policy_review_v1.json",
    "health_oversight_binding_policy_review_v1.json",
    "whitebox_trace_binding_policy_review_v1.json",
    "information_integration_binding_policy_review_v1.json",
    "decision_center_binding_policy_review_v1.json",
    "gate_chain_binding_policy_review_v1.json",
    "controlled_runtime_binding_policy_review_v1.json",
    "memory_worldmodel_admission_binding_policy_review_v1.json",
    "model_governance_binding_by_capability_layer_review_v1.json",
    "model_governance_binding_by_module_domain_review_v1.json",
    "vision_model_governance_binding_template_review_v1.json",
    "ocr_model_governance_binding_template_review_v1.json",
    "tts_model_governance_binding_template_review_v1.json",
    "asr_model_governance_binding_template_review_v1.json",
    "map_navigation_model_governance_binding_template_review_v1.json",
    "world_continuity_model_governance_binding_template_review_v1.json",
    "memory_emotion_evolution_model_governance_binding_template_review_v1.json",
    "dual_validation_to_midplatform_binding_handoff_policy_review_v1.json",
    "non_compliance_handling_deferment_review_v1.json",
    "midplatform_model_governance_binding_non_runtime_boundary_audit_v1.json",
    "midplatform_model_governance_binding_blocked_path_result_v1.json",
    "midplatform_model_governance_binding_closure_decision_v1.json",
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
            "midplatform_model_governance_binding_standardization_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_model_governance_binding_standardization_planning"
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

    summary = _load(root / "summary.json")
    candidate = _load(root / "midplatform_model_governance_binding_standard_candidate_v1.json")
    schema_review = _load(root / "midplatform_model_governance_binding_schema_review_v1.json")
    closure = _load(root / "midplatform_model_governance_binding_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    blocked = _load(root / "midplatform_model_governance_binding_blocked_path_result_v1.json")
    gov_reuse = _load(root / "governance_standard_reuse_review_v1.json")
    deferment = _load(root / "non_compliance_handling_deferment_review_v1.json")
    boundary = _load(root / "midplatform_model_governance_binding_non_runtime_boundary_audit_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.templates7", summary.get("template_count") == 7)
    ok("summary.domains10", summary.get("domain_coverage_count") == 10)
    ok("summary.layers6", summary.get("layer_binding_count") == 6)
    ok("summary.policies11", summary.get("binding_policy_count") == 11)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.standard", summary.get("standard_id") == STANDARD_ID)
    ok("summary.registry", summary.get("registry_ref") == REGISTRY_REF)
    ok("summary.ml_std", summary.get("module_local_profile_standard_ref") == MODULE_LOCAL_PROFILE_STANDARD_REF)
    ok("summary.dual_ref", summary.get("dual_validation_mechanism_ref") == DUAL_VALIDATION_MECHANISM_ID)
    ok("summary.constraints", summary.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    ok("summary.deferred", summary.get("non_compliant_module_model_handling_policy_deferred") is True)
    ok("summary.future_phase", summary.get("recommended_future_phase") == DEFERRED_NON_COMPLIANCE_HANDLING_PHASE)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("candidate.id", candidate.get("standard_id") == STANDARD_ID)
    ok("candidate.candidate", candidate.get("candidate_only") is True)
    ok("candidate.no_runtime", candidate.get("binding_runtime_enabled_now") is False)
    ok("candidate.no_select", candidate.get("model_selection_allowed_now") is False)
    ok("candidate.no_invoke", candidate.get("model_invocation_allowed_now") is False)

    ok("schema_review.pass", schema_review.get("review_pass") is True)
    ok("schema_review.count30", schema_review.get("field_count") == len(BINDING_SCHEMA_FIELDS))
    for field in BINDING_SCHEMA_FIELDS:
        ok(f"schema.{field[:16]}", any(
            c.get("check_id") == field and c.get("pass") for c in (schema_review.get("checks") or [])
        ))

    policy_reviews = (
        "constitution_bus_binding_policy_review_v1.json",
        "capability_bus_binding_policy_review_v1.json",
        "provider_abstraction_binding_policy_review_v1.json",
        "validation_binding_policy_review_v1.json",
        "health_oversight_binding_policy_review_v1.json",
        "whitebox_trace_binding_policy_review_v1.json",
        "information_integration_binding_policy_review_v1.json",
        "decision_center_binding_policy_review_v1.json",
        "gate_chain_binding_policy_review_v1.json",
        "controlled_runtime_binding_policy_review_v1.json",
        "memory_worldmodel_admission_binding_policy_review_v1.json",
    )
    for pr in policy_reviews:
        ok(f"review.{pr[:20]}", _load(root / pr).get("review_pass") is True)

    ok("layer_review.pass", _load(
        root / "model_governance_binding_by_capability_layer_review_v1.json"
    ).get("review_pass") is True)
    ok("domain_review.pass", _load(
        root / "model_governance_binding_by_module_domain_review_v1.json"
    ).get("review_pass") is True)

    for tpl in (
        "vision_model_governance_binding_template_review_v1.json",
        "ocr_model_governance_binding_template_review_v1.json",
        "tts_model_governance_binding_template_review_v1.json",
        "asr_model_governance_binding_template_review_v1.json",
        "map_navigation_model_governance_binding_template_review_v1.json",
        "world_continuity_model_governance_binding_template_review_v1.json",
        "memory_emotion_evolution_model_governance_binding_template_review_v1.json",
    ):
        ok(f"tpl.{tpl[:20]}", _load(root / tpl).get("review_pass") is True)

    ok("dual_handoff.pass", _load(
        root / "dual_validation_to_midplatform_binding_handoff_policy_review_v1.json"
    ).get("review_pass") is True)
    ok("deferment.pass", deferment.get("review_pass") is True)

    ok("gov_reuse.pass", gov_reuse.get("review_pass") is True)
    ok("gov_reuse.ref", gov_reuse.get("governance_constraints_ref") == CONSTRAINT_DOC_ID)
    for std in REUSED_GOVERNANCE_STANDARDS:
        ok(f"gov_reuse.{std[:16]}", std in (gov_reuse.get("reused_standards") or []))

    ok("planning_in.pass", _load(root / "planning_input_review_v1.json").get("review_pass") is True)

    ok("boundary.audit", boundary.get("audit_pass") is True)
    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count", blocked.get("blocked_count") == len(BLOCKED_PATHS))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("closure.no_high_risk", closure.get("high_risk") is False)

    ok("next_route.ready", next_route.get(
        "ready_for_vision_module_model_profile_governance_binding_planning"
    ) is True)
    ok("next_route.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))
    ok("non_claim.deferral", NON_COMPLIANCE_HANDLING_DEFERRAL_CLAIM in (
        _load(root / "non_claims_register_v1.json").get("non_claims") or []
    ))
    for claim in DUAL_VALIDATION_NON_CLAIMS:
        ok(f"dual_claim.{claim[:18]}", claim in (
            _load(root / "non_claims_register_v1.json").get("dual_validation_non_claims") or []
        ))

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
