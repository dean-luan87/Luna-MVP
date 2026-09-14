#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Seed Core / Pluggable Layer Architecture Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CZ_DR_FINAL,
    NEXT_PHASE_GO as CZ_DR_NEXT,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    PRODUCT_FORMS,
    SEED_CORE_COMPONENTS,
    SEED_CORE_CONFIRMATIONS,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS,
    CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES,
    CAPABILITY_MODULE_CONTRACT_FIELDS,
    EMOTION_ENGINE_RULES,
    EVOLUTIONARY_RECURSION_RULES,
    FINAL_DECISION_GO,
    GOVERNANCE_STANDARDS,
    IDENTITY_BOUNDARY_RULES,
    INVARIANT_FIXED,
    LUNA_1_0_FORM,
    LUNA_2_0_TARGET,
    MIGRATION_RISKS,
    MODULE_HEALTH_PERMISSION_RUNTIME_RULES,
    MODULE_REGISTRATION_PLAN,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PERSONAL_CONTINUITY_CONFIRMATIONS,
    PERSONAL_CONTINUITY_COVERAGE,
    PHASE_ID,
    PLUGGABLE_CAPABILITY_MODULES,
    PLUGGABLE_LAYER_CONFIRMATIONS,
    PLUGGABLE_VARIABLE,
    SCOPE,
    SEED_CORE_INVARIANTS,
    SEED_CORE_ZONE_FORBIDDEN,
    SEED_CORE_ZONE_INFLUENCES,
    SURVIVAL_DRIVE_SUBMODULES,
    UPSTREAM_CZ_DR_FINAL,
    UPSTREAM_CZ_DR_NEXT,
)

MIN_CHECKS = 455

REQUIRED = (
    "seed_core_pluggable_layer_architecture_planning_policy_v1.json",
    "cognitive_zoning_input_review_v1.json",
    "seed_core_pluggable_layer_architecture_model_v1.json",
    "fixed_seed_core_definition_v1.json",
    "seed_core_component_matrix_v1.json",
    "survival_drive_architecture_placeholder_v1.json",
    "personal_continuity_module_positioning_v1.json",
    "pluggable_capability_layer_definition_v1.json",
    "capability_module_contract_v1.json",
    "luna_capability_bus_architecture_placeholder_v1.json",
    "capability_bus_responsibility_matrix_v1.json",
    "product_form_topology_matrix_v1.json",
    "invariant_vs_pluggable_boundary_review_v1.json",
    "seed_core_to_cognitive_zone_influence_matrix_v1.json",
    "personal_continuity_identity_boundary_policy_v1.json",
    "module_registration_and_discovery_plan_v1.json",
    "module_health_permission_runtime_plan_v1.json",
    "migration_backup_restore_risk_register_v1.json",
    "seed_core_pluggable_layer_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "seed_core_pluggable_layer_architecture_planning_decision_v1.json",
    "summary.json",
)

COMPONENT_MATRIX_FIELDS = (
    "component_id",
    "component_role",
    "input_signals",
    "output_signals",
    "allowed_outputs",
    "forbidden_outputs",
    "governed_by",
    "downstream_consumers",
    "runtime_enabled_now",
)

