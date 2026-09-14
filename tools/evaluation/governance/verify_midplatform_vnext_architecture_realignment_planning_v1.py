#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform vNext Architecture Realignment Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_controlled_runtime_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as CR_DR_FINAL,
)
from capabilities.governance.midplatform_vnext_architecture_realignment_planning_v1 import (
    BLOCKED_ROUTES,
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    COGNITIVE_ZONES,
    COGNITIVE_ZONING_CONFIRMATIONS,
    CONTROLLED_RUNTIME_CONFIRMATIONS,
    DEFERRED_PHASES,
    DEFERRED_RUNTIMES,
    FINAL_DECISION_GO,
    GOVERNANCE_STANDARD_CONFIRMATIONS,
    GOVERNANCE_STANDARDS,
    INVARIANT_BOUNDARIES,
    NEXT_PHASE_GO,
    NO_MODULE_SOVEREIGNTY_RULES,
    NO_UNIVERSAL_BRAIN_RULES,
    NON_CLAIMS,
    PHASE_ID,
    PLUGGABLE_CAPABILITY_CONFIRMATIONS,
    PLUGGABLE_CAPABILITY_TYPES,
    PRODUCT_FORM_CONFIRMATIONS,
    PRODUCT_FORMS,
    RECOMMENDED_PHASE_SEQUENCE,
    SCOPE,
    SEED_CORE_COMPONENTS,
    SEED_CORE_CONFIRMATIONS,
    UPSTREAM_CONTROLLED_RUNTIME_DR_FINAL,
    VARIANT_BOUNDARIES,
    VNEXT_LAYERS,
    WORK_RHYTHM_CONFIRMATIONS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE

MIN_CHECKS = 206

REQUIRED = (
    "midplatform_vnext_architecture_realignment_policy_v1.json",
    "controlled_runtime_closure_input_review_v1.json",
    "midplatform_vnext_layer_model_v1.json",
    "fixed_seed_core_positioning_v1.json",
    "reusable_governance_standard_layer_v1.json",
    "cognitive_zoning_positioning_v1.json",
    "pluggable_capability_layer_positioning_v1.json",
    "controlled_runtime_layer_positioning_v1.json",
    "product_form_layer_positioning_v1.json",
    "no_universal_midplatform_brain_policy_v1.json",
    "no_module_sovereignty_policy_v1.json",
    "invariant_vs_variant_boundary_matrix_v1.json",
    "post_detection_work_rhythm_plan_v1.json",
    "downstream_phase_sequence_decision_v1.json",
    "deferred_runtime_register_v1.json",
    "non_claims_register_v1.json",
    "midplatform_vnext_architecture_realignment_decision_v1.json",
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
    args = p.parse_args()
    root = Path(args.output_root)
    cr_dr_root = Path(args.controlled_runtime_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    cr_dr_vr = _load(cr_dr_root / "verifier_report.json")
    cr_dr_sm = _load(cr_dr_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "midplatform_vnext_architecture_realignment_policy_v1.json")
    input_review = _load(root / "controlled_runtime_closure_input_review_v1.json")
    layer_model = _load(root / "midplatform_vnext_layer_model_v1.json")
    seed_core = _load(root / "fixed_seed_core_positioning_v1.json")
    governance = _load(root / "reusable_governance_standard_layer_v1.json")
    cognitive = _load(root / "cognitive_zoning_positioning_v1.json")
    pluggable = _load(root / "pluggable_capability_layer_positioning_v1.json")
    cr_layer = _load(root / "controlled_runtime_layer_positioning_v1.json")
    product = _load(root / "product_form_layer_positioning_v1.json")
    no_brain = _load(root / "no_universal_midplatform_brain_policy_v1.json")
    no_sovereignty = _load(root / "no_module_sovereignty_policy_v1.json")
    inv_var = _load(root / "invariant_vs_variant_boundary_matrix_v1.json")
    rhythm = _load(root / "post_detection_work_rhythm_plan_v1.json")
    downstream = _load(root / "downstream_phase_sequence_decision_v1.json")
    deferred_rt = _load(root / "deferred_runtime_register_v1.json")
    decision = _load(root / "midplatform_vnext_architecture_realignment_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.cr_dr_go", cr_dr_vr.get("verifier") == "GO")
    ok("upstream.cr_dr_final", cr_dr_sm.get("final_decision") == CR_DR_FINAL)
    ok("upstream.cr_dr_final_expected", cr_dr_sm.get("final_decision") == UPSTREAM_CONTROLLED_RUNTIME_DR_FINAL)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("architecture_realignment_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.simulated_go", summary.get("system_level_simulated_go") is True)
    ok("summary.vnext", summary.get("midplatform_vnext") is True)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.vnext", policy.get("midplatform_vnext") is True)
    ok("policy.not_refactor", policy.get("not_runtime_not_refactor") is True)
    ok("policy.layers7", policy.get("layer_count") == 7)
    ok("policy.four_layer", policy.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.simulated_go", input_review.get("system_level_simulated_go") is True)
    ok("input.no_leakage", input_review.get("no_runtime_leakage_in_upstream") is True)

    ok("layer.name", layer_model.get("architecture_name") == "Luna Midplatform vNext")
    ok("layer.count7", layer_model.get("layer_count") == 7)
    for layer in VNEXT_LAYERS:
        ok(
            f"layer.{layer['layer_id']}",
            any(l.get("layer_id") == layer["layer_id"] for l in (layer_model.get("layers") or [])),
        )

    ok("seed.count7", seed_core.get("component_count") == 7)
    ok("seed.fixed", seed_core.get("fixed_invariant") is True)
    for comp in SEED_CORE_COMPONENTS:
        ok(f"seed.{comp[:18]}", comp in (seed_core.get("components") or []))
    for conf in SEED_CORE_CONFIRMATIONS:
        ok(f"seed.conf.{conf[:18]}", conf in (seed_core.get("confirmations") or []))

    ok("gov.count10", governance.get("standard_count") == 10)
    for std in GOVERNANCE_STANDARDS:
        ok(f"gov.{std[:18]}", std in (governance.get("standards") or []))
    for conf in GOVERNANCE_STANDARD_CONFIRMATIONS:
        ok(f"gov.conf.{conf[:18]}", conf in (governance.get("confirmations") or []))

    ok("cog.count8", cognitive.get("zone_count") == 8)
    for zone in COGNITIVE_ZONES:
        ok(f"cog.{zone[:18]}", zone in (cognitive.get("zones") or []))
    for conf in COGNITIVE_ZONING_CONFIRMATIONS:
        ok(f"cog.conf.{conf[:18]}", conf in (cognitive.get("confirmations") or []))

    for cap in PLUGGABLE_CAPABILITY_TYPES:
        ok(f"plug.{cap[:18]}", cap in (pluggable.get("capability_types") or []))
    for conf in PLUGGABLE_CAPABILITY_CONFIRMATIONS:
        ok(f"plug.conf.{conf[:18]}", conf in (pluggable.get("confirmations") or []))

    ok("cr_layer.off", cr_layer.get("runtime_opened_now") is False)
    for conf in CONTROLLED_RUNTIME_CONFIRMATIONS:
        ok(f"cr.conf.{conf[:18]}", conf in (cr_layer.get("confirmations") or []))

    ok("product.count7", product.get("form_count") == 7)
    for form in PRODUCT_FORMS:
        ok(f"product.{form[:18]}", form in (product.get("product_forms") or []))
    for conf in PRODUCT_FORM_CONFIRMATIONS:
        ok(f"product.conf.{conf[:18]}", conf in (product.get("confirmations") or []))

    ok("brain.count6", no_brain.get("rule_count") == 6)
    for rule in NO_UNIVERSAL_BRAIN_RULES:
        ok(f"brain.{rule[:18]}", rule in (no_brain.get("rules") or []))

    ok("sov.count7", no_sovereignty.get("rule_count") == 7)
    for rule in NO_MODULE_SOVEREIGNTY_RULES:
        ok(f"sov.{rule[:18]}", rule in (no_sovereignty.get("rules") or []))

    ok("inv.count7", inv_var.get("invariant_count") == 7)
    ok("var.count8", inv_var.get("variant_count") == 8)
    for item in INVARIANT_BOUNDARIES:
        ok(f"inv.{item[:18]}", item in (inv_var.get("invariant") or []))
    for item in VARIANT_BOUNDARIES:
        ok(f"var.{item[:18]}", item in (inv_var.get("variant") or []))

    ok("rhythm.seq8", rhythm.get("sequence_count") == 8)
    for conf in WORK_RHYTHM_CONFIRMATIONS:
        ok(f"rhythm.{conf[:18]}", conf in (rhythm.get("confirmations") or []))
    for phase in RECOMMENDED_PHASE_SEQUENCE:
        ok(f"rhythm.phase.{phase[:18]}", phase in (rhythm.get("recommended_sequence") or []))

    ok("down.next", downstream.get("selected_next_phase") == NEXT_PHASE_GO)
    ok("down.deferred4", downstream.get("deferred_count") == 4)
    ok("down.blocked5", downstream.get("blocked_count") == 5)
    for phase in DEFERRED_PHASES:
        ok(f"down.defer.{phase[:18]}", phase in (downstream.get("deferred_phases") or []))
    for route in BLOCKED_ROUTES:
        ok(f"down.block.{route[:18]}", route in (downstream.get("blocked_routes") or []))

    ok("deferred_rt.count8", deferred_rt.get("deferred_count") == 8)
    ok("deferred_rt.not_cancelled", deferred_rt.get("deferred_not_cancelled") is True)
    for rt in DEFERRED_RUNTIMES:
        ok(f"deferred_rt.{rt[:18]}", rt in (deferred_rt.get("deferred_runtimes") or []))

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)

    for claim in NON_CLAIMS:
        ok(f"non_claim.{claim[:18]}", claim in (non_claims.get("non_claims") or []))

    total = len(checks)
    passed = sum(1 for c in checks if c["passed"])
    verifier = "GO" if passed == total and passed >= (MIN_CHECKS if MIN_CHECKS else total) else "NO_GO"
    report = {
        "phase": PHASE_ID,
        "verifier": verifier,
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
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
