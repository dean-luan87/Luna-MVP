#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Constitution-Capability-Bus Governance Baseline DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    BUS_GOVERNANCE_CONTRACT_FIELDS,
    CHANGE_PROPAGATION_RULES,
    DEFERRED_RUNTIME_ITEMS,
    DRYRUN_NON_CLAIMS,
    FINAL_DECISION_GO,
    MODULE_BOUNDARY_CONFIRMATIONS,
    MODULE_CONFIRMATIONS,
    MODULE_ENFORCEMENT_FIELDS,
    MODULE_ID,
    MODULE_SHORT_NAME,
    MODULE_VERSION,
    NEXT_PHASE_GO,
    PHASE_ID,
    PROPAGATION_CONFIRMATIONS,
    REGISTRATION_CONFIRMATIONS,
    RESPONSIBILITY_MATRIX,
    SCOPE,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
    VERSION_COMPATIBILITY_RULES,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    HEALTH_EXTERNAL_OBSERVATIONS,
    HEALTH_OVERSIGHT_CONFIRMATIONS,
    HEALTH_OVERSIGHT_MAY,
    HEALTH_OVERSIGHT_MUST_NOT,
    HEALTH_OVERSIGHT_PRINCIPLE,
)
from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    GOVERNANCE_STANDARDS,
)

MIN_CHECKS = 247

