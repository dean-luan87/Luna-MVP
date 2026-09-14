#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify Crossing Decision DryRun v1."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

PHASE_ID = "Phase-Crossing-Decision-DryRun-v1-001"
FINAL_DECISION = "CROSSING_DECISION_DRYRUN_READY_FOR_POST_DRYRUN_REVIEW"
NEXT_PHASE = "Phase-Crossing-Decision-Post-DryRun-Review-v1-001"
MIN_CHECKS = 220
BASELINE_REQUIREMENT = 180

EXPECTED_SCENARIOS = [
    "green_light_candidate_only",
    "green_light_with_vehicle_flow_uncertain",
    "red_light_candidate",
    "countdown_text_candidate_only",
    "crowd_flow_forward",
    "map_crossing_hint_only",
    "route_says_cross",
    "user_says_go",
    "crosswalk_candidate_but_vehicle_occluded",
    "traffic_light_uncertain",
    "no_crosswalk_detected",
    "stale_traffic_light_evidence",
    "conflicting_audio_visual_cues",
    "unknown_speaker_says_safe",
    "green_light_plus_crowd_flow_plus_map_hint",
    "all_evidence_low_confidence",
]

EXPECTED_FORBIDDEN_OUTPUTS = [
    "CROSS_NOW",
    "SAFE_TO_CROSS",
    "GO_AHEAD",
    "PROCEED",
    "FOLLOW_THE_CROWD",
    "GREEN_LIGHT_GO",
    "MAP_SAYS_CROSS",
    "COUNTDOWN_SAYS_GO",
]

ALLOWED_DECISION_TYPES = [
    "SAFETY_HOLD_CANDIDATE",
    "REOBSERVE_CANDIDATE",
    "HUMAN_ASSISTANCE_CANDIDATE",
    "LOW_CONFIDENCE_WARNING_CANDIDATE",
    "VISUAL_CONFIRMATION_REQUIRED_CANDIDATE",
    "NO_OUTPUT_SUPPRESSED",
]


