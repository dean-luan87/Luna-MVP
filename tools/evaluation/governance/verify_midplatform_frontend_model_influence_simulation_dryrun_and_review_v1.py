#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform Frontend Model Influence Simulation DryRunAndReview v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_dryrun_and_review_v1 import (
    FINAL_DECISION_GO as E2E_DR_FINAL_GO,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_dryrun_and_review_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_TRUE,
    CORE_SIMULATION_CHAIN,
    FINAL_DECISION_GO,
    FRONT_MODEL_TYPES,
    MODEL_IO_INFLUENCE_ASPECTS,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    PHASE_ID,
    SCOPE,
    SIMULATION_CASES,
)
from capabilities.governance.midplatform_frontend_model_influence_simulation_planning_v1 import (
    FINAL_DECISION_GO as PLANNING_FINAL_GO,
)
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)
from capabilities.governance.provider_abstraction_standard_alignment_planning_v1 import (
    FINAL_DECISION_GO as PROVIDER_ABS_PLANNING_FINAL_GO,
)

MIN_CHECKS = 227

REQUIRED = (
    "frontend_model_influence_simulation_dryrun_review_policy_v1.json",
    "frontend_model_influence_planning_input_review_v1.json",
    "front_model_type_inventory_review_v1.json",
    "model_io_contract_influence_matrix_v1.json",
    "rule_to_model_input_mapping_result_v1.json",
    "rule_to_model_output_mapping_result_v1.json",
    "health_to_model_behavior_mapping_result_v1.json",
    "enforcement_to_model_permission_mapping_result_v1.json",
    "whitebox_explainability_mapping_result_v1.json",
    "provider_abstraction_to_front_model_boundary_result_v1.json",
    "simulation_case_results_v1.json",
    "expected_vs_actual_influence_matrix_v1.json",
    "frontend_model_boundary_violation_matrix_v1.json",
    "frontend_model_traceability_matrix_v1.json",
    "case_1_normal_allowed_model_input_result_v1.json",
    "case_2_privacy_masked_input_result_v1.json",
    "case_3_uncertainty_required_output_result_v1.json",
    "case_4_safety_blocked_generation_result_v1.json",
    "case_5_health_degraded_mode_result_v1.json",
    "case_6_provider_not_ready_result_v1.json",
    "case_7_bypass_attempt_result_v1.json",
    "case_8_rule_change_propagation_result_v1.json",
    "system_level_front_model_influence_review_v1.json",
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
            "midplatform_frontend_model_influence_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_frontend_model_influence_simulation_planning"
        ),
    )
    p.add_argument(
        "--provider-abstraction-planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "provider_abstraction_standard_alignment_planning"
        ),
    )
    p.add_argument(
        "--e2e-dryrun-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--tts-runtime-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    planning_root = Path(args.planning_root)
    provider_root = Path(args.provider_abstraction_planning_root)
    e2e_root = Path(args.e2e_dryrun_root)
    tts_dr_root = Path(args.tts_runtime_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    plan_vr = _load(planning_root / "verifier_report.json")
    plan_sm = _load(planning_root / "summary.json")
    provider_vr = _load(provider_root / "verifier_report.json")
    provider_sm = _load(provider_root / "summary.json")
    e2e_vr = _load(e2e_root / "verifier_report.json")
    e2e_sm = _load(e2e_root / "summary.json")
    tts_model = _load(tts_dr_root / "tts_runtime_model_candidate_v1.json")
    tts_dr_sm = _load(tts_dr_root / "summary.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "frontend_model_influence_simulation_dryrun_review_policy_v1.json")
    input_review = _load(root / "frontend_model_influence_planning_input_review_v1.json")
    inventory_review = _load(root / "front_model_type_inventory_review_v1.json")
    io_matrix = _load(root / "model_io_contract_influence_matrix_v1.json")
    rule_in = _load(root / "rule_to_model_input_mapping_result_v1.json")
    rule_out = _load(root / "rule_to_model_output_mapping_result_v1.json")
    health_map = _load(root / "health_to_model_behavior_mapping_result_v1.json")
    enforcement_map = _load(root / "enforcement_to_model_permission_mapping_result_v1.json")
    whitebox_map = _load(root / "whitebox_explainability_mapping_result_v1.json")
    provider_boundary = _load(root / "provider_abstraction_to_front_model_boundary_result_v1.json")
    case_results = _load(root / "simulation_case_results_v1.json")
    expected_vs_actual = _load(root / "expected_vs_actual_influence_matrix_v1.json")
    boundary_violation = _load(root / "frontend_model_boundary_violation_matrix_v1.json")
    traceability = _load(root / "frontend_model_traceability_matrix_v1.json")
    system_review = _load(root / "system_level_front_model_influence_review_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")
    non_claims = _load(root / "non_claims_register_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == PLANNING_FINAL_GO)
    ok("upstream.provider_go", provider_vr.get("verifier") == "GO")
    ok("upstream.provider_final", provider_sm.get("final_decision") == PROVIDER_ABS_PLANNING_FINAL_GO)
    ok("upstream.e2e_go", e2e_vr.get("verifier") == "GO")
    ok("upstream.e2e_final", e2e_sm.get("final_decision") == E2E_DR_FINAL_GO)
    ok("upstream.tts_abstraction", tts_model.get("runtime_abstraction") is True)
    ok("upstream.qianwen_candidate", tts_model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("upstream.qianwen_not_invoked", tts_dr_sm.get("qianwen_tts_invoked_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("frontend_model_influence_simulation_dryrun_and_review_only") is True)
    ok("summary.sim_executed", summary.get("simulation_executed_now") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.cases8", summary.get("case_count") == 8)
    ok("summary.cases_passed8", summary.get("cases_passed") == 8)
    ok("summary.types8", summary.get("front_model_type_count") == 8)

    for field in BOUNDARY_TRUE:
        ok(f"summary.true.{field[:20]}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"summary.false.{field[:20]}", summary.get(field) is False)

    ok("policy.chain", policy.get("core_simulation_chain") == CORE_SIMULATION_CHAIN)
    ok("policy.sim_not_runtime", policy.get("simulation_executed_not_real_runtime") is True)

    ok("input_review.pass", input_review.get("review_pass") is True)
    ok("input_review.no_raw_constitution", input_review.get("front_models_no_raw_constitution") is True)
    ok("input_review.qianwen_reg", input_review.get("qianwen_registered_not_invoked") is True)

    ok("inventory.count8", inventory_review.get("type_count") == 8)
    ok("inventory.all_reviewed", inventory_review.get("all_types_reviewed") is True)
    ok("inventory.all_io_contract", inventory_review.get("all_consume_model_io_contract") is True)
    ok("inventory.all_no_raw", inventory_review.get("all_no_raw_constitution") is True)
    for mt in FRONT_MODEL_TYPES:
        reviewed = next(
            (x for x in (inventory_review.get("model_types") or []) if x.get("type_id") == mt["type_id"]),
            {},
        )
        ok(f"inventory.{mt['type_id']}.io", reviewed.get("consumes_model_io_contract") is True)
        ok(f"inventory.{mt['type_id']}.bundle", reviewed.get("consumes_constraint_bundle_or_enforcement_result") is True)
        ok(f"inventory.{mt['type_id']}.noraw", reviewed.get("does_not_read_raw_constitution") is True)
        ok(f"inventory.{mt['type_id']}.prov", reviewed.get("provider_abstraction_required") is True)
        ok(f"inventory.{mt['type_id']}.runtime", reviewed.get("runtime_invoked_now") is False)

    ok("io_matrix.all_aspects", io_matrix.get("all_aspects_covered") is True)
    for aspect in MODEL_IO_INFLUENCE_ASPECTS:
        ok(f"io_matrix.{aspect[:16]}", io_matrix.get("aspect_coverage", {}).get(aspect) is True)

    ok("rule_in.pass", rule_in.get("all_pass") is True)
    for key in (
        "constitution_not_in_raw_prompt",
        "resolver_output_in_model_io_contract",
        "enforcement_controls_allowed_blocked",
        "privacy_can_mask_input",
        "safety_can_block_input",
        "health_can_degrade_input_scope",
        "provider_readiness_controls_provider_call",
    ):
        ok(f"rule_in.{key[:16]}", rule_in.get("checks", {}).get(key) is True)

    ok("rule_out.pass", rule_out.get("all_pass") is True)
    for key in (
        "uncertainty_preserved",
        "required_disclosures_preserved",
        "no_unsupported_fact_expansion",
        "privacy_filtering_enforced",
        "safety_block_prevents_output",
        "tone_cannot_override_safety_privacy_uncertainty",
        "output_remains_candidate_only",
    ):
        ok(f"rule_out.{key[:16]}", rule_out.get("checks", {}).get(key) is True)

    ok("health.pass", health_map.get("all_pass") is True)
    for key in (
        "health_triggers_hold_degrade_fallback",
        "health_cannot_override_constitution_safety",
        "health_pressure_cannot_authorize_provider",
        "health_degradation_traceable",
        "health_produces_signal_not_execution",
    ):
        ok(f"health.{key[:16]}", health_map.get("checks", {}).get(key) is True)

    ok("enforcement.pass", enforcement_map.get("all_pass") is True)
    for key in (
        "safety_gate_affects_output_permission",
        "speech_gate_affects_speech_permission",
        "authorization_gate_affects_provider_permission",
        "validation_affects_model_action_permission",
        "enforcement_result_is_permission_surface",
        "front_model_cannot_bypass_enforcement",
    ):
        ok(f"enforcement.{key[:16]}", enforcement_map.get("checks", {}).get(key) is True)

    ok("whitebox.pass", whitebox_map.get("all_pass") is True)
    for key in (
        "every_influence_has_whitebox_trace",
        "masking_degrade_block_fallback_traceable",
        "rule_refs_preserved",
        "evidence_refs_preserved",
        "health_refs_preserved",
        "provider_readiness_refs_preserved",
        "no_unexplained_mutation",
    ):
        ok(f"whitebox.{key[:16]}", whitebox_map.get("checks", {}).get(key) is True)

    ok("provider_boundary.pass", provider_boundary.get("all_pass") is True)
    for key in (
        "runtime_core_not_provider",
        "provider_candidate_not_selected",
        "selected_not_invoked",
        "qianwen_registered_not_selected_invoked",
        "paddleocr_rapidocr_read_only_evidence",
        "adapter_cannot_bypass_readiness_authorization",
        "provider_output_candidate_not_fact",
    ):
        ok(f"provider.{key[:16]}", provider_boundary.get("checks", {}).get(key) is True)

    ok("case_results.all_pass", case_results.get("all_pass") is True)
    ok("case_results.count8", case_results.get("case_count") == 8)
    ok("expected.all_match", expected_vs_actual.get("all_match") is True)

    case_result_files = {
        "case_1_normal_allowed_model_input": "case_1_normal_allowed_model_input_result_v1.json",
        "case_2_privacy_masked_input": "case_2_privacy_masked_input_result_v1.json",
        "case_3_uncertainty_required_output": "case_3_uncertainty_required_output_result_v1.json",
        "case_4_safety_blocked_generation": "case_4_safety_blocked_generation_result_v1.json",
        "case_5_health_degraded_mode": "case_5_health_degraded_mode_result_v1.json",
        "case_6_provider_not_ready": "case_6_provider_not_ready_result_v1.json",
        "case_7_bypass_attempt": "case_7_bypass_attempt_result_v1.json",
        "case_8_rule_change_propagation": "case_8_rule_change_propagation_result_v1.json",
    }
    for case in SIMULATION_CASES:
        cid = case["case_id"]
        case_file = _load(root / case_result_files[cid])
        ok(f"case.{cid[:16]}.match", case_file.get("outcome_match") is True)
        ok(f"case.{cid[:16]}.sim", case_file.get("actual", {}).get("simulated") is True)
        ok(f"case.{cid[:16]}.no_runtime", case_file.get("actual", {}).get("real_front_model_invoked_now") is False)

    ok("boundary.clear", boundary_violation.get("all_boundaries_clear") is True)
    for field in BOUNDARY_FALSE:
        ok(f"boundary.{field[:16]}", boundary_violation.get("boundary_checks", {}).get(field) is False)

    ok("traceability.preserved", traceability.get("all_preserved") is True)

    ok("system.pass", system_review.get("dryrun_and_review_pass") is True)
    ok("system.influence", system_review.get("rules_influence_front_models") is True)
    ok("system.contracts", system_review.get("influence_via_contracts_not_raw_constitution") is True)
    ok("system.no_runtime", system_review.get("no_runtime_leakage") is True)

    ok("next_route.ready", next_route.get("ready_for_provider_abstraction_dryrun") is True)
    ok("next_route.go", next_route.get("front_model_influence_simulated_go") is True)
    ok("next_route.next", next_route.get("recommended_next_phase") == NEXT_PHASE_GO)

    for nc in NON_CLAIMS:
        ok(f"non_claims.{nc[:16]}", nc in (non_claims.get("non_claims") or []))

    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    report = {
        "phase": PHASE_ID,
        "scope": SCOPE,
        "verifier": "GO" if passed == total and total > 0 else "HOLD",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks": MIN_CHECKS if MIN_CHECKS else total,
        "checks": checks,
        "non_claims": list(NON_CLAIMS),
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if report["verifier"] == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