REQUIRED = (
    "constitution_bus_governance_baseline_dryrun_review_policy_v1.json",
    "constitution_bus_planning_input_review_v1.json",
    "constitution_bus_module_dryrun_review_v1.json",
    "constitution_bus_version_manifest_review_v1.json",
    "constitution_bus_module_boundary_review_v1.json",
    "constitution_bus_responsibility_matrix_review_v1.json",
    "constitution_to_bus_propagation_review_v1.json",
    "bus_to_module_contract_enforcement_review_v1.json",
    "module_registration_governance_review_v1.json",
    "capability_bus_governance_contract_review_v1.json",
    "governance_standard_binding_review_v1.json",
    "constitution_bus_version_compatibility_review_v1.json",
    "constitution_bus_change_propagation_review_v1.json",
    "constitution_bus_future_runtime_deferment_review_v1.json",
    "constitution_bus_external_health_oversight_review_v1.json",
    "constitution_bus_boundary_audit_v1.json",
    "constitution_bus_blocked_path_result_v1.json",
    "constitution_bus_governance_baseline_closure_decision_v1.json",
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
            "luna_constitution_capability_bus_governance_baseline_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "luna_constitution_capability_bus_governance_baseline_planning"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.planning_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")

    ok("upstream.plan_go", plan_vr.get("verifier") == "GO")
    ok("upstream.plan_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.plan_final_expected", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.plan_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.plan_next_expected", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)

    summary = _load(root / "summary.json")
    policy = _load(root / "constitution_bus_governance_baseline_dryrun_review_policy_v1.json")
    input_review = _load(root / "constitution_bus_planning_input_review_v1.json")
    module_review = _load(root / "constitution_bus_module_dryrun_review_v1.json")
    version_review = _load(root / "constitution_bus_version_manifest_review_v1.json")
    boundary_review = _load(root / "constitution_bus_module_boundary_review_v1.json")
    matrix_review = _load(root / "constitution_bus_responsibility_matrix_review_v1.json")
    propagation_review = _load(root / "constitution_to_bus_propagation_review_v1.json")
    enforcement_review = _load(root / "bus_to_module_contract_enforcement_review_v1.json")
    registration_review = _load(root / "module_registration_governance_review_v1.json")
    bus_review = _load(root / "capability_bus_governance_contract_review_v1.json")
    binding_review = _load(root / "governance_standard_binding_review_v1.json")
    compatibility_review = _load(root / "constitution_bus_version_compatibility_review_v1.json")
    change_review = _load(root / "constitution_bus_change_propagation_review_v1.json")
    deferment_review = _load(root / "constitution_bus_future_runtime_deferment_review_v1.json")
    health_review = _load(root / "constitution_bus_external_health_oversight_review_v1.json")
    boundary = _load(root / "constitution_bus_boundary_audit_v1.json")
    blocked = _load(root / "constitution_bus_blocked_path_result_v1.json")
    closure = _load(root / "constitution_bus_governance_baseline_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.v1_validated", summary.get("governance_baseline_v1_0_validated") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("dryrun_not_runtime_not_implement") is True)
    ok("policy.module_id", policy.get("governance_module_id") == MODULE_ID)
    ok("policy.version", policy.get("version") == MODULE_VERSION)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.plan_go", input_review.get("planning_verifier") == "GO")
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("module.review_pass", module_review.get("dryrun_and_review_pass") is True)
    ok("module.id", module_review.get("module_id") == MODULE_ID)
    ok("module.version", module_review.get("version") == MODULE_VERSION)
    ok("module.short", module_review.get("short_name") == MODULE_SHORT_NAME)
    ok("module.runtime_false", module_review.get("runtime_enabled_now") is False)
    for conf in MODULE_CONFIRMATIONS:
        ok(f"module.{conf[:18]}", conf in (module_review.get("confirmations") or []))

    ok("version.review_pass", version_review.get("dryrun_and_review_pass") is True)
    ok("version.v1", version_review.get("version") == MODULE_VERSION)
    ok("version.validated", version_review.get("v1_0_baseline_validated") is True)

    ok("boundary.review_pass", boundary_review.get("dryrun_and_review_pass") is True)
    for conf in MODULE_BOUNDARY_CONFIRMATIONS:
        ok(f"boundary.{conf[:18]}", conf in (boundary_review.get("confirmations") or []))

    ok("matrix.review_pass", matrix_review.get("dryrun_and_review_pass") is True)
    ok("matrix.count16", matrix_review.get("responsibility_count") == 16)
    for resp in RESPONSIBILITY_MATRIX:
        ok(f"matrix.{resp[:18]}", resp in (matrix_review.get("responsibilities") or []))

    ok("prop.review_pass", propagation_review.get("dryrun_and_review_pass") is True)
    for conf in PROPAGATION_CONFIRMATIONS:
        ok(f"prop.{conf[:18]}", conf in (propagation_review.get("confirmations") or []))

    ok("enforce.review_pass", enforcement_review.get("dryrun_and_review_pass") is True)
    ok("enforce.source_chain", enforcement_review.get("source_chain_required") is True)
    for field in MODULE_ENFORCEMENT_FIELDS:
        ok(f"enforce.{field[:18]}", field in (enforcement_review.get("required_fields") or []))

    ok("reg.review_pass", registration_review.get("dryrun_and_review_pass") is True)
    for conf in REGISTRATION_CONFIRMATIONS:
        ok(f"reg.{conf[:18]}", conf in (registration_review.get("confirmations") or []))

    ok("bus.review_pass", bus_review.get("dryrun_and_review_pass") is True)
    ok("bus.constitution_bound", bus_review.get("bus_constitution_bound") is True)
    ok("bus.not_plugin", bus_review.get("bus_not_ordinary_plugin_bus") is True)
    for field in BUS_GOVERNANCE_CONTRACT_FIELDS:
        ok(f"bus.{field[:18]}", field in (bus_review.get("required_fields") or []))

    ok("bind.review_pass", binding_review.get("dryrun_and_review_pass") is True)
    ok("bind.all", binding_review.get("all_bound") is True)
    for std in GOVERNANCE_STANDARDS:
        ok(f"bind.{std[:18]}", std in (binding_review.get("governance_standards") or []))

    ok("compat.review_pass", compatibility_review.get("dryrun_and_review_pass") is True)
    for rule in VERSION_COMPATIBILITY_RULES:
        ok(f"compat.{rule[:18]}", rule in (compatibility_review.get("rules") or []))

    ok("change.review_pass", change_review.get("dryrun_and_review_pass") is True)
    for rule in CHANGE_PROPAGATION_RULES:
        ok(f"change.{rule[:18]}", rule in (change_review.get("rules") or []))

    ok("defer.review_pass", deferment_review.get("dryrun_and_review_pass") is True)
    ok("defer.all", deferment_review.get("all_deferred") is True)
    for item in DEFERRED_RUNTIME_ITEMS:
        ok(f"defer.{item[:18]}", item in (deferment_review.get("deferred_items") or []))

    ok("health.review_pass", health_review.get("dryrun_and_review_pass") is True)
    ok("health.principle", health_review.get("principle") == HEALTH_OVERSIGHT_PRINCIPLE)
    ok("health.external", health_review.get("health_oversight_external") is True)
    ok("health.no_self", health_review.get("bus_self_health_judgment_forbidden") is True)
    for item in HEALTH_OVERSIGHT_MAY:
        ok(f"health.may.{item[:18]}", item in (health_review.get("bus_may") or []))
    for item in HEALTH_OVERSIGHT_MUST_NOT:
        ok(f"health.not.{item[:18]}", item in (health_review.get("bus_must_not") or []))
    for conf in HEALTH_OVERSIGHT_CONFIRMATIONS:
        ok(f"health.conf.{conf[:18]}", conf in (health_review.get("confirmations") or []))
    for obs in HEALTH_EXTERNAL_OBSERVATIONS:
        ok(f"health.obs.{obs[:18]}", obs in (health_review.get("health_external_observations") or []))

    ok("audit.pass", boundary.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"audit.{field}", boundary.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count12", blocked.get("blocked_count") == 12)
    for path in BLOCKED_PATHS:
        ok(f"blocked.{path[:18]}", any(
            b.get("path_id") == path and b.get("status") == "blocked"
            for b in (blocked.get("blocked_paths") or [])
        ))

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next_route.ready", next_route.get("ready_for_vision_navigation_mainline_resume") is True)
    ok("next_route.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

    for claim in DRYRUN_NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

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
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({"verifier": verifier, "checks_passed": passed, "checks_total": total}))
    return 0 if verifier == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
