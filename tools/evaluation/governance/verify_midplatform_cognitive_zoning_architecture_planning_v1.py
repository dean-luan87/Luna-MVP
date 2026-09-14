#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Cognitive Zoning Architecture Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_cognitive_zoning_architecture_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CAPABILITY_BUS_CONFIRMATIONS,
    CAPABILITY_BUS_RESPONSIBILITIES,
    COGNITIVE_ZONE_DEFINITIONS,
    FINAL_DECISION_GO,
    GOVERNANCE_STANDARDS,
    HANDOFF_RULES,
    LUNA_1_0_DEFINITION,
    LUNA_1_0_VALIDATION_ITEMS,
    LUNA_2_0_DIRECTIONS,
    LUNA_2_0_TARGET,
    MODULE_SPLIT_PRINCIPLES,
    MONOLITHIC_TO_MODULAR_CONFIRMATIONS,
    NEXT_PHASE_GO,
    NO_UNIVERSAL_BRAIN_RULES,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SEED_CORE_FORBIDDEN_DIRECT,
    SEED_CORE_INFLUENCES,
    SIGNAL_CONTRACT_FIELDS,
    UPSTREAM_VNEXT_FINAL,
    ZONE_COMMON_FIELDS,
    ZONE_PLUGGABLE_BINDINGS,
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
    NEXT_PHASE_GO as VNEXT_NEXT_PHASE,
)
from capabilities.governance.provider_abstraction_standard_alignment_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as PROVIDER_DR_FINAL,
)

MIN_CHECKS = 325

REQUIRED = (
    "cognitive_zoning_architecture_planning_policy_v1.json",
    "vnext_architecture_input_review_v1.json",
    "cognitive_zone_inventory_v1.json",
    "cognitive_zone_responsibility_matrix_v1.json",
    "cognitive_zone_boundary_policy_v1.json",
    "cognitive_zone_signal_contract_v1.json",
    "no_universal_brain_zoning_policy_v1.json",
    "monolithic_validation_form_to_modular_life_architecture_plan_v1.json",
    "luna_capability_bus_positioning_v1.json",
    "zone_to_seed_core_dependency_matrix_v1.json",
    "zone_to_governance_standard_dependency_matrix_v1.json",
    "zone_to_pluggable_capability_dependency_matrix_v1.json",
    "zone_communication_and_handoff_policy_v1.json",
    "future_module_split_principle_v1.json",
    "cognitive_zoning_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "cognitive_zoning_architecture_planning_decision_v1.json",
    "summary.json",
)

