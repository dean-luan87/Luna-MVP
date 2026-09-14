#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Seed Core / Pluggable Layer Architecture DryRunAndReview v1."""

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
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    PRODUCT_FORMS,
    SEED_CORE_COMPONENTS,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_dryrun_and_review_v1 import (
    AUTONOMOUS_WORLD_OBSERVATION_REVIEW_RULES,
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS,
    CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES,
    COMPONENT_MATRIX_REVIEW_FIELDS,
    EMOTION_ENGINE_REVIEW_RULES,
    EVOLUTIONARY_RECURSION_REVIEW_RULES,
    FINAL_DECISION_GO,
    FIXED_SEED_CORE_INVARIANT_CHECKS,
    IDENTITY_BOUNDARY_RULES,
    INVARIANT_FIXED,
    LUNA_1_0_FORM,
    LUNA_2_0_TARGET,
    MIGRATION_RISKS,
    MODULE_HEALTH_PERMISSION_RUNTIME_RULES,
    MODULE_REGISTRATION_PLAN,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PERSONAL_CONTINUITY_COVERAGE,
    PERSONAL_CONTINUITY_REVIEW_CONFIRMATIONS,
    PHASE_ID,
    PLUGGABLE_CAPABILITY_MODULES,
    PLUGGABLE_LAYER_CONFIRMATIONS,
    PLUGGABLE_VARIABLE,
    PRODUCT_FORM_TOPOLOGY_CONFIRMATIONS,
    PRODUCT_TOPOLOGY_REVIEW_FIELDS,
    SCOPE,
    SEED_CORE_DRYRUN_CONFIRMATIONS,
    SEED_CORE_ZONE_FORBIDDEN,
    SEED_CORE_ZONE_INFLUENCES,
    SURVIVAL_DRIVE_SUBMODULES,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.seed_core_pluggable_layer_architecture_planning_v1 import (
    CAPABILITY_MODULE_CONTRACT_FIELDS,
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)

MIN_CHECKS = 364

REQUIRED = (
    "seed_core_pluggable_layer_dryrun_review_policy_v1.json",
    "seed_core_pluggable_layer_planning_input_review_v1.json",
    "seed_core_pluggable_layer_architecture_candidate_v1.json",
    "fixed_seed_core_dryrun_review_v1.json",
    "seed_core_component_matrix_review_v1.json",
    "survival_drive_placeholder_review_v1.json",
    "personal_continuity_module_review_v1.json",
    "pluggable_capability_layer_review_v1.json",
    "capability_module_contract_review_v1.json",
    "capability_bus_placeholder_review_v1.json",
    "capability_bus_responsibility_matrix_review_v1.json",
    "product_form_topology_review_v1.json",
    "invariant_vs_pluggable_boundary_review_v1.json",
    "seed_core_to_cognitive_zone_influence_review_v1.json",
    "personal_continuity_identity_boundary_review_v1.json",
    "module_registration_discovery_review_v1.json",
    "module_health_permission_runtime_review_v1.json",
    "migration_backup_restore_risk_review_v1.json",
    "seed_core_pluggable_layer_boundary_audit_v1.json",
    "seed_core_pluggable_layer_blocked_path_result_v1.json",
    "seed_core_pluggable_layer_closure_decision_v1.json",
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
            "seed_core_pluggable_layer_architecture_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--seed-core-pluggable-planning-root",
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
    plan_root = Path(args.seed_core_pluggable_planning_root)
    cz_dr_root = Path(args.cognitive_zoning_dryrun_root)
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    cr_dr_root = Path(args.controlled_runtime_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    cz_dr_vr = _load(cz_dr_root / "verifier_report.json")
    provider_dr_vr = _load(provider_dr_root / "verifier_report.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    cr_dr_vr = _load(cr_dr_root / "verifier_report.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_final_expected", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.planning_next_expected", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.cz_dr_go", cz_dr_vr.get("verifier") == "GO")
    ok("upstream.cz_dr_final", _load(cz_dr_root / "summary.json").get("final_decision") == CZ_DR_FINAL)
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_DR_FINAL)
    ok("upstream.cr_dr_go", cr_dr_vr.get("verifier") == "GO")

    summary = _load(root / "summary.json")
    policy = _load(root / "seed_core_pluggable_layer_dryrun_review_policy_v1.json")
    input_review = _load(root / "seed_core_pluggable_layer_planning_input_review_v1.json")
    candidate = _load(root / "seed_core_pluggable_layer_architecture_candidate_v1.json")
    seed_review = _load(root / "fixed_seed_core_dryrun_review_v1.json")
    matrix_review = _load(root / "seed_core_component_matrix_review_v1.json")
    survival = _load(root / "survival_drive_placeholder_review_v1.json")
    continuity = _load(root / "personal_continuity_module_review_v1.json")
    pluggable = _load(root / "pluggable_capability_layer_review_v1.json")
    contract = _load(root / "capability_module_contract_review_v1.json")
    bus = _load(root / "capability_bus_placeholder_review_v1.json")
    bus_matrix = _load(root / "capability_bus_responsibility_matrix_review_v1.json")
    product = _load(root / "product_form_topology_review_v1.json")
    invariant = _load(root / "invariant_vs_pluggable_boundary_review_v1.json")
    seed_zone = _load(root / "seed_core_to_cognitive_zone_influence_review_v1.json")
    identity = _load(root / "personal_continuity_identity_boundary_review_v1.json")
    registration = _load(root / "module_registration_discovery_review_v1.json")
    health = _load(root / "module_health_permission_runtime_review_v1.json")
    migration = _load(root / "migration_backup_restore_risk_review_v1.json")
    boundary_audit = _load(root / "seed_core_pluggable_layer_boundary_audit_v1.json")
    blocked = _load(root / "seed_core_pluggable_layer_blocked_path_result_v1.json")
    closure = _load(root / "seed_core_pluggable_layer_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.simulated_go", summary.get("system_level_simulated_go") is True)
    ok("summary.candidate_gen", summary.get("seed_core_pluggable_layer_architecture_candidate_generated") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.four_layer", summary.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("dryrun_not_runtime_not_hardware_not_split") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.simulated_go", input_review.get("system_level_simulated_go") is True)
    ok("input.arch_id", input_review.get("architecture_model") == "luna_seed_core_pluggable_layer_architecture_v1")

    ok("cand.id", candidate.get("architecture_id") == "luna_seed_core_pluggable_layer_architecture_v1")
    ok("cand.type", candidate.get("architecture_type") == "modular_life_architecture")
    ok("cand.luna_1_0", candidate.get("luna_1_0_form") == LUNA_1_0_FORM)
    ok("cand.luna_2_0", candidate.get("luna_2_0_target") == LUNA_2_0_TARGET)
    ok("cand.seed_core", candidate.get("fixed_seed_core_required") is True)
    ok("cand.continuity", candidate.get("personal_continuity_module_required") is True)
    ok("cand.pluggable", candidate.get("pluggable_capability_layer_required") is True)
    ok("cand.bus", candidate.get("luna_capability_bus_required") is True)
    ok("cand.gov", candidate.get("reusable_governance_standard_layer_required") is True)
    ok("cand.product_var", candidate.get("product_form_layer_variable") is True)
    ok("cand.no_brain", candidate.get("no_universal_brain") is True)
    ok("cand.no_sovereignty", candidate.get("no_module_sovereignty") is True)
    ok("cand.runtime_false", candidate.get("runtime_enabled_now") is False)
    ok("cand.hw_false", candidate.get("hardware_implementation_started_now") is False)
    ok("cand.candidate_only", candidate.get("candidate_only") is True)

    ok("seed.pass", seed_review.get("dryrun_and_review_pass") is True)
    ok("seed.count7", seed_review.get("component_count") == 7)
    for inv in FIXED_SEED_CORE_INVARIANT_CHECKS:
        ok(f"seed.inv.{inv[:18]}", inv in (seed_review.get("invariant_checks") or []))
    for conf in SEED_CORE_DRYRUN_CONFIRMATIONS:
        ok(f"seed.conf.{conf[:18]}", conf in (seed_review.get("confirmations") or []))
    for comp in SEED_CORE_COMPONENTS:
        ok(f"seed.comp.{comp[:18]}", comp in (seed_review.get("components") or []))

    ok("matrix.pass", matrix_review.get("dryrun_and_review_pass") is True)
    ok("matrix.count7", matrix_review.get("component_count") == 7)
    for cr in matrix_review.get("component_reviews") or []:
        cid = cr.get("component_id", "unknown")
        ok(f"matrix.{cid}.pass", cr.get("dryrun_and_review_pass") is True)

    ok("survival.pass", survival.get("dryrun_and_review_pass") is True)
    ok("survival.count6", survival.get("submodule_count") == 6)
    for sub in SURVIVAL_DRIVE_SUBMODULES:
        ok(f"survival.{sub[:18]}", sub in (survival.get("future_submodules") or []))
    for rule in EMOTION_ENGINE_REVIEW_RULES:
        ok(f"emotion.{rule[:18]}", rule in (survival.get("emotion_engine", {}).get("rules") or []))
    for rule in EVOLUTIONARY_RECURSION_REVIEW_RULES:
        ok(f"evo.{rule[:18]}", rule in (survival.get("evolutionary_recursion", {}).get("rules") or []))
    ok("evo.proposal_only", survival.get("evolutionary_recursion", {}).get("proposal_only") is True)
    for rule in AUTONOMOUS_WORLD_OBSERVATION_REVIEW_RULES:
        ok(f"awo.{rule[:18]}", rule in (survival.get("autonomous_world_observation", {}).get("rules") or []))

    ok("continuity.pass", continuity.get("dryrun_and_review_pass") is True)
    ok("continuity.id", continuity.get("module_id") == "luna_personal_continuity_module_v1")
    ok("continuity.runtime_false", continuity.get("runtime_enabled_now") is False)
    ok("continuity.write_false", continuity.get("memory_write_enabled_now") is False)
    ok("continuity.count10", continuity.get("coverage_count") == 10)
    for cov in PERSONAL_CONTINUITY_COVERAGE:
        ok(f"continuity.cov.{cov[:18]}", cov in (continuity.get("coverage") or []))
    for conf in PERSONAL_CONTINUITY_REVIEW_CONFIRMATIONS:
        ok(f"continuity.conf.{conf[:18]}", conf in (continuity.get("confirmations") or []))

    ok("plug.pass", pluggable.get("dryrun_and_review_pass") is True)
    ok("plug.count13", pluggable.get("module_count") == 13)
    for mod in PLUGGABLE_CAPABILITY_MODULES:
        ok(f"plug.mod.{mod[:18]}", mod in (pluggable.get("capability_modules") or []))
    for conf in PLUGGABLE_LAYER_CONFIRMATIONS:
        ok(f"plug.conf.{conf[:18]}", conf in (pluggable.get("confirmations") or []))

    ok("contract.pass", contract.get("dryrun_and_review_pass") is True)
    ok("contract.count13", contract.get("contract_count") == 13)
    for field in CAPABILITY_MODULE_CONTRACT_FIELDS:
        ok(f"contract.field.{field[:18]}", field in (contract.get("required_fields") or []))

    ok("bus.pass", bus.get("dryrun_and_review_pass") is True)
    ok("bus.count12", bus.get("responsibility_count") == 12)
    ok("bus.runtime_false", bus.get("capability_bus_runtime_enabled_now") is False)
    for resp in CAPABILITY_BUS_ARCHITECTURE_RESPONSIBILITIES:
        ok(f"bus.{resp[:18]}", resp in (bus.get("responsibilities") or []))
    for conf in CAPABILITY_BUS_ARCHITECTURE_CONFIRMATIONS:
        ok(f"bus.conf.{conf[:18]}", conf in (bus.get("confirmations") or []))

    ok("bus_matrix.pass", bus_matrix.get("dryrun_and_review_pass") is True)
    ok("bus_matrix.count12", bus_matrix.get("responsibility_count") == 12)

    ok("product.pass", product.get("dryrun_and_review_pass") is True)
    ok("product.count7", product.get("form_count") == 7)
    for form in PRODUCT_FORMS:
        ok(f"product.{form[:18]}", any(
            f.get("product_form") == form for f in (product.get("product_forms") or [])
        ))
    for conf in PRODUCT_FORM_TOPOLOGY_CONFIRMATIONS:
        ok(f"product.conf.{conf[:18]}", conf in (product.get("confirmations") or []))

    ok("inv.pass", invariant.get("dryrun_and_review_pass") is True)
    ok("inv.count9", invariant.get("invariant_count") == 9)
    ok("inv.plug9", invariant.get("pluggable_count") == 9)
    for item in INVARIANT_FIXED:
        ok(f"inv.fixed.{item[:18]}", item in (invariant.get("invariant_fixed") or []))
    for item in PLUGGABLE_VARIABLE:
        ok(f"inv.plug.{item[:18]}", item in (invariant.get("pluggable_variable") or []))

    ok("seed_zone.pass", seed_zone.get("dryrun_and_review_pass") is True)
    ok("seed_zone.count9", seed_zone.get("influence_count") == 9)
    for inf in SEED_CORE_ZONE_INFLUENCES:
        ok(
            f"seed_zone.inf.{inf['influence'][:18]}",
            any(i.get("influence") == inf["influence"] for i in (seed_zone.get("influences") or [])),
        )
    for forbidden in SEED_CORE_ZONE_FORBIDDEN:
        ok(f"seed_zone.forbid.{forbidden[:18]}", forbidden in (seed_zone.get("forbidden_direct_actions") or []))

    ok("identity.pass", identity.get("dryrun_and_review_pass") is True)
    ok("identity.count8", identity.get("rule_count") == 8)
    for rule in IDENTITY_BOUNDARY_RULES:
        ok(f"identity.{rule[:18]}", rule in (identity.get("rules") or []))

    ok("reg.pass", registration.get("dryrun_and_review_pass") is True)
    ok("reg.count9", registration.get("step_count") == 9)
    for step in MODULE_REGISTRATION_PLAN:
        ok(f"reg.{step[:18]}", step in (registration.get("registration_steps") or []))

    ok("health.pass", health.get("dryrun_and_review_pass") is True)
    ok("health.count7", health.get("rule_count") == 7)
    for rule in MODULE_HEALTH_PERMISSION_RUNTIME_RULES:
        ok(f"health.{rule[:18]}", rule in (health.get("rules") or []))

    ok("migration.pass", migration.get("dryrun_and_review_pass") is True)
    ok("migration.count10", migration.get("risk_count") == 10)
    for risk in MIGRATION_RISKS:
        entry = next((r for r in (migration.get("risks") or []) if r.get("risk_id") == risk), None)
        ok(f"migration.{risk[:18]}", entry is not None and entry.get("review_only") is True)

    ok("audit.pass", boundary_audit.get("audit_pass") is True)
    for field in BOUNDARY_FALSE:
        ok(f"audit.{field}", boundary_audit.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count15", blocked.get("blocked_count") == 15)
    blocked_ids = [b.get("path_id") for b in (blocked.get("blocked_paths") or [])]
    for path in BLOCKED_PATHS:
        ok(f"blocked.{path[:18]}", path in blocked_ids)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_drive_signal_contract_planning") is True)
    ok("next.phase", next_route.get("selected_next_phase") == NEXT_PHASE_GO)

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