def _load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Crossing Decision DryRun v1")
    parser.add_argument(
        "--output-root",
        default="/Users/luanlei/Desktop/Luna-Workspace-Min/_eval_out/crossing_decision_dryrun_v1_smoke_v0",
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
    dryrun_case_schema = _load_json(root / "dryrun_case_schema.json")
    simulated_crossing_evidence_set_schema = _load_json(root / "simulated_crossing_evidence_set_schema.json")
    crossing_governance_decision_candidate_schema = _load_json(root / "crossing_governance_decision_candidate_schema.json")
    forbidden_crossing_output_check_schema = _load_json(root / "forbidden_crossing_output_check_schema.json")
    crossing_conflict_evaluation_candidate_schema = _load_json(root / "crossing_conflict_evaluation_candidate_schema.json")
    crossing_uncertainty_evaluation_candidate_schema = _load_json(root / "crossing_uncertainty_evaluation_candidate_schema.json")
    crossing_dryrun_boundary_decision_schema = _load_json(root / "crossing_dryrun_boundary_decision_schema.json")
    scenario_matrix = _load_json(root / "crossing_decision_dryrun_scenario_matrix.json")
    dryrun_results = _load_json(root / "crossing_decision_dryrun_results.json")
    forbidden_results = _load_json(root / "forbidden_crossing_output_check_results.json")
    boundary_matrix = _load_json(root / "crossing_dryrun_boundary_matrix.json")
    governance_debt_register = _load_json(root / "governance_debt_register.json")
    next_phase_recommendation = _load_json(root / "next_phase_recommendation.json")
    no_runtime_boundary_report = _load_json(root / "no_runtime_boundary_report.json")
    no_write_boundary_report = _load_json(root / "no_write_boundary_report.json")

    rows = input_root_matrix.get("rows", [])
    idx = {row.get("intake_id"): row for row in rows}

    for intake_id in (
        "crossing_safety_governance",
        "safety_constitution",
        "post_controlled_frame_roadmap_decision",
        "controlled_frame_input_closure",
        "map_location_readonly_context",
        "vision_strengthening_closure",
        "safety_task_arbitration_policy",
        "minimal_runtime_integration_closure",
        "ocr_final_closure",
    ):
        ok(f"input.{intake_id}.loaded", idx.get(intake_id, {}).get("loaded") is True)

    for intake_id in (
        "task_aware_visual_focus_policy",
        "selective_tracking_adapter_policy",
        "visual_ocr_map_task_feedback_dryrun",
        "basic_navigation_loop_vision_strengthening_dryrun",
        "minimal_runtime_controlled_output_definition",
        "minimal_runtime_text_only_output_post_review",
        "voice_command_ownership_gate_policy",
        "voice_interruption_governance_dryrun",
    ):
        status = idx.get(intake_id, {}).get("status")
        ok(f"input.{intake_id}.status", status in {"loaded", "optional_missing"}, status)

    ok("input.row_count", input_root_matrix.get("row_count") == len(rows))

    ok("summary.dryrun_scope", summary.get("dryrun_scope") == "crossing_decision_dryrun_only")
    for field in (
        "crossing_safety_governance_input_loaded",
        "safety_constitution_input_loaded",
        "post_controlled_frame_roadmap_decision_input_loaded",
        "controlled_frame_input_closure_input_loaded",
        "map_location_readonly_context_input_loaded",
        "vision_strengthening_closure_input_loaded",
        "safety_task_arbitration_policy_input_loaded",
        "minimal_runtime_integration_closure_loaded",
        "ocr_final_closure_loaded",
        "dryrun_case_schema_defined",
        "simulated_crossing_evidence_set_schema_defined",
        "crossing_governance_decision_candidate_schema_defined",
        "forbidden_crossing_output_check_schema_defined",
        "crossing_conflict_evaluation_candidate_schema_defined",
        "crossing_uncertainty_evaluation_candidate_schema_defined",
        "crossing_dryrun_boundary_decision_schema_defined",
        "scenario_matrix_generated",
        "dryrun_results_generated",
        "forbidden_crossing_output_check_results_generated",
        "forbidden_crossing_outputs_absent",
        "inherits_safety_constitution",
        "traffic_light_candidate_not_crossing_permission",
        "green_light_candidate_not_crossing_permission",
        "countdown_text_candidate_not_crossing_permission",
        "crowd_flow_candidate_not_crossing_permission",
        "map_crossing_hint_not_crossing_permission",
        "route_crossing_hint_not_crossing_permission",
        "user_says_go_not_crossing_permission",
        "single_modality_evidence_not_crossing_permission",
        "stale_evidence_not_crossing_permission",
        "conflicting_evidence_not_crossing_permission",
        "low_confidence_evidence_not_crossing_permission",
        "uncertainty_requires_hold_or_confirm",
        "conflict_blocks_crossing_action",
        "human_assistance_candidate_allowed",
        "speech_allowed_false_until_gate",
        "action_allowed_false",
        "fact_status_not_fact",
        "no_runtime_executed",
        "no_new_runtime_enabled",
        "boundary_ok",
    ):
        ok(f"summary.{field}", summary.get(field) is True)

    for field in (
        "crossing_permission_output_allowed",
        "crossing_action_instruction_allowed",
        "safe_to_cross_claim_allowed",
        "crossing_runtime_allowed",
        "crossing_runtime_invoked",
        "human_assistance_obtained_assumed",
        "navigation_action_allowed",
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

    ok("summary.scenario_count", summary.get("scenario_count", 0) >= 16, summary.get("scenario_count"))
    ok("summary.decision_candidate_count", summary.get("decision_candidate_count", 0) >= 16, summary.get("decision_candidate_count"))
    ok("summary.violations_empty", summary.get("violations") == [])
    ok("summary.final_decision", summary.get("final_decision") == FINAL_DECISION)
    ok("summary.recommended_next_phase", summary.get("recommended_next_phase") == NEXT_PHASE)

    def field_names(schema: Dict[str, Any]) -> List[str]:
        return [f.get("name") for f in schema.get("fields", [])]

    ok("schema.dryrun_case.object_name", dryrun_case_schema.get("object_name") == "CrossingDecisionDryRunCase")
    for name in (
        "dryrun_case_id",
        "case_type",
        "simulated_crossing_context",
        "simulated_evidence_candidates",
        "expected_governance_path",
        "expected_output_candidate",
        "expected_forbidden_outputs_absent",
        "expected_boundary_flags",
        "source_chain",
    ):
        ok(f"schema.dryrun_case.field.{name}", name in field_names(dryrun_case_schema))

    ok("schema.evidence_set.object_name", simulated_crossing_evidence_set_schema.get("object_name") == "SimulatedCrossingEvidenceSet")
    for name in ("evidence_set_id", "freshness_profile", "confidence_profile", "conflict_profile", "source_chain"):
        ok(f"schema.evidence_set.field.{name}", name in field_names(simulated_crossing_evidence_set_schema))

    ok(
        "schema.decision_candidate.object_name",
        crossing_governance_decision_candidate_schema.get("object_name") == "CrossingGovernanceDecisionCandidate",
    )
    for name in (
        "decision_candidate_id",
        "source_case_id",
        "decision_type",
        "crossing_permission_allowed",
        "crossing_action_instruction_allowed",
        "safe_to_cross_claim_allowed",
        "fact_status",
    ):
        ok(f"schema.decision_candidate.field.{name}", name in field_names(crossing_governance_decision_candidate_schema))

    ok("schema.forbidden_check.object_name", forbidden_crossing_output_check_schema.get("object_name") == "ForbiddenCrossingOutputCheck")
    ok("schema.conflict.object_name", crossing_conflict_evaluation_candidate_schema.get("object_name") == "CrossingConflictEvaluationCandidate")
    ok("schema.uncertainty.object_name", crossing_uncertainty_evaluation_candidate_schema.get("object_name") == "CrossingUncertaintyEvaluationCandidate")
    ok("schema.boundary.object_name", crossing_dryrun_boundary_decision_schema.get("object_name") == "CrossingDryRunBoundaryDecision")

    scenario_ids = [s.get("scenario_id") for s in scenario_matrix.get("scenarios", [])]
    ok("scenario.matrix.count", scenario_matrix.get("scenario_count", 0) >= 16)
    for sid in EXPECTED_SCENARIOS:
        ok(f"scenario.exists.{sid}", sid in scenario_ids)

    dryrun_cases = dryrun_results.get("dryrun_cases", [])
    decision_candidates = dryrun_results.get("decision_candidates", [])
    case_index = {c.get("dryrun_case_id"): c for c in dryrun_cases}
    decision_index = {d.get("source_case_id"): d for d in decision_candidates}

    ok("results.case_count", dryrun_results.get("case_count", 0) >= 16)
    ok("results.decision_candidate_count", dryrun_results.get("decision_candidate_count", 0) >= 16)

    for sid in EXPECTED_SCENARIOS:
        case = case_index.get(sid, {})
        decision = decision_index.get(sid, {})
        ok(f"case.present.{sid}", bool(case))
        ok(f"decision.present.{sid}", bool(decision))
        ok(f"case.expected_output.{sid}", case.get("expected_output_candidate") == decision.get("decision_type"))
        ok(f"decision.permission_false.{sid}", decision.get("crossing_permission_allowed") is False)
        ok(f"decision.action_false.{sid}", decision.get("crossing_action_instruction_allowed") is False)
        ok(f"decision.safe_to_cross_false.{sid}", decision.get("safe_to_cross_claim_allowed") is False)
        ok(f"decision.fact_not_fact.{sid}", decision.get("fact_status") == "not_fact")
        ok(f"decision.type_allowed.{sid}", decision.get("decision_type") in ALLOWED_DECISION_TYPES)
        for forbidden in EXPECTED_FORBIDDEN_OUTPUTS:
            ok(
                f"decision.forbidden_absent.{sid}.{forbidden}",
                decision.get("decision_type") != forbidden and decision.get("allowed_output_mode") != forbidden,
            )

    forbidden_checks = forbidden_results.get("checks", [])
    ok("forbidden.results.count", forbidden_results.get("check_count", 0) >= 16)
    ok("forbidden.results.all_absent", forbidden_results.get("forbidden_crossing_outputs_absent") is True)
    ok("forbidden.results.zero_violations", forbidden_results.get("total_violation_count", 1) == 0)
    for check in forbidden_checks:
        cid = check.get("source_case_id", "unknown")
        ok(f"forbidden.check.pass.{cid}", check.get("verdict") == "PASS")
        ok(f"forbidden.check.absent.{cid}", check.get("forbidden_outputs_absent") is True)
        ok(f"forbidden.check.zero_violations.{cid}", check.get("violation_count", 1) == 0)

    for forbidden in EXPECTED_FORBIDDEN_OUTPUTS:
        found_any = any(forbidden in c.get("forbidden_outputs_found", []) for c in forbidden_checks)
        ok(f"forbidden.global.{forbidden}.absent", not found_any)

    boundary_decisions = boundary_matrix.get("boundary_decisions", [])
    ok("boundary.matrix.count", boundary_matrix.get("case_count", 0) >= 16)
    ok("boundary.matrix.all_ok", boundary_matrix.get("all_boundary_ok") is True)
    bidx = {b.get("case_id"): b for b in boundary_decisions}
    for sid in EXPECTED_SCENARIOS:
        b = bidx.get(sid, {})
        ok(f"boundary.ok.{sid}", b.get("boundary_ok") is True)
        ok(f"boundary.runtime_ok.{sid}", b.get("runtime_boundary_ok") is True)
        ok(f"boundary.write_ok.{sid}", b.get("write_boundary_ok") is True)
        ok(f"boundary.speech_false.{sid}", b.get("speech_allowed") is False)
        ok(f"boundary.action_false.{sid}", b.get("action_allowed") is False)

    ok("next_phase.recommended", next_phase_recommendation.get("recommended_next_phase") == NEXT_PHASE)
    ok("next_phase.final_decision", next_phase_recommendation.get("final_decision") == FINAL_DECISION)
    ok("debt.post_dryrun_review", governance_debt_register.get("post_dryrun_review_required_next") is True)

    for report_name, report in (("no_runtime", no_runtime_boundary_report), ("no_write", no_write_boundary_report)):
        ok(f"{report_name}.boundary_ok", report.get("boundary_ok") is True)
        ok(f"{report_name}.violations_empty", report.get("violations") == [])
        for flag in (
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
            "task_state_committed_now",
            "navigation_action_triggered",
            "world_model_written",
            "memory_written",
            "library_written",
            "fact_written",
        ):
            ok(f"{report_name}.{flag}_false", report.get(flag) is False)
        for flag in ("no_runtime_executed", "no_new_runtime_enabled"):
            ok(f"{report_name}.{flag}_true", report.get(flag) is True)

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
        "final_decision": FINAL_DECISION if verdict == "GO" else "CROSSING_DECISION_DRYRUN_VERIFIER_FAILED",
        "recommended_next_phase": NEXT_PHASE if verdict == "GO" else PHASE_ID,
        "failed_checks": failed[:20],
        "checks": checks,
    }
    report_path = root / "verifier_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

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
