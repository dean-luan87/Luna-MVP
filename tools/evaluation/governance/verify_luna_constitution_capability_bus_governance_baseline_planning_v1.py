#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Luna Constitution-Capability-Bus Governance Baseline Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.luna_constitution_capability_bus_governance_baseline_planning_v1 import (
    ARCHITECTURE_LAYERS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    BUS_CANNOT_SELF_JUDGE,
    BUS_CORE_FUNCTIONS,
    BUS_GOVERNANCE_CONTRACT_FIELDS,
    CHANGE_PROPAGATION_RULES,
    DEFERRED_RUNTIME_ITEMS,
    FINAL_DECISION_GO,
    GOVERNANCE_POWER_STRUCTURE,
    GOVERNANCE_SEPARATION_SUMMARY,
    HEALTH_EXTERNAL_OBSERVATIONS,
    HEALTH_OVERSIGHT_CONFIRMATIONS,
    HEALTH_OVERSIGHT_MAY,
    HEALTH_OVERSIGHT_MUST_NOT,
    HEALTH_OVERSIGHT_PRINCIPLE,
    MODULE_BOUNDARY_CONFIRMATIONS,
    MODULE_CONFIRMATIONS,
    MODULE_ENFORCEMENT_FIELDS,
    MODULE_ID,
    MODULE_SHORT_NAME,
    MODULE_STATUS,
    MODULE_VERSION,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    PROPAGATION_CHAIN,
    PROPAGATION_CONFIRMATIONS,
    REGISTRATION_CONFIRMATIONS,
    RESPONSIBILITY_MATRIX,
    SCOPE,
    UPSTREAM_II_DR_FINAL,
    UPSTREAM_II_DR_NEXT,
    VERSION_COMPATIBILITY_RULES,
    VERSION_MANIFEST_COVERS,
    VERSION_MANIFEST_DOES_NOT_COVER,
)
from capabilities.governance.midplatform_information_integration_layer_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as II_DR_FINAL,
    NEXT_PHASE_GO as II_DR_NEXT,
)
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    GOVERNANCE_STANDARDS,
)

MIN_CHECKS = 290