PRODUCT_TOPOLOGY_FIELDS = (
    "seed_core_location",
    "personal_continuity_module_location",
    "capability_modules_available",
    "local_compute_level",
    "cloud_dependency_level",
    "offline_capability_level",
    "privacy_boundary",
    "bus_topology",
    "runtime_limitations",
)


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "seed_core_pluggable_layer_architecture_planning"
        ),
    )
    p.add_argument(
        "--cognitive-zoning-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_cognitive_zoning_architecture_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--provider-abstraction-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--controlled-runtime-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_controlled_runtime_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    cz_dr_root = Path(args.cognitive_zoning_dryrun_root)
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    cr_dr_root = Path(args.controlled_runtime_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    cz_dr_vr = _load(cz_dr_root / "verifier_report.json")
    cz_dr_sm = _load(cz_dr_root / "summary.json")
    provider_dr_vr = _load(provider_dr_root / "verifier_report.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    cr_dr_vr = _load(cr_dr_root / "verifier_report.json")

    ok("upstream.cz_dr_go", cz_dr_vr.get("verifier") == "GO")
    ok("upstream.cz_dr_final", cz_dr_sm.get("final_decision") == UPSTREAM_CZ_DR_FINAL)
    ok("upstream.cz_dr_final_expected", cz_dr_sm.get("final_decision") == CZ_DR_FINAL)
    ok("upstream.cz_dr_next", cz_dr_sm.get("recommended_next_phase") == UPSTREAM_CZ_DR_NEXT)
    ok("upstream.cz_dr_next_expected", cz_dr_sm.get("recommended_next_phase") == CZ_DR_NEXT)
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_DR_FINAL)
    ok("upstream.cr_dr_go", cr_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "seed_core_pluggable_layer_architecture_planning_policy_v1.json")
    input_review = _load(root / "cognitive_zoning_input_review_v1.json")
    arch_model = _load(root / "seed_core_pluggable_layer_architecture_model_v1.json")
    seed_core_def = _load(root / "fixed_seed_core_definition_v1.json")
    component_matrix = _load(root / "seed_core_component_matrix_v1.json")
    survival = _load(root / "survival_drive_architecture_placeholder_v1.json")
    continuity = _load(root / "personal_continuity_module_positioning_v1.json")
    pluggable = _load(root / "pluggable_capability_layer_definition_v1.json")
    module_contract = _load(root / "capability_module_contract_v1.json")
    bus_placeholder = _load(root / "luna_capability_bus_architecture_placeholder_v1.json")
    bus_matrix = _load(root / "capability_bus_responsibility_matrix_v1.json")
    product_topo = _load(root / "product_form_topology_matrix_v1.json")
    invariant_review = _load(root / "invariant_vs_pluggable_boundary_review_v1.json")
    seed_zone = _load(root / "seed_core_to_cognitive_zone_influence_matrix_v1.json")
    identity_policy = _load(root / "personal_continuity_identity_boundary_policy_v1.json")
    reg_plan = _load(root / "module_registration_and_discovery_plan_v1.json")
    health_plan = _load(root / "module_health_permission_runtime_plan_v1.json")
    risk_reg = _load(root / "migration_backup_restore_risk_register_v1.json")
    dryrun_plan = _load(root / "seed_core_pluggable_layer_dryrun_plan_v1.json")
    decision = _load(root / "seed_core_pluggable_layer_architecture_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.four_layer", summary.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.not_runtime", policy.get("planning_not_runtime_not_hardware_not_split") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.no_brain", input_review.get("no_universal_brain_pass") is True)
    ok("input.bus_positioned", input_review.get("capability_bus_positioned_not_implemented") is True)
    ok("input.evo_proposal", input_review.get("evolutionary_recursion_proposal_only") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("model.id", arch_model.get("architecture_id") == "luna_seed_core_pluggable_layer_architecture_v1")
    ok("model.type", arch_model.get("architecture_type") == "modular_life_architecture")
    ok("model.luna_1_0", arch_model.get("luna_1_0_form") == LUNA_1_0_FORM)
    ok("model.luna_2_0", arch_model.get("luna_2_0_target") == LUNA_2_0_TARGET)
    ok("model.seed_core", arch_model.get("fixed_seed_core_required") is True)
    ok("model.continuity", arch_model.get("personal_continuity_module_required") is True)
    ok("model.pluggable", arch_model.get("pluggable_capability_layer_required") is True)
    ok("model.bus", arch_model.get("luna_capability_bus_required") is True)
    ok("model.gov", arch_model.get("reusable_governance_standard_layer_required") is True)
    ok("model.product_var", arch_model.get("product_form_layer_variable") is True)
    ok("model.runtime_false", arch_model.get("runtime_enabled_now") is False)
    ok("model.hw_false", arch_model.get("hardware_implementation_started_now") is False)
    ok("model.candidate", arch_model.get("candidate_only") is True)

    ok("seed.count7", seed_core_def.get("component_count") == 7)
    for comp in SEED_CORE_COMPONENTS:
        ok(f"seed.comp.{comp[:18]}", comp in (seed_core_def.get("components") or []))
    for conf in SEED_CORE_CONFIRMATIONS:
        ok(f"seed.conf.{conf[:18]}", conf in (seed_core_def.get("confirmations") or []))
    for inv in SEED_CORE_INVARIANTS:
        ok(f"seed.inv.{inv[:18]}", inv in (seed_core_def.get("invariants") or []))

    ok("matrix.count7", component_matrix.get("component_count") == 7)
    components = component_matrix.get("components") or []
    for comp in components:
        cid = comp.get("component_id", "unknown")
        for field in COMPONENT_MATRIX_FIELDS:
            ok(f"comp.field.{cid}.{field}", field in comp)
        ok(f"comp.runtime.{cid}", comp.get("runtime_enabled_now") is False)

    ok("survival.count6", survival.get("submodule_count") == 6)
    for sub in SURVIVAL_DRIVE_SUBMODULES:
        ok(f"survival.{sub[:18]}", sub in (survival.get("future_submodules") or []))
    for rule in EMOTION_ENGINE_RULES:
        ok(f"emotion.{rule[:18]}", rule in (survival.get("emotion_engine", {}).get("rules") or []))
    for rule in EVOLUTIONARY_RECURSION_RULES:
        ok(f"evo.{rule[:18]}", rule in (survival.get("evolutionary_recursion", {}).get("rules") or []))
    ok("evo.proposal_only", survival.get("evolutionary_recursion", {}).get("proposal_only") is True)

    ok("continuity.id", continuity.get("module_id") == "luna_personal_continuity_module_v1")
    ok("continuity.type", continuity.get("module_type") == "memory_emotion_continuity_module")
    ok("continuity.hw", continuity.get("hardware_concept") == "memory_stick_or_life_memory_module")
    ok("continuity.identity_protected", continuity.get("pluggable_but_identity_protected") is True)
    ok("continuity.not_cloneable", continuity.get("portable_but_not_freely_cloneable") is True)
    ok("continuity.runtime_false", continuity.get("runtime_enabled_now") is False)
    ok("continuity.write_false", continuity.get("memory_write_enabled_now") is False)
    ok("continuity.count10", continuity.get("coverage_count") == 10)
    for cov in PERSONAL_CONTINUITY_COVERAGE:
        ok(f"continuity.cov.{cov[:18]}", cov in (continuity.get("coverage") or []))
    for conf in PERSONAL_CONTINUITY_CONFIRMATIONS:
        ok(f"continuity.conf.{conf[:18]}", conf in (continuity.get("confirmations") or []))

    ok("plug.count13", pluggable.get("module_count") == 13)
    for mod in PLUGGABLE_CAPABILITY_MODULES:
        ok(f"plug.mod.{mod[:18]}", mod in (pluggable.get("capability_modules") or []))
    for conf in PLUGGABLE_LAYER_CONFIRMATIONS:
        ok(f"plug.conf.{conf[:18]}", conf in (pluggable.get("confirmations") or []))

    ok("contract.count13", module_contract.get("contract_count") == 13)
    for field in CAPABILITY_MODULE_CONTRACT_FIELDS:
        ok(f"contract.field.{field[:18]}", field in (module_contract.get("required_fields") or []))
    for mc in module_contract.get("module_contracts") or []:
        mid = mc.get("module_id", "unknown")
        ok(f"contract.mc.{mid[:18]}", mc.get("source_chain_required") is True)
        ok(f"contract.candidate.{mid[:18]}", mc.get("candidate_only_outputs_by_default") is True)

    ok("bus.count12", bus_placeholder.get("responsibility_count") == 12)
    ok("bus.runtime_false", bus_placeholder.get("capability_bus_runtime_enabled_now") is False)
    ok("bus.not_impl", bus_placeholder.get("planned_not_implemented") is True)
    for resp in CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES:
        ok(f"bus.{resp[:18]}", resp in (bus_placeholder.get("responsibilities") or []))
    for conf in CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS:
        ok(f"bus.conf.{conf[:18]}", conf in (bus_placeholder.get("confirmations") or []))

    ok("bus_matrix.count12", bus_matrix.get("responsibility_count") == 12)

    ok("product.count7", product_topo.get("form_count") == 7)
    for form in PRODUCT_FORMS:
        entry = next(
            (f for f in (product_topo.get("product_forms") or []) if f.get("product_form") == form),
            None,
        )
        ok(f"product.{form[:18]}", entry is not None)
        if entry:
            for field in PRODUCT_TOPOLOGY_FIELDS:
                ok(f"product.field.{form[:12]}.{field[:12]}", field in entry)

    ok("inv.count9", invariant_review.get("invariant_count") == 9)
    ok("inv.plug9", invariant_review.get("pluggable_count") == 9)
    ok("inv.clear", invariant_review.get("boundary_clear") is True)
    for item in INVARIANT_FIXED:
        ok(f"inv.fixed.{item[:18]}", item in (invariant_review.get("invariant_fixed") or []))
    for item in PLUGGABLE_VARIABLE:
        ok(f"inv.plug.{item[:18]}", item in (invariant_review.get("pluggable_variable") or []))

    ok("seed_zone.count9", seed_zone.get("influence_count") == 9)
    for inf in SEED_CORE_ZONE_INFLUENCES:
        ok(
            f"seed_zone.inf.{inf['influence'][:18]}",
            any(i.get("influence") == inf["influence"] for i in (seed_zone.get("influences") or [])),
        )
    for forbidden in SEED_CORE_ZONE_FORBIDDEN:
        ok(f"seed_zone.forbid.{forbidden[:18]}", forbidden in (seed_zone.get("forbidden_direct_actions") or []))

    ok("identity.count8", identity_policy.get("rule_count") == 8)
    for rule in IDENTITY_BOUNDARY_RULES:
        ok(f"identity.{rule[:18]}", rule in (identity_policy.get("rules") or []))

    ok("reg.count9", reg_plan.get("step_count") == 9)
    ok("reg.not_impl", reg_plan.get("implemented_now") is False)
    for step in MODULE_REGISTRATION_PLAN:
        ok(f"reg.{step[:18]}", step in (reg_plan.get("registration_steps") or []))

    ok("health.count7", health_plan.get("rule_count") == 7)
    for rule in MODULE_HEALTH_PERMISSION_RUNTIME_RULES:
        ok(f"health.{rule[:18]}", rule in (health_plan.get("rules") or []))

    ok("risk.count10", risk_reg.get("risk_count") == 10)
    for risk in MIGRATION_RISKS:
        entry = next((r for r in (risk_reg.get("risks") or []) if r.get("risk_id") == risk), None)
        ok(f"risk.{risk[:18]}", entry is not None and entry.get("planned_only") is True)

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.no_runtime", "no runtime enabled" in (dryrun_plan.get("dryrun_objectives") or []))

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)

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
