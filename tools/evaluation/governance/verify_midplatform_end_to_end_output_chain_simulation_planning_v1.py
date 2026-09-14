#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform End-to-End Output Chain Simulation Planning v1."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from capabilities.governance.midplatform_end_to_end_output_chain_simulation_planning_v1 import (
    BOUNDARY_FALSE,
    BOUNDARY_SIMULATION_FALSE,
    BOUNDARY_TRUE,
    EXPECTED_SIMULATION_OUTPUTS,
    FINAL_DECISION_GO,
    MAIN_CHAIN,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CHAIN_STAGES,
    PHASE_ID,
    RULE_RESOLUTION_RULES,
    SCOPE,
    SIMULATION_CASES,
    SIMULATION_SCOPE_EXCLUDED,
    SIMULATION_SCOPE_INCLUDED,
    STAGE_HANDOFF_CONTRACTS,
    TRACEABILITY_FIELDS,
    UPSTREAM_REQUIREMENTS,
    UPSTREAM_TTS_DR_FINAL,
    UPSTREAM_TTS_DR_NEXT,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)

MIN_CHECKS = 299

REQUIRED = (
    "end_to_end_output_chain_simulation_planning_policy_v1.json",
    "upstream_output_chain_input_review_v1.json",
    "simulation_scope_definition_v1.json",
    "output_chain_stage_inventory_v1.json",
    "simulation_case_matrix_v1.json",
    "case_1_normal_low_risk_output_plan_v1.json",
    "case_2_missing_evidence_hold_plan_v1.json",
    "case_3_validation_fail_block_plan_v1.json",
    "case_4_high_uncertainty_disclosure_plan_v1.json",
    "case_5_privacy_risk_no_output_plan_v1.json",
    "case_6_urgent_safety_degrade_disclosure_plan_v1.json",
    "case_7_speech_forbidden_block_plan_v1.json",
    "case_8_execution_layer_bypass_attempt_block_plan_v1.json",
    "stage_handoff_contract_review_plan_v1.json",
    "rule_resolution_enforcement_execution_review_plan_v1.json",
    "traceability_preservation_review_plan_v1.json",
    "boundary_and_non_claims_review_plan_v1.json",
    "expected_simulation_outputs_contract_v1.json",
    "simulation_dryrun_plan_v1.json",
    "non_claims_register_v1.json",
    "end_to_end_output_chain_simulation_planning_decision_v1.json",
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
            "midplatform_end_to_end_output_chain_simulation_planning"
        ),
    )
    p.add_argument(
        "--tts-runtime-dryrun-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/midplatform_tts_runtime_dryrun_and_review",
    )
    args = p.parse_args()
    root = Path(args.output_root)
    tts_dr_root = Path(args.tts_runtime_dryrun_root)
    checks: List[Dict[str, Any]] = []

    def ok(cid: str, passed: bool) -> None:
        checks.append({"check_id": cid, "passed": bool(passed)})

    for f in REQUIRED:
        ok(f"file.{f}", (root / f).is_file())

    tts_dr_vr = _load(tts_dr_root / "verifier_report.json")
    tts_dr_sm = _load(tts_dr_root / "summary.json")
    tts_model = _load(tts_dr_root / "tts_runtime_model_candidate_v1.json")

    summary = _load(root / "summary.json")
    policy = _load(root / "end_to_end_output_chain_simulation_planning_policy_v1.json")
    upstream = _load(root / "upstream_output_chain_input_review_v1.json")
    scope = _load(root / "simulation_scope_definition_v1.json")
    stages = _load(root / "output_chain_stage_inventory_v1.json")
    case_matrix = _load(root / "simulation_case_matrix_v1.json")
    handoff = _load(root / "stage_handoff_contract_review_plan_v1.json")
    rule_res = _load(root / "rule_resolution_enforcement_execution_review_plan_v1.json")
    trace = _load(root / "traceability_preservation_review_plan_v1.json")
    boundary = _load(root / "boundary_and_non_claims_review_plan_v1.json")
    expected = _load(root / "expected_simulation_outputs_contract_v1.json")
    dryrun = _load(root / "simulation_dryrun_plan_v1.json")
    decision = _load(root / "end_to_end_output_chain_simulation_planning_decision_v1.json")

    ok("upstream.tts_go", tts_dr_vr.get("verifier") == "GO")
    ok("upstream.tts_final", tts_dr_sm.get("final_decision") == UPSTREAM_TTS_DR_FINAL)
    ok("upstream.tts_next", tts_dr_sm.get("recommended_next_phase") == UPSTREAM_TTS_DR_NEXT)
    ok("upstream.tts_abstraction", tts_model.get("runtime_abstraction") is True)
    ok("upstream.qianwen_candidate", tts_model.get("current_preferred_provider_candidate") == CURRENT_PREFERRED_PROVIDER_CANDIDATE)
    ok("upstream.no_qianwen_invoke", tts_dr_sm.get("qianwen_tts_invoked_now") is False)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.planning_only", summary.get("end_to_end_output_chain_simulation_planning_only") is True)
    ok("summary.pass", summary.get("planning_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.main_chain", summary.get("main_chain") == MAIN_CHAIN)
    ok("summary.no_sim_exec", summary.get("simulation_executed_now") is False)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.system_level", policy.get("system_level_acceptance_planning") is True)
    ok("policy.not_execution", policy.get("simulation_planning_not_execution") is True)
    ok("policy.tts_abstract", policy.get("tts_runtime_abstract_not_qianwen") is True)

    ok("upstream.pass", upstream.get("review_pass") is True)
    ok("upstream.tts_abstraction_review", upstream.get("tts_runtime_abstraction") is True)
    ok("upstream.qianwen_registered", upstream.get("qianwen_registered_not_invoked") is True)
    for req in UPSTREAM_REQUIREMENTS:
        ok(
            f"upstream.{req['key'][:12]}",
            any(
                x.get("upstream") == req["key"] and x.get("pass") is True
                for x in (upstream.get("upstream_checks") or [])
            ),
        )

    ok("scope.included14", scope.get("included_count") == 14)
    ok("scope.excluded10", scope.get("excluded_count") == 10)
    ok("scope.not_executed", scope.get("simulation_executed_now") is False)
    for item in SIMULATION_SCOPE_INCLUDED:
        ok(f"scope.in.{item[:18]}", item in (scope.get("included") or []))
    for item in SIMULATION_SCOPE_EXCLUDED:
        ok(f"scope.ex.{item[:18]}", item in (scope.get("excluded") or []))

    ok("stages.count23", stages.get("stage_count") == 23)
    ok("stages.list23", len(stages.get("stages") or []) == 23)
    for stage in OUTPUT_CHAIN_STAGES:
        ok(
            f"stage.{stage['stage_id']}",
            any(
                s.get("stage_id") == stage["stage_id"] and s.get("stage_name") == stage["stage_name"]
                for s in (stages.get("stages") or [])
            ),
        )

    ok("matrix.count8", case_matrix.get("case_count") == 8)
    for case in SIMULATION_CASES:
        ok(
            f"matrix.{case['case_id'][:16]}",
            any(
                x.get("case_id") == case["case_id"] and x.get("plan_file") == case["plan_file"]
                for x in (case_matrix.get("cases") or [])
            ),
        )

    for case in SIMULATION_CASES:
        plan = _load(root / case["plan_file"])
        ok(f"case.{case['case_id']}.file", plan.get("case_id") == case["case_id"])
        ok(f"case.{case['case_id']}.sim", plan.get("simulation_only") is True)
        ok(f"case.{case['case_id']}.no_runtime", plan.get("real_runtime") is False)
        ok(f"case.{case['case_id']}.no_tts", plan.get("real_tts") is False)
        ok(f"case.{case['case_id']}.no_audio", plan.get("real_audio") is False)
        for exp in case["expected"]:
            ok(f"case.{case['case_id']}.{exp[:12]}", exp in (plan.get("expected_outcomes") or []))

    ok("handoff.count10", handoff.get("handoff_count") == 10)
    ok("handoff.pass", handoff.get("review_pass") is True)
    for h in STAGE_HANDOFF_CONTRACTS:
        ok(
            f"handoff.{h['from'][:10]}",
            any(
                x.get("from") == h["from"] and x.get("to") == h["to"] and x.get("ref") == h["ref"]
                for x in (handoff.get("handoffs") or [])
            ),
        )

    ok("rule.count8", rule_res.get("rule_count") == 8)
    ok("rule.pass", rule_res.get("review_pass") is True)
    ok("rule.four_layer", rule_res.get("four_layer_architecture") == FOUR_LAYER_ARCHITECTURE)
    for rule in RULE_RESOLUTION_RULES:
        ok(f"rule.{rule[:18]}", rule in (rule_res.get("rules") or []))

    ok("trace.count11", trace.get("field_count") == 11)
    ok("trace.pass", trace.get("review_pass") is True)
    for field in TRACEABILITY_FIELDS:
        ok(f"trace.{field[:18]}", field in (trace.get("fields") or []))

    ok("boundary.pass", boundary.get("review_pass") is True)
    ok("boundary.all_false", boundary.get("all_simulation_boundaries_false") is True)
    for field in BOUNDARY_SIMULATION_FALSE:
        ok(f"sim_boundary.{field[:18]}", boundary.get("simulation_boundary_false", {}).get(field) is False)

    ok("expected.count8", expected.get("output_count") == 8)
    for out in EXPECTED_SIMULATION_OUTPUTS:
        ok(f"expected.{out[:18]}", out in (expected.get("next_phase_outputs") or []))

    ok("dryrun.next", dryrun.get("next_phase") == NEXT_PHASE_GO)
    ok("dryrun.cases8", "execute 8 simulated cases" in (dryrun.get("dryrun_objectives") or []))

    ok("decision.pass", decision.get("planning_pass") is True)
    ok("decision.final", decision.get("final_decision") == FINAL_DECISION_GO)
    ok("decision.next", decision.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("decision.stages23", decision.get("stage_count") == 23)
    ok("decision.cases8", decision.get("case_count") == 8)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    pass_all = summary.get("planning_pass") is True
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "planning_pass": pass_all,
        "final_decision": summary.get("final_decision"),
        "recommended_next_phase": summary.get("recommended_next_phase"),
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"verifier": report["verifier"], "checks_passed": passed, "checks_total": total}, ensure_ascii=False))
    return 0 if go else 1


if __name__ == "__main__":
    raise SystemExit(main())