REQUIRED = (
    "constitution_capability_bus_governance_baseline_policy_v1.json",
    "upstream_information_integration_input_review_v1.json",
    "luna_constitution_capability_bus_governance_module_v1.json",
    "constitution_bus_version_manifest_v1.json",
    "constitution_bus_module_boundary_v1.json",
    "constitution_bus_responsibility_matrix_v1.json",
    "constitution_to_bus_propagation_model_v1.json",
    "bus_to_module_contract_enforcement_model_v1.json",
    "module_registration_governance_contract_v1.json",
    "capability_bus_governance_contract_v1.json",
    "governance_standard_binding_matrix_v1.json",
    "constitution_bus_version_compatibility_policy_v1.json",
    "constitution_bus_change_propagation_policy_v1.json",
    "constitution_bus_non_runtime_boundary_matrix_v1.json",
    "constitution_bus_future_runtime_deferment_register_v1.json",
    "constitution_bus_external_health_oversight_policy_v1.json",
    "constitution_bus_baseline_closure_decision_v1.json",
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
            "luna_constitution_capability_bus_governance_baseline_planning"
        ),
    )
    p.add_argument(
        "--information-integration-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_information_integration_layer_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    ii_dr_root = Path(args.information_integration_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    ii_dr_vr = _load(ii_dr_root / "verifier_report.json")
    ii_dr_sm = _load(ii_dr_root / "summary.json")

    ok("upstream.ii_dr_go", ii_dr_vr.get("verifier") == "GO")
    ok("upstream.ii_dr_final", ii_dr_sm.get("final_decision") == UPSTREAM_II_DR_FINAL)
    ok("upstream.ii_dr_final_expected", ii_dr_sm.get("final_decision") == II_DR_FINAL)
    ok("upstream.ii_dr_next", ii_dr_sm.get("recommended_next_phase") == UPSTREAM_II_DR_NEXT)
    ok("upstream.ii_dr_next_expected", ii_dr_sm.get("recommended_next_phase") == II_DR_NEXT)

    summary = _load(root / "summary.json")
    policy = _load(root / "constitution_capability_bus_governance_baseline_policy_v1.json")
    input_review = _load(root / "upstream_information_integration_input_review_v1.json")
    module = _load(root / "luna_constitution_capability_bus_governance_module_v1.json")
    manifest = _load(root / "constitution_bus_version_manifest_v1.json")
    boundary = _load(root / "constitution_bus_module_boundary_v1.json")
    matrix = _load(root / "constitution_bus_responsibility_matrix_v1.json")
    propagation = _load(root / "constitution_to_bus_propagation_model_v1.json")
    enforcement = _load(root / "bus_to_module_contract_enforcement_model_v1.json")
    registration = _load(root / "module_registration_governance_contract_v1.json")
    bus_contract = _load(root / "capability_bus_governance_contract_v1.json")
    binding = _load(root / "governance_standard_binding_matrix_v1.json")
    compatibility = _load(root / "constitution_bus_version_compatibility_policy_v1.json")
    change_policy = _load(root / "constitution_bus_change_propagation_policy_v1.json")
    boundary_matrix = _load(root / "constitution_bus_non_runtime_boundary_matrix_v1.json")
    deferment = _load(root / "constitution_bus_future_runtime_deferment_register_v1.json")
    health_oversight = _load(root / "constitution_bus_external_health_oversight_policy_v1.json")
    closure = _load(root / "constitution_bus_baseline_closure_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("planning_not_runtime_not_implement") is True)
    ok("policy.module_id", policy.get("governance_module_id") == MODULE_ID)
    ok("policy.version", policy.get("version") == MODULE_VERSION)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.ii_go", input_review.get("information_integration_dryrun_verifier") == "GO")
    ok("input.ii_final", input_review.get("information_integration_dryrun_final_decision") == UPSTREAM_II_DR_FINAL)
    ok("input.bus", input_review.get("capability_bus_positioned") is True)
    ok("input.gov_std", input_review.get("reusable_governance_standard_layer_defined") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("module.id", module.get("module_id") == MODULE_ID)
    ok("module.name", module.get("module_name") == "Luna Constitution-Bus Governance Module")
    ok("module.version", module.get("version") == MODULE_VERSION)
    ok("module.short", module.get("short_name") == MODULE_SHORT_NAME)
    ok("module.status", module.get("status") == MODULE_STATUS)
    ok("module.type", module.get("module_type") == "governance_bus_baseline_module")
    ok("module.layer", module.get("architectural_layer") == "ReusableGovernanceStandardLayer")
    ok("module.runtime_false", module.get("runtime_enabled_now") is False)
    ok("module.impl_false", module.get("implementation_started_now") is False)
    ok("module.candidate", module.get("candidate_only") is True)
    ok("module.health_principle", module.get("health_oversight_principle") == HEALTH_OVERSIGHT_PRINCIPLE)
    for ps in GOVERNANCE_POWER_STRUCTURE:
        ok(f"module.power.{ps['system'][:12]}", any(
            p.get("system") == ps["system"] for p in (module.get("governance_power_structure") or [])
        ))
    for fn in BUS_CORE_FUNCTIONS:
        ok(f"module.fn.{fn[:18]}", fn in (module.get("bus_core_functions") or []))
    for item in BUS_CANNOT_SELF_JUDGE:
        ok(f"module.nojudge.{item[:18]}", item in (module.get("bus_cannot_self_judge") or []))
    for sep in GOVERNANCE_SEPARATION_SUMMARY:
        ok(f"module.sep.{sep[:18]}", sep in (module.get("governance_separation_summary") or []))
    for layer in ARCHITECTURE_LAYERS:
        ok(f"module.layer.{layer['role'][:12]}", any(
            l.get("role") == layer["role"] for l in (module.get("architecture_layers") or [])
        ))
    for conf in MODULE_CONFIRMATIONS:
        ok(f"module.conf.{conf[:18]}", conf in (module.get("confirmations") or []))

    ok("manifest.module_id", manifest.get("governance_module_id") == MODULE_ID)
    ok("manifest.version", manifest.get("version") == MODULE_VERSION)
    ok("manifest.scope", manifest.get("version_scope") == "governance_baseline")
    ok("manifest.applies", manifest.get("applies_to") == "Luna 2.0 Modular Life Architecture")
    ok("manifest.cover12", manifest.get("cover_count") == 12)
    for cover in VERSION_MANIFEST_COVERS:
        ok(f"manifest.cover.{cover[:18]}", cover in (manifest.get("covers") or []))
    for nc in VERSION_MANIFEST_DOES_NOT_COVER:
        ok(f"manifest.not.{nc[:18]}", nc in (manifest.get("does_not_cover") or []))

    ok("boundary.count7", boundary.get("confirmation_count") == 7)
    for conf in MODULE_BOUNDARY_CONFIRMATIONS:
        ok(f"boundary.{conf[:18]}", conf in (boundary.get("confirmations") or []))

    ok("matrix.count16", matrix.get("responsibility_count") == 16)
    for resp in RESPONSIBILITY_MATRIX:
        ok(f"matrix.{resp[:18]}", resp in (matrix.get("responsibilities") or []))

    ok("prop.chain6", propagation.get("chain_length") == 6)
    for step in PROPAGATION_CHAIN:
        ok(f"prop.{step[:18]}", step in (propagation.get("propagation_chain") or []))
    for conf in PROPAGATION_CONFIRMATIONS:
        ok(f"prop.conf.{conf[:18]}", conf in (propagation.get("confirmations") or []))

    ok("enforce.count15", enforcement.get("field_count") == 15)
    for field in MODULE_ENFORCEMENT_FIELDS:
        ok(f"enforce.{field[:18]}", field in (enforcement.get("required_fields") or []))
    ok("enforce.source_chain", enforcement.get("defaults", {}).get("source_chain_required") is True)
    ok("enforce.candidate_default", enforcement.get("defaults", {}).get("candidate_only_outputs_by_default") is True)

    ok("reg.count7", registration.get("confirmation_count") == 7)
    for conf in REGISTRATION_CONFIRMATIONS:
        ok(f"reg.{conf[:18]}", conf in (registration.get("confirmations") or []))

    ok("bus.count12", bus_contract.get("field_count") == 12)
    ok("bus.not_plugin", bus_contract.get("bus_not_ordinary_plugin_bus") is True)
    for field in BUS_GOVERNANCE_CONTRACT_FIELDS:
        ok(f"bus.{field[:18]}", field in (bus_contract.get("required_fields") or []))

    ok("bind.count10", binding.get("standard_count") == 10)
    ok("bind.all", binding.get("all_standards_bound") is True)
    for std in GOVERNANCE_STANDARDS:
        ok(f"bind.{std[:18]}", std in (binding.get("governance_standards") or []))

    ok("compat.count7", compatibility.get("rule_count") == 7)
    for rule in VERSION_COMPATIBILITY_RULES:
        ok(f"compat.{rule[:18]}", rule in (compatibility.get("rules") or []))

    ok("change.count6", change_policy.get("rule_count") == 6)
    for rule in CHANGE_PROPAGATION_RULES:
        ok(f"change.{rule[:18]}", rule in (change_policy.get("rules") or []))

    ok("bnd_matrix.pass", boundary_matrix.get("boundary_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"bnd_matrix.{field}", boundary_matrix.get("boundary_fields", {}).get(field) is False)

    ok("defer.count7", deferment.get("item_count") == 7)
    for item in DEFERRED_RUNTIME_ITEMS:
        ok(f"defer.{item[:18]}", item in (deferment.get("deferred_items") or []))

    ok("health.principle", health_oversight.get("principle") == HEALTH_OVERSIGHT_PRINCIPLE)
    ok("health.external", health_oversight.get("health_oversight_external") is True)
    ok("health.no_self", health_oversight.get("bus_self_health_judgment_forbidden") is True)
    ok("health.may5", health_oversight.get("may_count") == 5)
    for item in HEALTH_OVERSIGHT_MAY:
        ok(f"health.may.{item[:18]}", item in (health_oversight.get("bus_may") or []))
    ok("health.must_not8", health_oversight.get("must_not_count") == 8)
    for item in HEALTH_OVERSIGHT_MUST_NOT:
        ok(f"health.not.{item[:18]}", item in (health_oversight.get("bus_must_not") or []))
    for conf in HEALTH_OVERSIGHT_CONFIRMATIONS:
        ok(f"health.conf.{conf[:18]}", conf in (health_oversight.get("confirmations") or []))
    ok("health.obs7", health_oversight.get("observation_count") == 7)
    for obs in HEALTH_EXTERNAL_OBSERVATIONS:
        ok(f"health.obs.{obs[:18]}", obs in (health_oversight.get("health_external_observations") or []))

    ok("closure.pass", closure.get("planning_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
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
        "planning_pass": summary.get("planning_pass"),
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
