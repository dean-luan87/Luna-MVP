#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Cognitive Zoning Architecture DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_cognitive_zoning_architecture_dryrun_and_review_v1 import (
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_BUS_CONFIRMATIONS,
    CAPABILITY_BUS_RESPONSIBILITIES,
    FINAL_DECISION_GO,
    GOVERNANCE_STANDARDS,
    HANDOFF_REVIEW_RULES,
    MODULE_SPLIT_PRINCIPLES,
    MONOLITHIC_TO_MODULAR_CONFIRMATIONS,
    NEXT_PHASE_GO,
    NO_UNIVERSAL_BRAIN_REVIEW_RULES,
    NON_CLAIMS,
    PHASE_ID,
    PLUGGABLE_REVIEW_ITEMS,
    SCOPE,
    SEED_CORE_FORBIDDEN_DIRECT,
    SEED_CORE_INFLUENCES,
    SIGNAL_COMMUNICATION_OBJECTS,
    SIGNAL_CONTRACT_REQUIREMENTS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
    ZONE_BOUNDARY_REVIEW_RULES,
    ZONE_COMMON_FIELDS,
    ZONE_RESPONSIBILITY_RULES,
)
from capabilities.governance.midplatform_cognitive_zoning_architecture_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL,
    NEXT_PHASE_GO as PLANNING_NEXT,
)
from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as FMIS_DR_FINAL,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    COGNITIVE_ZONES,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL,
)

MIN_CHECKS = 404

