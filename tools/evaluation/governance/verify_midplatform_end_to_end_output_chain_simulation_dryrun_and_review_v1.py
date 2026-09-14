#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Midplatform End-to-End Output Chain Simulation DryRunAndReview v1."""

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
    BLOCKED_PATHS,
    BOUNDARY_FALSE,
    BOUNDARY_SIMULATION_FALSE,
    BOUNDARY_TRUE,
    FINAL_DECISION_GO,
    MAIN_CHAIN,
    NEXT_PHASE_GO,
    NON_CLAIMS,
    OUTPUT_CHAIN_STAGES,
    PHASE_ID,
    RULE_RESOLUTION_DRYRUN_RULES,
    SCOPE,
    TRACEABILITY_MATRIX_FIELDS,
    UPSTREAM_PLANNING_FINAL,
    UPSTREAM_PLANNING_NEXT,
)
from capabilities.governance.midplatform_end_to_end_output_chain_simulation_planning_v1 import (
    SIMULATION_CASES,
    UPSTREAM_REQUIREMENTS,
)
from capabilities.governance.midplatform_safety_gate_planning_v1 import FOUR_LAYER_ARCHITECTURE
from capabilities.governance.midplatform_tts_runtime_planning_v1 import (
    CURRENT_PREFERRED_PROVIDER_CANDIDATE,
)

MIN_CHECKS = 226

REQUIRED = (
    "end_to_end_output_chain_simulation_dryrun_review_policy_v1.json",
    "simulation_planning_input_review_v1.json",
    "simulation_case_results_v1.json",
    "chain_stage_result_matrix_v1.json",
    "expected_vs_actual_decision_matrix_v1.json",
    "boundary_violation_matrix_v1.json",
    "traceability_matrix_v1.json",
    "blocked_path_matrix_v1.json",
    "rule_resolution_enforcement_execution_review_v1.json",
    "case_1_normal_low_risk_output_result_v1.json",
    "case_2_missing_evidence_hold_result_v1.json",
    "case_3_validation_fail_block_result_v1.json",
    "case_4_high_uncertainty_disclosure_result_v1.json",
    "case_5_privacy_risk_no_output_result_v1.json",
    "case_6_urgent_safety_degrade_disclosure_result_v1.json",
    "case_7_speech_forbidden_block_result_v1.json",
    "case_8_execution_layer_bypass_attempt_result_v1.json",
    "system_level_chain_closure_review_v1.json",
    "end_to_end_boundary_audit_v1.json",
    "end_to_end_simulation_closure_decision_v1.json",
    "next_route_readiness_decision_v1.json",
    "non_claims_register_v1.json",
    "summary.json",
)

CASE_RESULT_FILES = (
    "case_1_normal_low_risk_output_result_v1.json",
    "case_2_missing_evidence_hold_result_v1.json",
    "case_3_validation_fail_block_result_v1.json",
    "case_4_high_uncertainty_disclosure_result_v1.json",
    "case_5_privacy_risk_no_output_result_v1.json",
    "case_6_urgent_safety_degrade_disclosure_result_v1.json",
    "case_7_speech_forbidden_block_result_v1.json",
    "case_8_execution_layer_bypass_attempt_result_v1.json",
)

EXPECTED_PATH_TYPES = {
    "case_1_normal_low_risk_output": "allow",
    "case_2_missing_evidence_hold": "hold",
    "case_3_validation_fail_block": "block",
    "case_4_high_uncertainty_disclosure": "disclosure",
    "case_5_privacy_risk_no_output": "no_output",
    "case_6_urgent_safety_degrade_disclosure": "degrade",
    "case_7_speech_forbidden_block": "block",
    "case_8_execution_layer_bypass_attempt": "bypass_blocked",
}


