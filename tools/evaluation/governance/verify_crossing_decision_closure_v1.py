#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Crossing Decision Closure v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Crossing-Decision-Closure-v1-001"
FINAL_DECISION = "CROSSING_DECISION_CLOSED_FOR_CURRENT_MAINLINE"
NEXT_PHASE = "Phase-Post-Crossing-Decision-Roadmap-Decision-v1-001"
MIN_CHECKS = 180
BASELINE_REQUIREMENT = 140

FORBIDDEN_OUTPUTS = [
    "SAFE_TO_CROSS",
    "CROSS_NOW",
    "GO_AHEAD",
    "PROCEED",
    "FOLLOW_THE_CROWD",
    "GREEN_LIGHT_GO",
    "MAP_SAYS_CROSS",
    "COUNTDOWN_SAYS_GO",
]

EXPECTED_PHASES = [
    "Luna Safety Constitution Policy v1",
    "Crossing Decision Safety Governance Policy v1",
    "Crossing Decision DryRun v1",
    "Crossing Decision Post-DryRun Review v1",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Crossing Decision Closure v1")
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/crossing_decision_closure_v1_smoke_v0",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.output_root)
    checks: List[Dict[str, Any]] = []

    def ok(check_id: str, passed: bool, detail: Any = None) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail})

    summary = _load_json(root / "summary.json")
    input_root_matrix = _load_json(root / "input_root_matrix.json")
    closure_summary = _load_json(root / "crossing_decision_closure_summary.json")
    completed_phase_matrix = _load_json(root / "completed_phase_matrix.json")
    validated_capability_summary = _load_json(root / "validated_capability_summary.json")
    disabled_runtime_summary = _load_json(root / "disabled_runtime_summary.json")
    closure_boundary_freeze = _load_json(root / "closure_boundary_freeze.json")
    forbidden_freeze = _load_json(root / "forbidden_crossing_output_freeze.json")
    non_claims = _load_json(root / "crossing_decision_non_claims_register.json")
    deferred_pool = _load_json(root / "deferred_capability_pool.json")
    governance_debt = _load_json(root / "governance_debt_carryover.json")
    readiness_gate = _load_json(root / "closure_readiness_gate.json")
    next_phase = _load_json(root / "next_phase_recommendation.json")
    no_runtime = _load_json(root / "no_runtime_boundary_report.json")
    no_write = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    for intake_id in (
        "post_dryrun_review",
        "crossing_decision_dryrun",
        "crossing_safety_governance",
        "safety_constitution",
        "post_controlled_frame_roadmap_decision",
        "controlled_frame_input_closure",
        "map_location_readonly_context",
        "vision_strengthening_closure",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    ok("summary.closure_scope", summary.get("closure_scope") == "crossing_decision_closure_only")

    for field in (
        "post_dryrun_review_input_loaded",
        "dryrun_input_loaded",
        "crossing_governance_input_loaded",
        "safety_constitution_input_loaded",
        "post_controlled_frame_roadmap_decision_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "completed_phase_matrix_generated",
        "validated_capability_summary_generated",
        "disabled_runtime_summary_generated",
        "closure_boundary_freeze_generated",
        "forbidden_crossing_output_freeze_generated",
        "non_claims_register_generated",
        "deferred_capability_pool_generated",
        "governance_debt_carryover_generated",
        "closure_readiness_gate_generated",
        "safety_constitution_inheritance_closed",
        "crossing_governance_policy_closed",
        "crossing_dryrun_closed",
        "crossing_post_review_closed",
        "crossing_decision_closed",
        "forbidden_crossing_outputs_absent",
        "crossing_permission_allowed_false_all_cases",
        "crossing_action_instruction_allowed_false_all_cases",
        "safe_to_cross_claim_allowed_false_all_cases",
        "conservative_handling_pass",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "gate_taxonomy_required_later",
        "survival_constitution_required_later",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True)

    for field in (
        "human_assistance_obtained_assumed",
        "crossing_runtime_claimed",
        "real_crossing_judgment_claimed",
        "safe_to_cross_capability_claimed",
        "production_readiness_claimed",
        "runtime_enablement_claimed",
        "crossing_runtime_invoked",
        "camera_invoked",
        "visual_model_invoked",
        "map_api_invoked",
        "gaode_api_invoked",
        "gps_runtime_invoked",
        "ocr_provider_invoked",
        "ocrrequest_submitted",
        "tracking_runtime_invoked",
        "optical_flow_runtime_invoked",
        "speech_gate_invoked",
        "vop_invoked",
        "tts_invoked",
        "user_heard_assumed",
        "task_state_committed_now",
        "navigation_action_triggered",
        "route_modified",
        "scene_delta_generated",
        "world_model_written",
        "memory_written",
        "library_written",
        "fact_written",
    ):
        ok(f"summary.{field}", summary.get(field) is False)

    ok("summary.forbidden_output_violation_count", summary.get("forbidden_output_violation_count", 1) == 0)
    ok("summary.completed_phase_count", summary.get("completed_phase_count", 0) >= 4)
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    ok("closure_summary.final_decision", closure_summary.get("final_decision") == FINAL_DECISION)
    ok("closure_summary.completed_phase_count", closure_summary.get("completed_phase_count", 0) >= 4)

    phase_ids = [p.get("phase_id") for p in completed_phase_matrix.get("phases", [])]
    ok("completed_phase_matrix.count", completed_phase_matrix.get("completed_phase_count", 0) >= 4)
    for phase_id in EXPECTED_PHASES:
        ok(f"completed_phase_matrix.present.{phase_id}", phase_id in phase_ids)
    for phase in completed_phase_matrix.get("phases", []):
        pid = phase.get("phase_id", "unknown")
        ok(f"completed_phase.{pid}.runtime_disabled", phase.get("runtime_enabled") is False)
        ok(f"completed_phase.{pid}.write_disabled", phase.get("write_enabled") is False)
        ok(f"completed_phase.{pid}.verifier_go", phase.get("verifier_verdict") == "GO")

    ok("validated_capability.count", len(validated_capability_summary.get("validated_capabilities", [])) >= 10)
    ok("disabled_runtime.count", len(disabled_runtime_summary.get("disabled_runtimes", [])) >= 10)
    ok("disabled_runtime.crossing_false", disabled_runtime_summary.get("crossing_runtime_allowed") is False)

    for flag in (
        "no_runtime",
        "no_write",
        "no_action",
        "no_speech",
        "no_fact",
        "no_crossing_runtime",
        "no_real_crossing_judgment",
        "no_safe_to_cross_claim",
        "no_crossing_permission_output",
        "candidate_not_fact",
        "conservative_output_required",
    ):
        ok(f"closure_boundary.{flag}", closure_boundary_freeze.get(flag) is True)

    forbidden_rows = forbidden_freeze.get("forbidden_outputs", [])
    ok("forbidden_freeze.count", forbidden_freeze.get("forbidden_count", 0) >= 8)
    for forbidden in FORBIDDEN_OUTPUTS:
        row = next((r for r in forbidden_rows if r.get("forbidden_output") == forbidden), None)
        ok(f"forbidden_freeze.present.{forbidden}", row is not None)
        if row:
            ok(f"forbidden_freeze.{forbidden}.runtime_false", row.get("runtime_allowed") is False)
            ok(f"forbidden_freeze.{forbidden}.dryrun_absent", row.get("verified_absent_in_dryrun") is True)
            ok(f"forbidden_freeze.{forbidden}.review_absent", row.get("verified_absent_in_review") is True)

    ok("non_claims.count", len(non_claims.get("non_claims", [])) >= 10)
    ok("deferred_pool.count", len(deferred_pool.get("deferred_capabilities", [])) >= 10)
    ok("deferred_pool.sample_not_started", deferred_pool.get("controlled_sample_planning_started") is False)
    ok("deferred_pool.runtime_not_started", deferred_pool.get("crossing_runtime_trial_started") is False)

    ok("governance_debt.midplatform_required", governance_debt.get("future_midplatform_function_governance_required") is True)
    ok("governance_debt.gate_taxonomy_required", governance_debt.get("future_gate_taxonomy_required") is True)
    ok("governance_debt.survival_constitution_required", governance_debt.get("future_survival_constitution_required") is True)

    ok("readiness_gate.ready", readiness_gate.get("ready_for_closure") is True)
    ok("readiness_gate.no_blockers", not readiness_gate.get("blockers"))
    ok("next_phase.recommended", next_phase.get("recommended_next_phase") == NEXT_PHASE)

    for report_name, report in (("no_runtime", no_runtime), ("no_write", no_write)):
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{report_name}.crossing_runtime_false", report.get("crossing_runtime_invoked") is False)
        ok(f"{report_name}.no_runtime_executed", report.get("no_runtime_executed") is True)
        for flag in (
            "camera_invoked",
            "visual_model_invoked",
            "map_api_invoked",
            "ocr_provider_invoked",
            "tracking_runtime_invoked",
            "speech_gate_invoked",
            "world_model_written",
            "memory_written",
            "fact_written",
        ):
            ok(f"{report_name}.{flag}_false", report.get(flag) is False)

    for claim in non_claims.get("non_claims", []):
        ok(f"non_claims.present.{hash(claim) % 10000}", isinstance(claim, str) and len(claim) > 0)

    for topic in governance_debt.get("carryover_topics", []):
        ok(f"governance_debt.topic.{hash(topic) % 10000}", isinstance(topic, str))

    for cap in validated_capability_summary.get("validated_capabilities", []):
        ok(f"validated_capability.{hash(cap) % 10000}", isinstance(cap, str))

    for rt in disabled_runtime_summary.get("disabled_runtimes", []):
        ok(f"disabled_runtime.{hash(rt) % 10000}", isinstance(rt, str))

    ok("closure_summary.source_chain_len", len(closure_summary.get("source_phase_chain", [])) >= 4)
    ok("readiness_gate.go_conditions", len(readiness_gate.get("go_conditions", [])) >= 10)
    ok("readiness_gate.no_go_conditions", len(readiness_gate.get("no_go_conditions", [])) >= 5)
    ok("governance_debt.no_duplicate", governance_debt.get("no_duplicate_governance_module_allowed") is True)
    ok("validated_capability.layers", len(validated_capability_summary.get("validation_layers", [])) >= 4)
    ok("validated_capability.clarifications", len(validated_capability_summary.get("clarifications", [])) >= 2)

    passed = sum(1 for c in checks if c["passed"])
    failed = [c for c in checks if not c["passed"]]
    verdict = "GO" if len(checks) >= MIN_CHECKS and not failed else "NO_GO"

    report = {
        "phase": PHASE_ID,
        "verifier": verdict,
        "check_count": len(checks),
        "passed_count": passed,
        "failed_count": len(failed),
        "min_checks": MIN_CHECKS,
        "baseline_requirement": BASELINE_REQUIREMENT,
        "final_decision": FINAL_DECISION if verdict == "GO" else "CROSSING_DECISION_CLOSURE_VERIFIER_FAILED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": failed[:20],
        "checks": checks,
    }
    (root / "verifier_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        json.dumps(
            {
                "verifier": verdict,
                "check_count": len(checks),
                "passed_count": passed,
                "failed_count": len(failed),
                "output_root": str(root),
            },
            ensure_ascii=False,
        )
    )
    return 0 if verdict == "GO" else 1


if __name__ == "__main__":
    raise SystemExit(main())