ZONE_RULE_CHECKS: Dict[str, Tuple[str, ...]] = {
    "perception_zone": (
        "perception outputs observation_candidate / evidence_candidate",
        "perception does not write fact directly",
        "perception does not write WorldModel directly",
        "perception does not emit user output directly",
        "perception provider must use provider abstraction",
    ),
    "memory_worldmodel_zone": (
        "memory retrieval output is candidate/evidence",
        "memory write requires admission",
        "worldmodel write requires fact admission",
        "stale info may be history candidate, not current action fact",
    ),
    "drive_zone": (
        "drive outputs drive_signal_candidate",
        "drive does not execute action",
        "survival drive priority can influence integration/decision",
        "task drive tracks goal/progress/interrupt/resume",
        "autonomous world observation belongs under Survival Drive as observation_intent_candidate",
    ),
    "information_integration_zone": (
        "consumes candidate/evidence/drive/health/task/map/memory context",
        "emits integrated_context_candidate",
        "flags conflict/gap/freshness/priority",
        "does not make final decision",
        "does not execute runtime",
    ),
    "decision_zone": (
        "consumes integrated_context_candidate + constitution refs + validation + health + whitebox",
        "emits decision_candidate",
        "does not invoke provider",
        "does not bypass gates",
        "does not execute runtime",
    ),
    "language_output_zone": (
        "output remains layered",
        "user_output_candidate ≠ user-facing output",
        "speech_request_candidate ≠ TTS",
        "display_gate_result_candidate ≠ Display Output",
    ),
    "execution_zone": (
        "execution requires controlled runtime",
        "execution cannot read raw constitution",
        "execution cannot bypass enforcement",
        "execution cannot self-authorize",
    ),
    "governance_zone": (
        "governance standards reusable",
        "modules cannot create parallel governance",
        "governance emits constraints/gate results/health/trace, not raw execution",
    ),
}


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_cognitive_zoning_architecture_planning"
        ),
    )
    p.add_argument(
        "--vnext-realignment-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_vnext_architecture_realignment_planning"
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
    vnext_root = Path(args.vnext_realignment_root)
    cr_dr_root = Path(args.controlled_runtime_dryrun_root)
    provider_dr_root = Path(args.provider_abstraction_dryrun_root)
    fmis_dr_root = Path(args.fmis_dryrun_root)
    e2e_dr_root = Path(args.e2e_simulation_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    vnext_vr = _load(vnext_root / "verifier_report.json")
    vnext_sm = _load(vnext_root / "summary.json")
    cr_dr_vr = _load(cr_dr_root / "verifier_report.json")
    cr_dr_sm = _load(cr_dr_root / "summary.json")
    provider_dr_vr = _load(provider_dr_root / "verifier_report.json")
    provider_dr_sm = _load(provider_dr_root / "summary.json")
    fmis_dr_vr = _load(fmis_dr_root / "verifier_report.json")
    fmis_dr_sm = _load(fmis_dr_root / "summary.json")
    e2e_dr_vr = _load(e2e_dr_root / "verifier_report.json")
    e2e_dr_sm = _load(e2e_dr_root / "summary.json")

    ok("upstream.vnext_go", vnext_vr.get("verifier") == "GO")
    ok("upstream.vnext_final", vnext_sm.get("final_decision") == UPSTREAM_VNEXT_FINAL)
    ok("upstream.vnext_next", vnext_sm.get("recommended_next_phase") == VNEXT_NEXT_PHASE)
    ok("upstream.cr_dr_go", cr_dr_vr.get("verifier") == "GO")
    ok("upstream.cr_dr_final", cr_dr_sm.get("final_decision") == CR_DR_FINAL)
    ok("upstream.provider_go", provider_dr_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_dr_sm.get("final_decision") == PROVIDER_DR_FINAL)
    ok("upstream.fmis_go", fmis_dr_vr.get("verifier") == "GO")
    ok("upstream.fmis_final", fmis_dr_sm.get("final_decision") == FMIS_DR_FINAL)
    ok("upstream.e2e_go", e2e_dr_vr.get("verifier") == "GO")
    ok("upstream.e2e_final", e2e_dr_sm.get("final_decision") == E2E_DR_FINAL)

    summary = _load(root / "summary.json")
    policy = _load(root / "cognitive_zoning_architecture_planning_policy_v1.json")
    input_review = _load(root / "vnext_architecture_input_review_v1.json")
    inventory = _load(root / "cognitive_zone_inventory_v1.json")
    responsibility = _load(root / "cognitive_zone_responsibility_matrix_v1.json")
    boundary = _load(root / "cognitive_zone_boundary_policy_v1.json")
    signal_contract = _load(root / "cognitive_zone_signal_contract_v1.json")
    no_brain = _load(root / "no_universal_brain_zoning_policy_v1.json")
    monolith = _load(root / "monolithic_validation_form_to_modular_life_architecture_plan_v1.json")
    bus = _load(root / "luna_capability_bus_positioning_v1.json")
    seed_matrix = _load(root / "zone_to_seed_core_dependency_matrix_v1.json")
    gov_matrix = _load(root / "zone_to_governance_standard_dependency_matrix_v1.json")
    plug_matrix = _load(root / "zone_to_pluggable_capability_dependency_matrix_v1.json")
    handoff = _load(root / "zone_communication_and_handoff_policy_v1.json")
    split_principle = _load(root / "future_module_split_principle_v1.json")
    dryrun_plan = _load(root / "cognitive_zoning_dryrun_plan_v1.json")
    decision = _load(root / "cognitive_zoning_architecture_planning_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.luna_1_0", summary.get("luna_1_0") == LUNA_1_0_DEFINITION)
    ok("summary.luna_2_0", summary.get("luna_2_0_target") == LUNA_2_0_TARGET)
    ok("summary.four_layer", summary.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.phase", policy.get("phase") == PHASE_ID)
    ok("policy.zone8", policy.get("zone_count") == 8)
    ok("policy.not_split", policy.get("planning_not_split_not_runtime") is True)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.planning_only", input_review.get("cognitive_zoning_planning_only") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    zones = inventory.get("zones") or []
    ok("inv.count8", inventory.get("zone_count") == 8)
    for zone_name in COGNITIVE_ZONES:
        ok(f"inv.name.{zone_name[:18]}", zone_name in (inventory.get("zone_names") or []))

    for defn in COGNITIVE_ZONE_DEFINITIONS:
        zid = defn["zone_id"]
        zone = next((z for z in zones if z.get("zone_id") == zid), None)
        ok(f"zone.present.{zid}", zone is not None)
        if zone:
            for field in ZONE_COMMON_FIELDS:
                ok(f"zone.field.{zid}.{field}", field in zone)
            ok(f"zone.candidate.{zid}", zone.get("candidate_only_outputs_by_default") is True)
            if zid == "execution_zone":
                ok(f"zone.exec.{zid}", zone.get("cannot_directly_execute") is False)
            else:
                ok(f"zone.noexec.{zid}", zone.get("cannot_directly_execute") is True)
            for rule in ZONE_RULE_CHECKS.get(zid, ()):
                ok(
                    f"zone.rule.{zid}.{rule[:18]}",
                    rule in (boundary.get("zone_rules_by_zone", {}).get(zid) or []),
                )

    ok("resp.count8", responsibility.get("entry_count") == 8)

    ok("signal.fields", all(f in (signal_contract.get("required_fields") or []) for f in SIGNAL_CONTRACT_FIELDS))
    ok("signal.candidate", signal_contract.get("candidate_only_default") is True)

    ok("brain.count6", no_brain.get("rule_count") == 6)
    for rule in NO_UNIVERSAL_BRAIN_RULES:
        ok(f"brain.{rule[:18]}", rule in (no_brain.get("rules") or []))

    ok("mono.luna_1_0", monolith.get("luna_1_0_definition") == LUNA_1_0_DEFINITION)
    ok("mono.luna_2_0", monolith.get("luna_2_0_target") == LUNA_2_0_TARGET)
    ok("mono.pc_mode", monolith.get("pc_building_block_mode") is True)
    for item in LUNA_1_0_VALIDATION_ITEMS:
        ok(f"mono.val.{item[:18]}", item in (monolith.get("luna_1_0_validation_items") or []))
    for item in LUNA_2_0_DIRECTIONS:
        ok(f"mono.dir.{item[:18]}", item in (monolith.get("luna_2_0_directions") or []))
    for conf in MONOLITHIC_TO_MODULAR_CONFIRMATIONS:
        ok(f"mono.conf.{conf[:18]}", conf in (monolith.get("confirmations") or []))

    ok("bus.count12", bus.get("responsibility_count") == 12)
    ok("bus.name", bus.get("bus_name") == "Luna Capability Bus")
    for resp in CAPABILITY_BUS_RESPONSIBILITIES:
        ok(f"bus.{resp[:18]}", resp in (bus.get("responsibilities") or []))
    for conf in CAPABILITY_BUS_CONFIRMATIONS:
        ok(f"bus.conf.{conf[:18]}", conf in (bus.get("confirmations") or []))

    ok("seed.influence7", len(seed_matrix.get("influences") or []) == 7)
    for inf in SEED_CORE_INFLUENCES:
        ok(
            f"seed.inf.{inf['influence'][:18]}",
            any(
                i.get("influence") == inf["influence"] for i in (seed_matrix.get("influences") or [])
            ),
        )
    for forbidden in SEED_CORE_FORBIDDEN_DIRECT:
        ok(f"seed.forbid.{forbidden[:18]}", forbidden in (seed_matrix.get("forbidden_direct_actions") or []))

    ok("gov.standards10", len(gov_matrix.get("governance_standards") or []) == 10)
    for std in GOVERNANCE_STANDARDS:
        ok(f"gov.std.{std[:18]}", std in (gov_matrix.get("governance_standards") or []))
    ok("gov.all_zones", gov_matrix.get("all_zones_bind_governance") is True)

    for binding in ZONE_PLUGGABLE_BINDINGS:
        zid = binding["zone_id"]
        ok(
            f"plug.{zid}",
            any(b.get("zone_id") == zid for b in (plug_matrix.get("bindings") or [])),
        )

    ok("handoff.count6", handoff.get("rule_count") == 6)
    for rule in HANDOFF_RULES:
        ok(f"handoff.{rule[:18]}", rule in (handoff.get("rules") or []))

    ok("split.count8", split_principle.get("principle_count") == 8)
    ok("split.not_now", split_principle.get("split_executed_now") is False)
    for principle in MODULE_SPLIT_PRINCIPLES:
        ok(f"split.{principle[:18]}", principle in (split_principle.get("principles") or []))

    ok("dryrun.next", dryrun_plan.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.no_runtime", "no runtime enabled" in (dryrun_plan.get("dryrun_objectives") or []))
    ok("dryrun.no_split", "no module split" in (dryrun_plan.get("dryrun_objectives") or []))

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