def _load(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--output-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_dryrun_and_review"
        ),
    )
    p.add_argument(
        "--planning-root",
        default=(
            "/Users/luanlei/Desktop/Luna-Workspace-Min/_tmp_eval_out/"
            "midplatform_end_to_end_output_chain_simulation_planning"
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

    summary = _load(root / "summary.json")
    policy = _load(root / "end_to_end_output_chain_simulation_dryrun_review_policy_v1.json")
    input_review = _load(root / "simulation_planning_input_review_v1.json")
    case_results = _load(root / "simulation_case_results_v1.json")
    stage_matrix = _load(root / "chain_stage_result_matrix_v1.json")
    exp_actual = _load(root / "expected_vs_actual_decision_matrix_v1.json")
    boundary_v = _load(root / "boundary_violation_matrix_v1.json")
    trace = _load(root / "traceability_matrix_v1.json")
    blocked = _load(root / "blocked_path_matrix_v1.json")
    rule_res = _load(root / "rule_resolution_enforcement_execution_review_v1.json")
    closure_review = _load(root / "system_level_chain_closure_review_v1.json")
    audit = _load(root / "end_to_end_boundary_audit_v1.json")
    closure = _load(root / "end_to_end_simulation_closure_decision_v1.json")
    next_route = _load(root / "next_route_readiness_decision_v1.json")

    ok("upstream.planning_go", plan_vr.get("verifier") == "GO")
    ok("upstream.planning_final", plan_sm.get("final_decision") == UPSTREAM_PLANNING_FINAL)
    ok("upstream.planning_next", plan_sm.get("recommended_next_phase") == UPSTREAM_PLANNING_NEXT)

    ok("summary.phase", summary.get("phase") == PHASE_ID)
    ok("summary.scope", summary.get("scope") == SCOPE)
    ok("summary.dryrun_only", summary.get("end_to_end_output_chain_simulation_dryrun_and_review_only") is True)
    ok("summary.simulated", summary.get("simulated") is True)
    ok("summary.sim_executed", summary.get("simulation_executed_now") is True)
    ok("summary.pass", summary.get("dryrun_and_review_pass") is True)
    ok("summary.final", summary.get("final_decision") == FINAL_DECISION_GO)
    ok("summary.next", summary.get("recommended_next_phase") == NEXT_PHASE_GO)
    ok("summary.cases8", summary.get("case_count") == 8)
    ok("summary.cases_passed8", summary.get("cases_passed") == 8)
    ok("summary.main_chain", summary.get("main_chain") == MAIN_CHAIN)

    for field in BOUNDARY_TRUE:
        ok(f"true.{field}", summary.get(field) is True)
    for field in BOUNDARY_FALSE:
        ok(f"false.{field}", summary.get(field) is False)

    ok("policy.system_level", policy.get("system_level_acceptance") is True)
    ok("policy.sim_not_runtime", policy.get("simulation_executed_not_real_runtime") is True)

    ok("input.pass", input_review.get("review_pass") is True)
    ok("input.upstream9", input_review.get("upstream_dryrun_count") == 9)
    ok("input.tts_abstraction", input_review.get("tts_runtime_abstraction") is True)
    ok("input.qianwen_registered", input_review.get("qianwen_registered_not_invoked") is True)

    ok("results.all_pass", case_results.get("all_pass") is True)
    ok("results.count8", case_results.get("case_count") == 8)
    ok("results.passed8", case_results.get("cases_passed") == 8)

    for case in SIMULATION_CASES:
        cid = case["case_id"]
        cr = next((c for c in (case_results.get("cases") or []) if c.get("case_id") == cid), {})
        ok(f"results.{cid[:16]}.match", cr.get("outcome_match") is True)
        ok(f"results.{cid[:16]}.path", cr.get("actual_path_type") == EXPECTED_PATH_TYPES.get(cid))

    case1 = _load(root / "case_1_normal_low_risk_output_result_v1.json")
    ok("c1.intake", case1.get("actual", {}).get("candidate_intake_pass") is True)
    ok("c1.evidence", case1.get("actual", {}).get("evidence_binding_pass") is True)
    ok("c1.validation", case1.get("actual", {}).get("validation_pass") is True)
    ok("c1.allow", case1.get("actual", {}).get("decision_action") == "allow_candidate_forward")
    ok("c1.speech_req", case1.get("actual", {}).get("speech_request_candidate_generated") is True)
    ok("c1.audio_art", case1.get("actual", {}).get("audio_artifact_candidate_generated") is True)
    ok("c1.no_qianwen", case1.get("actual", {}).get("qianwen_tts_invoked_now") is False)

    case2 = _load(root / "case_2_missing_evidence_hold_result_v1.json")
    ok("c2.missing", case2.get("actual", {}).get("missing_evidence_detected") is True)
    ok("c2.hold", case2.get("actual", {}).get("path_type") == "hold")
    ok("c2.no_speech", case2.get("actual", {}).get("speech_request_candidate_generated") is False)
    ok("c2.hold_reason", case2.get("actual", {}).get("hold_reason_preserved") is True)

    case3 = _load(root / "case_3_validation_fail_block_result_v1.json")
    ok("c3.fail_ref", case3.get("actual", {}).get("validation_fail_ref_preserved") is True)
    ok("c3.block", case3.get("actual", {}).get("path_type") == "block")
    ok("c3.no_speech", case3.get("actual", {}).get("speech_request_candidate_generated") is False)

    case4 = _load(root / "case_4_high_uncertainty_disclosure_result_v1.json")
    ok("c4.uncertainty", case4.get("actual", {}).get("uncertainty_level") == "high")
    ok("c4.surface", case4.get("actual", {}).get("uncertainty_surface_required") is True)
    ok("c4.preserved", case4.get("actual", {}).get("uncertainty_surface_preserved") is True)

    case5 = _load(root / "case_5_privacy_risk_no_output_result_v1.json")
    ok("c5.no_output", case5.get("actual", {}).get("path_type") == "no_output")
    ok("c5.privacy", case5.get("actual", {}).get("privacy_reason_preserved") is True)
    ok("c5.no_speech", case5.get("actual", {}).get("speech_request_candidate_generated") is False)

    case6 = _load(root / "case_6_urgent_safety_degrade_disclosure_result_v1.json")
    ok("c6.degrade", case6.get("actual", {}).get("path_type") == "degrade")
    ok("c6.urgent", case6.get("actual", {}).get("urgent_safety_context_preserved") is True)
    ok("c6.speech_req", case6.get("actual", {}).get("speech_request_candidate_generated") is True)
    ok("c6.no_real_audio", case6.get("actual", {}).get("real_tts_audio_false") is True)

    case7 = _load(root / "case_7_speech_forbidden_block_result_v1.json")
    ok("c7.speech_block", case7.get("actual", {}).get("speech_gate_action") == "speech_block_candidate")
    ok("c7.no_speech_req", case7.get("actual", {}).get("speech_request_candidate_generated") is False)

    case8 = _load(root / "case_8_execution_layer_bypass_attempt_result_v1.json")
    ok("c8.all_blocked", case8.get("actual", {}).get("all_bypass_blocked") is True)
    ok("c8.no_raw", case8.get("actual", {}).get("raw_constitution_clause_bound_now") is False)
    ok("c8.no_bypass", case8.get("actual", {}).get("speech_gate_bypassed_now") is False)
    ok("c8.no_qianwen", case8.get("actual", {}).get("qianwen_tts_invoked_now") is False)
    ok("c8.issue_trace", case8.get("actual", {}).get("issue_trace_candidate_generated") is True)
    ok("c8.violation", case8.get("actual", {}).get("violation_report_candidate_generated") is True)

    ok("stage.count23", stage_matrix.get("stage_count") == 23)
    ok("stage.all_defined", stage_matrix.get("all_stages_defined") is True)
    for stage in OUTPUT_CHAIN_STAGES:
        ok(
            f"stage.{stage['stage_id']}",
            any(
                s.get("stage_id") == stage["stage_id"] and s.get("stage_name") == stage["stage_name"]
                for s in (stage_matrix.get("stages") or [])
            ),
        )

    ok("exp_actual.all_match", exp_actual.get("all_match") is True)
    ok("exp_actual.rows8", len(exp_actual.get("rows") or []) == 8)
    for pt in ("allow", "hold", "block", "no_output", "degrade", "disclosure", "bypass_blocked"):
        ok(f"exp_actual.path.{pt}", pt in (exp_actual.get("path_types_covered") or []))

    ok("boundary.clear", boundary_v.get("all_boundaries_clear") is True)
    for field in BOUNDARY_SIMULATION_FALSE:
        ok(f"boundary.{field[:18]}", boundary_v.get("boundary_checks", {}).get(field) is False)

    ok("trace.all_preserved", trace.get("all_preserved") is True)
    ok("trace.fields13", len(trace.get("fields") or []) == 13)
    for field in TRACEABILITY_MATRIX_FIELDS:
        ok(f"trace.{field[:18]}", field in (trace.get("fields") or []))

    ok("blocked.all", blocked.get("all_blocked") is True)
    ok("blocked.count13", blocked.get("blocked_count") == 13)
    for bp in BLOCKED_PATHS:
        ok(
            f"blocked.{bp[:18]}",
            any(
                x.get("blocked_path") == bp and x.get("blocked") is True
                for x in (blocked.get("blocked_paths") or [])
            ),
        )

    ok("rule.pass", rule_res.get("dryrun_and_review_pass") is True)
    ok("rule.tts_abstract", rule_res.get("tts_runtime_abstraction") is True)
    ok("rule.qianwen_candidate", rule_res.get("qianwen_provider_candidate_only") is True)
    for rule in RULE_RESOLUTION_DRYRUN_RULES:
        ok(f"rule.{rule[:18]}", rule in (rule_res.get("rules") or []))

    ok("closure_review.pass", closure_review.get("dryrun_and_review_pass") is True)
    ok("closure_review.normal", closure_review.get("normal_path_closes_to_audio_artifact") is True)
    ok("closure_review.exec_boundary", closure_review.get("execution_layer_boundary_works") is True)
    ok("closure_review.provider", closure_review.get("provider_abstraction_works") is True)
    ok("closure_review.no_leak", closure_review.get("no_runtime_leakage") is True)

    ok("audit.pass", audit.get("dryrun_and_review_pass") is True)
    ok("audit.sim_not_runtime", audit.get("simulation_executed_not_real_runtime") is True)

    ok("closure.pass", closure.get("dryrun_and_review_pass") is True)
    ok("closure.system_go", closure.get("system_level_output_chain_go") is True)
    ok("closure.final", closure.get("final_decision") == FINAL_DECISION_GO)
    ok("closure.next", closure.get("recommended_next_phase") == NEXT_PHASE_GO)

    ok("next.ready", next_route.get("ready_for_post_simulation_roadmap_decision") is True)
    ok("next.system_go", next_route.get("system_level_simulated_go") is True)
    ok("next.no_runtime", next_route.get("real_runtime_enabled") is False)

    ok("non_claims", len(_load(root / "non_claims_register_v1.json").get("non_claims") or []) >= len(NON_CLAIMS))
    for claim in NON_CLAIMS:
        ok(f"claim.{claim[:18]}", claim in (_load(root / "non_claims_register_v1.json").get("non_claims") or []))

    pass_all = summary.get("dryrun_and_review_pass") is True
    passed = sum(1 for c in checks if c["passed"])
    total = len(checks)
    go = passed >= MIN_CHECKS and pass_all and passed == total

    report = {
        "phase": PHASE_ID,
        "verifier": "GO" if go else "NO_GO",
        "checks_passed": passed,
        "checks_total": total,
        "min_checks_required": MIN_CHECKS,
        "dryrun_and_review_pass": pass_all,
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