REQUIRED = (
    "cognitive_zoning_dryrun_review_policy_v1.json",
    "cognitive_zoning_planning_input_review_v1.json",
    "cognitive_zoning_model_candidate_v1.json",
    "zone_inventory_dryrun_review_v1.json",
    "zone_responsibility_matrix_review_v1.json",
    "zone_boundary_policy_review_v1.json",
    "zone_signal_contract_review_v1.json",
    "no_universal_brain_policy_review_v1.json",
    "monolithic_to_modular_life_architecture_review_v1.json",
    "capability_bus_positioning_review_v1.json",
    "zone_to_seed_core_dependency_review_v1.json",
    "zone_to_governance_standard_dependency_review_v1.json",
    "zone_to_pluggable_capability_dependency_review_v1.json",
    "zone_communication_handoff_review_v1.json",
    "future_module_split_principle_review_v1.json",
    "cognitive_zoning_boundary_audit_v1.json",
    "cognitive_zoning_blocked_path_result_v1.json",
    "cognitive_zoning_closure_decision_v1.json",
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
            "midplatform_cognitive_zoning_architecture_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--cognitive-zoning-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_cognitive_zoning_architecture_planning"
        ),
    )
    p.add_argument(
        "--controlled-runtime-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_controlled_runtime_dryrun_and_review"
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
        "--fmis-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_frontend_model_influence_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--e2e-simulation-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
        ),
    )
    args = p.parse_args()
    root = Path(args.output_root)
    plan_root = Path(args.cognitive_zoning_planning_root)
    cr_dr_root = Path(args.controlled_runtime_dryrun_root)
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    fmis_dr_root = Path(args.fmis_dryrun_root)
    e2e_dr_root = Path(args.e2e_simulation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(plan_root / "verifier_report.json")
    plan_sm = _load(plan_root / "summary.json")
    cr_dr_vr = _load(cr_dr_root / "verifier_report.json")
    cr_dr_sm = _load(cr_dr_root / "summary.json")
    provider_dr_vr = _load(provider_dr_root / "verifier_report.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    fmis_dr_vr = _load(fmis_dr_root / "verifier_report.json")
    fmis_dr_sm = _load(fmis_dr_root / "summary.json")
    e2e_dr_vr = _load(e2e_dr_root / "verifier_report.json")
    e2e_dr_sm = _load(e2e_dr_root / "summary.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_final_expected", plan_sm.get("final_decision") == PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)
    ok("upstream.planning_next_expected", plan_sm.get("recommended_next_phase") == PLANNING_NEXT)
    ok("upstream.cr_dr_go", cr_dr_vr.get("verifier") == "GO")
    ok("upstream.cr_dr_final", cr_dr_sm.get("final_decision") == CR_DR_FINAL)
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_DR_FINAL)
    ok("upstream.fmis_go", fmis_dr_vr.get("verifier") == "GO")
    ok("upstream.fmis_final", fmis_dr_sm.get("final_decision") == FMIS_DR_FINAL)
    ok("upstream.e2e_go", e2e_dr_vr.get("verifier") == "GO")
    ok("upstream.e2e_final", e2e_dr_sm.get("final_decision") == E2E_DR_FINAL)

    summary = _load(root / "summary.json")
    policy = _load(root / "cognitive_zoning_dryrun_review_policy_v1.json")
    input_review = _load(root / "cognitive_zoning_planning_input_review_v1.json")
    model = _load(root / "cognitive_zoning_model_candidate_v1.json")
    inv_review = _load(root / "zone_inventory_dryrun_review_v1.json")
    resp_review = _load(root / "zone_responsibility_matrix_review_v1.json")
    boundary_review = _load(root / "zone_boundary_policy_review_v1.json")
    signal_review = _load(root / "zone_signal_contract_review_v1.json")
    brain_review = _load(root / "no_universal_brain_policy_review_v1.json")
    mono_review = _load(root / "monolithic_to_modular_life_architecture_review_v1.json")
    bus_review = _load(root / "capability_bus_positioning_review_v1.json")
    seed_review = _load(root / "zone_to_seed_core_dependency_review_v1.json")
    gov_review = _load(root / "zone_to_governance_standard_dependency_review_v1.json")
    plug_review = _load(root / "zone_to_pluggable_capability_dependency_review_v1.json")
    handoff_review = _load(root / "zone_communication_handoff_review_v1.json")
    split_review = _load(root / "future_module_split_principle_review_v1.json")
    boundary_audit = _load(root / "cognitive_zoning_boundary_audit_v1.json")
    blocked = _load(root / "cognitive_zoning_blocked_path_result_v1.json")
    closure = _load(root / "cognitive_zoning_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.simulated_go", summary.get("system_level_simulated_go") is True)
    ok("summary.model_generated", summary.get("cognitive_zoning_model_candidate_generated") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.four_layer", summary.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.dryrun_only", policy.get("dryrun_not_runtime_not_split") is True)
    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.simulated_go", input_review.get("system_level_simulated_go") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("model.id", model.get("model_id") == "cognitive_zoning_architecture_v1")
    ok("model.type", model.get("architecture_type") == "distributed_cognitive_zoning")
    ok("model.luna_1_0", model.get("luna_1_0_form") == "monolithic_integration_validation_form")
    ok("model.luna_2_0", model.get("luna_2_0_target") == "modular_life_architecture")
    ok("model.no_brain", model.get("no_universal_brain") is True)
    ok("model.seed_core", model.get("fixed_seed_core_required") is True)
    ok("model.gov_layer", model.get("reusable_governance_standard_layer_required") is True)
    ok("model.pluggable", model.get("pluggable_capability_layer_required") is True)
    ok("model.bus_future", model.get("capability_bus_future_required") is True)
    ok("model.runtime_false", model.get("runtime_enabled_now") is False)
    ok("model.split_false", model.get("module_split_executed_now") is False)
    ok("model.candidate_only", model.get("candidate_only") is True)
    ok("model.zone8", model.get("zone_count") == 8)
    ok("model.no_single_owner", model.get("no_single_model_owns_all_zones") is True)

    zones = model.get("zones") or []
    for zone_name in COGNITIVE_ZONES:
        ok(f"inv.name.{zone_name[:18]}", zone_name in (inv_review.get("zones_present") or []))
    ok("inv.count8", inv_review.get("zone_count") == 8)
    ok("inv.no_universal", inv_review.get("no_zone_marked_universal_owner") is True)
    ok("inv.pass", inv_review.get("dryrun_and_review_pass") is True)

    for defn_zid in ZONE_RESPONSIBILITY_RULES:
        zone = next((z for z in zones if z.get("zone_id") == defn_zid), None)
        ok(f"zone.present.{defn_zid}", zone is not None)
        if zone:
            for field in ZONE_COMMON_FIELDS:
                ok(f"zone.field.{defn_zid}.{field}", field in zone)
            ok(f"zone.candidate.{defn_zid}", zone.get("candidate_only_outputs_by_default") is True)
            ok(f"zone.not_universal.{defn_zid}", zone.get("universal_owner") is False)
            if defn_zid == "execution_zone":
                ok(f"zone.exec.{defn_zid}", zone.get("cannot_directly_execute") is False)
            else:
                ok(f"zone.noexec.{defn_zid}", zone.get("cannot_directly_execute") is True)

    ok("resp.pass", resp_review.get("dryrun_and_review_pass") is True)
    ok("resp.count8", resp_review.get("zone_count") == 8)
    for zid, rules in ZONE_RESPONSIBILITY_RULES.items():
        zr = next((r for r in (resp_review.get("zone_reviews") or []) if r.get("zone_id") == zid), None)
        ok(f"resp.zone.{zid}", zr is not None and zr.get("dryrun_and_review_pass") is True)
        for rule in rules:
            ok(f"resp.rule.{zid}.{rule[:18]}", zr and rule in (zr.get("rules") or []))

    ok("boundary.pass", boundary_review.get("dryrun_and_review_pass") is True)
    ok("boundary.count7", boundary_review.get("rule_count") == 7)
    for rule in ZONE_BOUNDARY_REVIEW_RULES:
        ok(f"boundary.{rule[:18]}", rule in (boundary_review.get("rules") or []))

    ok("signal.pass", signal_review.get("dryrun_and_review_pass") is True)
    for obj in SIGNAL_COMMUNICATION_OBJECTS:
        ok(f"signal.obj.{obj[:18]}", obj in (signal_review.get("communication_objects") or []))
    for req in SIGNAL_CONTRACT_REQUIREMENTS:
        ok(f"signal.req.{req[:18]}", req in (signal_review.get("requirements") or []))

    ok("brain.pass", brain_review.get("dryrun_and_review_pass") is True)
    ok("brain.count7", brain_review.get("rule_count") == 7)
    for rule in NO_UNIVERSAL_BRAIN_REVIEW_RULES:
        ok(f"brain.{rule[:18]}", rule in (brain_review.get("rules") or []))

    ok("mono.pass", mono_review.get("dryrun_and_review_pass") is True)
    for conf in MONOLITHIC_TO_MODULAR_CONFIRMATIONS:
        ok(f"mono.{conf[:18]}", conf in (mono_review.get("confirmations") or []))

    ok("bus.pass", bus_review.get("dryrun_and_review_pass") is True)
    ok("bus.count12", bus_review.get("responsibility_count") == 12)
    ok("bus.runtime_false", bus_review.get("capability_bus_runtime_enabled_now") is False)
    for resp in CAPABILITY_BUS_RESPONSIBILITIES:
        ok(f"bus.{resp[:18]}", resp in (bus_review.get("responsibilities") or []))
    for conf in CAPABILITY_BUS_CONFIRMATIONS:
        ok(f"bus.conf.{conf[:18]}", conf in (bus_review.get("confirmations") or []))

    ok("seed.pass", seed_review.get("dryrun_and_review_pass") is True)
    for inf in SEED_CORE_INFLUENCES:
        ok(
            f"seed.inf.{inf['influence'][:18]}",
            any(i.get("influence") == inf["influence"] for i in (seed_review.get("influences") or [])),
        )
    for forbidden in SEED_CORE_FORBIDDEN_DIRECT:
        ok(f"seed.forbid.{forbidden[:18]}", forbidden in (seed_review.get("forbidden_direct_actions") or []))

    ok("gov.pass", gov_review.get("dryrun_and_review_pass") is True)
    ok("gov.all_zones", gov_review.get("all_zones_bind_governance") is True)
    for std in GOVERNANCE_STANDARDS:
        ok(f"gov.std.{std[:18]}", std in (gov_review.get("governance_standards") or []))

    ok("plug.pass", plug_review.get("dryrun_and_review_pass") is True)
    for item in PLUGGABLE_REVIEW_ITEMS:
        ok(f"plug.{item[:18]}", item in (plug_review.get("review_items") or []))

    ok("handoff.pass", handoff_review.get("dryrun_and_review_pass") is True)
    for rule in HANDOFF_REVIEW_RULES:
        ok(f"handoff.{rule[:18]}", rule in (handoff_review.get("rules") or []))

    ok("split.pass", split_review.get("dryrun_and_review_pass") is True)
    ok("split.not_now", split_review.get("split_executed_now") is False)
    for principle in MODULE_SPLIT_PRINCIPLES:
        ok(f"split.{principle[:18]}", principle in (split_review.get("principles") or []))

    ok("audit.pass", boundary_audit.get("audit_pass") is True)
    ok("audit.all_false", boundary_audit.get("all_false") is True)
    for field in BOUNDARY_FALSE:
        ok(f"audit.{field}", boundary_audit.get("boundary_fields", {}).get(field) is False)

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count14", blocked.get("blocked_count") == 14)
    blocked_ids = [b.get("path_id") for b in (blocked.get("blocked_paths") or [])]
    for path in BLOCKED_PATHS:
        ok(f"blocked.{path[:18]}", path in blocked_ids)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_seed_core_pluggable_planning") is True)
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
